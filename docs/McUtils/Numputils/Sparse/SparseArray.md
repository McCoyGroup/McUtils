## <a id="McUtils.Numputils.Sparse.SparseArray">SparseArray</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse.py#L25)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse.py#L25?message=Update%20Docs)]
</div>

Represents a generic sparse array format
which can be subclassed to provide a concrete implementation







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
backends: NoneType
cacheing_manager: cacheing_manager
initializer_list: initializer_list
```
<a id="McUtils.Numputils.Sparse.SparseArray.get_backends" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_backends(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L31)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L31?message=Update%20Docs)]
</div>
Provides the set of backends to try by default
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.from_data" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_data(cls, data, shape=None, dtype=None, target_backend=None, constructor=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L43)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L43?message=Update%20Docs)]
</div>
A wrapper so that we can dispatch to the best
sparse backend we've got defined.
Can be monkey patched.
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `SparseArray`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.from_diag" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_diag(cls, data, shape=None, dtype=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L84)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L84?message=Update%20Docs)]
</div>
A wrapper so that we can dispatch to the best
sparse backend we've got defined.
Can be monkey patched.
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.from_diagonal_data" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_diagonal_data(cls, diags, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L102?message=Update%20Docs)]
</div>
Constructs a sparse tensor from diagonal elements
  - `diags`: `Any`
    > 
  - `kw`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L117)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L117?message=Update%20Docs)]
</div>
Provides the shape of the sparse array
  - `:returns`: `tuple[int]`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.ndim" class="docs-object-method">&nbsp;</a> 
```python
@property
ndim(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L126)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L126?message=Update%20Docs)]
</div>
Provides the number of dimensions in the array
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.to_state" class="docs-object-method">&nbsp;</a> 
```python
to_state(self, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L134)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L134?message=Update%20Docs)]
</div>
Provides just the state that is needed to
serialize the object
  - `serializer`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.from_state" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_state(cls, state, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L145)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L145?message=Update%20Docs)]
</div>
Loads from the stored state
  - `serializer`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.empty" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
empty(cls, shape, dtype=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L157)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L157?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.SparseArray.initialize_empty" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
initialize_empty(cls, shp, shape=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L164?message=Update%20Docs)]
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


<a id="McUtils.Numputils.Sparse.SparseArray.block_data" class="docs-object-method">&nbsp;</a> 
```python
@property
block_data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L180)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L180?message=Update%20Docs)]
</div>
Returns the vector of values and corresponding indices
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.block_inds" class="docs-object-method">&nbsp;</a> 
```python
@property
block_inds(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L190)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L190?message=Update%20Docs)]
</div>
Returns indices for the stored values
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.transpose" class="docs-object-method">&nbsp;</a> 
```python
transpose(self, axes): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L200)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L200?message=Update%20Docs)]
</div>
Returns a transposed version of the tensor
  - `axes`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.ascoo" class="docs-object-method">&nbsp;</a> 
```python
ascoo(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L211)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L211?message=Update%20Docs)]
</div>
Converts the tensor into a scipy COO matrix...
  - `:returns`: `sp.coo_matrix`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.ascsr" class="docs-object-method">&nbsp;</a> 
```python
ascsr(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L220)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L220?message=Update%20Docs)]
</div>
Converts the tensor into a scipy CSR matrix...
  - `:returns`: `sp.csr_matrix`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.asarray" class="docs-object-method">&nbsp;</a> 
```python
asarray(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L228)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L228?message=Update%20Docs)]
</div>
Converts the tensor into a dense np.ndarray
  - `:returns`: `np.ndarray`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.reshape" class="docs-object-method">&nbsp;</a> 
```python
reshape(self, newshape): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L236?message=Update%20Docs)]
</div>
Returns a reshaped version of the tensor
  - `axes`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.resize" class="docs-object-method">&nbsp;</a> 
```python
resize(self, newsize): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L246)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L246?message=Update%20Docs)]
</div>
Returns a resized version of the tensor
  - `axes`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.pad_right" class="docs-object-method">&nbsp;</a> 
```python
pad_right(self, newshape): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L256)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L256?message=Update%20Docs)]
</div>
Returns a right-padded version of the tensor
  - `axes`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.broadcast_to" class="docs-object-method">&nbsp;</a> 
```python
broadcast_to(self, shape) -> 'SparseArray': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L266)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L266?message=Update%20Docs)]
</div>
Returns a broadcasted version of the tensor
  - `axes`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.expand_and_broadcast_to" class="docs-object-method">&nbsp;</a> 
```python
expand_and_broadcast_to(self, expansion, new_shape) -> 'SparseArray': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L276)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L276?message=Update%20Docs)]
</div>
Expands, then broadcasts (memory efficient)
  - `axes`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.expand_and_pad" class="docs-object-method">&nbsp;</a> 
```python
expand_and_pad(self, expansion, padding) -> 'SparseArray': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L287?message=Update%20Docs)]
</div>
Expands, then pads (memory efficient)
  - `axes`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.get_expanded_shape" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_expanded_shape(cls, shape, axis): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L299)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L299?message=Update%20Docs)]
</div>
adapted from np.expand_dims
  - `axis`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.expand_dims" class="docs-object-method">&nbsp;</a> 
```python
expand_dims(self, axis): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L320)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L320?message=Update%20Docs)]
</div>
adapted from np.expand_dims
  - `axis`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.moveaxis" class="docs-object-method">&nbsp;</a> 
```python
moveaxis(self, start, end): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L332)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L332?message=Update%20Docs)]
</div>
Adapted from np.moveaxis
  - `start`: `Any`
    > 
  - `end`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.concatenate" class="docs-object-method">&nbsp;</a> 
```python
concatenate(self, *others, axis=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L361)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L361?message=Update%20Docs)]
</div>
Concatenates multiple SparseArrays along the specified axis
  - `:returns`: `SparseArray`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.__truediv__" class="docs-object-method">&nbsp;</a> 
```python
__truediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L400)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L400?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.SparseArray.__rtruediv__" class="docs-object-method">&nbsp;</a> 
```python
__rtruediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L402)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L402?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.SparseArray.__rmul__" class="docs-object-method">&nbsp;</a> 
```python
__rmul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L404)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L404?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.SparseArray.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L406)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L406?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.SparseArray.true_multiply" class="docs-object-method">&nbsp;</a> 
```python
true_multiply(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L440)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L440?message=Update%20Docs)]
</div>
Multiplies self and other
  - `other`: `Any`
    > 
  - `:returns`: `SparseArray`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.multiply" class="docs-object-method">&nbsp;</a> 
```python
multiply(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L450)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L450?message=Update%20Docs)]
</div>
Multiplies self and other but allows for broadcasting
  - `other`: `SparseArray | np.ndarray | int | float`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.dot" class="docs-object-method">&nbsp;</a> 
```python
dot(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L465)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L465?message=Update%20Docs)]
</div>
Takes a regular dot product of self and other
  - `other`: `Any`
    > 
  - `axes`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.outer" class="docs-object-method">&nbsp;</a> 
```python
outer(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L478)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L478?message=Update%20Docs)]
</div>
Takes a tensor outer product of self and other
  - `other`: `Any`
    > 
  - `axes`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.tensordot" class="docs-object-method">&nbsp;</a> 
```python
tensordot(self, other, axes=2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/Sparse/SparseArray.py#L492)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse/SparseArray.py#L492?message=Update%20Docs)]
</div>
Takes the dot product of self and other along the specified axes
  - `other`: `Any`
    > 
  - `axes`: `Iterable[int] | Iterable[Iterable[int]]`
    > the axes to contract along
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.cache_options" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
cache_options(self, enabled=True, clear=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L632)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L632?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.SparseArray.get_caching_status" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_caching_status(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L635)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L635?message=Update%20Docs)]
</div>
A method to be overloaded.
Subclasses may want to cache things for performance, so we
provide a way for them to specify if caching is on or not
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.enable_caches" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
enable_caches(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L644)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L644?message=Update%20Docs)]
</div>
A method to be overloaded.
Subclasses may want to cache things for performance, so we
provide a way for them to turn this on
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.disable_caches" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
disable_caches(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L653)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L653?message=Update%20Docs)]
</div>
A method to be overloaded.
Subclasses may want to cache things for performance, so we
provide a way for them to turn this off
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.SparseArray.clear_cache" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
clear_cache(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L662)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L662?message=Update%20Docs)]
</div>
A method to be overloaded.
Subclasses may want to cache things for performance, so we
provide a way for them to clear this out.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Sparse/SparseArray.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Sparse/SparseArray.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Sparse/SparseArray.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Sparse/SparseArray.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/Sparse.py#L25?message=Update%20Docs)   
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