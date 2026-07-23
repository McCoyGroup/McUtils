## <a id="McUtils.Plots.X3DInterface.X3DInterpolatingAnimator">X3DInterpolatingAnimator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface.py#L2934)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L2934?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Plots.X3DInterface.X3DInterpolatingAnimator.get_animation_objects" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_animation_objects(cls, object_attr_sets: 'dict[X3DObject, dict]', id): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2935)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2935?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an interpolating animation from a mapping of objects to their per-property
frame values, validating a consistent frame count and resolving each property's
target node.
  - `object_attr_sets`: `dict`
    > the `{object: {property: per_frame_values}}` mapping
  - `id`: `Any`
    > the animator id
  - `:returns`: `tuple`
    > `(objects, attribute_sets, nframes)`


<a id="McUtils.Plots.X3DInterface.X3DInterpolatingAnimator.frame_diffs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
frame_diffs(cls, ref: 'X3DObject | X3DHTML.X3DElement', test: 'X3DObject | X3DHTML.X3DElement', *rest: 'X3DObject | X3DHTML.X3DElement'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2976)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2976?message=Update%20Docs)]
</div>
**LLM Docstring**

Walk several X3D object trees in parallel and find which nodes/attributes differ
across frames, separating the static nodes from the per-node attribute changes.
  - `ref`: `Any`
    > the reference (first-frame) tree
  - `test`: `Any`
    > the second-frame tree
  - `rest`: `Any`
    > the remaining frames' trees
  - `:returns`: `tuple`
    > `(static_nodes, {node: per_frame_attribute_values})`


<a id="McUtils.Plots.X3DInterface.X3DInterpolatingAnimator.from_frames" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_frames(cls, frames: 'list[X3DObject | X3DHTML.X3DElement]', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3060)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3060?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an interpolating animation from a list of frame trees by diffing them:
static content is kept as-is and only the changing attributes are animated.
  - `frames`: `list`
    > the per-frame object trees
  - `opts`: `Any`
    > options for the animator
  - `:returns`: `_`
    > the animation (or the single frame if nothing changes)
 </div>
</div>












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/X3DInterface/X3DInterpolatingAnimator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/X3DInterface/X3DInterpolatingAnimator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/X3DInterface/X3DInterpolatingAnimator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/X3DInterface/X3DInterpolatingAnimator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L2934?message=Update%20Docs)   
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