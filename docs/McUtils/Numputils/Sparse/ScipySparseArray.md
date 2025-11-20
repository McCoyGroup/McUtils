## <a id="McUtils.Numputils.Sparse.ScipySparseArray">ScipySparseArray</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse.py#L719)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse.py#L719?message=Update%20Docs)]
</div>

Array class that generalize the regular `scipy.sparse.spmatrix`.
Basically acts like a high-dimensional wrapper that manages the _shape_ of a standard `scipy.sparse_matrix`, since that is rigidly 2D.
We always use a combo of an underlying CSR or CSC matrix & COO-like shape operations.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
formats_map: dict
default_cache_size: int
caching_enabled: bool
```
<a id="McUtils.Numputils.Sparse.ScipySparseArray.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, a, shape=None, layout=None, dtype=None, initialize=True, cache_block_data=None, logger=None, init_kwargs=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse.py#L726)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse.py#L726?message=Update%20Docs)]
</div>

  - `a`: `Any`
    > 
  - `shape`: `Any`
    > 
  - `layout`: `Any`
    > 
  - `dtype`: `Any`
    > 
  - `initialize`: `Any`
    > 
  - `cache_block_data`: `Any`
    > whether or not
  - `logger`: `Logger`
    > the logger to use for debug purposes


<a id="McUtils.Numputils.Sparse.ScipySparseArray.coo_to_cs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
coo_to_cs(cls, shape, vals, ij_inds, memmap=False, assume_sorted=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L767)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L767?message=Update%20Docs)]
</div>
Reimplementation of scipy's internal "coo_tocsr" for memory-limited situations
Assumes `ij_inds` are sorted by row then column, which allows vals to be used
directly once indptr is computed
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.ScipySparseArray.to_state" class="docs-object-method">&nbsp;</a> 
```python
to_state(self, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L851)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L851?message=Update%20Docs)]
</div>
Provides just the state that is needed to
serialize the object
  - `serializer`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.ScipySparseArray.from_state" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_state(cls, state, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L866)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L866?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.initialize_empty" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
initialize_empty(cls, shape, dtype=None, layout=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L877)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L877?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.construct_sparse_from_val_inds" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct_sparse_from_val_inds(cls, a, shape, fmt, cache_block_data=True, logger=None, assume_sorted=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L991)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L991?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.dtype" class="docs-object-method">&nbsp;</a> 
```python
@property
dtype(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1169?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.diag" class="docs-object-method">&nbsp;</a> 
```python
@property
diag(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1173)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1173?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.from_diagonal_data" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_diagonal_data(cls, diags, shape=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1181)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1181?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.asarray" class="docs-object-method">&nbsp;</a> 
```python
asarray(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1197?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.todense" class="docs-object-method">&nbsp;</a> 
```python
todense(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1199)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1199?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.ascoo" class="docs-object-method">&nbsp;</a> 
```python
ascoo(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1201)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1201?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.ascsr" class="docs-object-method">&nbsp;</a> 
```python
ascsr(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1203)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1203?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.ascsc" class="docs-object-method">&nbsp;</a> 
```python
ascsc(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1205)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1205?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.data" class="docs-object-method">&nbsp;</a> 
```python
@property
data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1207)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1207?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.format_from_string" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
format_from_string(cls, fmt): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1234)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1234?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.fmt" class="docs-object-method">&nbsp;</a> 
```python
@property
fmt(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1242)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1242?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1250)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1250?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.ndim" class="docs-object-method">&nbsp;</a> 
```python
@property
ndim(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1257)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1257?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.non_zero_count" class="docs-object-method">&nbsp;</a> 
```python
@property
non_zero_count(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1260)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1260?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.get_caching_status" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_caching_status(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1267)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1267?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.enable_caches" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
enable_caches(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1270)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1270?message=Update%20Docs)]
</div>
A method to be overloaded.
Subclasses may want to cache things for performance, so we
provide a way for them to turn this on
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.ScipySparseArray.disable_caches" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
disable_caches(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1280)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1280?message=Update%20Docs)]
</div>
A method to be overloaded.
Subclasses may want to cache things for performance, so we
provide a way for them to turn this off
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.ScipySparseArray.clear_cache" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
clear_cache(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1290)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1290?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.clear_ravel_caches" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
clear_ravel_caches(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1293)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1293?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.set_ravel_cache_size" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
set_ravel_cache_size(cls, size): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1328)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1328?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.find" class="docs-object-method">&nbsp;</a> 
```python
find(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1388)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1388?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.block_vals" class="docs-object-method">&nbsp;</a> 
```python
@property
block_vals(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1433)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1433?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.block_inds" class="docs-object-method">&nbsp;</a> 
```python
@property
block_inds(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1445)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1445?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.block_data" class="docs-object-method">&nbsp;</a> 
```python
@property
block_data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1487)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1487?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.transpose" class="docs-object-method">&nbsp;</a> 
```python
transpose(self, transp): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1502)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1502?message=Update%20Docs)]
</div>
Transposes the array and returns a new one.
Not necessarily a cheap operation.
  - `transp`: `Iterable[int]`
    > the transposition to do
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.ScipySparseArray.reshape_internal" class="docs-object-method">&nbsp;</a> 
```python
reshape_internal(self, shp): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1637)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1637?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.reshape" class="docs-object-method">&nbsp;</a> 
```python
reshape(self, shp): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1677)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1677?message=Update%20Docs)]
</div>
Had to make this op not in-place because otherwise got scary errors...
  - `shp`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.ScipySparseArray.pad_right" class="docs-object-method">&nbsp;</a> 
```python
pad_right(self, amounts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1691)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1691?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.squeeze" class="docs-object-method">&nbsp;</a> 
```python
squeeze(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1696)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1696?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.resize" class="docs-object-method">&nbsp;</a> 
```python
resize(self, newsize): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1700)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1700?message=Update%20Docs)]
</div>
Returns a resized version of the tensor
  - `newsize`: `tuple[int]`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.ScipySparseArray.concatenate_coo" class="docs-object-method">&nbsp;</a> 
```python
concatenate_coo(self, *others, axis=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1759)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1759?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.concatenate_2d" class="docs-object-method">&nbsp;</a> 
```python
concatenate_2d(self, *others, axis=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1834)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1834?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.concatenate" class="docs-object-method">&nbsp;</a> 
```python
concatenate(self, *others, axis=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1849)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1849?message=Update%20Docs)]
</div>
Concatenates multiple arrays along the specified axis
This is relatively inefficient in terms of not tracking indices
throughout
  - `other`: `Any`
    > 
  - `axis`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.ScipySparseArray.broadcast_values" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
broadcast_values(cls, new_shape, old_shape, vals, inds): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1923)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1923?message=Update%20Docs)]
</div>
Implements broadcast_to using COO-style operations
to be a little bit more efficient
  - `shape`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.ScipySparseArray.broadcast_to" class="docs-object-method">&nbsp;</a> 
```python
broadcast_to(self, shape): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1966)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1966?message=Update%20Docs)]
</div>
Broadcasts to shape
  - `shape`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.Sparse.ScipySparseArray.expand_and_broadcast_to" class="docs-object-method">&nbsp;</a> 
```python
expand_and_broadcast_to(self, expansion, new_shape): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1983)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1983?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.expand_and_pad" class="docs-object-method">&nbsp;</a> 
```python
expand_and_pad(self, expansion, padding): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1995)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L1995?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.T" class="docs-object-method">&nbsp;</a> 
```python
@property
T(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2019)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2019?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__matmul__" class="docs-object-method">&nbsp;</a> 
```python
__matmul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2025)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2025?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.ascs" class="docs-object-method">&nbsp;</a> 
```python
ascs(self, inplace=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2036)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2036?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.dot" class="docs-object-method">&nbsp;</a> 
```python
dot(self, b, reverse=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2042)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2042?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.outer" class="docs-object-method">&nbsp;</a> 
```python
outer(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2079)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2079?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__neg__" class="docs-object-method">&nbsp;</a> 
```python
__neg__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2096)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2096?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__pos__" class="docs-object-method">&nbsp;</a> 
```python
__pos__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2098)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2098?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2100)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2100?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__iadd__" class="docs-object-method">&nbsp;</a> 
```python
__iadd__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2102?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__radd__" class="docs-object-method">&nbsp;</a> 
```python
__radd__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2104)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2104?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.plus" class="docs-object-method">&nbsp;</a> 
```python
plus(self, other, inplace=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2106?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.floopy_flop" class="docs-object-method">&nbsp;</a> 
```python
floopy_flop(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2145)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2145?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__truediv__" class="docs-object-method">&nbsp;</a> 
```python
__truediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2148)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2148?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__rtruediv__" class="docs-object-method">&nbsp;</a> 
```python
__rtruediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2150)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2150?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__rmul__" class="docs-object-method">&nbsp;</a> 
```python
__rmul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2154?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2156?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.true_multiply" class="docs-object-method">&nbsp;</a> 
```python
true_multiply(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2158)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2158?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2189)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2189?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.savez" class="docs-object-method">&nbsp;</a> 
```python
savez(self, file, compressed=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2496)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2496?message=Update%20Docs)]
</div>
Saves a SparseArray to a file (must have the npz extension)
  - `file`: `Any`
    > 
  - `compressed`: `Any`
    > 
  - `:returns`: `str`
    > t
h
e
 
s
a
v
e
d
 
f
i
l
e


<a id="McUtils.Numputils.Sparse.ScipySparseArray.loadz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
loadz(cls, file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2535)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2535?message=Update%20Docs)]
</div>
Loads a SparseArray from an npz file
  - `file`: `Any`
    > 
  - `:returns`: `SparseArray`
    >


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2551)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2551?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, item, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2553)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2553?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__delitem__" class="docs-object-method">&nbsp;</a> 
```python
__delitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2555)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2555?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Sparse.ScipySparseArray.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2558)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse/ScipySparseArray.py#L2558?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Sparse/ScipySparseArray.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Sparse/ScipySparseArray.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Sparse/ScipySparseArray.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Sparse/ScipySparseArray.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Sparse.py#L719?message=Update%20Docs)   
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