## <a id="McUtils.Scaffolding.Serializers.NumPySerializer">NumPySerializer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L1669)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L1669?message=Update%20Docs)]
</div>

A serializer that implements NPZ dumps







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_extension: str
binary: bool
atomic_types: tuple
converter_dispatch: NoneType
dict_key_sep: str
registry_name: str
```
<a id="McUtils.Scaffolding.Serializers.NumPySerializer.get_default_converters" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_default_converters(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1681)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1681?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the ordered dispatch table for NumPy arrays, array-like objects, scalars, mappings, and sequences.
  - `:returns`: `collections.OrderedDict`
    > an ordered converter-dispatch mapping


<a id="McUtils.Scaffolding.Serializers.NumPySerializer.get_converters" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_converters(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1699)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1699?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the custom converter dispatch or the default converter mapping.
  - `:returns`: `collections.OrderedDict`
    > the active converter-dispatch mapping


<a id="McUtils.Scaffolding.Serializers.NumPySerializer.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumPySerializer.py#L1812)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumPySerializer.py#L1812?message=Update%20Docs)]
</div>
**LLM Docstring**

Recursively convert data and flatten nested dictionaries into separator-delimited NPZ keys.
  - `data`: `object`
    > data to serialize, convert, or write
  - `:returns`: `object`
    > The converted representation described above.


<a id="McUtils.Scaffolding.Serializers.NumPySerializer.deconvert" class="docs-object-method">&nbsp;</a> 
```python
deconvert(self, data, sep=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumPySerializer.py#L1856)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumPySerializer.py#L1856?message=Update%20Docs)]
</div>
Unflattens nested dictionary structures so that the original data
can be recovered
  - `data`: `Any`
    > 
  - `sep`: `str | None`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Serializers.NumPySerializer.serialize" class="docs-object-method">&nbsp;</a> 
```python
serialize(self, file, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumPySerializer.py#L1888)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumPySerializer.py#L1888?message=Update%20Docs)]
</div>
**LLM Docstring**

Write a single array with `np.save` or a flattened mapping with `np.savez`.
  - `file`: `object`
    > path or file-like object
  - `data`: `object`
    > data to serialize, convert, or write
  - `kwargs`: `object`
    > keyword arguments forwarded to a callable
  - `:returns`: `None | object`
    > No explicit value unless noted by the underlying delegated operation.


<a id="McUtils.Scaffolding.Serializers.NumPySerializer.deserialize" class="docs-object-method">&nbsp;</a> 
```python
deserialize(self, file, key=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumPySerializer.py#L1910)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumPySerializer.py#L1910?message=Update%20Docs)]
</div>
**LLM Docstring**

Load NumPy data, reconstruct nested structures, and optionally select a slash-separated key.
  - `file`: `object`
    > path or file-like object
  - `key`: `object`
    > the storage or lookup key
  - `kwargs`: `object`
    > keyword arguments forwarded to a callable
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/NumPySerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/NumPySerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/NumPySerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/NumPySerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L1669?message=Update%20Docs)   
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