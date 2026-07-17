## <a id="McUtils.Devutils.FileHelpers.StreamInterface">StreamInterface</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers.py#L679)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L679?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Devutils.FileHelpers.StreamInterface.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, stream, file_backed=False, **file_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers.py#L680)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L680?message=Update%20Docs)]
</div>
**LLM Docstring**

Uniform context manager over a stream: accepts an open stream, a file path, or
raw string/bytes content.
  - `stream`: `Any`
    > the stream, file path, or raw content
  - `file_backed`: `bool`
    > back raw content with a temporary file rather than an in-memory buffer
  - `file_opts`: `Any`
    > options for opening/creating the stream


<a id="McUtils.Devutils.FileHelpers.StreamInterface.is_binary" class="docs-object-method">&nbsp;</a> 
```python
is_binary(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/StreamInterface.py#L699)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/StreamInterface.py#L699?message=Update%20Docs)]
</div>
**LLM Docstring**

Whether the stream is (or would be opened in) binary mode.
  - `:returns`: `bool`
    > whether the stream is binary


<a id="McUtils.Devutils.FileHelpers.StreamInterface.get_encoding" class="docs-object-method">&nbsp;</a> 
```python
get_encoding(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/StreamInterface.py#L713)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/StreamInterface.py#L713?message=Update%20Docs)]
</div>
**LLM Docstring**

The stream's text encoding.
  - `:returns`: `str`
    > the encoding


<a id="McUtils.Devutils.FileHelpers.StreamInterface.is_path_like" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_path_like(cls, input): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L727)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L727?message=Update%20Docs)]
</div>
**LLM Docstring**

Heuristic test for whether a string is a path rather than inline content (no
newlines, commas, or parentheses).
  - `input`: `str`
    > the string to test
  - `:returns`: `bool`
    > whether it looks like a path


<a id="McUtils.Devutils.FileHelpers.StreamInterface.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/StreamInterface.py#L742)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/StreamInterface.py#L742?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve the input into an open stream: open a file path, wrap raw content in a
buffer/file-backed stream, or pass through an already-open stream.
  - `:returns`: `_`
    > the open stream


<a id="McUtils.Devutils.FileHelpers.StreamInterface.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/StreamInterface.py#L769)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/StreamInterface.py#L769?message=Update%20Docs)]
</div>
**LLM Docstring**

Close any stream/buffer this interface opened, leaving already-open inputs alone.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/FileHelpers/StreamInterface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/FileHelpers/StreamInterface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/FileHelpers/StreamInterface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/FileHelpers/StreamInterface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L679?message=Update%20Docs)   
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