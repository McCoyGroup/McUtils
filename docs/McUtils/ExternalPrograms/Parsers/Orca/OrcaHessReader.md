## <a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader">OrcaHessReader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Orca.py#L17)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Orca.py#L17?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
ENumber: RegexPattern
matrix_types: dict
array_types: dict
OrcaCoords: OrcaCoords
```
<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, file, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Orca.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Orca.py#L19?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.get_special_handlers" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_special_handlers(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L32?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.handle_orca_block" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
handle_orca_block(cls, tag, data: str): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L38)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L38?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.parse_matrix" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_matrix(cls, data, col_blocks=5, data_pattern=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L67)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L67?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.parse_array" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_array(cls, data, data_pattern=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L99)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L99?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.parse_atoms" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_atoms(cls, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L112)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L112?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.get_next_block" class="docs-object-method">&nbsp;</a> 
```python
get_next_block(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.py#L122)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.py#L122?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, tags=None, excludes=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.py#L128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.py#L128?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Orca.py#L17?message=Update%20Docs)   
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