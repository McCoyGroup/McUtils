# <a id="McUtils.Numputils.CoordOps.book_deriv">book_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L1931)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L1931?message=Update%20Docs)]
</div>

```python
book_deriv(coords, i, j, k, l, /, order=1, zero_thresh=None, method='expansion', fixed_atoms=None, cache=None, reproject=True, expanded_vectors=None): 
```
**LLM Docstring**

Analytic derivative expansion of a *book* angle (the angle between the two
half-planes sharing the `i`-`j` edge, defined by atoms `i`, `j`, `k`, `l`) with
respect to the Cartesian coordinates.

Only `method='expansion'` is implemented. It builds the displacement/unit-vector
expansions for the three defining vectors, feeds them to
`TensorDerivatives.vec_dihed_deriv`, and (when `reproject`) maps the derivatives
back through the projection returned by the displacement setup.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `i`: `int`
    > first edge atom
  - `j`: `int`
    > second edge atom
  - `k`: `int`
    > atom defining the first half-plane
  - `l`: `int`
    > atom defining the second half-plane
  - `order`: `int`
    > maximum derivative order
  - `zero_thresh`: `float | None`
    > threshold below which values are treated as zero
  - `method`: `str`
    > derivative method (`'expansion'` only)
  - `fixed_atoms`: `Iterable[int] | None`
    > atoms whose contributions should be zeroed
  - `cache`: `dict | None`
    > expansion cache
  - `reproject`: `bool`
    > whether to reproject the derivatives onto the full coordinates
  - `expanded_vectors`: `Iterable[int] | None`
    > which of the defining vectors to expand (defaults to all)
  - `:returns`: `list`
    > the derivative expansion `[value, d1, d2, ...]`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/book_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/book_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/book_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/book_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L1931?message=Update%20Docs)   
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