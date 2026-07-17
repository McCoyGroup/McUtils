## <a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler">ObjectHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker.py#L175?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
protected_fields: set
default_fields: dict
```
<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, obj, *, spec=None, tree=None, name=None, parent=None, walker: 'ObjectWalker' = None, extra_fields=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker.py#L178)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker.py#L178?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize handler state, merge extra fields with defaults, and remove protected field overrides.
  - `obj`: `Any`
    > the object to inspect or dispatch
  - `spec`: `Any`
    > the object specification or template expression
  - `tree`: `Any`
    > the shared object-documentation tree
  - `name`: `Any`
    > an explicit display name
  - `parent`: `Any`
    > the parent object or handler
  - `walker`: `'ObjectWalker'`
    > the walker used to resolve related objects
  - `extra_fields`: `Any`
    > additional fields exposed to handlers and templates
  - `kwargs`: `Any`
    > keyword arguments forwarded to the wrapped callable

  - `:returns`: `None`
    > `None`.


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L237)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L237?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a handler field from the object specification or extra field mapping.
  - `item`: `Any`
    > the field name or positional key to resolve

  - `:returns`: `Any`
    > The resolved specification or extra-field value.


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.resolve_key" class="docs-object-method">&nbsp;</a> 
```python
resolve_key(self, key, default=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L250)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L250?message=Update%20Docs)]
</div>
**LLM Docstring**

Look up a field in the object specification first and then in the extra field mapping.
  - `key`: `Any`
    > the lookup, assignment, or formatting key
  - `default`: `Any`
    > fallback callable or value used when no match is found

  - `:returns`: `Any`
    > The matching specification or extra-field value, or `default` when absent.


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.name" class="docs-object-method">&nbsp;</a> 
```python
@property
name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L271?message=Update%20Docs)]
</div>
Returns the name (not full identifier) of the object
being documented
  - `:returns`: `_`
    >


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.get_name" class="docs-object-method">&nbsp;</a> 
```python
get_name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L282)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L282?message=Update%20Docs)]
</div>
Returns the name the object will have in its documentation page
  - `:returns`: `_`
    >


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.get_identifier" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_identifier(cls, o): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L299)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L299?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a dotted identifier from an explicit identifier, module name, and qualified object name.
  - `o`: `Any`
    > the object or import path to resolve

  - `:returns`: `Any`
    > The dotted identifier assembled for the object.


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.identifier" class="docs-object-method">&nbsp;</a> 
```python
@property
identifier(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L330)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L330?message=Update%20Docs)]
</div>
**LLM Docstring**

Lazily compute and cache the dotted identifier for the handled object.
  - `:returns`: `Any`
    > The cached dotted identifier for the handled object.


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.parent" class="docs-object-method">&nbsp;</a> 
```python
@property
parent(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L344)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L344?message=Update%20Docs)]
</div>
Returns the parent object for docs purposes
  - `:returns`: `_`
    >


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.resolve_parent" class="docs-object-method">&nbsp;</a> 
```python
resolve_parent(self, check_tree=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L355)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L355?message=Update%20Docs)]
</div>
Resolves the "parent" of obj.
By default, just the module in which it is contained.
Allows for easy skipping of pieces of the object tree,
though, since a parent can be directly added to the set of
written object which is distinct from the module it would
usually resolve to.
Also can be subclassed to provide more fine grained behavior.
  - `obj`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.resolve_relative_obj" class="docs-object-method">&nbsp;</a> 
```python
resolve_relative_obj(self, spec: str): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L402)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L402?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a relative or attribute-based object specification against the handled object and its module.
  - `spec`: `str`
    > the object specification or template expression

  - `:returns`: `Any`
    > The object resolved from the relative specification.


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.children" class="docs-object-method">&nbsp;</a> 
```python
@property
children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L444)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L444?message=Update%20Docs)]
</div>
Returns the child objects for docs purposes
  - `:returns`: `_`
    >


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.resolve_children" class="docs-object-method">&nbsp;</a> 
```python
resolve_children(self, check_tree=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L455)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L455?message=Update%20Docs)]
</div>
Resolves the "children" of obj.
First tries to use any info supplied by the docs tree
or a passed object spec, then that failing looks for an
`__all__` attribute
  - `obj`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.tree_spec" class="docs-object-method">&nbsp;</a> 
```python
@property
tree_spec(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L484)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L484?message=Update%20Docs)]
</div>
Provides info that gets added to the `written` dict and which allows
for a doc tree to be built out.
  - `:returns`: `_`
    >


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.handle" class="docs-object-method">&nbsp;</a> 
```python
handle(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L502)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L502?message=Update%20Docs)]
</div>
**LLM Docstring**

Define the abstract operation performed after an object and its descendants have been traversed.
  - `:returns`: `Any`
    > The handler-specific traversal result.


<a id="McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.stop_traversal" class="docs-object-method">&nbsp;</a> 
```python
stop_traversal(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L513)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L513?message=Update%20Docs)]
</div>
**LLM Docstring**

Report whether traversal should stop before recording or visiting the handled object.
  - `:returns`: `bool`
    > `False`, allowing traversal to continue by default.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker.py#L175?message=Update%20Docs)   
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