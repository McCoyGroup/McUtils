# <a id="McUtils.Numputils.PermutationOps.levi_cevita_tensor">levi_cevita_tensor</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/PermutationOps.py#L71)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L71?message=Update%20Docs)]
</div>

```python
levi_cevita_tensor(k, sparse=False): 
```
**LLM Docstring**

Build the rank-`k` Levi-Civita (permutation) tensor, dense or sparse.

Uses `levi_cevita_maps` to place `±1` at the permutation positions; a
`SparseArray` is returned when `sparse` is set, otherwise a dense integer array.
  - `k`: `int`
    > the tensor rank
  - `sparse`: `bool`
    > return a `SparseArray` instead of a dense array
  - `:returns`: `np.ndarray | SparseArray`
    > the Levi-Civita tensor











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/PermutationOps/levi_cevita_tensor.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/PermutationOps/levi_cevita_tensor.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/PermutationOps/levi_cevita_tensor.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/PermutationOps/levi_cevita_tensor.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L71?message=Update%20Docs)   
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