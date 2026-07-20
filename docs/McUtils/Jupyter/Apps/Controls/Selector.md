## <a id="McUtils.Jupyter.Apps.Controls.Selector">Selector</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L513)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L513?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
base_cls: list
```
<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Select" class="docs-object-method">&nbsp;</a> 
```python
base(*elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L304?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Controls.Selector.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, var, options=None, value=None, multiple=False, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L516)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L516?message=Update%20Docs)]
</div>
**LLM Docstring**

A `<select>` dropdown control, single- or multi-select.
  - `var`: `Any`
    > the bound variable
  - `options`: `Any`
    > the selectable options
  - `value`: `Any`
    > the initial value (defaults to the first option)
  - `multiple`: `bool`
    > allow multiple selections
  - `attrs`: `Any`
    > extra attributes


<a id="McUtils.Jupyter.Apps.Controls.Selector.multiple" class="docs-object-method">&nbsp;</a> 
```python
@property
multiple(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Selector.py#L535)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Selector.py#L535?message=Update%20Docs)]
</div>
**LLM Docstring**

Whether the selector allows multiple selections.
  - `:returns`: `bool`
    > the multi-select flag


<a id="McUtils.Jupyter.Apps.Controls.Selector.get_value" class="docs-object-method">&nbsp;</a> 
```python
get_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Selector.py#L553)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Selector.py#L553?message=Update%20Docs)]
</div>
**LLM Docstring**

Read the selection, splitting the multi-select value into a list.
  - `:returns`: `_`
    > the selected value(s)


<a id="McUtils.Jupyter.Apps.Controls.Selector.set_value" class="docs-object-method">&nbsp;</a> 
```python
set_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Selector.py#L571)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Selector.py#L571?message=Update%20Docs)]
</div>
**LLM Docstring**

Push the variable's selection into the widget (joining a multi-select list).


<a id="McUtils.Jupyter.Apps.Controls.Selector.canonicalize_options" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_options(cls, options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L585)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L585?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize the options into `(label, value)` pairs.
  - `options`: `Any`
    > the options (strings or `(label, value)` pairs)
  - `:returns`: `tuple`
    > the canonicalized options


<a id="McUtils.Jupyter.Apps.Controls.Selector.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Selector.py#L627)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Selector.py#L627?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the select element with its options.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Controls/Selector.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Controls/Selector.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Controls/Selector.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Controls/Selector.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L513?message=Update%20Docs)   
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