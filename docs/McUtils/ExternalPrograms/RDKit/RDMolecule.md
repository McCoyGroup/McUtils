## <a id="McUtils.ExternalPrograms.RDKit.RDMolecule">RDMolecule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit.py#L24)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L24?message=Update%20Docs)]
</div>

A simple interchange format for RDKit molecules







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
NullContext: NullContext
default_new_coord_alignment_method: str
implicit_hydrogen_to_conformer_method: str
default_fragment_placement_method: str
different_fragment_embedding_distance: int
draw_options_mapping: dict
drawing_defaults: dict
default_draw_options: dict
default_up_vector: tuple
default_right_vector: tuple
default_view_vector: tuple
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit.py#L29)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L29?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.rdmol" class="docs-object-method">&nbsp;</a> 
```python
@property
rdmol(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L35)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L35?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L40)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L40?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.bonds" class="docs-object-method">&nbsp;</a> 
```python
@property
bonds(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L44)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L44?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L51)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L51?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.rings" class="docs-object-method">&nbsp;</a> 
```python
@property
rings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L58)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L58?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.meta" class="docs-object-method">&nbsp;</a> 
```python
@property
meta(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L61)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L61?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L65)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L65?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.charges" class="docs-object-method">&nbsp;</a> 
```python
@property
charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L76)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L76?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.formal_charges" class="docs-object-method">&nbsp;</a> 
```python
@property
formal_charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L85)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L85?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.quiet_errors" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
quiet_errors(cls, verbose=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L97)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L97?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.chem_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
chem_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L105?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.guess_rdmol_bonds" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
guess_rdmol_bonds(cls, rdmol, charge=None, determine_orders=True, in_place=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L115?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_rdmol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_rdmol(cls, rdmol, conf_id=0, charge=None, guess_bonds=False, sanitize=True, add_implicit_hydrogens=False, sanitize_ops=None, allow_generate_conformers=False, num_confs=1, optimize=False, take_min=True, force_field_type='mmff'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L132)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L132?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.resolve_bond_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_bond_type(cls, t): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L183?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coords(cls, atoms, coords, bonds=None, charge=None, formal_charges=None, guess_bonds=None, add_implicit_hydrogens=False, implicit_hydrogen_method=None, distance_matrix_tol=0.05, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, sanitize=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L290)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L290?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, coord_unit='Angstroms', guess_bonds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L436)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L436?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_sdf" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_sdf(cls, sdf_string, which=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L456)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L456?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_confgen_opts" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_confgen_opts(cls, version='v3', use_experimental_torsion_angle_prefs=True, use_basic_knowledge=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L465)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L465?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.parse_smiles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_smiles(cls, smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, add_implicit_hydrogens=None, reorder_from_atom_map=False, replacements=None, quiet=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L488)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L488?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_smiles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_smiles(cls, smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, replacements=None, add_implicit_hydrogens=False, call_add_hydrogens=True, conf_id=None, num_confs=None, optimize=False, take_min=True, force_field_type='mmff', reorder_from_atom_map=True, confgen_opts=None, check_tag=True, coords=None, conf_tag=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L555)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L555?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_base_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_base_mol(cls, mol, conf_id=None, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L633)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L633?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.generate_conformers_for_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
generate_conformers_for_mol(cls, mol, *, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, distance_constraints=None, initial_coordinates=None, fragment_placement_method=None, fragments=None, embedding_mol=None, verbose=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L785)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L785?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_no_conformer_molecule" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_no_conformer_molecule(cls, mol, *, conf_id=None, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, confgen_opts=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1006)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1006?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_smiles" class="docs-object-method">&nbsp;</a> 
```python
to_smiles(self, remove_hydrogens=None, remove_implicit_hydrogens=None, include_tag=False, canonical=False, compute_stereo=False, remove_stereo=False, preserve_atom_order=False, binary=False, coords=None, mol=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1047)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1047?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.find_substructure" class="docs-object-method">&nbsp;</a> 
```python
find_substructure(self, query): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1770)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1770?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.apply_smarts_to_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
apply_smarts_to_mol(cls, mol, pattern, remove_hydrogens=True, readd_hydrogens=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1775)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1775?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.apply_smarts" class="docs-object-method">&nbsp;</a> 
```python
apply_smarts(self, tf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1878)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1878?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.take_mol_fragment" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
take_mol_fragment(cls, mol, inds, conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1921)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1921?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.break_bonds" class="docs-object-method">&nbsp;</a> 
```python
break_bonds(self, bonds, add_dummies=False, reguess_bonds=True, return_fragments=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1947)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1947?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.fragment_rdmol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fragment_rdmol(cls, mol, inds): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1977)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1977?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.fragment_rdmol_on_bonds" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fragment_rdmol_on_bonds(cls, mol, bonds, addDummies=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1992)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1992?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_atom_neighbors" class="docs-object-method">&nbsp;</a> 
```python
get_atom_neighbors(self, i, n=1, mol=None, graph=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2014)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2014?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.draw" class="docs-object-method">&nbsp;</a> 
```python
draw(self, figure=None, background=None, remove_atom_numbers=None, remove_hydrogens=True, display_atom_numbers=False, format='svg', drawer=None, coords=None, use_coords=False, align_2d=None, view_settings=None, plot_range=None, atom_labels=None, bond_labels=None, blend_mixed_bonds=True, highlight_atoms=None, highlight_bonds=None, highlight_atom_colors=None, highlight_bond_colors=None, highlight_atom_radii=None, highlight_bond_radii=None, highlight_bond_width_multiplier=None, atom_radii=None, bond_radius=None, allow_radius_rescaling=True, draw_coords=None, highlight_rings=None, label_offset=1, conf_id=None, include_save_buttons=False, no_free_type=None, postdraw=None, return_splits=None, radius_to_range_scaling=None, **draw_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2072)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2072?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, conf_id=None, image_size=(450, 450), **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2606)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2606?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.conformer_smiles_tag" class="docs-object-method">&nbsp;</a> 
```python
conformer_smiles_tag(self, coords=None, graph=None, zmatrix=None, encoder=None, byte_size=None, byte_encoding=None, binary=False, include_zmatrix=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2806)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2806?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.conformer_from_smiles_tag" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
conformer_from_smiles_tag(cls, tag, graph, decoder=None, byte_size=None, byte_encoding=None, zmatrix=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2869)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2869?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_mol_edge_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_mol_edge_graph(cls, mol): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2906)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2906?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_edge_graph" class="docs-object-method">&nbsp;</a> 
```python
get_edge_graph(self, mol=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2915)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2915?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_molblock" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_molblock(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3522)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3522?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mrv" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mrv(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3539)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3539?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_xyz(cls, molblock, add_implicit_hydrogens=False, guess_bonds=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3556)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3556?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mol2" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol2(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3573)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3573?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_cdxml" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_cdxml(cls, molblock, add_implicit_hydrogens=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3590)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3590?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_pdb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_pdb(cls, molblock, add_implicit_hydrogens=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3605)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3605?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_png" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_png(cls, molblock, add_implicit_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3620)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3620?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_fasta" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_fasta(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3635)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3635?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_inchi" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_inchi(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3652)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3652?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_helm" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_helm(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3669)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3669?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_xyz" class="docs-object-method">&nbsp;</a> 
```python
to_xyz(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3723)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3723?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_molblock" class="docs-object-method">&nbsp;</a> 
```python
to_molblock(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3735)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3735?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_mrv" class="docs-object-method">&nbsp;</a> 
```python
to_mrv(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3747)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3747?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_pdb" class="docs-object-method">&nbsp;</a> 
```python
to_pdb(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3759)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3759?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_cml" class="docs-object-method">&nbsp;</a> 
```python
to_cml(self, filename=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3771)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3771?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_sdf" class="docs-object-method">&nbsp;</a> 
```python
to_sdf(self, filename=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3804)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3804?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.allchem_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
allchem_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3812)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3812?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_force_field_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_force_field_type(cls, ff_type): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3815)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3815?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_force_field" class="docs-object-method">&nbsp;</a> 
```python
get_force_field(self, force_field_type='mmff', conf=None, mol=None, conf_id=None, **extra_props): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3829)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3829?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.evaluate_charges" class="docs-object-method">&nbsp;</a> 
```python
evaluate_charges(self, coords, model='gasteiger'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3862)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3862?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_energy" class="docs-object-method">&nbsp;</a> 
```python
calculate_energy(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3873)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3873?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_gradient" class="docs-object-method">&nbsp;</a> 
```python
calculate_gradient(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3902)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3902?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_hessian" class="docs-object-method">&nbsp;</a> 
```python
calculate_hessian(self, force_field_generator=None, force_field_type='mmff', stencil=5, mesh_spacing=0.01, **fd_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3932)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3932?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_optimizer_params" class="docs-object-method">&nbsp;</a> 
```python
get_optimizer_params(self, maxAttempts=1000, useExpTorsionAnglePrefs=True, useBasicKnowledge=True, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3957)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3957?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.optimize_structure" class="docs-object-method">&nbsp;</a> 
```python
optimize_structure(self, geoms=None, force_field_type='mmff', optimizer=None, maxIters=1000, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3969)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3969?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.show" class="docs-object-method">&nbsp;</a> 
```python
show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3997)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3997?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L24?message=Update%20Docs)   
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