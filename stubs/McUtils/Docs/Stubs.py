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
from ..Formatters import TemplateHandler
__all__ = ['StubSummaryBuilder']

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
    'Real access pattern: StubSummaryBuilder.<AttrName> (7 class attributes, e.g. StubSummaryBuilder.DATA_SIDECAR_THRESHOLD == 400). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:'
    _MEMBERS = {'DATA_SIDECAR_THRESHOLD': 400, 'SUMMARIES_DIRNAME': 'summaries', 'INDEX_FILENAME': 'index.md', 'LLM_README_FILENAME': 'LLM.md', 'INIT_FILENAME': '__init__.py', 'PACKAGE_SUMMARY_FILENAME_TEMPLATE': '{package_name}.md', 'SIDECAR_MODULE_NAME': '_registry_data'}
    SIDECAR_JSON_FILENAME = SIDECAR_MODULE_NAME + '.json'
    SIDECAR_LOADER_FILENAME = SIDECAR_MODULE_NAME + '.py'
    SIDECAR_LOADER_FUNC_NAME = '_load_registry_data'
    DEPENDENCY_GRAPH_FILENAME = 'dependency_graph.json'
    STDLIB_BLACKLIST_PACKAGES = frozenset(getattr(sys, 'stdlib_module_names', ())) | frozenset({'builtins'})
    COMMON_THIRD_PARTY_BLACKLIST_PACKAGES = frozenset(TemplateHandler.blacklist_packages)
    DEFAULT_DEPENDENCY_BLACKLIST = STDLIB_BLACKLIST_PACKAGES | COMMON_THIRD_PARTY_BLACKLIST_PACKAGES
    "Real access pattern: StubSummaryBuilder.<AttrName> (30 class attributes, e.g. StubSummaryBuilder.TRUNCATION_MARKER == '*(truncated — see stub for full docstring)*'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"
    _MEMBERS = {'TRUNCATION_MARKER': '*(truncated — see stub for full docstring)*', 'ENUM_ACCESS_NOTE_TEMPLATE': 'Real access pattern: {cname}.<MemberName> (this is an enum with {n_members} members, e.g. {cname}.{member_name} == {member_value}). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:', 'CLASS_ATTR_ACCESS_NOTE_TEMPLATE': 'Real access pattern: {cname}.<AttrName> ({n_members} class attributes, e.g. {cname}.{member_name} == {member_value}). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:', 'MODULE_SCALAR_ACCESS_NOTE_TEMPLATE': 'Real access pattern: bare module-level names (e.g. {member_name} == {member_value}), not a dict lookup. {n_members} names collapsed below purely for compactness:', 'EXTERNALIZED_DATA_NOTE_TEMPLATE': '{name} data externalized to {sidecar_json_filename} ({key_description})', 'OMITTED_DATA_NOTE_TEMPLATE': '{name} data omitted from this build ({key_description})', 'DESCRIBE_DICT_SMALL_TEMPLATE': '{n} keys: {keys!r}', 'DESCRIBE_DICT_LARGE_TEMPLATE': '{n} keys, first {max_listed}: {sample!r} ... and {remaining} more', 'DESCRIBE_LIST_SMALL_TEMPLATE': '{n} items: {items!r}', 'DESCRIBE_LIST_LARGE_TEMPLATE': '{n} items of type {elem_type}, first {sample_n}: {sample!r} ... and {remaining} more', 'DESCRIBE_SCALAR_TEMPLATE': 'a single {type_name} value', 'SIDECAR_LOADER_TEMPLATE': '"""Auto-generated loader for data externalized from stubbed modules (see StubSummaryBuilder.py)."""\nimport json, os\n_DATA_PATH = os.path.join(os.path.dirname(__file__), {sidecar_json_filename!r})\nwith open(_DATA_PATH, \'r\', encoding=\'utf-8\') as _f:\n    _DATA = json.load(_f)\n\ndef {loader_func_name}(key):\n    return _DATA[key]\n', 'INDEX_HEADER_TEMPLATE': '# {root_module_name} -- stub/summary index\n', 'INDEX_INTRO_TEMPLATE': "Read this file first to find the right package, then open that package's summary for its classes/functions, then the stub file only when you need the exact calling convention.\n", 'INDEX_ENTRY_TEMPLATE': '- **{pkg_name}** -- summary: `{rel_summary}` ({n_sections} modules) | stubs: `{rel_stub}` ({stub_bytes:,} bytes, {pct:.0f}% of source)', 'SIDECAR_PRESENT_NOTE_TEMPLATE': 'The real values live in `{sidecar_json_filename}` at the root of this directory (see `{sidecar_loader_filename}` for the loader function each affected stub imports).', 'SIDECAR_ABSENT_NOTE': 'The real values are NOT included anywhere in this directory at all -- only their keys/shape. If you need an actual value, say so rather than guessing one.', 'DEPENDENCY_GRAPH_NOTE_TEMPLATE': '`{dependency_graph_filename}` (at the root of this directory) maps which packages, classes, methods, and functions depend on which others -- both within `{root}` and on external packages (stdlib and a handful of very common third-party packages are excluded as noise). Use it to trace connections between parts of the codebase before writing an example that spans more than one package, or to find everything that uses a particular class or method. Resolution is best-effort static analysis, refined by live introspection where possible -- treat it as a strong hint, not a guarantee, especially for dynamic or conditional imports.', 'LLM_README_TEMPLATE': '# {root} -- how to use this directory\n\nThis is a **compressed, LLM-oriented reference** for the `{root}` codebase,\ngenerated from its real source. It is NOT the library itself: nothing here\nis meant to be imported or run as the real package. Use it to find out what\nexists and how to call it correctly, then write code against the real\n`{root}` package -- not against this directory.\n\n## Read in this order\n\n1. **`summaries/index.md`** -- one line per top-level package: what it\'s\n   for, how many modules it has, and where its summary/stubs live. Start\n   here to pick the right package.\n2. **`summaries/<package>.md`** -- every public class/function/method in\n   that package, with its exact call signature (parameter names and\n   defaults, no type annotations) and a short one-line purpose. This is\n   usually enough to write a correct call or import.\n3. **`{root}/<package>/<module>.py`** -- the full stub for one module:\n   real signatures, real docstrings (see caveats below), nothing\n   abbreviated further. Open this when the summary line isn\'t enough --\n   you need the full docstring, an edge case, or something the summary\n   truncated.\n\nDo not skip straight to step 3 for everything -- the summaries exist so you\nusually don\'t have to.\n\n## What\'s real vs. placeholder in the stub files\n\n- **Signatures** (parameter names, defaults, `*args`/`**kwargs`) are exact\n  copies of the real source.\n- **Docstrings** are the real docstrings. Class docstrings are capped at\n  their first paragraph (truncated ones are marked -- see "Compression\n  tricks" below); everything else is complete.\n- **Function/method bodies are placeholders** (`...`). They carry no\n  information about real behavior, return values, or edge cases -- never\n  infer runtime behavior from a stub body. The docstring is the only\n  source of behavioral information here; if it doesn\'t say, this\n  directory doesn\'t know either.\n- **`__all__`** (however it\'s constructed in the real source -- plain\n  assignment, `+=` accumulation, etc.) is preserved exactly, so each\n  stubbed module\'s real export list is accurate.\n\n## Compression tricks -- how to read them correctly\n\nThese exist purely to cut size; none of them drop information, but\nmisreading the compact form as the real API would be actively wrong:\n\n- **Enum-style / flat constant runs.** A class with many one-line members\n  (e.g. an `enum.Enum` with dozens of values) is collapsed into a single\n  `_MEMBERS = {{...}}` dict, immediately preceded by a comment stating the\n  REAL access pattern, e.g. `SomeEnum.Primary`, not\n  `SomeEnum._MEMBERS[\'Primary\']`. **Always follow that comment\'s stated\n  access pattern** -- the dict is a compact data table, not the calling\n  convention.\n- **Large literal data** (big lookup tables, constant dictionaries). When\n  a top-level literal is large, its value is replaced with a comment\n  describing its keys/shape (e.g. `1069 keys: [\'Hydrogen1\', \'Hydrogen2\', ...]`)\n  so you know what\'s queryable without the full payload inflating this\n  directory. {sidecar_note}\n- **Truncated class docstrings** end with the marker\n  `{truncation_marker}`. There is genuinely more\n  text in the real source that isn\'t reproduced anywhere in this\n  directory -- if the missing part matters, say you don\'t have it rather\n  than guessing at what follows.\n\n## Cross-package dependencies\n\n{dependency_graph_note}\n\n## Freshness\n\nThis is a point-in-time snapshot. It can drift out of date relative to the\nreal `{root}` source. If you need current, authoritative behavior (not\njust "does this function/class exist and roughly how do I call it"),\nverify against the real source rather than treating this directory as\nground truth.\n', 'SUMMARY_HEADER_TEMPLATE': '{n_packages} top-level packages processed under {out_dir!r}.', 'SUMMARY_SOURCE_LINE_TEMPLATE': '  source:     {n:,} bytes', 'SUMMARY_STUB_LINE_TEMPLATE': '  stubs:      {n:,} bytes ({pct:.1f}% of source)', 'SUMMARY_SUMMARY_LINE_TEMPLATE': '  summaries:  {n:,} bytes ({pct:.1f}% of source)', 'SUMMARY_SIDECAR_LINE_TEMPLATE': '  sidecar:    {n:,} bytes', 'SYNTAX_ERROR_WARNING_TEMPLATE': '[WARN] syntax error, copying as-is: {rel_path}: {error}', 'IMPORT_FALLBACK_INFO_TEMPLATE': '[INFO] real import of {root_module_name!r} failed ({error}); falling back to static __all__ parsing.', 'NO_PACKAGES_DISCOVERED_ERROR': 'No packages discovered yet -- call discover_top_level_packages(root_module_name) first, or pass root_module_name to generate().', 'PACKAGE_NOT_FOUND_ERROR_TEMPLATE': '{package_name!r} not found among discovered top-level packages: {available}', 'NO_TOP_LEVEL_PACKAGES_ERROR_TEMPLATE': 'No top-level packages discovered for {root_module_name!r} -- check that its __init__.py defines/builds __all__.', 'ROOT_DIR_NOT_FOUND_ERROR': "Could not locate the root module's source directory -- set root_src_dir explicitly."}

    def __init__(self, root_src_dir=None, out_dir='stubs', max_doc_len=800, min_words=5, write_sidecar_file=False, verbose=False):
        ...

    @property
    def root_module_name(self):
        ...

    @property
    def resolved_root_dir(self):
        ...

    @property
    def packages(self):
        ...

    @property
    def sidecar(self):
        ...

    @property
    def report(self):
        ...

    @property
    def dynamic_mode(self):
        ...

    @property
    def dependency_graph(self):
        ...

    def _is_scalar_assign(self, node):
        ...

    def collapse_scalar_assign_runs(self, body, min_group=6, context=None):
        ...

    def is_collapsed_registry(self, node):
        ...

    def _describe_keys(self, value, max_listed=40):
        ...

    def externalize_large_literal(self, node, module_key):
        ...

    def is_simple_assign(self, node, max_len=120):
        ...

    def is_all_operation(self, node):
        """True for any statement that assigns to, augments, or mutates
        `__all__` -- `__all__ = [...]`, `__all__ += [...]`,
        `__all__: list = [...]`, `__all__.append(...)`,
        `__all__.extend(...)`, etc. These must ALWAYS be kept verbatim
        and in their original relative order in the stub: dropping any
        one of them (as AugAssign lines silently were before this
        check existed) leaves `__all__` wrong at import time, which
        breaks the source tree for anything that relies on it --
        including this tool's own `discover_top_level_packages`."""
        ...

    def _is_all_only_import(self, node):
        """True for `from .X import __all__` / `from .X import __all__ as
        _all` -- an import whose ONLY purpose is __all__-construction
        bookkeeping (as opposed to `from .X import *`, which actually
        brings real names into the namespace and must always be kept
        regardless of dynamic/static mode)."""
        ...

    def _bake_all_node(self, names):
        """Build a single `__all__ = [...]` literal assignment from an
        already-resolved list of names."""
        ...

    def _dotted_module_name(self, package_name, rel_path=None):
        """Map a stub's (package_name, rel_path-within-that-package) back
        to the real dotted import path, e.g. ("Data", "CommonData.py")
        -> "McUtils.Data.CommonData", ("Data", "__init__.py") ->
        "McUtils.Data", (package_name, None) -> "McUtils.Data" (the
        package itself, e.g. when it's stubbed from a single .py file)."""
        ...

    def resolve_dynamic_all(self, package_name, rel_path=None):
        """If we're in dynamic_mode (the root module was really
        importable), look up this specific module's real, fully-resolved
        `__all__` -- so the stub can bake in the exact final result
        instead of copying the source's accumulation logic.

        Deliberately a PASSIVE `sys.modules` lookup, not a forcing
        `importlib.import_module` call: the one real import already done
        in `discover_top_level_packages` naturally cascades and loads
        every submodule the package actually uses (via its own `from .X
        import *` chains). We only bake __all__ for modules that showed
        up in memory as a result of that -- we never trigger an
        additional import of our own, so we can't accidentally force-load
        (and pay the cost/risk of) some module the package itself never
        needed. Returns None if dynamic_mode is off, the module was
        never loaded, or it has no __all__ -- the stub then falls back
        to preserving whatever __all__ operations exist in its own
        source, verbatim."""
        ...

    def _flatten_attribute_chain(self, node):
        """For `a.b.c`, return ('a', ['b', 'c']). Returns (None, []) if
        the chain doesn't bottom out in a plain Name (e.g. it starts
        with a call or subscript)."""
        ...

    def _dep_top_level_label(self, origin):
        """The blacklist-checkable label for a resolved dotted origin:
        the sibling top-level package name for internal (root_module_name-
        prefixed) origins (e.g. 'McUtils.Numputils.VectorOps.norm' ->
        'Numputils'), or the external package name otherwise (e.g.
        'numpy.linalg.norm' -> 'numpy')."""
        ...

    def _build_static_import_map(self, tree, current_package_dotted):
        """Map local names bound by import statements to a best-guess
        fully-qualified dotted origin, purely from the import statement
        text (relative imports resolved using current_package_dotted).
        Wildcard imports (`from .X import *`) can't be resolved this way
        -- individual names they bind are only recoverable via live
        introspection (see resolve_name in record_module_dependencies)."""
        ...

    def record_module_dependencies(self, source, package_name, rel_path=None):
        """Parse the ORIGINAL (pre-stub) source of one module and record,
        into self.dependency_graph, which packages/classes/methods/
        functions it references from other packages. Prefers live
        introspection (when dynamic_mode has the module loaded, via the
        same passive sys.modules lookup used for __all__ baking) over
        the static import map, since live introspection correctly
        resolves re-export chains like `from .X import *` that static
        parsing can't attribute to individual names. Silently returns
        (records nothing) on a syntax error -- dependency tracking is a
        best-effort bonus, not something that should block stubbing."""
        ...

    def write_dependency_graph(self):
        """Write dependency_graph.json at the root of out_dir. See
        record_module_dependencies for how entries are determined."""
        ...

    def stub_function(self, node):
        ...

    def stub_class(self, node):
        ...

    def stub_module(self, source, module_key, dynamic_all=None):
        ...

    def stub_package(self, src_dir, out_dir, package_name=None, keep_full=None):
        ...

    def write_sidecar_files(self):
        ...

    def first_line(self, docstring, max_len=100):
        ...

    def class_doc_summary(self, full_doc):
        ...

    def render_params(self, args, skip_first=False):
        ...

    def _decorator_names(self, node):
        ...

    def _signature_for(self, node, in_class=False):
        ...

    def summarize_class(self, node, indent='  '):
        ...

    def summarize_module(self, path, rel_path):
        ...

    def build_package_summary(self, src_dir, out_file):
        ...

    def _static_all_from_init(self, init_path):
        ...

    def discover_top_level_packages(self, root_module_name, try_dynamic=True, src_dir=None):
        ...

    class ModuleData:

        def __init__(self, parent, module_name, module_dir, packages, dynamic_mode):
            ...

        def __enter__(self):
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...

    def generate(self, package_name, root_module_name=None, update_current=False):
        ...

    def generate_all(self, root_module_name):
        ...

    def write_llm_readme(self):
        """Write LLM.md at the root of out_dir: an operating manual for
        an LLM consuming this directory -- navigation order, what's real
        vs. placeholder, and how to correctly read each of the lossy-
        looking-but-actually-lossless compression tricks used in the
        stubs (enum/constant-run collapsing, externalized data). This
        matters because misreading those tricks (e.g. treating a
        collapsed `_MEMBERS` dict as the real access pattern) would
        actively mislead an LLM rather than just under-inform it."""
        ...

    def finalize(self):
        ...

    def write_index(self):
        ...