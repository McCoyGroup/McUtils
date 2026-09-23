from __future__ import annotations

"""
graph_layout.py

A GraphLayout class with a plugin-based dispatch system for 2D graph
layout algorithms, plus a basic Kamada-Kawai implementation registered
as one such plugin.

Design
------
- `GraphLayout` holds the graph (nodes/edges/weights) and shared utilities
  (adjacency, shortest-path distances) that most layout algorithms need.
- `GraphLayout.register(name)` is a decorator used to add new layout
  functions to a class-level registry, so adding a new algorithm never
  requires touching `GraphLayout` itself.
- `GraphLayout.compute(method, **kwargs)` dispatches to the registered
  function by name and returns {node: (x, y)}.
"""

import math
import random
from typing import Callable, Dict, Hashable, Iterable, List, Optional, Tuple

from .. import Devutils as dev
from .. import Numputils as nput
from .EdgeGraph import EdgeGraph

import numpy as np
import scipy.sparse as sparse

# Node = Hashable
# Edge = Tuple[Node, Node]
# Position = Tuple[float, float]

__all__ = [
    "GraphLayout",
    "GraphPlotter"
]


class GraphLayout:
    """
    Computes 2D layouts for a graph, dispatching to a named, registered
    layout algorithm.

    Usage
    -----
        layout = GraphLayout(nodes, edges)
        positions = layout.compute("kamada_kawai")
        # positions: {node: (x, y)}

    Pinning nodes
    -------------
    Pass ``node_positions={node: (x, y), ...}`` to `compute` to fix one or
    more nodes at explicit coordinates. Every registered layout method is
    handed this mapping (as a `node_positions` keyword, keyed by original
    node label -- never an index) and is expected to honor it: the built-in
    ``"kamada_kawai"`` optimizer seeds pinned nodes at their given position
    and holds them there through every SMACOF iteration -- they still act as
    anchors that pull on their (free) neighbors via the ordinary stress
    terms, but never move themselves -- while ``"circular"`` simply places a
    pinned node at its given position instead of its circle point. A custom
    ``@GraphLayout.register``-ed method should accept a `node_positions`
    keyword the same way.

    On a disconnected graph, a component with any pinned nodes is, by
    default, exempted from the grid-tiling shift that keeps components'
    bounding boxes apart (see `_compute_disconnected` /
    `_tile_components`) -- otherwise pinning a node and then having the
    whole component silently translated out from under it would defeat the
    point. Pass ``fix_fragment_nodes=False`` to `compute` to have such a
    component tiled/shifted like any other instead (the pinned node still
    lands at its requested position *within* that component's own layout,
    it's just that the component as a whole is then free to be moved as a
    rigid body to avoid colliding with the others).

    Graph-supplied config (``meta``)
    ---------------------------------
    Every registered layout method is also handed the graph's ``meta`` dict
    (``EdgeGraph.meta``, always a dict -- empty by default) as a `meta`
    keyword, the same way it's handed `node_positions`: a graph can stash
    algorithm-specific config there for a layout method to pick up as its
    own default, without `GraphLayout` needing to know anything about that
    config itself. For example ``EdgeGraph.stacked_graph`` stashes
    ``{'layer_sizes': [...]}`` in ``meta``, which the built-in
    ``"stacked_layer"`` method reads as the default for its own
    `layer_sizes` argument when the caller doesn't pass one explicitly.
    Pass ``meta={...}`` to `compute` to override the graph's own `meta` for
    that one call (e.g. to lay out a graph that wasn't built with the
    config a particular method wants). A custom ``@GraphLayout.register``-ed
    method should accept a `meta` keyword the same way, even if it ignores
    it -- every registered method is called with both `node_positions` and
    `meta`, whether or not it uses them.
    """

    _registry = {}

    def __init__(self, graph:EdgeGraph, weights=None):
        """
        **LLM Docstring**

        Initialize layout state from an `EdgeGraph`, including node indexing and a dense adjacency matrix.

        :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
        :type graph: EdgeGraph

        :param weights: Optional mapping or values used as edge weights.
        :type weights: object

        :return: No value is returned.
        :rtype: None
        """
        self.graph = graph
        self.nodes = list(graph.labels)
        self.edges = list(graph.edges)
        self.weights = weights
        self._index = {n: i for i, n in enumerate(self.nodes)}
        self._adj = self._build_adjacency(weights)
        self.positions = {}

    # -- construction -------------------------------------------------

    def _build_adjacency(self, weights):
        """
        **LLM Docstring**

        Copy the graph adjacency matrix to dense form and overwrite selected directed entries with supplied weights.

        :param weights: Optional mapping or values used as edge weights.
        :type weights: object

        :return: A dense adjacency array.
        :rtype: object
        """
        adj = self.graph.graph.toarray()
        if weights is not None:
            for (i,j), w in weights.items():
                adj[i, j] = w
        return adj

    # -- plugin registry ------------------------------------------------

    @classmethod
    def register(cls, name: str):
        """Decorator: register a layout function under `name`.

        The function receives the GraphLayout instance as its first
        argument plus any algorithm-specific keyword arguments, and must
        return {node: (x, y)}.
        """

        def decorator(func):
            """
            **LLM Docstring**

            Register a layout function under the enclosing decorator name and return it unchanged.

            :param func: The layout function to associate with the registry name.
            :type func: object

            :return: The same function after registry insertion.
            :rtype: object
            """
            cls._registry[name] = func
            return func

        return decorator

    @classmethod
    def available_layouts(cls) -> List[str]:
        """
        **LLM Docstring**

        List registered layout algorithm names in sorted order.

        :return: Sorted registered layout names.
        :rtype: object
        """
        return sorted(cls._registry.keys())

    default_layout_method = "kamada_kawai"
    def compute(self, method: str = "default", node_positions: Optional[Dict[Hashable, Tuple[float, float]]] = None,
                meta: Optional[Dict] = None,
                fix_fragment_nodes: bool = True, **kwargs):
        """
        **LLM Docstring**

        Dispatch to a registered layout algorithm, cache its node-position mapping, and return it.

        :param method: Layout method name or callable selector.
        :type method: str

        :param node_positions: Optional ``{node: (x, y)}`` positions to pin one or more
            nodes at, forwarded to the registered layout function as a `node_positions`
            keyword (see the class docstring for how the built-in methods honor it).
        :type node_positions: dict

        :param meta: Optional dict of graph-supplied, algorithm-specific config,
            forwarded to the registered layout function as a `meta` keyword (see
            the class docstring). Defaults to `self.graph.meta`; pass this to
            override that for one call without touching the graph itself.
        :type meta: dict

        :param fix_fragment_nodes: On a disconnected graph, whether a component with any
            pinned `node_positions` is exempted from the grid-tiling shift (True, the
            default) or tiled/shifted like any other component regardless (False). No
            effect when the graph is a single connected component, since there's no
            tiling step to control.
        :type fix_fragment_nodes: bool

        :param kwargs: Additional keyword options forwarded to lower-level calls.
        :type kwargs: object

        :return: A mapping from node labels to 2D coordinate pairs.
        :rtype: dict
        """
        if dev.str_is(method, 'default'):
            method = self.default_layout_method
        if method not in self._registry:
            raise ValueError(
                f"Unknown layout method '{method}'. "
                f"Available: {self.available_layouts()}"
            )

        node_positions = self._validate_node_positions(node_positions)
        if meta is None:
            meta = self.graph.meta

        n = len(self.nodes)
        if n == 0:
            self.positions = {}
            return self.positions

        component_ids = self._connected_component_ids()
        n_components = int(component_ids.max()) + 1 if n > 0 else 0
        if n_components <= 1:
            self.positions = self._registry[method](self, node_positions=node_positions, meta=meta, **kwargs)
            return self.positions

        # Most layout algorithms (Kamada-Kawai in particular) place nodes by
        # minimizing an error against graph-theoretic shortest-path distances;
        # those distances are infinite between disconnected components, which
        # gives every cross-component pair zero weight and leaves nothing to
        # keep the components apart (or even finite) -- fragments end up
        # NaN'd out or piled on top of one another. Instead, lay out each
        # connected component on its own (recursing with the same method and
        # options, where cross-component distances are never an issue), then
        # tile the independent sub-layouts on a grid so their bounding boxes
        # can never intersect.
        self.positions = self._compute_disconnected(
            method, component_ids, n_components,
            node_positions=node_positions, fix_fragment_nodes=fix_fragment_nodes, **kwargs
        )
        return self.positions

    def _validate_node_positions(self, node_positions):
        """
        **LLM Docstring**

        Normalize a `node_positions` mapping to `{label: (float, float)}`, validating that every key names a node of this graph.

        :param node_positions: A falsy value, or a mapping from node label to an (x, y) pair.
        :type node_positions: object

        :return: A normalized `{node label: (float, float)}` mapping (possibly empty).
        :rtype: dict
        """
        if not node_positions:
            return {}
        unknown = [node for node in node_positions if node not in self._index]
        if unknown:
            raise ValueError(
                f"node_positions given for node(s) not in this graph: {unknown}"
            )
        return {
            node: (float(xy[0]), float(xy[1]))
            for node, xy in node_positions.items()
        }

    # -- shared utilities -------------------------------------------------

    def shortest_path_distances(self) -> np.ndarray:
        """
        **LLM Docstring**

        Compute and copy the graph-theoretic all-pairs shortest-path distance matrix.

        :return: A square shortest-path distance matrix.
        :rtype: np.ndarray
        """
        dits = self.graph.get_distances()
        dits = dits.copy()
        return dits

    # -- disconnected-fragment handling ------------------------------------

    def _connected_component_ids(self) -> np.ndarray:
        """
        **LLM Docstring**

        Label every node with the index of the connected component it belongs to.

        :return: An integer array of length `N` giving each node's component id.
        :rtype: np.ndarray
        """
        _, comp_ids = sparse.csgraph.connected_components(
            self.graph.graph, directed=False, return_labels=True
        )
        return comp_ids

    def _sub_layout(self, node_indices: List[int]) -> "GraphLayout":
        """
        **LLM Docstring**

        Build a `GraphLayout` over the induced subgraph on the given node indices, preserving original labels and remapped weights.

        :param node_indices: Indices (into `self.nodes`) of the nodes to keep.
        :type node_indices: list

        :return: A `GraphLayout` for just those nodes and the edges between them.
        :rtype: GraphLayout
        """
        idx_set = set(node_indices)
        idx_map = {old: new for new, old in enumerate(node_indices)}
        sub_labels = [self.nodes[i] for i in node_indices]
        sub_edges = [
            (idx_map[i], idx_map[j])
            for i, j in ((int(e[0]), int(e[1])) for e in self.edges)
            if i in idx_set and j in idx_set
        ]
        sub_weights = None
        if self.weights is not None:
            sub_weights = {
                (idx_map[i], idx_map[j]): w
                for (i, j), w in self.weights.items()
                if i in idx_set and j in idx_set
            }
        sub_graph = EdgeGraph(
            sub_labels, sub_edges, directed=self.graph.directed
        )
        return GraphLayout(sub_graph, weights=sub_weights)

    def _compute_disconnected(self, method: str, component_ids: np.ndarray, n_components: int, *,
                              node_positions: Optional[Dict] = None, fix_fragment_nodes: bool = True, **kwargs):
        """
        **LLM Docstring**

        Lay out each connected component independently with `method`, then tile the sub-layouts on a non-overlapping grid.

        :param method: Layout method name already validated against the registry.
        :type method: str

        :param component_ids: Per-node connected-component index, as from `_connected_component_ids`.
        :type component_ids: np.ndarray

        :param n_components: Total number of connected components.
        :type n_components: int

        :param node_positions: Optional ``{node: (x, y)}`` positions to pin, already
            validated/normalized by `compute`. Split per-component (by label
            membership -- `_sub_layout` preserves original labels, so no
            remapping is needed) and forwarded to that component's own
            `compute` call.
        :type node_positions: dict

        :param fix_fragment_nodes: Whether a component that received any pinned
            positions above is exempted from `_tile_components`'s grid shift.
        :type fix_fragment_nodes: bool

        :param kwargs: Layout-algorithm keyword options, forwarded unchanged to each component.
        :type kwargs: object

        :return: A mapping from node labels to 2D coordinate pairs.
        :rtype: dict
        """
        node_positions = node_positions or {}
        component_indices = [
            [i for i, c in enumerate(component_ids) if c == comp_id]
            for comp_id in range(n_components)
        ]
        sub_positions = []
        fixed_flags = []
        for idxs in component_indices:
            idx_labels = {self.nodes[i] for i in idxs}
            frag_positions = {node: xy for node, xy in node_positions.items() if node in idx_labels}
            sub_positions.append(
                self._sub_layout(idxs).compute(method, node_positions=frag_positions, **kwargs)
            )
            # only a component that both got pinned nodes *and* was asked to
            # keep them fixed sits out the tiling shift below
            fixed_flags.append(bool(frag_positions) and fix_fragment_nodes)
        merged = self._tile_components(sub_positions, fixed_flags=fixed_flags)
        # dict insertion order matters downstream (it's read positionally by
        # callers like `EdgeGraph.plot`), so return the merged positions back
        # in the same node order `compute` would otherwise have produced
        return {node: merged[node] for node in self.nodes}

    @staticmethod
    def _tile_components(sub_positions: List[Dict], padding: float = 0.5,
                         fixed_flags: Optional[List[bool]] = None) -> Dict:
        """
        **LLM Docstring**

        Translate each component's layout onto a shared grid so that no two bounding boxes can intersect.

        :param sub_positions: One `{node: (x, y)}` mapping per connected component.
        :type sub_positions: list

        :param padding: Extra gap between adjacent grid cells, as a fraction of the largest component's extent.
        :type padding: float

        :param fixed_flags: One bool per entry in `sub_positions`; a `True` component
            is passed through completely unshifted (its caller-requested absolute
            coordinates are kept exactly) and isn't given a grid cell at all --
            only components with `False` are tiled/shifted. Defaults to all-`False`.
        :type fixed_flags: list

        :return: A single merged `{node: (x, y)}` mapping. Re-centered at the origin,
            unless any component is fixed -- centering would otherwise move a fixed
            component's nodes away from their exact requested coordinates.
        :rtype: dict
        """
        if fixed_flags is None:
            fixed_flags = [False] * len(sub_positions)

        boxes = []
        for pos in sub_positions:
            pts = np.array(list(pos.values()), dtype=float) if pos else np.zeros((0, 2))
            if len(pts) == 0:
                boxes.append((np.zeros(2), np.zeros(2)))
                continue
            lo = pts.min(axis=0)
            hi = pts.max(axis=0)
            boxes.append(((lo + hi) / 2.0, hi - lo))

        # every grid cell is sized to the single largest *movable* component so
        # that, wherever it lands, its bounding box fits inside its cell --
        # this is what makes the non-overlap guarantee independent of cell
        # contents. A fixed component never occupies a cell (it isn't moved
        # at all), so its size shouldn't inflate the grid built for the rest.
        movable_sizes = [size for size, fixed in zip((s for _, s in boxes), fixed_flags) if not fixed]
        max_extent = max((float(np.max(size)) for size in movable_sizes), default=0.0)
        if max_extent <= 0:
            max_extent = 1.0
        cell = max_extent * (1.0 + padding)

        n_movable = sum(1 for fixed in fixed_flags if not fixed)
        cols = max(1, int(math.ceil(math.sqrt(n_movable)))) if n_movable else 1

        merged = {}
        grid_k = 0
        for pos, (center, _size), fixed in zip(sub_positions, boxes, fixed_flags):
            if fixed:
                # honor the caller's exact requested coordinates: no shift,
                # and no grid cell taken up by this component at all
                for node, xy in pos.items():
                    merged[node] = tuple(np.asarray(xy, dtype=float))
                continue
            row, col = divmod(grid_k, cols)
            grid_k += 1
            offset = np.array([col * cell, -row * cell])
            for node, xy in pos.items():
                merged[node] = tuple(np.asarray(xy, dtype=float) - center + offset)

        if merged and not any(fixed_flags):
            # only recenter at the origin when nothing is pinned -- doing this
            # unconditionally would silently move a fixed component's nodes
            # away from the exact coordinates the caller asked for
            pts = np.array(list(merged.values()))
            shift = pts.mean(axis=0)
            merged = {node: tuple(np.asarray(xy) - shift) for node, xy in merged.items()}
        return merged

# ---------------------------------------------------------------------------
# Plugin: circular layout (trivial baseline, shows the dispatch mechanism)
# ---------------------------------------------------------------------------

@GraphLayout.register("circular")
def circular_layout(layout: GraphLayout, scale: float = 1.0,
                    node_positions: Optional[Dict[Node, Position]] = None,
                    meta: Optional[Dict] = None):
    """
    **LLM Docstring**

    Place graph nodes evenly around a circle of the requested radius.

    :param layout: Layout object whose nodes and graph data are used.
    :type layout: GraphLayout

    :param scale: Overall layout radius or target size.
    :type scale: float

    :param node_positions: Optional ``{node: (x, y)}`` pins. A pinned node is placed
        at its given position instead of its circle point; every other node still
        gets its usual, evenly-spaced circle point (there's no optimization step
        here to "work around" the pin with, unlike `kamada_kawai_layout`).
    :type node_positions: dict

    :param meta: Graph-supplied config dict (see the `GraphLayout` class docstring).
        Unused here -- accepted for interface consistency with every other
        registered layout method.
    :type meta: dict

    :return: A node-to-coordinate mapping.
    :rtype: dict
    """
    n = len(layout.nodes)
    if n == 0:
        return {}
    node_positions = node_positions or {}
    positions = {}
    for i, node in enumerate(layout.nodes):
        if node in node_positions:
            positions[node] = node_positions[node]
            continue
        angle = 2 * math.pi * i / n
        positions[node] = (scale * math.cos(angle), scale * math.sin(angle))
    return positions


# ---------------------------------------------------------------------------
# Plugin: Kamada-Kawai layout
# ---------------------------------------------------------------------------

@GraphLayout.register("kamada_kawai")
def kamada_kawai_layout(
    layout: GraphLayout,
    scale: float = 1.0,
    iterations: int = 300,
    tol: float = 1e-9,
    seed: Optional[int] = None,
    node_positions: Optional[Dict[Node, Position]] = None,
    meta: Optional[Dict] = None,
) -> Dict[Node, Position]:
    """
    Basic Kamada-Kawai layout, minimizing the stress function

        E = sum_{i<j} k_ij * (|p_i - p_j| - L_ij)^2

    where L_ij is the graph-theoretic shortest-path distance between nodes
    i and j (rescaled to `scale`), and k_ij = 1 / L_ij^2 is a spring
    strength that penalizes errors on close pairs more heavily than errors
    on far-apart pairs.

    The original Kamada-Kawai paper minimizes E with Newton-Raphson, moving
    one node at a time. Here we use stress majorization (the SMACOF update,
    also how most modern implementations solve this in practice) instead:
    it minimizes the same E, updates all nodes at once each iteration, and
    is guaranteed to never increase E at any step -- so unlike plain
    gradient descent it needs no learning-rate tuning and won't diverge.

    Update rule (for each node i, holding all other nodes fixed):

        p_i <- ( sum_j k_ij * (p_j + L_ij * (p_i - p_j) / |p_i - p_j|) )
               ---------------------------------------------------------
                                  sum_j k_ij

    `node_positions` pins a subset of nodes: they're seeded at their given
    position instead of the initial circle, and after every SMACOF update
    their rows are snapped back to that position before the next iteration
    -- so they act purely as anchors (their `p_j` still pulls on every other
    node's update through `K`/`L` above) and never move themselves. This is
    the standard way to add fixed-node constraints to stress majorization:
    it's still minimizing the same E, just over the free nodes only.

    `meta` (graph-supplied config, see the `GraphLayout` class docstring) is
    accepted but unused here -- for interface consistency with every other
    registered layout method.
    """
    rng = random.Random(seed)
    n = len(layout.nodes)
    if n == 0:
        return {}

    node_positions = node_positions or {}
    fixed_mask = np.zeros(n, dtype=bool)
    fixed_xy = np.zeros((n, 2))
    for node, xy in node_positions.items():
        i = layout._index[node]
        fixed_mask[i] = True
        fixed_xy[i] = xy

    if n == 1:
        if fixed_mask[0]:
            return {layout.nodes[0]: (float(fixed_xy[0, 0]), float(fixed_xy[0, 1]))}
        return {layout.nodes[0]: (0.0, 0.0)}

    D = layout.shortest_path_distances()
    d_max = D[np.isfinite(D)].max()
    d_max = d_max if d_max > 0 else 1.0

    # Target Euclidean distances, scaled to the requested layout size.
    L = scale * D / d_max
    with np.errstate(divide="ignore"):
        K = np.where(L > 0, 1.0 / (L ** 2), 0.0)
    np.fill_diagonal(K, 0.0)
    w_sum = K.sum(axis=1)  # sum_j k_ij, per node i

    # Initialize on a circle (jittered) rather than pure random; this
    # avoids degenerate overlapping starts and speeds up convergence.
    pos = np.zeros((n, 2))
    for i in range(n):
        angle = 2 * math.pi * i / n
        jitter = rng.uniform(-1e-3, 1e-3)
        pos[i] = [scale * math.cos(angle) + jitter, scale * math.sin(angle) + jitter]
    if fixed_mask.any():
        # seed pinned nodes at their exact requested position, not the circle
        pos[fixed_mask] = fixed_xy[fixed_mask]
        if fixed_mask.all():
            # nothing left to optimize -- every node is pinned
            return {node: (float(pos[i, 0]), float(pos[i, 1])) for i, node in enumerate(layout.nodes)}

    def stress(p: np.ndarray) -> float:
        """
        **LLM Docstring**

        Evaluate the weighted Kamada-Kawai stress of a candidate 2D embedding.

        :param p: Candidate coordinates with shape `(n_nodes, 2)`.
        :type p: np.ndarray

        :return: The scalar weighted stress.
        :rtype: object
        """
        diff = p[:, None, :] - p[None, :, :]
        dist = np.linalg.norm(diff, axis=2)
        return float(np.sum(K * (dist - L) ** 2)) / 2.0

    prev_stress = stress(pos)
    for _ in range(iterations):
        diff = pos[:, None, :] - pos[None, :, :]     # (n, n, 2): p_i - p_j
        dist = np.linalg.norm(diff, axis=2)
        np.fill_diagonal(dist, 1.0)                   # avoid div-by-zero; K's diagonal is 0

        # "term_ij" = p_j + L_ij * (p_i - p_j) / dist_ij, weighted by k_ij
        unit = diff / dist[:, :, None]
        term = pos[None, :, :] + L[:, :, None] * unit  # (n, n, 2)
        numerator = np.einsum("ij,ijk->ik", K, term)     # (n, 2)

        pos = numerator / w_sum[:, None]
        if fixed_mask.any():
            # hold pinned nodes exactly at their requested position -- only
            # the free nodes actually move; the pinned ones still act as
            # anchors pulling on their neighbors via K/L above
            pos[fixed_mask] = fixed_xy[fixed_mask]

        cur_stress = stress(pos)
        if abs(prev_stress - cur_stress) < tol:
            break
        prev_stress = cur_stress

    return {node: (float(pos[i, 0]), float(pos[i, 1])) for i, node in enumerate(layout.nodes)}


# ---------------------------------------------------------------------------
# Plugin: stacked-layer layout (feed-forward-network-style diagrams)
# ---------------------------------------------------------------------------

@GraphLayout.register("stacked_layer")
def stacked_layer_layout(
    layout: GraphLayout,
    layer_sizes: Optional[Iterable[int]] = None,
    layer_spacing: float = 1.0,
    node_spacing: float = 1.0,
    layer_direction: float = 1.0,
    node_positions: Optional[Dict[Node, Position]] = None,
    meta: Optional[Dict] = None,
) -> Dict[Node, Position]:
    """
    Lay nodes out in horizontal stacks -- one row per layer -- the layout
    counterpart of `EdgeGraph.stacked_graph`: nothing here looks at the
    graph's edges at all, only at how many nodes belong to each layer, so
    it works equally well on a stack built by `stacked_graph` or on any
    other graph whose nodes happen to be grouped layer by layer.

    Nodes are assumed to be listed layer by layer, in `layout.nodes` order
    (i.e. `EdgeGraph.labels` order) -- exactly how `stacked_graph` builds
    them. `layer_sizes` says how to slice that flat list back into layers;
    if omitted, it falls back to `meta['layer_sizes']` (`meta` itself
    defaults to `layout.graph.meta`, populated automatically by
    `stacked_graph` -- see the `GraphLayout` class docstring), and only
    raises if neither is available.

    Within a layer, its `n` nodes are centered on `x = 0` and spaced
    `node_spacing` apart: node `i` of `n` sits at
    `x = (i - (n - 1) / 2) * node_spacing`. Layers are stacked along `y`,
    `layer_spacing` apart, in the order given, scaled by `layer_direction`
    (`+1`, the default, stacks layer 0 at the bottom and later layers
    upward; `-1` flips that -- e.g. to draw an "input on top" diagram).

    :param layout: Layout object whose nodes are grouped layer by layer.
    :type layout: GraphLayout

    :param layer_sizes: Node count per layer, summing to `len(layout.nodes)`.
        Defaults to `meta['layer_sizes']` when available.
    :type layer_sizes: Iterable[int]

    :param layer_spacing: Vertical gap between adjacent layers.
    :type layer_spacing: float

    :param node_spacing: Horizontal gap between adjacent nodes within a layer.
    :type node_spacing: float

    :param layer_direction: `+1` to stack layer 0 at the bottom and later
        layers upward, `-1` to flip the stack top-to-bottom.
    :type layer_direction: float

    :param node_positions: Optional ``{node: (x, y)}`` pins, honored the same
        way as in `circular_layout`/`kamada_kawai_layout`: a pinned node is
        placed at its given position instead of its regular stack slot.
    :type node_positions: dict

    :param meta: Graph-supplied config dict (see the `GraphLayout` class
        docstring); this is where `layer_sizes` is read from when not passed
        explicitly. Defaults to `layout.graph.meta`.
    :type meta: dict

    :return: A node-to-coordinate mapping.
    :rtype: dict
    """
    n = len(layout.nodes)
    if n == 0:
        return {}

    if layer_sizes is None:
        layer_sizes = (meta or {}).get('layer_sizes')
    if layer_sizes is None:
        raise ValueError(
            "`stacked_layer` layout needs `layer_sizes` (nodes per layer, "
            "in stacking order); pass it explicitly, pass it via `meta={'layer_sizes': ...}`, "
            "or build the graph with `EdgeGraph.stacked_graph`, which sets "
            "`graph.meta['layer_sizes']` automatically"
        )
    layer_sizes = [int(s) for s in layer_sizes]
    if sum(layer_sizes) != n:
        raise ValueError(
            f"`layer_sizes` {layer_sizes} totals {sum(layer_sizes)} nodes, "
            f"but the graph has {n}"
        )

    node_positions = node_positions or {}
    positions = {}
    idx = 0
    for l, size in enumerate(layer_sizes):
        y = layer_direction * layer_spacing * l
        for i in range(size):
            node = layout.nodes[idx]
            if node in node_positions:
                positions[node] = node_positions[node]
            else:
                x = (i - (size - 1) / 2.0) * node_spacing
                positions[node] = (x, y)
            idx += 1
    return positions


class GraphPlotter:
    """
    Flat 2D drawing of an ``EdgeGraph`` on a `Graphics` (2D) SVG backend -- the
    graph-layout analogue of ``SVG2DMoleculePlotter``.

    Where the molecule plotter *derives* node positions from a 3D geometry (via a
    principal-axis embedding + bond-length relaxation), this one is simply handed
    the layout::

        GraphPlotter(graph, coords).plot(**styles)

    ``coords`` is an ``(N, 2)`` array of node positions -- row ``i`` is node ``i`` --
    and ``graph`` is an ``EdgeGraph`` whose edges connect those nodes. Nodes are
    drawn as `Disk`s and edges as `Line`s.

    Labels are **off** by default (the graph analogue of leaving carbons/hydrogens
    implicit). Pass ``label_function`` to turn them on: it is called once per node,
    and every node for which it returns a non-``None`` value gets that value drawn
    as `Text` next to the node. A callable return value is instead invoked with the
    resolved label position and may return one graphics primitive, an SVG primitive,
    or a list/tuple of primitives. Returning ``None`` skips the label for that node,
    so a single function can label some nodes and not others.

    Mirrors the primitive/style handling of the molecule plotter: `_clean_style`
    (folds ``glow`` into a stroke), `_plot_range_2d`, half-colored edges, edge
    trimming back to the node radius, per-item + highlight styling, and the
    ``figure`` / ``objects`` / ``return_objects`` plumbing. What's graph-specific
    lives here: node/edge extraction from the graph, the optional ``pose``
    transform of an already-2D layout, and the flat `Disk`/`Line`/`Text` builders.

    Per-node / per-edge styles (``node_style`` / ``edge_style``) accept:
        * a single ``dict``            -> applied to every item,
        * a ``list``/``tuple`` of dicts -> indexed positionally, or
        * a ``callable(i) -> dict``     -> called per item.
    A ``'color'`` in an item's style wins over the base color; a ``'modifier'``
    callable ``(idx, obj, style) -> style`` is applied last, exactly as in the 3D
    path.

    Weighted graphs map their drawn weights linearly onto `weight_linewidth`
    (default ``(.01, .1)``). Missing entries in a partial weight mapping count
    as 1. Pass ``weight_linewidth=None`` to disable weight-based widths. An
    explicit width in an edge's `edge_style` takes precedence over its weight.
    This behavior is independent of whether the weights are also used by the
    selected layout method.

    Directed graphs render each stored ``(i, j)`` edge as an arrow from node
    ``i`` to node ``j`` by default; ``directed_edges`` can explicitly enable
    or disable arrows. Arrow tips use the same node-radius trimming as ordinary
    edges. With ``half_colored_edges=True``, the first half remains a line and
    the destination-colored second half carries the arrowhead.

    ``node_edge_offset`` adds spacing between an edge and its endpoint nodes.
    A scalar applies at both ends; ``(source_offset, destination_offset)``
    controls them independently. Positive offsets create a gap and negative
    offsets extend the edge into the node. Directed SVG edges also compensate
    automatically for the portion of the marker extending beyond its reference
    point, so the arrow tip -- rather than the line endpoint -- lands on the
    destination node boundary. The explicit destination offset is added to that
    automatic compensation.

    Draw order / layering: nodes, edges, and labels each paint in the category
    order given by ``draw_order`` (default ``('edges', 'nodes', 'labels')`` --
    edges paint first/underneath, so nodes overlap the edges that meet them,
    rather than the reverse). Pass e.g. ``draw_order=('nodes', 'edges',
    'labels')`` to flip that. For finer control than a whole category at a
    time, a ``'z_index'`` entry in any item's ``node_style`` / ``edge_style``
    / ``label_style`` (or set directly as an attribute on a primitive returned
    by ``annotation_function``) overrides that one item's category default,
    and is compared against *every* other item, node/edge/label/annotation
    alike -- so a single highlighted edge can be pushed above every node
    (``highlight_style={'z_index': 100, ...}``), or one background annotation
    pinned beneath everything, without touching `draw_order`. Ties (equal
    ``z_index``, including two untouched items of the same category) keep
    the category order, then each item's original position within it.
    """
    modes = ('svg2d',)
    subthemes = {
        'default': {
            'node_radius': .02,
            'disk_options': {'line_thickness': '.005px', 'line_color': 'black'},
            'line_options': {'line_thickness': '.005px', 'line_color': 'black'},
            'label_style': {'font_size': 6},
            'node_color': '#4C72B0',
            'edge_color': 'black',
            'highlight_style': {'stroke': '#d62728', 'color': '#d62728'},
        }
    }

    def __init__(self, graph, coords):
        """
        **LLM Docstring**

        Store a graph and validate that its supplied coordinates have shape `(N, 2)`.

        :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
        :type graph: object

        :param coords: Node coordinates.
        :type coords: object

        :return: No value is returned.
        :rtype: None
        """
        self.graph = graph
        self.coords = np.asanyarray(coords, dtype=float)
        if self.coords.ndim != 2 or self.coords.shape[1] != 2:
            raise ValueError(
                f"coords must be an (N, 2) layout; got shape {self.coords.shape}"
            )

    # ------------------------------------------------------------------ #
    #  Graph -> nodes / edges
    # ------------------------------------------------------------------ #
    @property
    def nodes(self):
        """
        **LLM Docstring**

        Resolve node identities from `graph.labels`, `graph.nodes`, `graph.node_list`,
        or positional indices.

        :return: A list of node identities.
        :rtype: object
        """
        # node identities (labels/keys); positions are always self.coords[i].
        # `.labels` is what `EdgeGraph` (the only graph type this actually gets
        # constructed with in this package) uses; `.nodes`/`.node_list` are
        # checked too for any other duck-typed graph object that happens to
        # expose one of those names instead.
        nodes = getattr(self.graph, 'labels', None)
        if nodes is None:
            nodes = getattr(self.graph, 'nodes', None)
        if nodes is None:
            nodes = getattr(self.graph, 'node_list', None)
        if nodes is None:
            return list(range(len(self.coords)))
        return list(nodes)

    def _edge_list(self, edges):
        """
        Normalize to a list of ``(i, j, data)`` triples of integer node indices.
        ``edges=None`` pulls them off the graph; ``edges=False`` draws none;
        an explicit iterable overrides the graph entirely.
        """
        if edges is False:
            return []
        if edges is None:
            edges = getattr(self.graph, 'edges', None)
            if edges is None:
                edges = getattr(self.graph, 'edge_list', None)
            if callable(edges):
                edges = edges()
        if edges is None:
            raise ValueError(
                "couldn't find an edge list on the graph; pass edges=[...] explicitly"
            )
        out = []
        for e in edges:
            e = tuple(e)
            i, j = int(e[0]), int(e[1])
            data = e[2] if len(e) > 2 else None
            out.append((i, j, data))
        return out

    # ------------------------------------------------------------------ #
    #  Layout / pose  (coords are already 2D, so this is just a transform)
    # ------------------------------------------------------------------ #
    def _apply_pose(self, coords, masses=None, pose=None, principal_axis_order=(0, 1)):
        """
        **LLM Docstring**

        Convert or transform coordinates into a 2D plotting pose using principal axes, an explicit projection, or a callback.

        :param coords: Node coordinates.
        :type coords: object

        :param masses: Optional per-node masses used for center-of-mass and inertia calculations.
        :type masses: object

        :param pose: A callable, explicit coordinates, or projection/rotation matrix selecting the plotted pose.
        :type pose: object

        :param principal_axis_order: Two principal-axis indices to retain in the 2D projection.
        :type principal_axis_order: object

        :return: An array with shape `(N, 2)`.
        :rtype: object
        """
        coords = np.asanyarray(coords, dtype=float)
        if coords.shape[-1] == 2:
            coords = np.pad(coords, [[0, 0], [0, 1]])
        i, j = principal_axis_order

        def _pa_project(c):
            """
            **LLM Docstring**

            Center 3D coordinates, rotate into principal axes, and select two requested axes.

            :param c: Coordinates with shape `(N, 3)` to center and project.
            :type c: object

            :return: Principal-axis coordinates with shape `(N, 2)`.
            :rtype: object
            """
            com = nput.center_of_mass(c, masses)
            _, axes = nput.moments_of_inertia(c, masses)  # ascending moment; cols=axes
            proj = (c - com[np.newaxis, :]) @ axes
            return np.stack([proj[:, i], proj[:, j]], axis=-1)

        if pose is None:
            # capture the *specific* com/axes this point cloud resolved to as a
            # standalone closure, not just the projected result -- so a caller
            # can pull it back out (see `plot()`'s `figure.graph_pose`) and
            # reapply this exact transform to a DIFFERENT point cloud later
            # (e.g. a second, overlaid plot), instead of that second call
            # computing its own, generally-different, independent PCA pose
            # from its own (typically smaller/differently-centered) points.
            com = nput.center_of_mass(coords, masses)
            _, axes = nput.moments_of_inertia(coords, masses)

            def _resolved_pose(c, _com=com, _axes=axes, _i=i, _j=j):
                c = np.asanyarray(c, dtype=float)
                if c.shape[-1] == 2:
                    c = np.pad(c, [[0, 0], [0, 1]])
                proj = (c - _com[np.newaxis, :]) @ _axes
                return np.stack([proj[:, _i], proj[:, _j]], axis=-1)

            self._resolved_pose = _resolved_pose
            proj = (coords - com[np.newaxis, :]) @ axes
            return np.stack([proj[:, i], proj[:, j]], axis=-1)
        if callable(pose):
            # already a standalone, reapplicable transform -- surface it as-is
            self._resolved_pose = pose
            return np.asanyarray(pose(coords), dtype=float)

        arr = np.asanyarray(pose, dtype=float)
        n = len(coords)
        if arr.ndim == 2 and arr.shape == (n, 2):
            return arr
        if arr.ndim == 2 and arr.shape == (2, 3):
            com = nput.center_of_mass(coords, masses)
            return (coords - com[np.newaxis, :]) @ arr.T
        if arr.ndim == 2 and arr.shape == (3, 3):
            com = nput.center_of_mass(coords, masses)
            proj = (coords - com[np.newaxis, :]) @ arr
            return np.stack([proj[:, i], proj[:, j]], axis=-1)
        if arr.ndim == 2 and arr.shape == (n, 3):
            return _pa_project(arr)
        raise ValueError(
            f"can't interpret pose of shape {arr.shape} for {n} atoms; "
            "expected (N,2), (N,3), (2,3), (3,3), or a callable"
        )

    # ------------------------------------------------------------------ #
    #  Style helpers  (mirror the 3D style handling)
    # ------------------------------------------------------------------ #
    _style_map = {
        # 'edgecolor': 'stroke',
        # 'edgecolors': 'stroke',
        # 'lw': 'stroke-width',
        # 'color': 'fill',
        'line_color': 'stroke',
        'line_width': 'stroke-width',
        'line_thickness': 'stroke-width'
    }
    @classmethod
    def _remap_style_names(cls, sty):
        return {
            cls._style_map.get(k, k): v
            for k, v in sty.items()
        }
    @classmethod
    def _clean_style(cls, sty):
        """
        **LLM Docstring**

        Translate an unsupported `glow` style into a stroke color when no stroke is already specified.

        :param sty: Style mapping to copy and normalize.
        :type sty: object

        :return: A normalized style dictionary.
        :rtype: object
        """
        # 2D Disk/Line don't take `glow`; fold it into a stroke outline instead
        sty = cls._remap_style_names(sty)
        glow = sty.pop('glow', None)
        if glow is not None and 'stroke' not in sty:
            sty['stroke'] = glow
        return sty

    @staticmethod
    def _normalize_styles(style, n):
        """global dict / per-item list / callable  ->  list of n dicts"""
        if style is None:
            return [dict() for _ in range(n)]
        if callable(style):
            return [dict(style(i) or {}) for i in range(n)]
        if isinstance(style, (list, tuple)):
            out = [dict(style[i]) if i < len(style) and style[i] else {} for i in range(n)]
            return out
        # a single dict -> shared across all items
        return [dict(style) for _ in range(n)]

    def _apply_highlights(self, styles, highlight, highlight_style, lookup=None):
        """merge `highlight_style` into the styles of the highlighted items"""
        if not highlight:
            return styles
        for h in highlight:
            idx = lookup[h] if (lookup is not None and h in lookup) else h
            if isinstance(idx, (int, np.integer)) and 0 <= idx < len(styles):
                merged = dict(highlight_style)
                merged.update(styles[idx])          # explicit per-item still wins
                styles[idx] = merged
        return styles

    def _plot_range_2d(self, xy, radii, plot_range_padding):
        """
        **LLM Docstring**

        Compute axis limits enclosing all coordinates with fixed, automatic, or zero padding.

        :param xy: Planar node coordinates with shape `(N, 2)`.
        :type xy: object

        :param radii: Per-node disk radii.
        :type radii: object

        :param plot_range_padding: Numeric padding, `None`, or `"auto"` based on the largest node radius.
        :type plot_range_padding: object

        :return: Two `[minimum, maximum]` axis intervals.
        :rtype: object
        """
        lo = np.min(xy, axis=0)
        hi = np.max(xy, axis=0)
        if plot_range_padding is None:
            pad = 0.0
        elif isinstance(plot_range_padding, str) and plot_range_padding == 'auto':
            pad = float(np.max(radii)) * 1.5
        else:
            pad = plot_range_padding

        if nput.is_numeric(pad):
            pad = [pad, pad]
        xpad, ypad = pad
        if nput.is_numeric(xpad):
            xpad = [xpad, xpad]
        if nput.is_numeric(ypad):
            ypad = [ypad, ypad]
        lpad, rpad = xpad
        bpad, hpad = ypad
        return [[lo[0] - lpad, hi[0] + rpad], [lo[1] - bpad, hi[1] + hpad]]

    def _get_node_radii(self, node_radius, n):
        """
        **LLM Docstring**

        Normalize a scalar or length-`N` node-radius specification to a NumPy vector.

        :param node_radius: Scalar radius or length-`N` radius vector.
        :type node_radius: object

        :param n: Number of items to normalize or process.
        :type n: object

        :return: A float array of length `N`.
        :rtype: object
        """
        if node_radius is None:
            node_radius = self.subthemes['default']['node_radius']
        if np.ndim(node_radius) == 0:
            return np.full(n, float(node_radius))
        r = np.asanyarray(node_radius, dtype=float)
        if r.shape != (n,):
            raise ValueError(f"node_radius must be scalar or length {n}; got {r.shape}")
        return r

    # ------------------------------------------------------------------ #
    #  2D primitive builders
    # ------------------------------------------------------------------ #
    def _get_node_primitives_2d(self, xy, radii, colors, node_style, drawn, *,
                                disk_class, disk_options, theme_function, plotos,
                                default_z=0):
        """
        **LLM Docstring**

        Build disk primitives for enabled nodes after applying per-node colors, radii, modifiers, and theme hooks.

        :param xy: Planar node coordinates with shape `(N, 2)`.
        :type xy: object

        :param radii: Per-node disk radii.
        :type radii: object

        :param colors: Per-node base colors.
        :type colors: object

        :param node_style: Normalized per-node style dictionaries.
        :type node_style: object

        :param drawn: Boolean mask indicating which node glyphs are drawn.
        :type drawn: object

        :param disk_class: Primitive class used to construct node disks.
        :type disk_class: object

        :param disk_options: Base keyword options for every disk primitive.
        :type disk_options: object

        :param theme_function: Optional callback that can rewrite primitive styles before construction.
        :type theme_function: object

        :param plotos: Remaining primitive keyword options shared by all generated objects.
        :type plotos: object

        :param default_z: Draw-order/z-index this node's category paints at when
            its style doesn't override it with its own `'z_index'`.
        :type default_z: object

        :return: A list of disk primitives, each carrying a resolved `.z_index`.
        :rtype: object
        """
        prims = []
        base = dict(disk_options)
        for i, (coord, r, color, sty0) in enumerate(zip(xy, radii, colors, node_style)):
            if not drawn[i]:
                continue
            sty = dict(sty0)
            modifier = sty.pop('modifier', None)
            col = sty.pop('color', None) or color
            rr = sty.pop('radius', r)
            zi = sty.pop('z_index', None)
            if modifier is not None:
                sty = modifier(i, self.nodes[i], dict(sty, color=col))
                col = sty.pop('color', col)
                rr = sty.pop('radius', rr)
                zi = sty.pop('z_index', zi)
            full = (plotos | base | {'color': col} | sty)
            full = self._clean_style(full)
            if theme_function is not None:
                full = theme_function(i, disk_class, full)
            prim = disk_class(np.asanyarray(coord), float(rr), **full)
            prim.z_index = default_z if zi is None else zi
            prims.append(prim)
        return prims

    def _get_edge_primitives_2d(self, xy, edges, radii, colors, node_style, drawn, *,
                                line_class, edge_style, edge_color, line_options,
                                trim_edges, node_edge_offset, half_colored_edges, weight_linewidth,
                                directed_edges, arrow_class, arrow_options, theme_function, plotos,
                                default_z=0):
        """
        **LLM Docstring**

        Build line primitives for graph edges, optionally trimming them to node disks and splitting each edge into endpoint-colored halves.

        :param xy: Planar node coordinates with shape `(N, 2)`.
        :type xy: object

        :param edges: Undirected edges as endpoint pairs, optionally carrying weights.
        :type edges: object

        :param radii: Per-node disk radii.
        :type radii: object

        :param colors: Per-node base colors.
        :type colors: object

        :param node_style: Normalized per-node style dictionaries.
        :type node_style: object

        :param drawn: Boolean mask indicating which node glyphs are drawn.
        :type drawn: object

        :param line_class: Primitive class used to construct graph edges.
        :type line_class: object

        :param edge_style: Per-edge styles keyed by index or endpoint pair.
        :type edge_style: object

        :param edge_color: Fallback color for edges that are not endpoint-colored.
        :type edge_color: object

        :param line_options: Base keyword options for every line primitive.
        :type line_options: object

        :param trim_edges: Whether edge endpoints are shortened by the radii of drawn nodes.
        :type trim_edges: object

        :param node_edge_offset: Additional source/destination endpoint spacing,
            as one number for both ends or a `(source, destination)` pair.
            Positive values create a gap; negative values overlap the node. For
            directed SVG edges, the destination value is added to the automatic
            marker-tip compensation.
        :type node_edge_offset: float | tuple[float, float]

        :param half_colored_edges: Whether each edge is split at its midpoint and colored by its endpoint nodes.
        :type half_colored_edges: object

        :param weight_linewidth: Minimum and maximum line widths used to visualize graph weights, or `None`.
        :type weight_linewidth: tuple[float, float] | None

        :param directed_edges: Whether to draw each `(i, j)` edge as an arrow from `i` to `j`.
        :type directed_edges: bool

        :param arrow_class: Primitive class used for directed edges.
        :type arrow_class: object

        :param arrow_options: Additional options applied only to arrow primitives.
        :type arrow_options: dict

        :param theme_function: Optional callback that can rewrite primitive styles before construction.
        :type theme_function: object

        :param plotos: Remaining primitive keyword options shared by all generated objects.
        :type plotos: object

        :param default_z: Draw-order/z-index this edge's category paints at when
            its style doesn't override it with its own `'z_index'`.
        :type default_z: object

        :return: A list of line primitives, each carrying a resolved `.z_index`.
        :rtype: object
        """
        prims = []
        base = dict(line_options)
        arrow_options = self._clean_style(dict(arrow_options))

        def marker_forward_offset(style):
            """Return the distance from an SVG marker's reference point to its tip."""
            if 'marker' in arrow_options:
                # An opaque marker URL provides no geometry to inspect. In that
                # case callers can still supply the required spacing explicitly
                # through node_edge_offset.
                return 0.0

            marker = dict(
                viewBox="0 0 10 10",
                refX="5",
                markerWidth="2",
                markerHeight="5",
                markerUnits="strokeWidth"
            )
            custom_marker = arrow_options.get('arrowhead')
            if custom_marker is not None:
                marker.update(custom_marker)

            def number(value):
                if isinstance(value, str):
                    value = value.strip()
                    if value.endswith('px'):
                        value = value[:-2]
                return float(value)

            try:
                view_x, _view_y, view_width, view_height = map(
                    number, str(marker['viewBox']).replace(',', ' ').split()
                )
                ref_x = number(marker['refX'])
                marker_width = number(marker['markerWidth'])
                marker_height = number(marker['markerHeight'])
                stroke_width = number(style.get('stroke-width', 0))
            except (KeyError, TypeError, ValueError):
                # Custom CSS lengths and externally defined markers cannot be
                # converted reliably in graph-coordinate space.
                return 0.0
            if view_width <= 0 or view_height <= 0:
                return 0.0

            preserve = str(marker.get('preserveAspectRatio', 'xMidYMid meet'))
            if preserve.strip() == 'none':
                scale = marker_width / view_width
            elif 'slice' in preserve.split():
                scale = max(marker_width / view_width, marker_height / view_height)
            else:
                scale = min(marker_width / view_width, marker_height / view_height)
            if marker.get('markerUnits', 'strokeWidth') == 'strokeWidth':
                scale *= stroke_width
            return max(0.0, (view_x + view_width - ref_x) * scale)

        if node_edge_offset is None:
            node_edge_offset = 0
        node_edge_offsets = np.asanyarray(node_edge_offset, dtype=float)
        if node_edge_offsets.ndim == 0:
            node_edge_offsets = np.repeat(node_edge_offsets, 2)
        if node_edge_offsets.shape != (2,):
            raise ValueError(
                "node_edge_offset must be a number or a "
                f"(source, destination) pair; got shape {node_edge_offsets.shape}"
            )
        # allow keying edge_style by edge index OR by (i, j) tuple
        by_index = edge_style if isinstance(edge_style, (list, tuple)) else None
        by_pair = edge_style if isinstance(edge_style, dict) else {}

        edge_widths = None
        graph_weights = getattr(self.graph, 'weights', None)
        if graph_weights is not None and weight_linewidth is not None and len(edges):
            lo, hi = map(float, weight_linewidth)
            if lo < 0 or hi < lo:
                raise ValueError(
                    "weight_linewidth must be an increasing pair of non-negative widths"
                )
            if hasattr(graph_weights, 'get'):
                drawn_weights = np.array([
                    graph_weights.get((i, j), graph_weights.get((j, i), 1.0))
                    for i, j, _ in edges
                ], dtype=float)
            else:
                graph_weights = np.asanyarray(graph_weights, dtype=float)
                if len(graph_weights) != len(edges):
                    raise ValueError(
                        f"got {len(graph_weights)} graph weights for {len(edges)} drawn edges"
                    )
                drawn_weights = graph_weights
            if not np.all(np.isfinite(drawn_weights)):
                raise ValueError("edge weights must be finite to determine line widths")
            wmin = np.min(drawn_weights)
            wmax = np.max(drawn_weights)
            if wmax == wmin:
                edge_widths = np.full(len(edges), (lo + hi) / 2)
            else:
                edge_widths = lo + (hi - lo) * (
                    (drawn_weights - wmin) / (wmax - wmin)
                )

        if isinstance(edge_style, dict):
            global_edge_style = {k:v for k,v in edge_style.items() if isinstance(k, str)}
        else:
            global_edge_style = {}

        for e_i, (i, j, offset) in enumerate(edges):
            pi, pj = xy[i], xy[j]
            d = pj - pi
            L = np.linalg.norm(d)
            if L < 1e-8:
                continue
            u = d / L
            if offset:
                # a numeric edge `data` value is treated as a perpendicular nudge,
                # so parallel/multi-edges between the same node pair fan out
                # instead of rendering exactly on top of one another
                perp = np.array([-u[1], u[0]]) * offset
                pi, pj = pi + perp, pj + perp

            # resolve this edge's style: (i,j)/(j,i) tuple key, or positional list
            if by_index is not None and e_i < len(by_index) and by_index[e_i]:
                e_sty = global_edge_style | by_index[e_i]
            else:
                e_sty = (
                        global_edge_style
                        | by_pair.get((j, i), {})
                        | by_pair.get((i, j), {})
                )
            explicit_width = any(
                key in e_sty
                for key in ('line_thickness', 'line_width', 'stroke-width', 'linewidth', 'lw')
            )
            if edge_widths is not None and not explicit_width:
                e_sty['line_thickness'] = float(edge_widths[e_i])

            zi = e_sty.pop('z_index', None)
            mod = e_sty.pop('modifier', None)
            if mod is not None:
                e_sty = mod((i, j), (self.nodes[i], self.nodes[j]), e_sty)
                zi = e_sty.pop('z_index', zi)
            e_sty = self._clean_style(e_sty)
            plotos = self._clean_style(plotos)
            base = self._clean_style(base)
            z_val = default_z if zi is None else zi

            # Trim to the node disk, then move a directed edge's SVG line
            # endpoint back by the marker's forward overhang. With the default
            # midpoint-referenced marker the shaft stops under the wide middle
            # of the triangle while its tip still touches the node boundary.
            source_offset = node_edge_offsets[0]
            destination_offset = node_edge_offsets[1]
            if trim_edges and drawn[i]:
                source_offset += radii[i]
            if trim_edges and drawn[j]:
                destination_offset += radii[j]
            if directed_edges:
                destination_offset += marker_forward_offset(
                    plotos | base | e_sty | arrow_options
                )
            start = pi + u * source_offset
            end = pj - u * destination_offset

            if half_colored_edges and 'color' not in e_sty:
                # color each half by its endpoint node -> reads like the CPK bonds
                mid = (start + end) / 2
                segments = (
                    ([start, mid], colors[i], False),
                    ([mid, end], colors[j], directed_edges)
                )
                for pts, c, use_arrow in segments:
                    primitive_class = arrow_class if use_arrow else line_class
                    sty = (plotos | base | {'color': c} | e_sty)
                    if use_arrow:
                        sty |= arrow_options
                    if theme_function is not None:
                        sty = theme_function((i, j), primitive_class, sty)
                    if use_arrow:
                        prim = primitive_class(pts[0], pts[1], **sty)
                    else:
                        prim = primitive_class(np.array(pts), **sty)
                    prim.z_index = z_val
                    prims.append(prim)
            else:
                sty = (plotos | base | e_sty)
                sty.setdefault('color', edge_color)
                primitive_class = arrow_class if directed_edges else line_class
                if directed_edges:
                    sty |= arrow_options
                if theme_function is not None:
                    sty = theme_function((i, j), primitive_class, sty)
                if directed_edges:
                    prim = primitive_class(start, end, **sty)
                else:
                    prim = primitive_class(np.array([start, end]), **sty)
                prim.z_index = z_val
                prims.append(prim)
        return prims

    def _get_label_primitives_2d(self, xy, colors, node_style, labels, *,
                                 text_class, label_style, plot_range, plotos,
                                 default_z=0):
        """
        **LLM Docstring**

        Build text or factory-provided primitives for non-`None` labels.

        :param xy: Planar node coordinates with shape `(N, 2)`.
        :type xy: object

        :param colors: Per-node base colors.
        :type colors: object

        :param node_style: Normalized per-node style dictionaries.
        :type node_style: object

        :param labels: Node labels indexed consistently with the graph.
        :type labels: object

        :param text_class: Primitive class used to construct labels.
        :type text_class: object

        :param label_style: Base text style for all labels.
        :type label_style: object

        :param plot_range: Figure plot range passed to text primitives.
        :type plot_range: object

        :param plotos: Remaining primitive keyword options shared by all generated objects.
        :type plotos: object

        :param default_z: Draw-order/z-index this label's category paints at when
            its style doesn't override it with its own `'z_index'`.
        :type default_z: object

        :return: A flat list of text, graphics, or SVG primitives, each carrying a resolved `.z_index`.
        :rtype: object
        """
        prims = []
        global_style = {k:v for k,v in label_style.items() if isinstance(k, str)}
        for j, (coord, color, lab) in enumerate(zip(xy, colors, labels)):
            if lab is None:
                continue
            ls = global_style | label_style.get(j, {})

            if callable(lab):
                # Primitive factories get the resolved label position. They own
                # their primitive-specific styling, while label_style can still
                # supply the common offset and z-index used by the text path.
                pos = coord + np.asanyarray(ls.get('offset', [0.0, 0.0]), dtype=float)
                made = lab(pos)
                if made is None:
                    continue
                made = made if isinstance(made, (list, tuple)) else [made]
                zi = ls.get('z_index', default_z)
                for prim in made:
                    if prim is None:
                        continue
                    if not hasattr(prim, 'z_index'):
                        prim.z_index = zi
                    prims.append(prim)
                continue

            # a label may be raw text, or a dict of text + per-label style overrides
            extra = {}
            if isinstance(lab, dict):
                extra = dict(lab)
                text = extra.pop('text')
            else:
                text = lab
            if isinstance(text, (int, float, np.integer, np.floating)):
                text = str(text)

            n_sty = dict(node_style[j])
            modifier = n_sty.pop('modifier', None)
            col = n_sty.pop('color', None) or color
            if modifier is not None:
                n_sty = modifier(j, self.nodes[j], dict(n_sty, color=col))
                col = n_sty.pop('color', col)
            n_sty = self._clean_style(n_sty)
            # a label-only style shouldn't drag the node's disk keys onto the text
            n_sty.pop('radius', None)

            sty = ({
                'color': col,
                'use_path': True,
                'invert': True,
                'anchor': (-.5, 1.25),
                'plot_range': plot_range,
            } | extra | ls)
            pos = coord + np.asanyarray(sty.pop('offset', [0.0, 0.0]), dtype=float)
            zi = sty.pop('z_index', None)
            prim = text_class(text, pos, **sty)
            prim.z_index = default_z if zi is None else zi
            prims.append(prim)
        return prims

    # ------------------------------------------------------------------ #
    #  Labeling
    # ------------------------------------------------------------------ #
    def _compute_labels(self, label_function, xy, node_style):
        """
        label_function is one of:
            * None  -> no labels at all (the default),
            * True  -> label every node with str(node),
            * callable(node, i, *, plotter, coords, position, **node_style) -> label|None
        A returned label may be text/a text-style dict, or a callable accepting the
        resolved position and returning one primitive or a list/tuple of primitives.
        Returns a list of per-node labels (or None to skip).
        """
        n = len(self.coords)
        if label_function is None:
            return [None] * n
        if label_function is True:
            return [str(node) for node in self.nodes]

        labels = []
        for i, node in enumerate(self.nodes):
            lab = label_function(
                node, i,
                plotter=self, coords=xy, position=xy[i],
                **node_style[i]
            )
            labels.append(lab)
        return labels

    # ------------------------------------------------------------------ #
    #  Entry point
    # ------------------------------------------------------------------ #
    def plot(self, **styles):
        """
        **LLM Docstring**

        Resolve graph styles and geometry, construct node, edge, label, and annotation primitives, and render or return them.

        :param styles: The value supplied for `styles`, interpreted according to the algorithm described above.
        :type styles: object

        :return: A graphics figure, rendered objects, or primitive groups according to output flags.
            The returned figure also carries a `.graph_pose` attribute -- the
            resolved `pose` transform this call actually used (a callable,
            reapplicable to a *different* set of coordinates), or `None` when
            no such transform exists. Pass it as `pose=` to a later `.plot(...,
            figure=this_figure)` call to draw that second graph in the same
            frame (same recentering/rotation) as this one, instead of each
            call's default pose being computed independently from its own
            point cloud -- which, for two different point clouds, generally
            lands them in different frames even when their raw coordinates
            agree.
        :rtype: object
        """
        from McUtils.Plots import Graphics, Disk, Line, Arrow, Text

        theme = self.subthemes['default']

        def _merge(key):  # shallow-merge nested option dicts over the theme
            """
            **LLM Docstring**

            Shallow-merge a nested plotting option dictionary over the default theme entry.

            :param key: Index, path, or mapping key selecting an item.
            :type key: object

            :return: The merged option dictionary.
            :rtype: object
            """
            return {**theme.get(key, {}), **(styles.pop(key, None) or {})}

        line_options = _merge('line_options')
        arrow_options = _merge('arrow_options')
        disk_options = _merge('disk_options')
        label_style = _merge('label_style')

        figure = styles.pop('figure', None)

        # geometry / layout
        pose = styles.pop('pose', None)
        edges = styles.pop('edges', None)
        node_radius = styles.pop('node_radius', theme['node_radius'])
        trim_edges = styles.pop('trim_edges', True)
        node_edge_offset = styles.pop('node_edge_offset', 0)

        # styling
        node_style = styles.pop('node_style', None)
        edge_style = styles.pop('edge_style', None)
        node_color = styles.pop('node_color', theme['node_color'])
        edge_color = styles.pop('edge_color', theme['edge_color'])
        weight_linewidth = styles.pop('weight_linewidth', (.01, .1))
        half_colored_edges = styles.pop('half_colored_edges', False)
        directed_edges = styles.pop('directed_edges', self.graph.directed)
        draw_nodes = styles.pop('draw_nodes', True)

        # labels: off unless a label_function is provided
        label_function = styles.pop('label_function', None)

        # highlighting
        highlight_nodes = styles.pop('highlight_nodes', None)
        highlight_edges = styles.pop('highlight_edges', None)
        highlight_style = styles.pop('highlight_style', theme['highlight_style'])

        # draw order / z-layering: which category paints first (bottom) vs. last
        # (top). Default is edges-then-nodes-then-labels, so nodes sit on top of
        # (visually overlap) the edges meeting them, not the other way around.
        # A per-item 'z_index' in node_style/edge_style/label_style overrides that
        # item's category default and is compared against every other item.
        draw_order = styles.pop('draw_order', ('edges', 'nodes', 'labels'))
        if isinstance(draw_order, str):
            draw_order = (draw_order,)
        category_z = {name: rank for rank, name in enumerate(draw_order)}
        for name in ('edges', 'nodes', 'labels'):
            category_z.setdefault(name, len(category_z))
        category_z.setdefault('annotations', category_z['labels'])

        # classes / backends
        disk_class = styles.pop('disk_class', None) or Disk
        line_class = styles.pop('line_class', None) or Line
        arrow_class = styles.pop('arrow_class', None) or Arrow
        text_class = styles.pop('text_class', None) or Text
        graphics_class = styles.pop('graphics_class', None) or Graphics
        theme_function = styles.pop('theme_function', None)
        annotation_function = styles.pop('annotation_function', None)

        # figure options
        # `None` here means "auto": size the canvas to the actual data extent
        # (see below) rather than forcing a fixed square. Pass an explicit
        # `image_size=(w, h)` to override.
        image_size = styles.pop('image_size', None)
        background = styles.pop('background', 'transparent')
        plot_range_padding = styles.pop('plot_range_padding', 'auto')

        # output shape
        return_objects = styles.pop('return_objects', False)
        objects = styles.pop('objects', False)

        # split any leftover Graphics figure kwargs from stray per-primitive kwargs
        gk = (getattr(Graphics, 'known_keys', set()) | getattr(Graphics, 'opt_keys', set())
              | getattr(Graphics, 'figure_keys', set()) | getattr(Graphics, 'axes_keys', set()))
        graphics_opts = {k: styles.pop(k) for k in list(styles.keys()) if k in gk}
        plotos = dict(styles)   # whatever remains rides along on each primitive

        # ---- resolve nodes/edges/positions ------------------------------------
        n = len(self.coords)
        edge_list = self._edge_list(edges)
        xy = self._apply_pose(self.coords, pose=pose)[:, :2]
        # the *actual* transform this call resolved to (whatever `pose` you
        # passed, or -- if you passed none -- the specific PCA com/axes this
        # point cloud landed on): stashed on the returned figure as
        # `figure.graph_pose` so it can be handed to a later `.plot(..., figure=this_figure)`
        # call as its own `pose=`, keeping the two draws in the same frame.
        # `None` when no reapplicable transform exists (an explicit (N,2)/(N,3)
        # coordinate array was passed as `pose` -- that's final coordinates,
        # not a transform, so there's nothing meaningful to reuse).
        resolved_pose = getattr(self, '_resolved_pose', None)

        radii = self._get_node_radii(node_radius, n)
        colors = [node_color] * n

        node_style = self._normalize_styles(node_style, n)
        # edge_style is kept in its original (list | dict | callable) form so the
        # edge builder can key it by index or by (i, j); callables get expanded now
        if callable(edge_style):
            edge_style = [edge_style(k) or {} for k in range(len(edge_list))]

        # highlights fold straight into the per-item styles
        node_style = self._apply_highlights(node_style, highlight_nodes, highlight_style)
        if highlight_edges and isinstance(edge_style, (list, tuple)):
            pair_to_index = {}
            for k, (i, j, _d) in enumerate(edge_list):
                pair_to_index[(i, j)] = k
                pair_to_index[(j, i)] = k
            edge_style = list(edge_style) + [{}] * (len(edge_list) - len(edge_style))
            edge_style = self._apply_highlights(
                edge_style, highlight_edges, highlight_style, lookup=pair_to_index)
        elif highlight_edges:
            # edge_style is a (i,j)->dict map: merge highlight into those entries
            edge_style = dict(edge_style or {})
            for e in highlight_edges:
                key = tuple(e) if not isinstance(e, (int, np.integer)) else edge_list[e][:2]
                edge_style[key] = dict(highlight_style, **edge_style.get(key, {}))

        drawn = [bool(draw_nodes)] * n

        labels = self._compute_labels(label_function, xy, node_style)

        # ---- figure -----------------------------------------------------------
        if figure is None:
            plot_range = self._plot_range_2d(xy, radii, plot_range_padding)
            if image_size is None:
                # A fixed square canvas (e.g. `(400, 400)`) combined with
                # `aspect_ratio='equal'` doesn't distort or clip anything --
                # it just pads whichever data axis is shorter with blank
                # space so the 1:1 data scale still fits the square frame.
                # For a graph that isn't naturally square (e.g. a wide,
                # short stacked-layer diagram) that shows up as a lot of
                # wasted empty margin. Instead, size the canvas so its
                # width:height ratio matches the data's own extent: the
                # longer data axis maps to 400px and the shorter one follows
                # the true aspect ratio, so `aspect_ratio='equal'` has
                # nothing left to pad.
                (x_lo, x_hi), (y_lo, y_hi) = plot_range
                w_data = max(x_hi - x_lo, 1e-9)
                h_data = max(y_hi - y_lo, 1e-9)
                target = 400
                if w_data >= h_data:
                    image_size = (target, target * h_data / w_data)
                else:
                    image_size = (target * w_data / h_data, target)
            fig_opts = dict(
                backend='svg', image_size=image_size, aspect_ratio='equal',
                frame=False, background=background, padding=0,
                plot_range=plot_range,
            )
            fig_opts.update(graphics_opts)
            figure = graphics_class(**fig_opts)
        # note: when an existing `figure=` was passed in (overlay), this
        # overwrites its `graph_pose` with *this* call's transform -- so grab
        # `figure.graph_pose` right after the call whose pose you want to
        # reuse, before making the next, overlaid `.plot()` call.
        figure.graph_pose = resolved_pose
        plot_range = figure.plot_range

        # ---- primitives -------------------------------------------------------
        edge_prims = self._get_edge_primitives_2d(
            xy, edge_list, radii, colors, node_style, drawn,
            line_class=line_class, edge_style=edge_style, edge_color=edge_color,
            line_options=line_options, trim_edges=trim_edges,
            node_edge_offset=node_edge_offset,
            half_colored_edges=half_colored_edges,
            weight_linewidth=weight_linewidth,
            directed_edges=directed_edges, arrow_class=arrow_class, arrow_options=arrow_options,
            theme_function=theme_function, plotos=plotos,
            default_z=category_z['edges'])
        node_prims = self._get_node_primitives_2d(
            xy, radii, colors, node_style, drawn,
            disk_class=disk_class, disk_options=disk_options,
            theme_function=theme_function, plotos=plotos,
            default_z=category_z['nodes'])
        label_prims = self._get_label_primitives_2d(
            xy, colors, node_style, labels,
            text_class=text_class, label_style=label_style,
            plot_range=plot_range, plotos=plotos,
            default_z=category_z['labels'])
        extra_prims = []
        if annotation_function is not None:
            extra_prims = list(annotation_function(self.graph, xy))
        for p in extra_prims:
            # an annotation_function can set its own `.z_index` on a primitive
            # it returns; otherwise it paints with the rest of the annotations
            if not hasattr(p, 'z_index'):
                p.z_index = category_z['annotations']

        # ---- render / return --------------------------------------------------
        def _render_one(p):
            """Render a single primitive into the figure, or pass it through in `objects` mode."""
            if objects:
                return p
            if hasattr(p, 'plot'):
                art = p.plot(figure)
            elif hasattr(p, 'to_svg') and hasattr(p, 'get_bbox'):
                # Low-level SVG primitives are already backend objects. Insert
                # them directly instead of requiring a GraphicsPrimitive wrapper.
                svg_figure = getattr(getattr(figure, 'axes', None), 'figure', None)
                if svg_figure is None or not hasattr(svg_figure, 'elements'):
                    raise TypeError(
                        "raw SVG label primitives require the SVG plotting backend"
                    )
                svg_figure.elements.append(p)
                art = p
            else:
                raise TypeError(
                    "label factories must return Graphics primitives, SVG primitives, "
                    "or lists/tuples containing them"
                )
            if isinstance(art, (list, tuple)):
                art = art[0]
            return art

        # Paint everything in one pass, ordered by ascending z_index, so the
        # *visual* stacking follows `draw_order`/per-item `z_index` regardless
        # of category -- while the objects returned per category stay in their
        # original, per-item order (nodes_out[i] is still node i, etc.), since
        # that's a separate concern from paint order.
        buckets = [
            ('edges', edge_prims), ('nodes', node_prims),
            ('labels', label_prims), ('annotations', extra_prims),
        ]
        painted = {name: [None] * len(prims) for name, prims in buckets}
        tagged = [
            (p.z_index, category_z[name], bucket_i, i, name, p)
            for bucket_i, (name, prims) in enumerate(buckets)
            for i, p in enumerate(prims)
        ]
        for z, cat_rank, bucket_i, i, name, p in sorted(tagged, key=lambda t: t[:4]):
            painted[name][i] = _render_one(p)

        nodes_out = painted['nodes']
        edges_out = painted['edges']
        labels_out = painted['labels'] + painted['annotations']

        if objects:
            return {'nodes': nodes_out, 'edges': edges_out, 'labels': labels_out}
        if return_objects:
            return figure, nodes_out, edges_out, labels_out
        return figure