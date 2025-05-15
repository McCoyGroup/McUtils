## <a id="McUtils.McUtils.Scaffolding.Jobs.JobManager">JobManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Jobs.py#L173)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Jobs.py#L173?message=Update%20Docs)]
</div>

A class to manage job instances.
Thin layer on a `PersistenceManager`







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_job_type: Job
```
<a id="McUtils.McUtils.Scaffolding.Jobs.JobManager.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, job_dir, job_type=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Jobs/JobManager.py#L179)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Jobs/JobManager.py#L179?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Scaffolding.Jobs.JobManager.job" class="docs-object-method">&nbsp;</a> 
```python
job(self, name, timestamp=False, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Jobs/JobManager.py#L184)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Jobs/JobManager.py#L184?message=Update%20Docs)]
</div>
Returns a loaded or new job with the given name and settings
  - `name`: `str`
    > 
  - `timestamp`: `Any`
    > 
  - `kw`: `Any`
    > 
  - `:returns`: `Job`
    >


<a id="McUtils.McUtils.Scaffolding.Jobs.JobManager.job_from_folder" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
job_from_folder(cls, folder, job_type=None, make_config=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L204)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L204?message=Update%20Docs)]
</div>
A special case convenience function that goes
directly to starting a job from a folder
  - `:returns`: `Job`
    >


<a id="McUtils.McUtils.Scaffolding.Jobs.JobManager.current_job" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
current_job(cls, job_type=None, make_config=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L223)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L223?message=Update%20Docs)]
</div>
A special case convenience function that starts a
JobManager one directory up from the current
working directory and intializes a job from the
current working directory
  - `:returns`: `Job`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Jobs/JobManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Jobs/JobManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Jobs/JobManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Jobs/JobManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Jobs.py#L173?message=Update%20Docs)   
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