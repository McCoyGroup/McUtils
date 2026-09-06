## <a id="McUtils.Numputils.Serialization.MemmappedNPZFile">MemmappedNPZFile</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization.py#L121)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization.py#L121?message=Update%20Docs)]
</div>

Lazy, memory-mapped stand-in for `numpy.lib.npyio.NpzFile`.

Only works for archives written with `np.savez` (uncompressed). Each
array is memmapped the first time it's accessed and then cached.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, path, mode: 'str' = 'r'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization.py#L129)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization.py#L129?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, key: 'str') -> 'np.memmap': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L140)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L140?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, key: 'str') -> 'bool': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L149)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L149?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self) -> 'Iterator[str]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L152?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self) -> 'int': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L155)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L155?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L158)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L158?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.values" class="docs-object-method">&nbsp;</a> 
```python
values(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L161)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L161?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.items" class="docs-object-method">&nbsp;</a> 
```python
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L164?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.get" class="docs-object-method">&nbsp;</a> 
```python
get(self, key, default=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L167)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L167?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.close" class="docs-object-method">&nbsp;</a> 
```python
close(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L171)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L171?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L175?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, *exc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L178)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L178?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Serialization.MemmappedNPZFile.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L181)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization/MemmappedNPZFile.py#L181?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Serialization/MemmappedNPZFile.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Serialization/MemmappedNPZFile.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Serialization/MemmappedNPZFile.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Serialization/MemmappedNPZFile.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization.py#L121?message=Update%20Docs)   
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