# <a id="McUtils.Numputils.CoordOps.transrot_expansion">transrot_expansion</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L4016)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L4016?message=Update%20Docs)]
</div>

```python
transrot_expansion(coords, *pos, order=1, shift=None, rotation=None, masses=None, axes=None, extra_atoms=None, return_rot=True, return_frame=False): 
```
**LLM Docstring**

Build the finite-displacement expansion of the coordinates associated with
translating and/or rotating an atom fragment as a rigid body.

The fragment (`pos` plus any `extra_atoms`) is optionally shifted along, and
rotated about, its principal axes, then the mass-weighted translation/rotation
eigenvectors from `CoordinateFrames.translation_rotation_eigenvectors` are
scattered into the full `3N` coordinate space to form the first-order term.
Higher-order terms are zero.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `pos`: `int`
    > atom indices defining the fragment (empty = all atoms)
  - `order`: `int`
    > maximum expansion order
  - `shift`: `np.ndarray | None`
    > translation applied in the principal-axis frame
  - `rotation`: `np.ndarray | None`
    > per-axis rotation angles
  - `masses`: `np.ndarray | None`
    > per-atom masses (defaults to unit masses)
  - `axes`: `np.ndarray | None`
    > optional fixed principal axes
  - `extra_atoms`: `Iterable[int] | None`
    > additional atoms carried with the fragment
  - `return_rot`: `bool`
    > whether to include rotational modes
  - `return_frame`: `bool`
    > whether to also return the frame
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
 
f
r
a
m
e
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/transrot_expansion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/transrot_expansion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/transrot_expansion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/transrot_expansion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L4016?message=Update%20Docs)   
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