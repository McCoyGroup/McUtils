## <a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueInformationHandler">ManagedJobQueueInformationHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L154?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueInformationHandler.get_job_info_command" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_job_info_command(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L157)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L157?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the command specification used to query scheduler job information.
  - `:returns`: `str | list[str]`
    > return the command specification used to query scheduler job information.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueInformationHandler.run_job_info_cmd" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
run_job_info_cmd(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L169?message=Update%20Docs)]
</div>
**LLM Docstring**

Run the scheduler information command with captured text output and raise `IOError` on stderr or a nonzero return code.
  - `:returns`: `subprocess.CompletedProcess`
    > run the scheduler information command with captured text output and raise `IOError` on stderr or a nonzero return code.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueInformationHandler.parse_raw_job_info" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_raw_job_info(cls, stdout) -> 'list[dict]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L185)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L185?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract parser that converts scheduler stdout into raw per-job dictionaries.
  - `stdout`: `object`
    > captured scheduler standard output

  - `:returns`: `list[dict]`
    > abstract parser that converts scheduler stdout into raw per-job dictionaries.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueInformationHandler.parse_job_info" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_job_info(cls, stdout) -> 'list[dict]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L229)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L229?message=Update%20Docs)]
</div>
**LLM Docstring**

Clean every field of every raw scheduler record, including state normalization.
  - `stdout`: `object`
    > captured scheduler standard output

  - `:returns`: `list[dict]`
    > clean every field of every raw scheduler record, including state normalization.


<a id="McUtils.ExternalPrograms.ManagedJobQueues.ManagedJobQueueInformationHandler.get_all_job_info" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_all_job_info(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L251)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L251?message=Update%20Docs)]
</div>
**LLM Docstring**

Run the scheduler query and index the parsed job records by their `id` field.
  - `:returns`: `dict`
    > run the scheduler query and index the parsed job records by their `id` field.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueInformationHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueInformationHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueInformationHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ManagedJobQueues/ManagedJobQueueInformationHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ManagedJobQueues.py#L154?message=Update%20Docs)   
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