## <a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule">OBMolecule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel.py#L19?message=Update%20Docs)]
</div>

A simple interchange format for OB molecules







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_conformer_generator: str
default_output_format: str
```
<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, obmol, charge=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel.py#L24)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel.py#L24?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.pbmol" class="docs-object-method">&nbsp;</a> 
```python
@property
pbmol(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L29)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L29?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.get_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L36)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L36?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L39)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L39?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.bonds" class="docs-object-method">&nbsp;</a> 
```python
@property
bonds(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L43)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L43?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L50)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L50?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.set_coords" class="docs-object-method">&nbsp;</a> 
```python
set_coords(self, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L57)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L57?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.atom_iter" class="docs-object-method">&nbsp;</a> 
```python
atom_iter(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L66)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L66?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_obmol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_obmol(cls, obmol, charge=None, guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L70)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L70?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.get_obmol_from_conversion" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_obmol_from_conversion(cls, data, fmt=None, add_implicit_hydrogens=False, target_fmt='mol2'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L77)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L77?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.get_obmol_from_gen3d" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_obmol_from_gen3d(cls, data, fmt=None, add_implicit_hydrogens=False, method='gen3D', target='best'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L89)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L89?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_string" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_string(cls, data, fmt=None, conformer_generator=None, add_implicit_hydrogens=False, charge=None, guess_bonds=False, **confgen_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L107)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L107?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_file" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_file(cls, file, fmt=None, target_fmt='mol2', add_implicit_hydrogens=False, charge=None, guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L126)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L126?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.to_file" class="docs-object-method">&nbsp;</a> 
```python
to_file(self, file, fmt=None, base_fmt='mol2'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L143)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L143?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.to_string" class="docs-object-method">&nbsp;</a> 
```python
to_string(self, fmt, base_fmt='mol2'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L155)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L155?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coords(cls, atoms, coords, bonds=None, add_implicit_hydrogens=False, charge=None, guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L162)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L162?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, coord_unit='Angstroms', guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L186)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L186?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L198)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L198?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.remove_hydrogens" class="docs-object-method">&nbsp;</a> 
```python
remove_hydrogens(self, copy=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L205)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L205?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.make_2d" class="docs-object-method">&nbsp;</a> 
```python
make_2d(self, copy=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L210)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L210?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.draw" class="docs-object-method">&nbsp;</a> 
```python
draw(self, fmt='svg', remove_hydrogens=True, plot_range=None, postdraw=None, scaling_factor=None, splits=None, include_save_buttons=False, use_smiles=False, use_coords=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L224)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L224?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel.py#L19?message=Update%20Docs)   
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