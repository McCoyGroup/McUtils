## <a id="McUtils.Scaffolding.ObjectBackers.FileBackedObjectManager">FileBackedObjectManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/ObjectBackers.py#L74)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/ObjectBackers.py#L74?message=Update%20Docs)]
</div>

Provides an interface to back an object with
a serializer







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_directory: PersistenceLocation
```
<a id="McUtils.Scaffolding.ObjectBackers.FileBackedObjectManager.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, obj, chk=None, loc=None, checkpoint_class=<class 'McUtils.Scaffolding.Checkpointing.NumPyCheckpointer'>): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/ObjectBackers/FileBackedObjectManager.py#L81)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/ObjectBackers/FileBackedObjectManager.py#L81?message=Update%20Docs)]
</div>

  - `obj`: `object`
    > the object to back
  - `chk`: `Checkpointer`
    > a checkpointer to manage storing attributes
  - `loc`: `str`
    > the location where attributes should be stored
  - `checkpoint_class`: `Type[Checkpointer]`
    > a subclass of Checkpointer that implements the actual writing to disk


<a id="McUtils.Scaffolding.ObjectBackers.FileBackedObjectManager.basename" class="docs-object-method">&nbsp;</a> 
```python
@property
basename(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/ObjectBackers/FileBackedObjectManager.py#L108)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/ObjectBackers/FileBackedObjectManager.py#L108?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.ObjectBackers.FileBackedObjectManager.get_basename" class="docs-object-method">&nbsp;</a> 
```python
get_basename(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/ObjectBackers/FileBackedObjectManager.py#L117)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/ObjectBackers/FileBackedObjectManager.py#L117?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.ObjectBackers.FileBackedObjectManager.save_attr" class="docs-object-method">&nbsp;</a> 
```python
save_attr(self, attr): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/ObjectBackers/FileBackedObjectManager.py#L124)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/ObjectBackers/FileBackedObjectManager.py#L124?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.ObjectBackers.FileBackedObjectManager.load_attr" class="docs-object-method">&nbsp;</a> 
```python
load_attr(self, attr): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/ObjectBackers/FileBackedObjectManager.py#L129)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/ObjectBackers/FileBackedObjectManager.py#L129?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/ObjectBackers/FileBackedObjectManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/ObjectBackers/FileBackedObjectManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/ObjectBackers/FileBackedObjectManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/ObjectBackers/FileBackedObjectManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/ObjectBackers.py#L74?message=Update%20Docs)   
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