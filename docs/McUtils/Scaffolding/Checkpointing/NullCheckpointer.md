## <a id="McUtils.Scaffolding.Checkpointing.NullCheckpointer">NullCheckpointer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing.py#L550)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing.py#L550?message=Update%20Docs)]
</div>

A checkpointer that saves absolutely nothing







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Scaffolding.Checkpointing.NullCheckpointer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, checkpoint_file=None, allowed_keys=None, omitted_keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/NullCheckpointer.py#L554)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/NullCheckpointer.py#L554?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.NullCheckpointer.open_checkpoint_file" class="docs-object-method">&nbsp;</a> 
```python
open_checkpoint_file(self, chk): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/NullCheckpointer.py#L561)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/NullCheckpointer.py#L561?message=Update%20Docs)]
</div>
Opens the passed `checkpoint_file` (if not already open)
  - `chk`: `str | file-like`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.NullCheckpointer.close_checkpoint_file" class="docs-object-method">&nbsp;</a> 
```python
close_checkpoint_file(self, stream): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/NullCheckpointer.py#L571)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/NullCheckpointer.py#L571?message=Update%20Docs)]
</div>
Opens the passed `checkpoint_file` (if not already open)
  - `chk`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.NullCheckpointer.save_parameter" class="docs-object-method">&nbsp;</a> 
```python
save_parameter(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/NullCheckpointer.py#L581)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/NullCheckpointer.py#L581?message=Update%20Docs)]
</div>
Saves a parameter to the checkpoint file
  - `key`: `Any`
    > 
  - `value`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.NullCheckpointer.load_parameter" class="docs-object-method">&nbsp;</a> 
```python
load_parameter(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/NullCheckpointer.py#L593)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/NullCheckpointer.py#L593?message=Update%20Docs)]
</div>
Loads a parameter from the checkpoint file
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.NullCheckpointer.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/NullCheckpointer.py#L603)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/NullCheckpointer.py#L603?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Checkpointing/NullCheckpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Checkpointing/NullCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Checkpointing/NullCheckpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Checkpointing/NullCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing.py#L550?message=Update%20Docs)   
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