## <a id="McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader">ElectronicStructureLogReader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Parsers.py#L8)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers.py#L8?message=Update%20Docs)]
</div>

Implements a stream based reader for a generic electronic structure .log file.
This is inherits from the `FileStreamReader` base, and takes a two pronged approach to getting data.
First, a block is found in a log file based on a pair of tags.
Next, a function (usually based on a `StringParser`) is applied to this data to convert it into a usable data format.
The goal is to move toward wrapping all returned data in a `QuantityArray` so as to include data type information, too.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
components_name: NoneType
components_package: str
```
<a id="McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.load_components" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_components(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L20?message=Update%20Docs)]
</div>
**LLM Docstring**

Import (and cache) the module registering this reader's parse components (the
block tag/parser table), resolving a relative `components_package`.
  - `:returns`: `module`
    > the loaded components module


<a id="McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.registered_components" class="docs-object-method">&nbsp;</a> 
```python
@property
registered_components(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L37?message=Update%20Docs)]
</div>
**LLM Docstring**

The mapping of component name to its block specification (tags, parser, mode),
taken from the loaded components module.
  - `:returns`: `dict`
    > the registered components


<a id="McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.default_keys" class="docs-object-method">&nbsp;</a> 
```python
@property
default_keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L49)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L49?message=Update%20Docs)]
</div>
**LLM Docstring**

The default set of component keys to parse, taken from the loaded components
module.
  - `:returns`: `tuple`
    > the default keys


<a id="McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.default_ordering" class="docs-object-method">&nbsp;</a> 
```python
@property
default_ordering(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L61)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L61?message=Update%20Docs)]
</div>
**LLM Docstring**

The default parse ordering for the components, taken from the loaded components
module.
  - `:returns`: `dict`
    > the ordering mapping


<a id="McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, keys, num=None, reset=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L74)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L74?message=Update%20Docs)]
</div>
The main function we'll actually use. Parses bits out of a .log file.
  - `keys`: `str or list(str)`
    > the keys we'd like to read from the log file
  - `num`: `int or None`
    > for keys with multiple entries, the number of entries to pull
  - `:returns`: `dict`
    > the data pulled from the log file, strung together as a `dict` and keyed by the _keys_


<a id="McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.read_props" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
read_props(cls, file, keys): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L152?message=Update%20Docs)]
</div>
**LLM Docstring**

Convenience classmethod: open `file`, parse the requested keys, and return the
result (unwrapped to the single value when one key is given).
  - `file`: `str`
    > the log file
  - `keys`: `str | list[str]`
    > the component key(s) to read
  - `:returns`: `dict | Any`
    > the parsed data
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers.py#L8?message=Update%20Docs)   
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