## <a id="McUtils.Jupyter.Apps.Interfaces.Progress">Progress</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L1272)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L1272?message=Update%20Docs)]
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
<a id="McUtils.Jupyter.Apps.Interfaces.Progress.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, value=0, label=None, wrappers=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L1275)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L1275?message=Update%20Docs)]
</div>
**LLM Docstring**

A Bootstrap progress bar.
  - `value`: `Any`
    > the initial percentage
  - `label`: `Any`
    > the bar label
  - `wrappers`: `Any`
    > the wrapper element classes
  - `attrs`: `Any`
    > extra attributes


<a id="McUtils.Jupyter.Apps.Interfaces.Progress.container" class="docs-object-method">&nbsp;</a> 
```python
@property
container(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Progress.py#L1304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Progress.py#L1304?message=Update%20Docs)]
</div>
**LLM Docstring**

The progress bar's outer container element.
  - `:returns`: `_`
    > the container


<a id="McUtils.Jupyter.Apps.Interfaces.Progress.bar" class="docs-object-method">&nbsp;</a> 
```python
@property
bar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Progress.py#L1314)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Progress.py#L1314?message=Update%20Docs)]
</div>
**LLM Docstring**

The progress bar's inner (filled) element.
  - `:returns`: `_`
    > the bar


<a id="McUtils.Jupyter.Apps.Interfaces.Progress.update_widget_attr" class="docs-object-method">&nbsp;</a> 
```python
update_widget_attr(self, attr, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Progress.py#L1324)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Progress.py#L1324?message=Update%20Docs)]
</div>
**LLM Docstring**

Push an attribute change into the bar's live widget.
  - `attr`: `Any`
    > the attribute name
  - `val`: `Any`
    > the value
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/Progress.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/Progress.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/Progress.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/Progress.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L1272?message=Update%20Docs)   
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