## <a id="McUtils.Devutils.Redirects.OutputRedirect">OutputRedirect</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects.py#L155)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects.py#L155?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Devutils.Redirects.OutputRedirect.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, redirect=True, stdout=None, stderr=None, capture_output=False, capture_errors=None, file_handles=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects.py#L156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects.py#L156?message=Update%20Docs)]
</div>
**LLM Docstring**

Context manager that redirects `stdout`/`stderr`, optionally capturing them to
in-memory buffers, files, or discarding them.
  - `redirect`: `bool`
    > whether to actually redirect
  - `stdout`: `Any`
    > an explicit stdout target (stream or file path)
  - `stderr`: `Any`
    > an explicit stderr target (stream or file path)
  - `capture_output`: `bool`
    > capture stdout to a buffer/temp file
  - `capture_errors`: `bool | None`
    > capture stderr (defaults to `capture_output`)
  - `file_handles`: `bool`
    > use file handles rather than in-memory buffers when capturing


<a id="McUtils.Devutils.Redirects.OutputRedirect.get_handle" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_handle(cls, handles=None, file_handles=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L196)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L196?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a capture target: return the supplied handle, a fresh in-memory buffer,
or `None` (for a file handle to be created later).
  - `handles`: `Any`
    > an explicit handle
  - `file_handles`: `bool`
    > prefer a file handle (returns `None`) over a buffer
  - `:returns`: `_`
    > the capture handle, or `None`


<a id="McUtils.Devutils.Redirects.OutputRedirect.get_temp_stream" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_temp_stream(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L216)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L216?message=Update%20Docs)]
</div>
**LLM Docstring**

Open and enter a writable named temporary file to capture output into.
  - `:returns`: `_`
    > the temporary file stream


<a id="McUtils.Devutils.Redirects.OutputRedirect.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/OutputRedirect.py#L227)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/OutputRedirect.py#L227?message=Update%20Docs)]
</div>
**LLM Docstring**

Redirect `sys.stdout`/`sys.stderr` to the configured targets (buffers, temp
files, given streams/paths, or the null device), saving the originals.


<a id="McUtils.Devutils.Redirects.OutputRedirect.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/OutputRedirect.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/OutputRedirect.py#L271?message=Update%20Docs)]
</div>
**LLM Docstring**

Restore the original `sys.stdout`/`sys.stderr` and close any streams opened on
entry.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/Redirects/OutputRedirect.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/Redirects/OutputRedirect.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/Redirects/OutputRedirect.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/Redirects/OutputRedirect.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects.py#L155?message=Update%20Docs)   
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