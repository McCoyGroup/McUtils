## <a id="McUtils.Plots.Primitives.Polygon">Polygon</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives.py#L493)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives.py#L493?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Plots.Primitives.Polygon.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, points, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives.py#L494)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives.py#L494?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a `Polygon` primitive.
  - `points`: `Any`
    > the polygon vertices
  - `opts`: `Any`
    > extra styling options


<a id="McUtils.Plots.Primitives.Polygon.get_bbox" class="docs-object-method">&nbsp;</a> 
```python
get_bbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives/Polygon.py#L506)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives/Polygon.py#L506?message=Update%20Docs)]
</div>
**LLM Docstring**

Not implemented: this primitive has no bounding-box computation.


<a id="McUtils.Plots.Primitives.Polygon.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, axes, *args, sphere_points=None, graphics=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives/Polygon.py#L516)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives/Polygon.py#L516?message=Update%20Docs)]
</div>
**LLM Docstring**

Draw the primitive onto the axes via `axes.draw_poly`.
  - `axes`: `Any`
    > the axes (or graphics) to draw onto
  - `args`: `Any`
    > extra positional arguments
  - `graphics`: `Any`
    > the owning graphics object
  - `kwargs`: `Any`
    > extra styling options
  - `:returns`: `_`
    > the drawn backend object
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Primitives/Polygon.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Primitives/Polygon.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Primitives/Polygon.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Primitives/Polygon.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives.py#L493?message=Update%20Docs)   
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