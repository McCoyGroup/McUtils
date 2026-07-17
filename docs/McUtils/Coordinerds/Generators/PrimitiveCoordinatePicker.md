## <a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker">PrimitiveCoordinatePicker</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators.py#L249)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L249?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators.py#L252)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L252?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize a primitive-coordinate picker from atom labels and molecular connectivity.

The constructor builds an `EdgeGraph`, discovers rings and connected fragments when they are not supplied, records the ring containing each ring atom, identifies light atoms from `light_atom_types` unless explicitly provided, and stores base coordinates and neighborhood depth. Coordinate generation is deferred until the `coords` property is accessed.
  - `atoms`: `collections.abc.Sequence`
    > Atom labels passed to `EdgeGraph`.
  - `bonds`: `collections.abc.Iterable[tuple[int, int]]`
    > Graph edges passed to `EdgeGraph`.
  - `base_coords`: `collections.abc.Iterable[tuple[int, ...]] | None`
    > Coordinates prepended to the automatically generated set.
  - `rings`: `collections.abc.Sequence | None`
    > Ordered atom-index cycles; discovered from the graph when omitted.
  - `fragments`: `collections.abc.Sequence | None`
    > Connected atom-index groups; discovered from the graph when omitted.
  - `light_atoms`: `collections.abc.Sequence[int] | None`
    > Explicit light-atom indices. Defaults to graph labels matching `light_atom_types`.
  - `backbone`: `collections.abc.Collection[int] | None`
    > Optional preferred backbone passed to chain searches.
  - `neighbor_count`: `int`
    > Neighborhood depth supplied to symmetry-coordinate generation.
  - `:returns`: `None`
    > None.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L299)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L299?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the cached primitive coordinate set, generating it on first access.

The first call evaluates `generate_coords`, materializes its result as a tuple, and stores it in `_coords`; later calls return the same tuple without regenerating coordinates.
  - `:returns`: `tuple[tuple[int, ...], ...]`
    > Cached primitive internal-coordinate specifications.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.generate_coords" class="docs-object-method">&nbsp;</a> 
```python
generate_coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L314)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L314?message=Update%20Docs)]
</div>
**LLM Docstring**

Assemble primitive coordinates for rings, fused rings, fragment connections, and non-ring atoms.

Ring-local bonds, angles, and dihedrals are generated first. Additional coordinates connect every pair of rings and every pair of fragments. For atoms not belonging to any ring, chain-based coordinates are generated from precedent paths. User-supplied base coordinates are prepended, then the combined list is canonicalized and pruned by `prune_excess_coords`.
  - `:returns`: `list[tuple[int, ...]]`
    > Canonicalized primitive coordinate list with duplicate and selected overcomplete coordinates removed.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.canonicalize_coord" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_coord(cls, coord): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L341)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L341?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize an internal coordinate so reversal-equivalent tuples have one orientation.

Coordinates containing a repeated atom are rejected with `None`. Bonds are ordered by ascending endpoints; angles place the smaller endpoint first; dihedrals are reversed when the first atom exceeds the last; longer tuples use the same endpoint comparison and full reversal.
  - `coord`: `collections.abc.Sequence[int]`
    > Internal coordinate atom-index sequence.
  - `:returns`: `tuple[int, ...] | None`
    > Canonical tuple, or `None` when an atom index is repeated.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.prep_unique_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_unique_coords(cls, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L373)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L373?message=Update%20Docs)]
</div>
**LLM Docstring**

Canonicalize coordinates and identify first occurrences, but currently return the original input.

The method builds `_coords` and `_cache` containing unique canonical coordinates. Those local results are never used in the return statement; as implemented, callers receive `coords` unchanged. This appears inconsistent with the method name and is documented rather than corrected here.
  - `coords`: `collections.abc.Iterable`
    > Coordinate iterable to inspect.
  - `:returns`: `collections.abc.Iterable`
    > The original `coords` object, unchanged.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.prune_excess_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prune_excess_coords(cls, coord_set, canonicalized=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L396)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L396?message=Update%20Docs)]
</div>
**LLM Docstring**

Canonicalize a coordinate set and remove duplicates plus selected redundant angle/dihedral orderings.

Repeated-atom coordinates are discarded. Exact duplicate tuples are skipped. For four-atom coordinates, only one ordering around a shared central bond is kept when the alternate `(i, k, j, l)` has already appeared. For three-atom coordinates, explicit index-order tests suppress configurations that would retain all three angles among the same atom triple.
  - `coord_set`: `collections.abc.Iterable[collections.abc.Sequence[int]]`
    > Candidate internal coordinates.
  - `canonicalized`: `bool`
    > Whether every input has already been normalized by `canonicalize_coord`.
  - `:returns`: `list[tuple[int, ...]]`
    > Coordinates retained in first-occurrence order.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
ring_coordinates(cls, ring_atoms): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L438)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L438?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate cyclic bonds, angles, and dihedrals around an ordered ring.

The atom list is wrapped at the end. Each atom starts one adjacent bond, one three-consecutive-atom angle, and one four-consecutive-atom dihedral, so a ring of size `n` contributes `3n` coordinates before later pruning.
  - `ring_atoms`: `list[int]`
    > Atom indices ordered consecutively around the ring.
  - `:returns`: `list[tuple[int, ...]]`
    > Ring bonds followed by ring angles and ring dihedrals.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.unfused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
unfused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L488)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L488?message=Update%20Docs)]
</div>
**LLM Docstring**

Return no additional coordinates for two rings that share no atoms.

All arguments are accepted to match the fused-ring dispatch signature and are otherwise unused.
  - `ring_atoms1`: `collections.abc.Sequence[int]`
    > First ring's ordered atoms.
  - `ring_atoms2`: `collections.abc.Sequence[int]`
    > Second ring's ordered atoms.
  - `shared_atoms`: `collections.abc.Sequence[int]`
    > Empty shared-atom collection.
  - `shared_indices1`: `collections.abc.Sequence[int]`
    > Shared positions in the first ring.
  - `shared_indices2`: `collections.abc.Sequence[int]`
    > Shared positions in the second ring.
  - `:returns`: `list`
    > Empty coordinate list.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.pivot_fused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
pivot_fused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L511)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L511?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate four cross-ring angles for rings fused at a single pivot atom.

For each ring, the atoms immediately before and after the shared pivot are found with cyclic indexing. The Cartesian product of those two neighbor pairs gives four angles centered on the pivot, describing the relative directions of the rings.
  - `ring_atoms1`: `collections.abc.Sequence[int]`
    > First ring in cyclic order.
  - `ring_atoms2`: `collections.abc.Sequence[int]`
    > Second ring in cyclic order.
  - `shared_atoms`: `collections.abc.Sequence[int]`
    > One-element sequence containing the pivot atom.
  - `shared_indices1`: `collections.abc.Sequence[int]`
    > Pivot position in the first ring.
  - `shared_indices2`: `collections.abc.Sequence[int]`
    > Pivot position in the second ring.
  - `:returns`: `list[tuple[int, int, int]]`
    > Four cross-ring angle triples centered on the shared atom.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.simple_fused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
simple_fused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L549)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L549?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate two cross-ring dihedrals for rings sharing one bond.

The two shared atoms define the central bond. For each ring, the atom preceding the first shared position and the atom following the second are found after ordering the shared positions. Two dihedrals are returned, each using an exterior atom from one ring and an exterior atom from the other.
  - `ring_atoms1`: `collections.abc.Sequence[int]`
    > First ring in cyclic order.
  - `ring_atoms2`: `collections.abc.Sequence[int]`
    > Second ring in cyclic order.
  - `shared_atoms`: `collections.abc.Sequence[int]`
    > The two atoms forming the fused bond.
  - `shared_indices1`: `collections.abc.Sequence[int]`
    > Positions of the shared atoms in the first ring.
  - `shared_indices2`: `collections.abc.Sequence[int]`
    > Positions of the shared atoms in the second ring.
  - `:returns`: `list[tuple[int, int, int, int]]`
    > Two dihedrals spanning the fused bond and both ring exteriors.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.fused_ring_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fused_ring_coordinates(cls, ring_atoms1, ring_atoms2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L588)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L588?message=Update%20Docs)]
</div>
**LLM Docstring**

Dispatch fused-ring coordinate generation according to the number of shared atoms.

The intersection of the two ordered ring lists is computed together with each ring's shared positions. Disjoint rings return no coordinates. One- and two-atom fusions use the registered handlers; any unsupported shared-atom count raises an error.
  - `ring_atoms1`: `collections.abc.Sequence[int]`
    > First ring's ordered atom indices.
  - `ring_atoms2`: `collections.abc.Sequence[int]`
    > Second ring's ordered atom indices.
  - `:returns`: `list[tuple[int, ...]]`
    > Additional angles or dihedrals describing the rings' relative orientation.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.fragment_connection_coords" class="docs-object-method">&nbsp;</a> 
```python
fragment_connection_coords(self, frag_1, frag_2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L615)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L615?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct up to six primitive coordinates connecting two disconnected fragments.

When a fragment contains more than two heavy atoms, light atoms are removed and the remaining indices are sorted; otherwise its original ordering is retained. The first atoms define an inter-fragment stretch. Available second and third atoms add two orientation angles and up to three dihedrals, yielding the standard distance/orientation coordinate pattern for two fragments.
  - `frag_1`: `collections.abc.Sequence[int]`
    > Atom indices in the first fragment.
  - `frag_2`: `collections.abc.Sequence[int]`
    > Atom indices in the second fragment.
  - `:returns`: `list[tuple[int, ...]]`
    > Inter-fragment stretch, orientation angles, and available dihedrals.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.get_neighborhood_symmetries" class="docs-object-method">&nbsp;</a> 
```python
get_neighborhood_symmetries(self, atoms, ignored=None, neighborhood=3): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L652)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L652?message=Update%20Docs)]
</div>
**LLM Docstring**

Compare local neighbor graphs for every unordered pair of atoms.

A `neighbor_graph` of the requested depth is constructed for each atom, respecting `ignored`. The returned Boolean list follows upper-triangular pair order `(0,1), (0,2), ..., (n-2,n-1)` and records graph equality for each pair.
  - `atoms`: `collections.abc.Sequence[int]`
    > Atom indices whose neighborhoods are compared.
  - `ignored`: `collections.abc.Collection[int] | None`
    > Atom indices omitted while constructing each neighborhood graph.
  - `neighborhood`: `int`
    > Number of graph shells included in each neighborhood.
  - `:returns`: `list[bool]`
    > Pairwise neighborhood-equivalence flags in upper-triangular order.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.chain_coords" class="docs-object-method">&nbsp;</a> 
```python
chain_coords(self, R, y): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L676)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L676?message=Update%20Docs)]
</div>
**LLM Docstring**

Attach an atom to the tail of a precedent chain with one stretch, one angle, and one dihedral when possible.

For a nonempty chain `R`, the new atom `y` is bonded to `R[-1]`. The preceding one or two chain atoms extend that bond into an angle and dihedral respectively.
  - `R`: `collections.abc.Sequence[int]`
    > Precedent atom chain ordered from oldest to nearest atom.
  - `y`: `int`
    > Atom to attach to the chain.
  - `:returns`: `list[tuple[int, ...]]`
    > Zero to three coordinates ending at `y`.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.RYX2_coords" class="docs-object-method">&nbsp;</a> 
```python
RYX2_coords(self, R, y, X): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L700)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L700?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate coordinates for a center atom with a three-member neighbor group and an optional precedent chain.

The routine adds stretches from `y` to every atom in `X`, all three pairwise `X-y-X` angles, and—when `R` is present—the stretch and three angles joining the nearest precedent atom to `y`. Additional precedent atoms supply one `R-R-y` angle and one `R-R-R-y` dihedral. Despite the name, the implementation indexes the first three entries of `X` and therefore expects at least three neighbors.
  - `R`: `collections.abc.Sequence[int]`
    > Precedent chain ending at the atom nearest `y`.
  - `y`: `int`
    > Central atom.
  - `X`: `collections.abc.Sequence[int]`
    > Neighbor atoms; at least three entries are required by the pair-generation loop.
  - `:returns`: `list[tuple[int, ...]]`
    > Stretches, angles, and optional chain dihedral around `y`.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.RYX3_coords" class="docs-object-method">&nbsp;</a> 
```python
RYX3_coords(self, R, y, X): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L743)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L743?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate coordinates for a center atom with three neighbors and an optional precedent chain.

The implementation is identical to `RYX2_coords`: it creates three `y-X` stretches, the three pairwise `X-y-X` angles, and coordinates linking `y` to up to three atoms from `R`.
  - `R`: `collections.abc.Sequence[int]`
    > Precedent chain ending at the atom nearest `y`.
  - `y`: `int`
    > Central atom.
  - `X`: `collections.abc.Sequence[int]`
    > Three or more neighbor atom indices.
  - `:returns`: `list[tuple[int, ...]]`
    > Stretches, angles, and optional chain dihedral around `y`.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.get_precedent_chains" class="docs-object-method">&nbsp;</a> 
```python
get_precedent_chains(self, atom, num_precs=2, ring_atoms=None, light_atoms=None, ignored=None, backbone=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L785)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L785?message=Update%20Docs)]
</div>
**LLM Docstring**

Enumerate graph paths leading away from an atom up to a requested predecessor depth.

A depth-first search starts at `atom`, shares one global visited set across branches, and expands unvisited graph neighbors. Paths terminate at dead ends or after `num_precs` atoms have been collected. Each stored path is reversed before return so it runs from the farthest predecessor toward the atom. `ring_atoms`, `light_atoms`, and `backbone` are normalized but do not currently affect branch selection.
  - `atom`: `int`
    > Root atom from which predecessor paths are explored.
  - `num_precs`: `int`
    > Maximum number of predecessor atoms in each path.
  - `ring_atoms`: `collections.abc.Collection[int] | None`
    > Optional ring-atom set; currently not used after normalization.
  - `light_atoms`: `collections.abc.Collection[int] | None`
    > Optional light-atom set; currently not used after normalization.
  - `ignored`: `collections.abc.Collection[int] | None`
    > Atom indices considered visited before traversal.
  - `backbone`: `collections.abc.Collection[int] | None`
    > Optional backbone set; currently not used by the active traversal.
  - `:returns`: `list[list[int]]`
    > Predecessor chains ordered from farthest atom to nearest atom.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.get_symmetry_groups" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_symmetry_groups(cls, neighbors, matches): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L959)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L959?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert pairwise equality flags into groups of equivalent neighbors.

`matches` is consumed in upper-triangular pair order. Equal pairs share the same mutable index set, causing connected equality relationships to merge. Duplicate set objects are removed by identity, groups are sorted largest first, and index groups are translated back to neighbor atom indices.
  - `neighbors`: `collections.abc.Sequence[int]`
    > Neighbor atom indices in the order used to compute `matches`.
  - `matches`: `collections.abc.Sequence[bool]`
    > Equality flags for every unordered neighbor pair in upper-triangular order.
  - `:returns`: `list[list[int]]`
    > Neighbor groups ordered from largest to smallest.


<a id="McUtils.Coordinerds.Generators.PrimitiveCoordinatePicker.symmetry_coords" class="docs-object-method">&nbsp;</a> 
```python
symmetry_coords(self, atom, neighborhood=3, backbone=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L994)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators/PrimitiveCoordinatePicker.py#L994?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate chain-based coordinates for a non-ring atom.

The previously intended neighborhood-symmetry dispatch is currently commented out. The active code finds predecessor chains of length up to three from `atom`; for each chain, it adds the stretch, angle, and dihedral that connect `atom` to the chain tail. If no chain is found, an empty chain contributes no coordinates. `neighborhood` is therefore currently unused.
  - `atom`: `int`
    > Atom for which primitive coordinates are generated.
  - `neighborhood`: `int`
    > Reserved neighborhood depth; unused by the active implementation.
  - `backbone`: `collections.abc.Collection[int] | None`
    > Optional backbone forwarded to `get_precedent_chains`.
  - `:returns`: `list[tuple[int, ...]]`
    > Chain-derived coordinates ending at `atom`.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L249?message=Update%20Docs)   
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