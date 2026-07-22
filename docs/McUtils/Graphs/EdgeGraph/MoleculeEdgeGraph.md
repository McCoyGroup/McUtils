## <a id="McUtils.Graphs.EdgeGraph.MoleculeEdgeGraph">MoleculeEdgeGraph</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph.py#L1720)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L1720?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
chemical_order: list
ring_type_dispatch: dict
functional_groups: dict
atom_identifier: atom_identifier
light_atoms: set
```
<a id="McUtils.Graphs.EdgeGraph.MoleculeEdgeGraph.get_rings" class="docs-object-method">&nbsp;</a> 
```python
get_rings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L1722)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L1722?message=Update%20Docs)]
</div>
**LLM Docstring**

Use RDKit cycle perception on a carbon-labeled graph with dummy coordinates.
  - `:returns`: `list`
    > A list of ordered ring vertex sequences.


<a id="McUtils.Graphs.EdgeGraph.MoleculeEdgeGraph.categorize_ring" class="docs-object-method">&nbsp;</a> 
```python
categorize_ring(self, ring): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2098)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2098?message=Update%20Docs)]
</div>
**LLM Docstring**

Match a ring and its external valencies against known ring templates, accounting for cyclic rotations.
  - `ring`: `object`
    > Ordered atom indices forming the ring to categorize.

  - `:returns`: `object`
    > A pair `(ring_category, ordered_ring_indices)`.


<a id="McUtils.Graphs.EdgeGraph.MoleculeEdgeGraph.match_functional_group" class="docs-object-method">&nbsp;</a> 
```python
match_functional_group(self, root, neighbor_lists, cache=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2160)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2160?message=Update%20Docs)]
</div>
**LLM Docstring**

Test a root atom’s nested neighbor pattern against known functional-group templates with optional caching.
  - `root`: `object`
    > Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.

  - `neighbor_lists`: `object`
    > Observed nested neighbor patterns.

  - `cache`: `object`
    > Optional dictionary caching functional-group matches.

  - `:returns`: `object`
    > A `(group_name, matched_pattern)` pair, or `None`.


<a id="McUtils.Graphs.EdgeGraph.MoleculeEdgeGraph.find_functional_groups" class="docs-object-method">&nbsp;</a> 
```python
find_functional_groups(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2201)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2201?message=Update%20Docs)]
</div>
**LLM Docstring**

Locate known functional groups and collect the atom indices consumed by each matched pattern.
  - `:returns`: `object`
    > A list of `[group_name, atom_indices]` records.


<a id="McUtils.Graphs.EdgeGraph.MoleculeEdgeGraph.get_label_types" class="docs-object-method">&nbsp;</a> 
```python
get_label_types(self, label_constructor=None, use_ring_identifiers=True, use_functional_group_identifiers=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2279)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2279?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate structured chemical identifiers for every node using optional ring and functional-group annotations.
  - `label_constructor`: `object`
    > The value supplied for `label_constructor`, interpreted according to the algorithm described above.

  - `use_ring_identifiers`: `object`
    > Whether ring categories are included in atom identifiers.

  - `use_functional_group_identifiers`: `object`
    > Whether functional-group names are included in atom identifiers.

  - `:returns`: `object`
    > One `atom_identifier` per graph node.


<a id="McUtils.Graphs.EdgeGraph.MoleculeEdgeGraph.get_heavy_atom_framework_graph" class="docs-object-method">&nbsp;</a> 
```python
get_heavy_atom_framework_graph(self, heavy_atoms=None, light_atoms=None, included_atoms=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2323)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2323?message=Update%20Docs)]
</div>
**LLM Docstring**

Extract a subgraph containing selected heavy atoms and return its original node indices.
  - `heavy_atoms`: `object`
    > Optional set of element symbols to retain as heavy atoms.

  - `light_atoms`: `object`
    > Element symbols to remove when constructing the heavy-atom framework.

  - `included_atoms`: `object`
    > Additional original indices that should remain in the framework.

  - `:returns`: `object`
    > A pair `(subgraph, original_indices)`.


<a id="McUtils.Graphs.EdgeGraph.MoleculeEdgeGraph.find_longest_chain" class="docs-object-method">&nbsp;</a> 
```python
find_longest_chain(self, rings=None, root=None, use_highest_valencies=True, heavy_atoms=True, light_atoms=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2363)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2363?message=Update%20Docs)]
</div>
**LLM Docstring**

Find a longest chain in the heavy-atom framework and map it back to original indices.
  - `rings`: `object`
    > Previously detected cycles, used to avoid recomputation.

  - `root`: `object`
    > Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.

  - `use_highest_valencies`: `object`
    > Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.

  - `heavy_atoms`: `object`
    > Optional set of element symbols to retain as heavy atoms.

  - `light_atoms`: `object`
    > Element symbols to remove when constructing the heavy-atom framework.

  - `:returns`: `object`
    > Original atom indices along the selected heavy-atom chain.


<a id="McUtils.Graphs.EdgeGraph.MoleculeEdgeGraph.segment_by_chains" class="docs-object-method">&nbsp;</a> 
```python
segment_by_chains(self, root=None, rings=None, use_highest_valencies=True, heavy_atoms=True, light_atoms=None, backbone=None, validate=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2429)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.py#L2429?message=Update%20Docs)]
</div>
**LLM Docstring**

Segment the heavy-atom framework into chains and restore original atom indices.
  - `root`: `object`
    > Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.

  - `rings`: `object`
    > Previously detected cycles, used to avoid recomputation.

  - `use_highest_valencies`: `object`
    > Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.

  - `heavy_atoms`: `object`
    > Optional set of element symbols to retain as heavy atoms.

  - `light_atoms`: `object`
    > Element symbols to remove when constructing the heavy-atom framework.

  - `backbone`: `object`
    > Optional preselected backbone chain.

  - `validate`: `object`
    > Whether to run duplicate and attachment consistency checks.

  - `:returns`: `object`
    > Nested node-index groups describing the resulting graph decomposition.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Graphs/EdgeGraph/MoleculeEdgeGraph.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L1720?message=Update%20Docs)   
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