## <a id="McUtils.Devutils.core.context_wrap">context_wrap</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/core.py#L608)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/core.py#L608?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Devutils.core.context_wrap.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/core.py#L609)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/core.py#L609?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap an arbitrary object so it can be used as a context manager, delegating to
its own `__enter__`/`__exit__` when present.
  - `obj`: `Any`
    > the object to wrap


<a id="McUtils.Devutils.core.context_wrap.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/core/context_wrap.py#L619)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/core/context_wrap.py#L619?message=Update%20Docs)]
</div>
**LLM Docstring**

Enter the wrapped object's context (or just return it if it isn't a context
manager).
  - `:returns`: `_`
    > the entered object


<a id="McUtils.Devutils.core.context_wrap.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/core/context_wrap.py#L632)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/core/context_wrap.py#L632?message=Update%20Docs)]
</div>
**LLM Docstring**

Exit the wrapped object's context, if it is a context manager.
  - `exc_type`: `Any`
    > the exception type, if any
  - `exc_val`: `Any`
    > the exception value, if any
  - `exc_tb`: `Any`
    > the traceback, if any
  - `:returns`: `_`
    > the wrapped `__exit__`'s result, if any
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/core/context_wrap.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/core/context_wrap.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/core/context_wrap.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/core/context_wrap.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/core.py#L608?message=Update%20Docs)   
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