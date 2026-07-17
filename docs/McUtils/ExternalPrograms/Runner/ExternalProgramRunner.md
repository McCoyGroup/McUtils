## <a id="McUtils.ExternalPrograms.Runner.ExternalProgramRunner">ExternalProgramRunner</a> 

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
<a id="McUtils.ExternalPrograms.Runner.ExternalProgramRunner.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, binary, parser=None, prefix=None, suffix=None, delete=True, **runtime_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Runner.py#L11)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Runner.py#L11?message=Update%20Docs)]
</div>
**LLM Docstring**

Configure an external-program wrapper around a binary and persistent runtime defaults.
  - `binary`: `object`
    > the executable path or command name

  - `parser`: `object`
    > an optional result parser retained on the runner

  - `prefix`: `object`
    > the temporary input-file prefix

  - `suffix`: `object`
    > the temporary input-file suffix

  - `delete`: `object`
    > whether temporary inputs and discovered outputs should be read and removed

  - `runtime_opts`: `object`
    > default options forwarded to job execution

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.ExternalPrograms.Runner.ExternalProgramRunner.prep_dir" class="docs-object-method">&nbsp;</a> 
```python
prep_dir(self, dir): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.py#L110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.py#L110?message=Update%20Docs)]
</div>
**LLM Docstring**

Placeholder hook for subclasses to populate a working directory before launching the external program.
  - `dir`: `object`
    > the working directory, or `None` to allocate a temporary directory

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.ExternalPrograms.Runner.ExternalProgramRunner.subprocess_run" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
subprocess_run(cls, binary, input_file, **subprocess_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L124)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L124?message=Update%20Docs)]
</div>
**LLM Docstring**

Run `binary input_file`, resolving a local binary to an absolute path before calling `subprocess.run`.
  - `binary`: `object`
    > the executable path or command name

  - `input_file`: `object`
    > the generated input-file path

  - `subprocess_opts`: `object`
    > options forwarded to `subprocess.run`

  - `:returns`: `subprocess.CompletedProcess`
    > run `binary input_file`, resolving a local binary to an absolute path before calling `subprocess.run`.


<a id="McUtils.ExternalPrograms.Runner.ExternalProgramRunner.run_job" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
run_job(cls, binary, job, dir=None, dir_prefix=None, dir_suffix=None, mode='w', runner=None, prep_dir=None, prep_job=None, prep_results=None, return_auxiliary_files=True, prefix=None, suffix=None, delete=True, raise_errors=True, **subprocess_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L184)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L184?message=Update%20Docs)]
</div>
**LLM Docstring**

Materialize a job in a named temporary input file, execute the external binary in the work directory, collect requested output files, and optionally remove all temporary artifacts. Stderr is decoded and treated as an error whenever `raise_errors` is true.
  - `binary`: `object`
    > the executable path or command name

  - `job`: `object`
    > the job text or formattable job object

  - `dir`: `object`
    > the working directory, or `None` to allocate a temporary directory

  - `dir_prefix`: `object`
    > prefix for an automatically created temporary directory

  - `dir_suffix`: `object`
    > suffix for an automatically created temporary directory

  - `mode`: `object`
    > the mode used to create the input file

  - `runner`: `object`
    > an optional replacement process-launch function

  - `prep_dir`: `object`
    > an optional callback that populates the work directory

  - `prep_job`: `object`
    > an optional callback that transforms the job text

  - `prep_results`: `object`
    > an optional callback that extracts additional results from the work directory

  - `return_auxiliary_files`: `object`
    > whether and how newly created output files should be collected

  - `prefix`: `object`
    > the temporary input-file prefix

  - `suffix`: `object`
    > the temporary input-file suffix

  - `delete`: `object`
    > whether temporary inputs and discovered outputs should be read and removed

  - `raise_errors`: `object`
    > whether nonempty stderr should raise `IOError`

  - `subprocess_opts`: `object`
    > options forwarded to `subprocess.run`

  - `:returns`: `dict | tuple`
    > materialize a job in a named temporary input file, execute the external binary in the work directory, collect requested output files, and optionally remove all temporary artifacts. Stderr is decoded and treated as an error whenever `raise_errors` is true.


<a id="McUtils.ExternalPrograms.Runner.ExternalProgramRunner.run" class="docs-object-method">&nbsp;</a> 
```python
run(self, job, dir=None, dir_prefix=None, dir_suffix=None, mode=None, runner=None, prep_dir=None, prep_job=None, prep_results=None, return_auxiliary_files=None, prefix=None, suffix=None, delete=None, raise_errors=None, **job_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.py#L307)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Runner/ExternalProgramRunner.py#L307?message=Update%20Docs)]
</div>
**LLM Docstring**

Merge per-call overrides with the runner defaults and invoke `run_job` using this instance’s binary and directory-preparation hook.
  - `job`: `object`
    > the job text or formattable job object

  - `dir`: `object`
    > the working directory, or `None` to allocate a temporary directory

  - `dir_prefix`: `object`
    > prefix for an automatically created temporary directory

  - `dir_suffix`: `object`
    > suffix for an automatically created temporary directory

  - `mode`: `object`
    > the mode used to create the input file

  - `runner`: `object`
    > an optional replacement process-launch function

  - `prep_dir`: `object`
    > an optional callback that populates the work directory

  - `prep_job`: `object`
    > an optional callback that transforms the job text

  - `prep_results`: `object`
    > an optional callback that extracts additional results from the work directory

  - `return_auxiliary_files`: `object`
    > whether and how newly created output files should be collected

  - `prefix`: `object`
    > the temporary input-file prefix

  - `suffix`: `object`
    > the temporary input-file suffix

  - `delete`: `object`
    > whether temporary inputs and discovered outputs should be read and removed

  - `raise_errors`: `object`
    > whether nonempty stderr should raise `IOError`

  - `job_opts`: `object`
    > per-call execution overrides

  - `:returns`: `dict | tuple`
    > merge per-call overrides with the runner defaults and invoke `run_job` using this instance’s binary and directory-preparation hook.
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