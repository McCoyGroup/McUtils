# <a id="McUtils.Numputils.VectorOps.semisparse_tensordot">semisparse_tensordot</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L1111)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1111?message=Update%20Docs)]
</div>

```python
semisparse_tensordot(sparse_data, a, /, axes, shared=None): 
```
**LLM Docstring**

Contract a sparse tensor (given as `(positions, values, shape)`) with a dense
array, analogous to `np.tensordot` but exploiting the sparsity.

The requested `axes` of each operand are aligned (with an optional number of
`shared` leading batch axes), the sparse positions are flattened into a
contracted/free index pair, and the contraction is performed either as a single
`vec_tensordot` (full contraction) or an explicit accumulation over the nonzero
entries.
  - `sparse_data`: `tuple`
    > the sparse tensor as `(positions, values, shape)`
  - `a`: `np.ndarray`
    > the dense array to contract against
  - `axes`: `tuple`
    > `(sparse_axes, dense_axes)` to contract
  - `shared`: `int | None`
    > number of shared leading batch axes
  - `:returns`: `np.ndarray`
    > the contracted result











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/semisparse_tensordot.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/semisparse_tensordot.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/semisparse_tensordot.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/semisparse_tensordot.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1111?message=Update%20Docs)   
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