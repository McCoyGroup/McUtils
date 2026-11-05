"""
Report sources: the named objects a report is built from.

A report never holds the objects it describes inside its text. It refers to them by *handle*
(``"water"``), and a `SourceCatalog` maps handles to live objects. The catalog knows what each object offers
(its readout sections, their descriptions and kinds) so that both people and models can choose from a menu, and it
fingerprints each source (`source_digest`) so a stored report can tell when its data has changed.
"""

import hashlib
import re

from ..Interface import (ReadoutInterface, RecordReadout, find_readout_adapter, to_readout, ReadoutSectionUnavailable)
from ..Nodes import Readout

__all__ = [
    "ReportSourceError",
    "resolve_readout_interface",
    "source_digest",
    "ReportSource",
    "SourceCatalog",
]


class ReportSourceError(ValueError):
    """A source can't be added, found, loaded or matched to the digest a report recorded."""


def resolve_readout_interface(obj):
    """
    The `ReadoutInterface` that lists and builds the sections of ``obj``.

    Order: ``obj.get_readout_interface()``; ``obj`` itself if it is an interface; a registered adapter
    (`register_readout`); otherwise the generic `RecordReadout`.
    """
    getter = getattr(obj, "get_readout_interface", None)
    if callable(getter) and not isinstance(obj, type):
        return getter()
    if isinstance(obj, ReadoutInterface):
        return obj
    adapter = find_readout_adapter(obj)
    if adapter is not None:
        res = adapter(obj)
        if isinstance(res, ReadoutInterface):
            return res
        raise ReportSourceError(
            "the readout adapter for {} returns a ready-made Readout, not an interface with sections, so "
            "its sections can't be listed".format(type(obj).__name__)
        )
    return RecordReadout(obj)


def source_digest(obj):
    """
    A short fingerprint of the data a source would report: ``obj.__report_digest__()`` if the object defines one,
    else the MD5 of its default readout's JSON export (first 16 hex characters).
    """
    custom = getattr(obj, "__report_digest__", None)
    if callable(custom):
        return str(custom())[:16]
    text = to_readout(obj).to_json()
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:16]


_FIGURE_KINDS = {"scene", "image", "plot", "gallery", "html", "presml"}
_TABLE_KINDS = {"table", "array"}


def _classify(node):
    kinds = {n.kind for _, n in node.walk()}
    if kinds & _TABLE_KINDS:
        return "table"
    if "fields" in kinds:
        return "fields"
    if kinds & _FIGURE_KINDS:
        return "figure"
    return "text"


def _truncate(text, max_chars):
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars]
    if "\n" in cut:
        cut = cut[:cut.rindex("\n")]
    return cut.rstrip() + "\n[... truncated]"


class ReportSource:
    """
    One named object in a catalog.

    :ivar handle: its name in the catalog
    :ivar obj: the object
    :ivar digest: the fingerprint recorded for it
    :ivar title: an optional display title
    :ivar type_name: ``module.QualName`` of the object's type
    """

    def __init__(self, handle, obj, digest, title=None):
        self.handle = handle
        self.obj = obj
        self.digest = digest
        self.title = title
        self.type_name = f"{type(obj).__module__}.{type(obj).__qualname__}"
        self._interface = None
        self._kinds = {}

    # ---- structure ---- #
    def interface(self):
        if self._interface is None:
            self._interface = resolve_readout_interface(self.obj)
        return self._interface

    @property
    def is_record(self):
        return isinstance(self.interface(), RecordReadout)

    def sections(self, kinds=False):
        """
        The section rows of the interface (``name, title, default, cost, options, description, available`` and
        ``reason`` when unavailable). A plain record has the one pseudo-section ``record``. With ``kinds=True``
        each available section also gets its ``kind`` (this builds the sections).
        """
        if self.is_record:
            rows = [dict(name="record", title="Record", default=True, cost=None, options=[],
                         description="Every retained field of the record.", available=True)]
        else:
            iface = self.interface()
            rows = iface.list_readout_sections(iface)
            for row in rows:
                row.setdefault("available", True)
                if row["available"]:
                    row.pop("reason", None)   # a reason only means something when the section is unavailable
        if kinds:
            for row in rows:
                row["kind"] = self.section_kind(row["name"]) if row["available"] else "unknown"
        return rows

    def section_names(self):
        return [r["name"] for r in self.sections()]

    def default_sections(self):
        return [r["name"] for r in self.sections() if r["default"] and r["available"]]

    # ---- building ---- #
    def readout(self, include=None, exclude=None, units=None, style=None):
        """
        Build a `Readout` of this source. ``include=None`` means the default sections; for a plain record the
        pseudo-section ``record`` is the whole record. (``style`` is a rendering option and is accepted for
        symmetry with readout markers; it doesn't change what is built.)
        """
        opts = {}
        if units is not None:
            opts["units"] = units
        if self.is_record:
            return to_readout(self.obj, **opts)
        if include is not None:
            opts["include"] = list(include)
        if exclude is not None:
            opts["exclude"] = list(exclude)
        return to_readout(self.obj, **opts)

    def _section_readout(self, name):
        return self.readout(include=[name]) if not self.is_record else self.readout()

    def section_text(self, name, max_chars=2400):
        """The text rendering of one section, cut at a line boundary."""
        return _truncate(self._section_readout(name).to_text(), max_chars)

    def section_kind(self, name):
        """``figure``, ``table``, ``fields``, ``text``, or ``unknown`` (building raised: see ``kind_error``)."""
        if name not in self._kinds:
            try:
                if self.is_record:
                    node = self.readout()
                else:
                    node = to_readout(self.obj, include=[name], strict=True)
                self._kinds[name] = (_classify(node), None)
            except Exception as e:  # noqa: BLE001 - the reason is the point
                self._kinds[name] = ("unknown", f"{type(e).__name__}: {e}")
        return self._kinds[name][0]

    def kind_error(self, name):
        self.section_kind(name)
        return self._kinds[name][1]


class SourceCatalog:
    """The handle -> `ReportSource` table a report is built against."""
    HANDLE_RE = re.compile(r"^[a-z][a-z0-9_]{0,39}$")

    def __init__(self):
        self._sources = {}

    def add(self, handle, obj, digest=None, title=None):
        if not isinstance(handle, str) or not self.HANDLE_RE.match(handle):
            raise ReportSourceError(f"bad source handle {handle!r}: use lower-case letters, digits and "
                                    f"underscores, starting with a letter (at most 40 characters)")
        if handle in self._sources:
            raise ReportSourceError(f"source handle {handle!r} is already in the catalog")
        src = ReportSource(handle, obj, digest if digest is not None else source_digest(obj), title=title)
        self._sources[handle] = src
        return src

    def get(self, handle):
        try:
            return self._sources[handle]
        except KeyError:
            raise ReportSourceError(f"unknown source {handle!r}; known sources: {self.handles()}") from None

    def handles(self):
        return list(self._sources)

    def __contains__(self, handle):
        return handle in self._sources

    def __len__(self):
        return len(self._sources)

    def describe(self, handle):
        """``{handle, type, title, digest, sections: [{name, title, description, default, available, reason?, kind, cost}]}``"""
        src = self.get(handle)
        rows = []
        for r in src.sections(kinds=True):
            row = {k: r.get(k) for k in ("name", "title", "description", "default", "available", "kind", "cost")}
            if r.get("reason"):
                row["reason"] = r["reason"]
            rows.append(row)
        return {"handle": handle, "type": src.type_name, "title": src.title, "digest": src.digest,
                "sections": rows}

    def peek(self, handle, section, max_chars=2400):
        return self.get(handle).section_text(section, max_chars=max_chars)

    def load(self, handle, digest=None):
        """The object behind ``handle``. A ``digest`` that doesn't match the catalog's is an error."""
        src = self.get(handle)
        if digest is not None and digest != src.digest:
            raise ReportSourceError(
                f"source {handle!r} has changed: the report recorded digest {digest} but the catalog's is {src.digest}"
            )
        return src.obj

    def namespace(self):
        """What a readout block's code needs to resolve ``report_source(...)``."""
        return {"report_source": self.load}
