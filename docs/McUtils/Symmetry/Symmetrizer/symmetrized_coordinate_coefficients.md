# <a id="McUtils.Symmetry.Symmetrizer.symmetrized_coordinate_coefficients">symmetrized_coordinate_coefficients</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Symmetrizer.py#L174)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Symmetrizer.py#L174?message=Update%20Docs)]
</div>

```python
symmetrized_coordinate_coefficients(point_group, coords, masses=None, permutation_basis=None, as_characters=True, character_reps=None, normalize=False, perms=None, ops=None, return_basis=None, merge_equivalents=None, drop_empty_modes=None, realign=True, permutation_tol=0.01, **pg_tols): 
```
**LLM Docstring**

Build Cartesian or custom permutation representations, optionally project them into character blocks, normalize modes, and merge symmetry-equivalent coordinates.
  - `point_group`: `object`
    > Point-group object, name, character table, or operation collection used for symmetrization.
  - `coords`: `object`
    > Cartesian coordinates, normally with shape `(n_atoms, 3)`.
  - `masses`: `object`
    > Optional atomic masses aligned with `coords`. Defaults to `None`.
  - `permutation_basis`: `object`
    > Callable that builds a representation basis from atom permutations. Defaults to `None`.
  - `as_characters`: `object`
    > Whether to project the operation basis into irreducible-character blocks. Defaults to `True`.
  - `normalize`: `object`
    > Whether to normalize generated mode vectors. Defaults to `False`.
  - `perms`: `object`
    > Precomputed atom permutations for symmetry operations. Defaults to `None`.
  - `ops`: `object`
    > Precomputed Cartesian symmetry matrices. Defaults to `None`.
  - `return_basis`: `object`
    > Whether to return the underlying basis metadata. Defaults to `None`.
  - `merge_equivalents`: `object`
    > Whether to merge coordinates connected by the symmetry action. Defaults to `None`.
  - `drop_empty_modes`: `object`
    > Whether to remove zero-norm modes. Defaults to `None`.
  - `realign`: `object`
    > Whether to orient the returned point group in the molecular principal-axis frame. Defaults to `True`.
  - `permutation_tol`: `object`
    > Tolerance used to infer atom permutations from transformed coordinates. Defaults to `0.01`.
  - `pg_tols`: `dict`
    > Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
  - `:returns`: `object`
    > Symmetry-adapted mode coefficients, optionally with the generated basis.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/Symmetrizer/symmetrized_coordinate_coefficients.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/Symmetrizer/symmetrized_coordinate_coefficients.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/Symmetrizer/symmetrized_coordinate_coefficients.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/Symmetrizer/symmetrized_coordinate_coefficients.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Symmetrizer.py#L174?message=Update%20Docs)   
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