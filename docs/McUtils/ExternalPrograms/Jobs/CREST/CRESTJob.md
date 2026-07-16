## <a id="McUtils.ExternalPrograms.Jobs.CREST.CRESTJob">CRESTJob</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/CREST.py#L180)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/CREST.py#L180?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
job_template: str
blocks: list
```
<a id="McUtils.ExternalPrograms.Jobs.CREST.CRESTJob.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *strs, path='crest', input_file='geom.xyz', log_file='confgen.log', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/CREST.py#L189)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/CREST.py#L189?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a CREST job, treating bare string arguments as boolean command-line flags
and wiring up the CREST executable, input geometry, and log-file paths.
  - `strs`: `Any`
    > bare command-line flags
  - `path`: `str`
    > path to the CREST executable
  - `input_file`: `str`
    > the input geometry file name
  - `log_file`: `str`
    > the log file name
  - `opts`: `Any`
    > the job options


<a id="McUtils.ExternalPrograms.Jobs.CREST.CRESTJob.get_block_types" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_block_types(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L222)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L222?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the ordered CREST block types.
  - `:returns`: `list`
    > the block types


<a id="McUtils.ExternalPrograms.Jobs.CREST.CRESTJob.load_template" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_template(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L234)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L234?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the path to the CREST job (shell-script) template.
  - `:returns`: `str`
    > the template path
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Jobs/CREST/CRESTJob.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Jobs/CREST/CRESTJob.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Jobs/CREST/CRESTJob.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Jobs/CREST/CRESTJob.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/CREST.py#L180?message=Update%20Docs)   
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