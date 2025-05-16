## <a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction">SharedLibraryFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/SharedLibraryManager.py#L59)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/SharedLibraryManager.py#L59?message=Update%20Docs)]
</div>

An object that provides a way to call into a shared library function







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, shared_library, signature: McUtils.Extensions.ArgumentSignature.FunctionSignature, defaults=None, docstring=None, call_directory=None, return_handler=None, prep_args=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L64)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L64?message=Update%20Docs)]
</div>

  - `shared_library`: `str |`
    > the path to the shared library file you want to use
  - `function_signature`: `FunctionSignature`
    > the signature of the function to load
  - `call_directory`: `str`
    > the directory for calling
  - `docstring`: `str`
    > the docstring for the function


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.construct" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct(cls, name, lib, docstring=None, defaults=None, return_type=None, return_handler=None, **args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L99)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L99?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.function" class="docs-object-method">&nbsp;</a> 
```python
@property
function(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L122)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L122?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.initialize" class="docs-object-method">&nbsp;</a> 
```python
initialize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L126)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L126?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.doc" class="docs-object-method">&nbsp;</a> 
```python
doc(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L136)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L136?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L138)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L138?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.signature" class="docs-object-method">&nbsp;</a> 
```python
@property
signature(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L145)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L145?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.uncast" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
uncast(cls, res): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L152?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.call" class="docs-object-method">&nbsp;</a> 
```python
call(self, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L170)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L170?message=Update%20Docs)]
</div>
Calls the function we loaded.
This will be parallelized out to handle more complicated usages.
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibraryFunction.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/SharedLibraryManager/SharedLibraryFunction.py#L188?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/SharedLibraryManager/SharedLibraryFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/SharedLibraryManager.py#L59?message=Update%20Docs)   
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