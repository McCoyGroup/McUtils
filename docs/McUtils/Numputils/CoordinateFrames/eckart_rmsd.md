# <a id="McUtils.Numputils.CoordinateFrames.eckart_rmsd">eckart_rmsd</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordinateFrames.py#L1194)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L1194?message=Update%20Docs)]
</div>

```python
eckart_rmsd(coords, ref, masses=None, embed=True, comparison_sel=None, embedding_sel=None, mass_weighted=False, return_diffs=False, averaged=False, total=False, **embedding_parameters): 
```
**LLM Docstring**

Compute the RMSD between a set of coordinates and a reference after Eckart
embedding.

The coordinates are optionally Eckart-embedded onto the reference (using
`embedding_sel`), optionally mass-weighted, and optionally restricted to
`comparison_sel` before the (unaligned) RMSD is taken with
`unembedded_pts_rmsd`.
  - `coords`: `np.ndarray`
    > the coordinates to compare
  - `ref`: `np.ndarray`
    > the reference geometry
  - `masses`: `np.ndarray | None`
    > per-atom masses
  - `embed`: `bool`
    > whether to Eckart-embed before comparing
  - `comparison_sel`: `Iterable[int] | None`
    > atoms included in the RMSD
  - `embedding_sel`: `Iterable[int] | None`
    > atoms used to define the embedding
  - `mass_weighted`: `bool`
    > mass-weight the coordinates before comparison
  - `return_diffs`: `bool`
    > also return the difference vectors
  - `averaged`: `bool`
    > per-atom rather than per-coordinate normalization
  - `total`: `bool`
    > apply the per-atom normalization
  - `embedding_parameters`: `Any`
    > extra options forwarded to `eckart_embedding`
  - `:returns`: `np.ndarray | tuple`
    > the Eckart RMSD (plus diffs if requested)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordinateFrames/eckart_rmsd.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordinateFrames/eckart_rmsd.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordinateFrames/eckart_rmsd.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordinateFrames/eckart_rmsd.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L1194?message=Update%20Docs)   
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