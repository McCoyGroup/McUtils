## <a id="McUtils.Graphs.EdgeGraph.EdgeGraph">EdgeGraph</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph.py#L23)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L23?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
intermediate_break_threshold: int
edges: member_descriptor
graph: member_descriptor
labels: member_descriptor
map: member_descriptor
weights: member_descriptor
```
<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, labels, edges, graph=None, edge_map=None, weights=None, allow_self_loops=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph.py#L26)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L26?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct an undirected labeled graph from edges, an optional adjacency matrix, and an optional edge map.
  - `labels`: `object`
    > Node labels indexed consistently with the graph.

  - `edges`: `object`
    > Undirected edges as endpoint pairs, optionally carrying weights.

  - `graph`: `object`
    > Graph object, adjacency matrix, or adjacency mapping used by the operation.

  - `edge_map`: `object`
    > Adjacency mapping from node indices to neighbor sets.

  - `weights`: `object`
    > Optional mapping or values used as edge weights.

  - `allow_self_loops`: `object`
    > Whether neighbor maps may contain a node as its own neighbor.

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.from_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_map(cls, edge_map): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L68)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L68?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert an arbitrary-key adjacency mapping to integer indices while preserving original keys as labels.
  - `edge_map`: `object`
    > Adjacency mapping from node indices to neighbor sets.

  - `:returns`: `object`
    > A graph whose labels are the original mapping keys.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.graph_difference" class="docs-object-method">&nbsp;</a> 
```python
graph_difference(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L89)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L89?message=Update%20Docs)]
</div>
**LLM Docstring**

Compare adjacency matrices and return directed edge positions added to and removed from this graph.
  - `other`: `object`
    > The graph or object to compare against.

  - `:returns`: `object`
    > A pair `(added_edges, removed_edges)` of endpoint arrays.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_edge_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_edge_graph(cls, spec, num_nodes=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L112)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L112?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize an adjacency mapping, sparse matrix, or edge list to a sparse adjacency matrix.
  - `spec`: `object`
    > Graph specification as an adjacency mapping, sparse matrix, or edge list.

  - `num_nodes`: `object`
    > Optional total node count, including isolated vertices.

  - `:returns`: `object`
    > A sparse adjacency matrix.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.layout" class="docs-object-method">&nbsp;</a> 
```python
layout(self, method='default', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L147)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L147?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute node coordinates through the registered `GraphLayout` dispatcher.
  - `method`: `object`
    > Layout method name or callable selector.

  - `opts`: `object`
    > Additional options forwarded to the delegated operation.

  - `:returns`: `dict`
    > A mapping from nodes to 2D positions.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, method='default', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L165)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L165?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute a layout and render the graph with `GraphPlotter`.
  - `method`: `object`
    > Layout method name or callable selector.

  - `opts`: `object`
    > Additional options forwarded to the delegated operation.

  - `:returns`: `object`
    > The result returned by `GraphPlotter.plot`.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_edge_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_edge_list(cls, spec): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L197?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize a mapping, sparse adjacency matrix, or existing iterable to an edge list.
  - `spec`: `object`
    > Graph specification as an adjacency mapping, sparse matrix, or edge list.

  - `:returns`: `object`
    > An edge-list representation.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_edge_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_edge_map(cls, spec): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L222)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L222?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize a mapping, sparse adjacency matrix, or edge list to an undirected neighbor map.
  - `spec`: `object`
    > Graph specification as an adjacency mapping, sparse matrix, or edge list.

  - `:returns`: `object`
    > An undirected adjacency mapping.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.adj_mat" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
adj_mat(cls, num_nodes, edges, weights=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L242)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L242?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a symmetric CSR adjacency matrix from unweighted, explicitly weighted, or weight-mapped edges.
  - `num_nodes`: `object`
    > Optional total node count, including isolated vertices.

  - `edges`: `object`
    > Undirected edges as endpoint pairs, optionally carrying weights.

  - `weights`: `object`
    > Optional mapping or values used as edge weights.

  - `:returns`: `object`
    > A symmetric CSR adjacency matrix.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_distances" class="docs-object-method">&nbsp;</a> 
```python
get_distances(self, indices=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L283?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute shortest-path distances for all nodes or selected source indices.
  - `indices`: `object`
    > One node index or a sequence of node indices.

  - `:returns`: `object`
    > A shortest-path distance array.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.build_edge_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
build_edge_map(cls, edge_list, num_nodes=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L302)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L302?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a symmetric dictionary of neighbor sets and optionally include isolated nodes.
  - `edge_list`: `object`
    > The value supplied for `edge_list`, interpreted according to the algorithm described above.

  - `num_nodes`: `object`
    > Optional total node count, including isolated vertices.

  - `:returns`: `object`
    > A dictionary mapping each node to a set of neighbors.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.take" class="docs-object-method">&nbsp;</a> 
```python
take(self, pos): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L391)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L391?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the induced subgraph on selected node positions.
  - `pos`: `object`
    > Selected node positions in the original graph.

  - `:returns`: `object`
    > The induced subgraph.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.split" class="docs-object-method">&nbsp;</a> 
```python
split(self, backbone_pos, return_subgraphs=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L405)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L405?message=Update%20Docs)]
</div>
**LLM Docstring**

Cut edges from a backbone to off-backbone nodes and return the resulting connected components.
  - `backbone_pos`: `object`
    > The value supplied for `backbone_pos`, interpreted according to the algorithm described above.

  - `return_subgraphs`: `object`
    > Whether to construct graph objects instead of returning index groups.

  - `:returns`: `object`
    > Component subgraphs or arrays of original node indices.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.break_bonds" class="docs-object-method">&nbsp;</a> 
```python
break_bonds(self, bonds, return_subgraphs=True, return_single_graph=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L436)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L436?message=Update%20Docs)]
</div>
**LLM Docstring**

Remove specified undirected bonds and return either one modified graph or its connected components.
  - `bonds`: `object`
    > The value supplied for `bonds`, interpreted according to the algorithm described above.

  - `return_subgraphs`: `object`
    > Whether to construct graph objects instead of returning index groups.

  - `return_single_graph`: `object`
    > The value supplied for `return_single_graph`, interpreted according to the algorithm described above.

  - `:returns`: `object`
    > A modified graph, component subgraphs, or component index groups.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_label_strings" class="docs-object-method">&nbsp;</a> 
```python
get_label_strings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L475)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L475?message=Update%20Docs)]
</div>
**LLM Docstring**

Reduce labels to strings, using the first item of non-string label records.
  - `:returns`: `object`
    > One string label per node.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.graph_match" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
graph_match(cls, graph1: "'EdgeGraph'", graph2: "'EdgeGraph'"): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L552)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L552?message=Update%20Docs)]
</div>
**LLM Docstring**

Test graph isomorphism after inexpensive checks on size, labels, edge count, and degree sequence.
  - `graph1`: `'EdgeGraph'`
    > First graph in the comparison.

  - `graph2`: `'EdgeGraph'`
    > Second graph in the comparison.

  - `:returns`: `bool`
    > Whether the tested condition holds.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L585)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L585?message=Update%20Docs)]
</div>
**LLM Docstring**

Compare two graphs using `graph_match`.
  - `other`: `object`
    > The graph or object to compare against.

  - `:returns`: `bool`
    > Whether the tested condition holds.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_neighborhood_iterator" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_neighborhood_iterator(cls, node, edge_map, ignored=None, num=1, visited=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L599)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L599?message=Update%20Docs)]
</div>
**LLM Docstring**

Yield directed discovery edges encountered in a breadth-layer expansion around a node.
  - `node`: `object`
    > Node identifier.

  - `edge_map`: `object`
    > Adjacency mapping from node indices to neighbor sets.

  - `ignored`: `object`
    > Nodes excluded from neighborhood expansion.

  - `num`: `object`
    > Number of breadth layers to expand from the root.

  - `visited`: `object`
    > Mutable or per-path set of nodes already seen.

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.build_neighborhood_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
build_neighborhood_graph(cls, node, labels, edge_map, ignored=None, num=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L639)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L639?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a remapped graph from edges discovered within a fixed neighborhood depth.
  - `node`: `object`
    > Node identifier.

  - `labels`: `object`
    > Node labels indexed consistently with the graph.

  - `edge_map`: `object`
    > Adjacency mapping from node indices to neighbor sets.

  - `ignored`: `object`
    > Nodes excluded from neighborhood expansion.

  - `num`: `object`
    > Number of breadth layers to expand from the root.

  - `:returns`: `object`
    > A remapped neighborhood graph.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.neighbor_graph" class="docs-object-method">&nbsp;</a> 
```python
neighbor_graph(self, root, ignored=None, num=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L672)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L672?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the local neighborhood graph around a root node.
  - `root`: `object`
    > Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.

  - `ignored`: `object`
    > Nodes excluded from neighborhood expansion.

  - `num`: `object`
    > Number of breadth layers to expand from the root.

  - `:returns`: `object`
    > A remapped neighborhood graph.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.neighbor_iterator" class="docs-object-method">&nbsp;</a> 
```python
neighbor_iterator(self, root, ignored=None, num=1, return_labels=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L692)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L692?message=Update%20Docs)]
</div>
**LLM Docstring**

Yield neighbor indices or labels discovered within a fixed number of expansion layers.
  - `root`: `object`
    > Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.

  - `ignored`: `object`
    > Nodes excluded from neighborhood expansion.

  - `num`: `object`
    > Number of breadth layers to expand from the root.

  - `return_labels`: `object`
    > Whether to translate indices back to labels.

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.rings" class="docs-object-method">&nbsp;</a> 
```python
@property
rings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L719)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L719?message=Update%20Docs)]
</div>
**LLM Docstring**

Lazily compute and cache rings detected in the graph.
  - `:returns`: `list`
    > A list of ordered ring vertex sequences.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.find_rings_in_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
find_rings_in_graph(cls, n_inds, edge_map): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L733)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L733?message=Update%20Docs)]
</div>
**LLM Docstring**

Enumerate minimal cycles by detecting revisitation candidates, testing vertex subsets, and removing duplicate or containing cycles.
  - `n_inds`: `object`
    > Number of indexed vertices represented by the adjacency map.

  - `edge_map`: `object`
    > Adjacency mapping from node indices to neighbor sets.

  - `:returns`: `object`
    > A list of minimal ordered cycles.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.check_ring_in_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
check_ring_in_graph(cls, ring_atoms, edge_map): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L813)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L813?message=Update%20Docs)]
</div>
**LLM Docstring**

Validate a proposed cycle and order its vertices by depth-first traversal around the induced ring.
  - `ring_atoms`: `object`
    > Candidate vertices that should form one cycle.

  - `edge_map`: `object`
    > Adjacency mapping from node indices to neighbor sets.

  - `:returns`: `object`
    > An ordered cycle, or `False` when the candidate is invalid.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_rings" class="docs-object-method">&nbsp;</a> 
```python
get_rings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L850)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L850?message=Update%20Docs)]
</div>
**LLM Docstring**

Find rings in this graph’s edge map.
  - `:returns`: `list`
    > A list of ordered ring vertex sequences.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_shortest_path_data" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_shortest_path_data(cls, graph): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L861)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L861?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute all-pairs shortest-path distances and predecessor indices.
  - `graph`: `object`
    > Graph object, adjacency matrix, or adjacency mapping used by the operation.

  - `:returns`: `object`
    > The requested path, or `None` when no connected path exists.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.shortest_path_data" class="docs-object-method">&nbsp;</a> 
```python
@property
shortest_path_data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L877)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L877?message=Update%20Docs)]
</div>
**LLM Docstring**

Lazily compute and cache shortest-path distances and predecessors.
  - `:returns`: `object`
    > The requested path, or `None` when no connected path exists.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_path_from_data" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_path_from_data(cls, start, end, sp_data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L891)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L891?message=Update%20Docs)]
</div>
**LLM Docstring**

Reconstruct a shortest path from a SciPy predecessor matrix.
  - `start`: `object`
    > Path start vertex.

  - `end`: `object`
    > Path destination vertex.

  - `sp_data`: `object`
    > Tuple of shortest-path distances and predecessor indices.

  - `:returns`: `object`
    > The requested path, or `None` when no connected path exists.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_longest_path_from_data" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_longest_path_from_data(cls, shortest_path_data, root=None, check_connected=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L922)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L922?message=Update%20Docs)]
</div>
**LLM Docstring**

Select a farthest connected node pair, optionally from a fixed root, and reconstruct its shortest path.
  - `shortest_path_data`: `object`
    > Tuple containing all-pairs distances and predecessor indices.

  - `root`: `object`
    > Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.

  - `check_connected`: `object`
    > The value supplied for `check_connected`, interpreted according to the algorithm described above.

  - `:returns`: `object`
    > The requested path, or `None` when no connected path exists.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_path" class="docs-object-method">&nbsp;</a> 
```python
get_path(self, start, end): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L951)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L951?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the cached shortest path between two nodes.
  - `start`: `object`
    > Path start vertex.

  - `end`: `object`
    > Path destination vertex.

  - `:returns`: `object`
    > The requested path, or `None` when no connected path exists.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.compute_edge_centralities" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
compute_edge_centralities(self, indices, map): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L968)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L968?message=Update%20Docs)]
</div>
**LLM Docstring**

Return node valencies for one index or an index array.
  - `indices`: `object`
    > One node index or a sequence of node indices.

  - `map`: `object`
    > Adjacency mapping from nodes to neighbor sets.

  - `:returns`: `object`
    > An integer valence or an integer array.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.compute_ring_centralities" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
compute_ring_centralities(cls, indices, rings): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L989)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L989?message=Update%20Docs)]
</div>
**LLM Docstring**

Count how many supplied rings contain each requested node.
  - `indices`: `object`
    > One node index or a sequence of node indices.

  - `rings`: `object`
    > Previously detected cycles, used to avoid recomputation.

  - `:returns`: `object`
    > An integer count or count array.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.find_longest_chain_from_breakpoints" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
find_longest_chain_from_breakpoints(cls, map, graph=None, rings=None, root=None, use_highest_valencies=True, shortest_path_data=None, raise_on_failure=True, allow_intermediate_breaks=True, return_breakpoints=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1067)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1067?message=Update%20Docs)]
</div>
**LLM Docstring**

Search combinations of ring-bond cuts until the graph becomes acyclic, then return its longest shortest path.
  - `map`: `object`
    > Adjacency mapping from nodes to neighbor sets.

  - `graph`: `object`
    > Graph object, adjacency matrix, or adjacency mapping used by the operation.

  - `rings`: `object`
    > Previously detected cycles, used to avoid recomputation.

  - `root`: `object`
    > Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.

  - `use_highest_valencies`: `object`
    > Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.

  - `shortest_path_data`: `object`
    > Tuple containing all-pairs distances and predecessor indices.

  - `raise_on_failure`: `object`
    > Whether failure to remove all rings raises an exception instead of returning `None`.

  - `allow_intermediate_breaks`: `object`
    > Whether newly exposed rings may add further candidate cuts during the search.

  - `return_breakpoints`: `object`
    > Whether to return the selected ring bonds together with the chain.

  - `:returns`: `object`
    > The selected chain, optionally paired with the bonds cut to obtain it.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.find_longest_chain" class="docs-object-method">&nbsp;</a> 
```python
find_longest_chain(self, rings=None, use_highest_valencies=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1207)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1207?message=Update%20Docs)]
</div>
**LLM Docstring**

Find a longest chain after breaking rings using the graph’s cached topology.
  - `rings`: `object`
    > Previously detected cycles, used to avoid recomputation.

  - `use_highest_valencies`: `object`
    > Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.

  - `:returns`: `object`
    > A tuple of node indices along the selected chain.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.segment_by_chains" class="docs-object-method">&nbsp;</a> 
```python
segment_by_chains(self, rings=None, root=None, use_highest_valencies=True, validate=True, backbone=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1236?message=Update%20Docs)]
</div>
**LLM Docstring**

Segment the graph recursively into a longest backbone and chain segments from the remaining fragments.
  - `rings`: `object`
    > Previously detected cycles, used to avoid recomputation.

  - `root`: `object`
    > Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.

  - `use_highest_valencies`: `object`
    > Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.

  - `validate`: `object`
    > Whether to run duplicate and attachment consistency checks.

  - `backbone`: `object`
    > Optional preselected backbone chain.

  - `:returns`: `object`
    > Nested node-index groups describing the resulting graph decomposition.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_canonical_fragments" class="docs-object-method">&nbsp;</a> 
```python
get_canonical_fragments(self, ordering=None, validate=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1280)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1280?message=Update%20Docs)]
</div>
**LLM Docstring**

Partition an ordering into contiguous bonded fragments and derive three-point attachment descriptors for each branch.
  - `ordering`: `object`
    > Proposed node ordering to partition into bonded fragments.

  - `validate`: `object`
    > Whether to run duplicate and attachment consistency checks.

  - `:returns`: `object`
    > Nested node-index groups describing the resulting graph decomposition.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.find_graph_centroid" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
find_graph_centroid(cls, graph, shortest_path_data=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1370)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1370?message=Update%20Docs)]
</div>
**LLM Docstring**

Choose the graph center minimizing the maximum shortest-path distance to all nodes.
  - `graph`: `object`
    > Graph object, adjacency matrix, or adjacency mapping used by the operation.

  - `shortest_path_data`: `object`
    > Tuple containing all-pairs distances and predecessor indices.

  - `:returns`: `object`
    > The centroid node index.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_centroid" class="docs-object-method">&nbsp;</a> 
```python
get_centroid(self, check_fragments=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1394)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1394?message=Update%20Docs)]
</div>
**LLM Docstring**

Return component-local centroids for disconnected graphs or the centroid of a connected graph.
  - `check_fragments`: `object`
    > Whether disconnected components are handled independently.

  - `:returns`: `object`
    > A centroid index, or component indices paired with component-local centroids.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_graph_fragment_indices" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_graph_fragment_indices(cls, graph): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1417)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1417?message=Update%20Docs)]
</div>
**LLM Docstring**

Group node indices by connected-component labels.
  - `graph`: `object`
    > Graph object, adjacency matrix, or adjacency mapping used by the operation.

  - `:returns`: `object`
    > Nested node-index groups describing the resulting graph decomposition.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_fragments" class="docs-object-method">&nbsp;</a> 
```python
get_fragments(self, return_labels=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1434)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1434?message=Update%20Docs)]
</div>
**LLM Docstring**

Return connected components as indices or original labels.
  - `return_labels`: `object`
    > Whether to translate indices back to labels.

  - `:returns`: `object`
    > Nested node-index groups describing the resulting graph decomposition.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.segment_graph_by_chains" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
segment_graph_by_chains(cls, map: 'dict[int, set[int]]', graph: "'sparse.coo_matrix|sparse.csr_matrix|sparse.csc_matrix'" = None, rings=None, root=None, use_highest_valencies=True, shortest_path_data=None, validate=True, backbone=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1479)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1479?message=Update%20Docs)]
</div>
**LLM Docstring**

Recursively remove a longest backbone, decompose the remainder into components, and segment each component into chains.
  - `map`: `dict[int, set[int]]`
    > Adjacency mapping from nodes to neighbor sets.

  - `graph`: `'sparse.coo_matrix|sparse.csr_matrix|sparse.csc_matrix'`
    > Graph object, adjacency matrix, or adjacency mapping used by the operation.

  - `rings`: `object`
    > Previously detected cycles, used to avoid recomputation.

  - `root`: `object`
    > Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.

  - `use_highest_valencies`: `object`
    > Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.

  - `shortest_path_data`: `object`
    > Tuple containing all-pairs distances and predecessor indices.

  - `validate`: `object`
    > Whether to run duplicate and attachment consistency checks.

  - `backbone`: `object`
    > Optional preselected backbone chain.

  - `:returns`: `object`
    > Nested node-index groups describing the resulting graph decomposition.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_maximum_overlap_permutation" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_maximum_overlap_permutation(cls, graph_1: "'EdgeGraph'", graph_2: "'EdgeGraph'"): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1619)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1619?message=Update%20Docs)]
</div>
**LLM Docstring**

Search label-preserving permutations of differing atoms to minimize the symmetric difference between two bond sets.
  - `graph_1`: `'EdgeGraph'`
    > Reference graph whose bonds are permuted.

  - `graph_2`: `'EdgeGraph'`
    > Target graph whose bond set should be matched.

  - `:returns`: `object`
    > An integer permutation array.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.get_reindexing" class="docs-object-method">&nbsp;</a> 
```python
get_reindexing(self, other_graph): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1691)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1691?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the label-preserving permutation that best aligns another graph to this one.
  - `other_graph`: `object`
    > The value supplied for `other_graph`, interpreted according to the algorithm described above.

  - `:returns`: `object`
    > An integer permutation array.


<a id="McUtils.Graphs.EdgeGraph.EdgeGraph.align_labels" class="docs-object-method">&nbsp;</a> 
```python
align_labels(self, other_graph): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1704)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/EdgeGraph.py#L1704?message=Update%20Docs)]
</div>
**LLM Docstring**

Reorder this graph using the maximum-overlap permutation relative to another graph.
  - `other_graph`: `object`
    > The value supplied for `other_graph`, interpreted according to the algorithm described above.

  - `:returns`: `object`
    > A reordered graph.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Graphs/EdgeGraph/EdgeGraph.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Graphs/EdgeGraph/EdgeGraph.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Graphs/EdgeGraph/EdgeGraph.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Graphs/EdgeGraph/EdgeGraph.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L23?message=Update%20Docs)   
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