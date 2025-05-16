## <a id="McUtils.Extensions.CLoader.CLoader">CLoader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader.py#L13)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader.py#L13?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L18)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L18?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.CLoader.CLoader.load" class="docs-object-method">&nbsp;</a> 
```python
load(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L71)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L71?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.CLoader.CLoader.find_extension" class="docs-object-method">&nbsp;</a> 
```python
find_extension(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L90)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L90?message=Update%20Docs)]
</div>
Tries to find the extension in the top-level directory
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.compile_extension" class="docs-object-method">&nbsp;</a> 
```python
compile_extension(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L103)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L103?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L116)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L116?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.CLoader.CLoader.lib_lib_dir" class="docs-object-method">&nbsp;</a> 
```python
@property
lib_lib_dir(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L119?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.CLoader.CLoader.get_extension" class="docs-object-method">&nbsp;</a> 
```python
get_extension(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L123)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L123?message=Update%20Docs)]
</div>
Gets the Extension module to be compiled
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.configure_make_command" class="docs-object-method">&nbsp;</a> 
```python
configure_make_command(self, make_file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L163)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L163?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.CLoader.CLoader.custom_make" class="docs-object-method">&nbsp;</a> 
```python
custom_make(self, make_file, make_dir): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L217)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L217?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L270)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L270?message=Update%20Docs)]
</div>
Makes any libs required by the current one
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.build_lib" class="docs-object-method">&nbsp;</a> 
```python
build_lib(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L305)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L305?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.CLoader.CLoader.locate_library" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
locate_library(cls, libname, roots, extensions, library_types=('.so', '.pyd', '.dll')): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L337)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L337?message=Update%20Docs)]
</div>
Tries to locate the library file (if it exists)
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.locate_lib" class="docs-object-method">&nbsp;</a> 
```python
locate_lib(self, name=None, roots=None, extensions=None, library_types=('.so', '.pyd', '.dll')): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L384)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L384?message=Update%20Docs)]
</div>
Tries to locate the build library file (if it exists)
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.CLoader.CLoader.cleanup" class="docs-object-method">&nbsp;</a> 
```python
cleanup(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/CLoader/CLoader.py#L406)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader/CLoader.py#L406?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/CLoader/CLoader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/CLoader/CLoader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/CLoader/CLoader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/CLoader/CLoader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/CLoader.py#L13?message=Update%20Docs)   
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