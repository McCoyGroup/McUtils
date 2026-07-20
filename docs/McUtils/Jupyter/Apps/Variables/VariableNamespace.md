## <a id="McUtils.Jupyter.Apps.Variables.VariableNamespace">VariableNamespace</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables.py#L342)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables.py#L342?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Jupyter.Apps.Variables.VariableNamespace.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name=None, dedupe=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables.py#L344)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables.py#L344?message=Update%20Docs)]
</div>
**LLM Docstring**

A named namespace of variables, optionally deduplicated so the same name reuses a
shared variable cache.
  - `name`: `Any`
    > the namespace name (a uuid if omitted)
  - `dedupe`: `bool`
    > share the variable cache with an existing namespace of the same name


<a id="McUtils.Jupyter.Apps.Variables.VariableNamespace.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L367)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L367?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the name and cached variables.
  - `:returns`: `str`
    > the representation


<a id="McUtils.Jupyter.Apps.Variables.VariableNamespace.create" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create(cls, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L381)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L381?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a namespace name (or namespace) to a cached `VariableNamespace`, creating
and caching it if needed.
  - `name`: `Any`
    > the namespace name or object
  - `:returns`: `VariableNamespace`
    > the namespace


<a id="McUtils.Jupyter.Apps.Variables.VariableNamespace.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L400)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L400?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether a variable name is in the namespace.
  - `item`: `Any`
    > the variable name
  - `:returns`: `bool`
    > whether it's present


<a id="McUtils.Jupyter.Apps.Variables.VariableNamespace.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L411)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L411?message=Update%20Docs)]
</div>
**LLM Docstring**

Get a variable from the namespace by name.
  - `item`: `Any`
    > the variable name
  - `:returns`: `_`
    > the variable


<a id="McUtils.Jupyter.Apps.Variables.VariableNamespace.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L421)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L421?message=Update%20Docs)]
</div>
**LLM Docstring**

Store a variable in the namespace under a name.
  - `key`: `Any`
    > the variable name
  - `value`: `Any`
    > the variable


<a id="McUtils.Jupyter.Apps.Variables.VariableNamespace.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L431)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L431?message=Update%20Docs)]
</div>
**LLM Docstring**

Activate this namespace as the current one, saving the previous.


<a id="McUtils.Jupyter.Apps.Variables.VariableNamespace.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L439)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables/VariableNamespace.py#L439?message=Update%20Docs)]
</div>
**LLM Docstring**

Restore the previously active namespace.
  - `exc_type`: `Any`
    > the exception type, if any
  - `exc_val`: `Any`
    > the exception value, if any
  - `exc_tb`: `Any`
    > the traceback, if any
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Variables/VariableNamespace.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Variables/VariableNamespace.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Variables/VariableNamespace.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Variables/VariableNamespace.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Variables.py#L342?message=Update%20Docs)   
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