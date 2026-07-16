# <a id="McUtils.Numputils.CoordOps.orientation_deriv">orientation_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L2513)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L2513?message=Update%20Docs)]
</div>

```python
orientation_deriv(coords, frame_pos_1, frame_pos_2, *, order=1, masses=None, fixed_atoms=None, cache=None, reproject=True, return_frame=False, return_rot=True): 
```
**LLM Docstring**

Derivative expansion of the relative orientation coordinate between two atom
fragments with respect to the Cartesian coordinates.

Both fragments are expanded with `transrot_deriv` in the shared axis system from
`_orientation_axis_system`, then combined with mass-weighted coefficients
`p1 = m1 / sqrt(m1^2 + m2^2)` and `p2 = m2 / sqrt(m1^2 + m2^2)`. (The commented
block preserves an earlier angle-based formulation.)
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `frame_pos_1`: `Iterable[int]`
    > atom indices of the first fragment
  - `frame_pos_2`: `Iterable[int]`
    > atom indices of the second fragment
  - `order`: `int`
    > maximum derivative order
  - `masses`: `np.ndarray | None`
    > per-atom masses (defaults to unit masses)
  - `fixed_atoms`: `Iterable[int] | None`
    > atoms whose contributions should be zeroed
  - `cache`: `dict | None`
    > expansion cache (interface parity)
  - `reproject`: `bool`
    > interface parity
  - `return_frame`: `bool`
    > whether to also return the per-fragment frames
  - `return_rot`: `bool`
    > whether to include rotational modes
  - `:returns`: `list | tuple`
    > the expansion, or `(expansion, frames)` if `return_frame`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/orientation_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/orientation_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/orientation_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/orientation_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L2513?message=Update%20Docs)   
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