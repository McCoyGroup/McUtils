## <a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunction">DynamicFFIFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/FFI/DynamicFFILibrary.py#L38)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/DynamicFFILibrary.py#L38?message=Update%20Docs)]
</div>

Specialization of base `SharedLibraryFunction` to call
through the `DynamicLibrary` module instead of `ctypes`







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
LibFFIMethodData: LibFFIMethodData
```
<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, shared_library, signature, defaults=None, docstring=None, call_directory=None, return_handler=None, prep_args=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L50)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L50?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunction.initialize" class="docs-object-method">&nbsp;</a> 
```python
initialize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L68)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L68?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunction.function_data" class="docs-object-method">&nbsp;</a> 
```python
@property
function_data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L84)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L84?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunction.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, *args, debug=False, threading_vars=None, threading_mode=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L127)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.py#L127?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/DynamicFFILibrary.py#L38?message=Update%20Docs)   
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