## <a id="McUtils.Symmetry.PointGroups.PointGroup">PointGroup</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups.py#L35)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups.py#L35?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Symmetry.PointGroups.PointGroup.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, character_table=None, elements=None, axes=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups.py#L38)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups.py#L38?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize lazy caches for the character table, symmetry elements, and embedding axes.
  - `character_table`: `object`
    > Optional precomputed character table. Defaults to `None`.
  - `elements`: `object`
    > Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
  - `axes`: `object`
    > Requested Cartesian embedding axes. Defaults to `None`.
  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.Symmetry.PointGroups.PointGroup.get_modification_kwargs" class="docs-object-method">&nbsp;</a> 
```python
get_modification_kwargs(self, character_table=<McUtils.Devutils.core.DefaultType instance>, elements=<McUtils.Devutils.core.DefaultType instance>, axes=<McUtils.Devutils.core.DefaultType instance>): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L58)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L58?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve modification sentinels into a complete constructor argument mapping.
  - `character_table`: `object`
    > Optional precomputed character table. Defaults to `dev.default`.
  - `elements`: `object`
    > Selected group elements or element indices; `None` requests the full set. Defaults to `dev.default`.
  - `axes`: `object`
    > Requested Cartesian embedding axes. Defaults to `dev.default`.
  - `:returns`: `dict`
    > Constructor keyword arguments for a modified point-group copy.


<a id="McUtils.Symmetry.PointGroups.PointGroup.modify" class="docs-object-method">&nbsp;</a> 
```python
modify(self, character_table=<McUtils.Devutils.core.DefaultType instance>, elements=<McUtils.Devutils.core.DefaultType instance>, axes=<McUtils.Devutils.core.DefaultType instance>): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L83)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L83?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a new point-group object with selected cached data or axes replaced.
  - `character_table`: `object`
    > Optional precomputed character table. Defaults to `dev.default`.
  - `elements`: `object`
    > Selected group elements or element indices; `None` requests the full set. Defaults to `dev.default`.
  - `axes`: `object`
    > Requested Cartesian embedding axes. Defaults to `dev.default`.
  - `:returns`: `PointGroup`
    > The modified point-group instance.


<a id="McUtils.Symmetry.PointGroups.PointGroup.get_name" class="docs-object-method">&nbsp;</a> 
```python
get_name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L108)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L108?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the conventional point-group name.
  - `:returns`: `str`
    > The point-group name.


<a id="McUtils.Symmetry.PointGroups.PointGroup.name" class="docs-object-method">&nbsp;</a> 
```python
@property
name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L119?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the conventional point-group name.
  - `:returns`: `str`
    > The point-group name.


<a id="McUtils.Symmetry.PointGroups.PointGroup.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L130?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a diagnostic string describing the symmetry element.
  - `:returns`: `str`
    > The representation string.


<a id="McUtils.Symmetry.PointGroups.PointGroup.from_name" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_name(cls, key, n=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L141)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L141?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse fixed and parametrized point-group names and construct the corresponding concrete group object.
  - `key`: `object`
    > Point-group family key or fixed group name.
  - `n`: `object`
    > Group order or problem size used to construct the requested representation. Defaults to `None`.
  - `etc`: `dict`
    > Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
  - `:returns`: `PointGroup`
    > The constructed point group.


<a id="McUtils.Symmetry.PointGroups.PointGroup.get_symmetry_element_primary_rotation" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_symmetry_element_primary_rotation(cls, elements: 'Iterable[SymmetryElement]'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L172)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L172?message=Update%20Docs)]
</div>
**LLM Docstring**

Select a highest-order proper rotation element and report how many elements share that order.
  - `elements`: `'Iterable[SymmetryElement]'`
    > Selected group elements or element indices; `None` requests the full set.
  - `:returns`: `tuple[RotationElement | None, int | None]`
    > The selected rotation and its multiplicity, or `(None, None)` when absent.


<a id="McUtils.Symmetry.PointGroups.PointGroup.from_symmetry_elements" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_symmetry_elements(cls, elements: list[McUtils.Symmetry.Elements.SymmetryElement], tol=0.01): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L191?message=Update%20Docs)]
</div>
**LLM Docstring**

Infer a low- or axial-symmetry point-group family from supplied symmetry elements; high-symmetry branches remain unimplemented.
  - `elements`: `list[SymmetryElement]`
    > Selected group elements or element indices; `None` requests the full set.
  - `tol`: `object`
    > Numerical tolerance used for geometric or equality tests. Defaults to `0.01`.
  - `:returns`: `PointGroup`
    > The inferred point group.


<a id="McUtils.Symmetry.PointGroups.PointGroup.get_symmetry_elements" class="docs-object-method">&nbsp;</a> 
```python
get_symmetry_elements(self, only_class_representatives=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L277)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L277?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert representative or full operation matrices into symmetry-element objects and embed them in requested axes.
  - `only_class_representatives`: `object`
    > Whether to return one operation per conjugacy class rather than every group operation. Defaults to `True`.
  - `:returns`: `tuple[SymmetryElement, ...] | list[SymmetryElement]`
    > The symmetry elements.


<a id="McUtils.Symmetry.PointGroups.PointGroup.character_table" class="docs-object-method">&nbsp;</a> 
```python
@property
character_table(self) -> McUtils.Symmetry.Characters.CharacterTable: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L316)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L316?message=Update%20Docs)]
</div>
**LLM Docstring**

Lazily construct and cache the group character table.
  - `:returns`: `CharacterTable`
    > The character table.


<a id="McUtils.Symmetry.PointGroups.PointGroup.elements" class="docs-object-method">&nbsp;</a> 
```python
@property
elements(self) -> 'tuple[SymmetryElement]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L330)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L330?message=Update%20Docs)]
</div>
**LLM Docstring**

Lazily construct and cache representative symmetry elements.
  - `:returns`: `tuple[SymmetryElement, ...]`
    > The symmetry elements.


<a id="McUtils.Symmetry.PointGroups.PointGroup.get_character_table" class="docs-object-method">&nbsp;</a> 
```python
get_character_table(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L344)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L344?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct the hard-coded or analytic character table for the `get` group family.
  - `:returns`: `np.ndarray`
    > The square character table with irreducible representations along rows.


<a id="McUtils.Symmetry.PointGroups.PointGroup.get_all_character_matrices" class="docs-object-method">&nbsp;</a> 
```python
get_all_character_matrices(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L356)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L356?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the three-dimensional Cartesian matrix representation for selected group elements.
  - `:returns`: `np.ndarray`
    > An array of shape `(n_elements, 3, 3)`.


<a id="McUtils.Symmetry.PointGroups.PointGroup.get_axes_from_symmetry_elements" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_axes_from_symmetry_elements(cls, elements): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L368)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L368?message=Update%20Docs)]
</div>
**LLM Docstring**

Choose primary and secondary molecular axes from rotations and reflection planes, then build an orthonormal view matrix.
  - `elements`: `object`
    > Selected group elements or element indices; `None` requests the full set.
  - `:returns`: `np.ndarray`
    > A `3 x 3` axis matrix.


<a id="McUtils.Symmetry.PointGroups.PointGroup.get_axes" class="docs-object-method">&nbsp;</a> 
```python
get_axes(self, elements=None, base_axes=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L428)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L428?message=Update%20Docs)]
</div>
**LLM Docstring**

Determine embedding axes from supplied, cached, or base representative elements.
  - `elements`: `object`
    > Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
  - `base_axes`: `object`
    > Value used as `base_axes` by the implementation. Defaults to `False`.
  - `:returns`: `np.ndarray`
    > A `3 x 3` axis matrix.


<a id="McUtils.Symmetry.PointGroups.PointGroup.axes" class="docs-object-method">&nbsp;</a> 
```python
@property
axes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L455)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L455?message=Update%20Docs)]
</div>
**LLM Docstring**

Lazily determine and cache the embedded or canonical point-group axes.
  - `:returns`: `np.ndarray`
    > A `3 x 3` axis matrix.


<a id="McUtils.Symmetry.PointGroups.PointGroup.base_axes" class="docs-object-method">&nbsp;</a> 
```python
@property
base_axes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L469)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L469?message=Update%20Docs)]
</div>
**LLM Docstring**

Lazily determine and cache the embedded or canonical point-group axes.
  - `:returns`: `np.ndarray`
    > A `3 x 3` axis matrix.


<a id="McUtils.Symmetry.PointGroups.PointGroup.align" class="docs-object-method">&nbsp;</a> 
```python
align(self, axes): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L483)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L483?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a copy aligned to explicitly supplied axes, transforming cached elements consistently.
  - `axes`: `object`
    > Requested Cartesian embedding axes.
  - `:returns`: `PointGroup`
    > The aligned point group.


<a id="McUtils.Symmetry.PointGroups.PointGroup.transform" class="docs-object-method">&nbsp;</a> 
```python
transform(self, tf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L499)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L499?message=Update%20Docs)]
</div>
**LLM Docstring**

Express the symmetry element in a transformed Cartesian basis.
  - `tf`: `object`
    > A `3 x 3` change-of-basis transformation.
  - `:returns`: `SymmetryElement`
    > A symmetry element with its defining axis transformed by `tf`.


<a id="McUtils.Symmetry.PointGroups.PointGroup.get_matrices" class="docs-object-method">&nbsp;</a> 
```python
get_matrices(self, only_class_representatives=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L515)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L515?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the three-dimensional Cartesian matrix representation for selected group elements.
  - `only_class_representatives`: `object`
    > Whether to return one operation per conjugacy class rather than every group operation. Defaults to `True`.
  - `:returns`: `np.ndarray`
    > An array of shape `(n_elements, 3, 3)`.


<a id="McUtils.Symmetry.PointGroups.PointGroup.axis_representation" class="docs-object-method">&nbsp;</a> 
```python
axis_representation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L535)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L535?message=Update%20Docs)]
</div>


<a id="McUtils.Symmetry.PointGroups.PointGroup.coordinate_representation" class="docs-object-method">&nbsp;</a> 
```python
coordinate_representation(self, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L537)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L537?message=Update%20Docs)]
</div>


<a id="McUtils.Symmetry.PointGroups.PointGroup.coordinate_mode_reduction" class="docs-object-method">&nbsp;</a> 
```python
coordinate_mode_reduction(self, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L539)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L539?message=Update%20Docs)]
</div>


<a id="McUtils.Symmetry.PointGroups.PointGroup.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, figure=None, elements=None, origin=None, inversion_styles=None, rotation_styles=None, reflection_styles=None, improper_rotation_styles=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/PointGroups/PointGroup.py#L542)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups/PointGroup.py#L542?message=Update%20Docs)]
</div>
**LLM Docstring**

Add graphical primitives representing this symmetry element to a figure.
  - `figure`: `object`
    > Plotting figure that receives generated graphics primitives. Defaults to `None`.
  - `elements`: `object`
    > Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
  - `origin`: `object`
    > Plot origin. Defaults to `None`.
  - `inversion_styles`: `object`
    > Style overrides for inversion elements. Defaults to `None`.
  - `rotation_styles`: `object`
    > Style overrides for rotation elements. Defaults to `None`.
  - `reflection_styles`: `object`
    > Style overrides for reflection elements. Defaults to `None`.
  - `improper_rotation_styles`: `object`
    > Style overrides for improper-rotation elements. Defaults to `None`.
  - `opts`: `dict`
    > Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
  - `:returns`: `object`
    > The plotted primitive or list of plotted primitives.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/PointGroups/PointGroup.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/PointGroups/PointGroup.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/PointGroups/PointGroup.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/PointGroups/PointGroup.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/PointGroups.py#L35?message=Update%20Docs)   
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