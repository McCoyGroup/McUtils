# <a id="McUtils.Numputils.VectorOps.symmetrize_array">symmetrize_array</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L2317)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L2317?message=Update%20Docs)]
</div>

```python
symmetrize_array(a, axes=None, symmetrization_mode='total', axes_block_ordering=None, mixed_block_symmetrize=False, restricted_diagonal=False, out=None): 
```
**LLM Docstring**

Symmetrize an array over one or more groups of axes.

The default `'total'` mode averages the array over all permutations within each
axis group. Other modes select rather than average a canonical ordering
(`'low'`, `'high'`, `'average'`) and broadcast it across the permuted positions;
`restricted_diagonal`, `axes_block_ordering`, and `mixed_block_symmetrize`
control which index tuples and permutations participate.
  - `a`: `np.ndarray`
    > the array to symmetrize
  - `axes`: `Iterable | None`
    > axis or list of axis groups to symmetrize over (defaults to all)
  - `symmetrization_mode`: `str`
    > `'total'`, `'low'`, `'high'`, `'average'`, or `'unhandled'`
  - `axes_block_ordering`: `Iterable | None`
    > explicit block ordering for the selected value
  - `mixed_block_symmetrize`: `bool`
    > permute across all axes rather than within blocks
  - `restricted_diagonal`: `bool`
    > restrict to diagonal index tuples
  - `out`: `np.ndarray | None`
    > optional output array to write into
  - `:returns`: `np.ndarray`
    > the symmetrized array











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/symmetrize_array.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/symmetrize_array.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/symmetrize_array.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/symmetrize_array.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L2317?message=Update%20Docs)   
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