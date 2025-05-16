## <a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter">CIFConverter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/CIFParser.py#L184)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser.py#L184?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, parsed_cif): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L185)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L185?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.cell_properties" class="docs-object-method">&nbsp;</a> 
```python
@property
cell_properties(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L188?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.atom_properties" class="docs-object-method">&nbsp;</a> 
```python
@property
atom_properties(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L193)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L193?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.symmetry_properties" class="docs-object-method">&nbsp;</a> 
```python
@property
symmetry_properties(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L198)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L198?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.prep_property_dict" class="docs-object-method">&nbsp;</a> 
```python
prep_property_dict(self, res): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L203)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L203?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.find" class="docs-object-method">&nbsp;</a> 
```python
find(self, item, strict=True, cache=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L209)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L209?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.find_all" class="docs-object-method">&nbsp;</a> 
```python
find_all(self, item, strict=True, cache=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L231)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L231?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L250)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L250?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.construct_base_atom_coords" class="docs-object-method">&nbsp;</a> 
```python
construct_base_atom_coords(self, property_dict): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L256)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L256?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.construct_atom_coords" class="docs-object-method">&nbsp;</a> 
```python
construct_atom_coords(self, atom_properties, symmetry_properties): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L272)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L272?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/CIFParser.py#L184?message=Update%20Docs)   
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