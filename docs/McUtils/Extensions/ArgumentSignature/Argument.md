## <a id="McUtils.Extensions.ArgumentSignature.Argument">Argument</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature.py#L670)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L670?message=Update%20Docs)]
</div>

Defines a single Argument for a C-level caller to support default values, etc.
We use a two-pronged approach where we have a set of ArgumentType serializers/deserializers







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
arg_types: list
```
<a id="McUtils.Extensions.ArgumentSignature.Argument.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name, dtype, default=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature.py#L683)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L683?message=Update%20Docs)]
</div>

  - `name`: `str`
    > the name of the argument
  - `dtype`: `ArgumentType`
    > the type of the argument; at some point we'll support type inference...
  - `default`: `Any`
    > the default value for the argument


<a id="McUtils.Extensions.ArgumentSignature.Argument.infer_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
infer_type(cls, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L697)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L697?message=Update%20Docs)]
</div>
Infers the type of an argument
  - `arg`: `ArgumentType | str | type | ctypes type`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.ArgumentSignature.Argument.infer_type_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
infer_type_type(cls, type_key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L753)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L753?message=Update%20Docs)]
</div>
**LLM Docstring**

Look up an argument type from a Python type object.
  - `type_key`: `type`
    > Python type to resolve

  - `:returns`: `ArgumentType | None`
    > matching registered argument type, or `None`


<a id="McUtils.Extensions.ArgumentSignature.Argument.infer_type_str" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
infer_type_str(cls, argstr): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L769)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L769?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve an argument type from a string specification.

Checks registered mappings first, then attempts the module's pointer-pattern branch. That branch constructs an `ArrayType`; malformed or unmatched strings return `None`.
  - `argstr`: `str`
    > type spelling to resolve

  - `:returns`: `ArgumentType | None`
    > resolved argument type or `None`


<a id="McUtils.Extensions.ArgumentSignature.Argument.inferred_type_string" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
inferred_type_string(cls, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L798)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L798?message=Update%20Docs)]
</div>
returns a type string for the inferred type


<a id="McUtils.Extensions.ArgumentSignature.Argument.prep_value" class="docs-object-method">&nbsp;</a> 
```python
prep_value(self, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/Argument.py#L805)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/Argument.py#L805?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a value to the C-call representation required by this argument.
  - `val`: `Any`
    > Python value to prepare

  - `:returns`: `Any`
    > converted value


<a id="McUtils.Extensions.ArgumentSignature.Argument.is_pointer" class="docs-object-method">&nbsp;</a> 
```python
is_pointer(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/Argument.py#L819)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/Argument.py#L819?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether this argument uses a `PointerType`.
  - `:returns`: `bool`
    > pointer-type flag


<a id="McUtils.Extensions.ArgumentSignature.Argument.is_array" class="docs-object-method">&nbsp;</a> 
```python
is_array(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/Argument.py#L829)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/Argument.py#L829?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether this argument uses an `ArrayType`.
  - `:returns`: `bool`
    > array-type flag


<a id="McUtils.Extensions.ArgumentSignature.Argument.dtypes" class="docs-object-method">&nbsp;</a> 
```python
@property
dtypes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/Argument.py#L839)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/Argument.py#L839?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the NumPy dtypes accepted by this argument type.
  - `:returns`: `tuple[np.dtype, ...]`
    > accepted dtypes


<a id="McUtils.Extensions.ArgumentSignature.Argument.typechar" class="docs-object-method">&nbsp;</a> 
```python
@property
typechar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/Argument.py#L850)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/Argument.py#L850?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the Python C-API format character for this argument type.
  - `:returns`: `str`
    > format character


<a id="McUtils.Extensions.ArgumentSignature.Argument.cpp_signature" class="docs-object-method">&nbsp;</a> 
```python
@property
cpp_signature(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/Argument.py#L861)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/Argument.py#L861?message=Update%20Docs)]
</div>
**LLM Docstring**

Format this argument as a C/C++ declaration fragment.
  - `:returns`: `str`
    > string of the form `<type> <name>`


<a id="McUtils.Extensions.ArgumentSignature.Argument.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/Argument.py#L875)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/Argument.py#L875?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation containing the argument name and resolved type.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/ArgumentSignature/Argument.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/ArgumentSignature/Argument.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/ArgumentSignature/Argument.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/ArgumentSignature/Argument.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L670?message=Update%20Docs)   
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