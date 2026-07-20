## <a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface">SphereUnionSurface</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L94)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L94?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L100)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L100?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a surface defined by the union of spheres (e.g. atomic van-der-Waals
spheres), deferring sample-point generation.
  - `centers`: `np.ndarray`
    > the sphere centers, shape `(n, 3)`
  - `radii`: `np.ndarray`
    > the sphere radii, shape `(n,)`
  - `scaling`: `float | None`
    > a multiplicative radius scaling
  - `expansion`: `float | None`
    > an additive radius expansion
  - `samples`: `int | None`
    > the number of sample points per sphere
  - `density`: `float | None`
    > sample points per unit area (overrides `samples`)
  - `tolerance`: `float | None`
    > the occlusion tolerance for exterior-point tests
  - `add_intersection_circles`: `bool`
    > seed extra points along sphere-sphere intersection circles
  - `generator_options`: `Any`
    > extra options for the point generator


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.from_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_xyz(cls, atoms, positions, scaling=None, expansion=None, samples=None, tolerance=None, radius_property='IconRadius', distance_units='BohrRadius'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L150)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L150?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a `SphereUnionSurface` from atoms and positions, taking each sphere radius
from an atomic radius property.
  - `atoms`: `Sequence[str]`
    > the atom labels
  - `positions`: `np.ndarray`
    > the atomic positions
  - `scaling`: `float | None`
    > a multiplicative radius scaling
  - `expansion`: `float | None`
    > an additive radius expansion
  - `samples`: `int | None`
    > the number of sample points per sphere
  - `tolerance`: `float | None`
    > the occlusion tolerance
  - `radius_property`: `str`
    > the `AtomData` property to use for the radii
  - `distance_units`: `str`
    > the units to convert the radii into
  - `:returns`: `SphereUnionSurface`
    > the surface


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sampling_points" class="docs-object-method">&nbsp;</a> 
```python
@property
sampling_points(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L192)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L192?message=Update%20Docs)]
</div>
**LLM Docstring**

The (flattened) exterior sample points on the sphere union, generated lazily.
Setting this overrides them.
  - `:returns`: `np.ndarray`
    > the sample points


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.atom_sampling_points" class="docs-object-method">&nbsp;</a> 
```python
@property
atom_sampling_points(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L220)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L220?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-sphere lists of exterior sample points, generated lazily.
  - `:returns`: `list`
    > the per-sphere sample points


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.nearest_centers" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
nearest_centers(cls, pts, centers, return_normals=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L235)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L235?message=Update%20Docs)]
</div>
**LLM Docstring**

For each point, find the index of the nearest sphere center, optionally also
returning the distance and outward unit vector.
  - `pts`: `np.ndarray`
    > the query points
  - `centers`: `np.ndarray`
    > the sphere centers
  - `return_normals`: `bool`
    > also return the `(distances, unit_vectors)`
  - `:returns`: `np.ndarray | tuple`
    > the nearest-center indices (and normals if requested)


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_project" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_project(cls, pts, centers, radii): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L261)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L261?message=Update%20Docs)]
</div>
**LLM Docstring**

Project each point radially onto the surface of its nearest sphere.
  - `pts`: `np.ndarray`
    > the points to project
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `:returns`: `np.ndarray`
    > the projected points


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_boundary_pruning" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_boundary_pruning(cls, pts, centers, min_component=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L287?message=Update%20Docs)]
</div>
**LLM Docstring**

Prune points that sit too close to a neighbouring sphere's point group,
inferring the spacing cutoff from the per-group nearest-neighbour distribution
when one isn't supplied.
  - `pts`: `np.ndarray`
    > the points
  - `centers`: `np.ndarray`
    > the sphere centers
  - `min_component`: `float | None`
    > the minimum-allowed inter-group spacing (inferred if omitted)
  - `:returns`: `np.ndarray`
    > the pruned points


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.point_cloud_repulsion" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
point_cloud_repulsion(cls, pts, centers, radii, min_displacement_cutoff=0.001, stochastic_factor=0.0001, force_constant=0.001, power=-3, max_iterations=15): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L344)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L344?message=Update%20Docs)]
</div>
**LLM Docstring**

Relax a point cloud on the sphere union by iterated inverse-power repulsion
projected onto the local tangent plane, reprojecting onto the spheres each step
(a simple electrostatic-style even-spreading).
  - `pts`: `np.ndarray`
    > the points
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `min_displacement_cutoff`: `float`
    > stop once all repulsive forces fall below this
  - `stochastic_factor`: `float`
    > magnitude of a random jitter added each step
  - `force_constant`: `float`
    > the repulsion strength
  - `power`: `float`
    > the repulsion distance power
  - `max_iterations`: `int`
    > the maximum number of relaxation steps
  - `:returns`: `np.ndarray`
    > the relaxed points


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.adjust_point_cloud_density" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
adjust_point_cloud_density(self, pts, centers=None, radii=None, min_component=None, min_component_bins=30, min_component_scaling=0.7, same_point_cutoff=1e-06, max_iterations=15): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L411)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L411?message=Update%20Docs)]
</div>
**LLM Docstring**

Even out a point cloud's density by iteratively merging pairs of points that are
closer than a spacing cutoff (re-projecting the merged point onto its nearest
sphere when centers/radii are given), inferring the cutoff from the
nearest-neighbour distribution.
  - `pts`: `np.ndarray`
    > the points
  - `centers`: `np.ndarray | None`
    > the sphere centers (optional; needed with `radii` to reproject)
  - `radii`: `np.ndarray | None`
    > the sphere radii
  - `min_component`: `float | None`
    > the merge distance cutoff (inferred if omitted)
  - `min_component_bins`: `int`
    > histogram bins used to infer the cutoff
  - `min_component_scaling`: `float`
    > scaling applied to the inferred cutoff
  - `same_point_cutoff`: `float`
    > distance below which points are treated as duplicates
  - `max_iterations`: `int`
    > the maximum number of merge iterations
  - `:returns`: `np.ndarray`
    > the adjusted points


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_exterior_points" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_exterior_points(cls, points, centers, radii, tolerance: float = 0, vertex_map=None, intersection_point_mask=None, intersection_point_tolerance=None, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L592)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L592?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a mask (or per-sphere components) of the points that lie outside (or on)
every sphere, i.e. on the exterior surface of the union, within a tolerance.
  - `points`: `np.ndarray`
    > the query points
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `tolerance`: `float`
    > the fractional distance tolerance
  - `vertex_map`: `np.ndarray | None`
    > sphere index(es) each point belongs to, forced exterior
  - `intersection_point_mask`: `np.ndarray | None`
    > points to test with a looser tolerance
  - `intersection_point_tolerance`: `float | None`
    > the looser tolerance for those points
  - `return_components`: `bool`
    > return the per-sphere boolean matrix
  - `:returns`: `np.ndarray`
    > the exterior mask (or per-sphere components)


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_interior_points" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_interior_points(cls, points, centers, radii, tolerance: float = 0, return_components=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L647)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L647?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a mask (or per-sphere components) of the points that lie inside (or on)
at least one sphere, within a tolerance.
  - `points`: `np.ndarray`
    > the query points
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `tolerance`: `float`
    > the fractional distance tolerance
  - `return_components`: `bool`
    > return the per-sphere boolean matrix
  - `:returns`: `np.ndarray`
    > the interior mask (or per-sphere components)


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_surface_points" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_surface_points(cls, centers, radii, samples=50, density=None, scaling=1, point_generator=None, expansion=0, preserve_origins=False, circle_samples=None, min_circle_samples=0.1, add_intersection_circles=False, intersection_radius_scaling=1, intersection_boundary_clipping_threshold=None, return_intersection_point_mask=False, extend_intersection_points=True, intersection_point_tolerance=None, clear_circle_neighbors=None, neighborhood_tolerance='auto', tolerance=0, prune=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L683)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L683?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate the exterior surface point cloud for a union of spheres: sample each
sphere, optionally add and clip points along the sphere-sphere intersection
circles, and prune occluded (interior) points.
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `samples`: `int`
    > the number of points per sphere
  - `density`: `float | None`
    > points per unit area (overrides `samples`)
  - `scaling`: `float`
    > a multiplicative radius scaling
  - `point_generator`: `str | Callable | None`
    > the per-sphere point generator
  - `expansion`: `float`
    > an additive radius expansion
  - `preserve_origins`: `bool`
    > return per-sphere point lists rather than one array
  - `circle_samples`: `int | None`
    > number of points per intersection circle
  - `min_circle_samples`: `float`
    > minimum intersection-circle sampling (fraction or count)
  - `add_intersection_circles`: `bool`
    > add points along the intersection circles
  - `intersection_radius_scaling`: `float`
    > scaling applied to the intersection-circle radius
  - `intersection_boundary_clipping_threshold`: `Any`
    > distance for snapping points onto circles
  - `return_intersection_point_mask`: `bool`
    > also return which points are intersection points
  - `extend_intersection_points`: `bool`
    > add fresh points around the intersection circles
  - `intersection_point_tolerance`: `float | None`
    > exterior-test tolerance for intersection points
  - `clear_circle_neighbors`: `bool | None`
    > drop base points near added circle points
  - `neighborhood_tolerance`: `Any`
    > the neighbour-clearing tolerance (or `'auto'`)
  - `tolerance`: `float`
    > the occlusion tolerance
  - `prune`: `bool`
    > drop occluded (interior) points
  - `:returns`: `np.ndarray | list | tuple`
    > the surface points (array or per-sphere lists), optionally with the mask


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.generate_points" class="docs-object-method">&nbsp;</a> 
```python
generate_points(self, scaling=None, expansion=None, samples=None, density=None, preserve_origins=False, tolerance=None, prune=True, add_intersection_circles=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1004)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1004?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate the exterior surface points for this surface, filling unset options
from the instance defaults.
  - `scaling`: `float | None`
    > a multiplicative radius scaling
  - `expansion`: `float | None`
    > an additive radius expansion
  - `samples`: `int | None`
    > the number of points per sphere
  - `density`: `float | None`
    > points per unit area
  - `preserve_origins`: `bool`
    > return per-sphere point lists
  - `tolerance`: `float | None`
    > the occlusion tolerance
  - `prune`: `bool`
    > drop occluded points
  - `add_intersection_circles`: `bool | None`
    > add intersection-circle points
  - `etc`: `Any`
    > extra options forwarded to `get_surface_points`
  - `:returns`: `np.ndarray | list`
    > the surface points


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.generate_mesh" class="docs-object-method">&nbsp;</a> 
```python
generate_mesh(self, points=None, normals=None, scaling=None, expansion=None, samples=None, method='poisson', depth=5, **reconstruction_settings): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1058)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1058?message=Update%20Docs)]
</div>
**LLM Docstring**

Reconstruct a triangle mesh from the surface point cloud (currently via Open3D
Poisson reconstruction), estimating per-point normals from the sphere centers
when none are given.
  - `points`: `np.ndarray | list | None`
    > the surface points (generated if omitted)
  - `normals`: `np.ndarray | None`
    > per-point normals (estimated if omitted)
  - `scaling`: `float | None`
    > a multiplicative radius scaling for point generation
  - `expansion`: `float | None`
    > an additive radius expansion for point generation
  - `samples`: `int | None`
    > the number of points per sphere
  - `method`: `str`
    > the reconstruction method (`'poisson'`)
  - `depth`: `int`
    > the Poisson reconstruction octree depth
  - `reconstruction_settings`: `Any`
    > extra options for the reconstruction
  - `:returns`: `SphereUnionSurfaceMesh`
    > the reconstructed mesh


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_points" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_points(cls, centers, radii, samples, generator=None, shells=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1122)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1122?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate points on each of a (possibly batched) set of spheres, supporting a
scalar, per-sphere, or per-sphere-per-batch sample count, and optional radial
shells.
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `samples`: `Any`
    > the sample count (scalar, per-sphere, or per-batch)
  - `generator`: `str | dict | Callable | None`
    > the point generator (name, dict spec, or callable)
  - `shells`: `int | np.ndarray | None`
    > number of radial shells (or explicit shell fractions)
  - `:returns`: `np.ndarray | list`
    > the sphere points (array or nested lists)


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.fibonacci_sphere" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fibonacci_sphere(cls, samples): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1217)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1217?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate `samples` roughly-even points on the unit sphere via the Fibonacci
(golden-angle) spiral.
  - `samples`: `int`
    > the number of points
  - `:returns`: `np.ndarray`
    > the unit-sphere points, shape `(samples, 3)`


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_bbox" class="docs-object-method">&nbsp;</a> 
```python
get_bbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1240)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1240?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the axis-aligned bounding box enclosing all of the spheres.
  - `:returns`: `np.ndarray`
    > the `[min_corner, max_corner]` bounding box


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.signed_distance" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
signed_distance(cls, inside_mask, spacing=1.0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1254)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1254?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1275)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1275?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1304?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the signed distance from each point to the sphere-union surface, either
as the plain solvent-accessible (SAS) van-der-Waals distance or, for the
solvent-excluded surface (SES), via a morphological close on a voxel grid.
  - `points`: `np.ndarray`
    > the query points
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `probe_radius`: `float`
    > the solvent probe radius
  - `probe_type`: `str`
    > `'sas'` or `'ses'`
  - `grid_spacing`: `Sequence[float] | None`
    > the voxel spacing (required for SES)
  - `:returns`: `np.ndarray`
    > the signed distances (shaped like the input grid)


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_surface_function" class="docs-object-method">&nbsp;</a> 
```python
get_surface_function(self, probe_radius=None, distance_function=None, probe_type='sas'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1358)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1358?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a callable mapping points to a scalar field whose zero level set is the
(SAS/SES) molecular surface, passed through a radial decay function.
  - `probe_radius`: `float | None`
    > the solvent probe radius
  - `distance_function`: `Callable | None`
    > the radial decay applied to the signed distance
  - `probe_type`: `str`
    > `'sas'` or `'ses'`
  - `:returns`: `Callable`
    > the scalar-field function


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_triangulation" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation(self, occlusion_type='auto', deduplicate_points=None, point_gen_options=None, add_intersection_circles=True, extend_intersection_points=False, method=None, bbox_scaling=1.2, grid_samples=20, probe_radius=None, probe_type='sas', bbox=None, **surface_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1409)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L1409?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a triangulated `SphereUnionSurfaceMesh` of the surface, either by hulling
and unioning the per-sphere point clouds or by marching cubes on the surface
scalar field.
  - `occlusion_type`: `str`
    > how to prune occluded triangles (`'auto'`/`'complete'`/`'partial'`/`'centroid'`)
  - `deduplicate_points`: `bool | None`
    > merge coincident points before meshing
  - `point_gen_options`: `dict | None`
    > options for the point generation
  - `add_intersection_circles`: `bool`
    > add intersection-circle points
  - `extend_intersection_points`: `bool`
    > add fresh intersection-circle points
  - `method`: `str | None`
    > `'hull-union'` or `'isosurface'`
  - `bbox_scaling`: `float`
    > bounding-box padding for the isosurface grid
  - `grid_samples`: `int | Sequence[int]`
    > grid resolution for the isosurface
  - `probe_radius`: `float | None`
    > the solvent probe radius (isosurface)
  - `probe_type`: `str`
    > `'sas'` or `'ses'` (isosurface)
  - `surface_opts`: `Any`
    > extra options forwarded to the mesh builder
  - `:returns`: `SphereUnionSurfaceMesh`
    > the triangulated mesh


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sampling_point_surface_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sampling_point_surface_area(cls, centers, radii, points=None, exterior_test=None, point_generator=None, generator_args=None, center_surface_areas=None, **test_args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1527)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1527?message=Update%20Docs)]
</div>
**LLM Docstring**

Estimate the exposed surface area of the sphere union by Monte-Carlo sampling:
the fraction of each sphere's sample points that are exterior times its area.
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `points`: `list | None`
    > precomputed per-sphere sample points (generated if omitted)
  - `exterior_test`: `Callable | None`
    > the exterior-point test (defaults to `get_exterior_points`)
  - `point_generator`: `Callable | None`
    > the per-sphere point generator
  - `generator_args`: `dict | None`
    > options for the point generator
  - `center_surface_areas`: `np.ndarray | None`
    > per-sphere areas (computed if omitted)
  - `test_args`: `Any`
    > extra arguments for the exterior test
  - `:returns`: `float`
    > the estimated surface area


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sampling_point_volume" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sampling_point_volume(cls, centers, radii, points=None, interior_test=None, point_generator=None, generator_args=None, center_volumes=None, shells=50, **test_args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1621)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1621?message=Update%20Docs)]
</div>
**LLM Docstring**

Estimate the union volume by Monte-Carlo sampling of interior shell points.
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `points`: `list | None`
    > precomputed per-sphere sample points (generated if omitted)
  - `interior_test`: `Callable | None`
    > the interior-point test
  - `point_generator`: `Callable | None`
    > the per-sphere point generator
  - `generator_args`: `dict | None`
    > options for the point generator
  - `center_volumes`: `np.ndarray | None`
    > per-sphere volumes (computed if omitted)
  - `shells`: `int`
    > number of radial shells to sample
  - `test_args`: `Any`
    > extra arguments for the interior test
  - `:returns`: `float`
    > the estimated volume


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.random_sphere_sampling" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
random_sphere_sampling(cls, center, radius, samples=500, seed=None, rng=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1678)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1678?message=Update%20Docs)]
</div>
**LLM Docstring**

Draw uniformly-distributed random points inside a sphere.
  - `center`: `np.ndarray`
    > the sphere center
  - `radius`: `float`
    > the sphere radius
  - `samples`: `int`
    > the number of points
  - `seed`: `int | None`
    > a random seed
  - `rng`: `Any`
    > an explicit random generator
  - `:returns`: `np.ndarray`
    > the sampled points


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.volume_union_mc" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
volume_union_mc(cls, centers, radii, n_samples=100000, seed=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1706)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1706?message=Update%20Docs)]
</div>
**LLM Docstring**

Estimate the union volume by Monte-Carlo sampling uniformly inside each sphere.
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `n_samples`: `int`
    > the number of samples per sphere
  - `seed`: `int | None`
    > a random seed
  - `:returns`: `float`
    > the estimated volume


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.volume_voxel" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
volume_voxel(cls, centers, radii, resolution=200): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1737)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1737?message=Update%20Docs)]
</div>
**LLM Docstring**

Estimate the union volume by voxelizing the bounding box and counting the voxels
inside any sphere.
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `resolution`: `int`
    > the number of voxels along each axis
  - `:returns`: `float`
    > the estimated volume


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_triple_intersection_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_triple_intersection_area(cls, a, b, c, r1, r2, r3): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1926)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1926?message=Update%20Docs)]
</div>
**LLM Docstring**

Analytic surface area of the triple overlap of three spheres, following Gibson &
Scheraga. Returns either a pair-index fallback (when the triple doesn't fully
intersect) or the analytic area.
  - `a`: `Any`
    > the distance between centers 2 and 3
  - `b`: `Any`
    > the distance between centers 1 and 3
  - `c`: `Any`
    > the distance between centers 1 and 2
  - `r1`: `Any`
    > the first radius
  - `r2`: `Any`
    > the second radius
  - `r3`: `Any`
    > the third radius
  - `:returns`: `tuple`
    > `(overlap_indices_or_None, area_or_None)`


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_double_intersection_circle" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_double_intersection_circle(cls, centers, radii, dist=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2002)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2002?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the circle where two spheres intersect (its center, unit normal, and
radius).
  - `centers`: `np.ndarray`
    > the two sphere centers
  - `radii`: `np.ndarray`
    > the two sphere radii
  - `dist`: `float | None`
    > the inter-center distance (computed if omitted)
  - `:returns`: `SphereUnionSurface.IntersectionCircle`
    > the intersection circle


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_triple_intersection_point" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_triple_intersection_point(cls, centers, radii, dists=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2027)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2027?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the two points where three (assumed mutually intersecting) spheres meet,
by building a local axis system and solving for the coordinates.
  - `centers`: `np.ndarray`
    > the three sphere centers
  - `radii`: `np.ndarray`
    > the three sphere radii
  - `dists`: `tuple | None`
    > the `(d_12, d_13)` inter-center distances
  - `:returns`: `list`
    > the two intersection points


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.get_intersections" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_intersections(cls, centers, radii): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2074)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2074?message=Update%20Docs)]
</div>
**LLM Docstring**

Find all pairwise intersection circles and all triple intersection points among
a set of spheres.
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `:returns`: `tuple`
    > `(intersection_points, intersection_disks)`


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_double_intersection_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_double_intersection_area(cls, a, r1, r2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2121)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2121?message=Update%20Docs)]
</div>
**LLM Docstring**

Analytic exposed surface-area contribution of the overlap of two spheres, or a
containment fallback when one sphere swallows the other.
  - `a`: `float`
    > the inter-center distance
  - `r1`: `float`
    > the first radius
  - `r2`: `float`
    > the second radius
  - `:returns`: `tuple`
    > `(overlap_indices_or_None, area)`


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.triangle_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
triangle_area(cls, a, b, c): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2230)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2230?message=Update%20Docs)]
</div>
**LLM Docstring**

Heron's-formula area of a triangle with the given side lengths.
  - `a`: `Any`
    > the first side
  - `b`: `Any`
    > the second side
  - `c`: `Any`
    > the third side
  - `:returns`: `float`
    > the area


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_quadruple_intersection_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_quadruple_intersection_area(cls, a, b, c, f, g, h, r1, r2, r3, r4, A123, A124, A134, A234, I4, I3, I2, I1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2246)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2246?message=Update%20Docs)]
</div>
**LLM Docstring**

Analytic surface-area contribution of the quadruple overlap of four spheres,
dispatching on a set of intersection-test bit patterns to the correct lower-order
fallback or the full analytic expression.
  - `a`: `Any`
    > the distance between centers 2 and 3
  - `b`: `Any`
    > the distance between centers 1 and 3
  - `c`: `Any`
    > the distance between centers 1 and 2
  - `f`: `Any`
    > the distance between centers 1 and 4
  - `g`: `Any`
    > the distance between centers 2 and 4
  - `h`: `Any`
    > the distance between centers 3 and 4
  - `r1`: `Any`
    > the first radius
  - `r2`: `Any`
    > the second radius
  - `r3`: `Any`
    > the third radius
  - `r4`: `Any`
    > the fourth radius
  - `A123`: `Any`
    > the 1-2-3 triple area
  - `A124`: `Any`
    > the 1-2-4 triple area
  - `A134`: `Any`
    > the 1-3-4 triple area
  - `A234`: `Any`
    > the 2-3-4 triple area
  - `I4`: `Any`
    > the pair of tests for center 4 vs the 1-2-3 intersection points
  - `I3`: `Any`
    > the pair of tests for center 3
  - `I2`: `Any`
    > the pair of tests for center 2
  - `I1`: `Any`
    > the pair of tests for center 1
  - `:returns`: `tuple`
    > `(overlap_indices_or_None, area_or_None)`


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_area(cls, radii, axis=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2473)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2473?message=Update%20Docs)]
</div>
**LLM Docstring**

The total surface area of one or more spheres, `4 pi sum(r^2)`.
  - `radii`: `np.ndarray`
    > the sphere radii
  - `axis`: `int | None`
    > the axis to sum over
  - `:returns`: `float | np.ndarray`
    > the surface area


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.sphere_union_surface_area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sphere_union_surface_area(cls, centers, radii, include_doubles=True, include_triples=None, include_quadruples=None, return_terms=False, overlap_tolerance=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2489)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2489?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the exact exposed surface area of a union of spheres via
inclusion-exclusion over the analytic single/double/triple/quadruple
intersection-area terms, dropping fully-occluded spheres as they are detected.
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `include_doubles`: `bool`
    > include the pairwise intersection terms
  - `include_triples`: `bool | None`
    > include the triple terms
  - `include_quadruples`: `bool | None`
    > include the quadruple terms
  - `return_terms`: `bool`
    > return the per-combination term dict rather than the sum
  - `overlap_tolerance`: `float`
    > fractional tolerance for treating spheres as overlapping
  - `:returns`: `float | dict`
    > the surface area (or the terms dict)


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.surface_area" class="docs-object-method">&nbsp;</a> 
```python
surface_area(self, method='union', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L2664)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L2664?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the surface area of the sphere union by the chosen method.
  - `method`: `str`
    > `'union'` (analytic), `'sampling'`, `'mesh'`, or `'pcmesh'`
  - `opts`: `Any`
    > method-specific options
  - `:returns`: `float`
    > the surface area


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.volume" class="docs-object-method">&nbsp;</a> 
```python
volume(self, method='monte-carlo', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L2700)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L2700?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the volume of the sphere union by the chosen method.
  - `method`: `str`
    > `'monte-carlo'`, `'sampling'`, `'voxel'`, `'mesh'`, or `'pcmesh'` (`'union'` not implemented)
  - `opts`: `Any`
    > method-specific options
  - `:returns`: `float`
    > the volume


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, figure=None, *, points=None, function=None, sphere_color='white', sphere_style=None, point_style=None, point_values=None, distance_units='Angstroms', plot_intersections=False, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L2741)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.py#L2741?message=Update%20Docs)]
</div>
**LLM Docstring**

Plot the surface: the sample points (colored by an optional scalar function),
the spheres, and optionally the intersection circles/points.
  - `figure`: `Any`
    > an existing figure to draw into
  - `points`: `np.ndarray | None`
    > the points to plot (defaults to the sampling points)
  - `function`: `Callable | None`
    > a scalar function to color the points by
  - `sphere_color`: `Any`
    > the sphere color
  - `sphere_style`: `dict | None`
    > extra sphere styling
  - `point_style`: `dict | None`
    > extra point styling
  - `point_values`: `np.ndarray | None`
    > explicit per-point color values
  - `distance_units`: `str`
    > the display distance units
  - `plot_intersections`: `bool`
    > also draw the intersection circles/points
  - `etc`: `Any`
    > extra plotting options
  - `:returns`: `object`
    > the figure


<a id="McUtils.Zachary.Surfaces.SphereUnionSurface.SphereUnionSurface.plot_sphere_points" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
plot_sphere_points(cls, points, centers, radii, figure=None, *, color='black', backend='x3d', return_objects=False, sphere_color='white', sphere_style=None, point_colors=None, point_values=None, vertex_colormap='WarioColors', rescale_color_values=True, plot_intersections=False, intersection_point_style=None, intersection_circle_style=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2805)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2805?message=Update%20Docs)]
</div>
**LLM Docstring**

Plot a set of points, spheres, and optional intersection geometry into a 3-D
figure.
  - `points`: `np.ndarray`
    > the points to plot
  - `centers`: `np.ndarray`
    > the sphere centers
  - `radii`: `np.ndarray`
    > the sphere radii
  - `figure`: `Any`
    > an existing figure to draw into
  - `color`: `Any`
    > the point color
  - `backend`: `str`
    > the plotting backend
  - `return_objects`: `bool`
    > also return the created plot objects
  - `sphere_color`: `Any`
    > the sphere color
  - `sphere_style`: `dict | None`
    > extra sphere styling
  - `point_colors`: `Any`
    > explicit per-point colors
  - `point_values`: `np.ndarray | None`
    > per-point scalar values to color by
  - `vertex_colormap`: `str`
    > the colormap for point values
  - `rescale_color_values`: `bool`
    > rescale the color values into the colormap range
  - `plot_intersections`: `bool`
    > draw the intersection circles/points
  - `intersection_point_style`: `dict | None`
    > styling for intersection points
  - `intersection_circle_style`: `dict | None`
    > styling for intersection circles
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Surfaces/SphereUnionSurface/SphereUnionSurface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/SphereUnionSurface.py#L94?message=Update%20Docs)   
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