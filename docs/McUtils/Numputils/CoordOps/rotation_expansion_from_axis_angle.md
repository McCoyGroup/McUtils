# <a id="McUtils.Numputils.CoordOps.rotation_expansion_from_axis_angle">rotation_expansion_from_axis_angle</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L3608)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3608?message=Update%20Docs)]
</div>

```python
rotation_expansion_from_axis_angle(coords, axis, order=1, *, angle=0.0, axis_order=0): 
```
**LLM Docstring**

Build the derivative expansion of coordinates rotated about a given axis, taken
with respect to either the rotation angle or the axis itself.

The rotation-generator derivatives come from `Geometry.axis_rot_gen_deriv`. With
`axis_order = 0` the expansion is taken in the angle; otherwise it is taken in
the axis components. A batched axis whose leading shape matches the coordinates
is handled by looping over the batch (a slow path); mismatched broadcasting is
not supported.
  - `coords`: `np.ndarray`
    > coordinates to rotate, shape `(..., N, 3)`
  - `axis`: `np.ndarray`
    > rotation axis (normalized internally)
  - `order`: `int`
    > maximum derivative order
  - `angle`: `float`
    > rotation angle
  - `axis_order`: `int`
    > `0` to differentiate w.r.t. the angle, else w.r.t. the axis
  - `:returns`: `list[np.ndarray]`
    > the rotated-coordinate expansion `[value, d1, d2, ...]`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/rotation_expansion_from_axis_angle.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/rotation_expansion_from_axis_angle.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/rotation_expansion_from_axis_angle.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/rotation_expansion_from_axis_angle.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3608?message=Update%20Docs)   
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