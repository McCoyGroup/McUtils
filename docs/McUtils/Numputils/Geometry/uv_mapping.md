# <a id="McUtils.Numputils.Geometry.uv_mapping">uv_mapping</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Geometry.py#L5830)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Geometry.py#L5830?message=Update%20Docs)]
</div>

```python
uv_mapping(uv): 
```
Map points on [0,1]^2 onto the unit sphere S^2 via the cylindrical
equal-area (Lambert / "hat-box") projection:

z   = 2v - 1
phi = 2*pi*u
x,y = sqrt(1-z^2)*cos(phi), sqrt(1-z^2)*sin(phi)

By Archimedes' hat-box theorem, orthogonal projection of the sphere
onto its circumscribing cylinder is area-preserving, so this map is
the inverse of that projection: it sends the *uniform* measure on the
square to the *uniform* (surface-area) measure on the sphere. That
means a low-discrepancy sequence on the square pushes forward to a
low-discrepancy-ish sample on the sphere -- no low-discrepancy
structure is invented in 3D, but no uniformity is lost in translation
either, since z is uniform in [-1,1] and phi uniform in [0,2*pi)
are exactly the two conditions that characterize the uniform
distribution on S^2.

Parameters
----------
uv : (N,2) array, both columns in [0,1)

Returns
-------
(N,3) array of points on the unit sphere












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Geometry/uv_mapping.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Geometry/uv_mapping.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Geometry/uv_mapping.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Geometry/uv_mapping.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Geometry.py#L5830?message=Update%20Docs)   
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