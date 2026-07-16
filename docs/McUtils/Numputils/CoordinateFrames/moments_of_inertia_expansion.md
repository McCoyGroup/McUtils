# <a id="McUtils.Numputils.CoordinateFrames.moments_of_inertia_expansion">moments_of_inertia_expansion</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordinateFrames.py#L239)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L239?message=Update%20Docs)]
</div>

```python
moments_of_inertia_expansion(coords, masses=None, order=1, force_rotation=True, mass_weighted=True): 
```
**LLM Docstring**

Compute the derivative expansion of the moments of inertia (eigenvalues) and
principal axes (eigenvectors) with respect to the Cartesian coordinates.

The inertia tensor and its derivatives (from `inertial_frame_derivatives`) form
an expansion that is fed, together with the base eigenvalues/eigenvectors, to
`TensorDerivatives.mateigh_deriv`; the eigenvalue derivatives are read off the
diagonal of the resulting tensors.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `masses`: `np.ndarray | None`
    > per-atom masses
  - `order`: `int`
    > maximum derivative order
  - `force_rotation`: `bool`
    > force a proper-rotation (right-handed) axis convention
  - `mass_weighted`: `bool`
    > whether the expansion is mass-weighted
  - `:returns`: `tuple[list, list]`
    > `
(
e
i
g
e
n
v
a
l
u
e
_
e
x
p
a
n
s
i
o
n
,
 
e
i
g
e
n
v
e
c
t
o
r
_
e
x
p
a
n
s
i
o
n
)
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordinateFrames/moments_of_inertia_expansion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordinateFrames/moments_of_inertia_expansion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordinateFrames/moments_of_inertia_expansion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordinateFrames/moments_of_inertia_expansion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L239?message=Update%20Docs)   
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