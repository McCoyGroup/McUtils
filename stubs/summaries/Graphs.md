### `EdgeGraph.py`
  - **class `EdgeGraph`**
    - `__init__(labels, edges, graph=None, edge_map=None, weights=None, allow_self_loops=False)`
    - `from_map(edge_map)` — Convert an arbitrary-key adjacency mapping to integer indices while preserving original keys as lab…
    - `graph_difference(other)` — Compare adjacency matrices and return directed edge positions added to and removed from this graph.
    - `get_edge_graph(spec, num_nodes=None)` — Normalize an adjacency mapping, sparse matrix, or edge list to a sparse adjacency matrix.
    - `layout(method='default', **opts)` — Compute node coordinates through the registered `GraphLayout` dispatcher.
    - `plot(method='default', **opts)` — Compute a layout and render the graph with `GraphPlotter`.
    - `get_edge_list(spec)` — Normalize a mapping, sparse adjacency matrix, or existing iterable to an edge list.
    - `get_edge_map(spec)` — Normalize a mapping, sparse adjacency matrix, or edge list to an undirected neighbor map.
    - `adj_mat(num_nodes, edges, weights=None)` — Build a symmetric CSR adjacency matrix from unweighted, explicitly weighted, or weight-mapped edges.
    - `get_distances(indices=None)` — Compute shortest-path distances for all nodes or selected source indices.
    - `build_edge_map(edge_list, num_nodes=None)` — Build a symmetric dictionary of neighbor sets and optionally include isolated nodes.
    - `take(pos)` — Return the induced subgraph on selected node positions.
    - `split(backbone_pos, return_subgraphs=True)` — Cut edges from a backbone to off-backbone nodes and return the resulting connected components.
    - `break_bonds(bonds, return_subgraphs=True, return_single_graph=False)` — Remove specified undirected bonds and return either one modified graph or its connected components.
    - `get_label_strings()` — Reduce labels to strings, using the first item of non-string label records.
    - `graph_match(graph1, graph2)` — Test graph isomorphism after inexpensive checks on size, labels, edge count, and degree sequence.
    - `get_neighborhood_iterator(node, edge_map, ignored=None, num=1, visited=None)` — Yield directed discovery edges encountered in a breadth-layer expansion around a node.
    - `build_neighborhood_graph(node, labels, edge_map, ignored=None, num=1)` — Build a remapped graph from edges discovered within a fixed neighborhood depth.
    - `neighbor_graph(root, ignored=None, num=1)` — Return the local neighborhood graph around a root node.
    - `neighbor_iterator(root, ignored=None, num=1, return_labels=False)` — Yield neighbor indices or labels discovered within a fixed number of expansion layers.
    - `rings()` — Lazily compute and cache rings detected in the graph.
    - `find_rings_in_graph(n_inds, edge_map)` — Enumerate minimal cycles by detecting revisitation candidates, testing vertex subsets, and removing…
    - `check_ring_in_graph(ring_atoms, edge_map)` — Validate a proposed cycle and order its vertices by depth-first traversal around the induced ring.
    - `get_rings()` — Find rings in this graph’s edge map.
    - `get_shortest_path_data(graph)` — Compute all-pairs shortest-path distances and predecessor indices.
    - `shortest_path_data()` — Lazily compute and cache shortest-path distances and predecessors.
    - `get_path_from_data(start, end, sp_data)` — Reconstruct a shortest path from a SciPy predecessor matrix.
    - `get_longest_path_from_data(shortest_path_data, root=None, check_connected=True)` — Select a farthest connected node pair, optionally from a fixed root, and reconstruct its shortest p…
    - `get_path(start, end)` — Return the cached shortest path between two nodes.
    - `compute_edge_centralities(indices, map)` — Return node valencies for one index or an index array.
    - `compute_ring_centralities(indices, rings)` — Count how many supplied rings contain each requested node.
    - `find_longest_chain_from_breakpoints(map, graph=None, rings=None, root=None, use_highest_valencies=True, shortest_path_data=None, raise_on_failure=True, allow_intermediate_breaks=True, return_breakpoints=False)` — Search combinations of ring-bond cuts until the graph becomes acyclic, then return its longest shor…
    - `find_longest_chain(rings=None, use_highest_valencies=True)` — Find a longest chain after breaking rings using the graph’s cached topology.
    - `segment_by_chains(rings=None, root=None, use_highest_valencies=True, validate=True, backbone=None)` — Segment the graph recursively into a longest backbone and chain segments from the remaining fragmen…
    - `get_canonical_fragments(ordering=None, validate=False)` — Partition an ordering into contiguous bonded fragments and derive three-point attachment descriptor…
    - `find_graph_centroid(graph, shortest_path_data=None)` — Choose the graph center minimizing the maximum shortest-path distance to all nodes.
    - `get_centroid(check_fragments=True)` — Return component-local centroids for disconnected graphs or the centroid of a connected graph.
    - `get_graph_fragment_indices(graph)` — Group node indices by connected-component labels.
    - `get_fragments(return_labels=False)` — Return connected components as indices or original labels.
    - `segment_graph_by_chains(map, graph=None, rings=None, root=None, use_highest_valencies=True, shortest_path_data=None, validate=True, backbone=None)` — Recursively remove a longest backbone, decompose the remainder into components, and segment each co…
    - `get_maximum_overlap_permutation(graph_1, graph_2)` — Search label-preserving permutations of differing atoms to minimize the symmetric difference betwee…
    - `get_reindexing(other_graph)` — Return the label-preserving permutation that best aligns another graph to this one.
    - `align_labels(other_graph)` — Reorder this graph using the maximum-overlap permutation relative to another graph.
  - **class `MoleculeEdgeGraph`** (EdgeGraph)
    - `get_rings()` — Use RDKit cycle perception on a carbon-labeled graph with dummy coordinates.
    - `categorize_ring(ring)` — Match a ring and its external valencies against known ring templates, accounting for cyclic rotatio…
    - `match_functional_group(root, neighbor_lists, cache=None)` — Test a root atom’s nested neighbor pattern against known functional-group templates with optional c…
    - `find_functional_groups()` — Locate known functional groups and collect the atom indices consumed by each matched pattern.
    - `get_label_types(label_constructor=None, use_ring_identifiers=True, use_functional_group_identifiers=True)` — Generate structured chemical identifiers for every node using optional ring and functional-group an…
    - `get_heavy_atom_framework_graph(heavy_atoms=None, light_atoms=None, included_atoms=None)` — Extract a subgraph containing selected heavy atoms and return its original node indices.
    - `find_longest_chain(rings=None, root=None, use_highest_valencies=True, heavy_atoms=True, light_atoms=None)` — Find a longest chain in the heavy-atom framework and map it back to original indices.
    - `segment_by_chains(root=None, rings=None, use_highest_valencies=True, heavy_atoms=True, light_atoms=None, backbone=None, validate=True)` — Segment the heavy-atom framework into chains and restore original atom indices.
  - **class `PebbleGameBoard`**
    - `__init__(n_vertices, k, l, min_pebbles=None)`
    - `add_edge(u, v)` — Attempt to add edge (u, v).
    - `components()` — Return rigid components (vertices sharing a pebble component).
  - **class `GraphSearcher`**
    - `__init__(data=None, track_components=True)`
    - `copy()` — Create an independent copy of the union-find state.
    - `add(node)` — Insert a node as a singleton component if needed and return its current root.
    - `find(node)` — Find root with path-halving compression.
    - `same_component(u, v)` — Test whether two nodes have the same union-find root.
    - `union(u, v)` — Merge the two components (union by rank).
    - `component(node)` — Return the tracked member set for a node’s component, or `None` when tracking is disabled.
  - **class `GraphComponentTracker`**
    - `__init__(k, l, track_components=False)`
    - `add_edge(u, v)` — Attempt to add constraint (u, v).
    - `add_edges(edges, revert_on_failure=True)` — Add a batch of constraints and optionally restore the previous state if any edge is redundant.
    - `rigid_components()` — Report whether each tracked component has reached its `(k, l)` rigidity threshold and optionally in…
- `pebble_rigidity(edge_sets, k, l=None)` — Test grouped edge constraints for `(k, l)` independence using a pebble game in 2D or component coun…
- `rigidity_matrix(points, edges)` — Construct the bar-and-joint rigidity matrix for one or a batch of point configurations.
- `statistically_rigid(edges, ndim, l=None, natoms=None, ntest=5, points=None, return_rigidity_matrix=False)` — Estimate generic rigidity by evaluating rigidity-matrix rank on random or supplied coordinates.
- `uniquely_rigid(edges, ndim, l=None, natoms=None, ntest=5, points=None, return_components=False, return_rigid_subgraphs=False)` — Estimate global rigidity using generic rigidity plus the rank of a random equilibrium stress matrix.

### `Layout.py`
  - **class `GraphLayout`**
    > Computes 2D layouts for a graph, dispatching to a named, registered
    > layout algorithm.
    > *(truncated — see stub for full docstring)*
    - `__init__(graph, weights=None)`
    - `register(name)` — Decorator: register a layout function under `name`.
    - `available_layouts()` — List registered layout algorithm names in sorted order.
    - `compute(method='default', **kwargs)` — Dispatch to a registered layout algorithm, cache its node-position mapping, and return it.
    - `shortest_path_distances()` — Compute and copy the graph-theoretic all-pairs shortest-path distance matrix.
- `circular_layout(layout, scale=1.0)` — Place graph nodes evenly around a circle of the requested radius.
- `kamada_kawai_layout(layout, scale=1.0, iterations=300, tol=1e-09, seed=None)` — Basic Kamada-Kawai layout, minimizing the stress function
  - **class `GraphPlotter`**
    > Flat 2D drawing of an ``EdgeGraph`` on a `Graphics` (2D) SVG backend -- the
    > graph-layout analogue of ``SVG2DMoleculePlotter``.
    > *(truncated — see stub for full docstring)*
    - `__init__(graph, coords)`
    - `nodes()` — Resolve node identities from `graph.nodes`, `graph.node_list`, or positional indices.
    - `plot(**styles)` — Resolve graph styles and geometry, construct node, edge, label, and annotation primitives, and rend…

### `Trees.py`
  - **class `TreeTraversalOrder`** (enum.Enum)
  - **class `TreeCallOrder`** (enum.Enum)
  - **class `TreeSentinels`** (enum.Enum)
- `tree_traversal(tree, callback, root=None, get_item=None, get_children=None, visited=None, check_visited=None, traversal_ordering='bfs', call_order='post')` — Traverse a tree or graph-like object and invoke a callback before visiting, after marking, or after…
- `tree_iter(tree, root=None, get_item=None, get_children=None, visited=None, check_visited=None, traversal_ordering='bfs', yield_paths=False, use_child_paths=None, per_path_visited=False, enable_disconnectivity=False)` — Yield nodes or root-to-node paths from a configurable breadth-first or depth-first traversal.
- `graph_iter(graph, root=None, get_item=None, get_children=None, visited=None, traversal_ordering='bfs', yield_paths=False, enable_disconnectivity=False)` — Adapt an adjacency mapping to `tree_iter`, enabling cycle-safe graph traversal and optional path en…
  - **class `TreeWrapper`**
    - `__init__(tree)`
    - `condense_subtrees()` — Merge a top-level sequence of mapping subtrees into one mapping when every element is dictionary-li…
    - `keys()` — Return mapping keys when the wrapped tree is mapping-like; otherwise return `None`.
    - `values()` — Return mapping values or the sequence itself for non-mapping trees.
    - `find_subtree(key)` — Find the first direct subtree associated with one of the requested keys.
    - `get_tree_item(tree, item)` — Follow a path through nested mappings and sequences, translating integer positions into mapping-key…
    - `bfs(callback, **opts)` — :param callback: Function called with traversal context for each visited node.
    - `dfs(callback, **opts)` — :param callback: Function called with traversal context for each visited node.

### `utils.py`
- `merge_sets(iterable)` — Merge an iterable of sets into transitive connected components under nonempty intersection.