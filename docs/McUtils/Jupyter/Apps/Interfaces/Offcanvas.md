## <a id="McUtils.Jupyter.Apps.Interfaces.Offcanvas">Offcanvas</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L2147)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2147?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
wrapper_classes: list
```
<a id="McUtils.Jupyter.Apps.Interfaces.Offcanvas.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, header=None, body=None, id=None, tabindex=-1, cls=None, placement='start', **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L2149)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2149?message=Update%20Docs)]
</div>
**LLM Docstring**

A Bootstrap offcanvas panel (header/body).
  - `args`: `Any`
    > the panel content
  - `attrs`: `Any`
    > extra attributes and per-section options


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Bootstrap.Button" class="docs-object-method">&nbsp;</a> 
```python
trigger_class(*elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML/JHTML/Bootstrap.py#L676)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML/JHTML/Bootstrap.py#L676?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Offcanvas.get_trigger" class="docs-object-method">&nbsp;</a> 
```python
get_trigger(self, *items, trigger_class=None, data_bs_toggle='offcanvas', data_bs_target=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Offcanvas.py#L2183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Offcanvas.py#L2183?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a trigger element that opens the offcanvas panel.
  - `items`: `Any`
    > the trigger content
  - `trigger_class`: `Any`
    > the trigger's CSS class
  - `data_bs_toggle`: `Any`
    > the Bootstrap toggle type
  - `data_bs_target`: `Any`
    > the panel target id
  - `attrs`: `Any`
    > extra attributes
  - `:returns`: `_`
    > the trigger element


<a id="McUtils.Jupyter.Apps.Interfaces.Offcanvas.close_button" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
close_button(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2201)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2201?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an offcanvas close button.
  - `:returns`: `_`
    > the close button
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/Offcanvas.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/Offcanvas.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/Offcanvas.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/Offcanvas.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2147?message=Update%20Docs)   
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