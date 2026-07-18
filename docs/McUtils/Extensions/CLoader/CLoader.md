## <a id="McUtils.Extensions.CLoader.CLoader">CLoader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader.py#L29)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader.py#L29?message=Update%20Docs)]
</div>

A general loader for C++ extensions to python, based off of the kind of thing that I have had to do multiple times







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.CLoader.CLoader.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, lib_name, lib_dir=None, load_path=None, src_ext='src', libs_ext='libs', description='An extension module', version='1.0.0', include_dirs=None, runtime_dirs=None, linked_libs=None, macros=None, extra_link_args=None, extra_compile_args=None, extra_objects=None, source_files=None, build_script=None, requires_make=True, out_dir=None, cleanup_build=True, recompile=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader.py#L34)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader.py#L34?message=Update%20Docs)]
</div>
**LLM Docstring**

Configure discovery, compilation, linking, and cleanup for a C++ extension module.

If `lib_dir` is omitted, `lib_name` must name an existing directory, whose basename becomes the extension name.
  - `lib_name`: `str`
    > extension module name or, when `lib_dir` is omitted, its project directory

  - `lib_dir`: `str | None`
    > project root containing source and auxiliary-library directories

  - `load_path`: `Iterable[str] | None`
    > directories searched for an already-built extension

  - `src_ext`: `str`
    > source-directory name relative to `lib_dir`

  - `libs_ext`: `str`
    > auxiliary-library directory name relative to `lib_dir`

  - `description`: `str`
    > package description passed to the build system

  - `version`: `str`
    > package version passed to the build system

  - `include_dirs`: `Iterable[str] | None`
    > header/library search directories

  - `runtime_dirs`: `Iterable[str] | None`
    > runtime library search directories

  - `linked_libs`: `Iterable[str] | None`
    > library names supplied to the linker

  - `macros`: `Iterable[tuple] | None`
    > preprocessor macro definitions

  - `extra_link_args`: `Iterable[str] | None`
    > additional linker arguments

  - `extra_compile_args`: `Iterable[str] | None`
    > additional compiler arguments

  - `extra_objects`: `Iterable[str] | None`
    > prebuilt object files to link

  - `source_files`: `Iterable[str] | None`
    > C/C++ source files; defaults to `<lib_name>.cpp`

  - `build_script`: `str | dict | None`
    > custom build script or command specification

  - `requires_make`: `bool | str | dict`
    > whether and how auxiliary libraries should be built

  - `out_dir`: `str | None`
    > directory receiving the finished extension

  - `cleanup_build`: `bool`
    > whether to remove the temporary build directory

  - `recompile`: `bool`
    > whether to bypass discovery and force recompilation

  - `:returns`: `None`
    > no value is returned


<a id="McUtils.Extensions.CLoader.CLoader.load" class="docs-object-method">&nbsp;</a> 
```python
load(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L157)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L157?message=Update%20Docs)]
</div>
**LLM Docstring**

Find or compile the configured extension and import it.

The loaded module is cached on the loader. During import, the extension directory is temporarily inserted at the front of `sys.path`.
  - `:returns`: `types.ModuleType`
    > loaded extension module


<a id="McUtils.Extensions.CLoader.CLoader.find_extension" class="docs-object-method">&nbsp;</a> 
```python
find_extension(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L186)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L186?message=Update%20Docs)]
</div>
Tries to find the extension in the top-level directory
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.compile_extension" class="docs-object-method">&nbsp;</a> 
```python
compile_extension(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L199)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L199?message=Update%20Docs)]
</div>
Compiles and loads a C++ extension
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.src_dir" class="docs-object-method">&nbsp;</a> 
```python
@property
src_dir(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L212?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the configured source directory.
  - `:returns`: `str`
    > `lib_dir/src_ext`


<a id="McUtils.Extensions.CLoader.CLoader.lib_lib_dir" class="docs-object-method">&nbsp;</a> 
```python
@property
lib_lib_dir(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L223)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L223?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the configured auxiliary-library directory.
  - `:returns`: `str`
    > `lib_dir/libs_ext`


<a id="McUtils.Extensions.CLoader.CLoader.get_extension" class="docs-object-method">&nbsp;</a> 
```python
get_extension(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L235)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L235?message=Update%20Docs)]
</div>
Gets the Extension module to be compiled
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.configure_make_command" class="docs-object-method">&nbsp;</a> 
```python
configure_make_command(self, make_file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L275)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L275?message=Update%20Docs)]
</div>
**LLM Docstring**

Translate a make configuration dictionary into compiler and linker command argument lists.

Creates the build directory, derives object-file paths, prefixes compiler/linker flags, and appends a platform-specific shared-library suffix. The read `python_dir` entry is not otherwise used.
  - `make_file`: `dict`
    > build configuration containing at least `python_dir`, `compiler`, and `linker`

  - `:returns`: `list[list[str]]`
    > one compile command per source followed by one link command


<a id="McUtils.Extensions.CLoader.CLoader.custom_make" class="docs-object-method">&nbsp;</a> 
```python
custom_make(self, make_file, make_dir): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L342)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L342?message=Update%20Docs)]
</div>
A way to call a custom make file either for building the helper lib or for building the proper lib
  - `make_file`: `Any`
    > 
  - `make_dir`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.make_required_libs" class="docs-object-method">&nbsp;</a> 
```python
make_required_libs(self, library_types=('.so', '.pyd', '.dll')): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L395)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L395?message=Update%20Docs)]
</div>
Makes any libs required by the current one
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.build_lib" class="docs-object-method">&nbsp;</a> 
```python
build_lib(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L430)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L430?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the extension in its source directory.

Runs a custom build when configured, otherwise invokes `distutils.setup` with `build_ext --inplace`. On macOS it also rewrites dependent library install names to use `@rpath`.
  - `:returns`: `None`
    > no value is returned


<a id="McUtils.Extensions.CLoader.CLoader.locate_library" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
locate_library(cls, libname, roots, extensions, library_types=('.so', '.pyd', '.dll')): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L472)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L472?message=Update%20Docs)]
</div>
Tries to locate the library file (if it exists)
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.locate_lib" class="docs-object-method">&nbsp;</a> 
```python
locate_lib(self, name=None, roots=None, extensions=None, library_types=('.so', '.pyd', '.dll')): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L519)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L519?message=Update%20Docs)]
</div>
Tries to locate the build library file (if it exists)
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.cleanup" class="docs-object-method">&nbsp;</a> 
```python
cleanup(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/CLoader/CLoader.py#L541)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader/CLoader.py#L541?message=Update%20Docs)]
</div>
**LLM Docstring**

Move the built extension to its output directory and optionally remove build artifacts.

The implementation locates the built library, replaces any existing target, and renames the library into place. The build-directory test uses `os.path.isdir` without calling it, so cleanup is attempted whenever `cleanup_build` is true.
  - `:returns`: `str | None`
    > target extension path, or `None` if no built library was found
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/CLoader/CLoader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/CLoader/CLoader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/CLoader/CLoader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/CLoader/CLoader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/CLoader.py#L29?message=Update%20Docs)   
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