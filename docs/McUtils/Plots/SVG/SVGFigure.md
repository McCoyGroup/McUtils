## <a id="McUtils.Plots.SVG.SVGFigure">SVGFigure</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG.py#L731)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG.py#L731?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
Circle: SVGCircle
Line: SVGLine
Ellipse: SVGEllipse
Rect: SVGRect
Polygon: SVGPolygon
Polyline: SVGPolyline
Path: SVGPath
element_mapping: dict
```
<a id="McUtils.Plots.SVG.SVGFigure.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, elements=None, defs=None, view_box=None, preserve_aspect_ratio=None, **svg_kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG.py#L747)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG.py#L747?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.create_element" class="docs-object-method">&nbsp;</a> 
```python
create_element(self, element_type, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L767)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L767?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.add_element" class="docs-object-method">&nbsp;</a> 
```python
add_element(self, element_type, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L769)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L769?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.add_rect" class="docs-object-method">&nbsp;</a> 
```python
add_rect(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L773)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L773?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.add_circle" class="docs-object-method">&nbsp;</a> 
```python
add_circle(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L775)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L775?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.add_ellipse" class="docs-object-method">&nbsp;</a> 
```python
add_ellipse(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L777)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L777?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.add_line" class="docs-object-method">&nbsp;</a> 
```python
add_line(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L779)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L779?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.add_polyline" class="docs-object-method">&nbsp;</a> 
```python
add_polyline(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L781)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L781?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.add_polygon" class="docs-object-method">&nbsp;</a> 
```python
add_polygon(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L783)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L783?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.add_path" class="docs-object-method">&nbsp;</a> 
```python
add_path(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L785)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L785?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.add_text" class="docs-object-method">&nbsp;</a> 
```python
add_text(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L787)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L787?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.compute_viewbox" class="docs-object-method">&nbsp;</a> 
```python
compute_viewbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L790)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L790?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.add_def" class="docs-object-method">&nbsp;</a> 
```python
add_def(self, id, *, tag, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L807)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L807?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.create_def" class="docs-object-method">&nbsp;</a> 
```python
create_def(self, *, id, tag='marker', body=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L809)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L809?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.prep_element" class="docs-object-method">&nbsp;</a> 
```python
prep_element(self, e): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L819)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L819?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.prep_draw_els" class="docs-object-method">&nbsp;</a> 
```python
prep_draw_els(self, bbox, compute_bbox=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L821)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L821?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.SVG.SVGFigure.to_svg" class="docs-object-method">&nbsp;</a> 
```python
to_svg(self, compute_bbox=None, view_box=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/SVG/SVGFigure.py#L840)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG/SVGFigure.py#L840?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/SVG/SVGFigure.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/SVG/SVGFigure.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/SVG/SVGFigure.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/SVG/SVGFigure.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/SVG.py#L731?message=Update%20Docs)   
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