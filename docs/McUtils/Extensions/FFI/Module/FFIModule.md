## <a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule">FFIModule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module.py#L419)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L419?message=Update%20Docs)]
</div>

Provides a layer to ingest a Python module containing an '_FFIModule' capsule.
The capsule is expected to point to a `plzffi::FFIModule` object and can be called using a `PotentialCaller`







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name=None, methods=None, module=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L425)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L425?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.captup" class="docs-object-method">&nbsp;</a> 
```python
@property
captup(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L433)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L433?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.from_lib" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_lib(cls, name, src=None, threaded=None, extra_compile_args=None, extra_link_args=None, linked_libs=None, **compile_kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L437)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L437?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.from_signature" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_signature(cls, sig, module=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L457)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L457?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.get_debug_level" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_debug_level(cls, debug): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L465)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L465?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.from_module" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_module(cls, module, debug=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L478)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L478?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.method_names" class="docs-object-method">&nbsp;</a> 
```python
@property
method_names(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L483)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L483?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.get_method" class="docs-object-method">&nbsp;</a> 
```python
get_method(self, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L487)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L487?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.call_method" class="docs-object-method">&nbsp;</a> 
```python
call_method(self, name, params, debug=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L498)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L498?message=Update%20Docs)]
</div>
Calls a method
  - `name`: `Any`
    > 
  - `params`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.call_method_threaded" class="docs-object-method">&nbsp;</a> 
```python
call_method_threaded(self, name, params, thread_var, mode='serial', debug=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L516)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L516?message=Update%20Docs)]
</div>
Calls a method with threading enabled
  - `name`: `Any`
    > 
  - `params`: `Any`
    > 
  - `thread_var`: `str`
    > 
  - `mode`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.__getattr__" class="docs-object-method">&nbsp;</a> 
```python
__getattr__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L542)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L542?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIModule.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L545)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L545?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/FFI/Module/FFIModule.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/FFI/Module/FFIModule.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/FFI/Module/FFIModule.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/FFI/Module/FFIModule.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L419?message=Update%20Docs)   
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