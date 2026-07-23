# <a id="McUtils.Numputils.CoordinateFrames.translation_rotation_invariant_transformation">translation_rotation_invariant_transformation</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordinateFrames.py#L667)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L667?message=Update%20Docs)]
</div>

```python
translation_rotation_invariant_transformation(coords, masses=None, mass_weighted=True, strip_embedding=True): 
```
**LLM Docstring**

Construct the transformation (and its inverse) into the space of internal,
translation/rotation-invariant coordinates.

The translation/rotation projector is diagonalized; the near-zero eigenvectors
are replaced by the exact translation/rotation modes, and the remaining
eigenvectors span the invariant subspace (optionally stripped of the embedding
directions). The transformation and inverse are un-mass-weighted with `M^{±1/2}`
when `mass_weighted` is off.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `masses`: `np.ndarray | None`
    > per-atom masses (defaults to unit masses)
  - `mass_weighted`: `bool`
    > whether to keep the transformation mass-weighted
  - `strip_embedding`: `bool`
    > drop the translation/rotation columns from the result
  - `:returns`: `tuple[np.ndarray, np.ndarray]`
    > `(transformation, inverse)`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordinateFrames/translation_rotation_invariant_transformation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordinateFrames/translation_rotation_invariant_transformation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordinateFrames/translation_rotation_invariant_transformation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordinateFrames/translation_rotation_invariant_transformation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L667?message=Update%20Docs)   
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