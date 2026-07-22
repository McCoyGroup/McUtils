## <a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList">SharedMemoryList</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory.py#L714)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L714?message=Update%20Docs)]
</div>

Implements a shared dict that uses
a managed dict to synchronize array metainfo
across processes







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *seq, sync_list=None, manager=None, marshaller=None, allocator=None, parallelizer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory.py#L721)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L721?message=Update%20Docs)]
</div>

  - `marshaller`: `Any`
    > 
  - `sync_dict`: `Any`
    > 
  - `allocator`: `Any`
    > 
  - `parallelizer`: `Any`
    >


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.__getstate__" class="docs-object-method">&nbsp;</a> 
```python
__getstate__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L746)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L746?message=Update%20Docs)]
</div>
**LLM Docstring**

Return picklable list state while dropping the local manager object.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L758)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L758?message=Update%20Docs)]
</div>
**LLM Docstring**

Test membership against the synchronized backing list.
  - `item`: `Any`
    > Value supplied for `item`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L770)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L770?message=Update%20Docs)]
</div>
**LLM Docstring**

Iterate over the synchronized backing list's stored representations.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L779)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L779?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the number of entries in the synchronized backing list.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.__del__" class="docs-object-method">&nbsp;</a> 
```python
__del__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L788)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L788?message=Update%20Docs)]
</div>
**LLM Docstring**

Attempt to delete every stored entry and release its shared arrays during finalization.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.unshare" class="docs-object-method">&nbsp;</a> 
```python
unshare(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L799)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L799?message=Update%20Docs)]
</div>
**LLM Docstring**

Reconstruct every list entry as process-local data.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.pop" class="docs-object-method">&nbsp;</a> 
```python
pop(self, k=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L809)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L809?message=Update%20Docs)]
</div>
**LLM Docstring**

Remove a stored representation and reconstruct it as process-local data.
  - `k`: `Any`
    > Value supplied for `k`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.insert" class="docs-object-method">&nbsp;</a> 
```python
insert(self, k, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L822)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L822?message=Update%20Docs)]
</div>
**LLM Docstring**

Insert an empty slot and then marshal the supplied value into that position.
  - `k`: `Any`
    > Value supplied for `k`.
  - `v`: `Any`
    > Value supplied for `v`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.append" class="docs-object-method">&nbsp;</a> 
```python
append(self, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L837)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L837?message=Update%20Docs)]
</div>
**LLM Docstring**

Append a placeholder and store the supplied value through the synchronized list. The implementation indexes the new slot using the post-append length.
  - `v`: `Any`
    > Value supplied for `v`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.extend" class="docs-object-method">&nbsp;</a> 
```python
extend(self, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L850)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L850?message=Update%20Docs)]
</div>
**LLM Docstring**

Reserve slots for all values and populate them. The current implementation stores the full input sequence in every new slot rather than each element.
  - `v`: `Any`
    > Value supplied for `v`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.close" class="docs-object-method">&nbsp;</a> 
```python
close(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L866)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory/SharedMemoryList.py#L866?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers/SharedMemory/SharedMemoryList.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers/SharedMemory/SharedMemoryList.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers/SharedMemory/SharedMemoryList.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers/SharedMemory/SharedMemoryList.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/SharedMemory.py#L714?message=Update%20Docs)   
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