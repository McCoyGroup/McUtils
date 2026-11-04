"""
Backend-neutral data payloads for readouts.

These classes hold values *already converted to display units* (see `Styles.ReadoutUnits`)
together with the unit they are expressed in, so every renderer and every export reads the
same numbers. They know nothing about HTML or PowerPoint; renderers only ask them for
formatted strings (using a theme) or for raw arrays.
"""

from __future__ import annotations

import numbers
import numpy as np

__all__ = [
    "Field",
    "FieldSet",
    "Column",
    "TabularData",
    "ArrayData",
]


def _is_missing(value):
    return value is None or (isinstance(value, float) and np.isnan(value))


def _to_plain(value):
    """Convert numpy scalars/arrays to plain Python values (for JSON and pandas)."""
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


class _Formattable:
    name: str
    unit: str | None
    quantity: str | None
    fmt: str | None

    def resolve_format(self, value, theme=None):
        fmt = self.fmt
        if fmt is None and theme is not None:
            fmt = theme.get_format(self.quantity, value)
        if fmt is None:
            fmt = "{:.6g}" if isinstance(value, (float, np.floating)) else "{}"
        return fmt

    def format_value(self, value, theme=None):
        if _is_missing(value):
            return "—"
        fmt = self.resolve_format(value, theme)
        try:
            if callable(fmt):
                return fmt(value)
            text = fmt.format(value)
        except (ValueError, TypeError):
            return str(value)
        if text.startswith("-") and isinstance(value, (float, np.floating)) and not text.strip("-0.") \
                and not any(c in text for c in "123456789"):
            text = text[1:]   # no "-0.000"
        return text

    def unit_label(self, theme=None):
        if self.unit is None:
            return None
        if theme is not None:
            return theme.get_unit_label(self.unit)
        return self.unit


class Field(_Formattable):
    """A labelled scalar (number, string or bool) with an optional unit."""

    def __init__(self, name, value, label=None, unit=None, source_unit=None, quantity=None,
                 fmt=None, description=None):
        self.name = name
        self.value = _to_plain(value)
        self.label = label if label is not None else name.replace("_", " ").capitalize()
        self.unit = unit
        self.source_unit = source_unit
        self.quantity = quantity
        self.fmt = fmt
        self.description = description

    def format(self, theme=None, with_unit=True):
        text = self.format_value(self.value, theme)
        unit = self.unit_label(theme) if with_unit else None
        if unit and not _is_missing(self.value):
            text = text + (unit if unit in ("°",) else " " + unit)
        return text

    def get_meta(self):
        return {k: v for k, v in dict(label=self.label, unit=self.unit, source_unit=self.source_unit,
                                       quantity=self.quantity, description=self.description).items()
                if v is not None}

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.value!r}, unit={self.unit!r})"


class FieldSet:
    """An ordered collection of `Field` objects (key/value data like charge or file path)."""

    def __init__(self, fields=(), name=None, title=None):
        if isinstance(fields, dict):
            fields = [f if isinstance(f, Field) else Field(k, f) for k, f in fields.items()]
        self.fields = [f for f in fields if f is not None]
        self.name = name
        self.title = title

    def __iter__(self):
        return iter(self.fields)

    def __len__(self):
        return len(self.fields)

    def __getitem__(self, item):
        if isinstance(item, str):
            for f in self.fields:
                if f.name == item:
                    return f
            raise KeyError(item)
        return self.fields[item]

    @property
    def names(self):
        return [f.name for f in self.fields]

    def take(self, sl):
        return type(self)(self.fields[sl], name=self.name, title=self.title)

    def to_dict(self):
        return {f.name: f.value for f in self.fields}

    def to_arrays(self):
        res = {}
        for f in self.fields:
            if _is_missing(f.value):
                continue
            res[f.name] = np.asarray(f.value)
        return res

    def get_meta(self):
        return {f.name: f.get_meta() for f in self.fields}

    def to_pandas(self):
        import pandas as pd
        df = pd.DataFrame(
            {"label": [f.label for f in self.fields],
             "value": [f.value for f in self.fields],
             "unit": [f.unit for f in self.fields]},
            index=pd.Index(self.names, name="field")
        )
        df.attrs["units"] = {f.name: f.unit for f in self.fields if f.unit is not None}
        return df


class Column(_Formattable):
    """One column of a `TabularData`: values plus naming, unit and format information."""

    def __init__(self, name, values, label=None, unit=None, source_unit=None, quantity=None,
                 fmt=None, description=None, align=None):
        self.name = name
        values = np.asarray(values)
        if values.ndim != 1:
            raise ValueError(f"column {name!r} must be one-dimensional, got shape {values.shape}")
        self.values = values
        self.label = label if label is not None else name.replace("_", " ")
        self.unit = unit
        self.source_unit = source_unit
        self.quantity = quantity
        self.fmt = fmt
        self.description = description
        if align is None:
            align = "right" if np.issubdtype(values.dtype, np.number) else "left"
        self.align = align

    def __len__(self):
        return len(self.values)

    def take(self, sl):
        new = object.__new__(type(self))
        new.__dict__.update(self.__dict__)
        new.values = self.values[sl]
        return new

    def header(self, theme=None):
        unit = self.unit_label(theme)
        return self.label if not unit else f"{self.label} ({unit})"

    def format_cells(self, theme=None):
        return [self.format_value(_to_plain(v), theme) for v in self.values]

    def get_meta(self):
        return {k: v for k, v in dict(label=self.label, unit=self.unit, source_unit=self.source_unit,
                                       quantity=self.quantity, description=self.description).items()
                if v is not None}


class TabularData:
    """
    A small, typed table: an ordered list of equal-length `Column` objects.

    This is the building block that makes readouts double as an intermediate representation
    for `.npz`/pandas export (`to_arrays`, `to_pandas`) while renderers use the formatted views.
    """

    def __init__(self, columns, name=None, title=None):
        if isinstance(columns, dict):
            columns = [c if isinstance(c, Column) else Column(k, c) for k, c in columns.items()]
        columns = list(columns)
        if len(columns) > 0:
            n = len(columns[0])
            bad = [c.name for c in columns if len(c) != n]
            if bad:
                raise ValueError(f"columns {bad} do not have {n} rows")
        self.columns = columns
        self.name = name
        self.title = title

    @property
    def nrows(self):
        return 0 if not self.columns else len(self.columns[0])

    @property
    def ncols(self):
        return len(self.columns)

    @property
    def column_names(self):
        return [c.name for c in self.columns]

    def __getitem__(self, item):
        if isinstance(item, str):
            for c in self.columns:
                if c.name == item:
                    return c
            raise KeyError(item)
        return self.columns[item]

    def take_rows(self, sl):
        return type(self)([c.take(sl) for c in self.columns], name=self.name, title=self.title)

    def headers(self, theme=None):
        return [c.header(theme) for c in self.columns]

    def format_rows(self, theme=None):
        cols = [c.format_cells(theme) for c in self.columns]
        return [list(r) for r in zip(*cols)]

    def to_dict(self):
        return {c.name: c.values for c in self.columns}

    def to_arrays(self):
        return {c.name: np.asarray(c.values) for c in self.columns}

    def get_meta(self):
        return {c.name: c.get_meta() for c in self.columns}

    def to_pandas(self):
        import pandas as pd
        df = pd.DataFrame({c.name: c.values for c in self.columns})
        df.attrs["units"] = {c.name: c.unit for c in self.columns if c.unit is not None}
        df.attrs["labels"] = {c.name: c.label for c in self.columns}
        return df

    def to_text(self, theme=None):
        headers = self.headers(theme)
        rows = self.format_rows(theme)
        widths = [max([len(h)] + [len(r[i]) for r in rows]) for i, h in enumerate(headers)]
        def line(cells):
            out = []
            for c, w, col in zip(cells, widths, self.columns):
                out.append(c.rjust(w) if col.align == "right" else c.ljust(w))
            return "  ".join(out)
        return "\n".join([line(headers), "  ".join("-" * w for w in widths)] + [line(r) for r in rows])


class ArrayData(_Formattable):
    """An n-dimensional array with axis labels and a unit (e.g. a mode matrix); exported, rarely displayed."""

    def __init__(self, name, array, axes=None, label=None, unit=None, source_unit=None, quantity=None,
                 fmt=None, description=None):
        self.name = name
        self.array = np.asarray(array)
        self.axes = axes
        self.label = label if label is not None else name.replace("_", " ")
        self.unit = unit
        self.source_unit = source_unit
        self.quantity = quantity
        self.fmt = fmt
        self.description = description

    def to_arrays(self):
        return {self.name: self.array}

    def get_meta(self):
        meta = {k: v for k, v in dict(label=self.label, unit=self.unit, source_unit=self.source_unit,
                                       quantity=self.quantity, description=self.description).items()
                if v is not None}
        if self.axes is not None:
            meta["axes"] = [list(a) if not isinstance(a, str) else a for a in self.axes]
        meta["shape"] = list(self.array.shape)
        return meta
