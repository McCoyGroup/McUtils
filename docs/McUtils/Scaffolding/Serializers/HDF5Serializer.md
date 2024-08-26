## <a id="McUtils.Scaffolding.Serializers.HDF5Serializer">HDF5Serializer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers.py#L670)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers.py#L670?message=Update%20Docs)]
</div>

Defines a serializer that can prep/dump python data to HDF5.
To minimize complexity, we always use NumPy & Pseudopickle as an interface layer.
This restricts what we can serialize, but generally in insignificant ways.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_extension: str
```
<a id="McUtils.Scaffolding.Serializers.HDF5Serializer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, allow_pickle=True, psuedopickler=None, converters=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/HDF5Serializer.py#L677)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/HDF5Serializer.py#L677?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.HDF5Serializer.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/HDF5Serializer.py#L692)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/HDF5Serializer.py#L692?message=Update%20Docs)]
</div>
Converts data into format that can be serialized easily
  - `data`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Serializers.HDF5Serializer.serialize" class="docs-object-method">&nbsp;</a> 
```python
serialize(self, file, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/HDF5Serializer.py#L858)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/HDF5Serializer.py#L858?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.HDF5Serializer.deconvert" class="docs-object-method">&nbsp;</a> 
```python
deconvert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/HDF5Serializer.py#L871)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/HDF5Serializer.py#L871?message=Update%20Docs)]
</div>
Converts an HDF5 Dataset into a NumPy array or Group into a dict
  - `data`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Serializers.HDF5Serializer.deserialize" class="docs-object-method">&nbsp;</a> 
```python
deserialize(self, file, key=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/HDF5Serializer.py#L904)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/HDF5Serializer.py#L904?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Scaffolding/Serializers/HDF5Serializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Scaffolding/Serializers/HDF5Serializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Scaffolding/Serializers/HDF5Serializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/HDF5Serializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers.py#L670?message=Update%20Docs)   
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