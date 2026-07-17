## <a id="McUtils.Devutils.FileHelpers.FileBackedIO">FileBackedIO</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers.py#L556)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L556?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Devutils.FileHelpers.FileBackedIO.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, buffer: 'str | bytes | Callable[[], str | bytes]', mode='w+', file=None, delete=True, **tempfile_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers.py#L557)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L557?message=Update%20Docs)]
</div>
**LLM Docstring**

A stream-like wrapper backing an in-memory (or lazily generated) buffer with a
temporary file.
  - `buffer`: `str | bytes | Callable`
    > the buffer content, or a callable producing it
  - `mode`: `str`
    > the open mode
  - `file`: `Any`
    > an explicit backing file
  - `delete`: `bool`
    > delete the backing file on exit
  - `tempfile_opts`: `Any`
    > options for the temporary file


<a id="McUtils.Devutils.FileHelpers.FileBackedIO.resolve_buffer" class="docs-object-method">&nbsp;</a> 
```python
resolve_buffer(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L580)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L580?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the buffer contents, calling the generator if the buffer is a callable.
  - `:returns`: `str | bytes`
    > the buffer contents


<a id="McUtils.Devutils.FileHelpers.FileBackedIO.name" class="docs-object-method">&nbsp;</a> 
```python
@property
name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L593)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L593?message=Update%20Docs)]
</div>
**LLM Docstring**

The backing file's path (or `None` if not yet created).
  - `:returns`: `str | None`
    > the file path


<a id="McUtils.Devutils.FileHelpers.FileBackedIO.file" class="docs-object-method">&nbsp;</a> 
```python
@property
file(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L610)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L610?message=Update%20Docs)]
</div>
**LLM Docstring**

The backing file path, creating (and seeding) a temporary file on first access.
  - `:returns`: `str`
    > the file path


<a id="McUtils.Devutils.FileHelpers.FileBackedIO.write" class="docs-object-method">&nbsp;</a> 
```python
write(self, file=None, mode=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L631)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L631?message=Update%20Docs)]
</div>
**LLM Docstring**

Write the buffer contents out to a file.
  - `file`: `Any`
    > the destination file (defaults to the backing file)
  - `mode`: `str | None`
    > the open mode (coerced to a writing mode)
  - `:returns`: `_`
    > the file written


<a id="McUtils.Devutils.FileHelpers.FileBackedIO.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L651)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L651?message=Update%20Docs)]
</div>
**LLM Docstring**

Open the backing file as a stream, seeding it from the buffer in write modes.
  - `:returns`: `_`
    > the open stream


<a id="McUtils.Devutils.FileHelpers.FileBackedIO.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L665)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers/FileBackedIO.py#L665?message=Update%20Docs)]
</div>
**LLM Docstring**

Close the stream and (optionally) delete the backing file.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/FileHelpers/FileBackedIO.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/FileHelpers/FileBackedIO.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/FileHelpers/FileBackedIO.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/FileHelpers/FileBackedIO.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L556?message=Update%20Docs)   
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