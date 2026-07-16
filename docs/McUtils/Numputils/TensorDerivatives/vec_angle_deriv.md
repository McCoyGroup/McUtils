# <a id="McUtils.Numputils.TensorDerivatives.vec_angle_deriv">vec_angle_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L2101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L2101?message=Update%20Docs)]
</div>

```python
vec_angle_deriv(A_expansion, B_expansion, order, up_vector=None, component_vectors=None, unit_expansions=None, unitized=False, planar=None, planar_threshold=None): 
```
**LLM Docstring**

Compute the derivative expansion of the angle between two vectors.

Builds the cosine and sine expansions (`vec_anglecos_deriv`,
`vec_anglesin_deriv`), takes the leading angle from `arctan2`, and forms the
higher orders from `d(atan2) = cos*d(sin) - sin*d(cos)` via `scalarprod_deriv`.
  - `A_expansion`: `list`
    > expansion of the first vector
  - `B_expansion`: `list`
    > expansion of the second vector
  - `order`: `int | list[int]`
    > the derivative order(s)
  - `up_vector`: `np.ndarray | None`
    > up vector defining the sign convention
  - `component_vectors`: `list | None`
    > surrounding edge-vector expansions (planar case)
  - `unit_expansions`: `list | None`
    > precomputed unit-norm expansions (planar case)
  - `unitized`: `bool`
    > whether the inputs are already unit vectors
  - `planar`: `bool | np.ndarray | None`
    > force (or disable) the planar branch
  - `planar_threshold`: `float | None`
    > cross-norm threshold for detecting planarity
  - `:returns`: `list`
    > the angle expansion











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/vec_angle_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/vec_angle_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/vec_angle_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/vec_angle_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L2101?message=Update%20Docs)   
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