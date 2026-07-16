# <a id="McUtils.Numputils.TensorDerivatives.vec_normal_deriv">vec_normal_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L2212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L2212?message=Update%20Docs)]
</div>

```python
vec_normal_deriv(A_expansion, B_expansion, order, up_vector=None, component_vectors=None, unit_expansions=None, unitized=False, planar=None, planar_threshold=None, normalize=True): 
```
**LLM Docstring**

Compute the derivative expansion of the normal vector to two vectors (the
direction of their cross product), optionally normalized.

When `normalize` is set the unit normal from `vec_anglesin_deriv` is returned;
otherwise the raw cross-product expansion is returned.
  - `A_expansion`: `list`
    > expansion of the first vector
  - `B_expansion`: `list`
    > expansion of the second vector
  - `order`: `int | list[int]`
    > the derivative order(s)
  - `up_vector`: `np.ndarray | None`
    > up vector defining the sign convention
  - `component_vectors`: `list | None`
    > surrounding edge-vector expansions
  - `unit_expansions`: `list | None`
    > precomputed unit-norm expansions
  - `unitized`: `bool`
    > whether the inputs are already unit vectors
  - `planar`: `bool | np.ndarray | None`
    > force (or disable) the planar branch
  - `planar_threshold`: `float | None`
    > cross-norm threshold for detecting planarity
  - `normalize`: `bool`
    > return the unit normal rather than the raw cross product
  - `:returns`: `list`
    > the normal-vector expansion











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/vec_normal_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/vec_normal_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/vec_normal_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/vec_normal_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L2212?message=Update%20Docs)   
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