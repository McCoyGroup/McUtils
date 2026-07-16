# <a id="McUtils.Numputils.CoordOps.inverse_internal_coordinate_tensors">inverse_internal_coordinate_tensors</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L3491)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3491?message=Update%20Docs)]
</div>

```python
inverse_internal_coordinate_tensors(expansion, coords=None, masses=None, order=None, mass_weighted=True, remove_translation_rotation=True, fixed_atoms=None, fixed_coords=None, fixed_cartesians=None): 
```
**LLM Docstring**

Invert a forward internals-by-Cartesians derivative expansion to obtain the
Cartesians-by-internals expansion, optionally removing translation/rotation and
mass-weighting.

Depending on the module flags `_transrot_projection_method` and
`_pre_mass_weight`, the translation/rotation subspace is either projected out
or augmented onto the transformation before the (pseudo)inverse is taken with
`TensorDerivatives.inverse_transformation`; mass weighting is applied and undone
around the inversion. Constraints are re-applied with `prep_inverse_derivatives`.
  - `expansion`: `list[np.ndarray]`
    > the forward derivative expansion
  - `coords`: `np.ndarray | None`
    > Cartesian coordinates (needed to remove translation/rotation)
  - `masses`: `np.ndarray | None`
    > per-atom masses
  - `order`: `int | None`
    > maximum derivative order (defaults to `len(expansion)`)
  - `mass_weighted`: `bool`
    > whether to mass-weight the plain inverse
  - `remove_translation_rotation`: `bool`
    > whether to strip translation/rotation
  - `fixed_atoms`: `Iterable[int] | None`
    > atoms to hold fixed
  - `fixed_coords`: `Iterable[int] | None`
    > internal coordinates to hold fixed
  - `fixed_cartesians`: `Iterable | None`
    > `(atom, component)` Cartesians to hold fixed
  - `:returns`: `list[np.ndarray]`
    > t
h
e
 
i
n
v
e
r
s
e
 
d
e
r
i
v
a
t
i
v
e
 
e
x
p
a
n
s
i
o
n











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/inverse_internal_coordinate_tensors.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/inverse_internal_coordinate_tensors.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/inverse_internal_coordinate_tensors.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/inverse_internal_coordinate_tensors.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3491?message=Update%20Docs)   
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