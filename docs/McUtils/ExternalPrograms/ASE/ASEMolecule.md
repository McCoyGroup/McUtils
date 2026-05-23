## <a id="McUtils.ExternalPrograms.ASE.ASEMolecule">ASEMolecule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE.py#L218)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE.py#L218?message=Update%20Docs)]
</div>

A simple interchange format for ASE molecules







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_optimizer: str
convergence_criterion: float
max_steps: int
default_mep: str
```
<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L223)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L223?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L226)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L226?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.charges" class="docs-object-method">&nbsp;</a> 
```python
@property
charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L229)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L229?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.meta" class="docs-object-method">&nbsp;</a> 
```python
@property
meta(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L232)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L232?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L236?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.from_atoms" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_atoms(cls, atoms, calculator=None, charge=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L242)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L242?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.from_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coords(cls, atoms, coords, charge=None, spin=None, info=None, calculator=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L250)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L250?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, coord_unit='Angstroms', calculator=None, calculator_options=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L269)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L269?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.calculate_props" class="docs-object-method">&nbsp;</a> 
```python
calculate_props(self, props, geoms=None, calc=None, extra_calcs=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L312)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L312?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.calculate_energy" class="docs-object-method">&nbsp;</a> 
```python
calculate_energy(self, geoms=None, order=None, calc=None, hessian_func_attr='get_hessian'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L366)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L366?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.lookup_optimizer_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lookup_optimizer_type(cls, method): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L404)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L404?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.resolve_optimizer" class="docs-object-method">&nbsp;</a> 
```python
resolve_optimizer(self, method): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L417)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L417?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.optimize_structure" class="docs-object-method">&nbsp;</a> 
```python
optimize_structure(self, geoms=None, calc=None, quiet=True, logfile=None, logger=None, fmax=None, steps=None, method=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L437)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L437?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.prep_trajectory_images" class="docs-object-method">&nbsp;</a> 
```python
prep_trajectory_images(self, geoms, mol=None, calc=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L491)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L491?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.resolve_trajectory_method" class="docs-object-method">&nbsp;</a> 
```python
resolve_trajectory_method(self, method, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L515)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L515?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.prep_trajectory_type" class="docs-object-method">&nbsp;</a> 
```python
prep_trajectory_type(self, geoms, method, calc=None, in_place=False, optimizer_method=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L530)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L530?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.optimize_trajectory" class="docs-object-method">&nbsp;</a> 
```python
optimize_trajectory(self, geoms, method, calc=None, quiet=True, logfile=None, logger=None, fmax=None, tol=None, steps=None, optimizer=None, optimizer_method=None, in_place=False, return_coords=True, optimizer_settings=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L557)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L557?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE.py#L218?message=Update%20Docs)   
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