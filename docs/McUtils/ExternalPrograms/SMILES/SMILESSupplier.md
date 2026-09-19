## <a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier">SMILESSupplier</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L47?message=Update%20Docs)]
</div>

A line-indexed supplier whose objects are SMILES strings.

``split_idx`` and ``split_char`` remain supported, but are implemented by
the default ``deserialization_function`` rather than by the generic base.
Passing the legacy ``line_parser`` argument still takes precedence.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
STORED_FILE_NAME: str
INDEX_FILE_NAME: str
META_FILE_NAME: str
LISMI_SMI_MEMBER: str
LISMI_IDX_MEMBER: str
LISMI_META_MEMBER: str
known_suppliers: dict
```
<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, smiles_file, line_indices=None, name=None, size=1000, split_idx=0, split_char=None, managed_streams=None, line_parser=None, metadata_arrays=None, deserialization_function=None, stored_file_name=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L82)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L82?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.from_name" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_name(cls, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L140)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L140?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.from_line_index_database" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_line_index_database(cls, database_file, name=None, split_idx=<McUtils.Devutils.core.DefaultType instance>, split_char=None, metadata_arrays=None, deserialization_function=None, **extra): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L144)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L144?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.to_mp_state" class="docs-object-method">&nbsp;</a> 
```python
to_mp_state(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L190)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L190?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.from_mp_state" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mp_state(cls, state, line_indices=None, **extra): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L200)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L200?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.find_smi" class="docs-object-method">&nbsp;</a> 
```python
find_smi(self, n, block_size=None, include_metadata=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L213)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L213?message=Update%20Docs)]
</div>
Backward-compatible alias for :meth:`find_object`.


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.write_database_index" class="docs-object-method">&nbsp;</a> 
```python
write_database_index(self, target, **options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L219)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L219?message=Update%20Docs)]
</div>
Backward-compatible alias for :meth:`write_jump_database`.


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.build_line_index_smiles_database_from_source" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
build_line_index_smiles_database_from_source(cls, supplier_or_smiles_file, out_file, line_indices=None, name=None, split_idx=0, split_char=None, metadata_arrays=None, overwrite=False, stored_file_name=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L230)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L230?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/SMILES/SMILESSupplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/SMILES/SMILESSupplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/SMILES/SMILESSupplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/SMILES/SMILESSupplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L47?message=Update%20Docs)   
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