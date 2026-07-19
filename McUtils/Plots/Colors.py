import re
import uuid

import numpy as np
import urllib.parse
from ..Data import ColorData
from .. import Numputils as nput
from .. import Devutils as dev

__all__ = [
    "ColorPalette",
    "prep_color"
]

#TODO: add ColorSpaces enum for validation

class ColorPalette:
    def __init__(self, colors, blend_spacings=None, lab_colors=None, color_space='rgb', cycle=False,
                 return_color_codes=True
                 ):
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
        if isinstance(colors, str):
            colors = self.resolve_color_palette(colors)
        elif self.is_colormap_like(colors):
            colors = self.discretize_colormap(colors)
        if not self.is_palette_list(colors):
            raise ValueError(f"{colors} is not a color palette list")
        self.color_strings, self.lab_colors = self.prep_color_palette(colors, color_space, lab_colors=lab_colors)
        # TODO: add more sophisticated blending
        if blend_spacings is None:
            blend_spacings = np.linspace(0, 1, len(self.color_strings))
        self.abcissae = np.asanyarray(blend_spacings)
        self.cycle = cycle

    def __hash__(self):
        """
        **LLM Docstring**

        Hash the palette by its type and color codes.

        :return: the hash
        :rtype: int
        """
        return hash((type(self), self.color_strings))
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
        if len(name) % 3 == 0 or len(name) % 4 == 0:
            return re.match(r"\w+", name)
        else:
            return False
    @classmethod
    def parse_color_string(cls, name:str, include_named_alpha=False, return_padding=False):
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
        if not name.startswith('#'):
            c = ColorData['Named'].data.get(name)
            if c is None:
                if cls._color_code_like(name):
                    c = '#'+name
                else:
                    from matplotlib.colors import to_rgba
                    vals = to_rgba(name)
                    c = [255 * x for x in vals[:3]]
                    if include_named_alpha:
                        c = c + list(vals[3:])
                    if return_padding:
                        c = (c, 2)
        else:
            c = name
        if isinstance(c, str):
            c = cls.parse_rgb_code(c, return_padding=return_padding)
        return c

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
        if lab_colors is not None:
            lab_colors = np.asanyarray(lab_colors)
        if isinstance(colors[0], str):
            if color_space != 'rgb':
                raise ValueError(f"only rgb color codes supported (got {colors})")
            color_lists = colors
            rgb_array = np.array([cls.parse_color_string(c) for c in colors])
            if lab_colors is None:
                lab_colors = cls.color_convert(rgb_array.T, "rgb", "lab").T
        else:
            colors = np.asanyarray(colors)
            if lab_colors is None:
                if color_space != 'lab':
                    lab_colors = cls.color_convert(colors.T, color_space, "lab").T
                else:
                    lab_colors = colors
            if color_space != 'rgb':
                rgb_colors = cls.color_convert(colors.T, color_space, 'rgb').T
            else:
                rgb_colors = colors
            color_lists = [cls.rgb_code(c, 2) for c in rgb_colors]

        return tuple(color_lists), lab_colors

    @classmethod
    def prep_color(cls,
                   base=None,
                   palette=None,
                   blending=None,
                   index=None,
                   lighten=None,
                   saturate=None,
                   modifier=None,
                   shift=False,
                   absolute=False,
                   clip=True,
                   color_space='rgb',
                   modification_space='lab',
                   return_color_code=True,
                   cycle=None,
                   alpha=None
                   ):
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
        if base is None:
            if palette is None:
                raise ValueError("can't compose color without base color or palette")
            palette:ColorPalette
            if not isinstance(palette, ColorPalette):
                if cycle is None:
                    cycle = index is not None
                palette = cls(palette, cycle=cycle)
            if index is not None:
                base = palette[index]
                if hasattr(base, 'color_strings'):
                    base = base.color_strings
            elif blending is not None:
                base = palette(blending, return_color_code=return_color_code)
            else:
                if return_color_code:
                    base = palette.color_strings
                else:
                    base = palette.color_convert(palette.lab_colors, 'lab', color_space)

        smol = isinstance(base, str) or not dev.is_atomic(base[0])
        if smol: base = [base]
        final = []
        for b in base:
            if saturate is not None:
                b = cls.color_saturate(b, saturate,
                                      color_space=color_space,
                                      modification_space=modification_space,
                                      shift=shift,
                                      absolute=absolute,
                                      clip=clip
                                      )
            if lighten is not None:
                b = cls.color_lighten(b, lighten,
                                      color_space=color_space,
                                      modification_space=modification_space,
                                      shift=shift,
                                      absolute=absolute,
                                      clip=clip
                                      )
            if modifier is not None:
                b = cls.color_modify(b, modifier,
                                      color_space=color_space,
                                      modification_space=modification_space,
                                      clip=clip
                                      )
            if alpha is not None:
                b = cls.set_alpha(b, alpha)
            final.append(b)
        if smol:
            final = final[0]
        return final

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
        if isinstance(b, str):
            if b.startswith('#'):
                _, padding = cls.parse_rgb_code(b, return_padding=True)
                if alpha < 1:
                    alpha = int(alpha*255)
                b = b + f'{alpha:0>{padding}x}'
            else:
                b, padding = cls.parse_color_string(b, return_padding=True)
                if len(b) < 4:
                    b = np.concatenate([b, [alpha]], axis=0)
                else:
                    b = np.array(b)
                    b[-1] = alpha
                b = cls.rgb_code(b, padding)
        elif cls.is_palette_list(b):
            return [cls.set_alpha(bb, alpha) for bb in b]
        else:
            if len(b) < 4:
                b = np.concatenate([b, [alpha]], axis=0)
            else:
                b = np.array(b)
                b[-1] = alpha
        return b


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
        try:
            data = ColorData[cmap_name].data
        except KeyError:
            from matplotlib import colormaps

            data = cls.discretize_colormap(colormaps[cmap_name])

        return data

    @classmethod
    def is_colormap_like(cls, cmap):
        """
        **LLM Docstring**

        Test whether an object is colormap-like (callable).

        :param cmap: the object
        :return: whether it's colormap-like
        :rtype: bool
        """
        return hasattr(cmap, '__call__')
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
        if isinstance(cmap, ColorPalette):
            return cmap.color_strings
        else:
            vals = cmap(np.linspace(0, 1, samples))
            return 255 * vals[:, :3]

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
        return (
                dev.is_list_like(colors)
                and all(
                    isinstance(c, str)
                    or nput.is_numeric_array_like(c)
                    for c in colors
                )
        )
    def flip(self):
        """
        **LLM Docstring**

        Return a copy of the palette with its colors reversed.

        :return: the reversed palette
        :rtype: ColorPalette
        """
        return type(self)(list(reversed(self.color_strings)))

    def __eq__(self, other):
        """
        **LLM Docstring**

        Two palettes are equal if they have the same color codes.

        :param other: the object to compare against
        :return: whether they are equal
        :rtype: bool
        """
        if not hasattr(other, "color_strings"): return False
        return self.color_strings == other.color_strings

    def get_colorblindness_test_url(self):
        """
        **LLM Docstring**

        Build a URL that previews the palette under color-blindness simulation.

        :return: the preview URL
        :rtype: str
        """
        return "https://davidmathlogic.com/colorblind/#" + "-".join(
            urllib.parse.quote(c[:7] if c.startswith("#") else c[:6]) for c in self.color_strings
        )

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
        amount = np.asanyarray(amount)
        smol = amount.ndim == 0
        if smol: amount = np.array([amount])
        insertion_indices = np.searchsorted(self.abcissae, amount)
        terminals = insertion_indices == len(self.abcissae)
        starts = insertion_indices == 0
        rems = np.logical_not(np.logical_or(terminals, starts))
        codes = [""] * len(amount)
        new_colors = np.empty((len(amount), len(self.lab_colors[0])), dtype=float)
        if return_color_code:
            term_pos = np.where(terminals)
            if len(term_pos) > 0:
                for i in term_pos[0]:
                    codes[i] = self.color_strings[-1]
            start_pos = np.where(starts)
            if len(start_pos) > 0:
                for i in start_pos[0]:
                    codes[i] = self.color_strings[0]
        else:
            if terminals.any():
                color = np.array(self.parse_rgb_code(self.color_strings[-1]))
                new_colors[terminals] = color[np.newaxis]
            if starts.any():
                color = np.array(self.parse_rgb_code(self.color_strings[0]))
                new_colors[starts] = color[np.newaxis]
        if rems.any():
            rem_inds = insertion_indices[rems]
            x = self.abcissae[rem_inds - 1,]
            y = self.abcissae[rem_inds,]
            d = ((amount[rems,] - x) / (y - x))[:, np.newaxis]

            colors = self.lab_colors
            if modification_space != 'lab':
                colors = self.color_convert(colors, 'lab', modification_space).T
            new_lab = colors[rem_inds - 1,] * (1 - d) + colors[rem_inds,] * d
            rgb = self.color_convert(new_lab.T, modification_space, 'rgb').T

            if clip:
                rgb = self.color_normalize(rgb, "rgb")

            if return_color_code:
                rgb = self.rgb_code(rgb.T)
                rems = np.where(rems)[0]
                for n,r in enumerate(rgb):
                    codes[rems[n]] = r
            else:
                new_colors[rems,] = rgb

        if return_color_code:
            if smol: codes = codes[0]
            return codes
        else:
            if rescale: new_colors = self.color_rescale(new_colors, 'rgb')
            if smol: new_colors = new_colors[0]
            return new_colors

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
        from matplotlib.colors import ListedColormap, LinearSegmentedColormap

        if levels is None:
            levels = np.linspace(0, 1, len(self.color_strings))
            vals = np.array(self.parse_rgb_code(self.color_strings)) / 255
        else:
            if nput.is_int(levels):
                levels = np.linspace(0, 1, levels)
            vals = self(levels)

        if dev.str_is(cmap_type, 'list'):
            cmap = np.concatenate([
                vals,
                np.ones((len(vals), 1)),
                ],
                axis=1
            )
            new_map = ListedColormap(cmap, **opts)
        elif dev.str_is(cmap_type, 'interpolated'):
            cmap_dict = {
                'red':np.concatenate([
                    levels[:, np.newaxis],
                    vals[:, (0,)],
                    vals[:, (0,)]
                ],axis=1),
                'green':np.concatenate([
                    levels[:, np.newaxis],
                    vals[:, (1,)],
                    vals[:, (1,)]
                ],axis=1),
                'blue':np.concatenate([
                    levels[:, np.newaxis],
                    vals[:, (2,)],
                    vals[:, (2,)]
                ],axis=1)
            }
            if name is None:
                name = '-'.join(['cmap']+str(uuid.uuid4()).split("-")[:2])
            new_map = LinearSegmentedColormap(name, segmentdata=cmap_dict, **opts)
        else:
            new_map: 'ListedColormap|LinearSegmentedColormap' = cmap_type(levels, vals, **opts)

        return new_map

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
        return self.blend(amount, rescale=rescale, return_color_code=return_color_code)

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
        return type(self)(
            modification_function(
                self.lab_colors.T,
                color_space='lab',
                modification_space=modification_space,
                clip=clip
            ).T,
            color_space='lab'
        )

    def lighten(self, percentage,
                modification_space='lab',
                shift=False,
                absolute=False, clip=True):
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
        return type(self)(
            self.color_lighten(self.lab_colors.T,
                               percentage,
                               color_space='lab',
                               modification_space=modification_space,
                               shift=shift,
                               absolute=absolute,
                               clip=clip
                               ).T,
            color_space='lab'
        )

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
        color_list = np.asanyarray(color_list)
        smol = color_list.ndim == 1
        if smol: color_list = color_list[:, np.newaxis]
        if color_space == 'rgb':
            color_list = np.clip(color_list, 0, 255)
        # elif color_space == 'xyz':
        #     color_list = np.clip(color_list, 0, 100)
        elif color_space in {'hsl', 'hsv'}:
            color_list = np.clip(color_list, 0, 1)
        if smol: color_list = color_list[:, 0]
        return color_list

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
        color_list = np.asanyarray(color_list)
        if color_space == 'rgb':
            color_list = color_list / 255
        elif color_space == 'xyz':
            color_list = color_list / 100
        return color_list
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
        as_code = isinstance(color, str)
        padding = 2
        if as_code:
            if color_space != 'rgb':
                raise ValueError(f"only rgb color codes supported (got {color})")
            color, padding = cls.parse_color_string(color, return_padding=True)
        if color_space != modification_space:
            lab_color = cls.color_convert(color, color_space, modification_space)
        else:
            lab_color = color
        lab_color = modification_function(*lab_color)
        if color_space != modification_space:
            color = cls.color_convert(lab_color, modification_space, color_space)
        if clip:
            color = cls.color_normalize(color, color_space)

        if as_code:
            color = cls.rgb_code(color, padding=padding)
        return color
    @classmethod
    def color_lighten(cls, color, percentage,
                      color_space='rgb',
                      modification_space='lab',
                      shift=False,
                      absolute=False, clip=True):
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
        if modification_space == 'lab':
            if shift:
                percentage = 100*percentage
                conversion = lambda l,a,b:[l+percentage, a, b]
            elif absolute:
                percentage = 100*percentage
                conversion = lambda l,a,b:[percentage, a, b]
            else:
                conversion = lambda l,a,b:[l*(1+percentage), a, b]
        elif modification_space in {'hsv', 'hsl'}:
            if shift:
                conversion = lambda h,s,l:[h, s, l+percentage]
            elif absolute:
                conversion = lambda h,s,l:[h, s, percentage]
            else:
                conversion = lambda h,s,l:[h, s, l*(1+percentage)]
        else:
            raise ValueError(f"can't lighten color in modification_space `{modification_space}`")

        return cls.color_modify(color, conversion, color_space=color_space, modification_space=modification_space, clip=clip)
    @classmethod
    def color_saturate(cls, color, percentage,
                      color_space='rgb',
                      modification_space='hsv',
                      shift=False,
                      absolute=False, clip=True):
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
        if modification_space in {'hsv', 'hsl'}:
            if shift:
                conversion = lambda h, s, l: [h, s + percentage, l]
            elif absolute:
                conversion = lambda h, s, l: [h, percentage, l]
            else:
                conversion = lambda h, s, l: [h, s * (1 + percentage), l]
        elif modification_space == 'lab':
            if shift:
                percentage = 100*percentage
                def conversion(l,a,b):
                    """
                    **LLM Docstring**

                    Compute the saturated color channels for the Lab-space saturation branch,
                    preserving the a/b hue direction while scaling/shifting the chroma.

                    :param l: the lightness channel
                    :param a: the a channel
                    :param b: the b channel
                    :return: the modified  channels
                    :rtype: list
                    """
                    z_mask = np.abs(b) < 1e-8
                    r = b.copy()
                    r[z_mask] = 1
                    r = a / r
                    r[z_mask] = 0
                    b = b + percentage
                    return [l, r * b, b]
            elif absolute:
                percentage = 100*percentage
                def conversion(l,a,b):
                    """
                    **LLM Docstring**

                    Compute the saturated color channels for the Lab-space saturation branch,
                    preserving the a/b hue direction while scaling/shifting the chroma.

                    :param l: the lightness channel
                    :param a: the a channel
                    :param b: the b channel
                    :return: the modified  channels
                    :rtype: list
                    """
                    z_mask = np.abs(b) < 1e-8
                    r = b.copy()
                    r[z_mask] = 1
                    r = a / r
                    r[z_mask] = 0
                    return [l, r * percentage, percentage]
            else:
                conversion = lambda l,a,b:[l, a*(1+percentage), b*(1+percentage)]
        else:
            raise ValueError(f"can't saturate color in modification_space `{modification_space}`")

        return cls.color_modify(color, conversion, color_space=color_space,
                                modification_space=modification_space,
                                clip=clip)

    def __len__(self):
        """
        **LLM Docstring**

        The number of colors in the palette.

        :return: the color count
        :rtype: int
        """
        return len(self.color_strings)
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Index the palette by an integer (a single color, cycling if enabled) or a
        slice/array (a sub-palette).

        :param item: the index or slice
        :return: the color or sub-palette
        """
        if nput.is_int(item):
            if not self.cycle:
                return self.color_strings[item]
            else:
                return self.color_strings[item % len(self.color_strings)]
        else:
            return type(self)(
                np.asanyarray(self.color_strings)[item],
                blend_spacings=self.abcissae[item],
                lab_colors=self.lab_colors[item]
            )


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
        if not isinstance(rgb[0], (int, float, np.floating, np.integer)):
            return [
                cls.rgb_code([r, g, b])
                for r, g, b in zip(*rgb)
            ]
        rgb = np.round(np.clip(rgb, 0, 255)).astype(int)
        return f"#{rgb[0]:0>{padding}x}{rgb[1]:0>{padding}x}{rgb[2]:0>{padding}x}"
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
        if not isinstance(code, str):
            if not return_padding:
                return [
                    cls.parse_rgb_code(c, padding=padding, return_padding=False)
                    for c in code
                ]
            else:
                padding, _ = cls.parse_rgb_code(code[0], padding=padding, return_padding=True)
                return [
                    cls.parse_rgb_code(c, padding=padding, return_padding=False)
                    for c in code
                ], padding
        if code[0] == "#":
            code = code[1:]
        if num_channels is None:
            lc = len(code)
            if lc % 3 == 0:
                num_channels = 3
            elif lc % 4 == 0:
                num_channels = 4
            elif lc == 1 or lc == 2:
                num_channels = 1
            else:
                num_channels = 3
        if padding is None:
            padding = len(code) // num_channels
        color_list = [
            int(code[(padding*i):(padding*(i+1))], 16)
            for i in range(num_channels)
        ]
        if return_padding:
            return color_list, padding
        else:
            return color_list

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
        if original_space == target_space:
            return color
        if (original_space, target_space) in self.converters:
            conversion = self.converters[(original_space, target_space)]
        else:
            if original_space == 'rgb' or target_space == 'rgb':
                conversion = getattr(self, f"{original_space}_to_{target_space}")
            else:
                try:
                    conversion = getattr(self, f"{original_space}_to_{target_space}") #TODO: register these better
                except AttributeError:
                    # send everything through RGB
                    conversion1 = getattr(self, f"{original_space}_to_rgb")
                    conversion2 = getattr(self, f"rgb_to_{target_space}")
                    conversion = lambda *c: conversion2(*conversion1(*c))
        return conversion(*color)

    xyz_to_rbg_array = [
        # exact-ish inverse of conversion matrix
        [
            670962301703 * (1000000 / 207056369298614928),
            -318277012021 * (1000000 / 207056369298614928),
            -103225121660 * (1000000 / 207056369298614928)
        ],
        [
            -200690410871 * (1000000 / 207056369298614928),
            388435678549 * (1000000 / 207056369298614928),
            8604419276 * (1000000 / 207056369298614928)
        ],
        [
            11521991063 * (1000000 / 207056369298614928),
            -42248058709 * (1000000 / 207056369298614928),
            218922991300 * (1000000 / 207056369298614928)
        ]
    ]
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
        # converted from https://www.easyrgb.com/en/math.php
        if not isinstance(self.xyz_to_rbg_array, np.ndarray):
            self.xyz_to_rbg_array = np.array(self.xyz_to_rbg_array)

        xyz = np.array([x, y, z]) / 100
        rgb = np.tensordot(self.xyz_to_rbg_array, xyz, axes=[0, 0])
        mask = rgb > 0.0031308
        rgb[mask] = 1.055*rgb[mask]**(1/2.4) - 0.055
        not_mask = np.logical_not(mask)
        rgb[not_mask] = rgb[not_mask] * 12.92
        return rgb * 255

    rgb_to_xyz_array = [ # just the inverse
        [0.412453, 0.357580, 0.180423],
        [0.212671, 0.715160, 0.072169],
        [0.019334, 0.119193, 0.950227],
    ]
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
        if not isinstance(self.rgb_to_xyz_array, np.ndarray):
            self.rgb_to_xyz_array = np.array(self.rgb_to_xyz_array)

        rgb = np.array([r, g, b]) / 255
        mask = rgb > 0.04045
        rgb[mask] = ((rgb[mask] + 0.055) / 1.055)**(2.4)
        not_mask = np.logical_not(mask)
        rgb[not_mask] = rgb[not_mask] / 12.92

        xyz = np.tensordot(self.rgb_to_xyz_array, rgb, axes=[0, 0])
        return xyz * 100

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

        diff_r, diff_g, diff_b = [
            ((max_val - c) / 6 + (diff / 2)) / diff
            for c in rgb
        ]
        r_primary, g_primary, b_primary = [
            max_val == c
            for c in rgb
        ]

        h = np.zeros_like(diff)
        h[r_primary] = (diff_b[r_primary,] - diff_g[r_primary,])
        h[g_primary] = (1 / 3 + diff_r[g_primary,] - diff_b[g_primary,])
        h[b_primary] = (2 / 3 + diff_g[b_primary,] - diff_r[b_primary,])

        h[h < 0] += 1
        h[h > 1] -= 1

        return h
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

        rgb = np.array([r, g, b]) / 255
        smol = rgb.ndim == 1
        if smol:
            rgb = rgb[:, np.newaxis]
        base_shape = rgb.shape[1:]
        rgb = rgb.reshape(3, -1)

        min_val = np.min(rgb, axis=0)
        max_val = np.max(rgb, axis=0)
        diff = max_val - min_val

        L = (max_val + min_val) / 2

        non_gray = diff > 0
        s = np.zeros_like(L)
        h = np.zeros_like(L)
        if non_gray.any():
            s[non_gray] = (diff[non_gray] / (2 - (max_val[non_gray] + min_val[non_gray])))
            dim_mask = np.logical_and(non_gray, L < .5)
            s[dim_mask] = (diff[dim_mask] / (max_val[dim_mask] + min_val[dim_mask]))

            h_ = self._rgb2hue(rgb[:, non_gray], diff[non_gray], max_val[non_gray])
            h[non_gray] = h_

        hsl = np.array([h, s, L])
        hsl = hsl.reshape((3,) + base_shape)
        if smol:
            hsl = hsl[:, 0]

        return hsl

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

        h = np.array(h)
        v1 = np.array(v1)
        v2 = np.array(v2)
        h[h < 0] += 1
        h[h > 1] -= 1

        res = v1.copy()
        mask = 6*h < 1
        res[mask] = v1[mask] + (v2[mask] - v1[mask]) * 6*h[mask]
        rem = np.logical_not(mask)
        mask = np.logical_and(rem, 2*h < 1)
        res[mask] = v2[mask]
        rem = np.logical_and(rem, np.logical_not(mask))
        mask = np.logical_and(rem, 3*h < 2)
        res[mask] = v1[mask] + (v2[mask] - v1[mask]) * 6*(2/3 - h[mask])

        return res

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

        hsl = np.array([h, s, l])
        smol = hsl.ndim == 1
        if smol:
            hsl = hsl[:, np.newaxis]
        base_shape = hsl.shape[1:]
        hsl = hsl.reshape((3,-1))

        non_gray = hsl[1] > 0
        dim = np.logical_and(non_gray, hsl[2] < .5)

        rgb = np.zeros_like(hsl)
        if non_gray.any():
            h, s, L = hsl
            v2 = np.zeros_like(h)
            v2[non_gray] = ((L + s) - (s * L))[non_gray]
            v2[dim] = (L * (1 + s))[dim]

            v1 = np.zeros_like(h)
            v1[non_gray] = 2 * L[non_gray] - v2[non_gray]

            for i,shift in enumerate([1/3, 0, -1/3]):
                rgb[i, non_gray] = cls._hue2rgb(v1[non_gray], v2[non_gray], h[non_gray] + shift)

        gray = np.logical_not(non_gray)
        for i in range(3):
            rgb[i, gray] = hsl[2, gray]

        rgb = rgb.reshape((3,) + base_shape)
        if smol:
            rgb = rgb[:, 0]

        return rgb * 255

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

        rgb = np.array([r, g, b]) / 255
        smol = rgb.ndim == 1
        if smol:
            rgb = rgb[:, np.newaxis]
        base_shape = rgb.shape[1:]
        rgb = rgb.reshape((3, -1))

        min_val = np.min(rgb, axis=0)
        max_val = np.max(rgb, axis=0)
        diff = max_val - min_val

        v = max_val

        non_gray = diff > 0
        s = np.zeros_like(v)
        h = np.zeros_like(v)
        if non_gray.any():
            s[non_gray] = (diff[non_gray] / max_val[non_gray])
            h_ = self._rgb2hue(rgb[:, non_gray], diff[non_gray], max_val[non_gray])
            h[non_gray] = h_

        hsl = np.array([h, s, v])
        hsl = hsl.reshape((3,) + base_shape)
        if smol:
            hsl = hsl[:, 0]

        return hsl

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

        hsv = np.array([h, s, v])
        smol = hsv.ndim == 1
        if smol:
            hsv = hsv[:, np.newaxis]
        base_shape = hsv.shape[1:]
        hsv = hsv.reshape((3, -1))

        h, s, v = hsv
        max_val = np.array(v)
        diff = max_val * np.array(s)
        min_val = max_val - diff

        L = (max_val + min_val) / 2

        non_gray = diff > 0
        s = np.zeros_like(L)
        if non_gray.any():
            s[non_gray] = (diff[non_gray] / (2 - (max_val[non_gray] + min_val[non_gray])))
            dim_mask = np.logical_and(non_gray, L < .5)
            s[dim_mask] = (diff[dim_mask] / (max_val[dim_mask] + min_val[dim_mask]))

        hsl = np.array([h, s, L])
        hsl = hsl.reshape((3,) + base_shape)
        if smol:
            hsl = hsl[:, 0]

        return hsl

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
        return cls.hsl_to_rgb(*cls.hsv_to_hsl(h, s, v))

    lab_scaling_reference = [95.0489, 100.0, 108.8840]
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

        xyz = np.array([x, y, z])
        smol = xyz.ndim == 1
        if smol:
            xyz = xyz[:, np.newaxis]
        base_shape = xyz.shape[1:]
        xyz = xyz.reshape((3, -1))

        if scaling is None:
            scaling = cls.lab_scaling_reference

        xyz /= np.array(scaling)[:, np.newaxis]

        mask = xyz > 0.008856
        xyz[mask] = xyz[mask] ** (1/3)
        not_max = np.logical_not(mask)
        xyz[not_max] = (7.787 * xyz[not_max]) + (16/116)

        L = 116 * xyz[1] - 16
        a = 500 * (xyz[0] - xyz[1])
        b = 200 * (xyz[1] - xyz[2])

        lab = np.array([L, a, b])
        lab = lab.reshape((3,) + base_shape)
        if smol:
            lab = lab[:, 0]

        return lab

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

        lab = np.array([l, a, b])
        smol = lab.ndim == 1
        if smol:
            lab = lab[:, np.newaxis]
        base_shape = lab.shape[1:]
        lab = lab.reshape((3, -1))

        if scaling is None:
            scaling = cls.lab_scaling_reference

        y = (lab[0] + 16) / 116
        x = lab[1] / 500 + y
        z = y - lab[2] / 200

        xyz = np.array([x, y, z])

        mask = xyz**3 > 0.008856
        xyz[mask] = xyz[mask] ** (3)
        not_max = np.logical_not(mask)
        xyz[not_max] = (xyz[not_max] - (16/116)) / 7.787

        xyz *= np.array(scaling)[:, np.newaxis]
        xyz = xyz.reshape((3,) + base_shape)
        if smol:
            xyz = xyz[:, 0]

        return xyz

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
        c = np.linalg.norm([a, b], axis=0)
        h = np.arctan2(b, a)
        return np.array([l, c, h])
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
        return np.array([
            l,
            np.cos(h) * c,
            np.sin(h) * c
        ])
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
        return cls.xyz_to_lab(*cls.rgb_to_xyz(r, g, b), scaling=xyz_scaling)
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
        return cls.xyz_to_rgb(*cls.lab_to_xyz(l, a, b, scaling=xyz_scaling))

def prep_color(
        base=None,
        palette=None,
        blending=None,
        index=None,
        lighten=None,
        saturate=None,
        modifier=None,
        shift=False,
        absolute=False,
        clip=True,
        color_space='rgb',
        modification_space='lab',
        return_color_code=True,
        alpha=None,
        cycle=None
):
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
    return ColorPalette.prep_color(
        base=base,
        palette=palette,
        blending=blending,
        index=index,
        lighten=lighten,
        saturate=saturate,
        modifier=modifier,
        shift=shift,
        absolute=absolute,
        clip=clip,
        color_space=color_space,
        modification_space=modification_space,
        return_color_code=return_color_code,
        cycle=cycle,
        alpha=alpha
    )
