## <a id="McUtils.Jupyter.APIs.d3_backend.FigureCanvasD3">FigureCanvasD3</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend.py#L837)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend.py#L837?message=Update%20Docs)]
</div>

The canvas the figure renders into.  Calls the draw and print fig
methods, creates the renderers, etc.

Note: GUI templates will want to connect events for button presses,
mouse movements and key presses to functions that call the base
class methods button_press_event, button_release_event,
motion_notify_event, key_press_event, and key_release_event.  See the
implementations of the interactive backends for examples.

Attributes
----------
figure : `~matplotlib.figure.Figure`
A high-level Figure instance







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
manager_class: FigureManagerD3
```
<a id="McUtils.Jupyter.APIs.d3_backend.FigureCanvasD3.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, figure=None, manager=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/FigureCanvasD3.py#L859)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/FigureCanvasD3.py#L859?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.APIs.d3_backend.FigureCanvasD3.draw" class="docs-object-method">&nbsp;</a> 
```python
draw(self, clear=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/APIs/d3_backend/FigureCanvasD3.py#L864)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend/FigureCanvasD3.py#L864?message=Update%20Docs)]
</div>
Draw the figure using the renderer.

It is important that this method actually walk the artist tree
even if not output is produced because this will trigger
deferred work (like computing limits auto-limits and tick
values) that users may want access to before saving to disk.


<a id="McUtils.Jupyter.APIs.d3_backend.FigureCanvasD3.render_objects" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
render_objects(cls, figure, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L882)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L882?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/APIs/d3_backend/FigureCanvasD3.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/APIs/d3_backend/FigureCanvasD3.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/APIs/d3_backend/FigureCanvasD3.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/APIs/d3_backend/FigureCanvasD3.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/APIs/d3_backend.py#L837?message=Update%20Docs)   
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