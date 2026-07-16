# <a id="McUtils.Numputils.CoordOps.transform_cartesian_derivatives">transform_cartesian_derivatives</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L5303)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L5303?message=Update%20Docs)]
</div>

```python
transform_cartesian_derivatives(derivs, tfs, axes=None): 
```
**LLM Docstring**

Apply a Cartesian coordinate transformation to a set of Cartesian derivative
tensors, one derivative axis at a time.

For each `n`-th order tensor the routine reshapes each Cartesian axis into
`(atom, 3)`, contracts the `3`-component sub-axis against the transformation
`tfs` (using a shared/broadcast contraction when the transformation is itself
batched), and restores the original shape. Numeric (scalar) entries are skipped.
  - `derivs`: `list[np.ndarray]`
    > the Cartesian derivative tensors
  - `tfs`: `np.ndarray`
    > the per-atom transformation matrices
  - `axes`: `list[int] | int | None`
    > `(derivative_axis, transform_axis)`; defaults to `[-1, -2]`
  - `:returns`: `list[np.ndarray]`
    > the transformed derivative tensors











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/transform_cartesian_derivatives.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/transform_cartesian_derivatives.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/transform_cartesian_derivatives.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/transform_cartesian_derivatives.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L5303?message=Update%20Docs)   
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