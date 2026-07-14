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


<a id="McUtils.Plots.Colors.ColorPalette.__hash__" class="docs-object-method">&nbsp;</a> 
```python
__hash__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L34)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L34?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.parse_color_string" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_color_string(cls, name: str, include_named_alpha=False, return_padding=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L42)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L42?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.prep_color_palette" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_color_palette(cls, colors, color_space='rgb', lab_colors=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L63)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L63?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.prep_color" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_color(cls, base=None, palette=None, blending=None, index=None, lighten=None, saturate=None, modifier=None, shift=False, absolute=False, clip=True, color_space='rgb', modification_space='lab', return_color_code=True, cycle=None, alpha=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L89)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L89?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.set_alpha" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
set_alpha(cls, b, alpha): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L160)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L160?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.resolve_color_palette" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_color_palette(cls, cmap_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L187)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L187?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.is_colormap_like" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_colormap_like(cls, cmap): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L198)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L198?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.discretize_colormap" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
discretize_colormap(cls, cmap, samples=10): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L201)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L201?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.is_palette_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_palette_list(self, colors): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L209)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L209?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.flip" class="docs-object-method">&nbsp;</a> 
```python
flip(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L219)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L219?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L222)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L222?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.get_colorblindness_test_url" class="docs-object-method">&nbsp;</a> 
```python
get_colorblindness_test_url(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L226)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L226?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.blend" class="docs-object-method">&nbsp;</a> 
```python
blend(self, amount, modification_space='lab', rescale=False, clip=True, return_color_code=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L231)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L231?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.as_colormap" class="docs-object-method">&nbsp;</a> 
```python
as_colormap(self, levels=None, cmap_type='list', name=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L288)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L288?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, amount, rescale=True, return_color_code=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L333)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L333?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.modify" class="docs-object-method">&nbsp;</a> 
```python
modify(self, modification_function, modification_space='lab', clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L336)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L336?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lighten" class="docs-object-method">&nbsp;</a> 
```python
lighten(self, percentage, modification_space='lab', shift=False, absolute=False, clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L347)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L347?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_normalize" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_normalize(cls, color_list, color_space='rgb'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L363)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L363?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_rescale" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_rescale(cls, color_list, color_space='rgb'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L377)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L377?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_modify" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_modify(cls, color, modification_function, color_space='rgb', modification_space='lab', clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L385)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L385?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_lighten" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_lighten(cls, color, percentage, color_space='rgb', modification_space='lab', shift=False, absolute=False, clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L406)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L406?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_saturate" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_saturate(cls, color, percentage, color_space='rgb', modification_space='hsv', shift=False, absolute=False, clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L432)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L432?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L474)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L474?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L476)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L476?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_code" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_code(cls, rgb, padding=2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L490)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L490?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.parse_rgb_code" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_rgb_code(cls, code, padding=None, return_padding=False, num_channels=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L499)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L499?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_convert" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_convert(self, color, original_space, target_space): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L537)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L537?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.xyz_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
xyz_to_rgb(self, x, y, z): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L574)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L574?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_xyz(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L593)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L593?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_hsl" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_hsl(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L628)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L628?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.hsl_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsl_to_rgb(cls, h, s, l): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L683)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L683?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_hsv" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_hsv(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L719)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L719?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.hsv_to_hsl" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsv_to_hsl(cls, h, s, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L750)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L750?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.hsv_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsv_to_rgb(cls, h, s, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L781)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L781?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.xyz_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
xyz_to_lab(cls, x, y, z, scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L786)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L786?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_xyz(cls, l, a, b, scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L817)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L817?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_lch" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_lch(cls, l, a, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L848)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L848?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lch_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lch_to_lab(cls, l, c, h): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L853)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L853?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_lab(cls, r, g, b, xyz_scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L860)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L860?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_rgb(cls, l, a, b, xyz_scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L863)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L863?message=Update%20Docs)]
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