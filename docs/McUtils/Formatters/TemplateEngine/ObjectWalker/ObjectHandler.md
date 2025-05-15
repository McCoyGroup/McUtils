## <a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler">ObjectHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker.py#L115?message=Update%20Docs)]
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
<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, obj, *, spec=None, tree=None, name=None, parent=None, walker: 'ObjectWalker' = None, extra_fields=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L118)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L118?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L152?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.resolve_key" class="docs-object-method">&nbsp;</a> 
```python
resolve_key(self, key, default=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L154?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.name" class="docs-object-method">&nbsp;</a> 
```python
@property
name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L162)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L162?message=Update%20Docs)]
</div>
Returns the name (not full identifier) of the object
being documented
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.get_name" class="docs-object-method">&nbsp;</a> 
```python
get_name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L173)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L173?message=Update%20Docs)]
</div>
Returns the name the object will have in its documentation page
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.get_identifier" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_identifier(cls, o): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L190)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L190?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.identifier" class="docs-object-method">&nbsp;</a> 
```python
@property
identifier(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L207)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L207?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.parent" class="docs-object-method">&nbsp;</a> 
```python
@property
parent(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L213)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L213?message=Update%20Docs)]
</div>
Returns the parent object for docs purposes
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.resolve_parent" class="docs-object-method">&nbsp;</a> 
```python
resolve_parent(self, check_tree=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L224)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L224?message=Update%20Docs)]
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


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.resolve_relative_obj" class="docs-object-method">&nbsp;</a> 
```python
resolve_relative_obj(self, spec: str): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L271?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.children" class="docs-object-method">&nbsp;</a> 
```python
@property
children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L302)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L302?message=Update%20Docs)]
</div>
Returns the child objects for docs purposes
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.resolve_children" class="docs-object-method">&nbsp;</a> 
```python
resolve_children(self, check_tree=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L313)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L313?message=Update%20Docs)]
</div>
Resolves the "children" of obj.
First tries to use any info supplied by the docs tree
or a passed object spec, then that failing looks for an
`__all__` attribute
  - `obj`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.tree_spec" class="docs-object-method">&nbsp;</a> 
```python
@property
tree_spec(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L342)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L342?message=Update%20Docs)]
</div>
Provides info that gets added to the `written` dict and which allows
for a doc tree to be built out.
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.handle" class="docs-object-method">&nbsp;</a> 
```python
handle(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L360)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L360?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TemplateEngine.ObjectWalker.ObjectHandler.stop_traversal" class="docs-object-method">&nbsp;</a> 
```python
stop_traversal(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L363)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.py#L363?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/ObjectWalker/ObjectHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/ObjectWalker.py#L115?message=Update%20Docs)   
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