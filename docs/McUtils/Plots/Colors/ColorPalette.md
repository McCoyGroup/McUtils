## <a id="McUtils.Plots.Colors.ColorPalette">ColorPalette</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors.py#L16?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
named_colors: dict
converters: dict
xyz_to_rbg_array: list
rgb_to_xyz_array: list
lab_scaling_reference: list
```
<a id="McUtils.Plots.Colors.ColorPalette.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, colors, blend_spacings=None, lab_colors=None, color_space='rgb', cycle=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors.py#L17)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors.py#L17?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__hash__" class="docs-object-method">&nbsp;</a> 
```python
__hash__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L31)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L31?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.parse_color_string" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_color_string(cls, name: str, include_named_alpha=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L35)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L35?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.prep_color_palette" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_color_palette(cls, colors, color_space='rgb', lab_colors=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L51)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L51?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.prep_color" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_color(cls, base=None, palette=None, blending=None, index=None, lighten=None, modifier=None, shift=False, absolute=False, clip=True, color_space='rgb', modification_space='lab', return_color_code=True, cycle=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L77)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L77?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.resolve_color_palette" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_color_palette(cls, cmap_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L136)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L136?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.is_colormap_like" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_colormap_like(cls, cmap): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L147)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L147?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.discretize_colormap" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
discretize_colormap(cls, cmap, samples=10): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L150)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L150?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.is_palette_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_palette_list(self, colors): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L158)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L158?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.flip" class="docs-object-method">&nbsp;</a> 
```python
flip(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L168)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L168?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L171)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L171?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.get_colorblindness_test_url" class="docs-object-method">&nbsp;</a> 
```python
get_colorblindness_test_url(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L175?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.blend" class="docs-object-method">&nbsp;</a> 
```python
blend(self, amount, modification_space='lab', rescale=False, clip=True, return_color_code=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L180)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L180?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.as_colormap" class="docs-object-method">&nbsp;</a> 
```python
as_colormap(self, levels=None, cmap_type='list', name=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L237)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L237?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, amount, rescale=True, return_color_code=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L282)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L282?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.modify" class="docs-object-method">&nbsp;</a> 
```python
modify(self, modification_function, modification_space='lab', clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L285)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L285?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lighten" class="docs-object-method">&nbsp;</a> 
```python
lighten(self, percentage, modification_space='lab', shift=False, absolute=False, clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L296)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L296?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_normalize" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_normalize(cls, color_list, color_space='rgb'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L312)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L312?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_rescale" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_rescale(cls, color_list, color_space='rgb'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L326)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L326?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_modify" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_modify(cls, color, modification_function, color_space='rgb', modification_space='lab', clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L334)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L334?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_lighten" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_lighten(cls, color, percentage, color_space='rgb', modification_space='lab', shift=False, absolute=False, clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L355)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L355?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L382)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L382?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L384)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L384?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_code" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_code(cls, rgb, padding=2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L398)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L398?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.parse_rgb_code" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_rgb_code(cls, code, padding=None, return_padding=False, num_channels=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L407)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L407?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_convert" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_convert(self, color, original_space, target_space): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L445)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L445?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.xyz_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
xyz_to_rgb(self, x, y, z): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L482)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L482?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_xyz(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L501)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L501?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_hsl" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_hsl(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L536)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L536?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.hsl_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsl_to_rgb(cls, h, s, l): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L591)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L591?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_hsv" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_hsv(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L627)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L627?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.hsv_to_hsl" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsv_to_hsl(cls, h, s, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L658)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L658?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.hsv_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsv_to_rgb(cls, h, s, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L689)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L689?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.xyz_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
xyz_to_lab(cls, x, y, z, scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L694)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L694?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_xyz(cls, l, a, b, scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L725)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L725?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_lch" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_lch(cls, l, a, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L756)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L756?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lch_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lch_to_lab(cls, l, c, h): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L761)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L761?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_lab(cls, r, g, b, xyz_scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L768)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L768?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_rgb(cls, l, a, b, xyz_scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L771)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L771?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors.py#L16?message=Update%20Docs)   
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