## <a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList">SharedMemoryList</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory.py#L476)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory.py#L476?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryList.py#L483)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryList.py#L483?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryList.py#L508)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryList.py#L508?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryList.py#L513)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryList.py#L513?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryList.py#L515)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryList.py#L515?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryList.py#L517)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryList.py#L517?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.__del__" class="docs-object-method">&nbsp;</a> 
```python
__del__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryList.py#L519)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryList.py#L519?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.unshare" class="docs-object-method">&nbsp;</a> 
```python
unshare(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryList.py#L523)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryList.py#L523?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.pop" class="docs-object-method">&nbsp;</a> 
```python
pop(self, k=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryList.py#L526)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryList.py#L526?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.insert" class="docs-object-method">&nbsp;</a> 
```python
insert(self, k, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryList.py#L529)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryList.py#L529?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.append" class="docs-object-method">&nbsp;</a> 
```python
append(self, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryList.py#L532)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryList.py#L532?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryList.extend" class="docs-object-method">&nbsp;</a> 
```python
extend(self, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryList.py#L535)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryList.py#L535?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory.py#L476?message=Update%20Docs)   
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