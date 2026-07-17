## <a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule">OBMolecule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel.py#L17)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel.py#L17?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel.py#L22)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel.py#L22?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap an OpenBabel `OBMol` as an `OBMolecule`.
  - `obmol`: `Any`
    > the OpenBabel mol
  - `charge`: `int | None`
    > the molecular charge


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.pbmol" class="docs-object-method">&nbsp;</a> 
```python
@property
pbmol(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L36)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L36?message=Update%20Docs)]
</div>
**LLM Docstring**

The Pybel wrapper around the underlying `OBMol` (built lazily).
  - `:returns`: `object`
    > the Pybel molecule


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.get_api" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_api(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L51)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L51?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the OpenBabel API interface.
  - `:returns`: `OpenBabelInterface`
    > the OpenBabel interface


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L62)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L62?message=Update%20Docs)]
</div>
**LLM Docstring**

The atomic numbers of the atoms, in order.
  - `:returns`: `list[int]`
    > the atomic numbers


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.bonds" class="docs-object-method">&nbsp;</a> 
```python
@property
bonds(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L74)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L74?message=Update%20Docs)]
</div>
**LLM Docstring**

The bonds as `[begin_atom, end_atom, order]` triples (0-indexed atoms).
  - `:returns`: `list[list]`
    > the bond list


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L89)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L89?message=Update%20Docs)]
</div>
**LLM Docstring**

The atomic Cartesian coordinates. Setting this writes new positions onto the
atoms.
  - `:returns`: `np.ndarray`
    > the coordinates


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.set_coords" class="docs-object-method">&nbsp;</a> 
```python
set_coords(self, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L105?message=Update%20Docs)]
</div>
**LLM Docstring**

Write new Cartesian coordinates onto the molecule's atoms.
  - `coords`: `np.ndarray`
    > the new coordinates


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.atom_iter" class="docs-object-method">&nbsp;</a> 
```python
atom_iter(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L131)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L131?message=Update%20Docs)]
</div>
**LLM Docstring**

Return an iterator over the molecule's OpenBabel atoms.
  - `:returns`: `Iterator`
    > the atom iterator


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_obmol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_obmol(cls, obmol, charge=None, guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L143)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L143?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap an `OBMol` as an `OBMolecule`, optionally perceiving connectivity and bond
orders from the geometry.
  - `obmol`: `Any`
    > the OpenBabel mol
  - `charge`: `int | None`
    > the molecular charge
  - `guess_bonds`: `bool`
    > perceive bonds/orders from geometry
  - `:returns`: `OBMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.get_obmol_from_conversion" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_obmol_from_conversion(cls, data, fmt=None, add_implicit_hydrogens=False, target_fmt='mol2'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L164?message=Update%20Docs)]
</div>
**LLM Docstring**

Read an `OBMol` from a string by converting from the input format to an
intermediate format via OpenBabel's converter.
  - `data`: `str`
    > the input molecule string
  - `fmt`: `str | None`
    > the input format (e.g. `'smi'`)
  - `add_implicit_hydrogens`: `bool`
    > add hydrogens after reading
  - `target_fmt`: `str`
    > the intermediate conversion format
  - `:returns`: `_`
    > the OpenBabel mol


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.get_obmol_from_gen3d" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_obmol_from_gen3d(cls, data, fmt=None, add_implicit_hydrogens=False, method='gen3D', target='best'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L192)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L192?message=Update%20Docs)]
</div>
**LLM Docstring**

Read an `OBMol` from a string and generate a 3D structure for it via OpenBabel's
`gen3D` operation.
  - `data`: `str`
    > the input molecule string
  - `fmt`: `str | None`
    > the input format
  - `add_implicit_hydrogens`: `bool`
    > add hydrogens after reading
  - `method`: `str`
    > the 3D-generation operation name
  - `target`: `str | None`
    > the gen3D quality target (e.g. `'best'`)
  - `:returns`: `_`
    > the OpenBabel mol


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_string" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_string(cls, data, fmt=None, conformer_generator=None, add_implicit_hydrogens=False, charge=None, guess_bonds=False, **confgen_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L228)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L228?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `OBMolecule` from a molecule string, choosing between plain conversion
and 3D generation (defaulting to `gen3d` for SMILES input).
  - `data`: `str`
    > the input molecule string
  - `fmt`: `str | None`
    > the input format
  - `conformer_generator`: `str | None`
    > `'convert'` or `'gen3d'` (auto-chosen if omitted)
  - `add_implicit_hydrogens`: `bool`
    > add hydrogens after reading
  - `charge`: `int | None`
    > the molecular charge
  - `guess_bonds`: `bool`
    > perceive bonds/orders from geometry
  - `confgen_opts`: `Any`
    > extra options for the chosen reader
  - `:returns`: `OBMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_file" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_file(cls, file, fmt=None, target_fmt='mol2', add_implicit_hydrogens=False, charge=None, guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L269)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L269?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `OBMolecule` from a file, inferring the format from the extension when
not given.
  - `file`: `str`
    > the input file path
  - `fmt`: `str | None`
    > the input format (inferred from the extension if omitted)
  - `target_fmt`: `str`
    > the intermediate conversion format
  - `add_implicit_hydrogens`: `bool`
    > add hydrogens after reading
  - `charge`: `int | None`
    > the molecular charge
  - `guess_bonds`: `bool`
    > perceive bonds/orders from geometry
  - `:returns`: `OBMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.to_file" class="docs-object-method">&nbsp;</a> 
```python
to_file(self, file, fmt=None, base_fmt='mol2'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L307)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L307?message=Update%20Docs)]
</div>
**LLM Docstring**

Write the molecule to a file, inferring the output format from the extension
when not given.
  - `file`: `str`
    > the output file path
  - `fmt`: `str | None`
    > the output format (inferred from the extension if omitted)
  - `base_fmt`: `str`
    > the intermediate conversion format
  - `:returns`: `str`
    > the file path


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.to_string" class="docs-object-method">&nbsp;</a> 
```python
to_string(self, fmt, base_fmt='mol2'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L334)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L334?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the molecule to a string in the requested format.
  - `fmt`: `str`
    > the output format
  - `base_fmt`: `str`
    > the intermediate conversion format
  - `:returns`: `str`
    > the serialized molecule


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coords(cls, atoms, coords, bonds=None, add_implicit_hydrogens=False, charge=None, guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L353)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L353?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `OBMolecule` from atoms, coordinates, and (optional) bonds.
  - `atoms`: `Sequence[str]`
    > the element symbols
  - `coords`: `np.ndarray`
    > the Cartesian coordinates
  - `bonds`: `Sequence | None`
    > the bonds as `[i, j(, order)]` (0-indexed)
  - `add_implicit_hydrogens`: `bool`
    > unused flag
  - `charge`: `int | None`
    > the molecular charge
  - `guess_bonds`: `bool`
    > perceive bonds/orders from geometry
  - `:returns`: `OBMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, coord_unit='Angstroms', guess_bonds=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L397)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L397?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `OBMolecule` from a generic molecule object, converting its coordinates
to Angstroms.
  - `mol`: `Any`
    > the source molecule
  - `coord_unit`: `str`
    > the source coordinate unit
  - `guess_bonds`: `bool`
    > perceive bonds/orders from geometry
  - `:returns`: `OBMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L423)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L423?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a copy of this molecule (copying the underlying `OBMol` and charge).
  - `:returns`: `OBMolecule`
    > the copied molecule


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.remove_hydrogens" class="docs-object-method">&nbsp;</a> 
```python
remove_hydrogens(self, copy=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L438)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L438?message=Update%20Docs)]
</div>
**LLM Docstring**

Remove the molecule's hydrogens (on a copy by default).
  - `copy`: `bool`
    > operate on a copy rather than in place
  - `:returns`: `OBMolecule`
    > the molecule without hydrogens


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.make_2d" class="docs-object-method">&nbsp;</a> 
```python
make_2d(self, copy=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L453)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L453?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate a 2D depiction of the molecule (on a copy by default), falling back to
an inertial-frame projection when OpenBabel's 2D coordinates come out invalid.
  - `copy`: `bool`
    > operate on a copy rather than in place
  - `:returns`: `OBMolecule`
    > the 2D molecule


<a id="McUtils.ExternalPrograms.OpenBabel.OBMolecule.draw" class="docs-object-method">&nbsp;</a> 
```python
draw(self, fmt='svg', remove_hydrogens=True, plot_range=None, postdraw=None, scaling_factor=None, splits=None, include_save_buttons=False, use_smiles=False, use_coords=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L478)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel/OBMolecule.py#L478?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the molecule to an image (SVG/PNG), optionally from its SMILES or its own
(flattened) coordinates, with hydrogen removal and 2D-depiction generation.
  - `fmt`: `str`
    > the output image format
  - `remove_hydrogens`: `bool`
    > hide hydrogens
  - `plot_range`: `tuple | None`
    > a fixed drawing range
  - `postdraw`: `Callable | None`
    > a callback invoked after drawing
  - `scaling_factor`: `Any`
    > an image scaling factor
  - `splits`: `Any`
    > drawing element split metadata
  - `include_save_buttons`: `bool`
    > include save buttons in the output
  - `use_smiles`: `bool`
    > depict from the SMILES rather than the current structure
  - `use_coords`: `bool`
    > use the molecule's own coordinates (projected to 2D)
  - `:returns`: `DisplayImage`
    > the rendered image
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/OpenBabel.py#L17?message=Update%20Docs)   
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