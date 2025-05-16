## <a id="McUtils.Scaffolding.Checkpointing.DictCheckpointer">DictCheckpointer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing.py#L493)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing.py#L493?message=Update%20Docs)]
</div>

A checkpointer that doesn't actually do anything, but which is provided
so that programs can turn off checkpointing without changing their layout







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Scaffolding.Checkpointing.DictCheckpointer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, checkpoint_file=None, allowed_keys=None, omitted_keys=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DictCheckpointer.py#L498)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DictCheckpointer.py#L498?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.DictCheckpointer.open_checkpoint_file" class="docs-object-method">&nbsp;</a> 
```python
open_checkpoint_file(self, chk): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DictCheckpointer.py#L505)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DictCheckpointer.py#L505?message=Update%20Docs)]
</div>
Opens the passed `checkpoint_file` (if not already open)
  - `chk`: `str | file-like`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DictCheckpointer.close_checkpoint_file" class="docs-object-method">&nbsp;</a> 
```python
close_checkpoint_file(self, stream): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DictCheckpointer.py#L515)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DictCheckpointer.py#L515?message=Update%20Docs)]
</div>
Opens the passed `checkpoint_file` (if not already open)
  - `chk`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DictCheckpointer.save_parameter" class="docs-object-method">&nbsp;</a> 
```python
save_parameter(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DictCheckpointer.py#L525)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DictCheckpointer.py#L525?message=Update%20Docs)]
</div>
Saves a parameter to the checkpoint file
  - `key`: `Any`
    > 
  - `value`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DictCheckpointer.load_parameter" class="docs-object-method">&nbsp;</a> 
```python
load_parameter(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DictCheckpointer.py#L537)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DictCheckpointer.py#L537?message=Update%20Docs)]
</div>
Loads a parameter from the checkpoint file
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.DictCheckpointer.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/DictCheckpointer.py#L547)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/DictCheckpointer.py#L547?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Checkpointing/DictCheckpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Checkpointing/DictCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Checkpointing/DictCheckpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Checkpointing/DictCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing.py#L493?message=Update%20Docs)   
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