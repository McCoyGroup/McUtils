import re
import uuid
import numpy as np
import urllib.parse
from ..Data import ColorData
from .. import Numputils as nput
from .. import Devutils as dev
__all__ = ['ColorPalette', 'prep_color']

class ColorPalette:

    def __init__(self, colors, blend_spacings=None, lab_colors=None, color_space='rgb', cycle=False, return_color_codes=True):
        """
        **LLM Docstring**

        Build a color palette from a list of colors (or a named colormap/colormap
        callable), precomputing the color codes and their Lab-space values for blending.

        :param colors: the colors, a named palette/colormap, or a colormap callable
        :param blend_spacings: the abcissae the colors sit at for blending (evenly spaced if omitted)
        :param lab_colors: precomputed Lab values (computed if omitted)
        :param color_space: the space the input colors are given in
        :type color_space: str
        :param cycle: index into the palette cyclically
        :type cycle: bool
        :param return_color_codes: return hex color codes by default
        :type return_color_codes: bool
        :raises ValueError: if the colors aren't a valid palette list
        """
        ...

    def __hash__(self):
        """
        **LLM Docstring**

        Hash the palette by its type and color codes.

        :return: the hash
        :rtype: int
        """
        ...

    @classmethod
    def _color_code_like(cls, name):
        """
        **LLM Docstring**

        Heuristic test for whether a bare (no `#`) string looks like a hex color code
        (length divisible by 3 or 4).

        :param name: the string
        :type name: str
        :return: whether it looks like a hex code
        """
        ...

    @classmethod
    def parse_color_string(cls, name: str, include_named_alpha=False, return_padding=False):
        """
        **LLM Docstring**

        Parse a color string (named color, hex code, or matplotlib name) into an RGB(A)
        value.

        :param name: the color string
        :type name: str
        :param include_named_alpha: keep the alpha channel of named colors
        :type include_named_alpha: bool
        :param return_padding: also return the per-channel hex padding
        :type return_padding: bool
        :return: the RGB(A) value (and padding if requested)
        """
        ...

    @classmethod
    def prep_color_palette(cls, colors, color_space='rgb', lab_colors=None):
        """
        **LLM Docstring**

        Normalize a palette's colors into hex color strings and their Lab values,
        converting from the given color space as needed.

        :param colors: the palette colors (strings or numeric arrays)
        :param color_space: the space the numeric colors are in
        :type color_space: str
        :param lab_colors: precomputed Lab values
        :return: `(color_strings, lab_colors)`
        :rtype: tuple
        """
        ...

    @classmethod
    def prep_color(cls, base=None, palette=None, blending=None, index=None, lighten=None, saturate=None, modifier=None, shift=False, absolute=False, clip=True, color_space='rgb', modification_space='lab', return_color_code=True, cycle=None, alpha=None):
        """
        **LLM Docstring**

        Compose a color (or list of colors) from a base color or palette, optionally
        indexing/blending the palette and applying saturate/lighten/modify/alpha
        transformations.

        :param base: an explicit base color (or list); required if no palette
        :param palette: a palette to draw the base from
        :param blending: a blend amount to sample the palette at
        :param index: a palette index to select
        :type index: int | None
        :param lighten: a lighten amount
        :param saturate: a saturate amount
        :param modifier: a custom color-modification callback
        :param shift: apply modifications additively rather than multiplicatively
        :type shift: bool
        :param absolute: set (rather than scale) the modified channel
        :type absolute: bool
        :param clip: clip the result into the valid range
        :type clip: bool
        :param color_space: the working color space
        :type color_space: str
        :param modification_space: the space modifications are applied in
        :type modification_space: str
        :param return_color_code: return hex codes
        :type return_color_code: bool
        :param cycle: cycle the palette when indexing
        :param alpha: an alpha value to apply
        :return: the composed color(s)
        :raises ValueError: if neither a base color nor a palette is given
        """
        ...

    @classmethod
    def set_alpha(cls, b, alpha):
        """
        **LLM Docstring**

        Set the alpha channel on a color (hex code, named color, RGB array, or list of
        colors).

        :param b: the color
        :param alpha: the alpha value
        :return: the color with alpha applied
        """
        ...

    @classmethod
    def resolve_color_palette(cls, cmap_name):
        """
        **LLM Docstring**

        Resolve a named palette to its color data, falling back to discretizing a
        matplotlib colormap of that name.

        :param cmap_name: the palette/colormap name
        :type cmap_name: str
        :return: the palette color data
        """
        ...

    @classmethod
    def is_colormap_like(cls, cmap):
        """
        **LLM Docstring**

        Test whether an object is colormap-like (callable).

        :param cmap: the object
        :return: whether it's colormap-like
        :rtype: bool
        """
        ...

    @classmethod
    def discretize_colormap(cls, cmap, samples=10):
        """
        **LLM Docstring**

        Sample a colormap at evenly-spaced points to produce a discrete palette.

        :param cmap: the colormap (or `ColorPalette`)
        :param samples: the number of samples
        :type samples: int
        :return: the discrete colors
        """
        ...

    @classmethod
    def is_palette_list(self, colors):
        """
        **LLM Docstring**

        Test whether an object is a valid palette list (a list of color strings or
        numeric color arrays).

        :param colors: the object
        :return: whether it's a palette list
        :rtype: bool
        """
        ...

    def flip(self):
        """
        **LLM Docstring**

        Return a copy of the palette with its colors reversed.

        :return: the reversed palette
        :rtype: ColorPalette
        """
        ...

    def __eq__(self, other):
        """
        **LLM Docstring**

        Two palettes are equal if they have the same color codes.

        :param other: the object to compare against
        :return: whether they are equal
        :rtype: bool
        """
        ...

    def get_colorblindness_test_url(self):
        """
        **LLM Docstring**

        Build a URL that previews the palette under color-blindness simulation.

        :return: the preview URL
        :rtype: str
        """
        ...

    def blend(self, amount, modification_space='lab', rescale=False, clip=True, return_color_code=True):
        """
        **LLM Docstring**

        Interpolate the palette at one or more blend amounts, linearly interpolating in
        the given space between the bracketing colors (clamping at the ends).

        :param amount: the blend amount(s) in `[0, 1]`
        :param modification_space: the space to interpolate in
        :type modification_space: str
        :param rescale: rescale the numeric result (e.g. to `[0, 1]`)
        :type rescale: bool
        :param clip: clip the result into the valid range
        :type clip: bool
        :param return_color_code: return hex codes rather than numeric colors
        :type return_color_code: bool
        :return: the blended color(s)
        """
        ...

    def as_colormap(self, levels=None, cmap_type='list', name=None, **opts):
        """
        **LLM Docstring**

        Build a matplotlib colormap (listed or interpolated) from the palette.

        :param levels: the levels (count or explicit) to sample at
        :param cmap_type: `'list'`, `'interpolated'`, or a colormap factory
        :type cmap_type: str
        :param name: the colormap name (auto-generated if omitted)
        :type name: str | None
        :param opts: options for the colormap constructor
        :return: the colormap
        """
        ...

    def __call__(self, amount, rescale=True, return_color_code=False):
        """
        **LLM Docstring**

        Sample the palette at a blend amount (delegates to `blend`).

        :param amount: the blend amount(s)
        :param rescale: rescale the numeric result
        :type rescale: bool
        :param return_color_code: return hex codes
        :type return_color_code: bool
        :return: the sampled color(s)
        """
        ...

    def modify(self, modification_function, modification_space='lab', clip=True):
        """
        **LLM Docstring**

        Return a new palette with a modification function applied to its Lab colors.

        :param modification_function: the color-modification callback
        :type modification_function: Callable
        :param modification_space: the space the modification acts in
        :type modification_space: str
        :param clip: clip the result
        :type clip: bool
        :return: the modified palette
        :rtype: ColorPalette
        """
        ...

    def lighten(self, percentage, modification_space='lab', shift=False, absolute=False, clip=True):
        """
        **LLM Docstring**

        Return a new palette lightened by the given amount.

        :param percentage: the lighten amount
        :param modification_space: the space to lighten in
        :type modification_space: str
        :param shift: lighten additively
        :type shift: bool
        :param absolute: set the lightness rather than scaling it
        :type absolute: bool
        :param clip: clip the result
        :type clip: bool
        :return: the lightened palette
        :rtype: ColorPalette
        """
        ...

    @classmethod
    def color_normalize(cls, color_list, color_space='rgb'):
        """
        **LLM Docstring**

        Clip color values into the valid range for their color space.

        :param color_list: the colors
        :param color_space: the color space
        :type color_space: str
        :return: the clipped colors
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def color_rescale(cls, color_list, color_space='rgb'):
        """
        **LLM Docstring**

        Rescale color values out of their integer range (RGB by 255, XYZ by 100).

        :param color_list: the colors
        :param color_space: the color space
        :type color_space: str
        :return: the rescaled colors
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def color_modify(cls, color, modification_function, color_space='rgb', modification_space='lab', clip=True):
        """
        **LLM Docstring**

        Apply a modification function to a single color, converting into the modification
        space and back and optionally clipping.

        :param color: the color (hex code or numeric)
        :param modification_function: the modification callback
        :type modification_function: Callable
        :param color_space: the color's space
        :type color_space: str
        :param modification_space: the space to modify in
        :type modification_space: str
        :param clip: clip the result
        :type clip: bool
        :return: the modified color
        """
        ...

    @classmethod
    def color_lighten(cls, color, percentage, color_space='rgb', modification_space='lab', shift=False, absolute=False, clip=True):
        """
        **LLM Docstring**

        Lighten a color by scaling/shifting/setting its lightness channel in the
        modification space.

        :param color: the color
        :param percentage: the lighten amount
        :param color_space: the color's space
        :type color_space: str
        :param modification_space: the space to lighten in (Lab or HSV/HSL)
        :type modification_space: str
        :param shift: lighten additively
        :type shift: bool
        :param absolute: set the lightness rather than scaling
        :type absolute: bool
        :param clip: clip the result
        :type clip: bool
        :return: the lightened color
        :raises ValueError: for an unsupported modification space
        """
        ...

    @classmethod
    def color_saturate(cls, color, percentage, color_space='rgb', modification_space='hsv', shift=False, absolute=False, clip=True):
        """
        **LLM Docstring**

        Saturate a color by scaling/shifting/setting its saturation (chroma) in the
        modification space.

        :param color: the color
        :param percentage: the saturate amount
        :param color_space: the color's space
        :type color_space: str
        :param modification_space: the space to saturate in (HSV/HSL or Lab)
        :type modification_space: str
        :param shift: saturate additively
        :type shift: bool
        :param absolute: set the saturation rather than scaling
        :type absolute: bool
        :param clip: clip the result
        :type clip: bool
        :return: the saturated color
        :raises ValueError: for an unsupported modification space
        """
        ...

    def __len__(self):
        """
        **LLM Docstring**

        The number of colors in the palette.

        :return: the color count
        :rtype: int
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Index the palette by an integer (a single color, cycling if enabled) or a
        slice/array (a sub-palette).

        :param item: the index or slice
        :return: the color or sub-palette
        """
        ...

    @classmethod
    def rgb_code(cls, rgb, padding=2):
        """
        **LLM Docstring**

        Format an RGB value (or list of them) as a hex color code.

        :param rgb: the RGB value(s)
        :param padding: the per-channel hex width
        :type padding: int
        :return: the hex code(s)
        :rtype: str | list
        """
        ...

    @classmethod
    def parse_rgb_code(cls, code, padding=None, return_padding=False, num_channels=None):
        """
        **LLM Docstring**

        Parse a hex color code into an RGB(A) value, inferring the per-channel padding.

        :param code: the hex code
        :type code: str
        :param padding: the per-channel hex width (inferred if omitted)
        :type padding: int | None
        :param return_padding: also return the inferred padding
        :type return_padding: bool
        :param num_channels: the expected number of channels
        :type num_channels: int | None
        :return: the RGB(A) value (and padding if requested)
        """
        ...
    converters = {}

    @classmethod
    def color_convert(self, color, original_space, target_space):
        """
        **LLM Docstring**

        Convert a color between two color spaces, routing through the intermediate spaces
        (e.g. RGB/XYZ/Lab/HSL/HSV) as needed.

        :param color: the color
        :param original_space: the source space
        :type original_space: str
        :param target_space: the destination space
        :type target_space: str
        :return: the converted color
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def xyz_to_rgb(self, x, y, z):
        """
        **LLM Docstring**

        Convert a color from CIE XYZ to sRGB.

        :param x: the X channel
        :param y: the Y channel
        :param z: the Z channel
        :return: the RGB color
        :rtype: np.ndarray
        """
        ...
    rgb_to_xyz_array = [[0.412453, 0.35758, 0.180423], [0.212671, 0.71516, 0.072169], [0.019334, 0.119193, 0.950227]]

    @classmethod
    def rgb_to_xyz(self, r, g, b):
        """
        **LLM Docstring**

        Convert a color from sRGB to CIE XYZ.

        :param r: the red channel
        :param g: the green channel
        :param b: the blue channel
        :return: the XYZ color
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def _rgb2hue(cls, rgb, diff, max_val):
        """
        **LLM Docstring**

        Compute the hue channel from RGB values and their max/range (a shared HSL/HSV
        helper).

        :param rgb: the RGB values
        :param diff: the max-minus-min range
        :param max_val: the per-color max channel
        :return: the hue
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def rgb_to_hsl(self, r, g, b):
        """
        **LLM Docstring**

        Convert a color from RGB to HSL.

        :param r: the red channel
        :param g: the green channel
        :param b: the blue channel
        :return: the HSL color
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def _hue2rgb(cls, v1, v2, h):
        """
        **LLM Docstring**

        Reconstruct a single RGB channel from HSL intermediates (a helper for
        `hsl_to_rgb`).

        :param v1: the first HSL intermediate
        :param v2: the second HSL intermediate
        :param h: the (shifted) hue
        :return: the channel value
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def hsl_to_rgb(cls, h, s, l):
        """
        **LLM Docstring**

        Convert a color from HSL to RGB.

        :param h: the hue
        :param s: the saturation
        :param l: the lightness
        :return: the RGB color
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def rgb_to_hsv(self, r, g, b):
        """
        **LLM Docstring**

        Convert a color from RGB to HSV.

        :param r: the red channel
        :param g: the green channel
        :param b: the blue channel
        :return: the HSV color
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def hsv_to_hsl(cls, h, s, v):
        """
        **LLM Docstring**

        Convert a color from HSV to HSL.

        :param h: the hue
        :param s: the saturation
        :param v: the value
        :return: the HSL color
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def hsv_to_rgb(cls, h, s, v):
        """
        **LLM Docstring**

        Convert a color from HSV to RGB (via HSL).

        :param h: the hue
        :param s: the saturation
        :param v: the value
        :return: the RGB color
        :rtype: np.ndarray
        """
        ...
    lab_scaling_reference = [95.0489, 100.0, 108.884]

    @classmethod
    def xyz_to_lab(cls, x, y, z, scaling=None):
        """
        **LLM Docstring**

        Convert a color from CIE XYZ to CIE Lab.

        :param x: the X channel
        :param y: the Y channel
        :param z: the Z channel
        :param scaling: the white-point scaling
        :return: the Lab color
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def lab_to_xyz(cls, l, a, b, scaling=None):
        """
        **LLM Docstring**

        Convert a color from CIE Lab to CIE XYZ.

        :param l: the lightness channel
        :param a: the a channel
        :param b: the b channel
        :param scaling: the white-point scaling
        :return: the XYZ color
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def lab_to_lch(cls, l, a, b):
        """
        **LLM Docstring**

        Convert a color from CIE Lab to CIE LCh.

        :param l: the lightness channel
        :param a: the a channel
        :param b: the b channel
        :return: the LCh color
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def lch_to_lab(cls, l, c, h):
        """
        **LLM Docstring**

        Convert a color from CIE LCh to CIE Lab.

        :param l: the lightness channel
        :param c: the chroma channel
        :param h: the hue channel
        :return: the Lab color
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def rgb_to_lab(cls, r, g, b, xyz_scaling=None):
        """
        **LLM Docstring**

        Convert a color from RGB to CIE Lab (via XYZ).

        :param r: the red channel
        :param g: the green channel
        :param b: the blue channel
        :param xyz_scaling: the white-point scaling
        :return: the Lab color
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def lab_to_rgb(cls, l, a, b, xyz_scaling=None):
        """
        **LLM Docstring**

        Convert a color from CIE Lab to RGB (via XYZ).

        :param l: the lightness channel
        :param a: the a channel
        :param b: the b channel
        :param xyz_scaling: the white-point scaling
        :return: the RGB color
        :rtype: np.ndarray
        """
        ...

def prep_color(base=None, palette=None, blending=None, index=None, lighten=None, saturate=None, modifier=None, shift=False, absolute=False, clip=True, color_space='rgb', modification_space='lab', return_color_code=True, alpha=None, cycle=None):
    """
    **LLM Docstring**

    Module-level shortcut for `ColorPalette.prep_color`: compose a color from a base
    color or palette with optional blending/indexing and saturate/lighten/modify/alpha
    transformations.

    :param base: an explicit base color
    :param palette: a palette to draw from
    :param blending: a blend amount
    :param index: a palette index
    :param lighten: a lighten amount
    :param saturate: a saturate amount
    :param modifier: a custom modification callback
    :param shift: apply modifications additively
    :type shift: bool
    :param absolute: set rather than scale the modified channel
    :type absolute: bool
    :param clip: clip the result
    :type clip: bool
    :param color_space: the working color space
    :type color_space: str
    :param modification_space: the modification space
    :type modification_space: str
    :param return_color_code: return hex codes
    :type return_color_code: bool
    :param alpha: an alpha value
    :param cycle: cycle the palette when indexing
    :return: the composed color(s)
    """
    ...