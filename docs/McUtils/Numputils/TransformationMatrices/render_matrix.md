# <a id="McUtils.Numputils.TransformationMatrices.render_matrix">render_matrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TransformationMatrices.py#L974)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L974?message=Update%20Docs)]
</div>

```python
render_matrix(view_matrix=None, perspective_matrix=None, world_matrix=None, view_position=None, view_center=None, up_vector=None, view_vector=None, right_vector=None, view_angle=None, aspect_ratio=None, view_distance=None, clip_distances=None, bbox=None, rescale_world_coordinates=False, include_perspective=True): 
```
**LLM Docstring**

Assemble the full model-view-projection render matrix from a flexible set of
camera parameters.

Fills in whichever of the view, world, and perspective matrices are missing
from the supplied vectors/positions/angles (deriving view center, distance, and
direction as needed), then multiplies them together, optionally including the
perspective stage.
  - `view_matrix`: `np.ndarray | None`
    > an explicit view matrix (derived if omitted)
  - `perspective_matrix`: `np.ndarray | None`
    > an explicit perspective matrix (derived if omitted)
  - `world_matrix`: `np.ndarray | None`
    > an explicit world matrix (derived if omitted)
  - `view_position`: `np.ndarray | None`
    > camera position
  - `view_center`: `np.ndarray | None`
    > point the camera looks at
  - `up_vector`: `np.ndarray | None`
    > camera up direction
  - `view_vector`: `np.ndarray | None`
    > camera view/forward direction
  - `right_vector`: `np.ndarray | None`
    > camera right direction
  - `view_angle`: `float | np.ndarray | None`
    > field-of-view angle
  - `aspect_ratio`: `float | np.ndarray | None`
    > viewport aspect ratio
  - `view_distance`: `float | None`
    > camera-to-center distance
  - `clip_distances`: `np.ndarray | None`
    > `(near, far)` clipping distances
  - `bbox`: `tuple | None`
    > world bounding box
  - `rescale_world_coordinates`: `bool`
    > rescale world coordinates into a unit cube
  - `include_perspective`: `bool`
    > include the perspective projection stage
  - `:returns`: `np.ndarray`
    > t
h
e
 
c
o
m
b
i
n
e
d
 
r
e
n
d
e
r
 
m
a
t
r
i
x











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TransformationMatrices/render_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TransformationMatrices/render_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TransformationMatrices/render_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TransformationMatrices/render_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L974?message=Update%20Docs)   
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