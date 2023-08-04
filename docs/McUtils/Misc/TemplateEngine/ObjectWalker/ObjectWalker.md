## <a id="McUtils.Misc.TemplateEngine.ObjectWalker.ObjectWalker">ObjectWalker</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateEngine/ObjectWalker.py#L366)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateEngine/ObjectWalker.py#L366?message=Update%20Docs)]
</div>

A class that walks a module/object structure, calling handlers
appropriately at each step

A class that walks a module structure, generating .md files for every class inside it as well as for global functions,
and a Markdown index file.

Takes a set of objects & writers and walks through the objects, generating files on the way







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
spec: ObjectSpec
default_handlers: OrderedDict
```
<a id="McUtils.Misc.TemplateEngine.ObjectWalker.ObjectWalker.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, handlers=None, tree=None, **extra_fields): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateEngine/ObjectWalker/ObjectWalker.py#L379)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateEngine/ObjectWalker/ObjectWalker.py#L379?message=Update%20Docs)]
</div>

  - `objects`: `Iterable[Any]`
    > the objects to write out
  - `out`: `None | str`
    > the directory in which to write the files (`None` means `sys.stdout`)
the directory in which to write the files (`None` means `sys.stdout`)
  - ``: `DispatchTable`
    > writers
  - `ignore_paths`: `None | Iterable[str]`
    > a set of paths not to write (passed to the objects)


<a id="McUtils.Misc.TemplateEngine.ObjectWalker.ObjectWalker.get_handler" class="docs-object-method">&nbsp;</a> 
```python
get_handler(self, obj, *, tree=None, walker=None, cls=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateEngine/ObjectWalker/ObjectWalker.py#L430)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateEngine/ObjectWalker/ObjectWalker.py#L430?message=Update%20Docs)]
</div>


<a id="McUtils.Misc.TemplateEngine.ObjectWalker.ObjectWalker.resolve_object" class="docs-object-method">&nbsp;</a> 
```python
resolve_object(o): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateEngine/ObjectWalker/ObjectWalker.py#L437)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateEngine/ObjectWalker/ObjectWalker.py#L437?message=Update%20Docs)]
</div>
Resolves to an arbitrary object by name
  - `o`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Misc.TemplateEngine.ObjectWalker.ObjectWalker.resolve_spec" class="docs-object-method">&nbsp;</a> 
```python
resolve_spec(self, spec, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateEngine/ObjectWalker/ObjectWalker.py#L486)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateEngine/ObjectWalker/ObjectWalker.py#L486?message=Update%20Docs)]
</div>
Resolves an object spec.
  - `spec`: `ObjectSpec`
    > object spec
  - `:returns`: `_`
    >


<a id="McUtils.Misc.TemplateEngine.ObjectWalker.ObjectWalker.visit" class="docs-object-method">&nbsp;</a> 
```python
visit(self, o, parent=None, depth=0, max_depth=-1, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateEngine/ObjectWalker/ObjectWalker.py#L501)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateEngine/ObjectWalker/ObjectWalker.py#L501?message=Update%20Docs)]
</div>
Visits a single object in the tree
Provides type dispatching to a handler, basically.
  - `o`: `Any`
    > the object we want to handler
  - `parent`: `ObjectHandler`
    > the handler that was called right before this
  - `:returns`: `Any`
    > t
h
e
 
r
e
s
u
l
t
 
o
f
 
h
a
n
d
l
i
n
g
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Misc/TemplateEngine/ObjectWalker/ObjectWalker.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Misc/TemplateEngine/ObjectWalker/ObjectWalker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Misc/TemplateEngine/ObjectWalker/ObjectWalker.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Misc/TemplateEngine/ObjectWalker/ObjectWalker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateEngine/ObjectWalker.py#L366?message=Update%20Docs)   
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