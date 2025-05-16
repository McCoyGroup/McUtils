## <a id="McUtils.Extensions.ArgumentSignature.ArrayType">ArrayType</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature.py#L143)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature.py#L143?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArrayType.py#L149)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArrayType.py#L149?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.ctypes_type" class="docs-object-method">&nbsp;</a> 
```python
@property
ctypes_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArrayType.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArrayType.py#L154?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.cpp_type" class="docs-object-method">&nbsp;</a> 
```python
@property
cpp_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArrayType.py#L159)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArrayType.py#L159?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.types" class="docs-object-method">&nbsp;</a> 
```python
@property
types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArrayType.py#L162)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArrayType.py#L162?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.dtypes" class="docs-object-method">&nbsp;</a> 
```python
@property
dtypes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArrayType.py#L165)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArrayType.py#L165?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.typechar" class="docs-object-method">&nbsp;</a> 
```python
@property
typechar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArrayType.py#L168)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArrayType.py#L168?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.isinstance" class="docs-object-method">&nbsp;</a> 
```python
isinstance(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArrayType.py#L171)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArrayType.py#L171?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.cast" class="docs-object-method">&nbsp;</a> 
```python
cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArrayType.py#L173)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArrayType.py#L173?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.c_cast" class="docs-object-method">&nbsp;</a> 
```python
c_cast(self, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArrayType.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArrayType.py#L175?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.ArrayType.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/ArrayType.py#L177)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/ArrayType.py#L177?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/ArgumentSignature/ArrayType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/ArgumentSignature/ArrayType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/ArgumentSignature/ArrayType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/ArgumentSignature/ArrayType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature.py#L143?message=Update%20Docs)   
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