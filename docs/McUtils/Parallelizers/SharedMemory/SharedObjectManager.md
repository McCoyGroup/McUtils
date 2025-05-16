## <a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager">SharedObjectManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory.py#L616)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L616?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory.py#L624)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L624?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L648)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L648?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.save_attr" class="docs-object-method">&nbsp;</a> 
```python
save_attr(self, attr): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L652)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L652?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.del_attr" class="docs-object-method">&nbsp;</a> 
```python
del_attr(self, attr): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L660)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L660?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.load_attr" class="docs-object-method">&nbsp;</a> 
```python
load_attr(self, attr): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L666)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L666?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.get_saved_keys" class="docs-object-method">&nbsp;</a> 
```python
get_saved_keys(self, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L673)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L673?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.save_keys" class="docs-object-method">&nbsp;</a> 
```python
save_keys(self, keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L676)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L676?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.share" class="docs-object-method">&nbsp;</a> 
```python
share(self, keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L682)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L682?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.load_keys" class="docs-object-method">&nbsp;</a> 
```python
load_keys(self, keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L694)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L694?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.unshare" class="docs-object-method">&nbsp;</a> 
```python
unshare(self, keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L700)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L700?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.__del__" class="docs-object-method">&nbsp;</a> 
```python
__del__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L724)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L724?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.list" class="docs-object-method">&nbsp;</a> 
```python
list(self, *l): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L731)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L731?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.dict" class="docs-object-method">&nbsp;</a> 
```python
dict(self, *d): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L738)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L738?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedObjectManager.array" class="docs-object-method">&nbsp;</a> 
```python
array(self, a): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L745)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedObjectManager.py#L745?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers/SharedMemory/SharedObjectManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers/SharedMemory/SharedObjectManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers/SharedMemory/SharedObjectManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers/SharedMemory/SharedObjectManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L616?message=Update%20Docs)   
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