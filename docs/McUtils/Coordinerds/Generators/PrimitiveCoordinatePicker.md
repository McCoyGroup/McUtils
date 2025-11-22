## <a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker">PrimitiveCoordinatePicker</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators.py#L104)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L104?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
light_atom_types: set
fused_ring_dispatch_table: dict
symmetry_type_dispatch: dict
```
<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, atoms, bonds, base_coords=None, rings=None, fragments=None, light_atoms=None, backbone=None, neighbor_count=3): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators.py#L107)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L107?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L128?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.generate_coords" class="docs-object-method">&nbsp;</a> 
```python
generate_coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L133)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L133?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.canonicalize_coord" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_coord(cls, coord): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L150)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L150?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.prep_unique_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_unique_coords(cls, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L170)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L170?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.prune_excess_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prune_excess_coords(cls, coord_set, canonicalized=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L181)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L181?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
ring_coordinates(cls, ring_atoms): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L209)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L209?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.unfused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
unfused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L237)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L237?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.pivot_fused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
pivot_fused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L240)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L240?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.simple_fused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
simple_fused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L258)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L258?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.fused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fused_ring_coordinates(cls, ring_atoms1, ring_atoms2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L277)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L277?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.fragment_connection_coords" class="docs-object-method">&nbsp;</a> 
```python
fragment_connection_coords(self, frag_1, frag_2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L289)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L289?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.get_neighborhood_symmetries" class="docs-object-method">&nbsp;</a> 
```python
get_neighborhood_symmetries(self, atoms, ignored=None, neighborhood=3): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L312)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L312?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.chain_coords" class="docs-object-method">&nbsp;</a> 
```python
chain_coords(self, R, y): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L320)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L320?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.RYX2_coords" class="docs-object-method">&nbsp;</a> 
```python
RYX2_coords(self, R, y, X): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L330)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L330?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.RYX3_coords" class="docs-object-method">&nbsp;</a> 
```python
RYX3_coords(self, R, y, X): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L357)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L357?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.get_precedent_chains" class="docs-object-method">&nbsp;</a> 
```python
get_precedent_chains(self, atom, num_precs=2, ring_atoms=None, light_atoms=None, ignored=None, backbone=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L383)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L383?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.get_symmetry_groups" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_symmetry_groups(cls, neighbors, matches): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L469)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L469?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.symmetry_coords" class="docs-object-method">&nbsp;</a> 
```python
symmetry_coords(self, atom, neighborhood=3, backbone=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L490)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L490?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L104?message=Update%20Docs)   
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