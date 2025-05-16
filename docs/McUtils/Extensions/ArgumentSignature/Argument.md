## <a id="McUtils.Extensions.ArgumentSignature.Argument">Argument</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature.py#L311)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature.py#L311?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/Argument.py#L324)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/Argument.py#L324?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L338)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L338?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L384)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L384?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.Argument.infer_type_str" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
infer_type_str(cls, argstr): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L389)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L389?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.Argument.inferred_type_string" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
inferred_type_string(cls, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L405)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L405?message=Update%20Docs)]
</div>
returns a type string for the inferred type


<a id="McUtils.Extensions.ArgumentSignature.Argument.prep_value" class="docs-object-method">&nbsp;</a> 
```python
prep_value(self, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/Argument.py#L412)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/Argument.py#L412?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.Argument.is_pointer" class="docs-object-method">&nbsp;</a> 
```python
is_pointer(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/Argument.py#L415)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/Argument.py#L415?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.Argument.is_array" class="docs-object-method">&nbsp;</a> 
```python
is_array(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/Argument.py#L417)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/Argument.py#L417?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.Argument.dtypes" class="docs-object-method">&nbsp;</a> 
```python
@property
dtypes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/Argument.py#L419)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/Argument.py#L419?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.Argument.typechar" class="docs-object-method">&nbsp;</a> 
```python
@property
typechar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/Argument.py#L422)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/Argument.py#L422?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.Argument.cpp_signature" class="docs-object-method">&nbsp;</a> 
```python
@property
cpp_signature(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/Argument.py#L425)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/Argument.py#L425?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.Argument.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/Argument.py#L431)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/Argument.py#L431?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/ArgumentSignature/Argument.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/ArgumentSignature/Argument.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/ArgumentSignature/Argument.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/ArgumentSignature/Argument.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature.py#L311?message=Update%20Docs)   
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