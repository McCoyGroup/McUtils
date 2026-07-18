## <a id="McUtils.Plots.Graphics.Graphics3D">Graphics3D</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics.py#L2239)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L2239?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_style: dict
opt_keys: set
known_keys: set
```
<a id="McUtils.Plots.Graphics.Graphics3D.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *args, figure=None, axes=None, subplot_kw=None, event_handlers=None, animate=None, axes_labels=None, plot_label=None, style_list=None, plot_range=None, plot_legend=None, ticks=None, scale=None, ticks_style=None, image_size=None, background=None, view_settings=None, box_ratios=None, projection_type=None, aspect_ratio=None, autoscale=None, backend='matplotlib3D', **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics.py#L2248)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L2248?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a 3D plot, forwarding the 2D styling options to `Graphics` and adding the
3D-specific ones (view settings, box ratios, projection, autoscale) with a 3D
backend and property manager.
  - `args`: `Any`
    > positional plot arguments
  - `figure`: `Any`
    > an existing figure to draw into
  - `axes`: `Any`
    > existing axes to draw into
  - `subplot_kw`: `dict | None`
    > subplot construction options
  - `event_handlers`: `Any`
    > interactive event handlers
  - `animate`: `Any`
    > an animation specification
  - `axes_labels`: `Any`
    > the axis labels
  - `plot_label`: `Any`
    > the plot title
  - `style_list`: `Any`
    > the style cycle
  - `plot_range`: `Any`
    > the data range
  - `plot_legend`: `Any`
    > the legend
  - `ticks`: `Any`
    > the tick specification
  - `scale`: `Any`
    > the axis scaling
  - `ticks_style`: `Any`
    > tick styling
  - `image_size`: `Any`
    > the image size
  - `background`: `Any`
    > the background color
  - `view_settings`: `Any`
    > the 3D camera/view settings
  - `box_ratios`: `Any`
    > the 3D box aspect ratios
  - `projection_type`: `Any`
    > the projection (e.g. perspective/ortho)
  - `aspect_ratio`: `Any`
    > the aspect ratio
  - `autoscale`: `Any`
    > the autoscale setting
  - `backend`: `str`
    > the plotting backend
  - `kwargs`: `Any`
    > extra options


<a id="McUtils.Plots.Graphics.Graphics3D.set_options" class="docs-object-method">&nbsp;</a> 
```python
set_options(self, view_settings=None, box_ratios=None, projection_type=None, aspect_ratio=None, autoscale=None, **parent_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics3D.py#L2334)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics3D.py#L2334?message=Update%20Docs)]
</div>
**LLM Docstring**

Set the 3D-specific options (view settings, box ratios, projection, autoscale,
aspect ratio) on top of the base options.
  - `view_settings`: `Any`
    > the 3D view settings
  - `box_ratios`: `Any`
    > the 3D box aspect ratios
  - `projection_type`: `Any`
    > the projection type
  - `aspect_ratio`: `Any`
    > the aspect ratio
  - `autoscale`: `Any`
    > the autoscale setting
  - `parent_opts`: `Any`
    > options forwarded to `Graphics.set_options`


<a id="McUtils.Plots.Graphics.Graphics3D.box_ratios" class="docs-object-method">&nbsp;</a> 
```python
@property
box_ratios(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics3D.py#L2370)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics3D.py#L2370?message=Update%20Docs)]
</div>
**LLM Docstring**

The 3D box aspect ratios. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the box ratios value


<a id="McUtils.Plots.Graphics.Graphics3D.autoscale" class="docs-object-method">&nbsp;</a> 
```python
@property
autoscale(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics3D.py#L2393)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics3D.py#L2393?message=Update%20Docs)]
</div>
**LLM Docstring**

Whether the 3D axes autoscale. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the autoscale value


<a id="McUtils.Plots.Graphics.Graphics3D.projection_type" class="docs-object-method">&nbsp;</a> 
```python
@property
projection_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics3D.py#L2416)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics3D.py#L2416?message=Update%20Docs)]
</div>
**LLM Docstring**

The 3D projection type. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the projection type value


<a id="McUtils.Plots.Graphics.Graphics3D.view_settings" class="docs-object-method">&nbsp;</a> 
```python
@property
view_settings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/Graphics3D.py#L2439)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/Graphics3D.py#L2439?message=Update%20Docs)]
</div>
**LLM Docstring**

The 3D camera/view settings. Getter/setter delegate to the property manager (the setter also records
the change for copying).
  - `:returns`: `_`
    > the view settings value
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Graphics/Graphics3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Graphics/Graphics3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Graphics/Graphics3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Graphics/Graphics3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L2239?message=Update%20Docs)   
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