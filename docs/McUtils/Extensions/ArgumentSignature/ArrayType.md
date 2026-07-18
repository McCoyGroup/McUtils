## <a id="McUtils.Extensions.ArgumentSignature.ArrayType">ArrayType</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature.py#L323)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L323?message=Update%20Docs)]
</div>

Extends the basic `ArgumentType` spec to handle array types of possibly fixed size.
To start, we're only adding in proper support for numpy arrays.
Other flavors might come, but given the use case, it's unlikely.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.ArgumentSignature.ArrayType.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, base_type, shape=None, ctypes_spec=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature.py#L329)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L329?message=Update%20Docs)]
</div>
**LLM Docstring**

Create an array argument type around a primitive base type.
  - `base_type`: `ArgumentType`
    > element type used for dtype checks and conversion

  - `shape`: `tuple[int, ...] | None`
    > stored optional shape metadata; it is not enforced by current methods

  - `ctypes_spec`: `Any | None`
    > optional precomputed `ctypes` array specification

  - `:returns`: `None`
    > no value is returned


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.ctypes_type" class="docs-object-method">&nbsp;</a> 
```python
@property
ctypes_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L351)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L351?message=Update%20Docs)]
</div>
**LLM Docstring**

Return or lazily create a C-contiguous NumPy `ndpointer` specification.
  - `:returns`: `Any`
    > or lazily create a C-contiguous NumPy `ndpointer` specification


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.cpp_type" class="docs-object-method">&nbsp;</a> 
```python
@property
cpp_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L364)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L364?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the pointer-like C/C++ type string formed from the cached `ctypes` specification.
  - `:returns`: `str`
    > the pointer-like C/C++ type string formed from the cached `ctypes` specification


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.types" class="docs-object-method">&nbsp;</a> 
```python
@property
types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L375)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L375?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the accepted Python container type, `numpy.ndarray`.
  - `:returns`: `tuple[type, ...]`
    > the accepted Python container type, `numpy.ndarray`


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.dtypes" class="docs-object-method">&nbsp;</a> 
```python
@property
dtypes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L386)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L386?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the element dtypes accepted by the base type.
  - `:returns`: `tuple[np.dtype, ...]`
    > the element dtypes accepted by the base type


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.typechar" class="docs-object-method">&nbsp;</a> 
```python
@property
typechar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L397)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L397?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the Python C-API format character of the base type.
  - `:returns`: `str`
    > the Python C-API format character of the base type


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.isinstance" class="docs-object-method">&nbsp;</a> 
```python
isinstance(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L408)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L408?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether a value is a NumPy array with an accepted base dtype.
  - `arg`: `Any`
    > value to test

  - `:returns`: `bool`
    > compatibility flag


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.cast" class="docs-object-method">&nbsp;</a> 
```python
cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L421)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L421?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a value to an array using the first accepted base dtype.
  - `arg`: `Any`
    > array-like value

  - `:returns`: `np.ndarray`
    > converted NumPy array


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.c_cast" class="docs-object-method">&nbsp;</a> 
```python
c_cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L434)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L434?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a value to a C-contiguous NumPy array of the required dtype.
  - `arg`: `Any`
    > array-like value

  - `:returns`: `np.ndarray`
    > contiguous converted array


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L447)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/ArrayType.py#L447?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a concise representation containing the array wrapper and base type.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/ArgumentSignature/ArrayType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/ArgumentSignature/ArrayType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/ArgumentSignature/ArrayType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/ArgumentSignature/ArrayType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L323?message=Update%20Docs)   
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