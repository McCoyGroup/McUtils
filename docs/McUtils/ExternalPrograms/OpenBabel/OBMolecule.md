## <a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule">OBMolecule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/OpenBabel.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/OpenBabel.py#L16?message=Update%20Docs)]
</div>

A simple interchange format for RDKit molecules







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, obmol, charge=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/OpenBabel/OBMolecule.py#L21)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/OpenBabel/OBMolecule.py#L21?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.get_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L26)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L26?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/OpenBabel/OBMolecule.py#L29)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/OpenBabel/OBMolecule.py#L29?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.bonds" class="docs-object-method">&nbsp;</a> 
```python
@property
bonds(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/OpenBabel/OBMolecule.py#L33)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/OpenBabel/OBMolecule.py#L33?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/OpenBabel/OBMolecule.py#L40)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/OpenBabel/OBMolecule.py#L40?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_obmol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_obmol(cls, obmol, add_implicit_hydrogens=False, charge=None, guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L48?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_string" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_string(cls, data, fmt=None, target_fmt='mol2', add_implicit_hydrogens=False, charge=None, guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L56)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L56?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_file" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_file(cls, file, fmt=None, target_fmt='mol2', add_implicit_hydrogens=False, charge=None, guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L70)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L70?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.to_file" class="docs-object-method">&nbsp;</a> 
```python
to_file(self, file, fmt=None, base_fmt='mol2'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/OpenBabel/OBMolecule.py#L87)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/OpenBabel/OBMolecule.py#L87?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.to_string" class="docs-object-method">&nbsp;</a> 
```python
to_string(self, fmt, base_fmt='mol2'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/OpenBabel/OBMolecule.py#L98)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/OpenBabel/OBMolecule.py#L98?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coords(cls, atoms, coords, bonds=None, add_implicit_hydrogens=False, charge=None, guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L105?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, coord_unit='Angstroms', guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L124)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L124?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.show" class="docs-object-method">&nbsp;</a> 
```python
show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/OpenBabel/OBMolecule.py#L242)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/OpenBabel/OBMolecule.py#L242?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/OpenBabel/OBMolecule.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/OpenBabel/OBMolecule.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/OpenBabel/OBMolecule.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/OpenBabel/OBMolecule.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/OpenBabel.py#L16?message=Update%20Docs)   
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