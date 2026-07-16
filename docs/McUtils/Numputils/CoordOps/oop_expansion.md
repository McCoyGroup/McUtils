# <a id="McUtils.Numputils.CoordOps.oop_expansion">oop_expansion</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L3902)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3902?message=Update%20Docs)]
</div>

```python
oop_expansion(coords, i, j, k, order=1, left_atoms=None, right_atoms=None, *, include_core=True, angle=0, axis_order=0): 
```
**LLM Docstring**

Build the finite-rotation expansion of the coordinates associated with an
out-of-plane bend of the `i`-`j`-`k` group.

The two halves are rotated by opposite half-angles about the averaged
`i`/`k` direction (relative to the vertex `j`), with group ownership resolved by
`_handle_expansion_atom_exclusions` and derivative terms halved.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `i`: `int`
    > first outer atom
  - `j`: `int`
    > vertex atom
  - `k`: `int`
    > second outer atom
  - `order`: `int`
    > maximum expansion order
  - `left_atoms`: `Iterable[int] | None`
    > atoms moving with `i` (defaults to `[i]`)
  - `right_atoms`: `Iterable[int] | None`
    > atoms moving with `k` (defaults to `[k]`)
  - `include_core`: `bool`
    > whether to prepend the core atom to the group lists
  - `angle`: `float`
    > total displacement angle
  - `axis_order`: `int`
    > differentiation order w.r.t. the axis
  - `:returns`: `list[np.ndarray]`
    > t
h
e
 
r
o
t
a
t
i
o
n
 
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
c
o
o
r
d
s
,
 
d
1
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/oop_expansion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/oop_expansion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/oop_expansion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/oop_expansion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3902?message=Update%20Docs)   
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