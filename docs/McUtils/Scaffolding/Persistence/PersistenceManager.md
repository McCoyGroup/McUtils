## <a id="McUtils.McUtils.Scaffolding.Persistence.PersistenceManager">PersistenceManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence.py#L75)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence.py#L75?message=Update%20Docs)]
</div>

Defines a manager that can load configuration data from a directory
or, maybe in the future, a SQL database or similar.
Requires class that supports `from_config` to load and `to_config` to save.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.McUtils.Scaffolding.Persistence.PersistenceManager.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, cls, persistence_loc=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L81)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L81?message=Update%20Docs)]
</div>

  - `cls`: `type`
    > 
  - `persistence_loc`: `str | None`
    > location from which to load/save objects


<a id="McUtils.McUtils.Scaffolding.Persistence.PersistenceManager.obj_loc" class="docs-object-method">&nbsp;</a> 
```python
obj_loc(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L99)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L99?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Scaffolding.Persistence.PersistenceManager.load_config" class="docs-object-method">&nbsp;</a> 
```python
load_config(self, key, make_new=False, init=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L102?message=Update%20Docs)]
</div>
Loads the config for the persistent structure named `key`
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Scaffolding.Persistence.PersistenceManager.new_config" class="docs-object-method">&nbsp;</a> 
```python
new_config(self, key, init=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L120)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L120?message=Update%20Docs)]
</div>
Creates a new space and config for the persistent structure named `key`
  - `key`: `str`
    > name for job
  - `init`: `str | dict | None`
    > initial parameters
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Scaffolding.Persistence.PersistenceManager.contains" class="docs-object-method">&nbsp;</a> 
```python
contains(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L164?message=Update%20Docs)]
</div>
Checks if `key` is a supported persistent structure
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Scaffolding.Persistence.PersistenceManager.load" class="docs-object-method">&nbsp;</a> 
```python
load(self, key, make_new=False, strict=True, init=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L175?message=Update%20Docs)]
</div>
Loads the persistent structure named `key`
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Scaffolding.Persistence.PersistenceManager.save" class="docs-object-method">&nbsp;</a> 
```python
save(self, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/PersistenceManager.py#L197?message=Update%20Docs)]
</div>
Saves requisite config data for a structure
  - `obj`: `Any`
    > 
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Persistence/PersistenceManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Persistence/PersistenceManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Persistence/PersistenceManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Persistence/PersistenceManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence.py#L75?message=Update%20Docs)   
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