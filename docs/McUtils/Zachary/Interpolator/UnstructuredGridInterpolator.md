## <a id="McUtils.Zachary.Interpolator.UnstructuredGridInterpolator">UnstructuredGridInterpolator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator.py#L259)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator.py#L259?message=Update%20Docs)]
</div>

Defines an interpolator appropriate for totally unstructured grids by
delegating to the scipy `RBF` interpolators







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_neighbors: int
```
<a id="McUtils.Zachary.Interpolator.UnstructuredGridInterpolator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, grid, values, order=None, neighbors=None, extrapolate=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/UnstructuredGridInterpolator.py#L266)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/UnstructuredGridInterpolator.py#L266?message=Update%20Docs)]
</div>

  - `grid`: `np.ndarray`
    > 
  - `values`: `np.ndarray`
    > 
  - `order`: `int`
    > 
  - `neighbors`: `int`
    > 
  - `extrapolate`: `bool`
    > 
  - `opts`: `Any`
    >


<a id="McUtils.Zachary.Interpolator.UnstructuredGridInterpolator.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, points): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/UnstructuredGridInterpolator.py#L319)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/UnstructuredGridInterpolator.py#L319?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Interpolator.UnstructuredGridInterpolator.derivative" class="docs-object-method">&nbsp;</a> 
```python
derivative(self, order): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/UnstructuredGridInterpolator.py#L328)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/UnstructuredGridInterpolator.py#L328?message=Update%20Docs)]
</div>
Constructs the derivatives of the interpolator at the given order
  - `order`: `Any`
    > 
  - `:returns`: `UnstructuredGridInterpolator`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Interpolator/UnstructuredGridInterpolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Interpolator/UnstructuredGridInterpolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Interpolator/UnstructuredGridInterpolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Interpolator/UnstructuredGridInterpolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator.py#L259?message=Update%20Docs)   
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