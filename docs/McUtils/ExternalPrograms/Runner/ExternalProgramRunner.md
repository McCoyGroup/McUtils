## <a id="McUtils.McUtils.ExternalPrograms.Runner.ExternalProgramRunner">ExternalProgramRunner</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Runner.py#L8)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Runner.py#L8?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_opts: dict
text_file_extensions: list
blacklist_files: list
```
<a id="McUtils.McUtils.ExternalPrograms.Runner.ExternalProgramRunner.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, binary, parser=None, prefix=None, suffix=None, delete=True, **runtime_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.py#L11)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.py#L11?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.Runner.ExternalProgramRunner.prep_dir" class="docs-object-method">&nbsp;</a> 
```python
prep_dir(self, dir): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.py#L39)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.py#L39?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.Runner.ExternalProgramRunner.subprocess_run" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
subprocess_run(cls, binary, input_file, **subprocess_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L42)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L42?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.Runner.ExternalProgramRunner.run_job" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
run_job(cls, binary, job, dir=None, dir_prefix=None, dir_suffix=None, mode='w', runner=None, prep_dir=None, prep_job=None, prep_results=None, return_auxiliary_files=True, prefix=None, suffix=None, delete=True, raise_errors=True, **subprocess_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L68)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L68?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.ExternalPrograms.Runner.ExternalProgramRunner.run" class="docs-object-method">&nbsp;</a> 
```python
run(self, job, dir=None, dir_prefix=None, dir_suffix=None, mode=None, runner=None, prep_dir=None, prep_job=None, prep_results=None, return_auxiliary_files=None, prefix=None, suffix=None, delete=None, raise_errors=None, **job_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.py#L135)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.py#L135?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Runner.py#L8?message=Update%20Docs)   
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