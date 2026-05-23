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


<a id="McUtils.ExternalPrograms.Jobs.SBatch.SBatchJob.clean_opts" class="docs-object-method">&nbsp;</a> 
```python
clean_opts(self, opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L70)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L70?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L90)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L90?message=Update%20Docs)]
</div>
Formats block of options
  - `:returns`: `_`
    >


<a id="McUtils.ExternalPrograms.Jobs.SBatch.SBatchJob.format" class="docs-object-method">&nbsp;</a> 
```python
format(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L124)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L124?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L175?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.SBatch.SBatchJob.run" class="docs-object-method">&nbsp;</a> 
```python
run(self, file=None, output_dir=None, sbatch_function='sbatch', delete=True, text=True, capture_output=True, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L199)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/SBatch/SBatchJob.py#L199?message=Update%20Docs)]
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