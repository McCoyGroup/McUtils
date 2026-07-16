# <a id="McUtils.Numputils.CoordinateFrames.inertial_frame_derivatives">inertial_frame_derivatives</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordinateFrames.py#L86)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L86?message=Update%20Docs)]
</div>

```python
inertial_frame_derivatives(coords, masses=None, sel=None, mass_weighted=True): 
```
**LLM Docstring**

Compute the first and second derivatives of the moment-of-inertia tensor with
respect to the (mass-weighted) Cartesian coordinates.

Working in center-of-mass, mass-weighted coordinates, the first derivatives are
assembled from the standard inertia-tensor identities and reshaped to `(3N, 3,
3)`; the second derivatives are coordinate-independent and nonzero only on the
diagonal atom blocks, so one block is built and tiled to `(3N, 3N, 3, 3)`. When
`mass_weighted` is off the derivatives are un-weighted by `M^{1/2}`.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `masses`: `np.ndarray | None`
    > per-atom masses (defaults to unit masses)
  - `sel`: `Iterable[int] | None`
    > optional subset of atoms to include
  - `mass_weighted`: `bool`
    > whether to return mass-weighted derivatives
  - `:returns`: `list[np.ndarray]`
    > `[first_derivatives, second_derivatives]` of the inertia tensor











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordinateFrames/inertial_frame_derivatives.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordinateFrames/inertial_frame_derivatives.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordinateFrames/inertial_frame_derivatives.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordinateFrames/inertial_frame_derivatives.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L86?message=Update%20Docs)   
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