## <a id="McUtils.McUtils.ExternalPrograms.WebAPI.GitHubReleaseManager">GitHubReleaseManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/WebAPI.py#L463)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/WebAPI.py#L463?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
request_base: str
resource_key: str
release_manager_class: ReleaseZIPManager
blacklist_repos: list
release_cache: dict
```
<a id="McUtils.McUtils.ExternalPrograms.WebAPI.GitHubReleaseManager.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, token=None, request_delay_time=None, release_manager=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L468)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L468?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.WebAPI.GitHubReleaseManager.list_repos" class="docs-object-method">&nbsp;</a> 
```python
list_repos(self, owner): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L479)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L479?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.WebAPI.GitHubReleaseManager.list_releases" class="docs-object-method">&nbsp;</a> 
```python
list_releases(self, owner, repo): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L486)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L486?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.WebAPI.GitHubReleaseManager.latest_release" class="docs-object-method">&nbsp;</a> 
```python
latest_release(self, owner, repo): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L491)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L491?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.WebAPI.GitHubReleaseManager.update_existing_releases" class="docs-object-method">&nbsp;</a> 
```python
update_existing_releases(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L500)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L500?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.WebAPI.GitHubReleaseManager.format_repo_key" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
format_repo_key(cls, owner, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L506)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L506?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.WebAPI.GitHubReleaseManager.resolve_resource_url" class="docs-object-method">&nbsp;</a> 
```python
resolve_resource_url(self, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L509)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L509?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.WebAPI.GitHubReleaseManager.get_release_list" class="docs-object-method">&nbsp;</a> 
```python
get_release_list(self, owner, name, update=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L511)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.py#L511?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/WebAPI/GitHubReleaseManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/WebAPI.py#L463?message=Update%20Docs)   
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