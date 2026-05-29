## <a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh">SphereUnionSurfaceMesh</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L1456)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L1456?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, verts, inds, surf=None, densities=None, tri_map=None, vert_map=None, normals=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L1457)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L1457?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.surface_area" class="docs-object-method">&nbsp;</a> 
```python
surface_area(self, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1467)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1467?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.volume" class="docs-object-method">&nbsp;</a> 
```python
volume(self, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1479)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1479?message=Update%20Docs)]
</div>
Exact volume of a closed mesh via the divergence theorem.
Assumes outward-pointing face normals and watertight mesh.


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.normal_derivatives" class="docs-object-method">&nbsp;</a> 
```python
normal_derivatives(self, order=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1491)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1491?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.area_derivatives" class="docs-object-method">&nbsp;</a> 
```python
area_derivatives(self, order=1, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1507)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1507?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.centroid_derivatives" class="docs-object-method">&nbsp;</a> 
```python
centroid_derivatives(self, order=1, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1553)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1553?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.volume_derivatives" class="docs-object-method">&nbsp;</a> 
```python
volume_derivatives(self, order=1, return_components=False, normal_order=None, area_order=None, centroid_order=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1571)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1571?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.normals" class="docs-object-method">&nbsp;</a> 
```python
@property
normals(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1597)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1597?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.signed_volumes" class="docs-object-method">&nbsp;</a> 
```python
@property
signed_volumes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1602)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1602?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.get_normals" class="docs-object-method">&nbsp;</a> 
```python
get_normals(self, normalize=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1607)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1607?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.from_submeshes" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_submeshes(cls, pts, submeshes, *, centers, radii, occlusion_type='complete', occlusion_tolerance=1e-05, check_normals=True, vert_map=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1612)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1612?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.from_subclouds" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_subclouds(cls, point_clouds, *, centers, radii, mesh_type='convex', occlusion_type='partial', vert_map=None, **mesh_kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1694)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1694?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.from_o3d" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_o3d(cls, mesh, densities=None, surf=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1723)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1723?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, figure=None, *, function=None, vertex_values=None, normals=False, distance_units='Angstroms', **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1732)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurfaceMesh.py#L1732?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurfaceMesh.plot_triangle_mesh" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
plot_triangle_mesh(cls, verts, indices, figure=None, *, color='blue', transparency=0.8, backend='x3d', return_objects=False, line_color='black', line_transparency=0.9, line_style=None, vertex_colors=None, vertex_values=None, vertex_colormap='WarioColors', rescale_color_values=True, normals=None, centroids=None, normal_color='black', normal_radius=0.01, normal_scaling=0.5, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1762)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1762?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L1456?message=Update%20Docs)   
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