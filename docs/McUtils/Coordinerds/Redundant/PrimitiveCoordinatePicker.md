## <a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker">PrimitiveCoordinatePicker</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant.py#L15?message=Update%20Docs)]
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
<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, atoms, bonds, base_coords=None, rings=None, fragments=None, light_atoms=None, backbone=None, neighbor_count=3): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L18)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L18?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L39)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L39?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.generate_coords" class="docs-object-method">&nbsp;</a> 
```python
generate_coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L44)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L44?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.canonicalize_coord" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_coord(cls, coord): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L61)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L61?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.prep_unique_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_unique_coords(cls, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L81)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L81?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.prune_excess_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prune_excess_coords(cls, coord_set, canonicalized=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L92)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L92?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
ring_coordinates(cls, ring_atoms): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L120)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L120?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.unfused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
unfused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L148)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L148?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.pivot_fused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
pivot_fused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L151)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L151?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.simple_fused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
simple_fused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L169?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.fused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fused_ring_coordinates(cls, ring_atoms1, ring_atoms2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L188?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.fragment_connection_coords" class="docs-object-method">&nbsp;</a> 
```python
fragment_connection_coords(self, frag_1, frag_2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L200)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L200?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.get_neighborhood_symmetries" class="docs-object-method">&nbsp;</a> 
```python
get_neighborhood_symmetries(self, atoms, ignored=None, neighborhood=3): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L223)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L223?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.chain_coords" class="docs-object-method">&nbsp;</a> 
```python
chain_coords(self, R, y): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L231)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L231?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.RYX2_coords" class="docs-object-method">&nbsp;</a> 
```python
RYX2_coords(self, R, y, X): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L241)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L241?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.RYX3_coords" class="docs-object-method">&nbsp;</a> 
```python
RYX3_coords(self, R, y, X): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L268)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L268?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.get_precedent_chains" class="docs-object-method">&nbsp;</a> 
```python
get_precedent_chains(self, atom, num_precs=2, ring_atoms=None, light_atoms=None, ignored=None, backbone=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L294)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L294?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.get_symmetry_groups" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_symmetry_groups(cls, neighbors, matches): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L380)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L380?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Coordinerds.Redundant.PrimitiveCoordinatePicker.symmetry_coords" class="docs-object-method">&nbsp;</a> 
```python
symmetry_coords(self, atom, neighborhood=3, backbone=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L401)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.py#L401?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Redundant/PrimitiveCoordinatePicker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant.py#L15?message=Update%20Docs)   
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