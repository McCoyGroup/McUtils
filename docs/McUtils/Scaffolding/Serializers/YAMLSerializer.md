## <a id="McUtils.Scaffolding.Serializers.YAMLSerializer">YAMLSerializer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L790)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L790?message=Update%20Docs)]
</div>

A serializer that makes dumping data to YAML simpler.
Doesn't support arbitrary python objects since that hasn't seemed like
a huge need yet...







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_extension: str
registry_name: str
```
<a id="McUtils.Scaffolding.Serializers.YAMLSerializer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L798)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L798?message=Update%20Docs)]
</div>
**LLM Docstring**

Import and retain the YAML backend, raising at construction time when YAML support is unavailable.
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Serializers.YAMLSerializer.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/YAMLSerializer.py#L811)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/YAMLSerializer.py#L811?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap YAML-compatible data without structural conversion.
  - `data`: `object`
    > data to serialize, convert, or write
  - `:returns`: `object`
    > The converted representation described above.


<a id="McUtils.Scaffolding.Serializers.YAMLSerializer.deconvert" class="docs-object-method">&nbsp;</a> 
```python
deconvert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/YAMLSerializer.py#L823)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/YAMLSerializer.py#L823?message=Update%20Docs)]
</div>
**LLM Docstring**

Return YAML-loaded data unchanged.
  - `data`: `object`
    > data to serialize, convert, or write
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Serializers.YAMLSerializer.serialize" class="docs-object-method">&nbsp;</a> 
```python
serialize(self, file, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/YAMLSerializer.py#L835)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/YAMLSerializer.py#L835?message=Update%20Docs)]
</div>
**LLM Docstring**

Dump converted or raw data through the YAML API.
  - `file`: `object`
    > path or file-like object
  - `data`: `object`
    > data to serialize, convert, or write
  - `kwargs`: `object`
    > keyword arguments forwarded to a callable
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Serializers.YAMLSerializer.deserialize" class="docs-object-method">&nbsp;</a> 
```python
deserialize(self, file, key=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/YAMLSerializer.py#L854)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/YAMLSerializer.py#L854?message=Update%20Docs)]
</div>
**LLM Docstring**

Load YAML data, deconvert it, and optionally select a nested slash-separated key.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/YAMLSerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/YAMLSerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/YAMLSerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/YAMLSerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L790?message=Update%20Docs)   
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