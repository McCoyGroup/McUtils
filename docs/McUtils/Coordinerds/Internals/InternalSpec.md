## <a id="McUtils.Coordinerds.Internals.InternalSpec">InternalSpec</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L327)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L327?message=Update%20Docs)]
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
__init__(self, coords, canonicalize=False, bond_graph=None, triangulation=None, masses=None, ungraphed_internals=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L328)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L328?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.from_zmatrix" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_zmatrix(cls, zmat, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L365)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L365?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.atom_sets" class="docs-object-method">&nbsp;</a> 
```python
@property
atom_sets(self) -> 'Tuple[Tuple[int]]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L373)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L373?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self) -> 'Tuple[int]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L378)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L378?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_triangulation" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L384)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L384?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_bond_graph" class="docs-object-method">&nbsp;</a> 
```python
get_bond_graph(self) -> 'EdgeGraph': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L388)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L388?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_dropped_internal_bond_graph" class="docs-object-method">&nbsp;</a> 
```python
get_dropped_internal_bond_graph(self, internals, method=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L394)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L394?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_direct_derivatives" class="docs-object-method">&nbsp;</a> 
```python
get_direct_derivatives(self, coords, order=1, cache=True, reproject=False, base_transformation=None, reference_internals=None, combine_expansions=True, terms=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L472)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L472?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.orthogonalize_transformations" class="docs-object-method">&nbsp;</a> 
```python
orthogonalize_transformations(cls, expansion, inverse, coords=None, masses=None, order=None, remove_translation_rotations=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L503)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L503?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_expansion" class="docs-object-method">&nbsp;</a> 
```python
get_expansion(self, coords, order=1, return_inverse=False, remove_translation_rotations=True, orthogonalize=True, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L577)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L577?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L628)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L628?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_direct_inverses" class="docs-object-method">&nbsp;</a> 
```python
get_direct_inverses(self, coords, order=1, terms=None, combine_expansions=True, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L632)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L632?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L327?message=Update%20Docs)   
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