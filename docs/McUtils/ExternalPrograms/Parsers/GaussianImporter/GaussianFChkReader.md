## <a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianFChkReader">GaussianFChkReader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/GaussianImporter.py#L153)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/GaussianImporter.py#L153?message=Update%20Docs)]
</div>

Implements a stream based reader for a Gaussian .fchk file. Pretty generall I think. Should be robust-ish.
One place to change things up is convenient parsers for specific commonly pulled parts of the fchk







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
GaussianFChkReaderException: GaussianFChkReaderException
registered_components: dict
common_names: dict
to_common_name: dict
fchk_re_pattern: str
fchk_re: Pattern
```
<a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianFChkReader.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, file, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/GaussianImporter.py#L164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/GaussianImporter.py#L164?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianFChkReader.read_header" class="docs-object-method">&nbsp;</a> 
```python
read_header(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L169?message=Update%20Docs)]
</div>
Reads the header and skips the stream to where we want to be
  - `:returns`: `str`
    > t
h
e
 
h
e
a
d
e
r


<a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianFChkReader.get_next_block_params" class="docs-object-method">&nbsp;</a> 
```python
get_next_block_params(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L179)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L179?message=Update%20Docs)]
</div>
Pulls the tag of the next block, the type, the number of bytes it'll be,
and if it's a single-line block it'll also spit back the block itself
  - `:returns`: `dict`
    >


<a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianFChkReader.get_block" class="docs-object-method">&nbsp;</a> 
```python
get_block(self, name=None, dtype=None, byte_count=None, value=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L245)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L245?message=Update%20Docs)]
</div>
Pulls the next block by first pulling the block tag
  - `:returns`: `_`
    >


<a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianFChkReader.skip_block" class="docs-object-method">&nbsp;</a> 
```python
skip_block(self, name=None, dtype=None, byte_count=None, value=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L272)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L272?message=Update%20Docs)]
</div>
Skips the next block
  - `:returns`: `_`
    >


<a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianFChkReader.num_atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
num_atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L282)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L282?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianFChkReader.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, keys=None, default='raise'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.py#L287?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianFChkReader.read_props" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
read_props(cls, file, keys): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L357)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L357?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianFChkReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/GaussianImporter.py#L153?message=Update%20Docs)   
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