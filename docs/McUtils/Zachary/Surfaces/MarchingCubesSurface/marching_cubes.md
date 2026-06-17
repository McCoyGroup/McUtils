# <a id="McUtils.Zachary.Surfaces.MarchingCubesSurface.marching_cubes">marching_cubes</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/MarchingCubesSurface.py#L381)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/MarchingCubesSurface.py#L381?message=Update%20Docs)]
</div>

```python
marching_cubes(grid, isovalue, spacing=(1.0, 1.0, 1.0), origin=(0.0, 0.0, 0.0), transformation=None, return_surface=True, return_normals=True): 
```
Extract an isosurface from a scalar voxel grid.

Parameters
----------
grid : array_like, shape (nx, ny, nz)
Scalar field values. Axis order is (x, y, z).
isovalue : float
The scalar value of the isosurface to extract.
spacing : (sx, sy, sz)
Physical step size along each axis. Defaults to unit voxels.
origin : (ox, oy, oz)
World-space coordinate of grid point (0, 0, 0).

Returns
-------
vertices : ndarray, shape (N, 3)
Isosurface vertex positions in world space.
triangles : ndarray, shape (M, 3), dtype int
Vertex index triples; each row is one triangle.












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Surfaces/MarchingCubesSurface/marching_cubes.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Surfaces/MarchingCubesSurface/marching_cubes.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Surfaces/MarchingCubesSurface/marching_cubes.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Surfaces/MarchingCubesSurface/marching_cubes.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/MarchingCubesSurface.py#L381?message=Update%20Docs)   
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