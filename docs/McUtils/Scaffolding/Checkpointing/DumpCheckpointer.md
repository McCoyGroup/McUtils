## <a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer">DumpCheckpointer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing.py#L494)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing.py#L494?message=Update%20Docs)]
</div>

A subclass of `CheckpointerBase` that writes an entire dump to file at once & maintains
a backend cache to update it cleanly







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, file, cache=None, open_kwargs=None, allowed_keys=None, omitted_keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing.py#L499)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing.py#L499?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize a whole-file checkpointer with an in-memory backend cache and file-open options.
  - `file`: `object`
    > path or file-like object
  - `cache`: `object`
    > initial in-memory backend cache
  - `open_kwargs`: `object`
    > arguments used when opening a file target
  - `allowed_keys`: `object`
    > optional whitelist of permitted top-level keys
  - `omitted_keys`: `object`
    > optional blacklist of top-level keys
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.load_cache" class="docs-object-method">&nbsp;</a> 
```python
load_cache(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L526)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L526?message=Update%20Docs)]
</div>
**LLM Docstring**

Create an empty dictionary when no backend cache has been loaded.
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L537)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L537?message=Update%20Docs)]
</div>
**LLM Docstring**

Ensure the backend cache is loaded before opening the checkpoint stream.
  - `:returns`: `object`
    > The active context object.


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L548)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L548?message=Update%20Docs)]
</div>
**LLM Docstring**

Dump the entire cache before closing the stream, even when cleanup must run after a dump failure.
  - `exc_type`: `object`
    > exception type passed by the context manager protocol
  - `exc_val`: `object`
    > exception instance passed by the context manager protocol
  - `exc_tb`: `object`
    > traceback passed by the context manager protocol
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.dump" class="docs-object-method">&nbsp;</a> 
```python
dump(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L567)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L567?message=Update%20Docs)]
</div>
Writes the entire data structure
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L575)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L575?message=Update%20Docs)]
</div>
Converts the cache to an exportable form if needed
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.open_checkpoint_file" class="docs-object-method">&nbsp;</a> 
```python
open_checkpoint_file(self, chk): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L582)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L582?message=Update%20Docs)]
</div>
Opens the passed `checkpoint_file` (if not already open)
  - `chk`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.close_checkpoint_file" class="docs-object-method">&nbsp;</a> 
```python
close_checkpoint_file(self, stream): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L593)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L593?message=Update%20Docs)]
</div>
Closes the opened checkpointing stream
  - `stream`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.save_parameter" class="docs-object-method">&nbsp;</a> 
```python
save_parameter(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L603)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L603?message=Update%20Docs)]
</div>
Saves a parameter to the checkpoint file
  - `key`: `Any`
    > 
  - `value`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.check_parameter" class="docs-object-method">&nbsp;</a> 
```python
check_parameter(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L623)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L623?message=Update%20Docs)]
</div>
Loads a parameter from the checkpoint file
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.load_parameter" class="docs-object-method">&nbsp;</a> 
```python
load_parameter(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L641)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L641?message=Update%20Docs)]
</div>
Loads a parameter from the checkpoint file
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.delete_parameter" class="docs-object-method">&nbsp;</a> 
```python
delete_parameter(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L661)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L661?message=Update%20Docs)]
</div>
Loads a parameter from the checkpoint file
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L681)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.py#L681?message=Update%20Docs)]
</div>
**LLM Docstring**

Return top-level backend keys, opening the checkpointer temporarily if necessary.
  - `:returns`: `collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list`
    > A view or list of the requested registry, cache, checkpoint, or mapping entries.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Checkpointing.py#L494?message=Update%20Docs)   
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