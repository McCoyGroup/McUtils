## <a id="McUtils.Scaffolding.Checkpointing.Checkpointer">Checkpointer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing.py#L20?message=Update%20Docs)]
</div>

General purpose base class that allows checkpointing to be done easily and cleanly.
Intended to be a passable object that allows code to checkpoint easily.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_extension: str
```
<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, checkpoint_file, allowed_keys=None, omitted_keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing.py#L27)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing.py#L27?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L37?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.extension_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
extension_map(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L41)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L41?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.build_canonical" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
build_canonical(cls, checkpoint): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L48?message=Update%20Docs)]
</div>
Dispatches over types of objects to make a canonical checkpointer
from the supplied data
  - `checkpoint`: `None | str | Checkpoint | file | dict`
    > provides
  - `:returns`: `Checkpointer`
    >


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.from_file" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_file(cls, file, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L86)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L86?message=Update%20Docs)]
</div>
Dispatch function to load from the appropriate file
  - `file`: `str | File`
    > 
  - `opts`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L113)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L113?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L118)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L118?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.cached_eval" class="docs-object-method">&nbsp;</a> 
```python
cached_eval(self, key, generator, *, condition=None, args=(), kwargs=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L125)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L125?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.is_open" class="docs-object-method">&nbsp;</a> 
```python
@property
is_open(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L138)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L138?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.stream" class="docs-object-method">&nbsp;</a> 
```python
@property
stream(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L142)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L142?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.open_checkpoint_file" class="docs-object-method">&nbsp;</a> 
```python
open_checkpoint_file(self, chk): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L146)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L146?message=Update%20Docs)]
</div>
Opens the passed `checkpoint_file` (if not already open)
  - `chk`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.close_checkpoint_file" class="docs-object-method">&nbsp;</a> 
```python
close_checkpoint_file(self, stream): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L156?message=Update%20Docs)]
</div>
Closes the opened checkpointing stream
  - `stream`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.save_parameter" class="docs-object-method">&nbsp;</a> 
```python
save_parameter(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L166)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L166?message=Update%20Docs)]
</div>
Saves a parameter to the checkpoint file
  - `key`: `Any`
    > 
  - `value`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.load_parameter" class="docs-object-method">&nbsp;</a> 
```python
load_parameter(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L178)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L178?message=Update%20Docs)]
</div>
Loads a parameter from the checkpoint file
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.delete_parameter" class="docs-object-method">&nbsp;</a> 
```python
delete_parameter(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L189)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L189?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.check_parameter" class="docs-object-method">&nbsp;</a> 
```python
check_parameter(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L191?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.update" class="docs-object-method">&nbsp;</a> 
```python
update(self, vals): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L200)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L200?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.get_keys" class="docs-object-method">&nbsp;</a> 
```python
get_keys(self, keys): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L210)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L210?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.check_allowed_key" class="docs-object-method">&nbsp;</a> 
```python
check_allowed_key(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L219)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L219?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L237)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L237?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L243)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L243?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.get" class="docs-object-method">&nbsp;</a> 
```python
get(self, key, default=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L249)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L249?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L255)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L255?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__delitem__" class="docs-object-method">&nbsp;</a> 
```python
__delitem__(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L262)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L262?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.pop" class="docs-object-method">&nbsp;</a> 
```python
pop(self, key, *default): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L268)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L268?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L281)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L281?message=Update%20Docs)]
</div>
Returns the keys of currently checkpointed
objects
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Checkpointing/Checkpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Checkpointing/Checkpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Checkpointing/Checkpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Checkpointing/Checkpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing.py#L20?message=Update%20Docs)   
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