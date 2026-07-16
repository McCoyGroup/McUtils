# <a id="McUtils.Numputils.CoordOps.angle_basis">angle_basis</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L4982)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L4982?message=Update%20Docs)]
</div>

```python
angle_basis(coords, i, j, k, angle_ordering='ijk', **opts): 
```
**LLM Docstring**

Return the projection data for a bend coordinate on atoms `i`, `j`, `k`.

Honors the `angle_ordering` convention (swapping `i`/`j` for `'jik'`), builds
the fixed basis with `fixed_angle_basis`, and passes it through
`coordinate_projection_data`.
  - `coords`: `np.ndarray`
    > Cartesian coordinates, shape `(..., N, 3)`
  - `i`: `int`
    > first atom (interpretation depends on `angle_ordering`)
  - `j`: `int`
    > second atom
  - `k`: `int`
    > third atom
  - `angle_ordering`: `str`
    > angle-index ordering (`'ijk'` or `'jik'`)
  - `opts`: `Any`
    > options forwarded to `coordinate_projection_data`
  - `:returns`: `tuple`
    > `
(
b
a
s
i
s
,
 
c
o
m
p
l
e
m
e
n
t
a
r
y
_
b
a
s
i
s
,
 
s
e
l
e
c
t
i
o
n
_
m
a
t
r
i
x
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/angle_basis.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/angle_basis.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/angle_basis.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/angle_basis.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L4982?message=Update%20Docs)   
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