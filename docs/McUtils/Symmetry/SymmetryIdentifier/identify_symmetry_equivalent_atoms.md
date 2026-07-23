# <a id="McUtils.Symmetry.SymmetryIdentifier.identify_symmetry_equivalent_atoms">identify_symmetry_equivalent_atoms</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier.py#L52)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier.py#L52?message=Update%20Docs)]
</div>

```python
identify_symmetry_equivalent_atoms(coords, masses=None, base_groups=None, mass_tol=1, tol=0.01): 
```
**LLM Docstring**

Partition atoms into groups with matching masses and sorted intragroup distance profiles.
  - `coords`: `object`
    > Cartesian coordinates, normally with shape `(n_atoms, 3)`.
  - `masses`: `object`
    > Optional atomic masses aligned with `coords`. Defaults to `None`.
  - `base_groups`: `object`
    > Initial atom groups within which geometric equivalence is tested. Defaults to `None`.
  - `mass_tol`: `object`
    > Mass binning tolerance used when grouping atoms. Defaults to `1`.
  - `tol`: `object`
    > Numerical tolerance used for geometric or equality tests. Defaults to `0.01`.
  - `:returns`: `list[list[int]]`
    > Lists of atom indices judged symmetry equivalent.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/SymmetryIdentifier/identify_symmetry_equivalent_atoms.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/SymmetryIdentifier/identify_symmetry_equivalent_atoms.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/SymmetryIdentifier/identify_symmetry_equivalent_atoms.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/SymmetryIdentifier/identify_symmetry_equivalent_atoms.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier.py#L52?message=Update%20Docs)   
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