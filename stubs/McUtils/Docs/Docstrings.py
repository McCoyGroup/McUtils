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
__all__ = ['DocstringParser', 'DocstringWriter', 'DocstringDialectHandler', 'DocstringDataAnalyzer', 'DocstringsHandler']

def _iter_funcs(tree):
    """Yield (qualname, node) for every function/method, in source order."""
    ...

def _header_end_line(lines, start_line):
    """1-based line where the def signature's closing ':' lives."""
    ...

def _strip_docstrings(src):
    """Parse, drop every module/class/function docstring, return unparsed code."""
    ...

def _has_docstring_node(node) -> bool:
    ...

def _signature_types(node) -> Dict[str, Any]:
    """Pull parameter/return annotations straight off the function signature."""
    ...
_DOCTEST_RE = re.compile('(?:^|\\n)([ \\t]*>>>.*(?:\\n(?!\\s*\\n)[ \\t]*.*)*)', re.MULTILINE)

def _split_intro(intro: str) -> Tuple[str, str]:
    """First paragraph -> short_description (collapsed to one line); rest -> details."""
    ...

def _extract_doctest_examples(raw: str) -> List[str]:
    """Pull out ``>>> ...`` doctest blocks. Dialect-independent."""
    ...

def _parse_list_field(text: str) -> List[str]:
    """Parse a free-form list section/field (e.g. Related/Links) into items.

    Splits on newlines first; if that yields a single line, falls back to
    splitting on commas or semicolons so a one-liner like
    ``:related: foo, bar`` still produces two items. Leading bullet markers
    ('-', '*', '•') are stripped from each item.
    """
    ...

def _blank_params(node: ast.AST) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Seed (params, returns) dicts straight from the signature, with no docs yet."""
    ...

class DocstringDialectHandler(abc.ABC):
    """A pluggable docstring convention: parses raw text into the canonical
    ``DocstringData`` fields, and renders those fields back into text using
    the same convention.

    Subclasses register themselves (see ``DIALECTS`` below) so a file can mix
    conventions function-by-function and each one round-trips in its own
    style.
    """
    name: str = 'base'

    @classmethod
    @abc.abstractmethod
    def sniff(cls, raw: str) -> bool:
        """Return True if `raw` looks like it was written in this dialect."""
        ...

    @abc.abstractmethod
    def extract(self, raw: str, node: ast.AST) -> Dict[str, Any]:
        """Parse `raw` (+ signature info from `node`) into the canonical dict:
        ``{"short_description", "details", "examples", "type_info"}``.
        """
        ...

    @abc.abstractmethod
    def render(self, data: 'DocstringData') -> str:
        """Render a (possibly edited) ``DocstringData`` back into body text."""
        ...

class GoogleDialectHandler(DocstringDialectHandler):
    """Google-style: ``Args:`` / ``Returns:`` / ``Examples:`` sections."""
    name = 'google'
    _ARG_LINE_RE = re.compile('^(\\s*)([\\w\\*]+)\\s*(?:\\(([^)]*)\\))?\\s*:\\s*(.*)$')
    _RETURN_LINE_RE = re.compile('^\\s*([\\w\\.\\[\\], \\\'"]+?)\\s*:\\s*(.+)$')

    @classmethod
    def sniff(cls, raw: str) -> bool:
        ...

    def _split_sections(self, text: str) -> Tuple[str, Dict[str, str]]:
        """Split a docstring body into (intro_text, {section_name: body_text})."""
        ...

    def _parse_args_section(self, text: str) -> Dict[str, Dict[str, str]]:
        """Parse an ``Args:`` body into {name: {doc_type, description}}."""
        ...

    def _parse_return_section(self, text: str) -> Tuple[str, str]:
        """Split a ``Returns:`` body's leading ``type: `` prefix from its description."""
        ...

    def _extract_examples(self, raw: str, sections: Dict[str, str]) -> List[str]:
        ...

    def extract(self, raw: str, node: ast.AST) -> Dict[str, Any]:
        ...

    def render(self, data: 'DocstringData') -> str:
        ...

class SphinxDialectHandler(DocstringDialectHandler):
    """reST/Sphinx-style: ``:param name:`` / ``:type name:`` / ``:return:`` /
    ``:rtype:`` field lists, e.g.::

        :param parameters: parameter names with type and description fields
        :type parameters: Mapping[str, Mapping[str, str]]
        :return: the parameter display
        :rtype: Any
    """
    name = 'sphinx'
    _DIRECTIVE_RE = re.compile('^\\s*:(\\w+)(?:\\s+([^:]+?))?\\s*:\\s*(.*)$')

    @classmethod
    def sniff(cls, raw: str) -> bool:
        ...

    def _parse_directives(self, raw: str) -> Tuple[str, List[Tuple[str, str, List[str]]]]:
        """Return (intro_text, [(tag, arg, body_lines), ...]) in source order.

        `body_lines` keeps each continuation line separate (rather than
        joining them into one string here) so callers can choose how to
        rejoin: single-value fields like ``:param:``/``:type:`` collapse to
        one line, while multi-line fields like ``:examples:`` keep their
        internal line breaks (important for doctest blocks).
        """
        ...

    def extract(self, raw: str, node: ast.AST) -> Dict[str, Any]:
        ...

    def render(self, data: 'DocstringData') -> str:
        ...

class PlainDialectHandler(DocstringDialectHandler):
    """Fallback for free-text docstrings with no recognized section markup.
    Preserves a summary/details split and any doctest examples, but does not
    impose ``Args:``/``:param:`` structure the original text didn't have.
    """
    name = 'plain'

    @classmethod
    def sniff(cls, raw: str) -> bool:
        ...

    def extract(self, raw: str, node: ast.AST) -> Dict[str, Any]:
        ...

    def render(self, data: 'DocstringData') -> str:
        ...
GOOGLE = GoogleDialectHandler()
SPHINX = SphinxDialectHandler()
PLAIN = PlainDialectHandler()
DIALECTS: Dict[str, DocstringDialectHandler] = {h.name: h for h in (GOOGLE, SPHINX, PLAIN)}
_SNIFF_ORDER: Tuple[DocstringDialectHandler, ...] = (SPHINX, GOOGLE)

def detect_dialect(raw: str, default: Optional[DocstringDialectHandler]=None) -> DocstringDialectHandler:
    """Pick the dialect handler that best matches `raw`.

    An empty/missing docstring has nothing to sniff, so it falls back to
    `default` (Google, richly-structured) since that's what a freshly written
    docstring will look like. Non-empty but unstructured text falls back to
    the Plain dialect so it isn't forced into a structure it never had.
    """
    ...

def resolve_dialect(dialect: str | DocstringDialectHandler | None, default=dev.default) -> DocstringDialectHandler | None:
    ...

def data_extractor(raw: str, node: ast.AST, dialect: Optional[DocstringDialectHandler]=None) -> Dict[str, Any]:
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
    ...

def _normalize_type(s: str) -> str:
    ...

def _signature_param_names(data: 'DocstringData'):
    ...

def default_exclude(qualname: str, package_name: Optional[str]=None) -> bool:
    """Default `exclude` predicate for `DocstringParser`/`DocstringsHandler`.

    True if any dotted component of `qualname` -- i.e. any class name or
    function/method name in its path, such as ``Widget`` or ``spin`` in
    ``Widget.spin`` -- starts with an underscore. Covers private names
    (``_helper``), private classes and everything under them, and other
    dunders (``__eq__``, ``__repr__``, ...) -- except ``__init__``, which
    is exempted since it's routinely the most useful method to document.
    """
    ...

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
    raw: str = ''
    short_description: str = ''
    details: str = ''
    examples: List[str] = field(default_factory=list)
    type_info: Dict[str, Any] = field(default_factory=lambda: {'params': {}, 'returns': {}})
    quality: Optional[Dict[str, Any]] = None
    dialect: str = ''
    related: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)

    def to_json(self) -> dict:
        """Return a plain, JSON-serializable dict of this record."""
        ...

    @classmethod
    def from_json(cls, d: dict) -> 'DocstringData':
        """Reconstruct a record from a dict produced by :meth:`to_json`."""
        ...

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

    def __init__(self, dialect: Optional[DocstringDialectHandler]=None, filter=None, exclude=default_exclude):
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
        ...

    def wanted(self, qualname: str, package_name: Optional[str]=None) -> bool:
        """True if `qualname` should actually be parsed, given this
        parser's `filter`/`exclude`."""
        ...

    def parse_source(self, src: str, only_missing: bool=False, package_name: Optional[str]=None) -> List[DocstringData]:
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
        ...

    def parse_file(self, path: str, only_missing: bool=False, package_name: Optional[str]=None) -> List[DocstringData]:
        """Read `path` and delegate to :meth:`parse_source`."""
        ...
DEFAULT_HEADER = ''

class DocstringWriter:
    """Write (possibly edited) :class:`DocstringData` records back into source.

    Each record renders via its own ``data.dialect`` handler by default, so a
    docstring parsed as Sphinx is written back as Sphinx and one parsed as
    Google comes back as Google -- pass `dialect` to force one convention for
    every record instead (e.g. to upgrade a whole file to Sphinx style).

    Guarantees, via :meth:`verify_code_identity`, that nothing except
    docstring text changes.
    """

    def __init__(self, header: str=DEFAULT_HEADER, add_header: bool=True, dialect: Optional[DocstringDialectHandler]=None):
        """
        Args:
            header (str): Line prepended to every rewritten docstring.
            add_header (bool): If False, no header is added.
            dialect (Optional[DocstringDialectHandler]): If given, every
                record is rendered with this handler regardless of its own
                ``dialect`` field.
        """
        ...
    default_dialect = SPHINX

    def _handler_for(self, data: DocstringData) -> DocstringDialectHandler:
        ...

    def _format_block(self, data: DocstringData) -> List[str]:
        ...

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
        ...

    def write_file(self, path: str, data_list: List[DocstringData], target: str=dev.default, backup: bool=None) -> tuple[str, str]:
        """Read `path`, apply `data_list`, and write the result back to `path`.

        Args:
            path (str): File to modify in place.
            data_list (List[DocstringData]): Records to write.
            backup (bool): If True (default), keep a ``<path>.docbak`` copy of
                the pre-rewrite source (only created the first time).

        Returns:
            str: The new source that was written.
        """
        ...

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
        ...

class DocstringQAField:
    issue_registry = {}
    tag_name = None
    default_short_name = None

    @classmethod
    def register(cls, name, method=None):
        ...
    __slots__ = ('description', 'score')
    default_description = None
    default_score = None

    def __init__(self, description=None, score=None):
        ...

    def __repr__(self):
        ...

    @property
    def short_name(self):
        ...

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

    def __init__(self, data: DocstringData, analyses=None):
        ...

    @property
    def default_analyses(self):
        ...

    def get_analyses(self):
        ...

    @classmethod
    def _check_doc_type(cls, typestr):
        ...

    @classmethod
    def _check_description(cls, data: DocstringData) -> list[DocstringQAField]:
        ...

    @classmethod
    def _check_undocumented_parameters(cls, data: DocstringData) -> list[DocstringQAField]:
        ...

    @classmethod
    def _check_stale_parameters(cls, data: DocstringData) -> list[DocstringQAField]:
        ...

    @classmethod
    def _check_return_values(cls, data: DocstringData) -> list[DocstringQAField]:
        ...

    @classmethod
    def _check_examples(cls, data: DocstringData) -> list[DocstringQAField]:
        ...

    @classmethod
    def _check_related(cls, data: DocstringData) -> list[DocstringQAField]:
        """Reward (not penalize) cross-referencing related functions/classes."""
        ...

    @classmethod
    def _check_links(cls, data: DocstringData) -> list[DocstringQAField]:
        """Reward (not penalize) including reference links."""
        ...

    def analyze_docstring_quality(self) -> tuple[dict[str, list[DocstringQAField]], int]:
        """Heuristically assess the quality of a parsed docstring."""
        ...

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
    name = 'docstring_quality'
    QUALITY_JSON_FILENAME = 'docstring_quality.json'
    SYNTAX_ERROR_WARNING_TEMPLATE = '[WARN] syntax error, skipping docstring QA: {rel_path}: {error}'
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
        ...

    def _iter_py_files(self, pkg_src_path):
        """Yield (full_path, rel_path) for every .py file under a package's
        source -- rel_path is relative to pkg_src_path for a package
        directory, or just the bare filename for a single-file package."""
        ...
    _SIMPLIFY_BY_DESCRIPTION = frozenset({'stale'})
    _SIMPLIFY_BY_TYPE = frozenset({'parameters', 'returns', 'descriptions'})

    @staticmethod
    def _issue_to_json(issue: DocstringQAField) -> dict:
        ...

    def _simplified_issues(self, tag, issues):
        """Drop any issue with a positive score -- those are bonuses (e.g.
        `HasExamples`), not problems, and don't belong in an `issues`
        listing -- then simplify what's left: `stale` collapses to its
        deduplicated `description`s, `parameters`/`returns` collapse to
        their deduplicated `type` names, and everything else keeps the
        full {type, description, score} form."""
        ...

    def _score_file(self, full_path, rel_path, package_name):
        ...

    def parse(self, package_name, pkg_src_path):
        """Score every docstring under `pkg_src_path`; safe against any one
        file failing to read/parse (best-effort -- one bad module shouldn't
        drop QA data for the rest of the package; its error is recorded
        under `errors` instead). Functions/methods ruled out by `filter`/
        `exclude` are never parsed in the first place -- see
        `DocstringParser.wanted`."""
        ...

    def write(self, components, compact=True):
        """Aggregate every package's `parse()` result into a single
        docstring_quality.json at the root of out_dir."""
        ...