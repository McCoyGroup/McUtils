## <a id="McUtils.ExternalPrograms.RDKit.RDMolecule">RDMolecule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit.py#L21)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L21?message=Update%20Docs)]
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
```
<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, rdconf, charge=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit.py#L26)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L26?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.rdmol" class="docs-object-method">&nbsp;</a> 
```python
@property
rdmol(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L32?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L37?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.bonds" class="docs-object-method">&nbsp;</a> 
```python
@property
bonds(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L41)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L41?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L48?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.rings" class="docs-object-method">&nbsp;</a> 
```python
@property
rings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L55)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L55?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.meta" class="docs-object-method">&nbsp;</a> 
```python
@property
meta(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L58)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L58?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L62)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L62?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.charges" class="docs-object-method">&nbsp;</a> 
```python
@property
charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L73)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L73?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.formal_charges" class="docs-object-method">&nbsp;</a> 
```python
@property
formal_charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L82)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L82?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.quiet_errors" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
quiet_errors(cls, verbose=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L94)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L94?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.chem_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
chem_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L102?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.guess_rdmol_bonds" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
guess_rdmol_bonds(cls, rdmol, charge=None, determine_orders=True, in_place=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L112)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L112?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_rdmol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_rdmol(cls, rdmol, conf_id=0, charge=None, guess_bonds=False, sanitize=True, add_implicit_hydrogens=False, sanitize_ops=None, allow_generate_conformers=False, num_confs=1, optimize=False, take_min=True, force_field_type='mmff'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L129)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L129?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.resolve_bond_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_bond_type(cls, t): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L180)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L180?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coords(cls, atoms, coords, bonds=None, charge=None, formal_charges=None, guess_bonds=None, add_implicit_hydrogens=False, implicit_hydrogen_method=None, distance_matrix_tol=0.05, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, sanitize=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L287?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, coord_unit='Angstroms', guess_bonds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L433)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L433?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_sdf" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_sdf(cls, sdf_string, which=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L453)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L453?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_confgen_opts" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_confgen_opts(cls, version='v3', use_experimental_torsion_angle_prefs=True, use_basic_knowledge=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L462)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L462?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.parse_smiles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_smiles(cls, smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, add_implicit_hydrogens=None, reorder_from_atom_map=False, replacements=None, quiet=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L485)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L485?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_smiles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_smiles(cls, smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, replacements=None, add_implicit_hydrogens=False, call_add_hydrogens=True, conf_id=None, num_confs=None, optimize=False, take_min=True, force_field_type='mmff', reorder_from_atom_map=True, confgen_opts=None, check_tag=True, coords=None, conf_tag=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L552)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L552?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_base_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_base_mol(cls, mol, conf_id=None, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L630)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L630?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.generate_conformers_for_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
generate_conformers_for_mol(cls, mol, *, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, distance_constraints=None, initial_coordinates=None, fragment_placement_method=None, fragments=None, embedding_mol=None, verbose=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L782)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L782?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_no_conformer_molecule" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_no_conformer_molecule(cls, mol, *, conf_id=None, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, confgen_opts=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1003)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1003?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_smiles" class="docs-object-method">&nbsp;</a> 
```python
to_smiles(self, remove_hydrogens=None, remove_implicit_hydrogens=None, include_tag=False, canonical=False, compute_stereo=False, remove_stereo=False, preserve_atom_order=False, binary=False, coords=None, mol=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1044)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1044?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.find_substructure" class="docs-object-method">&nbsp;</a> 
```python
find_substructure(self, query): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1767)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1767?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.apply_smarts_to_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
apply_smarts_to_mol(cls, mol, pattern, remove_hydrogens=True, readd_hydrogens=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1772)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1772?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.apply_smarts" class="docs-object-method">&nbsp;</a> 
```python
apply_smarts(self, tf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1875)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1875?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.take_mol_fragment" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
take_mol_fragment(cls, mol, inds, conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1918)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1918?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.break_bonds" class="docs-object-method">&nbsp;</a> 
```python
break_bonds(self, bonds, add_dummies=False, reguess_bonds=True, return_fragments=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1944)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1944?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.fragment_rdmol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fragment_rdmol(cls, mol, inds): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1974)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1974?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.fragment_rdmol_on_bonds" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fragment_rdmol_on_bonds(cls, mol, bonds, addDummies=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1989)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1989?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_atom_neighbors" class="docs-object-method">&nbsp;</a> 
```python
get_atom_neighbors(self, i, n=1, mol=None, graph=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2011)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2011?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.draw" class="docs-object-method">&nbsp;</a> 
```python
draw(self, figure=None, background=None, remove_atom_numbers=None, remove_hydrogens=True, display_atom_numbers=False, format='svg', drawer=None, coords=None, use_coords=False, align_2d=None, view_settings=None, plot_range=None, atom_labels=None, bond_labels=None, blend_mixed_bonds=True, highlight_atoms=None, highlight_bonds=None, highlight_atom_colors=None, highlight_bond_colors=None, highlight_atom_radii=None, highlight_bond_radii=None, highlight_bond_width_multiplier=None, atom_radii=None, bond_radius=None, allow_radius_rescaling=True, draw_coords=None, highlight_rings=None, label_offset=1, conf_id=None, include_save_buttons=False, no_free_type=None, postdraw=None, return_splits=None, radius_to_range_scaling=None, **draw_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2069)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2069?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, conf_id=None, image_size=(450, 450), **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2603)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2603?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.conformer_smiles_tag" class="docs-object-method">&nbsp;</a> 
```python
conformer_smiles_tag(self, coords=None, graph=None, zmatrix=None, encoder=None, byte_size=None, byte_encoding=None, binary=False, include_zmatrix=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2803)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2803?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.conformer_from_smiles_tag" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
conformer_from_smiles_tag(cls, tag, graph, decoder=None, byte_size=None, byte_encoding=None, zmatrix=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2866)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2866?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_mol_edge_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_mol_edge_graph(cls, mol): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2903)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2903?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_edge_graph" class="docs-object-method">&nbsp;</a> 
```python
get_edge_graph(self, mol=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2912)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2912?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_molblock" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_molblock(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2972)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2972?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mrv" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mrv(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2989)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2989?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_xyz(cls, molblock, add_implicit_hydrogens=False, guess_bonds=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3006)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3006?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mol2" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol2(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3023)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3023?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_cdxml" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_cdxml(cls, molblock, add_implicit_hydrogens=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3040)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3040?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_pdb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_pdb(cls, molblock, add_implicit_hydrogens=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3055)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3055?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_png" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_png(cls, molblock, add_implicit_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3070)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3070?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_fasta" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_fasta(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3085)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3085?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_inchi" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_inchi(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3102?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_helm" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_helm(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3119?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_xyz" class="docs-object-method">&nbsp;</a> 
```python
to_xyz(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3173)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3173?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_molblock" class="docs-object-method">&nbsp;</a> 
```python
to_molblock(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3185)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3185?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_mrv" class="docs-object-method">&nbsp;</a> 
```python
to_mrv(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3197?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_pdb" class="docs-object-method">&nbsp;</a> 
```python
to_pdb(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3209)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3209?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_cml" class="docs-object-method">&nbsp;</a> 
```python
to_cml(self, filename=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3221)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3221?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_sdf" class="docs-object-method">&nbsp;</a> 
```python
to_sdf(self, filename=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3254)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3254?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.allchem_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
allchem_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3262)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3262?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_force_field_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_force_field_type(cls, ff_type): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3265)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3265?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_force_field" class="docs-object-method">&nbsp;</a> 
```python
get_force_field(self, force_field_type='mmff', conf=None, mol=None, conf_id=None, **extra_props): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3279)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3279?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.evaluate_charges" class="docs-object-method">&nbsp;</a> 
```python
evaluate_charges(self, coords, model='gasteiger'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3312)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3312?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_energy" class="docs-object-method">&nbsp;</a> 
```python
calculate_energy(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3323)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3323?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_gradient" class="docs-object-method">&nbsp;</a> 
```python
calculate_gradient(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3352)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3352?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_hessian" class="docs-object-method">&nbsp;</a> 
```python
calculate_hessian(self, force_field_generator=None, force_field_type='mmff', stencil=5, mesh_spacing=0.01, **fd_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3382)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3382?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_optimizer_params" class="docs-object-method">&nbsp;</a> 
```python
get_optimizer_params(self, maxAttempts=1000, useExpTorsionAnglePrefs=True, useBasicKnowledge=True, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3407)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3407?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.optimize_structure" class="docs-object-method">&nbsp;</a> 
```python
optimize_structure(self, geoms=None, force_field_type='mmff', optimizer=None, maxIters=1000, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3419)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3419?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.show" class="docs-object-method">&nbsp;</a> 
```python
show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3447)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3447?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L21?message=Update%20Docs)   
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