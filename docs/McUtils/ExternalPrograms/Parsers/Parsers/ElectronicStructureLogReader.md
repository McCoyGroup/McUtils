## <a id="McUtils.McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader">ElectronicStructureLogReader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Parsers.py#L9)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers.py#L9?message=Update%20Docs)]
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
<a id="McUtils.McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.load_components" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_components(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L21)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L21?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.registered_components" class="docs-object-method">&nbsp;</a> 
```python
@property
registered_components(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L29)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L29?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.default_keys" class="docs-object-method">&nbsp;</a> 
```python
@property
default_keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L32?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.default_ordering" class="docs-object-method">&nbsp;</a> 
```python
@property
default_ordering(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L35)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L35?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, keys, num=None, reset=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L39)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.py#L39?message=Update%20Docs)]
</div>
The main function we'll actually use. Parses bits out of a .log file.
  - `keys`: `str or list(str)`
    > the keys we'd like to read from the log file
  - `num`: `int or None`
    > for keys with multiple entries, the number of entries to pull
  - `:returns`: `dict`
    > t
h
e
 
d
a
t
a
 
p
u
l
l
e
d
 
f
r
o
m
 
t
h
e
 
l
o
g
 
f
i
l
e
,
 
s
t
r
u
n
g
 
t
o
g
e
t
h
e
r
 
a
s
 
a
 
`
d
i
c
t
`
 
a
n
d
 
k
e
y
e
d
 
b
y
 
t
h
e
 
_
k
e
y
s
_


<a id="McUtils.McUtils.ExternalPrograms.Parsers.Parsers.ElectronicStructureLogReader.read_props" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
read_props(cls, file, keys): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L117)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L117?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/Parsers/ElectronicStructureLogReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Parsers.py#L9?message=Update%20Docs)   
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