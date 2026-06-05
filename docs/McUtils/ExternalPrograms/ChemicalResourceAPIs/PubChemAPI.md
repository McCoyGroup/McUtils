## <a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.PubChemAPI">PubChemAPI</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L94)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L94?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L101?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.PubChemAPI.compound" class="docs-object-method">&nbsp;</a> 
```python
@property
compound(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L104)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L104?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.PubChemAPI.name" class="docs-object-method">&nbsp;</a> 
```python
@property
name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L108)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L108?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.PubChemAPI.get_property_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_property_list(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L172)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L172?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.PubChemAPI.get_compounds_by_name" class="docs-object-method">&nbsp;</a> 
```python
get_compounds_by_name(self, name, fields=None, subfield='json', limit=10, query=None, wrap=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L194)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.py#L194?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ChemicalResourceAPIs/PubChemAPI.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L94?message=Update%20Docs)   
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