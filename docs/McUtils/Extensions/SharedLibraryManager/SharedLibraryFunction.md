## <a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction">SharedLibraryFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager.py#L134)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager.py#L134?message=Update%20Docs)]
</div>

An object that provides a way to call into a shared library function







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, shared_library, signature: McUtils.Extensions.ArgumentSignature.FunctionSignature, defaults=None, docstring=None, call_directory=None, return_handler=None, prep_args=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager.py#L139)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager.py#L139?message=Update%20Docs)]
</div>

  - `shared_library`: `str |`
    > the path to the shared library file you want to use
  - `function_signature`: `FunctionSignature`
    > the signature of the function to load
  - `call_directory`: `str`
    > the directory for calling
  - `docstring`: `str`
    > the docstring for the function


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.construct" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct(cls, name, lib, docstring=None, defaults=None, return_type=None, return_handler=None, **args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L174)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L174?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a shared-library function from a name and keyword type specifications.

The current implementation evaluates `name ** args` before calling `FunctionSignature.construct`, rather than forwarding `name, **args`; ordinary string names and dictionaries will therefore raise `TypeError` before construction.
  - `name`: `Any`
    > left operand used by the current exponentiation expression

  - `lib`: `str | ctypes.CDLL | SharedLibraryLoader`
    > library source

  - `docstring`: `str | None`
    > optional function documentation

  - `defaults`: `dict | None`
    > argument defaults

  - `return_type`: `Any | None`
    > return type specification

  - `return_handler`: `Callable | None`
    > postprocessor receiving the raw result and prepared arguments

  - `args`: `dict[str, Any]`
    > argument type specifications used as the exponentiation right operand

  - `:returns`: `SharedLibraryFunction`
    > constructed wrapper if the current expression succeeds


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.function" class="docs-object-method">&nbsp;</a> 
```python
@property
function(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L228)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L228?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize and return the underlying `ctypes` function.
  - `:returns`: `ctypes._CFuncPtr`
    > configured foreign function


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.initialize" class="docs-object-method">&nbsp;</a> 
```python
initialize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L240)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L240?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve the function from the library and apply its return and argument type declarations.

Initialization is performed only once and cached in `_fun`.
  - `:returns`: `None`
    > no value is returned


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.doc" class="docs-object-method">&nbsp;</a> 
```python
doc(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L260)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L260?message=Update%20Docs)]
</div>
**LLM Docstring**

Combine the generated C/C++ signature with the stored documentation string.
  - `:returns`: `str`
    > signature and documentation separated by a newline


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L270)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L270?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation containing the signature and loaded library.
  - `:returns`: `str`
    > representation string


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.signature" class="docs-object-method">&nbsp;</a> 
```python
@property
signature(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L285)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L285?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the stored function signature.
  - `:returns`: `FunctionSignature`
    > function signature


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.uncast" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
uncast(cls, res): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L316)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L316?message=Update%20Docs)]
</div>
**LLM Docstring**

Unwrap common `ctypes` by-reference and scalar containers.

Objects with `_obj` are replaced by that object; objects with `value` are then replaced by their Python value.
  - `res`: `Any`
    > result to unwrap

  - `:returns`: `Any`
    > unwrapped value


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.call" class="docs-object-method">&nbsp;</a> 
```python
call(self, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L363)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L363?message=Update%20Docs)]
</div>
Calls the function we loaded.
This will be parallelized out to handle more complicated usages.
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L381)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L381?message=Update%20Docs)]
</div>
**LLM Docstring**

Forward a normal Python call to `call`.
  - `args`: `tuple`
    > positional function arguments

  - `kwargs`: `dict`
    > keyword function arguments

  - `:returns`: `Any`
    > postprocessed foreign-function result
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager.py#L134?message=Update%20Docs)   
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