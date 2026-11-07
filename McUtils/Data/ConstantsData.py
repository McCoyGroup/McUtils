"""
Provides constants data and conversions between units and unit systems
"""
from .CommonData import DataHandler
from collections import OrderedDict, deque

__all__ = [ "UnitsData", "UnitsDataHandler", "UnitExpression", "ConversionError" ]

import ast, math, re
from numbers import Real
from fractions import Fraction
from dataclasses import dataclass, field
from itertools import combinations

# characters for building the unicode / ascii / latex label styles of `UnitsDataHandler`
_SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
        "⁻": "-", "⁺": "+"}
_SUB = {"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9",
        "ₕ": "h", "ₑ": "e", "ₐ": "a", "ₙ": "n", "ₘ": "m"}
_ASCII_WORDS = {"Å": "Ang", "°": "deg", "µ": "u", "μ": "u", "Ω": "Ohm"}
_SUP_CHARS = "".join(_SUP)
_SUB_CHARS = "".join(_SUB)
_SUP_OF = {v: k for k, v in _SUP.items()}
_PER = re.compile(r"(?<=[a-z])Per(?=[A-Z])")
_MATHRM = re.compile(r"\\mathrm\{([^{}]*)\}")
__reload_hook__ = [".CommonData"]

class ConversionError(Exception):
    pass

class UnitGraph:
    def __init__(self, stuff_to_update = ()):
        self._graph = {}
        self.update(stuff_to_update)

    def __contains__(self, item):
        return item in self._graph
    def add(self, node, connection):
        if node in self._graph:
            self._graph[node].add(connection)
        else:
            self._graph[node] = {connection}
        if not connection in self._graph:
            self._graph[connection] = set()
    def update(self, iterable):
        for connection in iterable:
            self.add(*connection)
    def keys(self):
        return self._graph.keys()
    def __getitem__(self, item):
        return self._graph[item]
    def find_path_bfs(self, start, end):
        """A shortest path, with deterministic ordering for equally short paths."""
        if start not in self._graph or end not in self._graph:
            return None
        parents = {start: None}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            if current == end:
                path = [end]
                while path[-1] != start:
                    path.append(parents[path[-1]])
                return path[::-1]
            for neighbor in sorted(self._graph[current], key=repr):
                if neighbor not in parents:
                    parents[neighbor] = current
                    queue.append(neighbor)
        return None

@dataclass(frozen=True, eq=False)
class UnitExpression:
    """Immutable unit algebra, bound to a UnitsDataHandler (not an array/quantity wrapper).

    ``to`` returns a numeric factor. Scalar products describe scaled units. Equality
    uses core definitions only; enabled energy equivalences never change identity.
    Expressions use current registry definitions after explicit registrations.
    """
    _handler: object = field(repr=False)
    factors: tuple
    scale: float = 1.
    __hash__ = None

    def __post_init__(self):
        self._handler.data
        scale, factors = self._handler._parse(tuple(self.factors))
        scale *= self.scale
        if not isinstance(scale, Real) or not math.isfinite(scale) or scale == 0:
            raise ValueError('a unit scale must be finite and nonzero')
        object.__setattr__(self, 'scale', float(scale))
        object.__setattr__(self, 'factors', self._handler._signature(factors))

    def _combine(self, other, power):
        if isinstance(other, Real):
            if not math.isfinite(other) or other == 0:
                raise ValueError('a unit scale must be finite and nonzero')
            return type(self)(self._handler, self.factors, self.scale * float(other) ** power)
        other = self._handler.unit(other)
        return self._handler._expression(self.scale * other.scale ** power,
                                         self.factors + tuple((name, exponent * power)
                                                              for name, exponent in other.factors))

    def __mul__(self, other):
        return self._combine(other, 1)
    __rmul__ = __mul__

    def __truediv__(self, other):
        return self._combine(other, -1)

    def __rtruediv__(self, other):
        return self._handler.unit(other) / self

    def __pow__(self, power):
        power = self._handler._power(power)
        return self._handler._expression(self.scale ** float(power),
                                         tuple((name, exponent * power) for name, exponent in self.factors))

    def __eq__(self, other):
        if not isinstance(other, UnitExpression) or self._handler is not other._handler:
            return False
        return self._handler._core(self) == self._handler._core(other)

    @property
    def dimensions(self):
        return dict(self._handler._core(self)[1])

    def to(self, target, *, equivalences=None):
        return self._handler.convert(self, target, equivalences=equivalences)

    def label(self, style=None):
        return self._handler.unit_label(self, style)

    def __str__(self):
        terms = [name if power == 1 else f'{name}**({power})' for name, power in self.factors]
        if self.scale != 1 or not terms:
            terms.insert(0, str(self.scale))
        return ' * '.join(terms)

    def __repr__(self):
        return f'UnitExpression({str(self)!r})'


class _UnitNamespace:
    """Autocomplete and item access on the existing handler's unit registry."""
    def __init__(self, handler):
        self._handler = handler

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        try:
            return self._handler.unit(name)
        except ConversionError as error:
            raise AttributeError(str(error)) from error

    def __getitem__(self, name):
        return self._handler.unit(name)

    def __dir__(self):
        self._handler.data
        return sorted(name for name in self._handler._known_names | self._handler._aliases.keys()
                      if name.isidentifier())


class UnitsDataHandler(DataHandler):
    """
    A DataHandler that's built for use with the units data we've collected.
    Usually used through the `UnitsData` object.

    ``u = UnitsData.units`` exposes discoverable immutable unit expressions:
    ``(u.hartree / u.bohr).to(u.eV / u.angstrom)`` returns a scalar factor.
    ``UnitsData.unit("cm^-1 / angstrom")`` parses the same algebra. Ordinary
    conversions always win; only the ``wavenumber`` energy equivalence is enabled
    by default. Select explicit fallbacks with ``equivalences=("thermal",)`` or
    disable all of them with ``equivalences=()``. ``search`` discovers units and
    ``explain_conversion`` reports the special relations used by a conversion.
    """
    prefix_map=OrderedDict((
        # most common
        ('Kilo', 1E3), ('Milli', 1E-3), ('Centi', 1E-2),
        # second most common ones
        ('Giga', 1E9), ('Mega', 1E6), ('Micro', 1E-6),
        ('Nano', 1E-9), ('Pico', 1E-12), ('Femto', 1E-15),
        ('Atto', 1E-18), ('Tera', 1E12), ('Deci', 1E-1),
        # least common ones
        ('Hecto', 1E2), ('Deka', 1E1), ('Yotta', 1E24),
        ('Zetta', 1E21), ('Exa', 1E18), ('Peta', 1E15),
        ('Zepto', 1E-21), ('Yocto', 1E-24)
    ))
    postfix_map=OrderedDict((
        ("Squared", 2),
        ("Cubed", 3),
        ("Fourthed", 4),
        ("Fifthed", 5)
        # need a better way to do this... but that's for a later date
    ))
    def __init__(self, *, default_equivalences=("wavenumber",)):
        super().__init__("ConstantsData")
        self.default_equivalences = (default_equivalences,) if isinstance(default_equivalences, str) else tuple(default_equivalences)
        self._registry_revision = 0
        self._namespace = _UnitNamespace(self)
        self._unit_graph = UnitGraph()
        self._unit_names = set()
        self._conversion_factors = {}
        self._conversion_cache = {}
        self._unit_labels = None
        self._prefix_labels = None
        self._label_cache = {}
        self._label_style = "unicode"
        self._label_version = 0

    #region Unit Labels
    # Short labels for units ("cm⁻¹", "cm-1", "\\mathrm{cm^{-1}}") in three styles. The data is the supplement
    # TheRealMcCoy/UnitLabelsSupplement.json (base units and prefixes); other names are composed from it by `_label_factors`
    label_supplement = "UnitLabelsSupplement.json"

    label_styles = ("unicode", "ascii", "latex")

    @classmethod
    def check_label_style(cls, style):
        """``style`` if it is one of `label_styles`, else a ``ValueError``"""
        if style not in cls.label_styles:
            raise ValueError(f"unit label style must be one of {list(cls.label_styles)}, got {style!r}")
        return style

    @staticmethod
    def ascii_label(label):
        """An ASCII spelling of a unicode label: ``cm⁻¹`` -> ``cm-1``, ``Eₕ`` -> ``Eh``, ``Å`` -> ``Ang``, ``°`` -> ``deg``"""
        return "".join(_ASCII_WORDS.get(ch) or _SUP.get(ch) or _SUB.get(ch) or ch for ch in label)

    @staticmethod
    def latex_label(label):
        r"""A LaTeX (math mode, no ``$``) spelling of a unicode label: ``cm⁻¹`` -> ``\mathrm{cm^{-1}}``, ``Eₕ`` -> ``E_{\mathrm{h}}``"""
        if not label:
            return label
        if label == "°":
            return r"^{\circ}"
        if label == "%":
            return r"\%"
        m = re.match(rf"^(.*?)([{re.escape(_SUP_CHARS)}]+)$", label)
        base, power = (m.group(1), "".join(_SUP[c] for c in m.group(2))) if m else (label, None)
        m = re.match(rf"^(.*?)([{re.escape(_SUB_CHARS)}]+)$", base)
        if m and len(m.group(1)) == 1:               # a symbol with a subscript: E_h, a_0, m_e
            sub = "".join(_SUB[c] for c in m.group(2))
            body = f"{m.group(1)}_{{{sub}}}" if sub.isdigit() else f"{m.group(1)}_{{\\mathrm{{{sub}}}}}"
            return body if power is None else f"{body}^{{{power}}}"
        text = base.replace("Å", r"\AA ").replace("µ", r"\mu ").replace("μ", r"\mu ").replace("Ω", r"\Omega ")
        return f"\\mathrm{{{text}}}" if power is None else f"\\mathrm{{{text}^{{{power}}}}}"

    @classmethod
    def _label_row(cls, row):
        """``row`` with all three styles (a missing one is built from the unicode label)"""
        uni = row.get("unicode")
        if uni is None:
            raise ValueError(f"a unit label needs at least a unicode entry: {row!r}")
        return {"unicode": uni, "ascii": row.get("ascii") or cls.ascii_label(uni),
                "latex": row.get("latex") or cls.latex_label(uni)}

    @staticmethod
    def _prefixed_label(prefix, base):
        pl, bl = prefix["latex"], base["latex"]
        text = _MATHRM.fullmatch(bl)
        if pl.isalpha():
            latex = r"\mathrm{%s%s}" % (pl, text.group(1)) if text else r"\mathrm{%s}%s" % (pl, bl)
        else:
            latex = pl + (r"\mathrm{%s}" % text.group(1) if text else bl)
        return {"unicode": prefix["unicode"] + base["unicode"], "ascii": prefix["ascii"] + base["ascii"], "latex": latex}

    def _label_factors(self, name, _depth=0):
        """
        The factors ``[(label row, power), ...]`` a unit name stands for, or ``None`` if some part of it has no label.
        The grammar is the one the conversions use: ``A/B``, ``A B``, ``Inverse``, ``Squared``..., ``APerB``, prefixes.
        """
        name = name.strip()
        if not name or _depth > 8:
            return None
        table, prefixes = self._unit_labels, self._prefix_labels
        sub = lambda n: self._label_factors(n, _depth + 1)
        if "/" in name:
            top, *bottoms = name.split("/")
            a = sub(top)
            if a is None:
                return None
            for bottom in bottoms:
                b = sub(bottom)
                if b is None:
                    return None
                a += [(r, -p) for r, p in b]
            return a
        if len(name.split()) > 1:
            out = []
            for part in name.split():
                f = sub(part)
                if f is None:
                    return None
                out += f
            return out
        row = table.get(name)
        if row is not None:
            return sub(row["alias"]) if "alias" in row else [(self._label_row(row), 1)]
        if name.startswith("Inverse") and len(name) > 7:
            f = sub(name[7:])
            return None if f is None else [(r, -p) for r, p in f]
        for post, n in self.postfix_map.items():
            if name.endswith(post) and len(name) > len(post):
                f = sub(name[:-len(post)])
                return None if f is None else [(r, p * n) for r, p in f]
        m = _PER.search(name)
        if m:
            a, b = sub(name[:m.start()]), sub(name[m.end():])
            return None if a is None or b is None else a + [(r, -p) for r, p in b]
        for pre, prow in prefixes.items():
            if name.startswith(pre) and len(name) > len(pre):
                rest = name[len(pre):]
                f = sub(rest[0].upper() + rest[1:])
                if f is not None and len(f) == 1 and f[0][1] == 1:
                    return [(self._prefixed_label(self._label_row(prow), f[0][0]), 1)]
        return None

    @staticmethod
    def _label_power(sym, p, style):
        if p == 1:
            return sym
        if isinstance(p, Fraction):
            if p.denominator != 1:
                return sym + f"^({p})"
            p = p.numerator
        if style == "unicode":
            return sym + "".join(_SUP_OF[c] for c in str(p))
        return sym + ("^" if sym[-1:].isdigit() else "") + str(p)

    @classmethod
    def _render_label_factors(cls, factors, style):
        """The label of ``factors`` in ``style``: ``kcal/mol``, ``cm⁻¹``, ``m·s⁻²``; LaTeX never uses ``/``"""
        if len(factors) == 1 and factors[0][1] == 1:
            return factors[0][0][style]
        if style == "latex":
            groups = []                                 # consecutive upright-text factors share one \\mathrm{...}
            for row, p in factors:
                frag = row["latex"]
                text = _MATHRM.fullmatch(frag)
                exp = "" if p == 1 else "^{%s}" % p
                if text:
                    if groups and groups[-1][0] == "text":
                        groups[-1][1].append(text.group(1) + exp)
                    else:
                        groups.append(("text", [text.group(1) + exp]))
                else:
                    groups.append(("math", [frag + exp]))
            return r"\,".join(r"\mathrm{%s}" % r"\,".join(g) if kind == "text" else g[0] for kind, g in groups)
        num = [(r, p) for r, p in factors if p > 0]
        den = [(r, p) for r, p in factors if p < 0]
        joiner = "·" if style == "unicode" else " "
        if num and len(den) == 1 and den[0][1] == -1:
            return joiner.join(cls._label_power(r[style], p, style) for r, p in num) + "/" + den[0][0][style]
        return joiner.join(cls._label_power(r[style], p, style) for r, p in factors)

    def _load_label_data(self):
        if self._unit_labels is None:
            import json, os
            path = os.path.join(self._dir, self._pkg, self.label_supplement)
            data = {}
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
            self._unit_labels = {k: dict(v) for k, v in data.get("units", {}).items()}
            self._prefix_labels = {k: dict(v) for k, v in data.get("prefixes", {}).items()}
            self._label_cache = {}

    def _label_table(self):
        """``{unit name: {style: label}}`` for the base units that have a label of their own (or ``{"alias": name}``)"""
        self._load_label_data()
        return self._unit_labels

    @property
    def label_style(self):
        """The style `unit_label` uses when none is given: ``"unicode"``, ``"ascii"`` or ``"latex"``"""
        return self._label_style

    @property
    def label_version(self):
        """Increases whenever labels or the default style change (so callers can invalidate caches)"""
        return self._label_version

    def _labels_changed(self):
        self._label_version += 1
        self._label_cache = {}

    def set_label_style(self, style):
        """Sets the default label style (``"unicode"``, ``"ascii"`` or ``"latex"``)"""
        self._label_style = self.check_label_style(style)
        self._labels_changed()

    def unit_labels(self, style=None):
        """``{unit name: label}`` for the units that have a label listed (not the composed ones), in ``style``"""
        return {k: self.unit_label(k, style) for k in self._label_table()}

    def unit_label(self, unit, style=None):
        """Short labels for unit expressions and legacy/custom display names."""
        style = self._label_style if style is None else self.check_label_style(style)
        self._load_label_data()
        try:
            expression = self.unit(unit)
        except (ConversionError, ValueError, TypeError):
            if not isinstance(unit, str):
                return str(unit)
            factors = self._label_factors(unit)
            return unit if factors is None else self._render_label_factors(factors, style)
        factors = []
        for name, power in sorted(expression.factors, key=lambda item: (item[1] < 0, item[0] != 'Moles' if item[1] < 0 else False, item[0])):
            atom = self._label_factors(name)
            if atom is None:
                return str(unit)
            factors.extend((row, inner_power * power) for row, inner_power in atom)
        label = self._render_label_factors(factors, style) if factors else '1'
        if expression.scale != 1:
            label = f'{expression.scale:g}' + (r'\,' if style == 'latex' else ' ') + label
        return label

    def update_unit_labels(self, table, styles=None, overwrite=True):
        """
        Merges ``{unit name: {style: label}}`` (or ``{unit name: {"alias": other name}}``) into the base-unit labels
        (other keys are ignored). ``styles`` limits which styles are taken; ``overwrite=False`` only fills labels that
        are missing.
        """
        styles = self.label_styles if styles is None else [self.check_label_style(s) for s in styles]
        labels = self._label_table()
        for name, row in table.items():
            cur = labels.setdefault(name, {})
            if "alias" in row and (overwrite or not cur):
                cur.clear()
                cur["alias"] = row["alias"]
            for st in styles:
                if st in row and row[st] and (overwrite or st not in cur):
                    cur.pop("alias", None)
                    cur[st] = row[st]
        self._labels_changed()

    def load_unit_labels(self, path, **kw):
        """Merges a JSON label table (``{unit name: {style: label}}``) with `update_unit_labels`"""
        import json
        with open(path, encoding="utf-8") as f:
            self.update_unit_labels(json.load(f), **kw)
    #endregion

    # A compact physical basis: energy, length, time, charge, temperature, angle,
    # and luminous intensity. Mass and derived mechanical units reduce into it.
    # McUtils' existing mole convention counts N_A entities (a dimensionless count).
    _base_dimensions = {
        'Joules': {'E': 1}, 'Meters': {'L': 1}, 'Seconds': {'T': 1},
        'Kilograms': {'E': 1, 'T': 2, 'L': -2}, 'Coulombs': {'Q': 1},
        'Kelvins': {'K': 1}, 'Radians': {'A': 1}, 'Candelas': {'Cd': 1},
        'Moles': {}, 'Newtons': {'E': 1, 'L': -1}, 'Pascal': {'E': 1, 'L': -3},
        'Watts': {'E': 1, 'T': -1}, 'Amperes': {'Q': 1, 'T': -1},
        'Volts': {'E': 1, 'Q': -1}, 'Farads': {'Q': 2, 'E': -1},
        'Ohms': {'E': 1, 'T': 1, 'Q': -2}, 'Henry': {'E': 1, 'T': 2, 'Q': -2},
        'Teslas': {'E': 1, 'T': 1, 'Q': -1, 'L': -2}, 'Wb': {'E': 1, 'T': 1, 'Q': -1},
        'S': {'Q': 2, 'E': -1, 'T': -1}, 'Hertz': {'T': -1}, 'Steradians': {'A': 2},
    }
    _definitions = {
        'Grams': (.001, 'Kilograms'), 'Degrees': (math.pi / 180, 'Radians'),
        'Percent': (.01, ''), 'Wavenumbers': (1., 'InverseCentimeters'),
        'EVSeconds': (1., ('ElectronVolts', 'Seconds')),
        'MegaElectronVoltsFm': (1., ('MegaElectronVolts', 'FemtoMeters')),
        'AtomicUnitOfForce': (1., ('Hartrees', 'InverseBohrRadius')),
    }
    _type_hints = {
        'Hartrees': {'E': 1}, 'HartreesEnergy': {'E': 1}, 'ElectronVolts': {'E': 1},
        'AtomicMassUnits': {'E': 1, 'T': 2, 'L': -2},
        'UnifiedAtomicMassUnits': {'E': 1, 'T': 2, 'L': -2},
    }
    _unit_aliases = {
        'm': 'Meters', 'meter': 'Meters', 'meters': 'Meters',
        's': 'Seconds', 'second': 'Seconds', 'seconds': 'Seconds',
        'kg': 'Kilograms', 'kilogram': 'Kilograms', 'g': 'Grams', 'gram': 'Grams',
        'J': 'Joules', 'joule': 'Joules', 'joules': 'Joules',
        'K': 'Kelvins', 'kelvin': 'Kelvins', 'kelvins': 'Kelvins', 'Kelvin': 'Kelvins',
        'mol': 'Moles', 'mole': 'Moles', 'Mole': 'Moles',
        'N': 'Newtons', 'newton': 'Newtons', 'Pa': 'Pascal', 'W': 'Watts',
        'C': 'Coulombs', 'A': 'Amperes', 'V': 'Volts', 'F': 'Farads',
        'Ohm': 'Ohms', 'H': 'Henry', 'T': 'Teslas', 'Tesla': 'Teslas',
        'Hz': 'Hertz', 'Herz': 'Hertz', 'hertz': 'Hertz',
        'rad': 'Radians', 'radian': 'Radians', 'deg': 'Degrees', 'degree': 'Degrees',
        'sr': 'Steradians', 'cd': 'Candelas',
        'bohr': 'BohrRadius', 'bohrs': 'BohrRadius', 'a0': 'BohrRadius', 'a_0': 'BohrRadius',
        'angstrom': 'Angstroms', 'angstroms': 'Angstroms', 'Å': 'Angstroms', 'Ang': 'Angstroms',
        'hartree': 'Hartrees', 'hartrees': 'Hartrees', 'Ha': 'Hartrees', 'Eh': 'Hartrees',
        'eV': 'ElectronVolts', 'electronvolt': 'ElectronVolts', 'electronvolts': 'ElectronVolts',
        'amu': 'AtomicMassUnits', 'u': 'UnifiedAtomicMassUnits',
        'me': 'ElectronMass', 'm_e': 'ElectronMass', 'e': 'ElementaryCharge',
        'cal': 'Calories', 'calorie': 'Calories', 'erg': 'Ergs', 'D': 'Debyes', 'debye': 'Debyes',
        'wavenumber': 'Wavenumbers', 'wavenumbers': 'Wavenumbers',
        'AtomicUnitOfEnergy': 'Hartrees', 'AtomicUnitOfLength': 'BohrRadius',
        'AtomicUnitOfMass': 'ElectronMass', 'AtomicUnitOfCharge': 'ElementaryCharge',
        'SpeedOfLight': 'SpeedOfLightInVacuum',
        'cm': 'CentiMeters', 'mm': 'MilliMeters', 'nm': 'NanoMeters', 'pm': 'PicoMeters',
        'fs': 'FemtoSeconds', 'ps': 'PicoSeconds', 'ns': 'NanoSeconds', 'ms': 'MilliSeconds',
        'kcal': 'KiloCalories', 'kJ': 'KiloJoules', 'GHz': 'GigaHertz',
        'THz': 'TeraHertz', 'MHz': 'MegaHertz', 'kHz': 'KiloHertz',
    }
    _symbol_prefixes = {
        'Y': 'Yotta', 'Z': 'Zetta', 'E': 'Exa', 'P': 'Peta', 'T': 'Tera', 'G': 'Giga',
        'M': 'Mega', 'k': 'Kilo', 'h': 'Hecto', 'da': 'Deka', 'd': 'Deci', 'c': 'Centi',
        'm': 'Milli', 'u': 'Micro', 'µ': 'Micro', 'μ': 'Micro', 'n': 'Nano', 'p': 'Pico',
        'f': 'Femto', 'a': 'Atto', 'z': 'Zepto', 'y': 'Yocto',
    }

    @staticmethod
    def _power(value):
        if not isinstance(value, Real) or not math.isfinite(value):
            raise ValueError(f'unit powers must be finite real numbers, got {value!r}')
        return value if isinstance(value, Fraction) else Fraction(str(value))

    @staticmethod
    def _signature(pairs):
        values = {}
        for name, power in pairs:
            values[name] = values.get(name, 0) + power
        return tuple(sorted((name, power) for name, power in values.items() if power))

    def _expression(self, scale, factors):
        if not isinstance(scale, Real) or not math.isfinite(scale) or scale == 0:
            raise ValueError('a unit scale must be finite and nonzero')
        return UnitExpression(self, self._signature(factors), float(scale))

    def _prefix(self, name):
        if name in self._base_dimensions or name in self._definitions:
            return None
        for prefix, scale in self.prefix_map.items():
            if name.startswith(prefix) and len(name) > len(prefix):
                rest = name[len(prefix):]
                rest = self._aliases.get(rest, rest[0].upper() + rest[1:])
                return scale, rest
        return None

    def _atom(self, name, validate):
        name = self._aliases.get(name, name)
        pieces = _PER.split(name)
        if len(pieces) > 1:
            return self._parse('/'.join(pieces), validate)
        if name.startswith('Inverse') and len(name) > 7:
            rest = name[7:]
            if not (name in self._known_names and rest.startswith('Of')):
                scale, factors = self._atom(rest, validate)
                return 1 / scale, tuple((base, -power) for base, power in factors)
        for suffix, power in self.postfix_map.items():
            if name.endswith(suffix) and len(name) > len(suffix):
                scale, factors = self._atom(name[:-len(suffix)], validate)
                return scale ** power, tuple((base, exponent * power) for base, exponent in factors)
        prefix = self._prefix(name)
        if prefix is not None and name not in self._definition_overrides:
            # Keep the prefixed name for labels; its core definition supplies the scale.
            _, rest = prefix
            self._atom(rest, validate)
        elif name not in self._known_names:
            for symbol in sorted(self._symbol_prefixes, key=len, reverse=True):
                rest = name[len(symbol):]
                if name.startswith(symbol) and rest in self._aliases and rest:
                    name = self._symbol_prefixes[symbol] + self._aliases[rest]
                    break
            else:
                if validate:
                    raise ConversionError(f'Unknown unit {name!r}; use UnitsData.search() to discover unit names')
        return 1., ((name, Fraction(1)),)

    def _parse(self, specification, validate=True):
        if isinstance(specification, UnitExpression):
            if specification._handler is not self:
                raise ValueError('unit expressions from different registries cannot be mixed')
            return specification.scale, specification.factors
        if isinstance(specification, Real):
            if specification == 0 or not math.isfinite(specification):
                raise ValueError('a unit scale must be finite and nonzero')
            return float(specification), ()
        if not isinstance(specification, str):
            if not isinstance(specification, (tuple, list)):
                raise TypeError('units must be names, expressions, scalars, or nested list/tuple specifications')
            if isinstance(specification, (tuple, list)) and len(specification) == 2 and isinstance(specification[1], Real):
                scale, factors = self._parse(specification[0], validate)
                power = self._power(specification[1])
                return scale ** float(power), tuple((name, exponent * power) for name, exponent in factors)
            scale, factors = 1., ()
            for part in specification:
                new_scale, new_factors = self._parse(part, validate)
                scale *= new_scale
                factors += new_factors
            return scale, self._signature(factors)
        text = specification.strip()
        if not text:
            return 1., ()
        if text in self._known_names or text in self._aliases:
            # A table name may contain a hyphen, but slash/product names remain algebra.
            if not any(character in text for character in ' /()*^'):
                return self._atom(text, validate)
        text = text.replace('·', '*').replace('°', 'Degrees').replace('%', 'Percent')
        text = text.replace('a₀', 'BohrRadius').replace('Eₕ', 'Hartrees').replace('mₑ', 'ElectronMass')
        text = re.sub(r'(?<=[\w)])([' + re.escape(_SUP_CHARS) + r']+)',
                      lambda match: '**(' + ''.join(_SUP[ch] for ch in match.group()) + ')', text)
        text = re.sub(r'\bcm-1\b', '(cm**-1)', text)
        text = text.replace('^', '**')
        text = re.sub(r'(?<=[\w)])\s+(?=[\w(])', '*', text)
        try:
            tree = ast.parse(text, mode='eval').body
        except SyntaxError as error:
            raise ValueError(f'invalid unit expression {specification!r}') from error

        def numeric(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, Real):
                return self._power(node.value)
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
                value = numeric(node.operand)
                return -value if isinstance(node.op, ast.USub) else value
            if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.Mult)):
                left, right = numeric(node.left), numeric(node.right)
                if isinstance(node.op, ast.Div) and right == 0:
                    raise ValueError('a unit power cannot divide by zero')
                return left / right if isinstance(node.op, ast.Div) else left * right
            raise ValueError('a unit exponent must be a finite numeric power')

        def visit(node):
            if isinstance(node, ast.Name):
                return self._atom(node.id, validate)
            if isinstance(node, (ast.Constant, ast.UnaryOp)):
                return float(numeric(node)), ()
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
                scale, factors = visit(node.left)
                power = numeric(node.right)
                return scale ** float(power), tuple((name, exponent * power) for name, exponent in factors)
            if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Mult, ast.Div)):
                left_scale, left = visit(node.left)
                right_scale, right = visit(node.right)
                power = -1 if isinstance(node.op, ast.Div) else 1
                if power == -1 and right_scale == 0:
                    raise ValueError('a unit denominator scale must be nonzero')
                return left_scale * right_scale ** power, left + tuple((name, exponent * power) for name, exponent in right)
            raise ValueError(f'unsupported syntax in unit expression {specification!r}')
        scale, factors = visit(tree)
        return scale, self._signature(factors)

    @property
    def units(self):
        return self._namespace

    def unit(self, specification):
        """Parse aliases, legacy names/tuples, or safe products, quotients and powers."""
        self.data
        if isinstance(specification, UnitExpression) and specification._handler is self:
            return specification
        scale, factors = self._parse(specification)
        return self._expression(scale, factors)

    @classmethod
    def _unit_key(cls, unit):
        if isinstance(unit, UnitExpression):
            return str(unit)
        return tuple(cls._unit_key(part) for part in unit) if isinstance(unit, (list, tuple)) else unit

    def load(self):
        super().load()
        self._data = {key: dict(record) for key, record in self._data.items()}
        self._definition_overrides = {}
        self._custom_equivalences = {}
        self._load_unit_graph()

    def _load_unit_graph(self):
        """Classify the legacy table into core definitions and physical equivalences."""
        self._registry_revision += 1
        self._conversion_cache.clear()
        self._core_cache = {}
        self._aliases = dict(self._unit_aliases)
        self._known_names = set(self._base_dimensions) | set(self._definitions)
        def collect(specification):
            if isinstance(specification, str):
                self._known_names.add(specification)
            elif isinstance(specification, (list, tuple)):
                for part in specification:
                    collect(part)
        for key, record in self._data.items():
            collect(key)
            if isinstance(key, str):
                collect(record.get('Unit', ()))
        self._known_names.discard('None')
        self._dimension_hints = {name: self._signature(values.items())
                                 for name, values in {**self._base_dimensions, **self._type_hints}.items()}

        def dimension(specification):
            try:
                _, factors = self._parse(specification, validate=False)
            except (ValueError, TypeError):
                return None
            out = []
            for name, power in factors:
                value = self._dimension_hints.get(name)
                if value is None:
                    prefix = self._prefix(name)
                    if prefix is not None:
                        value = dimension(prefix[1])
                    elif name in self._definitions:
                        value = dimension(self._definitions[name][1])
                if value is None:
                    return None
                out.extend((base, exponent * power) for base, exponent in value)
            return self._signature(out)

        rules = [(key, record) for key, record in self._data.items()
                 if isinstance(key, tuple) and len(key) == 2 and 'Value' in record]
        # Unit fields anchor quantities before graph inference, preventing physical
        # cross-type rows from declaring Kelvin or inverse length to be energy.
        changed = True
        while changed:
            changed = False
            for name, record in self._data.items():
                if isinstance(name, str) and name not in self._dimension_hints and record.get('Unit') not in (None, 'None'):
                    value = dimension(record['Unit'])
                    if value is not None:
                        self._dimension_hints[name] = value
                        changed = True
            for (source, target), record in rules:
                for unknown, known in ((source, target), (target, source)):
                    if isinstance(unknown, str):
                        _, factors = self._parse(unknown, validate=False)
                        if len(factors) == 1 and factors[0][1] == 1:
                            name = factors[0][0]
                            if name not in self._dimension_hints:
                                value = dimension(known)
                                if value is not None:
                                    self._dimension_hints[name] = value
                                    changed = True
        factors = {}
        for (source, target), record in rules:
            source_dim, target_dim = dimension(source), dimension(target)
            if record.get('Equivalence') or (source_dim is not None and target_dim is not None and source_dim != target_dim):
                continue
            source, target = self._unit_key(source), self._unit_key(target)
            factors[(source, target)] = record['Value']
        for (source, target), value in list(factors.items()):
            factors.setdefault((target, source), 1 / value)
        self._conversion_factors = factors
        self._unit_graph = UnitGraph(factors)

    def _core(self, expression, active=()):
        self.data
        key = expression.scale, expression.factors
        if not active and key in self._core_cache:
            return self._core_cache[key]
        scale = expression.scale
        dimensions = []
        for name, power in expression.factors:
            factor_scale, factor_dimensions = self._resolve_atom(name, active)
            scale *= factor_scale ** float(power)
            dimensions.extend((base, exponent * power) for base, exponent in factor_dimensions)
        result = scale, self._signature(dimensions)
        if not active:
            self._core_cache[key] = result
        return result

    def _core_spec(self, specification, active=()):
        scale, factors = self._parse(specification)
        return self._core(self._expression(scale, factors), active)

    def _resolve_atom(self, name, active):
        if name in active:
            raise ConversionError(f'cyclic unit definition involving {name!r}')
        active = active + (name,)
        override = self._definition_overrides.get(name)
        if override is not None:
            coefficient, specification = override
            scale, dimensions = self._core_spec(specification, active)
            return coefficient * scale, dimensions
        parsed_scale, parsed = self._parse(name, validate=False)
        if parsed != ((name, Fraction(1)),):
            return self._core(self._expression(parsed_scale, parsed), active)
        if name in self._base_dimensions:
            coefficient = self.constant('AvogadroConstant') if name == 'Moles' else 1.
            return coefficient, self._signature(self._base_dimensions[name].items())
        if name in self._definitions:
            coefficient, specification = self._definitions[name]
            scale, dimensions = self._core_spec(specification, active)
            return coefficient * scale, dimensions
        prefix = self._prefix(name)
        if prefix is not None:
            coefficient, base = prefix
            scale, dimensions = self._resolve_atom(base, active)
            return coefficient * scale, dimensions
        record = self._data.get(name)
        if record is not None and record.get('Unit') not in (None, 'None'):
            try:
                scale, dimensions = self._core_spec(record['Unit'], active)
            except (ConversionError, ValueError, TypeError):
                pass
            else:
                coefficient = self._data.get((name, self._unit_key(record['Unit'])), record)['Value']
                return coefficient * scale, dimensions
        queue, seen = deque([(name, 1.)]), {name}
        while queue:
            current, coefficient = queue.popleft()
            if current != name:
                try:
                    scale, parsed = self._parse(current)
                    if (parsed != ((current, Fraction(1)),) or current in self._base_dimensions
                            or current in self._definitions or current in self._data
                            or current in self._definition_overrides
                            or (isinstance(current, str) and self._prefix(current) is not None)):
                        unit_scale, dimensions = self._core(self._expression(scale, parsed), active)
                        return coefficient * unit_scale, dimensions
                except (ConversionError, ValueError, TypeError):
                    pass
            for neighbor in sorted(self._unit_graph._graph.get(current, ()),
                                   key=lambda item: (0 if isinstance(item, str) and item in self._base_dimensions else
                                                     1 if isinstance(item, tuple) else 2, repr(item))):
                if neighbor not in seen and neighbor not in active:
                    seen.add(neighbor)
                    queue.append((neighbor, coefficient * self._conversion_factors[(current, neighbor)]))
        # Registered primitives without a physical anchor still have ordinary algebra.
        # A shared scalar component gets one stable formal dimension and a relative scale.
        component_nodes, pending = {name}, deque([name])
        while pending:
            current = pending.popleft()
            for node in self._unit_graph._graph.get(current, ()):
                if isinstance(node, str) and node not in component_nodes:
                    component_nodes.add(node)
                    pending.append(node)
        component = sorted((node for node in component_nodes if self._parse(node, False)[1] == ((node, Fraction(1)),)),
                           key=lambda item: (item in self._definition_overrides, item))
        anchor = component[0] if component else name
        path = self._unit_graph.find_path_bfs(name, anchor)
        coefficient = 1.
        if path is not None:
            for source, target in zip(path, path[1:]):
                coefficient *= self._conversion_factors[(source, target)]
        dimensions = self._dimension_hints.get(name, ((f'unit:{anchor}', Fraction(1)),))
        return coefficient, dimensions

    def _bridges(self):
        h, c, kb = (self.constant(name) for name in ('PlanckConstant', 'SpeedOfLightInVacuum', 'BoltzmannConstant'))
        bridges = {
            'wavenumber': (h * c, self._signature({'E': 1, 'L': 1}.items()), 'E = h c sigma'),
            'thermal': (kb, self._signature({'E': 1, 'K': -1}.items()), 'E = k_B T'),
            'frequency': (h, self._signature({'E': 1, 'T': 1}.items()), 'E = h nu'),
            'mass_energy': (c ** 2, self._signature({'L': 2, 'T': -2}.items()), 'E = m c^2'),
            'angular_frequency': (h / (2 * math.pi), self._signature({'E': 1, 'T': 1, 'A': -1}.items()), 'E = hbar omega'),
        }
        return dict(bridges, **self._custom_equivalences)

    def _enabled_equivalences(self, equivalences):
        names = self.default_equivalences if equivalences is None else ((equivalences,) if isinstance(equivalences, str) else tuple(equivalences))
        enabled = frozenset(names)
        unknown = enabled - self._bridges().keys()
        if unknown:
            raise ValueError(f'unknown equivalences {sorted(unknown)}; available: {sorted(self._bridges())}')
        return enabled

    @property
    def equivalences(self):
        """Discover named physical bridges independently of which are enabled."""
        self.data
        return {name: {'factor': factor, 'dimensions': dict(dimensions), 'relation': relation}
                for name, (factor, dimensions, relation) in self._bridges().items()}

    def _bridge_solutions(self, difference, enabled):
        # Reuse McUtils' exact rational matrix inverse on the small Gram system.
        from ..Numputils import rational_matrix_inverse
        bridges = self._bridges()
        dimensions = sorted(set(dict(difference)) | {base for name in enabled for base, _ in bridges[name][1]})
        rhs = [dict(difference).get(base, 0) for base in dimensions]
        for size in range(1, len(enabled) + 1):
            solutions = []
            for names in combinations(sorted(enabled), size):
                columns = [[dict(bridges[name][1]).get(base, 0) for base in dimensions] for name in names]
                gram = [[sum(x * y for x, y in zip(left, right)) for right in columns] for left in columns]
                try:
                    inverse = rational_matrix_inverse(gram)
                except ValueError:
                    continue
                projected = [sum(x * y for x, y in zip(column, rhs)) for column in columns]
                powers = tuple(sum(x * y for x, y in zip(row, projected)) for row in inverse)
                if not all(powers) or any(sum(column[i] * power for column, power in zip(columns, powers)) != rhs[i] for i in range(len(rhs))):
                    continue
                factor = math.prod(bridges[name][0] ** float(power) for name, power in zip(names, powers))
                solutions.append((sum(map(abs, powers)), factor, tuple(zip(names, powers))))
            if solutions:
                solutions.sort(key=lambda item: (item[0], item[2]))
                best = solutions[0]
                if any(cost == best[0] and not math.isclose(factor, best[1], rel_tol=1e-10)
                       for cost, factor, _ in solutions[1:]):
                    raise ConversionError('ambiguous energy equivalences give different conversion factors')
                return best[1], best[2]
        return None

    def explain_conversion(self, unit, target, *, equivalences=None):
        """Factor and core/fallback provenance, including powers of any special bridges."""
        source, destination = self.unit(unit), self.unit(target)
        enabled = self._enabled_equivalences(equivalences)
        key = self._registry_revision, enabled, source.scale, source.factors, destination.scale, destination.factors
        if key in self._conversion_cache:
            factor, stage, selected = self._conversion_cache[key]
        else:
            source_scale, source_dimensions = self._core(source)
            target_scale, target_dimensions = self._core(destination)
            factor = source_scale / target_scale
            selected = ()
            if source_dimensions == target_dimensions:
                stage = 'core'
            else:
                difference = self._signature(target_dimensions + tuple((name, -power) for name, power in source_dimensions))
                applicable = set(self._bridges())
                mass_dimension = self._signature(self._base_dimensions['Kilograms'].items())
                if not any(self._resolve_atom(name, ())[1] == mass_dimension
                           for name, _ in source.factors + destination.factors):
                    # E = m c^2 is a mass/energy interpretation, not a generic
                    # permission to use sqrt(c^2) between length and time units.
                    applicable.discard('mass_energy')
                active = enabled & applicable
                solution = self._bridge_solutions(difference, active) if active else None
                if solution is None:
                    available = applicable - enabled
                    suggestions = []
                    for count in range(1, len(available) + 1):
                        for extra in combinations(sorted(available), count):
                            if self._bridge_solutions(difference, active | set(extra)) is not None:
                                suggestions.append(tuple(sorted(enabled | set(extra))))
                        if suggestions:
                            break
                    message = (f'Cannot convert {unit!s} to {target!s}. Enabled equivalences: '
                               + (', '.join(sorted(enabled)) or 'none') + '.')
                    if suggestions:
                        message += ' A different implicit energy equivalence supplies the relationship; pass ' + ' or '.join(f'equivalences={names!r}' for names in suggestions) + '.'
                    else:
                        message += ' No registered energy equivalence supplies the missing dimensions; a different explicitly registered equivalence may be required.'
                    raise ConversionError(message)
                extra_factor, selected = solution
                factor *= extra_factor
                stage = 'equivalence'
            self._conversion_cache[key] = factor, stage, selected
        return {'factor': factor, 'stage': stage, 'enabled_equivalences': tuple(sorted(enabled)),
                'bridges': tuple({'name': name, 'power': power, 'relation': self._bridges()[name][2]}
                                 for name, power in selected)}

    def convert(self, unit, target, *, equivalences=None):
        """Numeric factor. Core algebra always wins; only wavenumber is enabled by default.

        Pass equivalences=() for core-only conversions, or an explicit collection
        such as ('thermal',) or ('wavenumber', 'frequency') for optional fallbacks.
        """
        return self.explain_conversion(unit, target, equivalences=equivalences)['factor']

    def find_conversion(self, unit, target, *, equivalences=None):
        return self.convert(unit, target, equivalences=equivalences)

    def add_conversion(self, unit, target, value, *, equivalence=None):
        """Define a unit against another expression, or register a named special bridge."""
        if not isinstance(value, Real) or not math.isfinite(value) or value == 0:
            raise ValueError('conversion factor must be finite and nonzero')
        self.data
        if equivalence is not None:
            if not isinstance(equivalence, str) or not equivalence:
                raise ValueError('an equivalence needs a nonempty string name')
            source, destination = self._core(self.unit(unit)), self._core(self.unit(target))
            difference = self._signature(destination[1] + tuple((name, -power) for name, power in source[1]))
            if not difference:
                raise ValueError('special equivalences must connect different core dimensions')
            self._custom_equivalences[equivalence] = (value * destination[0] / source[0], difference, f'{unit} -> {target}')
            self._registry_revision += 1
            self._conversion_cache.clear()
            return
        unit, target = self._unit_key(unit), self._unit_key(target)
        if unit == target and value != 1:
            raise ValueError("a unit's conversion to itself must be 1")
        if unit == target:
            self._data[(unit, target)] = {'Value': 1., 'Conversion': (unit, target)}
            self._load_unit_graph()
            return
        try:
            source_dimensions = self._core(self.unit(unit))[1]
            target_dimensions = self._core(self.unit(target))[1]
        except ConversionError:
            pass  # A new named unit acquires its dimensions from its definition.
        else:
            if source_dimensions != target_dimensions and not any(
                    name.startswith('unit:') for name, _ in source_dimensions + target_dimensions):
                raise ValueError('cross-dimensional conversions require an explicitly named equivalence')
        _, source_factors = self._parse(unit, validate=False)
        _, target_factors = self._parse(target, validate=False)
        if len(source_factors) == 1 and source_factors[0][1] == 1:
            name = source_factors[0][0]
            if name in self._base_dimensions:
                if len(target_factors) != 1 or target_factors[0][1] != 1 or target_factors[0][0] in self._base_dimensions:
                    raise ValueError('base units cannot be redefined; define a named unit or special equivalence')
                name, unit, target, value = target_factors[0][0], target, unit, 1 / value
            prior = self._definition_overrides.get(target)
            if prior is not None and prior[1] == unit:
                self._definition_overrides.pop(target)
            self._definition_overrides[name] = value, target
        else:
            raise ValueError('register a named unit against a unit expression')
        self._data[(unit, target)] = {'Value': value, 'Conversion': (unit, target)}
        self._data[(target, unit)] = {'Value': 1 / value, 'Conversion': (target, unit)}
        self._load_unit_graph()

    def search(self, query='', *, equivalences=None):
        """Discover registered unit names/aliases, or units convertible to a quantity type."""
        self.data
        quantities = {'energy': 'Joules', 'force': 'Newtons', 'length': 'Meters', 'mass': 'Kilograms',
                      'temperature': 'Kelvins', 'frequency': 'Hertz', 'time': 'Seconds'}
        destination = quantities.get(query.lower())
        out = []
        for name in sorted(self._known_names):
            if any(character in name for character in ' /()*^') or name.startswith('Inverse'):
                continue
            aliases = tuple(sorted(alias for alias, canonical in self._aliases.items() if canonical == name))
            if destination is None and query.lower() not in ' '.join((name,) + aliases).lower():
                continue
            try:
                expression = self.unit(name)
                if destination is None:
                    details = {'stage': 'core', 'bridges': ()}
                else:
                    details = self.explain_conversion(expression, destination, equivalences=equivalences)
                out.append({'name': name, 'label': expression.label(), 'aliases': aliases,
                            'dimensions': expression.dimensions, 'stage': details['stage'],
                            'equivalences': tuple(item['name'] for item in details['bridges'])})
            except (ConversionError, ValueError, TypeError):
                continue
        return sorted(out, key=lambda item: (item['stage'] != 'core', item['name']))



    @property
    def constants(self):
        return [k for k in self.data.keys() if isinstance(k, str)]
    def constant(self, const):
        """Converts base unit into target using the scraped NIST data

        :param unit:
        :type unit:
        :param target:
        :type target:
        :return:
        :rtype:
        """
        return self[const]['Value']

    # Conveniences
    Wavenumbers = "Wavenumbers"
    Hartrees = "Hartrees"
    Angstroms = "Angstroms"
    BohrRadius = "BohrRadius"
    ElectronMass = "ElectronMass"
    AtomicMassUnits = "AtomicMassUnits"
    ElectronVolts = "ElectronVolts"
    KilocaloriesPerMole = "Kilocalories/Mole"
    KilojoulesPerMole = "Kilojoules/Mole"
    @property
    def hartrees_to_wavenumbers(self): # soooo common
        return self.convert("Hartrees", "Wavenumbers")
    @property
    def bohr_to_angstroms(self):
        return self.convert("BohrRadius", "Angstroms")
    @property
    def amu_to_me(self):
        return self.convert("AtomicMassUnits", "ElectronMass")
    @property
    def moles(self):
        return self.constant('AvogadroConstant')

    #endregion


UnitsData = UnitsDataHandler()
UnitsData.__doc__ = """An instance of UnitsDataHandler that can be used for unit conversion and fundamental constant lookups"""
UnitsData.__name__ = "UnitsData"