## <a id="McUtils.McUtils.Devutils.Loggers.Logger">Logger</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers.py#L147)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L147?message=Update%20Docs)]
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
<a id="McUtils.McUtils.Devutils.Loggers.Logger.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, log_file=None, log_level=None, print_function=None, padding='', newline='\n', repad_messages=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L156?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Devutils.Loggers.Logger.to_state" class="docs-object-method">&nbsp;</a> 
```python
to_state(self, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L175?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Devutils.Loggers.Logger.from_state" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_state(cls, state, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L183?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Devutils.Loggers.Logger.block" class="docs-object-method">&nbsp;</a> 
```python
block(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L187)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L187?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Devutils.Loggers.Logger.register" class="docs-object-method">&nbsp;</a> 
```python
register(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L190)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L190?message=Update%20Docs)]
</div>
Registers the logger under the given key
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Devutils.Loggers.Logger.lookup" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lookup(cls, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L199)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L199?message=Update%20Docs)]
</div>
Looks up a logger. Has the convenient, but potentially surprising
behavior that if no logger is found a `NullLogger` is returned.
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Devutils.Loggers.Logger.preformat_keys" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
preformat_keys(key_functions): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L230)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L230?message=Update%20Docs)]
</div>
Generates a closure that will take the supplied
keys/function pairs and update them appropriately
  - `key_functions`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Devutils.Loggers.Logger.format_message" class="docs-object-method">&nbsp;</a> 
```python
format_message(self, message, *params, preformatter=None, _repad=None, _newline=None, _padding=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L251)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L251?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Devutils.Loggers.Logger.format_metainfo" class="docs-object-method">&nbsp;</a> 
```python
format_metainfo(self, metainfo): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L284)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L284?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Devutils.Loggers.Logger.pad_newlines" class="docs-object-method">&nbsp;</a> 
```python
pad_newlines(self, obj, padding=None, newline=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L291)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L291?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Devutils.Loggers.Logger.split_lines" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
split_lines(obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L297)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L297?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Devutils.Loggers.Logger.prep_array" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
prep_array(obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L300)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L300?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Devutils.Loggers.Logger.prep_dict" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
prep_dict(obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L305)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L305?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Devutils.Loggers.Logger.log_print" class="docs-object-method">&nbsp;</a> 
```python
log_print(self, message, *messrest, message_prepper=None, padding=None, newline=None, log_level=None, metainfo=None, print_function=None, print_options=None, sep=None, end=None, file=None, flush=None, preformatter=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L309)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L309?message=Update%20Docs)]
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


<a id="McUtils.McUtils.Devutils.Loggers.Logger.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/Logger.py#L409)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/Logger.py#L409?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L147?message=Update%20Docs)   
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