# <a id="McUtils.Numputils.TransformationMatrices.render_points">render_points</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TransformationMatrices.py#L1219)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1219?message=Update%20Docs)]
</div>

```python
render_points(points, render_matrix, camera_cull_threshold=1e-08, return_w=False): 
```
**LLM Docstring**

Project a set of points through a render matrix into (culled) screen
coordinates.

Points are homogenized, transformed, perspective-divided by their `w` component,
and flagged as in-view when `w` exceeds `camera_cull_threshold`.
  - `points`: `np.ndarray`
    > the points to project
  - `render_matrix`: `np.ndarray`
    > the model-view-projection matrix
  - `camera_cull_threshold`: `float`
    > minimum `w` for a point to be considered in view
  - `return_w`: `bool`
    > also return the homogeneous `w` component
  - `:returns`: `tuple`
    > `
(
p
r
o
j
e
c
t
e
d
_
p
o
i
n
t
s
,
 
i
n
_
v
i
e
w
_
m
a
s
k
)
`
 
(
p
l
u
s
 
`
w
`
 
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TransformationMatrices/render_points.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TransformationMatrices/render_points.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TransformationMatrices/render_points.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TransformationMatrices/render_points.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1219?message=Update%20Docs)   
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