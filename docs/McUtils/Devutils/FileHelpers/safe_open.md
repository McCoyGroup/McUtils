## <a id="McUtils.Devutils.FileHelpers.safe_open">safe_open</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers.py#L59)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L59?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Devutils.FileHelpers.safe_open.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, file, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers.py#L60)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L60?message=Update%20Docs)]
</div>
**LLM Docstring**

Context manager that opens a file path, or passes through an already-open
stream.
  - `file`: `Any`
    > the file path or open stream
  - `opts`: `Any`
    > options forwarded to `open`


<a id="McUtils.Devutils.FileHelpers.safe_open.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/safe_open.py#L73)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/safe_open.py#L73?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the stream: the passed-in object if it's already stream-like, else a
freshly opened file.
  - `:returns`: `_`
    > the open stream


<a id="McUtils.Devutils.FileHelpers.safe_open.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/safe_open.py#L87)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/safe_open.py#L87?message=Update%20Docs)]
</div>
**LLM Docstring**

Close the stream if this manager opened it.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/FileHelpers/safe_open.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/FileHelpers/safe_open.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/FileHelpers/safe_open.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/FileHelpers/safe_open.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L59?message=Update%20Docs)   
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