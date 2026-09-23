import unittest

import numpy as np
import scipy.sparse as sparse

from McUtils.Graphs import EdgeGraph
from McUtils.Plots import Arrow, Disk, Line, Text
from McUtils.Plots.Backends import SVGAxes
from McUtils.Plots.SVG import SVGCircle


class GraphsTests(unittest.TestCase):

    def test_edge_graph_directed_construction_and_inference(self):
        directed = EdgeGraph(['a', 'b'], [(0, 1)], directed=True)
        self.assertTrue(directed.directed)
        self.assertEqual(directed.graph[0, 1], 1)
        self.assertEqual(directed.graph[1, 0], 0)
        self.assertEqual(directed.map, {0: {1}, 1: set()})
        self.assertTrue(np.isinf(directed.get_distances(indices=1)[0]))
        self.assertTrue(directed.take([0, 1]).directed)
        self.assertTrue(directed.neighbor_graph(0).directed)

        undirected = EdgeGraph(['a', 'b'], [(0, 1)])
        self.assertFalse(undirected.directed)
        self.assertEqual(undirected.graph[1, 0], 1)
        self.assertEqual(undirected.map, {0: {1}, 1: {0}})

        asymmetric = sparse.csr_matrix([[0, 2], [0, 0]])
        inferred = EdgeGraph(['a', 'b'], [(0, 1)], graph=asymmetric)
        self.assertTrue(inferred.directed)

        symmetric = sparse.csr_matrix([[0, 2], [2, 0]])
        inferred = EdgeGraph(['a', 'b'], [(0, 1)], graph=symmetric)
        self.assertFalse(inferred.directed)

    def test_directed_graph_edges(self):
        graph = EdgeGraph.stacked_graph([2, 2], neighbors=2)
        self.assertTrue(graph.directed)
        self.assertTrue(all(graph.graph[i, j] for i, j in graph.edges))
        self.assertTrue(all(graph.graph[j, i] == 0 for i, j in graph.edges))
        objects = graph.plot(
            method='stacked_layer', objects=True
        )
        self.assertEqual(len(objects['edges']), len(graph.edges))
        self.assertTrue(all(isinstance(edge, Arrow) for edge in objects['edges']))
        self.assertTrue(all(
            np.linalg.norm(edge.pos2 - edge.pos1) > 0
            for edge in objects['edges']
        ))
        arrowhead = {'markerWidth': '9'}
        objects = graph.plot(
            method='stacked_layer',
            arrow_options={'arrowhead': arrowhead}, objects=True
        )
        self.assertTrue(all(edge.opts['arrowhead'] == arrowhead for edge in objects['edges']))

        objects = graph.plot(
            method='stacked_layer', directed_edges=False, objects=True
        )
        self.assertTrue(all(isinstance(edge, Line) for edge in objects['edges']))

        objects = graph.plot(
            method='stacked_layer', directed_edges=True,
            half_colored_edges=True, objects=True
        )
        self.assertEqual(len(objects['edges']), 2 * len(graph.edges))
        self.assertTrue(all(isinstance(edge, Line) for edge in objects['edges'][::2]))
        self.assertTrue(all(isinstance(edge, Arrow) for edge in objects['edges'][1::2]))

    def test_graph_node_edge_offsets_and_arrowhead_defaults(self):
        graph = EdgeGraph.stacked_graph([2, 2], neighbors=2)
        objects = graph.plot(
            method='stacked_layer', node_radius=.2,
            node_edge_offset=(.05, .1),
            edge_style={'line_thickness': .2}, objects=True
        )
        for edge, (i, j) in zip(objects['edges'], graph.edges):
            self.assertAlmostEqual(
                np.linalg.norm(edge.pos1 - objects['nodes'][i].pos), .25
            )
            self.assertAlmostEqual(
                np.linalg.norm(edge.pos2 - objects['nodes'][j].pos), .5
            )

        # The default marker is two stroke-widths wide with its reference point
        # in the middle, so its forward half contributes one stroke width. A
        # partial arrowhead override is merged onto the backend defaults and is
        # reflected in the endpoint compensation too.
        custom = graph.plot(
            method='stacked_layer', node_radius=.2,
            edge_style={'line_thickness': .2},
            arrow_options={'arrowhead': {'markerWidth': '4'}}, objects=True
        )
        for edge, (_i, j) in zip(custom['edges'], graph.edges):
            self.assertAlmostEqual(
                np.linalg.norm(edge.pos2 - custom['nodes'][j].pos), .6
            )

        with self.assertRaisesRegex(ValueError, "node_edge_offset"):
            graph.plot(
                method='stacked_layer', node_edge_offset=(0, 0, 0), objects=True
            )

        self.assertEqual(SVGAxes.default_arrowhead['refX'], '5')
        self.assertEqual(SVGAxes.default_arrowhead['markerWidth'], '2')
        self.assertEqual(SVGAxes.default_arrowhead['markerHeight'], '5')
        self.assertEqual(SVGAxes.default_arrowhead['markerUnits'], 'strokeWidth')
        self.assertEqual(SVGAxes.default_arrowhead['overflow'], 'visible')

    def test_callable_graph_labels_build_graphics_and_svg_primitives(self):
        graph = EdgeGraph.stacked_graph([2, 1], neighbors=1)

        def graphic_labels(_node, i, **_):
            if i == 0:
                return lambda pos: [
                    Disk(pos + [-.025, 0], .01, color='red'),
                    Disk(pos + [.025, 0], .01, color='red')
                ]
            if i == 1:
                return {'text': 'text label', 'color': 'blue'}

        objects = graph.plot(
            method='stacked_layer', label_function=graphic_labels, objects=True
        )
        self.assertEqual(len(objects['labels']), 3)
        self.assertTrue(all(isinstance(label, Disk) for label in objects['labels'][:2]))
        self.assertIsInstance(objects['labels'][2], Text)
        expected = objects['nodes'][0].pos
        self.assertTrue(np.allclose(objects['labels'][0].pos, expected + [-.025, 0]))
        self.assertTrue(np.allclose(objects['labels'][1].pos, expected + [.025, 0]))

        raw = []

        def svg_label(_node, i, **_):
            if i != 0:
                return None

            def make_circle(pos):
                circle = SVGCircle(pos[0], pos[1], .01, fill='purple')
                raw.append(circle)
                return circle

            return make_circle

        figure, _nodes, _edges, labels = graph.plot(
            method='stacked_layer', label_function=svg_label, return_objects=True
        )
        self.assertEqual(labels, raw)
        self.assertIn(raw[0], figure.axes.figure.elements)

    def test_stacked_graph_layer_specific_connectivity(self):
        graph = EdgeGraph.stacked_graph([2, 3, 2], neighbors=[1, 2])
        first_transition = [edge for edge in graph.edges if edge[0] < 2]
        second_transition = [edge for edge in graph.edges if 2 <= edge[0] < 5]
        self.assertEqual(len(first_transition), 2)
        self.assertEqual(len(second_transition), 6)

        pruned = EdgeGraph.stacked_graph(
            [2, 3, 2],
            neighbors=[1, 1],
            random_thresholds=[None, (None, 1e12)],
            seed=17
        )
        first_transition = [edge for edge in pruned.edges if edge[0] < 2]
        second_transition = [edge for edge in pruned.edges if 2 <= edge[0] < 5]
        self.assertEqual(len(first_transition), 2)
        self.assertEqual(len(second_transition), 0)

        with self.assertRaisesRegex(ValueError, "neighbor counts"):
            EdgeGraph.stacked_graph([2, 3, 2], neighbors=[1])
        with self.assertRaisesRegex(ValueError, "random-threshold entries"):
            EdgeGraph.stacked_graph(
                [2, 3, 2], random_thresholds=[(None, None)]
            )

    def test_stacked_graph_partial_edge_weights(self):
        graph = EdgeGraph.stacked_graph(
            [3, 2],
            neighbors=2,
            edge_weights={
                ((0, 0), (1, 0)): 4.0,
                ((1, 1), (0, 1)): 2.0,  # reverse direction is accepted
            }
        )
        idx = {label: i for i, label in enumerate(graph.labels)}
        heavy = (idx[(0, 0)], idx[(1, 0)])
        medium = (idx[(0, 1)], idx[(1, 1)])

        self.assertEqual(graph.weights[heavy], 4.0)
        self.assertEqual(graph.weights[medium], 2.0)
        self.assertEqual(graph.graph[heavy], 4.0)
        self.assertEqual(graph.graph[medium], 2.0)

        unspecified = next(
            tuple(edge) for edge in graph.edges
            if tuple(edge) not in (heavy, medium)
        )
        self.assertEqual(graph.graph[unspecified], 1.0)

    def test_stacked_graph_weights_set_plot_widths(self):
        graph = EdgeGraph.stacked_graph(
            [3, 2],
            neighbors=2,
            edge_weights={
                ((0, 0), (1, 0)): 4.0,
                ((0, 1), (1, 1)): 2.0,
            }
        )
        idx = {label: i for i, label in enumerate(graph.labels)}
        heavy = (idx[(0, 0)], idx[(1, 0)])
        medium = (idx[(0, 1)], idx[(1, 1)])
        edge_indices = {tuple(edge): i for i, edge in enumerate(graph.edges)}

        objects = graph.plot(
            method='stacked_layer',
            node_radius=.1,
            weight_linewidth=(1.0, 7.0),
            objects=True
        )
        widths = [edge.opts['stroke-width'] for edge in objects['edges']]

        self.assertEqual(widths[edge_indices[heavy]], 7.0)
        self.assertEqual(widths[edge_indices[medium]], 3.0)
        self.assertEqual(min(widths), 1.0)  # unspecified edges have weight 1
        for edge, (_i, j), width in zip(objects['edges'], graph.edges, widths):
            self.assertAlmostEqual(
                np.linalg.norm(edge.pos2 - objects['nodes'][j].pos), .1 + width
            )

        objects = graph.plot(
            method='stacked_layer',
            weight_linewidth=(1.0, 7.0),
            edge_style={heavy: {'line_thickness': 11.0}},
            objects=True
        )
        widths = [edge.opts['stroke-width'] for edge in objects['edges']]
        self.assertEqual(widths[edge_indices[heavy]], 11.0)

    def test_stacked_graph_callable_edge_weights(self):
        baseline = EdgeGraph.stacked_graph(
            [4, 3], neighbors=2, random_thresholds=(0.5, 0.25), seed=17
        )
        self.assertEqual(
            baseline.labels,
            [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)]
        )
        generated_edges = [tuple(edge) for edge in baseline.edges]
        generated_positions = [
            tuple(baseline.labels[i] for i in edge)
            for edge in generated_edges
        ]
        target = generated_edges[0]
        calls = []

        def edge_weight(index_pair, coordinate_pair):
            calls.append((index_pair, coordinate_pair))
            return 5.0 if index_pair == target else None

        graph = EdgeGraph.stacked_graph(
            [4, 3], neighbors=2, random_thresholds=(0.5, 0.25), seed=17,
            edge_weights=edge_weight
        )

        self.assertEqual(calls, list(zip(generated_edges, generated_positions)))
        self.assertTrue(all(isinstance(pair, tuple) for call in calls for pair in call))
        self.assertEqual(graph.weights, {target: 5.0})
        self.assertEqual(graph.graph[target], 5.0)
        for edge in generated_edges[1:]:
            self.assertEqual(graph.graph[edge], 1.0)

    def test_stacked_graph_rejects_non_edge_weight(self):
        with self.assertRaisesRegex(ValueError, "not an edge"):
            EdgeGraph.stacked_graph(
                [2, 2],
                neighbors=1,
                edge_weights={((0, 0), (1, 1)): 3.0}
            )
