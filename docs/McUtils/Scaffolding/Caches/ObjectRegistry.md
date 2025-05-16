## <a id="McUtils.Scaffolding.Caches.ObjectRegistry">ObjectRegistry</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Caches.py#L60)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches.py#L60?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Caches/ObjectRegistry.py#L67)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches/ObjectRegistry.py#L67?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.temp_default" class="docs-object-method">&nbsp;</a> 
```python
temp_default(self, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Caches/ObjectRegistry.py#L71)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches/ObjectRegistry.py#L71?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Caches/ObjectRegistry.py#L74)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches/ObjectRegistry.py#L74?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.lookup" class="docs-object-method">&nbsp;</a> 
```python
lookup(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Caches/ObjectRegistry.py#L77)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches/ObjectRegistry.py#L77?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Caches/ObjectRegistry.py#L85)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches/ObjectRegistry.py#L85?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.register" class="docs-object-method">&nbsp;</a> 
```python
register(self, key, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Caches/ObjectRegistry.py#L88)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches/ObjectRegistry.py#L88?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Caches/ObjectRegistry.py#L90)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches/ObjectRegistry.py#L90?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Caches/ObjectRegistry.py#L93)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches/ObjectRegistry.py#L93?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.items" class="docs-object-method">&nbsp;</a> 
```python
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Caches/ObjectRegistry.py#L95)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches/ObjectRegistry.py#L95?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Caches.ObjectRegistry.values" class="docs-object-method">&nbsp;</a> 
```python
values(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Caches/ObjectRegistry.py#L97)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches/ObjectRegistry.py#L97?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Caches/ObjectRegistry.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Caches/ObjectRegistry.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Caches/ObjectRegistry.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Caches/ObjectRegistry.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Caches.py#L60?message=Update%20Docs)   
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