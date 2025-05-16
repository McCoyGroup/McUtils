## <a id="McUtils.ExternalPrograms.WebAPI.WebAPIConnection">WebAPIConnection</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/WebAPI.py#L249)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/WebAPI.py#L249?message=Update%20Docs)]
</div>

Base class for super simple web api interactions, use something better designed in general







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_content_type: str
default_return_type: str
default_request_handler: WebRequestHandler
request_base: NoneType
```
<a id="McUtils.ExternalPrograms.WebAPI.WebAPIConnection.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, auth_info, history_length=None, log_requests=False, request_delay_time=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L254)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L254?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.WebAPI.WebAPIConnection.prep_headers" class="docs-object-method">&nbsp;</a> 
```python
prep_headers(self, headers, content_type=None, return_type=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L264)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L264?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.WebAPI.WebAPIConnection.do_request" class="docs-object-method">&nbsp;</a> 
```python
do_request(self, method, root, *path, query=None, headers=None, content_type=None, return_type=None, handler=None, delay_time=None, json=None, data=None, **urllib3_request_kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L279)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L279?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.WebAPI.WebAPIConnection.get" class="docs-object-method">&nbsp;</a> 
```python
get(self, root, *path, query=None, **urllib3_request_kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L331)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L331?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.WebAPI.WebAPIConnection.post" class="docs-object-method">&nbsp;</a> 
```python
post(self, root, *path, query=None, **urllib3_request_kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L338)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L338?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.WebAPI.WebAPIConnection.delete" class="docs-object-method">&nbsp;</a> 
```python
delete(self, root, *path, query=None, **urllib3_request_kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L345)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L345?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.WebAPI.WebAPIConnection.get_endpoint_params" class="docs-object-method">&nbsp;</a> 
```python
get_endpoint_params(self, root, path, query=None, base=None, fragment=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L353)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L353?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.WebAPI.WebAPIConnection.get_subapi" class="docs-object-method">&nbsp;</a> 
```python
get_subapi(self, extension): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L378)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/WebAPI/WebAPIConnection.py#L378?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/WebAPI/WebAPIConnection.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/WebAPI/WebAPIConnection.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/WebAPI/WebAPIConnection.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/WebAPI/WebAPIConnection.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/WebAPI.py#L249?message=Update%20Docs)   
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