from __future__ import annotations

import numpy as np

from .. import Devutils as dev
from .EdgeGraph import EdgeGraph

__all__ = [
    "UnionMultiGraph"
]

class UnionMultiGraph(EdgeGraph):
    """
    A multigraph formed as the union of several component graphs defined
    over the same node set (e.g. a bond graph and a through-space contact
    graph over the same atoms, or several correlation graphs over the same
    variables).

    Component graphs will usually live on incompatible weight scales
    (Angstroms vs. correlation coefficients vs. bond order...), so rather
    than teach `GraphLayout`/`GraphPlotter` to juggle several graphs at
    once, each component is independently rescaled onto a common footing
    and the components are folded into ordinary single-graph data -- an
    adjacency matrix, an edge list, and a `{(i, j): weight}` map -- exactly
    what a plain weighted `EdgeGraph` carries. `layout`/`plot` are
    therefore inherited unchanged; `plot` only adds a thin default so
    edges stay colored by their dominant contributing component. Weight
    convention matches `EdgeGraph` throughout: larger values mean *more*
    graph-theoretic separation (they're fed straight to
    `scipy.sparse.csgraph.shortest_path` as costs), so similarity-style
    weights should be inverted before being handed in.

    Component provenance (raw per-component edges/weights/scale, and which
    components contributed to each merged edge) is kept on the side in
    `self.components` / `self.edge_components` -- `plot` uses it to draw
    every contributing edge separately (fanned out where several overlap
    the same node pair) rather than collapsing them; `layout` uses the
    single pooled weight per pair instead (see `pool_layout`), since node
    *placement* has no use for telling the edges apart.
    """
    __slots__ = ["components", "scales", "combine", "edge_components", "pooled_weights"]

    default_combine = "sum"
    default_palette = ("#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2", "#937860")
    _reducers = {"sum": sum, "max": max, "mean": lambda v: sum(v) / len(v)}

    def __init__(self, labels, edges=None, graph=None, edge_map=None, weights=None,
                 allow_self_loops=False, *, components=None, scales=None, combine=None,
                 pool_layout=True):
        """
        Base-`EdgeGraph`-compatible constructor: with `components=None` this
        behaves exactly like `EdgeGraph`, so derived views (`.take()`,
        `.break_bonds()`, ...) that call `type(self)(labels, edges)` keep
        working -- they just degrade to a plain single graph, since the
        induced-subgraph machinery has no notion of "which component". Use
        `UnionMultiGraph.from_graphs` to build an actual union.

        :param components: pre-built component specs (see `_build_components`); internal
        :param scales: per-component rescaling; see `_resolve_scales`
        :param combine: how overlapping edges are pooled across components: 'sum' (default),
            'max', 'mean', or a `callable(list[float]) -> float`
        :param pool_layout: whether node placement uses the pooled per-pair weight
            (default) or ignores magnitude and lays out on unweighted structure alone;
            either way, `self.pooled_weights` holds the pooled values and `plot` always
            draws each contributing edge on its own, unpooled weight
        """
        self.components = components
        self.combine = combine or self.default_combine
        self.scales = None
        self.edge_components = None
        self.pooled_weights = None
        if components is not None:
            edges, self.pooled_weights, self.scales, self.edge_components = self._merge_components(
                components, scales, self.combine
            )
            weights = self.pooled_weights if pool_layout else None
        super().__init__(labels, edges, graph=graph, edge_map=edge_map, weights=weights,
                         allow_self_loops=allow_self_loops)

    # ------------------------------------------------------------------ #
    #  Construction
    # ------------------------------------------------------------------ #
    @classmethod
    def from_graphs(cls, labels, graphs, names=None, scales=None, combine=None,
                    pool_layout=True, allow_self_loops=False):
        """
        Build the union of `graphs` over `labels`.

        :param graphs: one entry per component; each is an `EdgeGraph` (sharing `labels`),
            a `{'edges':..., 'weights':...}` dict, or a raw `(i, j[, w])` edge array
        :param names: optional per-component names, used for styling/legends
        :return: the union multigraph
        :rtype: UnionMultiGraph
        """
        components = cls._build_components(labels, graphs, names)
        return cls(labels, components=components, scales=scales, combine=combine,
                   pool_layout=pool_layout, allow_self_loops=allow_self_loops)

    @classmethod
    def _build_components(cls, labels, graphs, names):
        if names is None:
            names = [None] * len(graphs)
        comps = []
        for i, (name, g) in enumerate(zip(names, graphs)):
            if isinstance(g, EdgeGraph):
                if list(g.labels) != list(labels):
                    raise ValueError("component graph labels must match the union's labels")
                edges, w = g.edges, g.weights
            elif dev.is_dict_like(g):
                edges, w = g['edges'], g.get('weights')
            else:
                g = np.asanyarray(g)
                edges, w = g[:, :2], (g[:, 2] if g.shape[-1] > 2 else None)
            edges = np.asanyarray(edges, dtype=int).reshape(-1, 2)
            if w is None:
                weights = np.ones(len(edges))
            elif dev.is_dict_like(w):
                weights = np.array([w.get((i,j), w.get((j,i), 1.0)) for i,j in edges], dtype=float)
            else:
                weights = np.asanyarray(w, dtype=float)
            comps.append({'name': name if name is not None else i, 'edges': edges, 'weights': weights})
        return comps

    @classmethod
    def _resolve_scales(cls, components, scales):
        n = len(components)
        if scales is None:
            # default: normalize each component onto its own [0, 1] footing, so no
            # component dominates the merge purely because of its raw units
            return [
                1.0 / m if (m := (c['weights'].max() if len(c['weights']) else 0.0)) > 0 else 1.0
                for c in components
            ]
        if callable(scales):
            return [scales(c['edges'], c['weights']) for c in components]
        if dev.is_dict_like(scales):
            return [scales.get(c['name'], scales.get(i, 1.0)) for i, c in enumerate(components)]
        if np.ndim(scales) == 0:
            return [float(scales)] * n
        return list(scales)

    @classmethod
    def _merge_components(cls, components, scales, combine):
        scales = cls._resolve_scales(components, scales)
        reducer = combine if callable(combine) else cls._reducers[combine]
        pooled, contributors = {}, {}
        for k, (c, s) in enumerate(zip(components, scales)):
            for (i, j), w in zip(c['edges'], c['weights']):
                key = (int(i), int(j)) if i <= j else (int(j), int(i))
                sw = float(w) * s
                pooled.setdefault(key, []).append(sw)
                contributors.setdefault(key, []).append((k, sw))
        edges = list(pooled.keys())
        weights = {key: reducer(vals) for key, vals in pooled.items()}
        return edges, weights, scales, contributors

    # ------------------------------------------------------------------ #
    #  Weighted adjacency -- `EdgeGraph.adj_mat` truncates to int, which
    #  would quietly zero out rescaled (<1) weights; keep everything else
    #  identical, just widen the dtype.
    # ------------------------------------------------------------------ #
    @classmethod
    def adj_mat(cls, num_nodes, edges, weights=None):
        import scipy.sparse as sparse
        if weights is not None:
            edges = [
                (e[0], e[1], weights.get((e[0], e[1]), weights.get((e[1], e[0]), 1.0)))
                    if len(e) == 2 else e
                for e in edges
            ]
        edges = [(e[0], e[1], 1.0) if len(e) == 2 else e for e in edges]
        adj = np.zeros((num_nodes, num_nodes), dtype=float)
        if len(edges) > 0:
            rows, cols, ws = np.array(edges, dtype=float).T
            rows, cols = rows.astype(int), cols.astype(int)
            adj[rows, cols] = ws
            adj[cols, rows] = ws
        return sparse.csr_matrix(adj)

    # ------------------------------------------------------------------ #
    #  Provenance-aware plotting
    # ------------------------------------------------------------------ #
    def dominant_component(self, i, j):
        """Index of the component contributing the largest rescaled weight to edge (i, j)."""
        key = (i, j) if i <= j else (j, i)
        contribs = self.edge_components.get(key) if self.edge_components else None
        return max(contribs, key=lambda kw: kw[1])[0] if contribs else None

    def component_legend(self, colors=None):
        """List of `{'name', 'color'}` entries, one per component, for building a legend."""
        colors = colors or self.default_palette
        return [
            {'name': c['name'], 'color': colors[k % len(colors)]}
            for k, c in enumerate(self.components or [])
        ]

    def plot(self, method='default', *, component_colors=None, weight_linewidth=(.01, .1),
             edge_offset=None, **opts):
        """
        Like `EdgeGraph.plot`, but when this union carries component
        provenance, every contributing edge is drawn on its own -- colored
        by its component and widthed by its own (rescaled) weight -- instead
        of collapsing same-pair edges into one pooled line. Node placement
        still comes from the inherited `layout` (pooled per `pool_layout`);
        only drawing is per-edge here. Edges that share a node pair are
        fanned out by `edge_offset` (default: `0.6 *` the plotted node
        radius) so they stay individually visible rather than overlapping
        exactly. An explicit `edge_style`/`edges` in `opts` is left
        untouched and simply passed through.
        """
        if not self.components or 'edge_style' in opts or 'edges' in opts:
            return super().plot(method, **opts)

        from .Layout import GraphPlotter
        colors = component_colors or self.default_palette
        if edge_offset is None:
            edge_offset = 0.6 * opts.get('node_radius', GraphPlotter.subthemes['default']['node_radius'])

        raw = [
            (int(i), int(j), k, float(w) * s)
            for k, (c, s) in enumerate(zip(self.components, self.scales))
            for (i, j), w in zip(c['edges'], c['weights'])
        ]
        all_w = np.array([r[3] for r in raw])
        lo, hi = weight_linewidth
        wmin, wmax = (all_w.min(), all_w.max()) if len(all_w) else (0.0, 1.0)
        span = (wmax - wmin) or 1.0

        # fan overlapping (i, j) pairs out around the true edge so each stays visible
        counts, seen = {}, {}
        for i, j, _k, _w in raw:
            key = (min(i, j), max(i, j))
            counts[key] = counts.get(key, 0) + 1
        edge_list, meta = [], []
        for i, j, k, w in raw:
            key = (min(i, j), max(i, j))
            slot = seen.get(key, 0)
            seen[key] = slot + 1
            edge_list.append((i, j, (slot - (counts[key] - 1) / 2) * edge_offset))
            meta.append((k, w))

        def edge_style(idx):
            k, w = meta[idx]
            width = lo + (hi - lo) * (w - wmin) / span
            return {'color': colors[k % len(colors)], 'stroke-width': f'{width:.3f}px'}

        return super().plot(method, edges=edge_list, edge_style=edge_style, **opts)
