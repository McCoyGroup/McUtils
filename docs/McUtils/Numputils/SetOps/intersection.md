# <a id="McUtils.Numputils.SetOps.intersection">intersection</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/SetOps.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L115?message=Update%20Docs)]
</div>

```python
intersection(ar1, ar2, assume_unique=False, return_indices=False, sortings=None, union_sorting=None, minimal_dtype=False): 
```
**LLM Docstring**

Compute the intersection of two arrays, supporting multi-dimensional rows.

For 1D inputs this defers to `intersect1d`; for higher-dimensional inputs the
rows are coerced to a compound dtype, intersected, and un-coerced back. Indices
into the inputs can optionally be returned.
  - `ar1`: `np.ndarray`
    > the first array
  - `ar2`: `np.ndarray`
    > the second array
  - `assume_unique`: `bool`
    > assume both inputs already contain no duplicates
  - `return_indices`: `bool`
    > also return the indices of the shared rows
  - `sortings`: `tuple | None`
    > precomputed sortings of the inputs
  - `union_sorting`: `np.ndarray | None`
    > precomputed sorting of the concatenated inputs
  - `minimal_dtype`: `bool`
    > down-cast returned indices to a minimal dtype
  - `:returns`: `np.ndarray | tuple`
    > the intersection (plus indices if requested)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/SetOps/intersection.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/SetOps/intersection.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/SetOps/intersection.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/SetOps/intersection.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L115?message=Update%20Docs)   
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