"""
Units and themes for readouts.

* `ReadoutUnits` is part of the *content*: it is applied once while a readout is built, so
  every renderer and every export reports the same numbers in the same units.
* `ReadoutTheme` is pure presentation (fonts, colours, digits, slide geometry, lighting) and
  can be swapped freely at render time.
"""

import copy
import math
import numbers
import os
import warnings

import numpy as np

__all__ = [
    "ReadoutUnits",
    "ReadoutTheme",
]


class ReadoutUnits:
    """
    Display-unit preferences, keyed by quantity kind.

    ``convert(values, quantity, source_unit)`` returns ``(converted_values, unit)``. Quantities
    without a preference are returned unchanged in their source unit.
    """
    default_units = {
        "length": "Angstroms",
        "angle": "Degrees",
        "frequency": "Wavenumbers",
        "energy": "Hartrees",
        "mass": "AtomicMassUnits",
        "charge": None,
        "intensity": None,
        "time": None,
    }
    # factors used when `UnitsData` has no direct conversion
    local_factors = {
        ("Radians", "Degrees"): 180 / math.pi,
        ("Degrees", "Radians"): math.pi / 180,
        ("Hartrees", "ElectronVolts"): 27.211386245988,
        ("Hartrees", "KilocaloriesPerMole"): 627.5094740631,
        ("Hartrees", "KilojoulesPerMole"): 2625.4996394799,
    }

    def __init__(self, units=None, **overrides):
        if isinstance(units, ReadoutUnits):
            base = dict(units.units)
        else:
            base = dict(self.default_units)
            if isinstance(units, str):
                if units not in ("default", "atomic"):
                    raise ValueError(f"unknown unit preset {units!r}")
                if units == "atomic":
                    base = {k: None for k in base}
            elif units is not None:
                base.update(units)
        base.update(overrides)
        self.units = base

    @classmethod
    def resolve(cls, units):
        if isinstance(units, cls):
            return units
        return cls(units)

    def target_unit(self, quantity, source_unit=None):
        target = self.units.get(quantity)
        return source_unit if target is None else target

    @classmethod
    def conversion_factor(cls, source, target):
        if source is None or target is None or source == target:
            return 1
        key = (source, target)
        if key in cls.local_factors:
            return cls.local_factors[key]
        if (target, source) in cls.local_factors:
            return 1 / cls.local_factors[(target, source)]
        from ...Data import UnitsData
        return UnitsData.convert(source, target)

    def convert(self, values, quantity, source_unit):
        target = self.target_unit(quantity, source_unit)
        if target == source_unit or source_unit is None:
            return values, source_unit
        try:
            factor = self.conversion_factor(source_unit, target)
        except Exception as e:
            warnings.warn(f"can't convert {quantity} from {source_unit} to {target} ({e}); keeping {source_unit}")
            return values, source_unit
        if isinstance(values, numbers.Number):
            return values * factor, target
        return np.asarray(values) * factor, target

    def __repr__(self):
        return f"{type(self).__name__}({ {k: v for k, v in self.units.items() if v is not None} })"


def _deep_merge(base, update):
    out = copy.deepcopy(base)
    for k, v in (update or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


_STUDIO_LIGHTING = [
    {"type": "ambient", "color": (.5, .5, .5), "illuminance": .5},
    {"type": "point", "position": (.61, 1.97, .454), "color": (1, .75, .5), "intensity": 9.765625},
    {"type": "point", "position": (-1.055, 1.420, 1.601), "color": (.4, .6, .95), "intensity": 12.25},
    {"type": "point", "position": (-1.048, 1.613, -.966), "color": (.86837, .727, 1), "intensity": 3.125},
]


class ReadoutTheme:
    """
    Style tokens consulted by every renderer. Values are looked up with dotted keys
    (``theme.get('colors.primary')``); presets are merged with user dictionaries.
    """
    default_tokens = {
        "font": {
            "family": "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif",
            "mono": "Menlo, Consolas, 'DejaVu Sans Mono', monospace",
            "pptx_family": "Arial",
        },
        # point sizes, used for PowerPoint; HTML scales them by `html.font_scale`
        "sizes": {
            "title": 32, "subtitle": 18, "section": 24, "subsection": 18,
            "body": 14, "caption": 12, "table": 12, "scene_caption": 20,
        },
        "colors": {
            "text": "1F2328", "muted": "656D76", "primary": "1F4E79", "accent": "C55A11",
            "rule": "D0D7DE", "header_fill": "1F4E79", "header_text": "FFFFFF",
            "stripe": "F3F6F9", "background": "FFFFFF", "field_label": "656D76",
        },
        "formats": {
            "length": "{:.5f}", "angle": "{:.2f}", "frequency": "{:.1f}", "energy": "{:.8f}",
            "mass": "{:.5f}", "intensity": "{:.2f}", "charge": "{:d}", "index": "{:d}",
            "float": "{:.6g}", "int": "{:d}",
        },
        "unit_labels": {
            "Angstroms": "Å", "BohrRadius": "a₀", "Degrees": "°", "Radians": "rad",
            "Wavenumbers": "cm⁻¹", "Hartrees": "Eₕ", "ElectronVolts": "eV",
            "KilocaloriesPerMole": "kcal/mol", "KilojoulesPerMole": "kJ/mol",
            "AtomicMassUnits": "amu", "ElectronMass": "mₑ", "KilometersPerMole": "km/mol",
            "Seconds": "s",
        },
        "slide": {
            "size": (960, 540), "units": "pt",
            "margin": (28, 40, 24, 40),           # top, right, bottom, left
            "title_height": 44, "gap": 12,
            "row_height": 21, "line_height": 1.3, "cell_padding": (3, 6, 3, 6),
            "max_table_rows": 16, "min_table_rows": 3,
            "scene_size": (490, 370), "scene_caption_height": 40, "gallery_per_slide": 1,
            "field_label_fraction": .28, "title_slide": True, "pack_sections": True,
        },
        "scene": {
            "fov": 45, "padding": 1.15, "metres_per_unit": 0.03, "background": "white",
            "poster_scale": 2, "lighting": _STUDIO_LIGHTING,
        },
        "html": {
            "font_scale": 1.0, "max_width": 1100, "scene_size": (460, 340),
            "gallery_scene_size": (320, 260), "table_max_height": 380, "collapsible": True,
        },
    }

    presets = {
        "default": {},
        "compact": {
            "sizes": {"title": 26, "section": 20, "subsection": 15, "body": 12, "caption": 10,
                      "table": 10, "scene_caption": 16},
            "slide": {"row_height": 17, "max_table_rows": 22, "gallery_per_slide": 3},
            "html": {"font_scale": .9, "gallery_scene_size": (260, 220)},
        },
        "talk": {
            "sizes": {"title": 40, "section": 30, "subsection": 22, "body": 18, "caption": 14,
                      "table": 16, "scene_caption": 28},
            "slide": {"row_height": 28, "max_table_rows": 10},
        },
    }

    def __init__(self, tokens=None, preset="default", **overrides):
        base = _deep_merge(self.default_tokens, self.presets[preset] if isinstance(preset, str) else preset)
        base = _deep_merge(base, tokens)
        base = _deep_merge(base, overrides)
        self.tokens = base

    @classmethod
    def resolve(cls, style=None):
        if isinstance(style, cls):
            return style
        if style is None:
            style = os.environ.get("MCUTILS_READOUT_THEME", "default")
        if isinstance(style, str):
            if style not in cls.presets:
                raise ValueError(f"unknown readout theme {style!r}; known: {sorted(cls.presets)}")
            return cls(preset=style)
        if isinstance(style, dict):
            style = dict(style)
            preset = style.pop("preset", "default")
            return cls(style, preset=preset)
        raise TypeError(f"can't interpret {style!r} as a readout theme")

    def updated(self, tokens=None, **overrides):
        new = copy.copy(self)
        new.tokens = _deep_merge(_deep_merge(self.tokens, tokens), overrides)
        return new

    def get(self, key, default=None):
        node = self.tokens
        for k in key.split("."):
            if not isinstance(node, dict) or k not in node:
                return default
            node = node[k]
        return node

    def __getitem__(self, key):
        val = self.get(key, KeyError)
        if val is KeyError:
            raise KeyError(key)
        return val

    def get_format(self, quantity, value=None):
        fmts = self.tokens["formats"]
        if quantity is not None and quantity in fmts:
            fmt = fmts[quantity]
            if isinstance(fmt, str) and fmt.endswith("d}") and not isinstance(value, (int, np.integer)):
                return None
            return fmt
        if isinstance(value, (bool, np.bool_)):
            return "{}"
        if isinstance(value, (int, np.integer)):
            return fmts.get("int", "{}")
        if isinstance(value, (float, np.floating)):
            return fmts.get("float", "{:.6g}")
        return "{}"

    def get_unit_label(self, unit):
        return self.tokens["unit_labels"].get(unit, unit)

    def color(self, name):
        return self.tokens["colors"].get(name, name)

    def css_color(self, name):
        c = self.color(name)
        return c if c.startswith("#") or not all(ch in "0123456789abcdefABCDEF" for ch in c) else "#" + c
