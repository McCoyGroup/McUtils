## <a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob">ExternalProgramJob</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L526)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L526?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
registry: dict
distance_units: str
```
<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.register" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
register(cls, name, method=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L532)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L532?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.resolve" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve(cls, job_class): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L545)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L545?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.get_mol_options" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_mol_options(cls, mol, units=None, use_internals=False) -> dict: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L559)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L559?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, *args, use_internals=False, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L582)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L582?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L589)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L589?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up the job: collect its block types and template, index which option names
belong to which block, and sort the supplied options into per-block buckets.
  - `opts`: `Any`
    > the job options, distributed across the blocks


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.get_block_types" class="docs-object-method">&nbsp;</a> 
```python
get_block_types(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L606)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L606?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: return the ordered list of `OptionsBlock` types making up this job.
  - `:returns`: `list`
    > the block types


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.load_template" class="docs-object-method">&nbsp;</a> 
```python
load_template(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L617)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L617?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: return the top-level job template.
  - `:returns`: `str`
    > the job template


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.populate_blocks" class="docs-object-method">&nbsp;</a> 
```python
populate_blocks(self, opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L629)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L629?message=Update%20Docs)]
</div>
**LLM Docstring**

Route each supplied option into the first block that recognizes it, raising if
any option matches no block.
  - `opts`: `dict`
    > the job options
  - `:returns`: `list[dict]`
    > one option dict per block (in block order)


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.get_params" class="docs-object-method">&nbsp;</a> 
```python
get_params(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L659)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L659?message=Update%20Docs)]
</div>
**LLM Docstring**

Build every block's parameters and merge them into a single template-parameter
mapping, raising on key collisions between blocks.
  - `:returns`: `dict`
    > the merged template parameters


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.format" class="docs-object-method">&nbsp;</a> 
```python
format(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L682)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L682?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the full job input file by filling the job template with the merged block
parameters.
  - `:returns`: `str`
    > the formatted job text


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.write" class="docs-object-method">&nbsp;</a> 
```python
write(self, file, mode='w'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L695)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L695?message=Update%20Docs)]
</div>
**LLM Docstring**

Write the formatted job to a file (path or open stream).
  - `file`: `str | IO`
    > an open stream or a file path
  - `mode`: `str`
    > the file mode when a path is given
  - `:returns`: `str | IO`
    > the file/stream that was written
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L526?message=Update%20Docs)   
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