# <a id="McUtils.Numputils.TensorDerivatives.vec_plane_angle_deriv">vec_plane_angle_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L2384)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L2384?message=Update%20Docs)]
</div>

```python
vec_plane_angle_deriv(A_expansion, B_expansion, C_expansion, D_expansion, order, planar=None, planar_threshold=None): 
```
**LLM Docstring**

Compute the derivative expansion of the angle between two planes, each defined
by a pair of vector expansions.

Forms the two plane normals via cross products and takes the angle between them
with `vec_angle_deriv`.
  - `A_expansion`: `list`
    > first vector of plane 1
  - `B_expansion`: `list`
    > second vector of plane 1
  - `C_expansion`: `list`
    > first vector of plane 2
  - `D_expansion`: `list`
    > second vector of plane 2
  - `order`: `int | list[int]`
    > the derivative order(s)
  - `planar`: `bool | np.ndarray | None`
    > force (or disable) the planar branch
  - `planar_threshold`: `float | None`
    > cross-norm threshold for detecting planarity
  - `:returns`: `list`
    > the plane-angle expansion











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/vec_plane_angle_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/vec_plane_angle_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/vec_plane_angle_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/vec_plane_angle_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L2384?message=Update%20Docs)   
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