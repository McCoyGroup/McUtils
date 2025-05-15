## <a id="McUtils.McUtils.Zachary.Taylor.FiniteDifferenceFunction.IrregularGridFiniteDifference">IrregularGridFiniteDifference</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L508)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L508?message=Update%20Docs)]
</div>

Defines a finite difference over an irregular grid







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse " id="methods" markdown="1">
 
<a id="McUtils.McUtils.Zachary.Taylor.FiniteDifferenceFunction.IrregularGridFiniteDifference.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, grid, order, stencil=None, accuracy=2, end_point_accuracy=2, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/IrregularGridFiniteDifference.py#L512)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/IrregularGridFiniteDifference.py#L512?message=Update%20Docs)]
</div>

  - `grid`: `np.ndarray`
    > the grid to get the weights from
  - `order`: `int`
    > the order of the derivative to take
  - `stencil`: `int | None`
    > the number of stencil points to add
  - `accuracy`: `int | None`
    > the approximate accuracy to target with the method
  - `end_point_accuracy`: `int | None`
    > the extra number of stencil points to add to the end points
  - `kw`: `Any`
    > options passed through to the `FiniteDifferenceMatrix`


<a id="McUtils.McUtils.Zachary.Taylor.FiniteDifferenceFunction.IrregularGridFiniteDifference.get_grid_slices" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
get_grid_slices(grid, stencil): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L539)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L539?message=Update%20Docs)]
</div>

  - `grid`: `Any`
    > 
  - `stencil`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Zachary.Taylor.FiniteDifferenceFunction.IrregularGridFiniteDifference.get_weights" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
get_weights(m, z, x): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L552)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L552?message=Update%20Docs)]
</div>
Extracts the grid weights for an unevenly spaced grid based off of the algorithm outlined by
Fronberger in https://pdfs.semanticscholar.org/8bf5/912bde884f6bd4cfb4991ba3d077cace94c0.pdf
  - `m`: `Any`
    > highest derivative order
  - `z`: `Any`
    > center of the derivatives
  - `X`: `Any`
    > grid of points


<a id="McUtils.McUtils.Zachary.Taylor.FiniteDifferenceFunction.IrregularGridFiniteDifference.finite_difference_data" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
finite_difference_data(cls, grid, order, stencil, end_point_precision): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L569)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L569?message=Update%20Docs)]
</div>
Constructs a finite-difference function that computes the nth derivative with a given width
  - `deriv`: `Any`
    > 
  - `accuracy`: `Any`
    > 
  - `:returns`: `_`
    >
 </div>
</div>




## Examples
## <a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.IrregularGridFiniteDifference">IrregularGridFiniteDifference</a>
Defines a finite difference over an irregular grid

### Properties and Methods
```python
finite_difference_data: method
```
<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.IrregularGridFiniteDifference.__init__" class="docs-object-method">&nbsp;</a>
```python
__init__(self, grid, order, stencil=None, accuracy=2, end_point_accuracy=2, **kw): 
```

- `grid`: `np.ndarray`
    >the grid to get the weights from
- `order`: `int`
    >the order of the derivative to take
- `stencil`: `int | None`
    >the number of stencil points to add
- `accuracy`: `int | None`
    >the approximate accuracy to target with the method
- `end_point_accuracy`: `int | None`
    >the extra number of stencil points to add to the end points
- `kw`: `Any`
    >options passed through to the `FiniteDifferenceMatrix`

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.IrregularGridFiniteDifference.get_grid_slices" class="docs-object-method">&nbsp;</a>
```python
get_grid_slices(grid, stencil): 
```

- `grid`: `Any`
    >No description...
- `stencil`: `Any`
    >No description...
- `:returns`: `_`
    >No description...

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.IrregularGridFiniteDifference.get_weights" class="docs-object-method">&nbsp;</a>
```python
get_weights(m, z, x): 
```
Extracts the grid weights for an unevenly spaced grid based off of the algorithm outlined by
        Fronberger in https://pdfs.semanticscholar.org/8bf5/912bde884f6bd4cfb4991ba3d077cace94c0.pdf
- `m`: `Any`
    >highest derivative order
- `z`: `Any`
    >center of the derivatives
- `X`: `Any`
    >grid of points

### Examples


___

[Edit Examples](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/IrregularGridFiniteDifference.md) or 
[Create New Examples](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/IrregularGridFiniteDifference.md) <br/>
[Edit Template](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/IrregularGridFiniteDifference.md) or 
[Create New Template](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/IrregularGridFiniteDifference.md) <br/>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/IrregularGridFiniteDifference.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/IrregularGridFiniteDifference.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Taylor/FiniteDifferenceFunction/IrregularGridFiniteDifference.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/IrregularGridFiniteDifference.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L508?message=Update%20Docs)   
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