## <a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer">DumpCheckpointer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing.py#L215)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing.py#L215?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L220)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L220?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.load_cache" class="docs-object-method">&nbsp;</a> 
```python
load_cache(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L229)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L229?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L232)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L232?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L235)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L235?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.dump" class="docs-object-method">&nbsp;</a> 
```python
dump(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L240)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L240?message=Update%20Docs)]
</div>
Writes the entire data structure
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L248)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L248?message=Update%20Docs)]
</div>
Converts the cache to an exportable form if needed
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.open_checkpoint_file" class="docs-object-method">&nbsp;</a> 
```python
open_checkpoint_file(self, chk): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L255)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L255?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L266)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L266?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L276)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L276?message=Update%20Docs)]
</div>
Saves a parameter to the checkpoint file
  - `key`: `Any`
    > 
  - `value`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DumpCheckpointer.load_parameter" class="docs-object-method">&nbsp;</a> 
```python
load_parameter(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L296)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L296?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L316)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DumpCheckpointer.py#L316?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Checkpointing/DumpCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing.py#L215?message=Update%20Docs)   
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