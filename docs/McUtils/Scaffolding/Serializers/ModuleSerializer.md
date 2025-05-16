## <a id="McUtils.Scaffolding.Serializers.ModuleSerializer">ModuleSerializer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers.py#L1089)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers.py#L1089?message=Update%20Docs)]
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
default_loader: NoneType
default_attr: str
```
<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, attr=None, loader=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/ModuleSerializer.py#L1101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/ModuleSerializer.py#L1101?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.loader" class="docs-object-method">&nbsp;</a> 
```python
@property
loader(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/ModuleSerializer.py#L1105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/ModuleSerializer.py#L1105?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.attr" class="docs-object-method">&nbsp;</a> 
```python
@property
attr(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/ModuleSerializer.py#L1113)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/ModuleSerializer.py#L1113?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/ModuleSerializer.py#L1124)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/ModuleSerializer.py#L1124?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.deconvert" class="docs-object-method">&nbsp;</a> 
```python
deconvert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/ModuleSerializer.py#L1126)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/ModuleSerializer.py#L1126?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.serialize" class="docs-object-method">&nbsp;</a> 
```python
serialize(self, file, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/ModuleSerializer.py#L1128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/ModuleSerializer.py#L1128?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.ModuleSerializer.deserialize" class="docs-object-method">&nbsp;</a> 
```python
deserialize(self, file, key=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/ModuleSerializer.py#L1140)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/ModuleSerializer.py#L1140?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/ModuleSerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/ModuleSerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/ModuleSerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/ModuleSerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers.py#L1089?message=Update%20Docs)   
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