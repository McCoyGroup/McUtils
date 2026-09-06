## <a id="McUtils.Parsers.StorageBackends.PythonStorageBackend">PythonStorageBackend</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends.py#L488)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L488?message=Update%20Docs)]
</div>

`numpy`-free backend, storing data as nested Python lists. Never raises
on a shape mismatch -- ragged data is simply ragged -- and never raises
on a cast failure -- the raw string is kept in place of the cast value
and the failure recorded to `self.cast_failures`. This is what makes it
strictly *more permissive* than the numpy backend, which is the whole
point of offering it as `StringParser(regex, backend='python')`.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
name: str
```
<a id="McUtils.Parsers.StorageBackends.PythonStorageBackend.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, casters: 'Optional[Dict[Any, Callable[[str], Any]]]' = None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends.py#L501)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L501?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.PythonStorageBackend.empty" class="docs-object-method">&nbsp;</a> 
```python
empty(self, stype, num_elements, growth): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L507)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L507?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.PythonStorageBackend.append" class="docs-object-method">&nbsp;</a> 
```python
append(self, raw, stype, value, filled_to, growth): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L524)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L524?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.PythonStorageBackend.extend" class="docs-object-method">&nbsp;</a> 
```python
extend(self, raw, stype, values, filled_to, growth, prepend=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L529)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L529?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.PythonStorageBackend.fill" class="docs-object-method">&nbsp;</a> 
```python
fill(self, raw, stype, values): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L535)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L535?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.PythonStorageBackend.cast_to_array" class="docs-object-method">&nbsp;</a> 
```python
cast_to_array(self, raw, stype, txt): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L539)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L539?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.PythonStorageBackend.view" class="docs-object-method">&nbsp;</a> 
```python
view(self, raw, filled_to): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L547)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L547?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.PythonStorageBackend.add_axis" class="docs-object-method">&nbsp;</a> 
```python
add_axis(self, raw, stype): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L550)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L550?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.PythonStorageBackend.set_item" class="docs-object-method">&nbsp;</a> 
```python
set_item(self, raw, stype, key, value, growth): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L553)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L553?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.PythonStorageBackend.to_numpy" class="docs-object-method">&nbsp;</a> 
```python
to_numpy(self, raw, stype, allow_object=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L563)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L563?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.PythonStorageBackend.is_ragged" class="docs-object-method">&nbsp;</a> 
```python
is_ragged(self, raw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L580)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/PythonStorageBackend.py#L580?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/StorageBackends/PythonStorageBackend.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/StorageBackends/PythonStorageBackend.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/StorageBackends/PythonStorageBackend.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/StorageBackends/PythonStorageBackend.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L488?message=Update%20Docs)   
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