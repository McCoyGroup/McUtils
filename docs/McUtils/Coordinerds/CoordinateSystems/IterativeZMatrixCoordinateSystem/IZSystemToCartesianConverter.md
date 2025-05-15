## <a id="McUtils.McUtils.Coordinerds.CoordinateSystems.IterativeZMatrixCoordinateSystem.IZSystemToCartesianConverter">IZSystemToCartesianConverter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem.py#L66)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem.py#L66?message=Update%20Docs)]
</div>

A converter class for going from Cartesian coordinates to internals coordinates







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.McUtils.Coordinerds.CoordinateSystems.IterativeZMatrixCoordinateSystem.IZSystemToCartesianConverter.types" class="docs-object-method">&nbsp;</a> 
```python
@property
types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IZSystemToCartesianConverter.py#L71)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IZSystemToCartesianConverter.py#L71?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.CoordinateSystems.IterativeZMatrixCoordinateSystem.IZSystemToCartesianConverter.convert_many" class="docs-object-method">&nbsp;</a> 
```python
convert_many(self, coords, *, reference_coordinates, order=0, masses=None, remove_translation_rotation=True, derivs=None, return_derivs=None, ordering=None, origins=None, axes=None, embedding_coords=None, jacobian_prep=None, axes_labels=None, fixed_atoms=None, use_rad=True, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IZSystemToCartesianConverter.py#L75)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IZSystemToCartesianConverter.py#L75?message=Update%20Docs)]
</div>
We'll implement this by having the ordering arg wrap around in coords?


<a id="McUtils.McUtils.Coordinerds.CoordinateSystems.IterativeZMatrixCoordinateSystem.IZSystemToCartesianConverter.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, coords, *, reference_coordinates, specs, order=0, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IZSystemToCartesianConverter.py#L157)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IZSystemToCartesianConverter.py#L157?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IZSystemToCartesianConverter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IZSystemToCartesianConverter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IZSystemToCartesianConverter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IZSystemToCartesianConverter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem.py#L66?message=Update%20Docs)   
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