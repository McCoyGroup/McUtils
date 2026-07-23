# <a id="McUtils.Symmetry.Symmetrizer.symmetrize_internals">symmetrize_internals</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Symmetrizer.py#L440)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Symmetrizer.py#L440?message=Update%20Docs)]
</div>

```python
symmetrize_internals(point_group, internals, cartesians=None, *, masses=None, as_characters=True, normalize=None, perms=None, return_expansions=False, return_base_expansion=False, ops=None, atom_selection=None, reduce_redundant_coordinates=None, **etc): 
```
**LLM Docstring**

Generate symmetry-adapted internal-coordinate coefficients and optionally Cartesian expansion tensors and redundant-coordinate reductions.
  - `point_group`: `object`
    > Point-group object, name, character table, or operation collection used for symmetrization.
  - `internals`: `object`
    > Internal-coordinate definitions.
  - `cartesians`: `object`
    > Cartesian coordinates or, in supported integer-shaped cases, explicit atom permutations. Defaults to `None`.
  - `masses`: `object`
    > Optional atomic masses aligned with `coords`. Defaults to `None`.
  - `as_characters`: `object`
    > Whether to project the operation basis into irreducible-character blocks. Defaults to `True`.
  - `normalize`: `object`
    > Whether to normalize generated mode vectors. Defaults to `None`.
  - `perms`: `object`
    > Precomputed atom permutations for symmetry operations. Defaults to `None`.
  - `return_expansions`: `object`
    > Whether, and to what tensor order, internal-coordinate expansions are returned. Defaults to `False`.
  - `return_base_expansion`: `object`
    > Whether to include the unsymmetrized base expansion. Defaults to `False`.
  - `ops`: `object`
    > Precomputed Cartesian symmetry matrices. Defaults to `None`.
  - `atom_selection`: `object`
    > Optional atom subset used for the symmetry analysis. Defaults to `None`.
  - `reduce_redundant_coordinates`: `object`
    > Whether to construct a reduced redundant-coordinate transformation. Defaults to `None`.
  - `etc`: `dict`
    > Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
  - `:returns`: `tuple`
    > A tuple containing coefficients, basis coordinates, and any requested expansions.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/Symmetrizer/symmetrize_internals.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/Symmetrizer/symmetrize_internals.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/Symmetrizer/symmetrize_internals.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/Symmetrizer/symmetrize_internals.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Symmetrizer.py#L440?message=Update%20Docs)   
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