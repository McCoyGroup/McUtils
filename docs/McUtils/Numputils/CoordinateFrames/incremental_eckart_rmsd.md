# <a id="McUtils.Numputils.CoordinateFrames.incremental_eckart_rmsd">incremental_eckart_rmsd</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordinateFrames.py#L1273)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L1273?message=Update%20Docs)]
</div>

```python
incremental_eckart_rmsd(coords, refs=None, masses=None, mass_weighted=False, **embedding_parameters): 
```
**LLM Docstring**

Compute the cumulative Eckart RMSD along a sequence of geometries.

Consecutive structures are compared pairwise with `eckart_rmsd` (or against the
supplied `refs`), and the resulting step RMSDs are cumulatively summed to give a
running path length; a leading zero is prepended so the output aligns with the
input sequence.
  - `coords`: `np.ndarray`
    > the sequence of geometries
  - `refs`: `np.ndarray | None`
    > explicit references per step (defaults to the previous frame)
  - `masses`: `np.ndarray | None`
    > per-atom masses
  - `mass_weighted`: `bool`
    > mass-weight the coordinates before comparison
  - `embedding_parameters`: `Any`
    > extra options forwarded to `eckart_rmsd`
  - `:returns`: `np.ndarray`
    > the cumulative Eckart RMSD along the sequence











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordinateFrames/incremental_eckart_rmsd.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordinateFrames/incremental_eckart_rmsd.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordinateFrames/incremental_eckart_rmsd.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordinateFrames/incremental_eckart_rmsd.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L1273?message=Update%20Docs)   
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