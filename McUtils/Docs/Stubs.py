"""
StubSummaryBuilder
===================
Self-contained toolkit that turns a Python package into two LLM-friendly
artifacts, written under an output directory (default `stubs/`):

  1. **Stubs** -- per-module files with real signatures and full
     docstrings, but with boilerplate sibling classes, enum-style member
     runs, and large literal data tables collapsed into compact,
     information-preserving forms.

  2. **Summaries** -- one compact per-package "API index" file per
     top-level package (signatures + short descriptions only, no full
     docstrings beyond a capped class blurb), plus a root `index.md`
     that ties them together into a navigable graph: an LLM reads
     `index.md` to find the right package, that package's summary to
     find the right class/function, and the stub file only when it
     needs the exact calling convention.

Top-level packages are discovered by statically (or dynamically, if
importable) reading the root module's `__all__`.

Everything lives on the `StubSummaryBuilder` class so any piece --
discovery, stubbing, summarizing -- can be overridden via subclassing.
"""
import ast
import importlib
import importlib.util
import json
import os
import sys

from .. import Devutils as dev

__all__ = [
    "StubSummaryBuilder"
]


class StubSummaryBuilder:
    """
    Parameters
    ----------
    root_src_dir : str or None
        Path to the root module's source directory (the folder
        containing its __init__.py). If None, the root module must be
        importable and its location is resolved from that import.
    out_dir : str
        Output directory. Stub trees are written to
        `<out_dir>/<root_module_name>/<pkg_name>/...`, summaries to
        `<out_dir>/summaries/<pkg_name>.md`, and the graph index to
        `<out_dir>/summaries/index.md`.
    max_doc_len : int
        Cap on class docstrings in summaries: first paragraph or this
        many characters, whichever comes first.
    min_words : int
        For one-line descriptions: skip docstring lines with this many
        words or fewer (filters out short placeholder lines), using the
        first line that exceeds it.
    write_sidecar_file : bool
        If True, externalized large literals are written to a shared
        `_registry_data.json` (+ loader module) under out_dir, and stubs
        get a loader call to fetch them. If False (default), only a
        key/shape summary comment is left in the stub and the raw data
        is dropped entirely.

    Overridable methods
    --------------------
    Every step is a plain instance method, so a subclass can override
    any piece of the pipeline, e.g.:

        class MyBuilder(StubSummaryBuilder):
            def discover_top_level_packages(self, root_module_name):
                # custom discovery logic, e.g. a hardcoded package list
                ...

            def build_package_summary(self, src_dir, out_file):
                # custom summary format
                ...
    """

    DATA_SIDECAR_THRESHOLD = 400  # rendered length above which we externalize
                                   # a literal assignment instead of dropping it

    def __init__(self, root_src_dir=None, out_dir="stubs",
                 max_doc_len=800, min_words=5, write_sidecar_file=False,
                 verbose=False):
        self.root_src_dir = root_src_dir
        self.out_dir = out_dir
        self.max_doc_len = max_doc_len
        self.min_words = min_words
        self.write_sidecar_file = write_sidecar_file
        self._module_stack = []
        self._current_module = None
        self.verbose = verbose

    @property
    def root_module_name(self):
        return self._current_module.root_module_name
    @property
    def resolved_root_dir(self):
        return self._current_module.resolved_root_dir
    @property
    def packages(self):
        return self._current_module.packages
    @property
    def sidecar(self):
        return self._current_module.sidecar
    @property
    def report(self):
        return self._current_module.report

    # ==================================================================
    # Section 1: stub generation
    # ==================================================================

    def _is_scalar_assign(self, node):
        return (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Constant))

    def collapse_scalar_assign_runs(self, body, min_group=6, context=None):
        out = []
        i = 0
        while i < len(body):
            if self._is_scalar_assign(body[i]):
                j = i
                run = []
                while j < len(body) and self._is_scalar_assign(body[j]):
                    run.append(body[j])
                    j += 1
                if len(run) >= min_group:
                    keys = [ast.Constant(value=n.targets[0].id) for n in run]
                    values = [n.value for n in run]

                    if context and context.get("kind") == "class":
                        cname = context["name"]
                        bases = context.get("bases") or []
                        base_strs = [ast.unparse(b) for b in bases]
                        is_enum = any("enum" in b.lower() or "flag" in b.lower() for b in base_strs)
                        if is_enum:
                            note = (
                                f"Real access pattern: {cname}.<MemberName> (this is an "
                                f"enum with {len(run)} members, e.g. {cname}.{run[0].targets[0].id} "
                                f"== {ast.unparse(run[0].value)}). Collapsed into a dict below "
                                f"purely for compactness -- do not index it as a dict in real code:"
                            )
                        else:
                            note = (
                                f"Real access pattern: {cname}.<AttrName> ({len(run)} class "
                                f"attributes, e.g. {cname}.{run[0].targets[0].id} == "
                                f"{ast.unparse(run[0].value)}). Collapsed into a dict below "
                                f"purely for compactness -- do not index it as a dict in real code:"
                            )
                    else:
                        note = (
                            f"Real access pattern: bare module-level names (e.g. "
                            f"{run[0].targets[0].id} == {ast.unparse(run[0].value)}), not a "
                            f"dict lookup. {len(run)} names collapsed below purely for "
                            f"compactness:"
                        )
                    out.append(ast.Expr(value=ast.Constant(value=note)))
                    out.append(ast.Assign(
                        targets=[ast.Name(id="_MEMBERS", ctx=ast.Store())],
                        value=ast.Dict(keys=keys, values=values)))
                    i = j
                    continue
                else:
                    out.extend(run)
                    i = j
                    continue
            out.append(body[i])
            i += 1
        return out

    def is_collapsed_registry(self, node):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, str):
            return True
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name == "_MEMBERS" or name.endswith("_REGISTRY"):
                return True
        return False

    def _describe_keys(self, value, max_listed=40):
        if isinstance(value, dict):
            keys = list(value.keys())
            if len(keys) <= max_listed:
                return f"{len(keys)} keys: {keys!r}"
            sample = keys[:max_listed]
            return f"{len(keys)} keys, first {max_listed}: {sample!r} ... and {len(keys) - max_listed} more"
        elif isinstance(value, (list, tuple)):
            n = len(value)
            if n <= max_listed:
                return f"{n} items: {list(value)!r}"
            sample = value[:5]
            elem_type = type(value[0]).__name__ if value else "unknown"
            return f"{n} items of type {elem_type}, first 5: {list(sample)!r} ... and {n - 5} more"
        else:
            return f"a single {type(value).__name__} value"

    def externalize_large_literal(self, node, module_key):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1 \
                or not isinstance(node.targets[0], ast.Name):
            return None
        name = node.targets[0].id
        if name.startswith("__") and name.endswith("__"):
            return None
        try:
            rendered = ast.unparse(node.value)
        except Exception:
            return None
        if len(rendered) < self.DATA_SIDECAR_THRESHOLD:
            return None
        try:
            value = ast.literal_eval(node.value)
            json.dumps(value)
        except Exception:
            return None

        data_key = f"{module_key}::{name}"
        self.sidecar[data_key] = value

        if self.write_sidecar_file:
            note = f"{name} data externalized to _registry_data.json ({self._describe_keys(value)})"
            return [ast.Expr(value=ast.Constant(value=note)),
                    ast.parse(f"{name} = _load_registry_data({data_key!r})").body[0]]
        else:
            note = f"{name} data omitted from this build ({self._describe_keys(value)})"
            return [ast.Expr(value=ast.Constant(value=note))]

    def is_simple_assign(self, node, max_len=120):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            return False
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name.startswith("__") and name.endswith("__"):
                return True
        value = node.value
        if value is None:
            return True
        try:
            rendered = ast.unparse(value)
        except Exception:
            return False
        return len(rendered) < max_len

    def stub_function(self, node):
        docstring = ast.get_docstring(node, clean=False)
        new_body = []
        if docstring is not None:
            new_body.append(ast.Expr(value=ast.Constant(value=docstring)))
        new_body.append(ast.Expr(value=ast.Constant(value=Ellipsis)))
        node.body = new_body
        return node

    def stub_class(self, node):
        docstring = ast.get_docstring(node, clean=False)
        new_body = []
        if docstring is not None:
            new_body.append(ast.Expr(value=ast.Constant(value=docstring)))

        body = list(node.body)
        if docstring is not None and body and isinstance(body[0], ast.Expr) \
                and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            body = body[1:]

        body = self.collapse_scalar_assign_runs(
            body, context={"kind": "class", "name": node.name, "bases": node.bases})

        for child in body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                new_body.append(self.stub_function(child))
            elif isinstance(child, ast.ClassDef):
                new_body.append(self.stub_class(child))
            elif self.is_simple_assign(child):
                new_body.append(child)
            elif self.is_collapsed_registry(child):
                new_body.append(child)

        if not new_body:
            new_body.append(ast.Expr(value=ast.Constant(value=Ellipsis)))
        node.body = new_body
        return node

    def stub_module(self, source, module_key):
        tree = ast.parse(source)
        new_body = []

        module_doc = ast.get_docstring(tree, clean=False)
        start = 0
        if module_doc is not None:
            new_body.append(ast.Expr(value=ast.Constant(value=module_doc)))
            start = 1

        body = tree.body[start:]
        body = self.collapse_scalar_assign_runs(body)
        used_sidecar = False

        for node in body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                new_body.append(node)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                new_body.append(self.stub_function(node))
            elif isinstance(node, ast.ClassDef):
                new_body.append(self.stub_class(node))
            elif self.is_simple_assign(node):
                new_body.append(node)
            elif self.is_collapsed_registry(node):
                new_body.append(node)
            else:
                replacement = self.externalize_large_literal(node, module_key)
                if replacement is not None:
                    new_body.extend(replacement)
                    used_sidecar = used_sidecar or self.write_sidecar_file

        if used_sidecar:
            new_body.insert(start, ast.ImportFrom(
                module="_registry_data", names=[ast.alias(name="_load_registry_data")], level=0))

        tree.body = new_body
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def stub_package(self, src_dir, out_dir, keep_full=None):
        keep_full = set(keep_full or [])
        stats = []

        for root, _, files in os.walk(src_dir):
            for fname in files:
                if not fname.endswith(".py"):
                    continue
                src_path = os.path.join(root, fname)
                rel_path = os.path.relpath(src_path, src_dir)
                out_path = os.path.join(out_dir, rel_path)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)

                with open(src_path, "r", encoding="utf-8", errors="replace") as f:
                    source = f.read()
                orig_size = len(source)

                if rel_path in keep_full:
                    stubbed = source
                else:
                    try:
                        stubbed = self.stub_module(source, rel_path)
                    except SyntaxError as e:
                        print(f"[WARN] syntax error, copying as-is: {rel_path}: {e}", file=sys.stderr)
                        stubbed = source

                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(stubbed)
                stats.append((rel_path, orig_size, len(stubbed)))

        return stats

    def write_sidecar_files(self):
        if not self.sidecar or not self.write_sidecar_file:
            return 0
        data_path = os.path.join(self.out_dir, "_registry_data.json")
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(self.sidecar, f, separators=(",", ":"))

        loader_path = os.path.join(self.out_dir, "_registry_data.py")
        with open(loader_path, "w", encoding="utf-8") as f:
            f.write(
                '"""Auto-generated loader for data externalized from stubbed '
                'modules (see StubSummaryBuilder.py)."""\n'
                "import json, os\n"
                "_DATA_PATH = os.path.join(os.path.dirname(__file__), '_registry_data.json')\n"
                "with open(_DATA_PATH, 'r', encoding='utf-8') as _f:\n"
                "    _DATA = json.load(_f)\n\n"
                "def _load_registry_data(key):\n"
                "    return _DATA[key]\n"
            )
        return os.path.getsize(data_path)

    # ==================================================================
    # Section 2: API summary generation
    # ==================================================================

    def first_line(self, docstring, max_len=100):
        if not docstring:
            return None
        lines = [l.strip() for l in docstring.strip().split("\n") if l.strip()]
        if not lines:
            return None

        chosen = None
        for l in lines:
            if len(l.split()) > self.min_words:
                chosen = l
                break
        if chosen is None:
            chosen = lines[0]

        line = chosen
        for sep in (". ", ".\n"):
            idx = line.find(sep)
            if 0 < idx < max_len:
                line = line[:idx + 1]
                break
        if len(line) > max_len:
            line = line[:max_len - 1].rstrip() + "…"
        return line

    def class_doc_summary(self, full_doc):
        if not full_doc:
            return None, False
        text = full_doc.strip("\n")
        paragraphs = text.split("\n\n")
        first_para = paragraphs[0].strip()
        truncated = len(paragraphs) > 1
        if len(first_para) > self.max_doc_len:
            first_para = first_para[:self.max_doc_len].rstrip() + "…"
            truncated = True
        return first_para, truncated

    def render_params(self, args, skip_first=False):
        parts = []
        posonly = list(getattr(args, "posonlyargs", []))
        pos = posonly + list(args.args)
        if skip_first and pos:
            pos = pos[1:]
            posonly = posonly[1:] if posonly else posonly

        defaults = list(args.defaults)
        num_no_default = len(pos) - len(defaults)
        for i, a in enumerate(pos):
            if posonly and i == len(posonly):
                parts.append("/")
            if i >= num_no_default:
                d = defaults[i - num_no_default]
                try:
                    parts.append(f"{a.arg}={ast.unparse(d)}")
                except Exception:
                    parts.append(f"{a.arg}=...")
            else:
                parts.append(a.arg)

        if args.vararg:
            parts.append(f"*{args.vararg.arg}")
        elif args.kwonlyargs:
            parts.append("*")

        for a, d in zip(args.kwonlyargs, args.kw_defaults):
            if d is not None:
                try:
                    parts.append(f"{a.arg}={ast.unparse(d)}")
                except Exception:
                    parts.append(f"{a.arg}=...")
            else:
                parts.append(a.arg)

        if args.kwarg:
            parts.append(f"**{args.kwarg.arg}")

        return ", ".join(parts)

    def _decorator_names(self, node):
        names = []
        for d in node.decorator_list:
            try:
                names.append(ast.unparse(d))
            except Exception:
                pass
        return names

    def _signature_for(self, node, in_class=False):
        decs = self._decorator_names(node)
        skip_first = False
        if in_class and "staticmethod" not in decs:
            first_arg = node.args.args[0].arg if node.args.args else None
            if "classmethod" in decs or first_arg in ("cls", "self"):
                skip_first = True
        params = self.render_params(node.args, skip_first=skip_first)
        return f"{node.name}({params})"

    def summarize_class(self, node, indent="  "):
        lines = []
        full_doc = ast.get_docstring(node)
        bases = ", ".join(ast.unparse(b) for b in node.bases) if node.bases else ""
        header = f"{indent}- **class `{node.name}`**"
        if bases:
            header += f" ({bases})"
        lines.append(header)

        doc_text, truncated = self.class_doc_summary(full_doc)
        if doc_text:
            for doc_line in doc_text.split("\n"):
                lines.append(f"{indent}  > {doc_line}".rstrip())
            if truncated:
                lines.append(f"{indent}  > *(truncated — see stub for full docstring)*")

        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if child.name.startswith("_") and child.name != "__init__":
                    continue
                sig = self._signature_for(child, in_class=True)
                entry = f"{indent}  - `{sig}`"
                if child.name != "__init__":
                    cdoc = self.first_line(ast.get_docstring(child))
                    if cdoc:
                        entry += f" — {cdoc}"
                lines.append(entry)
            elif isinstance(child, ast.ClassDef):
                lines.extend(self.summarize_class(child, indent=indent + "  "))
        return lines

    def summarize_module(self, path, rel_path):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            source = f.read()
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return None

        mod_doc = self.first_line(ast.get_docstring(tree))
        lines = [f"### `{rel_path}`" + (f" — {mod_doc}" if mod_doc else "")]

        body_lines = []
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                body_lines.extend(self.summarize_class(node))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("_"):
                    continue
                doc = self.first_line(ast.get_docstring(node))
                sig = self._signature_for(node, in_class=False)
                entry = f"- `{sig}`"
                if doc:
                    entry += f" — {doc}"
                body_lines.append(entry)

        if not body_lines:
            return None
        lines.extend(body_lines)
        return "\n".join(lines)

    def build_package_summary(self, src_dir, out_file):
        sections = []
        for root, _, files in sorted(os.walk(src_dir)):
            for fname in sorted(files):
                if not fname.endswith(".py"):
                    continue
                path = os.path.join(root, fname)
                rel = os.path.relpath(path, src_dir)
                section = self.summarize_module(path, rel)
                if section:
                    sections.append(section)

        with open(out_file, "w", encoding="utf-8") as f:
            f.write("\n\n".join(sections))
        return len(sections)

    # ==================================================================
    # Section 3: top-level package discovery via __all__
    # ==================================================================

    def _static_all_from_init(self, init_path):
        try:
            with open(init_path, "r", encoding="utf-8", errors="replace") as f:
                source = f.read()
            tree = ast.parse(source)
        except (OSError, SyntaxError):
            return None

        all_list = None
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                    and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "__all__":
                try:
                    all_list = list(ast.literal_eval(node.value))
                except Exception:
                    pass
            elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name) \
                    and node.target.id == "__all__" and isinstance(node.op, ast.Add):
                try:
                    addition = ast.literal_eval(node.value)
                    if all_list is None:
                        all_list = []
                    all_list.extend(addition)
                except Exception:
                    pass
        return all_list

    def discover_top_level_packages(self, root_module_name, src_dir=None):
        if src_dir is None:
            src_dir = self.root_src_dir
        resolved_root_dir = src_dir
        all_names = None

        if src_dir is None:
            src_dir = ''
        else:
            src_dir = os.path.dirname(src_dir)

        with dev.temporary_sys_path_insert(src_dir):
            try:
                module = importlib.import_module(root_module_name)
                all_names = list(getattr(module, "__all__", []) or [])
                resolved_root_dir = os.path.dirname(os.path.abspath(module.__file__))
            except (ImportError,AttributeError) as e:
                print(f"[INFO] real import of {root_module_name!r} failed ({e}); "
                      f"falling back to static __all__ parsing.", file=sys.stderr)

        if resolved_root_dir is None:
            raise ValueError(
                "Could not locate the root module's source directory -- "
                "set root_src_dir explicitly.")

        if all_names is None:
            init_path = os.path.join(resolved_root_dir, "__init__.py")
            all_names = self._static_all_from_init(init_path) or []

        discovered = {}
        for name in all_names:
            pkg_dir = os.path.join(resolved_root_dir, name)
            pkg_file = os.path.join(resolved_root_dir, f"{name}.py")
            if os.path.isdir(pkg_dir) and os.path.isfile(os.path.join(pkg_dir, "__init__.py")):
                discovered[name] = pkg_dir
            elif os.path.isfile(pkg_file):
                discovered[name] = pkg_file

        return resolved_root_dir, discovered

    # ==================================================================
    # Section 4: orchestration
    # ==================================================================

    class ModuleData:
        def __init__(self, parent, module_name, module_dir, packages):
            self.parent = parent
            # populated by discover_top_level_packages()
            self.root_module_name, self.resolved_root_dir, self.packages = module_name, module_dir, packages

            # accumulated across generate() calls
            self.sidecar = {}
            self.report = {}

        def __enter__(self):
            self.parent._module_stack.append(self.parent._current_module)
            self.parent._current_module = self
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.parent._current_module = self.parent._module_stack.pop()


    def generate(self, package_name, root_module_name=None, update_current=False):
        if update_current or self._current_module is None:
            root_dir, packages = self.discover_top_level_packages(root_module_name)
            module_data = self.ModuleData(self, package_name, root_dir, packages)
        else:
            module_data = self._current_module
        with module_data:
            if not self.packages:
                raise ValueError(
                    "No packages discovered yet -- call discover_top_level_packages(root_module_name) "
                    "first, or pass root_module_name to generate().")
            if package_name not in self.packages:
                raise KeyError(
                    f"{package_name!r} not found among discovered top-level packages: "
                    f"{sorted(self.packages)}")

            pkg_src_path = self.packages[package_name]
            summaries_dir = os.path.join(self.out_dir, "summaries")
            os.makedirs(summaries_dir, exist_ok=True)

            pkg_stub_out = os.path.join(self.out_dir, self.root_module_name, package_name)
            pkg_summary_out = os.path.join(summaries_dir, f"{package_name}.md")

            if os.path.isdir(pkg_src_path):
                stats = self.stub_package(pkg_src_path, pkg_stub_out)
            else:
                os.makedirs(pkg_stub_out, exist_ok=True)
                with open(pkg_src_path, "r", encoding="utf-8", errors="replace") as f:
                    source = f.read()
                out_file = os.path.join(pkg_stub_out, os.path.basename(pkg_src_path))
                stubbed = self.stub_module(source, package_name)
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(stubbed)
                stats = [(os.path.basename(pkg_src_path), len(source), len(stubbed))]

            n_sections = self.build_package_summary(pkg_stub_out, pkg_summary_out)

            orig_total = sum(s[1] for s in stats)
            stub_total = sum(s[2] for s in stats)
            summary_size = os.path.getsize(pkg_summary_out)
            info = {
                "stub_dir": pkg_stub_out,
                "summary_file": pkg_summary_out,
                "orig_bytes": orig_total,
                "stub_bytes": stub_total,
                "summary_bytes": summary_size,
                "n_summary_sections": n_sections,
            }
        return info

    def generate_all(self, root_module_name):
        root_dir, packages = self.discover_top_level_packages(root_module_name)
        with self.ModuleData(self, root_module_name, root_dir, packages):
            if not self.packages:
                raise ValueError(
                    f"No top-level packages discovered for {root_module_name!r} -- "
                    f"check that its __init__.py defines/builds __all__.")

            for package_name in sorted(self.packages):
                info = self.generate(package_name)
                self.report[package_name] = info
            summary = self.finalize()
            info = self.report
        return info, summary

    def finalize(self):
        sidecar_size = self.write_sidecar_files()
        self.write_index()

        total_orig = sum(r["orig_bytes"] for r in self.report.values())
        total_stub = sum(r["stub_bytes"] for r in self.report.values())
        total_summary = sum(r["summary_bytes"] for r in self.report.values())
        if self.verbose:
            print(f"{len(self.report)} top-level packages processed under {self.out_dir!r}.")
            if total_orig:
                print(f"  source:     {total_orig:,} bytes")
                print(f"  stubs:      {total_stub:,} bytes ({100 * total_stub / total_orig:.1f}% of source)")
                print(f"  summaries:  {total_summary:,} bytes ({100 * total_summary / total_orig:.1f}% of source)")
            if self.write_sidecar_file:
                print(f"  sidecar:    {sidecar_size:,} bytes")
        summary = {
            'original_size': total_orig,
            'stub_size': total_stub,
            'sidecar_size': sidecar_size,
            'summary_size': total_summary
        }
        return summary

    def write_index(self):
        summaries_dir = os.path.join(self.out_dir, "summaries")
        os.makedirs(summaries_dir, exist_ok=True)
        lines = [
            f"# {self.root_module_name} -- stub/summary index\n",
            "Read this file first to find the right package, then open that "
            "package's summary for its classes/functions, then the stub file "
            "only when you need the exact calling convention.\n",
        ]
        for pkg_name, info in sorted(self.report.items()):
            rel_summary = os.path.relpath(info["summary_file"], self.out_dir)
            rel_stub = os.path.relpath(info["stub_dir"], self.out_dir)
            pct = (100 * info["stub_bytes"] / info["orig_bytes"]) if info["orig_bytes"] else 0
            lines.append(
                f"- **{pkg_name}** -- summary: `{rel_summary}` "
                f"({info['n_summary_sections']} modules) | stubs: `{rel_stub}` "
                f"({info['stub_bytes']:,} bytes, {pct:.0f}% of source)"
            )
        with open(os.path.join(summaries_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

# def main():
#     import argparse
#     ap = argparse.ArgumentParser(description=__doc__)
#     ap.add_argument("root_module_name", help="e.g. McUtils")
#     ap.add_argument("--src-dir", default=None,
#                      help="Path to the root module's source directory "
#                           "(the folder containing its __init__.py). If "
#                           "omitted, the module must be importable.")
#     ap.add_argument("--out-dir", default="stubs")
#     ap.add_argument("--max-doc-len", type=int, default=800)
#     ap.add_argument("--min-words", type=int, default=5)
#     ap.add_argument("--write-sidecar-file", action="store_true",
#                      help="Also write a raw _registry_data.json with the "
#                           "full externalized data (off by default -- key/"
#                           "shape summaries stay inline either way).")
#     args = ap.parse_args()
#
#     builder = StubSummaryBuilder(
#         root_src_dir=args.src_dir, out_dir=args.out_dir,
#         max_doc_len=args.max_doc_len, min_words=args.min_words,
#         write_sidecar_file=args.write_sidecar_file)
#     builder.generate_all(args.root_module_name)
