## <a id="McUtils.Scaffolding.Persistence.ResourceManager">ResourceManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence.py#L271?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence.py#L278)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence.py#L278?message=Update%20Docs)]
</div>
**LLM Docstring**

Configure resource namespace, base location, metadata preference, and temporary-location policy.
  - `name`: `object`
    > registry, command, resource, or object name
  - `location`: `object`
    > explicit resource base directory, or `None` to resolve the class default
  - `write_metadata`: `object`
    > whether resource metadata should be written
  - `temporary`: `object`
    > whether a temporary base directory should be used
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Persistence.ResourceManager.resolve_shared_directory" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_shared_directory(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L302)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L302?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the user-local shared resource directory `~/.local`.
  - `:returns`: `str`
    > The resolved filesystem path or basename.


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_default_base_location" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_default_base_location(cls, temporary=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L314)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L314?message=Update%20Docs)]
</div>
**LLM Docstring**

Choose a new temporary directory or the shared user directory.
  - `temporary`: `object`
    > whether a temporary base directory should be used
  - `:returns`: `str`
    > The resolved filesystem path or basename.


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_base_location" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_base_location(cls, temporary=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L330)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L330?message=Update%20Docs)]
</div>
**LLM Docstring**

Lazily resolve and cache the class base directory from an environment variable or default location.
  - `temporary`: `object`
    > whether a temporary base directory should be used
  - `:returns`: `str`
    > The resolved filesystem path or basename.


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_resource_path" class="docs-object-method">&nbsp;</a> 
```python
get_resource_path(self, *path): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L349)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L349?message=Update%20Docs)]
</div>
**LLM Docstring**

Join the base location, resource namespace, and optional subpath components.
  - `path`: `object`
    > additional resource path components
  - `:returns`: `str`
    > The resolved filesystem path or basename.


<a id="McUtils.Scaffolding.Persistence.ResourceManager.list_resources" class="docs-object-method">&nbsp;</a> 
```python
list_resources(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L363)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L363?message=Update%20Docs)]
</div>
**LLM Docstring**

Ensure the resource directory exists and map non-blacklisted entry names to their paths.
  - `:returns`: `dict[str, str]`
    > a mapping from resource names to filesystem paths


<a id="McUtils.Scaffolding.Persistence.ResourceManager.save_resource" class="docs-object-method">&nbsp;</a> 
```python
save_resource(self, loc, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L382)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L382?message=Update%20Docs)]
</div>
**LLM Docstring**

Write a resource in binary, text, or JSON mode according to class flags.
  - `loc`: `object`
    > filesystem location
  - `val`: `object`
    > the value being stored, converted, or installed
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Persistence.ResourceManager.load_resource" class="docs-object-method">&nbsp;</a> 
```python
load_resource(self, loc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L400)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L400?message=Update%20Docs)]
</div>
**LLM Docstring**

Read and decode a resource in binary, text, or JSON mode according to class flags.
  - `loc`: `object`
    > filesystem location
  - `:returns`: `object | str | bytes`
    > decoded JSON data, text, or bytes according to class flags


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_metadata_filename" class="docs-object-method">&nbsp;</a> 
```python
get_metadata_filename(self, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L417)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L417?message=Update%20Docs)]
</div>
**LLM Docstring**

Derive the sidecar metadata filename by appending `.meta.json`.
  - `name`: `object`
    > registry, command, resource, or object name
  - `:returns`: `str`
    > The resolved filesystem path or basename.


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_resource_metadata" class="docs-object-method">&nbsp;</a> 
```python
get_resource_metadata(self, loc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L429)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L429?message=Update%20Docs)]
</div>
**LLM Docstring**

Default metadata hook, currently returning an empty dictionary.
  - `loc`: `object`
    > filesystem location
  - `:returns`: `dict`
    > an empty metadata mapping in the base implementation


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_resource_filename" class="docs-object-method">&nbsp;</a> 
```python
get_resource_filename(self, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L441)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L441?message=Update%20Docs)]
</div>
**LLM Docstring**

Default filename hook, currently returning the resource name unchanged.
  - `name`: `object`
    > registry, command, resource, or object name
  - `:returns`: `str`
    > The resolved filesystem path or basename.


<a id="McUtils.Scaffolding.Persistence.ResourceManager.get_resource" class="docs-object-method">&nbsp;</a> 
```python
get_resource(self, name, resource_function=None, load_resource=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L455)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence/ResourceManager.py#L455?message=Update%20Docs)]
</div>
**LLM Docstring**

Return an existing resource, or generate and persist it with the configured factory before loading it.
  - `name`: `object`
    > registry, command, resource, or object name
  - `resource_function`: `object`
    > factory used to create a missing resource
  - `load_resource`: `object`
    > whether to return loaded content instead of its path
  - `:returns`: `object | str | None`
    > loaded resource content, its path when `load_resource=False`, or `None` when unavailable
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Persistence.py#L271?message=Update%20Docs)   
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