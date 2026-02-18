## <a id="McUtils.Coordinerds.Internals.InternalSpec">InternalSpec</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L303)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L303?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Coordinerds.Internals.InternalSpec.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, coords, canonicalize=False, bond_graph=None, triangulation=None, masses=None, ungraphed_internals=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L304?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.atom_sets" class="docs-object-method">&nbsp;</a> 
```python
@property
atom_sets(self) -> 'Tuple[Tuple[int]]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L342)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L342?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self) -> 'Tuple[int]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L347)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L347?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_triangulation" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L353)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L353?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_bond_graph" class="docs-object-method">&nbsp;</a> 
```python
get_bond_graph(self) -> 'EdgeGraph': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L357)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L357?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_dropped_internal_bond_graph" class="docs-object-method">&nbsp;</a> 
```python
get_dropped_internal_bond_graph(self, internals): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L362)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L362?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_direct_derivatives" class="docs-object-method">&nbsp;</a> 
```python
get_direct_derivatives(self, coords, order=1, cache=True, reproject=False, base_transformation=None, reference_internals=None, combine_expansions=True, terms=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L400)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L400?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.orthogonalize_transformations" class="docs-object-method">&nbsp;</a> 
```python
orthogonalize_transformations(cls, expansion, inverse, coords=None, masses=None, order=None, remove_translation_rotations=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L431)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L431?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_expansion" class="docs-object-method">&nbsp;</a> 
```python
get_expansion(self, coords, order=1, return_inverse=False, remove_translation_rotations=True, orthogonalize=True, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L505)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L505?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L542)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L542?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_direct_inverses" class="docs-object-method">&nbsp;</a> 
```python
get_direct_inverses(self, coords, order=1, terms=None, combine_expansions=True, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L546)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L546?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L303?message=Update%20Docs)   
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