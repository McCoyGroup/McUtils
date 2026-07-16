# <a id="McUtils.Numputils.CoordOps.orientation_vecs">orientation_vecs</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L3038)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3038?message=Update%20Docs)]
</div>

```python
orientation_vecs(coords, frame_pos_1, frame_pos_2, *, order=None, masses=None, cache=None, reproject=True, fixed_atoms=None, return_rot=True): 
```
**LLM Docstring**

Convenience wrapper returning the orientation-coordinate derivative(s) as bare
vectors.

Calls `orientation_deriv`; when `order is None` returns only the
first-derivative term, otherwise the full expansion.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `frame_pos_1`: `Iterable[int]`
    > atom indices of the first fragment
  - `frame_pos_2`: `Iterable[int]`
    > atom indices of the second fragment
  - `order`: `int | None`
    > derivative order (`None` returns only the first derivative)
  - `masses`: `np.ndarray | None`
    > per-atom masses
  - `cache`: `dict | None`
    > expansion cache (interface parity)
  - `reproject`: `bool`
    > interface parity
  - `fixed_atoms`: `Iterable[int] | None`
    > atoms whose contributions should be zeroed
  - `return_rot`: `bool`
    > whether to include rotational modes
  - `:returns`: `np.ndarray | list`
    > the orientation derivative vector(s)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/orientation_vecs.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/orientation_vecs.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/orientation_vecs.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/orientation_vecs.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3038?message=Update%20Docs)   
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