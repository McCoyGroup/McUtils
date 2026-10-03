"""
Readout dispatch for objects that can't (or shouldn't) carry a ``to_readout`` method themselves:
namedtuple records, parsed dictionaries, third-party objects.

`register_readout(target, adapter)` maps a type (or a dotted type name, matched as a suffix of
``module.QualName`` so it works however McUtils is put on the path, or registered lazily without
importing it) to an adapter: a callable ``adapter(obj) -> ReadoutInterface | Readout`` or a lazy
``"package.module:attribute"`` string (a leading ``.`` means relative to the McUtils package).
`to_readout(obj, **opts)` uses, in order, a registered adapter (so registrations can override),
the object's own ``to_readout``, then a generic record view (`record_nodes`).

Plain records produced by McUtils parsers (namedtuples that can't carry methods) are registered
here by default; their adapters live in each subpackage's ``Readouts`` package and are imported
only when first used.
"""

import dataclasses
import importlib
import numbers

import numpy as np

from .Data import Field, FieldSet, ArrayData, Column, TabularData
from .Nodes import ReadoutSection, ReadoutFields, ReadoutTable, ReadoutArray, ReadoutText, Readout, _slug
from .Interface import ReadoutAdapter, readout_section

__all__ = [
    "register_readout",
    "find_readout_adapter",
    "to_readout",
    "record_nodes",
    "RecordReadout",
    "is_secret_key",
    "mask_secrets",
]

_ADAPTERS = {}
_ROOT = __name__.rsplit(".Jupyter.", 1)[0]  # the McUtils package, however it was imported

_SECRET_HINTS = ("password", "passwd", "token", "secret", "api_key", "apikey", "credential", "private_key")


def is_secret_key(key):
    """Whether an option/setting name looks like it holds a credential."""
    k = str(key).lower()
    return any(h in k for h in _SECRET_HINTS)


def mask_secrets(record, mask="••••"):
    """A copy of a (nested) dict with credential-like values replaced by ``mask``."""
    if isinstance(record, dict):
        return {k: (mask if is_secret_key(k) and v is not None else mask_secrets(v, mask)) for k, v in record.items()}
    return record


def register_readout(target, adapter=None):
    """
    Register ``adapter`` for ``target`` (a class, or a dotted name such as
    ``"ExternalPrograms.Parsers.CubeParser.CubeFileData"``). Usable as a decorator.
    """
    def reg(adapter):
        key = target if isinstance(target, str) else f"{target.__module__}.{target.__qualname__}"
        _ADAPTERS[key] = adapter
        return adapter
    return reg if adapter is None else reg(adapter)


def _load(adapter):
    if isinstance(adapter, str):
        mod, attr = adapter.split(":")
        obj = importlib.import_module(_ROOT + mod if mod.startswith(".") else mod)
        for a in attr.split("."):
            obj = getattr(obj, a)
        return obj
    return adapter


def find_readout_adapter(obj):
    for cls in type(obj).__mro__:
        full = f"{cls.__module__}.{cls.__qualname__}"
        for key, adapter in _ADAPTERS.items():
            if full == key or full.endswith("." + key):
                return _load(adapter)
    return None


def to_readout(obj, *, title=None, **opts):
    """Build a `Readout` for any object (see the module docstring for the dispatch order)."""
    if isinstance(obj, Readout):
        return obj
    adapter = find_readout_adapter(obj)
    if adapter is None and hasattr(obj, "to_readout") and not isinstance(obj, type):
        res = obj.to_readout(**opts)
    elif adapter is not None:
        res = adapter(obj)
        if not isinstance(res, Readout):
            res = res.to_readout(**opts) if title is None else res.to_readout(title=title, **opts)
    else:
        res = RecordReadout(obj).to_readout(**opts)
    if title is not None:
        res.title = title
    return res


# --------------------------------------------------------------------------------------------- #
#  generic records
# --------------------------------------------------------------------------------------------- #
def _items(obj):
    if isinstance(obj, dict):
        return list(obj.items())
    if hasattr(obj, "_fields") and isinstance(obj, tuple):
        return [(f, getattr(obj, f)) for f in obj._fields]
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return [(f.name, getattr(obj, f.name)) for f in dataclasses.fields(obj)]
    return None


def _is_scalar(v):
    return isinstance(v, (numbers.Number, str, bool, np.generic)) or (isinstance(v, np.ndarray) and v.ndim == 0)


def _scalar(v):
    if isinstance(v, np.ndarray):
        v = v.item()
    if isinstance(v, np.generic):
        v = v.item()
    return v


def record_nodes(obj, name="record", depth=0, max_depth=3, max_items=12, units=None):
    """
    A generic view of a record (dict, namedtuple, dataclass): scalars become a field list,
    arrays become array blocks (small ones shown as tables), lists of homogeneous records become
    tables, nested records become subsections. ``units`` maps field names to unit names.
    """
    units = units or {}
    items = _items(obj)
    if items is None:
        if isinstance(obj, np.ndarray) or (isinstance(obj, (list, tuple)) and obj and
                                           all(isinstance(x, numbers.Number) for x in obj)):
            return [ReadoutArray(ArrayData(_slug(name), np.asarray(obj)), display=True)]
        if _is_scalar(obj):
            return [ReadoutFields(FieldSet([Field(_slug(name), _scalar(obj))]))]
        return [ReadoutText(f"{type(obj).__name__}: {str(obj)[:200]}", role="note")]
    fields, nodes = [], []
    for k, v in items:
        key = _slug(k)
        label = str(k).replace("_", " ")
        if v is None or (isinstance(v, (list, tuple, dict)) and len(v) == 0):
            continue
        if _is_scalar(v):
            fields.append(Field(key, _scalar(v), label=label, unit=units.get(k)))
        elif isinstance(v, (list, tuple)) and all(isinstance(x, str) for x in v) and len(v) <= 24:
            fields.append(Field(key, ", ".join(v), label=label))
        elif isinstance(v, np.ndarray) or (isinstance(v, (list, tuple)) and
                                           all(isinstance(x, numbers.Number) for x in v)):
            arr = np.asarray(v)
            if arr.dtype == object:
                fields.append(Field(key, str(v)[:200], label=label))
            else:
                nodes.append(ReadoutArray(ArrayData(key, arr, label=label, unit=units.get(k)), display=True,
                                          title=label))
        elif isinstance(v, (list, tuple)) and all(_items(x) is not None for x in v):
            rows = [dict(_items(x)) for x in v]
            keys = list(rows[0])
            if all(list(r) == keys for r in rows) and all(_is_scalar(r[c]) or r[c] is None for r in rows for c in keys):
                cols = [Column(_slug(c), np.array([_scalar(r[c]) if r[c] is not None else np.nan for r in rows]),
                               label=str(c).replace("_", " ")) for c in keys]
                nodes.append(ReadoutTable(TabularData(cols, name=key), title=label))
            elif depth < max_depth:
                subs = [ReadoutSection(*record_nodes(x, f"{k}_{i}", depth + 1, max_depth, max_items),
                                       id=f"{key}_{i + 1}", title=f"{label} {i + 1}")
                        for i, x in enumerate(v[:max_items])]
                if len(v) > max_items:
                    subs.append(ReadoutText(f"{len(v) - max_items} more {label} entries not shown", role="note"))
                nodes.append(ReadoutSection(*subs, id=key, title=label))
        elif _items(v) is not None and depth < max_depth:
            nodes.append(ReadoutSection(*record_nodes(v, k, depth + 1, max_depth, max_items), id=key, title=label))
        elif hasattr(v, "to_readout"):
            from .Views import as_readout_node
            nodes.append(as_readout_node(v, id=key, title=label))
        else:
            fields.append(Field(key, f"{type(v).__name__}", label=label))
    out = []
    if fields:
        out.append(ReadoutFields(FieldSet(fields, name="fields")))
    return out + nodes


class RecordReadout(ReadoutAdapter):
    """Generic readout for records (dicts, namedtuples, dataclasses) and plain values."""
    readout_id = "record"

    def __init__(self, obj, title=None, units=None):
        super().__init__(obj)
        self._title = title
        self._units = units

    def get_readout_title(self):
        return self._title or type(self.obj).__name__

    @readout_section("contents", title="Contents")
    def readout_contents(self, ctx, max_depth=3, max_items=12):
        """Every retained field: scalars, arrays, nested records."""
        return record_nodes(self.obj, type(self.obj).__name__, max_depth=max_depth, max_items=max_items,
                            units=self._units)


# --------------------------------------------------------------------------------------------- #
#  default (lazy) registrations for McUtils records that can't carry methods
# --------------------------------------------------------------------------------------------- #
for _target, _adapter in {
    "ExternalPrograms.Parsers.CubeParser.CubeFileData": ".ExternalPrograms.Readouts.Volumes:CubeReadout",
    "ExternalPrograms.Parsers.Crest.CRESTConformers": ".ExternalPrograms.Readouts.Conformers:ConformerEnsembleReadout.from_crest",
    "ExternalPrograms.Parsers.Crest.CRESTRotamers": ".ExternalPrograms.Readouts.Conformers:ConformerEnsembleReadout.from_crest",
    "ExternalPrograms.Conformers.ConformerRecord": ".ExternalPrograms.Readouts.Conformers:ConformerRecordReadout",
}.items():
    register_readout(_target, _adapter)
