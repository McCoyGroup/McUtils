## <a id="McUtils.Scaffolding.Serializers.NumPySerializer">NumPySerializer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers.py#L911)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers.py#L911?message=Update%20Docs)]
</div>

A serializer that implements NPZ dumps







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_extension: str
atomic_types: tuple
converter_dispatch: NoneType
dict_key_sep: str
```
<a id="McUtils.Scaffolding.Serializers.NumPySerializer.get_default_converters" class="docs-object-method">&nbsp;</a> 
```python
get_default_converters(): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NumPySerializer.py#L921)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NumPySerializer.py#L921?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NumPySerializer.get_converters" class="docs-object-method">&nbsp;</a> 
```python
get_converters(): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NumPySerializer.py#L931)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NumPySerializer.py#L931?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NumPySerializer.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NumPySerializer.py#L1006)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NumPySerializer.py#L1006?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NumPySerializer.deconvert" class="docs-object-method">&nbsp;</a> 
```python
deconvert(self, data, sep=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NumPySerializer.py#L1030)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NumPySerializer.py#L1030?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NumPySerializer.py#L1062)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NumPySerializer.py#L1062?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NumPySerializer.deserialize" class="docs-object-method">&nbsp;</a> 
```python
deserialize(self, file, key=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NumPySerializer.py#L1070)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NumPySerializer.py#L1070?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Scaffolding/Serializers/NumPySerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Scaffolding/Serializers/NumPySerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Scaffolding/Serializers/NumPySerializer.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/NumPySerializer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers.py#L911?message=Update%20Docs)   
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