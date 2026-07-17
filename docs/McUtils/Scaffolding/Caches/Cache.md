## <a id="McUtils.Scaffolding.Caches.Cache">Cache</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches.py#L12)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches.py#L12?message=Update%20Docs)]
</div>

Simple cache base class







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Scaffolding.Caches.Cache.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/Cache.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/Cache.py#L16?message=Update%20Docs)]
</div>
**LLM Docstring**

Retrieve a cached value for `item`; concrete cache classes define the storage and access policy.

This is an abstract or unfinished implementation and raises `NotImplementedError`.
  - `item`: `object`
    > the lookup key or index
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Caches.Cache.get" class="docs-object-method">&nbsp;</a> 
```python
get(self, item, default=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/Cache.py#L31)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/Cache.py#L31?message=Update%20Docs)]
</div>
**LLM Docstring**

Retrieve `item`, returning `default` only when the cache raises `KeyError`.
  - `item`: `object`
    > the lookup key or index
  - `default`: `object`
    > the fallback returned when a key is absent
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Caches.Cache.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/Cache.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/Cache.py#L48?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether an item is present in the concrete cache backend.

This is an abstract or unfinished implementation and raises `NotImplementedError`.
  - `item`: `object`
    > the lookup key or index
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Caches.Cache.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/Cache.py#L63)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/Cache.py#L63?message=Update%20Docs)]
</div>
**LLM Docstring**

Store a value under a cache key using the concrete backend policy.

This is an abstract or unfinished implementation and raises `NotImplementedError`.
  - `key`: `object`
    > the storage or lookup key
  - `value`: `object`
    > the value to store
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Caches/Cache.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Caches/Cache.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Caches/Cache.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Caches/Cache.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches.py#L12?message=Update%20Docs)   
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