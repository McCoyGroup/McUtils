## <a id="McUtils.Coordinerds.CoordinateSystems.CommonCoordinateSystems.ZMatrixCoordinateSystem">ZMatrixCoordinateSystem</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems.py#L164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems.py#L164?message=Update%20Docs)]
</div>

Represents ZMatrix coordinates generally







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
name: str
```
<a id="McUtils.Coordinerds.CoordinateSystems.CommonCoordinateSystems.ZMatrixCoordinateSystem.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, converter_options=None, dimension=(None, None), coordinate_shape=(None, 3), **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems.py#L169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems.py#L169?message=Update%20Docs)]
</div>

  - `converter_options`: `None | dict`
    > options to be passed through to a `CoordinateSystemConverter`
  - `coordinate_shape`: `Iterable[None | int]`
    > shape of a single coordinate in this coordiante system
  - `dimension`: `Iterable[None | int]`
    > the dimension of the coordinate system
  - `opts`: `Any`
    > other options, if `converter_options` is None, these are used as the `converter_options`


<a id="McUtils.Coordinerds.CoordinateSystems.CommonCoordinateSystems.ZMatrixCoordinateSystem.jacobian_prep_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
jacobian_prep_coordinates(coord, displacements, values, dihedral_cutoff=6): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L188?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CommonCoordinateSystems.ZMatrixCoordinateSystem.to_state" class="docs-object-method">&nbsp;</a> 
```python
to_state(self, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/ZMatrixCoordinateSystem.py#L225)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/ZMatrixCoordinateSystem.py#L225?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CommonCoordinateSystems.ZMatrixCoordinateSystem.canonicalize_order_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_order_list(self, ncoords, order_list): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L234)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L234?message=Update%20Docs)]
</div>
Normalizes the way the ZMatrix coordinates are built out
  - `ncoords`: `Any`
    > 
  - `order_list`: `iterable or None`
    > the basic ordering to apply for the
  - `:returns`: `iterator of int triples`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CommonCoordinateSystems.ZMatrixCoordinateSystem.tile_order_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
tile_order_list(self, ol, ncoords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L320)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L320?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/ZMatrixCoordinateSystem.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/ZMatrixCoordinateSystem.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/ZMatrixCoordinateSystem.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/ZMatrixCoordinateSystem.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems.py#L164?message=Update%20Docs)   
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