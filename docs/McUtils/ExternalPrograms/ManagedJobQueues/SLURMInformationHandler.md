## <a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMInformationHandler">SLURMInformationHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L170)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L170?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
STATES_MAP: list
FMT_SPECS: list
FMT_SQUEUE_KEYS: list
SQUEUE_CMD: list
SACCT_CMD: list
```
<a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMInformationHandler.prep_job_kwargs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_job_kwargs(cls, *, sbatch_script, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L193)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L193?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMInformationHandler.get_job_info_command" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_job_info_command(cls, sacct_error=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L197?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMInformationHandler.parse_raw_job_info" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_raw_job_info(cls, stdout) -> 'list[dict]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L205)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L205?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMInformationHandler.run_job_info_cmd" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
run_job_info_cmd(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L220)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L220?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/SLURMInformationHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/SLURMInformationHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ManagedJobQueues/SLURMInformationHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ManagedJobQueues/SLURMInformationHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L170?message=Update%20Docs)   
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