## <a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh">SphereUnionSurfaceMesh</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L3359)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L3359?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, verts, inds, surf=None, densities=None, tri_map=None, vert_map=None, normals=None, vertex_normals=None, centers=None, radii=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L3360)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L3360?message=Update%20Docs)]
</div>
**LLM Docstring**

Hold a triangle mesh (vertices and triangle indices) plus optional metadata for
a sphere-union surface.
  - `verts`: `np.ndarray`
    > the mesh vertices
  - `inds`: `np.ndarray`
    > the triangle vertex indices
  - `surf`: `SphereUnionSurface | None`
    > the source surface, if any
  - `densities`: `np.ndarray | None`
    > per-vertex reconstruction densities
  - `tri_map`: `np.ndarray | None`
    > per-triangle owning-sphere map
  - `vert_map`: `np.ndarray | None`
    > per-vertex owning-sphere map
  - `normals`: `np.ndarray | None`
    > per-triangle normals
  - `vertex_normals`: `np.ndarray | None`
    > per-vertex normals
  - `centers`: `np.ndarray | None`
    > the sphere centers
  - `radii`: `np.ndarray | None`
    > the sphere radii


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.surface_area" class="docs-object-method">&nbsp;</a> 
```python
surface_area(self, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3401)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3401?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the mesh surface area as the sum of its triangle areas (Heron's
formula).
  - `return_components`: `bool`
    > return the per-triangle areas rather than the sum
  - `:returns`: `float | np.ndarray`
    > the surface area (or per-triangle areas)


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.volume" class="docs-object-method">&nbsp;</a> 
```python
volume(self, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3424)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3424?message=Update%20Docs)]
</div>
Exact volume of a closed mesh via the divergence theorem.
Assumes outward-pointing face normals and watertight mesh.


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.normal_derivatives" class="docs-object-method">&nbsp;</a> 
```python
normal_derivatives(self, order=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3436)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3436?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the derivatives (up to `order`) of each triangle's normal with respect to
its vertex coordinates.
  - `order`: `int`
    > the derivative order
  - `:returns`: `list`
    > the per-order normal-derivative tensors


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.area_derivatives" class="docs-object-method">&nbsp;</a> 
```python
area_derivatives(self, order=1, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3476)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3476?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the derivatives (up to `order`) of each triangle's area with respect to
its vertex coordinates, via the Heron expansion of its edge lengths.
  - `order`: `int`
    > the derivative order
  - `return_components`: `bool`
    > return the per-triangle derivatives rather than their sum
  - `:returns`: `list`
    > the per-order area-derivative tensors


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.centroid_derivatives" class="docs-object-method">&nbsp;</a> 
```python
centroid_derivatives(self, order=1, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3535)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3535?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the derivatives (up to `order`) of each triangle's centroid with respect
to its vertex coordinates.
  - `order`: `int`
    > the derivative order
  - `return_components`: `bool`
    > accepted for interface parity
  - `:returns`: `list`
    > the per-order centroid-derivative tensors


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.volume_derivatives" class="docs-object-method">&nbsp;</a> 
```python
volume_derivatives(self, order=1, return_components=False, normal_order=None, area_order=None, centroid_order=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3566)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3566?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the derivatives (up to `order`) of the enclosed volume with respect to
the vertex coordinates, combining the area, centroid, and normal derivatives via
the divergence theorem.
  - `order`: `int`
    > the derivative order
  - `return_components`: `bool`
    > return the per-triangle derivatives rather than their sum
  - `normal_order`: `int | None`
    > override the order for the normal derivatives
  - `area_order`: `int | None`
    > override the order for the area derivatives
  - `centroid_order`: `int | None`
    > override the order for the centroid derivatives
  - `:returns`: `list`
    > the per-order volume-derivative tensors


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.normals" class="docs-object-method">&nbsp;</a> 
```python
@property
normals(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3612)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3612?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-triangle unit normals (computed lazily).
  - `:returns`: `np.ndarray`
    > the triangle normals


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.signed_volumes" class="docs-object-method">&nbsp;</a> 
```python
@property
signed_volumes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3625)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3625?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-triangle signed tetrahedron volumes (the cross-product norms used in the
divergence-theorem volume), computed lazily.
  - `:returns`: `np.ndarray`
    > the signed volumes


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.get_normals" class="docs-object-method">&nbsp;</a> 
```python
get_normals(self, normalize=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3639)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3639?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the per-triangle normals (and their norms) from the triangle edge cross
products.
  - `normalize`: `bool`
    > return unit normals
  - `:returns`: `tuple`
    > the `(normals, norms)`


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.from_submeshes" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_submeshes(cls, pts, submeshes, *, centers, radii, occlusion_type='complete', occlusion_tolerance=0.01, check_normals=True, deduplicate_points=False, duplicate_point_threshold=1e-14, vert_map=None, intersection_point_mask=None, occlusion_intersection_tolerance=0.05, stitch=True, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3655)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3655?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a mesh from a shared point set and per-sphere triangle sub-meshes,
optionally deduplicating coincident points and pruning triangles occluded inside
the sphere union (by vertex or centroid tests), fixing triangle orientations.
  - `pts`: `np.ndarray`
    > the shared vertex set
  - `submeshes`: `list`
    > the per-sphere triangle index arrays
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `occlusion_type`: `str | None`
    > how to prune occluded triangles (`None`/`'complete'`/`'partial'`/`'centroid'`)
  - `occlusion_tolerance`: `float`
    > the exterior-test tolerance
  - `check_normals`: `bool`
    > reorient triangle normals to point outward
  - `deduplicate_points`: `bool`
    > merge coincident points
  - `duplicate_point_threshold`: `float`
    > the coincidence distance threshold
  - `vert_map`: `np.ndarray | None`
    > per-vertex owning-sphere map
  - `intersection_point_mask`: `np.ndarray | None`
    > which points are intersection points
  - `occlusion_intersection_tolerance`: `float`
    > the looser tolerance for intersection points
  - `stitch`: `bool`
    > accepted for interface parity
  - `etc`: `Any`
    > extra options forwarded to the constructor
  - `:returns`: `SphereUnionSurfaceMesh`
    > the mesh


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.stitch" class="docs-object-method">&nbsp;</a> 
```python
stitch(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3820)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3820?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a topologically repaired copy of the mesh (seams stitched, holes capped)
via `MeshCleaner`.
  - `:returns`: `SphereUnionSurfaceMesh`
    > the cleaned mesh


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.from_subclouds" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_subclouds(cls, point_clouds, *, centers, radii, mesh_type='convex', occlusion_type='partial', vert_map=None, deduplicate_points=False, mesh_kwargs=None, intersection_point_mask=None, **surface_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3847)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3847?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a mesh by convex-hulling each per-sphere point cloud and unioning the
resulting sub-meshes (pruning occluded triangles).
  - `point_clouds`: `list`
    > the per-sphere point clouds
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `mesh_type`: `str | type`
    > the per-cloud hull type (`'convex'` or a hull class)
  - `occlusion_type`: `str`
    > how to prune occluded triangles
  - `vert_map`: `np.ndarray | None`
    > per-vertex owning-sphere map (built if omitted)
  - `deduplicate_points`: `bool`
    > merge coincident points
  - `mesh_kwargs`: `dict | None`
    > extra options for the hull construction
  - `intersection_point_mask`: `np.ndarray | None`
    > which points are intersection points
  - `surface_options`: `Any`
    > extra options forwarded to `from_submeshes`
  - `:returns`: `SphereUnionSurfaceMesh`
    > the mesh


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.from_o3d" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_o3d(cls, mesh, densities=None, surf=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3914)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3914?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a mesh from an Open3D triangle mesh.
  - `mesh`: `Any`
    > the Open3D mesh
  - `densities`: `np.ndarray | None`
    > per-vertex reconstruction densities
  - `surf`: `SphereUnionSurface | None`
    > the source surface
  - `:returns`: `SphereUnionSurfaceMesh`
    > the mesh


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, figure=None, *, function=None, vertex_values=None, normals=None, invert_mesh=False, distance_units='Angstroms', **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3936)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L3936?message=Update%20Docs)]
</div>
**LLM Docstring**

Plot the triangle mesh, optionally coloring vertices by a scalar function and
drawing normals.
  - `figure`: `Any`
    > an existing figure to draw into
  - `function`: `Callable | None`
    > a scalar function to color vertices by
  - `vertex_values`: `np.ndarray | None`
    > explicit per-vertex color values
  - `normals`: `Any`
    > per-triangle normals to draw (or `True` to use the mesh normals)
  - `invert_mesh`: `bool`
    > flip the triangle winding
  - `distance_units`: `str`
    > the display distance units
  - `etc`: `Any`
    > extra plotting options
  - `:returns`: `object`
    > the figure


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.plot_triangle_mesh" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
plot_triangle_mesh(cls, verts, indices, figure=None, *, color='blue', transparency=0.8, backend='x3d', return_objects=False, line_color='black', line_transparency=0.9, line_style=None, vertex_colors=None, vertex_values=None, vertex_colormap='WarioColors', rescale_color_values=True, normals=None, centroids=None, normal_color='black', normal_radius=0.01, normal_scaling=0.5, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3991)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3991?message=Update%20Docs)]
</div>
**LLM Docstring**

Plot a triangle mesh (faces, edges, and optional per-triangle normals) into a 3-D
figure.
  - `verts`: `np.ndarray`
    > the mesh vertices
  - `indices`: `np.ndarray`
    > the triangle vertex indices
  - `figure`: `Any`
    > an existing figure to draw into
  - `color`: `Any`
    > the face color
  - `transparency`: `float`
    > the face transparency
  - `backend`: `str`
    > the plotting backend
  - `return_objects`: `bool`
    > also return the created plot objects
  - `line_color`: `Any`
    > the edge color
  - `line_transparency`: `float`
    > the edge transparency
  - `line_style`: `dict | None`
    > extra edge styling
  - `vertex_colors`: `Any`
    > explicit per-vertex colors
  - `vertex_values`: `np.ndarray | None`
    > per-vertex scalar values to color by
  - `vertex_colormap`: `str`
    > the colormap for vertex values
  - `rescale_color_values`: `bool`
    > rescale the color values into the colormap range
  - `normals`: `np.ndarray | None`
    > per-triangle normals to draw
  - `centroids`: `np.ndarray | None`
    > triangle centroids for the normals (computed if omitted)
  - `normal_color`: `Any`
    > the normal-arrow color
  - `normal_radius`: `float`
    > the normal-arrow radius
  - `normal_scaling`: `float`
    > the normal-arrow length scaling
  - `etc`: `Any`
    > extra plotting options
  - `:returns`: `object | tuple`
    > the figure (and objects if requested)
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L3359?message=Update%20Docs)   
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