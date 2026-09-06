## <a id="McUtils.Jupyter.Apps.Interfaces.Component">Component</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L236?message=Update%20Docs)]
</div>

Provides an abstract base class for an interface element
to allow for the easy construction of interesting interfaces







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Jupyter.Apps.Interfaces.Component.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, dynamic=True, debug_pane=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L241)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L241?message=Update%20Docs)]
</div>
**LLM Docstring**

Base interface component holding its attributes, parent links, and widget cache.
  - `dynamic`: `bool`
    > build a dynamic (reactive) widget
  - `debug_pane`: `Any`
    > the output pane for construction errors
  - `attrs`: `Any`
    > the component attributes


<a id="McUtils.Jupyter.Apps.Interfaces.Component.attrs" class="docs-object-method">&nbsp;</a> 
```python
@property
attrs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L258)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L258?message=Update%20Docs)]
</div>
**LLM Docstring**

The component's attributes (as an immutable mapping). The setter replaces the
attribute dict.
  - `:returns`: `frozendict`
    > the attributes


<a id="McUtils.Jupyter.Apps.Interfaces.Component.get_attr" class="docs-object-method">&nbsp;</a> 
```python
get_attr(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L283?message=Update%20Docs)]
</div>
**LLM Docstring**

Get an attribute by key.
  - `key`: `Any`
    > the attribute name
  - `:returns`: `_`
    > the value


<a id="McUtils.Jupyter.Apps.Interfaces.Component.get_child" class="docs-object-method">&nbsp;</a> 
```python
get_child(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L293)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L293?message=Update%20Docs)]
</div>
**LLM Docstring**

Get a child by key (unsupported on the base component).
  - `key`: `Any`
    > the child index


<a id="McUtils.Jupyter.Apps.Interfaces.Component.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L305)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L305?message=Update%20Docs)]
</div>
**LLM Docstring**

Get an attribute (string key) or a child (other key).
  - `item`: `Any`
    > the key
  - `:returns`: `_`
    > the attribute value or child


<a id="McUtils.Jupyter.Apps.Interfaces.Component.set_attr" class="docs-object-method">&nbsp;</a> 
```python
set_attr(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L319)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L319?message=Update%20Docs)]
</div>
**LLM Docstring**

Set an attribute in the component's attribute dict.
  - `key`: `Any`
    > the attribute name
  - `value`: `Any`
    > the value


<a id="McUtils.Jupyter.Apps.Interfaces.Component.update_widget_attr" class="docs-object-method">&nbsp;</a> 
```python
update_widget_attr(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L329)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L329?message=Update%20Docs)]
</div>
**LLM Docstring**

Push an attribute change into the live widget cache.
  - `key`: `Any`
    > the attribute name
  - `value`: `Any`
    > the value


<a id="McUtils.Jupyter.Apps.Interfaces.Component.set_child" class="docs-object-method">&nbsp;</a> 
```python
set_child(self, which, new): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L339)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L339?message=Update%20Docs)]
</div>
**LLM Docstring**

Set a child (unsupported on the base component).
  - `which`: `Any`
    > the child index
  - `new`: `Any`
    > the new child


<a id="McUtils.Jupyter.Apps.Interfaces.Component.update_widget_child" class="docs-object-method">&nbsp;</a> 
```python
update_widget_child(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L352)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L352?message=Update%20Docs)]
</div>
**LLM Docstring**

Push a child change into the live widget cache.
  - `key`: `Any`
    > the child index
  - `value`: `Any`
    > the new child


<a id="McUtils.Jupyter.Apps.Interfaces.Component.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L362)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L362?message=Update%20Docs)]
</div>
**LLM Docstring**

Set an attribute (string key) or child (other key), syncing the widget cache.
  - `key`: `Any`
    > the key
  - `value`: `Any`
    > the value


<a id="McUtils.Jupyter.Apps.Interfaces.Component.del_attr" class="docs-object-method">&nbsp;</a> 
```python
del_attr(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L380)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L380?message=Update%20Docs)]
</div>
**LLM Docstring**

Delete an attribute from the attribute dict.
  - `key`: `Any`
    > the attribute name


<a id="McUtils.Jupyter.Apps.Interfaces.Component.del_widget_attr" class="docs-object-method">&nbsp;</a> 
```python
del_widget_attr(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L389)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L389?message=Update%20Docs)]
</div>
**LLM Docstring**

Delete an attribute from the live widget cache.
  - `key`: `Any`
    > the attribute name


<a id="McUtils.Jupyter.Apps.Interfaces.Component.del_child" class="docs-object-method">&nbsp;</a> 
```python
del_child(self, which): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L398)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L398?message=Update%20Docs)]
</div>
**LLM Docstring**

Delete a child (unsupported on the base component).
  - `which`: `Any`
    > the child index


<a id="McUtils.Jupyter.Apps.Interfaces.Component.del_widget_child" class="docs-object-method">&nbsp;</a> 
```python
del_widget_child(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L410)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L410?message=Update%20Docs)]
</div>
**LLM Docstring**

Delete a child from the live widget cache.
  - `key`: `Any`
    > the child index


<a id="McUtils.Jupyter.Apps.Interfaces.Component.__delitem__" class="docs-object-method">&nbsp;</a> 
```python
__delitem__(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L419)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L419?message=Update%20Docs)]
</div>
**LLM Docstring**

Delete an attribute (string key) or child (other key), syncing the widget cache.
  - `key`: `Any`
    > the key


<a id="McUtils.Jupyter.Apps.Interfaces.Component.insert" class="docs-object-method">&nbsp;</a> 
```python
insert(self, where, new): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L436)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L436?message=Update%20Docs)]
</div>
**LLM Docstring**

Insert a new child at a position, syncing the widget cache.
  - `where`: `Any`
    > the insertion index
  - `new`: `Any`
    > the child to insert


<a id="McUtils.Jupyter.Apps.Interfaces.Component.append" class="docs-object-method">&nbsp;</a> 
```python
append(self, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L448)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L448?message=Update%20Docs)]
</div>
**LLM Docstring**

Append a child to the end.
  - `child`: `Any`
    > the child to append


<a id="McUtils.Jupyter.Apps.Interfaces.Component.insert_child" class="docs-object-method">&nbsp;</a> 
```python
insert_child(self, where, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L458)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L458?message=Update%20Docs)]
</div>
**LLM Docstring**

Insert a child (unsupported on the base component).
  - `where`: `Any`
    > the index
  - `child`: `Any`
    > the child


<a id="McUtils.Jupyter.Apps.Interfaces.Component.insert_widget_child" class="docs-object-method">&nbsp;</a> 
```python
insert_widget_child(self, where, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L471)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L471?message=Update%20Docs)]
</div>
**LLM Docstring**

Insert a child into the live widget cache.
  - `where`: `Any`
    > the index
  - `child`: `Any`
    > the child


<a id="McUtils.Jupyter.Apps.Interfaces.Component.add_class" class="docs-object-method">&nbsp;</a> 
```python
add_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L482)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L482?message=Update%20Docs)]
</div>
**LLM Docstring**

Add CSS class(es) to the component (and the live widget).
  - `cls`: `Any`
    > the class name(s)


<a id="McUtils.Jupyter.Apps.Interfaces.Component.add_component_class" class="docs-object-method">&nbsp;</a> 
```python
add_component_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L493)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L493?message=Update%20Docs)]
</div>
**LLM Docstring**

Add CSS class(es) to the component's stored attributes.
  - `cls`: `Any`
    > the class name(s)


<a id="McUtils.Jupyter.Apps.Interfaces.Component.add_widget_class" class="docs-object-method">&nbsp;</a> 
```python
add_widget_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L509)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L509?message=Update%20Docs)]
</div>
**LLM Docstring**

Add CSS class(es) to the live widget.
  - `cls`: `Any`
    > the class name(s)


<a id="McUtils.Jupyter.Apps.Interfaces.Component.remove_class" class="docs-object-method">&nbsp;</a> 
```python
remove_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L518)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L518?message=Update%20Docs)]
</div>
**LLM Docstring**

Remove CSS class(es) from the component (and the live widget).
  - `cls`: `Any`
    > the class name(s)


<a id="McUtils.Jupyter.Apps.Interfaces.Component.remove_component_class" class="docs-object-method">&nbsp;</a> 
```python
remove_component_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L529)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L529?message=Update%20Docs)]
</div>
**LLM Docstring**

Remove CSS class(es) from the component's stored attributes.
  - `cls`: `Any`
    > the class name(s)


<a id="McUtils.Jupyter.Apps.Interfaces.Component.remove_widget_class" class="docs-object-method">&nbsp;</a> 
```python
remove_widget_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L547)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L547?message=Update%20Docs)]
</div>
**LLM Docstring**

Remove CSS class(es) from the live widget.
  - `cls`: `Any`
    > the class name(s)


<a id="McUtils.Jupyter.Apps.Interfaces.Component.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self, parent=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L557)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L557?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: render the component to its JHTML element.
  - `parent`: `Any`
    > the parent component
  - `:returns`: `_`
    > the JHTML element


<a id="McUtils.Jupyter.Apps.Interfaces.Component.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self, parent=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L568)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L568?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the component to a widget (cached), registering the parent and wrapping any
conversion failure as a `JHTMLConversionError`.
  - `parent`: `Any`
    > the parent component
  - `:returns`: `_`
    > the widget


<a id="McUtils.Jupyter.Apps.Interfaces.Component.mutate" class="docs-object-method">&nbsp;</a> 
```python
mutate(self, fn): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L593)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L593?message=Update%20Docs)]
</div>
**LLM Docstring**

Apply a mutation function to the component and invalidate its cached widget.
  - `fn`: `Callable`
    > the mutation callback


<a id="McUtils.Jupyter.Apps.Interfaces.Component.invalidate_cache" class="docs-object-method">&nbsp;</a> 
```python
invalidate_cache(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L604)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Component.py#L604?message=Update%20Docs)]
</div>
**LLM Docstring**

Invalidate the cached widget (and propagate the invalidation to parents).
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/Component.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/Component.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/Component.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/Component.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L236?message=Update%20Docs)   
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