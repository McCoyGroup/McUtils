## <a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder">ConformerEncoder</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Conformers.py#L9)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers.py#L9?message=Update%20Docs)]
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
angle_distribution: dict
dihedral_distribution: dict
distribution_grid_size: int
```
<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.bond_encoder" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
bond_encoder(cls, bonds, byte_size, primary_bond_range=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L315)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L315?message=Update%20Docs)]
</div>
Encode a standalone bond-length stream.


<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.bond_decoder" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
bond_decoder(cls, encoded_bonds, byte_size, primary_bond_range=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L353)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L353?message=Update%20Docs)]
</div>
Decode a standalone encoded bond-length stream.


<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.angle_encoder" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
angle_encoder(cls, angles, byte_size, angle_range=None, pack_angles=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L394)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L394?message=Update%20Docs)]
</div>
Encode a standalone angle stream.

The first angle always uses the full integer width. Remaining
angles use either the full width or half width depending on
`pack_angles`.


<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.angle_decoder" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
angle_decoder(cls, encoded_angles, byte_size, angle_range=None, pack_angles=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L443)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L443?message=Update%20Docs)]
</div>
Decode a standalone angle stream.


<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.dihedral_encoder" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
dihedral_encoder(cls, dihedrals, byte_size, dihedral_range=None, pack_angles=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L488)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L488?message=Update%20Docs)]
</div>
Encode a standalone dihedral stream.


<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.dihedral_decoder" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
dihedral_decoder(cls, encoded_dihedrals, byte_size, dihedral_range=None, pack_angles=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L527)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L527?message=Update%20Docs)]
</div>
Decode a standalone dihedral stream.


<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.encode" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
encode(cls, flat_z, byte_size, primary_bond_range=None, angle_range=None, dihedral_range=None, pack_angles=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L613)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L613?message=Update%20Docs)]
</div>
Encode a flattened Z-matrix coordinate stream.


<a id="McUtils.ExternalPrograms.Conformers.ConformerEncoder.decode" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
decode(cls, buffer, byte_size, primary_bond_range=None, angle_range=None, dihedral_range=None, pack_angles=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L725)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L725?message=Update%20Docs)]
</div>
Decode a packed flattened Z-matrix coordinate stream.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers.py#L9?message=Update%20Docs)   
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