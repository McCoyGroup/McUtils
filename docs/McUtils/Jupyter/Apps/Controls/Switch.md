## <a id="McUtils.Jupyter.Apps.Controls.Switch">Switch</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L410)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L410?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
base_cls: list
```
<a id="McUtils.Jupyter.Apps.Controls.Switch.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, var, type='checkbox', role='switch', **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L412)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L412?message=Update%20Docs)]
</div>
**LLM Docstring**

A toggle-switch control (a checkbox with a `switch` role).
  - `var`: `Any`
    > the bound variable
  - `type`: `str`
    > the input type
  - `role`: `str`
    > the ARIA role
  - `attrs`: `Any`
    > extra attributes


<a id="McUtils.Jupyter.Apps.Controls.Switch.get_value" class="docs-object-method">&nbsp;</a> 
```python
get_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Switch.py#L426)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Switch.py#L426?message=Update%20Docs)]
</div>
**LLM Docstring**

Read the switch as a bool (from its inner checkbox).
  - `:returns`: `bool`
    > the toggled state


<a id="McUtils.Jupyter.Apps.Controls.Switch.set_value" class="docs-object-method">&nbsp;</a> 
```python
set_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Switch.py#L438)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Switch.py#L438?message=Update%20Docs)]
</div>
**LLM Docstring**

Set the switch's inner checkbox from the variable's truthiness.


<a id="McUtils.Jupyter.Apps.Controls.Switch.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Switch.py#L449)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Switch.py#L449?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the switch (wrapping the checkbox in a `form-switch` div).
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Controls/Switch.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Controls/Switch.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Controls/Switch.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Controls/Switch.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L410?message=Update%20Docs)   
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