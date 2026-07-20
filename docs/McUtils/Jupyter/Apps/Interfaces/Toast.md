## <a id="McUtils.Jupyter.Apps.Interfaces.Toast">Toast</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L2300)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2300?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
wrappers: dict
theme: dict
```
<a id="McUtils.Jupyter.Apps.Interfaces.Toast.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, header=None, body=None, role='alert', hidden=True, cls=None, id=None, javascript_handles=None, onevents=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L2307)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2307?message=Update%20Docs)]
</div>
**LLM Docstring**

A Bootstrap toast notification (header/body).
  - `args`: `Any`
    > the toast content
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


<a id="McUtils.Jupyter.Apps.Interfaces.Toast.get_trigger" class="docs-object-method">&nbsp;</a> 
```python
get_trigger(self, *items, trigger_class=None, data_bs_toggle='toast', data_bs_target=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Toast.py#L2349)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Toast.py#L2349?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a trigger element that shows the toast.
  - `items`: `Any`
    > the trigger content
  - `trigger_class`: `Any`
    > the trigger's CSS class
  - `data_bs_toggle`: `Any`
    > the Bootstrap toggle type
  - `data_bs_target`: `Any`
    > the toast target id
  - `attrs`: `Any`
    > extra attributes
  - `:returns`: `_`
    > the trigger element


<a id="McUtils.Jupyter.Apps.Interfaces.Toast.close_button" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
close_button(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2373)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2373?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a toast close button.
  - `:returns`: `_`
    > the close button


<a id="McUtils.Jupyter.Apps.Interfaces.Toast.show" class="docs-object-method">&nbsp;</a> 
```python
show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Toast.py#L2383)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Toast.py#L2383?message=Update%20Docs)]
</div>
**LLM Docstring**

Show the toast.


<a id="McUtils.Jupyter.Apps.Interfaces.Toast.hide" class="docs-object-method">&nbsp;</a> 
```python
hide(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Toast.py#L2391)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Toast.py#L2391?message=Update%20Docs)]
</div>
**LLM Docstring**

Hide the toast.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/Toast.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/Toast.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/Toast.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/Toast.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2300?message=Update%20Docs)   
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