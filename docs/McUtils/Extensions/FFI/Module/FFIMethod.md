## <a id="McUtils.Extensions.FFI.Module.FFIMethod">FFIMethod</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module.py#L539)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L539?message=Update%20Docs)]
</div>

Represents a C++ method callable through the plzffi interface







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.FFI.Module.FFIMethod.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name=None, arguments=None, rtype=None, vectorized=None, module=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module.py#L544)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L544?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a callable method specification and bind each argument dictionary to `FFIArgument`.
  - `name`: `Any`
    > method name

  - `arguments`: `Any`
    > argument specifications

  - `rtype`: `Any`
    > numeric FFI return-type code

  - `vectorized`: `Any`
    > whether the method returns vectorized output

  - `module`: `Any`
    > module used to dispatch calls

  - `:returns`: `None`
    > nothing; initializes the method metadata


<a id="McUtils.Extensions.FFI.Module.FFIMethod.bind_module" class="docs-object-method">&nbsp;</a> 
```python
bind_module(self, mod): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L574)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L574?message=Update%20Docs)]
</div>
**LLM Docstring**

Attach the module that will execute this method.
  - `mod`: `Any`
    > FFI module wrapper

  - `:returns`: `None`
    > nothing; updates `self.mod`


<a id="McUtils.Extensions.FFI.Module.FFIMethod.arg_names" class="docs-object-method">&nbsp;</a> 
```python
@property
arg_names(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L588)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L588?message=Update%20Docs)]
</div>
**LLM Docstring**

Return argument names in declaration order.
  - `:returns`: `tuple[str, ...]`
    > the method argument names


<a id="McUtils.Extensions.FFI.Module.FFIMethod.collect_args_from_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
collect_args_from_list(cls, arg_list, *args, excluded_args=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L600)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L600?message=Update%20Docs)]
</div>
**LLM Docstring**

Match positional and keyword values to argument specifications, cast them, and reject missing required arguments.
  - `arg_list`: `Any`
    > ordered argument specifications

  - `excluded_args`: `Any`
    > argument names to omit from required-value checks

  - `args`: `tuple[Any, ...]`
    > positional argument values

  - `kwargs`: `dict[str, Any]`
    > keyword argument values

  - `:returns`: `collections.OrderedDict[str, FFIParameter]`
    > cast parameters in supplied order


<a id="McUtils.Extensions.FFI.Module.FFIMethod.collect_args" class="docs-object-method">&nbsp;</a> 
```python
collect_args(self, *args, excluded_args=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L651)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L651?message=Update%20Docs)]
</div>
**LLM Docstring**

Collect and cast values using this method's declared arguments.
  - `excluded_args`: `Any`
    > argument names to omit

  - `args`: `tuple[Any, ...]`
    > positional argument values

  - `kwargs`: `dict[str, Any]`
    > keyword argument values

  - `:returns`: `collections.OrderedDict[str, FFIParameter]`
    > the prepared parameter mapping


<a id="McUtils.Extensions.FFI.Module.FFIMethod.from_signature" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_signature(cls, sig, module=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L671)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L671?message=Update%20Docs)]
</div>
**LLM Docstring**

Create a method specification from the four-part native signature tuple.
  - `sig`: `Any`
    > `(name, arguments, return_type, vectorized)` signature tuple

  - `module`: `Any`
    > optional module to bind

  - `:returns`: `FFIMethod`
    > the reconstructed method specification


<a id="McUtils.Extensions.FFI.Module.FFIMethod.call" class="docs-object-method">&nbsp;</a> 
```python
call(self, *args, debug=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L696)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L696?message=Update%20Docs)]
</div>
**LLM Docstring**

Collect arguments and dispatch a non-threaded call through the bound module.
  - `debug`: `Any`
    > debug level selector passed to the module

  - `args`: `tuple[Any, ...]`
    > positional argument values

  - `kwargs`: `dict[str, Any]`
    > keyword argument values

  - `:returns`: `Any`
    > the native method result


<a id="McUtils.Extensions.FFI.Module.FFIMethod.call_threaded" class="docs-object-method">&nbsp;</a> 
```python
call_threaded(self, *args, threading_var=None, threading_mode='serial', debug=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L716)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L716?message=Update%20Docs)]
</div>
**LLM Docstring**

Collect arguments and dispatch through the module's threaded call path.
  - `threading_var`: `Any`
    > argument name used to partition work

  - `threading_mode`: `Any`
    > threading backend name or mode

  - `debug`: `Any`
    > debug level selector

  - `args`: `tuple[Any, ...]`
    > positional argument values

  - `kwargs`: `dict[str, Any]`
    > keyword argument values

  - `:returns`: `Any`
    > the threaded native method result


<a id="McUtils.Extensions.FFI.Module.FFIMethod.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, *args, threading_var=None, threading_mode='serial', debug=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L742)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L742?message=Update%20Docs)]
</div>
**LLM Docstring**

Dispatch serially unless a threading variable or non-serial threading mode is requested.
  - `threading_var`: `Any`
    > optional partitioning argument name

  - `threading_mode`: `Any`
    > threading backend or `serial`

  - `debug`: `Any`
    > debug level selector

  - `args`: `tuple[Any, ...]`
    > positional argument values

  - `kwargs`: `dict[str, Any]`
    > keyword argument values

  - `:returns`: `Any`
    > the native method result


<a id="McUtils.Extensions.FFI.Module.FFIMethod.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L772)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIMethod.py#L772?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation of the method name, argument specs, and scalar or vectorized return type.
  - `:returns`: `str`
    > the formatted method representation
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L539?message=Update%20Docs)   
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