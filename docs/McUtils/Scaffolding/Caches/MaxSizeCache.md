## <a id="McUtils.Scaffolding.Caches.MaxSizeCache">MaxSizeCache</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches.py#L339)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches.py#L339?message=Update%20Docs)]
</div>

Simple lru-cache to support ravel/unravel ops







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
Backends: Backends
cache_types: OptionsMethodDispatch
```
<a id="McUtils.Scaffolding.Caches.MaxSizeCache.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, max_items=128, cache_type=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches.py#L343)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches.py#L343?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a bounded cache using the selected backend and maximum entry count.
  - `max_items`: `object`
    > maximum number of entries retained before eviction
  - `cache_type`: `object`
    > backend specification, callable, or registered backend name
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Caches.MaxSizeCache.resolve_cache_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_cache_type(cls, type_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L369)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L369?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a callable or registered backend specification and instantiate the backend with its options.
  - `type_name`: `object`
    > the backend class, registered name, option specification, or factory to resolve
  - `:returns`: `MaxSizeBackend`
    > an initialized cache backend


<a id="McUtils.Scaffolding.Caches.MaxSizeCache.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/MaxSizeCache.py#L388)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/MaxSizeCache.py#L388?message=Update%20Docs)]
</div>
**LLM Docstring**

Expose the keys from the selected backend.
  - `:returns`: `collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list`
    > A view or list of the requested registry, cache, checkpoint, or mapping entries.


<a id="McUtils.Scaffolding.Caches.MaxSizeCache.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/MaxSizeCache.py#L398)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/MaxSizeCache.py#L398?message=Update%20Docs)]
</div>
**LLM Docstring**

Delegate membership testing to the backend.
  - `item`: `object`
    > the lookup key or index
  - `:returns`: `bool`
    > Whether the tested condition is satisfied.


<a id="McUtils.Scaffolding.Caches.MaxSizeCache.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/MaxSizeCache.py#L410)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/MaxSizeCache.py#L410?message=Update%20Docs)]
</div>
**LLM Docstring**

Retrieve an item through the backend, allowing policies such as LRU to update access order.
  - `item`: `object`
    > the lookup key or index
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Caches.MaxSizeCache.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Caches/MaxSizeCache.py#L422)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches/MaxSizeCache.py#L422?message=Update%20Docs)]
</div>
**LLM Docstring**

Store an item and evict one backend-selected entry when the size exceeds `max_items`.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Caches/MaxSizeCache.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Caches/MaxSizeCache.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Caches/MaxSizeCache.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Caches/MaxSizeCache.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Caches.py#L339?message=Update%20Docs)   
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