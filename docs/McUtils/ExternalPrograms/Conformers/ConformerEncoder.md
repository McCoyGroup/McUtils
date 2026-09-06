## <a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder">ConformerEncoder</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Conformers.py#L523)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers.py#L523?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
compressed_bond_range: tuple
compressed_angle_range: tuple
compressed_dihedral_range: tuple
```
<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, byte_size=None, bond_encoder=None, angle_encoder=None, dihedral_encoder=None, stream_packer=None, primary_bond_range=None, angle_range=None, dihedral_range=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Conformers.py#L528)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers.py#L528?message=Update%20Docs)]
</div>
Parameters
----------
byte_size : int, optional
    Bit width (16/32/64) used to build whichever of the default
    encoders below aren't overridden, and to interpret buffers
    in `decode`. If omitted (None), it's resolved from the first
    supplied `bond_encoder` / `angle_encoder` / `dihedral_encoder`
    / `stream_packer` that exposes its own `.byte_size`. If none
    of those are supplied either, there's nothing to build the
    defaults from, so construction raises immediately rather
    than failing later with a confusing error. `decode` can
    still work even with `byte_size=None` here, by inferring bit
    width directly from a typed buffer at call time -- see
    `decode`.
... (see previous docstring for the rest of the parameters)


<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.encode" class="docs-object-method">&nbsp;</a> 
```python
encode(self, flat_z, pack_angles=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Conformers/ConformerEncoder.py#L609)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers/ConformerEncoder.py#L609?message=Update%20Docs)]
</div>
Encode a flattened Z-matrix coordinate stream.


<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.decode" class="docs-object-method">&nbsp;</a> 
```python
decode(self, buffer, pack_angles=False, return_streams=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Conformers/ConformerEncoder.py#L675)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers/ConformerEncoder.py#L675?message=Update%20Docs)]
</div>
Decode a packed flattened Z-matrix coordinate stream.


<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.decode_from_data" class="docs-object-method">&nbsp;</a> 
```python
decode_from_data(self, encoded_bonds, encoded_angles, encoded_dihedrals, pack_angles=False, return_streams=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Conformers/ConformerEncoder.py#L696)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers/ConformerEncoder.py#L696?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.from_distributions" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_distributions(cls, byte_size, angle_distribution=None, dihedral_distribution=None, primary_bond_range=None, angle_range=None, dihedral_range=None, bond_encoder=None, stream_packer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L721)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L721?message=Update%20Docs)]
</div>
Build a ConformerEncoder whose angle and/or dihedral encoders use
distributions loaded from saved PPF-grid files -- i.e. `.npz`
files written by `MixtureDistribution.save_ppf_grid` (after
fitting a `FittedMixtureDistribution` via `fit_mixture`) -- rather
than the plain uniform-on-range default.

Parameters
----------
angle_ppf_path, dihedral_ppf_path : str or os.PathLike, optional
    Paths to `.npz` PPF-grid files. Loaded via
    `MixtureDistribution.load_ppf_grid`, which reconstructs the
    distribution's kernels/params/weights plus its precomputed
    PPF lookup -- no re-fitting needed at load time. If either
    is omitted, that encoder falls back to the usual
    uniform-distribution default (`distribution=None`), exactly
    like the plain constructor.
bond_encoder : object, optional
    Bonds aren't periodic and don't currently have a saved-file
    path here -- pass a pre-built encoder directly if you want a
    non-uniform bond distribution; otherwise the usual uniform
    default is used.
(all other parameters as in `__init__`)

Returns
-------
ConformerEncoder
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Conformers/ConformerEncoder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Conformers/ConformerEncoder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Conformers/ConformerEncoder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Conformers/ConformerEncoder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers.py#L523?message=Update%20Docs)   
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