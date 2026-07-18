## <a id="McUtils.Extensions.SharedLibraryManager.SharedLibrary">SharedLibrary</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager.py#L398)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager.py#L398?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
method_type: SharedLibraryFunction
```
<a id="McUtils.Extensions.SharedLibraryManager.SharedLibrary.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, library, **functions): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager.py#L401)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager.py#L401?message=Update%20Docs)]
</div>
**LLM Docstring**

Create a shared-library facade and optionally register functions from configuration dictionaries.
  - `library`: `str | ctypes.CDLL | SharedLibraryLoader`
    > library path, handle, or loader

  - `functions`: `dict[str, dict]`
    > registration options keyed by exposed attribute name

  - `:returns`: `None`
    > no value is returned


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibrary.register" class="docs-object-method">&nbsp;</a> 
```python
register(self, tag, name=None, docstring=None, defaults=None, return_handler=None, prep_args=None, **params): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager/SharedLibrary.py#L426)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager/SharedLibrary.py#L426?message=Update%20Docs)]
</div>
**LLM Docstring**

Register and return a callable wrapper for one library function.

The exposed `tag` may differ from the native function `name`; remaining keyword parameters define the `FunctionSignature` arguments.
  - `tag`: `str`
    > lookup name stored in the facade

  - `name`: `str | None`
    > native symbol name, defaulting to `tag`

  - `docstring`: `str | None`
    > optional function documentation

  - `defaults`: `dict | None`
    > argument defaults

  - `return_handler`: `Callable | None`
    > raw-result postprocessor

  - `prep_args`: `Callable | None`
    > keyword-argument preprocessing callback

  - `params`: `dict[str, Any]`
    > argument names mapped to type specifications

  - `:returns`: `SharedLibraryFunction`
    > registered function wrapper


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibrary.get_function" class="docs-object-method">&nbsp;</a> 
```python
get_function(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager/SharedLibrary.py#L471)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager/SharedLibrary.py#L471?message=Update%20Docs)]
</div>
**LLM Docstring**

Retrieve a registered function wrapper by tag.
  - `item`: `str`
    > registered function tag

  - `:returns`: `SharedLibraryFunction`
    > registered wrapper


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibrary.__getattr__" class="docs-object-method">&nbsp;</a> 
```python
__getattr__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager/SharedLibrary.py#L488)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager/SharedLibrary.py#L488?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve missing attributes as registered function tags.
  - `item`: `str`
    > attribute name

  - `:returns`: `SharedLibraryFunction`
    > registered wrapper


<a id="McUtils.Extensions.SharedLibraryManager.SharedLibrary.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/SharedLibraryManager/SharedLibrary.py#L502)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager/SharedLibrary.py#L502?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation of the library facade.

The current formatting expression passes a generator to `str.format` without a placeholder and therefore does not list the registered signatures.
  - `:returns`: `str`
    > representation string
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions/SharedLibraryManager/SharedLibrary.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions/SharedLibraryManager/SharedLibrary.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions/SharedLibraryManager/SharedLibrary.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions/SharedLibraryManager/SharedLibrary.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/SharedLibraryManager.py#L398?message=Update%20Docs)   
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