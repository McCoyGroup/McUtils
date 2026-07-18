## <a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunctionLoader">DynamicFFIFunctionLoader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L11)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L11?message=Update%20Docs)]
</div>

This is a singleton class that can be set to define the global
linkage to the DynamicLibrary extension module







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunctionLoader.configure" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
configure(cls, **compile_args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L19?message=Update%20Docs)]
</div>
**LLM Docstring**

Merge compiler options into the process-wide dynamic FFI loader configuration.
  - `compile_args`: `dict[str, Any]`
    > compiler and loader options

  - `:returns`: `None`
    > nothing; updates the shared configuration


<a id="McUtils.Extensions.FFI.DynamicFFILibrary.DynamicFFIFunctionLoader.load" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L33)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L33?message=Update%20Docs)]
</div>
**LLM Docstring**

Compile or load and cache the bundled dynamic FFI support module.
  - `:returns`: `FFIModule`
    > the singleton caller module
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunctionLoader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunctionLoader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunctionLoader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/FFI/DynamicFFILibrary/DynamicFFIFunctionLoader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/FFI/DynamicFFILibrary.py#L11?message=Update%20Docs)   
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