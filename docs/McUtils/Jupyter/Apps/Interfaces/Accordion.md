## <a id="McUtils.Jupyter.Apps.Interfaces.Accordion">Accordion</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L1820)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L1820?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
wrapper_classes: list
item_classes: list
header_classes: list
```
<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Div" class="docs-object-method">&nbsp;</a> 
```python
item(*elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L304?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Accordion.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, items, base_name=None, header_classes=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L1825)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L1825?message=Update%20Docs)]
</div>
**LLM Docstring**

A Bootstrap accordion of collapsible items.
  - `items`: `Any`
    > the `{label: content}` items
  - `base_name`: `Any`
    > the accordion id prefix
  - `header_classes`: `Any`
    > extra header CSS classes
  - `attrs`: `Any`
    > extra attributes


<a id="McUtils.Jupyter.Apps.Interfaces.Accordion.create_item" class="docs-object-method">&nbsp;</a> 
```python
create_item(self, item, cls=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Accordion.py#L1845)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Accordion.py#L1845?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an accordion item (header plus collapsible body).
  - `item`: `Any`
    > the item spec
  - `cls`: `Any`
    > extra CSS classes
  - `kw`: `Any`
    > extra options
  - `:returns`: `_`
    > the item element
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/Accordion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/Accordion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/Accordion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/Accordion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L1820?message=Update%20Docs)   
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