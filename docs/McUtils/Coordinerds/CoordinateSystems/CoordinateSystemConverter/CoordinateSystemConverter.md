## <a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverter">CoordinateSystemConverter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L23)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L23?message=Update%20Docs)]
</div>

A base class for type converters







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
converters: weakref
```
<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverter.types" class="docs-object-method">&nbsp;</a> 
```python
@property
types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.py#L30)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.py#L30?message=Update%20Docs)]
</div>
The types property of a converter returns the types the converter converts


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverter.convert_many" class="docs-object-method">&nbsp;</a> 
```python
convert_many(self, coords_list, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.py#L38)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.py#L38?message=Update%20Docs)]
</div>
Converts many coordinates. Used in cases where a CoordinateSet has higher dimension
than its basis dimension. Should be overridden by a converted to provide efficient conversions
where necessary.
  - `coords_list`: `np.ndarray`
    > many sets of coords
  - `kwargs`: `Any`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverter.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, coords, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.py#L50)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.py#L50?message=Update%20Docs)]
</div>
The main necessary implementation method for a converter class.
Provides the actual function that converts the coords set
  - `coords`: `np.ndarray`
    > 
  - `kwargs`: `Any`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverter.register" class="docs-object-method">&nbsp;</a> 
```python
register(self, where=None, check=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.py#L62)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.py#L62?message=Update%20Docs)]
</div>
Registers the CoordinateSystemConverter
  - `:returns`: `_`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverter.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, coords, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.py#L76)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.py#L76?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L23?message=Update%20Docs)   
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