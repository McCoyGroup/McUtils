## <a id="McUtils.Devutils.Loggers.Logger">Logger</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers.py#L332)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L332?message=Update%20Docs)]
</div>

Defines a simple logger object to write log data to a file based on log levels.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
LogLevel: LogLevel
default_verbosity: LogLevel
```
<a id="McUtils.Devutils.Loggers.Logger.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, log_file=None, log_level=None, print_function=None, padding='', newline='\n', repad_messages=True, block_options=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers.py#L341)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L341?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a logger that writes to a file (or stdout) based on log levels.
  - `log_file`: `str | None`
    > the log file path (stdout if omitted)
  - `log_level`: `Any`
    > the verbosity threshold
  - `print_function`: `Callable | None`
    > the print callable (defaults to `print`)
  - `padding`: `str`
    > the per-line prefix padding
  - `newline`: `str`
    > the newline string
  - `repad_messages`: `bool`
    > re-pad newlines within message arguments
  - `block_options`: `dict | None`
    > default options for `block`


<a id="McUtils.Devutils.Loggers.Logger.to_state" class="docs-object-method">&nbsp;</a> 
```python
to_state(self, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L382)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L382?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the serializable state of the logger (dropping the print function when
it's the builtin `print`).
  - `serializer`: `Any`
    > an optional serializer
  - `:returns`: `dict`
    > the state dict


<a id="McUtils.Devutils.Loggers.Logger.from_state" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_state(cls, state, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L400)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L400?message=Update%20Docs)]
</div>
**LLM Docstring**

Rebuild a logger from its serialized state.
  - `state`: `dict`
    > the state dict
  - `serializer`: `Any`
    > an optional serializer
  - `:returns`: `Logger`
    > the logger


<a id="McUtils.Devutils.Loggers.Logger.block" class="docs-object-method">&nbsp;</a> 
```python
block(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L415)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L415?message=Update%20Docs)]
</div>
**LLM Docstring**

Open a nested logging block on this logger.
  - `kwargs`: `Any`
    > options forwarded to `LoggingBlock` (merged with the defaults)
  - `:returns`: `LoggingBlock`
    > the logging block


<a id="McUtils.Devutils.Loggers.Logger.register" class="docs-object-method">&nbsp;</a> 
```python
register(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L427)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L427?message=Update%20Docs)]
</div>
Registers the logger under the given key
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Devutils.Loggers.Logger.lookup" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lookup(cls, key, construct=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L436)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L436?message=Update%20Docs)]
</div>
Looks up a logger. Has the convenient, but potentially surprising
behavior that if no logger is found a `NullLogger` is returned.
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Devutils.Loggers.Logger.preformat_keys" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
preformat_keys(key_functions): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L470)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L470?message=Update%20Docs)]
</div>
Generates a closure that will take the supplied
keys/function pairs and update them appropriately
  - `key_functions`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Devutils.Loggers.Logger.format_message" class="docs-object-method">&nbsp;</a> 
```python
format_message(self, message, *params, preformatter=None, _repad=None, _newline=None, _padding=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L502)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L502?message=Update%20Docs)]
</div>
**LLM Docstring**

Format a message template with the given parameters, optionally running a
preformatter over the arguments and re-padding multi-line string arguments.
  - `message`: `str`
    > the message template
  - `params`: `Any`
    > positional format arguments
  - `preformatter`: `Callable | None`
    > a callable transforming the arguments first
  - `_repad`: `bool | None`
    > re-pad newlines in string arguments
  - `_newline`: `Any`
    > the newline override
  - `_padding`: `Any`
    > the padding override
  - `kwargs`: `Any`
    > keyword format arguments
  - `:returns`: `str`
    > the formatted message


<a id="McUtils.Devutils.Loggers.Logger.format_metainfo" class="docs-object-method">&nbsp;</a> 
```python
format_metainfo(self, metainfo): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L554)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L554?message=Update%20Docs)]
</div>
**LLM Docstring**

Format block meta-information as a JSON string (or empty string when absent).
  - `metainfo`: `Any`
    > the meta-information
  - `:returns`: `str`
    > the formatted meta string


<a id="McUtils.Devutils.Loggers.Logger.pad_newlines" class="docs-object-method">&nbsp;</a> 
```python
pad_newlines(self, obj, padding=None, newline=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L570)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L570?message=Update%20Docs)]
</div>
**LLM Docstring**

Replace newlines in a value with the newline-plus-padding prefix so multi-line
output stays aligned under the current prompt.
  - `obj`: `Any`
    > the value (coerced to a string)
  - `padding`: `Any`
    > the padding (defaults to the logger's)
  - `newline`: `Any`
    > the newline (defaults to the logger's)
  - `kwargs`: `Any`
    > variables used to format the prefix
  - `:returns`: `str`
    > the re-padded string


<a id="McUtils.Devutils.Loggers.Logger.split_lines" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
split_lines(obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L589)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L589?message=Update%20Docs)]
</div>
**LLM Docstring**

Split a value's string form into lines.
  - `obj`: `Any`
    > the value
  - `:returns`: `list[str]`
    > the lines


<a id="McUtils.Devutils.Loggers.Logger.prep_array" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
prep_array(obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L601)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L601?message=Update%20Docs)]
</div>
**LLM Docstring**

Render a numpy array to lines without truncation (wide/high print limits).
  - `obj`: `Any`
    > the array
  - `:returns`: `list[str]`
    > the rendered lines


<a id="McUtils.Devutils.Loggers.Logger.prep_dict" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
prep_dict(obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L615)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L615?message=Update%20Docs)]
</div>
**LLM Docstring**

Render a dict as `key: value` lines.
  - `obj`: `Any`
    > the dict
  - `:returns`: `list[str]`
    > the rendered lines


<a id="McUtils.Devutils.Loggers.Logger.log_print" class="docs-object-method">&nbsp;</a> 
```python
log_print(self, message, *messrest, message_prepper=None, padding=None, newline=None, log_level=None, metainfo=None, print_function=None, print_options=None, sep=None, end=None, file=None, flush=None, preformatter=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L628)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L628?message=Update%20Docs)]
</div>

  - `message`: `str | Iterable[str]`
    > message to print
  - `params`: `Any`
    > 
  - `print_options`: `Any`
    > options to be passed through to print
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Devutils.Loggers.Logger.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L748)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L748?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the log file and verbosity.
  - `:returns`: `str`
    > the representation
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/Loggers/Logger.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/Loggers/Logger.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/Loggers/Logger.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/Loggers/Logger.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L332?message=Update%20Docs)   
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