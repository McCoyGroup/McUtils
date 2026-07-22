## <a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceFunction">FiniteDifferenceFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L26)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L26?message=Update%20Docs)]
</div>

The FiniteDifferenceFunction encapsulates a bunch of functionality extracted from [Fornberger's
Calculation of Wieghts in Finite Difference Formulas](https://epubs.siam.org/doi/pdf/10.1137/S0036144596322507)

Only applies to direct product grids, but each subgrid can be regular or irregular.
Used in a large number of other places, but relatively rarely on its own.
A convenient application is the `FiniteDifferenceDerivative` class in the `Derivatives` module.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *diffs, axes=0, contract=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L43)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L43?message=Update%20Docs)]
</div>
Constructs an object to take finite differences derivatives of grids of data
  - `diffs`: `FiniteDifference1D`
    > A set of differences to take along successive axes in the data
  - `axes`: `int | Iterable[int]`
    > The axes to take the specified differences along
  - `contract`: `bool`
    > Whether to reduce the shape of the returned tensor if applicable after application


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceFunction.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, vals, axes=None, mesh_spacing=None, contract=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.py#L57)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.py#L57?message=Update%20Docs)]
</div>
Iteratively applies the stored finite difference objects to the vals
  - `vals`: `np.ndarray`
    > The tensor of values to take the difference on
  - `axes`: `int | Iterable[int]`
    > The axis or axes to take the differences along (defaults to `self.axes`)
  - `:returns`: `np.ndarray`
    > The tensor of derivatives


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceFunction.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, vals, axes=None, mesh_spacing=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.py#L91)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.py#L91?message=Update%20Docs)]
</div>
**LLM Docstring**

Apply the finite-difference weights to a set of values (delegates to `apply`).
  - `vals`: `np.ndarray`
    > the values on the grid
  - `axes`: `Any`
    > the axes to difference along
  - `mesh_spacing`: `Any`
    > the grid spacing(s)
  - `:returns`: `np.ndarray`
    > the finite-difference derivative


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceFunction.order" class="docs-object-method">&nbsp;</a> 
```python
@property
order(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.py#L106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.py#L106?message=Update%20Docs)]
</div>

  - `:returns`: `tuple[int]`
    > the order of the derivative requested


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceFunction.weights" class="docs-object-method">&nbsp;</a> 
```python
@property
weights(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.py#L114)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.py#L114?message=Update%20Docs)]
</div>

  - `:returns`: `tuple[np.array[float]]`
    > the weights for the specified stencil


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceFunction.widths" class="docs-object-method">&nbsp;</a> 
```python
@property
widths(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.py#L122)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.py#L122?message=Update%20Docs)]
</div>

  - `:returns`: `tuple[(int, int)]`
    > the number of points in each dimension, left and right, for the specified stencil


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceFunction.regular_difference" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
regular_difference(cls, order, mesh_spacing=None, accuracy=2, stencil=None, end_point_accuracy=2, axes=0, contract=True, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L130?message=Update%20Docs)]
</div>
Constructs a `FiniteDifferenceFunction` appropriate for a _regular grid_ with the given stencil
  - `order`: `tuple[int]`
    > the order of the derivative
  - `mesh_spacing`: `None | float | tuple[float]`
    > the spacing between grid points in the regular grid `h`
  - `accuracy`: `None | int | tuple[int]`
    > the accuracy of the derivative that we'll try to achieve as a power on `h`
  - `stencil`: `None | int | tuple[int]`
    > the stencil to use for the derivative (overrides `accuracy`)
  - `end_point_accuracy`: `None | int | tuple[int]`
    > the amount of extra accuracy to use at the edges of the grid
  - `axes`: `None | int | tuple[int]`
    > the axes of the passed array for the derivative to be applied along
  - `contract`: `bool`
    > whether to eliminate any axes of size `1` from the results
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceFunction.from_grid" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_grid(cls, grid, order, accuracy=2, stencil=None, end_point_accuracy=2, axes=0, contract=True, allow_irregular=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L188?message=Update%20Docs)]
</div>
Constructs a `FiniteDifferenceFunction` from a grid and order.
Deconstructs the grid into its subgrids and builds a different differencer for each dimension
  - `grid`: `np.ndarray`
    > The grid to use as input data when defining the derivative
  - `order`: `int or list of ints`
    > order of the derivative to compute
  - `stencil`: `int or list of ints`
    > number of points to use in the stencil
  - `:returns`: `FiniteDifferenceFunction`
    > deriv func
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L26?message=Update%20Docs)   
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