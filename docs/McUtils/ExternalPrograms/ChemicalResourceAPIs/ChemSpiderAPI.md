## <a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.ChemSpiderAPI">ChemSpiderAPI</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L9)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L9?message=Update%20Docs)]
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
<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.ChemSpiderAPI.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, token=None, request_delay_time=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L16?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a connection to the RSC ChemSpider compounds API, resolving and sending
the API key as the `apikey` header.
  - `token`: `str | None`
    > the API key (falls back to the environment variable)
  - `request_delay_time`: `float | None`
    > minimum delay between requests
  - `opts`: `Any`
    > extra options for the base connection


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.ChemSpiderAPI.get_chemspider_apikey" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_chemspider_apikey(cls, token): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L32?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve the ChemSpider API key, falling back to the `CHEM_SPIDER_APIKEY`
environment variable when none is given.
  - `token`: `str | None`
    > an explicit API key (or `None`)
  - `:returns`: `str | None`
    > the resolved API key


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.ChemSpiderAPI.filter" class="docs-object-method">&nbsp;</a> 
```python
@property
filter(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L49)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L49?message=Update%20Docs)]
</div>
**LLM Docstring**

The `filter` sub-API (asynchronous compound-search queries).
  - `:returns`: `object`
    > the sub-API connection


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.ChemSpiderAPI.records" class="docs-object-method">&nbsp;</a> 
```python
@property
records(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L61)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L61?message=Update%20Docs)]
</div>
**LLM Docstring**

The `records` sub-API (compound record lookups).
  - `:returns`: `object`
    > the sub-API connection


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.ChemSpiderAPI.lookups" class="docs-object-method">&nbsp;</a> 
```python
@property
lookups(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L73)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L73?message=Update%20Docs)]
</div>
**LLM Docstring**

The `lookups` sub-API (controlled-vocabulary lookups).
  - `:returns`: `object`
    > the sub-API connection


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.ChemSpiderAPI.tool" class="docs-object-method">&nbsp;</a> 
```python
@property
tool(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L85)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L85?message=Update%20Docs)]
</div>
**LLM Docstring**

The `tool` sub-API (utility endpoints).
  - `:returns`: `object`
    > the sub-API connection


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.ChemSpiderAPI.handle_filter_query" class="docs-object-method">&nbsp;</a> 
```python
handle_filter_query(self, query_id, count=1, start=0, **polling_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L97)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L97?message=Update%20Docs)]
</div>
**LLM Docstring**

Fetch a page of results for a completed filter query.
  - `query_id`: `str`
    > the filter query id
  - `count`: `int`
    > the number of results to fetch
  - `start`: `int`
    > the result offset
  - `polling_opts`: `Any`
    > extra polling options
  - `:returns`: `dict`
    > the query results


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.ChemSpiderAPI.apply_filter_query" class="docs-object-method">&nbsp;</a> 
```python
apply_filter_query(self, filter_path, retries=None, timeout=None, request_delay_time=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L118)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L118?message=Update%20Docs)]
</div>
**LLM Docstring**

Submit a filter query and return its results, raising if the API doesn't return a
query id.
  - `filter_path`: `str`
    > the filter endpoint (e.g. `'name'`)
  - `retries`: `int | None`
    > the retry count forwarded to the results fetch
  - `timeout`: `float | None`
    > the timeout forwarded to the results fetch
  - `request_delay_time`: `float | None`
    > a per-query request delay
  - `opts`: `Any`
    > the query payload fields (posted as JSON)
  - `:returns`: `dict`
    > the query results


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.ChemSpiderAPI.get_info" class="docs-object-method">&nbsp;</a> 
```python
get_info(self, ids, fields=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L151)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L151?message=Update%20Docs)]
</div>
**LLM Docstring**

Fetch the requested fields for a batch of compound record ids.
  - `ids`: `list`
    > the compound record ids
  - `fields`: `list | str | None`
    > the fields to return (defaults to common name, SMILES, InChI)
  - `opts`: `Any`
    > extra request options
  - `:returns`: `list`
    > the compound records


<a id="McUtils.ExternalPrograms.ChemicalResourceAPIs.ChemSpiderAPI.get_compounds_by_name" class="docs-object-method">&nbsp;</a> 
```python
get_compounds_by_name(self, name, return_ids=False, fields=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L172)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.py#L172?message=Update%20Docs)]
</div>
**LLM Docstring**

Look up compounds by name (via a cached name filter query), returning either the
matching record ids or their full field info.
  - `name`: `str`
    > the compound name
  - `return_ids`: `bool`
    > return only the record ids
  - `fields`: `list | str | None`
    > the fields to return
  - `opts`: `Any`
    > extra query options
  - `:returns`: `list`
    > the record ids, or the compound records
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ChemicalResourceAPIs/ChemSpiderAPI.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ChemicalResourceAPIs.py#L9?message=Update%20Docs)   
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