## <a id="McUtils.Jupyter.Apps.Controls.ProgressBar">ProgressBar</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L856)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L856?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Jupyter.Apps.Controls.ProgressBar.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, var, bar=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls.py#L857)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L857?message=Update%20Docs)]
</div>
**LLM Docstring**

A control that drives a progress bar from a variable.
  - `var`: `Any`
    > the bound variable (the percentage)
  - `bar`: `Any`
    > the progress bar component (created if omitted)
  - `attrs`: `Any`
    > extra bar attributes


<a id="McUtils.Jupyter.Apps.Controls.ProgressBar.get_value" class="docs-object-method">&nbsp;</a> 
```python
get_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/ProgressBar.py#L871)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/ProgressBar.py#L871?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the variable's value, coercing empty/None to 0 and strings to ints.
  - `:returns`: `_`
    > the progress percentage


<a id="McUtils.Jupyter.Apps.Controls.ProgressBar.set_value" class="docs-object-method">&nbsp;</a> 
```python
set_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/ProgressBar.py#L885)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/ProgressBar.py#L885?message=Update%20Docs)]
</div>
**LLM Docstring**

Set the bar's width from the current percentage.


<a id="McUtils.Jupyter.Apps.Controls.ProgressBar.update" class="docs-object-method">&nbsp;</a> 
```python
update(self, e): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/ProgressBar.py#L892)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/ProgressBar.py#L892?message=Update%20Docs)]
</div>
**LLM Docstring**

Re-render the bar (a change handler).
  - `e`: `Any`
    > the change event


<a id="McUtils.Jupyter.Apps.Controls.ProgressBar.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Controls/ProgressBar.py#L901)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls/ProgressBar.py#L901?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the progress bar widget.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Controls/ProgressBar.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Controls/ProgressBar.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Controls/ProgressBar.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Controls/ProgressBar.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Controls.py#L856?message=Update%20Docs)   
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