## <a id="McUtils.ExternalPrograms.ASE.ASEMolecule">ASEMolecule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE.py#L15?message=Update%20Docs)]
</div>

A simple interchange format for ASE molecules







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
convergence_criterion: float
max_steps: int
```
<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L20?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L23)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L23?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.charges" class="docs-object-method">&nbsp;</a> 
```python
@property
charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L26)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L26?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.from_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coords(cls, atoms, coords, charge=None, calculator=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L30)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L30?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, coord_unit='Angstroms', calculator=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L44)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L44?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.calculate_energy" class="docs-object-method">&nbsp;</a> 
```python
calculate_energy(self, geoms=None, order=None, calc=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L83)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L83?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.optimize_structure" class="docs-object-method">&nbsp;</a> 
```python
optimize_structure(self, geoms=None, calc=None, quiet=True, logfile=None, fmax=None, steps=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L134)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L134?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ASE/ASEMolecule.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ASE/ASEMolecule.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ASE/ASEMolecule.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ASE/ASEMolecule.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE.py#L15?message=Update%20Docs)   
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