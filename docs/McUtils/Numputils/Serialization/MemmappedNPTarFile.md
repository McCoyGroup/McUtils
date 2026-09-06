## <a id="McUtils.Numputils.Serialization.MemmappedNPTarFile">MemmappedNPTarFile</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization.py#L218)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization.py#L218?message=Update%20Docs)]
</div>

Lazy, memory-mapped reader for `.nptar` archives: plain (uncompressed)
tar files whose members are `.npy` arrays, written by `save_nptar`.

Same access pattern as `MemmappedNPZFile` / `NpzFile`.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, path, mode: 'str' = 'r'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization.py#L226)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization.py#L226?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, key: 'str') -> 'np.memmap': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L235)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L235?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, key: 'str') -> 'bool': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L244)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L244?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self) -> 'Iterator[str]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L247)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L247?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self) -> 'int': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L250)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L250?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L253)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L253?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.values" class="docs-object-method">&nbsp;</a> 
```python
values(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L256)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L256?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.items" class="docs-object-method">&nbsp;</a> 
```python
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L259)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L259?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.get" class="docs-object-method">&nbsp;</a> 
```python
get(self, key, default=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L262)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L262?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.close" class="docs-object-method">&nbsp;</a> 
```python
close(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L265)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L265?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L268)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L268?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, *exc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L271?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPTarFile.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L274)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPTarFile.py#L274?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Serialization/MemmappedNPTarFile.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Serialization/MemmappedNPTarFile.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Serialization/MemmappedNPTarFile.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Serialization/MemmappedNPTarFile.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization.py#L218?message=Update%20Docs)   
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