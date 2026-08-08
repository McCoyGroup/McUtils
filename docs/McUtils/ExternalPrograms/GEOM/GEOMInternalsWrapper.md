## <a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper">GEOMInternalsWrapper</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM.py#L943)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L943?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, loader, zdata, managed_store=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM.py#L944)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L944?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.from_files" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_files(cls, root=None, geom_file='geom_dataset.tar.gz', jump_index_path='geom_jump_indices.npz', coords_zip='geom_coordinates.zip'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L949)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L949?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.close" class="docs-object-method">&nbsp;</a> 
```python
close(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L965)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L965?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L968)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L968?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, *exit_args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L970)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L970?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.load_chunk" class="docs-object-method">&nbsp;</a> 
```python
load_chunk(self, i): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L972)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L972?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.load_conformer" class="docs-object-method">&nbsp;</a> 
```python
load_conformer(self, i): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L988)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L988?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.get_system_offsets" class="docs-object-method">&nbsp;</a> 
```python
get_system_offsets(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L993)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L993?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.system_offset" class="docs-object-method">&nbsp;</a> 
```python
system_offset(self, i, return_nconfs=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L997)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L997?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.load_system_chunks" class="docs-object-method">&nbsp;</a> 
```python
load_system_chunks(self, i, load_confs=False, load_representative=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1004)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1004?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.get_internals" class="docs-object-method">&nbsp;</a> 
```python
get_internals(self, mol): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1036)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1036?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.block_iter" class="docs-object-method">&nbsp;</a> 
```python
block_iter(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1039)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1039?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L943?message=Update%20Docs)   
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