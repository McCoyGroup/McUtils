## <a id="McUtils.Jupyter.Apps.Interfaces.Layout">Layout</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L2787)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2787?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
Item: LayoutItem
```
<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Div" class="docs-object-method">&nbsp;</a> 
```python
wrapper(*elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L304?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Layout.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, elements, wrapper=None, item_attrs=None, style=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L2790)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2790?message=Update%20Docs)]
</div>
**LLM Docstring**

A container that arranges its elements via CSS layout styles.
  - `elements`: `Any`
    > the elements to arrange
  - `wrapper`: `Any`
    > the wrapper element class
  - `item_attrs`: `dict | None`
    > default per-item attributes
  - `style`: `Any`
    > extra container styles
  - `attrs`: `Any`
    > extra attributes


<a id="McUtils.Jupyter.Apps.Interfaces.Layout.wrap_item" class="docs-object-method">&nbsp;</a> 
```python
wrap_item(self, e, attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Layout.py#L2812)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Layout.py#L2812?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap an element as a layout `Item`.
  - `e`: `Any`
    > the element
  - `attrs`: `Any`
    > the item attributes
  - `:returns`: `_`
    > the layout item


<a id="McUtils.Jupyter.Apps.Interfaces.Layout.setup_layout" class="docs-object-method">&nbsp;</a> 
```python
setup_layout(self, elements, item_attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Layout.py#L2823)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Layout.py#L2823?message=Update%20Docs)]
</div>
**LLM Docstring**

Prepare the layout: wrap each element as an item, returning `(layout_settings, items)`.
  - `elements`: `Any`
    > the elements
  - `item_attrs`: `Any`
    > the per-item attributes
  - `:returns`: `tuple`
    > `(settings, items)`


<a id="McUtils.Jupyter.Apps.Interfaces.Layout.get_layout_styles" class="docs-object-method">&nbsp;</a> 
```python
get_layout_styles(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Layout.py#L2835)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Layout.py#L2835?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: return the CSS styles for the container.
  - `kwargs`: `Any`
    > layout parameters
  - `:returns`: `dict`
    > the styles


<a id="McUtils.Jupyter.Apps.Interfaces.Layout.styles" class="docs-object-method">&nbsp;</a> 
```python
@property
styles(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Layout.py#L2847)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Layout.py#L2847?message=Update%20Docs)]
</div>
**LLM Docstring**

The container's combined explicit and computed layout styles.
  - `:returns`: `dict`
    > the styles


<a id="McUtils.Jupyter.Apps.Interfaces.Layout.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Layout.py#L2858)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Layout.py#L2858?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the layout container with its items and styles.
  - `:returns`: `_`
    > the JHTML element
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/Layout.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/Layout.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/Layout.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/Layout.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2787?message=Update%20Docs)   
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