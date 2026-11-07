"""
The report document: an ordered list of typed blocks, edited only through validated operations.

A `ReportDocument` is what a person, a script, a staged harness or a model with tools all edit. Every operation
validates its arguments against the document and the `SourceCatalog` *before* changing anything, and fails with a
`ReportOperationError` whose ``code`` and ``detail`` say what was wrong, so a caller (a model included) can correct
itself. The document serializes to Markdown (`to_markdown`/`from_markdown`, an exact round trip) in the readout
marker format of `McUtils.Docs`, so the same text renders to HTML through the docs pipeline; `to_readout` builds
the equivalent `Readout` tree for PowerPoint and plain-text export.
"""

import ast
import contextlib
import datetime
import json
import re

from ..Nodes import Readout, ReadoutSection, ReadoutText
from ..Views import as_readout_node
from .Sources import ReportSourceError
from .History import DocumentSnapshot, diff_snapshots

__all__ = [
    "ReportOperationError",
    "Receipt",
    "Heading",
    "ReadoutBlock",
    "Prose",
    "PROSE_BASES",
    "Callout",
    "RawMarkdown",
    "ReportDocument",
]

FORMAT = "mcr-report-v1"
HEADING_CHARS = 80
CAPTION_CHARS = 300
CAPTION_STATUSES = ("checked", "no_numbers", "unchecked", "manual", "template")
PROSE_STATUSES = ("checked", "no_numbers", "unchecked", "manual")
# ``checked``: at least one number in the text was verified against the cited data; ``no_numbers``: the text passed
# the number check but has nothing to check; ``grounded`` is the older
# name of ``checked`` and is still read and accepted.
LEGACY_STATUSES = {"grounded": "checked"}
# what a paragraph says it is about: ``data`` (the readouts it cites), ``background`` (general context, no data) or
# ``user_input`` (values the user gave); ``None`` is unspecified
PROSE_BASES = ("data", "background", "user_input")


def _status(status):
    return LEGACY_STATUSES.get(status, status)
ERROR_CODES = ("unknown_block", "unknown_source", "unknown_section", "unavailable_section",
               "bad_argument", "bad_position", "invalid_document", "locked", "needs_citation", "bad_reference",
               "derived_disabled", "unit_mismatch")


class ReportOperationError(ValueError):
    """
    An operation was refused.

    :ivar code: one of ``unknown_block, unknown_source, unknown_section, unavailable_section, bad_argument,
        bad_position, invalid_document``
    :ivar detail: a sentence saying what was wrong and (where possible) what would be accepted
    :ivar info: extra fields (the offending value, the valid choices)
    """

    def __init__(self, code, detail, **info):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.info = info

    def to_dict(self):
        return {"code": self.code, "detail": self.detail, **self.info}


class Receipt:
    """What a mutating operation returns: whether it worked, the block it touched, and the new outline."""

    def __init__(self, block_id, outline, ok=True):
        self.ok = ok
        self.block_id = block_id
        self.outline = outline

    def to_dict(self):
        return {"ok": self.ok, "block_id": self.block_id, "outline": self.outline}

    def __repr__(self):
        return f"Receipt(ok={self.ok}, block_id={self.block_id!r}, blocks={len(self.outline)})"


# ------------------------------------------------------------------------------------------------ #
#  literals in marker comments
# ------------------------------------------------------------------------------------------------ #
def _escape_comment(s):
    """Makes text safe inside an HTML comment without changing what it means as a JSON/Python string."""
    return s.replace("--", "\\u002d\\u002d").replace(">", "\\u003e")


def _lit(value):
    """A Python/JSON-compatible literal for a marker argument (strings are comment-safe)."""
    if value is None or isinstance(value, bool):
        return repr(value)
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return _escape_comment(json.dumps(value, ensure_ascii=False))
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(_lit(v) for v in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(f"{_lit(k)}:{_lit(v)}" for k, v in value.items()) + "}"
    raise TypeError(f"can't write {type(value).__name__} in a marker")


def _call(name, ident, **kw):
    """``name(ident, key=value, ...)`` with only literal values; ``None`` values are left out."""
    parts = [ident] if ident is not None else []
    parts += [f"{k}={_lit(v)}" for k, v in kw.items() if v is not None]
    return f"<!-- {name}({', '.join(parts)}) -->"


def _parse_call(text, name):
    """Parses ``name(ident, key=literal, ...)`` -> ``(ident, {key: value})`` (literals only, through `ast`)."""
    try:
        call = ast.parse(text.strip(), mode="eval").body
    except SyntaxError as e:
        raise ReportOperationError("invalid_document", f"can't parse the {name} marker {text!r}: {e.msg}")
    if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Name) or call.func.id != name:
        raise ReportOperationError("invalid_document", f"expected a {name}(...) marker, got {text!r}")
    ident = None
    if call.args:
        a = call.args[0]
        if len(call.args) > 1:
            raise ReportOperationError("invalid_document", f"{name} marker takes one positional id: {text!r}")
        if isinstance(a, ast.Name):
            ident = a.id
        else:
            try:
                ident = ast.literal_eval(a)
            except ValueError:
                raise ReportOperationError("invalid_document", f"{name} marker id must be a name: {text!r}")
    kw = {}
    for k in call.keywords:
        if k.arg is None:
            raise ReportOperationError("invalid_document", f"{name} marker can't use **: {text!r}")
        try:
            kw[k.arg] = ast.literal_eval(k.value)
        except ValueError:
            raise ReportOperationError("invalid_document", f"{name} option {k.arg!r} must be a literal: {text!r}")
    return ident, kw


def _escape_caption(text):
    return re.sub(r"([\\*_])", r"\\\1", text)


def _unescape_caption(text):
    return re.sub(r"\\([\\*_])", r"\1", text)


# ------------------------------------------------------------------------------------------------ #
#  blocks
# ------------------------------------------------------------------------------------------------ #
class _Block:
    kind = None
    prefix = None

    def __init__(self, id):
        self.id = id


class Heading(_Block):
    kind, prefix = "heading", "h"

    def __init__(self, id, text, level=2):
        super().__init__(id)
        self.text, self.level = text, level

    def to_markdown(self, doc):
        return f"{_call('block', self.id, level=self.level)}\n{'#' * self.level} {self.text}"


class ReadoutBlock(_Block):
    """A readout of a catalog source: which sections, in which units, and an optional caption."""
    kind, prefix = "readout", "r"

    def __init__(self, id, handle, include=None, exclude=None, units=None, style=None, display="readout",
                 caption=None, caption_status=None, header=False):
        super().__init__(id)
        self.handle, self.include, self.exclude = handle, include, exclude
        self.units, self.style, self.display = units, style, display
        self.caption, self.caption_status = caption, _status(caption_status)
        self.header = bool(header)    # show the readout's own title block (title, subtitle, units)?

    def to_markdown(self, doc):
        opts = {"include": self.include, "exclude": self.exclude, "units": self.units, "style": self.style,
                "display": None if self.display == "readout" else self.display}
        marker = _call("readout", None, id=self.id, **opts, header=self.header, show_code=False, isolated=True)
        digest = doc.source_digest(self.handle)
        body = f"report_source({_lit(self.handle)}, digest={_lit(digest)})"
        out = f"{marker}\n```python\n{body}\n```"
        if self.caption:
            out += f"\n\n{_call('caption', self.id, status=self.caption_status or 'manual')}\n*{_escape_caption(self.caption)}*"
        return out


class Prose(_Block):
    """
    A paragraph. ``fills`` records the values the server wrote into it (placeholders and given values, see
    `McUtils.Readouts.Reports.Fill`); ``basis`` is what it says it is about (`PROSE_BASES`) or ``None``.
    """
    kind, prefix = "prose", "p"

    def __init__(self, id, text, cites=(), status="manual", role="body", fills=None, basis=None):
        super().__init__(id)
        self.text, self.cites, self.status, self.role = text, list(cites), _status(status), role
        self.fills = list(fills) if fills else None
        self.basis = basis

    def to_markdown(self, doc):
        marker = _call("block", self.id, role=self.role, status=self.status, cites=self.cites or None,
                       fills=self.fills or None, basis=self.basis)
        return f"{marker}\n{self.text}"


class Callout(_Block):
    kind, prefix = "callout", "c"

    def __init__(self, id, text, callout_kind="note"):
        super().__init__(id)
        self.text, self.callout_kind = text, callout_kind

    def to_markdown(self, doc):
        return f"{_call('block', self.id, kind=self.callout_kind)}\n> **{self.callout_kind.capitalize()}:** {self.text}"


class RawMarkdown(_Block):
    """Hand-written Markdown the document model doesn't classify; kept verbatim."""
    kind, prefix = "raw", "x"

    def __init__(self, id, text):
        super().__init__(id)
        self.text = text

    def to_markdown(self, doc):
        return f"{_call('block', self.id)}\n{self.text}"


_PREFIXES = {c.prefix: c for c in (Heading, ReadoutBlock, Prose, Callout, RawMarkdown)}


def _clip(text, n=80):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n - 1] + "…"


# ------------------------------------------------------------------------------------------------ #
#  the document
# ------------------------------------------------------------------------------------------------ #
class ReportDocument:
    """
    :param title: the report's title (one line)
    :param catalog: the `SourceCatalog` readout blocks are validated and rendered against
    :param meta: free-form provenance (writing policy, template, ledger path, ...); stored in the Markdown
    :param block_headers: whether new readout blocks show their readout's own title block (title, subtitle,
        units) in the output. Off by default: the report's headings and captions label the blocks instead. Each
        block can override it (``add_readout(header=True)``) and carries its own setting in the Markdown.
    """
    FORMAT = FORMAT

    def __init__(self, title, catalog=None, meta=None, created=None, block_headers=False):
        title = self._check_line(title, "title", HEADING_CHARS)
        self.title = title
        self.catalog = catalog
        self.meta = dict(meta or {})
        self.created = created or datetime.date.today().isoformat()
        self.block_headers = bool(block_headers)   # default for new readout blocks: show each readout's own title block?
        self.sources = {}      # handle -> {"type": ..., "digest": ...}: what the report recorded
        self.blocks = []
        self._counters = {}

    # ---- helpers ---------------------------------------------------------------------------- #
    @staticmethod
    def _check_line(text, what, limit):
        if not isinstance(text, str):
            raise ReportOperationError("bad_argument", f"{what} must be a string, got {type(text).__name__}")
        text = text.strip()
        if not text:
            raise ReportOperationError("bad_argument", f"{what} is empty")
        if "\n" in text or "\r" in text:
            raise ReportOperationError("bad_argument", f"{what} must be a single line")
        if len(text) > limit:
            raise ReportOperationError("bad_argument", f"{what} is {len(text)} characters; the limit is {limit}",
                                       limit=limit)
        if "<!--" in text:
            raise ReportOperationError("bad_argument", f"{what} can't contain an HTML comment")
        return text

    @classmethod
    def _check_heading(cls, text):
        text = cls._check_line(text, "heading text", HEADING_CHARS)
        if text.startswith("#"):
            raise ReportOperationError("bad_argument", "heading text is plain text without '#' (the level is a "
                                       "separate argument)")
        return text

    @staticmethod
    def _check_text(text, what):
        if not isinstance(text, str):
            raise ReportOperationError("bad_argument", f"{what} must be a string, got {type(text).__name__}")
        text = text.strip("\n").strip()
        if not text:
            raise ReportOperationError("bad_argument", f"{what} is empty")
        if "<!--" in text:
            raise ReportOperationError("bad_argument", f"{what} can't contain an HTML comment")
        if any(line.startswith("#") for line in text.split("\n")):
            raise ReportOperationError("bad_argument", f"{what} can't contain a line starting with '#' "
                                       f"(use add_heading for headings)")
        return text

    def _mint(self, cls):
        n = self._counters.get(cls.prefix, 0) + 1
        self._counters[cls.prefix] = n
        return f"{cls.prefix}{n}"

    def _note_id(self, id):
        m = re.match(r"^([a-z])(\d+)$", id or "")
        if m:
            self._counters[m.group(1)] = max(self._counters.get(m.group(1), 0), int(m.group(2)))

    def _index(self, block_id):
        for i, b in enumerate(self.blocks):
            if b.id == block_id:
                return i
        raise ReportOperationError("unknown_block", f"no block {block_id!r}; the blocks are "
                                   f"{[b.id for b in self.blocks]}", block_id=block_id)

    def _position(self, after):
        if after is None:
            return len(self.blocks)
        if after == "start":
            return 0
        for i, b in enumerate(self.blocks):
            if b.id == after:
                return i + 1
        raise ReportOperationError("bad_position", f"after={after!r} is not 'start' or the id of a block; the "
                                   f"blocks are {[b.id for b in self.blocks]}", after=after)

    def _where(self, after, under):
        """The ``after`` to use: ``under`` (a heading id) means after the last block of that heading's section."""
        if under is None:
            return after
        if after is not None:
            raise ReportOperationError("bad_argument", "give either `after` or `under`, not both")
        return self.section_end(under)

    def section_end(self, heading_id):
        """
        The id of the last block of the section that starts at heading ``heading_id``: the blocks that follow it up to
        (not including) the next heading of the same or a higher level. A heading with nothing under it returns
        its own id.
        """
        i = self._index(heading_id)
        head = self.blocks[i]
        if not isinstance(head, Heading):
            raise ReportOperationError("bad_argument", f"block {heading_id!r} is a {head.kind} block, not a heading; "
                                       f"sections start at headings", block_id=heading_id)
        j = i + 1
        while j < len(self.blocks) and not (isinstance(self.blocks[j], Heading) and self.blocks[j].level <= head.level):
            j += 1
        return self.blocks[j - 1].id

    def section_ids(self, heading_id):
        """The ids of the heading and every block in its section, in order."""
        end = self.section_end(heading_id)
        i, j = self._index(heading_id), self._index(end)
        return [b.id for b in self.blocks[i:j + 1]]

    def _insert(self, block, after):
        pos = self._position(after)
        self.blocks.insert(pos, block)
        return Receipt(block.id, self.outline())

    def source_digest(self, handle):
        rec = self.sources.get(handle)
        if rec is not None:
            return rec["digest"]
        if self.catalog is not None and handle in self.catalog:
            return self.catalog.get(handle).digest
        raise ReportOperationError("unknown_source", f"no recorded source {handle!r}", handle=handle)

    # ---- operations ------------------------------------------------------------------------- #
    def add_heading(self, text, level=2, after=None, under=None):
        after = self._where(after, under)
        text = self._check_heading(text)
        if level not in (2, 3):
            raise ReportOperationError("bad_argument", f"heading level must be 2 or 3, got {level!r}")
        self._position(after)
        return self._insert(Heading(self._mint(Heading), text, level), after)

    def _check_sections(self, handle, include, exclude):
        if self.catalog is None or handle not in self.catalog:
            known = self.catalog.handles() if self.catalog is not None else []
            raise ReportOperationError("unknown_source", f"no source {handle!r}; the sources are {known}",
                                       handle=handle, choices=known)
        src = self.catalog.get(handle)
        rows = {r["name"]: r for r in src.sections()}
        names = list(rows)
        for what, group in (("include", include), ("exclude", exclude)):
            if group is None:
                continue
            if isinstance(group, str) or not all(isinstance(g, str) for g in group):
                raise ReportOperationError("bad_argument", f"{what} must be a list of section names")
            if what == "include" and not group:
                raise ReportOperationError("bad_argument", "include is empty; use None for the default sections")
            for name in group:
                head = name.split(".", 1)[0]
                if head not in rows:
                    raise ReportOperationError("unknown_section", f"source {handle!r} has no section {name!r}; "
                                               f"its sections are {names}", handle=handle, section=name, choices=names)
                if "." in name and rows[head]["available"] and not src.is_record:
                    if src.section_kind(name) == "unknown":
                        raise ReportOperationError("unknown_section", f"source {handle!r} has no section {name!r}: "
                                                   f"{src.kind_error(name)}", handle=handle, section=name,
                                                   choices=names)
                if what == "include" and not rows[head]["available"]:
                    raise ReportOperationError("unavailable_section", f"section {name!r} of {handle!r} is not "
                                               f"available: {rows[head].get('reason') or 'required data is missing'}",
                                               handle=handle, section=name)
        return src

    def add_readout(self, handle, include=None, exclude=None, units=None, style=None, caption=None, after=None,
                    header=None, under=None):
        after = self._where(after, under)
        src = self._check_sections(handle, include, exclude)
        include = None if include is None else list(include)
        exclude = None if exclude is None else list(exclude)
        if src.is_record:
            if include is not None and include != ["record"]:
                raise ReportOperationError("unknown_section", f"source {handle!r} is a plain record; its only "
                                           f"section is 'record'", handle=handle, choices=["record"])
            include = None
            if exclude:
                raise ReportOperationError("unknown_section", f"source {handle!r} is a plain record with no "
                                           f"sections to exclude", handle=handle)
        for what, v in (("units", units), ("style", style)):
            if v is not None and not isinstance(v, (str, dict)):
                raise ReportOperationError("bad_argument", f"{what} must be a string or a dict")
        if caption is not None:
            caption = self._check_line(caption, "caption", CAPTION_CHARS)
        if header is not None and not isinstance(header, bool):
            raise ReportOperationError("bad_argument", "header must be True, False or None (the document default)")
        self._position(after)
        block = ReadoutBlock(self._mint(ReadoutBlock), handle, include, exclude, units, style,
                             caption=caption, caption_status="manual" if caption else None,
                             header=self.block_headers if header is None else header)
        self.sources[handle] = {"type": src.type_name, "digest": src.digest}
        return self._insert(block, after)

    @staticmethod
    def _check_basis(basis):
        if basis is not None and basis not in PROSE_BASES:
            raise ReportOperationError("bad_argument", f"basis must be one of {PROSE_BASES} or left out, got {basis!r}")
        return basis

    def add_text(self, text, cites=(), after=None, status="manual", role="body", under=None, fills=None, basis=None):
        after = self._where(after, under)
        text = self._check_text(text, "text")
        basis = self._check_basis(basis)
        status = _status(status)
        if status not in PROSE_STATUSES:
            raise ReportOperationError("bad_argument", f"status must be one of {PROSE_STATUSES}, got {status!r}")
        if role not in ("body", "summary"):
            raise ReportOperationError("bad_argument", f"role must be 'body' or 'summary', got {role!r}")
        cites = list(cites or ())
        for c in cites:
            if not any(b.id == c and isinstance(b, ReadoutBlock) for b in self.blocks):
                raise ReportOperationError("unknown_block", f"cited block {c!r} is not a readout block of this "
                                           f"document", block_id=c)
        self._position(after)
        return self._insert(Prose(self._mint(Prose), text, cites, status, role, fills, basis), after)

    def add_callout(self, text, kind="note", after=None, under=None):
        after = self._where(after, under)
        text = self._check_line(text, "callout text", 600)
        if kind not in ("flag", "note"):
            raise ReportOperationError("bad_argument", f"callout kind must be 'flag' or 'note', got {kind!r}")
        self._position(after)
        return self._insert(Callout(self._mint(Callout), text, kind), after)

    def set_caption(self, block_id, text, status="manual"):
        block = self.blocks[self._index(block_id)]
        if not isinstance(block, ReadoutBlock):
            raise ReportOperationError("bad_argument", f"block {block_id!r} is a {block.kind} block; only "
                                       f"readout blocks have captions", block_id=block_id)
        status = _status(status)
        if status not in CAPTION_STATUSES:
            raise ReportOperationError("bad_argument", f"status must be one of {CAPTION_STATUSES}, got {status!r}")
        text = self._check_line(text, "caption", CAPTION_CHARS)
        block.caption, block.caption_status = text, status
        return Receipt(block_id, self.outline())

    def edit_text(self, block_id, text, status="manual", cites=None, fills=None, basis=None):
        block = self.blocks[self._index(block_id)]
        if isinstance(block, Prose):
            if basis is not None:
                block.basis = self._check_basis(basis)
            if cites is not None:
                cites = list(cites)
                for c in cites:
                    if not any(b.id == c and isinstance(b, ReadoutBlock) for b in self.blocks):
                        raise ReportOperationError("unknown_block", f"cited block {c!r} is not a readout block of "
                                                   f"this document", block_id=c)
                block.cites = cites
            status = _status(status)
            if status not in PROSE_STATUSES:
                raise ReportOperationError("bad_argument", f"status must be one of {PROSE_STATUSES}, got {status!r}")
            block.text = self._check_text(text, "text")
            block.status = status
            block.fills = list(fills) if fills else None
        elif isinstance(block, Callout):
            block.text = self._check_line(text, "callout text", 600)
        elif isinstance(block, Heading):
            block.text = self._check_heading(text)
        else:
            raise ReportOperationError("bad_argument", f"block {block_id!r} is a {block.kind} block; text can "
                                       f"be edited on prose, callout and heading blocks", block_id=block_id)
        return Receipt(block_id, self.outline())

    def move(self, block_id, after):
        i = self._index(block_id)
        if after == block_id:
            raise ReportOperationError("bad_position", "a block can't be moved after itself", after=after)
        block = self.blocks.pop(i)
        try:
            pos = self._position(after)
        except ReportOperationError:
            self.blocks.insert(i, block)
            raise
        self.blocks.insert(pos, block)
        return Receipt(block_id, self.outline())

    def move_section(self, heading_id, after):
        """
        Move a heading together with the blocks of its section (see `section_end`). ``after`` is ``"start"`` or a
        block id; if it is a heading, the section goes after that heading's whole section. Moving a section into
        itself is an error.
        """
        ids = self.section_ids(heading_id)
        if after in ids:
            raise ReportOperationError("bad_position", f"a section can't be moved into itself (after={after!r})",
                                       after=after)
        if after != "start" and after is not None:
            self._position(after)
            if isinstance(self.get(after), Heading):
                after = self.section_end(after)
        i, j = self._index(heading_id), self._index(ids[-1])
        moving = self.blocks[i:j + 1]
        del self.blocks[i:j + 1]
        try:
            pos = self._position(after)
        except ReportOperationError:
            self.blocks[i:i] = moving
            raise
        self.blocks[pos:pos] = moving
        return Receipt(heading_id, self.outline())

    # ---- source groups: the sections that show one source -------------------------------------- #
    def _top_sections(self):
        """``[(heading id, [block ids of its section])]`` for every level-2 heading, in order."""
        return [(b.id, self.section_ids(b.id)) for b in self.blocks if isinstance(b, Heading) and b.level == 2]

    def section_sources(self, heading_id):
        """The handles of the readout blocks in the section of ``heading_id``, in order of appearance."""
        return list(dict.fromkeys(self.get(i).handle for i in self.section_ids(heading_id)
                                  if isinstance(self.get(i), ReadoutBlock)))

    def source_sections(self, handle):
        """The level-2 heading ids whose sections show only ``handle`` (at least one readout of it), in order."""
        return [h for h, ids in self._top_sections() if self.section_sources(h) == [handle]]

    def move_source(self, handle, after):
        """
        Move every level-2 section that shows only source ``handle`` (`source_sections`) together, in their current
        order, to ``after`` (``"start"`` or a block id; a heading id means after that heading's whole section).
        This is how two sources' parts of a report are swapped: one call per source.
        """
        heads = self.source_sections(handle)
        if not heads:
            raise ReportOperationError("bad_argument", f"no section of the report shows only source {handle!r}",
                                       handle=handle, choices=self.handles_shown())
        ids = [i for h in heads for i in self.section_ids(h)]
        if after in ids:
            raise ReportOperationError("bad_position", f"after={after!r} is inside the sections being moved",
                                       after=after)
        if after != "start" and after is not None:
            self._position(after)
            if isinstance(self.get(after), Heading):
                after = self.section_end(after)
        keep = set(ids)
        moving = [b for b in self.blocks if b.id in keep]
        before = list(self.blocks)
        self.blocks = [b for b in self.blocks if b.id not in keep]
        try:
            pos = self._position(after)
        except ReportOperationError:
            self.blocks = before
            raise
        self.blocks[pos:pos] = moving
        return Receipt(heads[0], self.outline())

    def handles_shown(self):
        """The sources the report's readout blocks show, in order of first appearance."""
        return list(dict.fromkeys(b.handle for b in self.blocks if isinstance(b, ReadoutBlock)))

    def grouping_warnings(self):
        """
        Sources whose sections are split up by another source's sections (for example HOD Structure, HOH Structure,
        HOH Vibrations, HOD Vibrations): ``[{"code": "interleaved", "handle", "sections", "detail"}]``. Only
        sections that show a single source count.
        """
        seq = [(h, self.section_sources(h)) for h, _ in self._top_sections()]
        seq = [(h, srcs[0]) for h, srcs in seq if len(srcs) == 1]
        out = []
        for handle in dict.fromkeys(src for _, src in seq):
            pos = [i for i, (_, src) in enumerate(seq) if src == handle]
            if pos[-1] - pos[0] + 1 != len(pos):
                heads = [seq[i][0] for i in pos]
                between = sorted({seq[i][1] for i in range(pos[0], pos[-1]) if seq[i][1] != handle})
                out.append({"code": "interleaved", "handle": handle, "sections": heads,
                            "detail": f"the sections of {handle!r} ({', '.join(heads)}) are split by sections of "
                                      f"{between}; move_source({handle!r}, ...) moves them together"})
        return out

    def remove(self, block_id):
        i = self._index(block_id)
        block = self.blocks.pop(i)
        for b in self.blocks:
            if isinstance(b, Prose) and block_id in b.cites:
                b.cites = [c for c in b.cites if c != block_id]
        return Receipt(block_id, self.outline())

    # ---- queries ---------------------------------------------------------------------------- #
    def get(self, block_id):
        return self.blocks[self._index(block_id)]

    def outline(self):
        rows = []
        for b in self.blocks:
            row = {"id": b.id, "kind": b.kind}
            if isinstance(b, Heading):
                row.update(level=b.level, text=b.text)
            elif isinstance(b, ReadoutBlock):
                row.update(handle=b.handle, include=b.include)
                if b.caption:
                    row["caption"] = _clip(b.caption)
            elif isinstance(b, Prose):
                row.update(role=b.role, text=_clip(b.text))
                if b.basis:
                    row["basis"] = b.basis
            elif isinstance(b, Callout):
                row.update(callout=b.callout_kind, text=_clip(b.text))
            else:
                row.update(text=_clip(b.text))
            rows.append(row)
        return rows

    def sections(self):
        """``[(level-2 Heading or None, [blocks])]``; blocks before the first level-2 heading come first under ``None``."""
        groups, current = [], (None, [])
        for b in self.blocks:
            if isinstance(b, Heading) and b.level == 2:
                if current[0] is not None or current[1]:
                    groups.append(current)
                current = (b, [])
            else:
                current[1].append(b)
        if current[0] is not None or current[1]:
            groups.append(current)
        return groups

    def refresh_sources(self):
        """Adopt the catalog's current digests; returns the handles whose recorded digest changed."""
        changed = []
        for handle, rec in self.sources.items():
            if self.catalog is not None and handle in self.catalog:
                src = self.catalog.get(handle)
                if rec["digest"] != src.digest:
                    changed.append(handle)
                rec["digest"], rec["type"] = src.digest, src.type_name
        return changed

    def validate(self):
        """Every problem found, as `ReportOperationError`s (an empty list means the document is sound)."""
        problems = []
        seen = set()
        for b in self.blocks:
            if b.id in seen:
                problems.append(ReportOperationError("invalid_document", f"block id {b.id!r} is used twice",
                                                     block_id=b.id))
            seen.add(b.id)
        readouts = {b.id for b in self.blocks if isinstance(b, ReadoutBlock)}
        for b in self.blocks:
            if isinstance(b, Prose):
                for c in b.cites:
                    if c not in readouts:
                        problems.append(ReportOperationError("unknown_block", f"block {b.id!r} cites {c!r}, which "
                                                             f"is not a readout block", block_id=c))
            if isinstance(b, ReadoutBlock) and self.catalog is not None:
                if b.handle not in self.catalog:
                    problems.append(ReportOperationError("unknown_source", f"block {b.id!r} uses source "
                                                         f"{b.handle!r}, which is not in the catalog",
                                                         block_id=b.id, handle=b.handle))
                    continue
                try:
                    self._check_sections(b.handle, b.include, b.exclude)
                except ReportOperationError as e:
                    e.info.setdefault("block_id", b.id)
                    problems.append(e)
                recorded = self.sources.get(b.handle, {}).get("digest")
                current = self.catalog.get(b.handle).digest
                if recorded is not None and recorded != current:
                    problems.append(ReportOperationError(
                        "invalid_document", f"source {b.handle!r} has changed since the report was written "
                        f"(recorded digest {recorded}, catalog digest {current}); call refresh_sources() to adopt it",
                        problem="digest_mismatch", block_id=b.id, handle=b.handle))
        return problems

    # ---- templates --------------------------------------------------------------------------- #
    def apply_template(self, handle, after=None, optional=(), lock=True):
        """
        Build the report template's fixed outline for a source: its headings and readout blocks in the template's order,
        with the template's captions (status ``template``). Sections that are unavailable for the source are skipped.

        :param optional: names from the template's ``optional`` list to add under an "Additional detail" heading
        :param lock: lock the blocks the template locks (see `lock`)
        :return: ``{"added": [block ids], "locked": [block ids], "skipped_unavailable": [section names]}``
        """
        from .Templates import find_report_template
        if self.catalog is None:
            raise ReportOperationError("bad_argument", "this document has no catalog to take a template from")
        src = self.catalog.get(handle)
        tmpl = find_report_template(src)
        if not tmpl.is_fixed:
            raise ReportOperationError("no_template", f"source {handle!r} has no fixed template outline "
                                       f"(template {tmpl.name!r}); build the report with add_heading and add_readout",
                                       handle=handle)
        extra = list(optional or [])
        bad = [n for n in extra if n not in tmpl.optional]
        if bad:
            raise ReportOperationError("unknown_section", f"{bad} are not optional sections of template {tmpl.name!r}; "
                                       f"the choices are {list(tmpl.optional)}", handle=handle,
                                       choices=list(tmpl.optional))
        rows = {r["name"]: r for r in src.sections()}
        plan = [(h, list(ns)) for h, ns in tmpl.sections]
        if extra:
            plan.append(("Additional detail", extra))
        added, skipped, locks, pos = [], [], [], after
        with self.transaction():
            for heading, names in plan:
                usable = [n for n in names if rows.get(n.split(".", 1)[0], {}).get("available", False)]
                skipped += [n for n in names if n not in usable]
                if not usable:
                    continue
                pos = self.add_heading(heading, after=pos).block_id
                added.append(pos)
                if heading in tmpl.locked_headings:
                    locks.append(pos)
                for n in usable:
                    cap = tmpl.caption_for(handle, n, src)
                    pos = self.add_readout(handle, include=[n], after=pos).block_id
                    if cap:
                        self.set_caption(pos, cap, status="template")
                    added.append(pos)
                    if tmpl.locks(heading, n):
                        locks.append(pos)
            if lock and locks:
                self.lock(locks)
        return {"added": added, "locked": locks if lock else [], "skipped_unavailable": skipped}

    @classmethod
    def from_template(cls, title, catalog, handle, optional=(), **kwargs):
        """A new document holding the template outline of one source (see `apply_template`); ``kwargs`` go to the constructor."""
        doc = cls(title, catalog, **kwargs)
        doc.apply_template(handle, optional=optional)
        return doc

    # ---- locking: a note that some blocks should be left alone --------------------------------- #
    # The document's own operations never refuse a locked block (so a person can always edit it); the tools offered
    # to a model (`report_toolset`) do, via `check_unlocked`.
    @property
    def locked(self):
        """Ids of the locked blocks that are in the document, in the order they were locked."""
        present = {b.id for b in self.blocks}
        return [i for i in self.meta.get("locked", []) if i in present]

    @property
    def unit_style(self):
        """The unit label style filled values are written in (``"unicode"``, ``"ascii"``, ``"latex"``), stored in the
        report's ``report-meta``; ``None`` means `UnitsData.label_style`. Fills already written keep their own style."""
        return self.meta.get("unit_style")

    @unit_style.setter
    def unit_style(self, style):
        if style is None:
            self.meta.pop("unit_style", None)
        else:
            from ...Data import UnitsData
            self.meta["unit_style"] = UnitsData.check_label_style(style)

    def is_locked(self, block_id):
        return block_id in self.meta.get("locked", ())

    def lock(self, block_ids):
        """Lock blocks (saved with the report in its ``report-meta`` header). Returns the locked ids."""
        for b in block_ids:
            self._index(b)
        have = list(self.meta.get("locked", []))
        self.meta["locked"] = have + [b for b in dict.fromkeys(block_ids) if b not in have]
        return self.locked

    def unlock(self, block_ids=None):
        """Unlock ``block_ids`` (every block if ``None``). Returns the ids still locked."""
        keep = [] if block_ids is None else [b for b in self.meta.get("locked", []) if b not in set(block_ids)]
        if keep:
            self.meta["locked"] = keep
        else:
            self.meta.pop("locked", None)
        return self.locked

    def check_unlocked(self, block_id):
        """Raise ``ReportOperationError("locked")`` if ``block_id`` is locked."""
        if self.is_locked(block_id):
            raise ReportOperationError("locked", f"block {block_id!r} is locked: it can't be edited, captioned, moved "
                                       f"or removed. You can add text or other blocks after it.", block_id=block_id)

    # ---- history ---------------------------------------------------------------------------- #
    def snapshot(self):
        """An independent `DocumentSnapshot` of the document as it is now."""
        return DocumentSnapshot(self)

    def restore(self, snapshot):
        """Put the document back to a snapshot."""
        snapshot.restore(self)

    def diff(self, since):
        """What changed since ``since`` (a `snapshot`): a list of added, removed, changed and moved blocks."""
        return diff_snapshots(since, self.snapshot())

    @contextlib.contextmanager
    def transaction(self):
        """``with doc.transaction(): ...`` — if the block raises, the document is restored and the error propagates."""
        before = self.snapshot()
        try:
            yield self
        except BaseException:
            self.restore(before)
            raise

    # ---- text checks ------------------------------------------------------------------------ #
    def text_status(self):
        """How many captions and paragraphs have each status: ``{"checked": n, "no_numbers": n, "template": n, ...}``."""
        counts = {}
        for b in self.blocks:
            st = b.caption_status if isinstance(b, ReadoutBlock) and b.caption else b.status if isinstance(b, Prose) else None
            if st:
                counts[st] = counts.get(st, 0) + 1
        return counts

    def check_text(self, text, cites=(), rel_tol=1e-3, small_int_max=10, max_chars=4000, year_range=(1900, 2100),
                   skip=(), extra=(), items=None):
        """
        Check the numbers of ``text`` against the data of the readout blocks ``cites``
        (see `McUtils.Readouts.Reports.check_grounding`). Returns a `GroundingResult` (``ok``, ``unmatched``, and
        ``matches``: which cited value each number matched). The match is unit- and quantity-aware: a number written
        with a unit only matches a value in that unit, and a percentage never matches an index, a count or a value
        with a unit. Four-digit integers inside ``year_range`` are taken to be years and not checked unless they carry
        a unit; pass ``None`` to check them (they overlap vibrational frequencies such as 1948 or 2000 cm-1).
        ``skip`` are spans of ``text`` not to check; ``extra`` are more `EvidenceItem`s (values the server derived);
        ``items`` is the `EvidenceSet` of ``cites`` if the caller has it already (`evidence`).
        """
        from .Grounding import evidence_items, check_grounding
        if items is None:
            items = self.evidence(cites, max_chars=max_chars)
        items.extend(extra)
        return check_grounding(text, items, rel_tol=rel_tol, small_int_max=small_int_max,
                               year_range=(1, 0) if year_range is None else year_range, skip=skip)

    def evidence(self, cites, max_chars=4000):
        """The `EvidenceSet` of the readout blocks ``cites``: their data (with units and labels) and their section text."""
        from .Grounding import evidence_items
        texts, readouts = [], []
        for c in cites:
            blk = self.get(c)
            if not isinstance(blk, ReadoutBlock):
                raise ReportOperationError("bad_argument", f"block {c!r} is a {blk.kind} block; only readout blocks "
                                           f"have data to check against", block_id=c)
            src = self.catalog.get(blk.handle)
            readouts.append((c, src.readout(include=blk.include, exclude=blk.exclude)))
            for name in (blk.include or src.default_sections()):
                try:
                    texts.append((c, src.section_text(name, max_chars=max_chars)))
                except Exception:  # noqa: BLE001 - a section that can't render has no text evidence
                    pass
        return evidence_items(texts, readouts)

    def fill_text(self, text, cites=(), allow_derived=False):
        """
        Write the values of ``{r3.frequency[2]}``-style references into ``text`` (see
        `McUtils.Readouts.Reports.Fill`): each value is written with its unit label, and a unit typed after the
        reference is replaced by it (a different unit is an error). Blocks a reference names are added to ``cites``.
        Computed values (``{mean(...)}``) are refused unless ``allow_derived``. ``{=300 K}`` marks a value given from
        outside the data: it is written as given and recorded as a literal.

        :return: ``(text, cites, fills)``: the filled text, the cites (with the referenced blocks), the `Fill`s
        """
        from .Fill import find_references, fill_text, _REF
        cites = list(cites or ())
        for _, inner in find_references(text):
            for m in _REF.finditer(inner):
                if m.group("block") not in cites:
                    self.get(m.group("block"))
                    cites.append(m.group("block"))
        style = self.unit_style
        if style is None:
            from ...Data import UnitsData
            style = UnitsData.label_style
        filled, fills = fill_text(text, self.evidence(cites), allow_derived=allow_derived, style=style)
        return filled, cites, fills

    def written_text(self, block_id):
        """
        A paragraph as it was written: the values the server filled in are shown as the placeholders (``{r3.frequency[1]}``)
        or given-value markers (``{=300 K}``) that wrote them. The stored text (``Prose.text``) has the values.
        """
        from .Fill import unfill
        blk = self.get(block_id)
        if not isinstance(blk, Prose):
            raise ReportOperationError("bad_argument", f"block {block_id!r} is not a paragraph", block_id=block_id)
        return unfill(blk.text, blk.fills)

    def number_coverage(self, rel_tol=1e-3, small_int_max=10, year_range=(1900, 2100), match=True):
        """
        How the numbers of the paragraphs were written: ``placeholders`` (filled in from the data), ``literals``
        (given from outside it), ``typed`` and, with ``match``, ``typed_in_data`` (typed numbers that are values of the
        data, so could have been placeholders); see `McUtils.Readouts.Reports.Advice.coverage`.
        """
        from .Advice import coverage
        return coverage(self, rel_tol=rel_tol, small_int_max=small_int_max, year_range=year_range, match=match)

    def check_prose(self, block_id, rel_tol=1e-3, small_int_max=10, year_range=(1900, 2100)):
        """
        Re-check a stored paragraph: its recorded fills are recomputed from the current data (a changed or missing
        value is reported as unmatched) and its other numbers are checked against what it cites.
        Returns a `GroundingResult`.
        """
        from .Fill import refill
        from .Grounding import NumberToken
        blk = self.get(block_id)
        if not isinstance(blk, Prose):
            raise ReportOperationError("bad_argument", f"block {block_id!r} is not a paragraph", block_id=block_id)
        spans, problems = refill(blk.text, blk.fills, self.evidence(blk.cites), self.unit_style) if blk.fills else ([], [])
        res = self.check_text(blk.text, blk.cites, rel_tol=rel_tol, small_int_max=small_int_max,
                              year_range=year_range, skip=spans)
        for p in problems:
            tok = NumberToken(p, float("nan"), 0, (0, 0))
            res.unmatched.append(tok)
            res.reasons[p] = "(a filled value) no longer follows from the data"
        res.ok = not res.unmatched
        return res

    # ---- Markdown --------------------------------------------------------------------------- #
    def to_markdown(self):
        used = {b.handle for b in self.blocks if isinstance(b, ReadoutBlock)}
        header = {"format": FORMAT, "title": self.title, "created": self.created,
                  "sources": {h: self.sources[h] for h in sorted(used) if h in self.sources},
                  "block_headers": self.block_headers, "meta": self.meta}
        blob = _escape_comment(json.dumps(header, sort_keys=True, separators=(",", ":"), ensure_ascii=True))
        parts = [f"<!-- report-meta {blob} -->", f"# {self.title}"]
        parts += [b.to_markdown(self) for b in self.blocks]
        return "\n\n".join(parts) + "\n"

    _MARKER = re.compile(r"^<!--\s*(report-meta|block|readout|caption)\b(.*?)\s*-->\s*$")
    _FENCE = re.compile(r"^```")

    @classmethod
    def from_markdown(cls, text, catalog=None):
        """
        Reads a report back from its Markdown (including text that has been edited by hand).

        Text outside any marker becomes `RawMarkdown` (an unmarked ``##``/``###`` line becomes a `Heading`); a
        readout marker whose fence isn't a ``report_source(...)`` call is kept as raw text. A source digest that
        doesn't match the catalog's is not an error here; `validate` reports it.
        """
        lines = text.replace("\r\n", "\n").split("\n")
        n = len(lines)
        meta_header, h1 = None, None
        items = []        # ("block", id, kw, [lines]) | ("readout", kw, fence_lines) | ("caption", id, kw, [lines]) | ("raw", [lines])

        def marker(i):
            m = cls._MARKER.match(lines[i]) if i < n else None
            return (m.group(1), m.group(2)) if m else None

        def is_report_readout(i):
            """Is lines[i] a readout marker whose fence is a report_source(...) call?"""
            mk = marker(i)
            if not mk or mk[0] != "readout" or i + 2 >= n or not cls._FENCE.match(lines[i + 1]):
                return False
            return lines[i + 2].lstrip().startswith("report_source(")

        i = 0
        raw_buf = []

        def flush_raw():
            if any(l.strip() for l in raw_buf):
                items.append(("raw", list(raw_buf)))
            raw_buf.clear()

        while i < n:
            mk = marker(i)
            if mk is None:
                if h1 is None and not items and lines[i].startswith("# ") and not any(l.strip() for l in raw_buf):
                    # the document title comes first
                    h1 = lines[i][2:].strip()
                    i += 1
                    continue
                raw_buf.append(lines[i])
                i += 1
                continue
            kind, args = mk
            flush_raw()
            if kind == "report-meta":
                try:
                    meta_header = json.loads(args.strip())
                except ValueError as e:
                    raise ReportOperationError("invalid_document", f"can't read the report-meta comment: {e}")
                i += 1
            elif kind == "block":
                ident, kw = _parse_call(f"block{args}", "block")
                i += 1
                body = []
                is_raw = ident is not None and ident.startswith("x")
                while i < n:
                    nxt = marker(i)
                    if nxt is not None and nxt[0] in ("block", "caption", "report-meta"):
                        break
                    if nxt is not None and nxt[0] == "readout" and (not is_raw or is_report_readout(i)):
                        break
                    body.append(lines[i])
                    i += 1
                items.append(("block", ident, kw, body))
            elif kind == "caption":
                ident, kw = _parse_call(f"caption{args}", "caption")
                i += 1
                body = []
                while i < n and marker(i) is None and (lines[i].strip() or not body):
                    body.append(lines[i])
                    i += 1
                items.append(("caption", ident, kw, body))
            else:  # readout
                _, kw = _parse_call(f"readout{args}", "readout")
                if is_report_readout(i):
                    j = i + 1
                    fence = []
                    while j < n:
                        fence.append(lines[j])
                        if j > i + 1 and cls._FENCE.match(lines[j]):
                            break
                        j += 1
                    items.append(("readout", kw, fence))
                    i = j + 1
                else:   # a hand-written marked example: keep it whole
                    j = i + 1
                    block = [lines[i]]
                    if j < n and cls._FENCE.match(lines[j]):
                        block.append(lines[j])
                        j += 1
                        while j < n:
                            block.append(lines[j])
                            if cls._FENCE.match(lines[j]):
                                j += 1
                                break
                            j += 1
                    items.append(("raw", block))
                    i = j
        flush_raw()

        title = h1 or (meta_header or {}).get("title") or "Untitled report"
        doc = cls(title, catalog=catalog, meta=(meta_header or {}).get("meta"),
                  created=(meta_header or {}).get("created"),
                  block_headers=(meta_header or {}).get("block_headers", False))
        doc.sources = dict((meta_header or {}).get("sources") or {})

        # ids found in the text come first, so minted ids don't collide with them
        for it in items:
            if it[0] == "block" and it[1]:
                doc._note_id(it[1])
            elif it[0] == "readout" and it[1].get("id"):
                doc._note_id(it[1]["id"])

        captions = {}
        for it in items:
            if it[0] == "caption":
                body = "\n".join(it[3]).strip()
                m = re.match(r"^\*(.*)\*$", body, re.S)
                captions[it[1]] = (_unescape_caption(m.group(1)) if m else body, it[2].get("status", "manual"))

        for it in items:
            kind = it[0]
            if kind == "caption":
                continue
            if kind == "raw":
                doc._add_unmarked("\n".join(it[1]))
            elif kind == "readout":
                kw, fence = it[1], it[2]
                call = fence[1] if len(fence) > 1 else ""
                try:
                    handle, rkw = _parse_call(call.strip(), "report_source")
                    if not isinstance(handle, str):
                        raise ValueError(handle)
                except (ReportOperationError, ValueError):
                    doc.blocks.append(RawMarkdown(doc._mint(RawMarkdown), "\n".join(fence)))
                    continue
                bid = kw.get("id") or doc._mint(ReadoutBlock)
                cap, status = captions.get(bid, (None, None))
                doc.blocks.append(ReadoutBlock(bid, handle, kw.get("include"), kw.get("exclude"), kw.get("units"),
                                               kw.get("style"), kw.get("display", "readout"), cap, status,
                                               header=kw.get("header", False)))
                if rkw.get("digest") is not None and handle not in doc.sources:
                    doc.sources[handle] = {"type": None, "digest": rkw["digest"]}
                elif rkw.get("digest") is not None:
                    doc.sources[handle]["digest"] = rkw["digest"]
            else:  # block
                _, ident, kw, body = it
                content = "\n".join(body).strip("\n")
                ident = ident or doc._mint(RawMarkdown)
                rest = ""
                if ident.startswith("h") and re.match(r"^#{2,3} ", content):
                    first, _, rest = content.partition("\n")
                    doc.blocks.append(Heading(ident, first.split(" ", 1)[1].strip(),
                                              kw.get("level", len(first.split(" ", 1)[0]))))
                elif ident.startswith("p"):
                    # a prose block ends at the first unfenced heading line; what follows was added by hand
                    lines_p, in_fence, cut = content.split("\n"), False, None
                    for k, line in enumerate(lines_p):
                        if line.startswith("```"):
                            in_fence = not in_fence
                        elif not in_fence and re.match(r"^#{1,3} ", line):
                            cut = k
                            break
                    keep = lines_p if cut is None else lines_p[:cut]
                    rest = "" if cut is None else "\n".join(lines_p[cut:])
                    doc.blocks.append(Prose(ident, "\n".join(keep).strip(), kw.get("cites") or (),
                                            kw.get("status", "manual"), kw.get("role", "body"), kw.get("fills"),
                                            kw.get("basis")))
                elif ident.startswith("c"):
                    first, _, rest = content.partition("\n")
                    m = re.match(r"^> \*\*(?:Flag|Note):\*\* ?(.*)$", first, re.S)
                    doc.blocks.append(Callout(ident, m.group(1) if m else first, kw.get("kind", "note")))
                else:
                    doc.blocks.append(RawMarkdown(ident, content))
                if rest.strip():
                    doc._add_unmarked(rest)
        return doc

    def _add_unmarked(self, text):
        """Text that had no marker: unmarked ``##``/``###`` lines become headings, the rest raw blocks."""
        buf, in_fence = [], False

        def flush():
            body = "\n".join(buf).strip("\n")
            if body.strip():
                self.blocks.append(RawMarkdown(self._mint(RawMarkdown), body))
            buf.clear()

        for line in text.split("\n"):
            if line.startswith("```"):
                in_fence = not in_fence
            m = None if in_fence else re.match(r"^(#{2,3}) (.+?)\s*$", line)
            if m:
                flush()
                self.blocks.append(Heading(self._mint(Heading), m.group(2), len(m.group(1))))
            else:
                buf.append(line)
        flush()

    # ---- Readout tree ----------------------------------------------------------------------- #
    def to_readout(self):
        """
        The same report as a `Readout` tree (for PowerPoint and text export).

        A hand-written ``RawMarkdown`` block that holds a readout marker can't be built here; it contributes a
        note saying to see the HTML report (a known limitation of the first version).
        """
        root = Readout(title=self.title, id="report")
        for b in self.blocks:
            if isinstance(b, Prose) and b.role == "summary":
                root.children.append(ReadoutText(b.text, id=b.id))
        current2, current3 = None, None

        def target():
            return current3 or current2 or root

        for b in self.blocks:
            if isinstance(b, Prose) and b.role == "summary":
                continue
            if isinstance(b, Heading):
                node = ReadoutSection(title=b.text, id=b.id)
                if b.level == 2:
                    root.children.append(node)
                    current2, current3 = node, None
                else:
                    (current2 or root).children.append(node)
                    current3 = node
            elif isinstance(b, ReadoutBlock):
                if self.catalog is None:
                    raise ReportSourceError("this document has no catalog, so its readouts can't be built")
                ro = self.catalog.get(b.handle).readout(include=b.include, exclude=b.exclude, units=b.units,
                                                        style=b.style)
                # the library's own composition: a Readout placed in a section becomes a section of it
                node = as_readout_node(ro, id=b.id)
                if b.header:
                    target().children.append(node)
                else:          # without its title block the readout's content sits directly under the heading
                    target().children.extend(node.children)
                if b.caption:
                    target().children.append(ReadoutText(b.caption, role="note", id=b.id + "_caption"))
            elif isinstance(b, Prose):
                target().children.append(ReadoutText(b.text, id=b.id))
            elif isinstance(b, Callout):
                target().children.append(ReadoutText(b.text, role="error" if b.callout_kind == "flag" else "note",
                                                     id=b.id))
            else:
                target().children.append(ReadoutText(b.text, id=b.id))
                if "<!-- readout(" in b.text:
                    target().children.append(ReadoutText("[hand-written readout: see the HTML report]",
                                                         role="note", id=b.id + "_note"))
        return root
