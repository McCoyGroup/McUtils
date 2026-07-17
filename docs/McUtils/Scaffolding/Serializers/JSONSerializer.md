## <a id="McUtils.Scaffolding.Serializers.JSONSerializer">JSONSerializer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L593)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L593?message=Update%20Docs)]
</div>

A serializer that makes dumping data to JSON simpler







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_extension: str
BaseEncoder: BaseEncoder
registry_name: str
```
<a id="McUtils.Scaffolding.Serializers.JSONSerializer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, encoder=None, allow_pickle=True, pseudopickler=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L649)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L649?message=Update%20Docs)]
</div>
**LLM Docstring**

Configure the JSON encoder, pseudo-pickler, and unsupported-object fallback policy.
  - `encoder`: `object`
    > JSON encoder instance
  - `allow_pickle`: `object`
    > whether unsupported values may fall back to pickle
  - `pseudopickler`: `object`
    > pseudo-pickler used for arbitrary objects
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Serializers.JSONSerializer.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L670)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L670?message=Update%20Docs)]
</div>
**LLM Docstring**

Encode data to a JSON string and mark it as converted.
  - `data`: `object`
    > data to serialize, convert, or write
  - `:returns`: `object`
    > The converted representation described above.


<a id="McUtils.Scaffolding.Serializers.JSONSerializer.deconvert" class="docs-object-method">&nbsp;</a> 
```python
deconvert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L682)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L682?message=Update%20Docs)]
</div>
**LLM Docstring**

Return decoded JSON data unchanged before optional pseudo-pickle restoration.
  - `data`: `object`
    > data to serialize, convert, or write
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Serializers.JSONSerializer.serialize" class="docs-object-method">&nbsp;</a> 
```python
serialize(self, file, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L694)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L694?message=Update%20Docs)]
</div>
**LLM Docstring**

JSON-encode input when needed and write the resulting text.
  - `file`: `object`
    > path or file-like object
  - `data`: `object`
    > data to serialize, convert, or write
  - `kwargs`: `object`
    > keyword arguments forwarded to a callable
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Serializers.JSONSerializer.dumps" class="docs-object-method">&nbsp;</a> 
```python
dumps(self, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L712)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L712?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the JSON text representation directly.
  - `data`: `object`
    > data to serialize, convert, or write
  - `kwargs`: `object`
    > keyword arguments forwarded to a callable
  - `:returns`: `str`
    > the JSON document text


<a id="McUtils.Scaffolding.Serializers.JSONSerializer.loads" class="docs-object-method">&nbsp;</a> 
```python
loads(self, file, key=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L753)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L753?message=Update%20Docs)]
</div>
**LLM Docstring**

Decode JSON text and postprocess optional key selection and pseudo-pickled values.
  - `file`: `object`
    > path or file-like object
  - `key`: `object`
    > the storage or lookup key
  - `kwargs`: `object`
    > keyword arguments forwarded to a callable
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Serializers.JSONSerializer.deserialize" class="docs-object-method">&nbsp;</a> 
```python
deserialize(self, file, key=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L771)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/JSONSerializer.py#L771?message=Update%20Docs)]
</div>
**LLM Docstring**

Decode JSON from a file object and postprocess optional key selection and pseudo-pickled values.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/JSONSerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/JSONSerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/JSONSerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/JSONSerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L593?message=Update%20Docs)   
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