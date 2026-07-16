## <a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface">SphereUnionSurface</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L53)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L53?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_samples: int
default_scaling: int
default_expansion: int
default_tolerance: float
default_point_generator: str
default_triangulation_method: str
IntersectionCircle: IntersectionCircle
```
<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, centers, radii, scaling=None, expansion=None, samples=None, density=None, tolerance=None, add_intersection_circles=False, **generator_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L59)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L59?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.from_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_xyz(cls, atoms, positions, scaling=None, expansion=None, samples=None, tolerance=None, radius_property='IconRadius', distance_units='BohrRadius'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L85)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L85?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sampling_points" class="docs-object-method">&nbsp;</a> 
```python
@property
sampling_points(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L102?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.atom_sampling_points" class="docs-object-method">&nbsp;</a> 
```python
@property
atom_sampling_points(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L112)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L112?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.nearest_centers" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
nearest_centers(cls, pts, centers, return_normals=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L119?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_project" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_project(cls, pts, centers, radii): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L130?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_boundary_pruning" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_boundary_pruning(cls, pts, centers, min_component=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L142)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L142?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.point_cloud_repulsion" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
point_cloud_repulsion(cls, pts, centers, radii, min_displacement_cutoff=0.001, stochastic_factor=0.0001, force_constant=0.001, power=-3, max_iterations=15): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L183?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.adjust_point_cloud_density" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
adjust_point_cloud_density(self, pts, centers=None, radii=None, min_component=None, min_component_bins=30, min_component_scaling=0.7, same_point_cutoff=1e-06, max_iterations=15): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L224)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L224?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_exterior_points" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_exterior_points(cls, points, centers, radii, tolerance: float = 0, vertex_map=None, intersection_point_mask=None, intersection_point_tolerance=None, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L377)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L377?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_interior_points" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_interior_points(cls, points, centers, radii, tolerance: float = 0, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L407)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L407?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_surface_points" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_surface_points(cls, centers, radii, samples=50, density=None, scaling=1, point_generator=None, expansion=0, preserve_origins=False, circle_samples=None, min_circle_samples=0.1, add_intersection_circles=False, intersection_radius_scaling=1, intersection_boundary_clipping_threshold=None, return_intersection_point_mask=False, extend_intersection_points=True, intersection_point_tolerance=None, clear_circle_neighbors=None, neighborhood_tolerance='auto', tolerance=0, prune=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L424)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L424?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.generate_points" class="docs-object-method">&nbsp;</a> 
```python
generate_points(self, scaling=None, expansion=None, samples=None, density=None, preserve_origins=False, tolerance=None, prune=True, add_intersection_circles=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L697)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L697?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.generate_mesh" class="docs-object-method">&nbsp;</a> 
```python
generate_mesh(self, points=None, normals=None, scaling=None, expansion=None, samples=None, method='poisson', depth=5, **reconstruction_settings): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L725)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L725?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_points" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_points(cls, centers, radii, samples, generator=None, shells=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L763)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L763?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.fibonacci_sphere" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fibonacci_sphere(cls, samples): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L839)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L839?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_bbox" class="docs-object-method">&nbsp;</a> 
```python
get_bbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L851)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L851?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.signed_distance" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
signed_distance(cls, inside_mask, spacing=1.0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L857)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L857?message=Update%20Docs)]
</div>
Exact signed distance field from a binary mask.
Positive outside, negative inside, zero at the boundary.

inside_mask : bool ndarray, True where the object is
spacing     : float or tuple of floats, physical size of one voxel per axis


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.morphological_close_sdf" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
morphological_close_sdf(cls, inside_mask, probe_radius, spacing=1.0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L878)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L878?message=Update%20Docs)]
</div>
Fill concave crevices smaller than probe_radius via
SDF dilate -> redistance -> erode.

Returns
-------
F_final : float ndarray
Signed distance field whose zero level set is the closed surface.


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.solvent_surface_distance" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
solvent_surface_distance(cls, points, centers, radii, probe_radius=0, probe_type='sas', grid_spacing=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L907)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L907?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_surface_function" class="docs-object-method">&nbsp;</a> 
```python
get_surface_function(self, probe_radius=None, distance_function=None, probe_type='sas'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L938)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L938?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_triangulation" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation(self, occlusion_type='auto', deduplicate_points=None, point_gen_options=None, add_intersection_circles=True, extend_intersection_points=False, method=None, bbox_scaling=1.2, grid_samples=20, probe_radius=None, probe_type='sas', **surface_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L958)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L958?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sampling_point_surface_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sampling_point_surface_area(cls, centers, radii, points=None, exterior_test=None, point_generator=None, generator_args=None, center_surface_areas=None, **test_args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1027)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1027?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sampling_point_volume" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sampling_point_volume(cls, centers, radii, points=None, interior_test=None, point_generator=None, generator_args=None, center_volumes=None, shells=50, **test_args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1076)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1076?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.random_sphere_sampling" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
random_sphere_sampling(cls, center, radius, samples=500, seed=None, rng=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1108)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1108?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.volume_union_mc" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
volume_union_mc(cls, centers, radii, n_samples=100000, seed=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1119?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.volume_voxel" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
volume_voxel(cls, centers, radii, resolution=200): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1134)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1134?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_triple_intersection_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_triple_intersection_area(cls, a, b, c, r1, r2, r3): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1218)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1218?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_double_intersection_circle" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_double_intersection_circle(cls, centers, radii, dist=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1278)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1278?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_triple_intersection_point" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_triple_intersection_point(cls, centers, radii, dists=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1288)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1288?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_intersections" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_intersections(cls, centers, radii): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1320)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1320?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_double_intersection_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_double_intersection_area(cls, a, r1, r2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1354)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1354?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.triangle_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
triangle_area(cls, a, b, c): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1405)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1405?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_quadruple_intersection_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_quadruple_intersection_area(cls, a, b, c, f, g, h, r1, r2, r3, r4, A123, A124, A134, A234, I4, I3, I2, I1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1410)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1410?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_area(cls, radii, axis=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1608)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1608?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_union_surface_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_union_surface_area(cls, centers, radii, include_doubles=True, include_triples=None, include_quadruples=None, return_terms=False, overlap_tolerance=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1612)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1612?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.surface_area" class="docs-object-method">&nbsp;</a> 
```python
surface_area(self, method='union', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1763)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1763?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.volume" class="docs-object-method">&nbsp;</a> 
```python
volume(self, method='monte-carlo', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1787)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1787?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, figure=None, *, points=None, function=None, sphere_color='white', sphere_style=None, point_style=None, point_values=None, distance_units='Angstroms', plot_intersections=False, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1815)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1815?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.plot_sphere_points" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
plot_sphere_points(cls, points, centers, radii, figure=None, *, color='black', backend='x3d', return_objects=False, sphere_color='white', sphere_style=None, point_colors=None, point_values=None, vertex_colormap='WarioColors', rescale_color_values=True, plot_intersections=False, intersection_point_style=None, intersection_circle_style=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1853)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1853?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L53?message=Update%20Docs)   
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