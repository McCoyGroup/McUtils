## <a id="McUtils.Jupyter.Apps.Controls.Control">Control</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L32?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
layout_orientation: str
control_types: dict
```
<a id="McUtils.Jupyter.Apps.Controls.Control.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, var, namespace=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L34)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L34?message=Update%20Docs)]
</div>
**LLM Docstring**

Base control component bound to a reactive variable.
  - `var`: `Any`
    > the variable (name or synchronizer) the control drives
  - `namespace`: `Any`
    > the variable namespace


<a id="McUtils.Jupyter.Apps.Controls.Control.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self, parent=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Control.py#L46)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Control.py#L46?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the control to a widget, linking it to its variable and syncing the initial
value on first construction.
  - `parent`: `Any`
    > the parent component
  - `:returns`: `_`
    > the widget


<a id="McUtils.Jupyter.Apps.Controls.Control.set_value" class="docs-object-method">&nbsp;</a> 
```python
set_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Control.py#L64)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Control.py#L64?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: push the variable's value into the underlying widget.


<a id="McUtils.Jupyter.Apps.Controls.Control.get_value" class="docs-object-method">&nbsp;</a> 
```python
get_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Control.py#L72)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Control.py#L72?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: read the control's current value.
  - `:returns`: `_`
    > the value


<a id="McUtils.Jupyter.Apps.Controls.Control.value" class="docs-object-method">&nbsp;</a> 
```python
@property
value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Control.py#L82)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Control.py#L82?message=Update%20Docs)]
</div>
**LLM Docstring**

The control's current value. The getter reads the widget; the setter updates the
bound variable (as the caller) and syncs the widget.
  - `:returns`: `_`
    > the value


<a id="McUtils.Jupyter.Apps.Controls.Control.observe" class="docs-object-method">&nbsp;</a> 
```python
observe(self, fn, names=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Control.py#L105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Control.py#L105?message=Update%20Docs)]
</div>
**LLM Docstring**

Observe changes on the underlying widget.
  - `fn`: `Any`
    > the change handler
  - `names`: `Any`
    > the trait name(s) to observe
  - `:returns`: `_`
    > the observation handle


<a id="McUtils.Jupyter.Apps.Controls.Control.unobserve" class="docs-object-method">&nbsp;</a> 
```python
unobserve(self, fn, names=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/Control.py#L119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/Control.py#L119?message=Update%20Docs)]
</div>
**LLM Docstring**

Remove a change observer from the underlying widget.
  - `fn`: `Any`
    > the handler to remove
  - `names`: `Any`
    > the trait name(s)


<a id="McUtils.Jupyter.Apps.Controls.Control.construct" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct(cls, var, control_type=None, field_type=None, value=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L131)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L131?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a control of the appropriate type (inferred from the field type/value
if not given), from the control-type registry.
  - `var`: `Any`
    > the bound variable
  - `control_type`: `Any`
    > the control type name/class (inferred if omitted)
  - `field_type`: `Any`
    > the value's field type
  - `value`: `Any`
    > the initial value
  - `attrs`: `Any`
    > extra control attributes
  - `:returns`: `Control`
    > the control


<a id="McUtils.Jupyter.Apps.Controls.Control.infer_control" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
infer_control(cls, field_type=None, value=None, **ignored): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L154?message=Update%20Docs)]
</div>
**LLM Docstring**

Infer the control type from a field type or value (string→`StringField`,
bool→`Checkbox`, number→`Slider`, a `range`→`Slider`).
  - `field_type`: `Any`
    > the field type
  - `value`: `Any`
    > the value (used to infer the field type)
  - `ignored`: `Any`
    > other attributes (checked for `range`)
  - `:returns`: `type`
    > the control class
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Controls/Control.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Controls/Control.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Controls/Control.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Controls/Control.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L32?message=Update%20Docs)   
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