## <a id="McUtils.Scaffolding.Serializers.NDarrayMarshaller">NDarrayMarshaller</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers.py#L400)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers.py#L400?message=Update%20Docs)]
</div>

Support class for `HDF5Serializer` and other
NumPy-friendly interfaces that marshalls data
to/from NumPy arrays







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
atomic_types: tuple
```
<a id="McUtils.Scaffolding.Serializers.NDarrayMarshaller.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, base_serializer=None, allow_pickle=True, psuedopickler=None, allow_records=False, all_dicts=False, converters=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NDarrayMarshaller.py#L407)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NDarrayMarshaller.py#L407?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NDarrayMarshaller.get_default_converters" class="docs-object-method">&nbsp;</a> 
```python
get_default_converters(): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NDarrayMarshaller.py#L429)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NDarrayMarshaller.py#L429?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NDarrayMarshaller.converter_dispatch" class="docs-object-method">&nbsp;</a> 
```python
@property
converter_dispatch(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NDarrayMarshaller.py#L441)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NDarrayMarshaller.py#L441?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NDarrayMarshaller.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, data, allow_pickle=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NDarrayMarshaller.py#L567)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NDarrayMarshaller.py#L567?message=Update%20Docs)]
</div>
Recursively loop through, test data, make sure HDF5 compatible
  - `data`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Serializers.NDarrayMarshaller.deconvert" class="docs-object-method">&nbsp;</a> 
```python
deconvert(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NDarrayMarshaller.py#L611)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NDarrayMarshaller.py#L611?message=Update%20Docs)]
</div>
Reverses the conversion process
used to marshall the data
  - `data`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Serializers.NDarrayMarshaller.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, data, allow_pickle=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Serializers/NDarrayMarshaller.py#L661)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers/NDarrayMarshaller.py#L661?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Scaffolding/Serializers/NDarrayMarshaller.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Scaffolding/Serializers/NDarrayMarshaller.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Scaffolding/Serializers/NDarrayMarshaller.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/NDarrayMarshaller.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Serializers.py#L400?message=Update%20Docs)   
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