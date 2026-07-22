## <a id="McUtils.Plots.Graphics.Graphics">Graphics</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics.py#L1320)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L1320?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
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
set_options(self, axes_labels=None, plot_label=None, style_list=None, plot_range=None, plot_legend=None, legend_style=None, frame=None, frame_style=None, grid=None, grid_style=None, ticks=None, scale=None, padding=None, spacings=None, ticks_style=None, ticks_label_style=None, image_size=None, axes_bbox=None, aspect_ratio=None, background=None, colorbar=None, prolog=None, epilog=None, theme=None, **parent_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1356)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1356?message=Update%20Docs)]
</div>
**LLM Docstring**

Set the plot's styling and layout options (labels, legend, frame, ticks, range,
scale, padding, spacings, background, colorbar, etc.), resolving defaults and
applying each non-`None` value.
  - `axes_labels`: `Any`
    > the axis labels
  - `plot_label`: `Any`
    > the plot title
  - `style_list`: `Any`
    > the per-series style cycle
  - `plot_range`: `Any`
    > the plotted data range
  - `plot_legend`: `Any`
    > the legend (or legend spec)
  - `legend_style`: `Any`
    > legend styling
  - `frame`: `Any`
    > which frame edges to draw
  - `frame_style`: `Any`
    > frame styling
  - `ticks`: `Any`
    > the tick specification
  - `scale`: `Any`
    > the axis scaling
  - `padding`: `Any`
    > the figure padding
  - `spacings`: `Any`
    > the panel spacings
  - `ticks_style`: `Any`
    > tick styling
  - `ticks_label_style`: `Any`
    > tick-label styling
  - `image_size`: `Any`
    > the image size
  - `axes_bbox`: `Any`
    > the axes bounding box
  - `aspect_ratio`: `Any`
    > the aspect ratio
  - `background`: `Any`
    > the background color
  - `colorbar`: `Any`
    > the colorbar spec
  - `prolog`: `Any`
    > prolog primitives
  - `epilog`: `Any`
    > epilog primitives
  - `parent_opts`: `Any`
    > options forwarded to the base class


<a id="McUtils.Plots.Graphics.Graphics.get_plot_label_padding" class="docs-object-method">&nbsp;</a> 
```python
get_plot_label_padding(self, plot_label): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1453)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1453?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the extra padding needed to fit a plot label (top padding when a label is
present).
  - `plot_label`: `Any`
    > the plot label (or `None`)
  - `:returns`: `list`
    > the `((left, right), (bottom, top))` padding contribution


<a id="McUtils.Plots.Graphics.Graphics.get_axes_label_padding" class="docs-object-method">&nbsp;</a> 
```python
get_axes_label_padding(self, axes_labels): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1469)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1469?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the extra padding needed to fit the axis labels (left/bottom padding for
the y/x labels).
  - `axes_labels`: `Any`
    > the axis labels (or `None`)
  - `:returns`: `list`
    > the `((left, right), (bottom, top))` padding contribution


<a id="McUtils.Plots.Graphics.Graphics.resolve_default_padding" class="docs-object-method">&nbsp;</a> 
```python
resolve_default_padding(self, padding, modifications=None, theme=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1490)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1490?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve the final padding by filling unset sides from the default style and
adding the supplied label-padding modifications.
  - `padding`: `Any`
    > the requested padding (or `None`)
  - `modifications`: `list | None`
    > per-side padding contributions to add
  - `:returns`: `tuple`
    > the resolved `((left, right), (bottom, top))` padding


<a id="McUtils.Plots.Graphics.Graphics.artists" class="docs-object-method">&nbsp;</a> 
```python
@property
artists(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1562)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1562?message=Update%20Docs)]
</div>
**LLM Docstring**

The plot's artist objects (empty for the base `Graphics`).
  - `:returns`: `list`
    > the artists


<a id="McUtils.Plots.Graphics.Graphics.plot_label" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_label(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1575)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1575?message=Update%20Docs)]
</div>
**LLM Docstring**

The plot title/label. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the plot label value


<a id="McUtils.Plots.Graphics.Graphics.style_list" class="docs-object-method">&nbsp;</a> 
```python
@property
style_list(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1600)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1600?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-series style cycle (shared with the parent). Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the style list value


<a id="McUtils.Plots.Graphics.Graphics.plot_legend" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_legend(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1624)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1624?message=Update%20Docs)]
</div>
**LLM Docstring**

The plot legend (or legend spec). Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the plot legend value


<a id="McUtils.Plots.Graphics.Graphics.legend_style" class="docs-object-method">&nbsp;</a> 
```python
@property
legend_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1648)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1648?message=Update%20Docs)]
</div>
**LLM Docstring**

The legend styling options. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the legend style value


<a id="McUtils.Plots.Graphics.Graphics.axes_labels" class="docs-object-method">&nbsp;</a> 
```python
@property
axes_labels(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1672)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1672?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-axis labels. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the axes labels value


<a id="McUtils.Plots.Graphics.Graphics.frame" class="docs-object-method">&nbsp;</a> 
```python
@property
frame(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1696)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1696?message=Update%20Docs)]
</div>
**LLM Docstring**

Which frame (spine) edges are drawn. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the frame value


<a id="McUtils.Plots.Graphics.Graphics.frame_style" class="docs-object-method">&nbsp;</a> 
```python
@property
frame_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1720)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1720?message=Update%20Docs)]
</div>
**LLM Docstring**

The frame styling options. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the frame style value


<a id="McUtils.Plots.Graphics.Graphics.grid" class="docs-object-method">&nbsp;</a> 
```python
@property
grid(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1744)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1744?message=Update%20Docs)]
</div>
**LLM Docstring**

Which frame (spine) edges are drawn. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the frame value


<a id="McUtils.Plots.Graphics.Graphics.grid_style" class="docs-object-method">&nbsp;</a> 
```python
@property
grid_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1768)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1768?message=Update%20Docs)]
</div>
**LLM Docstring**

The frame styling options. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the frame style value


<a id="McUtils.Plots.Graphics.Graphics.plot_range" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_range(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1792)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1792?message=Update%20Docs)]
</div>
**LLM Docstring**

The plotted data range per axis. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the plot range value


<a id="McUtils.Plots.Graphics.Graphics.ticks" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1816)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1816?message=Update%20Docs)]
</div>
**LLM Docstring**

The tick locations/specification. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the ticks value


<a id="McUtils.Plots.Graphics.Graphics.ticks_style" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1840)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1840?message=Update%20Docs)]
</div>
**LLM Docstring**

The tick styling options. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the ticks style value


<a id="McUtils.Plots.Graphics.Graphics.ticks_label_style" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks_label_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1864)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1864?message=Update%20Docs)]
</div>
**LLM Docstring**

The tick-label styling options. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the tick-label style value


<a id="McUtils.Plots.Graphics.Graphics.scale" class="docs-object-method">&nbsp;</a> 
```python
@property
scale(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1888)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1888?message=Update%20Docs)]
</div>
**LLM Docstring**

The axis scaling (e.g. linear/log). Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the scale value


<a id="McUtils.Plots.Graphics.Graphics.axes_bbox" class="docs-object-method">&nbsp;</a> 
```python
@property
axes_bbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1912)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1912?message=Update%20Docs)]
</div>
**LLM Docstring**

The axes bounding box within the figure. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the axes bbox value


<a id="McUtils.Plots.Graphics.Graphics.aspect_ratio" class="docs-object-method">&nbsp;</a> 
```python
@property
aspect_ratio(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1936)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1936?message=Update%20Docs)]
</div>
**LLM Docstring**

The axes aspect ratio. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the aspect ratio value


<a id="McUtils.Plots.Graphics.Graphics.image_size" class="docs-object-method">&nbsp;</a> 
```python
@property
image_size(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1960)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1960?message=Update%20Docs)]
</div>
**LLM Docstring**

The figure image size in pixels. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the image size value


<a id="McUtils.Plots.Graphics.Graphics.figure_label" class="docs-object-method">&nbsp;</a> 
```python
@property
figure_label(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L1984)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L1984?message=Update%20Docs)]
</div>
**LLM Docstring**

The overall figure label. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the figure label value


<a id="McUtils.Plots.Graphics.Graphics.padding" class="docs-object-method">&nbsp;</a> 
```python
@property
padding(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L2008)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L2008?message=Update%20Docs)]
</div>
**LLM Docstring**

The figure padding on each side. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the padding value


<a id="McUtils.Plots.Graphics.Graphics.padding_left" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_left(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L2031)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L2031?message=Update%20Docs)]
</div>
**LLM Docstring**

The left figure padding. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the left padding value


<a id="McUtils.Plots.Graphics.Graphics.padding_right" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_right(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L2054)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L2054?message=Update%20Docs)]
</div>
**LLM Docstring**

The right figure padding. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the right padding value


<a id="McUtils.Plots.Graphics.Graphics.padding_top" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_top(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L2077)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L2077?message=Update%20Docs)]
</div>
**LLM Docstring**

The top figure padding. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the top padding value


<a id="McUtils.Plots.Graphics.Graphics.padding_bottom" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_bottom(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L2100)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L2100?message=Update%20Docs)]
</div>
**LLM Docstring**

The bottom figure padding. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the bottom padding value


<a id="McUtils.Plots.Graphics.Graphics.spacings" class="docs-object-method">&nbsp;</a> 
```python
@property
spacings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L2124)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L2124?message=Update%20Docs)]
</div>
**LLM Docstring**

The inter-panel spacings. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the spacings value


<a id="McUtils.Plots.Graphics.Graphics.background" class="docs-object-method">&nbsp;</a> 
```python
@property
background(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L2148)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L2148?message=Update%20Docs)]
</div>
**LLM Docstring**

The figure background color. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the background value


<a id="McUtils.Plots.Graphics.Graphics.colorbar" class="docs-object-method">&nbsp;</a> 
```python
@property
colorbar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L2172)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L2172?message=Update%20Docs)]
</div>
**LLM Docstring**

The colorbar specification. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the colorbar value


<a id="McUtils.Plots.Graphics.Graphics.get_padding_offsets" class="docs-object-method">&nbsp;</a> 
```python
get_padding_offsets(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L2219)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L2219?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the padding, expressed in plot-data coordinates, on each side of the
axes (from the pixel padding and the plot range).
  - `:returns`: `list`
    > the `((left, right), (bottom, top))` data-coordinate offsets


<a id="McUtils.Plots.Graphics.Graphics.get_bbox" class="docs-object-method">&nbsp;</a> 
```python
get_bbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L2242)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L2242?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the effective bounding box (in plot-data coordinates) of the total space
the figure occupies, including padding.
  - `:returns`: `list`
    > the `[(min_x, min_y), (max_x, max_y)]` bbox


<a id="McUtils.Plots.Graphics.Graphics.create_inset" class="docs-object-method">&nbsp;</a> 
```python
create_inset(self, bbox, coordinates='absolute', graphics_class=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics.py#L2269)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics.py#L2269?message=Update%20Docs)]
</div>
**LLM Docstring**

Create an inset within this plot, converting an absolute-data-coordinate bbox
into frame-scaled coordinates first.
  - `bbox`: `Any`
    > the inset bounding box
  - `coordinates`: `str`
    > `'absolute'` (data coordinates) or `'scaled'`
  - `graphics_class`: `Any`
    > the inset class (defaults to `Graphics`)
  - `opts`: `Any`
    > options for the inset
  - `:returns`: `Graphics`
    > the inset graphics object
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Graphics/Graphics.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Graphics/Graphics.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Graphics/Graphics.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Graphics/Graphics.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L1320?message=Update%20Docs)   
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