## <a id="McUtils.Extensions.FFI.Module.FFIModule">FFIModule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module.py#L788)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L788?message=Update%20Docs)]
</div>

Provides a layer to ingest a Python module containing an '_FFIModule' capsule.
The capsule is expected to point to a `plzffi::FFIModule` object and can be called using a `PotentialCaller`







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.FFI.Module.FFIModule.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name=None, methods=None, module=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module.py#L794)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L794?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct an FFI module wrapper, normalize method dictionaries, and bind every method back to this module.
  - `name`: `Any`
    > module name

  - `methods`: `Any`
    > method specifications

  - `module`: `Any`
    > underlying Python extension module

  - `:returns`: `None`
    > nothing; initializes the module wrapper


<a id="McUtils.Extensions.FFI.Module.FFIModule.captup" class="docs-object-method">&nbsp;</a> 
```python
@property
captup(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L819)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L819?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the extension module's `_FFIModule` capsule.
  - `:returns`: `object`
    > the native module capsule


<a id="McUtils.Extensions.FFI.Module.FFIModule.from_lib" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_lib(cls, name, src=None, threaded=None, extra_compile_args=None, extra_link_args=None, linked_libs=None, debug_level=False, **compile_kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L831)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L831?message=Update%20Docs)]
</div>
**LLM Docstring**

Compile or load an FFI extension through `FFILoader` and return its wrapped call object.
  - `name`: `Any`
    > library/module name

  - `src`: `Any`
    > source directory

  - `threaded`: `Any`
    > optional threaded-build override

  - `extra_compile_args`: `Any`
    > additional compiler arguments

  - `extra_link_args`: `Any`
    > additional linker arguments

  - `linked_libs`: `Any`
    > additional libraries

  - `debug_level`: `Any`
    > debug setting for the wrapper

  - `compile_kwargs`: `dict[str, Any]`
    > other `FFILoader` options

  - `:returns`: `FFIModule`
    > the loaded module wrapper


<a id="McUtils.Extensions.FFI.Module.FFIModule.from_signature" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_signature(cls, sig, module=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L885)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L885?message=Update%20Docs)]
</div>
**LLM Docstring**

Create a module wrapper from a native `(name, methods)` signature.
  - `sig`: `Any`
    > module signature tuple

  - `module`: `Any`
    > underlying extension module

  - `:returns`: `FFIModule`
    > the reconstructed wrapper


<a id="McUtils.Extensions.FFI.Module.FFIModule.get_debug_level" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_debug_level(cls, debug): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L907)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L907?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert booleans, enum names, enum values, and numeric values to the integer native debug level.
  - `debug`: `Any`
    > debug selector

  - `:returns`: `int | float`
    > the numeric debug level


<a id="McUtils.Extensions.FFI.Module.FFIModule.from_module" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_module(cls, module, debug=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L931)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L931?message=Update%20Docs)]
</div>
**LLM Docstring**

Query an extension module for its FFI signature and wrap it.
  - `module`: `Any`
    > extension exposing `get_signature` and `_FFIModule`

  - `debug`: `Any`
    > debug selector used while requesting the signature

  - `:returns`: `FFIModule`
    > the module wrapper


<a id="McUtils.Extensions.FFI.Module.FFIModule.method_names" class="docs-object-method">&nbsp;</a> 
```python
@property
method_names(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L950)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L950?message=Update%20Docs)]
</div>
**LLM Docstring**

Return method names in declaration order.
  - `:returns`: `tuple[str, ...]`
    > the available method names


<a id="McUtils.Extensions.FFI.Module.FFIModule.get_method" class="docs-object-method">&nbsp;</a> 
```python
get_method(self, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L962)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L962?message=Update%20Docs)]
</div>
**LLM Docstring**

Look up a method by name.
  - `name`: `Any`
    > method name

  - `:returns`: `FFIMethod`
    > the matching method; raises `AttributeError` when absent


<a id="McUtils.Extensions.FFI.Module.FFIModule.call_method" class="docs-object-method">&nbsp;</a> 
```python
call_method(self, name, params, debug=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L984)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L984?message=Update%20Docs)]
</div>
Calls a method
  - `name`: `Any`
    > 
  - `params`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.FFI.Module.FFIModule.call_method_threaded" class="docs-object-method">&nbsp;</a> 
```python
call_method_threaded(self, name, params, thread_var, mode='serial', debug=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L1002)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L1002?message=Update%20Docs)]
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


<a id="McUtils.Extensions.FFI.Module.FFIModule.__getattr__" class="docs-object-method">&nbsp;</a> 
```python
__getattr__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L1028)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L1028?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve unknown attributes as FFI methods.
  - `item`: `Any`
    > requested method name

  - `:returns`: `FFIMethod`
    > the matching method


<a id="McUtils.Extensions.FFI.Module.FFIModule.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIModule.py#L1042)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIModule.py#L1042?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation containing the module name and available method names.
  - `:returns`: `str`
    > the formatted module representation
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L788?message=Update%20Docs)   
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