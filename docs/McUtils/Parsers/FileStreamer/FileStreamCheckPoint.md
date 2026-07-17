## <a id="McUtils.Parsers.FileStreamer.FileStreamCheckPoint">FileStreamCheckPoint</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/FileStreamer.py#L23)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer.py#L23?message=Update%20Docs)]
</div>

A checkpoint for a file that can be returned to when parsing







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Parsers.FileStreamer.FileStreamCheckPoint.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, parent, revert=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/FileStreamer.py#L27)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer.py#L27?message=Update%20Docs)]
</div>
**LLM Docstring**

Record the reader's current byte/character offset and configure whether leaving the context restores that position.
  - `parent`: `object`
    > the parent reader or regex node

  - `revert`: `object`
    > whether to restore the captured position on context exit


<a id="McUtils.Parsers.FileStreamer.FileStreamCheckPoint.disable" class="docs-object-method">&nbsp;</a> 
```python
disable(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.py#L42)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.py#L42?message=Update%20Docs)]
</div>
**LLM Docstring**

Disable automatic restoration when the checkpoint context exits.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.FileStreamer.FileStreamCheckPoint.enable" class="docs-object-method">&nbsp;</a> 
```python
enable(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.py#L52)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.py#L52?message=Update%20Docs)]
</div>
**LLM Docstring**

Enable automatic restoration when the checkpoint context exits.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.FileStreamer.FileStreamCheckPoint.revert" class="docs-object-method">&nbsp;</a> 
```python
revert(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.py#L62)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.py#L62?message=Update%20Docs)]
</div>
**LLM Docstring**

Seek the parent reader back to the offset captured when this checkpoint was created.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.FileStreamer.FileStreamCheckPoint.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.py#L72)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.py#L72?message=Update%20Docs)]
</div>
**LLM Docstring**

Return this checkpoint for use in a `with` statement.
  - `:returns`: `object`
    > The opened stream, reader, parser, or checkpoint object.


<a id="McUtils.Parsers.FileStreamer.FileStreamCheckPoint.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.py#L82)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.py#L82?message=Update%20Docs)]
</div>
**LLM Docstring**

Restore the captured stream position when reversion is enabled; exceptions are not suppressed.
  - `exc_type`: `object`
    > the exception class raised in the context, if any

  - `exc_val`: `object`
    > the exception instance raised in the context, if any

  - `exc_tb`: `object`
    > the traceback raised in the context, if any
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer.py#L23?message=Update%20Docs)   
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