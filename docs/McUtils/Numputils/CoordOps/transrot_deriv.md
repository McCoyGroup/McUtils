# <a id="McUtils.Numputils.CoordOps.transrot_deriv">transrot_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L2209)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L2209?message=Update%20Docs)]
</div>

```python
transrot_deriv(coords, *pos, order=1, masses=None, return_rot=True, return_frame=False, cache=None, reproject=True, axes=None, fixed_atoms=None): 
```
**LLM Docstring**

Derivative expansion of the translation (center of mass) and, optionally,
rotation degrees of freedom of a (sub)set of atoms with respect to the
Cartesian coordinates.

The center of mass and the translation/rotation eigenvectors are obtained from
`CoordinateFrames.translation_rotation_eigenvectors`. When atom positions `pos`
are supplied only those atoms contribute; their eigenvectors are scattered back
into the full `3N` coordinate space and rows for `fixed_atoms` are zeroed.
Higher-order terms are exact zeros for these (linear) coordinates.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `pos`: `int`
    > atom indices defining the fragment (empty = all atoms)
  - `order`: `int`
    > maximum derivative order
  - `masses`: `np.ndarray | None`
    > per-atom masses (defaults to unit masses)
  - `return_rot`: `bool`
    > whether to include the rotational modes
  - `return_frame`: `bool`
    > whether to also return the principal-axis frame
  - `cache`: `dict | None`
    > expansion cache (unused here, kept for interface parity)
  - `reproject`: `bool`
    > kept for interface parity
  - `axes`: `np.ndarray | None`
    > optional fixed principal axes to use
  - `fixed_atoms`: `Iterable[int] | None`
    > atoms whose contributions should be zeroed
  - `:returns`: `list | tuple`
    > t
h
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
,
 
o
r
 
`
(
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
 
p
r
i
n
c
i
p
a
l
_
a
x
e
s
)
`
 
i
f
 
`
r
e
t
u
r
n
_
f
r
a
m
e
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/transrot_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/transrot_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/transrot_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/transrot_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L2209?message=Update%20Docs)   
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