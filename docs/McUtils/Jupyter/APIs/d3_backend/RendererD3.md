## <a id="McUtils.Jupyter.APIs.d3_backend.RendererD3">RendererD3</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend.py#L21)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend.py#L21?message=Update%20Docs)]
</div>

A modification of the base matplotlib SVG renderer to plug into the D3 library work we've done







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, width, height, basename=None, image_dpi=72, *, metadata=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L47?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.write_defs" class="docs-object-method">&nbsp;</a> 
```python
write_defs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L83)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L83?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.option_image_nocomposite" class="docs-object-method">&nbsp;</a> 
```python
option_image_nocomposite(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L235)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L235?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.draw_path" class="docs-object-method">&nbsp;</a> 
```python
draw_path(self, gc, path, transform, rgbFace=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L248)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L248?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.draw_markers" class="docs-object-method">&nbsp;</a> 
```python
draw_markers(self, gc, marker_path, marker_trans, path, trans, rgbFace=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L269)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L269?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.draw_path_collection" class="docs-object-method">&nbsp;</a> 
```python
draw_path_collection(self, gc, master_transform, paths, all_transforms, offsets, offset_trans, facecolors, edgecolors, linewidths, linestyles, antialiaseds, urls, offset_position): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L301)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L301?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.option_scale_image" class="docs-object-method">&nbsp;</a> 
```python
option_scale_image(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L355)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L355?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.get_image_magnification" class="docs-object-method">&nbsp;</a> 
```python
get_image_magnification(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L359)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L359?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.draw_image" class="docs-object-method">&nbsp;</a> 
```python
draw_image(self, gc, x, y, im, transform=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L362)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L362?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.draw_text" class="docs-object-method">&nbsp;</a> 
```python
draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L697)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L697?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.flipy" class="docs-object-method">&nbsp;</a> 
```python
flipy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L716)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L716?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.get_canvas_width_height" class="docs-object-method">&nbsp;</a> 
```python
get_canvas_width_height(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L720)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L720?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.get_text_width_height_descent" class="docs-object-method">&nbsp;</a> 
```python
get_text_width_height_descent(self, s, prop, ismath): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L724)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L724?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.RendererD3.insert_d3" class="docs-object-method">&nbsp;</a> 
```python
insert_d3(self, root: 'D3.Frame'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/RendererD3.py#L728)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/RendererD3.py#L728?message=Update%20Docs)]
</div>
width='%spt' % str_width,
height='%spt' % str_height,
viewBox='0 0 %s %s' % (str_width, str_height),
xmlns="http://www.w3.org/2000/svg",
version="1.1",
attrib={'xmlns:xlink': "http://www.w3.org/1999/xlink"}
  - `root`: `Any`
    > 
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Jupyter/APIs/d3_backend/RendererD3.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Jupyter/APIs/d3_backend/RendererD3.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Jupyter/APIs/d3_backend/RendererD3.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Jupyter/APIs/d3_backend/RendererD3.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend.py#L21?message=Update%20Docs)   
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