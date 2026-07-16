# <a id="McUtils.Numputils.CoordOps.prep_unit_vector_expansion_from_cache">prep_unit_vector_expansion_from_cache</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L1145)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L1145?message=Update%20Docs)]
</div>

```python
prep_unit_vector_expansion_from_cache(cache, coords, i, j, at_list, *, order, expand, fixed_atoms): 
```
**LLM Docstring**

Prepare the derivative expansion of the *normalized* displacement vector
(unit bond vector) between atoms `i` and `j`, reusing a cache where possible.

When no cache is available (or `fixed_atoms`/non-expanded requests make caching
unsafe) the norm/unit-vector expansion is computed directly from
`prep_disp_expansion`. Otherwise the expensive `(i, j)` unit-vector expansion is
computed once on the minimal atom pair, cached keyed by `((i, j), expand,
fixed_atoms)`, and re-embedded into the `at_list` block with
`prep_expanded_mats_from_cache`.
  - `cache`: `dict | None`
    > expansion cache (may be `None`)
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `i`: `int`
    > index of the tail atom
  - `j`: `int`
    > index of the head atom
  - `at_list`: `Iterable[int]`
    > atoms retained in the reduced block
  - `order`: `int`
    > maximum derivative order
  - `expand`: `bool`
    > whether to compute derivatives (vs. just the value)
  - `fixed_atoms`: `Iterable[int] | None`
    > atoms whose contributions should be zeroed
  - `:returns`: `tuple`
    > `(projection, (norm_expansion, unit_vector_expansion))`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/prep_unit_vector_expansion_from_cache.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/prep_unit_vector_expansion_from_cache.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/prep_unit_vector_expansion_from_cache.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/prep_unit_vector_expansion_from_cache.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L1145?message=Update%20Docs)   
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