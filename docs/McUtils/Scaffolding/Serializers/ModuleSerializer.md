## <a id="McUtils.Scaffolding.Serializers.ModuleSerializer">ModuleSerializer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L1939)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L1939?message=Update%20Docs)]
</div>

A somewhat hacky serializer that supports module-based serialization.
Writes all module parameters to a dict with a given attribute.
Serialization doesn't support loading arbitrary python code, but deserialization does.
Use at your own risk.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_extension: str
binary: bool
default_loader: NoneType
default_attr: str
registry_name: str
```
<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, attr=None, loader=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L1953)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L1953?message=Update%20Docs)]
</div>
**LLM Docstring**

Configure the target module attribute and optional module loader.
  - `attr`: `object`
    > attribute name
  - `loader`: `object`
    > module loader
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.loader" class="docs-object-method">&nbsp;</a> 
```python
@property
loader(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L1969)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L1969?message=Update%20Docs)]
</div>
**LLM Docstring**

Lazily construct or return the module loader used for deserialization.
  - `:returns`: `object`
    > the configured or lazily created module loader


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.attr" class="docs-object-method">&nbsp;</a> 
```python
@property
attr(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L1985)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L1985?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the configured module attribute or the default `config` name.
  - `:returns`: `str`
    > the module attribute containing serialized data


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L2012)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L2012?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap module configuration data without structural conversion.
  - `data`: `object`
    > data to serialize, convert, or write
  - `:returns`: `object`
    > The converted representation described above.


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.deconvert" class="docs-object-method">&nbsp;</a> 
```python
deconvert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L2024)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L2024?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the loaded module attribute unchanged.
  - `data`: `object`
    > data to serialize, convert, or write
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.serialize" class="docs-object-method">&nbsp;</a> 
```python
serialize(self, file, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L2036)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L2036?message=Update%20Docs)]
</div>
**LLM Docstring**

JSON-encode data and emit a Python assignment to the configured module attribute.
  - `file`: `object`
    > path or file-like object
  - `data`: `object`
    > data to serialize, convert, or write
  - `kwargs`: `object`
    > keyword arguments forwarded to a callable
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.deserialize" class="docs-object-method">&nbsp;</a> 
```python
deserialize(self, file, key=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L2062)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/ModuleSerializer.py#L2062?message=Update%20Docs)]
</div>
**LLM Docstring**

Execute/load the module, retrieve the configured attribute, and optionally select a nested key.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/ModuleSerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/ModuleSerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/ModuleSerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/ModuleSerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L1939?message=Update%20Docs)   
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