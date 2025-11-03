## <a id="McUtils.Plots.Graphics.Graphics">Graphics</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics.py#L902)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L902?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse " id="methods" markdown="1">
 ```python
default_style: dict
axes_keys: set
figure_keys: set
layout_keys: set
known_keys: set
padding_line_height: int
inset_options: dict
```
<a id="McUtils.Plots.Graphics.Graphics.set_options" class="docs-object-method">&nbsp;</a> 
```python
set_options(self, axes_labels=None, plot_label=None, style_list=None, plot_range=None, plot_legend=None, legend_style=None, frame=None, frame_style=None, ticks=None, scale=None, padding=None, spacings=None, ticks_style=None, ticks_label_style=None, image_size=None, axes_bbox=None, aspect_ratio=None, background=None, colorbar=None, prolog=None, epilog=None, **parent_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L939)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L939?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.get_plot_label_padding" class="docs-object-method">&nbsp;</a> 
```python
get_plot_label_padding(self, plot_label): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L998)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L998?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.get_axes_label_padding" class="docs-object-method">&nbsp;</a> 
```python
get_axes_label_padding(self, axes_labels): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1004)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1004?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.resolve_default_padding" class="docs-object-method">&nbsp;</a> 
```python
resolve_default_padding(self, padding, modifications=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1015)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1015?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.artists" class="docs-object-method">&nbsp;</a> 
```python
@property
artists(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1065)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1065?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.plot_label" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_label(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1070)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1070?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.style_list" class="docs-object-method">&nbsp;</a> 
```python
@property
style_list(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1079)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1079?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.plot_legend" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_legend(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1087)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1087?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.legend_style" class="docs-object-method">&nbsp;</a> 
```python
@property
legend_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1095)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1095?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.axes_labels" class="docs-object-method">&nbsp;</a> 
```python
@property
axes_labels(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1103)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1103?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.frame" class="docs-object-method">&nbsp;</a> 
```python
@property
frame(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1111)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1111?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.frame_style" class="docs-object-method">&nbsp;</a> 
```python
@property
frame_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1119?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.plot_range" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_range(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1127)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1127?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.ticks" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1135)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1135?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.ticks_style" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1143)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1143?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.ticks_label_style" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks_label_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1151)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1151?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.scale" class="docs-object-method">&nbsp;</a> 
```python
@property
scale(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1159)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1159?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.axes_bbox" class="docs-object-method">&nbsp;</a> 
```python
@property
axes_bbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1167)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1167?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.aspect_ratio" class="docs-object-method">&nbsp;</a> 
```python
@property
aspect_ratio(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1175?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.image_size" class="docs-object-method">&nbsp;</a> 
```python
@property
image_size(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1183?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.figure_label" class="docs-object-method">&nbsp;</a> 
```python
@property
figure_label(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1191?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.padding" class="docs-object-method">&nbsp;</a> 
```python
@property
padding(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1199)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1199?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.padding_left" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_left(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1206)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1206?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.padding_right" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_right(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1213)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1213?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.padding_top" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_top(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1220)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1220?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.padding_bottom" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_bottom(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1227)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1227?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.spacings" class="docs-object-method">&nbsp;</a> 
```python
@property
spacings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1235)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1235?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.background" class="docs-object-method">&nbsp;</a> 
```python
@property
background(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1243)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1243?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.colorbar" class="docs-object-method">&nbsp;</a> 
```python
@property
colorbar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1251)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1251?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.get_padding_offsets" class="docs-object-method">&nbsp;</a> 
```python
get_padding_offsets(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1273)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1273?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.get_bbox" class="docs-object-method">&nbsp;</a> 
```python
get_bbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1287?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Graphics.Graphics.create_inset" class="docs-object-method">&nbsp;</a> 
```python
create_inset(self, bbox, coordinates='absolute', graphics_class=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1305)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1305?message=Update%20Docs)]
</div>
 </div>
</div>




## Examples
The `Graphics` object is a simple interface to the [matplotlib.figure.Figure
](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure) class. 
This is bound to the `figure` attribute of the object.

```python
from McUtils.Plots import *

g = Graphics()
type(g.figure)

# Out: matplotlib.figure.Figure
```

Each `Graphics` object also binds an [matplotlib.axes.Axes](https://matplotlib.org/3.1.1/api/axes_api.html#the-axes-class) object.
Because of this, the framework is set up so that multiple `Graphics` objects can
 use the same underlying `figure`:
 
 ```python
g = Graphics()
f = Graphics(figure=g)
g.figure is f.figure

# Out: True
```

Usually one won't use `Graphics` on its own, but will instead use on of the
other plotting functions, such as `Plot` or `ContourPlot` to create a
`Graphics` object.






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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Graphics/Graphics.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Graphics/Graphics.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Graphics/Graphics.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Graphics/Graphics.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L902?message=Update%20Docs)   
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