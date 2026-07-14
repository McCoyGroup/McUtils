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

# Node = Hashable
# Edge = Tuple[Node, Node]
# Position = Tuple[float, float]

__all__ = [
    "GraphLayout",
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
    """

    _registry = {}

    def __init__(self, graph:EdgeGraph, weights=None):
        self.graph = graph
        self.nodes = list(graph.labels)
        self.edges = list(graph.edges)
        self.weights = weights
        self._index = {n: i for i, n in enumerate(self.nodes)}
        self._adj = self._build_adjacency(weights)
        self.positions = {}

    # -- construction -------------------------------------------------

    def _build_adjacency(self, weights):
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
            cls._registry[name] = func
            return func

        return decorator

    @classmethod
    def available_layouts(cls) -> List[str]:
        return sorted(cls._registry.keys())

    default_layout_method = "kamada_kawai"
    def compute(self, method: str = "default", **kwargs):
        if dev.str_is(method, 'default'):
            method = self.default_layout_method
        if method not in self._registry:
            raise ValueError(
                f"Unknown layout method '{method}'. "
                f"Available: {self.available_layouts()}"
            )
        self.positions = self._registry[method](self, **kwargs)
        return self.positions

    # -- shared utilities -------------------------------------------------

    def shortest_path_distances(self) -> np.ndarray:
        dits = self.graph.get_distances()
        dits = dits.copy()
        return dits

# ---------------------------------------------------------------------------
# Plugin: circular layout (trivial baseline, shows the dispatch mechanism)
# ---------------------------------------------------------------------------

@GraphLayout.register("circular")
def circular_layout(layout: GraphLayout, scale: float = 1.0):
    n = len(layout.nodes)
    if n == 0:
        return {}
    positions = {}
    for i, node in enumerate(layout.nodes):
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
    """
    rng = random.Random(seed)
    n = len(layout.nodes)
    if n == 0:
        return {}
    if n == 1:
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

    def stress(p: np.ndarray) -> float:
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

        cur_stress = stress(pos)
        if abs(prev_stress - cur_stress) < tol:
            break
        prev_stress = cur_stress

    return {node: (float(pos[i, 0]), float(pos[i, 1])) for i, node in enumerate(layout.nodes)}

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
    as `Text` next to the node. Returning ``None`` skips the label for that node, so
    a single function can label some nodes and not others.

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
    """
    modes = ('svg2d',)
    subthemes = {
        'default': {
            'node_radius': .02,
            'disk_options': {'stroke-width': '.005px', 'stroke': 'black'},
            'line_options': {'stroke-width': '.005px', 'stroke': 'black'},
            'label_style': {'font_size': 6},
            'node_color': '#4C72B0',
            'edge_color': 'black',
            'highlight_style': {'stroke': '#d62728', 'color': '#d62728'},
        }
    }

    def __init__(self, graph, coords):
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
        # node identities (labels/keys); positions are always self.coords[i]
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
        coords = np.asanyarray(coords, dtype=float)
        if coords.shape[-1] == 2:
            coords = np.pad(coords, [[0, 0], [0, 1]])
        i, j = principal_axis_order

        def _pa_project(c):
            com = nput.center_of_mass(c, masses)
            _, axes = nput.moments_of_inertia(c, masses)  # ascending moment; cols=axes
            proj = (c - com[np.newaxis, :]) @ axes
            return np.stack([proj[:, i], proj[:, j]], axis=-1)

        if pose is None:
            return _pa_project(coords)
        if callable(pose):
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
    @staticmethod
    def _clean_style(sty):
        # 2D Disk/Line don't take `glow`; fold it into a stroke outline instead
        sty = dict(sty)
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
        lo = np.min(xy, axis=0)
        hi = np.max(xy, axis=0)
        if plot_range_padding is None:
            pad = 0.0
        elif isinstance(plot_range_padding, str) and plot_range_padding == 'auto':
            pad = float(np.max(radii)) * 1.5
        else:
            pad = float(plot_range_padding)
        return [[lo[0] - pad, hi[0] + pad], [lo[1] - pad, hi[1] + pad]]

    def _get_node_radii(self, node_radius, n):
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
                                disk_class, disk_options, theme_function, plotos):
        prims = []
        base = dict(disk_options)
        for i, (coord, r, color, sty0) in enumerate(zip(xy, radii, colors, node_style)):
            if not drawn[i]:
                continue
            sty = dict(sty0)
            modifier = sty.pop('modifier', None)
            col = sty.pop('color', None) or color
            rr = sty.pop('radius', r)
            if modifier is not None:
                sty = modifier(i, self.nodes[i], dict(sty, color=col))
                col = sty.pop('color', col)
                rr = sty.pop('radius', rr)
            sty = self._clean_style(sty)
            full = (plotos | base | {'color': col} | sty)
            if theme_function is not None:
                full = theme_function(i, disk_class, full)
            prims.append(disk_class(np.asanyarray(coord), float(rr), **full))
        return prims

    def _get_edge_primitives_2d(self, xy, edges, radii, colors, node_style, drawn, *,
                                line_class, edge_style, edge_color, line_options,
                                trim_edges, half_colored_edges, theme_function, plotos):
        prims = []
        base = dict(line_options)
        # allow keying edge_style by edge index OR by (i, j) tuple
        by_index = edge_style if isinstance(edge_style, (list, tuple)) else None
        by_pair = edge_style if isinstance(edge_style, dict) else {}

        for e_i, (i, j, _data) in enumerate(edges):
            pi, pj = xy[i], xy[j]
            d = pj - pi
            L = np.linalg.norm(d)
            if L < 1e-8:
                continue
            u = d / L

            # trim back to the node disk so the line doesn't run under the glyph;
            # only trim at an endpoint whose node is actually drawn
            start = pi + u * radii[i] if (trim_edges and drawn[i]) else pi
            end = pj - u * radii[j] if (trim_edges and drawn[j]) else pj

            # resolve this edge's style: (i,j)/(j,i) tuple key, or positional list
            e_sty = {}
            if by_index is not None and e_i < len(by_index) and by_index[e_i]:
                e_sty = dict(by_index[e_i])
            else:
                e_sty = dict(by_pair.get((j, i), {}), **by_pair.get((i, j), {}))
            mod = e_sty.pop('modifier', None)
            if mod is not None:
                e_sty = mod((i, j), (self.nodes[i], self.nodes[j]), e_sty)
            e_sty = self._clean_style(e_sty)

            if half_colored_edges and 'color' not in e_sty:
                # color each half by its endpoint node -> reads like the CPK bonds
                mid = (start + end) / 2
                for pts, c in (([start, mid], colors[i]), ([mid, end], colors[j])):
                    sty = (plotos | base | {'color': c} | e_sty)
                    if theme_function is not None:
                        sty = theme_function((i, j), line_class, sty)
                    prims.append(line_class(np.array(pts), **sty))
            else:
                sty = (plotos | base | e_sty)
                sty.setdefault('color', edge_color)
                if theme_function is not None:
                    sty = theme_function((i, j), line_class, sty)
                prims.append(line_class(np.array([start, end]), **sty))
        return prims

    def _get_label_primitives_2d(self, xy, colors, node_style, labels, *,
                                 text_class, label_style, plot_range, plotos):
        prims = []
        for j, (coord, color, lab) in enumerate(zip(xy, colors, labels)):
            if lab is None:
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

            sty = (label_style | {
                'color': col,
                'use_path': True,
                'invert': True,
                'anchor': (-.5, 1.25),
                'plot_range': plot_range,
            } | extra)
            pos = coord + np.asanyarray(sty.pop('offset', [0.0, 0.0]), dtype=float)
            prims.append(text_class(text, pos, **sty))
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
        Returns a list of per-node labels (each str/number/dict, or None to skip).
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
        from McUtils.Plots import Graphics, Disk, Line, Text

        theme = self.subthemes['default']

        def _merge(key):  # shallow-merge nested option dicts over the theme
            return {**theme.get(key, {}), **(styles.pop(key, None) or {})}

        line_options = _merge('line_options')
        disk_options = _merge('disk_options')
        label_style = _merge('label_style')

        figure = styles.pop('figure', None)

        # geometry / layout
        pose = styles.pop('pose', None)
        edges = styles.pop('edges', None)
        node_radius = styles.pop('node_radius', theme['node_radius'])
        trim_edges = styles.pop('trim_edges', True)

        # styling
        node_style = styles.pop('node_style', None)
        edge_style = styles.pop('edge_style', None)
        node_color = styles.pop('node_color', theme['node_color'])
        edge_color = styles.pop('edge_color', theme['edge_color'])
        half_colored_edges = styles.pop('half_colored_edges', False)
        draw_nodes = styles.pop('draw_nodes', True)

        # labels: off unless a label_function is provided
        label_function = styles.pop('label_function', None)

        # highlighting
        highlight_nodes = styles.pop('highlight_nodes', None)
        highlight_edges = styles.pop('highlight_edges', None)
        highlight_style = styles.pop('highlight_style', theme['highlight_style'])

        # classes / backends
        disk_class = styles.pop('disk_class', None) or Disk
        line_class = styles.pop('line_class', None) or Line
        text_class = styles.pop('text_class', None) or Text
        graphics_class = styles.pop('graphics_class', None) or Graphics
        theme_function = styles.pop('theme_function', None)
        annotation_function = styles.pop('annotation_function', None)

        # figure options
        image_size = styles.pop('image_size', (400, 400))
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
            fig_opts = dict(
                backend='svg', image_size=image_size, aspect_ratio='equal',
                frame=False, background=background,
                plot_range=self._plot_range_2d(xy, radii, plot_range_padding),
            )
            fig_opts.update(graphics_opts)
            figure = graphics_class(**fig_opts)
        plot_range = figure.plot_range

        # ---- primitives -------------------------------------------------------
        edge_prims = self._get_edge_primitives_2d(
            xy, edge_list, radii, colors, node_style, drawn,
            line_class=line_class, edge_style=edge_style, edge_color=edge_color,
            line_options=line_options, trim_edges=trim_edges,
            half_colored_edges=half_colored_edges,
            theme_function=theme_function, plotos=plotos)
        node_prims = self._get_node_primitives_2d(
            xy, radii, colors, node_style, drawn,
            disk_class=disk_class, disk_options=disk_options,
            theme_function=theme_function, plotos=plotos)
        label_prims = self._get_label_primitives_2d(
            xy, colors, node_style, labels,
            text_class=text_class, label_style=label_style,
            plot_range=plot_range, plotos=plotos)
        extra_prims = []
        if annotation_function is not None:
            extra_prims = list(annotation_function(self.graph, xy))

        # ---- render / return --------------------------------------------------
        def _render(prims):
            if objects:
                return prims
            out = []
            for p in prims:
                art = p.plot(figure)
                if isinstance(art, (list, tuple)):
                    art = art[0]
                out.append(art)
            return out

        nodes_out = _render(node_prims)
        edges_out = _render(edge_prims)
        labels_out = _render(label_prims + extra_prims)

        if objects:
            return {'nodes': nodes_out, 'edges': edges_out, 'labels': labels_out}
        if return_objects:
            return figure, nodes_out, edges_out, labels_out
        return figure