# <a id="McUtils.Numputils.VectorOps.find_basis">find_basis</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L1794)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1794?message=Update%20Docs)]
</div>

```python
find_basis(mat, nonzero_cutoff=1e-08, method='svd'): 
```
**LLM Docstring**

Find an orthonormal basis for the column space (range) of a matrix.

Supports several methods: `'qr'` returns the `Q` factor, `'svd'` returns the
left singular vectors with singular values above `nonzero_cutoff`, and
`'right-svd'` / `'right-unitary'` build right-projected bases. Batched inputs are
handled per matrix; when the retained rank varies across the batch a list of
per-matrix bases is returned rather than a single stacked array.
  - `mat`: `np.ndarray`
    > the matrix (or stack of matrices)
  - `nonzero_cutoff`: `float`
    > singular-value cutoff for retained directions
  - `method`: `str`
    > `'svd'`, `'qr'`, `'right-svd'`, or `'right-unitary'`
  - `:returns`: `np.ndarray | list[np.ndarray]`
    > the basis (or a list of bases for ragged batches)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/find_basis.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/find_basis.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/find_basis.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/find_basis.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1794?message=Update%20Docs)   
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