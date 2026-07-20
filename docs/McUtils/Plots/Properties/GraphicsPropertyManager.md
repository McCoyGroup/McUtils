## <a id="McUtils.Plots.Properties.GraphicsPropertyManager">GraphicsPropertyManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties.py#L16?message=Update%20Docs)]
</div>

Manages properties for Graphics objects so that concrete GraphicsBase instances don't need to duplicate code, but
at the same time things that build off of GraphicsBase don't need to implement all of these properties







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
ticks_label_base_styles: set
ticks_label_style_remapping: dict
```
<a id="McUtils.Plots.Properties.GraphicsPropertyManager.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, graphics, figure, axes, managed=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties.py#L22)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties.py#L22?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up the property manager that backs a `Graphics` object's styling/layout
properties, holding references to the graphics, figure, and axes and initializing
the cached property values.
  - `graphics`: `GraphicsBase`
    > the owning graphics object
  - `figure`: `Any`
    > the backend figure
  - `axes`: `Any`
    > the backend axes
  - `managed`: `bool`
    > whether an external manager owns the layout (e.g. a grid panel)


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.figure_label" class="docs-object-method">&nbsp;</a> 
```python
@property
figure_label(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L62)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L62?message=Update%20Docs)]
</div>
**LLM Docstring**

The overall figure label. The getter returns the cached value (reading it from the backend axes when
unset); the setter caches it and pushes it to the backend axes (unwrapping any
`Styled` value).
  - `:returns`: `_`
    > the figure label


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.plot_label" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_label(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L94)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L94?message=Update%20Docs)]
</div>
**LLM Docstring**

The plot title/label. The getter returns the cached value (reading it from the backend axes when
unset); the setter caches it and pushes it to the backend axes (unwrapping any
`Styled` value).
  - `:returns`: `_`
    > the plot label


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.style_list" class="docs-object-method">&nbsp;</a> 
```python
@property
style_list(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L128?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-series style cycle. The getter returns the cached styles; the setter
merges in new styles and pushes them to the backend axes when anything changed.
  - `:returns`: `_`
    > the style cycle


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.plot_legend" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_legend(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L167)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L167?message=Update%20Docs)]
</div>
**LLM Docstring**

The plot legend. The setter coerces legend-like values into a `PlotLegend`
(accepting `True` to keep an inferred legend).
  - `:returns`: `_`
    > the legend


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.legend_style" class="docs-object-method">&nbsp;</a> 
```python
@property
legend_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L216)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L216?message=Update%20Docs)]
</div>
**LLM Docstring**

The legend styling options. The getter returns the cached value (reading it from the backend axes when
unset); the setter caches it and pushes it to the backend axes (unwrapping any
`Styled` value).
  - `:returns`: `_`
    > the legend style


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.axes_labels" class="docs-object-method">&nbsp;</a> 
```python
@property
axes_labels(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L251)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L251?message=Update%20Docs)]
</div>
**LLM Docstring**

The `(x, y)` axis labels. The setter fills the missing side from the cached
labels and pushes each to the backend axes (unwrapping `Styled` values).
  - `:returns`: `_`
    > the axis labels


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.plot_range" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_range(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L300)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L300?message=Update%20Docs)]
</div>
**LLM Docstring**

The plotted `(x, y)` data range. The getter reads (and sorts) the backend limits
when unset; the setter caches the range and pushes each axis's limits (unwrapping
`Styled` values).
  - `:returns`: `_`
    > the plot range


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.absolute_plot_range" class="docs-object-method">&nbsp;</a> 
```python
@property
absolute_plot_range(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L361)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L361?message=Update%20Docs)]
</div>
**LLM Docstring**

The plot range with any unset axis filled in from the backend limits.
  - `:returns`: `_`
    > the absolute plot range


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.ticks" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L378)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L378?message=Update%20Docs)]
</div>
**LLM Docstring**

The tick specification. The getter returns the cached value; the setter applies
the x/y tick specs via the tick-setting helpers.
  - `:returns`: `_`
    > the tick specification


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.ticks_style" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L579)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L579?message=Update%20Docs)]
</div>
**LLM Docstring**

The tick styling. The getter returns the cached value; the setter applies the
x/y tick styles to the backend axes.
  - `:returns`: `_`
    > the tick styling


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.frame_style" class="docs-object-method">&nbsp;</a> 
```python
@property
frame_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L625)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L625?message=Update%20Docs)]
</div>
**LLM Docstring**

The frame (spine) styling. The getter returns the cached value; the setter
applies it to the backend axes.
  - `:returns`: `_`
    > the frame styling


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.clean_tick_label_styles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
clean_tick_label_styles(cls, k): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L678)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L678?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize a tick-label style key: strip/add the `label` prefix as appropriate and
apply the style-name remapping.
  - `k`: `str`
    > the style key
  - `:returns`: `str`
    > the normalized key


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.ticks_label_style" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks_label_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L698)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L698?message=Update%20Docs)]
</div>
**LLM Docstring**

The tick-label styling. The getter returns the cached value; the setter applies
the cleaned label styles to the backend axes.
  - `:returns`: `_`
    > the tick-label styling


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.aspect_ratio" class="docs-object-method">&nbsp;</a> 
```python
@property
aspect_ratio(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L736)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L736?message=Update%20Docs)]
</div>
**LLM Docstring**

The axes aspect ratio. The getter returns the cached value; the setter pushes it
to the backend axes (accepting a `(value, opts)` pair).
  - `:returns`: `_`
    > the aspect ratio


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.image_size" class="docs-object-method">&nbsp;</a> 
```python
@property
image_size(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L781)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L781?message=Update%20Docs)]
</div>
**LLM Docstring**

The figure image size in pixels. The getter resolves `'auto'` to the computed
inset size; the setter caches the size (filling a missing dimension from the
aspect ratio) and resizes the backend figure (in inches) unless managed/inset.
  - `:returns`: `_`
    > the image size


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.axes_bbox" class="docs-object-method">&nbsp;</a> 
```python
@property
axes_bbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L849)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L849?message=Update%20Docs)]
</div>
**LLM Docstring**

The axes bounding box. The getter reads it from the backend axes; the setter
pushes a new bbox.
  - `:returns`: `_`
    > the axes bbox


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.background" class="docs-object-method">&nbsp;</a> 
```python
@property
background(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L875)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L875?message=Update%20Docs)]
</div>
**LLM Docstring**

The background/face color. The getter returns the cached value; the setter
applies it to the backend axes (and figure).
  - `:returns`: `_`
    > the background color


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.frame" class="docs-object-method">&nbsp;</a> 
```python
@property
frame(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L908)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L908?message=Update%20Docs)]
</div>
**LLM Docstring**

Which frame (spine) edges are drawn. The getter returns the cached value; the
setter applies the visibility spec to the backend axes.
  - `:returns`: `_`
    > the frame visibility


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.scale" class="docs-object-method">&nbsp;</a> 
```python
@property
scale(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L946)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L946?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-axis scaling (e.g. linear/log). The getter returns the cached value; the
setter applies the x/y scales to the backend axes.
  - `:returns`: `_`
    > the axis scaling


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding" class="docs-object-method">&nbsp;</a> 
```python
@property
padding(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L991)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L991?message=Update%20Docs)]
</div>
**LLM Docstring**

The figure padding on each side. The getter returns the cached value; the setter
caches it and pushes it to the backend.
  - `:returns`: `_`
    > the padding


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_left" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_left(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1045)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1045?message=Update%20Docs)]
</div>
**LLM Docstring**

The left figure padding. The getter returns the cached value; the setter updates
just the left component of the padding.
  - `:returns`: `_`
    > the left padding


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_right" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_right(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1069)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1069?message=Update%20Docs)]
</div>
**LLM Docstring**

The right figure padding. The getter returns the cached value; the setter updates
just the right component of the padding.
  - `:returns`: `_`
    > the right padding


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_top" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_top(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1093)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1093?message=Update%20Docs)]
</div>
**LLM Docstring**

The top figure padding. The getter returns the cached value; the setter updates
just the top component of the padding.
  - `:returns`: `_`
    > the top padding


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_bottom" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_bottom(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1117)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1117?message=Update%20Docs)]
</div>
**LLM Docstring**

The bottom figure padding. The getter returns the cached value; the setter updates
just the bottom component of the padding.
  - `:returns`: `_`
    > the bottom padding


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.spacings" class="docs-object-method">&nbsp;</a> 
```python
@property
spacings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1142)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1142?message=Update%20Docs)]
</div>
**LLM Docstring**

The inter-panel spacings. The getter returns `[0, 0]` for a managed/inset axes,
else the cached value; the setter converts fractional spacings to absolute sizes
(from the panel bboxes) and pushes them to the figure.
  - `:returns`: `_`
    > the spacings


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.colorbar" class="docs-object-method">&nbsp;</a> 
```python
@property
colorbar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1204)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L1204?message=Update%20Docs)]
</div>
**LLM Docstring**

The colorbar specification. The getter returns the cached value; the setter
records it and adds a colorbar to the graphics (from `True` or an options dict).
  - `:returns`: `_`
    > the colorbar spec
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Properties/GraphicsPropertyManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Properties/GraphicsPropertyManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Properties/GraphicsPropertyManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Properties/GraphicsPropertyManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties.py#L16?message=Update%20Docs)   
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