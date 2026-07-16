# <a id="McUtils.Numputils.VectorOps.diag_indices">diag_indices</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L792)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L792?message=Update%20Docs)]
</div>

```python
diag_indices(block_shape, n, k=2): 
```
**LLM Docstring**

Build the fancy-index tuple that addresses the `k`-fold diagonal of a tensor of
shape `block_shape + (n,) * k`.

The leading `block_shape` axes are indexed elementwise while the trailing `k`
axes share a single `arange(n)` index, so assigning through the result writes
values along the generalized diagonal.
  - `block_shape`: `tuple[int, ...]`
    > shape of the leading (batch) axes
  - `n`: `int`
    > size of each diagonal axis
  - `k`: `int`
    > number of diagonal axes
  - `:returns`: `tuple`
    > the diagonal index tuple











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/diag_indices.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/diag_indices.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/diag_indices.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/diag_indices.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L792?message=Update%20Docs)   
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