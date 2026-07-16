# <a id="McUtils.Numputils.CoordinateFrames.frame_displacement_projector">frame_displacement_projector</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordinateFrames.py#L534)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L534?message=Update%20Docs)]
</div>

```python
frame_displacement_projector(tr_modes, masses, mass_weighted=False, orthonormal=True, pre_weighted=False): 
```
**LLM Docstring**

Build the projector that removes a set of frame (translation/rotation) modes
from a displacement space.

Depending on `mass_weighted` and `pre_weighted`, the appropriate left inverse of
the mode matrix is formed (applying or assuming the `M^{±1/2}` weighting), then
the complementary projector `I - L Lᵀ` is assembled — orthonormally via
`orthogonal_projection_matrix` when `orthonormal` is set, otherwise by an
explicit contraction.
  - `tr_modes`: `np.ndarray`
    > the translation/rotation mode vectors
  - `masses`: `np.ndarray`
    > per-atom masses
  - `mass_weighted`: `bool`
    > whether the output space should be mass-weighted
  - `orthonormal`: `bool`
    > whether the modes are orthonormal
  - `pre_weighted`: `bool`
    > whether the modes already carry the mass weighting
  - `:returns`: `np.ndarray`
    > the frame-removing projector











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordinateFrames/frame_displacement_projector.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordinateFrames/frame_displacement_projector.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordinateFrames/frame_displacement_projector.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordinateFrames/frame_displacement_projector.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L534?message=Update%20Docs)   
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