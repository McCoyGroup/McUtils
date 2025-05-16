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


<a id="McUtils.Zachary.Mesh.Mesh.__array_finalize__" class="docs-object-method">&nbsp;</a> 
```python
__array_finalize__(self, mesh): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L67)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L67?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Mesh.Mesh.mesh_spacings" class="docs-object-method">&nbsp;</a> 
```python
@property
mesh_spacings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L83)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L83?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Mesh.Mesh.subgrids" class="docs-object-method">&nbsp;</a> 
```python
@property
subgrids(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L88)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L88?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Mesh.Mesh.bounding_box" class="docs-object-method">&nbsp;</a> 
```python
@property
bounding_box(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L98)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L98?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Mesh.Mesh.dimension" class="docs-object-method">&nbsp;</a> 
```python
@property
dimension(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L102?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L110?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Mesh/Mesh.py#L119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Mesh/Mesh.py#L119?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L128?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L138)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L138?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L151)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L151?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L179)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L179?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Mesh.Mesh.get_mesh_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_mesh_type(cls, grid, check_product_grid=True, check_regular_grid=True, tol=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L210)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L210?message=Update%20Docs)]
</div>
Determines what kind of grid we're working with
  - `grid`: `np.ndarray`
    > 
  - `:returns`: `MeshType`
    > m
e
s
h
_
t
y
p
e


<a id="McUtils.Zachary.Mesh.Mesh.RegularMesh" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
RegularMesh(cls, *mesh_specs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L305)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L305?message=Update%20Docs)]
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