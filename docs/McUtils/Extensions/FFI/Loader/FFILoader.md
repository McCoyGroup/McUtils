## <a id="McUtils.Extensions.FFI.Loader.FFILoader">FFILoader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/FFI/Loader.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/Loader.py#L15?message=Update%20Docs)]
</div>

Provides a standardized way to load and compile a potential using a potential template







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
libs_folder: str
cpp_std: str
```
<a id="McUtils.Extensions.FFI.Loader.FFILoader.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name, src=None, src_ext='src', load_path=None, description='A compiled potential', version='1.0.0', include_dirs=None, linked_libs=None, runtime_dirs=None, macros=None, source_files=None, build_script=None, requires_make=True, out_dir=None, cleanup_build=True, pointer_name=None, build_kwargs=None, nodebug=False, threaded=False, extra_compile_args=None, extra_link_args=None, recompile=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/FFI/Loader/FFILoader.py#L42)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/Loader/FFILoader.py#L42?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.FFI.Loader.FFILoader.lib" class="docs-object-method">&nbsp;</a> 
```python
@property
lib(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/FFI/Loader/FFILoader.py#L117)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/Loader/FFILoader.py#L117?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.FFI.Loader.FFILoader.caller_api_version" class="docs-object-method">&nbsp;</a> 
```python
@property
caller_api_version(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/FFI/Loader/FFILoader.py#L122)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/Loader/FFILoader.py#L122?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.FFI.Loader.FFILoader.call_obj" class="docs-object-method">&nbsp;</a> 
```python
@property
call_obj(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/FFI/Loader/FFILoader.py#L128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/Loader/FFILoader.py#L128?message=Update%20Docs)]
</div>
The object that defines how to call the potential.
Can either be a pure python function, an FFIModule, or a PyCapsule
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/FFI/Loader/FFILoader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/FFI/Loader/FFILoader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/FFI/Loader/FFILoader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/FFI/Loader/FFILoader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/FFI/Loader.py#L15?message=Update%20Docs)   
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