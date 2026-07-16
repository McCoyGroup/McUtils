# <a id="McUtils.Numputils.CoordinateFrames.translation_rotation_projector">translation_rotation_projector</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordinateFrames.py#L583)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L583?message=Update%20Docs)]
</div>

```python
translation_rotation_projector(coords, masses=None, mass_weighted=False, return_modes=False, orthonormal=True): 
```
**LLM Docstring**

Build the projector that removes overall translation and rotation from a
Cartesian displacement space.

The translation/rotation eigenvectors are obtained from
`translation_rotation_eigenvectors` and passed to
`frame_displacement_projector`. The mode vectors themselves can optionally be
returned alongside the projector.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `masses`: `np.ndarray | None`
    > per-atom masses (defaults to unit masses)
  - `mass_weighted`: `bool`
    > whether the output space should be mass-weighted
  - `return_modes`: `bool`
    > also return the translation/rotation modes
  - `orthonormal`: `bool`
    > whether to build an orthonormal projector
  - `:returns`: `np.ndarray | tuple`
    > the projector (and the modes if `return_modes`)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordinateFrames/translation_rotation_projector.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordinateFrames/translation_rotation_projector.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordinateFrames/translation_rotation_projector.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordinateFrames/translation_rotation_projector.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L583?message=Update%20Docs)   
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