## <a id="McUtils.Scaffolding.Persistence.ResourceManager">ResourceManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Persistence.py#L231)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Persistence.py#L231?message=Update%20Docs)]
</div>

A very simple framework for writing resources to a given directory
Designed to be extended and to support metadata







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_resource_name: str
base_location: NoneType
location_env_var: NoneType
use_temporary: bool
blacklist_files: list
binary_resource: bool
json_resource: bool
resource_function: NoneType
```
<a id="McUtils.Scaffolding.Persistence.ResourceManager.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name=None, location=None, write_metadata=False, temporary=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Persistence/ResourceManager.py#L238)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Persistence/ResourceManager.py#L238?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Persistence.ResourceManager.resolve_shared_directory" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_shared_directory(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L246)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L246?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_default_base_location" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_default_base_location(cls, temporary=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L250)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L250?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_base_location" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_base_location(cls, temporary=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L256)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L256?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_resource_path" class="docs-object-method">&nbsp;</a> 
```python
get_resource_path(self, *path): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Persistence/ResourceManager.py#L265)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Persistence/ResourceManager.py#L265?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Persistence.ResourceManager.list_resources" class="docs-object-method">&nbsp;</a> 
```python
list_resources(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Persistence/ResourceManager.py#L269)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Persistence/ResourceManager.py#L269?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Persistence.ResourceManager.save_resource" class="docs-object-method">&nbsp;</a> 
```python
save_resource(self, loc, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Persistence/ResourceManager.py#L280)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Persistence/ResourceManager.py#L280?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Persistence.ResourceManager.load_resource" class="docs-object-method">&nbsp;</a> 
```python
load_resource(self, loc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Persistence/ResourceManager.py#L286)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Persistence/ResourceManager.py#L286?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_metadata_filename" class="docs-object-method">&nbsp;</a> 
```python
get_metadata_filename(self, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Persistence/ResourceManager.py#L293)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Persistence/ResourceManager.py#L293?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_resource_metadata" class="docs-object-method">&nbsp;</a> 
```python
get_resource_metadata(self, loc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Persistence/ResourceManager.py#L295)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Persistence/ResourceManager.py#L295?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_resource_filename" class="docs-object-method">&nbsp;</a> 
```python
get_resource_filename(self, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Persistence/ResourceManager.py#L297)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Persistence/ResourceManager.py#L297?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_resource" class="docs-object-method">&nbsp;</a> 
```python
get_resource(self, name, resource_function=None, load_resource=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/Persistence/ResourceManager.py#L301)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Persistence/ResourceManager.py#L301?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Persistence/ResourceManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Persistence/ResourceManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Persistence/ResourceManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Persistence/ResourceManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/Persistence.py#L231?message=Update%20Docs)   
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