## <a id="McUtils.Jupyter.Apps.Interfaces.DelayedResult">DelayedResult</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L3460)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L3460?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
NoResult: str
```
<a id="McUtils.Jupyter.Apps.Interfaces.DelayedResult.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, func, *args, output=None, callback=None, parent=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L3464)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L3464?message=Update%20Docs)]
</div>
**LLM Docstring**

Run a function on a background thread and display its result when ready.
  - `func`: `Callable`
    > the function to run
  - `args`: `Any`
    > positional arguments for the function
  - `output`: `Any`
    > the output area (created if omitted)
  - `callback`: `Any`
    > a `(result, error, runner)` completion callback
  - `parent`: `Any`
    > the parent interface
  - `kwargs`: `Any`
    > keyword arguments for the function


<a id="McUtils.Jupyter.Apps.Interfaces.DelayedResult.get_output_area" class="docs-object-method">&nbsp;</a> 
```python
get_output_area(self, output=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/DelayedResult.py#L3491)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/DelayedResult.py#L3491?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the output area (creating one if none is given).
  - `output`: `Any`
    > an explicit output area
  - `:returns`: `_`
    > the output area


<a id="McUtils.Jupyter.Apps.Interfaces.DelayedResult.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/DelayedResult.py#L3504)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/DelayedResult.py#L3504?message=Update%20Docs)]
</div>
**LLM Docstring**

Enter the output area's context.
  - `:returns`: `DelayedResult`
    > self


<a id="McUtils.Jupyter.Apps.Interfaces.DelayedResult.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/DelayedResult.py#L3516)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/DelayedResult.py#L3516?message=Update%20Docs)]
</div>
**LLM Docstring**

Exit the output area's context.
  - `exc_type`: `Any`
    > the exception type, if any
  - `exc_val`: `Any`
    > the exception value, if any
  - `exc_tb`: `Any`
    > the traceback, if any


<a id="McUtils.Jupyter.Apps.Interfaces.DelayedResult.start_process" class="docs-object-method">&nbsp;</a> 
```python
start_process(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/DelayedResult.py#L3561)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/DelayedResult.py#L3561?message=Update%20Docs)]
</div>
**LLM Docstring**

Start the background thread running the function (once).
  - `:returns`: `_`
    > the thread


<a id="McUtils.Jupyter.Apps.Interfaces.DelayedResult.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/DelayedResult.py#L3574)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/DelayedResult.py#L3574?message=Update%20Docs)]
</div>
**LLM Docstring**

Start the background process and return the output area widget.
  - `:returns`: `_`
    > the output area
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/DelayedResult.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/DelayedResult.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/DelayedResult.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/DelayedResult.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L3460?message=Update%20Docs)   
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