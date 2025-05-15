## <a id="McUtils.McUtils.Extensions.FFI.Module.FFIMethod">FFIMethod</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module.py#L334)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L334?message=Update%20Docs)]
</div>

Represents a C++ method callable through the plzffi interface







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.McUtils.Extensions.FFI.Module.FFIMethod.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name=None, arguments=None, rtype=None, vectorized=None, module=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L339)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L339?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIMethod.bind_module" class="docs-object-method">&nbsp;</a> 
```python
bind_module(self, mod): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L346)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L346?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIMethod.arg_names" class="docs-object-method">&nbsp;</a> 
```python
@property
arg_names(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L349)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L349?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIMethod.collect_args_from_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
collect_args_from_list(cls, arg_list, *args, excluded_args=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L353)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L353?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIMethod.collect_args" class="docs-object-method">&nbsp;</a> 
```python
collect_args(self, *args, excluded_args=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L384)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L384?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIMethod.from_signature" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_signature(cls, sig, module=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L387)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L387?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIMethod.call" class="docs-object-method">&nbsp;</a> 
```python
call(self, *args, debug=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L398)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L398?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIMethod.call_threaded" class="docs-object-method">&nbsp;</a> 
```python
call_threaded(self, *args, threading_var=None, threading_mode='serial', debug=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L401)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L401?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIMethod.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, *args, threading_var=None, threading_mode='serial', debug=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L404)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L404?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIMethod.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L411)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L411?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/FFI/Module/FFIMethod.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/FFI/Module/FFIMethod.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/FFI/Module/FFIMethod.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/FFI/Module/FFIMethod.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L334?message=Update%20Docs)   
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