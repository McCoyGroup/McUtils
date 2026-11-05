"""Scalar-field semantics and default X3D animation integration."""
import unittest
import os
import shutil
import subprocess
import json
import numpy as np
from McUtils.Zachary import ScalarField, ScalarFieldIsosurface
from McUtils.ExternalPrograms import CubePropEvaluator, CubeFileIsosurface
from McUtils.Plots import Graphics3D, Triangle


class ScalarFieldTests(unittest.TestCase):
    def field(self, offset=0., **options):
        grid = np.indices((5, 5, 5), dtype=float)
        return ScalarField(grid[0] + 2 * grid[1] - grid[2] + offset, **options)

    def packets(self, scene):
        return [node.scalar_field_animation_data for node in scene._walk_scene(scene.to_x3d())
                if hasattr(node, 'scalar_field_animation_data')]

    def test_linear_field_interpolation_and_exact_endpoints(self):
        a, b = self.field(), self.field(4.)
        self.assertIs(a.interpolate(b, 0), a)
        self.assertIs(a.interpolate(b, 1), b)
        np.testing.assert_allclose(a.interpolate(b, .25).values, a.values + 1.)
        for fraction in (-.01, 1.01, float('nan')):
            with self.assertRaises(ValueError):
                a.interpolate(b, fraction)

    def test_spatial_evaluation_in_affine_coordinates(self):
        axes = np.array([[.4, .1, 0], [0, .5, .2], [0, 0, .6]])
        a = self.field(origin=[1., 2., 3.], axes=axes, order=1)
        point = np.array([[1.2, 2.1, .8]])
        np.testing.assert_allclose(a(a.unembed_points(point)), point[:, 0] + 2 * point[:, 1] - point[:, 2])

    def test_grid_and_unit_mismatches_are_explicit(self):
        a = self.field()
        others = [self.field(origin=[.1, 0, 0]), self.field(axes=2 * np.eye(3)),
                  self.field(coordinate_units='BohrRadius'), ScalarField(np.zeros((6, 5, 5)))]
        for other in others:
            with self.assertRaises(ValueError):
                a.interpolate(other, .5)

    def test_invalid_grids_and_fields(self):
        for values in (np.full((2, 2, 2), np.nan), np.zeros((1, 2, 2)), np.ones((2, 2, 2), complex)):
            with self.assertRaises(ValueError):
                ScalarField(values)
        with self.assertRaises(ValueError):
            ScalarField(np.zeros((2, 2, 2)), axes=np.zeros((3, 3)))

    def test_surface_interpolation_and_empty_geometry(self):
        a, b = self.field().isosurface(1.2), self.field(2.).isosurface(1.8)
        c = a.interpolate(b, .3)
        self.assertIsInstance(c, ScalarFieldIsosurface)
        np.testing.assert_allclose(c.field.values, a.field.values + .6)
        self.assertAlmostEqual(c.isovalue, 1.38)
        self.assertEqual(ScalarField(np.ones((3, 3, 3))).isosurface(0).get_mesh().inds.shape, (0, 3))

    def test_cube_field_preserves_legacy_mesh_api(self):
        values = self.field().values
        cube = CubePropEvaluator([0, 0, 0], np.eye(3), values.shape, values)
        self.assertIsInstance(cube, ScalarField)
        surface = cube.isosurface(1.3)
        self.assertIsInstance(surface, CubeFileIsosurface)
        np.testing.assert_array_equal(surface.get_mesh().inds, cube.get_isosurface(1.3, return_normals=False).inds)
        np.testing.assert_allclose(surface.get_mesh().verts, cube.get_isosurface(1.3, return_normals=False).verts)

    def test_default_animation_retains_sources_and_shares_fields(self):
        a, b = self.field(), self.field(1.)
        frames = []
        for field in (a, b):
            figure = field.isosurface(1.2).plot(transparency=.2)
            field.isosurface(-1.2).plot(figure=figure, color='yellow', transparency=.2)
            frames.append(figure.axes)
        scene = figure.animate_frames(frames)
        packet, = self.packets(scene)
        self.assertEqual(len(packet['fields']), 2)
        self.assertEqual(len(packet['tracks']), 2)
        self.assertEqual(packet['tracks'][0]['fields'], packet['tracks'][1]['fields'])
        self.assertEqual(packet['interpolation'], 'linear')
        tags = [str(node.tag).lower() for node in scene._walk_scene(scene.to_x3d())]
        self.assertNotIn('switch', tags)
        self.assertEqual(tags.count('timesensor'), 1)
        self.assertTrue(scene.has_playback())
        self.assertIn('createScalarFieldIsosurfaceEvaluator', scene.to_html().tostring())

    def test_animation_rejects_incompatible_fields(self):
        a = self.field().isosurface(1.2).plot()
        b = self.field(origin=[1, 0, 0]).isosurface(1.2).plot()
        with self.assertRaisesRegex(ValueError, 'physical grid'):
            a.animate_frames([a.axes, b.axes])

    def test_plain_mesh_animation_remains_a_mesh_track(self):
        figures = []
        for z in (0., .2):
            f = Graphics3D(backend='x3d')
            Triangle([[0, 0, z], [1, 0, z], [0, 1, z]], indices=[[0, 1, 2]]).plot(f)
            figures.append(f)
        scene = figures[0].animate_frames([f.axes for f in figures])
        self.assertEqual(self.packets(scene), [])
        self.assertEqual(len(scene.get_mesh_comparisons()), 1)

    def test_multiple_keys_and_repeated_field_payloads(self):
        a, b = self.field(), self.field(1.)
        figures = [field.isosurface(1.2).plot() for field in (a, b, a)]
        packet, = self.packets(figures[0].animate_frames([f.axes for f in figures]))
        self.assertEqual(packet['tracks'][0]['fields'], [0, 1, 0])
        self.assertEqual(packet['times'], [0., .5, 1.])

    def test_field_and_mesh_tracks_share_the_native_clock(self):
        figures = []
        for offset in (0., .2):
            f = self.field(offset).isosurface(1.2).plot()
            Triangle([[0, 0, offset], [1, 0, offset], [0, 1, offset]], indices=[[0, 1, 2]]).plot(f)
            figures.append(f)
        scene = figures[0].animate_frames([f.axes for f in figures])
        self.assertEqual(len(self.packets(scene)), 1)
        self.assertEqual(len(scene.get_mesh_comparisons()), 1)
        clocks = [n for n in scene._walk_scene(scene.to_x3d()) if str(n.tag).lower() == 'timesensor']
        self.assertEqual(len(clocks), 1)

    def test_javascript_contours_match_python_at_intermediate_fractions(self):
        # Optional Node runtime test; no browser or third-party JS packages needed.
        node = os.environ.get('MCUTILS_TEST_NODE') or shutil.which('node')
        if node is None:
            self.skipTest('Node is unavailable; set MCUTILS_TEST_NODE to run JS/Python contour parity')
        grid = np.indices((5, 5, 5), dtype=float)[0]
        axes = [[.3, .07, 0], [0, .4, .05], [0, 0, .5]]
        fields = [ScalarField(values, origin=[.1, -.3, .2], axes=axes) for values in (grid - 5.43, grid + 1.71)]
        figures = [field.isosurface(0.).plot() for field in fields]
        packet, = self.packets(figures[0].animate_frames([f.axes for f in figures]))
        source = ScalarFieldIsosurface.javascript_source()
        script = """
const fs = require('fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const factory = new Function(input.source + '\\nreturn createScalarFieldIsosurfaceEvaluator;')();
const evaluator = factory(input.packet);
process.stdout.write(JSON.stringify(input.fractions.map(t => evaluator.evaluate(t).meshes[0])));
"""
        fractions = [0., .25, .5, .75, 1.]
        completed = subprocess.run([node, '-e', script], input=json.dumps(dict(
            source=source, packet=packet, fractions=fractions)), text=True, capture_output=True, check=True)
        meshes = json.loads(completed.stdout)
        self.assertEqual(len(meshes[0]['faces']), 0)
        self.assertGreater(len(meshes[2]['faces']), 0)
        self.assertEqual(len(meshes[-1]['faces']), 0)
        for fraction, actual in zip(fractions, meshes):
            expected = fields[0].interpolate(fields[1], fraction).isosurface(0.).get_mesh()
            np.testing.assert_array_equal(np.asarray(actual['faces']).reshape(-1, 3), expected.inds)
            np.testing.assert_allclose(np.asarray(actual['vertices']).reshape(-1, 3), expected.verts, atol=2.e-12, rtol=0.)


if __name__ == '__main__':
    unittest.main()
