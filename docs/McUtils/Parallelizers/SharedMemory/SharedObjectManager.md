## <a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager">SharedObjectManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory.py#L1038)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L1038?message=Update%20Docs)]
</div>

Provides a high-level interface to create a manager
that supports shared memory objects through the multiprocessing
interface
Only supports data that can be marshalled into a NumPy array.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
primitive_types: tuple
```
<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, obj, base_dict=None, parallelizer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory.py#L1046)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L1046?message=Update%20Docs)]
</div>

  - `mem_manager`: `Any`
    > a memory manager like `multiprocessing.SharedMemoryManager`
  - `obj`: `Any`
    > the object whose attributes should be given by shared memory objects
  - `base_dict`: `SharedMemoryDict`
    > the dict that stores the shared arrays (can also be shared)


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.is_primitive" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_primitive(cls, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1070)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1070?message=Update%20Docs)]
</div>
**LLM Docstring**

Return whether a value belongs to the container and ndarray types wrapped in `PrimitiveTypeHolder`.
  - `val`: `Any`
    > Value supplied for `val`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.save_attr" class="docs-object-method">&nbsp;</a> 
```python
save_attr(self, attr): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1084)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1084?message=Update%20Docs)]
</div>
**LLM Docstring**

Move an object attribute into the shared dictionary and replace it with a `SharedAttribute` marker.
  - `attr`: `Any`
    > Value supplied for `attr`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.del_attr" class="docs-object-method">&nbsp;</a> 
```python
del_attr(self, attr): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1102?message=Update%20Docs)]
</div>
**LLM Docstring**

Delete a shared attribute's backing entry when marked, then remove the object attribute.
  - `attr`: `Any`
    > Value supplied for `attr`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.load_attr" class="docs-object-method">&nbsp;</a> 
```python
load_attr(self, attr): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1118)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1118?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a marked shared attribute and replace the marker on the object with the stored representation.
  - `attr`: `Any`
    > Value supplied for `attr`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.get_saved_keys" class="docs-object-method">&nbsp;</a> 
```python
get_saved_keys(self, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1135)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1135?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the keys currently present in the managed object's `__dict__`.
  - `obj`: `Any`
    > Value supplied for `obj`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.save_keys" class="docs-object-method">&nbsp;</a> 
```python
save_keys(self, keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1148)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1148?message=Update%20Docs)]
</div>
**LLM Docstring**

Share each requested object attribute, defaulting to all keys in the object dictionary.
  - `keys`: `Any`
    > Value supplied for `keys`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.share" class="docs-object-method">&nbsp;</a> 
```python
share(self, keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1164?message=Update%20Docs)]
</div>
**LLM Docstring**

Delegate to an object-specific `share` method when present, otherwise share selected attributes.
  - `keys`: `Any`
    > Value supplied for `keys`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.load_keys" class="docs-object-method">&nbsp;</a> 
```python
load_keys(self, keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1186)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1186?message=Update%20Docs)]
</div>
**LLM Docstring**

Load each requested shared attribute, defaulting to all object dictionary keys.
  - `keys`: `Any`
    > Value supplied for `keys`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.unshare" class="docs-object-method">&nbsp;</a> 
```python
unshare(self, keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1202)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1202?message=Update%20Docs)]
</div>
**LLM Docstring**

Delegate to an object-specific `unshare` method or restore attributes and unwrap primitive holders.
  - `keys`: `Any`
    > Value supplied for `keys`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.__del__" class="docs-object-method">&nbsp;</a> 
```python
__del__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1243)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1243?message=Update%20Docs)]
</div>
**LLM Docstring**

Run best-effort cleanup when the manager is finalized.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.list" class="docs-object-method">&nbsp;</a> 
```python
list(self, *l): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1257)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1257?message=Update%20Docs)]
</div>
**LLM Docstring**

Create a `SharedMemoryList` reusing this manager's synchronization manager, marshaller, allocator, and parallelizer.
  - `l`: `Any`
    > Value supplied for `l`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.dict" class="docs-object-method">&nbsp;</a> 
```python
dict(self, *d): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1274)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1274?message=Update%20Docs)]
</div>
**LLM Docstring**

Create a `SharedMemoryDict` reusing this manager's synchronization manager, marshaller, allocator, and parallelizer.
  - `d`: `Any`
    > Value supplied for `d`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.array" class="docs-object-method">&nbsp;</a> 
```python
array(self, a): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1291)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L1291?message=Update%20Docs)]
</div>
**LLM Docstring**

Return an existing shared array unchanged or allocate a new shared-memory copy.
  - `a`: `Any`
    > Value supplied for `a`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers/SharedMemory/SharedObjectManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers/SharedMemory/SharedObjectManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers/SharedMemory/SharedObjectManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers/SharedMemory/SharedObjectManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L1038?message=Update%20Docs)   
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