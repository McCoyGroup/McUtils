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
**LLM Docstring**

Initialize checkpoint location, key filters, nested-open depth, and stream state.
  - `checkpoint_file`: `object`
    > path or file-like checkpoint target
  - `allowed_keys`: `object`
    > optional whitelist of permitted top-level keys
  - `omitted_keys`: `object`
    > optional blacklist of top-level keys
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L51)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L51?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the concrete checkpointer type and checkpoint target.
  - `:returns`: `str`
    > A human-readable string representation.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.extension_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
extension_map(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L63)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L63?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the extension-to-checkpointer dispatch table, honoring a class-level override when present.
  - `:returns`: `dict[str, type[Checkpointer]]`
    > a mapping from filename extensions to concrete checkpointer classes


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.build_canonical" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
build_canonical(cls, checkpoint): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L78)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L78?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L116)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L116?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L143)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L143?message=Update%20Docs)]
</div>
**LLM Docstring**

Increment the nested-open count and lazily open the checkpoint stream on the outermost entry.
  - `:returns`: `object`
    > The active context object.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L156?message=Update%20Docs)]
</div>
**LLM Docstring**

Decrement the nested-open count and close the stream after the outermost context exits.
  - `exc_type`: `object`
    > exception type passed by the context manager protocol
  - `exc_val`: `object`
    > exception instance passed by the context manager protocol
  - `exc_tb`: `object`
    > traceback passed by the context manager protocol
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.cached_eval" class="docs-object-method">&nbsp;</a> 
```python
cached_eval(self, key, generator, *, condition=None, args=(), kwargs=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L177)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L177?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate or load a keyed value through `dev.cached_eval`, using this checkpointer as the mapping backend.
  - `key`: `object`
    > the storage or lookup key
  - `generator`: `object`
    > callable used to produce a missing cached value
  - `condition`: `object`
    > optional predicate controlling cache reuse
  - `args`: `object`
    > positional arguments forwarded to a callable
  - `kwargs`: `object`
    > keyword arguments forwarded to a callable
  - `:returns`: `object`
    > the cached value when valid, otherwise the newly generated and stored value


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.is_open" class="docs-object-method">&nbsp;</a> 
```python
@property
is_open(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L208)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L208?message=Update%20Docs)]
</div>
**LLM Docstring**

Report whether a checkpoint stream is currently open.
  - `:returns`: `bool`
    > Whether the tested condition is satisfied.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.stream" class="docs-object-method">&nbsp;</a> 
```python
@property
stream(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L220)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L220?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the currently open stream, or `None` outside an active context.
  - `:returns`: `object | None`
    > the current backend stream, or `None` when closed


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.open_checkpoint_file" class="docs-object-method">&nbsp;</a> 
```python
open_checkpoint_file(self, chk): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L232)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L232?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L242)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L242?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L252)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L252?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L264)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L264?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L275)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L275?message=Update%20Docs)]
</div>
**LLM Docstring**

Default deletion hook; concrete checkpointers must override it to support deletion.
  - `key`: `object`
    > the storage or lookup key
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.check_parameter" class="docs-object-method">&nbsp;</a> 
```python
check_parameter(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L287?message=Update%20Docs)]
</div>
**LLM Docstring**

Validate the key policy and test whether loading the key succeeds.
  - `key`: `object`
    > the storage or lookup key
  - `:returns`: `bool`
    > Whether the tested condition is satisfied.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.update" class="docs-object-method">&nbsp;</a> 
```python
update(self, vals): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L306)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L306?message=Update%20Docs)]
</div>
**LLM Docstring**

Write all key/value pairs from a mapping or iterable, opening the checkpoint around the operation when needed.
  - `vals`: `object`
    > mapping or iterable of key/value pairs
  - `:returns`: `None | object`
    > No explicit value unless noted by the underlying delegated operation.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.get_keys" class="docs-object-method">&nbsp;</a> 
```python
get_keys(self, keys): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L326)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L326?message=Update%20Docs)]
</div>
**LLM Docstring**

Load a sequence of keys in order, with automatic context management.
  - `keys`: `object`
    > keys to load, save, or filter
  - `:returns`: `list[object]`
    > values loaded for `keys` in the same order


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.check_allowed_key" class="docs-object-method">&nbsp;</a> 
```python
check_allowed_key(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L345)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L345?message=Update%20Docs)]
</div>
**LLM Docstring**

Enforce top-level allow and omit lists; tuple paths are checked by their first component.
  - `item`: `object`
    > the lookup key or index
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L373)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L373?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether a permitted key exists, opening the checkpoint temporarily if required.
  - `key`: `object`
    > the storage or lookup key
  - `:returns`: `bool`
    > Whether the tested condition is satisfied.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L389)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L389?message=Update%20Docs)]
</div>
**LLM Docstring**

Validate and load a key, automatically managing the stream lifecycle.
  - `item`: `object`
    > the lookup key or index
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.get" class="docs-object-method">&nbsp;</a> 
```python
get(self, key, default=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L405)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L405?message=Update%20Docs)]
</div>
**LLM Docstring**

Load a key and return `default` when the backend raises `KeyError`.
  - `key`: `object`
    > the storage or lookup key
  - `default`: `object`
    > the fallback returned when a key is absent
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L423)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L423?message=Update%20Docs)]
</div>
**LLM Docstring**

Validate and save a key/value pair, opening the checkpoint temporarily if required.
  - `key`: `object`
    > the storage or lookup key
  - `value`: `object`
    > the value to store
  - `:returns`: `None | object`
    > No explicit value unless noted by the underlying delegated operation.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__delitem__" class="docs-object-method">&nbsp;</a> 
```python
__delitem__(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L442)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L442?message=Update%20Docs)]
</div>
**LLM Docstring**

Validate and delete a key, opening the checkpoint temporarily if required.
  - `key`: `object`
    > the storage or lookup key
  - `:returns`: `None`
    > no explicit value; the selected key is removed


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.pop" class="docs-object-method">&nbsp;</a> 
```python
pop(self, key, *default): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L458)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L458?message=Update%20Docs)]
</div>
**LLM Docstring**

Load and delete a key, optionally returning a supplied default when the key is absent.
  - `key`: `object`
    > the storage or lookup key
  - `default`: `object`
    > the fallback returned when a key is absent
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L483)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/Checkpointer.py#L483?message=Update%20Docs)]
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