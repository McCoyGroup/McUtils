# <a id="McUtils.Numputils.CoordOps.internal_conversion_function">internal_conversion_function</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L3232)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3232?message=Update%20Docs)]
</div>

```python
internal_conversion_function(specs, base_transformation=None, reference_internals=None, use_cache=True, reproject=False, **opts): 
```
**LLM Docstring**

Build a reusable Cartesian-to-internal conversion function from a set of
coordinate specifications.

The specs are normalized once with `internal_conversion_specs`; the returned
`convert` closure evaluates every coordinate's derivative expansion for a given
Cartesian geometry and stitches them together with
`combine_coordinate_deriv_expansions`, optionally applying a base
transformation and reference internals.
  - `specs`: `Iterable`
    > the coordinate specifications
  - `base_transformation`: `list[np.ndarray] | None`
    > optional transformation into a new coordinate basis
  - `reference_internals`: `np.ndarray | None`
    > reference internal values to subtract
  - `use_cache`: `bool`
    > whether to share an expansion cache across coordinates
  - `reproject`: `bool`
    > whether individual coordinate derivatives are reprojected
  - `opts`: `Any`
    > options forwarded to `internal_conversion_specs`
  - `:returns`: `Callable`
    > a
 
`
c
o
n
v
e
r
t
(
c
o
o
r
d
s
,
 
o
r
d
e
r
=
N
o
n
e
)
`
 
f
u
n
c
t
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/internal_conversion_function.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/internal_conversion_function.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/internal_conversion_function.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/internal_conversion_function.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L3232?message=Update%20Docs)   
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