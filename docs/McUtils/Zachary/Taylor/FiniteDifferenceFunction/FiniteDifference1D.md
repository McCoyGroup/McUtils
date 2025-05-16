## <a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D">FiniteDifference1D</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction.py#L271?message=Update%20Docs)]
</div>

A one-dimensional finite difference derivative object.
Higher-dimensional derivatives are built by chaining these.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse " id="methods" markdown="1">
 
<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, finite_difference_data, matrix): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.py#L276)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.py#L276?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.order" class="docs-object-method">&nbsp;</a> 
```python
@property
order(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.py#L280)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.py#L280?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.weights" class="docs-object-method">&nbsp;</a> 
```python
@property
weights(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.widths" class="docs-object-method">&nbsp;</a> 
```python
@property
widths(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.py#L286)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.py#L286?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.get_stencil" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_stencil(cls, order, stencil, accuracy): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L290)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L290?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, vals, val_dim=None, axis=0, mesh_spacing=None, check_shape=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.py#L298)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.py#L298?message=Update%20Docs)]
</div>
Applies the held `FiniteDifferenceMatrix` to the array of values
  - `vals`: `np.ndarray | sparse.csr_matrix`
    > values to do the difference over
  - `val_dim`: `int`
    > dimensions of the vals
  - `axis`: `int | tuple[int]`
    > the axis to apply along
  - `mesh_spacing`: `float`
    > the mesh spacing for the weights
  - `:returns`: `np.ndarray`
    >


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.sparse_tensordot" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
sparse_tensordot(sparse, mat, axis): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L383)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L383?message=Update%20Docs)]
</div>
Not sure how fast this will be, but does a very simple contraction of `mat` along `axis` by the final axis of `sparse`

Heavily de-generalized from here: https://github.com/pydata/sparse/blob/9dc40e15a04eda8d8efff35dfc08950b4c07a810/sparse/_coo/common.py
  - `sparse`: `sparse.sparsemat`
    > 
  - `mat`: `np.ndarray`
    > 
  - `axis`: `Any`
    > 
  - `:returns`: `_`
    >
 </div>
</div>




## Examples
## <a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D">FiniteDifference1D</a>
A one-dimensional finite difference derivative object.
Higher-dimensional derivatives are built by chaining these.

### Properties and Methods
```python
get_stencil: method
```
<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.__init__" class="docs-object-method">&nbsp;</a>
```python
__init__(self, finite_difference_data, matrix): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.order" class="docs-object-method">&nbsp;</a>
```python
@property
order(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.weights" class="docs-object-method">&nbsp;</a>
```python
@property
weights(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.widths" class="docs-object-method">&nbsp;</a>
```python
@property
widths(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.apply" class="docs-object-method">&nbsp;</a>
```python
apply(self, vals, val_dim=None, axis=0, mesh_spacing=None): 
```
Applies the held `FiniteDifferenceMatrix` to the array of values
- `vals`: `np.ndarray | sparse.csr_matrix`
    >values to do the difference over
- `val_dim`: `int`
    >dimensions of the vals
- `axis`: `int | tuple[int]`
    >the axis to apply along
- `mesh_spacing`: `float`
    >the mesh spacing for the weights
- `:returns`: `np.ndarray`
    >No description...

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifference1D.sparse_tensordot" class="docs-object-method">&nbsp;</a>
```python
sparse_tensordot(sparse, mat, axis): 
```
Not sure how fast this will be, but does a very simple contraction of `mat` along `axis` by the final axis of `sparse`

        Heavily de-generalized from here: https://github.com/pydata/sparse/blob/9dc40e15a04eda8d8efff35dfc08950b4c07a810/sparse/_coo/common.py
- `sparse`: `sparse.sparsemat`
    >No description...
- `mat`: `np.ndarray`
    >No description...
- `axis`: `Any`
    >No description...
- `:returns`: `_`
    >No description...

### Examples


___

[Edit Examples](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.md) or 
[Create New Examples](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.md) <br/>
[Edit Template](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.md) or 
[Create New Template](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.md) <br/>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction.py#L271?message=Update%20Docs)   
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