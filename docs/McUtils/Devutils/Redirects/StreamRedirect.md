## <a id="McUtils.Devutils.Redirects.StreamRedirect">StreamRedirect</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects.py#L10)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects.py#L10?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Devutils.Redirects.StreamRedirect.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, logger, base_stream=None, line_join=True, strip_empty=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects.py#L11)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects.py#L11?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap a logging callback as a writable stream, so writes are forwarded to the
logger.
  - `logger`: `Callable`
    > the callback invoked with written data
  - `base_stream`: `Any`
    > an underlying stream to delegate reads/seeks/flush to
  - `line_join`: `Any`
    > joiner for `writelines` (`True` uses `''`), or `None` to pass lines through
  - `strip_empty`: `bool`
    > drop whitespace-only writes


<a id="McUtils.Devutils.Redirects.StreamRedirect.write" class="docs-object-method">&nbsp;</a> 
```python
write(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/StreamRedirect.py#L31)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/StreamRedirect.py#L31?message=Update%20Docs)]
</div>
**LLM Docstring**

Forward written data to the logger, skipping whitespace-only data when
`strip_empty` is set.
  - `data`: `Any`
    > the data to write


<a id="McUtils.Devutils.Redirects.StreamRedirect.writelines" class="docs-object-method">&nbsp;</a> 
```python
writelines(self, lines): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/StreamRedirect.py#L44)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/StreamRedirect.py#L44?message=Update%20Docs)]
</div>
**LLM Docstring**

Forward multiple lines to the logger, joining them with the configured joiner
(encoding it for bytes lines) or passing them through when no joiner is set.
  - `lines`: `Sequence`
    > the lines to write


<a id="McUtils.Devutils.Redirects.StreamRedirect.flush" class="docs-object-method">&nbsp;</a> 
```python
flush(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/StreamRedirect.py#L64)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/StreamRedirect.py#L64?message=Update%20Docs)]
</div>
**LLM Docstring**

Flush the underlying base stream, if any.


<a id="McUtils.Devutils.Redirects.StreamRedirect.seek" class="docs-object-method">&nbsp;</a> 
```python
seek(self, offset: int, whence: int = 0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/StreamRedirect.py#L72)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/StreamRedirect.py#L72?message=Update%20Docs)]
</div>
**LLM Docstring**

Seek on the underlying base stream, if any.
  - `offset`: `int`
    > the seek offset
  - `whence`: `int`
    > the seek origin
  - `:returns`: `_`
    > the new position, or `None`


<a id="McUtils.Devutils.Redirects.StreamRedirect.seekable" class="docs-object-method">&nbsp;</a> 
```python
seekable(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/StreamRedirect.py#L88)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/StreamRedirect.py#L88?message=Update%20Docs)]
</div>
**LLM Docstring**

Whether the underlying base stream is seekable.
  - `:returns`: `bool`
    > whether seeking is supported


<a id="McUtils.Devutils.Redirects.StreamRedirect.read" class="docs-object-method">&nbsp;</a> 
```python
read(self, size): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/StreamRedirect.py#L101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/StreamRedirect.py#L101?message=Update%20Docs)]
</div>
**LLM Docstring**

Read from the underlying base stream, if any.
  - `size`: `Any`
    > the number of bytes/characters to read
  - `:returns`: `_`
    > the data read, or `None`


<a id="McUtils.Devutils.Redirects.StreamRedirect.readline" class="docs-object-method">&nbsp;</a> 
```python
readline(self, limit: int = -1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/StreamRedirect.py#L114)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/StreamRedirect.py#L114?message=Update%20Docs)]
</div>
**LLM Docstring**

Read a line from the underlying base stream, if any.
  - `limit`: `int`
    > the maximum number of bytes/characters
  - `:returns`: `_`
    > the line read, or `None`


<a id="McUtils.Devutils.Redirects.StreamRedirect.readlines" class="docs-object-method">&nbsp;</a> 
```python
readlines(self, hint: int = -1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/StreamRedirect.py#L128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/StreamRedirect.py#L128?message=Update%20Docs)]
</div>
**LLM Docstring**

Read all lines from the underlying base stream, if any.
  - `hint`: `int`
    > an approximate byte-count hint
  - `:returns`: `_`
    > the lines read, or `None`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/Redirects/StreamRedirect.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/Redirects/StreamRedirect.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/Redirects/StreamRedirect.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/Redirects/StreamRedirect.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects.py#L10?message=Update%20Docs)   
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