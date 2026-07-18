## <a id="McUtils.Extensions.FFI.Module.FFIArgument">FFIArgument</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module.py#L201)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L201?message=Update%20Docs)]
</div>

An argument spec for data to be passed to an FFIMethod







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.FFI.Module.FFIArgument.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name=None, dtype=None, shape=None, container_type=None, value=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module.py#L206)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L206?message=Update%20Docs)]
</div>
**LLM Docstring**

Create an FFI argument specification and normalize its data and container types.
  - `name`: `Any`
    > argument name

  - `dtype`: `Any`
    > FFI type descriptor accepted by `infer_dtype`

  - `shape`: `Any`
    > declared argument shape; defaults to `()`

  - `container_type`: `Any`
    > container representation accepted by `infer_ctype`

  - `value`: `Any`
    > unused compatibility parameter

  - `:returns`: `None`
    > nothing; initializes the argument metadata


<a id="McUtils.Extensions.FFI.Module.FFIArgument.infer_dtype" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
infer_dtype(cls, dtype): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L242)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L242?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize an enum, integer code, string, NumPy dtype, or mapped Python type to `FFIType`.
  - `dtype`: `Any`
    > type descriptor to normalize

  - `:returns`: `FFIType`
    > the resolved FFI type


<a id="McUtils.Extensions.FFI.Module.FFIArgument.infer_ctype" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
infer_ctype(cls, container_type): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L274)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L274?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize a container-type enum, name, or numeric value to `FFIContainerType`.
  - `container_type`: `Any`
    > container representation descriptor

  - `:returns`: `FFIContainerType`
    > the resolved container type


<a id="McUtils.Extensions.FFI.Module.FFIArgument.from_arg_sig" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_arg_sig(cls, arg): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L293)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L293?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an FFI argument from an `ArgumentSignature.Argument`-like object.
  - `arg`: `Any`
    > argument exposing `name`, `typechar`, `is_pointer()`, and `is_array()`

  - `:returns`: `FFIArgument`
    > an argument marked `Raw` for pointer/array signatures and `Untyped` otherwise


<a id="McUtils.Extensions.FFI.Module.FFIArgument.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIArgument.py#L314)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIArgument.py#L314?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a constructor-style representation of the argument metadata.
  - `:returns`: `str`
    > the formatted argument representation


<a id="McUtils.Extensions.FFI.Module.FFIArgument.cast" class="docs-object-method">&nbsp;</a> 
```python
cast(self, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module/FFIArgument.py#L330)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module/FFIArgument.py#L330?message=Update%20Docs)]
</div>

  - `val`: `Any`
    > 
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/FFI/Module/FFIArgument.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/FFI/Module/FFIArgument.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/FFI/Module/FFIArgument.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/FFI/Module/FFIArgument.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L201?message=Update%20Docs)   
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