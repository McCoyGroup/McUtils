## <a id="McUtils.Scaffolding.Serializers.BaseSerializer">BaseSerializer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L318)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L318?message=Update%20Docs)]
</div>

Serializer base class to define the interface







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_extension: str
binary: bool
registry_name: NoneType
registry: dict
```
<a id="McUtils.Scaffolding.Serializers.BaseSerializer.register" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
register(cls, name, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L328)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L328?message=Update%20Docs)]
</div>
**LLM Docstring**

Register a serializer class under a name, either immediately or through decorator syntax.
  - `name`: `object`
    > registry, command, resource, or object name
  - `serializer`: `object`
    > serializer instance or specification
  - `:returns`: `None | object`
    > No explicit value unless noted by the underlying delegated operation.


<a id="McUtils.Scaffolding.Serializers.BaseSerializer.construct" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct(cls, serializer_type, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L360)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L360?message=Update%20Docs)]
</div>
**LLM Docstring**

Return an existing serializer or instantiate one resolved from a registry name or class.
  - `serializer_type`: `object`
    > serializer instance, registry name, or class
  - `kwargs`: `object`
    > keyword arguments forwarded to a callable
  - `:returns`: `object`
    > The resolved or newly constructed helper object.


<a id="McUtils.Scaffolding.Serializers.BaseSerializer.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L379)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L379?message=Update%20Docs)]
</div>
Converts data into a serializable format
  - `data`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Serializers.BaseSerializer.deconvert" class="docs-object-method">&nbsp;</a> 
```python
deconvert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L389)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L389?message=Update%20Docs)]
</div>
Converts data from a serialized format into a python format
  - `data`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Serializers.BaseSerializer.serialize" class="docs-object-method">&nbsp;</a> 
```python
serialize(self, file, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L399)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L399?message=Update%20Docs)]
</div>
Writes the data
  - `file`: `Any`
    > 
  - `data`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Serializers.BaseSerializer.dumps" class="docs-object-method">&nbsp;</a> 
```python
dumps(self, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L411)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L411?message=Update%20Docs)]
</div>
Write data to a string
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Serializers.BaseSerializer.deserialize" class="docs-object-method">&nbsp;</a> 
```python
deserialize(self, file, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L425)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L425?message=Update%20Docs)]
</div>
Loads data from a file
  - `file`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Serializers.BaseSerializer.loads" class="docs-object-method">&nbsp;</a> 
```python
loads(self, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L435)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/BaseSerializer.py#L435?message=Update%20Docs)]
</div>
Write data to a string
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/BaseSerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/BaseSerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/BaseSerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/BaseSerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L318?message=Update%20Docs)   
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