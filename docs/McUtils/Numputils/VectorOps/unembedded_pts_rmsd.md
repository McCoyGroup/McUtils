# <a id="McUtils.Numputils.VectorOps.unembedded_pts_rmsd">unembedded_pts_rmsd</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L232)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L232?message=Update%20Docs)]
</div>

```python
unembedded_pts_rmsd(coords, ref, return_diffs=False, averaged=False, total=False): 
```
**LLM Docstring**

Compute the RMSD between a set of coordinates and a reference *without* first
aligning (embedding) them.

The straight coordinate difference norm is taken; when `total` is set the norm
is divided by `sqrt(n_atoms)` (or `sqrt(n_atoms * 3)` unless `averaged`) to give
a per-atom value. The raw difference vectors can optionally be returned.
  - `coords`: `np.ndarray`
    > the coordinates, shape `(..., N, 3)`
  - `ref`: `np.ndarray`
    > the reference coordinates
  - `return_diffs`: `bool`
    > also return the difference vectors
  - `averaged`: `bool`
    > normalize by `sqrt(n_atoms)` rather than `sqrt(3 * n_atoms)`
  - `total`: `bool`
    > whether to apply the per-atom normalization
  - `:returns`: `np.ndarray | tuple`
    > the RMSD (plus diffs if requested)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/unembedded_pts_rmsd.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/unembedded_pts_rmsd.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/unembedded_pts_rmsd.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/unembedded_pts_rmsd.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L232?message=Update%20Docs)   
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