# <a id="McUtils.Numputils.CoordOps.transrot_vecs">transrot_vecs</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L3001)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3001?message=Update%20Docs)]
</div>

```python
transrot_vecs(coords, *pos, order=None, masses=None, return_rot=True, cache=None, reproject=True, fixed_atoms=None): 
```
**LLM Docstring**

Convenience wrapper returning the translation/rotation derivative(s) as bare
vectors.

Calls `transrot_deriv`; when `order is None` returns only the first-derivative
term, otherwise the full expansion.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `pos`: `int`
    > atom indices defining the fragment (empty = all atoms)
  - `order`: `int | None`
    > derivative order (`None` returns only the first derivative)
  - `masses`: `np.ndarray | None`
    > per-atom masses
  - `return_rot`: `bool`
    > whether to include rotational modes
  - `cache`: `dict | None`
    > expansion cache (interface parity)
  - `reproject`: `bool`
    > interface parity
  - `fixed_atoms`: `Iterable[int] | None`
    > atoms whose contributions should be zeroed
  - `:returns`: `np.ndarray | list`
    > t
h
e
 
t
r
a
n
s
l
a
t
i
o
n
/
r
o
t
a
t
i
o
n
 
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
 
v
e
c
t
o
r
(
s
)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/transrot_vecs.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/transrot_vecs.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/transrot_vecs.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/transrot_vecs.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3001?message=Update%20Docs)   
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