## <a id="McUtils.Plots.SVG.SVGFigure3D">SVGFigure3D</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG.py#L1247)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG.py#L1247?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
element_mapping: dict
```
<a id="McUtils.Plots.SVG.SVGFigure3D.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, elements=None, defs=None, view_matrix=None, perspective_matrix=None, world_matrix=None, view_position=None, view_center=None, up_vector=None, view_vector=None, right_vector=None, view_angle=None, aspect_ratio=None, view_distance=None, clip_distances=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG.py#L1249)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG.py#L1249?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.get_projection_matrix" class="docs-object-method">&nbsp;</a> 
```python
get_projection_matrix(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1280)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1280?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.get_projection_kwargs" class="docs-object-method">&nbsp;</a> 
```python
get_projection_kwargs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1285)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1285?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.set_projection_kwargs" class="docs-object-method">&nbsp;</a> 
```python
set_projection_kwargs(self, render_matrix=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1287?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.create_element" class="docs-object-method">&nbsp;</a> 
```python
create_element(self, element_type, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1304?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.add_cylinder" class="docs-object-method">&nbsp;</a> 
```python
add_cylinder(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1306)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1306?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.add_sphere" class="docs-object-method">&nbsp;</a> 
```python
add_sphere(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1308)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1308?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.prep_element" class="docs-object-method">&nbsp;</a> 
```python
prep_element(self, e): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1311)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1311?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.compare_primitives" class="docs-object-method">&nbsp;</a> 
```python
compare_primitives(self, e1, e2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1321)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1321?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.sort_draw_els" class="docs-object-method">&nbsp;</a> 
```python
sort_draw_els(self, els): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1359)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1359?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.prep_draw_els" class="docs-object-method">&nbsp;</a> 
```python
prep_draw_els(self, bbox, compute_bbox=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1362)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1362?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.compute_viewbox" class="docs-object-method">&nbsp;</a> 
```python
compute_viewbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1369)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1369?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure3D.to_svg" class="docs-object-method">&nbsp;</a> 
```python
to_svg(self, compute_bbox=None, view_box=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure3D.py#L1391)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure3D.py#L1391?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG.py#L1247?message=Update%20Docs)   
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