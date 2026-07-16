## <a id="McUtils.ExternalPrograms.Jobs.SBatch.SBatchJob">SBatchJob</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch.py#L14?message=Update%20Docs)]
</div>

Provides a simple interface to formatting SLURM
files so that they can be submitted to `sbatch`.
The hope is that this can be subclassed codify
options for different HPC paritions and whatnot.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
slurm_keys: list
default_opts: dict
sbatch_opt_template: str
sbatch_template: str
sbatch_enter_command: str
sbatch_exit_command: str
```
<a id="McUtils.ExternalPrograms.Jobs.SBatch.SBatchJob.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, description=None, job_name=None, account=None, partition=None, mem=None, nodes=None, ntasks_per_node=None, chdir=None, output=None, steps=(), precall=None, environment=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch.py#L43)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch.py#L43?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a SLURM batch job from the common `#SBATCH` options plus any additional
ones, the job steps, and optional environment/precall hooks.
  - `description`: `str | None`
    > a human-readable description echoed into the script
  - `job_name`: `str | None`
    > the SLURM job name
  - `account`: `str | None`
    > the SLURM account
  - `partition`: `str | None`
    > the SLURM partition
  - `mem`: `Any`
    > the memory request
  - `nodes`: `Any`
    > the node count
  - `ntasks_per_node`: `Any`
    > tasks per node
  - `chdir`: `str | None`
    > the working directory
  - `output`: `str | None`
    > the output-file pattern
  - `steps`: `tuple | str`
    > the job steps (shell commands)
  - `precall`: `Callable | None`
    > a callable run before writing the file
  - `environment`: `dict | None`
    > environment variables to export
  - `opts`: `Any`
    > additional `#SBATCH` options


<a id="McUtils.ExternalPrograms.Jobs.SBatch.SBatchJob.clean_opts" class="docs-object-method">&nbsp;</a> 
```python
clean_opts(self, opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L99)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L99?message=Update%20Docs)]
</div>
Makes sure opt names are clean.
Does no validation of the values sent in.
  - `opts`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.ExternalPrograms.Jobs.SBatch.SBatchJob.format_opt_block" class="docs-object-method">&nbsp;</a> 
```python
format_opt_block(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L119?message=Update%20Docs)]
</div>
Formats block of options
  - `:returns`: `_`
    >


<a id="McUtils.ExternalPrograms.Jobs.SBatch.SBatchJob.format" class="docs-object-method">&nbsp;</a> 
```python
format(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L153)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L153?message=Update%20Docs)]
</div>
Formats an SBATCH file from the held options
  - `call_steps`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.ExternalPrograms.Jobs.SBatch.SBatchJob.write" class="docs-object-method">&nbsp;</a> 
```python
write(self, file, output_dir=None, mode='w+', **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L204)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L204?message=Update%20Docs)]
</div>
**LLM Docstring**

Write the formatted SLURM script to a file, optionally within a working
directory (into which any `precall` hook is run).
  - `file`: `str | IO`
    > an open stream or a file path
  - `output_dir`: `str | None`
    > directory to write into (split from `file` if omitted)
  - `mode`: `str`
    > the file mode when a path is given
  - `kwargs`: `Any`
    > extra arguments for `open`
  - `:returns`: `str | IO`
    > the path (or stream) written


<a id="McUtils.ExternalPrograms.Jobs.SBatch.SBatchJob.run" class="docs-object-method">&nbsp;</a> 
```python
run(self, file=None, output_dir=None, sbatch_function='sbatch', delete=True, text=True, capture_output=True, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L244)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L244?message=Update%20Docs)]
</div>
**LLM Docstring**

Write the SLURM script and submit it with `sbatch` (via `subprocess.run`),
optionally deleting the script afterward.
  - `file`: `str | None`
    > the script file name (a temporary name is generated if omitted)
  - `output_dir`: `str | None`
    > directory to write the script into
  - `sbatch_function`: `str`
    > the submission command
  - `delete`: `bool`
    > remove the script file after submission
  - `text`: `bool`
    > run the subprocess in text mode
  - `capture_output`: `bool`
    > capture the subprocess output
  - `args`: `Any`
    > extra positional arguments passed to `sbatch`
  - `kwargs`: `Any`
    > extra flags passed to `sbatch`
  - `:returns`: `subprocess.CompletedProcess`
    > the completed-process result
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch.py#L14?message=Update%20Docs)   
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