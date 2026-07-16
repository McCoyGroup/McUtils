# <a id="McUtils.Numputils.TransformationMatrices.extract_rotation_angle_axis">extract_rotation_angle_axis</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TransformationMatrices.py#L291)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L291?message=Update%20Docs)]
</div>

```python
extract_rotation_angle_axis(rot_mat, normalize=True): 
```
**LLM Docstring**

Extract the rotation angle and axis from a rotation matrix.

For 2D matrices only the angle is returned; for 3D the axis comes from the skew
part with careful handling of the near-`pi` and identity degeneracies, and the
angle from an orthogonal reference vector. Higher-dimensional rotations are
decomposed via a Schur/Youla factorization into a set of plane angles and axes.
  - `rot_mat`: `np.ndarray`
    > the rotation matrix (or stack)
  - `normalize`: `bool`
    > normalize the extracted axis
  - `:returns`: `tuple`
    > `(angle, axis)` (axis is `None` in 2D)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TransformationMatrices/extract_rotation_angle_axis.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TransformationMatrices/extract_rotation_angle_axis.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TransformationMatrices/extract_rotation_angle_axis.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TransformationMatrices/extract_rotation_angle_axis.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L291?message=Update%20Docs)   
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