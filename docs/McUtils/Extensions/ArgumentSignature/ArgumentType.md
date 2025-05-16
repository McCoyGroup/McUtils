## <a id="McUtils.Extensions.ArgumentSignature.ArgumentType">ArgumentType</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature.py#L24)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature.py#L24?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArgumentType.py#L35)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArgumentType.py#L35?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.cpp_type" class="docs-object-method">&nbsp;</a> 
```python
@property
cpp_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArgumentType.py#L39)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArgumentType.py#L39?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.types" class="docs-object-method">&nbsp;</a> 
```python
@property
types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArgumentType.py#L43)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArgumentType.py#L43?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.dtypes" class="docs-object-method">&nbsp;</a> 
```python
@property
dtypes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArgumentType.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArgumentType.py#L47?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.typechar" class="docs-object-method">&nbsp;</a> 
```python
@property
typechar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArgumentType.py#L51)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArgumentType.py#L51?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.isinstance" class="docs-object-method">&nbsp;</a> 
```python
isinstance(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArgumentType.py#L55)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArgumentType.py#L55?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.cast" class="docs-object-method">&nbsp;</a> 
```python
cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArgumentType.py#L58)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArgumentType.py#L58?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArgumentType.c_cast" class="docs-object-method">&nbsp;</a> 
```python
c_cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArgumentType.py#L61)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArgumentType.py#L61?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/ArgumentSignature/ArgumentType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/ArgumentSignature/ArgumentType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/ArgumentSignature/ArgumentType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/ArgumentSignature/ArgumentType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature.py#L24?message=Update%20Docs)   
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