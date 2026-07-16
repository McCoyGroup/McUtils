# <a id="McUtils.Numputils.CoordOps.combine_coordinate_deriv_expansions">combine_coordinate_deriv_expansions</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L3153)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3153?message=Update%20Docs)]
</div>

```python
combine_coordinate_deriv_expansions(expansions, order=None, base_dim=0, base_transformation=None, reference_internals=None): 
```
**LLM Docstring**

Concatenate the per-coordinate derivative expansions into a single stacked
expansion for the full internal-coordinate set.

Each coordinate's tensors are expanded along a new trailing coordinate axis and
concatenated. When an `order` is given the value term and derivative terms are
handled separately: reference internals are subtracted, and an optional
`base_transformation` is applied (via `TensorDerivatives.tensor_reexpand`) to
re-express the coordinates and their derivatives in a new basis.
  - `expansions`: `list`
    > per-coordinate expansions to combine
  - `order`: `int | None`
    > maximum derivative order (`None` = values only)
  - `base_dim`: `int`
    > number of leading (structure/batch) dimensions
  - `base_transformation`: `list[np.ndarray] | None`
    > optional transformation into a new coordinate basis
  - `reference_internals`: `np.ndarray | None`
    > reference values subtracted from the internals
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
 
e
x
p
a
n
s
i
o
n
 
`
[
i
n
t
e
r
n
a
l
s
,
 
d
1
,
 
d
2
,
 
.
.
.
]
`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/combine_coordinate_deriv_expansions.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/combine_coordinate_deriv_expansions.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/combine_coordinate_deriv_expansions.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/combine_coordinate_deriv_expansions.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3153?message=Update%20Docs)   
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