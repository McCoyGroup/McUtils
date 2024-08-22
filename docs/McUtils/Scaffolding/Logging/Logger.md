## <a id="McUtils.Scaffolding.Logging.Logger">Logger</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging.py#L148)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging.py#L148?message=Update%20Docs)]
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
<a id="McUtils.Scaffolding.Logging.Logger.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, log_file=None, log_level=None, print_function=None, padding='', newline='\n', repad_messages=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L157)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L157?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.Logger.to_state" class="docs-object-method">&nbsp;</a> 
```python
to_state(self, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L176)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L176?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.Logger.from_state" class="docs-object-method">&nbsp;</a> 
```python
from_state(state, serializer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L184)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L184?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.Logger.block" class="docs-object-method">&nbsp;</a> 
```python
block(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L188?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.Logger.register" class="docs-object-method">&nbsp;</a> 
```python
register(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L191?message=Update%20Docs)]
</div>
Registers the logger under the given key
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Logging.Logger.lookup" class="docs-object-method">&nbsp;</a> 
```python
lookup(key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L200)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L200?message=Update%20Docs)]
</div>
Looks up a logger. Has the convenient, but potentially surprising
behavior that if no logger is found a `NullLogger` is returned.
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Logging.Logger.preformat_keys" class="docs-object-method">&nbsp;</a> 
```python
preformat_keys(key_functions): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L231)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L231?message=Update%20Docs)]
</div>
Generates a closure that will take the supplied
keys/function pairs and update them appropriately
  - `key_functions`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Logging.Logger.format_message" class="docs-object-method">&nbsp;</a> 
```python
format_message(self, message, *params, preformatter=None, _repad=None, _newline=None, _padding=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L252)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L252?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.Logger.format_metainfo" class="docs-object-method">&nbsp;</a> 
```python
format_metainfo(self, metainfo): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L285)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L285?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.Logger.pad_newlines" class="docs-object-method">&nbsp;</a> 
```python
pad_newlines(self, obj, padding=None, newline=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L292)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L292?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.Logger.split_lines" class="docs-object-method">&nbsp;</a> 
```python
split_lines(obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L298)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L298?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.Logger.prep_array" class="docs-object-method">&nbsp;</a> 
```python
prep_array(obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L301)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L301?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.Logger.prep_dict" class="docs-object-method">&nbsp;</a> 
```python
prep_dict(obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L306)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L306?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.Logger.log_print" class="docs-object-method">&nbsp;</a> 
```python
log_print(self, message, *messrest, message_prepper=None, padding=None, newline=None, log_level=None, metainfo=None, print_function=None, print_options=None, sep=None, end=None, file=None, flush=None, preformatter=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L310)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L310?message=Update%20Docs)]
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


<a id="McUtils.Scaffolding.Logging.Logger.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Logging/Logger.py#L410)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging/Logger.py#L410?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Scaffolding/Logging/Logger.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Scaffolding/Logging/Logger.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Scaffolding/Logging/Logger.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Scaffolding/Logging/Logger.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Logging.py#L148?message=Update%20Docs)   
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