## <a id="McUtils.ExternalPrograms.ChemSpiderAPI.ChemSpiderAPI">ChemSpiderAPI</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemSpiderAPI.py#L9)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemSpiderAPI.py#L9?message=Update%20Docs)]
</div>

It is better in general to just use the ChemSpiderPy package, but this works for now







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
request_base: str
api_key_env_var: str
default_molecule_fields: list
```
<a id="McUtils.ExternalPrograms.ChemSpiderAPI.ChemSpiderAPI.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, token=None, request_delay_time=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemSpiderAPI.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemSpiderAPI.py#L16?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemSpiderAPI.ChemSpiderAPI.get_chemspider_apikey" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_chemspider_apikey(cls, token): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L20?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemSpiderAPI.ChemSpiderAPI.filter" class="docs-object-method">&nbsp;</a> 
```python
@property
filter(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L26)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L26?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemSpiderAPI.ChemSpiderAPI.records" class="docs-object-method">&nbsp;</a> 
```python
@property
records(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L30)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L30?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemSpiderAPI.ChemSpiderAPI.lookups" class="docs-object-method">&nbsp;</a> 
```python
@property
lookups(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L34)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L34?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemSpiderAPI.ChemSpiderAPI.tool" class="docs-object-method">&nbsp;</a> 
```python
@property
tool(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L38)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L38?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemSpiderAPI.ChemSpiderAPI.handle_filter_query" class="docs-object-method">&nbsp;</a> 
```python
handle_filter_query(self, query_id, count=1, start=0, **polling_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L42)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L42?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemSpiderAPI.ChemSpiderAPI.apply_filter_query" class="docs-object-method">&nbsp;</a> 
```python
apply_filter_query(self, filter_path, retries=None, timeout=None, request_delay_time=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L48?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemSpiderAPI.ChemSpiderAPI.get_info" class="docs-object-method">&nbsp;</a> 
```python
get_info(self, ids, fields=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L62)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L62?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ChemSpiderAPI.ChemSpiderAPI.get_compounds_by_name" class="docs-object-method">&nbsp;</a> 
```python
get_compounds_by_name(self, name, return_ids=False, fields=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L70)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.py#L70?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ChemSpiderAPI/ChemSpiderAPI.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemSpiderAPI.py#L9?message=Update%20Docs)   
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