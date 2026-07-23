# <a id="McUtils.Numputils.TensorDerivatives.vec_dihed_deriv">vec_dihed_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L2294)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L2294?message=Update%20Docs)]
</div>

```python
vec_dihed_deriv(A_expansion, B_expansion, C_expansion, order, B_norms=None, planar=None, planar_threshold=None, up_vector=None): 
```
**LLM Docstring**

Compute the derivative expansion of a dihedral angle from the three edge-vector
expansions that define it.

Forms the two plane normals (`b x a`, `b x c`), unitizes them, handles colinear
degeneracies by perturbing along an up vector, and takes the signed angle
between the normals with `vec_angle_deriv`. A `pi` shift is applied to match the
Gaussian sign convention.
  - `A_expansion`: `list`
    > expansion of the first edge vector
  - `B_expansion`: `list`
    > expansion of the central edge vector
  - `C_expansion`: `list`
    > expansion of the third edge vector
  - `order`: `int | list[int]`
    > the derivative order(s)
  - `B_norms`: `list | None`
    > precomputed norm expansion of the central vector
  - `planar`: `bool | np.ndarray | None`
    > force (or disable) the planar branch
  - `planar_threshold`: `float | None`
    > cross-norm threshold for detecting planarity
  - `up_vector`: `np.ndarray | None`
    > up vector for resolving fully colinear inputs
  - `:returns`: `list`
    > the dihedral-angle expansion











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/vec_dihed_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/vec_dihed_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/vec_dihed_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/vec_dihed_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L2294?message=Update%20Docs)   
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