## <a id="McUtils.ExternalPrograms.RDKit.RDMolecule">RDMolecule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L19?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit.py#L24)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L24?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap an RDKit conformer (and its owning mol) as an `RDMolecule`.
  - `rdconf`: `Chem.Conformer`
    > the RDKit conformer
  - `charge`: `int | None`
    > the molecular charge


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.rdmol" class="docs-object-method">&nbsp;</a> 
```python
@property
rdmol(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L40)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L40?message=Update%20Docs)]
</div>
**LLM Docstring**

The underlying RDKit `Mol` object (recovered from the conformer if needed).
  - `:returns`: `Chem.Mol`
    > the RDKit mol


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L53)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L53?message=Update%20Docs)]
</div>
**LLM Docstring**

The element symbols of the atoms, in order.
  - `:returns`: `list[str]`
    > the atom symbols


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.bonds" class="docs-object-method">&nbsp;</a> 
```python
@property
bonds(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L65)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L65?message=Update%20Docs)]
</div>
**LLM Docstring**

The bonds as `[begin_atom, end_atom, order]` triples.
  - `:returns`: `list[list]`
    > the bond list


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L80)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L80?message=Update%20Docs)]
</div>
**LLM Docstring**

The atomic Cartesian coordinates (Angstroms). Setting this writes new positions
onto the conformer.
  - `:returns`: `np.ndarray`
    > the coordinates


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.rings" class="docs-object-method">&nbsp;</a> 
```python
@property
rings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L105?message=Update%20Docs)]
</div>
**LLM Docstring**

The atom-index tuples of the rings found by RDKit's ring perception.
  - `:returns`: `tuple`
    > the ring atom indices


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.meta" class="docs-object-method">&nbsp;</a> 
```python
@property
meta(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L116)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L116?message=Update%20Docs)]
</div>
**LLM Docstring**

The molecule's RDKit properties as a dict.
  - `:returns`: `dict`
    > the property dict


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L128?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a copy of this molecule, carrying over the current conformer and charge.
  - `:returns`: `RDMolecule`
    > the copied molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.charges" class="docs-object-method">&nbsp;</a> 
```python
@property
charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L147)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L147?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-atom Gasteiger partial charges (computed on access).
  - `:returns`: `list[float]`
    > the partial charges


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.formal_charges" class="docs-object-method">&nbsp;</a> 
```python
@property
formal_charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L164?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-atom formal charges.
  - `:returns`: `list[int]`
    > the formal charges


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.quiet_errors" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
quiet_errors(cls, verbose=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L200)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L200?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a context manager that suppresses RDKit's C++ log output, unless
`verbose` is set (in which case a no-op context is returned).
  - `verbose`: `bool`
    > don't suppress logging
  - `:returns`: `object`
    > the (log-blocking or no-op) context manager


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.chem_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
chem_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L219)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L219?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the RDKit `Chem` submodule.
  - `:returns`: `module`
    > the `Chem` module


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.guess_rdmol_bonds" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
guess_rdmol_bonds(cls, rdmol, charge=None, determine_orders=True, in_place=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L246)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L246?message=Update%20Docs)]
</div>
**LLM Docstring**

Perceive the bonds (and, optionally, bond orders) of a mol from its atomic
coordinates, falling back to connectivity-only perception when order
determination fails.
  - `rdmol`: `Chem.Mol`
    > the mol
  - `charge`: `int | None`
    > the molecular charge (inferred if omitted)
  - `determine_orders`: `bool`
    > also perceive bond orders
  - `in_place`: `bool`
    > modify the mol in place rather than copying
  - `:returns`: `Chem.Mol`
    > the mol with perceived bonds


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_rdmol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_rdmol(cls, rdmol, conf_id=0, charge=None, guess_bonds=False, sanitize=True, add_implicit_hydrogens=False, sanitize_ops=None, allow_generate_conformers=False, num_confs=1, optimize=False, take_min=True, force_field_type='mmff'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L281)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L281?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from an RDKit mol, adding hydrogens and optionally guessing
bonds, sanitizing, and generating conformers.
  - `rdmol`: `Chem.Mol`
    > the source mol
  - `conf_id`: `int`
    > the conformer id to use
  - `charge`: `int | None`
    > the molecular charge (inferred if omitted)
  - `guess_bonds`: `bool`
    > perceive bonds from geometry
  - `sanitize`: `bool`
    > run RDKit sanitization
  - `add_implicit_hydrogens`: `bool`
    > add implicit (not just explicit) hydrogens
  - `sanitize_ops`: `Any`
    > sanitization operation flags
  - `allow_generate_conformers`: `bool`
    > generate conformers if none exist
  - `num_confs`: `int`
    > number of conformers to generate
  - `optimize`: `bool`
    > force-field optimize generated conformers
  - `take_min`: `bool`
    > keep only the lowest-energy generated conformer
  - `force_field_type`: `str`
    > the force field for optimization
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.resolve_bond_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_bond_type(cls, t): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L364)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L364?message=Update%20Docs)]
</div>
**LLM Docstring**

Map a numeric bond order to the corresponding RDKit `BondType` (handling the
aromatic/half-integer cases).
  - `t`: `float`
    > the numeric bond order
  - `:returns`: `Chem.BondType`
    > the RDKit bond type


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coords(cls, atoms, coords, bonds=None, charge=None, formal_charges=None, guess_bonds=None, add_implicit_hydrogens=False, implicit_hydrogen_method=None, distance_matrix_tol=0.05, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, sanitize=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L500)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L500?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from atoms, coordinates, and (optional) bonds, optionally
adding implicit hydrogens (placed by conformer generation) and guessing bonds.
  - `atoms`: `Sequence[str]`
    > the element symbols
  - `coords`: `np.ndarray`
    > the Cartesian coordinates
  - `bonds`: `Sequence | None`
    > the bonds as `[i, j(, order)]`
  - `charge`: `int | None`
    > the molecular charge
  - `formal_charges`: `Sequence | None`
    > per-atom formal charges
  - `guess_bonds`: `bool | None`
    > perceive bonds from geometry (defaults to when no bonds given)
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `implicit_hydrogen_method`: `str | None`
    > how to place added hydrogens (`'align'`/`'initial'`/`'builtin'`)
  - `distance_matrix_tol`: `float`
    > tolerance for distance constraints when aligning
  - `num_confs`: `int | None`
    > number of conformers to generate
  - `optimize`: `bool`
    > force-field optimize generated conformers
  - `take_min`: `bool | None`
    > keep only the lowest-energy conformer
  - `force_field_type`: `str`
    > the force field for optimization
  - `confgen_opts`: `dict | None`
    > extra conformer-generation options
  - `sanitize`: `bool`
    > run sanitization
  - `:returns`: `RDMolecule | list`
    > the wrapped molecule (or a list, when multiple conformers are kept)


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, coord_unit='Angstroms', guess_bonds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L685)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L685?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from a generic molecule object, converting its coordinates
to Angstroms.
  - `mol`: `Any`
    > the source molecule
  - `coord_unit`: `str`
    > the source coordinate unit
  - `guess_bonds`: `bool | None`
    > perceive bonds from geometry
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_sdf" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_sdf(cls, sdf_string, which=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L730)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L730?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from an SDF file path or string.
  - `sdf_string`: `str`
    > the SDF file path or content
  - `which`: `int`
    > the index of the entry to read
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_confgen_opts" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_confgen_opts(cls, version='v3', use_experimental_torsion_angle_prefs=True, use_basic_knowledge=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L751)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L751?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an RDKit ETKDG conformer-generation parameter object of the requested
version, applying the torsion/knowledge flags and any extra options.
  - `version`: `str`
    > the ETKDG version (`'v1'`/`'v2'`/`'v3'`)
  - `use_experimental_torsion_angle_prefs`: `bool`
    > use experimental torsion prefs
  - `use_basic_knowledge`: `bool`
    > use basic chemical knowledge
  - `opts`: `Any`
    > extra parameters set on the params object (camel-cased)
  - `:returns`: `object`
    > the parameter object


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.parse_smiles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_smiles(cls, smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, add_implicit_hydrogens=None, reorder_from_atom_map=False, replacements=None, quiet=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L790)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L790?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse a SMILES (or CXSMILES) string into an RDKit mol, with control over
sanitization, hydrogen handling, and atom-map-based reordering.
  - `smiles`: `str`
    > the SMILES string
  - `sanitize`: `bool`
    > run sanitization
  - `parse_name`: `bool`
    > parse a trailing molecule name
  - `allow_cxsmiles`: `bool`
    > allow CXSMILES extensions
  - `strict_cxsmiles`: `bool`
    > fail on bad CXSMILES rather than ignoring
  - `remove_hydrogens`: `bool`
    > remove explicit hydrogens
  - `add_implicit_hydrogens`: `bool | str | None`
    > add hydrogens (or `'full'` to also re-enable implicit Hs)
  - `reorder_from_atom_map`: `bool`
    > renumber atoms by their atom-map numbers
  - `replacements`: `dict | None`
    > SMILES token replacements
  - `quiet`: `bool`
    > suppress RDKit logging
  - `:returns`: `Chem.Mol | None`
    > the parsed mol, or `None` on failure


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_smiles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_smiles(cls, smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, replacements=None, add_implicit_hydrogens=False, call_add_hydrogens=True, conf_id=None, num_confs=None, optimize=False, take_min=True, force_field_type='mmff', reorder_from_atom_map=True, confgen_opts=None, check_tag=True, coords=None, conf_tag=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L886)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L886?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from a SMILES string (or file), embedding a conformer
(generated, or decoded from a conformer tag / supplied coordinates).
  - `smiles`: `str`
    > the SMILES string or file path
  - `sanitize`: `bool`
    > run sanitization
  - `parse_name`: `bool`
    > parse a trailing molecule name
  - `allow_cxsmiles`: `bool`
    > allow CXSMILES extensions
  - `strict_cxsmiles`: `bool`
    > fail on bad CXSMILES
  - `remove_hydrogens`: `bool`
    > remove explicit hydrogens
  - `replacements`: `dict | None`
    > SMILES token replacements
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `call_add_hydrogens`: `bool`
    > call `AddHs` before embedding
  - `conf_id`: `int | None`
    > the conformer id to use
  - `num_confs`: `int | None`
    > number of conformers to generate
  - `optimize`: `bool`
    > force-field optimize generated conformers
  - `take_min`: `bool`
    > keep only the lowest-energy conformer
  - `force_field_type`: `str`
    > the force field for optimization
  - `reorder_from_atom_map`: `bool`
    > renumber atoms by atom-map number
  - `confgen_opts`: `dict | None`
    > extra conformer-generation options
  - `check_tag`: `bool`
    > split off a trailing `_`-delimited conformer tag
  - `coords`: `np.ndarray | None`
    > explicit coordinates to use instead of generating a conformer
  - `conf_tag`: `str | None`
    > an explicit conformer tag to decode
  - `:returns`: `RDMolecule | list`
    > the wrapped molecule (or list, for multiple conformers)


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_base_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_base_mol(cls, mol, conf_id=None, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1011)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1011?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from an RDKit mol, using an existing conformer when
available and otherwise generating one.
  - `mol`: `Chem.Mol`
    > the source mol
  - `conf_id`: `int | None`
    > the conformer id to use
  - `num_confs`: `int | None`
    > number of conformers to generate
  - `optimize`: `bool`
    > force-field optimize generated conformers
  - `take_min`: `bool | None`
    > keep only the lowest-energy conformer
  - `force_field_type`: `str`
    > the force field for optimization
  - `confgen_opts`: `dict | None`
    > extra conformer-generation options
  - `mol_opts`: `Any`
    > extra options forwarded to `from_rdmol`
  - `:returns`: `RDMolecule | list`
    > the wrapped molecule (or list)


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.generate_conformers_for_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
generate_conformers_for_mol(cls, mol, *, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, distance_constraints=None, initial_coordinates=None, fragment_placement_method=None, fragments=None, embedding_mol=None, verbose=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1261)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1261?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate one or more conformers for a mol via RDKit's ETKDG embedding,
handling disconnected fragments (embedded separately and placed), distance
constraints, fixed initial coordinates, optional force-field optimization, and
lowest-energy selection.
  - `mol`: `Chem.Mol`
    > the mol to embed (modified in place; conformers are added)
  - `num_confs`: `int`
    > number of conformers to generate
  - `optimize`: `bool`
    > force-field optimize the conformers
  - `take_min`: `bool`
    > return only the lowest-energy conformer id
  - `force_field_type`: `str`
    > the force field for optimization/selection
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens before embedding
  - `distance_constraints`: `dict | list | None`
    > pairwise distance bounds (or a full bounds matrix)
  - `initial_coordinates`: `dict | Sequence | None`
    > fixed starting coordinates for some/all atoms
  - `fragment_placement_method`: `str | Callable | None`
    > how to place disconnected fragments
  - `fragments`: `list | None`
    > precomputed fragment atom groups
  - `embedding_mol`: `Chem.Mol | None`
    > a hydrogen-added mol to embed into
  - `verbose`: `bool`
    > don't suppress RDKit logging
  - `:returns`: `int | list`
    > the generated conformer id (or list of ids)


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_no_conformer_molecule" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_no_conformer_molecule(cls, mol, *, conf_id=None, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, confgen_opts=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1518)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1518?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate conformer(s) for a mol that has none, then wrap the result(s) as
`RDMolecule`(s).
  - `mol`: `Chem.Mol`
    > the source mol
  - `conf_id`: `int | None`
    > a specific conformer id to keep (disables optimization)
  - `num_confs`: `int`
    > number of conformers to generate
  - `optimize`: `bool`
    > force-field optimize the conformers
  - `take_min`: `bool`
    > keep only the lowest-energy conformer
  - `force_field_type`: `str`
    > the force field for optimization
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `confgen_opts`: `dict | None`
    > extra conformer-generation options
  - `etc`: `Any`
    > extra options forwarded to `from_rdmol`
  - `:returns`: `RDMolecule | list`
    > the wrapped molecule (or list)


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_smiles" class="docs-object-method">&nbsp;</a> 
```python
to_smiles(self, remove_hydrogens=None, remove_implicit_hydrogens=None, include_tag=False, canonical=False, compute_stereo=False, remove_stereo=False, preserve_atom_order=False, binary=False, coords=None, mol=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1598)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L1598?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the molecule to a SMILES string, with options for hydrogen/stereo
handling, atom-order preservation, and appending a conformer tag encoding the
3D geometry.
  - `remove_hydrogens`: `bool | None`
    > remove explicit hydrogens
  - `remove_implicit_hydrogens`: `bool | None`
    > remove only implicit hydrogens
  - `include_tag`: `bool`
    > append a `_`-delimited conformer tag
  - `canonical`: `bool`
    > emit canonical SMILES
  - `compute_stereo`: `bool`
    > assign stereochemistry from the 3D coordinates first
  - `remove_stereo`: `bool`
    > strip stereochemistry
  - `preserve_atom_order`: `bool`
    > keep the current atom ordering
  - `binary`: `bool`
    > return/encode the tag in binary form
  - `coords`: `np.ndarray | None`
    > coordinates to encode in the tag (defaults to the current ones)
  - `mol`: `Chem.Mol | None`
    > an explicit mol to serialize (defaults to this one)
  - `:returns`: `str | bytes`
    > the SMILES string (optionally with a conformer tag)


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.find_substructure" class="docs-object-method">&nbsp;</a> 
```python
find_substructure(self, query): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2555)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2555?message=Update%20Docs)]
</div>
**LLM Docstring**

Return all substructure matches of a SMARTS query in the molecule.
  - `query`: `str`
    > the SMARTS query
  - `:returns`: `tuple`
    > the matching atom-index tuples


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.apply_smarts_to_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
apply_smarts_to_mol(cls, mol, pattern, remove_hydrogens=True, readd_hydrogens=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2570)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2570?message=Update%20Docs)]
</div>
**LLM Docstring**

Apply a SMARTS reaction transform to a mol, running the reaction and
reassembling the products while preserving atom mapping and re-adding
hydrogens consistently.
  - `mol`: `Chem.Mol`
    > the reactant mol
  - `pattern`: `str | object`
    > the SMARTS reaction (string or reaction object)
  - `remove_hydrogens`: `bool`
    > strip hydrogens before reacting
  - `readd_hydrogens`: `bool`
    > re-add hydrogens to the products
  - `:returns`: `list[Chem.Mol]`
    > the product mols


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.apply_smarts" class="docs-object-method">&nbsp;</a> 
```python
apply_smarts(self, tf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2692)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2692?message=Update%20Docs)]
</div>
**LLM Docstring**

Apply a SMARTS reaction transform to this molecule, returning the products as
`RDMolecule`s carrying the current coordinates.
  - `tf`: `str | object`
    > the SMARTS reaction
  - `:returns`: `list[RDMolecule]`
    > the product molecules


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.take_mol_fragment" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
take_mol_fragment(cls, mol, inds, conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2746)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2746?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a sub-mol from the given atom indices (with the bonds among them),
optionally carrying over a conformer's coordinates.
  - `mol`: `Chem.Mol`
    > the source mol
  - `inds`: `Sequence[int]`
    > the atom indices to keep
  - `conf_id`: `int | None`
    > a conformer id whose coordinates to copy
  - `:returns`: `Chem.Mol`
    > the sub-mol


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.break_bonds" class="docs-object-method">&nbsp;</a> 
```python
break_bonds(self, bonds, add_dummies=False, reguess_bonds=True, return_fragments=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2787)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2787?message=Update%20Docs)]
</div>
**LLM Docstring**

Break the given bonds and return the resulting (fragmented) molecule, carrying
over coordinates and optionally re-perceiving bond orders.
  - `bonds`: `Sequence`
    > the `(i, j)` bonds to break
  - `add_dummies`: `bool`
    > add dummy atoms at the broken bonds
  - `reguess_bonds`: `bool`
    > re-perceive bond orders afterward
  - `return_fragments`: `bool`
    > unused flag
  - `:returns`: `RDMolecule`
    > the fragmented molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.fragment_rdmol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fragment_rdmol(cls, mol, inds): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2834)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2834?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a sub-mol from the given atom indices and the bonds among them.
  - `mol`: `Chem.Mol`
    > the source mol
  - `inds`: `Sequence[int]`
    > the atom indices to keep
  - `:returns`: `Chem.Mol`
    > the sub-mol


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.fragment_rdmol_on_bonds" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fragment_rdmol_on_bonds(cls, mol, bonds, addDummies=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2861)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2861?message=Update%20Docs)]
</div>
**LLM Docstring**

Fragment a mol by breaking the given bonds, returning a mapping from each
fragment's atom-index tuple to its sub-mol (with atom maps restored).
  - `mol`: `Chem.Mol`
    > the source mol
  - `bonds`: `Sequence`
    > the `(i, j)` bonds to break (by atom-map number)
  - `addDummies`: `bool`
    > add dummy atoms at the broken bonds
  - `:returns`: `dict`
    > the `{fragment_indices: sub_mol}` mapping


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_atom_neighbors" class="docs-object-method">&nbsp;</a> 
```python
get_atom_neighbors(self, i, n=1, mol=None, graph=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2898)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2898?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the labels of the atoms within `n` bonds of a given atom.
  - `i`: `int`
    > the central atom index
  - `n`: `int`
    > the neighborhood radius (in bonds)
  - `mol`: `Chem.Mol | None`
    > an explicit mol (defaults to this one)
  - `graph`: `Any`
    > a precomputed edge graph
  - `:returns`: `list`
    > the neighbor atom labels


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.draw" class="docs-object-method">&nbsp;</a> 
```python
draw(self, figure=None, background=None, remove_atom_numbers=None, remove_hydrogens=True, display_atom_numbers=False, format='svg', drawer=None, coords=None, use_coords=False, align_2d=None, view_settings=None, plot_range=None, atom_labels=None, bond_labels=None, blend_mixed_bonds=True, highlight_atoms=None, highlight_bonds=None, highlight_atom_colors=None, highlight_bond_colors=None, highlight_atom_radii=None, highlight_bond_radii=None, highlight_bond_width_multiplier=None, atom_radii=None, bond_radius=None, allow_radius_rescaling=True, draw_coords=None, highlight_rings=None, label_offset=1, conf_id=None, include_save_buttons=False, no_free_type=None, postdraw=None, return_splits=None, radius_to_range_scaling=None, **draw_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2987)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L2987?message=Update%20Docs)]
</div>
**LLM Docstring**

Draw the molecule in 2D (SVG/PNG), with extensive control over hydrogen removal,
2D-coordinate generation and alignment, atom/bond labels and highlights, ring
highlighting, and save buttons.
  - `figure`: `Any`
    > an existing figure/drawer to draw into
  - `background`: `Any`
    > the background color
  - `remove_atom_numbers`: `bool | None`
    > strip atom-map numbers from the drawing
  - `remove_hydrogens`: `bool`
    > hide hydrogens
  - `display_atom_numbers`: `bool`
    > annotate atoms with their indices
  - `format`: `str`
    > `'svg'` or `'png'`
  - `drawer`: `Any`
    > an explicit drawing function
  - `coords`: `np.ndarray | None`
    > explicit 2D coordinates to draw at
  - `use_coords`: `bool`
    > draw using the molecule's own coordinates (projected)
  - `align_2d`: `bool | None`
    > align the generated 2D coordinates to the view
  - `view_settings`: `dict | None`
    > 3D view settings for coordinate alignment
  - `plot_range`: `tuple | None`
    > a fixed drawing range
  - `atom_labels`: `Any`
    > per-atom label overrides
  - `bond_labels`: `Any`
    > per-bond label overrides
  - `blend_mixed_bonds`: `bool`
    > blend colors on bonds between differently colored atoms
  - `highlight_atoms`: `Any`
    > atoms to highlight
  - `highlight_bonds`: `Any`
    > bonds to highlight
  - `highlight_atom_colors`: `Any`
    > per-atom highlight colors
  - `highlight_bond_colors`: `Any`
    > per-bond highlight colors
  - `highlight_atom_radii`: `Any`
    > per-atom highlight radii
  - `highlight_bond_radii`: `Any`
    > per-bond highlight radii
  - `highlight_bond_width_multiplier`: `Any`
    > highlight bond-width multiplier
  - `atom_radii`: `Any`
    > per-atom radii
  - `bond_radius`: `Any`
    > the bond radius
  - `allow_radius_rescaling`: `bool`
    > allow radii to rescale with the plot range
  - `draw_coords`: `Any`
    > extra coordinate annotations
  - `highlight_rings`: `Any`
    > rings to highlight
  - `label_offset`: `Any`
    > the annotation label offset
  - `conf_id`: `int | None`
    > the conformer id
  - `include_save_buttons`: `bool`
    > include save buttons in the output
  - `no_free_type`: `bool | None`
    > disable FreeType font rendering
  - `postdraw`: `Callable | None`
    > a callback invoked after drawing
  - `return_splits`: `bool | None`
    > also return drawing element split metadata
  - `radius_to_range_scaling`: `Any`
    > radius-to-range scaling factor
  - `draw_opts`: `Any`
    > extra drawing options
  - `:returns`: `object`
    > the rendered drawing


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, conf_id=None, image_size=(450, 450), **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3583)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3583?message=Update%20Docs)]
</div>
**LLM Docstring**

Display an interactive 3D rendering of the molecule (via RDKit's IPython 3D
console).
  - `conf_id`: `int | None`
    > the conformer id (defaults to the current one)
  - `image_size`: `tuple`
    > the `(width, height)` of the view
  - `opts`: `Any`
    > extra drawing options
  - `:returns`: `object`
    > the 3D display


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.conformer_smiles_tag" class="docs-object-method">&nbsp;</a> 
```python
conformer_smiles_tag(self, coords=None, graph=None, zmatrix=None, encoder=None, byte_size=None, byte_encoding=None, binary=False, include_zmatrix=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3821)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3821?message=Update%20Docs)]
</div>
**LLM Docstring**

Encode the molecule's 3D geometry into a compact string tag (a Z-matrix of the
canonical-fragment internal coordinates, packed and base-N encoded) suitable for
appending to a SMILES string.
  - `coords`: `np.ndarray | None`
    > the coordinates to encode (defaults to the current ones)
  - `graph`: `Any`
    > the molecular edge graph (built if omitted)
  - `zmatrix`: `Any`
    > an explicit Z-matrix connectivity (built if omitted)
  - `encoder`: `str | Callable | None`
    > the value encoder (`'plain'`/`'compressed'`/`'precision'` or a callable)
  - `byte_size`: `int | None`
    > the per-value bit width
  - `byte_encoding`: `int | Callable | None`
    > the base-N text encoding (16/32/64/85)
  - `binary`: `bool`
    > return raw bytes rather than text
  - `include_zmatrix`: `bool`
    > also return the encoded Z-matrix connectivity
  - `:returns`: `str | bytes | tuple`
    > the conformer tag (and Z-matrix data if requested)


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.conformer_from_smiles_tag" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
conformer_from_smiles_tag(cls, tag, graph, decoder=None, byte_size=None, byte_encoding=None, zmatrix=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3908)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3908?message=Update%20Docs)]
</div>
**LLM Docstring**

Decode a conformer tag back into Cartesian coordinates, using the molecular graph
to reconstruct the canonical-fragment Z-matrix.
  - `tag`: `str`
    > the conformer tag
  - `graph`: `Any`
    > the molecular edge graph
  - `decoder`: `str | Callable | None`
    > the value decoder (`'plain'`/`'compressed'`/`'precision'` or a callable)
  - `byte_size`: `int | None`
    > the per-value bit width
  - `byte_encoding`: `int | Callable | None`
    > the base-N text encoding
  - `zmatrix`: `Any`
    > an explicit Z-matrix connectivity (built if omitted)
  - `:returns`: `np.ndarray`
    > the decoded Cartesian coordinates


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_mol_edge_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_mol_edge_graph(cls, mol): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3964)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3964?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `EdgeGraph` of a mol's atom/bond connectivity.
  - `mol`: `Chem.Mol`
    > the mol
  - `:returns`: `EdgeGraph`
    > the edge graph


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_edge_graph" class="docs-object-method">&nbsp;</a> 
```python
get_edge_graph(self, mol=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3983)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L3983?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `EdgeGraph` of this molecule's connectivity (or of a supplied mol).
  - `mol`: `Chem.Mol | None`
    > an explicit mol (defaults to this one)
  - `:returns`: `EdgeGraph`
    > the edge graph


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_molblock" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_molblock(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4097)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4097?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from a MDL molblock/`.mol` file or string.
  - `molblock`: `str`
    > the molblock file path or content
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `sanitize`: `bool`
    > run sanitization
  - `remove_hydrogens`: `bool`
    > remove explicit hydrogens
  - `mol_opts`: `Any`
    > extra options forwarded to the reader
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mrv" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mrv(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4131)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4131?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from a Marvin `.mrv` file or string.
  - `molblock`: `str`
    > the MRV file path or content
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `sanitize`: `bool`
    > run sanitization
  - `remove_hydrogens`: `bool`
    > remove explicit hydrogens
  - `mol_opts`: `Any`
    > extra options forwarded to the reader
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_xyz" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_xyz(cls, molblock, add_implicit_hydrogens=False, guess_bonds=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4165)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4165?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from an XYZ file or string (perceiving bonds by default).
  - `molblock`: `str`
    > the XYZ file path or content
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `guess_bonds`: `bool`
    > perceive bonds from geometry
  - `mol_opts`: `Any`
    > extra options forwarded to the reader
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_mol2" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol2(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4197?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from a Tripos `.mol2` file or string.
  - `molblock`: `str`
    > the mol2 file path or content
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `sanitize`: `bool`
    > run sanitization
  - `remove_hydrogens`: `bool`
    > remove explicit hydrogens
  - `mol_opts`: `Any`
    > extra options forwarded to the reader
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_cdxml" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_cdxml(cls, molblock, add_implicit_hydrogens=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4231)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4231?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from a ChemDraw `.cdxml` file or string.
  - `molblock`: `str`
    > the CDXML file path or content
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `mol_opts`: `Any`
    > extra options forwarded to the reader
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_pdb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_pdb(cls, molblock, add_implicit_hydrogens=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4259)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4259?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from a PDB file or string.
  - `molblock`: `str`
    > the PDB file path or content
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `mol_opts`: `Any`
    > extra options forwarded to the reader
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_png" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_png(cls, molblock, add_implicit_hydrogens=False, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4287?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from an RDKit-metadata-bearing PNG file or string.
  - `molblock`: `str`
    > the PNG file path or content
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `mol_opts`: `Any`
    > extra options forwarded to the reader
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_fasta" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_fasta(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4315)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4315?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from a FASTA sequence (generating a conformer by default).
  - `molblock`: `str`
    > the FASTA content
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `allow_generate_conformers`: `bool`
    > generate a conformer
  - `mol_opts`: `Any`
    > extra options forwarded to the reader
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_inchi" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_inchi(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4347)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4347?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from an InChI string (generating a conformer by default).
  - `molblock`: `str`
    > the InChI string
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `allow_generate_conformers`: `bool`
    > generate a conformer
  - `mol_opts`: `Any`
    > extra options forwarded to the reader
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.from_helm" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_helm(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4379)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4379?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `RDMolecule` from a HELM (macromolecule) string (generating a conformer
by default).
  - `molblock`: `str`
    > the HELM string
  - `add_implicit_hydrogens`: `bool`
    > add implicit hydrogens
  - `allow_generate_conformers`: `bool`
    > generate a conformer
  - `mol_opts`: `Any`
    > extra options forwarded to the reader
  - `:returns`: `RDMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_xyz" class="docs-object-method">&nbsp;</a> 
```python
to_xyz(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4470)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4470?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the molecule to XYZ (returned as a string, or written to a file).
  - `filename`: `str | None`
    > the output file path (or `None` to return a string)
  - `conf_id`: `int | None`
    > the conformer id
  - `opts`: `Any`
    > extra writer options
  - `:returns`: `str`
    > the file path or XYZ string


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_molblock" class="docs-object-method">&nbsp;</a> 
```python
to_molblock(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4495)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4495?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the molecule to an MDL molblock (returned as a string, or written to a
file).
  - `filename`: `str | None`
    > the output file path (or `None` to return a string)
  - `conf_id`: `int | None`
    > the conformer id
  - `opts`: `Any`
    > extra writer options
  - `:returns`: `str`
    > the file path or molblock string


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_mrv" class="docs-object-method">&nbsp;</a> 
```python
to_mrv(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4521)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4521?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the molecule to Marvin MRV (returned as a string, or written to a
file).
  - `filename`: `str | None`
    > the output file path (or `None` to return a string)
  - `conf_id`: `int | None`
    > the conformer id
  - `opts`: `Any`
    > extra writer options
  - `:returns`: `str`
    > the file path or MRV string


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_pdb" class="docs-object-method">&nbsp;</a> 
```python
to_pdb(self, filename=None, conf_id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4547)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4547?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the molecule to PDB (returned as a string, or written to a file).
  - `filename`: `str | None`
    > the output file path (or `None` to return a string)
  - `conf_id`: `int | None`
    > the conformer id
  - `opts`: `Any`
    > extra writer options
  - `:returns`: `str`
    > the file path or PDB string


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_cml" class="docs-object-method">&nbsp;</a> 
```python
to_cml(self, filename=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4572)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4572?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the molecule to CML (returned as a string, or written to a file).
  - `filename`: `str | None`
    > the output file path (or `None` to return a string)
  - `opts`: `Any`
    > extra writer options
  - `:returns`: `str`
    > the file path or CML string


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.to_sdf" class="docs-object-method">&nbsp;</a> 
```python
to_sdf(self, filename=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4632)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4632?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the molecule to SDF (returned as a string, or written to a file).
  - `filename`: `str | None`
    > the output file path (or `None` to return a string)
  - `opts`: `Any`
    > extra writer options (e.g. `conf_ids`)
  - `:returns`: `str`
    > the file path or SDF string


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.allchem_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
allchem_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4651)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4651?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the RDKit `Chem.AllChem` submodule.
  - `:returns`: `module`
    > the `AllChem` module


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_force_field_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_force_field_type(cls, ff_type): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4662)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4662?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a force-field name to the RDKit `(force_field_getter, property_generator)`
pair.
  - `ff_type`: `str | tuple`
    > the force-field name (`'mmff'`/`'uff'`) or an existing pair
  - `:returns`: `tuple`
    > the force-field getter (and property generator)


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_force_field" class="docs-object-method">&nbsp;</a> 
```python
get_force_field(self, force_field_type='mmff', conf=None, mol=None, conf_id=None, **extra_props): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4687)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4687?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an RDKit force-field object for a conformer, computing any needed
force-field properties.
  - `force_field_type`: `str | tuple`
    > the force-field name or getter pair
  - `conf`: `Any`
    > an explicit conformer
  - `mol`: `Any`
    > an explicit mol
  - `conf_id`: `int | None`
    > the conformer id
  - `extra_props`: `Any`
    > extra keyword arguments for the force-field getter
  - `:returns`: `object`
    > the force-field object


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.evaluate_charges" class="docs-object-method">&nbsp;</a> 
```python
evaluate_charges(self, coords, model='gasteiger'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4736)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4736?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the per-atom partial charges for a set of coordinates (currently only
the Gasteiger model).
  - `coords`: `np.ndarray`
    > the coordinates (used to set the conformer)
  - `model`: `str`
    > the charge model
  - `:returns`: `list[float]`
    > the partial charges


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_energy" class="docs-object-method">&nbsp;</a> 
```python
calculate_energy(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4761)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4761?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the force-field energy of the current geometry, or of each geometry in a
batch.
  - `geoms`: `np.ndarray | None`
    > a batch of geometries (or `None` for the current one)
  - `force_field_generator`: `Callable | None`
    > a force-field factory (defaults to `get_force_field`)
  - `force_field_type`: `str`
    > the force-field name
  - `conf_id`: `int | None`
    > the conformer id
  - `:returns`: `float | np.ndarray`
    > the energy (or array of energies)


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_gradient" class="docs-object-method">&nbsp;</a> 
```python
calculate_gradient(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4807)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4807?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the force-field energy gradient of the current geometry, or of each
geometry in a batch.
  - `geoms`: `np.ndarray | None`
    > a batch of geometries (or `None` for the current one)
  - `force_field_generator`: `Callable | None`
    > a force-field factory (defaults to `get_force_field`)
  - `force_field_type`: `str`
    > the force-field name
  - `conf_id`: `int | None`
    > the conformer id
  - `:returns`: `np.ndarray`
    > the gradient (or batch of gradients)


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.calculate_hessian" class="docs-object-method">&nbsp;</a> 
```python
calculate_hessian(self, force_field_generator=None, force_field_type='mmff', stencil=5, mesh_spacing=0.01, **fd_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4854)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4854?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the force-field Hessian at the current geometry by finite-differencing
the analytic gradient.
  - `force_field_generator`: `Callable | None`
    > a force-field factory
  - `force_field_type`: `str`
    > the force-field name
  - `stencil`: `int`
    > the finite-difference stencil size
  - `mesh_spacing`: `float`
    > the finite-difference step
  - `fd_opts`: `Any`
    > extra finite-difference options
  - `:returns`: `np.ndarray`
    > the Hessian tensor


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.get_optimizer_params" class="docs-object-method">&nbsp;</a> 
```python
get_optimizer_params(self, maxAttempts=1000, useExpTorsionAnglePrefs=True, useBasicKnowledge=True, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4908)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4908?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an RDKit ETKDGv3 parameter object for structure optimization/embedding.
  - `maxAttempts`: `int`
    > the maximum embedding attempts
  - `useExpTorsionAnglePrefs`: `bool`
    > use experimental torsion prefs
  - `useBasicKnowledge`: `bool`
    > use basic chemical knowledge
  - `etc`: `Any`
    > extra parameters set on the params object
  - `:returns`: `object`
    > the parameter object


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.optimize_structure" class="docs-object-method">&nbsp;</a> 
```python
optimize_structure(self, geoms=None, force_field_type='mmff', optimizer=None, maxIters=1000, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4935)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4935?message=Update%20Docs)]
</div>
**LLM Docstring**

Force-field optimize the current geometry, or each geometry in a batch, returning
the optimizer status and optimized coordinates.
  - `geoms`: `np.ndarray | None`
    > a batch of geometries (or `None` for the current one)
  - `force_field_type`: `str`
    > the force-field name
  - `optimizer`: `Callable | None`
    > a custom optimizer callable
  - `maxIters`: `int`
    > the maximum optimization iterations
  - `opts`: `Any`
    > extra optimizer options
  - `:returns`: `tuple`
    > `(status, optimized_coords, extra)`


<a id="McUtils.ExternalPrograms.RDKit.RDMolecule.show" class="docs-object-method">&nbsp;</a> 
```python
show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4993)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit/RDMolecule.py#L4993?message=Update%20Docs)]
</div>
**LLM Docstring**

Display an interactive 3D rendering of the current conformer (via RDKit's
IPython 3D console).
  - `:returns`: `object`
    > the 3D display
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/RDKit.py#L19?message=Update%20Docs)   
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