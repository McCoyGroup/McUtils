## <a id="McUtils.Zachary.Surfaces.Surface.MultiSurface">MultiSurface</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/Surface.py#L159)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface.py#L159?message=Update%20Docs)]
</div>

A _reallly_ simple extension to the Surface infrastructure to handle vector valued functions,
assuming each vector value corresponds to a different Surfaces







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Surfaces.Surface.MultiSurface.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *surfs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/Surface.py#L164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface.py#L164?message=Update%20Docs)]
</div>

  - `surfs`: `Iterable[Surface]`
    > a set of Surface objects to use when evaluating


<a id="McUtils.Zachary.Surfaces.Surface.MultiSurface.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, gridpoints, order=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/Surface/MultiSurface.py#L171)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface/MultiSurface.py#L171?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate every component surface at the grid points, stacking the results (per
derivative order when `order` is given).
  - `gridpoints`: `np.ndarray`
    > the points to evaluate at
  - `order`: `int | None`
    > the derivative order to request from each surface
  - `kwargs`: `Any`
    > extra evaluation options
  - `:returns`: `np.ndarray | list`
    > the stacked per-surface values
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Surfaces/Surface/MultiSurface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Surfaces/Surface/MultiSurface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Surfaces/Surface/MultiSurface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Surfaces/Surface/MultiSurface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface.py#L159?message=Update%20Docs)   
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