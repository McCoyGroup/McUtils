## <a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine">ExecutionEngine</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine.py#L71)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L71?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
engine_types: dict
```
<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.register" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
register(cls, name, engine=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L75)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L75?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.resolve" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve(cls, name, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L88)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L88?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine.py#L92)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L92?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.submit_job" class="docs-object-method">&nbsp;</a> 
```python
submit_job(self, **kwargs) -> 'ExecutionFuture': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L96)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L96?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.submit_jobs" class="docs-object-method">&nbsp;</a> 
```python
submit_jobs(self, jobs: 'list[dict]', **kwargs) -> 'ExecutionQueue': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L100)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L100?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L106?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L110?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.shutdown" class="docs-object-method">&nbsp;</a> 
```python
shutdown(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L115?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L71?message=Update%20Docs)   
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