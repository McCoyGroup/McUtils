## <a id="McUtils.Extensions.ArgumentSignature.FunctionSignature">FunctionSignature</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature.py#L438)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature.py#L438?message=Update%20Docs)]
</div>

Defines a function signature for a C-level caller.
To be used inside `SharedLibraryFunction` and things to manage the core interface.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name, *args, defaults=None, return_type=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/FunctionSignature.py#L444)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/FunctionSignature.py#L444?message=Update%20Docs)]
</div>

  - `name`: `str`
    > the name of the function
  - `args`: `Iterable[ArgumentType]`
    > the arguments passed to the function
  - `return_type`: `ArgumentType | None`
    > the return type of the function


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.construct" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct(cls, name, defaults=None, return_type=None, **args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L462)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L462?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.build_argument" class="docs-object-method">&nbsp;</a> 
```python
build_argument(self, argtup, which=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/FunctionSignature.py#L471)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/FunctionSignature.py#L471?message=Update%20Docs)]
</div>
Converts an argument tuple into an Argument object
  - `argtup`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.args" class="docs-object-method">&nbsp;</a> 
```python
@property
args(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/FunctionSignature.py#L494)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/FunctionSignature.py#L494?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.return_argtype" class="docs-object-method">&nbsp;</a> 
```python
@property
return_argtype(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/FunctionSignature.py#L497)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/FunctionSignature.py#L497?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.return_type" class="docs-object-method">&nbsp;</a> 
```python
@property
return_type(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/FunctionSignature.py#L500)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/FunctionSignature.py#L500?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.arg_types" class="docs-object-method">&nbsp;</a> 
```python
@property
arg_types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/FunctionSignature.py#L506)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/FunctionSignature.py#L506?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.cpp_signature" class="docs-object-method">&nbsp;</a> 
```python
@property
cpp_signature(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/FunctionSignature.py#L510)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/FunctionSignature.py#L510?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.populate_kwargs" class="docs-object-method">&nbsp;</a> 
```python
populate_kwargs(self, args, kwargs, defaults=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/FunctionSignature.py#L518)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/FunctionSignature.py#L518?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.prep_args" class="docs-object-method">&nbsp;</a> 
```python
prep_args(self, args, kwargs, defaults=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/FunctionSignature.py#L539)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/FunctionSignature.py#L539?message=Update%20Docs)]
</div>


<a id="McUtils.Extensions.ArgumentSignature.FunctionSignature.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Extensions/ArgumentSignature/FunctionSignature.py#L551)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature/FunctionSignature.py#L551?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/ArgumentSignature/FunctionSignature.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/ArgumentSignature/FunctionSignature.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/ArgumentSignature/FunctionSignature.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/ArgumentSignature/FunctionSignature.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Extensions/ArgumentSignature.py#L438?message=Update%20Docs)   
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