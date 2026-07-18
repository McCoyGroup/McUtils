## <a id="McUtils.Extensions.ArgumentSignature.PointerType">PointerType</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature.py#L461)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L461?message=Update%20Docs)]
</div>

Extends the basic `ArgumentType` spec to handle pointer types







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.ArgumentSignature.PointerType.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, base_type): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature.py#L465)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L465?message=Update%20Docs)]
</div>

  - `base_type`: `ArgumentType`
    > The base type we're building off of


<a id="McUtils.Extensions.ArgumentSignature.PointerType.ctypes_type" class="docs-object-method">&nbsp;</a> 
```python
@property
ctypes_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L473)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L473?message=Update%20Docs)]
</div>
**LLM Docstring**

Return or lazily create a `ctypes.POINTER` to the base type.
  - `:returns`: `Any`
    > or lazily create a `ctypes.POINTER` to the base type


<a id="McUtils.Extensions.ArgumentSignature.PointerType.cpp_type" class="docs-object-method">&nbsp;</a> 
```python
@property
cpp_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L487)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L487?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the pointer-like C/C++ type string formed from the cached `ctypes` specification.
  - `:returns`: `str`
    > the pointer-like C/C++ type string formed from the cached `ctypes` specification


<a id="McUtils.Extensions.ArgumentSignature.PointerType.types" class="docs-object-method">&nbsp;</a> 
```python
@property
types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L498)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L498?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the Python types accepted by the base type.
  - `:returns`: `tuple[type, ...]`
    > the Python types accepted by the base type


<a id="McUtils.Extensions.ArgumentSignature.PointerType.dtypes" class="docs-object-method">&nbsp;</a> 
```python
@property
dtypes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L509)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L509?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the NumPy dtypes accepted by the base type.
  - `:returns`: `tuple[np.dtype, ...]`
    > the NumPy dtypes accepted by the base type


<a id="McUtils.Extensions.ArgumentSignature.PointerType.typechar" class="docs-object-method">&nbsp;</a> 
```python
@property
typechar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L520)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L520?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the Python C-API format character of the base type.
  - `:returns`: `str`
    > the Python C-API format character of the base type


<a id="McUtils.Extensions.ArgumentSignature.PointerType.isinstance" class="docs-object-method">&nbsp;</a> 
```python
isinstance(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L531)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L531?message=Update%20Docs)]
</div>
**LLM Docstring**

Delegate compatibility testing to the base type.
  - `arg`: `Any`
    > value to test

  - `:returns`: `bool`
    > compatibility flag


<a id="McUtils.Extensions.ArgumentSignature.PointerType.cast" class="docs-object-method">&nbsp;</a> 
```python
cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L544)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L544?message=Update%20Docs)]
</div>
**LLM Docstring**

Delegate Python-side conversion to the base type.
  - `arg`: `Any`
    > value to convert

  - `:returns`: `Any`
    > converted base value


<a id="McUtils.Extensions.ArgumentSignature.PointerType.c_cast" class="docs-object-method">&nbsp;</a> 
```python
c_cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L557)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L557?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a value with the base type and return a `ctypes.byref` pointer to it.
  - `arg`: `Any`
    > value to convert

  - `:returns`: `Any`
    > by-reference `ctypes` object


<a id="McUtils.Extensions.ArgumentSignature.PointerType.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L571)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature/PointerType.py#L571?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a concise representation containing the pointer wrapper and base type.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/ArgumentSignature/PointerType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/ArgumentSignature/PointerType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/ArgumentSignature/PointerType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/ArgumentSignature/PointerType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/ArgumentSignature.py#L461?message=Update%20Docs)   
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