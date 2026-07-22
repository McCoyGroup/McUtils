## <a id="McUtils.Jupyter.Apps.Apps.Manipulator">Manipulator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps.py#L52)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps.py#L52?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
theme: dict
```
<a id="McUtils.Jupyter.Apps.Apps.Manipulator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, func, *controls, debounce=None, autoclear=True, namespace=None, layout_function=None, control_layout_function=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps.py#L61)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps.py#L61?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an interactive `Card` that re-runs a function over a set of controls
(ipywidgets-`interact`-style), laying out the output above the controls.
  - `func`: `Callable`
    > the function driven by the controls
  - `controls`: `Any`
    > the control specs (values, ranges, or existing controls)
  - `debounce`: `Any`
    > the debounce interval for updates
  - `autoclear`: `bool`
    > clear the output before each update
  - `namespace`: `Any`
    > the variable namespace (a fresh one if omitted)
  - `etc`: `Any`
    > extra `Card` options


<a id="McUtils.Jupyter.Apps.Apps.Manipulator.default_layout" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
default_layout(cls, self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L94)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L94?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.Manipulator.default_control_layout" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
default_control_layout(cls, self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L103)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L103?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.Manipulator.canonicalize_control" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_control(cls, settings, namespace=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L106?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize a control spec into a `Control`: pass existing controls through, else
build one from a `(var, settings)` pair (inferring a `range`/`value` settings dict
and the control type).
  - `settings`: `Any`
    > the control spec
  - `namespace`: `Any`
    > the variable namespace
  - `:returns`: `Control`
    > the control


<a id="McUtils.Jupyter.Apps.Apps.Manipulator.initialize" class="docs-object-method">&nbsp;</a> 
```python
initialize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/Manipulator.py#L137)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/Manipulator.py#L137?message=Update%20Docs)]
</div>
**LLM Docstring**

Run the function once (with no event) to populate the output.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Apps/Manipulator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Apps/Manipulator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Apps/Manipulator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Apps/Manipulator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps.py#L52?message=Update%20Docs)   
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