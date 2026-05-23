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
__init__(self, colors, blend_spacings=None, lab_colors=None, color_space='rgb', cycle=False): 
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L32?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.parse_color_string" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_color_string(cls, name: str, include_named_alpha=False, return_padding=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L40)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L40?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.prep_color_palette" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_color_palette(cls, colors, color_space='rgb', lab_colors=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L61)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L61?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.prep_color" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_color(cls, base=None, palette=None, blending=None, index=None, lighten=None, saturate=None, modifier=None, shift=False, absolute=False, clip=True, color_space='rgb', modification_space='lab', return_color_code=True, cycle=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L87)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L87?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.resolve_color_palette" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_color_palette(cls, cmap_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L155)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L155?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.is_colormap_like" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_colormap_like(cls, cmap): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L166)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L166?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.discretize_colormap" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
discretize_colormap(cls, cmap, samples=10): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L169?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.is_palette_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_palette_list(self, colors): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L177)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L177?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.flip" class="docs-object-method">&nbsp;</a> 
```python
flip(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L187)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L187?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L190)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L190?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.get_colorblindness_test_url" class="docs-object-method">&nbsp;</a> 
```python
get_colorblindness_test_url(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L194)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L194?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.blend" class="docs-object-method">&nbsp;</a> 
```python
blend(self, amount, modification_space='lab', rescale=False, clip=True, return_color_code=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L199)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L199?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.as_colormap" class="docs-object-method">&nbsp;</a> 
```python
as_colormap(self, levels=None, cmap_type='list', name=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L256)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L256?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, amount, rescale=True, return_color_code=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L301)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L301?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.modify" class="docs-object-method">&nbsp;</a> 
```python
modify(self, modification_function, modification_space='lab', clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L304?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lighten" class="docs-object-method">&nbsp;</a> 
```python
lighten(self, percentage, modification_space='lab', shift=False, absolute=False, clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L315)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L315?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_normalize" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_normalize(cls, color_list, color_space='rgb'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L331)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L331?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_rescale" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_rescale(cls, color_list, color_space='rgb'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L345)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L345?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_modify" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_modify(cls, color, modification_function, color_space='rgb', modification_space='lab', clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L353)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L353?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_lighten" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_lighten(cls, color, percentage, color_space='rgb', modification_space='lab', shift=False, absolute=False, clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L374)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L374?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_saturate" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_saturate(cls, color, percentage, color_space='rgb', modification_space='hsv', shift=False, absolute=False, clip=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L400)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L400?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L442)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L442?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors/ColorPalette.py#L444)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors/ColorPalette.py#L444?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_code" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_code(cls, rgb, padding=2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L458)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L458?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.parse_rgb_code" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_rgb_code(cls, code, padding=None, return_padding=False, num_channels=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L467)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L467?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.color_convert" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
color_convert(self, color, original_space, target_space): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L505)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L505?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.xyz_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
xyz_to_rgb(self, x, y, z): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L542)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L542?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_xyz(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L561)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L561?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_hsl" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_hsl(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L596)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L596?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.hsl_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsl_to_rgb(cls, h, s, l): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L651)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L651?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_hsv" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_hsv(self, r, g, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L687)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L687?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.hsv_to_hsl" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsv_to_hsl(cls, h, s, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L718)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L718?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.hsv_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
hsv_to_rgb(cls, h, s, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L749)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L749?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.xyz_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
xyz_to_lab(cls, x, y, z, scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L754)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L754?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_xyz(cls, l, a, b, scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L785)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L785?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_lch" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_lch(cls, l, a, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L816)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L816?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lch_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lch_to_lab(cls, l, c, h): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L821)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L821?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.rgb_to_lab" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
rgb_to_lab(cls, r, g, b, xyz_scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L828)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L828?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Colors.ColorPalette.lab_to_rgb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lab_to_rgb(cls, l, a, b, xyz_scaling=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L831)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L831?message=Update%20Docs)]
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