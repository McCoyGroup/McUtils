## <a id="McUtils.Scaffolding.Serializers.NDarrayMarshaller">NDarrayMarshaller</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L881)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L881?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L888)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L888?message=Update%20Docs)]
</div>
**LLM Docstring**

Configure recursive conversion to NumPy-compatible trees, pseudo-pickle fallback, record handling, and custom dispatch.
  - `base_serializer`: `object`
    > parent serializer used during deconversion
  - `allow_pickle`: `object`
    > whether unsupported values may fall back to pickle
  - `psuedopickler`: `object`
    > pseudo-pickler used for arbitrary objects
  - `allow_records`: `object`
    > whether homogeneous object sequences may become NumPy record arrays
  - `all_dicts`: `object`
    > whether heterogeneous sequences are encoded as dictionaries
  - `converters`: `object`
    > custom ordered conversion dispatch
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Serializers.NDarrayMarshaller.get_default_converters" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_default_converters(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L930)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L930?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the ordered type/duck-type dispatch table used to coerce values into NumPy-compatible forms.
  - `:returns`: `collections.OrderedDict`
    > an ordered converter-dispatch mapping


<a id="McUtils.Scaffolding.Serializers.NDarrayMarshaller.converter_dispatch" class="docs-object-method">&nbsp;</a> 
```python
@property
converter_dispatch(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NDarrayMarshaller.py#L950)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NDarrayMarshaller.py#L950?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the custom converter mapping or create the default ordered dispatch table.
  - `:returns`: `collections.OrderedDict`
    > the active ordered converter-dispatch mapping


<a id="McUtils.Scaffolding.Serializers.NDarrayMarshaller.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, data, allow_pickle=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NDarrayMarshaller.py#L1208)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NDarrayMarshaller.py#L1208?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NDarrayMarshaller.py#L1264)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NDarrayMarshaller.py#L1264?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NDarrayMarshaller.py#L1314)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NDarrayMarshaller.py#L1314?message=Update%20Docs)]
</div>
**LLM Docstring**

Invoke recursive conversion, using the marshaller default pickle policy unless overridden.
  - `data`: `object`
    > data to serialize, convert, or write
  - `allow_pickle`: `object`
    > whether unsupported values may fall back to pickle
  - `:returns`: `object`
    > the NumPy-compatible converted representation
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/NDarrayMarshaller.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/NDarrayMarshaller.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/NDarrayMarshaller.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/NDarrayMarshaller.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L881?message=Update%20Docs)   
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