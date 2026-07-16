# <a id="McUtils.Numputils.CoordOps.dist_expansion">dist_expansion</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L3723)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3723?message=Update%20Docs)]
</div>

```python
dist_expansion(coords, i, j, order=1, left_atoms=None, right_atoms=None, *, include_core=True, amount=0): 
```
**LLM Docstring**

Build the finite-displacement expansion of the coordinates associated with
stretching the `i`-`j` bond.

Atoms on the `i` side are displaced by `-vec` and atoms on the `j` side by
`+vec` (half the normalized bond vector), with a first-order term equal to that
unit direction and higher-order terms zero. Group membership (and unaffected
atoms) is resolved by `_handle_expansion_atom_exclusions`.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `i`: `int`
    > tail atom of the bond
  - `j`: `int`
    > head atom of the bond
  - `order`: `int`
    > maximum expansion order
  - `left_atoms`: `Iterable[int] | None`
    > atoms moving with `i` (defaults to `[i]`)
  - `right_atoms`: `Iterable[int] | None`
    > atoms moving with `j` (defaults to `[j]`)
  - `include_core`: `bool`
    > whether to prepend the core atom to the group lists
  - `amount`: `float`
    > displacement magnitude applied to the value term
  - `:returns`: `list[np.ndarray]`
    > the displacement expansion `[coords, d1, ...]`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/dist_expansion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/dist_expansion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/dist_expansion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/dist_expansion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3723?message=Update%20Docs)   
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