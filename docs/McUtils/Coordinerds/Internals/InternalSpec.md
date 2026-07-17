## <a id="McUtils.Coordinerds.Internals.InternalSpec">InternalSpec</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L834)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L834?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L835)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L835?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize a collection of coordinate specifications into `InternalCoordinateType` objects, optionally canonicalize and deduplicate them, collect the participating atoms, and initialize cached triangulations, bond graphs, masses, and conversion data.
  - `coords`: `Any`
    > Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
  - `canonicalize`: `Any`
    > Whether to put coordinates in canonical orientation before comparison or storage.
  - `bond_graph`: `Any`
    > Optional precomputed connectivity graph.
  - `triangulation`: `Any`
    > Optional precomputed triangle/dihedron representation.
  - `masses`: `Any`
    > Atomic masses used for mass weighting or rigid-body modes.
  - `ungraphed_internals`: `Any`
    > Coordinates that cannot be represented directly as edges in the bond graph and therefore require separate handling.
  - `distance_conversions`: `Any`
    > Precomputed recipes for reconstructing pair distances from the available internal coordinates.
  - `:returns`: `None`
    > None.


<a id="McUtils.Coordinerds.Internals.InternalSpec.from_zmatrix" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_zmatrix(cls, *zmats, additions=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L904)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L904?message=Update%20Docs)]
</div>
**LLM Docstring**

Create an `InternalSpec` from one or more Z-matrix index arrays by collecting each row’s distance, angle, and dihedral definitions, then appending any explicitly requested coordinates.
  - `additions`: `Any`
    > Additional coordinates to append to those extracted from the Z-matrix.
  - `zmats`: `Any`
    > One or more Z-matrix index arrays.
  - `opts`: `Any`
    > Additional options forwarded to the numerical conversion routine.
  - `:returns`: `Any`
    > The value or updated object described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.atom_sets" class="docs-object-method">&nbsp;</a> 
```python
@property
atom_sets(self) -> 'Tuple[Tuple[int]]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L930)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L930?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the defining atom tuple for every coordinate in the specification.
  - `:returns`: `Tuple[Tuple[int]]`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self) -> 'Tuple[int]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L943)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L943?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the sorted unique atom indices appearing in any coordinate.
  - `:returns`: `Tuple[int]`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_triangulation" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L957)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L957?message=Update%20Docs)]
</div>
**LLM Docstring**

Lazily derive and cache the triangle and dihedron sets that express the specification as connected distance geometry.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_pruned_rads" class="docs-object-method">&nbsp;</a> 
```python
get_pruned_rads(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L970)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L970?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the subset of primitive coordinates retained after removing redundancies implied by the triangulation.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_pruned_triangulation" class="docs-object-method">&nbsp;</a> 
```python
get_pruned_triangulation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L982)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L982?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a triangulation rebuilt from the nonredundant primitive coordinates.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_bond_graph" class="docs-object-method">&nbsp;</a> 
```python
get_bond_graph(self) -> 'EdgeGraph': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L995)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L995?message=Update%20Docs)]
</div>
**LLM Docstring**

Lazily construct an `EdgeGraph` whose edges are the bond distances represented by the coordinate set.
  - `:returns`: `EdgeGraph`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.graph" class="docs-object-method">&nbsp;</a> 
```python
@property
graph(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1009)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1009?message=Update%20Docs)]
</div>
**LLM Docstring**

Expose the cached or newly constructed bond graph for the specification.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_distance_conversions" class="docs-object-method">&nbsp;</a> 
```python
get_distance_conversions(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1022)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1022?message=Update%20Docs)]
</div>
**LLM Docstring**

Build and cache the conversion specification and callable that reconstruct all triangulation distances from the stored internal coordinates.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_zmat_conv" class="docs-object-method">&nbsp;</a> 
```python
get_zmat_conv(self, raise_on_incomplete=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1049)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1049?message=Update%20Docs)]
</div>
**LLM Docstring**

Find and cache a conversion from this coordinate set to a Z-matrix ordering. Optionally raise when no complete Z-matrix can be constructed.
  - `raise_on_incomplete`: `Any`
    > Whether failure to build a complete conversion raises instead of returning an incomplete result.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_dmat_conv" class="docs-object-method">&nbsp;</a> 
```python
get_dmat_conv(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1079)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1079?message=Update%20Docs)]
</div>
**LLM Docstring**

Build and cache a converter from internal-coordinate values to the condensed or square distance-matrix representation required by the triangulation.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_dropped_internal_bond_graph" class="docs-object-method">&nbsp;</a> 
```python
get_dropped_internal_bond_graph(self, internals, method=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1128?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a copy of the bond graph with the bonds implied by selected coordinates removed, using either direct coordinate decomposition or the requested removal method.
  - `internals`: `Any`
    > Available internal-coordinate specifications or their numerical values.
  - `method`: `Any`
    > Strategy used to remove coordinate-implied bonds.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_direct_derivatives" class="docs-object-method">&nbsp;</a> 
```python
get_direct_derivatives(self, coords, order=1, cache=True, reproject=False, base_transformation=None, reference_internals=None, combine_expansions=True, terms=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1218)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1218?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate direct Cartesian derivatives for every coordinate, pad them to the full atom set, and stack like derivative orders into coordinate-by-Cartesian tensors.
  - `coords`: `Any`
    > Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
  - `order`: `Any`
    > Highest derivative order to compute.
  - `cache`: `Any`
    > Optional mutable cache of triangulation or conversion results.
  - `reproject`: `Any`
    > Whether to project the orthogonalized transformations back into the original coordinate basis.
  - `base_transformation`: `Any`
    > Optional transformation used as the starting basis before orthogonalization.
  - `reference_internals`: `Any`
    > Reference internal-coordinate values used to select the periodic branch or initialize reconstruction.
  - `combine_expansions`: `Any`
    > Whether per-coordinate inverse derivatives are assembled into global tensors.
  - `terms`: `Any`
    > Triangle or dihedron conversion metadata to permute.
  - `opts`: `Any`
    > Additional options forwarded to the numerical conversion routine.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.orthogonalize_transformations" class="docs-object-method">&nbsp;</a> 
```python
orthogonalize_transformations(cls, expansion, inverse, coords=None, masses=None, order=None, remove_translation_rotations=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1275)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1275?message=Update%20Docs)]
</div>
**LLM Docstring**

Mass-weight and orthogonalize forward and inverse transformation matrices with an SVD-based pseudoinverse, optionally removing translational/rotational null modes and returning the retained singular subspace.
  - `expansion`: `Any`
    > Forward internal-to-Cartesian derivative tensors to orthogonalize.
  - `inverse`: `Any`
    > Inverse Cartesian-to-internal derivative tensors paired with `expansion`.
  - `coords`: `Any`
    > Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
  - `masses`: `Any`
    > Atomic masses used for mass weighting or rigid-body modes.
  - `order`: `Any`
    > Highest derivative order to compute.
  - `remove_translation_rotations`: `Any`
    > Whether rigid translations and rotations are removed from the retained Cartesian subspace.
  - `:returns`: `Any`
    > The value or updated object described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_expansion" class="docs-object-method">&nbsp;</a> 
```python
get_expansion(self, coords, order=1, return_inverse=False, remove_translation_rotations=True, orthogonalize=True, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1365)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1365?message=Update%20Docs)]
</div>
**LLM Docstring**

Assemble derivatives of the complete internal-coordinate vector with respect to Cartesian coordinates. It combines each coordinate’s expansion, optionally applies mass weighting or orthogonalization, and can return the associated inverse transformations.
  - `coords`: `Any`
    > Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
  - `order`: `Any`
    > Highest derivative order to compute.
  - `return_inverse`: `Any`
    > Whether to return inverse transformation data in addition to the primary result.
  - `remove_translation_rotations`: `Any`
    > Whether rigid translations and rotations are removed from the retained Cartesian subspace.
  - `orthogonalize`: `Any`
    > Whether to replace raw derivative transformations with an orthogonalized pair.
  - `opts`: `Any`
    > Additional options forwarded to the numerical conversion routine.
  - `:returns`: `List[np.ndarray]`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1436)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1436?message=Update%20Docs)]
</div>
**LLM Docstring**

Format the specification as the class name containing its normalized coordinate list.
  - `:returns`: `str`
    > A concise representation of the object.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_direct_inverses" class="docs-object-method">&nbsp;</a> 
```python
get_direct_inverses(self, coords, order=1, terms=None, combine_expansions=True, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1448)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1448?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate each coordinate’s inverse Cartesian expansion and combine the per-coordinate tensors into global inverse transformation derivatives when requested.
  - `coords`: `Any`
    > Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
  - `order`: `Any`
    > Highest derivative order to compute.
  - `terms`: `Any`
    > Triangle or dihedron conversion metadata to permute.
  - `combine_expansions`: `Any`
    > Whether per-coordinate inverse derivatives are assembled into global tensors.
  - `opts`: `Any`
    > Additional options forwarded to the numerical conversion routine.
  - `:returns`: `List[np.ndarray]`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.cartesians_to_internals" class="docs-object-method">&nbsp;</a> 
```python
cartesians_to_internals(self, coords, order=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1481)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1481?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate every stored coordinate on Cartesian geometries and optionally return its Cartesian derivative expansion.
  - `coords`: `Any`
    > Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
  - `order`: `Any`
    > Highest derivative order to compute.
  - `opts`: `Any`
    > Additional options forwarded to the numerical conversion routine.
  - `:returns`: `Any`
    > The value or updated object described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.internals_to_cartesians" class="docs-object-method">&nbsp;</a> 
```python
internals_to_cartesians(self, coords, order=None, reference_cartesians=None, return_fragments=False, return_inverse=True, transformations=None, reference_internals=None, use_distance_matrix_fallback=False, **deriv_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1504)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1504?message=Update%20Docs)]
</div>
**LLM Docstring**

Recover Cartesian geometries from internal values using either the cached Z-matrix route or distance-geometry route, applying reference coordinates, embedding options, and optional derivative information.
  - `coords`: `Any`
    > Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
  - `order`: `Any`
    > Highest derivative order to compute.
  - `reference_cartesians`: `Any`
    > Reference Cartesian geometry used to align or initialize reconstructed structures.
  - `return_fragments`: `Any`
    > Whether disconnected fragment geometries are returned separately instead of as one assembled structure.
  - `return_inverse`: `Any`
    > Whether to return inverse transformation data in addition to the primary result.
  - `transformations`: `Any`
    > Optional precomputed coordinate transformations used during reconstruction.
  - `reference_internals`: `Any`
    > Reference internal-coordinate values used to select the periodic branch or initialize reconstruction.
  - `use_distance_matrix_fallback`: `Any`
    > Whether to fall back to distance-matrix embedding when a direct Z-matrix conversion is unavailable.
  - `deriv_opts`: `Any`
    > Options forwarded specifically to derivative and inverse-expansion calculations.
  - `:returns`: `Any`
    > The value or updated object described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_triangulation_novel_internals" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation_novel_internals(self, rads=None, triangulation=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1746)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1746?message=Update%20Docs)]
</div>
**LLM Docstring**

Return coordinates that contribute distances not already represented by a triangulation, together with the corresponding novel distance pairs.
  - `rads`: `Any`
    > Primitive coordinate subset to analyze.
  - `triangulation`: `Any`
    > Optional precomputed triangle/dihedron representation.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.get_triangulation_distances" class="docs-object-method">&nbsp;</a> 
```python
get_triangulation_distances(self, rads=None, triangulation=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1799)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1799?message=Update%20Docs)]
</div>
**LLM Docstring**

Collect and deduplicate all pair distances required by the triangulation and optionally by an explicit coordinate subset.
  - `rads`: `Any`
    > Primitive coordinate subset to analyze.
  - `triangulation`: `Any`
    > Optional precomputed triangle/dihedron representation.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalSpec.check_redundancy" class="docs-object-method">&nbsp;</a> 
```python
check_redundancy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1823)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalSpec.py#L1823?message=Update%20Docs)]
</div>
**LLM Docstring**

Check whether the coordinate set contains more independent constraints than its atom count permits, using the triangulation rigidity test.
  - `:returns`: `Any`
    > The value or updated object described above.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L834?message=Update%20Docs)   
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