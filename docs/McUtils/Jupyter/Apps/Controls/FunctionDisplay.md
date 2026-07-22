## <a id="McUtils.Jupyter.Apps.Controls.FunctionDisplay">FunctionDisplay</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L699)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L699?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Jupyter.Apps.Controls.FunctionDisplay.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, fn, vars, pane=None, autoclear=True, debounce=None, delay_time=0.1, namespace=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L700)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L700?message=Update%20Docs)]
</div>
**LLM Docstring**

A component that re-runs a function (over a set of variables) and displays its
result whenever an input changes, with optional debouncing.
  - `fn`: `Callable`
    > the function to run
  - `vars`: `Any`
    > the input variables
  - `pane`: `Any`
    > the output pane (created if omitted)
  - `autoclear`: `bool`
    > clear the pane before each update
  - `debounce`: `Any`
    > the debounce interval (seconds)
  - `delay_time`: `float`
    > the minimum time between calls
  - `namespace`: `Any`
    > the variable namespace
  - `attrs`: `Any`
    > extra pane attributes


<a id="McUtils.Jupyter.Apps.Controls.FunctionDisplay.link_vars" class="docs-object-method">&nbsp;</a> 
```python
link_vars(self, *var): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L734)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L734?message=Update%20Docs)]
</div>
**LLM Docstring**

Link the display's update handler to every input variable (and to future
variable additions).


<a id="McUtils.Jupyter.Apps.Controls.FunctionDisplay.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self, parent=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L746)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L746?message=Update%20Docs)]
</div>
**LLM Docstring**

Render to a widget, linking the input variables on first construction (with a
temporarily relaxed debounce).
  - `parent`: `Any`
    > the parent component
  - `:returns`: `_`
    > the widget


<a id="McUtils.Jupyter.Apps.Controls.FunctionDisplay.observe" class="docs-object-method">&nbsp;</a> 
```python
observe(self, fn, names=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L769)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L769?message=Update%20Docs)]
</div>
**LLM Docstring**

Observe changes on the underlying widget.
  - `fn`: `Any`
    > the change handler
  - `names`: `Any`
    > the trait name(s)
  - `:returns`: `_`
    > the observation handle


<a id="McUtils.Jupyter.Apps.Controls.FunctionDisplay.unobserve" class="docs-object-method">&nbsp;</a> 
```python
unobserve(self, fn, names=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L783)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L783?message=Update%20Docs)]
</div>
**LLM Docstring**

Remove a change observer.
  - `fn`: `Any`
    > the handler
  - `names`: `Any`
    > the trait name(s)


<a id="McUtils.Jupyter.Apps.Controls.FunctionDisplay.update" class="docs-object-method">&nbsp;</a> 
```python
update(self, event): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L806)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L806?message=Update%20Docs)]
</div>
**LLM Docstring**

Handle an input change: run the update immediately or schedule a debounced
execution, honoring the minimum delay between calls and reporting errors to the
pane.
  - `event`: `Any`
    > the change event


<a id="McUtils.Jupyter.Apps.Controls.FunctionDisplay.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L844)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/FunctionDisplay.py#L844?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the display, running the function once to populate the pane.
  - `:returns`: `_`
    > the output pane
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Controls/FunctionDisplay.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Controls/FunctionDisplay.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Controls/FunctionDisplay.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Controls/FunctionDisplay.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L699?message=Update%20Docs)   
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