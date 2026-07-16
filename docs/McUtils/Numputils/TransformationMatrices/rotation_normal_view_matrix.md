# <a id="McUtils.Numputils.TransformationMatrices.rotation_normal_view_matrix">rotation_normal_view_matrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TransformationMatrices.py#L1268)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1268?message=Update%20Docs)]
</div>

```python
rotation_normal_view_matrix(rotation, normal, output_order=('x', 'y', 'z')): 
```
**LLM Docstring**

Build a viewing frame from a plane normal and an in-plane rotation angle.

The up vector is taken either from rotating within the plane by `rotation` or,
when no rotation is given, from the cross product of the normal with the default
right vector; the frame is then built with `view_matrix`.
  - `rotation`: `float | None`
    > in-plane rotation angle (or `None`)
  - `normal`: `np.ndarray | None`
    > the plane normal / view direction
  - `output_order`: `tuple`
    > axis output ordering
  - `:returns`: `np.ndarray`
    > the viewing frame matrix











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TransformationMatrices/rotation_normal_view_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TransformationMatrices/rotation_normal_view_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TransformationMatrices/rotation_normal_view_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TransformationMatrices/rotation_normal_view_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1268?message=Update%20Docs)   
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