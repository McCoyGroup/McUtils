## <a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueSubmissionHandler">ManagedJobQueueSubmissionHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L38)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L38?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueSubmissionHandler.map_option_name" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
map_option_name(cls, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L41)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L41?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a Python-style option name to a GNU-style `--kebab-case` command-line flag.
  - `key`: `object`
    > an option or record field name

  - `:returns`: `str`
    > convert a Python-style option name to a GNU-style `--kebab-case` command-line flag.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueSubmissionHandler.format_job_args" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
format_job_args(cls, **kwargs) -> 'list[str]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L56)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L56?message=Update%20Docs)]
</div>
**LLM Docstring**

Flatten keyword options into command-line arguments: true emits a flag, false omits it, and other non-`None` values emit a flag/value pair.
  - `kwargs`: `object`
    > scheduler, backend, or function keyword arguments

  - `:returns`: `list[str]`
    > flatten keyword options into command-line arguments: true emits a flag, false omits it, and other non-`None` values emit a flag/value pair.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueSubmissionHandler.get_job_command" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_job_command(cls, *args, **opts) -> 'list[str]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L82)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L82?message=Update%20Docs)]
</div>
**LLM Docstring**

Assemble the queue submission command from the configured executable, formatted options, and positional arguments.
  - `args`: `object`
    > positional command or function arguments

  - `opts`: `object`
    > backend-specific construction or command options

  - `:returns`: `list[str]`
    > assemble the queue submission command from the configured executable, formatted options, and positional arguments.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueSubmissionHandler.parse_job_id" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_job_id(cls, res: str): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L104)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L104?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract parser for extracting a scheduler job identifier from submission stdout.
  - `res`: `str`
    > captured scheduler response text

  - `:returns`: `str`
    > abstract parser for extracting a scheduler job identifier from submission stdout.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueSubmissionHandler.prep_job_kwargs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_job_kwargs(cls, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L120)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L120?message=Update%20Docs)]
</div>
**LLM Docstring**

Default submission hook that contributes no positional arguments and passes keyword arguments through unchanged.
  - `kwargs`: `object`
    > scheduler, backend, or function keyword arguments

  - `:returns`: `tuple[tuple, dict]`
    > default submission hook that contributes no positional arguments and passes keyword arguments through unchanged.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueSubmissionHandler.create_job_process" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_job_process(cls, **opts) -> 'tuple[str, _]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L134)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L134?message=Update%20Docs)]
</div>
**LLM Docstring**

Prepare and run the scheduler submission command, reject nonzero or stderr-producing executions, and parse the resulting job id.
  - `opts`: `object`
    > backend-specific construction or command options

  - `:returns`: `tuple[str, subprocess.CompletedProcess]`
    > prepare and run the scheduler submission command, reject nonzero or stderr-producing executions, and parse the resulting job id.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueSubmissionHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueSubmissionHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueSubmissionHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueSubmissionHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L38?message=Update%20Docs)   
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