## <a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter">CIFConverter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser.py#L338)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser.py#L338?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser.py#L339)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser.py#L339?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap parsed CIF data to provide higher-level property/coordinate extraction.
  - `parsed_cif`: `list`
    > the parsed CIF blocks


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.cell_properties" class="docs-object-method">&nbsp;</a> 
```python
@property
cell_properties(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L350)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L350?message=Update%20Docs)]
</div>
**LLM Docstring**

The unit-cell properties (all `cell_*` fields), merged into one dict.
  - `:returns`: `dict`
    > the cell properties


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.atom_properties" class="docs-object-method">&nbsp;</a> 
```python
@property
atom_properties(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L363)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L363?message=Update%20Docs)]
</div>
**LLM Docstring**

The atom-site properties (all `atom_*` fields), merged into one dict.
  - `:returns`: `dict`
    > the atom properties


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.symmetry_properties" class="docs-object-method">&nbsp;</a> 
```python
@property
symmetry_properties(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L376)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L376?message=Update%20Docs)]
</div>
**LLM Docstring**

The symmetry properties (all `symmetry_*` fields), merged into one dict.
  - `:returns`: `dict`
    > the symmetry properties


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.prep_property_dict" class="docs-object-method">&nbsp;</a> 
```python
prep_property_dict(self, res): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L389)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L389?message=Update%20Docs)]
</div>
**LLM Docstring**

Flatten a list of per-block property dicts into a single merged dict.
  - `res`: `list[dict]`
    > the per-block property dicts
  - `:returns`: `dict`
    > the merged properties


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.find" class="docs-object-method">&nbsp;</a> 
```python
find(self, item, strict=True, cache=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L405)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L405?message=Update%20Docs)]
</div>
**LLM Docstring**

Find the first value matching a field name (exact or, when `strict` is off, by
regex), optionally caching the result.
  - `item`: `str`
    > the field name or pattern
  - `strict`: `bool`
    > match the name exactly
  - `cache`: `bool`
    > cache the lookup
  - `:returns`: `Any`
    > the matched value (or matching `{key: value}`), or `None`


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.find_all" class="docs-object-method">&nbsp;</a> 
```python
find_all(self, item, strict=True, cache=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L442)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L442?message=Update%20Docs)]
</div>
**LLM Docstring**

Find every value matching a field name (exact or, when `strict` is off, by
regex), optionally caching the result.
  - `item`: `str`
    > the field name or pattern
  - `strict`: `bool`
    > match the name exactly
  - `cache`: `bool`
    > cache the lookup
  - `:returns`: `list`
    > the matched values


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L476)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L476?message=Update%20Docs)]
</div>
**LLM Docstring**

The atom coordinates built from the atom and symmetry properties (applying the
symmetry operations to the base coordinates).
  - `:returns`: `dict`
    > the `{atoms, coords, charges}` structure


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.construct_base_atom_coords" class="docs-object-method">&nbsp;</a> 
```python
construct_base_atom_coords(self, property_dict): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L491)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L491?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the base (asymmetric-unit) atom structure from a property dict: element
symbols, charges, and fractional coordinates.
  - `property_dict`: `dict`
    > the merged atom properties
  - `:returns`: `dict`
    > the `{atoms, coords, charges}` structure


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFConverter.construct_atom_coords" class="docs-object-method">&nbsp;</a> 
```python
construct_atom_coords(self, atom_properties, symmetry_properties): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L518)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFConverter.py#L518?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the full atom structure by applying the crystallographic symmetry
operations to the base coordinates (replicating atoms/charges accordingly).
  - `atom_properties`: `dict`
    > the merged atom properties
  - `symmetry_properties`: `dict`
    > the merged symmetry properties
  - `:returns`: `dict`
    > the `{atoms, coords, charges}` structure
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser.py#L338?message=Update%20Docs)   
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