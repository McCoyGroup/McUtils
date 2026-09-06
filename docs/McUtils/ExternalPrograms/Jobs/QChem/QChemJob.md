## <a id="McUtils.ExternalPrograms.Jobs.QChem.QChemJob">QChemJob</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/QChem.py#L118)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/QChem.py#L118?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
extension: str
job_template: str
blocks: list
```
<a id="McUtils.ExternalPrograms.Jobs.QChem.QChemJob.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *strs, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/QChem.py#L133)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/QChem.py#L133?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.QChem.QChemJob.get_block_types" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_block_types(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L138)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L138?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.QChem.QChemJob.load_template" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_template(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L142)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L142?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.QChem.QChemJob.optimization" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
optimization(cls, *strs, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L146)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L146?message=Update%20Docs)]
</div>
Construct a Q-Chem geometry-optimization job (`JOBTYPE = OPT`). An
explicit `jobtype=...` (or a bare jobtype string in `strs`) takes
precedence over the default.
  - `strs`: `Any`
    > bare positional options (first non-jobtype-overridden one
    sets `jobtype`)
  - `opts`: `Any`
    > the job options
  - `:returns`: `QChemJob`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Jobs/QChem/QChemJob.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Jobs/QChem/QChemJob.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Jobs/QChem/QChemJob.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Jobs/QChem/QChemJob.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/QChem.py#L118?message=Update%20Docs)   
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