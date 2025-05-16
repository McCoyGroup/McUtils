# <a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.finite_difference">finite_difference</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction.py#L895)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction.py#L895?message=Update%20Docs)]
</div>

```python
finite_difference(grid, values, order, accuracy=2, stencil=None, end_point_accuracy=1, axes=None, only_core=False, only_center=False, dtype='float64', **kw): 
```
Computes a finite difference derivative for the values on the grid
  - `grid`: `np.ndarray`
    > the grid of points for which the vlaues lie on
  - `values`: `np.ndarray`
    > the values on the grid
  - `order`: `int | Iterable[int]`
    > order of the derivative to compute
  - `stencil`: `int | Iterable[int]`
    > number of points to use in the stencil
  - `accuracy`: `int | Iterable[int]`
    > approximate accuracy of the derivative to request (overridden by `stencil`)
  - `end_point_accuracy`: `int | Iterable[int]`
    > extra stencil points to use on the edges
extra stencil points to use on the edges
  - `axes`: `int | Iterable[int]`
    > which axes to perform the successive derivatives over (defaults to the first _n_ axes)
  - `only_center`: `bool`
    > whether or not to only take the central value
  - `only_core`: `bool`
    > whether or not to avoid edge values where a different stencil would be used
  - `:returns`: `_`
    > 



## Examples
# <a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.finite_difference">finite_difference</a>

```python
finite_difference(grid, values, order, accuracy=2, stencil=None, end_point_accuracy=1, axes=None, dtype='float64', **kw): 
```
Computes a finite difference derivative for the values on the grid
- `grid`: `np.ndarray`
    >the grid of points for which the vlaues lie on
- `values`: `np.ndarray`
    >the values on the grid
- `order`: `int | Iterable[int]`
    >order of the derivative to compute
- `stencil`: `int | Iterable[int]`
    >number of points to use in the stencil
- `accuracy`: `int | Iterable[int]`
    >approximate accuracy of the derivative to request (overridden by `stencil`)
- `end_point_accuracy`: `int | Iterable[int]`
    >extra stencil points to use on the edges
- `axes`: `int | Iterable[int]`
    >which axes to perform the successive derivatives over (defaults to the first _n_ axes)
- `:returns`: `_`
    >No description... 

### Examples: 


___

[Edit Examples](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/finite_difference.md) or 
[Create New Examples](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/finite_difference.md) <br/>
[Edit Template](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/finite_difference.md) or 
[Create New Template](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/finite_difference.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction.py?message=Update%20Docs)






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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/finite_difference.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/finite_difference.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Taylor/FiniteDifferenceFunction/finite_difference.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/finite_difference.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction.py#L895?message=Update%20Docs)   
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