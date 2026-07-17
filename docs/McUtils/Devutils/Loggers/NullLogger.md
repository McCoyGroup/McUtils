## <a id="McUtils.Devutils.Loggers.NullLogger">NullLogger</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers.py#L763)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L763?message=Update%20Docs)]
</div>

A logger that implements the interface, but doesn't ever print.
Allows code to avoid a bunch of "if logger is not None" blocks







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Devutils.Loggers.NullLogger.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *log_files, **logger_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers.py#L768)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L768?message=Update%20Docs)]
</div>
**LLM Docstring**

A logger that implements the interface but never prints (so callers can avoid
`if logger is not None` checks).
  - `log_files`: `Any`
    > forwarded to `Logger`
  - `logger_opts`: `Any`
    > forwarded to `Logger`


<a id="McUtils.Devutils.Loggers.NullLogger.log_print" class="docs-object-method">&nbsp;</a> 
```python
log_print(self, message, *params, print_options=None, padding=None, newline=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/NullLogger.py#L780)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/NullLogger.py#L780?message=Update%20Docs)]
</div>
**LLM Docstring**

No-op: discards the message.
  - `message`: `Any`
    > the (ignored) message
  - `params`: `Any`
    > ignored positional arguments
  - `print_options`: `Any`
    > ignored
  - `padding`: `Any`
    > ignored
  - `newline`: `Any`
    > ignored
  - `kwargs`: `Any`
    > ignored


<a id="McUtils.Devutils.Loggers.NullLogger.__bool__" class="docs-object-method">&nbsp;</a> 
```python
__bool__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/NullLogger.py#L794)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/NullLogger.py#L794?message=Update%20Docs)]
</div>
**LLM Docstring**

A null logger is always falsy.
  - `:returns`: `bool`
    > `False`


<a id="McUtils.Devutils.Loggers.NullLogger.block" class="docs-object-method">&nbsp;</a> 
```python
block(self, capture_output=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/NullLogger.py#L804)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/NullLogger.py#L804?message=Update%20Docs)]
</div>
**LLM Docstring**

Open a logging block with output capture disabled by default.
  - `capture_output`: `bool`
    > capture stdout/stderr (off by default)
  - `kwargs`: `Any`
    > options forwarded to `Logger.block`
  - `:returns`: `LoggingBlock`
    > the logging block
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/Loggers/NullLogger.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/Loggers/NullLogger.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/Loggers/NullLogger.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/Loggers/NullLogger.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L763?message=Update%20Docs)   
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