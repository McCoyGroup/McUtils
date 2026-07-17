## <a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMSubmissionHandler">SLURMSubmissionHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L331)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L331?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
START_JOB_COMMAND: list
```
<a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMSubmissionHandler.prep_job_kwargs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_job_kwargs(cls, *, sbatch_file, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L334)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L334?message=Update%20Docs)]
</div>
**LLM Docstring**

Move `sbatch_file` into the positional argument list expected by `sbatch`.
  - `sbatch_file`: `object`
    > path to the sbatch script

  - `etc`: `object`
    > additional scheduler options

  - `:returns`: `tuple[tuple, dict]`
    > move `sbatch_file` into the positional argument list expected by `sbatch`.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMSubmissionHandler.parse_job_id" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_job_id(self, res: str): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L353)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L353?message=Update%20Docs)]
</div>
**LLM Docstring**

Extract the numeric job id from SLURM’s `Submitted batch job N` response.
  - `res`: `str`
    > captured scheduler response text

  - `:returns`: `str`
    > extract the numeric job id from SLURM’s `Submitted batch job N` response.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/SLURMSubmissionHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/SLURMSubmissionHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ManagedJobQueues/SLURMSubmissionHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ManagedJobQueues/SLURMSubmissionHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L331?message=Update%20Docs)   
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