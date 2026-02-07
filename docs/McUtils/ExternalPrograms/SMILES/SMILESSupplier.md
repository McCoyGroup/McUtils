## <a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier">SMILESSupplier</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L14?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
known_suppliers: dict
```
<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, smiles_file, line_indices=None, name=None, size=1000, split_idx=0, split_char=None, line_parser=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L15?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.from_name" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_name(cls, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L58)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L58?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L62)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L62?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L83)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L83?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L93)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L93?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.find_smi" class="docs-object-method">&nbsp;</a> 
```python
find_smi(self, n, block_size=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L116)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L116?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.consume_iter" class="docs-object-method">&nbsp;</a> 
```python
consume_iter(self, start_at=None, upto=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L140)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L140?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__next__" class="docs-object-method">&nbsp;</a> 
```python
__next__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L172)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L172?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L180)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L180?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.create_line_index" class="docs-object-method">&nbsp;</a> 
```python
create_line_index(self, upto=None, return_index=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L191?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.save_line_index" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
save_line_index(cls, file, line_index): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L227)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L227?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L14?message=Update%20Docs)   
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