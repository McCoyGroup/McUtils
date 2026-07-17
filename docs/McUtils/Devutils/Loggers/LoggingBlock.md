## <a id="McUtils.Devutils.Loggers.LoggingBlock">LoggingBlock</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers.py#L90)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L90?message=Update%20Docs)]
</div>

A class that extends the utility of a logger by automatically setting up a
named block of logs that add context and can be
that







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
block_settings: list
block_level_padding: str
```
<a id="McUtils.Devutils.Loggers.LoggingBlock.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, logger, log_level=None, block_level=0, block_level_padding=None, tag=None, opener=None, prompt=None, closer=None, printoptions=None, captured_output_tag='', capture_output=True, captured_error_tag='', capture_errors=None, **tag_vars): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers.py#L109)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L109?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a nested, tagged block of log output with its own verbosity, prompt, and
optional stdout/stderr capture.
  - `logger`: `Logger`
    > the owning logger
  - `log_level`: `Any`
    > the block's verbosity (defaults to the logger's)
  - `block_level`: `int`
    > the nesting depth (selects the opener/prompt/closer style)
  - `block_level_padding`: `Any`
    > the per-level indentation
  - `tag`: `Any`
    > the block tag (string, `(template, vars)`, or callable)
  - `opener`: `Any`
    > an explicit opener line
  - `prompt`: `Any`
    > an explicit per-line prompt
  - `closer`: `Any`
    > an explicit closer line
  - `printoptions`: `dict | None`
    > numpy print options to apply within the block
  - `captured_output_tag`: `str`
    > tag prefix for captured stdout
  - `capture_output`: `bool`
    > capture stdout within the block
  - `captured_error_tag`: `str`
    > tag prefix for captured stderr
  - `capture_errors`: `bool | None`
    > capture stderr (defaults to `capture_output`)
  - `tag_vars`: `Any`
    > variables used to format the tag


<a id="McUtils.Devutils.Loggers.LoggingBlock.tag" class="docs-object-method">&nbsp;</a> 
```python
@property
tag(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/LoggingBlock.py#L184)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/LoggingBlock.py#L184?message=Update%20Docs)]
</div>
**LLM Docstring**

The resolved (formatted) block tag, computed lazily from a string, a
`(template, vars)` pair, or a callable.
  - `:returns`: `str`
    > the tag string


<a id="McUtils.Devutils.Loggers.LoggingBlock.stream_redirect" class="docs-object-method">&nbsp;</a> 
```python
stream_redirect(self, tag, base_stream): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/LoggingBlock.py#L244)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/LoggingBlock.py#L244?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a `StreamRedirect` that routes writes through the logger with the given
tag.
  - `tag`: `str`
    > the tag prefix
  - `base_stream`: `Any`
    > the underlying stream
  - `:returns`: `redirects.StreamRedirect`
    > the stream redirect


<a id="McUtils.Devutils.Loggers.LoggingBlock.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/LoggingBlock.py#L260)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/LoggingBlock.py#L260?message=Update%20Docs)]
</div>
**LLM Docstring**

Open the block: print the opener, start output capture (if enabled and none is
already active), raise the logger's prompt/verbosity/nesting, and apply any
numpy print options.


<a id="McUtils.Devutils.Loggers.LoggingBlock.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/LoggingBlock.py#L301)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/LoggingBlock.py#L301?message=Update%20Docs)]
</div>
**LLM Docstring**

Close the block: stop output capture, print the closer, and restore the
logger's prompt, verbosity, and nesting.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/Loggers/LoggingBlock.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/Loggers/LoggingBlock.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/Loggers/LoggingBlock.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/Loggers/LoggingBlock.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L90?message=Update%20Docs)   
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