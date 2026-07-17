## <a id="McUtils.Zachary.Surfaces.BaseSurface.TaylorSeriesSurface">TaylorSeriesSurface</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/BaseSurface.py#L121)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface.py#L121?message=Update%20Docs)]
</div>

A surface with an evaluator built off of a Taylor series expansion







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Surfaces.BaseSurface.TaylorSeriesSurface.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *derivs, dimension=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/BaseSurface.py#L125)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface.py#L125?message=Update%20Docs)]
</div>

  - `data`: `Any`
    > derivs or a tuple of derivs + options
  - `dimension`: `Any`
    >


<a id="McUtils.Zachary.Surfaces.BaseSurface.TaylorSeriesSurface.center" class="docs-object-method">&nbsp;</a> 
```python
@property
center(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.py#L141)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.py#L141?message=Update%20Docs)]
</div>
**LLM Docstring**

The expansion center of the underlying Taylor series.
  - `:returns`: `np.ndarray`
    > the center


<a id="McUtils.Zachary.Surfaces.BaseSurface.TaylorSeriesSurface.ref" class="docs-object-method">&nbsp;</a> 
```python
@property
ref(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.py#L152?message=Update%20Docs)]
</div>
**LLM Docstring**

The reference (constant) value of the underlying Taylor series.
  - `:returns`: `_`
    > the reference value


<a id="McUtils.Zachary.Surfaces.BaseSurface.TaylorSeriesSurface.expansion_tensors" class="docs-object-method">&nbsp;</a> 
```python
@property
expansion_tensors(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.py#L162)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.py#L162?message=Update%20Docs)]
</div>
**LLM Docstring**

The derivative tensors of the underlying Taylor series.
  - `:returns`: `list`
    > the expansion tensors


<a id="McUtils.Zachary.Surfaces.BaseSurface.TaylorSeriesSurface.check_dimension" class="docs-object-method">&nbsp;</a> 
```python
check_dimension(self, gridpoints, target=None, raise_exception=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.py#L174)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.py#L174?message=Update%20Docs)]
</div>
**LLM Docstring**

Check the grid-point dimension, additionally accepting either side of the
expansion's coordinate transform when one is present.
  - `gridpoints`: `np.ndarray`
    > the points to check
  - `target`: `int | None`
    > an explicit expected dimension
  - `raise_exception`: `bool`
    > raise on a mismatch
  - `:returns`: `bool`
    > whether the dimension matches


<a id="McUtils.Zachary.Surfaces.BaseSurface.TaylorSeriesSurface.evaluate" class="docs-object-method">&nbsp;</a> 
```python
evaluate(self, points, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.py#L201)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.py#L201?message=Update%20Docs)]
</div>
Since the Taylor expansion stuff is already built out this is super easy
  - `points`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface.py#L121?message=Update%20Docs)   
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