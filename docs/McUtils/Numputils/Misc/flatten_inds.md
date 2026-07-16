# <a id="McUtils.Numputils.Misc.flatten_inds">flatten_inds</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Misc.py#L311)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Misc.py#L311?message=Update%20Docs)]
</div>

```python
flatten_inds(A, *idx_blocks): 
```
**LLM Docstring**

Reshape an array by collapsing one or more contiguous axis blocks into single
axes.

Each `(i, j)` block (negative indices allowed) is fused into one axis of size
`prod(shape[i:j+1])`, leaving the other axes untouched. This mirrors the index
bookkeeping used when flattening atom/component blocks.
  - `A`: `np.ndarray`
    > the array to reshape
  - `idx_blocks`: `tuple[int, int]`
    > `(start, end)` inclusive axis ranges to collapse
  - `:returns`: `np.ndarray`
    > the reshaped array











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Misc/flatten_inds.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Misc/flatten_inds.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Misc/flatten_inds.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Misc/flatten_inds.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Misc.py#L311?message=Update%20Docs)   
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