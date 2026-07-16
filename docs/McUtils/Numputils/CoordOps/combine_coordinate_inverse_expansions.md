# <a id="McUtils.Numputils.CoordOps.combine_coordinate_inverse_expansions">combine_coordinate_inverse_expansions</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L4352)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L4352?message=Update%20Docs)]
</div>

```python
combine_coordinate_inverse_expansions(expansions, order=None, base_dim=None, base_transformation=None): 
```
**LLM Docstring**

Concatenate the per-coordinate *inverse* (Cartesians-by-internals) expansions
into one stacked inverse expansion.

Each sub-expansion's tensors are expanded along new leading internal-coordinate
axes and concatenated with `TensorDerivatives.concatenate_expansions`. An
optional `base_transformation` re-expresses the result via
`TensorDerivatives.tensor_reexpand`. When `order is None` only the first-order
block is returned; otherwise the coordinate values are prepended.
  - `expansions`: `list`
    > per-coordinate inverse expansions
  - `order`: `int | None`
    > maximum derivative order (`None` = first order only)
  - `base_dim`: `int | None`
    > number of leading dimensions (inferred if omitted)
  - `base_transformation`: `list[np.ndarray] | None`
    > optional transformation to apply
  - `:returns`: `list`
    > t
h
e
 
c
o
m
b
i
n
e
d
 
i
n
v
e
r
s
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/combine_coordinate_inverse_expansions.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/combine_coordinate_inverse_expansions.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/combine_coordinate_inverse_expansions.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/combine_coordinate_inverse_expansions.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L4352?message=Update%20Docs)   
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