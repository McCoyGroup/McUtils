## <a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier">PointGroupIdentifier</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier.py#L138)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier.py#L138?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, coords, masses=None, groups=None, tol=0.01, mass_tol=1, mom_tol=1, grouping_tol=0.01, verbose=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier.py#L139)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier.py#L139?message=Update%20Docs)]
</div>
**LLM Docstring**

Prepare atom-equivalence groups, principal-axis coordinates, group rotation orders, and per-group rotor data for point-group detection.
  - `coords`: `object`
    > Cartesian coordinates, normally with shape `(n_atoms, 3)`.
  - `masses`: `object`
    > Optional atomic masses aligned with `coords`. Defaults to `None`.
  - `groups`: `object`
    > Optional atom-index groups that constrain equivalence matching. Defaults to `None`.
  - `tol`: `object`
    > Numerical tolerance used for geometric or equality tests. Defaults to `0.01`.
  - `mass_tol`: `object`
    > Mass binning tolerance used when grouping atoms. Defaults to `1`.
  - `mom_tol`: `object`
    > Tolerance used to compare principal moments of inertia. Defaults to `1`.
  - `grouping_tol`: `object`
    > Distance-profile tolerance used to identify equivalent atoms. Defaults to `0.01`.
  - `verbose`: `object`
    > Whether to print diagnostic information. Defaults to `False`.
  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.get_groups" class="docs-object-method">&nbsp;</a> 
```python
get_groups(self, coords, base_groups): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L191?message=Update%20Docs)]
</div>
**LLM Docstring**

Refine supplied atom groups by matching sorted distance profiles and merging overlapping equivalence sets.
  - `coords`: `object`
    > Cartesian coordinates, normally with shape `(n_atoms, 3)`.
  - `base_groups`: `object`
    > Initial atom groups within which geometric equivalence is tested.
  - `:returns`: `list[list[int]]`
    > The refined atom-index groups.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.get_rotor_type" class="docs-object-method">&nbsp;</a> 
```python
get_rotor_type(self, moms): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L263)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L263?message=Update%20Docs)]
</div>
**LLM Docstring**

Classify principal moments using the identifier moment tolerance.
  - `moms`: `object`
    > Value used as `moms` by the implementation.
  - `:returns`: `tuple[RotorTypes, bool]`
    > The rotor type and planarity flag.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.get_group_orders" class="docs-object-method">&nbsp;</a> 
```python
get_group_orders(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L276)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L276?message=Update%20Docs)]
</div>
**LLM Docstring**

Derive candidate proper-rotation orders from common factors of equivalent-atom group sizes.
  - `:returns`: `list[int]`
    > Candidate orders sorted from largest to smallest.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.check_element" class="docs-object-method">&nbsp;</a> 
```python
check_element(self, elem: 'SymmetryElement', verbose=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L316)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L316?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether a candidate operation maps every equivalent-atom group onto itself within coordinate tolerances.
  - `elem`: `SymmetryElement`
    > Candidate symmetry element.
  - `verbose`: `object`
    > Whether to print diagnostic information. Defaults to `False`.
  - `:returns`: `bool`
    > Whether the element is a molecular symmetry.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.get_groups_from_masses" class="docs-object-method">&nbsp;</a> 
```python
get_groups_from_masses(self, masses): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L352)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L352?message=Update%20Docs)]
</div>
**LLM Docstring**

Group atom indices by rounded mass values.
  - `masses`: `object`
    > Optional atomic masses aligned with `coords`.
  - `:returns`: `list[np.ndarray]`
    > Mass-equivalent atom groups.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.prep_coords" class="docs-object-method">&nbsp;</a> 
```python
prep_coords(self, coords, masses=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L366)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L366?message=Update%20Docs)]
</div>
**LLM Docstring**

Center coordinates, diagonalize the inertia tensor, rotate into principal axes, and classify rotor type and planarity.
  - `coords`: `object`
    > Cartesian coordinates, normally with shape `(n_atoms, 3)`.
  - `masses`: `object`
    > Optional atomic masses aligned with `coords`. Defaults to `None`.
  - `:returns`: `SymmetryEquivalentAtomData`
    > Prepared coordinate metadata.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.rotation_axis_iterator" class="docs-object-method">&nbsp;</a> 
```python
rotation_axis_iterator(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L396)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L396?message=Update%20Docs)]
</div>
**LLM Docstring**

Yield candidate rotation axes from Cartesian basis axes, atom directions, and pair midpoints while suppressing collinear duplicates.
  - `:returns`: `typing.Iterator[np.ndarray]`
    > An iterator over normalized axis vectors.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.reflection_plane_iterator" class="docs-object-method">&nbsp;</a> 
```python
reflection_plane_iterator(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L427)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L427?message=Update%20Docs)]
</div>
**LLM Docstring**

Yield candidate reflection-plane normals from Cartesian axes and pairwise coordinate differences.
  - `:returns`: `typing.Iterator[np.ndarray]`
    > An iterator over plane-normal vectors.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.rotation_face_iterator" class="docs-object-method">&nbsp;</a> 
```python
rotation_face_iterator(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L444)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L444?message=Update%20Docs)]
</div>
**LLM Docstring**

Yield normals to equilateral-like faces formed by triples of equivalent atoms.
  - `:returns`: `typing.Iterator[np.ndarray]`
    > An iterator over candidate rotation axes.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.embed_point_group" class="docs-object-method">&nbsp;</a> 
```python
embed_point_group(self, point_group: "'PointGroup|list[SymmetryElement]'"): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L465)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L465?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct the hard-coded or analytic character table for the `embed` group family.
  - `point_group`: `'PointGroup|list[SymmetryElement]'`
    > Point-group object, name, character table, or operation collection used for symmetrization.
  - `:returns`: `np.ndarray`
    > The square character table with irreducible representations along rows.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.find_point_group_alignment_axes" class="docs-object-method">&nbsp;</a> 
```python
find_point_group_alignment_axes(self, point_group: "'PointGroup|list[SymmetryElement]'"): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L484)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L484?message=Update%20Docs)]
</div>
**LLM Docstring**

Match defining rotations or reflection planes from a reference group to molecular symmetry elements and construct embedded axes.
  - `point_group`: `'PointGroup|list[SymmetryElement]'`
    > Point-group object, name, character table, or operation collection used for symmetrization.
  - `:returns`: `np.ndarray`
    > A `3 x 3` axis matrix in the original Cartesian frame.


<a id="McUtils.Symmetry.SymmetryIdentifier.PointGroupIdentifier.identify_point_group" class="docs-object-method">&nbsp;</a> 
```python
identify_point_group(self, realign=True) -> 'tuple[list[SymmetryElement], PointGroup]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L636)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.py#L636?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct the hard-coded or analytic character table for the `identify` group family.
  - `realign`: `object`
    > Whether to orient the returned point group in the molecular principal-axis frame. Defaults to `True`.
  - `:returns`: `np.ndarray`
    > The square character table with irreducible representations along rows.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/SymmetryIdentifier/PointGroupIdentifier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier.py#L138?message=Update%20Docs)   
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