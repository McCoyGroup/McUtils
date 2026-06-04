## <a id="McUtils.Coordinerds.Internals.InternalSpec">InternalSpec</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L358)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L358?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
graph_split_method: str
```
<a id="McUtils.Coordinerds.Internals.InternalSpec.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, coords, canonicalize=True, bond_graph=None, triangulation=None, masses=None, ungraphed_internals=None, distance_conversions=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L359)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L359?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.from_zmatrix" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_zmatrix(cls, *zmats, additions=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L406)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L406?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.atom_sets" class="docs-object-method">&nbsp;</a> 
```python
@property
atom_sets(self) -> 'Tuple[Tuple[int]]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L418)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L418?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self) -> 'Tuple[int]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L423)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L423?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_triangulation" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L429)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L429?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_pruned_rads" class="docs-object-method">&nbsp;</a> 
```python
get_pruned_rads(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L434)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L434?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_pruned_triangulation" class="docs-object-method">&nbsp;</a> 
```python
get_pruned_triangulation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L438)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L438?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_bond_graph" class="docs-object-method">&nbsp;</a> 
```python
get_bond_graph(self) -> 'EdgeGraph': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L443)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L443?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.graph" class="docs-object-method">&nbsp;</a> 
```python
@property
graph(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L449)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L449?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_distance_conversions" class="docs-object-method">&nbsp;</a> 
```python
get_distance_conversions(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L454)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L454?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_zmat_conv" class="docs-object-method">&nbsp;</a> 
```python
get_zmat_conv(self, raise_on_incomplete=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L473)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L473?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_dmat_conv" class="docs-object-method">&nbsp;</a> 
```python
get_dmat_conv(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L491)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L491?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_dropped_internal_bond_graph" class="docs-object-method">&nbsp;</a> 
```python
get_dropped_internal_bond_graph(self, internals, method=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L520)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L520?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_direct_derivatives" class="docs-object-method">&nbsp;</a> 
```python
get_direct_derivatives(self, coords, order=1, cache=True, reproject=False, base_transformation=None, reference_internals=None, combine_expansions=True, terms=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L598)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L598?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.orthogonalize_transformations" class="docs-object-method">&nbsp;</a> 
```python
orthogonalize_transformations(cls, expansion, inverse, coords=None, masses=None, order=None, remove_translation_rotations=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L629)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L629?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_expansion" class="docs-object-method">&nbsp;</a> 
```python
get_expansion(self, coords, order=1, return_inverse=False, remove_translation_rotations=True, orthogonalize=True, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L699)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L699?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L750)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L750?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_direct_inverses" class="docs-object-method">&nbsp;</a> 
```python
get_direct_inverses(self, coords, order=1, terms=None, combine_expansions=True, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L754)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L754?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.cartesians_to_internals" class="docs-object-method">&nbsp;</a> 
```python
cartesians_to_internals(self, coords, order=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L769)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L769?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.internals_to_cartesians" class="docs-object-method">&nbsp;</a> 
```python
internals_to_cartesians(self, coords, order=None, reference_cartesians=None, return_fragments=False, return_inverse=True, transformations=None, reference_internals=None, **deriv_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L778)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L778?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_triangulation_novel_internals" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation_novel_internals(self, rads=None, triangulation=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L980)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L980?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_triangulation_distances" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation_distances(self, rads=None, triangulation=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1007)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1007?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.check_redundancy" class="docs-object-method">&nbsp;</a> 
```python
check_redundancy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1019)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1019?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Internals/InternalSpec.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Internals/InternalSpec.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Internals/InternalSpec.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Internals/InternalSpec.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L358?message=Update%20Docs)   
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