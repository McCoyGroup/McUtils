# <a id="McUtils.Numputils.CoordinateFrames.eckart_permutation">eckart_permutation</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordinateFrames.py#L1045)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L1045?message=Update%20Docs)]
</div>

```python
eckart_permutation(ref, coords, masses=None, sel=None, in_paf=False, prealign=False, planar_ref_tolerance=1e-06, proper_rotation=False, permutable_groups=None): 
```
**LLM Docstring**

Find, for each structure, the atom permutation that best matches a reference
under the Eckart embedding.

Optionally pre-aligns the coordinates, then works group by group over the
`permutable_groups`: for each group it Eckart-embeds, builds the mass-weighted
distance matrix between embedded coordinates and reference atoms, and solves the
assignment problem (`scipy.optimize.linear_sum_assignment`) to get the optimal
relabeling.
  - `ref`: `np.ndarray`
    > the reference geometry
  - `coords`: `np.ndarray`
    > the coordinates to permute
  - `masses`: `np.ndarray | None`
    > per-atom masses (defaults to unit masses)
  - `sel`: `Iterable[int] | None`
    > optional subset of atoms to consider
  - `in_paf`: `bool`
    > whether the inputs are already in the principal-axis frame
  - `prealign`: `bool`
    > Eckart-align the coordinates before matching
  - `planar_ref_tolerance`: `float`
    > tolerance for detecting a planar reference
  - `proper_rotation`: `bool`
    > restrict embeddings to proper rotations
  - `permutable_groups`: `Iterable | None`
    > groups of atoms allowed to permute (defaults to all)
  - `:returns`: `np.ndarray`
    > the optimal per-structure atom permutations











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordinateFrames/eckart_permutation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordinateFrames/eckart_permutation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordinateFrames/eckart_permutation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordinateFrames/eckart_permutation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L1045?message=Update%20Docs)   
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