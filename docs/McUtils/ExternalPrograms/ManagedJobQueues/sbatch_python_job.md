# <a id="McUtils.ExternalPrograms.ManagedJobQueues.sbatch_python_job">sbatch_python_job</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L727)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L727?message=Update%20Docs)]
</div>

```python
sbatch_python_job(func, *args, sbatch_kwargs=None, job_name=None, id=None, script=None, environment=None, cleanup=False, post_processor='print', **kwargs): 
```
**LLM Docstring**

Build a generated Python runner and an `SBatchJob`, merging SLURM defaults, propagating the active environment, and installing a pre-call hook that writes the generated script.
  - `func`: `object`
    > the Python callable executed by the generated runner

  - `sbatch_kwargs`: `object`
    > SLURM options, using underscore or native key spellings as accepted by the caller

  - `job_name`: `object`
    > scheduler-visible job name

  - `id`: `object`
    > explicit generated-script identifier

  - `script`: `object`
    > the shell script or script path to submit

  - `environment`: `object`
    > environment values exported by the generated batch job

  - `cleanup`: `object`
    > whether the generated runner removes its files after execution

  - `post_processor`: `object`
    > callable or named post-processing expression for the result

  - `args`: `object`
    > positional command or function arguments

  - `kwargs`: `object`
    > scheduler, backend, or function keyword arguments

  - `:returns`: `tuple[SBatchJob, dev.FileBackedIO]`
    > build a generated Python runner and an `SBatchJob`, merging SLURM defaults, propagating the active environment, and installing a pre-call hook that writes the generated script.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/sbatch_python_job.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/sbatch_python_job.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ManagedJobQueues/sbatch_python_job.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ManagedJobQueues/sbatch_python_job.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L727?message=Update%20Docs)   
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