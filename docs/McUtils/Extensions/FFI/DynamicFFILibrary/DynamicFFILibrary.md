## <a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFILibrary">DynamicFFILibrary</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L268)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L268?message=Update%20Docs)]
</div>

Directly analogous to a regular shared library but it uses
`DynamicFFIFunction` to dispatch calls







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
method_type: DynamicFFIFunction
```
<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFILibrary.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, library, compiler_options=None, **functions): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L275)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L275?message=Update%20Docs)]
</div>
**LLM Docstring**

Create a dynamic FFI library and retain optional compiler configuration for lazy application.
  - `library`: `Any`
    > library path or loader

  - `compiler_options`: `Any`
    > options applied before the first function lookup

  - `functions`: `dict[str, Any]`
    > registered function definitions

  - `:returns`: `None`
    > nothing; initializes the library


<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFILibrary.get_function" class="docs-object-method">&nbsp;</a> 
```python
get_function(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFILibrary.py#L302)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFILibrary.py#L302?message=Update%20Docs)]
</div>
**LLM Docstring**

Apply compiler options once on first access, then retrieve a registered function.
  - `item`: `Any`
    > registered function tag

  - `:returns`: `DynamicFFIFunction`
    > the requested function


<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFILibrary.configure_loader" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
configure_loader(cls, **compile_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L319)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L319?message=Update%20Docs)]
</div>
**LLM Docstring**

Forward compile options to the singleton dynamic FFI loader.
  - `compile_opts`: `dict[str, Any]`
    > compiler and loader options

  - `:returns`: `None`
    > nothing; updates global loader configuration
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFILibrary.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFILibrary.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFILibrary.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFILibrary.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L268?message=Update%20Docs)   
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