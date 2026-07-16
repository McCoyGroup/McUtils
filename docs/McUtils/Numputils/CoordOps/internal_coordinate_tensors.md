# <a id="McUtils.Numputils.CoordOps.internal_coordinate_tensors">internal_coordinate_tensors</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L3313)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3313?message=Update%20Docs)]
</div>

```python
internal_coordinate_tensors(coords, specs, order=None, return_inverse=False, masses=None, fixed_atoms=None, fixed_cartesians=None, fixed_coords=None, remove_inverse_translation_rotation=True, **opts): 
```
**LLM Docstring**

Compute the internal coordinates for a geometry together with their forward
(and optionally inverse) derivative tensors.

The forward expansion comes from `internal_conversion_function`; its derivative
terms are cleaned with `prep_internal_derivatives` (zeroing fixed
atoms/Cartesians/coordinates). When `return_inverse` is set the inverse
transformation is also produced via `inverse_internal_coordinate_tensors`.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `specs`: `Iterable`
    > the coordinate specifications
  - `order`: `int | None`
    > maximum derivative order (`None` = values only)
  - `return_inverse`: `bool`
    > whether to also return the inverse tensors
  - `masses`: `np.ndarray | None`
    > per-atom masses (used for the inverse)
  - `fixed_atoms`: `Iterable[int] | None`
    > atoms to hold fixed
  - `fixed_cartesians`: `Iterable | None`
    > `(atom, component)` Cartesians to hold fixed
  - `fixed_coords`: `Iterable[int] | None`
    > internal coordinates to hold fixed
  - `remove_inverse_translation_rotation`: `bool`
    > strip translation/rotation from the
    inverse
  - `opts`: `Any`
    > options forwarded to the conversion function
  - `:returns`: `list | tuple`
    > the forward tensors, or `(forward, inverse)` if `return_inverse`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/internal_coordinate_tensors.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/internal_coordinate_tensors.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/internal_coordinate_tensors.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/internal_coordinate_tensors.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3313?message=Update%20Docs)   
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