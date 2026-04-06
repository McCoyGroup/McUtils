import itertools
import re
import numbers
import uuid
from xml.etree import ElementTree
import weakref, numpy as np, copy, textwrap, inspect
import contextlib

__all__ = [
    "HTML",
    "CSS",
    "ContentXML",
    "SVG",
]

from ...Data import ColorData
from ...Misc import mixedmethod
from .Enums import Options
from .WidgetTools import frozendict

class ValidationError(ValueError):
    ...

_CSS_COLOR_KEYWORDS = {
    "none", "inherit", "currentcolor", "transparent"
}

_RE_HEX3  = re.compile(r"^#[0-9a-f]{3}$",  re.I)
_RE_HEX4  = re.compile(r"^#[0-9a-f]{4}$",  re.I)
_RE_HEX6  = re.compile(r"^#[0-9a-f]{6}$",  re.I)
_RE_HEX8  = re.compile(r"^#[0-9a-f]{8}$",  re.I)
_RE_RGB   = re.compile(r"^rgb\(\s*(\d+%?)\s*,\s*(\d+%?)\s*,\s*(\d+%?)\s*\)$", re.I)
_RE_RGBA  = re.compile(r"^rgba\(\s*(\d+%?)\s*,\s*(\d+%?)\s*,\s*(\d+%?)\s*,\s*([0-9.]+)\s*\)$", re.I)
_RE_HSL   = re.compile(r"^hsl\(\s*[\d.]+\s*,\s*[\d.]+%\s*,\s*[\d.]+%\s*\)$",  re.I)
_RE_HSLA  = re.compile(r"^hsla\(\s*[\d.]+\s*,\s*[\d.]+%\s*,\s*[\d.]+%\s*,\s*[0-9.]+\s*\)$", re.I)
_RE_URL   = re.compile(r"^url\(#[^)]+\)$")
_RE_NUM   = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")
_RE_LEN   = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?(px|pt|pc|mm|cm|in|em|ex|rem|vh|vw|vmin|vmax|%)?$")
_RE_ANGLE = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)(deg|rad|grad|turn)?$", re.I)


def _is_number(v: str|numbers.Number) -> bool:
    return isinstance(v, numbers.Number) or bool(_RE_NUM.match(v.strip()))

def _is_length(v: str) -> bool:
    return bool(_RE_LEN.match(v.strip()))

def _is_angle(v: str) -> bool:
    return bool(_RE_ANGLE.match(v.strip()))

def _is_color(v: str) -> bool:
    s = v.strip().lower()
    return (
        s in _CSS_COLOR_KEYWORDS
        or s in ColorData['Named'].data
        or bool(_RE_HEX3.match(s))
        or bool(_RE_HEX4.match(s))
        or bool(_RE_HEX6.match(s))
        or bool(_RE_HEX8.match(s))
        or bool(_RE_RGB.match(s))
        or bool(_RE_RGBA.match(s))
        or bool(_RE_HSL.match(s))
        or bool(_RE_HSLA.match(s))
    )


def _is_paint(v: str) -> bool:
    """Paint value: colour, none, inherit, or url(#id) optionally followed by a fallback colour."""
    s = v.strip()
    if _is_color(s):
        return True
    if _RE_URL.match(s):
        return True
    # url(#id) <fallback-color>
    m = re.match(r"^(url\(#[^)]+\))\s+(.+)$", s)
    if m:
        return _is_color(m.group(2))
    return False


def _is_opacity(v: str|numbers.Number) -> bool:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return False
    else:
        return 0.0 <= f <= 1.0

def _check_oneof(value, attr, types) -> list[ValidationError]:
    if value not in types:
        types = sorted(list(types))
        if len(types) == 1:
            typeset = f"'{types[0]}'"
        elif len(types) == 2:
            typeset = f"'{types[0]}' or '{types[1]}'"
        else:
            typeset = ", ".join(f"'{t}'" for t in types[:-1]) + f" or '{types[-1]}'"
        return [ValidationError(attr, value, f"must be {typeset}")]
    else:
        return []

# ── fill & stroke ──────────────────────────────────────────────────────────

def _check_paint(attr: str, value) -> list[ValidationError]:
    if not isinstance(value, str):
        return [ValidationError(attr, value, "must be a string")]
    elif not _is_paint(value):
        return [ValidationError(attr, value,
                    "must be a color, 'none', 'inherit', 'currentColor', or url(#id)")]
    else:
        return []

def check_fill(value): return _check_paint("fill", value)
def check_stroke(value): return _check_paint("stroke", value)
def check_color(value): return _check_paint("color", value)
def check_flood_color(value):_check_paint("flood-color", value)
def check_stop_color(value): _check_paint("stop-color", value)
def check_lighting_color(value): return _check_paint("lighting-color", value)

# ── opacity ────────────────────────────────────────────────────────────────

def _check_opacity_attr(attr: str, value) -> list[ValidationError]:
    if isinstance(value, str) and value.strip().lower() == "inherit":
        return []
    elif not _is_opacity(value):
        return [ValidationError(attr, value, "must be a number in [0, 1] or 'inherit'")]
    else:
        return []

def check_opacity(value): return _check_opacity_attr("opacity", value)
def check_fill_opacity(value): return _check_opacity_attr("fill-opacity", value)
def check_stroke_opacity(value): return _check_opacity_attr("stroke-opacity", value)
def check_flood_opacity(value): return _check_opacity_attr("flood-opacity", value)
def check_stop_opacity(value): return _check_opacity_attr("stop-opacity", value)


# ── fill-rule ──────────────────────────────────────────────────────────────

def check_fill_rule(value) -> list[ValidationError]:
    if value not in ("nonzero", "evenodd", "inherit"):
        return [ValidationError("fill-rule", value, "must be 'nonzero', 'evenodd', or 'inherit'")]
    else:
        return []

# ── stroke-width ───────────────────────────────────────────────────────────

def check_stroke_width(value) -> list[ValidationError]:
    if isinstance(value, str) and value.strip().lower() == "inherit":
        return []
    if isinstance(value, numbers.Number):
        if value < 0: return [ValidationError("stroke-width", value, "must be non-negative")]
        value = f"{value:.0f}px"
    s = str(value).strip()
    if not _is_length(s):
        return [ValidationError("stroke-width", value, "must be a non-negative length or 'inherit'")]
    else:
        value = re.sub(r"[a-z%]+$", "", s, flags=re.I)
        try:
            value = float(value)
        except (TypeError, ValueError):
            return [ValidationError("stroke-width", value, "must be a non-negative length or 'inherit'")]
        else:
            if value < 0:
                return [ValidationError("stroke-width", value, "must be a non-negative length or 'inherit'")]
            else:
                return []


# ── stroke-linecap ─────────────────────────────────────────────────────────
linecap_types = {"butt", "round", "square", "inherit"}
def check_stroke_linecap(value) -> list[ValidationError]:
    return _check_oneof(value, "stroke-linecap", linecap_types)

# ── stroke-linejoin ────────────────────────────────────────────────────────
linejoin_types = {"miter", "miter-clip", "round", "bevel", "arcs", "inherit"}
def check_stroke_linejoin(value) -> list[ValidationError]:
    return _check_oneof(value, "stroke-linejoin", linejoin_types)

# ── stroke-miterlimit ──────────────────────────────────────────────────────

def check_stroke_miterlimit(value) -> list[ValidationError]:
    if isinstance(value, str) and value.strip().lower() == "inherit":
        return []
    if isinstance(value, str):
        try:
            value = float(value)
        except (TypeError, ValueError):
            return [ValidationError("stroke-miterlimit", value, "must be a number ≥ 1 or 'inherit'")]
    if value < 1:
        return  [
            ValidationError("stroke-miterlimit", value, "must be ≥ 1")
        ]
    else:
        return []


# ── stroke-dasharray ───────────────────────────────────────────────────────

def check_stroke_dasharray(value) -> list[ValidationError]:
    if not isinstance(value, str):
        value = " ".join(f"{v:.0f}px" if not isinstance(v, str) else v for v in value)
    s = value.strip().lower()
    if s in ("none", "inherit"):
        return []
    tokens = re.split(r"[\s,]+", s)
    bad = [t for t in tokens if t and not _is_length(t)]
    if len(bad) > 0:
        return [ValidationError("stroke-dasharray", value,
                                f"contains invalid length tokens: {bad}")]
    else:
        return []


# ── stroke-dashoffset ──────────────────────────────────────────────────────

def check_stroke_dashoffset(value) -> list[ValidationError]:
    if isinstance(value, str) and value.strip().lower() == "inherit":
        return []
    if not isinstance(value, str):
        value = f"{value:.0f}px"
    if not _is_length(str(value).strip()):
        return [ValidationError("stroke-dashoffset", value,
                                "must be a length/percentage or 'inherit'")]
    else:
        return []

# ── visibility ─────────────────────────────────────────────────────────────
visibility_types = {"visible", "hidden", "collapse", "inherit"}
def check_visibility(value) -> list[ValidationError]:
    return _check_oneof(value, "visibility", visibility_types)

# ── display ────────────────────────────────────────────────────────────────

display_types = {
    "inline", "block", "list-item", "run-in", "compact",
    "marker", "table", "inline-table", "table-row-group",
    "table-header-group", "table-footer-group", "table-row",
    "table-column-group", "table-column", "table-cell",
    "table-caption", "none", "inherit",
}
def check_display(value) -> list[ValidationError]:
    return _check_oneof(value, "display", display_types)


# ── paint-order ────────────────────────────────────────────────────────────
paint_order_tokens = {"fill", "stroke", "markers"}
def check_paint_order(value) -> list[ValidationError]:
    if not isinstance(value, str):
        value = " ".join(value)
    s = value.strip().lower()
    if s in ("normal", "inherit"):
        return []
    tokens = s.split()
    if not all(t in paint_order_tokens for t in tokens) or len(tokens) != len(set(tokens)):
        return [
            ValidationError("paint-order", value,
                            "must be 'normal', or a unique permutation of 'fill', 'stroke', 'markers'")
        ]
    else:
        return []

# ── clip-path / mask / filter ──────────────────────────────────────────────

def _check_uri_or_none(attr: str, value: str) -> list[ValidationError]:
    s = value.strip().lower()
    if s in ("none", "inherit") or _RE_URL.match(value.strip()):
        return []
    else:
        return [
            ValidationError(attr, value, "must be 'none', 'inherit', or url(#id)")
        ]

def check_clip_path(value): return _check_uri_or_none("clip-path", value)
def check_mask(value): return _check_uri_or_none("mask", value)
def check_filter(value): return _check_uri_or_none("filter", value)


# ── transform ──────────────────────────────────────────────────────────────

_RE_TRANSFORM = re.compile(
    r"(?:matrix|translate|scale|rotate|skewX|skewY)"
    r"\(\s*[+-]?[\d.eE+\-]+(?:\s*[,\s]\s*[+-]?[\d.eE+\-]+)*\s*\)",
    re.I,
)

def check_transform(value) -> list[ValidationError]:
    if not isinstance(value, str):
        if isinstance(value, numbers.Number):
            value = f"scale({value:.3f})"
        elif isinstance(value[0], numbers.Number):
            value = "translate(" + ",".join(f"{v:.3f}" for v in value) + ")"
        else:
            value = "matrix(" + ",".join(f"{v:.3f}" for l in value for v in l) + ")"
    s = value.strip().lower()
    if s in ("none", "inherit"):
        return []
    remainder = _RE_TRANSFORM.sub("", value).strip().replace(",", "").strip()
    if remainder:
        return [
            ValidationError("transform", value,
                    "contains unrecognised transform functions or syntax")
        ]
    else:
        return []


# ── pointer-events ─────────────────────────────────────────────────────────

_POINTER_EVENTS = {
    "bounding-box", "visiblepainted", "visiblefill", "visiblestroke",
    "visible", "painted", "fill", "stroke", "all", "none", "inherit",
}
def check_pointer_events(value) -> list[ValidationError]:
    return _check_oneof(value, "pointer", _POINTER_EVENTS)


# ── cursor ─────────────────────────────────────────────────────────────────

_CURSOR_KEYWORDS = {
    "auto", "default", "none", "context-menu", "help", "pointer",
    "progress", "wait", "cell", "crosshair", "text", "vertical-text",
    "alias", "copy", "move", "no-drop", "not-allowed", "grab", "grabbing",
    "e-resize", "n-resize", "ne-resize", "nw-resize", "s-resize",
    "se-resize", "sw-resize", "w-resize", "ew-resize", "ns-resize",
    "nesw-resize", "nwse-resize", "col-resize", "row-resize",
    "all-scroll", "zoom-in", "zoom-out", "inherit",
}

def check_cursor(value) -> list[ValidationError]:
    parts = [p.strip() for p in value.split(",")]
    for part in parts:
        low = part.lower()
        if low in _CURSOR_KEYWORDS:
            continue
        if _RE_URL.match(part):
            continue
        return [ValidationError("cursor", value,
                                f"unknown cursor value '{part}'; must be a keyword or url(#id)")]
    else:
        return []


# ── vector-effect ──────────────────────────────────────────────────────────
vector_effect_types = {"none", "non-scaling-stroke", "non-scaling-size",
               "non-rotation", "fixed-position", "inherit"}
def check_vector_effect(value) -> list[ValidationError]:
    return _check_oneof(value, "vector-effect", vector_effect_types)


# ── font-family ────────────────────────────────────────────────────────────

def check_font_family(value) -> list[ValidationError]:
    return []

# ── font-size ──────────────────────────────────────────────────────────────

_FONT_SIZE_KEYWORDS = {
    "xx-small", "x-small", "small", "medium", "large",
    "x-large", "xx-large", "smaller", "larger", "inherit",
}
def check_font_size(value) -> list[ValidationError]:
    if not isinstance(value, str):
        value = f"{value:.0f}"
    s = value.strip().lower()
    if s in _FONT_SIZE_KEYWORDS or _is_length(s):
        return []
    else:
        return [ValidationError("font-size", value,
                                "must be a length, percentage, or keyword "
                                f"({sorted(_FONT_SIZE_KEYWORDS)})")]


# ── font-weight ────────────────────────────────────────────────────────────
font_weight_types = {"normal", "bold", "bolder", "lighter", "inherit"}
def check_font_weight(value) -> list[ValidationError]:
    if isinstance(value, str) and value.strip().lower() in font_weight_types:
        return []
    elif not isinstance(value, str):
        w = value
    else:
        try:
            w = int(value)
        except (TypeError, ValueError):
            return [ValidationError("font-weight", value,
                                    "must be 'normal', 'bold', 'bolder', 'lighter', 'inherit', "
                                    "or a multiple of 100 in [100, 1000]")]
    if 100 <= w and w <= 1000 and w % 100 == 0:
        return []
    else:
        return [ValidationError("font-weight", value,
                                "must be 'normal', 'bold', 'bolder', 'lighter', 'inherit', "
                                "or a multiple of 100 in [100, 1000]")]


# ── font-style ─────────────────────────────────────────────────────────────
font_style_types = {"normal", "italic", "oblique", "inherit"}
def check_font_style(value) -> list[ValidationError]:
    return _check_oneof(value, "font-style", font_style_types)


# ── font-variant ───────────────────────────────────────────────────────────
font_variant_types = {"normal", "small-caps", "inherit"}
def check_font_variant(value) -> list[ValidationError]:
    return _check_oneof(value, "font-variant", font_variant_types)


# ── text-anchor ────────────────────────────────────────────────────────────
text_anchor_types = {"start", "middle", "end", "inherit"}
def check_text_anchor(value) -> list[ValidationError]:
    return _check_oneof(value, "text-anchor", text_anchor_types)


# ── dominant-baseline ──────────────────────────────────────────────────────

_DOMINANT_BASELINE = {
    "auto", "text-bottom", "alphabetic", "ideographic", "middle",
    "central", "mathematical", "hanging", "text-top", "inherit",
}
def check_dominant_baseline(value) -> list[ValidationError]:
    return _check_oneof(value, "dominant-baseline", _DOMINANT_BASELINE)


# ── text-decoration ────────────────────────────────────────────────────────
text_decoration_types = {"underline", "overline", "line-through", "blink"}
def check_text_decoration(value) -> list[ValidationError]:
    if not isinstance(value, str):
        tokens = set(value)
    else:
        s = value.strip().lower()
        if s in {"none", "inherit"}:
            return []
        tokens = set(s.split())
    if not tokens.issubset(text_decoration_types):
        return [ValidationError("text-decoration", value,
                    f"must be 'none', 'inherit', or a combination of: {sorted(text_decoration_types)}")]
    else:
       return []


# ── letter-spacing / word-spacing ──────────────────────────────────────────

def _check_spacing(attr: str, value) -> list[ValidationError]:
    s = value.strip().lower()
    if s in {"normal", "inherit"} or _is_length(s):
        return []
    else:
        return [
            ValidationError(attr, value, "must be 'normal', 'inherit', or a length value")
        ]

def check_letter_spacing(value) -> list[ValidationError]: return _check_spacing("letter-spacing", value)
def check_word_spacing(value)   -> list[ValidationError]: return _check_spacing("word-spacing", value)


# ── writing-mode ───────────────────────────────────────────────────────────
writing_mode_types =  {
        "lr-tb", "rl-tb", "tb-rl", "lr", "rl", "tb",
        "horizontal-tb", "vertical-rl", "vertical-lr", "inherit",
    }
def check_writing_mode(value) -> list[ValidationError]:
    return _check_oneof(value, "writing-mode", writing_mode_types)

BASE_VALIDATORS = {
        "fill": check_fill,
        "fill-opacity": check_fill_opacity,
        "fill-rule": check_fill_rule,
        "stroke": check_stroke,
        "stroke-width": check_stroke_width,
        "stroke-opacity": check_stroke_opacity,
        "stroke-linecap": check_stroke_linecap,
        "stroke-linejoin": check_stroke_linejoin,
        "stroke-miterlimit": check_stroke_miterlimit,
        "stroke-dasharray": check_stroke_dasharray,
        "stroke-dashoffset": check_stroke_dashoffset,
        "opacity": check_opacity,
        "visibility": check_visibility,
        "display": check_display,
        "color": check_color,
        "paint-order": check_paint_order,
        "clip-path": check_clip_path,
        "mask": check_mask,
        "filter": check_filter,
        "transform": check_transform,
        "pointer-events": check_pointer_events,
        "cursor": check_cursor,
        "vector-effect": check_vector_effect,
        # COMMON_TEXT_PRESENTATION
        "font-family": check_font_family,
        "font-size": check_font_size,
        "font-weight": check_font_weight,
        "font-style": check_font_style,
        "font-variant": check_font_variant,
        "text-anchor": check_text_anchor,
        "dominant-baseline": check_dominant_baseline,
        "text-decoration": check_text_decoration,
        "letter-spacing": check_letter_spacing,
        "word-spacing": check_word_spacing,
        "writing-mode": check_writing_mode,
    }

def validate_props(props:dict, validators:dict, raise_on_invalid=True, undefined_is_missing=False):
    errors = []
    for k, v in props.items():
        if v is None: continue
        validator = validators.get(k)
        if validator is not None:
            errors.extend(validator(k, v))
        elif undefined_is_missing:
            errors.append(ValidationError("unknown property for validation", k))
    if len(errors) > 0 and raise_on_invalid:
        if len(errors) > 1:
            error = ValidationError(
                "\n".join(str(e) for e in errors)
            )
        else:
            error = errors[0]
        raise error
    return errors

class CSS:
    """
    Defines a holder for CSS properties
    """
    def __init__(self, *selectors, **props):
        self.selectors = selectors
        self.props = self.canonicalize_props(props)
    known_properties = set(o.value for o in Options)
    @classmethod
    def construct(cls,
                  *selectors,
                  aspect_ratio=None,
                  background=None,
                  background_attachment=None,
                  background_color=None,
                  background_image=None,
                  background_position=None,
                  background_repeat=None,
                  border=None,
                  border_bottom=None,
                  border_bottom_color=None,
                  border_bottom_style=None,
                  border_bottom_width=None,
                  border_color=None,
                  border_left=None,
                  border_left_color=None,
                  border_left_style=None,
                  border_left_width=None,
                  border_right=None,
                  border_right_color=None,
                  border_right_style=None,
                  border_right_width=None,
                  border_style=None,
                  border_top=None,
                  border_top_color=None,
                  border_top_style=None,
                  border_top_width=None,
                  border_width=None,
                  clear=None,
                  clip=None,
                  color=None,
                  cursor=None,
                  display=None,
                  filter=None,
                  float=None,
                  font=None,
                  font_family=None,
                  font_size=None,
                  font_variant=None,
                  font_weight=None,
                  height=None,
                  left=None,
                  letter_spacing=None,
                  line_height=None,
                  list_style=None,
                  list_style_image=None,
                  list_style_position=None,
                  list_style_type=None,
                  margin=None,
                  margin_bottom=None,
                  margin_left=None,
                  margin_right=None,
                  margin_top=None,
                  overflow=None,
                  padding=None,
                  padding_bottom=None,
                  padding_left=None,
                  padding_right=None,
                  padding_top=None,
                  page_break_after=None,
                  page_break_before=None,
                  position=None,
                  text_align=None,
                  text_decoration=None,
                  text_indent=None,
                  text_transform=None,
                  top=None,
                  vertical_align=None,
                  visibility=None,
                  width=None,
                  z_index=None,
                  **props
                  ):
        """
        Provides a convenience constructor for systems with autocompletions

        :param selectors:
        :type selectors:
        :param background:
        :type background:
        :param background_attachment:
        :type background_attachment:
        :param background_color:
        :type background_color:
        :param background_image:
        :type background_image:
        :param background_position:
        :type background_position:
        :param background_repeat:
        :type background_repeat:
        :param border:
        :type border:
        :param border_bottom:
        :type border_bottom:
        :param border_bottom_color:
        :type border_bottom_color:
        :param border_bottom_style:
        :type border_bottom_style:
        :param border_bottom_width:
        :type border_bottom_width:
        :param border_color:
        :type border_color:
        :param border_left:
        :type border_left:
        :param border_left_color:
        :type border_left_color:
        :param border_left_style:
        :type border_left_style:
        :param border_left_width:
        :type border_left_width:
        :param border_right:
        :type border_right:
        :param border_right_color:
        :type border_right_color:
        :param border_right_style:
        :type border_right_style:
        :param border_right_width:
        :type border_right_width:
        :param border_style:
        :type border_style:
        :param border_top:
        :type border_top:
        :param border_top_color:
        :type border_top_color:
        :param border_top_style:
        :type border_top_style:
        :param border_top_width:
        :type border_top_width:
        :param border_width:
        :type border_width:
        :param clear:
        :type clear:
        :param clip:
        :type clip:
        :param color:
        :type color:
        :param cursor:
        :type cursor:
        :param display:
        :type display:
        :param filter:
        :type filter:
        :param float:
        :type float:
        :param font:
        :type font:
        :param font_family:
        :type font_family:
        :param font_size:
        :type font_size:
        :param font_variant:
        :type font_variant:
        :param font_weight:
        :type font_weight:
        :param height:
        :type height:
        :param left:
        :type left:
        :param letter_spacing:
        :type letter_spacing:
        :param line_height:
        :type line_height:
        :param list_style:
        :type list_style:
        :param list_style_image:
        :type list_style_image:
        :param list_style_position:
        :type list_style_position:
        :param list_style_type:
        :type list_style_type:
        :param margin:
        :type margin:
        :param margin_bottom:
        :type margin_bottom:
        :param margin_left:
        :type margin_left:
        :param margin_right:
        :type margin_right:
        :param margin_top:
        :type margin_top:
        :param overflow:
        :type overflow:
        :param padding:
        :type padding:
        :param padding_bottom:
        :type padding_bottom:
        :param padding_left:
        :type padding_left:
        :param padding_right:
        :type padding_right:
        :param padding_top:
        :type padding_top:
        :param page_break_after:
        :type page_break_after:
        :param page_break_before:
        :type page_break_before:
        :param position:
        :type position:
        :param text_align:
        :type text_align:
        :param text_decoration:
        :type text_decoration:
        :param text_indent:
        :type text_indent:
        :param text_transform:
        :type text_transform:
        :param top:
        :type top:
        :param vertical_align:
        :type vertical_align:
        :param visibility:
        :type visibility:
        :param width:
        :type width:
        :param z_index:
        :type z_index:
        :param props:
        :type props:
        :return:
        :rtype:
        """
        common_props = dict(
            aspect_ratio=aspect_ratio,
            background=background,
            background_attachment=background_attachment,
            background_color=background_color,
            background_image=background_image,
            background_position=background_position,
            background_repeat=background_repeat,
            border=border,
            border_bottom=border_bottom,
            border_bottom_color=border_bottom_color,
            border_bottom_style=border_bottom_style,
            border_bottom_width=border_bottom_width,
            border_color=border_color,
            border_left=border_left,
            border_left_color=border_left_color,
            border_left_style=border_left_style,
            border_left_width=border_left_width,
            border_right=border_right,
            border_right_color=border_right_color,
            border_right_style=border_right_style,
            border_right_width=border_right_width,
            border_style=border_style,
            border_top=border_top,
            border_top_color=border_top_color,
            border_top_style=border_top_style,
            border_top_width=border_top_width,
            border_width=border_width,
            clear=clear,
            clip=clip,
            color=color,
            cursor=cursor,
            display=display,
            filter=filter,
            float=float,
            font=font,
            font_family=font_family,
            font_size=font_size,
            font_variant=font_variant,
            font_weight=font_weight,
            height=height,
            left=left,
            letter_spacing=letter_spacing,
            line_height=line_height,
            list_style=list_style,
            list_style_image=list_style_image,
            list_style_position=list_style_position,
            list_style_type=list_style_type,
            margin=margin,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            overflow=overflow,
            padding=padding,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            page_break_after=page_break_after,
            page_break_before=page_break_before,
            position=position,
            text_align=text_align,
            text_decoration=text_decoration,
            text_indent=text_indent,
            text_transform=text_transform,
            top=top,
            vertical_align=vertical_align,
            visibility=visibility,
            width=width,
            z_index=z_index
        )
        for k, v in common_props.items():
            if v is not None:
                props[k] = v
        return cls(*selectors, **props)
    @classmethod
    def canonicalize_props(cls, props):
        return {k.replace("_", "-"):v for k,v in props.items()}
    @classmethod
    def parse(cls, sty):
        header = sty.split("{", 1)[0]
        if len(header) == len(sty): # inline styles
            chunks = [x.strip() for x in sty.split(";")]
            splits = [x.split(":") for x in chunks if len(x) > 0]
            return cls(**{k.strip(): v.strip() for k, v in splits})
        else:
            splits = [x.split("{") for x in sty.split("}")]
            styles = []
            for key, vals in splits:
                key = [x.strip() for x in key.split(",")]
                chunks = [x.strip() for x in vals.split(";")]
                pairs = [x.split(":") for x in chunks if len(x) > 0]
                styles.append(
                    cls(*key, **{k.strip(): v.strip() for k, v in pairs})
                )
                return styles

    def tostring(self):
        if len(self.selectors) > 0:
            return "{sel} {{\n  {body}\n}}".format(
                sel=",".join(self.selectors),
                body="\n  ".join("{k}:{v};".format(k=k,v=v) for k,v in self.props.items())
            )
        else:
            return " ".join("{k}:{v};".format(k=k,v=v) for k,v in self.props.items())

    validators = BASE_VALIDATORS
    def validate(self, **kwargs):
        return validate_props(self.props, self.validators, **kwargs)

class HTMLManager:
    @classmethod
    def manage_class(kls, cls):
        if cls is None:
            cls = []
        elif hasattr(cls, 'tostring'):
            cls = cls.tostring
        if isinstance(cls, str):
            cls = cls.split()
        else:
            try:
                iter(cls)
            except TypeError:
                cls = str(cls).split()
        return list(cls)

    @classmethod
    def manage_styles(cls, styles):
        if hasattr(styles, 'items'):
            styles = CSS(**styles)
        elif isinstance(styles, str):
            styles = CSS.parse(styles)
        return styles

    keyword_replacements = {
        'cls': 'class',
        'in_': 'in',
        'use_for': 'for',
        'custom_type': 'is'
    }

    @classmethod
    def clean_key(cls, k):
        if k in cls.keyword_replacements:
            return cls.keyword_replacements[k]
        else:
            return k.replace("_", "-")

    @classmethod
    def sanitize_value(cls, val):
        if isinstance(val, np.integer):
            val = int(val)
        elif isinstance(val, np.floating):
            val = float(val)
        elif (not hasattr(val, 'to_tree')) and hasattr(val, '_repr_html_'):
            val = HTML.parse(val._repr_html_())
        elif hasattr(val, '_repr_png_'):
            val = HTML.image_from_string(val._repr_png_())
        return val

    @classmethod
    def manage_attrs(cls, attrs, sanitize=True):
        for k, v in cls.keyword_replacements.items():
            if k in attrs:
                attrs[v] = attrs[k]
                del attrs[k]
        attrs = {k.replace("_", "-"): v for k, v in attrs.items()}
        if sanitize:
            attrs = {k: cls.sanitize_value(v) for k, v in attrs.items()}
        return attrs

    @classmethod
    def extract_styles(cls, attrs, style_props=None, ignored_styles=None):
        if style_props is None:
            style_props = CSS.known_properties
        if ignored_styles is not None:
            style_props = style_props - set(ignored_styles)
        styles = {}
        for k, v in tuple(attrs.items()):
            if k in style_props:
                styles[k] = v
                del attrs[k]
        return styles, attrs

    validators = BASE_VALIDATORS
    @classmethod
    def validate_props(cls, props, **kwargs):
        return validate_props(props, cls.validators, **kwargs)

    class ElementModifier:
        def __init__(self, my_el, copy=False):
            self.el = my_el
            self.needs_copy = copy
            self._parents = None
            self._tree_cache = None
        def modify(self):
            if self.needs_copy:
                el = self.el.copy()
            else:
                el = self.el
            return el
        def tostring(self):
            return self.modify().tostring()
        def _repr_html_(self):
            return self.tostring()
        def copy(self):
            import copy
            new = copy.copy(self)
            new.el = new.el.copy()
        def add_class(self, *cls, copy=True):
            return self.el.context.ClassAdder(self, cls=cls, copy=copy)
        def remove_class(self, *cls, copy=True):
            return self.el.ClassRemover(self, cls=cls, copy=copy)
        def add_styles(self, copy=True, **sty):
            return self.el.StyleAdder(self, copy=copy, **sty)
    class ClassAdder(ElementModifier):
        cls = None
        def __init__(self, el, cls=None, copy=True):
            if cls is None:
                cls = self.cls
            if isinstance(cls, str):
                cls = cls.split()
            self.cls = cls
            super().__init__(el, copy=copy)
        def modify(self):
            if hasattr(self.el, 'modify'):
                el = self.el.modify()
            else:
                if self.needs_copy:
                    el = self.el.copy()
                else:
                    el = self.el
            if 'class' in el.attrs:
                if isinstance(el['class'], str):
                    el.make_class_list()
                class_list = list(el['class'])
                for cls in self.cls:
                    cls = str(cls)
                    if cls not in class_list:
                        class_list.append(cls)
                el['class'] = tuple(class_list)
            else:
                el['class'] = self.cls
            return el
        def __repr__(self):
            return "{}({}, {})".format(type(self).__name__, self.el, self.cls)
    class ClassRemover(ElementModifier):
        cls = None
        def __init__(self, el, cls=None, copy=True):
            if cls is None:
                cls = self.cls
            if isinstance(cls, str):
                cls = cls.split()
            self.cls = cls
            super().__init__(el, copy=copy)
        def modify(self):
            if hasattr(self.el, 'modify'):
                el = self.el.modify()
            else:
                if self.needs_copy:
                    el = self.el.copy()
                else:
                    el = self.el
            if 'class' in el.attrs:
                if isinstance(el['class'], str):
                    el.make_class_list()
                class_list = list(el['class'])
                for cls in self.cls:
                    cls = str(cls)
                    try:
                        class_list.remove(cls)
                    except ValueError:
                        pass
                el['class'] = tuple(class_list)
            else:
                el['class'] = self.cls
            return el
        def __repr__(self):
            return "{}({}, {})".format(type(self).__name__, self.el, self.cls)
    class StyleAdder(ElementModifier):
        def __init__(self, el, copy=True, **styles):
            self.styles = styles
            super().__init__(el, copy=copy)
        def modify(self):
            if hasattr(self.el, 'modify'):
                el = self.el.modify()
            else:
                if self.needs_copy:
                    el = self.el.copy()
                else:
                    el = self.el

            if 'style' in el.attrs:
                style = el.attrs['style']
                if isinstance(style, str):
                    style = CSS.parse(style)
                else:
                    style = style.copy()
                style.props = dict(style.props, **self.styles)
                el.attrs['style'] = style
            else:
                el.attrs['style'] = CSS(**self.styles)
            return el
        def __repr__(self):
            return "{}({}, {})".format(type(self).__name__, self.el, self.styles)

    class StyleRemover(ElementModifier):
        def __init__(self, el, *styles, copy=True):
            self.styles = styles
            super().__init__(el, copy=copy)
        def modify(self):
            if hasattr(self.el, 'modify'):
                el = self.el.modify()
            else:
                if self.needs_copy:
                    el = self.el.copy()
                else:
                    el = self.el

            if 'style' in el.attrs:
                style = el.attrs['style']
                if isinstance(style, str):
                    style = CSS.parse(style)
                else:
                    style = style.copy()
                for k in self.styles:
                    if k in style.props:
                        del style.props[k]
                el.attrs['style'] = style
            # else:
            #     el.attrs['style'] = CSS(**self.styles)
            return el
        def __repr__(self):
            return "{}({}, {})".format(type(self).__name__, self.el, self.styles)

    @classmethod
    def xml_to_json(cls, tree:ElementTree.Element, root=None):
        children = []
        if root is not None and tree.text in root._raw_html_cache:
            node = dict(tag='raw', body=root._raw_html_cache[tree.text])
        else:
            node = dict(tag=tree.tag, body=tree.text, tail=tree.tail, children=children, attrs=tree.attrib)
            for child in tree.getchildren():
                children.append(cls.xml_to_json(child))
        return node

class XMLBase:

    class ElementBase:
        ...

    @classmethod
    def find_globals(cls):
        for frame in inspect.stack(1):
            globs = frame.frame.f_globals
            if globs['__name__'] == '__main__':
                return globs
        else:
            return inspect.stack(1)[1].frame.f_globals

    @classmethod
    def expose(cls, globs=None):
        if globs is None:
            globs = cls.find_globals()
        for x in cls.get_class_map().values():
            globs[x.__name__] = x

    _cls_map = None
    @classmethod
    def get_class_map(cls):
        if cls._cls_map is None:
            cls._cls_map = {}
            for v in cls.__dict__.values():
                if isinstance(v, type) and hasattr(v, 'tag'):
                    cls._cls_map[v.tag] = v
        return cls._cls_map

    @classmethod
    @contextlib.contextmanager
    def class_map_context(cls, extra_classes):
        og_map = cls._cls_map
        try:
            base_map = cls.get_class_map().copy()
            base_map.update(extra_classes)
            cls._cls_map = base_map
            yield base_map
        finally:
            cls._cls_map = og_map

    base_element = None
    @classmethod
    def convert(cls, etree:ElementTree.Element, strip=True, converter=None, **extra_attrs):
        import copy

        if converter is None:
            converter = cls.convert
        children = []
        for x in etree:
            if x.tail is not None:
                x = copy.copy(x)
                t = x.tail
                x.tail = None
                children.append(converter(x, strip=strip))
                children.append(t)
            else:
                children.append(converter(x, strip=strip))
        text = etree.text
        if text is not None:
            if isinstance(text, str):
                text = [text]
        else:
            text = []
        tail = etree.tail
        if tail is not None:
            if isinstance(tail, str):
                tail = [tail]
        else:
            tail = []
        tag = etree.tag

        elems = (
                [t.strip("\n") if strip else t for t in text]
                + children
                + [t.strip("\n") if strip else t for t in tail]
        )
        if strip:
            elems = [e for e in elems if not isinstance(e, str) or len(e) > 0]

        map = cls.get_class_map()
        try:
            tag_class = map[tag]
        except KeyError:
            tag_class = lambda *es,**ats:cls.base_element(tag, *es, **ats)

        attrs = {} if etree.attrib is None else etree.attrib

        return tag_class(*elems, **dict(extra_attrs, **attrs))

    @classmethod
    def parse(cls, str, strict=True, strip=True, fallback=None, converter=None, namespace=None):
        if namespace is not None:
            ElementTree.register_namespace("", namespace)
        if strict:
            etree = ElementTree.fromstring(str)
        else:
            try:
                etree = ElementTree.fromstring(str)
            except ElementTree.ParseError as e:
                # print('no element found' in e.args[0])
                if 'junk after document element' in e.args[0]:
                    try:
                        return cls.parse('<div>\n\n'+str+'\n\n</div>', strict=True, strip=strip, fallback=fallback, converter=converter)
                    except ElementTree.ParseError:
                        if fallback is None:
                            fallback = HTML.Span
                        return fallback(str)
                if fallback is None:
                    fallback = HTML.Span
                return fallback(str)

        if converter is None:
            converter = cls.convert

        return converter(etree, strip=strip)
    # @classmethod
    # def split_roots(cls, xml_chunk:str, end_tag="/>", open_tag="<"):
    #     #TODO: pull this out of the RDKit parser code
    #     chunk = ""
    #     cur_l = -1
    #     end_l = len(xml_chunk)
    #     cur_counts = 0
    #     end_counts = 0
    #     while cur_l < end_l:
    #         tag_end = xml_chunk.find(end_tag, cur_l+1)
    #         if tag_end < 0:
    #             break
    #         end_counts += 1
    #         sub_chunk = xml_chunk[cur_l:tag_end]
    #         chunk += sub_chunk
    #         cur_l += len(sub_chunk)
    #         cur_counts += sub_chunk.count(open_tag)
    #         if cur_counts == end_counts:
    #             yield chunk
    #             cur_counts = 0
    #             end_counts = 0
    # @classmethod
    # def parse_iter(cls, xml_chunk:str, end_tag="/>", open_tag="<", **opts):
    #     for chunk in cls.split_roots(xml_chunk, end_tag=end_tag, open_tag=open_tag):
    #         yield cls.parse(chunk, **opts)


class HTML(XMLBase):
    """
    A namespace for holding various HTML attributes
    """

    class XMLElement(XMLBase.ElementBase):
        """
        Convenience API for ElementTree
        """

        ignored_styles = None
        unsynced_properties = None
        can_be_dynamic = True
        style_props = None
        context = HTMLManager

        @classmethod
        def get_class_map_updates(cls):
            return {}

        @classmethod
        def expanded_class_map(cls):
            return HTML.class_map_context(cls.get_class_map_updates())

        def __init__(self, tag, *elems, on_update=None, style=None, activator=None, can_be_dynamic=None, **attrs):
            self.tag = tag
            self._elems = [
                self.context.sanitize_value(v)
                for v in (
                    elems[0]
                        if len(elems) == 1 and isinstance(elems[0], (list, tuple)) else
                    elems
                )
            ]
            self._elem_view = None
            attrs = self.context.manage_attrs(attrs)
            extra_styles, attrs = self.context.extract_styles(attrs, style_props=self.style_props, ignored_styles=self.ignored_styles)
            if style is not None:
                style = self.context.manage_styles(style).props
                for k,v in extra_styles.items():
                    if k in style:
                        raise ValueError("got style {} specified in two different locations".format(k))
                    style[k] = v
            else:
                style = extra_styles
            if len(style) > 0:
                attrs['style'] = style
            self._attrs = attrs
            self._attr_view = None
            self._parents = weakref.WeakSet()
            self._tree_cache = None
            self._tree_root = None
            self._json_cache = None
            self._on_update_callbacks = self._canonicalize_callback_dict(on_update)
            self.activator = activator
            if can_be_dynamic is not None:
                self.can_be_dynamic = can_be_dynamic
        class _update_callbacks:
            """
            Simple set of callbacks both weakly keyed and default
            """
            def __init__(self, base_callbacks, weak_callbacks):
                self.base_callbacks = base_callbacks
                self.weak_callbacks = weak_callbacks
            @classmethod
            def from_raw(cls, data):
                if data is None:
                    base = {}
                    weak = None
                elif isinstance(data, dict):
                    if all(k is None or isinstance(k, str) for k in data):
                        base = data
                        weak = None
                    else:
                        base = data.get(None, {})
                        if len(data) > 1:
                            weak = weakref.WeakKeyDictionary(
                                {
                                    k: {None: x if isinstance(x, list) else [x]} if not isinstance(x, dict) else x
                                    for k, x in data.items()
                                    if k is not None
                                }
                            )
                        else:
                            weak = None
                elif isinstance(data, weakref.WeakKeyDictionary):
                    base = {}
                    weak = data
                else:
                    base = {None: [data]}
                    weak = None
                return cls(base, weak)
            def items(self):
                if self.weak_callbacks is not None:
                    for k,v in self.weak_callbacks.items():
                        yield k,v
                yield None,self.base_callbacks
            def __contains__(self, item):
                if item is None:
                    return True
                elif self.weak_callbacks is None:
                    return False
                else:
                    return item in self.weak_callbacks
            def __setitem__(self, key, value):
                if key is None:
                    self.base_callbacks = value
                else:
                    if self.weak_callbacks is None: self.weak_callbacks = weakref.WeakKeyDictionary()
                    self.weak_callbacks[key] = value
            def get(self, item, default):
                if item is None:
                    return self.base_callbacks
                else:
                    if self.weak_callbacks is None:
                        return default
                    else:
                        return self.weak_callbacks.get(item, default)
            def __getitem__(self, item):
                if item is None:
                    return self.base_callbacks
                else:
                    if self.weak_callbacks is None:
                        raise KeyError("key {} not found".format(item))
                    else:
                        return self.weak_callbacks[item]
        def _canonicalize_callback_dict(self, on_update):
            if not isinstance(on_update, self._update_callbacks):
                on_update = self._update_callbacks.from_raw(on_update)
            return on_update
        def on_update(self, key, new_value, old_value, subkey=None):
            for registrant, callback_dict in self._on_update_callbacks.items():
                for f in callback_dict.get(key, []) + callback_dict.get(None, []):
                    sentinel = f(self, key, new_value, old_value, registrant, subkey)
                    # TODO: handle breaks from the sentinel
        def update_callbacks(self, key=None, registrant=None):
            return self._on_update_callbacks.get(registrant, {}).get(key, [])
        def add_update_callback(self, callback, key=None, registrant=None):
            if registrant not in self._on_update_callbacks: self._on_update_callbacks[registrant] = {}
            if key not in self._on_update_callbacks[registrant]: self._on_update_callbacks[registrant][key] = []
            self._on_update_callbacks[registrant][key].append(callback)
        def remove_update_callback(self, callback, key=None, registrant=None):
            if registrant not in self._on_update_callbacks: self._on_update_callbacks[registrant] = {}
            if key not in self._on_update_callbacks[registrant]: self._on_update_callbacks[registrant][key] = []
            self._on_update_callbacks[registrant][key].remove(callback)

        def __call__(self, *elems, **kwargs):
            return type(self)(
                self.tag,
                self._elems + list(elems),
                activator=self.activator,
                on_update=self.on_update,
                **dict(self.attrs, **kwargs)
            )
        @property
        def attrs(self):
            if self._attr_view is None:
                self._attr_view = frozendict(self._attrs)
            return self._attr_view
        @attrs.setter
        def attrs(self, attrs):
            old_attrs = self.attrs
            self._attrs = self.context.manage_attrs(attrs)
            self._attr_view = None
            self.invalidate_cache()
            self.on_update('attributes', attrs, old_attrs)
        @property
        def elems(self):
            if self._elem_view is None:
                self._elem_view = tuple(
                        str(x)
                            if isinstance(x, (int, float, bool, numbers.Number)) else
                        x
                        for x in self._elems
                )
            return self._elem_view
        @elems.setter
        def elems(self, elems):
            self.set_elems(elems)
        def set_elems(self, elems):
            old_elems = self.elems
            self._elems = elems
            self._elem_view = None
            self.invalidate_cache()
            # self.on_update(self)
            self.on_update('elements', elems, old_elems)
        def activate(self):
            return self.activator(self)

        class StyleWrapper: # proxy for style
            def __init__(self, style_dict, obj):
                self.base_dict = style_dict
                self.base_obj = obj
            def __repr__(self):
                return "{}({})".format(type(self).__name__, self.base_dict)
            def __getitem__(self, item):
                return self.base_dict[item]
            def __setitem__(self, key, value):
                self.base_dict = dict(self.base_dict, **{key:value})
                self.base_obj.style = self.base_dict
            def __iter__(self):
                return iter(self.base_dict)
            def get(self, item, default=None):
                return self.base_dict.get(item, default)
            def items(self):
                return self.base_dict.items()
            def keys(self):
                return self.base_dict.keys()
            def values(self):
                return self.base_dict.values()

        @property
        def style(self):
            if 'style' in self._attrs:
                return self.StyleWrapper(self._attrs['style'], self)
        @style.setter
        def style(self, styles):
            self['style'] = styles

        @property
        def class_list(self):
            if 'class' in self._attrs:
                return self.context.manage_class(self._attrs['class'])
            else:
                return []

        def invalidate_cache(self):
            if self._tree_cache is not None:
                self._tree_cache = None
                self._tree_root = None
                for p in tuple(self._parents):
                    p.invalidate_cache()
                    self._parents.remove(p)
        def __getitem__(self, item):
            if isinstance(item, str):
                item = item.replace("_", "-")
                return self._attrs[item]
            else:
                return self._elems[item]
        def __setitem__(self, item, value):
            if isinstance(item, str):
                item = item.replace("_", "-")
                old_value = self._attrs.get(item, None)
                self._attrs[item] = self.context.sanitize_value(value)
                self._attr_view = None
            else:
                old_value = self._elems[item]
                self._elems[item] = value
                self._elem_view = None
            self.invalidate_cache()
            self.on_update('attribute', value, old_value, subkey=item)
        def insert(self, where, child):
            if where is None:
                where = len(self._elems)
            self._elems.insert(where, child)
            self._elem_view = None
            self.invalidate_cache()
            self.on_update('element', child, None, subkey=where)
        def append(self, child):
            self.insert(None, child)
        def __delitem__(self, item):
            if isinstance(item, str):
                item = item.replace("_", "-")
                old_value = self._attrs.get(item, None)
                try:
                    del self._attrs[item]
                except KeyError:
                    pass
                else:
                    self._attr_view = None
            else:
                old_value = self._elems[item]
                del self._elems[item]
                self._elem_view = None
            self.invalidate_cache()
            self.on_update('attribute' if isinstance(item, str) else 'element', None, old_value, subkey=item)

        atomic_types = (int, bool, float)
        @classmethod
        def construct_etree_element(cls, elem, root, top, parent=None, attr_converter=None):
            if isinstance(elem, cls.atomic_types):
                elem = str(elem)
            elif isinstance(elem, HTML.RawHTML):
                key = f"$~raw:{elem.id}~$"
                top._raw_html_cache[key] = elem
                elem = key
            if hasattr(elem, 'to_tree'):
                elem.to_tree(root=root, parent=parent, top=top, attr_converter=attr_converter)
            elif hasattr(elem, 'modify'):
                elem.modify().to_tree(root=root, parent=parent, attr_converter=attr_converter)
            elif isinstance(elem, ElementTree.Element):
                root.append(elem)
            elif isinstance(elem, (str, int, float, CSS)):
                elem = str(elem)
                kids = list(root)
                if len(kids) > 0:
                    if kids[-1].tail is None:
                        kids[-1].tail = elem
                    else:
                        kids[-1].tail += "\n" + elem
                else:
                    root.text = elem
            elif hasattr(elem, 'to_widget'):
                elem = elem.to_widget()
                if not isinstance(elem, HTML.XMLElement):
                    raise ValueError(
                        f"can't convert {elem} to pure HTML. "
                        "It looks like a Jupyter widget so look for the appropriate `JHTML` subclass."
                    )
                else:
                    cls.construct_etree_element(elem, root, top, parent=parent, attr_converter=attr_converter)
            else:
                raise ValueError(f"don't know what to do with {elem} in converting {parent}")

        attr_converter = None
        @classmethod
        def construct_etree_attrs(cls, attrs, attr_converter=None):
            _copied = False
            if 'style' in attrs:
                styles = attrs['style']
                if hasattr(styles, 'items'):
                    styles = CSS(**styles)
                if hasattr(styles, 'tostring'):
                    if not _copied:
                        attrs = attrs.copy()
                        _copied = True
                    attrs['style'] = styles.tostring()
            if 'class' in attrs:
                if not isinstance(attrs['class'], str):
                    if not _copied:
                        attrs = attrs.copy()
                        _copied = True
                    try:
                        iter(attrs['class'])
                    except TypeError:
                        attrs['class'] = str(attrs['class'])
                    else:
                        attrs['class'] = " ".join(str(c) for c in attrs['class'])
                    if len(attrs['class']) == 0:
                        del attrs['class']
            if attr_converter is None:
                attr_converter = cls.attr_converter
            if attr_converter is not None:
                attrs = attr_converter(attrs)
            return attrs
        @property
        def tree(self):
            return self.to_tree()
        class TreeRoot(ElementTree.Element):
            def __init__(self):
                super().__init__('root')
                self._raw_html_cache = {}
            def __repr__(self):
                return f'{type(self).__name__}()'
        def to_tree(self, root=None, top=None, parent=None, attr_converter=None):
            if parent is not None:
                self._parents.add(parent)
            if attr_converter is None:
                attr_converter = self.__dict__.get('attr_converter') # don't want to resolve to class-level converter
            if self._tree_cache is None:
                if top is None:
                    top = self._tree_root
                if top is None and parent is not None:
                    top = parent._tree_root
                if top is None:
                    top = self.TreeRoot()
                if root is None:
                    root = top
                attrs = self.construct_etree_attrs(self.attrs, attr_converter=attr_converter)
                my_el = ElementTree.SubElement(root, self.tag, attrs)
                if all(isinstance(e, str) for e in self.elems):
                    my_el.text = "\n".join(self.elems)
                else:
                    for elem in self.elems:
                        self.construct_etree_element(elem, my_el, top, parent=self, attr_converter=attr_converter)
                self._tree_root = top
                self._tree_cache = my_el
            elif root is not None:
                if self._tree_cache not in root:
                    root.append(self._tree_cache)
                if self._tree_root is None and top is not None:
                    self._tree_root = top
            return self._tree_cache, self._tree_root
        def modify(self, elems=None, **attrs):
            attrs = self.context.manage_attrs(attrs)
            extra_styles, attrs = self.context.extract_styles(attrs, style_props=self.style_props, ignored_styles=self.ignored_styles)
            base_attrs = dict(self.attrs, **attrs)
            return type(self)(
                self.elems if elems is None else elems,
                style=dict(base_attrs.pop('style', {}), **extra_styles),
                **base_attrs
            )
        def clean_props(self, attr_converter=None):
            if attr_converter is None:
                attr_converter = self.attr_converter
            return self.modify(
                elems=[
                    e.clean_props(attr_converter=attr_converter)
                        if hasattr(e, 'clean_props') else e
                    for e in self.elems
                ],
                **(attr_converter(self.attrs) if attr_converter is not None else self.attrs)
            )
        def to_json(self, root=None, parent=None, attr_converter=None):
            tree, root = self.to_tree(root=root, parent=parent, attr_converter=attr_converter)
            return self.context.xml_to_json(tree, root)
        @classmethod
        def _prettyify(cls, current, *, indent, riffle, parent=None, index=-1, depth=0):
            # lightly adapted from https://stackoverflow.com/a/65808327/5720002
            for i, node in enumerate(current):
                cls._prettyify(node, indent=indent, riffle=riffle, parent=current, index=i, depth=depth + 1)
            if current.text is not None and len(current.text.strip()) > 0:
                current.text = (
                        riffle + textwrap.indent(current.text, prefix=indent * (depth+1))
                        + riffle + (indent * depth)
                )
            if parent is not None:
                if index == 0:
                    txt = parent.text
                    if txt is None:
                        txt = ""
                    parent.text = txt + riffle + (indent * depth)
                else:
                    txt = parent[index - 1].tail
                    if txt is not None:
                        txt = riffle + (indent * (depth)) + txt
                    else:
                        txt = ""
                    parent[index - 1].tail = txt + riffle + (indent * depth)
                if index == len(parent) - 1:
                    txt = current.tail
                    if txt is not None:
                        txt = riffle + (indent * (depth)) + txt
                    else:
                        txt = ""
                    current.tail = txt + riffle + (indent * (depth - 1))

        default_indent = "  "
        default_newline = "\n"
        def tostring(self, attr_converter=None, indent=None, method='html', riffle=True, prettify=False,
                     write_string=None,
                     **base_etree_opts):
            tree, root = self.to_tree(attr_converter=attr_converter)
            if prettify:
                if indent is not False:
                    if indent is None or indent is True:
                        indent = self.default_indent
                else:
                    indent = ""
                if riffle is not False:
                    if riffle is None or riffle is True:
                        riffle = self.default_newline
                else:
                    riffle = ""
                tree = copy.deepcopy(tree)
                self._prettyify(tree, indent=indent, riffle=riffle)
                if write_string is None:
                    write_string = ElementTree.tostring
                base_str = write_string(tree, **base_etree_opts)
            else:
                if indent is not None and indent is not False:
                    if indent is True:
                        indent = self.default_indent
                    tree = copy.deepcopy(tree)
                    ElementTree.indent(tree, space=indent)

                if riffle is not None and indent is not False:
                    if riffle is True:
                        riffle = self.default_newline
                    strs = [
                        s.decode() for s in ElementTree.tostringlist(
                            tree,
                            method=method,
                            **base_etree_opts
                        )
                    ]
                    base_str = riffle.join(strs)
                    if write_string is not None:
                        base_str = write_string(base_str)
                else:
                    if write_string is None:
                        write_string = ElementTree.tostring
                    base_str = write_string(tree)

            if hasattr(base_str, 'decode'):
                base_str = base_str.decode()
            try:
                replacements = root._raw_html_cache
            except AttributeError:
                replacements = {}
            if len(replacements) > 0:
                for key,elem in replacements.items():
                    base_str = base_str.replace(key, elem.tostring())
            return base_str

        def sanitize_key(self, key):
            key = key.replace("-", "_")
            for safe, danger in self.context.keyword_replacements.items():
                key = key.replace(danger, safe)
            return key
        def format(self, padding="", prefix="", linewidth=100):
            template_header = "{name}("
            template_footer = ")"
            template_pieces = []
            args_joiner = ", "
            full_joiner = ""
            elem_padding = ""
            def use_lines():
                nonlocal full_joiner, args_joiner, elem_padding, template_footer
                full_joiner = "\n"
                args_joiner = ",\n"
                elem_padding = padding + "  "
                template_footer = "{padding}  )"

            name = type(self).__name__
            tag = repr(self.tag) if len(template_pieces) > 1 else repr(self.tag)

            inner_comps = [
                (x.format(padding=padding+"  ", prefix=prefix, linewidth=linewidth) if isinstance(x, HTML.XMLElement) else repr(x))
                for x in self.elems if not (isinstance(x, str) and x.strip() == "")
            ]

            if not isinstance(self, HTML.TagElement):
                template_pieces.append("{tag}")
            if len(self.attrs) > 0:
                attr_pieces = ["{}={!r}".format(self.sanitize_key(k), v) for k,v in self.attrs.items()]
                if len(inner_comps) > 0:
                    template_pieces.append("{inner}")
                    template_pieces.append("{attrs}")
                else:
                    template_pieces.append("{attrs}")
            else:
                attr_pieces = []
                template_pieces.append("{inner}")
                # if "\n" not in inner:
                #     inner = inner.strip()
                #     full_joiner = ""
                #     template_footer = ")"

            template = full_joiner.join([
                template_header,
                args_joiner.join(template_pieces),
                template_footer
            ])
            out = template.format(
                padding=padding,
                tag=padding + "  " + tag,
                name=prefix+name,
                inner=args_joiner.join(elem_padding+x for x in inner_comps),
                attrs=args_joiner.join(elem_padding+x for x in attr_pieces),
            )
            if len(out) > linewidth + len(prefix):
                use_lines()
                template = full_joiner.join([
                    template_header,
                    args_joiner.join(template_pieces),
                    template_footer
                ])
                out = template.format(
                    padding=padding,
                    tag=padding + "  " + tag,
                    name=prefix + name,
                    inner=args_joiner.join(elem_padding + x for x in inner_comps),
                    attrs=args_joiner.join(elem_padding + x for x in attr_pieces),
                )
            return out
        def dump(self, prefix="", linewidth=80):
            print(self.format(prefix=prefix, linewidth=linewidth))
        def write(self, file, **opts):
            ## Stream version is faster but more fragile
            # def write_str(tree, **base_opts):
            #     if isinstance(tree, str):
            #         if hasattr(file, 'write'):
            #             file.write(tree)
            #         else:
            #             with open(file, 'w+') as f:
            #                 f.write(tree)
            #     elif hasattr(tree, 'write'):
            #         tree.write(file, **base_opts)
            #     else:
            #         write_str(ElementTree.tostring(tree), **base_opts)
            base_str = self.tostring(**opts)
            if hasattr(file, 'write'):
                file.write(base_str)
            else:
                with open(file, 'w+') as dump:
                    dump.write(base_str)

        MAX_REPR_LENGTH = 1000
        def __repr__(self):
            base_repr = "{}({}, {})".format(type(self).__name__, self.elems, self.attrs)
            if len(base_repr) > self.MAX_REPR_LENGTH + 3:
                split_len = self.MAX_REPR_LENGTH // 2
                base_repr = base_repr[:split_len] + "..." + base_repr[-split_len:]
            return base_repr
        def _repr_html_(self):
            return self.tostring()
        def _ipython_display_(self):
            self.display()
        def get_display_element(self):
            return HTML.Div(self, cls='jhtml')
        def get_mime_bundle(self):
            # from .WidgetTools import JupyterAPIs
            # display = JupyterAPIs.get_display_api()
            # from IPython.display import HTML as dispHTML
            wrapper = self.get_display_element()
            data = {
                'text/html': wrapper.tostring()
            }
            return data

        @classmethod
        def _cross_plat_open(cls, file, delay=5):
            import os, sys, subprocess, time
            if sys.platform.startswith('darwin'):  # macOS
                subprocess.run(['open', file])
            elif sys.platform.startswith('win'):  # Windows
                os.startfile(file, 'open')
            elif sys.platform.startswith('linux'):  # Linux
                subprocess.run(['xdg-open', file])
            else:
                raise NotImplementedError(f"unsure how to open file on {sys.platform}")
            time.sleep(delay)

        @classmethod
        def display_in_browser_from_wrapper(cls, wrapper):
            import tempfile as tf

            with tf.NamedTemporaryFile(suffix='.html', prefix=type(wrapper).__name__+"-", mode='w+',
                                       # delete=False
                                       ) as tmp_html:
                tmp_html.write(wrapper.tostring())
                tmp_html.seek(0)
                tmp_html.flush()
                cls._cross_plat_open(tmp_html.name)
        def display_in_browser(self):
            if self.tag.lower() != 'html':
                if self.tag.lower() != 'body':
                    wrapper = HTML.Body(self.get_display_element())
                else:
                    wrapper = self
                wrapper = HTML.Html(wrapper)
            else:
                wrapper = self
            return self.display_in_browser_from_wrapper(wrapper)

        @classmethod
        def display_ipython_from_wrapper(self, wrapper):
            from .WidgetTools import JupyterAPIs

            display = JupyterAPIs.get_display_api()
            return display.display(display.HTML(wrapper.tostring()))
        def display_ipython(self):
            return self.display_ipython_from_wrapper(self.get_display_element())

        def display(self):
            from .WidgetTools import JupyterAPIs

            use_ipython = JupyterAPIs.in_jupyter_environment()
            if use_ipython:
                self.display_ipython()
            else:
                self.display_in_browser()
        @mixedmethod
        def _ipython_pinfo_(self):
            from ...Docs import jdoc
            return jdoc(self)

        def validate_props(self, **kwargs):
            return self.context.validate_props(self._attrs, **kwargs)

        def make_class_list(self):
            self._attrs['class'] = self._attrs['class'].split()
        def add_class(self, *cls, copy=True):
            return self.context.ClassAdder(self, cls, copy=copy).modify()
        def remove_class(self, *cls, copy=True):
            return self.context.ClassRemover(self, cls, copy=copy).modify()
        def add_styles(self, copy=True, **sty):
            return self.context.StyleAdder(self, copy=copy, **sty).modify()
        def remove_styles(self, copy=True, **sty):
            return self.context.StyleRemover(self, copy=copy, **sty).modify()
        # def remove_styles(self, copy=True, **sty):
        #     return HTML.StyleAdder(self, copy=copy, **sty).modify()

        def _find_child_node(self, etree):
            from collections import deque
            # BFS to try to find the element that matches
            remaining = deque()
            remaining.append(self)
            while remaining:
                elem = remaining.popleft()
                if isinstance(elem, self.context.ElementModifier):
                    elem = elem.modify()
                if isinstance(elem, HTML.XMLElement):
                    if etree == elem.tree:
                        return elem
                    else:
                        for e in elem.elems:
                            remaining.append(e)

        def find(self, path, find_element=True):
            base = self.tree.find(path)
            if find_element and base is not None:
                new = self._find_child_node(base)
                if new is not None:
                    base = new
            return base
        def findall(self, path, find_element=True):
            bases = self.tree.findall(path)
            if find_element:
                new = []
                for b in bases:
                    newb = self._find_child_node(b)
                    if newb is not None:
                        new.append(newb)
                    else:
                        new.append(b)
                bases = new
            return bases
        def iterfind(self, path, find_element=True):
            bases = self.tree.iterfind(path)
            for b in bases:
                if find_element:
                    newb = self._find_child_node(b)
                    if newb is not None:
                        yield newb
                    else:
                        yield b
                else:
                    yield b
        def _build_single_selector(self, root='.//', node_type='*', parents=None, **attrs):
            return "{root}{node_type}{atts}{parents}".format(
                root=root,
                node_type=node_type,
                atts='[' +
                     ' and '.join(
                         "@{k}='{v}'".format(k='class' if k == 'cls' else k, v=v)
                         for k,v in attrs.items()
                     ) + ']' if len(attrs) > 0 else '',
                parents="" if parents is None else ('.' + '.' * parents)
            )

        def _build_xpath_selector(self,  root='.//', node_type='*', parents=None, **attrs):
            attrs.update({
                'root':root,
                'node_type':node_type,
                'parents':parents
            })
            direct_prod_attrs = [
                [v]
                    if v is None else
                [str(vv) for vv in v]
                    if not isinstance(v, (str, int, float, bool)) else
                [str(v)]
                for v in attrs.values()
            ]
            selectors = [
                self._build_single_selector(
                    **dict(zip(attrs.keys(), p))
                )
                for p in itertools.product(*direct_prod_attrs)
            ]
            return " | ".join(selectors)

        def find_by_id(self, id, mode='first', parent=None, find_element=True):
            fn = {
                'first':self.find,
                'all':self.findall,
                'iter':self.iterfind
            }[mode]
            sel = ".//*[@id='{id}']{parents}".format(id=id, parents="" if parent is None else ('.'+'.'*parent))
            return fn(sel, find_element=find_element)
        def find_by_attributes(self,
                               *,
                               root='.//', node_type='*', parents=None,
                               mode='first',
                               find_element=True,
                               **attrs
        ):
            fn = {
                'first': self.find,
                'all': self.findall,
                'iter': self.iterfind
            }[mode]
            sel = self._build_xpath_selector(root=root, node_type=node_type, parents=parents, **attrs)
            return fn(sel, find_element=find_element)
        def build_selector(self, *dicts, **attrs):
            if len(dicts) == 0:
                return self._build_xpath_selector(**attrs)
            elif len(attrs) == 0:
                cur = self._build_xpath_selector(**dicts[0])
                for d in dicts[1:]:
                    if 'root' in d:
                        raise ValueError("root is inherited from previous selector")
                    d = dict(d, root=cur+'/')
                    cur = self._build_xpath_selector(**d)
                return cur
            else:
                raise ValueError("unsure what to do when given both dicts and kwargs?")


        def copy(self):
            import copy
            base = copy.copy(self)
            base.attrs = base.attrs.copy()
            base._tree_cache = None
            base._parents = weakref.WeakSet()
            return base

    base_element = XMLElement

    class RawHTML(XMLElement):
        """
        Not a properly constructed subclass, but inserted as part of the
        type hierarchy for explicit isintance check purposes, should have a
        trait-style base class but too much work now
        """
        def __init__(self, text, id=None):
            if id is None:
                id = str(uuid.uuid4())
            self.id = id
            self.text = text
        def tostring(self, **opts):
            return self.text
        def display(self):
            from .WidgetTools import JupyterAPIs

            use_ipython = JupyterAPIs.in_jupyter_environment()
            if use_ipython:
                self.display_ipython()
            else:
                self.display_in_browser()
        def display_in_browser(self):
            return self.display_in_browser_from_wrapper(self)
        def display_ipython(self):
            return self.display_ipython_from_wrapper(self)
        def _repr_html_(self):
            return self.tostring()
        def _ipython_display_(self):
            self.display()
        def get_display_element(self):
            return HTML.Div(self, cls='jhtml')
        def dump(self, prefix="", linewidth=80):
            print(self.tostring())
        def write(self, file, **opts):
            base_str = self.tostring(**opts)
            if hasattr(file, 'write'):
                file.write(base_str)
            else:
                with open(file, 'w+') as dump:
                    dump.write(base_str)

    class Comment(XMLElement):
        def __init__(self, *elems, **attrs):
            super().__init__(ElementTree.Comment, *elems, **attrs)

    class TagElement(XMLElement):
        tag = None
        def __init__(self, *elems, **attrs):
            super().__init__(self.tag, *elems, **attrs)
        def __call__(self, *elems, **kwargs):
            return type(self)(
                self._elems + list(elems),
                activator=self.activator,
                on_update=self.on_update,
                **dict(self.attrs, **kwargs)
            )
    class Nav(TagElement): tag='nav'
    class Anchor(TagElement): tag='a'
    class Text(TagElement): tag='p'
    class Div(TagElement): tag='div'
    class Heading(TagElement): tag='h1'
    class SubHeading(TagElement): tag='h2'
    class SubsubHeading(TagElement): tag='h3'
    class SubsubsubHeading(TagElement): tag='h4'
    class SubHeading5(TagElement): tag='h5'
    class SubHeading6(TagElement): tag='h6'
    class Small(TagElement): tag='small'
    class Bold(TagElement): tag='b'
    class Italic(TagElement): tag='i'
    class Image(TagElement): tag='img'
    @classmethod
    def image_from_string(cls, image_string: bytes | str, format='image/png', **styles):
        import base64
        if isinstance(image_string, bytes):
            image_string = base64.b64encode(image_string).decode()
        return cls.Image(
            src=f"data:{format};base64,{image_string}",
            **styles
        )
    class ListItem(TagElement): tag='li'
    class BaseList(TagElement):
        def __init__(self, *elems, item_attributes=None, **attrs):
            if item_attributes is None:
                item_attributes = {}
            # elems = [HTML.ListItem(x, **item_attributes) if not isinstance(x, HTML.ListItem) else x for x in elems]
            super().__init__(*elems, **attrs)
    class List(BaseList): tag='ul'
    class NumberedList(BaseList): tag='ol'
    class Pre(TagElement): tag='pre'
    class Style(TagElement): tag='style'
    class Script(TagElement): tag='script'
    class Span(TagElement): tag='span'
    class Button(TagElement): tag='button'
    class TableRow(TagElement): tag='tr'
    class TableHeading(TagElement): tag='th'
    class TableHeader(TagElement): tag='thead'
    class TableFooter(TagElement): tag='tfoot'
    class TableBody(TagElement): tag='tbody'
    class TableItem(TagElement): tag='td'
    class Table(TagElement):
        tag = 'table'
        def __init__(self, *rows, headers=None, **attrs):
            if len(rows) == 1 and isinstance(rows[0], (list, tuple)):
                rows = rows[0]
            rows = [
                HTML.TableRow(
                    [HTML.TableItem(y) if not isinstance(y, HTML.TableItem) else y for y in x]
                ) if not isinstance(x, HTML.TableRow) else x for x in rows
            ]
            if headers is not None:
                rows = [
                    HTML.TableRow([HTML.TableHeading(x) if not isinstance(x, HTML.TableHeading) else x for x in headers])
                ] + rows
            super().__init__(rows, **attrs)

    class Canvas(TagElement): tag='canvas'

    A = Anchor
    class Abbr(TagElement): tag= "abbr"
    class Address(TagElement): tag= "address"
    class Area(TagElement): tag= "area"
    class Article(TagElement): tag= "article"
    class Aside(TagElement): tag= "aside"
    class Audio(TagElement): tag= "audio"
    class B(TagElement): tag= "b"
    class Base(TagElement): tag= "base"
    class Bdi(TagElement): tag= "bdi"
    class Bdo(TagElement): tag= "bdo"
    class Blockquote(TagElement): tag= "blockquote"
    class Body(TagElement): tag= "body"
    class Br(TagElement): tag= "br"
    class Caption(TagElement): tag= "caption"
    class Cite(TagElement): tag= "cite"
    class Code(TagElement): tag= "code"
    class Col(TagElement): tag= "col"
    class Colgroup(TagElement): tag= "colgroup"
    class Data(TagElement): tag= "data"
    class Datalist(TagElement): tag= "datalist"
    class Dd(TagElement): tag= "dd"
    class Del(TagElement): tag= "del"
    class Details(TagElement): tag= "details"
    class Dfn(TagElement): tag= "dfn"
    class Dialog(TagElement): tag= "dialog"
    class Dl(TagElement): tag= "dl"
    class Dt(TagElement): tag= "dt"
    class Em(TagElement): tag= "em"
    class Embed(TagElement): tag= "embed"
    class Fieldset(TagElement): tag= "fieldset"
    class Figcaption(TagElement): tag= "figcaption"
    class Figure(TagElement): tag= "figure"
    class Footer(TagElement): tag= "footer"
    class Form(TagElement): tag= "form"
    class Head(TagElement): tag= "head"
    class Header(TagElement): tag= "header"
    class Hr(TagElement): tag= "hr"
    class Html(TagElement): tag = "Html"
    i = Italic
    class Iframe(TagElement): tag= "iframe"
    Img = Image
    class Inline(TagElement): tag= "inline"
    class Input(TagElement): tag= "input"
    class Ins(TagElement): tag= "ins"
    class Kbd(TagElement): tag= "kbd"
    class Label(TagElement): tag= "label"
    class Legend(TagElement): tag= "legend"
    Li = ListItem
    class Link(TagElement): tag= "link"
    class Main(TagElement): tag= "main"
    class Map(TagElement): tag= "map"
    class Mark(TagElement): tag= "mark"
    class Meta(TagElement): tag= "meta"
    class Meter(TagElement): tag= "meter"
    class Noscript(TagElement): tag= "noscript"
    class Object(TagElement): tag= "object"
    Ol = NumberedList
    P = Text
    class Optgroup(TagElement): tag= "optgroup"
    class Option(TagElement): tag= "option"
    class Output(TagElement): tag= "output"
    class Param(TagElement): tag= "param"
    class Picture(TagElement): tag= "picture"
    class Progress(TagElement): tag= "progress"
    class Q(TagElement): tag= "q"
    class Rp(TagElement): tag= "rp"
    class Rt(TagElement): tag= "rt"
    class Ruby(TagElement): tag= "ruby"
    class S(TagElement): tag= "s"
    class Samp(TagElement): tag= "samp"
    class Section(TagElement): tag= "section"
    class Select(TagElement): tag= "select"
    class Source(TagElement): tag= "source"
    class Strong(TagElement): tag= "strong"
    class Sub(TagElement): tag= "sub"
    class Summary(TagElement): tag= "summary"
    class Sup(TagElement): tag= "sup"
    class Svg(TagElement): tag= "svg"
    Tbody = TableBody
    Td = TableItem
    class Template(TagElement): tag= "template"
    class Textarea(TagElement): tag= "textarea"
    Tfoot = TableFooter
    Th = TableHeading
    Thead = TableHeader
    class Time(TagElement): tag= "time"
    class Title(TagElement): tag= "title"
    Tr = TableRow
    class Track(TagElement): tag= "track"
    class U(TagElement): tag= "u"
    Ul = List
    class Var(TagElement): tag= "var"
    class Video(TagElement): tag= "video"
    class Wbr(TagElement): tag= "wbr"

    # @classmethod
    # def extract_body(cls, etree, strip=True):
    #     text = etree.text
    #     if text is not None:
    #         if isinstance(text, str):
    #             text = [text]
    #     else:
    #         text = []
    #     tail = etree.tail
    #     if tail is not None:
    #         if isinstance(tail, str):
    #             tail = [tail]
    #     else:
    #         tail = []
    #     tag = etree.tag
    #
    #     elems = (
    #             [t.strip() if strip else t for t in text]
    #             + children
    #             + [t.strip() if strip else t for t in tail]
    #     )
    #     if strip:
    #         elems = [e for e in elems if not isinstance(e, str) or len(e) > 0]

class ContentXML(XMLBase):

    class Element(HTML.XMLElement):
        ignored_styles = CSS.known_properties
        def get_display_element(self):
            return HTML.Pre(self.tostring()).get_display_element()
        def tostring(self, method='xml', prettify=True, **opts):
            return super().tostring(method=method, prettify=prettify, **opts)

    base_element = Element
    class TagElement(Element):
        tag = None

        def __init__(self, *elems, **attrs):
            super().__init__(self.tag, *elems, **attrs)

        def __call__(self, *elems, **kwargs):
            return type(self)(
                self._elems + list(elems),
                activator=self.activator,
                on_update=self.on_update,
                **dict(self.attrs, **kwargs)
            )

    class DeclarativeElement(TagElement):
        def __init__(self, *elems, **attrs):
            self.tag = type(self).__name__
            super().__init__(*elems, **attrs)

    class Comment(HTML.Comment): ...

    class PrefixedElement(Element):
        prefix = None
        def __init__(self, base_tag, *elems, **attrs):
            self.base_tag = base_tag
            super().__init__(self.prefix + base_tag, *elems, **attrs)
        def __call__(self, *elems, **kwargs):
            return type(self)(
                self.base_tag,
                self._elems + list(elems),
                activator=self.activator,
                on_update=self.on_update,
                **dict(self.attrs, **kwargs)
            )


COMMON_PRESENTATION = {
    "fill": "black",  # interior fill colour
    "fill-opacity": 1.0,  # 0–1
    "fill-rule": "nonzero",  # "nonzero" | "evenodd"
    "stroke": "none",  # outline colour
    "stroke-width": 1,  # in user units
    "stroke-opacity": 1.0,
    "stroke-linecap": "butt",  # "butt" | "round" | "square"
    "stroke-linejoin": "miter",  # "miter" | "round" | "bevel"
    "stroke-miterlimit": 4,
    "stroke-dasharray": "none",  # e.g. "5 3" for dashes
    "stroke-dashoffset": 0,
    "opacity": 1.0,  # applies to fill + stroke together
    "visibility": "visible",  # "visible" | "hidden" | "collapse"
    "display": "inline",
    "color": "inherit",
    "paint-order": "fill",  # "fill" | "stroke" | "markers"
    "clip-path": "none",  # url(#id)
    "mask": "none",  # url(#id)
    "filter": "none",  # url(#id)
    "transform": None,  # e.g. "rotate(45) translate(10,0)"
    "pointer-events": "visiblePainted",
    "cursor": "auto",
    "vector-effect": "none",  # "non-scaling-stroke" is very useful
}

COMMON_TEXT_PRESENTATION = {
    "font-family": "sans-serif",
    "font-size": "16px",
    "font-weight": "normal",  # "normal" | "bold" | 100–900
    "font-style": "normal",  # "normal" | "italic" | "oblique"
    "font-variant": "normal",
    "text-anchor": "start",  # "start" | "middle" | "end"
    "dominant-baseline": "auto",  # "auto" | "central" | "hanging" …
    "text-decoration": "none",
    "letter-spacing": "normal",
    "word-spacing": "normal",
    "writing-mode": "lr-tb",
}

COMMON_ALL = COMMON_PRESENTATION | COMMON_TEXT_PRESENTATION
class SVG(HTML):
    COMMON_PRESENTATION = COMMON_PRESENTATION
    COMMON_ALL = COMMON_ALL
    COMMON_TEXT_PRESENTATION = COMMON_TEXT_PRESENTATION


    _class_map = None
    @classmethod
    def get_class_map(cls):
        if cls._class_map is None:
            cls._class_map = {}
            for v in cls.__dict__.values():
                if isinstance(v, type) and hasattr(v, 'tag'):
                    cls._class_map[v.tag] = v
        return cls._class_map


    class TagElement(HTML.TagElement):
        tag = None
        required: dict
        optional: dict
        display_opts: dict

        ignored_styles = {"height", "width", "position", "color"}
        can_be_dynamic = False

        @classmethod
        def get_class_map_updates(cls):
            return SVG.get_class_map()

        @classmethod
        def convert_attrs(cls, attrs: dict):
            copied = False
            for k, v in attrs.items():
                if isinstance(v, str):
                    continue
                if not copied:
                    copied = True
                    attrs = attrs.copy()
                if v is None:
                    del attrs[k]
                else:
                    if hasattr(v, 'tolists') and hasattr(v, 'ndim') and v.ndim == 0:
                        v = v.tolists() # flatten len(0) arrays
                    if hasattr(v, "__getitem__") or hasattr(v, "__iter__"):
                        if hasattr(v, 'reshape'):
                            v = v.reshape(-1)
                        v = " ".join(str(x) for x in v)
                    elif v in {True, False}:
                        v = str(v).lower()
                    else:
                        v = str(v)
                    attrs[k] = v
            return attrs
        attr_converter = convert_attrs
        
        def validate(self, **kwargs):
            attrs = self.attrs
            missing = attrs.keys() - self.required.keys()
            if len(missing) > 0:
                raise ValueError(f"missing required attributes {missing}")
            #TODO: check other props
            self.validate_props(**kwargs)

        def __call__(self, *elems, **kwargs):
            return type(self)(
                self._elems + list(elems),
                activator=self.activator,
                on_update=self.on_update,
                **dict(self.attrs, **kwargs)
            )
    class Svg(TagElement):
       '''Root element. Always set viewBox for responsive sizing.'''
       tag = 'svg'
       required = {'xmlns': str, 'width': str, 'height': str}
       optional = {'viewBox': None, 'preserveAspectRatio': str, 'version': str, 'x': numbers.Number, 'y': numbers.Number}
       styles = ['transform', 'overflow']
       def __init__(self, *elems, xmlns='http://www.w3.org/2000/svg', width='100%', height='auto', **kwargs):
           super().__init__(*elems, xmlns=xmlns, width=width, height=height, **kwargs)
    class G(TagElement):
       '''Group element. Inherits presentation attrs to all children.'''
       tag = 'g'
       required = {}
       optional = {'id': None, 'transform': None}
       styles = COMMON_PRESENTATION
       def __init__(self, *elems, **kwargs):
           super().__init__(*elems, **kwargs)
    class Defs(TagElement):
       '''Container for reusable definitions (markers, gradients, etc.).'''
       tag = 'defs'
       required = {}
       optional = {'id': None}
       styles = []
       def __init__(self, *elems, **kwargs):
           super().__init__(*elems, **kwargs)
    class Symbol(TagElement):
       '''Reusable graphic referenced via <use>. Not rendered directly.'''
       tag = 'symbol'
       required = {'id': None}
       optional = {'viewBox': None, 'preserveAspectRatio': str, 'x': numbers.Number, 'y': numbers.Number, 'width': None, 'height': None}
       styles = COMMON_PRESENTATION
       def __init__(self, *elems, id=None, **kwargs):
           super().__init__(*elems, id=id, **kwargs)
    class Use(TagElement):
       '''Instantiates a <symbol> or any element by id.'''
       tag = 'use'
       required = {'href': None}
       optional = {'x': numbers.Number, 'y': numbers.Number, 'width': None, 'height': None}
       styles = COMMON_PRESENTATION
       def __init__(self, *elems, href=None, **kwargs):
           super().__init__(*elems, href=href, **kwargs)
    class Rect(TagElement):
       '''Axis-aligned rectangle. rx/ry round the corners.'''
       tag = 'rect'
       required = {'x': numbers.Number, 'y': numbers.Number, 'width': None, 'height': None}
       optional = {'rx': numbers.Number, 'ry': numbers.Number}
       styles = COMMON_PRESENTATION
       def __init__(self, *elems, x=0, y=0, width=None, height=None, **kwargs):
           super().__init__(*elems, x=x, y=y, width=width, height=height, **kwargs)
    class Circle(TagElement):
       '''Circle defined by centre (cx, cy) and radius r.'''
       tag = 'circle'
       required = {'cx': numbers.Number, 'cy': numbers.Number, 'r': None}
       optional = {}
       styles = COMMON_PRESENTATION
       def __init__(self, *elems, cx=0, cy=0, r=None, **kwargs):
           super().__init__(*elems, cx=cx, cy=cy, r=r, **kwargs)
    class Ellipse(TagElement):
       '''Ellipse with independent x- and y-radii.'''
       tag = 'ellipse'
       required = {'cx': numbers.Number, 'cy': numbers.Number, 'rx': None, 'ry': None}
       optional = {}
       styles = COMMON_PRESENTATION
       def __init__(self, *elems, cx=0, cy=0, rx=None, ry=None, **kwargs):
           super().__init__(*elems, cx=cx, cy=cy, rx=rx, ry=ry, **kwargs)
    class Line(TagElement):
       '''Straight line. stroke must be set; fill has no effect.'''
       tag = 'line'
       required = {'x1': numbers.Number, 'y1': numbers.Number, 'x2': numbers.Number, 'y2': numbers.Number}
       optional = {'marker-start': None, 'marker-mid': None, 'marker-end': None}
       styles = COMMON_PRESENTATION
       def __init__(self, *elems, x1=0, y1=0, x2=0, y2=0, **kwargs):
           super().__init__(*elems, x1=x1, y1=y1, x2=x2, y2=y2, **kwargs)
    class Polyline(TagElement):
       '''Open polygon (not closed). Use fill='none' for pure outline.'''
       tag = 'polyline'
       required = {'points': None}
       optional = {'marker-start': None, 'marker-mid': None, 'marker-end': None}
       styles = COMMON_PRESENTATION
       def __init__(self, *elems, points=None, **kwargs):
           super().__init__(*elems, points=points, **kwargs)
    class Polygon(TagElement):
       '''Closed polygon. Last point auto-connects to first.'''
       tag = 'polygon'
       required = {'points': None}
       optional = {'marker-start': None, 'marker-mid': None, 'marker-end': None}
       styles = COMMON_PRESENTATION
       def __init__(self, *elems, points=None, **kwargs):
           super().__init__(*elems, points=points, **kwargs)
    class Path(TagElement):
       '''Most versatile shape. Path commands: M/m (move), L/l (line), H/h (horiz), V/v (vert), C/c (cubic bezier), S/s (smooth cubic), Q/q (quadratic), T/t (smooth quad), A/a (arc), Z/z (close).'''
       tag = 'path'
       required = {'d': None}
       optional = {'pathLength': None, 'marker-start': None, 'marker-mid': None, 'marker-end': None}
       styles = COMMON_PRESENTATION
       def __init__(self, *elems, d=None, **kwargs):
           super().__init__(*elems, d=d, **kwargs)
    class Text(TagElement):
       '''Text element. Contains plain text or <tspan> children.'''
       tag = 'text'
       required = {'x': numbers.Number, 'y': numbers.Number}
       optional = {'dx': numbers.Number, 'dy': numbers.Number, 'rotate': None, 'textLength': None, 'lengthAdjust': str}
       styles = COMMON_ALL
       def __init__(self, *elems, x=0, y=0, **kwargs):
           super().__init__(*elems, x=x, y=y, **kwargs)
    class Tspan(TagElement):
       '''Inline text span; child of <text>. Use dy='1.2em' for line breaks.'''
       tag = 'tspan'
       required = {}
       optional = {'x': None, 'y': None, 'dx': None, 'dy': None, 'rotate': None, 'textLength': None, 'lengthAdjust': str}
       styles = COMMON_ALL
       def __init__(self, *elems, **kwargs):
           super().__init__(*elems, **kwargs)
    class Textpath(TagElement):
       '''Renders text along a <path>.'''
       tag = 'textPath'
       required = {'href': None}
       optional = {'startOffset': str, 'method': str, 'spacing': str, 'side': str}
       styles = COMMON_ALL
       def __init__(self, *elems, href=None, **kwargs):
           super().__init__(*elems, href=href, **kwargs)
    class Image(TagElement):
       '''Embeds a raster or SVG image.'''
       tag = 'image'
       required = {'href': None, 'x': numbers.Number, 'y': numbers.Number, 'width': None, 'height': None}
       optional = {'preserveAspectRatio': str, 'crossorigin': None, 'decoding': str, 'image-rendering': str}
       styles = ['opacity', 'transform', 'clip-path', 'mask', 'filter']
       def __init__(self, *elems, href=None, x=0, y=0, width=None, height=None, **kwargs):
           super().__init__(*elems, href=href, x=x, y=y, width=width, height=height, **kwargs)
    class Foreignobject(TagElement):
       '''Embeds arbitrary XML (e.g. HTML) inside SVG.'''
       tag = 'foreignObject'
       required = {'x': numbers.Number, 'y': numbers.Number, 'width': None, 'height': None}
       optional = {}
       styles = ['opacity', 'transform', 'clip-path', 'mask']
       def __init__(self, *elems, x=0, y=0, width=None, height=None, **kwargs):
           super().__init__(*elems, x=x, y=y, width=width, height=height, **kwargs)
    class Lineargradient(TagElement):
       '''Define with <stop> children; apply via fill='url(#id)'.'''
       tag = 'linearGradient'
       required = {'id': None}
       optional = {'x1': str, 'y1': str, 'x2': str, 'y2': str, 'gradientUnits': str, 'gradientTransform': None, 'spreadMethod': str, 'href': None}
       styles = []
       def __init__(self, *elems, id=None, **kwargs):
           super().__init__(*elems, id=id, **kwargs)
    class Radialgradient(TagElement):
       '''Radial gradient. fx/fy shift the highlight off-centre.'''
       tag = 'radialGradient'
       required = {'id': None}
       optional = {'cx': str, 'cy': str, 'r': str, 'fx': None, 'fy': None, 'fr': str, 'gradientUnits': str, 'gradientTransform': None, 'spreadMethod': str, 'href': None}
       styles = []
       def __init__(self, *elems, id=None, **kwargs):
           super().__init__(*elems, id=id, **kwargs)
    class Stop(TagElement):
       '''Colour stop inside a gradient. Always set stop-color.'''
       tag = 'stop'
       required = {'offset': None}
       optional = {'stop-color': str, 'stop-opacity': numbers.Number}
       styles = []
       def __init__(self, *elems, offset=None, **kwargs):
           super().__init__(*elems, offset=offset, **kwargs)
    class Pattern(TagElement):
       '''Tiling pattern paint server. Apply via fill='url(#id)'.'''
       tag = 'pattern'
       required = {'id': None, 'width': None, 'height': None}
       optional = {'x': numbers.Number, 'y': numbers.Number, 'patternUnits': str, 'patternContentUnits': str, 'patternTransform': None, 'viewBox': None, 'preserveAspectRatio': str, 'href': None}
       styles = []
       def __init__(self, *elems, id=None, width=None, height=None, **kwargs):
           super().__init__(*elems, id=id, width=width, height=height, **kwargs)
    class Clippath(TagElement):
       '''Hard clip. Apply via clip-path='url(#id)' on the target.'''
       tag = 'clipPath'
       required = {'id': None}
       optional = {'clipPathUnits': str, 'transform': None}
       styles = []
       def __init__(self, *elems, id=None, **kwargs):
           super().__init__(*elems, id=id, **kwargs)
    class Mask(TagElement):
       '''Luminance mask (white=visible, black=hidden). Apply via mask='url(#id)'.'''
       tag = 'mask'
       required = {'id': None}
       optional = {'x': str, 'y': str, 'width': str, 'height': str, 'maskUnits': str, 'maskContentUnits': str}
       styles = []
       def __init__(self, *elems, id=None, **kwargs):
           super().__init__(*elems, id=id, **kwargs)
    class Marker(TagElement):
       '''Arrowhead / endpoint decoration. orient='auto-start-reverse' flips for start markers automatically.'''
       tag = 'marker'
       required = {'id': None, 'viewBox': str, 'refX': numbers.Number, 'refY': numbers.Number, 'markerWidth': numbers.Number, 'markerHeight': numbers.Number}
       optional = {'orient': str, 'markerUnits': str, 'preserveAspectRatio': str}
       styles = COMMON_PRESENTATION
       def __init__(self, *elems, id=None, viewBox='0 0 10 10', refX=5, refY=5, markerWidth=6, markerHeight=6, **kwargs):
           super().__init__(*elems, id=id, viewBox=viewBox, refX=refX, refY=refY, markerWidth=markerWidth, markerHeight=markerHeight, **kwargs)
    class Filter(TagElement):
       '''Container for filter primitives. Apply via filter='url(#id)'.'''
       tag = 'filter'
       required = {'id': None}
       optional = {'x': str, 'y': str, 'width': str, 'height': str, 'filterUnits': str, 'primitiveUnits': str, 'color-interpolation-filters': str}
       styles = []
       def __init__(self, *elems, id=None, **kwargs):
           super().__init__(*elems, id=id, **kwargs)
    class Fegaussianblur(TagElement):
       '''Gaussian blur. stdDeviation='x y' for asymmetric blur.'''
       tag = 'feGaussianBlur'
       required = {'stdDeviation': None}
       optional = {'in': str, 'result': None, 'edgeMode': str}
       styles = []
       def __init__(self, *elems, stdDeviation=None, **kwargs):
           super().__init__(*elems, stdDeviation=stdDeviation, **kwargs)
    class Fecolormatrix(TagElement):
       '''Colour transform. type='saturate' values='0' → grayscale.'''
       tag = 'feColorMatrix'
       required = {'type': str}
       optional = {'in': str, 'result': None, 'values': None}
       styles = []
       def __init__(self, *elems, type='matrix', **kwargs):
           super().__init__(*elems, type=type, **kwargs)
    class Feblend(TagElement):
       '''Composites two inputs using a blend mode.'''
       tag = 'feBlend'
       required = {'in': str, 'in2': str}
       optional = {'mode': str, 'result': None}
       styles = []
       def __init__(self, *elems, in_='SourceGraphic', in2='BackgroundImage', **kwargs):
           super().__init__(*elems, in_=in_, in2=in2, **kwargs)
    class Fecomposite(TagElement):
       '''Alpha compositing of two filter inputs.'''
       tag = 'feComposite'
       required = {'in': str, 'in2': str}
       optional = {'operator': str, 'k1': numbers.Number, 'k2': numbers.Number, 'k3': numbers.Number, 'k4': numbers.Number, 'result': None}
       styles = []
       def __init__(self, *elems, in_='SourceGraphic', in2='SourceGraphic', **kwargs):
           super().__init__(*elems, in_=in_, in2=in2, **kwargs)
    class Feoffset(TagElement):
       '''Shifts its input. Combine with feGaussianBlur for drop shadows.'''
       tag = 'feOffset'
       required = {'dx': numbers.Number, 'dy': numbers.Number}
       optional = {'in': str, 'result': None}
       styles = []
       def __init__(self, *elems, dx=0, dy=0, **kwargs):
           super().__init__(*elems, dx=dx, dy=dy, **kwargs)
    class Femerge(TagElement):
       '''Combines multiple filter results. Children are <feMergeNode in_='…'>.'''
       tag = 'feMerge'
       required = {}
       optional = {'result': None}
       styles = []
       def __init__(self, *elems, **kwargs):
           super().__init__(*elems, **kwargs)
    class Femergenode(TagElement):
       '''Child of <feMerge>; references a filter result by name.'''
       tag = 'feMergeNode'
       required = {}
       optional = {'in': None}
       styles = []
       def __init__(self, *elems, **kwargs):
           super().__init__(*elems, **kwargs)
    class Feflood(TagElement):
       '''Fills filter region with a solid colour.'''
       tag = 'feFlood'
       required = {'flood-color': None}
       optional = {'flood-opacity': numbers.Number, 'result': None}
       styles = []
       def __init__(self, *elems, flood_color=None, **kwargs):
           super().__init__(*elems, flood_color=flood_color, **kwargs)
    class Feturbulence(TagElement):
       '''Perlin / fractal noise. Good base for texture effects.'''
       tag = 'feTurbulence'
       required = {'baseFrequency': None}
       optional = {'type': str, 'numOctaves': numbers.Number, 'seed': numbers.Number, 'stitchTiles': str, 'result': None}
       styles = []
       def __init__(self, *elems, baseFrequency=None, **kwargs):
           super().__init__(*elems, baseFrequency=baseFrequency, **kwargs)
    class Fedisplacementmap(TagElement):
       '''Warps 'in' using a displacement map from 'in2'.'''
       tag = 'feDisplacementMap'
       required = {'in': str, 'in2': None, 'scale': numbers.Number}
       optional = {'xChannelSelector': str, 'yChannelSelector': str, 'result': None}
       styles = []
       def __init__(self, *elems, in_='SourceGraphic', in2=None, scale=0, **kwargs):
           super().__init__(*elems, in_=in_, in2=in2, scale=scale, **kwargs)
    class Animate(TagElement):
       '''SMIL animation of a single attribute on the parent element.'''
       tag = 'animate'
       required = {'attributeName': None}
       optional = {'from': None, 'to': None, 'values': None, 'keyTimes': None, 'keySplines': None, 'calcMode': str, 'dur': None, 'repeatCount': str, 'repeatDur': None, 'begin': str, 'end': None, 'fill': str, 'additive': str, 'accumulate': str}
       styles = []
       def __init__(self, *elems, attributeName=None, **kwargs):
           super().__init__(*elems, attributeName=attributeName, **kwargs)
    class Animatetransform(TagElement):
       '''Animates a transform. type='rotate' from/to can include cx,cy: '0 50 50'.'''
       tag = 'animateTransform'
       required = {'attributeName': str, 'type': str}
       optional = {'from': None, 'to': None, 'values': None, 'dur': None, 'repeatCount': str, 'begin': str, 'fill': str, 'additive': str}
       styles = []
       def __init__(self, *elems, attributeName='transform', type='rotate', **kwargs):
           super().__init__(*elems, attributeName=attributeName, type=type, **kwargs)
    class Animatemotion(TagElement):
       '''Moves element along a path. Add <mpath href='#path-id'> as child.'''
       tag = 'animateMotion'
       required = {}
       optional = {'path': None, 'keyPoints': None, 'rotate': str, 'dur': None, 'repeatCount': str, 'begin': str, 'calcMode': str}
       styles = []
       def __init__(self, *elems, **kwargs):
           super().__init__(*elems, **kwargs)
    class Set(TagElement):
       '''Discretely sets an attribute value for a duration (no interpolation).'''
       tag = 'set'
       required = {'attributeName': None, 'to': None}
       optional = {'begin': str, 'dur': None, 'end': None, 'fill': str}
       styles = []
       def __init__(self, *elems, attributeName=None, to=None, **kwargs):
           super().__init__(*elems, attributeName=attributeName, to=to, **kwargs)
    class Title(TagElement):
       '''Accessible name for the SVG or a group. First child of <svg> or <g>.'''
       tag = 'title'
       required = {}
       optional = {}
       styles = []
       def __init__(self, *elems, **kwargs):
           super().__init__(*elems, **kwargs)
    class Desc(TagElement):
       '''Longer accessible description. Complements <title>.'''
       tag = 'desc'
       required = {}
       optional = {}
       styles = []
       def __init__(self, *elems, **kwargs):
           super().__init__(*elems, **kwargs)
    class Metadata(TagElement):
       '''Container for non-SVG metadata (e.g. RDF, XMP).'''
       tag = 'metadata'
       required = {}
       optional = {}
       styles = []
       def __init__(self, *elems, **kwargs):
           super().__init__(*elems, **kwargs)


del COMMON_ALL
del COMMON_PRESENTATION
del COMMON_TEXT_PRESENTATION