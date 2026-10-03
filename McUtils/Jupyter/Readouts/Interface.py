"""
The producer side of readouts.

Objects become readable by subclassing `ReadoutInterface` (or wrapping themselves in a
`ReadoutAdapter`, which keeps large classes uncluttered) and declaring named sections::

    class MoleculeReadoutInterface(ReadoutAdapter):
        @readout_section("cartesians", title="Cartesian coordinates")
        def readout_cartesians(self, ctx, units=None):
            ...
            return ReadoutTable(...)

`to_readout(include=..., exclude=..., units=..., **section_options)` then picks, orders and
builds the sections. Sections may delegate to other objects' interfaces with
`get_readout_sections(..., ctx=ctx.child(name, parent=self.obj))`, which is how sub-reports are
composed.
"""

import inspect
import traceback
import warnings

import numpy as np

from .Data import Field, Column
from .Nodes import ReadoutNode, ReadoutSection, ReadoutText, Readout
from .Styles import ReadoutUnits

__all__ = [
    "readout_section",
    "ReadoutSectionSpec",
    "ReadoutContext",
    "ReadoutInterface",
    "ReadoutAdapter",
    "ReadoutSectionUnavailable",
]


class ReadoutSectionUnavailable(Exception):
    """Raise from a section (or an `available` check) to report it can't be built."""


class ReadoutSectionSpec:
    def __init__(self, name, func, title=None, default=True, available=None, description=None,
                 order=None, cost=None):
        self.name = name
        self.func = func
        self.title = title if title is not None else name.replace("_", " ").capitalize()
        self.default = default
        self.available = available
        self.description = description if description is not None else inspect.getdoc(func)
        self.order = order
        self.cost = cost
        sig = inspect.signature(func)
        self.accepts_var_kw = any(p.kind is p.VAR_KEYWORD for p in sig.parameters.values())
        self.parameters = [p for p in list(sig.parameters)[2:]
                           if sig.parameters[p].kind not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)]

    def check_available(self, interface):
        """``(bool, reason)``"""
        check = self.available
        if check is None:
            return True, None
        try:
            if isinstance(check, str):
                ok = getattr(interface, check)()
            else:
                ok = check(interface)
        except Exception as e:
            return False, f"{type(e).__name__}: {e}"
        if isinstance(ok, tuple):
            return ok
        return bool(ok), None if ok else "required data is missing"

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, default={self.default})"


def readout_section(name=None, *, title=None, default=True, available=None, description=None,
                    order=None, cost=None):
    """
    Mark a method ``f(self, ctx, **options)`` as a readout section.

    :param available: ``callable(interface) -> bool | (bool, reason)`` or the name of such a method
    :param default: whether the section is built when no ``include`` is given
    :param cost: an informational hint (e.g. ``'expensive'``) shown by `list_readout_sections`
    """
    def decorate(func):
        func._readout_section = dict(name=name or func.__name__.replace("readout_", ""),
                                     title=title, default=default, available=available,
                                     description=description, order=order, cost=cost)
        return func
    return decorate


class ReadoutContext:
    """
    Build-time state passed to every section: units (so values are converted once, while the
    readout is built), the path of the section being built, and the chain of parent objects.
    """

    def __init__(self, units=None, path=(), parents=(), strict=False):
        self.units = ReadoutUnits.resolve(units)
        self.path = tuple(path)
        self.parents = tuple(parents)
        self.strict = strict

    def child(self, name, parent=None):
        return type(self)(self.units, self.path + (name,),
                          self.parents + ((parent,) if parent is not None else ()), self.strict)

    def find_parent(self, cls):
        for p in reversed(self.parents):
            if isinstance(p, cls):
                return p
        return None

    # helpers that apply the unit preferences
    def convert(self, values, quantity, source_unit):
        return self.units.convert(values, quantity, source_unit)

    def field(self, name, value, quantity=None, unit=None, **opts):
        """A `Field` whose value is converted from ``unit`` to the display unit for ``quantity``."""
        if value is not None and quantity is not None and unit is not None:
            value, target = self.convert(value, quantity, unit)
        else:
            target = unit
        return Field(name, value, quantity=quantity, unit=target, source_unit=unit, **opts)

    def column(self, name, values, quantity=None, unit=None, **opts):
        """A `Column` whose values are converted from ``unit`` to the display unit for ``quantity``."""
        if quantity is not None and unit is not None:
            values, target = self.convert(values, quantity, unit)
        else:
            target = unit
        return Column(name, values, quantity=quantity, unit=target, source_unit=unit, **opts)


def _normalize_include(include, registry):
    """-> ordered list of (name, options dict | None, explicitly_requested)"""
    names = list(registry)
    if include is None:
        return [(n, {}, False) for n in names if registry[n].default]
    if include is True or include == "all":
        return [(n, {}, False) for n in names]
    if include == "default":
        return [(n, {}, False) for n in names if registry[n].default]
    if isinstance(include, str):
        include = [include]
    items = []
    if isinstance(include, dict):
        for k, v in include.items():
            if v is False or v is None:
                continue
            items.append((k, {} if v is True else dict(v)))
    else:
        for k in include:
            if isinstance(k, (tuple, list)):
                items.append((k[0], dict(k[1]) if len(k) > 1 else {}))
            elif k in ("all", "default"):
                items.extend((n, {}) for n in names if k == "all" or registry[n].default)
            else:
                items.append((k, {}))
    merged = {}
    for name, opts in items:
        if "." in name:
            head, rest = name.split(".", 1)
            sub = merged.setdefault(head, {})
            sub.setdefault("include", [])
            if isinstance(sub["include"], list):
                sub["include"].append(rest if not opts else (rest, opts))
            name, opts = head, {}
        if name not in registry:
            raise ValueError(f"unknown readout section {name!r}; available sections: {names}")
        merged.setdefault(name, {}).update(opts)
    return [(n, o, True) for n, o in merged.items()]


class ReadoutInterface:
    """
    Mixin for objects that can produce a `Readout`. Sections are methods decorated with
    `readout_section`; subclasses inherit, override (same name) or add sections.
    """
    readout_id = None
    readout_title = None
    readout_sections = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        registry = {}
        for base in reversed(cls.__mro__[1:]):
            registry.update(getattr(base, "readout_sections", {}) or {})
        defs = []
        for attr, val in cls.__dict__.items():
            spec = getattr(val, "_readout_section", None)
            if spec is not None:
                defs.append(ReadoutSectionSpec(func=val, **spec))
        for spec in defs:
            registry[spec.name] = spec  # an override keeps the inherited position
        names = list(registry)
        ordered = sorted(registry.values(),
                         key=lambda s: s.order if s.order is not None else 1e6 + names.index(s.name))
        cls.readout_sections = {s.name: s for s in ordered}

    # -------------------------------------------------------------------------------------- #
    def get_readout_target(self):
        return self

    def get_readout_id(self):
        return self.readout_id or type(self.get_readout_target()).__name__.lower()

    def get_readout_title(self):
        return self.readout_title or type(self.get_readout_target()).__name__

    def get_readout_subtitle(self):
        return None

    def get_readout_meta(self):
        return {}

    @classmethod
    def list_readout_sections(cls, obj=None):
        """Names, titles, defaults and (given an instance) availability of every section."""
        rows = []
        for name, spec in cls.readout_sections.items():
            row = dict(name=name, title=spec.title, default=spec.default, cost=spec.cost,
                       options=spec.parameters,
                       description=(spec.description or "").split("\n")[0])
            if obj is not None:
                interface = obj if isinstance(obj, ReadoutInterface) else cls(obj)
                ok, reason = spec.check_available(interface)
                row["available"] = ok
                if reason:
                    row["reason"] = reason
            rows.append(row)
        return rows

    def _placeholder(self, spec, reason):
        return ReadoutSection(ReadoutText(f"Not available: {reason}", role="note"),
                              id=spec.name, title=spec.title, meta={"unavailable": reason})

    def build_readout_section(self, name, ctx, requested=False, **opts):
        spec = self.readout_sections[name]
        ok, reason = spec.check_available(self)
        if not ok:
            if ctx.strict and requested:
                raise ReadoutSectionUnavailable(f"section {name!r} unavailable: {reason}")
            return self._placeholder(spec, reason) if requested else None
        if not spec.accepts_var_kw:
            bad = set(opts) - set(spec.parameters)
            if bad:
                raise TypeError(f"readout section {name!r} got unknown options {sorted(bad)}; "
                                f"it accepts {spec.parameters}")
        sub = ctx.child(name, parent=self.get_readout_target())
        try:
            res = spec.func(self, sub, **opts)
        except ReadoutSectionUnavailable as e:
            if ctx.strict and requested:
                raise
            return self._placeholder(spec, str(e)) if requested else None
        except Exception as e:
            if ctx.strict:
                raise
            warnings.warn(f"readout section {name!r} failed: {type(e).__name__}: {e}")
            return ReadoutSection(
                ReadoutText(f"Failed to build: {type(e).__name__}: {e}", role="error"),
                id=name, title=spec.title,
                meta={"error": "".join(traceback.format_exception_only(type(e), e)).strip()})
        if res is None:
            return None
        if isinstance(res, ReadoutSection) and not isinstance(res, Readout):
            if res.title is None:
                res.title = spec.title
            res.id = name
            return res
        if isinstance(res, ReadoutNode):
            res = [res]
        return ReadoutSection(*res, id=name, title=spec.title)

    def get_readout_sections(self, include=None, exclude=None, ctx=None, strict=False, units=None,
                             **section_options):
        """Build the requested sections as a list (for embedding in a parent readout)."""
        if ctx is None:
            ctx = ReadoutContext(units=units, strict=strict)
        plan = _normalize_include(include, self.readout_sections)
        exclude = [exclude] if isinstance(exclude, str) else list(exclude or [])
        nested_exclude = {}
        for e in exclude:
            if "." in e:
                head, rest = e.split(".", 1)
                nested_exclude.setdefault(head, []).append(rest)
            elif e not in self.readout_sections:
                raise ValueError(f"unknown readout section {e!r}; available sections: {list(self.readout_sections)}")
        unknown = set(section_options) - set(self.readout_sections)
        if unknown:
            raise TypeError(f"unknown readout options {sorted(unknown)}; per-section options are passed "
                            f"as section_name={{...}} for sections {list(self.readout_sections)}")
        sections = []
        for name, opts, requested in plan:
            if name in exclude:
                continue
            extra = section_options.get(name)
            if extra is False:
                continue
            opts = dict(opts, **(extra if isinstance(extra, dict) else {}))
            if name in nested_exclude:
                opts["exclude"] = list(opts.get("exclude", [])) + nested_exclude[name]
            node = self.build_readout_section(name, ctx, requested=requested or extra is not None, **opts)
            if node is not None:
                sections.append(node)
        return sections

    def to_readout(self, include=None, exclude=None, *, title=None, subtitle=None, units=None,
                   strict=False, **section_options):
        """
        Build a `Readout`.

        :param include: ``None`` (default sections), ``'all'``, a list of section names (dotted
            names reach nested sections, e.g. ``'normal_modes.frequencies'``), or a dict of
            ``name -> options | bool``
        :param exclude: section names to drop
        :param units: display units, e.g. ``{'length': 'Angstroms'}``; all exports use these
        :param strict: raise instead of inserting placeholders for unavailable/failed sections
        :param section_options: per-section options, ``section_name={...}`` (or ``False`` to drop)
        """
        ctx = ReadoutContext(units=units, path=(self.get_readout_id(),), strict=strict)
        sections = self.get_readout_sections(include=include, exclude=exclude, ctx=ctx, **section_options)
        return Readout(*sections, title=title if title is not None else self.get_readout_title(),
                       subtitle=subtitle if subtitle is not None else self.get_readout_subtitle(),
                       units=ctx.units, id=self.get_readout_id(), meta=self.get_readout_meta())


class ReadoutAdapter(ReadoutInterface):
    """A `ReadoutInterface` that wraps another object (``self.obj``)."""

    def __init__(self, obj):
        self.obj = obj

    def get_readout_target(self):
        return self.obj
