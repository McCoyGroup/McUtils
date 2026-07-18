## <a id="McUtils.Extensions.ArgumentSignature.PrimitiveType">PrimitiveType</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature.py#L153)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L153?message=Update%20Docs)]
</div>

Defines a general purpose ArgumentType so that we can easily manage complicated type specs
The basic idea is to define a hierarchy of types that can then convert themselves down to
a `ctypes`-style spec as well as a C++ argument spec so that we can enable `SharedLibraryFunction`
to use either the basic `ctypes` FFI or a more efficient, but fragile system based off of extension modules







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
typeset: dict
```
<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name, ctypes_spec, cpp_spec, capi_spec, python_types, numpy_dtypes, serializer, deserializer): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature.py#L162)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L162?message=Update%20Docs)]
</div>

  - `name`: `str`
    > argument name (e.g. 'double')
  - `ctypes_spec`: `Any`
    > the ctypes data-type that arguments of this type would be converted to
  - `cpp_spec`: `str`
    > the C++ spec for this type (as a string)
  - `capi_spec`: `str`
    > the python C-API string for use in `Py_BuildValue`
  - `python_types`: `Iterable[type]`
    > the python types that this argument maps onto
  - `numpy_dtypes`: `Iterable[np.dtype]`
    > the numpy dtypes that this argument maps onto
  - `serializer`: `Callable`
    > a serializer for converting this object into a byte-stream
  - `deserializer`: `Callable`
    > a deserializer for converting the byte-stream into a C-level object


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.name" class="docs-object-method">&nbsp;</a> 
```python
@property
name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L201)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L201?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the descriptive type name.
  - `:returns`: `str`
    > the descriptive type name


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.ctypes_type" class="docs-object-method">&nbsp;</a> 
```python
@property
ctypes_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L212?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the stored `ctypes` type specification.
  - `:returns`: `type | None`
    > the stored `ctypes` type specification


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.cpp_type" class="docs-object-method">&nbsp;</a> 
```python
@property
cpp_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L223)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L223?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the stored C/C++ type spelling.
  - `:returns`: `str`
    > the stored C/C++ type spelling


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.types" class="docs-object-method">&nbsp;</a> 
```python
@property
types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L234)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L234?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the accepted Python types.
  - `:returns`: `tuple[type, ...]`
    > the accepted Python types


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.dtypes" class="docs-object-method">&nbsp;</a> 
```python
@property
dtypes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L245)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L245?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the accepted NumPy dtypes.
  - `:returns`: `tuple[np.dtype, ...]`
    > the accepted NumPy dtypes


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.typechar" class="docs-object-method">&nbsp;</a> 
```python
@property
typechar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L256)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L256?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the stored Python C-API format character.
  - `:returns`: `str`
    > the stored Python C-API format character


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.isinstance" class="docs-object-method">&nbsp;</a> 
```python
isinstance(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L267)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L267?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether a value belongs to one of the configured Python types.
  - `arg`: `Any`
    > value to test

  - `:returns`: `bool`
    > `True` when `arg` is an instance of an accepted type


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.cast" class="docs-object-method">&nbsp;</a> 
```python
cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L280)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L280?message=Update%20Docs)]
</div>
**LLM Docstring**

Cast a value with the first configured Python type.
  - `arg`: `Any`
    > value to convert

  - `:returns`: `Any`
    > Python-side converted value


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.c_cast" class="docs-object-method">&nbsp;</a> 
```python
c_cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L293)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L293?message=Update%20Docs)]
</div>
**LLM Docstring**

Cast a value to the configured `ctypes` scalar.

The value is first converted with `cast`.
  - `arg`: `Any`
    > value to convert

  - `:returns`: `Any`
    > `ctypes` scalar instance


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L309)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PrimitiveType.py#L309?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a concise representation containing the wrapper class and primitive name.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/ArgumentSignature/PrimitiveType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/ArgumentSignature/PrimitiveType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/ArgumentSignature/PrimitiveType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/ArgumentSignature/PrimitiveType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L153?message=Update%20Docs)   
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