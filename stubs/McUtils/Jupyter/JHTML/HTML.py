from __future__ import annotations
import itertools
import re
import numbers
import uuid
from xml.etree import ElementTree
import weakref, numpy as np, copy, textwrap, inspect
import contextlib
__all__ = ['HTML', 'CSS', 'ContentXML', 'SVG']
from ...Data import ColorData
from ...Misc import mixedmethod
from .Enums import Options
from .WidgetTools import frozendict

class ValidationError(ValueError):
    ...
_CSS_COLOR_KEYWORDS = {'none', 'inherit', 'currentcolor', 'transparent'}
_RE_HEX3 = re.compile('^#[0-9a-f]{3}$', re.I)
_RE_HEX4 = re.compile('^#[0-9a-f]{4}$', re.I)
_RE_HEX6 = re.compile('^#[0-9a-f]{6}$', re.I)
_RE_HEX8 = re.compile('^#[0-9a-f]{8}$', re.I)
_RE_RGB = re.compile('^rgb\\(\\s*(\\d+%?)\\s*,\\s*(\\d+%?)\\s*,\\s*(\\d+%?)\\s*\\)$', re.I)
_RE_RGBA = re.compile('^rgba\\(\\s*(\\d+%?)\\s*,\\s*(\\d+%?)\\s*,\\s*(\\d+%?)\\s*,\\s*([0-9.]+)\\s*\\)$', re.I)
_RE_HSL = re.compile('^hsl\\(\\s*[\\d.]+\\s*,\\s*[\\d.]+%\\s*,\\s*[\\d.]+%\\s*\\)$', re.I)
_RE_HSLA = re.compile('^hsla\\(\\s*[\\d.]+\\s*,\\s*[\\d.]+%\\s*,\\s*[\\d.]+%\\s*,\\s*[0-9.]+\\s*\\)$', re.I)
_RE_URL = re.compile('^url\\(#[^)]+\\)$')
_RE_NUM = re.compile('^[+-]?(\\d+\\.?\\d*|\\.\\d+)([eE][+-]?\\d+)?$')
_RE_LEN = re.compile('^[+-]?(\\d+\\.?\\d*|\\.\\d+)([eE][+-]?\\d+)?(px|pt|pc|mm|cm|in|em|ex|rem|vh|vw|vmin|vmax|%)?$')
_RE_ANGLE = re.compile('^[+-]?(\\d+\\.?\\d*|\\.\\d+)(deg|rad|grad|turn)?$', re.I)

def _is_number(v: str | numbers.Number) -> bool:
    """
    **LLM Docstring**

    Return whether a value is numeric or a string matching the module’s numeric-literal pattern.

    :param v: The value to inspect.
    :type v: str | numbers.Number

    :return: `True` when the implemented condition is satisfied; otherwise `False`.
    :rtype: bool
    """
    ...

def _is_length(v: str) -> bool:
    """
    **LLM Docstring**

    Return whether a string is a CSS/SVG length, optionally including a supported unit.

    :param v: The value to inspect.
    :type v: str

    :return: `True` when the implemented condition is satisfied; otherwise `False`.
    :rtype: bool
    """
    ...

def _is_angle(v: str) -> bool:
    """
    **LLM Docstring**

    Return whether a string is a numeric angle with an optional CSS angle unit.

    :param v: The value to inspect.
    :type v: str

    :return: `True` when the implemented condition is satisfied; otherwise `False`.
    :rtype: bool
    """
    ...

def _is_color(v: str) -> bool:
    """
    **LLM Docstring**

    Recognize named colors, CSS color keywords, hexadecimal forms, and supported RGB/HSL function syntax.

    :param v: The value to inspect.
    :type v: str

    :return: `True` when the implemented condition is satisfied; otherwise `False`.
    :rtype: bool
    """
    ...

def _is_paint(v: str) -> bool:
    """Paint value: colour, none, inherit, or url(#id) optionally followed by a fallback colour."""
    ...

def _is_opacity(v: str | numbers.Number) -> bool:
    """
    **LLM Docstring**

    Convert the value to `float` and test whether it lies in the inclusive interval `[0, 1]`.

    :param v: The value to inspect.
    :type v: str | numbers.Number

    :return: `True` when the implemented condition is satisfied; otherwise `False`.
    :rtype: bool
    """
    ...

def _check_oneof(value, attr, types) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate membership in an allowed-value set and build a human-readable `ValidationError` when membership fails.

    :param value: The value to validate or assign.
    :type value: object
    :param attr: The attribute or property name associated with the value.
    :type attr: object
    :param types: The allowed values.
    :type types: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def _check_paint(attr: str, value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate a paint-valued property as a string containing a color, inherited value, `none`, or an SVG `url(#id)` reference.

    :param attr: The attribute or property name associated with the value.
    :type attr: str
    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_fill(value):
    ...

def check_stroke(value):
    ...

def check_color(value):
    ...

def check_flood_color(value):
    ...

def check_stop_color(value):
    ...

def check_lighting_color(value):
    ...

def _check_opacity_attr(attr: str, value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate an opacity property, accepting `inherit` or a numeric value in `[0, 1]`.

    :param attr: The attribute or property name associated with the value.
    :type attr: str
    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_opacity(value):
    ...

def check_fill_opacity(value):
    ...

def check_stroke_opacity(value):
    ...

def check_flood_opacity(value):
    ...

def check_stop_opacity(value):
    ...

def check_fill_rule(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `fill-rule` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_stroke_width(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `stroke-width` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...
linecap_types = {'butt', 'round', 'square', 'inherit'}

def check_stroke_linecap(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `stroke-linecap` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...
linejoin_types = {'miter', 'miter-clip', 'round', 'bevel', 'arcs', 'inherit'}

def check_stroke_linejoin(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `stroke-linejoin` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_stroke_miterlimit(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `stroke-miterlimit` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_stroke_dasharray(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `stroke-dasharray` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_stroke_dashoffset(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `stroke-dashoffset` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...
visibility_types = {'visible', 'hidden', 'collapse', 'inherit'}

def check_visibility(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `visibility` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_display(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `display` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...
paint_order_tokens = {'fill', 'stroke', 'markers'}

def check_paint_order(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `paint-order` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def _check_uri_or_none(attr: str, value: str) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate a URI-valued presentation property, accepting `none`, `inherit`, or an SVG `url(#id)` reference.

    :param attr: The attribute or property name associated with the value.
    :type attr: str
    :param value: The value to validate or assign.
    :type value: str

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_clip_path(value):
    ...

def check_mask(value):
    ...

def check_filter(value):
    ...

def check_transform(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `transform` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_pointer_events(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `pointer-events` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_cursor(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `cursor` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...
vector_effect_types = {'none', 'non-scaling-stroke', 'non-scaling-size', 'non-rotation', 'fixed-position', 'inherit'}

def check_vector_effect(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `vector-effect` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_font_family(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Accept any font-family value without performing validation; this function currently always returns an empty error list.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...
_FONT_SIZE_KEYWORDS = {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large', 'smaller', 'larger', 'inherit'}

def check_font_size(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `font-size` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...
font_weight_types = {'normal', 'bold', 'bolder', 'lighter', 'inherit'}

def check_font_weight(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `font-weight` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...
font_style_types = {'normal', 'italic', 'oblique', 'inherit'}

def check_font_style(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `font-style` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...
font_variant_types = {'normal', 'small-caps', 'inherit'}

def check_font_variant(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `font-variant` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...
text_anchor_types = {'start', 'middle', 'end', 'inherit'}

def check_text_anchor(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `text-anchor` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_dominant_baseline(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `dominant-baseline` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...
text_decoration_types = {'underline', 'overline', 'line-through', 'blink'}

def check_text_decoration(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `text-decoration` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def _check_spacing(attr: str, value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate letter or word spacing as `normal`, `inherit`, or a supported CSS length.

    :param attr: The attribute or property name associated with the value.
    :type attr: str
    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def check_letter_spacing(value) -> list[ValidationError]:
    ...

def check_word_spacing(value) -> list[ValidationError]:
    ...
writing_mode_types = {'lr-tb', 'rl-tb', 'tb-rl', 'lr', 'rl', 'tb', 'horizontal-tb', 'vertical-rl', 'vertical-lr', 'inherit'}

def check_writing_mode(value) -> list[ValidationError]:
    """
    **LLM Docstring**

    Validate the `writing-mode` presentation value according to the constraints implemented in this module.

    :param value: The value to validate or assign.
    :type value: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

def validate_props(props: dict, validators: dict, raise_on_invalid=True, undefined_is_missing=False):
    """
    **LLM Docstring**

    Run registered validators over a property mapping, optionally treating unknown properties as errors and raising aggregated failures.

    :param props: The property mapping to validate or normalize.
    :type props: dict
    :param validators: Mapping from property names to validator callables.
    :type validators: dict
    :param raise_on_invalid: Whether to raise when validation errors are found.
    :type raise_on_invalid: object
    :param undefined_is_missing: Whether unknown properties should be reported as validation errors.
    :type undefined_is_missing: object

    :return: Validation errors found by the check, or an empty list when the value is accepted.
    :rtype: list[ValidationError]
    """
    ...

class CSS:
    """
    Defines a holder for CSS properties
    """

    def __init__(self, *selectors, **props):
        """
        **LLM Docstring**

        Store CSS selectors and canonicalize underscore-separated property names to hyphenated CSS names.

        :param selectors: CSS selectors associated with the rule.
        :type selectors: tuple
        :param props: The property mapping to validate or normalize.
        :type props: dict
        """
        ...
    known_properties = set((o.value for o in Options))

    @classmethod
    def construct(cls, *selectors, aspect_ratio=None, background=None, background_attachment=None, background_color=None, background_image=None, background_position=None, background_repeat=None, border=None, border_bottom=None, border_bottom_color=None, border_bottom_style=None, border_bottom_width=None, border_color=None, border_left=None, border_left_color=None, border_left_style=None, border_left_width=None, border_right=None, border_right_color=None, border_right_style=None, border_right_width=None, border_style=None, border_top=None, border_top_color=None, border_top_style=None, border_top_width=None, border_width=None, clear=None, clip=None, color=None, cursor=None, display=None, filter=None, float=None, font=None, font_family=None, font_size=None, font_variant=None, font_weight=None, height=None, left=None, letter_spacing=None, line_height=None, list_style=None, list_style_image=None, list_style_position=None, list_style_type=None, margin=None, margin_bottom=None, margin_left=None, margin_right=None, margin_top=None, overflow=None, padding=None, padding_bottom=None, padding_left=None, padding_right=None, padding_top=None, page_break_after=None, page_break_before=None, position=None, text_align=None, text_decoration=None, text_indent=None, text_transform=None, top=None, vertical_align=None, visibility=None, width=None, z_index=None, **props):
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
        ...

    @classmethod
    def canonicalize_props(cls, props):
        """
        **LLM Docstring**

        Convert Python-style underscore property names to CSS hyphenated names without changing values.

        :param props: The property mapping to validate or normalize.
        :type props: object

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

    @classmethod
    def parse(cls, sty):
        """
        **LLM Docstring**

        Parse either inline declarations or selector blocks into one or more `CSS` objects; block parsing returns after the first parsed block in the current implementation.

        :param sty: A CSS declaration string or complete rule block.
        :type sty: object

        :return: a set of CSS ops
        :rtype: list[CSS]
        """
        ...

    def tostring(self):
        """
        **LLM Docstring**

        Serialize the stored CSS rule as either a selector block or an inline declaration string.

        :return: The generated string representation.
        :rtype: str
        """
        ...
    validators = BASE_VALIDATORS

    def validate(self, **kwargs):
        """
        **LLM Docstring**

        Validate the stored CSS properties with the class validator mapping.

        :param kwargs: Additional attributes or options forwarded to the constructed element.
        :type kwargs: dict

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

class HTMLManager:

    @classmethod
    def manage_class(kls, cls):
        """
        **LLM Docstring**

        Normalize a class specification into a list of class-name strings.

        :param kls: The manager class performing normalization.
        :type kls: object

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

    @classmethod
    def manage_styles(cls, styles):
        """
        **LLM Docstring**

        Convert mappings or strings into a `CSS` object while leaving existing style objects unchanged.

        :param styles: Style values to apply.
        :type styles: object

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...
    keyword_replacements = {'cls': 'class', 'in_': 'in', 'use_for': 'for', 'custom_type': 'is'}

    @classmethod
    def clean_key(cls, k):
        """
        **LLM Docstring**

        Map reserved Python attribute aliases and underscores to their HTML attribute spelling.

        :param k: The attribute or property name.
        :type k: object

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

    @classmethod
    def sanitize_value(cls, val):
        """
        **LLM Docstring**

        Convert NumPy scalars and rich display objects into plain Python or HTML element representations.

        :param val: The value to sanitize.
        :type val: object

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

    @classmethod
    def manage_attrs(cls, attrs, sanitize=True):
        """
        **LLM Docstring**

        Canonicalize attribute names and optionally sanitize each attribute value.

        :param attrs: Attribute values to normalize or apply.
        :type attrs: object
        :param sanitize: Whether to convert supported Python values into HTML-compatible representations.
        :type sanitize: object

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

    @classmethod
    def extract_styles(cls, attrs, style_props=None, ignored_styles=None):
        """
        **LLM Docstring**

        Remove recognized style properties from an attribute mapping and return them separately.

        :param attrs: Attribute values to normalize or apply.
        :type attrs: object
        :param style_props: The set of attribute names treated as CSS properties.
        :type style_props: object
        :param ignored_styles: Style names to exclude from extraction.
        :type ignored_styles: object

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...
    validators = BASE_VALIDATORS

    @classmethod
    def validate_props(cls, props, **kwargs):
        """
        **LLM Docstring**

        Validate a property mapping using `HTMLManager.validators`.

        :param props: The property mapping to validate or normalize.
        :type props: object
        :param kwargs: Additional attributes or options forwarded to the constructed element.
        :type kwargs: dict

        :return: Validation errors found by the check, or an empty list when the value is accepted.
        :rtype: list[ValidationError]
        """
        ...

    class ElementModifier:

        def __init__(self, my_el, copy=False):
            """
            **LLM Docstring**

            Initialize a deferred element modifier and record whether modification requires copying.

            :param my_el: The element or modifier to wrap.
            :type my_el: object
            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            """
            ...

        def modify(self):
            """
            **LLM Docstring**

            Return either the wrapped element or a copy, depending on the modifier setting.

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def tostring(self):
            """
            **LLM Docstring**

            Serialize the element produced by `modify`.

            :return: The generated string representation.
            :rtype: str
            """
            ...

        def _repr_html_(self):
            """
            **LLM Docstring**

            Return the modified element’s HTML serialization for notebook display.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def copy(self):
            """
            **LLM Docstring**

            Shallow-copy the modifier and replace its wrapped element with a copied element.

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def add_class(self, *cls, copy=True):
            """
            **LLM Docstring**

            Create a class-adding modifier around this modifier.

            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            :param cls: The class performing the operation.
            :type cls: tuple

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def remove_class(self, *cls, copy=True):
            """
            **LLM Docstring**

            Create a class-removing modifier around this modifier.

            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            :param cls: The class performing the operation.
            :type cls: tuple

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def add_styles(self, copy=True, **sty):
            """
            **LLM Docstring**

            Create a style-adding modifier around this modifier.

            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            :param sty: A CSS declaration string or complete rule block.
            :type sty: dict

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

    class ClassAdder(ElementModifier):
        cls = None

        def __init__(self, el, cls=None, copy=True):
            """
            **LLM Docstring**

            Initialize or apply a deferred class addition, preserving existing classes and avoiding duplicates.

            :param el: The element or modifier to wrap.
            :type el: object
            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            """
            ...

        def modify(self):
            """
            **LLM Docstring**

            Initialize or apply a deferred class addition, preserving existing classes and avoiding duplicates.

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def __repr__(self):
            """
            **LLM Docstring**

            Return a debugging representation of the class-adder modifier.

            :return: The generated string representation.
            :rtype: str
            """
            ...

    class ClassRemover(ElementModifier):
        cls = None

        def __init__(self, el, cls=None, copy=True):
            """
            **LLM Docstring**

            Initialize or apply a deferred class removal, silently ignoring classes that are absent.

            :param el: The element or modifier to wrap.
            :type el: object
            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            """
            ...

        def modify(self):
            """
            **LLM Docstring**

            Initialize or apply a deferred class removal, silently ignoring classes that are absent.

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def __repr__(self):
            """
            **LLM Docstring**

            Return a debugging representation of the class-remover modifier.

            :return: The generated string representation.
            :rtype: str
            """
            ...

    class StyleAdder(ElementModifier):

        def __init__(self, el, copy=True, **styles):
            """
            **LLM Docstring**

            Initialize or apply a deferred style merge onto an element’s inline `CSS` mapping.

            :param el: The element or modifier to wrap.
            :type el: object
            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            :param styles: Style values to apply.
            :type styles: dict
            """
            ...

        def modify(self):
            """
            **LLM Docstring**

            Initialize or apply a deferred style merge onto an element’s inline `CSS` mapping.

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def __repr__(self):
            """
            **LLM Docstring**

            Return a debugging representation of the style-adder modifier.

            :return: The generated string representation.
            :rtype: str
            """
            ...

    class StyleRemover(ElementModifier):

        def __init__(self, el, *styles, copy=True):
            """
            **LLM Docstring**

            Initialize or apply removal of selected inline style keys when a style attribute exists.

            :param el: The element or modifier to wrap.
            :type el: object
            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            :param styles: Style values to apply.
            :type styles: tuple
            """
            ...

        def modify(self):
            """
            **LLM Docstring**

            Initialize or apply removal of selected inline style keys when a style attribute exists.

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def __repr__(self):
            """
            **LLM Docstring**

            Return a debugging representation of the style-remover modifier.

            :return: The generated string representation.
            :rtype: str
            """
            ...

    @classmethod
    def xml_to_json(cls, tree: ElementTree.Element, root=None):
        """
        **LLM Docstring**

        Recursively convert an `ElementTree` node into the module’s JSON-compatible tree representation, preserving registered raw HTML.

        :param tree: The XML tree node to convert.
        :type tree: ElementTree.Element
        :param root: Destination root element or XPath root expression.
        :type root: object

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

class XMLBase:

    class ElementBase:
        ...

    @classmethod
    def find_globals(cls):
        """
        **LLM Docstring**

        Find the first `__main__` global namespace in the call stack, falling back to the immediate caller globals.

        :return: The value produced by the implemented operation.
        :rtype: object | None
        """
        ...

    @classmethod
    def expose(cls, globs=None):
        """
        **LLM Docstring**

        Insert every registered tag class into a target global namespace under its class name.

        :param globs: Namespace into which generated element classes are exposed.
        :type globs: object

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...
    _cls_map = None

    @classmethod
    def get_class_map(cls):
        """
        **LLM Docstring**

        Lazily build and cache the tag-to-element-class mapping from nested classes defining `tag`.

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

    @classmethod
    @contextlib.contextmanager
    def class_map_context(cls, extra_classes):
        """
        **LLM Docstring**

        Temporarily extend the cached tag-class mapping and restore the previous mapping afterward.

        :param extra_classes: Additional tag-to-class mappings active inside the context.
        :type extra_classes: object

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...
    base_element = None

    @classmethod
    def convert(cls, etree: ElementTree.Element, strip=True, converter=None, **extra_attrs):
        """
        **LLM Docstring**

        Recursively convert an `ElementTree` element, including text and tails, into registered wrapper classes.

        :param etree: The `ElementTree` element to convert.
        :type etree: ElementTree.Element
        :param strip: Whether surrounding newline characters and empty text nodes are removed.
        :type strip: object
        :param converter: Recursive element conversion callable.
        :type converter: object
        :param extra_attrs: Additional attributes merged onto the converted element.
        :type extra_attrs: dict

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

    @classmethod
    def parse(cls, str, strict=True, strip=True, fallback=None, converter=None, namespace=None):
        """
        **LLM Docstring**

        Parse XML/HTML text and, in non-strict mode, wrap multi-root or invalid input with a fallback element.

        :param str: The XML or HTML source string.
        :type str: object
        :param strict: Whether parsing errors should be propagated instead of using a fallback.
        :type strict: object
        :param strip: Whether surrounding newline characters and empty text nodes are removed.
        :type strip: object
        :param fallback: Callable used to wrap invalid or multi-root input when non-strict parsing is enabled.
        :type fallback: object
        :param converter: Recursive element conversion callable.
        :type converter: object
        :param namespace: Optional default XML namespace to register before parsing.
        :type namespace: object

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

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
            """
            **LLM Docstring**

            Return additional tag-class mappings for this element type; the base implementation supplies none.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @classmethod
        def expanded_class_map(cls):
            """
            **LLM Docstring**

            Return a context manager that temporarily installs this element type’s class-map updates.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def __init__(self, tag, *elems, on_update=None, style=None, activator=None, can_be_dynamic=None, **attrs):
            """
            **LLM Docstring**

            Initialize an HTML element, sanitize children and attributes, split inline styles, and prepare callback and serialization caches.

            :param tag: The element tag name.
            :type tag: object
            :param on_update: Callbacks invoked when element content or attributes change.
            :type on_update: object
            :param style: Inline style specification.
            :type style: object
            :param activator: Callable that converts the element into an active representation.
            :type activator: object
            :param can_be_dynamic: Optional override controlling whether the element may be converted to a dynamic widget.
            :type can_be_dynamic: object
            :param elems: Child elements or text content.
            :type elems: tuple
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict
            """
            ...

        class _update_callbacks:
            """
            Simple set of callbacks both weakly keyed and default
            """

            def __init__(self, base_callbacks, weak_callbacks):
                """
                **LLM Docstring**

                Store global callbacks and optional weakly keyed registrant-specific callbacks.

                :param base_callbacks: Callbacks not associated with a registrant.
                :type base_callbacks: object
                :param weak_callbacks: Weak-keyed callbacks associated with registrant objects.
                :type weak_callbacks: object
                """
                ...

            @classmethod
            def from_raw(cls, data):
                """
                **LLM Docstring**

                Canonicalize callback input into global and weakly keyed callback mappings.

                :param data: Raw callback data or values to convert.
                :type data: object

                :return: The value produced by the implemented operation.
                :rtype: object
                """
                ...

            def items(self):
                """
                **LLM Docstring**

                Iterate registrant-specific callback mappings followed by the global callback mapping.

                :return: An iterator or view over the requested values.
                :rtype: iterator
                """
                ...

            def __contains__(self, item):
                """
                **LLM Docstring**

                Test whether a registrant-specific callback mapping exists; `None` always denotes the global mapping.

                :param item: The attribute name or child index.
                :type item: object

                :return: `True` when the implemented condition is satisfied; otherwise `False`.
                :rtype: bool
                """
                ...

            def __setitem__(self, key, value):
                """
                **LLM Docstring**

                Replace either the global callback mapping or a registrant-specific weak mapping.

                :param key: The update category or mapping key.
                :type key: object
                :param value: The value to validate or assign.
                :type value: object

                :return: The value produced by the implemented operation.
                :rtype: object
                """
                ...

            def get(self, item, default):
                """
                **LLM Docstring**

                Retrieve callbacks for the global or a registrant-specific mapping.

                :param item: The attribute name or child index.
                :type item: object
                :param default: Fallback value returned when the item is absent.
                :type default: object

                :return: The value produced by the implemented operation.
                :rtype: object
                """
                ...

            def __getitem__(self, item):
                """
                **LLM Docstring**

                Retrieve callbacks and raise `KeyError` when a non-global registrant is absent.

                :param item: The attribute name or child index.
                :type item: object

                :return: The value produced by the implemented operation.
                :rtype: object
                """
                ...

        def _canonicalize_callback_dict(self, on_update):
            """
            **LLM Docstring**

            Convert raw update callback input into the internal callback container.

            :param on_update: Callbacks invoked when element content or attributes change.
            :type on_update: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def on_update(self, key, new_value, old_value, subkey=None):
            """
            **LLM Docstring**

            Invoke callbacks registered for the specific update key and callbacks registered for all updates.

            :param key: The update category or mapping key.
            :type key: object
            :param new_value: The value after an update.
            :type new_value: object
            :param old_value: The value before an update.
            :type old_value: object
            :param subkey: The affected nested key or element index.
            :type subkey: object

            :return: No value is returned.
            :rtype: None
            """
            ...

        def update_callbacks(self, key=None, registrant=None):
            """
            **LLM Docstring**

            Return callbacks registered for a key and optional registrant.

            :param key: The update category or mapping key.
            :type key: object
            :param registrant: Optional object used to weakly scope callbacks.
            :type registrant: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def add_update_callback(self, callback, key=None, registrant=None):
            """
            **LLM Docstring**

            Register an update callback under an optional update key and registrant.

            :param callback: The callback to register or remove.
            :type callback: object
            :param key: The update category or mapping key.
            :type key: object
            :param registrant: Optional object used to weakly scope callbacks.
            :type registrant: object

            :return: No value is returned.
            :rtype: None
            """
            ...

        def remove_update_callback(self, callback, key=None, registrant=None):
            """
            **LLM Docstring**

            Remove a previously registered update callback.

            :param callback: The callback to register or remove.
            :type callback: object
            :param key: The update category or mapping key.
            :type key: object
            :param registrant: Optional object used to weakly scope callbacks.
            :type registrant: object

            :return: No value is returned.
            :rtype: None
            """
            ...

        def __call__(self, *elems, **kwargs):
            """
            **LLM Docstring**

            Create another element of the same type by appending children and merging attributes.

            :param elems: Child elements or text content.
            :type elems: tuple
            :param kwargs: Additional attributes or options forwarded to the constructed element.
            :type kwargs: dict

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @property
        def attrs(self):
            """
            **LLM Docstring**

            Access or replace the element’s immutable attribute view; assignment normalizes attributes and emits an update.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @attrs.setter
        def attrs(self, attrs):
            """
            **LLM Docstring**

            Access or replace the element’s immutable attribute view; assignment normalizes attributes and emits an update.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @property
        def elems(self):
            """
            **LLM Docstring**

            Access or replace the element’s immutable child view, converting scalar numeric children to strings on read.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @elems.setter
        def elems(self, elems):
            """
            **LLM Docstring**

            Access or replace the element’s immutable child view, converting scalar numeric children to strings on read.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def set_elems(self, elems):
            """
            **LLM Docstring**

            Replace child content, invalidate cached trees, and emit an element-update callback.

            :param elems: Child elements or text content.
            :type elems: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def activate(self):
            """
            **LLM Docstring**

            Pass the element to its configured activator callable.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        class StyleWrapper:

            def __init__(self, style_dict, obj):
                """
                **LLM Docstring**

                Create a mapping-like proxy that writes style changes back through the owning element.

                :param style_dict: The underlying mutable style mapping.
                :type style_dict: object
                :param obj: The element that owns the style mapping.
                :type obj: object
                """
                ...

            def __repr__(self):
                """
                **LLM Docstring**

                Return a representation of the wrapped style dictionary.

                :return: The generated string representation.
                :rtype: str
                """
                ...

            def __getitem__(self, item):
                """
                **LLM Docstring**

                Read a style value from the wrapped mapping.

                :param item: The attribute name or child index.
                :type item: object

                :return: The value produced by the implemented operation.
                :rtype: object
                """
                ...

            def __setitem__(self, key, value):
                """
                **LLM Docstring**

                Copy-update one style entry and assign the resulting mapping through the owning element.

                :param key: The update category or mapping key.
                :type key: object
                :param value: The value to validate or assign.
                :type value: object

                :return: The value produced by the implemented operation.
                :rtype: object
                """
                ...

            def __iter__(self):
                """
                **LLM Docstring**

                Iterate style keys.

                :return: The value produced by the implemented operation.
                :rtype: object
                """
                ...

            def get(self, item, default=None):
                """
                **LLM Docstring**

                Return a style value with an optional default.

                :param item: The attribute name or child index.
                :type item: object
                :param default: Fallback value returned when the item is absent.
                :type default: object

                :return: The value produced by the implemented operation.
                :rtype: object
                """
                ...

            def items(self):
                """
                **LLM Docstring**

                Return the style mapping’s items view.

                :return: An iterator or view over the requested values.
                :rtype: iterator
                """
                ...

            def keys(self):
                """
                **LLM Docstring**

                Return the style mapping’s keys view.

                :return: An iterator or view over the requested values.
                :rtype: iterator
                """
                ...

            def values(self):
                """
                **LLM Docstring**

                Return the style mapping’s values view.

                :return: An iterator or view over the requested values.
                :rtype: iterator
                """
                ...

        @property
        def style(self):
            """
            **LLM Docstring**

            Access inline styles through a write-through mapping proxy, or replace the style attribute.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @style.setter
        def style(self, styles):
            """
            **LLM Docstring**

            Access inline styles through a write-through mapping proxy, or replace the style attribute.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @property
        def class_list(self):
            """
            **LLM Docstring**

            Return the normalized list of CSS classes.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def invalidate_cache(self):
            """
            **LLM Docstring**

            Clear the cached `ElementTree` representation and recursively invalidate parent elements.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def __getitem__(self, item):
            """
            **LLM Docstring**

            Read an attribute by string key or a child by numeric/slice index.

            :param item: The attribute name or child index.
            :type item: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def __setitem__(self, item, value):
            """
            **LLM Docstring**

            Assign an attribute or child, invalidate serialization caches, and emit an update callback.

            :param item: The attribute name or child index.
            :type item: object
            :param value: The value to validate or assign.
            :type value: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def insert(self, where, child):
            """
            **LLM Docstring**

            Insert a child at an index or append when the index is `None`, then invalidate caches and emit an update.

            :param where: Insertion index, or `None` to append.
            :type where: object
            :param child: Child object to insert.
            :type child: object

            :return: No value is returned.
            :rtype: None
            """
            ...

        def append(self, child):
            """
            **LLM Docstring**

            Append a child through `insert`.

            :param child: Child object to insert.
            :type child: object

            :return: No value is returned.
            :rtype: None
            """
            ...

        def __delitem__(self, item):
            """
            **LLM Docstring**

            Delete an attribute or child if present, invalidate caches, and emit the corresponding update callback.

            :param item: The attribute name or child index.
            :type item: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...
        atomic_types = (int, bool, float)

        @classmethod
        def construct_etree_element(cls, elem, root, top, parent=None, attr_converter=None):
            """
            **LLM Docstring**

            Append one child to an `ElementTree`, handling wrapped elements, raw HTML sentinels, text, modifiers, widgets, and native nodes.

            :param elem: Child object to serialize into an `ElementTree` node.
            :type elem: object
            :param root: Destination root element or XPath root expression.
            :type root: object
            :param top: Top-level tree root carrying raw-HTML substitutions.
            :type top: object
            :param parent: Parent element used for cache invalidation or selector traversal.
            :type parent: object
            :param attr_converter: Optional callable that converts the serialized attribute mapping.
            :type attr_converter: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...
        attr_converter = None

        @classmethod
        def construct_etree_attrs(cls, attrs, attr_converter=None):
            """
            **LLM Docstring**

            Convert style and class attributes to serialized strings and apply an optional final attribute converter.

            :param attrs: Attribute values to normalize or apply.
            :type attrs: object
            :param attr_converter: Optional callable that converts the serialized attribute mapping.
            :type attr_converter: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @property
        def tree(self):
            """
            **LLM Docstring**

            Return the cached or newly constructed `ElementTree` node.

            :return: The value produced by the implemented operation.
            :rtype: ElementTree.Element
            """
            ...

        class TreeRoot(ElementTree.Element):

            def __init__(self):
                """
                **LLM Docstring**

                Initialize the synthetic tree root and its raw-HTML replacement cache.
                """
                ...

            def __repr__(self):
                """
                **LLM Docstring**

                Return a compact representation of the synthetic root.

                :return: The generated string representation.
                :rtype: str
                """
                ...

        def to_tree(self, root=None, top=None, parent=None, attr_converter=None):
            """
            **LLM Docstring**

            Build or attach the cached `ElementTree` node while tracking parent relationships and the shared raw-HTML root.

            :param root: Destination root element or XPath root expression.
            :type root: object
            :param top: Top-level tree root carrying raw-HTML substitutions.
            :type top: object
            :param parent: Parent element used for cache invalidation or selector traversal.
            :type parent: object
            :param attr_converter: Optional callable that converts the serialized attribute mapping.
            :type attr_converter: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def modify(self, elems=None, **attrs):
            """
            **LLM Docstring**

            Create a new element with optionally replaced children and merged attributes/styles.

            :param elems: Child elements or text content.
            :type elems: object
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def clean_props(self, attr_converter=None):
            """
            **LLM Docstring**

            Recursively rebuild the element after applying an attribute converter to this element and compatible children.

            :param attr_converter: Optional callable that converts the serialized attribute mapping.
            :type attr_converter: object

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def to_json(self, root=None, parent=None, attr_converter=None):
            """
            **LLM Docstring**

            Convert the serialized tree into the module’s JSON-compatible node representation.

            :param root: Destination root element or XPath root expression.
            :type root: object
            :param parent: Parent element used for cache invalidation or selector traversal.
            :type parent: object
            :param attr_converter: Optional callable that converts the serialized attribute mapping.
            :type attr_converter: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @classmethod
        def _prettyify(cls, current, *, indent, riffle, parent=None, index=-1, depth=0):
            """
            **LLM Docstring**

            Recursively inject indentation and line breaks into an `ElementTree` node in place.

            :param current: Current `ElementTree` node being indented.
            :type current: object
            :param indent: Indentation string.
            :type indent: object
            :param riffle: Text inserted between serialized fragments or lines.
            :type riffle: object
            :param parent: Parent element used for cache invalidation or selector traversal.
            :type parent: object
            :param index: Position of the current node within its parent.
            :type index: object
            :param depth: Current recursion depth.
            :type depth: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...
        default_indent = '  '
        default_newline = '\n'

        def tostring(self, attr_converter=None, indent=None, method='html', riffle=True, prettify=False, write_string=None, **base_etree_opts):
            """
            **LLM Docstring**

            Serialize the element, optionally pretty-printing or riffle-joining fragments, then restore raw HTML sentinels.

            :param attr_converter: Optional callable that converts the serialized attribute mapping.
            :type attr_converter: object
            :param indent: Indentation string.
            :type indent: object
            :param method: Serialization method passed to `ElementTree`.
            :type method: object
            :param riffle: Text inserted between serialized fragments or lines.
            :type riffle: object
            :param prettify: Whether to run the custom recursive pretty-printer.
            :type prettify: object
            :param write_string: Optional final serialization callable.
            :type write_string: object
            :param base_etree_opts: Additional keyword arguments passed to `ElementTree` serialization.
            :type base_etree_opts: dict

            :return: The generated string representation.
            :rtype: str
            """
            ...

        def sanitize_key(self, key):
            """
            **LLM Docstring**

            Convert an HTML attribute name into the Python keyword-safe spelling used by constructor representations.

            :param key: The update category or mapping key.
            :type key: object

            :return: The generated string representation.
            :rtype: str
            """
            ...

        def format(self, padding='', prefix='', linewidth=100):
            """
            **LLM Docstring**

            Build a reconstructible constructor-style representation, switching to multiline output when it exceeds the requested width.

            :param padding: Indentation prefix used in the generated constructor representation.
            :type padding: object
            :param prefix: Prefix added to the generated class name.
            :type prefix: object
            :param linewidth: Maximum preferred output width before switching to multiline formatting.
            :type linewidth: object

            :return: The generated string representation.
            :rtype: str
            """
            ...

        def dump(self, prefix='', linewidth=80):
            """
            **LLM Docstring**

            Print the constructor-style representation.

            :param prefix: Prefix added to the generated class name.
            :type prefix: object
            :param linewidth: Maximum preferred output width before switching to multiline formatting.
            :type linewidth: object

            :return: No value is returned.
            :rtype: None
            """
            ...

        def write(self, file, **opts):
            """
            **LLM Docstring**

            Serialize the element and write it to a path or writable stream.

            :param file: Path or writable stream receiving serialized content.
            :type file: object
            :param opts: Additional options forwarded to the underlying operation.
            :type opts: dict

            :return: No value is returned.
            :rtype: None
            """
            ...
        MAX_REPR_LENGTH = 1000

        def __repr__(self):
            """
            **LLM Docstring**

            Return a bounded-length representation containing the element type, children, and attributes.

            :return: The generated string representation.
            :rtype: str
            """
            ...

        def _repr_html_(self):
            """
            **LLM Docstring**

            Return the HTML serialization used by notebook rich display.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def _ipython_display_(self):
            """
            **LLM Docstring**

            Display the element using the environment-sensitive display method.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def get_display_element(self):
            """
            **LLM Docstring**

            Wrap the element in a `div.jhtml` display container.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def get_mime_bundle(self):
            """
            **LLM Docstring**

            Build a `text/html` MIME bundle for notebook display.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @classmethod
        def _cross_plat_open(cls, file, delay=5):
            """
            **LLM Docstring**

            Open a file with the platform’s default application and keep it alive for the requested delay.

            :param file: Path or writable stream receiving serialized content.
            :type file: object
            :param delay: Seconds to keep the temporary browser file available after opening it.
            :type delay: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @classmethod
        def display_in_browser_from_wrapper(cls, wrapper):
            """
            **LLM Docstring**

            Write a wrapper to a temporary HTML file and open it in the default browser.

            :param wrapper: Element wrapper to display.
            :type wrapper: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def display_in_browser(self):
            """
            **LLM Docstring**

            Ensure the element is wrapped in `body` and `html` tags before browser display.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @classmethod
        def display_ipython_from_wrapper(self, wrapper):
            """
            **LLM Docstring**

            Render a wrapper through IPython’s HTML display object.

            :param wrapper: Element wrapper to display.
            :type wrapper: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def display_ipython(self):
            """
            **LLM Docstring**

            Display the element’s standard display wrapper in IPython.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def display(self):
            """
            **LLM Docstring**

            Choose IPython display in Jupyter and browser display otherwise.

            :return: No value is returned.
            :rtype: None
            """
            ...

        @mixedmethod
        def _ipython_pinfo_(self):
            """
            **LLM Docstring**

            Delegate rich object inspection to the project documentation helper.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def validate_props(self, **kwargs):
            """
            **LLM Docstring**

            Validate the element’s stored attributes using the manager validator mapping.

            :param kwargs: Additional attributes or options forwarded to the constructed element.
            :type kwargs: dict

            :return: Validation errors found by the check, or an empty list when the value is accepted.
            :rtype: list[ValidationError]
            """
            ...

        def make_class_list(self):
            """
            **LLM Docstring**

            Split a string-valued `class` attribute into a list in place.

            :return: No value is returned.
            :rtype: None
            """
            ...

        def add_class(self, *cls, copy=True):
            """
            **LLM Docstring**

            Return an element with the requested classes added.

            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            :param cls: The class performing the operation.
            :type cls: tuple

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def remove_class(self, *cls, copy=True):
            """
            **LLM Docstring**

            Return an element with the requested classes removed.

            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            :param cls: The class performing the operation.
            :type cls: tuple

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def add_styles(self, copy=True, **sty):
            """
            **LLM Docstring**

            Return an element with the requested inline styles merged.

            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            :param sty: A CSS declaration string or complete rule block.
            :type sty: dict

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def remove_styles(self, copy=True, **sty):
            """
            **LLM Docstring**

            Return an element with the requested inline styles removed.

            :param copy: Whether modifications should operate on a copy.
            :type copy: object
            :param sty: A CSS declaration string or complete rule block.
            :type sty: dict

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...

        def _find_child_node(self, etree):
            """
            **LLM Docstring**

            Breadth-first search the wrapped element hierarchy for the object corresponding to an `ElementTree` node.

            :param etree: The `ElementTree` element to convert.
            :type etree: object

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def find(self, path, find_element=True):
            """
            **LLM Docstring**

            Run an XPath search and optionally map the result back to its wrapped element.

            :param path: ElementTree-compatible XPath expression.
            :type path: str
            :param find_element: Whether matching tree nodes should be mapped back to their `XMLElement` objects.
            :type find_element: object

            :return: The value produced by the implemented operation.
            :rtype: object | None
            """
            ...

        def findall(self, path, find_element=True):
            """
            **LLM Docstring**

            Run an XPath search for all matches and optionally map each result back to its wrapped element.

            :param path: ElementTree-compatible XPath expression.
            :type path: str
            :param find_element: Whether matching tree nodes should be mapped back to their `XMLElement` objects.
            :type find_element: object

            :return: The value produced by the implemented operation.
            :rtype: list
            """
            ...

        def iterfind(self, path, find_element=True):
            """
            **LLM Docstring**

            Iterate XPath matches and optionally map each result back to its wrapped element.

            :param path: ElementTree-compatible XPath expression.
            :type path: str
            :param find_element: Whether matching tree nodes should be mapped back to their `XMLElement` objects.
            :type find_element: object

            :return: An iterator or view over the requested values.
            :rtype: iterator
            """
            ...

        def _build_single_selector(self, root='.//', node_type='*', parents=None, **attrs):
            """
            **LLM Docstring**

            Construct one ElementTree XPath selector from a root, tag, attribute constraints, and parent traversal count.

            :param root: Destination root element or XPath root expression.
            :type root: object
            :param node_type: Element tag used in a generated XPath selector.
            :type node_type: object
            :param parents: Number of parent traversals appended to the selector.
            :type parents: object
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict

            :return: The generated string representation.
            :rtype: str
            """
            ...

        def _build_xpath_selector(self, root='.//', node_type='*', parents=None, **attrs):
            """
            **LLM Docstring**

            Expand iterable selector arguments into a union of concrete XPath selectors.

            :param root: Destination root element or XPath root expression.
            :type root: object
            :param node_type: Element tag used in a generated XPath selector.
            :type node_type: object
            :param parents: Number of parent traversals appended to the selector.
            :type parents: object
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict

            :return: The generated string representation.
            :rtype: str
            """
            ...

        def find_by_id(self, id, mode='first', parent=None, find_element=True):
            """
            **LLM Docstring**

            Search for an element with a given `id` using first, all, or iterator mode.

            :param id: Optional element identifier.
            :type id: object
            :param mode: The operation mode or compositing mode.
            :type mode: str
            :param parent: Parent element used for cache invalidation or selector traversal.
            :type parent: object
            :param find_element: Whether matching tree nodes should be mapped back to their `XMLElement` objects.
            :type find_element: bool

            :return: The value produced by the implemented operation.
            :rtype: object | None
            """
            ...

        def find_by_attributes(self, *, root='.//', node_type='*', parents=None, mode='first', find_element=True, **attrs):
            """
            **LLM Docstring**

            Build an attribute selector and dispatch to first, all, or iterator search mode.

            :param root: Destination root element or XPath root expression.
            :type root: object
            :param node_type: Element tag used in a generated XPath selector.
            :type node_type: object
            :param parents: Number of parent traversals appended to the selector.
            :type parents: object
            :param mode: The operation mode or compositing mode.
            :type mode: object
            :param find_element: Whether matching tree nodes should be mapped back to their `XMLElement` objects.
            :type find_element: object
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict

            :return: The value produced by the implemented operation.
            :rtype: object | None
            """
            ...

        def build_selector(self, *dicts, **attrs):
            """
            **LLM Docstring**

            Build a selector from keyword constraints or chain multiple selector dictionaries.

            :param dicts: Sequential selector specifications.
            :type dicts: tuple
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def copy(self):
            """
            **LLM Docstring**

            Shallow-copy the element, copy its attributes, and reset parent and tree caches.

            :return: The value produced by the implemented operation.
            :rtype: HTML.XMLElement
            """
            ...
    base_element = XMLElement

    class RawHTML(XMLElement):
        """
        Not a properly constructed subclass, but inserted as part of the
        type hierarchy for explicit isintance check purposes, should have a
        trait-style base class but too much work now
        """

        def __init__(self, text, id=None):
            """
            **LLM Docstring**

            Store an opaque HTML fragment with a unique replacement identifier.

            :param text: Raw HTML or CDATA text.
            :type text: object
            :param id: Optional element identifier.
            :type id: object
            """
            ...

        def tostring(self, **opts):
            """
            **LLM Docstring**

            Return the raw fragment unchanged.

            :param opts: Additional options forwarded to the underlying operation.
            :type opts: dict

            :return: The generated string representation.
            :rtype: str
            """
            ...

        def display(self):
            """
            **LLM Docstring**

            Choose IPython or browser display for the raw fragment.

            :return: No value is returned.
            :rtype: None
            """
            ...

        def display_in_browser(self):
            """
            **LLM Docstring**

            Display the raw fragment through the shared temporary-browser helper.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def display_ipython(self):
            """
            **LLM Docstring**

            Display the raw fragment through the shared IPython helper.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def _repr_html_(self):
            """
            **LLM Docstring**

            Return the raw fragment for notebook display.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def _ipython_display_(self):
            """
            **LLM Docstring**

            Display the raw fragment.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def get_display_element(self):
            """
            **LLM Docstring**

            Wrap the raw fragment in a `div.jhtml` container.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def dump(self, prefix='', linewidth=80):
            """
            **LLM Docstring**

            Print the raw fragment.

            :param prefix: Prefix added to the generated class name.
            :type prefix: object
            :param linewidth: Maximum preferred output width before switching to multiline formatting.
            :type linewidth: object

            :return: No value is returned.
            :rtype: None
            """
            ...

        def write(self, file, **opts):
            """
            **LLM Docstring**

            Write the raw fragment to a path or writable stream.

            :param file: Path or writable stream receiving serialized content.
            :type file: object
            :param opts: Additional options forwarded to the underlying operation.
            :type opts: dict

            :return: No value is returned.
            :rtype: None
            """
            ...

    class CDATA(RawHTML):

        def __init__(self, text, id=None):
            """
            **LLM Docstring**

            Wrap text in a CDATA section and initialize it as raw HTML.

            :param text: Raw HTML or CDATA text.
            :type text: object
            :param id: Optional element identifier.
            :type id: object
            """
            ...

    class Comment(XMLElement):

        def __init__(self, *elems, **attrs):
            """
            **LLM Docstring**

            Construct an `ElementTree.Comment` wrapper from the supplied content and attributes.

            :param elems: Child elements or text content.
            :type elems: tuple
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict
            """
            ...

    class TagElement(XMLElement):
        tag = None

        def __init__(self, *elems, **attrs):
            """
            **LLM Docstring**

            Construct the fixed-tag element from children and attributes.

            :param elems: Child elements or text content.
            :type elems: tuple
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict
            """
            ...

        def __call__(self, *elems, **kwargs):
            """
            **LLM Docstring**

            Clone the fixed-tag element with appended children and merged attributes.

            :param elems: Child elements or text content.
            :type elems: tuple
            :param kwargs: Additional attributes or options forwarded to the constructed element.
            :type kwargs: dict

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

    class Nav(TagElement):
        tag = 'nav'

    class Anchor(TagElement):
        tag = 'a'

    class Text(TagElement):
        tag = 'p'

    class Div(TagElement):
        tag = 'div'

    class Heading(TagElement):
        tag = 'h1'

    class SubHeading(TagElement):
        tag = 'h2'

    class SubsubHeading(TagElement):
        tag = 'h3'

    class SubsubsubHeading(TagElement):
        tag = 'h4'

    class SubHeading5(TagElement):
        tag = 'h5'

    class SubHeading6(TagElement):
        tag = 'h6'

    class Small(TagElement):
        tag = 'small'

    class Bold(TagElement):
        tag = 'b'

    class Italic(TagElement):
        tag = 'i'

    class Image(TagElement):
        tag = 'img'

    @classmethod
    def image_from_string(cls, image_string: bytes | str, format='image/png', **styles):
        """
        **LLM Docstring**

        Create an `<img>` element whose source is a base64 data URI, encoding byte input when necessary.

        :param image_string: Raw image bytes or an already base64-encoded string.
        :type image_string: bytes | str
        :param format: MIME type used in the generated data URI.
        :type format: object
        :param styles: Style values to apply.
        :type styles: dict

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

    class ListItem(TagElement):
        tag = 'li'

    class BaseList(TagElement):

        def __init__(self, *elems, item_attributes=None, **attrs):
            """
            **LLM Docstring**

            Initialize a list container; `item_attributes` is accepted but the current implementation does not apply it to children.

            :param item_attributes: Attributes intended for generated list items; currently retained only for API compatibility.
            :type item_attributes: object
            :param elems: Child elements or text content.
            :type elems: tuple
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict
            """
            ...

    class List(BaseList):
        tag = 'ul'

    class NumberedList(BaseList):
        tag = 'ol'

    class Pre(TagElement):
        tag = 'pre'

    class Style(TagElement):
        tag = 'style'

    class Script(TagElement):
        tag = 'script'

    class Span(TagElement):
        tag = 'span'

    class Button(TagElement):
        tag = 'button'

    class TableRow(TagElement):
        tag = 'tr'

    class TableHeading(TagElement):
        tag = 'th'

    class TableHeader(TagElement):
        tag = 'thead'

    class TableFooter(TagElement):
        tag = 'tfoot'

    class TableBody(TagElement):
        tag = 'tbody'

    class TableItem(TagElement):
        tag = 'td'

    class Table(TagElement):
        tag = 'table'

        def __init__(self, *rows, headers=None, **attrs):
            """
            **LLM Docstring**

            Normalize rows and optional headers into `TableRow`, `TableItem`, and `TableHeading` wrappers before constructing the table.

            :param headers: Optional header row.
            :type headers: object
            :param rows: Rows used to construct the table.
            :type rows: tuple
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict
            """
            ...

    class Canvas(TagElement):
        tag = 'canvas'
    A = Anchor

    class Abbr(TagElement):
        tag = 'abbr'

    class Address(TagElement):
        tag = 'address'

    class Area(TagElement):
        tag = 'area'

    class Article(TagElement):
        tag = 'article'

    class Aside(TagElement):
        tag = 'aside'

    class Audio(TagElement):
        tag = 'audio'

    class B(TagElement):
        tag = 'b'

    class Base(TagElement):
        tag = 'base'

    class Bdi(TagElement):
        tag = 'bdi'

    class Bdo(TagElement):
        tag = 'bdo'

    class Blockquote(TagElement):
        tag = 'blockquote'

    class Body(TagElement):
        tag = 'body'

    class Br(TagElement):
        tag = 'br'

    class Caption(TagElement):
        tag = 'caption'

    class Cite(TagElement):
        tag = 'cite'

    class Code(TagElement):
        tag = 'code'

    class Col(TagElement):
        tag = 'col'

    class Colgroup(TagElement):
        tag = 'colgroup'

    class Data(TagElement):
        tag = 'data'

    class Datalist(TagElement):
        tag = 'datalist'

    class Dd(TagElement):
        tag = 'dd'

    class Del(TagElement):
        tag = 'del'

    class Details(TagElement):
        tag = 'details'

    class Dfn(TagElement):
        tag = 'dfn'

    class Dialog(TagElement):
        tag = 'dialog'

    class Dl(TagElement):
        tag = 'dl'

    class Dt(TagElement):
        tag = 'dt'

    class Em(TagElement):
        tag = 'em'

    class Embed(TagElement):
        tag = 'embed'

    class Fieldset(TagElement):
        tag = 'fieldset'

    class Figcaption(TagElement):
        tag = 'figcaption'

    class Figure(TagElement):
        tag = 'figure'

    class Footer(TagElement):
        tag = 'footer'

    class Form(TagElement):
        tag = 'form'

    class Head(TagElement):
        tag = 'head'

    class Header(TagElement):
        tag = 'header'

    class Hr(TagElement):
        tag = 'hr'

    class Html(TagElement):
        tag = 'html'
    i = Italic

    class Iframe(TagElement):
        tag = 'iframe'
    Img = Image

    class Inline(TagElement):
        tag = 'inline'

    class Input(TagElement):
        tag = 'input'

    class Ins(TagElement):
        tag = 'ins'

    class Kbd(TagElement):
        tag = 'kbd'

    class Label(TagElement):
        tag = 'label'

    class Legend(TagElement):
        tag = 'legend'
    Li = ListItem

    class Link(TagElement):
        tag = 'link'

    class Main(TagElement):
        tag = 'main'

    class Map(TagElement):
        tag = 'map'

    class Mark(TagElement):
        tag = 'mark'

    class Meta(TagElement):
        tag = 'meta'

    class Meter(TagElement):
        tag = 'meter'

    class Noscript(TagElement):
        tag = 'noscript'

    class Object(TagElement):
        tag = 'object'
    Ol = NumberedList
    P = Text

    class Optgroup(TagElement):
        tag = 'optgroup'

    class Option(TagElement):
        tag = 'option'

    class Output(TagElement):
        tag = 'output'

    class Param(TagElement):
        tag = 'param'

    class Picture(TagElement):
        tag = 'picture'

    class Progress(TagElement):
        tag = 'progress'

    class Q(TagElement):
        tag = 'q'

    class Rp(TagElement):
        tag = 'rp'

    class Rt(TagElement):
        tag = 'rt'

    class Ruby(TagElement):
        tag = 'ruby'

    class S(TagElement):
        tag = 's'

    class Samp(TagElement):
        tag = 'samp'

    class Section(TagElement):
        tag = 'section'

    class Select(TagElement):
        tag = 'select'

    class Source(TagElement):
        tag = 'source'

    class Strong(TagElement):
        tag = 'strong'

    class Sub(TagElement):
        tag = 'sub'

    class Summary(TagElement):
        tag = 'summary'

    class Sup(TagElement):
        tag = 'sup'

    class Svg(TagElement):
        tag = 'svg'
    Tbody = TableBody
    Td = TableItem

    class Template(TagElement):
        tag = 'template'

    class Textarea(TagElement):
        tag = 'textarea'
    Tfoot = TableFooter
    Th = TableHeading
    Thead = TableHeader

    class Time(TagElement):
        tag = 'time'

    class Title(TagElement):
        tag = 'title'
    Tr = TableRow

    class Track(TagElement):
        tag = 'track'

    class U(TagElement):
        tag = 'u'
    Ul = List

    class Var(TagElement):
        tag = 'var'

    class Video(TagElement):
        tag = 'video'

    class Wbr(TagElement):
        tag = 'wbr'

class ContentXML(XMLBase):

    class Element(HTML.XMLElement):
        ignored_styles = CSS.known_properties

        def get_display_element(self):
            """
            **LLM Docstring**

            Wrap XML serialization in a preformatted HTML display element.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def tostring(self, method='xml', prettify=True, **opts):
            """
            **LLM Docstring**

            Serialize content as prettified XML by default.

            :param method: Serialization method passed to `ElementTree`.
            :type method: object
            :param prettify: Whether to run the custom recursive pretty-printer.
            :type prettify: object
            :param opts: Additional options forwarded to the underlying operation.
            :type opts: dict

            :return: The generated string representation.
            :rtype: str
            """
            ...
    base_element = Element

    class TagElement(Element):
        tag = None

        def __init__(self, *elems, **attrs):
            """
            **LLM Docstring**

            Construct the fixed-tag element from children and attributes.

            :param elems: Child elements or text content.
            :type elems: tuple
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict
            """
            ...

        def __call__(self, *elems, **kwargs):
            """
            **LLM Docstring**

            Clone the fixed-tag element with appended children and merged attributes.

            :param elems: Child elements or text content.
            :type elems: tuple
            :param kwargs: Additional attributes or options forwarded to the constructed element.
            :type kwargs: dict

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

    class DeclarativeElement(TagElement):

        def __init__(self, *elems, **attrs):
            """
            **LLM Docstring**

            Use the subclass name as the XML tag before constructing the declarative element.

            :param elems: Child elements or text content.
            :type elems: tuple
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict
            """
            ...

    class Comment(HTML.Comment):
        ...

    class PrefixedElement(Element):
        prefix = None

        def __init__(self, base_tag, *elems, **attrs):
            """
            **LLM Docstring**

            Construct or clone an XML element whose tag is formed by prepending the class prefix to a stored base tag.

            :param base_tag: Unprefixed XML element name.
            :type base_tag: object
            :param elems: Child elements or text content.
            :type elems: tuple
            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict
            """
            ...

        def __call__(self, *elems, **kwargs):
            """
            **LLM Docstring**

            Construct or clone an XML element whose tag is formed by prepending the class prefix to a stored base tag.

            :param elems: Child elements or text content.
            :type elems: tuple
            :param kwargs: Additional attributes or options forwarded to the constructed element.
            :type kwargs: dict

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...
"COMMON_PRESENTATION data omitted from this build (23 keys: ['fill', 'fill-opacity', 'fill-rule', 'stroke', 'stroke-width', 'stroke-opacity', 'stroke-linecap', 'stroke-linejoin', 'stroke-miterlimit', 'stroke-dasharray', 'stroke-dashoffset', 'opacity', 'visibility', 'display', 'color', 'paint-order', 'clip-path', 'mask', 'filter', 'transform', 'pointer-events', 'cursor', 'vector-effect'])"
COMMON_ALL = COMMON_PRESENTATION | COMMON_TEXT_PRESENTATION

class SVG(HTML):
    COMMON_PRESENTATION = COMMON_PRESENTATION
    COMMON_ALL = COMMON_ALL
    COMMON_TEXT_PRESENTATION = COMMON_TEXT_PRESENTATION
    _class_map = None

    @classmethod
    def get_class_map(cls):
        """
        **LLM Docstring**

        Lazily build and cache the SVG tag-to-wrapper-class mapping.

        :return: The value produced by the implemented operation.
        :rtype: object
        """
        ...

    class TagElement(HTML.TagElement):
        tag = None
        required: dict
        optional: dict
        display_opts: dict
        ignored_styles = {'height', 'width', 'position', 'color'}
        can_be_dynamic = False

        @classmethod
        def get_class_map_updates(cls):
            """
            **LLM Docstring**

            Return the complete SVG class map for temporary expansion during conversion.

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        @classmethod
        def convert_attrs(cls, attrs: dict):
            """
            **LLM Docstring**

            Copy and stringify non-string SVG attributes, flattening arrays and iterables and omitting `None` values.

            :param attrs: Attribute values to normalize or apply.
            :type attrs: dict

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...
        attr_converter = convert_attrs

        def validate(self, **kwargs):
            """
            **LLM Docstring**

            Check required SVG attributes and then validate presentation properties; the current required-key difference is computed in the implemented direction.

            :param kwargs: Additional attributes or options forwarded to the constructed element.
            :type kwargs: dict

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

        def __call__(self, *elems, **kwargs):
            """
            **LLM Docstring**

            Clone the SVG element with appended children and merged attributes.

            :param elems: Child elements or text content.
            :type elems: tuple
            :param kwargs: Additional attributes or options forwarded to the constructed element.
            :type kwargs: dict

            :return: The value produced by the implemented operation.
            :rtype: object
            """
            ...

    class Svg(TagElement):
        """Root element. Always set viewBox for responsive sizing."""
        tag = 'svg'
        required = {'xmlns': str, 'width': str, 'height': str}
        optional = {'viewBox': None, 'preserveAspectRatio': str, 'version': str, 'x': numbers.Number, 'y': numbers.Number}
        styles = ['transform', 'overflow']

        def __init__(self, *elems, xmlns='http://www.w3.org/2000/svg', width='100%', height='auto', **kwargs):
            """
           **LLM Docstring**

           Construct a root SVG element and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param xmlns: The SVG XML namespace URI.
           :type xmlns: object
           :param width: The element width or width-like SVG attribute.
           :type width: object
           :param height: The element height or height-like SVG attribute.
           :type height: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class G(TagElement):
        """Group element. Inherits presentation attrs to all children."""
        tag = 'g'
        required = {}
        optional = {'id': None, 'transform': None}
        styles = COMMON_PRESENTATION

        def __init__(self, *elems, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG group and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Defs(TagElement):
        """Container for reusable definitions (markers, gradients, etc.)."""
        tag = 'defs'
        required = {}
        optional = {'id': None}
        styles = []

        def __init__(self, *elems, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG definitions container and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Symbol(TagElement):
        """Reusable graphic referenced via <use>. Not rendered directly."""
        tag = 'symbol'
        required = {'id': None}
        optional = {'viewBox': None, 'preserveAspectRatio': str, 'x': numbers.Number, 'y': numbers.Number, 'width': None, 'height': None}
        styles = COMMON_PRESENTATION

        def __init__(self, *elems, id=None, **kwargs):
            """
           **LLM Docstring**

           Construct a reusable SVG symbol and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param id: Optional element identifier.
           :type id: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Use(TagElement):
        """Instantiates a <symbol> or any element by id."""
        tag = 'use'
        required = {'href': None}
        optional = {'x': numbers.Number, 'y': numbers.Number, 'width': None, 'height': None}
        styles = COMMON_PRESENTATION

        def __init__(self, *elems, href=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG use reference and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param href: The referenced resource or element identifier.
           :type href: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Rect(TagElement):
        """Axis-aligned rectangle. rx/ry round the corners."""
        tag = 'rect'
        required = {'x': numbers.Number, 'y': numbers.Number, 'width': None, 'height': None}
        optional = {'rx': numbers.Number, 'ry': numbers.Number}
        styles = COMMON_PRESENTATION

        def __init__(self, *elems, x=0, y=0, width=None, height=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG rectangle and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param x: The x coordinate.
           :type x: object
           :param y: The y coordinate.
           :type y: object
           :param width: The element width or width-like SVG attribute.
           :type width: object
           :param height: The element height or height-like SVG attribute.
           :type height: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Circle(TagElement):
        """Circle defined by centre (cx, cy) and radius r."""
        tag = 'circle'
        required = {'cx': numbers.Number, 'cy': numbers.Number, 'r': None}
        optional = {}
        styles = COMMON_PRESENTATION

        def __init__(self, *elems, cx=0, cy=0, r=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG circle and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param cx: The center x coordinate.
           :type cx: object
           :param cy: The center y coordinate.
           :type cy: object
           :param r: The circle radius.
           :type r: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Ellipse(TagElement):
        """Ellipse with independent x- and y-radii."""
        tag = 'ellipse'
        required = {'cx': numbers.Number, 'cy': numbers.Number, 'rx': None, 'ry': None}
        optional = {}
        styles = COMMON_PRESENTATION

        def __init__(self, *elems, cx=0, cy=0, rx=None, ry=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG ellipse and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param cx: The center x coordinate.
           :type cx: object
           :param cy: The center y coordinate.
           :type cy: object
           :param rx: The horizontal radius or corner radius.
           :type rx: object
           :param ry: The vertical radius or corner radius.
           :type ry: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Line(TagElement):
        """Straight line. stroke must be set; fill has no effect."""
        tag = 'line'
        required = {'x1': numbers.Number, 'y1': numbers.Number, 'x2': numbers.Number, 'y2': numbers.Number}
        optional = {'marker-start': None, 'marker-mid': None, 'marker-end': None}
        styles = COMMON_PRESENTATION

        def __init__(self, *elems, x1=0, y1=0, x2=0, y2=0, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG line and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param x1: The first x coordinate.
           :type x1: object
           :param y1: The first y coordinate.
           :type y1: object
           :param x2: The second x coordinate.
           :type x2: object
           :param y2: The second y coordinate.
           :type y2: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Polyline(TagElement):
        """Open polygon (not closed). Use fill='none' for pure outline."""
        tag = 'polyline'
        required = {'points': None}
        optional = {'marker-start': None, 'marker-mid': None, 'marker-end': None}
        styles = COMMON_PRESENTATION

        def __init__(self, *elems, points=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG polyline and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param points: Coordinate sequence for the SVG shape.
           :type points: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Polygon(TagElement):
        """Closed polygon. Last point auto-connects to first."""
        tag = 'polygon'
        required = {'points': None}
        optional = {'marker-start': None, 'marker-mid': None, 'marker-end': None}
        styles = COMMON_PRESENTATION

        def __init__(self, *elems, points=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG polygon and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param points: Coordinate sequence for the SVG shape.
           :type points: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Path(TagElement):
        """Most versatile shape. Path commands: M/m (move), L/l (line), H/h (horiz), V/v (vert), C/c (cubic bezier), S/s (smooth cubic), Q/q (quadratic), T/t (smooth quad), A/a (arc), Z/z (close)."""
        tag = 'path'
        required = {'d': None}
        optional = {'pathLength': None, 'marker-start': None, 'marker-mid': None, 'marker-end': None}
        styles = COMMON_PRESENTATION

        def __init__(self, *elems, d=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG path and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param d: The SVG path-data string.
           :type d: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Text(TagElement):
        """Text element. Contains plain text or <tspan> children."""
        tag = 'text'
        required = {'x': numbers.Number, 'y': numbers.Number}
        optional = {'dx': numbers.Number, 'dy': numbers.Number, 'rotate': None, 'textLength': None, 'lengthAdjust': str}
        styles = COMMON_ALL

        def __init__(self, *elems, x=0, y=0, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG text element and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param x: The x coordinate.
           :type x: object
           :param y: The y coordinate.
           :type y: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Tspan(TagElement):
        """Inline text span; child of <text>. Use dy='1.2em' for line breaks."""
        tag = 'tspan'
        required = {}
        optional = {'x': None, 'y': None, 'dx': None, 'dy': None, 'rotate': None, 'textLength': None, 'lengthAdjust': str}
        styles = COMMON_ALL

        def __init__(self, *elems, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG text span and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Textpath(TagElement):
        """Renders text along a <path>."""
        tag = 'textPath'
        required = {'href': None}
        optional = {'startOffset': str, 'method': str, 'spacing': str, 'side': str}
        styles = COMMON_ALL

        def __init__(self, *elems, href=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG text-path element and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param href: The referenced resource or element identifier.
           :type href: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Image(TagElement):
        """Embeds a raster or SVG image."""
        tag = 'image'
        required = {'href': None, 'x': numbers.Number, 'y': numbers.Number, 'width': None, 'height': None}
        optional = {'preserveAspectRatio': str, 'crossorigin': None, 'decoding': str, 'image-rendering': str}
        styles = ['opacity', 'transform', 'clip-path', 'mask', 'filter']

        def __init__(self, *elems, href=None, x=0, y=0, width=None, height=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG image element and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param href: The referenced resource or element identifier.
           :type href: object
           :param x: The x coordinate.
           :type x: object
           :param y: The y coordinate.
           :type y: object
           :param width: The element width or width-like SVG attribute.
           :type width: object
           :param height: The element height or height-like SVG attribute.
           :type height: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Foreignobject(TagElement):
        """Embeds arbitrary XML (e.g. HTML) inside SVG."""
        tag = 'foreignObject'
        required = {'x': numbers.Number, 'y': numbers.Number, 'width': None, 'height': None}
        optional = {}
        styles = ['opacity', 'transform', 'clip-path', 'mask']

        def __init__(self, *elems, x=0, y=0, width=None, height=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG foreign-object element and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param x: The x coordinate.
           :type x: object
           :param y: The y coordinate.
           :type y: object
           :param width: The element width or width-like SVG attribute.
           :type width: object
           :param height: The element height or height-like SVG attribute.
           :type height: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Lineargradient(TagElement):
        """Define with <stop> children; apply via fill='url(#id)'."""
        tag = 'linearGradient'
        required = {'id': None}
        styles = []

        def __init__(self, *elems, id=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG linear gradient and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param id: Optional element identifier.
           :type id: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Radialgradient(TagElement):
        """Radial gradient. fx/fy shift the highlight off-centre."""
        tag = 'radialGradient'
        required = {'id': None}
        styles = []

        def __init__(self, *elems, id=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG radial gradient and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param id: Optional element identifier.
           :type id: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Stop(TagElement):
        """Colour stop inside a gradient. Always set stop-color."""
        tag = 'stop'
        required = {'offset': None}
        optional = {'stop-color': str, 'stop-opacity': numbers.Number}
        styles = []

        def __init__(self, *elems, offset=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG gradient stop and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param offset: The gradient-stop or animation offset.
           :type offset: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Pattern(TagElement):
        """Tiling pattern paint server. Apply via fill='url(#id)'."""
        tag = 'pattern'
        required = {'id': None, 'width': None, 'height': None}
        styles = []

        def __init__(self, *elems, id=None, width=None, height=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG pattern and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param id: Optional element identifier.
           :type id: object
           :param width: The element width or width-like SVG attribute.
           :type width: object
           :param height: The element height or height-like SVG attribute.
           :type height: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Clippath(TagElement):
        """Hard clip. Apply via clip-path='url(#id)' on the target."""
        tag = 'clipPath'
        required = {'id': None}
        optional = {'clipPathUnits': str, 'transform': None}
        styles = []

        def __init__(self, *elems, id=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG clip path and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param id: Optional element identifier.
           :type id: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Mask(TagElement):
        """Luminance mask (white=visible, black=hidden). Apply via mask='url(#id)'."""
        tag = 'mask'
        required = {'id': None}
        optional = {'x': str, 'y': str, 'width': str, 'height': str, 'maskUnits': str, 'maskContentUnits': str}
        styles = []

        def __init__(self, *elems, id=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG mask and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param id: Optional element identifier.
           :type id: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Marker(TagElement):
        """Arrowhead / endpoint decoration. orient='auto-start-reverse' flips for start markers automatically."""
        tag = 'marker'
        optional = {'orient': str, 'markerUnits': str, 'preserveAspectRatio': str}
        styles = COMMON_PRESENTATION

        def __init__(self, *elems, id=None, viewBox='0 0 10 10', refX=5, refY=5, markerWidth=6, markerHeight=6, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG marker and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param id: Optional element identifier.
           :type id: object
           :param viewBox: The SVG view-box specification.
           :type viewBox: object
           :param refX: The marker reference x coordinate.
           :type refX: object
           :param refY: The marker reference y coordinate.
           :type refY: object
           :param markerWidth: The rendered marker width.
           :type markerWidth: object
           :param markerHeight: The rendered marker height.
           :type markerHeight: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Filter(TagElement):
        """Container for filter primitives. Apply via filter='url(#id)'."""
        tag = 'filter'
        required = {'id': None}
        styles = []

        def __init__(self, *elems, id=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG filter container and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param id: Optional element identifier.
           :type id: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Fegaussianblur(TagElement):
        """Gaussian blur. stdDeviation='x y' for asymmetric blur."""
        tag = 'feGaussianBlur'
        required = {'stdDeviation': None}
        optional = {'in': str, 'result': None, 'edgeMode': str}
        styles = []

        def __init__(self, *elems, stdDeviation=None, **kwargs):
            """
           **LLM Docstring**

           Construct a Gaussian-blur filter primitive and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param stdDeviation: The Gaussian blur standard deviation.
           :type stdDeviation: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Fecolormatrix(TagElement):
        """Colour transform. type='saturate' values='0' → grayscale."""
        tag = 'feColorMatrix'
        required = {'type': str}
        optional = {'in': str, 'result': None, 'values': None}
        styles = []

        def __init__(self, *elems, type='matrix', **kwargs):
            """
           **LLM Docstring**

           Construct a color-matrix filter primitive and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param type: The SVG operation or animation type.
           :type type: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Feblend(TagElement):
        """Composites two inputs using a blend mode."""
        tag = 'feBlend'
        required = {'in': str, 'in2': str}
        optional = {'mode': str, 'result': None}
        styles = []

        def __init__(self, *elems, in_='SourceGraphic', in2='BackgroundImage', **kwargs):
            """
           **LLM Docstring**

           Construct a blend filter primitive and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param in_: The primary SVG filter input; the trailing underscore avoids Python’s `in` keyword.
           :type in_: object
           :param in2: The secondary SVG filter input.
           :type in2: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Fecomposite(TagElement):
        """Alpha compositing of two filter inputs."""
        tag = 'feComposite'
        required = {'in': str, 'in2': str}
        styles = []

        def __init__(self, *elems, in_='SourceGraphic', in2='SourceGraphic', **kwargs):
            """
           **LLM Docstring**

           Construct a composite filter primitive and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param in_: The primary SVG filter input; the trailing underscore avoids Python’s `in` keyword.
           :type in_: object
           :param in2: The secondary SVG filter input.
           :type in2: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Feoffset(TagElement):
        """Shifts its input. Combine with feGaussianBlur for drop shadows."""
        tag = 'feOffset'
        required = {'dx': numbers.Number, 'dy': numbers.Number}
        optional = {'in': str, 'result': None}
        styles = []

        def __init__(self, *elems, dx=0, dy=0, **kwargs):
            """
           **LLM Docstring**

           Construct a offset filter primitive and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param dx: The horizontal offset.
           :type dx: object
           :param dy: The vertical offset.
           :type dy: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Femerge(TagElement):
        """Combines multiple filter results. Children are <feMergeNode in_='…'>."""
        tag = 'feMerge'
        required = {}
        optional = {'result': None}
        styles = []

        def __init__(self, *elems, **kwargs):
            """
           **LLM Docstring**

           Construct a merge filter primitive and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Femergenode(TagElement):
        """Child of <feMerge>; references a filter result by name."""
        tag = 'feMergeNode'
        required = {}
        optional = {'in': None}
        styles = []

        def __init__(self, *elems, **kwargs):
            """
           **LLM Docstring**

           Construct a merge-node filter primitive and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Feflood(TagElement):
        """Fills filter region with a solid colour."""
        tag = 'feFlood'
        required = {'flood-color': None}
        optional = {'flood-opacity': numbers.Number, 'result': None}
        styles = []

        def __init__(self, *elems, flood_color=None, **kwargs):
            """
           **LLM Docstring**

           Construct a flood filter primitive and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param flood_color: The color used by the flood filter primitive.
           :type flood_color: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Feturbulence(TagElement):
        """Perlin / fractal noise. Good base for texture effects."""
        tag = 'feTurbulence'
        required = {'baseFrequency': None}
        optional = {'type': str, 'numOctaves': numbers.Number, 'seed': numbers.Number, 'stitchTiles': str, 'result': None}
        styles = []

        def __init__(self, *elems, baseFrequency=None, **kwargs):
            """
           **LLM Docstring**

           Construct a turbulence filter primitive and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param baseFrequency: The turbulence base-frequency value.
           :type baseFrequency: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Fedisplacementmap(TagElement):
        """Warps 'in' using a displacement map from 'in2'."""
        tag = 'feDisplacementMap'
        required = {'in': str, 'in2': None, 'scale': numbers.Number}
        optional = {'xChannelSelector': str, 'yChannelSelector': str, 'result': None}
        styles = []

        def __init__(self, *elems, in_='SourceGraphic', in2=None, scale=0, **kwargs):
            """
           **LLM Docstring**

           Construct a displacement-map filter primitive and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param in_: The primary SVG filter input; the trailing underscore avoids Python’s `in` keyword.
           :type in_: object
           :param in2: The secondary SVG filter input.
           :type in2: object
           :param scale: The displacement scale factor.
           :type scale: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Animate(TagElement):
        """SMIL animation of a single attribute on the parent element."""
        tag = 'animate'
        required = {'attributeName': None}
        styles = []

        def __init__(self, *elems, attributeName=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG attribute animation and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param attributeName: The SVG attribute targeted by the animation.
           :type attributeName: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Animatetransform(TagElement):
        """Animates a transform. type='rotate' from/to can include cx,cy: '0 50 50'."""
        tag = 'animateTransform'
        required = {'attributeName': str, 'type': str}
        optional = {'from': None, 'to': None, 'values': None, 'dur': None, 'repeatCount': str, 'begin': str, 'fill': str, 'additive': str}
        styles = []

        def __init__(self, *elems, attributeName='transform', type='rotate', **kwargs):
            """
           **LLM Docstring**

           Construct a SVG transform animation and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param attributeName: The SVG attribute targeted by the animation.
           :type attributeName: object
           :param type: The SVG operation or animation type.
           :type type: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Animatemotion(TagElement):
        """Moves element along a path. Add <mpath href='#path-id'> as child."""
        tag = 'animateMotion'
        required = {}
        optional = {'path': None, 'keyPoints': None, 'rotate': str, 'dur': None, 'repeatCount': str, 'begin': str, 'calcMode': str}
        styles = []

        def __init__(self, *elems, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG motion animation and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Set(TagElement):
        """Discretely sets an attribute value for a duration (no interpolation)."""
        tag = 'set'
        required = {'attributeName': None, 'to': None}
        optional = {'begin': str, 'dur': None, 'end': None, 'fill': str}
        styles = []

        def __init__(self, *elems, attributeName=None, to=None, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG set animation and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param attributeName: The SVG attribute targeted by the animation.
           :type attributeName: object
           :param to: The target animation value.
           :type to: object
           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Title(TagElement):
        """Accessible name for the SVG or a group. First child of <svg> or <g>."""
        tag = 'title'
        required = {}
        optional = {}
        styles = []

        def __init__(self, *elems, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG title and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Desc(TagElement):
        """Longer accessible description. Complements <title>."""
        tag = 'desc'
        required = {}
        optional = {}
        styles = []

        def __init__(self, *elems, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG description and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...

    class Metadata(TagElement):
        """Container for non-SVG metadata (e.g. RDF, XMP)."""
        tag = 'metadata'
        required = {}
        optional = {}
        styles = []

        def __init__(self, *elems, **kwargs):
            """
           **LLM Docstring**

           Construct a SVG metadata element and forward its element-specific defaults and attributes to `SVG.TagElement`.

           :param elems: Child elements or text content.
           :type elems: tuple
           :param kwargs: Additional attributes or options forwarded to the constructed element.
           :type kwargs: dict
           """
            ...