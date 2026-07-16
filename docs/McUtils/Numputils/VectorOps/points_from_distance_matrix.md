# <a id="McUtils.Numputils.VectorOps.points_from_distance_matrix">points_from_distance_matrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L123)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L123?message=Update%20Docs)]
</div>

```python
points_from_distance_matrix(dist_mat, test_idx=None, target_dim=None, use_triu=False, zero_cutoff=1e-08): 
```
**LLM Docstring**

Reconstruct a set of point coordinates that reproduce a given pairwise
distance matrix (classical multidimensional scaling).

The distance matrix is squared and double-centered (or centered on `test_idx`
when supplied) to form the Gram matrix, which is diagonalized; the positive
eigenvalues and their eigenvectors give the embedded coordinates. Distances may
be passed as a dense matrix or as the flattened upper triangle (`use_triu`), and
the output can be zero-padded up to `target_dim`.
  - `dist_mat`: `np.ndarray`
    > pairwise distances (dense matrix or flattened upper triangle)
  - `test_idx`: `int | None`
    > reference point to center on (double-centering if omitted)
  - `target_dim`: `int | None`
    > dimension to zero-pad the coordinates up to
  - `use_triu`: `bool`
    > whether `dist_mat` is a flattened upper triangle
  - `zero_cutoff`: `float`
    > eigenvalue cutoff for counting significant dimensions
  - `:returns`: `np.ndarray`
    > the reconstructed point coordinates











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/points_from_distance_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/points_from_distance_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/points_from_distance_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/points_from_distance_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L123?message=Update%20Docs)   
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