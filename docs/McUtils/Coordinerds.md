# <a id="McUtils.Coordinerds">McUtils.Coordinerds</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Coordinerds/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Coordinerds/__init__.py#L1?message=Update%20Docs)]
</div>
    
The Coordinerds package implements stuff for dealing with coordinates and generalized coordinate systems

It provides a semi-symbolic way to represent a CoordinateSystem and a CoordinateSet that provides coordinates within a
coordinate system. An extensible system for converting between coordinate systems and is provided.

The basic design of the package is set up so that one creates a `CoordinateSet` object, which in turn tracks its `CoordinateSystem`.
A `CoordinateSet` is a subclass of `np.ndarray`, and so any operation that works for a `np.ndarray` will work in turn for `CoordinateSet`.
This provides a large amount flexibility.

The `CoordinateSystem` object handles much of the heavy lifting for a `CoordinateSet`.
Conversions between different systems are implemented by a `CoordinateSystemConverter`.
Chained conversions are not _currently_ supported, but might well become supported in the future.

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[CoordinateSystemConverters](McUtils/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverters.md)   
</div>
   <div class="col" markdown="1">
[CoordinateSystemConverter](McUtils/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.md)   
</div>
   <div class="col" markdown="1">
[SimpleCoordinateSystemConverter](McUtils/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/SimpleCoordinateSystemConverter.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CartesianCoordinateSystem](McUtils/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/CartesianCoordinateSystem.md)   
</div>
   <div class="col" markdown="1">
[InternalCoordinateSystem](McUtils/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/InternalCoordinateSystem.md)   
</div>
   <div class="col" markdown="1">
[CartesianCoordinateSystem3D](McUtils/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/CartesianCoordinateSystem3D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CartesianCoordinates3D](McUtils/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/CartesianCoordinates3D.md)   
</div>
   <div class="col" markdown="1">
[CartesianCoordinates1D](McUtils/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/CartesianCoordinates1D.md)   
</div>
   <div class="col" markdown="1">
[CartesianCoordinates2D](McUtils/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/CartesianCoordinates2D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[SphericalCoordinateSystem](McUtils/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/SphericalCoordinateSystem.md)   
</div>
   <div class="col" markdown="1">
[SphericalCoordinates](McUtils/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/SphericalCoordinates.md)   
</div>
   <div class="col" markdown="1">
[ZMatrixCoordinateSystem](McUtils/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/ZMatrixCoordinateSystem.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ZMatrixCoordinates](McUtils/McUtils/Coordinerds/CoordinateSystems/CommonCoordinateSystems/ZMatrixCoordinates.md)   
</div>
   <div class="col" markdown="1">
[CoordinateSystem](McUtils/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.md)   
</div>
   <div class="col" markdown="1">
[BaseCoordinateSystem](McUtils/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/BaseCoordinateSystem.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CoordinateSystemError](McUtils/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystemError.md)   
</div>
   <div class="col" markdown="1">
[CompositeCoordinateSystem](McUtils/McUtils/Coordinerds/CoordinateSystems/CompositeCoordinateSystems/CompositeCoordinateSystem.md)   
</div>
   <div class="col" markdown="1">
[CompositeCoordinateSystemConverter](McUtils/McUtils/Coordinerds/CoordinateSystems/CompositeCoordinateSystems/CompositeCoordinateSystemConverter.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[GenericInternalCoordinateSystem](McUtils/McUtils/Coordinerds/CoordinateSystems/GenericInternalCoordinateSystem/GenericInternalCoordinateSystem.md)   
</div>
   <div class="col" markdown="1">
[ZMatrixCoordinates](McUtils/McUtils/Coordinerds/CoordinateSystems/GenericInternalCoordinateSystem/ZMatrixCoordinates.md)   
</div>
   <div class="col" markdown="1">
[CartesianToGICSystemConverter](McUtils/McUtils/Coordinerds/CoordinateSystems/GenericInternalCoordinateSystem/CartesianToGICSystemConverter.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[GICSystemToCartesianConverter](McUtils/McUtils/Coordinerds/CoordinateSystems/GenericInternalCoordinateSystem/GICSystemToCartesianConverter.md)   
</div>
   <div class="col" markdown="1">
[IterativeZMatrixCoordinateSystem](McUtils/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IterativeZMatrixCoordinateSystem.md)   
</div>
   <div class="col" markdown="1">
[IterativeZMatrixCoordinates](McUtils/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IterativeZMatrixCoordinates.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CartesianToIZSystemConverter](McUtils/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/CartesianToIZSystemConverter.md)   
</div>
   <div class="col" markdown="1">
[IZSystemToCartesianConverter](McUtils/McUtils/Coordinerds/CoordinateSystems/IterativeZMatrixCoordinateSystem/IZSystemToCartesianConverter.md)   
</div>
   <div class="col" markdown="1">
[CoordinateSet](McUtils/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[cartesian_to_zmatrix](McUtils/McUtils/Coordinerds/Conveniences/cartesian_to_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[zmatrix_to_cartesian](McUtils/McUtils/Coordinerds/Conveniences/zmatrix_to_cartesian.md)   
</div>
   <div class="col" markdown="1">
[canonicalize_internal](McUtils/McUtils/Coordinerds/Conveniences/canonicalize_internal.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[enumerate_zmatrices](McUtils/McUtils/Coordinerds/Conveniences/enumerate_zmatrices.md)   
</div>
   <div class="col" markdown="1">
[extract_zmatrix_internals](McUtils/McUtils/Coordinerds/Conveniences/extract_zmatrix_internals.md)   
</div>
   <div class="col" markdown="1">
[parse_zmatrix_string](McUtils/McUtils/Coordinerds/Conveniences/parse_zmatrix_string.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[validate_zmatrix](McUtils/McUtils/Coordinerds/Conveniences/validate_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[chain_zmatrix](McUtils/McUtils/Coordinerds/Conveniences/chain_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[attached_zmatrix_fragment](McUtils/McUtils/Coordinerds/Conveniences/attached_zmatrix_fragment.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[functionalized_zmatrix](McUtils/McUtils/Coordinerds/Conveniences/functionalized_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[reindex_zmatrix](McUtils/McUtils/Coordinerds/Conveniences/reindex_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[PrimitiveCoordinatePicker](McUtils/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[RedundantCoordinateGenerator](McUtils/McUtils/Coordinerds/Redundant/RedundantCoordinateGenerator.md)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Coordinerds/__init__.py#L1?message=Update%20Docs)   
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