## <a id="McUtils.Plots.Properties.GraphicsPropertyManager3D">GraphicsPropertyManager3D</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties.py#L1271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties.py#L1271?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, graphics, figure, axes, managed=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties.py#L1272)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties.py#L1272?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up the 3D property manager, adding the cached view-settings and box-ratios
values.
  - `graphics`: `GraphicsBase`
    > the owning graphics object
  - `figure`: `Any`
    > the backend figure
  - `axes`: `Any`
    > the backend 3D axes
  - `managed`: `bool`
    > whether an external manager owns the layout


<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.axes_labels" class="docs-object-method">&nbsp;</a> 
```python
@property
axes_labels(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1290)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1290?message=Update%20Docs)]
</div>
**LLM Docstring**

The `(x, y, z)` axis labels. The setter fills missing sides from the cached
labels and pushes each to the backend 3D axes (unwrapping `Styled` values).
  - `:returns`: `_`
    > the axis labels


<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.box_ratios" class="docs-object-method">&nbsp;</a> 
```python
@property
box_ratios(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1349)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1349?message=Update%20Docs)]
</div>
**LLM Docstring**

The 3D box aspect ratios. The getter reads them from the backend when unset; the
setter resolves `'auto'` from the plot range and pushes the ratios to the backend
axes.
  - `:returns`: `_`
    > the box aspect ratios


<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.projection_type" class="docs-object-method">&nbsp;</a> 
```python
@property
projection_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1383)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1383?message=Update%20Docs)]
</div>
**LLM Docstring**

The 3D projection type, read from / written to the backend axes.
  - `:returns`: `_`
    > the projection type


<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.autoscale" class="docs-object-method">&nbsp;</a> 
```python
@property
autoscale(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1404)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1404?message=Update%20Docs)]
</div>
**LLM Docstring**

The 3D autoscale setting, read from / written to the backend axes.
  - `:returns`: `_`
    > the autoscale setting


<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.plot_range" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_range(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1425)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1425?message=Update%20Docs)]
</div>
**LLM Docstring**

The plotted `(x, y, z)` data range. The getter reads the backend limits when
unset; the setter fills missing axes from the cache and pushes each axis's limits
(unwrapping `Styled` values).
  - `:returns`: `_`
    > the plot range


<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.absolute_plot_range" class="docs-object-method">&nbsp;</a> 
```python
@property
absolute_plot_range(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1490)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1490?message=Update%20Docs)]
</div>
**LLM Docstring**

The 3D plot range with any unset axis filled in from the backend limits.
  - `:returns`: `_`
    > the absolute plot range


<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.frame" class="docs-object-method">&nbsp;</a> 
```python
@property
frame(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1524)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1524?message=Update%20Docs)]
</div>
**LLM Docstring**

Which 3D frame edges are drawn. The getter returns the cached value; the setter
applies the visibility spec to the backend 3D axes.
  - `:returns`: `_`
    > the frame visibility


<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.frame_style" class="docs-object-method">&nbsp;</a> 
```python
@property
frame_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1566)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1566?message=Update%20Docs)]
</div>
**LLM Docstring**

The 3D frame styling. The getter returns the cached value; the setter applies it
to the backend 3D axes.
  - `:returns`: `_`
    > the frame styling


<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.ticks" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1622)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1622?message=Update%20Docs)]
</div>
**LLM Docstring**

The 3D tick specification. The getter returns the cached value; the setter applies
the x/y/z tick specs.
  - `:returns`: `_`
    > the tick specification


<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.ticks_style" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1657)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1657?message=Update%20Docs)]
</div>
**LLM Docstring**

The 3D tick styling. The getter returns the cached value; the setter applies the
x/y/z tick styles to the backend axes.
  - `:returns`: `_`
    > the tick styling


<a id="McUtils.Plots.Properties.GraphicsPropertyManager3D.view_settings" class="docs-object-method">&nbsp;</a> 
```python
@property
view_settings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1698)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager3D.py#L1698?message=Update%20Docs)]
</div>
**LLM Docstring**

The 3D camera/view settings, read from / written to the backend axes.
  - `:returns`: `_`
    > the view settings
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Properties/GraphicsPropertyManager3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Properties/GraphicsPropertyManager3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Properties/GraphicsPropertyManager3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Properties/GraphicsPropertyManager3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties.py#L1271?message=Update%20Docs)   
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