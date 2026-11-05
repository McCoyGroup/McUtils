"""Independent geometry checks and signed-distance animation regression tests."""
import unittest
import numpy as np
from scipy.spatial import ConvexHull

from McUtils import Numputils as nput
from McUtils.Zachary import MeshGeometry, MeshSignedDistanceField, ScalarField
from McUtils.Plots import Graphics3D, Triangle


class MeshDistanceTests(unittest.TestCase):
    def box(self, low=-1., high=1.):
        vertices, faces = nput.uv_box()
        return MeshGeometry(low + (high-low)*vertices, faces)

    def test_box_distance_matches_analytic_formula(self):
        mesh = self.box()
        points = np.random.default_rng(731).uniform(-2., 2., (500, 3))
        q = np.abs(points)-1.
        expected = np.linalg.norm(np.maximum(q, 0.), axis=1) + np.minimum(q.max(axis=1), 0.)
        np.testing.assert_allclose(mesh.signed_distance(points), expected, atol=2.e-14, rtol=1.e-13)

    def test_closest_triangle_interior_edges_and_vertices(self):
        query = self.box().distance_query()
        points = np.array([[0, 0, 2], [2, 0, 2], [2, 2, 2], [0, 0, 0.]])
        distance, closest, ids = query.distance(points, return_closest=True)
        np.testing.assert_allclose(distance, [1., np.sqrt(2), np.sqrt(3), 1.])
        np.testing.assert_allclose(closest[:3], [[0, 0, 1], [1, 0, 1], [1, 1, 1]])
        self.assertTrue(np.all((ids >= 0) & (ids < len(query.faces))))

    def test_oblique_tetrahedron_against_brute_force_projection(self):
        vertices = np.array([[0.,0.,0.], [2.,.1,0.], [.3,1.4,.2], [.2,.3,1.7]])
        hull = ConvexHull(vertices)
        faces = nput.orient_mesh_faces_outward(vertices,hull.simplices,vertices.mean(axis=0))
        triangles = vertices[faces]
        points = np.random.default_rng(981).uniform(-.4,2.,(100,3))
        expected = []
        for p in points:
            a,b,c = triangles[:,0],triangles[:,1],triangles[:,2]
            u,v = b-a,c-a
            normal = np.cross(u,v); normal /= np.linalg.norm(normal,axis=1)[:,None]
            offset = np.einsum('ij,ij->i',p-a,normal)
            projected = p-offset[:,None]*normal
            w = projected-a
            uu=np.einsum('ij,ij->i',u,u);vv=np.einsum('ij,ij->i',v,v);uv=np.einsum('ij,ij->i',u,v)
            wu=np.einsum('ij,ij->i',w,u);wv=np.einsum('ij,ij->i',w,v)
            s=(wu*vv-wv*uv)/(uu*vv-uv*uv);t=(wv*uu-wu*uv)/(uu*vv-uv*uv)
            candidates = list(np.abs(offset[(s>=0)&(t>=0)&(s+t<=1)]))
            for start,end in ((a,b),(b,c),(c,a)):
                edge=end-start
                fraction=np.clip(np.einsum('ij,ij->i',p-start,edge)/np.einsum('ij,ij->i',edge,edge),0,1)
                candidates.extend(np.linalg.norm(p-(start+fraction[:,None]*edge),axis=1))
            distance=min(candidates)
            inside=np.all(hull.equations[:,:3]@p+hull.equations[:,3]<0)
            expected.append(-distance if inside else distance)
        np.testing.assert_allclose(MeshGeometry(vertices,faces).signed_distance(points),expected,atol=2.e-14,rtol=1.e-12)

    def test_reversed_orientation_and_nested_cavity(self):
        box = self.box()
        reversed_mesh = MeshGeometry(box.verts, box.inds[:, ::-1])
        np.testing.assert_allclose(reversed_mesh.signed_distance([[0,0,0], [2,0,0]]), [-1, 1])
        inner = self.box(-.5, .5)
        nested = MeshGeometry(np.concatenate([box.verts, inner.verts]),
                              np.concatenate([box.inds, inner.inds[:, ::-1]+len(box.verts)]))
        np.testing.assert_allclose(nested.signed_distance([[0,0,0], [.75,0,0], [2,0,0]]), [.5,-.25,1.])

    def test_queries_accept_split_vertices_without_mutation(self):
        box = self.box()
        vertices = box.verts[box.inds].reshape(-1,3)
        faces = np.arange(len(vertices)).reshape(-1,3)
        original = vertices.copy()
        query = nput.MeshDistanceQuery(vertices, faces)
        self.assertEqual(len(query.vertices), 8)
        np.testing.assert_array_equal(vertices, original)
        np.testing.assert_allclose(query.signed_distance([[0,0,0], [2,0,0]]), [-1,1])

    def test_open_and_intersecting_meshes_are_rejected(self):
        box = self.box()
        with self.assertRaisesRegex(ValueError, 'closed'):
            nput.MeshDistanceQuery(box.verts, box.inds[:-1])
        other = self.box(0., 2.)
        with self.assertRaisesRegex(ValueError, 'self-intersections'):
            nput.MeshDistanceQuery(np.concatenate([box.verts, other.verts]),
                                   np.concatenate([box.inds, other.inds+len(box.verts)]))

    def test_cached_query_and_snapshot(self):
        mesh = self.box()
        query = mesh.distance_query()
        self.assertIs(query, mesh.distance_query())
        mesh.verts[:] += 10.
        self.assertAlmostEqual(float(query.signed_distance([0,0,0])), -1.)

    def test_field_samples_are_exact_distances_in_coordinate_units(self):
        mesh = self.box()
        grid = dict(origin=[-2., -2., -2.], axes=np.diag([.5,.5,.5]), shape=[9,9,9])
        field = mesh.to_scalar_field(grid=grid, coordinate_units='Angstroms')
        self.assertIsInstance(field, MeshSignedDistanceField)
        q = np.abs(field.grid_coords)-1.
        expected = np.linalg.norm(np.maximum(q,0), axis=-1) + np.minimum(q.max(axis=-1),0)
        np.testing.assert_allclose(field.values, expected, atol=2.e-14)
        self.assertEqual(field.coordinate_units, 'Angstroms')

    def test_interpolation_reuses_one_physical_grid(self):
        a, b = self.box(), self.box(-.7, .7)
        fields = MeshSignedDistanceField.from_meshes([a,b], spacing=.35)
        self.assertTrue(np.array_equal(fields[0].origin, fields[1].origin))
        self.assertTrue(np.array_equal(fields[0].axes, fields[1].axes))
        middle = fields[0].interpolate(fields[1], .5)
        np.testing.assert_allclose(middle.values, (fields[0].values+fields[1].values)/2)
        self.assertEqual(middle.isosurface(0.).normal_direction, 'increasing')

    def test_distance_level_normals_point_outward(self):
        field = self.box().to_scalar_field(spacing=.31)
        surface = field.isosurface(0)
        mesh = surface.get_mesh()
        signed_volume = nput.mesh_volume(mesh.verts, mesh.inds, signed=True)
        self.assertGreater(signed_volume, 0.)
        self.assertEqual(surface.normal_direction, 'increasing')

    def test_explicit_animation_mode_converts_only_meshes(self):
        frames = []
        for mesh in (self.box(), self.box(-.7,.7)):
            figure = Graphics3D(backend='x3d')
            Triangle(mesh.verts, indices=mesh.inds, color='blue', transparency=.2).plot(figure)
            frames.append(figure.axes)
        scene = figure.animate_frames(frames, mode='signed_distance', signed_distance_options={'spacing':.35})
        packet = next(node.scalar_field_animation_data for node in scene._walk_scene(scene.to_x3d())
                      if hasattr(node, 'scalar_field_animation_data'))
        self.assertEqual(packet['representation'], 'signed_distance')
        self.assertEqual(packet['tracks'][0]['isovalues'], [0.,0.])
        self.assertEqual(packet['tracks'][0]['normal_direction'], 'increasing')
        self.assertTrue(scene.has_playback())
        with self.assertRaisesRegex(ValueError,'mesh detection'):
            figure.animate_frames(frames,mode='signed_distance',detect_meshes=False)

    def test_invalid_grid_and_query_parameters(self):
        mesh = self.box()
        for spacing in (0., -1., float('nan')):
            with self.assertRaises(ValueError): mesh.to_scalar_field(spacing=spacing)
        with self.assertRaises(ValueError): mesh.distance_query(leaf_size=0)
        with self.assertRaises(ValueError): mesh.signed_distance([[np.nan,0,0]])
        with self.assertRaisesRegex(ValueError, 'enclose'):
            mesh.to_scalar_field(grid=dict(origin=[0,0,0], axes=np.eye(3), shape=[2,2,2]))
        with self.assertRaisesRegex(ValueError, 'exterior band'):
            mesh.to_scalar_field(grid=dict(origin=[-1,-1,-1], axes=np.eye(3), shape=[3,3,3]))

    def test_sdf_conversion_preserves_source_precision(self):
        figures = []
        for size in (1.e-5, 1.2e-5):
            mesh = self.box(0.,size)
            figure = Graphics3D(backend='x3d')
            Triangle(mesh.verts, indices=mesh.inds).plot(figure)
            figures.append(figure)
        scene = figures[0].animate_frames([f.axes for f in figures], mode='signed_distance',
                                          signed_distance_options={'spacing':2.e-6})
        packet = next(n.scalar_field_animation_data for n in scene._walk_scene(scene.to_x3d())
                      if hasattr(n, 'scalar_field_animation_data'))
        self.assertGreater(len(packet['fields'][0]['values']), 0)


if __name__ == '__main__':
    unittest.main()
