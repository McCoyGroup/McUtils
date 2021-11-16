## <a id="McUtils.Extensions.CLoader.CLoader">CLoader</a>
A general loader for C++ extensions to python, based off of the kind of thing that I have had to do multiple times

### Properties and Methods
<a id="McUtils.Extensions.CLoader.CLoader.__init__" class="docs-object-method">&nbsp;</a>
```python
__init__(self, lib_name, lib_dir, load_path=None, src_ext='src', description='An extension module', version='1.0.0', include_dirs=None, runtime_dirs=None, linked_libs=None, macros=None, extra_link_args=None, extra_compile_args=None, extra_objects=None, source_files=None, build_script=None, requires_make=False, out_dir=None, cleanup_build=True): 
```

<a id="McUtils.Extensions.CLoader.CLoader.load" class="docs-object-method">&nbsp;</a>
```python
load(self): 
```

<a id="McUtils.Extensions.CLoader.CLoader.find_extension" class="docs-object-method">&nbsp;</a>
```python
find_extension(self): 
```
Tries to find the extension in the top-level directory
- `:returns`: `_`
    >No description...

<a id="McUtils.Extensions.CLoader.CLoader.compile_extension" class="docs-object-method">&nbsp;</a>
```python
compile_extension(self): 
```
Compiles and loads a C++ extension
- `:returns`: `_`
    >No description...

<a id="McUtils.Extensions.CLoader.CLoader.src_dir" class="docs-object-method">&nbsp;</a>
```python
@property
src_dir(self): 
```

<a id="McUtils.Extensions.CLoader.CLoader.lib_lib_dir" class="docs-object-method">&nbsp;</a>
```python
@property
lib_lib_dir(self): 
```

<a id="McUtils.Extensions.CLoader.CLoader.get_extension" class="docs-object-method">&nbsp;</a>
```python
get_extension(self): 
```
Gets the Extension module to be compiled
- `:returns`: `_`
    >No description...

<a id="McUtils.Extensions.CLoader.CLoader.custom_make" class="docs-object-method">&nbsp;</a>
```python
custom_make(self, make_file, make_dir): 
```
A way to call a custom make file either for building the helper lib or for building the proper lib
- `make_file`: `Any`
    >No description...
- `make_dir`: `Any`
    >No description...
- `:returns`: `_`
    >No description...

<a id="McUtils.Extensions.CLoader.CLoader.make_required_libs" class="docs-object-method">&nbsp;</a>
```python
make_required_libs(self): 
```
Makes any libs required by the current one
- `:returns`: `_`
    >No description...

<a id="McUtils.Extensions.CLoader.CLoader.build_lib" class="docs-object-method">&nbsp;</a>
```python
build_lib(self): 
```

<a id="McUtils.Extensions.CLoader.CLoader.locate_lib" class="docs-object-method">&nbsp;</a>
```python
locate_lib(self, root=None): 
```
Tries to locate the build library file (if it exists)
- `:returns`: `_`
    >No description...

<a id="McUtils.Extensions.CLoader.CLoader.cleanup" class="docs-object-method">&nbsp;</a>
```python
cleanup(self): 
```





___

[Edit Examples](https://github.com/McCoyGroup/McUtils/edit/edit/ci/examples/ci/docs/McUtils/Extensions/CLoader/CLoader.md) or 
[Create New Examples](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/examples/ci/docs/McUtils/Extensions/CLoader/CLoader.md) <br/>
[Edit Template](https://github.com/McCoyGroup/McUtils/edit/edit/ci/docs/ci/docs/McUtils/Extensions/CLoader/CLoader.md) or 
[Create New Template](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/docs/templates/ci/docs/McUtils/Extensions/CLoader/CLoader.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/edit/McUtils/Extensions/CLoader.py?message=Update%20Docs)