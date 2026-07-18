## <a id="McUtils.Extensions.ArgumentSignature.FunctionSignature">FunctionSignature</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature.py#L890)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L890?message=Update%20Docs)]
</div>

Defines a function signature for a C-level caller.
To be used inside `SharedLibraryFunction` and things to manage the core interface.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name, *args, defaults=None, return_type=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature.py#L896)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L896?message=Update%20Docs)]
</div>

  - `name`: `str`
    > the name of the function
  - `args`: `Iterable[ArgumentType]`
    > the arguments passed to the function
  - `return_type`: `ArgumentType | None`
    > the return type of the function


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.construct" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct(cls, name, defaults=None, return_type=None, **args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L914)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L914?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a signature from keyword argument type specifications.

Keyword insertion order determines positional argument order.
  - `name`: `str`
    > function name

  - `defaults`: `dict | None`
    > default values keyed by argument name

  - `return_type`: `Any | None`
    > return type specification accepted by `Argument.infer_type`

  - `args`: `dict[str, Any]`
    > argument names mapped to type specifications

  - `:returns`: `FunctionSignature`
    > new function signature


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.build_argument" class="docs-object-method">&nbsp;</a> 
```python
build_argument(self, argtup, which=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L945)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L945?message=Update%20Docs)]
</div>
Converts an argument tuple into an Argument object
  - `argtup`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.args" class="docs-object-method">&nbsp;</a> 
```python
@property
args(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L968)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L968?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the immutable argument sequence.
  - `:returns`: `tuple[Argument, ...]`
    > the immutable argument sequence


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.return_argtype" class="docs-object-method">&nbsp;</a> 
```python
@property
return_argtype(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L979)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L979?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the resolved return `ArgumentType`.
  - `:returns`: `ArgumentType | None`
    > the resolved return `ArgumentType`


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.return_type" class="docs-object-method">&nbsp;</a> 
```python
@property
return_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L990)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L990?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the `ctypes` return type used to configure a foreign function.
  - `:returns`: `type | None`
    > the `ctypes` return type used to configure a foreign function


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.arg_types" class="docs-object-method">&nbsp;</a> 
```python
@property
arg_types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L1004)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L1004?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the ordered `ctypes` types for all arguments.
  - `:returns`: `list[type]`
    > the ordered `ctypes` types for all arguments


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.cpp_signature" class="docs-object-method">&nbsp;</a> 
```python
@property
cpp_signature(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L1016)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L1016?message=Update%20Docs)]
</div>
**LLM Docstring**

Format the complete C/C++-style function signature.
  - `:returns`: `str`
    > Format the complete C/C++-style function signature


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.populate_kwargs" class="docs-object-method">&nbsp;</a> 
```python
populate_kwargs(self, args, kwargs, defaults=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L1032)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L1032?message=Update%20Docs)]
</div>
**LLM Docstring**

Merge positional and keyword arguments and fill missing entries from defaults.

Explicit `defaults` override signature-level defaults, which override each `Argument.default`. Duplicate positional/keyword assignments raise `ValueError`; unresolved arguments remain mapped to `None`.
  - `args`: `Iterable[Any]`
    > positional values paired with signature arguments

  - `kwargs`: `Mapping[str, Any]`
    > explicit keyword values

  - `defaults`: `Mapping[str, Any] | None`
    > per-call fallback defaults

  - `:returns`: `dict[str, Any]`
    > complete argument-name mapping


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.prep_args" class="docs-object-method">&nbsp;</a> 
```python
prep_args(self, args, kwargs, defaults=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L1072)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L1072?message=Update%20Docs)]
</div>
**LLM Docstring**

Prepare arguments in signature order for a foreign-function call.

When `args` is not `None`, positional and keyword values are first normalized with `populate_kwargs`; each value is then converted by its `Argument.prep_value` method.
  - `args`: `Iterable[Any] | None`
    > positional values, or `None` when `kwargs` is already populated

  - `kwargs`: `Mapping[str, Any]`
    > argument values keyed by name

  - `defaults`: `Mapping[str, Any] | None`
    > per-call fallback defaults

  - `:returns`: `list[Any]`
    > ordered converted arguments


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L1103)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/FunctionSignature.py#L1103?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the function name, arguments, and return type.
  - `:returns`: `str`
    > representation string
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/ArgumentSignature/FunctionSignature.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/ArgumentSignature/FunctionSignature.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/ArgumentSignature/FunctionSignature.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/ArgumentSignature/FunctionSignature.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L890?message=Update%20Docs)   
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