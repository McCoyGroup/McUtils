# <a id="McUtils.Numputils.TransformationMatrices.perspective_matrix">perspective_matrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TransformationMatrices.py#L831)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L831?message=Update%20Docs)]
</div>

```python
perspective_matrix(view_angle=None, aspect=None, near=None, far=None, view_distance=None): 
```
**LLM Docstring**

Build a 4x4 perspective-projection matrix from view-frustum parameters.

The near/far planes are inferred from whichever of `near`, `far`, and
`view_distance` are supplied; the focal terms are then assembled into the
standard perspective matrix.
  - `view_angle`: `float | np.ndarray | None`
    > the field-of-view angle
  - `aspect`: `float | np.ndarray | None`
    > the aspect ratio
  - `near`: `float | None`
    > near clipping distance
  - `far`: `float | None`
    > far clipping distance
  - `view_distance`: `float | None`
    > distance from camera to the view center
  - `:returns`: `np.ndarray`
    > t
h
e
 
p
e
r
s
p
e
c
t
i
v
e
-
p
r
o
j
e
c
t
i
o
n
 
m
a
t
r
i
x
 
(
o
r
 
s
t
a
c
k
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TransformationMatrices/perspective_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TransformationMatrices/perspective_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TransformationMatrices/perspective_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TransformationMatrices/perspective_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L831?message=Update%20Docs)   
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