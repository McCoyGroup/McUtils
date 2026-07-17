## <a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMInformationHandler">SLURMInformationHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L368)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L368?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L391)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L391?message=Update%20Docs)]
</div>
**LLM Docstring**

Return an sbatch script as the sole positional argument and preserve the remaining keyword options.
  - `sbatch_script`: `object`
    > the SLURM batch script path

  - `kwargs`: `object`
    > scheduler, backend, or function keyword arguments

  - `:returns`: `tuple[tuple, dict]`
    > return an sbatch script as the sole positional argument and preserve the remaining keyword options.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMInformationHandler.get_job_info_command" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_job_info_command(cls, sacct_error=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L409)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L409?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a user-scoped `sacct` query, or an `squeue` fallback command when `sacct_error` is true.
  - `sacct_error`: `object`
    > whether to use the `squeue` fallback instead of `sacct`

  - `:returns`: `list[str]`
    > build a user-scoped `sacct` query, or an `squeue` fallback command when `sacct_error` is true.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMInformationHandler.parse_raw_job_info" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_raw_job_info(cls, stdout) -> 'list[dict]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L428)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L428?message=Update%20Docs)]
</div>
**LLM Docstring**

Slice fixed-width SLURM output lines according to `FMT_SPECS` and return one dictionary per line.
  - `stdout`: `object`
    > captured scheduler standard output

  - `:returns`: `list[dict]`
    > slice fixed-width SLURM output lines according to `FMT_SPECS` and return one dictionary per line.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.SLURMInformationHandler.run_job_info_cmd" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
run_job_info_cmd(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L454)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L454?message=Update%20Docs)]
</div>
**LLM Docstring**

Run the normal SLURM accounting query and fall back to `squeue` when the first command fails.
  - `:returns`: `subprocess.CompletedProcess`
    > run the normal SLURM accounting query and fall back to `squeue` when the first command fails.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L368?message=Update%20Docs)   
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