## <a id="McUtils.Misc.DebugTools.ModificationTracker">ModificationTracker</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools.py#L27)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools.py#L27?message=Update%20Docs)]
</div>

A simple class to wrap an object to track when it is accessed or
modified







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Misc.DebugTools.ModificationTracker.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, obj, handlers=<ModificationTypeHandler.Log: 'log'>, logger=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools/ModificationTracker.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools/ModificationTracker.py#L32?message=Update%20Docs)]
</div>


<a id="McUtils.Misc.DebugTools.ModificationTracker.handler_dispatch" class="docs-object-method">&nbsp;</a> 
```python
@property
handler_dispatch(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools/ModificationTracker.py#L44)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools/ModificationTracker.py#L44?message=Update%20Docs)]
</div>


<a id="McUtils.Misc.DebugTools.ModificationTracker.log_modification" class="docs-object-method">&nbsp;</a> 
```python
log_modification(self, obj, handler_type, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools/ModificationTracker.py#L51)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools/ModificationTracker.py#L51?message=Update%20Docs)]
</div>
Logs on modification
  - `obj`: `Any`
    > 
  - `handler_type`: `Any`
    > 
  - `args`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Misc.DebugTools.ModificationTracker.raise_modification" class="docs-object-method">&nbsp;</a> 
```python
raise_modification(self, obj, handler_type, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools/ModificationTracker.py#L81)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools/ModificationTracker.py#L81?message=Update%20Docs)]
</div>
Raises an error on modification
  - `obj`: `Any`
    > 
  - `handler_type`: `Any`
    > 
  - `args`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Misc.DebugTools.ModificationTracker.__getattr__" class="docs-object-method">&nbsp;</a> 
```python
__getattr__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools/ModificationTracker.py#L125)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools/ModificationTracker.py#L125?message=Update%20Docs)]
</div>
Handler to intercept `getattr` requests
  - `item`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Misc.DebugTools.ModificationTracker.__setattr__" class="docs-object-method">&nbsp;</a> 
```python
__setattr__(self, item, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools/ModificationTracker.py#L137)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools/ModificationTracker.py#L137?message=Update%20Docs)]
</div>
Handler to intercept `setattr` requests
  - `item`: `Any`
    > 
  - `val`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Misc.DebugTools.ModificationTracker.__iadd__" class="docs-object-method">&nbsp;</a> 
```python
__iadd__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools/ModificationTracker.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools/ModificationTracker.py#L152?message=Update%20Docs)]
</div>
Handler to intercept `add` requests
  - `item`: `Any`
    > 
  - `val`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Misc.DebugTools.ModificationTracker.__isub__" class="docs-object-method">&nbsp;</a> 
```python
__isub__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools/ModificationTracker.py#L167)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools/ModificationTracker.py#L167?message=Update%20Docs)]
</div>
Handler to intercept `sub` requests
  - `item`: `Any`
    > 
  - `val`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Misc.DebugTools.ModificationTracker.__imul__" class="docs-object-method">&nbsp;</a> 
```python
__imul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools/ModificationTracker.py#L182)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools/ModificationTracker.py#L182?message=Update%20Docs)]
</div>
Handler to intercept `div` requests
  - `item`: `Any`
    > 
  - `val`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Misc.DebugTools.ModificationTracker.__idiv__" class="docs-object-method">&nbsp;</a> 
```python
__idiv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools/ModificationTracker.py#L197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools/ModificationTracker.py#L197?message=Update%20Docs)]
</div>
Handler to intercept `div` requests
  - `item`: `Any`
    > 
  - `val`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Misc.DebugTools.ModificationTracker.__imatmul__" class="docs-object-method">&nbsp;</a> 
```python
__imatmul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/DebugTools/ModificationTracker.py#L212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools/ModificationTracker.py#L212?message=Update%20Docs)]
</div>
Handler to intercept `matmul` requests
  - `item`: `Any`
    > 
  - `val`: `Any`
    > 
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Misc/DebugTools/ModificationTracker.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Misc/DebugTools/ModificationTracker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Misc/DebugTools/ModificationTracker.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Misc/DebugTools/ModificationTracker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/DebugTools.py#L27?message=Update%20Docs)   
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