## <a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters">CoordinateSystemConverters</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L87)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L87?message=Update%20Docs)]
</div>

A coordinate converter class. It's a singleton so can't be instantiated.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
converters: OrderedDict
converter_graph: NoneType
converters_dir: str
converters_package: str
converter_type: CoordinateSystemConverter
```
<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L102?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters.get_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_coordinates(self, coordinate_set): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L105?message=Update%20Docs)]
</div>
Extracts coordinates from a coordinate_set


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters.load_converter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_converter(self, converter): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L119?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters.get_converter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_converter(cls, system1, system2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L159)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L159?message=Update%20Docs)]
</div>
Gets the appropriate converter for two CoordinateSystem objects
  - `system1`: `CoordinateSystem`
    > 
  - `system2`: `CoordinateSystem`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters.register_converter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
register_converter(cls, system1, system2, converter, check=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L228)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L228?message=Update%20Docs)]
</div>
Registers a converter between two coordinate systems
  - `system1`: `CoordinateSystem`
    > 
  - `system2`: `CoordinateSystem`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverters.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverters.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverters.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverters.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L87?message=Update%20Docs)   
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