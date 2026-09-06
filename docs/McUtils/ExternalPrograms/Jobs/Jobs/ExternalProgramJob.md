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


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.get_common_aliases" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_common_aliases(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L562)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L562?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.translate_common_opts" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
translate_common_opts(cls, opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L567)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L567?message=Update%20Docs)]
</div>
Rewrites universal option names (`memory`, `nproc`, `checkpoint`, ...) into
whatever this backend's `__common_aliases__` maps them to, before block
routing. A target can be a canonical prop name, a dotted "block.subopt"
path (for options nested in a `%block ... end`-style spec), or a callable
that gets first crack (useful when one common option depends on another,
e.g. ORCA's per-core `MaxCore` depending on `nproc`).


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.get_mol_options" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_mol_options(cls, mol, units=None, use_internals=False) -> dict: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L608)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L608?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, *args, use_internals=False, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L631)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L631?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.Jobs.ExternalProgramJob.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L638)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L638?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L656)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L656?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L667)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L667?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L679)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L679?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L709)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L709?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L732)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L732?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L745)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/ExternalProgramJob.py#L745?message=Update%20Docs)]
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