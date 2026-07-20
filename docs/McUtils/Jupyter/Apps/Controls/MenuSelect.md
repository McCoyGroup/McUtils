## <a id="McUtils.Jupyter.Apps.Controls.MenuSelect">MenuSelect</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L908)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L908?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
menu_type: ListGroup
```
<a id="McUtils.Jupyter.Apps.Controls.MenuSelect.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, var, options, menu_type=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L910)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L910?message=Update%20Docs)]
</div>
**LLM Docstring**

A control that selects a value by activating an item in a menu component (e.g. a
list group).
  - `var`: `Any`
    > the bound variable
  - `options`: `Any`
    > the menu options
  - `menu_type`: `Any`
    > the menu component class
  - `attrs`: `Any`
    > extra menu attributes


<a id="McUtils.Jupyter.Apps.Controls.MenuSelect.get_value" class="docs-object-method">&nbsp;</a> 
```python
get_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L928)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L928?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the value mapped to the currently active item.
  - `:returns`: `_`
    > the value


<a id="McUtils.Jupyter.Apps.Controls.MenuSelect.set_value" class="docs-object-method">&nbsp;</a> 
```python
set_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L938)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L938?message=Update%20Docs)]
</div>
**LLM Docstring**

Activate the menu item matching the variable's value.


<a id="McUtils.Jupyter.Apps.Controls.MenuSelect.update" class="docs-object-method">&nbsp;</a> 
```python
update(self, e): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L945)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L945?message=Update%20Docs)]
</div>
**LLM Docstring**

Activate the item matching the current value (a change handler).
  - `e`: `Any`
    > the change event


<a id="McUtils.Jupyter.Apps.Controls.MenuSelect.set_active" class="docs-object-method">&nbsp;</a> 
```python
set_active(self, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L954)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L954?message=Update%20Docs)]
</div>
**LLM Docstring**

Activate the menu item whose mapped value equals `v`.
  - `v`: `Any`
    > the value to select


<a id="McUtils.Jupyter.Apps.Controls.MenuSelect.set_active_key" class="docs-object-method">&nbsp;</a> 
```python
set_active_key(self, k): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L969)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L969?message=Update%20Docs)]
</div>
**LLM Docstring**

Activate the menu item with the given key, deactivating the previously active one.
  - `k`: `Any`
    > the item key


<a id="McUtils.Jupyter.Apps.Controls.MenuSelect.onclick" class="docs-object-method">&nbsp;</a> 
```python
onclick(self, e, i, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L989)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L989?message=Update%20Docs)]
</div>
**LLM Docstring**

Handle a menu-item click: set the variable and activate the item.
  - `e`: `Any`
    > the click event
  - `i`: `Any`
    > the item id
  - `v`: `Any`
    > the item's value


<a id="McUtils.Jupyter.Apps.Controls.MenuSelect.canonicalize_options" class="docs-object-method">&nbsp;</a> 
```python
canonicalize_options(self, options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L1003)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L1003?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize the menu options into item dicts (with ids and click handlers) and a
`{id: value}` value map.
  - `options`: `Any`
    > the options
  - `:returns`: `tuple`
    > `(value_map, item_dicts)`


<a id="McUtils.Jupyter.Apps.Controls.MenuSelect.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L1036)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/MenuSelect.py#L1036?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the menu widget and activate the initial item.
  - `:returns`: `_`
    > the widget
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Controls/MenuSelect.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Controls/MenuSelect.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Controls/MenuSelect.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Controls/MenuSelect.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L908?message=Update%20Docs)   
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