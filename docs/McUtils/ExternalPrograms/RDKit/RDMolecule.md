## <a id="McUtils.ExternalPrograms.RDKit.RDMolecule">RDMolecule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L14?message=Update%20Docs)]
</div>

A simple interchange format for RDKit molecules







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, rdconf, charge=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L19?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.rdmol" class="docs-object-method">&nbsp;</a> 
```python
@property
rdmol(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L25)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L25?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L30)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L30?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.bonds" class="docs-object-method">&nbsp;</a> 
```python
@property
bonds(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L34)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L34?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L41)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L41?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.rings" class="docs-object-method">&nbsp;</a> 
```python
@property
rings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L44)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L44?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.meta" class="docs-object-method">&nbsp;</a> 
```python
@property
meta(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L47?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L51)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L51?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.charges" class="docs-object-method">&nbsp;</a> 
```python
@property
charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L59)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L59?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.chem_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
chem_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L68)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L68?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_rdmol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_rdmol(cls, rdmol, conf_id=0, charge=None, guess_bonds=False, sanitize=True, add_implicit_hydrogens=False, sanitize_ops=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L71)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L71?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coords(cls, atoms, coords, bonds=None, charge=None, guess_bonds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L99)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L99?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, coord_unit='Angstroms', guess_bonds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L133)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L133?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_sdf" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_sdf(cls, sdf_string, which=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L152?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_confgen_opts" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_confgen_opts(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L161)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L161?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_smiles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_smiles(cls, smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, replacements=None, add_implicit_hydrogens=False, call_add_hydrogens=True, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L168)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L168?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_base_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_base_mol(cls, mol, conf_id=-1, num_confs=1, optimize=False, take_min=None, force_field_type='mmff', **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L214)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L214?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_no_conformer_molecule" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_no_conformer_molecule(cls, mol, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L236?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_smiles" class="docs-object-method">&nbsp;</a> 
```python
to_smiles(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L282)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L282?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_molblock" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_molblock(cls, molblock): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L285)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L285?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.allchem_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
allchem_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L294)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L294?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_force_field_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_force_field_type(cls, ff_type): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L297)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L297?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_force_field" class="docs-object-method">&nbsp;</a> 
```python
get_force_field(self, force_field_type='mmff', mol=None, conf_id=None, **extra_props): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L311)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L311?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.evaluate_charges" class="docs-object-method">&nbsp;</a> 
```python
evaluate_charges(self, coords, model='gasteiger'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L334)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L334?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_energy" class="docs-object-method">&nbsp;</a> 
```python
calculate_energy(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L345)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L345?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_gradient" class="docs-object-method">&nbsp;</a> 
```python
calculate_gradient(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L366)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L366?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_hessian" class="docs-object-method">&nbsp;</a> 
```python
calculate_hessian(self, force_field_generator=None, force_field_type='mmff', stencil=5, mesh_spacing=0.01, **fd_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L387)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L387?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_optimizer_params" class="docs-object-method">&nbsp;</a> 
```python
get_optimizer_params(self, maxAttempts=1000, useExpTorsionAnglePrefs=True, useBasicKnowledge=True, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L412)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L412?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.optimize_structure" class="docs-object-method">&nbsp;</a> 
```python
optimize_structure(self, geoms=None, force_field_type='mmff', optimizer=None, maxIters=1000, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L424)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L424?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.show" class="docs-object-method">&nbsp;</a> 
```python
show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L452)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L452?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/RDKit/RDMolecule.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/RDKit/RDMolecule.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/RDKit/RDMolecule.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/RDKit/RDMolecule.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L14?message=Update%20Docs)   
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