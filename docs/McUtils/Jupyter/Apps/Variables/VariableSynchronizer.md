## <a id="McUtils.Jupyter.Apps.Variables.VariableSynchronizer">VariableSynchronizer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables.py#L451)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables.py#L451?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
current_namespace: VariableNamespace
```
<a id="McUtils.Jupyter.Apps.Variables.VariableSynchronizer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name, namespace=None, value=None, callbacks=(), output_pane=None, autounlink=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables.py#L453)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables.py#L453?message=Update%20Docs)]
</div>
**LLM Docstring**

A reactive variable that synchronizes its value across linked widgets and fires
callbacks on change.
  - `name`: `Any`
    > the variable name
  - `namespace`: `Any`
    > the owning namespace
  - `value`: `Any`
    > the initial value
  - `callbacks`: `Any`
    > change callbacks
  - `output_pane`: `Any`
    > the output pane for error display
  - `autounlink`: `bool`
    > unlink other widgets when a new one links


<a id="McUtils.Jupyter.Apps.Variables.VariableSynchronizer.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L475)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L475?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the name and value.
  - `:returns`: `str`
    > the representation


<a id="McUtils.Jupyter.Apps.Variables.VariableSynchronizer.create_var" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_var(cls, var, namespace=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L489)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L489?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a name (or synchronizer) to a `VariableSynchronizer` in the namespace,
creating and caching it if needed, and registering it with the active variable
set.
  - `var`: `Any`
    > the variable name or synchronizer
  - `namespace`: `Any`
    > the namespace (defaults to the current one)
  - `:returns`: `VariableSynchronizer`
    > the variable


<a id="McUtils.Jupyter.Apps.Variables.VariableSynchronizer.name" class="docs-object-method">&nbsp;</a> 
```python
@property
name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L517)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L517?message=Update%20Docs)]
</div>
**LLM Docstring**

The variable's name.
  - `:returns`: `_`
    > the name


<a id="McUtils.Jupyter.Apps.Variables.VariableSynchronizer.value" class="docs-object-method">&nbsp;</a> 
```python
@property
value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L527)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L527?message=Update%20Docs)]
</div>
**LLM Docstring**

The variable's current value. Setting it propagates to linked widgets and fires
the change callbacks.
  - `:returns`: `_`
    > the value


<a id="McUtils.Jupyter.Apps.Variables.VariableSynchronizer.set_value" class="docs-object-method">&nbsp;</a> 
```python
set_value(self, v, caller=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L549)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L549?message=Update%20Docs)]
</div>
**LLM Docstring**

Set the value (if changed), firing the change callbacks and propagating to every
linked widget except the caller.
  - `v`: `Any`
    > the new value
  - `caller`: `Any`
    > the widget that triggered the change (not re-notified)


<a id="McUtils.Jupyter.Apps.Variables.VariableSynchronizer.link" class="docs-object-method">&nbsp;</a> 
```python
link(self, widget): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L572)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L572?message=Update%20Docs)]
</div>
**LLM Docstring**

Link a widget to the variable: seed the variable from the widget's value, observe
the widget for changes, and (if `autounlink`) unlink other widgets.
  - `widget`: `Any`
    > the widget to link


<a id="McUtils.Jupyter.Apps.Variables.VariableSynchronizer.unlink" class="docs-object-method">&nbsp;</a> 
```python
unlink(self, widget): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L596)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.py#L596?message=Update%20Docs)]
</div>
**LLM Docstring**

Unlink a widget from the variable, removing its change observers.
  - `widget`: `Any`
    > the widget to unlink
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Variables/VariableSynchronizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables.py#L451?message=Update%20Docs)   
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