## <a id="McUtils.Jupyter.Apps.Interfaces.Dropdown">Dropdown</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L1402)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L1402?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
components: dict
theme: dict
```
<a id="McUtils.Jupyter.Apps.Interfaces.Dropdown.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, header: Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType], Mapping], NoneType, Iterable[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType], Mapping]]]], actions: Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType], Mapping], NoneType, Iterable[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType], Mapping]]]], **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L1411)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L1411?message=Update%20Docs)]
</div>
**LLM Docstring**

A Bootstrap dropdown with a header/toggle and a list of actions.
  - `header`: `Any`
    > the toggle content
  - `actions`: `Any`
    > the dropdown actions
  - `attrs`: `Any`
    > extra attributes


<a id="McUtils.Jupyter.Apps.Interfaces.Dropdown.prep_actions" class="docs-object-method">&nbsp;</a> 
```python
prep_actions(self, actions): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Dropdown.py#L1428)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Dropdown.py#L1428?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize the dropdown actions into item specs.
  - `actions`: `Any`
    > the actions
  - `:returns`: `_`
    > the prepared action items
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/Dropdown.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/Dropdown.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/Dropdown.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/Dropdown.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L1402?message=Update%20Docs)   
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