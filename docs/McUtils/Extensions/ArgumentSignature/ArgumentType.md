## <a id="McUtils.Extensions.ArgumentSignature.ArgumentType">ArgumentType</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature.py#L24)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L24?message=Update%20Docs)]
</div>

Defines a general purpose `ArgumentType` so that we can easily manage complicated type specs
The basic idea is to define a hierarchy of types that can then convert themselves down to
a `ctypes`-style spec as well as a C++ argument spec so that we can enable `SharedLibraryFunction`
to use either the basic `ctypes` FFI or a more efficient, but fragile system based off of extension modules.
This will be explicitly overridden by the `PrimitiveType`, `ArrayType` and `PointerType` subclasses that provide
the actual useable classes.
I'd really live to be integrate with what's in the `typing` module to be able to reuse that type-inference machinery







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.ctypes_type" class="docs-object-method">&nbsp;</a> 
```python
@property
ctypes_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L35)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L35?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the `ctypes` representation used for foreign-function calls.

Subclasses must implement this abstract property.
  - `:returns`: `type | None`
    > the `ctypes` representation used for foreign-function calls


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.cpp_type" class="docs-object-method">&nbsp;</a> 
```python
@property
cpp_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L49)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L49?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the C/C++ spelling for this argument type.

Subclasses must implement this abstract property.
  - `:returns`: `str`
    > the C/C++ spelling for this argument type


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.types" class="docs-object-method">&nbsp;</a> 
```python
@property
types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L63)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L63?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the accepted Python runtime types.

Subclasses must implement this abstract property.
  - `:returns`: `tuple[type, ...]`
    > the accepted Python runtime types


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.dtypes" class="docs-object-method">&nbsp;</a> 
```python
@property
dtypes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L77)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L77?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the accepted NumPy data types.

Subclasses must implement this abstract property.
  - `:returns`: `tuple[np.dtype, ...]`
    > the accepted NumPy data types


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.typechar" class="docs-object-method">&nbsp;</a> 
```python
@property
typechar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L91)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L91?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the Python C-API format character for this type.

Subclasses must implement this abstract property.
  - `:returns`: `str`
    > the Python C-API format character for this type


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.isinstance" class="docs-object-method">&nbsp;</a> 
```python
isinstance(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L105?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether a value is already compatible with this argument type.

Subclasses must implement this abstract operation.
  - `arg`: `Any`
    > value to inspect or convert

  - `:returns`: `bool`
    > whether a value is already compatible with this argument type


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.cast" class="docs-object-method">&nbsp;</a> 
```python
cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L121)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L121?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a Python value to the corresponding Python-side representation.

Subclasses must implement this abstract operation.
  - `arg`: `Any`
    > value to inspect or convert

  - `:returns`: `Any`
    > converted a Python value to the corresponding Python-side representation


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.c_cast" class="docs-object-method">&nbsp;</a> 
```python
c_cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L137)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArgumentType.py#L137?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a Python value to the object passed through `ctypes`.

Subclasses must implement this abstract operation.
  - `arg`: `Any`
    > value to inspect or convert

  - `:returns`: `Any`
    > converted a Python value to the object passed through `ctypes`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/ArgumentSignature/ArgumentType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/ArgumentSignature/ArgumentType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/ArgumentSignature/ArgumentType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/ArgumentSignature/ArgumentType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L24?message=Update%20Docs)   
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