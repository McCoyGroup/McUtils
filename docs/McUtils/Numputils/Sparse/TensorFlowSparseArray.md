## <a id="McUtils.Numputils.Sparse.TensorFlowSparseArray">TensorFlowSparseArray</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse.py#L2558)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse.py#L2558?message=Update%20Docs)]
</div>

Provides a SparseArray implementation that uses TensorFlow as the backend







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, data, dtype=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2562)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2562?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2616)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2616?message=Update%20Docs)]
</div>
Provides the shape of the sparse array
  - `:returns`: `tuple[int]`
    >


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.to_state" class="docs-object-method">&nbsp;</a> 
```python
to_state(self, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2625)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2625?message=Update%20Docs)]
</div>
Provides just the state that is needed to
serialize the object
  - `serializer`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.from_state" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_state(cls, state, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L2636)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L2636?message=Update%20Docs)]
</div>
Loads from the stored state
  - `serializer`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.empty" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
empty(cls, shape, dtype=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L2647)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L2647?message=Update%20Docs)]
</div>
Returns an empty SparseArray with the appropriate shape and dtype
  - `shape`: `Any`
    > 
  - `dtype`: `Any`
    > 
  - `kw`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.block_data" class="docs-object-method">&nbsp;</a> 
```python
@property
block_data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2662)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2662?message=Update%20Docs)]
</div>
Returns the row and column indices and vector of
values that the sparse array is storing
  - `:returns`: `Tuple[np.ndarray, Iterable[np.ndarray]]`
    >


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.transpose" class="docs-object-method">&nbsp;</a> 
```python
transpose(self, axes): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2672)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2672?message=Update%20Docs)]
</div>
Returns a transposed version of the tensor
  - `axes`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.ascoo" class="docs-object-method">&nbsp;</a> 
```python
ascoo(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2684)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2684?message=Update%20Docs)]
</div>
Converts the tensor into a scipy COO matrix...
  - `:returns`: `sp.coo_matrix`
    >


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.ascsr" class="docs-object-method">&nbsp;</a> 
```python
ascsr(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2691)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2691?message=Update%20Docs)]
</div>
Converts the tensor into a scipy COO matrix...
  - `:returns`: `sp.coo_matrix`
    >


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.reshape" class="docs-object-method">&nbsp;</a> 
```python
reshape(self, newshape): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2698)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2698?message=Update%20Docs)]
</div>
Returns a reshaped version of the tensor
  - `axes`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.__truediv__" class="docs-object-method">&nbsp;</a> 
```python
__truediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2710)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2710?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.__rtruediv__" class="docs-object-method">&nbsp;</a> 
```python
__rtruediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2713)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2713?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.__rmul__" class="docs-object-method">&nbsp;</a> 
```python
__rmul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2716)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2716?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2719)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2719?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.true_multiply" class="docs-object-method">&nbsp;</a> 
```python
true_multiply(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2722)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2722?message=Update%20Docs)]
</div>
Multiplies self and other
  - `other`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.TensorFlowSparseArray.dot" class="docs-object-method">&nbsp;</a> 
```python
dot(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/TensorFlowSparseArray.py#L2776)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/TensorFlowSparseArray.py#L2776?message=Update%20Docs)]
</div>
Takes a regular dot product of self and other
  - `other`: `Any`
    > 
  - `axes`: `Any`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Sparse/TensorFlowSparseArray.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Sparse/TensorFlowSparseArray.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Sparse/TensorFlowSparseArray.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Sparse/TensorFlowSparseArray.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse.py#L2558?message=Update%20Docs)   
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