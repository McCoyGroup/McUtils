## <a id="McUtils.Jupyter.Apps.Variables.InterfaceVars">InterfaceVars</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables.py#L174)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables.py#L174?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Jupyter.Apps.Variables.InterfaceVars.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *vars, callbacks=None, namespace=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables.py#L176)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables.py#L176?message=Update%20Docs)]
</div>
**LLM Docstring**

Hold a set of interface variables (coercing each into a `Var`) plus the callbacks
fired when the set changes.
  - `vars`: `Any`
    > the variables (names or synchronizers)
  - `callbacks`: `Any`
    > callbacks fired when a variable is added
  - `namespace`: `Any`
    > the variable namespace


<a id="McUtils.Jupyter.Apps.Variables.InterfaceVars.unique_namespace" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
unique_namespace(cls, tag='vars'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L191?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate a unique namespace name.
  - `tag`: `str`
    > the name prefix
  - `:returns`: `str`
    > the namespace name


<a id="McUtils.Jupyter.Apps.Variables.InterfaceVars.active_vars" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
active_vars(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L204)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L204?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the innermost active variable set (from the context stack), or `None`.
  - `:returns`: `InterfaceVars | None`
    > the active variable set


<a id="McUtils.Jupyter.Apps.Variables.InterfaceVars.dict" class="docs-object-method">&nbsp;</a> 
```python
@property
dict(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L218)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L218?message=Update%20Docs)]
</div>
**LLM Docstring**

The variables as a `{name: value}` mapping.
  - `:returns`: `dict`
    > the variable values


<a id="McUtils.Jupyter.Apps.Variables.InterfaceVars.items" class="docs-object-method">&nbsp;</a> 
```python
@property
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L229)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L229?message=Update%20Docs)]
</div>
**LLM Docstring**

The variables as a list of `(name, value)` pairs.
  - `:returns`: `list`
    > the variable items


<a id="McUtils.Jupyter.Apps.Variables.InterfaceVars.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L240)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L240?message=Update%20Docs)]
</div>
**LLM Docstring**

Iterate over the variables.
  - `:returns`: `_`
    > the variable iterator


<a id="McUtils.Jupyter.Apps.Variables.InterfaceVars.add" class="docs-object-method">&nbsp;</a> 
```python
add(self, var): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L249)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L249?message=Update%20Docs)]
</div>
**LLM Docstring**

Add a variable to the set (if new), firing the change callbacks.
  - `var`: `Any`
    > the variable to add


<a id="McUtils.Jupyter.Apps.Variables.InterfaceVars.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L262)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L262?message=Update%20Docs)]
</div>
**LLM Docstring**

Push this set onto the active-vars stack so newly created variables register
here.
  - `:returns`: `list`
    > the variable list


<a id="McUtils.Jupyter.Apps.Variables.InterfaceVars.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L274)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L274?message=Update%20Docs)]
</div>
**LLM Docstring**

Pop this set off the active-vars stack.
  - `exc_type`: `Any`
    > the exception type, if any
  - `exc_val`: `Any`
    > the exception value, if any
  - `exc_tb`: `Any`
    > the traceback, if any


<a id="McUtils.Jupyter.Apps.Variables.InterfaceVars.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L285)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/InterfaceVars.py#L285?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation listing the variable names.
  - `:returns`: `str`
    > the representation
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Variables/InterfaceVars.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Variables/InterfaceVars.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Variables/InterfaceVars.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Variables/InterfaceVars.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables.py#L174?message=Update%20Docs)   
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