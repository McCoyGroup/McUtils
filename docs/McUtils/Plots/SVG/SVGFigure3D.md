## <a id="McUtils.Plots.SVG.SVGFigure3D">SVGFigure3D</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG.py#L1419)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG.py#L1419?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
interactive_runtime_template: str
element_mapping: dict
```
<a id="McUtils.Plots.SVG.SVGFigure3D.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, elements=None, defs=None, view_matrix=None, perspective_matrix=None, world_matrix=None, view_position=None, view_center=None, up_vector=None, view_vector=None, right_vector=None, view_angle=None, aspect_ratio=None, view_distance=None, view_scale=None, clip_distances=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG.py#L1657)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG.py#L1657?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.get_projection_matrix" class="docs-object-method">&nbsp;</a> 
```python
get_projection_matrix(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1692)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1692?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.get_projection_kwargs" class="docs-object-method">&nbsp;</a> 
```python
get_projection_kwargs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1697)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1697?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.set_projection_kwargs" class="docs-object-method">&nbsp;</a> 
```python
set_projection_kwargs(self, render_matrix=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1702)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1702?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.scale_view_box" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
scale_view_box(view_box, view_scale): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1713)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1713?message=Update%20Docs)]
</div>
Expand a 2D view box about its center without changing the canvas.


<a id="McUtils.Plots.SVG.SVGFigure3D.create_element" class="docs-object-method">&nbsp;</a> 
```python
create_element(self, element_type, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1740)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1740?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.add_cylinder" class="docs-object-method">&nbsp;</a> 
```python
add_cylinder(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1742)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1742?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.add_sphere" class="docs-object-method">&nbsp;</a> 
```python
add_sphere(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1744)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1744?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.prep_element" class="docs-object-method">&nbsp;</a> 
```python
prep_element(self, e): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1747)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1747?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.compare_primitives" class="docs-object-method">&nbsp;</a> 
```python
compare_primitives(self, e1, e2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1762)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1762?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.sort_draw_els" class="docs-object-method">&nbsp;</a> 
```python
sort_draw_els(self, els): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1800)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1800?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.prep_draw_els" class="docs-object-method">&nbsp;</a> 
```python
prep_draw_els(self, bbox, compute_bbox=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1803)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1803?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.compute_viewbox" class="docs-object-method">&nbsp;</a> 
```python
compute_viewbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1810)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1810?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.get_interactive_runtime" class="docs-object-method">&nbsp;</a> 
```python
get_interactive_runtime(self, scene, renderers): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1866)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1866?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.write_interactive_runtime" class="docs-object-method">&nbsp;</a> 
```python
write_interactive_runtime(self, file, scene, renderers): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1881)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1881?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.to_svg" class="docs-object-method">&nbsp;</a> 
```python
to_svg(self, compute_bbox=None, view_box=None, *, interactive=False, dynamic_loading=False, runtime_file=None, runtime_src=None, rotation_sensitivity=0.01, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1885)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1885?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/SVG/SVGFigure3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/SVG/SVGFigure3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/SVG/SVGFigure3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/SVG/SVGFigure3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG.py#L1419?message=Update%20Docs)   
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