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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L404)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L404?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.atom_sets" class="docs-object-method">&nbsp;</a> 
```python
@property
atom_sets(self) -> 'Tuple[Tuple[int]]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L416)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L416?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self) -> 'Tuple[int]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L421)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L421?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_triangulation" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L427)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L427?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_pruned_rads" class="docs-object-method">&nbsp;</a> 
```python
get_pruned_rads(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L432)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L432?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_pruned_triangulation" class="docs-object-method">&nbsp;</a> 
```python
get_pruned_triangulation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L436)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L436?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_bond_graph" class="docs-object-method">&nbsp;</a> 
```python
get_bond_graph(self) -> 'EdgeGraph': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L441)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L441?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_distance_conversions" class="docs-object-method">&nbsp;</a> 
```python
get_distance_conversions(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L447)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L447?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_zmat_conv" class="docs-object-method">&nbsp;</a> 
```python
get_zmat_conv(self, raise_on_incomplete=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L465)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L465?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_dmat_conv" class="docs-object-method">&nbsp;</a> 
```python
get_dmat_conv(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L483)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L483?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_dropped_internal_bond_graph" class="docs-object-method">&nbsp;</a> 
```python
get_dropped_internal_bond_graph(self, internals, method=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L514)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L514?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_direct_derivatives" class="docs-object-method">&nbsp;</a> 
```python
get_direct_derivatives(self, coords, order=1, cache=True, reproject=False, base_transformation=None, reference_internals=None, combine_expansions=True, terms=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L592)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L592?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.orthogonalize_transformations" class="docs-object-method">&nbsp;</a> 
```python
orthogonalize_transformations(cls, expansion, inverse, coords=None, masses=None, order=None, remove_translation_rotations=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L623)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L623?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_expansion" class="docs-object-method">&nbsp;</a> 
```python
get_expansion(self, coords, order=1, return_inverse=False, remove_translation_rotations=True, orthogonalize=True, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L697)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L697?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L748)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L748?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_direct_inverses" class="docs-object-method">&nbsp;</a> 
```python
get_direct_inverses(self, coords, order=1, terms=None, combine_expansions=True, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L752)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L752?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.cartesians_to_internals" class="docs-object-method">&nbsp;</a> 
```python
cartesians_to_internals(self, coords, order=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L767)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L767?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.internals_to_cartesians" class="docs-object-method">&nbsp;</a> 
```python
internals_to_cartesians(self, coords, order=None, reference_cartesians=None, return_fragments=False, return_inverse=True, transformations=None, reference_internals=None, **deriv_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L776)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L776?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_triangulation_novel_internals" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation_novel_internals(self, rads=None, triangulation=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L945)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L945?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_triangulation_distances" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation_distances(self, rads=None, triangulation=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L972)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L972?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.check_redundancy" class="docs-object-method">&nbsp;</a> 
```python
check_redundancy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L984)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L984?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.non_redundant_rads" class="docs-object-method">&nbsp;</a> 
```python
non_redundant_rads(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L990)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L990?message=Update%20Docs)]
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