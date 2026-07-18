## <a id="McUtils.Extensions.FFI.Loader.FFILoader">FFILoader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Loader.py#L120)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Loader.py#L120?message=Update%20Docs)]
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
__init__(self, name, src=None, src_ext='src', load_path=None, description='A compiled potential', version='1.0.0', include_dirs=None, linked_libs=None, runtime_dirs=None, macros=None, source_files=None, build_script=None, requires_make=True, out_dir=None, cleanup_build=True, pointer_name=None, build_kwargs=None, nodebug=False, threaded=False, manage_threading_flags=True, manage_libffi_flags=True, extra_compile_args=None, extra_link_args=None, recompile=False, debug_level=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Loader.py#L147)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Loader.py#L147?message=Update%20Docs)]
</div>
**LLM Docstring**

Configure compilation and loading of the FFI extension, including NumPy, libffi, OpenMP, macro, and linker settings.
  - `name`: `Any`
    > extension module name

  - `src`: `Any`
    > source root

  - `src_ext`: `Any`
    > source subdirectory name

  - `load_path`: `Any`
    > locations searched for an existing extension

  - `description`: `Any`
    > package description

  - `version`: `Any`
    > package version

  - `include_dirs`: `Any`
    > additional include directories

  - `linked_libs`: `Any`
    > additional linked libraries

  - `runtime_dirs`: `Any`
    > runtime library directories

  - `macros`: `Any`
    > compiler macro definitions

  - `source_files`: `Any`
    > extension source files

  - `build_script`: `Any`
    > optional custom build script

  - `requires_make`: `Any`
    > whether helper libraries require a make step

  - `out_dir`: `Any`
    > output directory

  - `cleanup_build`: `Any`
    > whether build products are removed

  - `pointer_name`: `Any`
    > stored legacy pointer attribute

  - `build_kwargs`: `Any`
    > additional `CLoader` arguments

  - `nodebug`: `Any`
    > whether to define `_NODEBUG`

  - `threaded`: `Any`
    > whether OpenMP support is enabled

  - `manage_threading_flags`: `Any`
    > whether platform OpenMP flags are added

  - `manage_libffi_flags`: `Any`
    > whether libffi paths are discovered

  - `extra_compile_args`: `Any`
    > additional compiler flags

  - `extra_link_args`: `Any`
    > additional linker flags

  - `recompile`: `Any`
    > whether to force recompilation

  - `debug_level`: `Any`
    > debug selector used by the wrapped module

  - `:returns`: `None`
    > nothing; creates the configured `CLoader`


<a id="McUtils.Extensions.FFI.Loader.FFILoader.lib" class="docs-object-method">&nbsp;</a> 
```python
@property
lib(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Loader/FFILoader.py#L367)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Loader/FFILoader.py#L367?message=Update%20Docs)]
</div>
**LLM Docstring**

Load and cache the compiled extension module.
  - `:returns`: `module`
    > the loaded Python extension


<a id="McUtils.Extensions.FFI.Loader.FFILoader.caller_api_version" class="docs-object-method">&nbsp;</a> 
```python
@property
caller_api_version(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Loader/FFILoader.py#L380)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Loader/FFILoader.py#L380?message=Update%20Docs)]
</div>
**LLM Docstring**

Detect the extension calling API from the presence of `_FFIModule`.
  - `:returns`: `int`
    > `2` for capsule-based modules, otherwise `1`


<a id="McUtils.Extensions.FFI.Loader.FFILoader.call_obj" class="docs-object-method">&nbsp;</a> 
```python
@property
call_obj(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/Loader/FFILoader.py#L394)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Loader/FFILoader.py#L394?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/Loader.py#L120?message=Update%20Docs)   
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