## <a id="McUtils.ExternalPrograms.RDKit.RDMolecule">RDMolecule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L20?message=Update%20Docs)]
</div>

A simple interchange format for RDKit molecules







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_new_coord_alignment_method: str
implicit_hydrogen_to_conformer_method: str
draw_options_mapping: dict
drawing_defaults: dict
defaul_conformer_compression: str
default_tag_byte_size: int
default_tag_byte_encoding: int
DisplayImage: DisplayImage
```
<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, rdconf, charge=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit.py#L25)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L25?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.rdmol" class="docs-object-method">&nbsp;</a> 
```python
@property
rdmol(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L31)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L31?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L36)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L36?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.bonds" class="docs-object-method">&nbsp;</a> 
```python
@property
bonds(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L40)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L40?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L47?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.rings" class="docs-object-method">&nbsp;</a> 
```python
@property
rings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L50)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L50?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.meta" class="docs-object-method">&nbsp;</a> 
```python
@property
meta(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L53)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L53?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L57)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L57?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.charges" class="docs-object-method">&nbsp;</a> 
```python
@property
charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L68)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L68?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.formal_charges" class="docs-object-method">&nbsp;</a> 
```python
@property
formal_charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L77)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L77?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.quiet_errors" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
quiet_errors(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L84)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L84?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.chem_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
chem_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L89)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L89?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_rdmol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_rdmol(cls, rdmol, conf_id=0, charge=None, guess_bonds=False, sanitize=True, add_implicit_hydrogens=False, sanitize_ops=None, allow_generate_conformers=False, num_confs=1, optimize=False, take_min=True, force_field_type='mmff'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L99)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L99?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.resolve_bond_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_bond_type(cls, t): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L152?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coords(cls, atoms, coords, bonds=None, charge=None, formal_charges=None, guess_bonds=None, add_implicit_hydrogens=False, implicit_hydrogen_method=None, distance_matrix_tol=0.05, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, sanitize=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L259)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L259?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, coord_unit='Angstroms', guess_bonds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L400)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L400?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_sdf" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_sdf(cls, sdf_string, which=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L420)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L420?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_confgen_opts" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_confgen_opts(cls, version='v3', use_experimental_torsion_angle_prefs=True, use_basic_knowledge=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L429)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L429?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.parse_smiles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_smiles(cls, smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, replacements=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L452)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L452?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_smiles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_smiles(cls, smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, replacements=None, add_implicit_hydrogens=False, call_add_hydrogens=True, conf_id=None, num_confs=None, optimize=False, take_min=True, force_field_type='mmff', reorder_from_atom_map=True, confgen_opts=None, check_tag=True, coords=None, conf_tag=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L485)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L485?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_base_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_base_mol(cls, mol, conf_id=None, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L567)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L567?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.generate_conformers_for_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
generate_conformers_for_mol(cls, mol, *, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, distance_constraints=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L606)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L606?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_no_conformer_molecule" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_no_conformer_molecule(cls, mol, *, conf_id=None, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, confgen_opts=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L685)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L685?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_smiles" class="docs-object-method">&nbsp;</a> 
```python
to_smiles(self, remove_hydrogens=None, remove_implicit_hydrogens=None, include_tag=False, canonical=False, compute_stereo=False, remove_stereo=False, preserve_atom_order=False, binary=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L723)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L723?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.find_substructure" class="docs-object-method">&nbsp;</a> 
```python
find_substructure(self, query): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L899)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L899?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.draw" class="docs-object-method">&nbsp;</a> 
```python
draw(self, figure=None, background=None, remove_atom_numbers=False, remove_hydrogens=True, display_atom_numbers=False, format='svg', drawer=None, use_coords=False, atom_labels=None, highlight_atoms=None, highlight_bonds=None, highlight_atom_colors=None, highlight_bond_colors=None, conf_id=None, include_save_buttons=False, **draw_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L904)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L904?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, conf_id=None, image_size=(450, 450), **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1066)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1066?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.conformer_smiles_tag" class="docs-object-method">&nbsp;</a> 
```python
conformer_smiles_tag(self, coords=None, graph=None, zmatrix=None, encoder=None, byte_size=None, byte_encoding=None, binary=False, include_zmatrix=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1265)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1265?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.conformer_from_smiles_tag" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
conformer_from_smiles_tag(cls, tag, graph, decoder=None, byte_size=None, byte_encoding=None, zmatrix=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1328)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1328?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_mol_edge_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_mol_edge_graph(cls, mol): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1365)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1365?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_edge_graph" class="docs-object-method">&nbsp;</a> 
```python
get_edge_graph(self, mol=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1374)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1374?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_molblock" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_molblock(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1556)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1556?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mrv" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mrv(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1573)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1573?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_xyz(cls, molblock, add_implicit_hydrogens=False, guess_bonds=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1590)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1590?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mol2" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol2(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1607)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1607?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_cdxml" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_cdxml(cls, molblock, add_implicit_hydrogens=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1624)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1624?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_pdb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_pdb(cls, molblock, add_implicit_hydrogens=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1639)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1639?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_png" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_png(cls, molblock, add_implicit_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1654)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1654?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_fasta" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_fasta(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1669)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1669?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_inchi" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_inchi(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1686)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1686?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_helm" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_helm(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1703)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1703?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_xyz" class="docs-object-method">&nbsp;</a> 
```python
to_xyz(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1742)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1742?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_molblock" class="docs-object-method">&nbsp;</a> 
```python
to_molblock(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1754)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1754?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_mrv" class="docs-object-method">&nbsp;</a> 
```python
to_mrv(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1766)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1766?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_pdb" class="docs-object-method">&nbsp;</a> 
```python
to_pdb(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1778)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1778?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_cml" class="docs-object-method">&nbsp;</a> 
```python
to_cml(self, filename=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1790)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1790?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.allchem_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
allchem_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1800)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1800?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_force_field_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_force_field_type(cls, ff_type): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1803)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1803?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_force_field" class="docs-object-method">&nbsp;</a> 
```python
get_force_field(self, force_field_type='mmff', conf=None, mol=None, conf_id=None, **extra_props): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1817)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1817?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.evaluate_charges" class="docs-object-method">&nbsp;</a> 
```python
evaluate_charges(self, coords, model='gasteiger'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1852)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1852?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_energy" class="docs-object-method">&nbsp;</a> 
```python
calculate_energy(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1863)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1863?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_gradient" class="docs-object-method">&nbsp;</a> 
```python
calculate_gradient(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1892)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1892?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_hessian" class="docs-object-method">&nbsp;</a> 
```python
calculate_hessian(self, force_field_generator=None, force_field_type='mmff', stencil=5, mesh_spacing=0.01, **fd_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1922)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1922?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_optimizer_params" class="docs-object-method">&nbsp;</a> 
```python
get_optimizer_params(self, maxAttempts=1000, useExpTorsionAnglePrefs=True, useBasicKnowledge=True, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1947)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1947?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.optimize_structure" class="docs-object-method">&nbsp;</a> 
```python
optimize_structure(self, geoms=None, force_field_type='mmff', optimizer=None, maxIters=1000, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1959)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1959?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.show" class="docs-object-method">&nbsp;</a> 
```python
show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1987)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1987?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L20?message=Update%20Docs)   
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