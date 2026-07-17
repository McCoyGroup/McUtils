## <a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueHandler">ManagedJobQueueHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L268)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L268?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueHandler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, information_handler: McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueInformationHandler, submission_handler: McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueSubmissionHandler): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L271?message=Update%20Docs)]
</div>
**LLM Docstring**

Combine independent scheduler information and submission handlers behind one queue interface.
  - `information_handler`: `ManagedJobQueueInformationHandler`
    > the component that queries scheduler state

  - `submission_handler`: `ManagedJobQueueSubmissionHandler`
    > the component that submits jobs

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueHandler.get_job_info" class="docs-object-method">&nbsp;</a> 
```python
get_job_info(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueHandler.py#L291)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueHandler.py#L291?message=Update%20Docs)]
</div>
**LLM Docstring**

Return all current job records from the information handler.
  - `:returns`: `dict`
    > return all current job records from the information handler.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueHandler.get_job_status" class="docs-object-method">&nbsp;</a> 
```python
get_job_status(self, job_id): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueHandler.py#L302)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueHandler.py#L302?message=Update%20Docs)]
</div>
**LLM Docstring**

Look up a job record and return its `status` field.
  - `job_id`: `object`
    > the scheduler-assigned job identifier

  - `:returns`: `ManagedJobQueueJobStatus`
    > look up a job record and return its `status` field.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueHandler.submit_job" class="docs-object-method">&nbsp;</a> 
```python
submit_job(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueHandler.py#L317)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueHandler.py#L317?message=Update%20Docs)]
</div>
**LLM Docstring**

Forward scheduler options to the submission handler and return its submission result.
  - `kwargs`: `object`
    > scheduler, backend, or function keyword arguments

  - `:returns`: `tuple`
    > forward scheduler options to the submission handler and return its submission result.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L268?message=Update%20Docs)   
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