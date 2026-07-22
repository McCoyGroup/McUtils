## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateWalker">TemplateWalker</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1896)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1896?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
module_handler: ModuleTemplateHandler
class_handler: ClassTemplateHandler
function_handler: FunctionTemplateHandler
method_handler: MethodTemplateHandler
object_handler: ObjectTemplateHandler
index_handler: IndexTemplateHandler
```
<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateWalker.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, engine: McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateEngine, out=None, description=None, **extra_fields): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1903)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1903?message=Update%20Docs)]
</div>
**LLM Docstring**

Store template-engine output settings and initialize the underlying object walker.
  - `engine`: `TemplateEngine`
    > the template engine used to render content
  - `out`: `Any`
    > the output root, file, or stream
  - `description`: `Any`
    > the description passed to the generated index
  - `extra_fields`: `Any`
    > additional fields exposed to handlers and templates

  - `:returns`: `None`
    > `None`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateWalker.default_handlers" class="docs-object-method">&nbsp;</a> 
```python
@property
default_handlers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.py#L1926)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.py#L1926?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the ordered mapping from modules, classes, functions, and fallback objects to handler classes.
  - `:returns`: `Any`
    > The ordered mapping from dispatch tests to handler classes.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateWalker.get_handler" class="docs-object-method">&nbsp;</a> 
```python
get_handler(self, obj, *, out=None, engine=None, tree=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.py#L1943)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.py#L1943?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a handler while injecting this walker’s output directory and template engine.
  - `obj`: `Any`
    > the object to inspect or dispatch
  - `out`: `Any`
    > the output root, file, or stream
  - `engine`: `Any`
    > the template engine used to render content
  - `tree`: `Any`
    > the shared object-documentation tree
  - `kwargs`: `Any`
    > keyword arguments forwarded to the wrapped callable

  - `:returns`: `Any`
    > The handler constructed with this walker’s engine and output settings.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateWalker.visit_root" class="docs-object-method">&nbsp;</a> 
```python
visit_root(self, o, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.py#L1971)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.py#L1971?message=Update%20Docs)]
</div>
**LLM Docstring**

Visit a root object through the standard traversal implementation.
  - `o`: `Any`
    > the object or import path to resolve
  - `kwargs`: `Any`
    > keyword arguments forwarded to the wrapped callable

  - `:returns`: `Any`
    > The result returned by visiting the root object.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateWalker.write" class="docs-object-method">&nbsp;</a> 
```python
write(self, objects, max_depth=-1, index='index.md'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.py#L1987)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.py#L1987?message=Update%20Docs)]
</div>
Walks through the objects supplied and applies the appropriate templates
  - `:returns`: `str`
    > index of written files
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateWalker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1896?message=Update%20Docs)   
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