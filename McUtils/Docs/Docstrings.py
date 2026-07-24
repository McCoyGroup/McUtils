import abc
import ast
import dataclasses
import io
import os
import re
import tokenize
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .. import Devutils as dev

__all__ = [
    "DocstringParser",
    "DocstringWriter",
    "DocstringDialectHandler"
]


# --------------------------------------------------------------------------- #
# AST helpers
# --------------------------------------------------------------------------- #
def _iter_funcs(tree):
    """Yield (qualname, node) for every function/method, in source order."""
    out = []

    class V(ast.NodeVisitor):
        def __init__(self):
            self.stack = []

        def visit_ClassDef(self, n):
            self.stack.append(n.name)
            self.generic_visit(n)
            self.stack.pop()

        def _f(self, n):
            out.append((".".join(self.stack + [n.name]), n))
            self.stack.append(n.name)
            self.generic_visit(n)
            self.stack.pop()

        visit_FunctionDef = _f
        visit_AsyncFunctionDef = _f

    V().visit(tree)
    return out

def _header_end_line(lines, start_line):
    """1-based line where the def signature's closing ':' lives."""
    sub = "\n".join(lines[start_line - 1:])
    toks = tokenize.generate_tokens(io.StringIO(sub).readline)
    depth = 0
    opened = False
    for tok in toks:
        if tok.type == tokenize.OP:
            if tok.string in "([{":
                depth += 1
                opened = True
            elif tok.string in ")]}":
                depth -= 1
            elif tok.string == ":" and depth == 0 and opened:
                return start_line - 1 + tok.end[0]
    raise RuntimeError(f"couldn't find signature end from line {start_line}")

def _strip_docstrings(src):
    """Parse, drop every module/class/function docstring, return unparsed code."""
    tree = ast.parse(src)

    class R(ast.NodeTransformer):
        def _s(self, n):
            self.generic_visit(n)
            b = n.body
            if (
                b
                and isinstance(b[0], ast.Expr)
                and isinstance(getattr(b[0], "value", None), ast.Constant)
                and isinstance(b[0].value.value, str)
            ):
                n.body = b[1:] or [ast.Pass()]
            return n

        visit_FunctionDef = _s
        visit_AsyncFunctionDef = _s
        visit_ClassDef = _s
        visit_Module = _s

    return ast.unparse(ast.fix_missing_locations(R().visit(tree)))

def _has_docstring_node(node) -> bool:
    b0 = node.body[0]
    return (
        isinstance(b0, ast.Expr)
        and isinstance(getattr(b0, "value", None), ast.Constant)
        and isinstance(b0.value.value, str)
    )

def _signature_types(node) -> Dict[str, Any]:
    """Pull parameter/return annotations straight off the function signature."""
    info: Dict[str, Any] = {"params": {}, "returns": None}
    a = node.args
    all_args = (
        list(getattr(a, "posonlyargs", []))
        + list(a.args)
        + ([a.vararg] if a.vararg else [])
        + list(a.kwonlyargs)
        + ([a.kwarg] if a.kwarg else [])
    )
    for arg in all_args:
        if arg is None:
            continue
        ann = ast.unparse(arg.annotation) if arg.annotation is not None else None
        info["params"][arg.arg] = {"annotation": ann}
    if node.returns is not None:
        info["returns"] = ast.unparse(node.returns)
    return info

# --------------------------------------------------------------------------- #
# Shared text-parsing helpers (dialect-agnostic)
# --------------------------------------------------------------------------- #
_DOCTEST_RE = re.compile(
    r'(?:^|\n)([ \t]*>>>.*(?:\n(?!\s*\n)[ \t]*.*)*)', re.MULTILINE
)


def _split_intro(intro: str) -> Tuple[str, str]:
    """First paragraph -> short_description (collapsed to one line); rest -> details."""
    parts = intro.strip("\n").split("\n\n", 1)
    short = " ".join(parts[0].split())
    details = parts[1].strip() if len(parts) > 1 else ""
    return short, details


def _extract_doctest_examples(raw: str) -> List[str]:
    """Pull out ``>>> ...`` doctest blocks. Dialect-independent."""
    return [m.group(1).strip("\n") for m in _DOCTEST_RE.finditer(raw or "") if m.group(1).strip()]


def _blank_params(node: ast.AST) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Seed (params, returns) dicts straight from the signature, with no docs yet."""
    sig = _signature_types(node)
    params = {
        name: {"annotation": info["annotation"], "doc_type": "", "description": ""}
        for name, info in sig["params"].items()
    }
    returns = {"annotation": sig["returns"], "doc_type": "", "description": ""}
    return params, returns


# --------------------------------------------------------------------------- #
# Docstring dialects
# --------------------------------------------------------------------------- #
class DocstringDialectHandler(abc.ABC):
    """A pluggable docstring convention: parses raw text into the canonical
    ``DocstringData`` fields, and renders those fields back into text using
    the same convention.

    Subclasses register themselves (see ``DIALECTS`` below) so a file can mix
    conventions function-by-function and each one round-trips in its own
    style.
    """

    name: str = "base"

    @classmethod
    @abc.abstractmethod
    def sniff(cls, raw: str) -> bool:
        """Return True if `raw` looks like it was written in this dialect."""

    @abc.abstractmethod
    def extract(self, raw: str, node: ast.AST) -> Dict[str, Any]:
        """Parse `raw` (+ signature info from `node`) into the canonical dict:
        ``{"short_description", "details", "examples", "type_info"}``.
        """

    @abc.abstractmethod
    def render(self, data: "DocstringData") -> str:
        """Render a (possibly edited) ``DocstringData`` back into body text."""


class GoogleDialectHandler(DocstringDialectHandler):
    """Google-style: ``Args:`` / ``Returns:`` / ``Examples:`` sections."""

    name = "google"

    _SECTION_RE = re.compile(
        r'^(Args|Arguments|Parameters|Returns|Return|Yields|Yield|'
        r'Raises|Raise|Example|Examples|Note|Notes|Attributes|Attribute)\s*:\s*$',
        re.IGNORECASE,
    )
    _SNIFF_RE = re.compile(
        r'^[ \t]*(Args|Arguments|Parameters|Returns|Return|Yields|Yield|Raises|Raise)\s*:\s*$',
        re.IGNORECASE | re.MULTILINE,
    )
    _ARG_LINE_RE = re.compile(r'^(\s*)([\w\*]+)\s*(?:\(([^)]*)\))?\s*:\s*(.*)$')
    _RETURN_LINE_RE = re.compile(r'^\s*([\w\.\[\], \'"]+?)\s*:\s*(.+)$')

    @classmethod
    def sniff(cls, raw: str) -> bool:
        return bool(cls._SNIFF_RE.search(raw or ""))

    def _split_sections(self, text: str) -> Tuple[str, Dict[str, str]]:
        """Split a docstring body into (intro_text, {section_name: body_text})."""
        lines = text.split("\n")
        intro_lines: List[str] = []
        sections: Dict[str, List[str]] = {}
        current = None
        cur_lines: List[str] = []

        def flush():
            if current is not None:
                sections.setdefault(current, []).append("\n".join(cur_lines).strip("\n"))

        for line in lines:
            m = self._SECTION_RE.match(line.strip())
            if m:
                flush()
                current = m.group(1).lower()
                cur_lines = []
            elif current is None:
                intro_lines.append(line)
            else:
                cur_lines.append(line)
        flush()

        merged = {k: "\n\n".join(v).strip("\n") for k, v in sections.items()}
        return "\n".join(intro_lines).strip(), merged

    def _parse_args_section(self, text: str) -> Dict[str, Dict[str, str]]:
        """Parse an ``Args:`` body into {name: {doc_type, description}}."""
        result: Dict[str, Dict[str, str]] = {}
        current = None
        for raw_line in text.split("\n"):
            if not raw_line.strip():
                continue
            m = self._ARG_LINE_RE.match(raw_line)
            # A new "name (type): desc" entry is only at the section's own
            # indent level (a continuation line is indented deeper).
            if m and (current is None or len(m.group(1)) <= result.get(current, {}).get("_indent", 0)):
                indent, name, typ, desc = m.groups()
                name = name.rstrip("*")
                result[name] = {
                    "doc_type": (typ or "").strip(),
                    "description": desc.strip(),
                    "_indent": len(indent),
                }
                current = name
            elif current is not None:
                result[current]["description"] = (
                    result[current]["description"] + " " + raw_line.strip()
                ).strip()
        for v in result.values():
            v.pop("_indent", None)
        return result

    def _parse_return_section(self, text: str) -> Tuple[str, str]:
        """Split a ``Returns:`` body's leading ``type: `` prefix from its description."""
        text = text.strip()
        if not text:
            return "", ""
        first, _, rest = text.partition("\n")
        m = self._RETURN_LINE_RE.match(first)
        if m:
            doc_type, desc_first = m.group(1).strip(), m.group(2).strip()
            return doc_type, (desc_first + ("\n" + rest if rest else "")).strip()
        return "", text

    def _extract_examples(self, raw: str, sections: Dict[str, str]) -> List[str]:
        examples, seen = [], set()

        def norm(s):
            return "\n".join(l.strip() for l in s.strip().split("\n"))

        for key in ("example", "examples"):
            body = sections.get(key, "").strip()
            if body:
                examples.append(body)
                seen.add(norm(body))
        for block in _extract_doctest_examples(raw):
            if norm(block) not in seen:
                examples.append(block)
                seen.add(norm(block))
        return examples

    def extract(self, raw: str, node: ast.AST) -> Dict[str, Any]:
        intro, sections = self._split_sections(raw or "")
        short, details = _split_intro(intro)
        examples = self._extract_examples(raw or "", sections)

        params, returns = _blank_params(node)
        param_key = next((k for k in ("args", "arguments", "parameters") if k in sections), None)
        documented = self._parse_args_section(sections[param_key]) if param_key else {}
        for name, sig in params.items():
            doc = documented.get(name, {})
            sig["doc_type"] = doc.get("doc_type", "")
            sig["description"] = doc.get("description", "")
        # documented parameters that don't correspond to a real argument
        # (typos, stale docs) are kept too, so `analysis` / a human can flag them.
        for name, doc in documented.items():
            if name not in params:
                params[name] = {
                    "annotation": None,
                    "doc_type": doc.get("doc_type", ""),
                    "description": doc.get("description", ""),
                }

        ret_key = next((k for k in ("returns", "return") if k in sections), None)
        if ret_key:
            returns["doc_type"], returns["description"] = self._parse_return_section(sections[ret_key])

        return {
            "short_description": short,
            "details": details,
            "examples": examples,
            "type_info": {"params": params, "returns": returns},
        }

    def render(self, data: "DocstringData") -> str:
        parts = []
        if data.short_description:
            parts.append(data.short_description.strip())
        if data.details:
            parts.append(data.details.strip())

        params = data.type_info.get("params", {}) if data.type_info else {}
        param_lines = []
        for name, info in params.items():
            typ = (info.get("doc_type") or info.get("annotation") or "").strip()
            desc = (info.get("description") or "").strip()
            head = f"{name} ({typ}): {desc}" if typ else f"{name}: {desc}"
            param_lines.append(head.rstrip(": "))
        if param_lines:
            parts.append("Args:\n" + "\n".join("    " + l for l in param_lines))

        ret = (data.type_info or {}).get("returns") or {}
        ret_typ = (ret.get("doc_type") or ret.get("annotation") or "").strip()
        ret_desc = (ret.get("description") or "").strip()
        if ret_typ or ret_desc:
            head = f"{ret_typ}: {ret_desc}" if ret_typ else ret_desc
            parts.append("Returns:\n    " + head.strip())

        if data.examples:
            ex_body = "\n\n".join(data.examples)
            parts.append(
                "Examples:\n"
                + "\n".join(("    " + l if l.strip() else "") for l in ex_body.split("\n"))
            )

        return "\n\n".join(p for p in parts if p.strip())


class SphinxDialectHandler(DocstringDialectHandler):
    """reST/Sphinx-style: ``:param name:`` / ``:type name:`` / ``:return:`` /
    ``:rtype:`` field lists, e.g.::

        :param parameters: parameter names with type and description fields
        :type parameters: Mapping[str, Mapping[str, str]]
        :return: the parameter display
        :rtype: Any
    """

    name = "sphinx"

    _SNIFF_RE = re.compile(
        r'^[ \t]*:(param|parameter|type|return|returns|rtype|raises|raise|yield|yields)\b',
        re.IGNORECASE | re.MULTILINE,
    )
    _DIRECTIVE_RE = re.compile(r'^\s*:(\w+)(?:\s+([^:]+?))?\s*:\s*(.*)$')

    @classmethod
    def sniff(cls, raw: str) -> bool:
        return bool(cls._SNIFF_RE.search(raw or ""))

    def _parse_directives(self, raw: str) -> Tuple[str, List[Tuple[str, str, str]]]:
        """Return (intro_text, [(tag, arg, body_text), ...]) in source order."""
        intro_lines: List[str] = []
        directives: List[List[Any]] = []
        current = None
        for line in (raw or "").split("\n"):
            m = self._DIRECTIVE_RE.match(line)
            if m:
                tag, arg, rest = m.groups()
                current = [tag.lower(), (arg or "").strip(), [rest]]
                directives.append(current)
            elif current is not None:
                current[2].append(line.strip())
            else:
                intro_lines.append(line)
        return "\n".join(intro_lines).strip(), [
            (tag, arg, " ".join(l for l in body if l).strip()) for tag, arg, body in directives
        ]

    def extract(self, raw: str, node: ast.AST) -> Dict[str, Any]:
        intro, directives = self._parse_directives(raw or "")
        short, details = _split_intro(intro)
        params, returns = _blank_params(node)

        for tag, arg, text in directives:
            if tag in ("param", "parameter"):
                params.setdefault(arg, {"annotation": None, "doc_type": "", "description": ""})
                params[arg]["description"] = text
            elif tag == "type":
                params.setdefault(arg, {"annotation": None, "doc_type": "", "description": ""})
                params[arg]["doc_type"] = text
            elif tag in ("return", "returns"):
                returns["description"] = text
            elif tag == "rtype":
                returns["doc_type"] = text
            # :raises:/:yield: etc. aren't part of the canonical schema; ignored.

        examples = _extract_doctest_examples(raw or "")
        return {
            "short_description": short,
            "details": details,
            "examples": examples,
            "type_info": {"params": params, "returns": returns},
        }

    def render(self, data: "DocstringData") -> str:
        parts = []
        if data.short_description:
            parts.append(data.short_description.strip())
        if data.details:
            parts.append(data.details.strip())

        field_lines = []
        for name, info in (data.type_info.get("params") or {}).items():
            desc = (info.get("description") or "").strip()
            typ = (info.get("doc_type") or info.get("annotation") or "").strip()
            if desc:
                field_lines.append(f":param {name}: {desc}")
            if typ:
                field_lines.append(f":type {name}: {typ}")

        ret = (data.type_info or {}).get("returns") or {}
        ret_desc = (ret.get("description") or "").strip()
        ret_typ = (ret.get("doc_type") or ret.get("annotation") or "").strip()
        if ret_desc:
            field_lines.append(f":return: {ret_desc}")
        if ret_typ:
            field_lines.append(f":rtype: {ret_typ}")
        if field_lines:
            parts.append("\n".join(field_lines))

        if data.examples:
            parts.append("\n\n".join(data.examples))

        return "\n\n".join(p for p in parts if p.strip())


class PlainDialectHandler(DocstringDialectHandler):
    """Fallback for free-text docstrings with no recognized section markup.
    Preserves a summary/details split and any doctest examples, but does not
    impose ``Args:``/``:param:`` structure the original text didn't have.
    """

    name = "plain"

    @classmethod
    def sniff(cls, raw: str) -> bool:
        return True  # catch-all; only reached once Google/Sphinx don't match

    def extract(self, raw: str, node: ast.AST) -> Dict[str, Any]:
        short, details = _split_intro((raw or "").strip())
        params, returns = _blank_params(node)
        return {
            "short_description": short,
            "details": details,
            "examples": _extract_doctest_examples(raw or ""),
            "type_info": {"params": params, "returns": returns},
        }

    def render(self, data: "DocstringData") -> str:
        parts = []
        if data.short_description:
            parts.append(data.short_description.strip())
        if data.details:
            parts.append(data.details.strip())
        if data.examples:
            parts.append("\n\n".join(data.examples))
        return "\n\n".join(p for p in parts if p.strip())


GOOGLE = GoogleDialectHandler()
SPHINX = SphinxDialectHandler()
PLAIN = PlainDialectHandler()

#: Registry of available dialects, keyed by ``DocstringDialectHandler.name``.
DIALECTS: Dict[str, DocstringDialectHandler] = {h.name: h for h in (GOOGLE, SPHINX, PLAIN)}

#: Sniffing order: more specific/structured dialects first; Plain is the catch-all.
_SNIFF_ORDER: Tuple[DocstringDialectHandler, ...] = (SPHINX, GOOGLE)


def detect_dialect(raw: str, default: Optional[DocstringDialectHandler] = None) -> DocstringDialectHandler:
    """Pick the dialect handler that best matches `raw`.

    An empty/missing docstring has nothing to sniff, so it falls back to
    `default` (Google, richly-structured) since that's what a freshly written
    docstring will look like. Non-empty but unstructured text falls back to
    the Plain dialect so it isn't forced into a structure it never had.
    """
    default = default or GOOGLE
    if not (raw or "").strip():
        return default
    for handler in _SNIFF_ORDER:
        if handler.sniff(raw):
            return handler
    return PLAIN

def resolve_dialect(dialect: str|DocstringDialectHandler|None, default=dev.default) -> DocstringDialectHandler | None:
    if isinstance(dialect, str):
        if dev.is_default(default, allow_None=False):
            return DIALECTS[dialect]
        else:
            return DIALECTS.get(dialect, default)
    else:
        if dialect is None and not dev.is_default(default):
            dialect = resolve_dialect(default)
        return dialect


# --------------------------------------------------------------------------- #
# Public extractor / analysis functions
# --------------------------------------------------------------------------- #
def data_extractor(raw: str, node: ast.AST, dialect: Optional[DocstringDialectHandler] = None) -> Dict[str, Any]:
    """Break a raw docstring + its function node into structured fields.

    Args:
        raw (str): The cleaned docstring text (may be empty if there is none).
        node (ast.AST): The FunctionDef/AsyncFunctionDef node, used to read
            parameter/return annotations directly off the signature.
        dialect (Optional[DocstringDialectHandler]): Force a specific dialect
            instead of auto-detecting one via :func:`detect_dialect`.

    Returns:
        dict: with keys ``short_description``, ``details``, ``examples``
        (list[str]) and ``type_info`` (dict with ``params`` and ``returns``).
    """
    handler = dialect or detect_dialect(raw)
    return handler.extract(raw, node)


def analysis(data: "DocstringData") -> Dict[str, Any]:
    """Heuristically assess the quality of a parsed docstring.

    Args:
        data (DocstringData): A parsed (and possibly hand-edited) record.

    Returns:
        dict: ``{"score": int 0-100, "issues": list[str], "ok": bool}``.
    """
    issues: List[str] = []
    score = 100

    if not data.short_description:
        issues.append("missing short description")
        score -= 30
    else:
        if len(data.short_description) > 120:
            issues.append("short description too long (should be one concise line)")
            score -= 10
        if not data.short_description[:1].isupper():
            issues.append("short description should start with a capital letter")
            score -= 5

    params = data.type_info.get("params", {})
    real_params = {n: v for n, v in params.items() if n not in ("self", "cls")}

    undocumented = [n for n, v in real_params.items() if not v.get("description")]
    if undocumented:
        issues.append(f"undocumented parameter(s): {', '.join(undocumented)}")
        score -= min(30, 10 * len(undocumented))

    stale = [n for n, v in real_params.items() if v.get("annotation") is None and v.get("doc_type")]
    # only flag as "stale" if it's not a real signature param at all
    stale = [n for n in stale if n not in _signature_param_names(data)]
    if stale:
        issues.append(f"documented parameter(s) not in signature: {', '.join(stale)}")
        score -= min(20, 10 * len(stale))

    mismatched = []
    for n, v in real_params.items():
        ann, doc_t = v.get("annotation"), v.get("doc_type")
        if ann and doc_t and _normalize_type(ann) != _normalize_type(doc_t):
            mismatched.append(n)
    if mismatched:
        issues.append(f"type mismatch between annotation and docs: {', '.join(mismatched)}")
        score -= min(20, 10 * len(mismatched))

    ret = data.type_info.get("returns", {}) or {}
    if ret.get("annotation") and ret["annotation"] != "None" and not ret.get("description"):
        issues.append("return value not documented")
        score -= 10

    if len(real_params) >= 3 and not data.examples:
        issues.append("no usage example for a non-trivial signature")
        score -= 10

    score = max(0, score)
    return {"score": score, "issues": issues, "ok": score >= 70}


def _normalize_type(s: str) -> str:
    return re.sub(r"\s+", "", s or "").lower()


def _signature_param_names(data: "DocstringData"):
    return {n for n, v in data.type_info.get("params", {}).items() if v.get("annotation") is not None
            or n in ("self", "cls")}


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #
@dataclass
class DocstringData:
    """Structured record of one function/method's docstring and metadata.

    Args:
        qualname (str): Dotted qualified name (``Class.method`` for methods).
        lineno (int): 1-based line of the ``def``/``async def``.
        end_lineno (int): 1-based last line of the function body.
        body_indent (int): Column offset of the function body (drives the
            indentation used when writing a docstring back).
        doc_start_line (Optional[int]): 1-based line of the docstring's
            opening quotes, or ``None`` if the function has no docstring.
        doc_end_line (Optional[int]): 1-based line of the docstring's closing
            quotes, or ``None`` if the function has no docstring.
        raw (str): The original cleaned docstring text (``""`` if absent).
        short_description (str): One-line summary.
        details (str): Any extended prose beyond the summary.
        examples (List[str]): Extracted example blocks (doctest or an
            ``Examples:`` section).
        type_info (Dict[str, Any]): ``{"params": {name: {annotation,
            doc_type, description}}, "returns": {annotation, doc_type,
            description}}``.
        quality (Optional[Dict[str, Any]]): Filled in by :func:`analysis`.
        dialect (str): Name of the :class:`DocstringDialectHandler` this
            record was parsed with (e.g. ``"google"``, ``"sphinx"``,
            ``"plain"``) -- see ``DIALECTS``. Used by :class:`DocstringWriter`
            to render back in the same convention.
    """

    qualname: str
    lineno: int
    end_lineno: int
    body_indent: int
    doc_start_line: Optional[int]
    doc_end_line: Optional[int]
    raw: str = ""
    short_description: str = ""
    details: str = ""
    examples: List[str] = field(default_factory=list)
    type_info: Dict[str, Any] = field(default_factory=lambda: {"params": {}, "returns": {}})
    quality: Optional[Dict[str, Any]] = None
    dialect: str = ""

    def to_json(self) -> dict:
        """Return a plain, JSON-serializable dict of this record."""
        return dataclasses.asdict(self)

    @classmethod
    def from_json(cls, d: dict) -> "DocstringData":
        """Reconstruct a record from a dict produced by :meth:`to_json`."""
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})


# --------------------------------------------------------------------------- #
# DocstringParser
# --------------------------------------------------------------------------- #
class DocstringParser:
    """Parse a Python source file into a list of :class:`DocstringData`.

    Each function's docstring is parsed by whichever
    :class:`DocstringDialectHandler` matches it best (see
    :func:`detect_dialect`), so a single file with a mix of Google-style and
    Sphinx-style docstrings parses correctly function-by-function -- unless a
    `dialect` is passed to force one convention for the whole file.
    """

    def __init__(self, dialect: Optional[DocstringDialectHandler] = None):
        """
        Args:
            dialect (Optional[DocstringDialectHandler]): If given, every
                docstring is parsed with this handler instead of
                auto-detecting one per function.
        """
        self.dialect = dialect

    def parse_source(self, src: str, only_missing: bool = False) -> List[DocstringData]:
        """Parse `src` text and return one :class:`DocstringData` per function.

        Args:
            src (str): Python source code.
            only_missing (bool): If True, skip functions that already have a
                docstring.

        Returns:
            List[DocstringData]: records in source order.
        """
        tree = ast.parse(src)
        out: List[DocstringData] = []
        for qual, node in _iter_funcs(tree):
            has_doc = _has_docstring_node(node)
            if only_missing and has_doc:
                continue

            raw = ast.get_docstring(node, clean=True) or ""
            doc_start = doc_end = None
            if has_doc:
                body0 = node.body[0]
                doc_start, doc_end = body0.lineno, body0.end_lineno

            handler = self.dialect or detect_dialect(raw)
            extracted = handler.extract(raw, node)
            out.append(DocstringData(
                qualname=qual,
                lineno=node.lineno,
                end_lineno=node.end_lineno,
                body_indent=node.body[0].col_offset,
                doc_start_line=doc_start,
                doc_end_line=doc_end,
                raw=raw,
                dialect=handler.name,
                **extracted,
            ))
        return out

    def parse_file(self, path: str, only_missing: bool = False) -> List[DocstringData]:
        """Read `path` and delegate to :meth:`parse_source`."""
        return self.parse_source(dev.read_file(path), only_missing=only_missing)


# --------------------------------------------------------------------------- #
# DocstringWriter
# --------------------------------------------------------------------------- #
DEFAULT_HEADER = ""
class DocstringWriter:
    """Write (possibly edited) :class:`DocstringData` records back into source.

    Each record renders via its own ``data.dialect`` handler by default, so a
    docstring parsed as Sphinx is written back as Sphinx and one parsed as
    Google comes back as Google -- pass `dialect` to force one convention for
    every record instead (e.g. to upgrade a whole file to Sphinx style).

    Guarantees, via :meth:`verify_code_identity`, that nothing except
    docstring text changes.
    """

    def __init__(self, header: str = DEFAULT_HEADER, add_header: bool = True,
                 dialect: Optional[DocstringDialectHandler] = None):
        """
        Args:
            header (str): Line prepended to every rewritten docstring.
            add_header (bool): If False, no header is added.
            dialect (Optional[DocstringDialectHandler]): If given, every
                record is rendered with this handler regardless of its own
                ``dialect`` field.
        """
        self.header = header
        self.add_header = add_header
        self.dialect = resolve_dialect(dialect)

    default_dialect = SPHINX
    def _handler_for(self, data: DocstringData) -> DocstringDialectHandler:
        if self.dialect is not None:
            return self.dialect
        else:
            return resolve_dialect(data.dialect, self.default_dialect)

    def _format_block(self, data: DocstringData) -> List[str]:
        indent = " " * data.body_indent
        body = self._handler_for(data).render(data)
        if self.add_header and self.header:
            body = f"{self.header}\n\n{body}" if body else self.header
        lines = [indent + '"""']
        lines += [((indent + l).rstrip() if l.strip() else "") for l in body.split("\n")]
        lines.append(indent + '"""')
        return lines

    def write_source(self, src: str, data_list: List[DocstringData]) -> str:
        """Return a new source string with the given records' docstrings applied.

        Records are matched to functions by ``qualname`` (not by stored line
        numbers, which may be stale) and located freshly against `src`.

        Args:
            src (str): Original source code.
            data_list (List[DocstringData]): Records to write; others in the
                file are left untouched.

        Returns:
            str: The rewritten source. Raises ``SyntaxError`` if the result
            would not parse, and never returns a result that changes any
            executable code (see :meth:`verify_code_identity`).
        """
        lines = src.split("\n")
        by_qual = {d.qualname: d for d in data_list}

        tree = ast.parse(src)
        edits = []  # (start_line_1based, end_line_1based_or_less_than_start, block_lines)
        for qual, node in _iter_funcs(tree):
            if qual not in by_qual:
                continue
            data = by_qual[qual]
            block = self._format_block(data)
            if _has_docstring_node(node):
                body0 = node.body[0]
                edits.append((body0.lineno, body0.end_lineno, block))
            else:
                hedln = _header_end_line(lines, node.lineno)
                edits.append((hedln + 1, hedln, block))  # end < start => pure insert

        for start, end, block in sorted(edits, key=lambda x: x[0], reverse=True):
            if end >= start:
                lines[start - 1:end] = block
            else:
                lines[start - 1:start - 1] = block

        new_src = "\n".join(lines)
        ast.parse(new_src)  # raises SyntaxError if broken
        return new_src

    def write_file(self, path: str,
                   data_list: List[DocstringData],
                   target:str = dev.default,
                   backup: bool = None) -> tuple[str, str]:
        """Read `path`, apply `data_list`, and write the result back to `path`.

        Args:
            path (str): File to modify in place.
            data_list (List[DocstringData]): Records to write.
            backup (bool): If True (default), keep a ``<path>.docbak`` copy of
                the pre-rewrite source (only created the first time).

        Returns:
            str: The new source that was written.
        """
        src = dev.read_file(path)
        if dev.is_default(target, allow_None=False):
            target = src
            if backup is None: backup = True
        new_src = self.write_source(src, data_list)
        if not self.verify_code_identity(src, new_src):
            raise ValueError("rewrite would change executable code")
        if target is not None and backup:
            bak = path + ".docbak"
            if not os.path.exists(bak):
                dev.write_file(bak, src)
        if target is not None:
            dev.write_file(target, new_src)
            return target, new_src
        else:
            return new_src

    @staticmethod
    def verify_code_identity(original_src: str, new_src: str) -> bool:
        """Confirm only docstrings differ between two versions of a file.

        Args:
            original_src (str): The "before" source.
            new_src (str): The "after" source.

        Returns:
            bool: True if stripping all docstrings from both yields identical
            (``ast.unparse``-normalized) code.
        """
        return _strip_docstrings(original_src) == _strip_docstrings(new_src)