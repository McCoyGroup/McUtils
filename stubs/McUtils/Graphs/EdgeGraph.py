from __future__ import annotations
import itertools, collections
import typing
import scipy
import math
import scipy.sparse as sparse, numpy as np
from .. import Devutils as dev
from .. import Numputils as nput
from .. import Iterators as itut
from . import Trees as tree
__all__ = ['EdgeGraph', 'MoleculeEdgeGraph', 'GraphSearcher', 'pebble_rigidity', 'statistically_rigid', 'uniquely_rigid']

class EdgeGraph:
    map: dict[int, set[int]]
    __slots__ = ['labels', 'edges', 'graph', 'map', 'weights', '_rings', '_sp_data']

    def __init__(self, labels, edges, graph=None, edge_map=None, weights=None, allow_self_loops=False):
        """
        **LLM Docstring**

        Construct an undirected labeled graph from edges, an optional adjacency matrix, and an optional edge map.

        :param labels: Node labels indexed consistently with the graph.
        :type labels: object

        :param edges: Undirected edges as endpoint pairs, optionally carrying weights.
        :type edges: object

        :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
        :type graph: object

        :param edge_map: Adjacency mapping from node indices to neighbor sets.
        :type edge_map: object

        :param weights: Optional mapping or values used as edge weights.
        :type weights: object

        :param allow_self_loops: Whether neighbor maps may contain a node as its own neighbor.
        :type allow_self_loops: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    @classmethod
    def from_map(cls, edge_map):
        """
        **LLM Docstring**

        Convert an arbitrary-key adjacency mapping to integer indices while preserving original keys as labels.

        :param edge_map: Adjacency mapping from node indices to neighbor sets.
        :type edge_map: object

        :return: A graph whose labels are the original mapping keys.
        :rtype: object
        """
        ...

    def graph_difference(self, other):
        """
        **LLM Docstring**

        Compare adjacency matrices and return directed edge positions added to and removed from this graph.

        :param other: The graph or object to compare against.
        :type other: object

        :return: A pair `(added_edges, removed_edges)` of endpoint arrays.
        :rtype: object
        """
        ...

    @classmethod
    def get_edge_graph(cls, spec, num_nodes=None):
        """
        **LLM Docstring**

        Normalize an adjacency mapping, sparse matrix, or edge list to a sparse adjacency matrix.

        :param spec: Graph specification as an adjacency mapping, sparse matrix, or edge list.
        :type spec: object

        :param num_nodes: Optional total node count, including isolated vertices.
        :type num_nodes: object

        :return: A sparse adjacency matrix.
        :rtype: object
        """
        ...

    def layout(self, method='default', **opts):
        """
        **LLM Docstring**

        Compute node coordinates through the registered `GraphLayout` dispatcher.

        :param method: Layout method name or callable selector.
        :type method: object

        :param opts: Additional options forwarded to the delegated operation.
        :type opts: object

        :return: A mapping from nodes to 2D positions.
        :rtype: dict
        """
        ...

    def plot(self, method='default', **opts):
        """
        **LLM Docstring**

        Compute a layout and render the graph with `GraphPlotter`.

        :param method: Layout method name or callable selector.
        :type method: object

        :param opts: Additional options forwarded to the delegated operation.
        :type opts: object

        :return: The result returned by `GraphPlotter.plot`.
        :rtype: object
        """
        ...

    @classmethod
    def get_edge_list(cls, spec):
        """
        **LLM Docstring**

        Normalize a mapping, sparse adjacency matrix, or existing iterable to an edge list.

        :param spec: Graph specification as an adjacency mapping, sparse matrix, or edge list.
        :type spec: object

        :return: An edge-list representation.
        :rtype: object
        """
        ...

    @classmethod
    def get_edge_map(cls, spec):
        """
        **LLM Docstring**

        Normalize a mapping, sparse adjacency matrix, or edge list to an undirected neighbor map.

        :param spec: Graph specification as an adjacency mapping, sparse matrix, or edge list.
        :type spec: object

        :return: An undirected adjacency mapping.
        :rtype: object
        """
        ...

    @classmethod
    def adj_mat(cls, num_nodes, edges, weights=None):
        """
        **LLM Docstring**

        Build a symmetric CSR adjacency matrix from unweighted, explicitly weighted, or weight-mapped edges.

        :param num_nodes: Optional total node count, including isolated vertices.
        :type num_nodes: object

        :param edges: Undirected edges as endpoint pairs, optionally carrying weights.
        :type edges: object

        :param weights: Optional mapping or values used as edge weights.
        :type weights: object

        :return: A symmetric CSR adjacency matrix.
        :rtype: object
        """
        ...

    def get_distances(self, indices=None):
        """
        **LLM Docstring**

        Compute shortest-path distances for all nodes or selected source indices.

        :param indices: One node index or a sequence of node indices.
        :type indices: object

        :return: A shortest-path distance array.
        :rtype: object
        """
        ...

    @classmethod
    def build_edge_map(cls, edge_list, num_nodes=None):
        """
        **LLM Docstring**

        Build a symmetric dictionary of neighbor sets and optionally include isolated nodes.

        :param edge_list: The value supplied for `edge_list`, interpreted according to the algorithm described above.
        :type edge_list: object

        :param num_nodes: Optional total node count, including isolated vertices.
        :type num_nodes: object

        :return: A dictionary mapping each node to a set of neighbors.
        :rtype: object
        """
        ...

    @classmethod
    def _remap(cls, labels, pos, rows, cols):
        """
        **LLM Docstring**

        Relabel a selected node subset densely and remap retained edge endpoints into that new index space.

        :param labels: Node labels indexed consistently with the graph.
        :type labels: object

        :param pos: Selected node positions in the original graph.
        :type pos: object

        :param rows: The value supplied for `rows`, interpreted according to the algorithm described above.
        :type rows: object

        :param cols: The value supplied for `cols`, interpreted according to the algorithm described above.
        :type cols: object

        :return: A pair `(selected_labels, remapped_edges)`.
        :rtype: object
        """
        ...

    @classmethod
    def _take(cls, pos, labels, adj_mat: sparse.compressed) -> 'typing.Self':
        """
        **LLM Docstring**

        Extract the induced subgraph on selected node positions from a sparse adjacency matrix.

        :param pos: Selected node positions in the original graph.
        :type pos: object

        :param labels: Node labels indexed consistently with the graph.
        :type labels: object

        :param adj_mat: The value supplied for `adj_mat`, interpreted according to the algorithm described above.
        :type adj_mat: sparse.compressed

        :return: The induced subgraph.
        :rtype: object
        """
        ...

    def take(self, pos):
        """
        **LLM Docstring**

        Return the induced subgraph on selected node positions.

        :param pos: Selected node positions in the original graph.
        :type pos: object

        :return: The induced subgraph.
        :rtype: object
        """
        ...

    def split(self, backbone_pos, return_subgraphs=True):
        """
        **LLM Docstring**

        Cut edges from a backbone to off-backbone nodes and return the resulting connected components.

        :param backbone_pos: The value supplied for `backbone_pos`, interpreted according to the algorithm described above.
        :type backbone_pos: object

        :param return_subgraphs: Whether to construct graph objects instead of returning index groups.
        :type return_subgraphs: object

        :return: Component subgraphs or arrays of original node indices.
        :rtype: object
        """
        ...

    def break_bonds(self, bonds, return_subgraphs=True, return_single_graph=False):
        """
        **LLM Docstring**

        Remove specified undirected bonds and return either one modified graph or its connected components.

        :param bonds: The value supplied for `bonds`, interpreted according to the algorithm described above.
        :type bonds: object

        :param return_subgraphs: Whether to construct graph objects instead of returning index groups.
        :type return_subgraphs: object

        :param return_single_graph: The value supplied for `return_single_graph`, interpreted according to the algorithm described above.
        :type return_single_graph: object

        :return: A modified graph, component subgraphs, or component index groups.
        :rtype: object
        """
        ...

    def get_label_strings(self):
        """
        **LLM Docstring**

        Reduce labels to strings, using the first item of non-string label records.

        :return: One string label per node.
        :rtype: object
        """
        ...

    @classmethod
    def _subgraph_match(cls, root1, labels1, edge_map1, root2, labels2, edge_map2, visited=None):
        """
        **LLM Docstring**

        Recursively match two rooted labeled graphs by label, valence, and a greedy neighbor correspondence.

        :param root1: Root index in the first graph.
        :type root1: object

        :param labels1: Labels for the first graph.
        :type labels1: object

        :param edge_map1: Adjacency map for the first graph.
        :type edge_map1: object

        :param root2: Root index in the second graph.
        :type root2: object

        :param labels2: Labels for the second graph.
        :type labels2: object

        :param edge_map2: Adjacency map for the second graph.
        :type edge_map2: object

        :param visited: Mutable or per-path set of nodes already seen.
        :type visited: object

        :return: Whether the tested condition holds.
        :rtype: bool
        """
        ...

    @classmethod
    def graph_match(cls, graph1: 'EdgeGraph', graph2: 'EdgeGraph'):
        """
        **LLM Docstring**

        Test graph isomorphism after inexpensive checks on size, labels, edge count, and degree sequence.

        :param graph1: First graph in the comparison.
        :type graph1: 'EdgeGraph'

        :param graph2: Second graph in the comparison.
        :type graph2: 'EdgeGraph'

        :return: Whether the tested condition holds.
        :rtype: bool
        """
        ...

    def __eq__(self, other):
        """
        **LLM Docstring**

        Compare two graphs using `graph_match`.

        :param other: The graph or object to compare against.
        :type other: object

        :return: Whether the tested condition holds.
        :rtype: bool
        """
        ...

    @classmethod
    def get_neighborhood_iterator(cls, node, edge_map, ignored=None, num=1, visited=None):
        """
        **LLM Docstring**

        Yield directed discovery edges encountered in a breadth-layer expansion around a node.

        :param node: Node identifier.
        :type node: object

        :param edge_map: Adjacency mapping from node indices to neighbor sets.
        :type edge_map: object

        :param ignored: Nodes excluded from neighborhood expansion.
        :type ignored: object

        :param num: Number of breadth layers to expand from the root.
        :type num: object

        :param visited: Mutable or per-path set of nodes already seen.
        :type visited: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    @classmethod
    def build_neighborhood_graph(cls, node, labels, edge_map, ignored=None, num=1):
        """
        **LLM Docstring**

        Build a remapped graph from edges discovered within a fixed neighborhood depth.

        :param node: Node identifier.
        :type node: object

        :param labels: Node labels indexed consistently with the graph.
        :type labels: object

        :param edge_map: Adjacency mapping from node indices to neighbor sets.
        :type edge_map: object

        :param ignored: Nodes excluded from neighborhood expansion.
        :type ignored: object

        :param num: Number of breadth layers to expand from the root.
        :type num: object

        :return: A remapped neighborhood graph.
        :rtype: object
        """
        ...

    def neighbor_graph(self, root, ignored=None, num=1):
        """
        **LLM Docstring**

        Return the local neighborhood graph around a root node.

        :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
        :type root: object

        :param ignored: Nodes excluded from neighborhood expansion.
        :type ignored: object

        :param num: Number of breadth layers to expand from the root.
        :type num: object

        :return: A remapped neighborhood graph.
        :rtype: object
        """
        ...

    def neighbor_iterator(self, root, ignored=None, num=1, return_labels=False):
        """
        **LLM Docstring**

        Yield neighbor indices or labels discovered within a fixed number of expansion layers.

        :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
        :type root: object

        :param ignored: Nodes excluded from neighborhood expansion.
        :type ignored: object

        :param num: Number of breadth layers to expand from the root.
        :type num: object

        :param return_labels: Whether to translate indices back to labels.
        :type return_labels: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    @property
    def rings(self):
        """
        **LLM Docstring**

        Lazily compute and cache rings detected in the graph.

        :return: A list of ordered ring vertex sequences.
        :rtype: list
        """
        ...

    @classmethod
    def find_rings_in_graph(cls, n_inds, edge_map):
        """
        **LLM Docstring**

        Enumerate minimal cycles by detecting revisitation candidates, testing vertex subsets, and removing duplicate or containing cycles.

        :param n_inds: Number of indexed vertices represented by the adjacency map.
        :type n_inds: object

        :param edge_map: Adjacency mapping from node indices to neighbor sets.
        :type edge_map: object

        :return: A list of minimal ordered cycles.
        :rtype: object
        """
        ...

    @classmethod
    def check_ring_in_graph(cls, ring_atoms, edge_map):
        """
        **LLM Docstring**

        Validate a proposed cycle and order its vertices by depth-first traversal around the induced ring.

        :param ring_atoms: Candidate vertices that should form one cycle.
        :type ring_atoms: object

        :param edge_map: Adjacency mapping from node indices to neighbor sets.
        :type edge_map: object

        :return: An ordered cycle, or `False` when the candidate is invalid.
        :rtype: object
        """
        ...

    def get_rings(self):
        """
        **LLM Docstring**

        Find rings in this graph’s edge map.

        :return: A list of ordered ring vertex sequences.
        :rtype: list
        """
        ...

    @classmethod
    def get_shortest_path_data(cls, graph):
        """
        **LLM Docstring**

        Compute all-pairs shortest-path distances and predecessor indices.

        :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
        :type graph: object

        :return: The requested path, or `None` when no connected path exists.
        :rtype: object
        """
        ...

    @property
    def shortest_path_data(self):
        """
        **LLM Docstring**

        Lazily compute and cache shortest-path distances and predecessors.

        :return: The requested path, or `None` when no connected path exists.
        :rtype: object
        """
        ...

    @classmethod
    def get_path_from_data(cls, start, end, sp_data):
        """
        **LLM Docstring**

        Reconstruct a shortest path from a SciPy predecessor matrix.

        :param start: Path start vertex.
        :type start: object

        :param end: Path destination vertex.
        :type end: object

        :param sp_data: Tuple of shortest-path distances and predecessor indices.
        :type sp_data: object

        :return: The requested path, or `None` when no connected path exists.
        :rtype: object
        """
        ...

    @classmethod
    def get_longest_path_from_data(cls, shortest_path_data, root=None, check_connected=True):
        """
        **LLM Docstring**

        Select a farthest connected node pair, optionally from a fixed root, and reconstruct its shortest path.

        :param shortest_path_data: Tuple containing all-pairs distances and predecessor indices.
        :type shortest_path_data: object

        :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
        :type root: object

        :param check_connected: The value supplied for `check_connected`, interpreted according to the algorithm described above.
        :type check_connected: object

        :return: The requested path, or `None` when no connected path exists.
        :rtype: object
        """
        ...

    def get_path(self, start, end):
        """
        **LLM Docstring**

        Return the cached shortest path between two nodes.

        :param start: Path start vertex.
        :type start: object

        :param end: Path destination vertex.
        :type end: object

        :return: The requested path, or `None` when no connected path exists.
        :rtype: object
        """
        ...

    @classmethod
    def compute_edge_centralities(self, indices, map):
        """
        **LLM Docstring**

        Return node valencies for one index or an index array.

        :param indices: One node index or a sequence of node indices.
        :type indices: object

        :param map: Adjacency mapping from nodes to neighbor sets.
        :type map: object

        :return: An integer valence or an integer array.
        :rtype: object
        """
        ...

    @classmethod
    def compute_ring_centralities(cls, indices, rings):
        """
        **LLM Docstring**

        Count how many supplied rings contain each requested node.

        :param indices: One node index or a sequence of node indices.
        :type indices: object

        :param rings: Previously detected cycles, used to avoid recomputation.
        :type rings: object

        :return: An integer count or count array.
        :rtype: object
        """
        ...

    @classmethod
    def _get_bond_breaks(cls, rings, map, use_highest_valencies=True):
        """
        **LLM Docstring**

        Generate candidate ring bonds to cut, prioritizing nodes with high ring participation or valence.

        :param rings: Previously detected cycles, used to avoid recomputation.
        :type rings: object

        :param map: Adjacency mapping from nodes to neighbor sets.
        :type map: object

        :param use_highest_valencies: Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.
        :type use_highest_valencies: object

        :return: Candidate bond lists, one list per ring.
        :rtype: object
        """
        ...
    intermediate_break_threshold = 10

    @classmethod
    def find_longest_chain_from_breakpoints(cls, map, graph=None, rings=None, root=None, use_highest_valencies=True, shortest_path_data=None, raise_on_failure=True, allow_intermediate_breaks=True, return_breakpoints=False):
        """
        **LLM Docstring**

        Search combinations of ring-bond cuts until the graph becomes acyclic, then return its longest shortest path.

        :param map: Adjacency mapping from nodes to neighbor sets.
        :type map: object

        :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
        :type graph: object

        :param rings: Previously detected cycles, used to avoid recomputation.
        :type rings: object

        :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
        :type root: object

        :param use_highest_valencies: Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.
        :type use_highest_valencies: object

        :param shortest_path_data: Tuple containing all-pairs distances and predecessor indices.
        :type shortest_path_data: object

        :param raise_on_failure: Whether failure to remove all rings raises an exception instead of returning `None`.
        :type raise_on_failure: object

        :param allow_intermediate_breaks: Whether newly exposed rings may add further candidate cuts during the search.
        :type allow_intermediate_breaks: object

        :param return_breakpoints: Whether to return the selected ring bonds together with the chain.
        :type return_breakpoints: object

        :return: The selected chain, optionally paired with the bonds cut to obtain it.
        :rtype: object
        """
        ...

    def find_longest_chain(self, rings=None, use_highest_valencies=True):
        """
        **LLM Docstring**

        Find a longest chain after breaking rings using the graph’s cached topology.

        :param rings: Previously detected cycles, used to avoid recomputation.
        :type rings: object

        :param use_highest_valencies: Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.
        :type use_highest_valencies: object

        :return: A tuple of node indices along the selected chain.
        :rtype: object
        """
        ...

    def segment_by_chains(self, rings=None, root=None, use_highest_valencies=True, validate=True, backbone=None):
        """
        **LLM Docstring**

        Segment the graph recursively into a longest backbone and chain segments from the remaining fragments.

        :param rings: Previously detected cycles, used to avoid recomputation.
        :type rings: object

        :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
        :type root: object

        :param use_highest_valencies: Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.
        :type use_highest_valencies: object

        :param validate: Whether to run duplicate and attachment consistency checks.
        :type validate: object

        :param backbone: Optional preselected backbone chain.
        :type backbone: object

        :return: Nested node-index groups describing the resulting graph decomposition.
        :rtype: object
        """
        ...

    def get_canonical_fragments(self, ordering=None, validate=False):
        """
        **LLM Docstring**

        Partition an ordering into contiguous bonded fragments and derive three-point attachment descriptors for each branch.

        :param ordering: Proposed node ordering to partition into bonded fragments.
        :type ordering: object

        :param validate: Whether to run duplicate and attachment consistency checks.
        :type validate: object

        :return: Nested node-index groups describing the resulting graph decomposition.
        :rtype: object
        """
        ...

    @classmethod
    def find_graph_centroid(cls, graph, shortest_path_data=None):
        """
        **LLM Docstring**

        Choose the graph center minimizing the maximum shortest-path distance to all nodes.

        :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
        :type graph: object

        :param shortest_path_data: Tuple containing all-pairs distances and predecessor indices.
        :type shortest_path_data: object

        :return: The centroid node index.
        :rtype: object
        """
        ...

    def get_centroid(self, check_fragments=True):
        """
        **LLM Docstring**

        Return component-local centroids for disconnected graphs or the centroid of a connected graph.

        :param check_fragments: Whether disconnected components are handled independently.
        :type check_fragments: object

        :return: A centroid index, or component indices paired with component-local centroids.
        :rtype: object
        """
        ...

    @classmethod
    def get_graph_fragment_indices(cls, graph):
        """
        **LLM Docstring**

        Group node indices by connected-component labels.

        :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
        :type graph: object

        :return: Nested node-index groups describing the resulting graph decomposition.
        :rtype: object
        """
        ...

    def get_fragments(self, return_labels=False):
        """
        **LLM Docstring**

        Return connected components as indices or original labels.

        :param return_labels: Whether to translate indices back to labels.
        :type return_labels: object

        :return: Nested node-index groups describing the resulting graph decomposition.
        :rtype: object
        """
        ...

    @classmethod
    def _reindex_segmentss(cls, frags, remapping):
        """
        **LLM Docstring**

        Recursively translate nested segment indices through a remapping table.

        :param frags: A node segment or nested collection of segments.
        :type frags: object

        :param remapping: Mapping from current indices to indices in the parent graph.
        :type remapping: object

        :return: Nested node-index groups describing the resulting graph decomposition.
        :rtype: object
        """
        ...

    @classmethod
    def segment_graph_by_chains(cls, map: dict[int, set[int]], graph: 'sparse.coo_matrix|sparse.csr_matrix|sparse.csc_matrix'=None, rings=None, root=None, use_highest_valencies=True, shortest_path_data=None, validate=True, backbone=None):
        """
        **LLM Docstring**

        Recursively remove a longest backbone, decompose the remainder into components, and segment each component into chains.

        :param map: Adjacency mapping from nodes to neighbor sets.
        :type map: dict[int, set[int]]

        :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
        :type graph: 'sparse.coo_matrix|sparse.csr_matrix|sparse.csc_matrix'

        :param rings: Previously detected cycles, used to avoid recomputation.
        :type rings: object

        :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
        :type root: object

        :param use_highest_valencies: Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.
        :type use_highest_valencies: object

        :param shortest_path_data: Tuple containing all-pairs distances and predecessor indices.
        :type shortest_path_data: object

        :param validate: Whether to run duplicate and attachment consistency checks.
        :type validate: object

        :param backbone: Optional preselected backbone chain.
        :type backbone: object

        :return: Nested node-index groups describing the resulting graph decomposition.
        :rtype: object
        """
        ...

    @classmethod
    def get_maximum_overlap_permutation(cls, graph_1: 'EdgeGraph', graph_2: 'EdgeGraph'):
        """
        **LLM Docstring**

        Search label-preserving permutations of differing atoms to minimize the symmetric difference between two bond sets.

        :param graph_1: Reference graph whose bonds are permuted.
        :type graph_1: 'EdgeGraph'

        :param graph_2: Target graph whose bond set should be matched.
        :type graph_2: 'EdgeGraph'

        :return: An integer permutation array.
        :rtype: object
        """
        ...

    def get_reindexing(self, other_graph):
        """
        **LLM Docstring**

        Return the label-preserving permutation that best aligns another graph to this one.

        :param other_graph: The value supplied for `other_graph`, interpreted according to the algorithm described above.
        :type other_graph: object

        :return: An integer permutation array.
        :rtype: object
        """
        ...

    def align_labels(self, other_graph):
        """
        **LLM Docstring**

        Reorder this graph using the maximum-overlap permutation relative to another graph.

        :param other_graph: The value supplied for `other_graph`, interpreted according to the algorithm described above.
        :type other_graph: object

        :return: A reordered graph.
        :rtype: object
        """
        ...

class MoleculeEdgeGraph(EdgeGraph):

    def get_rings(self):
        """
        **LLM Docstring**

        Use RDKit cycle perception on a carbon-labeled graph with dummy coordinates.

        :return: A list of ordered ring vertex sequences.
        :rtype: list
        """
        ...

    @classmethod
    def _match_motif(cls, label, neighbors, motif_root, *motif_branches):
        """
        **LLM Docstring**

        Partially implemented motif test that currently only checks whether the label occurs in any motif branch.

        The branch loop contains only an ellipsis, so no branch topology is currently checked.

        :param label: Central atom label.
        :type label: object

        :param neighbors: Neighbor labels or nested neighbor descriptions.
        :type neighbors: object

        :param motif_root: Required root label for a motif.
        :type motif_root: object

        :param motif_branches: Allowed motif branch definitions.
        :type motif_branches: object

        :return: `False` when the label is absent; otherwise currently `None` because branch matching is unfinished.
        :rtype: object
        """
        ...

    @classmethod
    def _idenfity_motifs(cls, label, neighbors, index=None, graph=None):
        """
        **LLM Docstring**

        Placeholder for motif identification; the function body is only an ellipsis.

        This method is a stub and currently performs no computation.

        :param label: Central atom label.
        :type label: object

        :param neighbors: Neighbor labels or nested neighbor descriptions.
        :type neighbors: object

        :param index: Index of the atom currently being labeled.
        :type index: object

        :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
        :type graph: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    @classmethod
    def _make_label(cls, label, neighbors, index=None, graph=None):
        """
        **LLM Docstring**

        Create a local chemical label from an atom and its immediate neighbor element labels.

        :param label: Central atom label.
        :type label: object

        :param neighbors: Neighbor labels or nested neighbor descriptions.
        :type neighbors: object

        :param index: Index of the atom currently being labeled.
        :type index: object

        :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
        :type graph: object

        :return: A compact local atom-type string.
        :rtype: object
        """
        ...

    def _collect_neighbor_list(self, root, depth=1, visited=None):
        """
        **LLM Docstring**

        Recursively collect nested neighbor labels and matching index trees to a requested depth.

        :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
        :type root: object

        :param depth: Remaining neighborhood recursion depth.
        :type depth: object

        :param visited: Mutable or per-path set of nodes already seen.
        :type visited: object

        :return: A pair of nested label and index tuples.
        :rtype: object
        """
        ...
    chemical_order = ['C', 'O', 'N', 'H', 'F', 'Cl', 'Br', 'I']

    @classmethod
    def _sort_atom_types(cls, counts, chemical_order=None):
        """
        **LLM Docstring**

        Sort atom labels or `(label, count)` pairs by a preferred chemical element order.

        :param counts: Atom labels or `(label, count)` pairs to order or format.
        :type counts: object

        :param chemical_order: Element ordering used when sorting atom types.
        :type chemical_order: object

        :return: A sorted list.
        :rtype: object
        """
        ...

    @classmethod
    def _format_atom_counts(cls, neighbors):
        """
        **LLM Docstring**

        Format atom counts as a compact molecular-fragment string such as `CH3`.

        :param neighbors: Neighbor labels or nested neighbor descriptions.
        :type neighbors: object

        :return: A compact atom-count string.
        :rtype: object
        """
        ...

    @classmethod
    def _format_ring_counts(cls, neighbors):
        """
        **LLM Docstring**

        Format atom counts inside square brackets for an unidentified ring.

        :param neighbors: Neighbor labels or nested neighbor descriptions.
        :type neighbors: object

        :return: A bracketed atom-count string.
        :rtype: object
        """
        ...

    @classmethod
    def _atomlist_match(cls, list_1, list_2):
        """
        **LLM Docstring**

        Greedily match required atom counts, treating `_` as a wildcard for remaining atoms.

        :param list_1: Observed atom labels.
        :type list_1: object

        :param list_2: Required atom labels, possibly including `_` wildcards.
        :type list_2: object

        :return: Whether the tested condition holds.
        :rtype: bool
        """
        ...

    @classmethod
    def _bonding_pattern_matcher(cls, neighbor_lists):
        """
        **LLM Docstring**

        Build a closure that compares observed nested neighbor patterns against functional-group requirements.

        :param neighbor_lists: Observed nested neighbor patterns.
        :type neighbor_lists: object

        :return: A callable accepting a required-count specification.
        :rtype: object
        """
        ...

    def categorize_ring(self, ring):
        """
        **LLM Docstring**

        Match a ring and its external valencies against known ring templates, accounting for cyclic rotations.

        :param ring: Ordered atom indices forming the ring to categorize.
        :type ring: object

        :return: A pair `(ring_category, ordered_ring_indices)`.
        :rtype: object
        """
        ...

    def match_functional_group(self, root, neighbor_lists, cache=None):
        """
        **LLM Docstring**

        Test a root atom’s nested neighbor pattern against known functional-group templates with optional caching.

        :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
        :type root: object

        :param neighbor_lists: Observed nested neighbor patterns.
        :type neighbor_lists: object

        :param cache: Optional dictionary caching functional-group matches.
        :type cache: object

        :return: A `(group_name, matched_pattern)` pair, or `None`.
        :rtype: object
        """
        ...

    def find_functional_groups(self):
        """
        **LLM Docstring**

        Locate known functional groups and collect the atom indices consumed by each matched pattern.

        :return: A list of `[group_name, atom_indices]` records.
        :rtype: object
        """
        ...
    atom_identifier = collections.namedtuple('atom_identifier', ['ring', 'group', 'motif', 'atom'])

    def _get_identifier(self, n, label_constructor, rings, groups):
        """
        **LLM Docstring**

        Assemble ring, functional-group, local-motif, and atomic identifiers for one atom.

        :param n: Number of items to normalize or process.
        :type n: object

        :param label_constructor: The value supplied for `label_constructor`, interpreted according to the algorithm described above.
        :type label_constructor: object

        :param rings: Previously detected cycles, used to avoid recomputation.
        :type rings: object

        :param groups: Functional-group matches used when building an atom identifier.
        :type groups: object

        :return: An `atom_identifier` named tuple.
        :rtype: object
        """
        ...

    def get_label_types(self, label_constructor=None, use_ring_identifiers=True, use_functional_group_identifiers=True):
        """
        **LLM Docstring**

        Generate structured chemical identifiers for every node using optional ring and functional-group annotations.

        :param label_constructor: The value supplied for `label_constructor`, interpreted according to the algorithm described above.
        :type label_constructor: object

        :param use_ring_identifiers: Whether ring categories are included in atom identifiers.
        :type use_ring_identifiers: object

        :param use_functional_group_identifiers: Whether functional-group names are included in atom identifiers.
        :type use_functional_group_identifiers: object

        :return: One `atom_identifier` per graph node.
        :rtype: object
        """
        ...
    light_atoms = {'H', 'D'}

    def get_heavy_atom_framework_graph(self, heavy_atoms=None, light_atoms=None, included_atoms=None):
        """
        **LLM Docstring**

        Extract a subgraph containing selected heavy atoms and return its original node indices.

        :param heavy_atoms: Optional set of element symbols to retain as heavy atoms.
        :type heavy_atoms: object

        :param light_atoms: Element symbols to remove when constructing the heavy-atom framework.
        :type light_atoms: object

        :param included_atoms: Additional original indices that should remain in the framework.
        :type included_atoms: object

        :return: A pair `(subgraph, original_indices)`.
        :rtype: object
        """
        ...

    def find_longest_chain(self, rings=None, root=None, use_highest_valencies=True, heavy_atoms=True, light_atoms=None):
        """
        **LLM Docstring**

        Find a longest chain in the heavy-atom framework and map it back to original indices.

        :param rings: Previously detected cycles, used to avoid recomputation.
        :type rings: object

        :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
        :type root: object

        :param use_highest_valencies: Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.
        :type use_highest_valencies: object

        :param heavy_atoms: Optional set of element symbols to retain as heavy atoms.
        :type heavy_atoms: object

        :param light_atoms: Element symbols to remove when constructing the heavy-atom framework.
        :type light_atoms: object

        :return: Original atom indices along the selected heavy-atom chain.
        :rtype: object
        """
        ...

    @classmethod
    def _reindex_segments(cls, inds, segments):
        """
        **LLM Docstring**

        Recursively map heavy-atom segment indices back to the original graph.

        :param inds: Original graph indices corresponding to the reduced heavy-atom graph.
        :type inds: object

        :param segments: Nested chain segments indexed in the reduced graph.
        :type segments: object

        :return: Nested node-index groups describing the resulting graph decomposition.
        :rtype: object
        """
        ...

    def segment_by_chains(self, root=None, rings=None, use_highest_valencies=True, heavy_atoms=True, light_atoms=None, backbone=None, validate=True):
        """
        **LLM Docstring**

        Segment the heavy-atom framework into chains and restore original atom indices.

        :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
        :type root: object

        :param rings: Previously detected cycles, used to avoid recomputation.
        :type rings: object

        :param use_highest_valencies: Whether candidate ring cuts are restricted to the most central or highest-valence ring nodes.
        :type use_highest_valencies: object

        :param heavy_atoms: Optional set of element symbols to retain as heavy atoms.
        :type heavy_atoms: object

        :param light_atoms: Element symbols to remove when constructing the heavy-atom framework.
        :type light_atoms: object

        :param backbone: Optional preselected backbone chain.
        :type backbone: object

        :param validate: Whether to run duplicate and attachment consistency checks.
        :type validate: object

        :return: Nested node-index groups describing the resulting graph decomposition.
        :rtype: object
        """
        ...

class PebbleGameBoard:

    def __init__(self, n_vertices: int, k, l, min_pebbles=None):
        """
        **LLM Docstring**

        Initialize a simplified `(k, l)` pebble-game state with per-vertex pebbles, parent links, and component sets.

        :param n_vertices: Number of vertices on the pebble-game board.
        :type n_vertices: int

        :param k: Degrees of freedom assigned per vertex.
        :type k: object

        :param l: Sparsity offset; defaults to rigid-body motions for the dimension.
        :type l: object

        :param min_pebbles: Minimum free-pebble threshold used to reject a new constraint.
        :type min_pebbles: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def _free_pebble(self, v: int, visited: set=None) -> bool:
        """
        Try to move a pebble to vertex v by reversing edge orientations
        (DFS over the directed graph). Returns True if successful.
        """
        ...

    def _connected_nodes(self, src, visited=None):
        """
        **LLM Docstring**

        Follow parent links from a source and collect reachable vertices.

        :param src: Starting vertex for following directed parent links.
        :type src: object

        :param visited: Mutable or per-path set of nodes already seen.
        :type visited: object

        :return: The visited set including vertices reachable through parent links.
        :rtype: object
        """
        ...

    def _count_pebbles(self, u: int, v: int) -> int:
        """
        Count free pebbles reachable from u and v combined
        (union of their directed components).
        """
        ...

    def add_edge(self, u: int, v: int) -> bool:
        """
        Attempt to add edge (u, v).
        Returns True if edge is independent (added to the graph),
        False if it would violate sparsity (redundant/over-constrained).
        """
        ...

    def components(self) -> dict[int, list[int]]:
        """Return rigid components (vertices sharing a pebble component)."""
        ...

class GraphSearcher:

    def __init__(self, data=None, track_components=True):
        """
        **LLM Docstring**

        Initialize union-find parent, rank, and optional component-member tables.

        :param data: Input data consumed by the operation.
        :type data: object

        :param track_components: Whether union-find member sets should be maintained.
        :type track_components: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def copy(self):
        """
        **LLM Docstring**

        Create an independent copy of the union-find state.

        :return: An independent `GraphSearcher`.
        :rtype: object
        """
        ...

    def add(self, node) -> None:
        """
        **LLM Docstring**

        Insert a node as a singleton component if needed and return its current root.

        :param node: Node identifier.
        :type node: object

        :return: The union-find root of the node.
        :rtype: object
        """
        ...

    def find(self, node):
        """Find root with path-halving compression."""
        ...

    def same_component(self, u, v) -> bool:
        """
        **LLM Docstring**

        Test whether two nodes have the same union-find root.

        :param u: First endpoint.
        :type u: object

        :param v: Second endpoint.
        :type v: object

        :return: Whether both nodes have the same root.
        :rtype: object
        """
        ...

    def union(self, u, v):
        """Merge the two components (union by rank)."""
        ...

    def component(self, node):
        """
        **LLM Docstring**

        Return the tracked member set for a node’s component, or `None` when tracking is disabled.

        :param node: Node identifier.
        :type node: object

        :return: The tracked component member set, or `None`.
        :rtype: object
        """
        ...

class GraphComponentTracker:

    def __init__(self, k, l, track_components=False):
        """
        **LLM Docstring**

        Initialize a union-find-based `(k, l)` sparsity tracker for grouped constraints.

        :param k: Degrees of freedom assigned per vertex.
        :type k: object

        :param l: Sparsity offset; defaults to rigid-body motions for the dimension.
        :type l: object

        :param track_components: Whether union-find member sets should be maintained.
        :type track_components: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def add_edge(self, u, v) -> bool | None:
        """
        Attempt to add constraint (u, v).

        Returns True if independent (accepted), False if redundant (rejected).
        """
        ...

    def add_edges(self, edges, revert_on_failure=True) -> list[bool | None]:
        """
        **LLM Docstring**

        Add a batch of constraints and optionally restore the previous state if any edge is redundant.

        :param edges: Undirected edges as endpoint pairs, optionally carrying weights.
        :type edges: object

        :param revert_on_failure: Whether a failed batch should roll back all changes.
        :type revert_on_failure: object

        :return: A status list containing `True`, `False`, or `None` for each edge.
        :rtype: object
        """
        ...

    def rigid_components(self):
        """
        **LLM Docstring**

        Report whether each tracked component has reached its `(k, l)` rigidity threshold and optionally include members.

        :return: A mapping from component roots to rigidity flags or `(flag, members)` pairs.
        :rtype: object
        """
        ...

def pebble_rigidity(edge_sets, k, l=None):
    """
    **LLM Docstring**

    Test grouped edge constraints for `(k, l)` independence using a pebble game in 2D or component counting otherwise.

    :param edge_sets: Groups of one or more constraints to test in sequence.
    :type edge_sets: object

    :param k: Degrees of freedom assigned per vertex.
    :type k: object

    :param l: Sparsity offset; defaults to rigid-body motions for the dimension.
    :type l: object

    :return: One Boolean result per supplied edge group.
    :rtype: object
    """
    ...

def rigidity_matrix(points, edges):
    """
    **LLM Docstring**

    Construct the bar-and-joint rigidity matrix for one or a batch of point configurations.

    :param points: Coordinates with trailing shape `(n_atoms, ndim)`.
    :type points: object

    :param edges: Undirected edges as endpoint pairs, optionally carrying weights.
    :type edges: object

    :return: An array with trailing shape `(n_edges, n_atoms * ndim)`.
    :rtype: np.ndarray
    """
    ...

def statistically_rigid(edges, ndim, l=None, natoms=None, ntest=5, points=None, return_rigidity_matrix=False):
    """
    **LLM Docstring**

    Estimate generic rigidity by evaluating rigidity-matrix rank on random or supplied coordinates.

    :param edges: Undirected edges as endpoint pairs, optionally carrying weights.
    :type edges: object

    :param ndim: Spatial dimension of the rigidity problem.
    :type ndim: object

    :param l: Sparsity offset; defaults to rigid-body motions for the dimension.
    :type l: object

    :param natoms: Number of vertices represented by the edge list.
    :type natoms: object

    :param ntest: Number of random coordinate realizations to test.
    :type ntest: object

    :param points: Coordinates with trailing shape `(n_atoms, ndim)`.
    :type points: object

    :param return_rigidity_matrix: Whether to return the matrix and computed rank with the Boolean result.
    :type return_rigidity_matrix: object

    :return: A rigidity flag, optionally with the rigidity matrix and rank.
    :rtype: np.ndarray
    """
    ...

def uniquely_rigid(edges, ndim, l=None, natoms=None, ntest=5, points=None, return_components=False, return_rigid_subgraphs=False):
    """
    **LLM Docstring**

    Estimate global rigidity using generic rigidity plus the rank of a random equilibrium stress matrix.

    :param edges: Undirected edges as endpoint pairs, optionally carrying weights.
    :type edges: object

    :param ndim: Spatial dimension of the rigidity problem.
    :type ndim: object

    :param l: Sparsity offset; defaults to rigid-body motions for the dimension.
    :type l: object

    :param natoms: Number of vertices represented by the edge list.
    :type natoms: object

    :param ntest: Number of random coordinate realizations to test.
    :type ntest: object

    :param points: Coordinates with trailing shape `(n_atoms, ndim)`.
    :type points: object

    :param return_components: Whether to include rank and stress diagnostics.
    :type return_components: object

    :param return_rigid_subgraphs: Request for an unimplemented rigid-subgraph analysis.
    :type return_rigid_subgraphs: object

    :return: A global-rigidity flag, optionally with rigidity and stress diagnostics.
    :rtype: object
    """
    ...