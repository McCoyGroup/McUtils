## <a id="McUtils.Plots.Primitives.Text">Text</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives.py#L154?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Plots.Primitives.Text.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, txt, pos, bbox=((1, 1), (1, 1)), **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives.py#L155)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives.py#L155?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a `Text` primitive.
  - `txt`: `Any`
    > the text string
  - `pos`: `Any`
    > the text position
  - `bbox`: `Any`
    > the per-side padding box around the text
  - `opts`: `Any`
    > extra styling options


<a id="McUtils.Plots.Primitives.Text.get_bbox" class="docs-object-method">&nbsp;</a> 
```python
get_bbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives/Text.py#L170)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives/Text.py#L170?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the primitive's bounding box (the padded box around the text).
  - `:returns`: `list`
    > the `[(min_x, min_y), (max_x, max_y)]` bounding box


<a id="McUtils.Plots.Primitives.Text.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, axes, *args, graphics=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Primitives/Text.py#L183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives/Text.py#L183?message=Update%20Docs)]
</div>
**LLM Docstring**

Draw the primitive onto the axes via `axes.draw_text`.
  - `axes`: `Any`
    > the axes (or graphics) to draw onto
  - `args`: `Any`
    > extra positional arguments
  - `graphics`: `Any`
    > the owning graphics object
  - `kwargs`: `Any`
    > extra styling options
  - `:returns`: `_`
    > the drawn backend object
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Primitives/Text.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Primitives/Text.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Primitives/Text.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Primitives/Text.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Primitives.py#L154?message=Update%20Docs)   
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