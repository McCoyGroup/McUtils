# <a id="McUtils.Numputils.VectorOps.distance_matrix">distance_matrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L177)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L177?message=Update%20Docs)]
</div>

```python
distance_matrix(pts, axis=-1, axis2=None, return_triu=False, return_indices=False, return_diffs=False): 
```
**LLM Docstring**

Compute the matrix of pairwise distances between a set of points.

Distances are formed from the upper-triangular pairs and scattered into a
symmetric matrix (or returned as the compact upper triangle when `return_triu`).
The pair indices and/or the raw difference vectors can optionally be returned
alongside the distances.
  - `pts`: `np.ndarray`
    > the points, with the coordinate axis given by `axis`
  - `axis`: `int`
    > axis holding each point's Cartesian components
  - `axis2`: `int | None`
    > axis enumerating the points (defaults to `axis - 1`)
  - `return_triu`: `bool`
    > return the compact upper triangle instead of a full matrix
  - `return_indices`: `bool`
    > also return the `(rows, cols)` pair indices
  - `return_diffs`: `bool`
    > also return the difference vectors
  - `:returns`: `np.ndarray | tuple`
    > t
h
e
 
d
i
s
t
a
n
c
e
s
 
(
p
l
u
s
 
i
n
d
i
c
e
s
/
d
i
f
f
s
 
i
f
 
r
e
q
u
e
s
t
e
d
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/distance_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/distance_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/distance_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/distance_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L177?message=Update%20Docs)   
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