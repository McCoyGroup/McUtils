## <a id="McUtils.Plots.Colors.ColorPalette">ColorPalette</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors.py#L17)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors.py#L17?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
converters: dict
xyz_to_rbg_array: list
rgb_to_xyz_array: list
lab_scaling_reference: list
```
<a id="McUtils.Plots.Colors.ColorPalette.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, colors, blend_spacings=None, lab_colors=None, color_space='rgb', cycle=False, return_color_codes=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors.py#L18)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors.py#L18?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a color palette from a list of colors (or a named colormap/colormap
callable), precomputing the color codes and their Lab-space values for blending.
  - `colors`: `Any`
    > the colors, a named palette/colormap, or a colormap callable
  - `blend_spacings`: `Any`
    > the abcissae the colors sit at for blending (evenly spaced if omitted)
  - `lab_colors`: `Any`
    > precomputed Lab values (computed if omitted)
  - `color_space`: `str`
    > the space the input colors are given in
  - `cycle`: `bool`
    > index into the palette cyclically
  - `return_color_codes`: `bool`
    > return hex color codes by default


<a id="McUtils.Plots.Colors.ColorPalette.__hash__" class="docs-object-method">&nbsp;</a> 
```python
__hash__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L51)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L51?message=Update%20Docs)]
</div>
**LLM Docstring**

Hash the palette by its type and color codes.
  - `:returns`: `int`
    > the hash


<a id="McUtils.Plots.Colors.ColorPalette.parse_color_string" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_color_string(cls, name: str, include_named_alpha=False, return_padding=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L77)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L77?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse a color string (named color, hex code, or matplotlib name) into an RGB(A)
value.
  - `name`: `str`
    > the color string
  - `include_named_alpha`: `bool`
    > keep the alpha channel of named colors
  - `return_padding`: `bool`
    > also return the per-channel hex padding
  - `:returns`: `_`
    > the RGB(A) value (and padding if requested)


<a id="McUtils.Plots.Colors.ColorPalette.prep_color_palette" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_color_palette(cls, colors, color_space='rgb', lab_colors=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L112)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L112?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize a palette's colors into hex color strings and their Lab values,
converting from the given color space as needed.
  - `colors`: `Any`
    > the palette colors (strings or numeric arrays)
  - `color_space`: `str`
    > the space the numeric colors are in
  - `lab_colors`: `Any`
    > precomputed Lab values
  - `:returns`: `tuple`
    > `(color_strings, lab_colors)`


<a id="McUtils.Plots.Colors.ColorPalette.prep_color" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_color(cls, base=None, palette=None, blending=None, index=None, lighten=None, saturate=None, modifier=None, shift=False, absolute=False, clip=True, color_space='rgb', modification_space='lab', return_color_code=True, cycle=None, alpha=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L151)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L151?message=Update%20Docs)]
</div>
**LLM Docstring**

Compose a color (or list of colors) from a base color or palette, optionally
indexing/blending the palette and applying saturate/lighten/modify/alpha
transformations.
  - `base`: `Any`
    > an explicit base color (or list); required if no palette
  - `palette`: `Any`
    > a palette to draw the base from
  - `blending`: `Any`
    > a blend amount to sample the palette at
  - `index`: `int | None`
    > a palette index to select
  - `lighten`: `Any`
    > a lighten amount
  - `saturate`: `Any`
    > a saturate amount
  - `modifier`: `Any`
    > a custom color-modification callback
  - `shift`: `bool`
    > apply modifications additively rather than multiplicatively
  - `absolute`: `bool`
    > set (rather than scale) the modified channel
  - `clip`: `bool`
    > clip the result into the valid range
  - `color_space`: `str`
    > the working color space
  - `modification_space`: `str`
    > the space modifications are applied in
  - `return_color_code`: `bool`
    > return hex codes
  - `cycle`: `Any`
    > cycle the palette when indexing
  - `alpha`: `Any`
    > an alpha value to apply
  - `:returns`: `_`
    > the composed color(s)


<a id="McUtils.Plots.Colors.ColorPalette.set_alpha" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
set_alpha(cls, b, alpha): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L254)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L254?message=Update%20Docs)]
</div>
**LLM Docstring**

Set the alpha channel on a color (hex code, named color, RGB array, or list of
colors).
  - `b`: `Any`
    > the color
  - `alpha`: `Any`
    > the alpha value
  - `:returns`: `_`
    > the color with alpha applied


<a id="McUtils.Plots.Colors.ColorPalette.resolve_color_palette" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_color_palette(cls, cmap_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L291)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L291?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a named palette to its color data, falling back to discretizing a
matplotlib colormap of that name.
  - `cmap_name`: `str`
    > the palette/colormap name
  - `:returns`: `_`
    > the palette color data


<a id="McUtils.Plots.Colors.ColorPalette.is_colormap_like" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_colormap_like(cls, cmap): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L312)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L312?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether an object is colormap-like (callable).
  - `cmap`: `Any`
    > the object
  - `:returns`: `bool`
    > whether it's colormap-like


<a id="McUtils.Plots.Colors.ColorPalette.discretize_colormap" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
discretize_colormap(cls, cmap, samples=10): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L324)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L324?message=Update%20Docs)]
</div>
**LLM Docstring**

Sample a colormap at evenly-spaced points to produce a discrete palette.
  - `cmap`: `Any`
    > the colormap (or `ColorPalette`)
  - `samples`: `int`
    > the number of samples
  - `:returns`: `_`
    > the discrete colors


<a id="McUtils.Plots.Colors.ColorPalette.is_palette_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_palette_list(self, colors): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L342)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L342?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether an object is a valid palette list (a list of color strings or
numeric color arrays).
  - `colors`: `Any`
    > the object
  - `:returns`: `bool`
    > whether it's a palette list


<a id="McUtils.Plots.Colors.ColorPalette.flip" class="docs-object-method">&nbsp;</a> 
```python
flip(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L362)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L362?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a copy of the palette with its colors reversed.
  - `:returns`: `ColorPalette`
    > the reversed palette


<a id="McUtils.Plots.Colors.ColorPalette.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L373)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L373?message=Update%20Docs)]
</div>
**LLM Docstring**

Two palettes are equal if they have the same color codes.
  - `other`: `Any`
    > the object to compare against
  - `:returns`: `bool`
    > whether they are equal


<a id="McUtils.Plots.Colors.ColorPalette.get_colorblindness_test_url" class="docs-object-method">&nbsp;</a> 
```python
get_colorblindness_test_url(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L386)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L386?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a URL that previews the palette under color-blindness simulation.
  - `:returns`: `str`
    > the preview URL


<a id="McUtils.Plots.Colors.ColorPalette.blend" class="docs-object-method">&nbsp;</a> 
```python
blend(self, amount, modification_space='lab', rescale=False, clip=True, return_color_code=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L399)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L399?message=Update%20Docs)]
</div>
**LLM Docstring**

Interpolate the palette at one or more blend amounts, linearly interpolating in
the given space between the bracketing colors (clamping at the ends).
  - `amount`: `Any`
    > the blend amount(s) in `[0, 1]`
  - `modification_space`: `str`
    > the space to interpolate in
  - `rescale`: `bool`
    > rescale the numeric result (e.g. to `[0, 1]`)
  - `clip`: `bool`
    > clip the result into the valid range
  - `return_color_code`: `bool`
    > return hex codes rather than numeric colors
  - `:returns`: `_`
    > the blended color(s)


<a id="McUtils.Plots.Colors.ColorPalette.as_colormap" class="docs-object-method">&nbsp;</a> 
```python
as_colormap(self, levels=None, cmap_type='list', name=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L473)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L473?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a matplotlib colormap (listed or interpolated) from the palette.
  - `levels`: `Any`
    > the levels (count or explicit) to sample at
  - `cmap_type`: `str`
    > `'list'`, `'interpolated'`, or a colormap factory
  - `name`: `str | None`
    > the colormap name (auto-generated if omitted)
  - `opts`: `Any`
    > options for the colormap constructor
  - `:returns`: `_`
    > the colormap


<a id="McUtils.Plots.Colors.ColorPalette.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, amount, rescale=True, return_color_code=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L531)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L531?message=Update%20Docs)]
</div>
**LLM Docstring**

Sample the palette at a blend amount (delegates to `blend`).
  - `amount`: `Any`
    > the blend amount(s)
  - `rescale`: `bool`
    > rescale the numeric result
  - `return_color_code`: `bool`
    > return hex codes
  - `:returns`: `_`
    > the sampled color(s)


<a id="McUtils.Plots.Colors.ColorPalette.modify" class="docs-object-method">&nbsp;</a> 
```python
modify(self, modification_function, modification_space='lab', clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L546)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L546?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a new palette with a modification function applied to its Lab colors.
  - `modification_function`: `Callable`
    > the color-modification callback
  - `modification_space`: `str`
    > the space the modification acts in
  - `clip`: `bool`
    > clip the result
  - `:returns`: `ColorPalette`
    > the modified palette


<a id="McUtils.Plots.Colors.ColorPalette.lighten" class="docs-object-method">&nbsp;</a> 
```python
lighten(self, percentage, modification_space='lab', shift=False, absolute=False, clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L571)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L571?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a new palette lightened by the given amount.
  - `percentage`: `Any`
    > the lighten amount
  - `modification_space`: `str`
    > the space to lighten in
  - `shift`: `bool`
    > lighten additively
  - `absolute`: `bool`
    > set the lightness rather than scaling it
  - `clip`: `bool`
    > clip the result
  - `:returns`: `ColorPalette`
    > the lightened palette


<a id="McUtils.Plots.Colors.ColorPalette.color_normalize" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_normalize(cls, color_list, color_space='rgb'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L604)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L604?message=Update%20Docs)]
</div>
**LLM Docstring**

Clip color values into the valid range for their color space.
  - `color_list`: `Any`
    > the colors
  - `color_space`: `str`
    > the color space
  - `:returns`: `np.ndarray`
    > the clipped colors


<a id="McUtils.Plots.Colors.ColorPalette.color_rescale" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_rescale(cls, color_list, color_space='rgb'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L629)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L629?message=Update%20Docs)]
</div>
**LLM Docstring**

Rescale color values out of their integer range (RGB by 255, XYZ by 100).
  - `color_list`: `Any`
    > the colors
  - `color_space`: `str`
    > the color space
  - `:returns`: `np.ndarray`
    > the rescaled colors


<a id="McUtils.Plots.Colors.ColorPalette.color_modify" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_modify(cls, color, modification_function, color_space='rgb', modification_space='lab', clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L648)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L648?message=Update%20Docs)]
</div>
**LLM Docstring**

Apply a modification function to a single color, converting into the modification
space and back and optionally clipping.
  - `color`: `Any`
    > the color (hex code or numeric)
  - `modification_function`: `Callable`
    > the modification callback
  - `color_space`: `str`
    > the color's space
  - `modification_space`: `str`
    > the space to modify in
  - `clip`: `bool`
    > clip the result
  - `:returns`: `_`
    > the modified color


<a id="McUtils.Plots.Colors.ColorPalette.color_lighten" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_lighten(cls, color, percentage, color_space='rgb', modification_space='lab', shift=False, absolute=False, clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L686)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L686?message=Update%20Docs)]
</div>
**LLM Docstring**

Lighten a color by scaling/shifting/setting its lightness channel in the
modification space.
  - `color`: `Any`
    > the color
  - `percentage`: `Any`
    > the lighten amount
  - `color_space`: `str`
    > the color's space
  - `modification_space`: `str`
    > the space to lighten in (Lab or HSV/HSL)
  - `shift`: `bool`
    > lighten additively
  - `absolute`: `bool`
    > set the lightness rather than scaling
  - `clip`: `bool`
    > clip the result
  - `:returns`: `_`
    > the lightened color


<a id="McUtils.Plots.Colors.ColorPalette.color_saturate" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_saturate(cls, color, percentage, color_space='rgb', modification_space='hsv', shift=False, absolute=False, clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L733)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L733?message=Update%20Docs)]
</div>
**LLM Docstring**

Saturate a color by scaling/shifting/setting its saturation (chroma) in the
modification space.
  - `color`: `Any`
    > the color
  - `percentage`: `Any`
    > the saturate amount
  - `color_space`: `str`
    > the color's space
  - `modification_space`: `str`
    > the space to saturate in (HSV/HSL or Lab)
  - `shift`: `bool`
    > saturate additively
  - `absolute`: `bool`
    > set the saturation rather than scaling
  - `clip`: `bool`
    > clip the result
  - `:returns`: `_`
    > the saturated color


<a id="McUtils.Plots.Colors.ColorPalette.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L820)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L820?message=Update%20Docs)]
</div>
**LLM Docstring**

The number of colors in the palette.
  - `:returns`: `int`
    > the color count


<a id="McUtils.Plots.Colors.ColorPalette.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L830)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L830?message=Update%20Docs)]
</div>
**LLM Docstring**

Index the palette by an integer (a single color, cycling if enabled) or a
slice/array (a sub-palette).
  - `item`: `Any`
    > the index or slice
  - `:returns`: `_`
    > the color or sub-palette


<a id="McUtils.Plots.Colors.ColorPalette.rgb_code" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_code(cls, rgb, padding=2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L853)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L853?message=Update%20Docs)]
</div>
**LLM Docstring**

Format an RGB value (or list of them) as a hex color code.
  - `rgb`: `Any`
    > the RGB value(s)
  - `padding`: `int`
    > the per-channel hex width
  - `:returns`: `str | list`
    > the hex code(s)


<a id="McUtils.Plots.Colors.ColorPalette.parse_rgb_code" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_rgb_code(cls, code, padding=None, return_padding=False, num_channels=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L873)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L873?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse a hex color code into an RGB(A) value, inferring the per-channel padding.
  - `code`: `str`
    > the hex code
  - `padding`: `int | None`
    > the per-channel hex width (inferred if omitted)
  - `return_padding`: `bool`
    > also return the inferred padding
  - `num_channels`: `int | None`
    > the expected number of channels
  - `:returns`: `_`
    > the RGB(A) value (and padding if requested)


<a id="McUtils.Plots.Colors.ColorPalette.color_convert" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_convert(self, color, original_space, target_space): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L926)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L926?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color between two color spaces, routing through the intermediate spaces
(e.g. RGB/XYZ/Lab/HSL/HSV) as needed.
  - `color`: `Any`
    > the color
  - `original_space`: `str`
    > the source space
  - `target_space`: `str`
    > the destination space
  - `:returns`: `np.ndarray`
    > the converted color


<a id="McUtils.Plots.Colors.ColorPalette.xyz_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
xyz_to_rgb(self, x, y, z): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L977)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L977?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from CIE XYZ to sRGB.
  - `x`: `Any`
    > the X channel
  - `y`: `Any`
    > the Y channel
  - `z`: `Any`
    > the Z channel
  - `:returns`: `np.ndarray`
    > the RGB color


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_xyz(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1007)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1007?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from sRGB to CIE XYZ.
  - `r`: `Any`
    > the red channel
  - `g`: `Any`
    > the green channel
  - `b`: `Any`
    > the blue channel
  - `:returns`: `np.ndarray`
    > the XYZ color


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_hsl" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_hsl(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1065)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1065?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from RGB to HSL.
  - `r`: `Any`
    > the red channel
  - `g`: `Any`
    > the green channel
  - `b`: `Any`
    > the blue channel
  - `:returns`: `np.ndarray`
    > the HSL color


<a id="McUtils.Plots.Colors.ColorPalette.hsl_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsl_to_rgb(cls, h, s, l): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1143)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1143?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from HSL to RGB.
  - `h`: `Any`
    > the hue
  - `s`: `Any`
    > the saturation
  - `l`: `Any`
    > the lightness
  - `:returns`: `np.ndarray`
    > the RGB color


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_hsv" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_hsv(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1190)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1190?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from RGB to HSV.
  - `r`: `Any`
    > the red channel
  - `g`: `Any`
    > the green channel
  - `b`: `Any`
    > the blue channel
  - `:returns`: `np.ndarray`
    > the HSV color


<a id="McUtils.Plots.Colors.ColorPalette.hsv_to_hsl" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsv_to_hsl(cls, h, s, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1232)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1232?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from HSV to HSL.
  - `h`: `Any`
    > the hue
  - `s`: `Any`
    > the saturation
  - `v`: `Any`
    > the value
  - `:returns`: `np.ndarray`
    > the HSL color


<a id="McUtils.Plots.Colors.ColorPalette.hsv_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsv_to_rgb(cls, h, s, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1274)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1274?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from HSV to RGB (via HSL).
  - `h`: `Any`
    > the hue
  - `s`: `Any`
    > the saturation
  - `v`: `Any`
    > the value
  - `:returns`: `np.ndarray`
    > the RGB color


<a id="McUtils.Plots.Colors.ColorPalette.xyz_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
xyz_to_lab(cls, x, y, z, scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1290)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1290?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from CIE XYZ to CIE Lab.
  - `x`: `Any`
    > the X channel
  - `y`: `Any`
    > the Y channel
  - `z`: `Any`
    > the Z channel
  - `scaling`: `Any`
    > the white-point scaling
  - `:returns`: `np.ndarray`
    > the Lab color


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_xyz(cls, l, a, b, scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1333)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1333?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from CIE Lab to CIE XYZ.
  - `l`: `Any`
    > the lightness channel
  - `a`: `Any`
    > the a channel
  - `b`: `Any`
    > the b channel
  - `scaling`: `Any`
    > the white-point scaling
  - `:returns`: `np.ndarray`
    > the XYZ color


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_lch" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_lch(cls, l, a, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1376)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1376?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from CIE Lab to CIE LCh.
  - `l`: `Any`
    > the lightness channel
  - `a`: `Any`
    > the a channel
  - `b`: `Any`
    > the b channel
  - `:returns`: `np.ndarray`
    > the LCh color


<a id="McUtils.Plots.Colors.ColorPalette.lch_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lch_to_lab(cls, l, c, h): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1392)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1392?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from CIE LCh to CIE Lab.
  - `l`: `Any`
    > the lightness channel
  - `c`: `Any`
    > the chroma channel
  - `h`: `Any`
    > the hue channel
  - `:returns`: `np.ndarray`
    > the Lab color


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_lab(cls, r, g, b, xyz_scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1410)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1410?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from RGB to CIE Lab (via XYZ).
  - `r`: `Any`
    > the red channel
  - `g`: `Any`
    > the green channel
  - `b`: `Any`
    > the blue channel
  - `xyz_scaling`: `Any`
    > the white-point scaling
  - `:returns`: `np.ndarray`
    > the Lab color


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_rgb(cls, l, a, b, xyz_scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1425)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1425?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a color from CIE Lab to RGB (via XYZ).
  - `l`: `Any`
    > the lightness channel
  - `a`: `Any`
    > the a channel
  - `b`: `Any`
    > the b channel
  - `xyz_scaling`: `Any`
    > the white-point scaling
  - `:returns`: `np.ndarray`
    > the RGB color
 </div>
</div>












---


<div markdown="1" class="text-secondary">
<div class="container">
  <div class="row">
   <div class="col" markdown="1">
**Feedback**   
</div>
   <div class="col" markdown="1">
**Examples**   
</div>
   <div class="col" markdown="1">
**Templates**   
</div>
   <div class="col" markdown="1">
**Documentation**   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Bug](https://github.com/McCoyGroup/McUtils/issues/new?title=Documentation%20Improvement%20Needed)/[Request](https://github.com/McCoyGroup/McUtils/issues/new?title=Example%20Request)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Colors/ColorPalette.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Colors/ColorPalette.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Colors/ColorPalette.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Colors/ColorPalette.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors.py#L17?message=Update%20Docs)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>
</div>