# <a id="McUtils.Symmetry.Symmetrizer.symmetrize_structure">symmetrize_structure</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Symmetrizer.py#L95)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Symmetrizer.py#L95?message=Update%20Docs)]
</div>

```python
symmetrize_structure(coords, symmetry_elements: 'PointGroup|list[SymmetryElement|np.ndarray]', labels=None, masses=None, groups=None, tol=0.1, mass_tol=1, expand=True): 
```
**LLM Docstring**

Reduce each chemically equivalent coordinate group under supplied operations and optionally expand complete symmetry orbits.
  - `coords`: `object`
    > Cartesian coordinates, normally with shape `(n_atoms, 3)`.
  - `symmetry_elements`: `'PointGroup|list[SymmetryElement|np.ndarray]'`
    > Point group, symmetry elements, or raw transformation matrices.
  - `labels`: `object`
    > Optional labels associated with coordinates. Defaults to `None`.
  - `masses`: `object`
    > Optional atomic masses aligned with `coords`. Defaults to `None`.
  - `groups`: `object`
    > Optional atom-index groups that constrain equivalence matching. Defaults to `None`.
  - `tol`: `object`
    > Numerical tolerance used for geometric or equality tests. Defaults to `0.1`.
  - `mass_tol`: `object`
    > Mass binning tolerance used when grouping atoms. Defaults to `1`.
  - `expand`: `object`
    > Whether to regenerate full symmetry orbits after reduction. Defaults to `True`.
  - `:returns`: `np.ndarray | tuple[np.ndarray, list]`
    > Symmetrized coordinates, optionally paired with labels.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/Symmetrizer/symmetrize_structure.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/Symmetrizer/symmetrize_structure.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/Symmetrizer/symmetrize_structure.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/Symmetrizer/symmetrize_structure.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Symmetrizer.py#L95?message=Update%20Docs)   
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