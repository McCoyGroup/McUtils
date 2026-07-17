## <a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict">SharedMemoryDict</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory.py#L858)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L858?message=Update%20Docs)]
</div>

Implements a shared dict that uses
a managed dict to synchronize array metainfo
across processes







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *seq, sync_dict=None, manager=None, marshaller=None, allocator=None, parallelizer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory.py#L865)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L865?message=Update%20Docs)]
</div>

  - `marshaller`: `Any`
    > 
  - `sync_dict`: `Any`
    > 
  - `allocator`: `Any`
    > 
  - `parallelizer`: `Any`
    >


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.__getstate__" class="docs-object-method">&nbsp;</a> 
```python
__getstate__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L890)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L890?message=Update%20Docs)]
</div>
**LLM Docstring**

Return picklable dictionary state while dropping the local manager object.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L902)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L902?message=Update%20Docs)]
</div>
**LLM Docstring**

Test key membership in the synchronized backing dictionary.
  - `item`: `Any`
    > Value supplied for `item`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L914)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L914?message=Update%20Docs)]
</div>
**LLM Docstring**

Iterate over keys in the synchronized backing dictionary.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L923)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L923?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the number of entries in the synchronized backing dictionary.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.__del__" class="docs-object-method">&nbsp;</a> 
```python
__del__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L932)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L932?message=Update%20Docs)]
</div>
**LLM Docstring**

On the main process, attempt to delete every stored key and release its shared arrays.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L947)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L947?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the backing dictionary's dynamic key view.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.values" class="docs-object-method">&nbsp;</a> 
```python
values(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L956)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L956?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the backing dictionary's dynamic value view of shared representations.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.items" class="docs-object-method">&nbsp;</a> 
```python
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L965)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L965?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the backing dictionary's dynamic item view.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.unshare" class="docs-object-method">&nbsp;</a> 
```python
unshare(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L974)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L974?message=Update%20Docs)]
</div>
**LLM Docstring**

Reconstruct all entries into a process-local dictionary.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.update" class="docs-object-method">&nbsp;</a> 
```python
update(self, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L984)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.py#L984?message=Update%20Docs)]
</div>
**LLM Docstring**

Reserve the incoming keys and marshal each incoming value into shared storage.
  - `v`: `Any`
    > Value supplied for `v`.
  - `:returns`: `None`
    > None.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L858?message=Update%20Docs)   
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