## <a id="McUtils.ExternalPrograms.ExecutionEngine.ManagedJobQueueExecutionEngine">ManagedJobQueueExecutionEngine</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine.py#L450)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L450?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
future_type: ManagedJobQueueExecutionFuture
```
<a id="McUtils.ExternalPrograms.ExecutionEngine.ManagedJobQueueExecutionEngine.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, queue_manager: 'queues.ManagedJobQueueHandler', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine.py#L452)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L452?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize an execution engine backed by a managed job-queue handler.
  - `queue_manager`: `queues.ManagedJobQueueHandler`
    > the managed queue used for submission and status lookup

  - `opts`: `object`
    > backend-specific construction or command options

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.ExternalPrograms.ExecutionEngine.ManagedJobQueueExecutionEngine.prep_future_opts" class="docs-object-method">&nbsp;</a> 
```python
prep_future_opts(self, watch_dir=None, results_file=None, status_file=None, poll_time=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ManagedJobQueueExecutionEngine.py#L470)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ManagedJobQueueExecutionEngine.py#L470?message=Update%20Docs)]
</div>
**LLM Docstring**

Separate file-watching and polling options for the future from the remaining scheduler submission options.
  - `watch_dir`: `object`
    > directory containing result and status files

  - `results_file`: `object`
    > result JSON filename

  - `status_file`: `object`
    > status JSON filename

  - `poll_time`: `object`
    > seconds between status polls

  - `kwargs`: `object`
    > scheduler, backend, or function keyword arguments

  - `:returns`: `tuple[dict, dict]`
    > separate file-watching and polling options for the future from the remaining scheduler submission options.


<a id="McUtils.ExternalPrograms.ExecutionEngine.ManagedJobQueueExecutionEngine.submit_job" class="docs-object-method">&nbsp;</a> 
```python
submit_job(self, *, watch_dir=None, poll_time=None, results_file=None, status_file=None, **kwargs) -> 'ManagedJobQueueExecutionFuture': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ManagedJobQueueExecutionEngine.py#L506)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ManagedJobQueueExecutionEngine.py#L506?message=Update%20Docs)]
</div>
**LLM Docstring**

Submit the scheduler options through the queue manager and construct a future for the returned job identifier.
  - `watch_dir`: `object`
    > directory containing result and status files

  - `poll_time`: `object`
    > seconds between status polls

  - `results_file`: `object`
    > result JSON filename

  - `status_file`: `object`
    > status JSON filename

  - `kwargs`: `object`
    > scheduler, backend, or function keyword arguments

  - `:returns`: `ManagedJobQueueExecutionFuture`
    > submit the scheduler options through the queue manager and construct a future for the returned job identifier.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ExecutionEngine/ManagedJobQueueExecutionEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ExecutionEngine/ManagedJobQueueExecutionEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ExecutionEngine/ManagedJobQueueExecutionEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ExecutionEngine/ManagedJobQueueExecutionEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L450?message=Update%20Docs)   
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