## <a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray">SharedMemoryNDarray</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory.py#L63)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L63?message=Update%20Docs)]
</div>

Provides a very simple tracker for shared NumPy arrays







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, shape, dtype, buf, autoclose=True, parallelizer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory.py#L74)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L74?message=Update%20Docs)]
</div>

  - `shape`: `tuple[int]`
    > 
  - `dtype`: `np.dtype`
    > 
  - `buf`: `SharedMemoryInterface`
    > 
  - `parallelizer`: `Parallelizer`
    >


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray.__getstate__" class="docs-object-method">&nbsp;</a> 
```python
__getstate__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L176)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L176?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the array metadata, buffer handle, cleanup policy, and parallelizer without serializing the NumPy view.
  - `:returns`: `dict`
    > The serializable state mapping.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray.__setstate__" class="docs-object-method">&nbsp;</a> 
```python
__setstate__(self, state): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L192)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L192?message=Update%20Docs)]
</div>
**LLM Docstring**

Restore serialized metadata and rebuild the NumPy view over the shared buffer.
  - `state`: `Any`
    > Value supplied for `state`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray.from_array" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_array(cls, arr, buf, autoclose=None, parallelizer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L215)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L215?message=Update%20Docs)]
</div>
Initializes by pulling metainfo from an array
  - `arr`: `np.ndarray`
    > 
  - `buf`: `SharedMemoryInterface`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L239)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L239?message=Update%20Docs)]
</div>
**LLM Docstring**

Assign values through the NumPy view backed by shared memory.
  - `key`: `Any`
    > Value supplied for `key`.
  - `value`: `Any`
    > Value supplied for `value`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L254)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L254?message=Update%20Docs)]
</div>
**LLM Docstring**

Read values through the NumPy view backed by shared memory.
  - `item`: `Any`
    > Value supplied for `item`.
  - `:returns`: `Any`
    > The selected scalar or array view.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray.close" class="docs-object-method">&nbsp;</a> 
```python
close(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L267)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L267?message=Update%20Docs)]
</div>
**LLM Docstring**

Release one local reference and close the underlying buffer when the count reaches zero.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray.unlink" class="docs-object-method">&nbsp;</a> 
```python
unlink(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L281)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L281?message=Update%20Docs)]
</div>
**LLM Docstring**

Unlink the underlying buffer only when no tracked local references remain.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray.__del__" class="docs-object-method">&nbsp;</a> 
```python
__del__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L292)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L292?message=Update%20Docs)]
</div>
**LLM Docstring**

Automatically close and unlink the buffer on the main process when `autoclose` is enabled.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L314)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L314?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a compact representation containing the shared array shape and dtype.
  - `:returns`: `str`
    > A compact description of the shared array.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryNDarray.unshare" class="docs-object-method">&nbsp;</a> 
```python
unshare(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L328)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.py#L328?message=Update%20Docs)]
</div>
**LLM Docstring**

Copy the shared NumPy view into an ordinary process-local array.
  - `:returns`: `np.ndarray`
    > A process-local copy.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers/SharedMemory/SharedMemoryNDarray.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L63?message=Update%20Docs)   
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