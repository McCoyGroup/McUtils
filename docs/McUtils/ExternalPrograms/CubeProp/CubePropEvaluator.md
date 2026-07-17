## <a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator">CubePropEvaluator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp.py#L11)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp.py#L11?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, origin, axes, steps, values, base_data=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp.py#L12)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp.py#L12?message=Update%20Docs)]
</div>
**LLM Docstring**

Hold a volumetric grid property (a cube file's values on a parallelepiped grid)
and set up lazy interpolation.
  - `origin`: `np.ndarray`
    > the grid origin
  - `axes`: `np.ndarray`
    > the three grid axis vectors (rows)
  - `steps`: `Sequence[int]`
    > the number of grid points along each axis
  - `values`: `np.ndarray`
    > the flat grid values (reshaped to `steps`)
  - `base_data`: `Any`
    > the full parsed cube data, if available
  - `opts`: `Any`
    > interpolation options


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.from_file" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_file(cls, file, **interpolation_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L41)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L41?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a `CubePropEvaluator` by parsing a cube file.
  - `file`: `str`
    > the cube file
  - `interpolation_opts`: `Any`
    > interpolation options
  - `:returns`: `CubePropEvaluator`
    > the evaluator


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.element_volume" class="docs-object-method">&nbsp;</a> 
```python
@property
element_volume(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L58)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L58?message=Update%20Docs)]
</div>
**LLM Docstring**

The volume of one grid cell (the absolute determinant of the axis vectors),
computed lazily.
  - `:returns`: `float`
    > the grid-cell volume


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.coords_from_grid" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
coords_from_grid(cls, origin, axes, steps): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L73)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L73?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the Cartesian coordinates of every grid point from the origin, axis
vectors, and step counts.
  - `origin`: `np.ndarray`
    > the grid origin
  - `axes`: `np.ndarray`
    > the three grid axis vectors
  - `steps`: `Sequence[int]`
    > the number of grid points along each axis
  - `:returns`: `np.ndarray`
    > the `(nx, ny, nz, 3)` coordinate array


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.grid_coords" class="docs-object-method">&nbsp;</a> 
```python
@property
grid_coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L103)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L103?message=Update%20Docs)]
</div>
**LLM Docstring**

The Cartesian coordinates of every grid point (computed lazily).
  - `:returns`: `np.ndarray`
    > the grid coordinates


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.get_value_interpolator" class="docs-object-method">&nbsp;</a> 
```python
get_value_interpolator(self, steps, values, **interpolation_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L117)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L117?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an interpolator over the grid values in (integer) grid-index space.
  - `steps`: `Sequence[int]`
    > the number of grid points along each axis
  - `values`: `np.ndarray`
    > the grid values
  - `interpolation_options`: `Any`
    > interpolation options
  - `:returns`: `Interpolator`
    > the interpolator


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.interpolator" class="docs-object-method">&nbsp;</a> 
```python
@property
interpolator(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L138)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L138?message=Update%20Docs)]
</div>
**LLM Docstring**

The value interpolator over the grid (built lazily).
  - `:returns`: `Interpolator`
    > the interpolator


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.inverse_axes" class="docs-object-method">&nbsp;</a> 
```python
@property
inverse_axes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L152?message=Update%20Docs)]
</div>
**LLM Docstring**

The inverse of the grid axis matrix (computed lazily), used to map Cartesian
points into grid-index space.
  - `:returns`: `np.ndarray`
    > the inverse axis matrix


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.embed_points" class="docs-object-method">&nbsp;</a> 
```python
embed_points(self, points): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L166)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L166?message=Update%20Docs)]
</div>
**LLM Docstring**

Map Cartesian points into (fractional) grid-index coordinates.
  - `points`: `np.ndarray`
    > the Cartesian points
  - `:returns`: `np.ndarray`
    > the grid-index coordinates


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.unembed_points" class="docs-object-method">&nbsp;</a> 
```python
unembed_points(self, points): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L180)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L180?message=Update%20Docs)]
</div>
**LLM Docstring**

Map (fractional) grid-index coordinates back into Cartesian space.
  - `points`: `np.ndarray`
    > the grid-index coordinates
  - `:returns`: `np.ndarray`
    > the Cartesian points


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.evaluate" class="docs-object-method">&nbsp;</a> 
```python
evaluate(self, points): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L193)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L193?message=Update%20Docs)]
</div>
**LLM Docstring**

Interpolate the grid property at arbitrary Cartesian points.
  - `points`: `np.ndarray`
    > the Cartesian points
  - `:returns`: `np.ndarray`
    > the interpolated values


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.get_isosurface" class="docs-object-method">&nbsp;</a> 
```python
get_isosurface(self, isoval, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L206)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L206?message=Update%20Docs)]
</div>
**LLM Docstring**

Extract an isosurface at the given value via marching cubes, transformed back
into Cartesian coordinates.
  - `isoval`: `float`
    > the isosurface value
  - `opts`: `Any`
    > extra marching-cubes options
  - `:returns`: `object`
    > the isosurface mesh
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp.py#L11?message=Update%20Docs)   
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