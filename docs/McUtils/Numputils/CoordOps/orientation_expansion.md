# <a id="McUtils.Numputils.CoordOps.orientation_expansion">orientation_expansion</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L4127)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L4127?message=Update%20Docs)]
</div>

```python
orientation_expansion(coords, frame_pos_1, frame_pos_2, *, order=1, masses=None, fixed_atoms=None, cache=None, reproject=True, return_frame=False, left_extra_atoms=None, right_extra_atoms=None, shift=None, rotation=None, return_rot=True): 
```
**LLM Docstring**

Build the finite-displacement expansion of the relative orientation coordinate
between two atom fragments.

Each fragment is expanded with `transrot_expansion` in the shared axis system
from `_orientation_axis_system`, with the applied `shift`/`rotation` split
between the fragments by the mass-weighted coefficients `p1` and `p2`. The two
expansions are combined through `_handle_expansion_atom_exclusions`. (The long
commented block preserves an earlier explicit-construction approach.)
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `frame_pos_1`: `Iterable[int]`
    > atom indices of the first fragment
  - `frame_pos_2`: `Iterable[int]`
    > atom indices of the second fragment
  - `order`: `int`
    > maximum expansion order
  - `masses`: `np.ndarray | None`
    > per-atom masses (defaults to unit masses)
  - `fixed_atoms`: `Iterable[int] | None`
    > atoms to hold fixed
  - `cache`: `dict | None`
    > expansion cache (interface parity)
  - `reproject`: `bool`
    > interface parity
  - `return_frame`: `bool`
    > whether to also return the frame
  - `left_extra_atoms`: `Iterable[int] | None`
    > extra atoms carried with the first fragment
  - `right_extra_atoms`: `Iterable[int] | None`
    > extra atoms carried with the second fragment
  - `shift`: `np.ndarray | None`
    > relative translation to apply
  - `rotation`: `np.ndarray | None`
    > relative rotation to apply
  - `return_rot`: `bool`
    > whether to include rotational modes
  - `:returns`: `list[np.ndarray]`
    > t
h
e
 
o
r
i
e
n
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/orientation_expansion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/orientation_expansion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/orientation_expansion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/orientation_expansion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L4127?message=Update%20Docs)   
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