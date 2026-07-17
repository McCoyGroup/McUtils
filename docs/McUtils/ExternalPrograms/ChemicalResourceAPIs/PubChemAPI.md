## <a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.PubChemAPI">PubChemAPI</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L211)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L211?message=Update%20Docs)]
</div>

It is better in general to just use the ChemSpiderPy package, but this works for now







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
request_base: str
Compound: Compound
IDENTITY_PROPERTIES: frozenset
DESCRIPTOR_PROPERTIES: frozenset
COUNT_PROPERTIES: frozenset
ANNOTATION_PROPERTIES: frozenset
CONFORMER_3D_PROPERTIES: frozenset
FINGERPRINT_PROPERTIES: frozenset
property_aliases: dict
default_fields: list
```
<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.PubChemAPI.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, request_delay_time=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L218)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L218?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a connection to the PubChem PUG REST API.
  - `request_delay_time`: `float | None`
    > minimum delay between requests
  - `opts`: `Any`
    > extra options for the base connection


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.PubChemAPI.compound" class="docs-object-method">&nbsp;</a> 
```python
@property
compound(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L230)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L230?message=Update%20Docs)]
</div>
**LLM Docstring**

The `compound` sub-API.
  - `:returns`: `object`
    > the sub-API connection


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.PubChemAPI.name" class="docs-object-method">&nbsp;</a> 
```python
@property
name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L242)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L242?message=Update%20Docs)]
</div>
**LLM Docstring**

The `compound/name` sub-API (lookups by compound name).
  - `:returns`: `object`
    > the sub-API connection


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.PubChemAPI.get_property_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_property_list(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L353)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L353?message=Update%20Docs)]
</div>
**LLM Docstring**

Return (and cache) the mapping of case-folded property names to their canonical
PubChem spellings.
  - `:returns`: `dict`
    > the property-name mapping


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.PubChemAPI.get_compounds_by_name" class="docs-object-method">&nbsp;</a> 
```python
get_compounds_by_name(self, name, fields=None, subfield='json', limit=10, query=None, wrap=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L396)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L396?message=Update%20Docs)]
</div>
**LLM Docstring**

Look up compounds by name via the PubChem name endpoint (with result caching),
returning the requested properties as `Compound` objects (or the raw records).
  - `name`: `str`
    > the compound name
  - `fields`: `list | str | None`
    > the properties to fetch (defaults to SMILES and name)
  - `subfield`: `str`
    > the response format sub-path (e.g. `'json'`)
  - `limit`: `int`
    > the maximum number of records
  - `query`: `dict | None`
    > extra query parameters
  - `wrap`: `bool`
    > wrap the records as `Compound` objects
  - `opts`: `Any`
    > extra request options
  - `:returns`: `list`
    > the compounds (or raw records)
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L211?message=Update%20Docs)   
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