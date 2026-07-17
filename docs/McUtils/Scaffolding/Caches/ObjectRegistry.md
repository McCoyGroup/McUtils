## <a id="McUtils.Scaffolding.Caches.ObjectRegistry">ObjectRegistry</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches.py#L488)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches.py#L488?message=Update%20Docs)]
</div>

Provides a simple interface to global object registries
so that pieces of code don't need to pass things like loggers
or parallelizers through every step of the code







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Scaffolding.Caches.ObjectRegistry.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, default='raise'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches.py#L495)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches.py#L495?message=Update%20Docs)]
</div>
**LLM Docstring**

Create a weak-value registry with configurable behavior for missing keys.
  - `default`: `object`
    > the fallback returned when a key is absent
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.temp_default" class="docs-object-method">&nbsp;</a> 
```python
temp_default(self, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L509)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L509?message=Update%20Docs)]
</div>
**LLM Docstring**

Create a context manager that temporarily replaces the registry fallback value.
  - `val`: `object`
    > the value being stored, converted, or installed
  - `:returns`: `object`
    > The resolved or newly constructed helper object.


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L522)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L522?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether a live weakly referenced object is registered under a key.
  - `item`: `object`
    > the lookup key or index
  - `:returns`: `bool`
    > Whether the tested condition is satisfied.


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.lookup" class="docs-object-method">&nbsp;</a> 
```python
lookup(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L535)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L535?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the registered object, or the configured default when missing-key lookup is non-raising.
  - `key`: `object`
    > the storage or lookup key
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L553)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L553?message=Update%20Docs)]
</div>
**LLM Docstring**

Look up a registry key using the configured missing-key policy.
  - `item`: `object`
    > the lookup key or index
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.register" class="docs-object-method">&nbsp;</a> 
```python
register(self, key, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L566)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L566?message=Update%20Docs)]
</div>
**LLM Docstring**

Store a weak reference to `val` under `key`.
  - `key`: `object`
    > the storage or lookup key
  - `val`: `object`
    > the value being stored, converted, or installed
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L580)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L580?message=Update%20Docs)]
</div>
**LLM Docstring**

Register a value using dictionary assignment syntax.
  - `key`: `object`
    > the storage or lookup key
  - `value`: `object`
    > the value to store
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L595)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L595?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the live registry keys.
  - `:returns`: `collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list`
    > A view or list of the requested registry, cache, checkpoint, or mapping entries.


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.items" class="docs-object-method">&nbsp;</a> 
```python
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L605)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L605?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the live registry key/value pairs.
  - `:returns`: `collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list`
    > A view or list of the requested registry, cache, checkpoint, or mapping entries.


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.values" class="docs-object-method">&nbsp;</a> 
```python
values(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L615)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/ObjectRegistry.py#L615?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the live registered objects.
  - `:returns`: `collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list`
    > A view or list of the requested registry, cache, checkpoint, or mapping entries.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Caches/ObjectRegistry.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Caches/ObjectRegistry.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Caches/ObjectRegistry.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Caches/ObjectRegistry.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches.py#L488?message=Update%20Docs)   
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