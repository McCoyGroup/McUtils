## <a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh">SphereUnionSurfaceMesh</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L2325)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L2325?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L2326)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L2326?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.surface_area" class="docs-object-method">&nbsp;</a> 
```python
surface_area(self, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2340)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2340?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.volume" class="docs-object-method">&nbsp;</a> 
```python
volume(self, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2352)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2352?message=Update%20Docs)]
</div>
Exact volume of a closed mesh via the divergence theorem.
Assumes outward-pointing face normals and watertight mesh.


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.normal_derivatives" class="docs-object-method">&nbsp;</a> 
```python
normal_derivatives(self, order=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2364)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2364?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.area_derivatives" class="docs-object-method">&nbsp;</a> 
```python
area_derivatives(self, order=1, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2380)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2380?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.centroid_derivatives" class="docs-object-method">&nbsp;</a> 
```python
centroid_derivatives(self, order=1, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2426)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2426?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.volume_derivatives" class="docs-object-method">&nbsp;</a> 
```python
volume_derivatives(self, order=1, return_components=False, normal_order=None, area_order=None, centroid_order=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2444)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2444?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.normals" class="docs-object-method">&nbsp;</a> 
```python
@property
normals(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2470)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2470?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.signed_volumes" class="docs-object-method">&nbsp;</a> 
```python
@property
signed_volumes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2475)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2475?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.get_normals" class="docs-object-method">&nbsp;</a> 
```python
get_normals(self, normalize=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2480)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2480?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.from_submeshes" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_submeshes(cls, pts, submeshes, *, centers, radii, occlusion_type='complete', occlusion_tolerance=0.01, check_normals=True, deduplicate_points=False, duplicate_point_threshold=1e-14, vert_map=None, intersection_point_mask=None, occlusion_intersection_tolerance=0.05, stitch=True, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2485)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2485?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.stitch" class="docs-object-method">&nbsp;</a> 
```python
stitch(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2611)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2611?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.from_subclouds" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_subclouds(cls, point_clouds, *, centers, radii, mesh_type='convex', occlusion_type='partial', vert_map=None, deduplicate_points=False, mesh_kwargs=None, intersection_point_mask=None, **surface_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2629)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2629?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.from_o3d" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_o3d(cls, mesh, densities=None, surf=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2668)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2668?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, figure=None, *, function=None, vertex_values=None, normals=None, invert_mesh=False, distance_units='Angstroms', **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2677)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L2677?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.plot_triangle_mesh" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
plot_triangle_mesh(cls, verts, indices, figure=None, *, color='blue', transparency=0.8, backend='x3d', return_objects=False, line_color='black', line_transparency=0.9, line_style=None, vertex_colors=None, vertex_values=None, vertex_colormap='WarioColors', rescale_color_values=True, normals=None, centroids=None, normal_color='black', normal_radius=0.01, normal_scaling=0.5, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2712)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2712?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L2325?message=Update%20Docs)   
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