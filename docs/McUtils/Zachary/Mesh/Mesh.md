## <a id="McUtils.Zachary.Mesh.Mesh">Mesh</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh.py#L22)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh.py#L22?message=Update%20Docs)]
</div>

A general Mesh class representing data points in n-dimensions
in either a structured, unstructured, or semi-structured manner.
Exists mostly to provides a unified interface to difference FD and Surface methods.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
MeshError: MeshError
MeshType: MeshType
```
<a id="McUtils.Zachary.Mesh.Mesh.__new__" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
__new__(cls, data, mesh_type=None, allow_indeterminate=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L35)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L35?message=Update%20Docs)]
</div>

  - `griddata`: `np.ndarray`
    > the raw grid-point data the mesh uses
  - `mesh_type`: `None | str`
    > the type of mesh we have
  - `opts`: `Any`
    >


<a id="McUtils.Zachary.Mesh.Mesh.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh.py#L63)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh.py#L63?message=Update%20Docs)]
</div>
**LLM Docstring**

No-op initializer; the real setup happens in `__new__` (as required for an
`np.ndarray` subclass).
  - `args`: `Any`
    > ignored
  - `kwargs`: `Any`
    > ignored


<a id="McUtils.Zachary.Mesh.Mesh.__array_finalize__" class="docs-object-method">&nbsp;</a> 
```python
__array_finalize__(self, mesh): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L76)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L76?message=Update%20Docs)]
</div>
**LLM Docstring**

NumPy subclass hook: propagate (or infer) the mesh type and the
`allow_indeterminate` flag onto a newly created view/copy, validating that an
indeterminate mesh is only allowed when explicitly permitted.
  - `mesh`: `Any`
    > the source array being finalized from


<a id="McUtils.Zachary.Mesh.Mesh.mesh_spacings" class="docs-object-method">&nbsp;</a> 
```python
@property
mesh_spacings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L102?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-axis grid spacings (computed and cached lazily).
  - `:returns`: `np.ndarray | list`
    > the mesh spacings


<a id="McUtils.Zachary.Mesh.Mesh.subgrids" class="docs-object-method">&nbsp;</a> 
```python
@property
subgrids(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L115?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-axis subgrids for a regular or structured mesh (or `None` for
unstructured meshes).
  - `:returns`: `list | None`
    > the subgrids, or `None`


<a id="McUtils.Zachary.Mesh.Mesh.bounding_box" class="docs-object-method">&nbsp;</a> 
```python
@property
bounding_box(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L134)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L134?message=Update%20Docs)]
</div>
**LLM Docstring**

The `(min, max)` extent of the mesh along each coordinate.
  - `:returns`: `list[tuple]`
    > the per-coordinate bounds


<a id="McUtils.Zachary.Mesh.Mesh.dimension" class="docs-object-method">&nbsp;</a> 
```python
@property
dimension(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L146)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L146?message=Update%20Docs)]
</div>
Returns the dimension of the grid (not necessarily ndim)
  - `:returns`: `int`
    >


<a id="McUtils.Zachary.Mesh.Mesh.npoints" class="docs-object-method">&nbsp;</a> 
```python
@property
npoints(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L154?message=Update%20Docs)]
</div>
Returns the number of gridpoints in the mesh
  - `:returns`: `int`
    >


<a id="McUtils.Zachary.Mesh.Mesh.gridpoints" class="docs-object-method">&nbsp;</a> 
```python
@property
gridpoints(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L163)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L163?message=Update%20Docs)]
</div>
Returns the flattened set of gridpoints for a structured tensor grid and otherwise just returns the gridpoints
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.Mesh.Mesh.get_npoints" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_npoints(cls, g): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L172)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L172?message=Update%20Docs)]
</div>
Returns the number of gridpoints in the grid
  - `g`: `np.ndarray`
    > 
  - `:returns`: `int`
    >


<a id="McUtils.Zachary.Mesh.Mesh.get_gridpoints" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_gridpoints(cls, g): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L182)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L182?message=Update%20Docs)]
</div>
Returns the gridpoints in the grid
  - `g`: `np.ndarray`
    > 
  - `:returns`: `int`
    >


<a id="McUtils.Zachary.Mesh.Mesh.get_mesh_subgrids" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_mesh_subgrids(cls, grid, tol=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L195)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L195?message=Update%20Docs)]
</div>
Returns the subgrids for a mesh
  - `grid`: `Any`
    > 
  - `tol`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.Mesh.Mesh.get_mesh_spacings" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_mesh_spacings(cls, grid, tol=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L233)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L233?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the per-axis spacings of a grid as the unique rounded successive
differences of each subgrid (or `None` if there are no subgrids).
  - `grid`: `np.ndarray`
    > the grid
  - `tol`: `int | None`
    > the rounding tolerance (decimal places)
  - `:returns`: `np.ndarray | list | None`
    > the per-axis spacings


<a id="McUtils.Zachary.Mesh.Mesh.get_mesh_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_mesh_type(cls, grid, check_product_grid=True, check_regular_grid=True, tol=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L277)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L277?message=Update%20Docs)]
</div>
Determines what kind of grid we're working with
  - `grid`: `np.ndarray`
    > 
  - `:returns`: `MeshType`
    > mesh_type


<a id="McUtils.Zachary.Mesh.Mesh.RegularMesh" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
RegularMesh(cls, *mesh_specs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L372)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L372?message=Update%20Docs)]
</div>
Builds a grid from multiple linspace arguments,
basically insuring it's structured (if non-Empty)
  - `mesh_specs`: `Any`
    > 
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Mesh/Mesh.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Mesh/Mesh.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Mesh/Mesh.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Mesh/Mesh.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh.py#L22?message=Update%20Docs)   
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