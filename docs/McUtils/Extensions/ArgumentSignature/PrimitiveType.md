## <a id="McUtils.Extensions.ArgumentSignature.PrimitiveType">PrimitiveType</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature.py#L64)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature.py#L64?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/PrimitiveType.py#L73)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/PrimitiveType.py#L73?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/PrimitiveType.py#L112)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/PrimitiveType.py#L112?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.ctypes_type" class="docs-object-method">&nbsp;</a> 
```python
@property
ctypes_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/PrimitiveType.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/PrimitiveType.py#L115?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.cpp_type" class="docs-object-method">&nbsp;</a> 
```python
@property
cpp_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/PrimitiveType.py#L118)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/PrimitiveType.py#L118?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.types" class="docs-object-method">&nbsp;</a> 
```python
@property
types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/PrimitiveType.py#L121)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/PrimitiveType.py#L121?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.dtypes" class="docs-object-method">&nbsp;</a> 
```python
@property
dtypes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/PrimitiveType.py#L124)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/PrimitiveType.py#L124?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.typechar" class="docs-object-method">&nbsp;</a> 
```python
@property
typechar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/PrimitiveType.py#L127)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/PrimitiveType.py#L127?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.isinstance" class="docs-object-method">&nbsp;</a> 
```python
isinstance(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/PrimitiveType.py#L130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/PrimitiveType.py#L130?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.cast" class="docs-object-method">&nbsp;</a> 
```python
cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/PrimitiveType.py#L132)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/PrimitiveType.py#L132?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.c_cast" class="docs-object-method">&nbsp;</a> 
```python
c_cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/PrimitiveType.py#L134)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/PrimitiveType.py#L134?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.PrimitiveType.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/PrimitiveType.py#L137)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/PrimitiveType.py#L137?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature.py#L64?message=Update%20Docs)   
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