# <a id="McUtils.Numputils.TensorDerivatives.vec_anglesin_deriv">vec_anglesin_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L1916)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L1916?message=Update%20Docs)]
</div>

```python
vec_anglesin_deriv(A_expansion, B_expansion, order, unitized=False, return_unit_vectors=True, planar=None, up_vector=None, component_vectors=None, unit_expansions=None, planar_threshold=None): 
```
**LLM Docstring**

Compute the derivative expansion of the sine of the angle between two vectors
(the norm of the cross product of their unit vectors), with sign and planar
handling.

Non-planar structures use the cross-product norm directly; planar (parallel)
structures fall back to `vec_parallel_cross_norm_deriv`; mixed batches are
computed separately and merged. An `up_vector` supplies the sign convention, and
the unit normal vectors can optionally be returned.
  - `A_expansion`: `list`
    > expansion of the first vector
  - `B_expansion`: `list`
    > expansion of the second vector
  - `order`: `int | list[int]`
    > the derivative order(s)
  - `unitized`: `bool`
    > whether the inputs are already unit vectors
  - `return_unit_vectors`: `bool`
    > also return the unit normal expansion
  - `planar`: `bool | np.ndarray | None`
    > force (or disable) the planar branch (auto-detected if `None`)
  - `up_vector`: `np.ndarray | list | None`
    > up vector defining the sign convention
  - `component_vectors`: `list | None`
    > the surrounding edge-vector expansions (planar case)
  - `unit_expansions`: `list | None`
    > precomputed unit-norm expansions (planar case)
  - `planar_threshold`: `float | None`
    > cross-norm threshold for detecting planarity
  - `:returns`: `list | tuple`
    > the sine expansion (and unit normals if requested)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/vec_anglesin_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/vec_anglesin_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/vec_anglesin_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/vec_anglesin_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L1916?message=Update%20Docs)   
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