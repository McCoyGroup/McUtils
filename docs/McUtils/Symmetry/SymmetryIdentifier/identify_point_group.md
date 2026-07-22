# <a id="McUtils.Symmetry.SymmetryIdentifier.identify_point_group">identify_point_group</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/SymmetryIdentifier.py#L903)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier.py#L903?message=Update%20Docs)]
</div>

```python
identify_point_group(coords, masses=None, groups=None, tol=1e-08, mass_tol=1, mom_tol=1, grouping_tol=0.01, realign=True, verbose=False): 
```
**LLM Docstring**

Construct the hard-coded or analytic character table for the `identify` group family.
  - `coords`: `object`
    > Cartesian coordinates, normally with shape `(n_atoms, 3)`.
  - `masses`: `object`
    > Optional atomic masses aligned with `coords`. Defaults to `None`.
  - `groups`: `object`
    > Optional atom-index groups that constrain equivalence matching. Defaults to `None`.
  - `tol`: `object`
    > Numerical tolerance used for geometric or equality tests. Defaults to `1e-08`.
  - `mass_tol`: `object`
    > Mass binning tolerance used when grouping atoms. Defaults to `1`.
  - `mom_tol`: `object`
    > Tolerance used to compare principal moments of inertia. Defaults to `1`.
  - `grouping_tol`: `object`
    > Distance-profile tolerance used to identify equivalent atoms. Defaults to `0.01`.
  - `realign`: `object`
    > Whether to orient the returned point group in the molecular principal-axis frame. Defaults to `True`.
  - `verbose`: `object`
    > Whether to print diagnostic information. Defaults to `False`.
  - `:returns`: `np.ndarray`
    > The square character table with irreducible representations along rows.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/SymmetryIdentifier/identify_point_group.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/SymmetryIdentifier/identify_point_group.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/SymmetryIdentifier/identify_point_group.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/SymmetryIdentifier/identify_point_group.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/SymmetryIdentifier.py#L903?message=Update%20Docs)   
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