from __future__ import annotations

import abc
import ast
import dataclasses
import io
import json
import os
import re
import sys
import tokenize
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .. import Devutils as dev
from .Stubs import PackageHandler

__all__ = [
    "DocstringParser",
    "DocstringWriter",
    "DocstringDialectHandler",
    "DocstringDataAnalyzer",
    "DocstringsHandler",
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


def _parse_list_field(text: str) -> List[str]:
    """Parse a free-form list section/field (e.g. Related/Links) into items.

    Splits on newlines first; if that yields a single line, falls back to
    splitting on commas or semicolons so a one-liner like
    ``:related: foo, bar`` still produces two items. Leading bullet markers
    ('-', '*', '\u2022') are stripped from each item.
    """
    text = (text or "").strip()
    if not text:
        return []
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if len(lines) <= 1 and lines:
        parts = re.split(r'[,;]', lines[0])
        if len(parts) > 1:
            lines = [p.strip() for p in parts if p.strip()]
    return [re.sub(r'^[-*\u2022]\s*', '', l) for l in lines if l]


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
        r'Raises|Raise|Example|Examples|Note|Notes|Attributes|Attribute|'
        r'Related|Links)\s*:\s*$',
        re.IGNORECASE,
    )
    _SNIFF_RE = re.compile(
        r'^[ \t]*(Args|Arguments|Parameters|Returns|Return|Yields|Yield|Raises|Raise|'
        r'Related|Links)\s*:\s*$',
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

        related = _parse_list_field(sections.get("related", ""))
        links = _parse_list_field(sections.get("links", ""))

        return {
            "short_description": short,
            "details": details,
            "examples": examples,
            "type_info": {"params": params, "returns": returns},
            "related": related,
            "links": links,
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

        if data.related:
            parts.append("Related:\n" + "\n".join("    " + r for r in data.related))

        if data.links:
            parts.append("Links:\n" + "\n".join("    " + l for l in data.links))

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
        r'^[ \t]*:(param|parameter|type|return|returns|rtype|raises|raise|yield|yields|'
        r'example|examples|related|links|link)\b',
        re.IGNORECASE | re.MULTILINE,
    )
    _DIRECTIVE_RE = re.compile(r'^\s*:(\w+)(?:\s+([^:]+?))?\s*:\s*(.*)$')

    @classmethod
    def sniff(cls, raw: str) -> bool:
        return bool(cls._SNIFF_RE.search(raw or ""))

    def _parse_directives(self, raw: str) -> Tuple[str, List[Tuple[str, str, List[str]]]]:
        """Return (intro_text, [(tag, arg, body_lines), ...]) in source order.

        `body_lines` keeps each continuation line separate (rather than
        joining them into one string here) so callers can choose how to
        rejoin: single-value fields like ``:param:``/``:type:`` collapse to
        one line, while multi-line fields like ``:examples:`` keep their
        internal line breaks (important for doctest blocks).
        """
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
                current[2].append(line)
            else:
                intro_lines.append(line)
        return "\n".join(intro_lines).strip(), [(tag, arg, body) for tag, arg, body in directives]

    def extract(self, raw: str, node: ast.AST) -> Dict[str, Any]:
        intro, directives = self._parse_directives(raw or "")
        short, details = _split_intro(intro)
        params, returns = _blank_params(node)
        examples: List[str] = []
        related: List[str] = []
        links: List[str] = []

        def single_line(body_lines):
            return " ".join(l.strip() for l in body_lines if l.strip())

        def multi_line(body_lines):
            return "\n".join(l.strip() for l in body_lines).strip()

        for tag, arg, body_lines in directives:
            if tag in ("param", "parameter"):
                text = single_line(body_lines)
                params.setdefault(arg, {"annotation": None, "doc_type": "", "description": ""})
                params[arg]["description"] = text
            elif tag == "type":
                text = single_line(body_lines)
                params.setdefault(arg, {"annotation": None, "doc_type": "", "description": ""})
                params[arg]["doc_type"] = text
            elif tag in ("return", "returns"):
                returns["description"] = single_line(body_lines)
            elif tag == "rtype":
                returns["doc_type"] = single_line(body_lines)
            elif tag in ("example", "examples"):
                text = multi_line(body_lines)
                if text:
                    examples.append(text)
            elif tag == "related":
                related.extend(_parse_list_field(multi_line(body_lines)))
            elif tag in ("links", "link"):
                links.extend(_parse_list_field(multi_line(body_lines)))
            # :raises:/:yield: etc. aren't part of the canonical schema; ignored.

        examples.extend(
            block for block in _extract_doctest_examples(intro) if block not in examples
        )
        return {
            "short_description": short,
            "details": details,
            "examples": examples,
            "type_info": {"params": params, "returns": returns},
            "related": related,
            "links": links,
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

        if data.examples:
            field_lines.append(":examples:")
            for example in data.examples:
                for l in example.split("\n"):
                    field_lines.append("    " + l if l.strip() else "")

        if data.related:
            field_lines.append(":related: " + ", ".join(data.related))

        if data.links:
            field_lines.append(":links: " + ", ".join(data.links))

        if field_lines:
            parts.append("\n".join(field_lines))

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
            "related": [],
            "links": [],
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


def _normalize_type(s: str) -> str:
    return re.sub(r"\s+", "", s or "").lower()


def _signature_param_names(data: "DocstringData"):
    return {n for n, v in data.type_info.get("params", {}).items() if v.get("annotation") is not None
            or n in ("self", "cls")}


def default_exclude(qualname: str, package_name: Optional[str] = None) -> bool:
    """Default `exclude` predicate for `DocstringParser`/`DocstringsHandler`.

    True if any dotted component of `qualname` -- i.e. any class name or
    function/method name in its path, such as ``Widget`` or ``spin`` in
    ``Widget.spin`` -- starts with an underscore. Covers private names
    (``_helper``), private classes and everything under them, and other
    dunders (``__eq__``, ``__repr__``, ...) -- except ``__init__``, which
    is exempted since it's routinely the most useful method to document.
    """
    return any(part.startswith("_") and part != "__init__" for part in qualname.split("."))
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
        related (List[str]): Names of related functions/classes, from a
            ``Related:`` section (Google) or ``:related:`` field (Sphinx).
        links (List[str]): Reference URLs/links, from a ``Links:`` section
            (Google) or ``:links:`` field (Sphinx).
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
    related: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)

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
    `DocstringDialectHandler` matches it best (see `detect_dialect`), so a single file with a mix of Google-style and
    Sphinx-style docstrings parses correctly function-by-function -- unless a
    `dialect` is passed to force one convention for the whole file.

    `filter`/`exclude` let a caller skip docstring parsing entirely for
    functions/methods/classes-of-methods that don't matter to it -- neither
    the docstring nor the signature is even read for anything they skip.
    Both are called as ``predicate(qualname, package_name)``, where
    `qualname` is the dotted ``Class.method`` (or bare function) name and
    `package_name` is whatever the caller passed to `parse_source`/
    `parse_file` (``None`` if not given -- `DocstringsHandler` passes the
    actual top-level package name, giving predicates "package information"
    alongside the name).
    """

    def __init__(self, dialect: Optional[DocstringDialectHandler] = None,
                 filter=None, exclude=default_exclude):
        """
        Args:
            dialect (Optional[DocstringDialectHandler]): If given, every
                docstring is parsed with this handler instead of
                auto-detecting one per function.
            filter: optional ``(qualname, package_name) -> bool``. If
                given, only qualnames for which this returns True are
                parsed at all; ``None`` (the default) applies no filter,
                i.e. everything is a candidate.
            exclude: optional ``(qualname, package_name) -> bool``.
                Qualnames for which this returns True are skipped, same as
                an inverted `filter`. Defaults to :func:`default_exclude`
                (skip anything with a leading-underscore name); pass
                ``None`` to disable exclusion entirely.
        """
        self.dialect = resolve_dialect(dialect)
        self.filter = filter
        self.exclude = exclude

    def wanted(self, qualname: str, package_name: Optional[str] = None) -> bool:
        """True if `qualname` should actually be parsed, given this
        parser's `filter`/`exclude`."""
        if self.filter is not None and not self.filter(qualname, package_name):
            return False
        if self.exclude is not None and self.exclude(qualname, package_name):
            return False
        return True

    def parse_source(self, src: str, only_missing: bool = False,
                      package_name: Optional[str] = None) -> List[DocstringData]:
        """Parse `src` text and return one :class:`DocstringData` per function.

        Args:
            src (str): Python source code.
            only_missing (bool): If True, skip functions that already have a
                docstring.
            package_name (Optional[str]): Passed through to `filter`/
                `exclude` alongside each qualname; has no other effect.

        Returns:
            List[DocstringData]: records in source order, excluding any
            qualname `filter`/`exclude` ruled out (those are never parsed
            at all, not merely omitted after the fact).
        """
        tree = ast.parse(src)
        out: List[DocstringData] = []
        for qual, node in _iter_funcs(tree):
            if not self.wanted(qual, package_name):
                continue

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

    def parse_file(self, path: str, only_missing: bool = False,
                    package_name: Optional[str] = None) -> List[DocstringData]:
        """Read `path` and delegate to :meth:`parse_source`."""
        return self.parse_source(dev.read_file(path), only_missing=only_missing,
                                  package_name=package_name)


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

class DocstringQAField:
    issue_registry = {}
    tag_name = None
    default_short_name = None
    @classmethod
    def register(cls, name, method=None):
        if method is None and hasattr(name, 'name'):
            method = name
            name = method.name
        if method is not None:
            method.tag_name = name
            cls.issue_registry[name] = method
            return method
        else:
            def register(method, name=name):
                return cls.register(name, method)
            return register

    __slots__ = ("description", "score")
    default_description = None
    default_score = None
    def __init__(self, description=None, score=None):
        if description is None: description = self.default_description
        self.description = description
        if score is None: score = self.default_score
        self.score = score
    def __repr__(self):
        argstr_bits = []
        if self.description is not None:
            argstr_bits.append(f"{self.description=!r}")
        if self.score is not None:
            argstr_bits.append(f"{self.score=!r}")
        argstr = ", ".join(argstr_bits)
        return f"{type(self).__name__}({argstr})"
    @property
    def short_name(self):
        if self.default_short_name is None:
            name = self.tag_name
            if name is None:
                name = type(self).__name__
            return name
        else:
            return self.default_short_name

@DocstringQAField.register('missing_description')
class MissingDescription(DocstringQAField):
    default_short_name = 'description'
    default_score = -50
@DocstringQAField.register('missing_short_description')
class MissingShortDescription(MissingDescription):
    default_short_name = 'short_description'
    default_score = -10
@DocstringQAField.register('missing_parameter')
class MissingParameter(DocstringQAField):
    default_short_name = 'missing'
    default_score = -30
@DocstringQAField.register('missing_return_value')
class MissingReturnValue(DocstringQAField):
    default_short_name = 'missing'
    default_score = -50
@DocstringQAField.register('missing_return_type')
class MissingReturnType(DocstringQAField):
    default_short_name = 'type'
    default_score = -30
@DocstringQAField.register('stale_parameter')
class StaleParameter(DocstringQAField):
    default_score = -30
@DocstringQAField.register('stale_parameter_type')
class StaleParameterType(DocstringQAField):
    default_score = -20
@DocstringQAField.register('missing_parameter_description')
class MissingParameterDescription(MissingDescription):
    default_short_name = 'description'
    default_score = -10
@DocstringQAField.register('missing_parameter_type')
class MissingParameterType(DocstringQAField):
    default_short_name = 'type'
    default_score = -5
@DocstringQAField.register('bad_description')
class BadDescription(DocstringQAField):
    default_short_name = 'description'
    default_score = -10
@DocstringQAField.register('short_description_too_long')
class ShortDescriptionTooLong(BadDescription):
    default_short_name = 'too_long'
    default_score = -5

@DocstringQAField.register('has_examples')
class HasExamples(DocstringQAField):
    default_score = 75
@DocstringQAField.register('has_related')
class HasRelated(DocstringQAField):
    default_score = 1
@DocstringQAField.register('has_links')
class HasLinks(DocstringQAField):
    default_score = 1

class DocstringDataAnalyzer:
    def __init__(self, data:DocstringData, analyses=None):
        self.data = data
        self.analyses = analyses

    @property
    def default_analyses(self):
        return {
            "descriptions":self._check_description,
            "parameters":self._check_undocumented_parameters,
            "stale":self._check_stale_parameters,
            "returns":self._check_return_values,
            "examples":self._check_examples,
            "related":self._check_related,
            "links":self._check_links,
        }
    def get_analyses(self):
        if self.analyses is None:
            return self.default_analyses
        elif dev.is_list_like(self.analyses):
            df = self.default_analyses
            return {k:df[k] for k in self.analyses}
        else:
            return self.analyses

    @classmethod
    def _check_doc_type(cls, typestr):
        return (
            typestr is not None and
            typestr not in ("object", "Any", "_", "")
        )

    @classmethod
    def _check_description(cls, data:DocstringData) -> list[DocstringQAField]:
        issues = []
        if not data.short_description:
            if not data.details:
                issues.append(MissingDescription())
            else:
                issues.append(MissingShortDescription())
        else:
            if len(data.short_description) > 120:
                issues.append(ShortDescriptionTooLong())
        return issues

    @classmethod
    def _check_undocumented_parameters(cls, data:DocstringData) -> list[DocstringQAField]:
        issues = []

        params = data.type_info.get("params", {})
        real_params = {n: v for n, v in params.items() if n not in ("self", "cls")}

        for n, v in real_params.items():
            if not v.get("description"):
                issues.append(MissingParameterDescription())
            if not cls._check_doc_type(v.get("doc_type")):
                issues.append(MissingParameterType())

        return issues

    @classmethod
    def _check_stale_parameters(cls, data: DocstringData) -> list[DocstringQAField]:
        issues = []

        params = data.type_info.get("params", {})
        real_params = {n: v for n, v in params.items() if n not in ("self", "cls")}

        stale = [n for n, v in real_params.items() if v.get("annotation") is None and v.get("doc_type")]
        # only flag as "stale" if it's not a real signature param at all
        stale = [n for n in stale if n not in _signature_param_names(data)]
        if stale:
            for n in stale:
                issues.append(StaleParameter(n))

        mismatched = []
        for n, v in real_params.items():
            ann, doc_t = v.get("annotation"), v.get("doc_type")
            if ann and doc_t and _normalize_type(ann) != _normalize_type(doc_t):
                mismatched.append(n)
        if mismatched:
            for n in mismatched:
                issues.append(StaleParameterType(n))

        return issues

    @classmethod
    def _check_return_values(cls, data: DocstringData) -> list[DocstringQAField]:
        issues = []

        ret = data.type_info.get("returns", {}) or {}
        if not ret.get("description"):
            issues.append(MissingReturnValue())
        if not cls._check_doc_type(ret.get("doc_type")):
            issues.append(MissingReturnType())

        return issues

    @classmethod
    def _check_examples(cls, data: DocstringData) -> list[DocstringQAField]:
        issues = []
        examples = data.examples or []
        n = len(examples)
        for example in examples:
            issues.append(HasExamples())
        return issues

    @classmethod
    def _check_related(cls, data: DocstringData) -> list[DocstringQAField]:
        """Reward (not penalize) cross-referencing related functions/classes."""
        issues = []
        related = data.related or []
        for rel in related:
            issues.append(HasRelated())
        return issues

    @classmethod
    def _check_links(cls, data: DocstringData) -> list[DocstringQAField]:
        """Reward (not penalize) including reference links."""
        issues = []
        links = data.links or []
        for link in links:
            issues.append(HasLinks())
        return issues

    def analyze_docstring_quality(self) -> tuple[dict[str, list[DocstringQAField]], int]:
        """Heuristically assess the quality of a parsed docstring."""
        score = 0
        issue_breakdowns = {}
        data = self.data
        for tag, analysis in self.get_analyses().items():
            issues = analysis(data)
            issue_breakdowns[tag] = issues
            score += sum(i.score for i in issues)

        return issue_breakdowns, score


# --------------------------------------------------------------------------- #
# DocstringsHandler -- DocumentationPackageDispatcher integration
# --------------------------------------------------------------------------- #
class DocstringsHandler(PackageHandler):
    """`PackageHandler` that runs `DocstringParser` + `DocstringDataAnalyzer`
    over every function/method in a package's source during `parse()`, then
    -- at `write()` time, once every package has been processed -- writes a
    single `docstring_quality.json` at the root of `out_dir` tracking the
    score and issue breakdown for every docstring in the whole run.

    Not one of `DocumentationPackageDispatcher.DEFAULT_HANDLERS`; opt in by
    passing it explicitly, e.g.::

        DocumentationPackageDispatcher(
            ..., handlers=(StubSummaryHandler, ExampleHandler, DocstringsHandler))
    """

    name = "docstring_quality"

    QUALITY_JSON_FILENAME = "docstring_quality.json"
    SYNTAX_ERROR_WARNING_TEMPLATE = "[WARN] syntax error, skipping docstring QA: {rel_path}: {error}"
    READ_ERROR_WARNING_TEMPLATE = "[WARN] couldn't read {rel_path} for docstring QA: {error}"

    def __init__(self, dispatcher, dialect=None, analyses=None, filter=None, exclude=default_exclude):
        """
        Args:
            dialect: forced `DocstringDialectHandler`, passed straight
                through to `DocstringParser` (default: auto-detect per
                docstring).
            analyses: forced subset/mapping of checks, passed straight
                through to every `DocstringDataAnalyzer` (default: all of
                `DocstringDataAnalyzer.default_analyses`).
            filter: optional ``(qualname, package_name) -> bool`` forwarded
                to `DocstringParser` -- only matching functions/methods are
                parsed at all. Defaults to ``None`` (no filtering).
            exclude: optional ``(qualname, package_name) -> bool`` forwarded
                to `DocstringParser` -- matching functions/methods are
                skipped entirely (never parsed). Defaults to
                :func:`default_exclude` (anything with a leading-underscore
                class or function/method name); pass ``None`` to disable.
        """
        super().__init__(dispatcher)
        self.parser = DocstringParser(dialect=dialect, filter=filter, exclude=exclude)
        self.analyses = analyses

    def _iter_py_files(self, pkg_src_path):
        """Yield (full_path, rel_path) for every .py file under a package's
        source -- rel_path is relative to pkg_src_path for a package
        directory, or just the bare filename for a single-file package."""
        if os.path.isdir(pkg_src_path):
            for root, _, files in os.walk(pkg_src_path):
                for fname in sorted(files):
                    if fname.endswith(".py"):
                        full = os.path.join(root, fname)
                        yield full, os.path.relpath(full, pkg_src_path)
        else:
            yield pkg_src_path, os.path.basename(pkg_src_path)

    #: tags whose issues get collapsed to their (deduplicated) `description`
    #: rather than the full {type, description, score} dict.
    _SIMPLIFY_BY_DESCRIPTION = frozenset({"stale"})
    #: tags whose issues get collapsed to their (deduplicated) `type` name.
    _SIMPLIFY_BY_TYPE = frozenset({"parameters", "returns", "descriptions"})

    @staticmethod
    def _issue_to_json(issue: DocstringQAField) -> dict:
        return {"type": type(issue).__name__, "description": issue.description, "score": issue.score}

    def _simplified_issues(self, tag, issues):
        """Drop any issue with a positive score -- those are bonuses (e.g.
        `HasExamples`), not problems, and don't belong in an `issues`
        listing -- then simplify what's left: `stale` collapses to its
        deduplicated `description`s, `parameters`/`returns` collapse to
        their deduplicated `type` names, and everything else keeps the
        full {type, description, score} form."""
        kept = [i for i in issues if (i.score or 0) <= 0]
        if not kept:
            kept = []
        elif tag in self._SIMPLIFY_BY_DESCRIPTION:
            kept = list(dict.fromkeys(i.description for i in kept))
        elif tag in self._SIMPLIFY_BY_TYPE:
            kept = list(dict.fromkeys(i.short_name for i in kept))
        else:
            kept = [self._issue_to_json(i) for i in kept]
        if tag == "returns" and len(kept) == 2:
            kept = ["both"]
        return kept

    def _score_file(self, full_path, rel_path, package_name):
        try:
            src = dev.read_file(full_path)
        except Exception as e:
            print(self.READ_ERROR_WARNING_TEMPLATE.format(rel_path=rel_path, error=e), file=sys.stderr)
            return [], str(e)
        try:
            data_list = self.parser.parse_source(src, package_name=package_name)
        except SyntaxError as e:
            print(self.SYNTAX_ERROR_WARNING_TEMPLATE.format(rel_path=rel_path, error=e), file=sys.stderr)
            return [], str(e)

        records = []
        for data in data_list:
            issue_breakdown, score = DocstringDataAnalyzer(data, analyses=self.analyses).analyze_docstring_quality()
            records.append({
                "rel_path": rel_path,
                "qualname": data.qualname,
                "has_docstring": bool(data.raw),
                "dialect": data.dialect,
                "score": score,
                "issues": {
                    tag: simplified
                    for tag, issues in issue_breakdown.items()
                    if (simplified := self._simplified_issues(tag, issues))
                },
            })
        return records, None

    def parse(self, package_name, pkg_src_path):
        """Score every docstring under `pkg_src_path`; safe against any one
        file failing to read/parse (best-effort -- one bad module shouldn't
        drop QA data for the rest of the package; its error is recorded
        under `errors` instead). Functions/methods ruled out by `filter`/
        `exclude` are never parsed in the first place -- see
        `DocstringParser.wanted`."""
        records = []
        errors = []
        for full_path, rel_path in self._iter_py_files(pkg_src_path):
            recs, err = self._score_file(full_path, rel_path, package_name)
            records.extend(recs)
            if err is not None:
                errors.append({"rel_path": rel_path, "error": err})

        n = len(records)
        total_score = sum(r["score"] for r in records)
        return {
            "records": records,
            "errors": errors,
            "n_functions": n,
            "total_score": total_score,
            "average_score": (total_score / n) if n else None,
        }

    def write(self, components, compact=True):
        """Aggregate every package's `parse()` result into a single
        docstring_quality.json at the root of out_dir."""
        packages = {
            pkg: info[self.name] for pkg, info in components.items() if self.name in info
        }
        grand_n = sum(p["n_functions"] for p in packages.values())
        grand_total = sum(p["total_score"] for p in packages.values())
        average_score = (grand_total / grand_n) if grand_n else None
        grand_errors = sum(len(p.get("errors", [])) for p in packages.values())

        if compact:
            payload = packages
        else:
            payload = {
                "packages": packages,
                "n_functions": grand_n,
                "total_score": grand_total,
                "average_score": average_score,
                "n_errors": grand_errors,
            }
        os.makedirs(self.dispatcher.out_dir, exist_ok=True)
        path = os.path.join(self.dispatcher.out_dir, self.QUALITY_JSON_FILENAME)
        with open(path, "w", encoding="utf-8") as f:
            if compact:
                json.dump(payload, f, sort_keys=True)
            else:
                json.dump(payload, f, indent=2, sort_keys=True)

        if self.dispatcher.verbose:
            print(f"docstring quality: {grand_n} functions scored, "
                  f"average score {average_score}, written to {path}")

        return {"docstring_quality_size": os.path.getsize(path), "average_score": average_score}
