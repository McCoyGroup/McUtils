## <a id="McUtils.Zachary.Interpolator.Interpolator">Interpolator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator.py#L376)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator.py#L376?message=Update%20Docs)]
</div>

A general purpose that takes your data and just interpolates it without whining or making you do a pile of extra work







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
DefaultExtrapolator: ExtrapolatorType
```
<a id="McUtils.Zachary.Interpolator.Interpolator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, grid, vals, interpolation_function=None, interpolation_order=None, extrapolator=None, extrapolation_order=None, **interpolation_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/Interpolator.py#L381)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/Interpolator.py#L381?message=Update%20Docs)]
</div>

  - `grid`: `np.ndarray`
    > an unstructured grid of points **or** a structured grid of points **or** a 1D array
  - `vals`: `np.ndarray`
    > the values at the grid points
  - `interpolation_function`: `None | BasicInterpolator`
    > the basic function to be used to handle the raw interpolation
  - `interpolation_order`: `int | str | None`
    > the order of extrapolation to use (when applicable)
  - `extrapolator`: `Extrapolator | None | str | function`
    > the extrapolator to use for data points not on the grid
  - `extrapolation_order`: `int | str | None`
    > the order of extrapolation to use by default
  - `interpolation_opts`: `Any`
    > the options to be fed into the interpolating_function


<a id="McUtils.Zachary.Interpolator.Interpolator.get_interpolator" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_interpolator(cls, grid, vals, interpolation_order=None, allow_extrapolation=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L426)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L426?message=Update%20Docs)]
</div>
Returns a function that can be called on grid points to interpolate them
  - `grid`: `Mesh`
    > 
  - `vals`: `np.ndarray`
    > 
  - `interpolation_order`: `int | str | None`
    > 
  - `opts`: `Any`
    > 
  - `:returns`: `function`
    > i
n
t
e
r
p
o
l
a
t
o
r


<a id="McUtils.Zachary.Interpolator.Interpolator.get_extrapolator" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_extrapolator(cls, grid, vals, extrapolation_order=1, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L477)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L477?message=Update%20Docs)]
</div>
Returns an Extrapolator that can be called on grid points to extrapolate them
  - `grid`: `Mesh`
    > 
  - `extrapolation_order`: `int`
    > 
  - `:returns`: `Extrapolator`
    > e
x
t
r
a
p
o
l
a
t
o
r


<a id="McUtils.Zachary.Interpolator.Interpolator.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, grid_points, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/Interpolator.py#L539)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/Interpolator.py#L539?message=Update%20Docs)]
</div>
Interpolates then extrapolates the function at the grid_points
  - `grid_points`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.Interpolator.Interpolator.derivative" class="docs-object-method">&nbsp;</a> 
```python
derivative(self, order): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/Interpolator.py#L555)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/Interpolator.py#L555?message=Update%20Docs)]
</div>
Returns a new function representing the requested derivative
of the current interpolator
  - `order`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.Interpolator.Interpolator.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/Interpolator.py#L572)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/Interpolator.py#L572?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Interpolator/Interpolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Interpolator/Interpolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Interpolator/Interpolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Interpolator/Interpolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator.py#L376?message=Update%20Docs)   
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