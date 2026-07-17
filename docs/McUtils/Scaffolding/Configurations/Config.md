## <a id="McUtils.Scaffolding.Configurations.Config">Config</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations.py#L13)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations.py#L13?message=Update%20Docs)]
</div>

A configuration object which basically just supports
a dictionary interface, but which also can automatically
filter itself so that it only provides the keywords supported
by a `from_config` method.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
config_file_name: str
config_file_extensions: list
```
<a id="McUtils.Scaffolding.Configurations.Config.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, config, serializer=None, extra_params=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations.py#L20?message=Update%20Docs)]
</div>
Loads the config from a file
  - `config`: `str`
    > 
  - `serializer`: `None | BaseSerializer`
    >


<a id="McUtils.Scaffolding.Configurations.Config.find_config" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
find_config(self, config, name=None, extensions=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L37?message=Update%20Docs)]
</div>
Finds configuration file (if config isn't a file)
  - `config`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Configurations.Config.get_serializer" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_serializer(self, file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L65)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L65?message=Update%20Docs)]
</div>
**LLM Docstring**

Select a serializer instance from the configuration file extension.
  - `file`: `object`
    > path or file-like object
  - `:returns`: `object`
    > The resolved or newly constructed helper object.


<a id="McUtils.Scaffolding.Configurations.Config.new" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
new(cls, loc, init=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L83)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L83?message=Update%20Docs)]
</div>
**LLM Docstring**

Create the default JSON configuration file in a directory and initialize it with the supplied mapping.
  - `loc`: `object`
    > filesystem location
  - `init`: `object`
    > initial configuration mapping or source
  - `:returns`: `object`
    > The newly constructed object.


<a id="McUtils.Scaffolding.Configurations.Config.serialize" class="docs-object-method">&nbsp;</a> 
```python
serialize(self, file, ops): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L107)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L107?message=Update%20Docs)]
</div>
**LLM Docstring**

Choose the configured or extension-derived serializer and write options to a text file.
  - `file`: `object`
    > path or file-like object
  - `ops`: `object`
    > options mapping to serialize
  - `:returns`: `None | object`
    > No explicit value unless noted by the underlying delegated operation.


<a id="McUtils.Scaffolding.Configurations.Config.deserialize" class="docs-object-method">&nbsp;</a> 
```python
deserialize(self, file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L126)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L126?message=Update%20Docs)]
</div>
**LLM Docstring**

Choose the configured or extension-derived serializer and read options from a text file.
  - `file`: `object`
    > path or file-like object
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Configurations.Config.save" class="docs-object-method">&nbsp;</a> 
```python
save(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L144)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L144?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the current merged option dictionary back to the configuration file.
  - `:returns`: `None | object`
    > No explicit value unless noted by the underlying delegated operation.


<a id="McUtils.Scaffolding.Configurations.Config.load" class="docs-object-method">&nbsp;</a> 
```python
load(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L154?message=Update%20Docs)]
</div>
**LLM Docstring**

Deserialize and return the raw configuration file contents.
  - `:returns`: `object`
    > The reconstructed, loaded, or selected Python value.


<a id="McUtils.Scaffolding.Configurations.Config.name" class="docs-object-method">&nbsp;</a> 
```python
@property
name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L165)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L165?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the configured `name`, falling back to the configuration filename when absent.
  - `:returns`: `str`
    > the configured name or configuration filename


<a id="McUtils.Scaffolding.Configurations.Config.opt_dict" class="docs-object-method">&nbsp;</a> 
```python
@property
opt_dict(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L180)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L180?message=Update%20Docs)]
</div>
**LLM Docstring**

Return loaded configuration values merged with runtime-only extra parameters.
  - `:returns`: `dict`
    > a new dictionary containing file options plus runtime extras


<a id="McUtils.Scaffolding.Configurations.Config.filter" class="docs-object-method">&nbsp;</a> 
```python
filter(self, keys, strict=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L193)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L193?message=Update%20Docs)]
</div>
Returns a filtered option dictionary according to keys.
Strict mode will raise an error if there is a key in the config that isn't
in keys.
  - `keys`: `Iterable[str] | function`
    > 
  - `strict`: `bool`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Configurations.Config.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, func, strict=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L228)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L228?message=Update%20Docs)]
</div>
Applies func to stored parameters
  - `func`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Configurations.Config.update" class="docs-object-method">&nbsp;</a> 
```python
update(self, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L240)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L240?message=Update%20Docs)]
</div>
**LLM Docstring**

Merge keyword updates into the current option dictionary and persist the result.
  - `kw`: `object`
    > keyword values merged into the current configuration
  - `:returns`: `None`
    > no explicit value; the configuration file is rewritten


<a id="McUtils.Scaffolding.Configurations.Config.load_opts" class="docs-object-method">&nbsp;</a> 
```python
load_opts(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L255)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L255?message=Update%20Docs)]
</div>
**LLM Docstring**

Load the configuration once and add its containing directory as `config_location`.
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Configurations.Config.get_conf_attr" class="docs-object-method">&nbsp;</a> 
```python
get_conf_attr(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L271?message=Update%20Docs)]
</div>
**LLM Docstring**

Read a value from the loaded configuration object using item or attribute access according to its stored type.
  - `item`: `object`
    > the lookup key or index
  - `:returns`: `object`
    > the selected configuration value


<a id="McUtils.Scaffolding.Configurations.Config.__getattr__" class="docs-object-method">&nbsp;</a> 
```python
__getattr__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Configurations/Config.py#L289)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations/Config.py#L289?message=Update%20Docs)]
</div>
**LLM Docstring**

Forward unresolved attributes to the loaded configuration data.
  - `item`: `object`
    > the lookup key or index
  - `:returns`: `object`
    > the selected configuration value
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Configurations/Config.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Configurations/Config.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Configurations/Config.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Configurations/Config.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Configurations.py#L13?message=Update%20Docs)   
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