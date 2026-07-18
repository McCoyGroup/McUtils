## <a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunction">DynamicFFIFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L57)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L57?message=Update%20Docs)]
</div>

Specialization of base `SharedLibraryFunction` to call
through the `DynamicLibrary` module instead of `ctypes`







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
LibFFIMethodData: LibFFIMethodData
```
<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, shared_library, signature, defaults=None, docstring=None, call_directory=None, return_handler=None, prep_args=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L77)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L77?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize a shared-library function that dispatches through the dynamic FFI module.
  - `shared_library`: `Any`
    > library path or loader

  - `signature`: `Any`
    > function signature

  - `defaults`: `Any`
    > argument defaults

  - `docstring`: `Any`
    > optional function documentation

  - `call_directory`: `Any`
    > optional working directory

  - `return_handler`: `Any`
    > result postprocessor

  - `prep_args`: `Any`
    > keyword preprocessing callback

  - `:returns`: `None`
    > nothing; initializes lazy FFI metadata and call-state storage


<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunction.initialize" class="docs-object-method">&nbsp;</a> 
```python
initialize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L124)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L124?message=Update%20Docs)]
</div>
**LLM Docstring**

Ensure the caller module is loaded and translate signature arguments to `FFIArgument` objects.
  - `:returns`: `None`
    > nothing; initializes `_ffi_args` lazily


<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunction.function_data" class="docs-object-method">&nbsp;</a> 
```python
@property
function_data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L171)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L171?message=Update%20Docs)]
</div>
**LLM Docstring**

Build and cache the lightweight method metadata consumed by the dynamic caller.
  - `:returns`: `DynamicFFIFunction.LibFFIMethodData`
    > the cached call descriptor


<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunction.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, *args, debug=False, threading_vars=None, threading_mode=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L236?message=Update%20Docs)]
</div>
**LLM Docstring**

Queue debug and threading options for one call, then delegate argument preprocessing and return handling to the base class.
  - `debug`: `Any`
    > debug selector

  - `threading_vars`: `Any`
    > argument name or names used for threaded partitioning

  - `threading_mode`: `Any`
    > threading backend

  - `args`: `tuple[Any, ...]`
    > positional argument values

  - `kwargs`: `dict[str, Any]`
    > keyword argument values

  - `:returns`: `Any`
    > the postprocessed dynamic FFI result
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L57?message=Update%20Docs)   
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