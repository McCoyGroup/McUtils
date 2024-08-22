## <a id="McUtils.Scaffolding.Checkpointing.Checkpointer">Checkpointer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing.py#L20?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L27)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L27?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L37?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.extension_map" class="docs-object-method">&nbsp;</a> 
```python
extension_map(): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L41)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L41?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.build_canonical" class="docs-object-method">&nbsp;</a> 
```python
build_canonical(checkpoint): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L48?message=Update%20Docs)]
</div>
Dispatches over types of objects to make a canonical checkpointer
from the supplied data
  - `checkpoint`: `None | str | Checkpoint | file | dict`
    > provides
  - `:returns`: `Checkpointer`
    >


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.from_file" class="docs-object-method">&nbsp;</a> 
```python
from_file(file, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L83)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L83?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L110?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L115?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.is_open" class="docs-object-method">&nbsp;</a> 
```python
@property
is_open(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L122)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L122?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.stream" class="docs-object-method">&nbsp;</a> 
```python
@property
stream(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L126)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L126?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.open_checkpoint_file" class="docs-object-method">&nbsp;</a> 
```python
open_checkpoint_file(self, chk): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L130?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L140)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L140?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L150)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L150?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L162)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L162?message=Update%20Docs)]
</div>
Loads a parameter from the checkpoint file
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.check_allowed_key" class="docs-object-method">&nbsp;</a> 
```python
check_allowed_key(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L173)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L173?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L191?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L197?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Checkpointing.Checkpointer.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Checkpointing/Checkpointer.py#L204)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing/Checkpointer.py#L204?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Scaffolding/Checkpointing/Checkpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Scaffolding/Checkpointing/Checkpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Scaffolding/Checkpointing/Checkpointer.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Scaffolding/Checkpointing/Checkpointer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Checkpointing.py#L20?message=Update%20Docs)   
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