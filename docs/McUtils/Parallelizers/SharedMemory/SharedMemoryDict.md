## <a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict">SharedMemoryDict</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory.py#L541)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory.py#L541?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L548)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L548?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L573)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L573?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L578)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L578?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L580)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L580?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L582)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L582?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.__del__" class="docs-object-method">&nbsp;</a> 
```python
__del__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L584)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L584?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L592)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L592?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.values" class="docs-object-method">&nbsp;</a> 
```python
values(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L594)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L594?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.items" class="docs-object-method">&nbsp;</a> 
```python
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L596)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L596?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.unshare" class="docs-object-method">&nbsp;</a> 
```python
unshare(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L598)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L598?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.SharedMemory.SharedMemoryDict.update" class="docs-object-method">&nbsp;</a> 
```python
update(self, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L601)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory/SharedMemoryDict.py#L601?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/SharedMemory.py#L541?message=Update%20Docs)   
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