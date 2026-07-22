## <a id="McUtils.Symmetry.Characters.CharacterTable">CharacterTable</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters.py#L2856)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters.py#L2856?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Symmetry.Characters.CharacterTable.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, characters, group_name=None, class_names=None, irrep_names=None, permutations=None, classes=None, matrices=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters.py#L2857)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters.py#L2857?message=Update%20Docs)]
</div>
**LLM Docstring**

Store a character table and derive its group order and conjugacy-class sizes from column norms.
  - `characters`: `object`
    > Character table values with irreducible representations along rows.
  - `group_name`: `object`
    > Optional label for the group. Defaults to `None`.
  - `class_names`: `object`
    > Value used as `class_names` by the implementation. Defaults to `None`.
  - `irrep_names`: `object`
    > Optional irreducible-representation labels. Defaults to `None`.
  - `permutations`: `object`
    > Atom permutations for each symmetry operation. Defaults to `None`.
  - `classes`: `object`
    > Conjugacy-class definitions or display labels. Defaults to `None`.
  - `matrices`: `object`
    > Value used as `matrices` by the implementation. Defaults to `None`.
  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.Symmetry.Characters.CharacterTable.symmetric_group" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
symmetric_group(cls, n): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2902)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2902?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a `CharacterTable` for the requested symmetric group using the module-level generators.
  - `n`: `object`
    > Group order or problem size used to construct the requested representation.
  - `:returns`: `CharacterTable`
    > The populated character-table object.


<a id="McUtils.Symmetry.Characters.CharacterTable.cyclic_group" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
cyclic_group(cls, n): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2925)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2925?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a `CharacterTable` for the requested cyclic group using the module-level generators.
  - `n`: `object`
    > Group order or problem size used to construct the requested representation.
  - `:returns`: `CharacterTable`
    > The populated character-table object.


<a id="McUtils.Symmetry.Characters.CharacterTable.dihedral_group" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
dihedral_group(cls, n): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2949)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2949?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a `CharacterTable` for the requested dihedral group using the module-level generators.
  - `n`: `object`
    > Group order or problem size used to construct the requested representation.
  - `:returns`: `CharacterTable`
    > The populated character-table object.


<a id="McUtils.Symmetry.Characters.CharacterTable.improper_rotation_group" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
improper_rotation_group(cls, n): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2972)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2972?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a `CharacterTable` for the requested improper rotation group using the module-level generators.
  - `n`: `object`
    > Group order or problem size used to construct the requested representation.
  - `:returns`: `CharacterTable`
    > The populated character-table object.


<a id="McUtils.Symmetry.Characters.CharacterTable.point_group" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
point_group(cls, key, n=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2996)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2996?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a `CharacterTable` for the requested point group using the module-level generators.
  - `key`: `object`
    > Point-group family key or fixed group name.
  - `n`: `object`
    > Group order or problem size used to construct the requested representation. Defaults to `None`.
  - `:returns`: `CharacterTable`
    > The populated character-table object.


<a id="McUtils.Symmetry.Characters.CharacterTable.fixed_size_point_group" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fixed_size_point_group(cls, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3026)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3026?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct the hard-coded or analytic character table for the `fixed_size` group family.
  - `key`: `object`
    > Point-group family key or fixed group name.
  - `:returns`: `np.ndarray`
    > The square character table with irreducible representations along rows.


<a id="McUtils.Symmetry.Characters.CharacterTable.format_character_table" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
format_character_table(self, table, group_name=None, classes=None, irrep_names=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3040)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3040?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct the hard-coded or analytic character table for the `format` group family.
  - `table`: `object`
    > Character table to format.
  - `group_name`: `object`
    > Optional label for the group. Defaults to `None`.
  - `classes`: `object`
    > Conjugacy-class definitions or display labels. Defaults to `None`.
  - `irrep_names`: `object`
    > Optional irreducible-representation labels. Defaults to `None`.
  - `:returns`: `np.ndarray`
    > The square character table with irreducible representations along rows.


<a id="McUtils.Symmetry.Characters.CharacterTable.group_key" class="docs-object-method">&nbsp;</a> 
```python
@property
group_key(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3085)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3085?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert stored group metadata into a compact point-group key such as `C3v`.
  - `:returns`: `str | None`
    > The normalized group key, or `None` when unnamed.


<a id="McUtils.Symmetry.Characters.CharacterTable.symmetry_symbol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
symmetry_symbol(cls, primary_axis, secondary_axis, type, axis, root, order): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3106?message=Update%20Docs)]
</div>
**LLM Docstring**

Translate a classified Cartesian transformation into a conventional symmetry-operation symbol.
  - `primary_axis`: `object`
    > Primary molecular symmetry axis.
  - `secondary_axis`: `object`
    > Secondary reference axis.
  - `type`: `object`
    > Cartesian transformation type code.
  - `axis`: `object`
    > Axis vector defining the symmetry operation.
  - `root`: `object`
    > Integer power of the primitive rotation.
  - `order`: `object`
    > Order of the rotation or improper rotation.
  - `:returns`: `str`
    > A symbol such as `E`, `i`, `Cn`, `Sn`, or a reflection-plane label.


<a id="McUtils.Symmetry.Characters.CharacterTable.get_class_symbols" class="docs-object-method">&nbsp;</a> 
```python
get_class_symbols(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3158)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3158?message=Update%20Docs)]
</div>
**LLM Docstring**

Classify representative matrices and produce display symbols for each conjugacy class.
  - `:returns`: `list[str]`
    > The ordered class symbols.


<a id="McUtils.Symmetry.Characters.CharacterTable.format" class="docs-object-method">&nbsp;</a> 
```python
format(self, classes=None, irrep_names=None, group_name=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3198)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3198?message=Update%20Docs)]
</div>
**LLM Docstring**

Format this table using stored metadata unless explicit labels are supplied.
  - `classes`: `object`
    > Conjugacy-class definitions or display labels. Defaults to `None`.
  - `irrep_names`: `object`
    > Optional irreducible-representation labels. Defaults to `None`.
  - `group_name`: `object`
    > Optional label for the group. Defaults to `None`.
  - `:returns`: `str`
    > A formatted character-table string.


<a id="McUtils.Symmetry.Characters.CharacterTable.character_basis" class="docs-object-method">&nbsp;</a> 
```python
@property
character_basis(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3228)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3228?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the class-weighted, group-order-normalized character basis used for projections.
  - `:returns`: `np.ndarray`
    > The projection basis matrix.


<a id="McUtils.Symmetry.Characters.CharacterTable.extend_class_representation" class="docs-object-method">&nbsp;</a> 
```python
extend_class_representation(self, rep): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3244)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3244?message=Update%20Docs)]
</div>
**LLM Docstring**

Expand class-level representation values to one value per concrete group element.
  - `rep`: `object`
    > Character or class representation to transform or decompose.
  - `:returns`: `np.ndarray`
    > The element-level representation array.


<a id="McUtils.Symmetry.Characters.CharacterTable.get_extended_character_table" class="docs-object-method">&nbsp;</a> 
```python
get_extended_character_table(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3263)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3263?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct the hard-coded or analytic character table for the `get_extended` group family.
  - `:returns`: `np.ndarray`
    > The square character table with irreducible representations along rows.


<a id="McUtils.Symmetry.Characters.CharacterTable.decompose_representation" class="docs-object-method">&nbsp;</a> 
```python
decompose_representation(self, rep): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3274)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3274?message=Update%20Docs)]
</div>
**LLM Docstring**

Project a representation onto irreducible characters using the weighted character inner product.
  - `rep`: `object`
    > Character or class representation to transform or decompose.
  - `:returns`: `np.ndarray`
    > Irreducible-representation multiplicities.


<a id="McUtils.Symmetry.Characters.CharacterTable.space_representation" class="docs-object-method">&nbsp;</a> 
```python
space_representation(self, mats, symms=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3291)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3291?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute traces of transformation matrices, optionally after combining them with supplied symmetry operations.
  - `mats`: `object`
    > Transformation matrices whose traces or actions define a representation.
  - `symms`: `object`
    > Optional symmetry matrices associated with `mats`. Defaults to `None`.
  - `:returns`: `np.ndarray`
    > The character vector of the matrix representation.


<a id="McUtils.Symmetry.Characters.CharacterTable.matrix_from_representation" class="docs-object-method">&nbsp;</a> 
```python
matrix_from_representation(self, vec): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3346)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3346?message=Update%20Docs)]
</div>
**LLM Docstring**

Form a matrix as a linear combination of the full group-operation matrices.
  - `vec`: `object`
    > Representation coefficients or vector to convert into a matrix.
  - `:returns`: `np.ndarray`
    > The resulting Cartesian matrix.


<a id="McUtils.Symmetry.Characters.CharacterTable.inverse_character_representation" class="docs-object-method">&nbsp;</a> 
```python
inverse_character_representation(self, chars): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3362)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3362?message=Update%20Docs)]
</div>
**LLM Docstring**

Map irreducible-character coefficients back into class-representation values.
  - `chars`: `object`
    > Character coefficients to invert into class-space values.
  - `:returns`: `np.ndarray`
    > The reconstructed class representation.


<a id="McUtils.Symmetry.Characters.CharacterTable.symmetry_permutations" class="docs-object-method">&nbsp;</a> 
```python
symmetry_permutations(self, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3377)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3377?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate permutation representatives for the requested cyclic action.
  - `coords`: `object`
    > Cartesian coordinates, normally with shape `(n_atoms, 3)`.
  - `:returns`: `np.ndarray`
    > An integer array whose rows are permutations.


<a id="McUtils.Symmetry.Characters.CharacterTable.axis_representation" class="docs-object-method">&nbsp;</a> 
```python
axis_representation(self, include_rotations=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3393)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3393?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the translational, and optionally rotational, Cartesian character representation from operation traces and determinants.
  - `include_rotations`: `object`
    > Whether rotational components are included with translations. Defaults to `True`.
  - `:returns`: `np.ndarray`
    > The axis character representation.


<a id="McUtils.Symmetry.Characters.CharacterTable.fixed_permutation_representation" class="docs-object-method">&nbsp;</a> 
```python
fixed_permutation_representation(self, base_rep, perms): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3415)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3415?message=Update%20Docs)]
</div>
**LLM Docstring**

Combine a base representation with permutation matrices by applying the same Cartesian block to each permuted index.
  - `base_rep`: `object`
    > Base representation matrix or tensor.
  - `perms`: `object`
    > Precomputed atom permutations for symmetry operations.
  - `:returns`: `np.ndarray`
    > The fixed-permutation representation tensors.


<a id="McUtils.Symmetry.Characters.CharacterTable.coordinate_representation" class="docs-object-method">&nbsp;</a> 
```python
coordinate_representation(self, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3454)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3454?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the full Cartesian coordinate representation induced by molecular symmetry permutations.
  - `coords`: `object`
    > Cartesian coordinates, normally with shape `(n_atoms, 3)`.
  - `:returns`: `np.ndarray`
    > The coordinate representation matrices.


<a id="McUtils.Symmetry.Characters.CharacterTable.coordinate_mode_reduction" class="docs-object-method">&nbsp;</a> 
```python
coordinate_mode_reduction(self, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3470)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3470?message=Update%20Docs)]
</div>
**LLM Docstring**

Decompose the Cartesian coordinate representation and subtract translational/rotational content.
  - `coords`: `object`
    > Cartesian coordinates, normally with shape `(n_atoms, 3)`.
  - `:returns`: `np.ndarray`
    > Vibrational irreducible-representation multiplicities.


<a id="McUtils.Symmetry.Characters.CharacterTable.get_full_matrices" class="docs-object-method">&nbsp;</a> 
```python
get_full_matrices(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3486)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3486?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the three-dimensional Cartesian matrix representation for selected group elements.
  - `:returns`: `np.ndarray`
    > An array of shape `(n_elements, 3, 3)`.


<a id="McUtils.Symmetry.Characters.CharacterTable.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Characters/CharacterTable.py#L3499)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters/CharacterTable.py#L3499?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a compact representation containing the group key.
  - `:returns`: `str`
    > The representation string.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/Characters/CharacterTable.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/Characters/CharacterTable.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/Characters/CharacterTable.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/Characters/CharacterTable.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Characters.py#L2856?message=Update%20Docs)   
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