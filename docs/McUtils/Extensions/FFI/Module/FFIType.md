## <a id="McUtils.McUtils.Extensions.FFI.Module.FFIType">FFIType</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Module.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L16?message=Update%20Docs)]
</div>

The set of supported enum types.
Maps onto the native python convertable types and NumPy dtypes.
In the future, this should be done more elegantly, but for now it suffices
that these types align on the C++ side and this side.
Only NumPy arrays are handled using the buffer interface & so if you want to pass a pointer
you gotta do it using a NumPy array.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
GENERIC: FFIType
Void: FFIType
PY_TYPES: FFIType
UnsignedChar: FFIType
Short: FFIType
UnsignedShort: FFIType
Int: FFIType
UnsignedInt: FFIType
Long: FFIType
UnsignedLong: FFIType
LongLong: FFIType
UnsignedLongLong: FFIType
PySizeT: FFIType
Float: FFIType
Double: FFIType
Bool: FFIType
String: FFIType
PyObject: FFIType
Compound: FFIType
NUMPY_TYPES: FFIType
NUMPY_Int8: FFIType
NUMPY_UnsignedInt8: FFIType
NUMPY_Int16: FFIType
NUMPY_UnsignedInt16: FFIType
NUMPY_Int32: FFIType
NUMPY_UnsignedInt32: FFIType
NUMPY_Int64: FFIType
NUMPY_UnsignedInt64: FFIType
NUMPY_Float16: FFIType
NUMPY_Float32: FFIType
NUMPY_Float64: FFIType
NUMPY_Float128: FFIType
NUMPY_Bool: FFIType
```
<a id="McUtils.McUtils.Extensions.FFI.Module.FFIType.type_data" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
type_data(cls, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L112)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L112?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Extensions.FFI.Module.FFIType.resolve_ffi_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_ffi_type(cls, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L120)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L120?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/FFI/Module/FFIType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/FFI/Module/FFIType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/FFI/Module/FFIType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/FFI/Module/FFIType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Module.py#L16?message=Update%20Docs)   
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