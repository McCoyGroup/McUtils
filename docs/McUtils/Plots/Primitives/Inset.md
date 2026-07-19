## <a id="McUtils.Plots.Primitives.Inset">Inset</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives.py#L571)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives.py#L571?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Plots.Primitives.Inset.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, prims, position, offset=(0.5, 0.5), dimensions=None, plot_range=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives.py#L572)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives.py#L572?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up an inset primitive: a group of sub-primitives placed in their own inset
axes at a position within the parent.
  - `prims`: `Any`
    > the sub-primitives to draw in the inset
  - `position`: `Any`
    > the inset's anchor position in the parent
  - `offset`: `Any`
    > the anchor's alignment within the inset box
  - `dimensions`: `Any`
    > the inset's `(width, height)` (inferred from the sub-primitives if omitted)
  - `plot_range`: `Any`
    > the inset's data range (inferred if omitted)
  - `opts`: `Any`
    > extra options for the inset axes


<a id="McUtils.Plots.Primitives.Inset.plot_range" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_range(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives/Inset.py#L594)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives/Inset.py#L594?message=Update%20Docs)]
</div>
**LLM Docstring**

The inset's data range (computed from the sub-primitives when not set).
  - `:returns`: `list`
    > the `[(left, right), (bottom, top)]` range


<a id="McUtils.Plots.Primitives.Inset.get_plot_range" class="docs-object-method">&nbsp;</a> 
```python
get_plot_range(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives/Inset.py#L620)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives/Inset.py#L620?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the inset's data range as the union of its sub-primitives' bounding
boxes.
  - `:returns`: `list`
    > the `[(left, right), (bottom, top)]` range


<a id="McUtils.Plots.Primitives.Inset.dimensions" class="docs-object-method">&nbsp;</a> 
```python
@property
dimensions(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives/Inset.py#L641)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives/Inset.py#L641?message=Update%20Docs)]
</div>
**LLM Docstring**

The inset's `(width, height)`, derived from the data range (and filling in a
missing dimension from the aspect ratio).
  - `:returns`: `tuple`
    > the dimensions


<a id="McUtils.Plots.Primitives.Inset.get_bbox" class="docs-object-method">&nbsp;</a> 
```python
get_bbox(self, graphics=None, preserve_aspect=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives/Inset.py#L666)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives/Inset.py#L666?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the inset's bounding box in the parent's coordinates, optionally
correcting the height/width to preserve the sub-primitives' aspect ratio.
  - `graphics`: `Any`
    > the parent graphics (used for aspect correction)
  - `preserve_aspect`: `bool | None`
    > preserve the sub-primitives' aspect ratio
  - `:returns`: `list`
    > the `[[min_x, min_y], [max_x, max_y]]` bounding box


<a id="McUtils.Plots.Primitives.Inset.get_axes" class="docs-object-method">&nbsp;</a> 
```python
get_axes(self, graphics, bbox=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives/Inset.py#L706)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives/Inset.py#L706?message=Update%20Docs)]
</div>
**LLM Docstring**

Create (and cache) the inset axes on the parent graphics for the given bounding
box, closing any previous inset for that figure.
  - `graphics`: `Any`
    > the parent graphics
  - `bbox`: `Any`
    > the inset bounding box (computed if omitted)
  - `opts`: `Any`
    > options for the inset axes
  - `:returns`: `_`
    > the inset axes


<a id="McUtils.Plots.Primitives.Inset.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, axes, *args, graphics=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives/Inset.py#L725)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives/Inset.py#L725?message=Update%20Docs)]
</div>
**LLM Docstring**

Draw the inset: create its axes on the parent and render (or re-host) each
sub-primitive into it.
  - `axes`: `Any`
    > the axes (or graphics) to draw onto
  - `args`: `Any`
    > extra positional arguments
  - `graphics`: `Any`
    > the parent graphics (defaults to `axes`)
  - `kwargs`: `Any`
    > extra options
  - `:returns`: `list`
    > the drawn sub-primitives
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Primitives/Inset.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Primitives/Inset.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Primitives/Inset.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Primitives/Inset.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives.py#L571?message=Update%20Docs)   
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