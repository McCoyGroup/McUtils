"""
Tests for `McUtils.Numputils`, paralleling the structure and patterns of the
real `ci/tests/NumputilsTests.py` (one `TestCase`, one `test_` method per
feature, analytic derivatives cross-checked against
`McUtils.Zachary.FiniteDifferenceDerivative`).

Drafted from the stub docstrings under `McUtils/stubs/McUtils/Numputils`
(`VectorOps.py`, `TransformationMatrices.py`, `EulerSystem.py`, `SetOps.py`,
`Sparse.py`, `CoordOps.py`, `Geometry.py`) plus the patterns already present
in the real `ci/tests/NumputilsTests.py` (e.g. `test_PtsDistDeriv`,
`test_PtsAngleDeriv`, `test_SetOps`, `test_SparseArray`, `test_Bezier`,
`test_Arc`). No third-party dependency beyond `numpy`/`scipy` (both part of
McUtils' own declared dependency set) is introduced; `McUtils.Zachary` is used
for the finite-difference cross-checks the same way the real suite does.

This module intentionally avoids `Peeves.TestUtils` (`validationTest` and
friends) since `Peeves` is an internal McCoy Group testing harness, not part
of McUtils itself; plain `unittest` is used instead.
"""

import math
import unittest

import numpy as np
import scipy.linalg

import McUtils.Numputils as nput
from McUtils.Numputils import *
from McUtils.Zachary import FiniteDifferenceDerivative


class ClaudeNumputilsTests(unittest.TestCase):
    """
    Exercises `McUtils.Numputils`: vector ops, transformation matrices,
    set ops, `SparseArray`, parametric/curve geometry, and the analytic
    Cartesian-derivative machinery in `CoordOps` (cross-checked against
    finite differences).
    """

    @classmethod
    def setUpClass(cls):
        np.set_printoptions(linewidth=int(1e8))

    # region VectorOps

    def test_VecNormalize(self):
        """`vec_normalize` rescales a stack of vectors to unit norm along the given axis."""
        np.random.seed(0)
        v = np.random.rand(16, 3, 5)
        u = vec_normalize(v, axis=1)
        self.assertTrue(np.allclose(vec_norms(u, axis=1), np.ones((16, 5))))

    def test_VecCrossesAndAngles(self):
        """`vec_crosses`/`vec_angles` agree with the textbook cross-product/angle formulas."""
        np.random.seed(1)
        a = np.random.rand(10, 3)
        b = np.random.rand(10, 3)

        cross = vec_crosses(a, b, normalize=False)
        self.assertTrue(np.allclose(cross, np.cross(a, b)))

        angs, normals = vec_angles(a, b)
        ref_angs = np.array([
            np.arccos(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y)))
            for x, y in zip(a, b)
        ])
        self.assertTrue(np.allclose(angs, ref_angs))

    def test_VecDihedrals(self):
        """`pts_dihedrals` matches a hand-rolled dihedral-angle computation."""
        coords = np.array([
            [1, 0, 0],
            [1, -1, 0],
            [-1, 1, 0],
            [-1, 0, 0],
        ], dtype=float)

        ang = pts_dihedrals(coords[0], coords[1], coords[2], coords[3])

        b1 = coords[1] - coords[0]
        b2 = coords[2] - coords[1]
        b3 = coords[3] - coords[2]
        n1 = np.cross(b1, b2)
        n2 = np.cross(b2, b3)
        m1 = np.cross(n1, b2 / np.linalg.norm(b2))
        x = np.dot(n1, n2)
        y = np.dot(m1, n2)
        ref_ang = np.arctan2(y, x)

        self.assertAlmostEqual(abs(float(ang)), abs(ref_ang), places=6)

    def test_DistanceMatrixRoundTrip(self):
        """`points_from_distance_matrix` reconstructs points (up to isometry) from `distance_matrix`."""
        np.random.seed(2)
        pts = np.random.rand(8, 3)
        dmat = distance_matrix(pts)
        self.assertEqual(dmat.shape, (8, 8))
        self.assertTrue(np.allclose(np.diag(dmat), 0.0))

        rebuilt = points_from_distance_matrix(dmat, target_dim=3)
        rebuilt_dmat = distance_matrix(rebuilt)
        self.assertTrue(np.allclose(dmat, rebuilt_dmat, atol=1e-6))

    def test_ProjectionOntoAndOut(self):
        """`project_onto` + `project_out` split a vector into a basis component and its complement."""
        np.random.seed(3)
        basis = np.eye(3)[:, :2]  # the xy-plane, as column vectors
        v = np.array([1.0, 2.0, 3.0])

        onto = project_onto(v, basis)
        out = project_out(v, basis)

        self.assertTrue(np.allclose(onto, [1.0, 2.0, 0.0]))
        self.assertTrue(np.allclose(out, [0.0, 0.0, 3.0]))
        self.assertTrue(np.allclose(onto + out, v))

    def test_ProjectionMatrixIdempotent(self):
        """A `projection_matrix` `P` satisfies `P @ P == P` and `(I-P)` is its orthogonal complement."""
        np.random.seed(4)
        basis = np.linalg.qr(np.random.rand(5, 2))[0]
        P = projection_matrix(basis, orthonormal=True)
        self.assertTrue(np.allclose(P @ P, P, atol=1e-8))
        Q = orthogonal_projection_matrix(basis, orthonormal=True)
        self.assertTrue(np.allclose(P + Q, np.eye(5), atol=1e-8))

    def test_PolarDecomposition(self):
        """`polar_decomposition` factors a matrix into a symmetric part and a unitary part that recombine to it."""
        np.random.seed(5)
        A = np.random.rand(4, 4)
        P, Q = polar_decomposition(A, order='scale-first')
        self.assertTrue(np.allclose(P @ Q, A, atol=1e-8))
        self.assertTrue(np.allclose(Q @ Q.T, np.eye(4), atol=1e-8))
        self.assertTrue(np.allclose(P, P.T, atol=1e-8))

    def test_SymmetricMatrixExpLogRoundTrip(self):
        """`symmetric_matrix_exp`/`symmetric_matrix_log` match `scipy.linalg.expm`/`logm` and round-trip."""
        np.random.seed(6)
        M = np.random.rand(4, 4)
        M = M @ M.T + np.eye(4)  # symmetric positive-definite
        exp_M = symmetric_matrix_exp(M)
        self.assertEqual(exp_M.shape, (4, 4))
        self.assertTrue(np.allclose(exp_M, scipy.linalg.expm(M)))
        log_exp_M = symmetric_matrix_log(exp_M)
        self.assertTrue(np.allclose(log_exp_M, M, atol=1e-6))
        self.assertTrue(np.allclose(symmetric_matrix_log(M), scipy.linalg.logm(M)))

    def test_SymmetricMatrixExpBatched(self):
        """`symmetric_matrix_exp` matches `scipy.linalg.expm` applied matrix-by-matrix to a batch."""
        np.random.seed(6)
        base = np.random.rand(4, 4)
        base = base @ base.T + np.eye(4)
        mats = np.array([base, 0.5 * base + 0.1 * np.eye(4), 2 * base])
        exp_mats = symmetric_matrix_exp(mats)
        self.assertEqual(exp_mats.shape, (3, 4, 4))
        ref = np.array([scipy.linalg.expm(m) for m in mats])
        self.assertTrue(np.allclose(exp_mats, ref))
        self.assertTrue(np.allclose(symmetric_matrix_log(exp_mats), mats, atol=1e-6))

    def test_FractionalPower(self):
        """`fractional_power(A, 0.5)` squared reproduces the original symmetric matrix."""
        np.random.seed(7)
        M = np.random.rand(4, 4)
        M = M @ M.T + np.eye(4)
        sqrt_M = fractional_power(M, 0.5)
        self.assertTrue(np.allclose(sqrt_M @ sqrt_M, M, atol=1e-6))

    # endregion

    # region TransformationMatrices / EulerSystem

    def test_RotationMatrixOrthogonality(self):
        """A `rotation_matrix(axis, theta)` is orthogonal with determinant `+1`."""
        np.random.seed(8)
        axis = vec_normalize(np.random.rand(3))
        R = rotation_matrix(axis, np.pi / 5)
        self.assertTrue(np.allclose(R @ R.T, np.eye(3), atol=1e-8))
        self.assertAlmostEqual(np.linalg.det(R), 1.0, places=6)

    def test_SkewRotationMatrixVsExpm(self):
        """`rotation_matrix_skew` agrees with `scipy.linalg.expm` of the corresponding skew matrix."""
        np.random.seed(9)
        for _ in range(10):
            ut = np.random.rand(3)
            U1 = rotation_matrix_skew(ut)
            U2 = scipy.linalg.expm(skew_symmetric_matrix(ut))
            self.assertTrue(np.allclose(U1, U2))

    def test_SkewRotationMatrixVsExpm_HigherDimensions(self):
        """`rotation_matrix_skew` agrees with `scipy.linalg.expm` across a range of even and odd dimensions."""
        for n in (2, 3, 4, 5, 6, 7, 8, 9, 10):
            l_len = n * (n - 1) // 2
            for trial in range(20):
                np.random.seed(100 * n + trial)
                ut = np.random.rand(l_len)
                U1 = rotation_matrix_skew(ut)
                U2 = scipy.linalg.expm(skew_symmetric_matrix(ut))
                self.assertTrue(np.allclose(U1, U2, atol=1e-6), msg=f"n={n}, trial={trial}")

    def test_SkewRotationMatrixVsExpm_OddDimensionInteriorFixedAxis(self):
        """
        `youla_skew_decomp` must locate the fixed (zero-row) axis that
        `scipy.linalg.schur` leaves for an odd-dimensional skew matrix wherever it
        actually lands, not just at position `0` or `n-1` -- LAPACK's real Schur
        form gives no guarantee it will be at an edge (for `n >= 5` it can just as
        easily land in the interior, e.g. index `2` of `5`, flanked by two
        independent rotation blocks). The seed below is chosen to reliably
        reproduce such an interior fixed axis for `n=5`, so this test specifically
        exercises that code path rather than the (already well-covered) edge case.
        """
        n = 5
        np.random.seed(2000 * n + 3)  # known to produce an interior (index-2) fixed axis
        ut = np.random.rand(n * (n - 1) // 2)

        A = skew_symmetric_matrix(ut)
        s, _ = scipy.linalg.schur(A)
        row_norms = np.max(np.abs(s), axis=1)
        zero_rows = np.where(row_norms < 1e-6)[0]
        self.assertEqual(len(zero_rows), 1)
        self.assertNotIn(zero_rows[0], (0, n - 1), msg="seed no longer reproduces an interior fixed axis")

        U1 = rotation_matrix_skew(ut)
        U2 = scipy.linalg.expm(A)
        self.assertTrue(np.allclose(U1, U2, atol=1e-6))

    def test_EulerAnglesRoundTrip(self):
        """`euler_angles`/`euler_matrix` round-trip for the `'xyz'` ordering."""
        np.random.seed(10)
        angles = np.random.uniform(-np.pi / 2, np.pi / 2, 3)
        basis = np.asarray(euler_matrix(angles, ordering='xyz'))
        self.assertTrue(np.allclose(basis @ basis.T, np.eye(3), atol=1e-8))
        recovered = euler_angles(basis, ordering='xyz')
        rebuilt = np.asarray(euler_matrix(recovered, ordering='xyz'))
        self.assertTrue(np.allclose(basis, rebuilt, atol=1e-6))

    def test_TranslationAndAffineMatrix(self):
        """`translation_matrix`/`affine_matrix` correctly move a point via homogeneous coordinates."""
        shift = np.array([1.0, 2.0, 3.0])
        T = translation_matrix(shift)
        p = np.array([0.5, 0.5, 0.5, 1.0])
        moved = T @ p
        self.assertTrue(np.allclose(moved[:3], shift + 0.5))

        rot = rotation_matrix(vec_normalize(np.array([0.0, 0.0, 1.0])), np.pi / 2)
        A = affine_matrix(rot, shift)
        moved2 = A @ p
        self.assertTrue(np.allclose(moved2[:3], rot @ p[:3] + shift, atol=1e-8))

    def test_ReflectionMatrix(self):
        """A `reflection_matrix` is orthogonal with determinant `-1` and squares to the identity."""
        np.random.seed(11)
        axis = vec_normalize(np.random.rand(3))
        M = reflection_matrix(axis)
        self.assertTrue(np.allclose(M @ M.T, np.eye(3), atol=1e-8))
        self.assertAlmostEqual(np.linalg.det(M), -1.0, places=6)
        self.assertTrue(np.allclose(M @ M, np.eye(3), atol=1e-8))

    def test_PermutationMatrix(self):
        """`permutation_matrix` reorders the standard basis exactly like fancy-indexing would."""
        perm = np.array([2, 0, 1])
        P = permutation_matrix(perm)
        v = np.array([10, 20, 30])
        self.assertTrue(np.allclose(P @ v, v[perm]))

    def test_IdentifyCartesianTransformationType(self):
        """`identify_cartesian_transformation_type` classifies a rotation, a reflection, and their product."""
        np.random.seed(12)
        axis = vec_normalize(np.random.rand(3))
        test_rot = rotation_matrix(axis, np.pi / 7)
        purrf = reflection_matrix(axis)
        refl = test_rot @ purrf

        scalings, types, axes, roots, orders = identify_cartesian_transformation_type([
            test_rot, purrf, refl
        ])
        self.assertEqual(
            types.tolist(),
            [TransformationTypes.Rotation.value, TransformationTypes.Reflection.value, TransformationTypes.ImproperRotation.value]
        )

    # endregion

    # region SetOps (lifted directly from ci/tests/NumputilsTests.py::test_SetOps)

    def test_Unique(self):
        """`unique` sorts and de-duplicates both 1D arrays and rows of a 2D array."""
        unums, sorting = unique([1, 2, 3, 4, 5])
        self.assertEqual(unums.tolist(), [1, 2, 3, 4, 5])
        self.assertEqual(sorting.tolist(), [0, 1, 2, 3, 4])

        unums, sorting = unique([1, 1, 3, 4, 5])
        self.assertEqual(unums.tolist(), [1, 3, 4, 5])

        unums, sorting = unique([[1, 3], [1, 1], [1, 3]])
        self.assertEqual(unums.tolist(), [[1, 1], [1, 3]])
        self.assertEqual(sorting.tolist(), [1, 0, 2])

    def test_IntersectionDifferenceContained(self):
        """`intersection`/`difference`/`contained` agree with the plain-NumPy equivalents."""
        inters, sortings, merge = intersection([1, 1, 3, 2, 5], [0, 0, 0, 5, 1])
        self.assertEqual(inters.tolist(), [1, 5])

        diffs, sortings, merge = difference([1, 1, 3, 2, 5], [0, 0, 0, 5, 1])
        self.assertEqual(diffs.tolist(), [2, 3])

        diffs, sortings, merge = contained([1, 1, 3, 2, 5], [0, 0, 0, 5, 1])
        self.assertEqual(diffs.tolist(), [True, True, False, False, True])

        np.random.seed(13)
        ugh = np.arange(1000)
        bleh = np.random.choice(1000, size=100)
        diffs, sortings, merge = contained(bleh, ugh)
        self.assertEqual(diffs.tolist(), np.isin(bleh, ugh).tolist())

        diffs2, sortings, merge = contained(bleh, ugh, method='find')
        self.assertEqual(diffs.tolist(), diffs2.tolist())

    def test_GroupBy(self):
        """`group_by` splits an array into per-key groups matching a manual partition."""
        ar = np.array([10, 11, 12, 13, 14, 15])
        keys = np.array([0, 1, 0, 1, 2, 0])
        (unique_keys, groups), sorting = group_by(ar, keys)
        by_key = dict(zip(unique_keys.tolist(), [list(g) for g in groups]))
        self.assertEqual(sorted(by_key[0]), [10, 12, 15])
        self.assertEqual(sorted(by_key[1]), [11, 13])
        self.assertEqual(sorted(by_key[2]), [14])

    # endregion

    # region SparseArray (lifted directly from ci/tests/NumputilsTests.py::test_SparseArray)

    def test_SparseArray(self):
        """`SparseArray.from_data` supports `shape`, `transpose`, item indexing, and `tensordot` like a dense array."""
        array = SparseArray.from_data([
            [[1, 0, 0], [0, 0, 1], [0, 1, 0]],
            [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
            [[0, 1, 0], [1, 0, 1], [0, 0, 1]],
            [[1, 1, 0], [1, 0, 1], [0, 1, 1]],
        ])

        self.assertEqual(array.shape, (4, 3, 3))
        tp = array.transpose((1, 0, 2))
        self.assertEqual(tp.shape, (3, 4, 3))
        self.assertLess(
            np.linalg.norm((tp.asarray() - array.asarray().transpose((1, 0, 2))).flatten()), 1e-8
        )
        self.assertEqual(array[2, :, 2].shape, (3,))
        td = array.tensordot(array, axes=[1, 1])
        self.assertEqual(td.shape, (4, 3, 4, 3))
        self.assertEqual(array.tensordot(array, axes=[[1, 2], [1, 2]]).shape, (4, 4))

    def test_SparseArray_directConstructorRegression(self):
        """
        The real `ci/tests/NumputilsTests.py::test_SparseArray` constructs a
        `SparseArray` by calling the class directly (`SparseArray([...])`), the same
        way `test_SparseArray` above uses `SparseArray.from_data([...])`. Against
        this installed version, direct construction raises `TypeError` -- the base
        class defines neither `__new__` nor `__init__`, so `object.__new__` rejects
        the positional argument. This documents that regression/gap explicitly
        rather than silently routing around it.
        """
        data = [[[1, 0, 0], [0, 0, 1], [0, 1, 0]]]
        with self.assertRaises(TypeError):
            SparseArray(data)

    # endregion

    # region Geometry / curves (mirrors ci/tests/NumputilsTests.py::test_Arc / test_Bezier)

    def test_ArcPointsFromEndpoints(self):
        """Every point on `arc_points_from_endpoints`'s (circular) arc sits at the requested radius from its center."""
        points, arc = nput.arc_points_from_endpoints(
            [.8, 0],
            [-.8, 0],
            radius=1.5,
            return_arc=True,
            clockwise=True,
            use_major_rotation=False,
            rotation=np.pi / 3
        )
        center = arc[0]
        dists = np.linalg.norm(points - np.asarray(center).reshape(1, -1), axis=-1)
        self.assertTrue(np.allclose(dists, 1.5, atol=1e-6))

    def test_BezierEvalEndpoints(self):
        """A Bezier curve defined by `knots` starts and ends exactly at its first and last knots."""
        knots = np.array([
            [0, 0], [.1, 1], [.5, 2], [.8, 0], [1, 0], [1.2, 0], [2, 2]
        ])
        points = nput.bezier_eval(knots, 50, return_points=False)
        self.assertTrue(np.allclose(points[0], knots[0], atol=1e-6))
        self.assertTrue(np.allclose(points[-1], knots[-1], atol=1e-6))

    def test_ParametricPathPoints(self):
        """`parametric_path_points` stitches Bezier/line/spline segments into one continuous point path."""
        point = nput.parametric_path_points([
            ["BEZIER", [(0, 5), (5, 10), (10, 10)]],
            ["line", [(-5, 0), (-10, -5), (-10, -10)]],
            ["interp", [(0, 5), (5, 10), (10, 10)], {'k': 2}]
        ])
        self.assertEqual(point.shape[-1], 2)
        self.assertGreater(len(point), 3)

    # endregion

    # region CoordOps analytic derivatives vs. finite differences
    # (adapted from ci/tests/NumputilsTests.py::test_PtsDistDeriv / test_PtsAngleDeriv / test_PtsDihedralsDeriv,
    # using scalar atom indices -- see the *_BatchedAtomIndices regression tests below for the batched case)

    def test_DistDerivValueAndFiniteDifference(self):
        """`dist_deriv`'s value and first-derivative tensor match a direct/finite-difference computation."""
        np.random.seed(14)
        coords = np.random.rand(16, 3)
        dist, derivs, *_ = dist_deriv(coords, 5, 4, order=1)
        self.assertAlmostEqual(float(dist), float(vec_norms(coords[4] - coords[5])), places=8)

        # derivs is the full (48,) = (16 atoms x 3) Cartesian gradient; only atoms 5 and 4 are nonzero
        deriv_sub = np.concatenate([derivs[5 * 3:5 * 3 + 3], derivs[4 * 3:4 * 3 + 3]])
        fd = FiniteDifferenceDerivative(
            lambda pt: vec_norms(pt[..., 1, :] - pt[..., 0, :]),
            function_shape=((None, 3), 0),
            mesh_spacing=1.0e-5
        )
        fd1, = fd(coords[(5, 4),]).derivative_tensor([1])
        self.assertTrue(np.allclose(deriv_sub, fd1.flatten(), atol=1e-5), msg="{} and {} aren't close".format(
            deriv_sub, fd1.flatten()
        ))

    def test_AngleDerivValueAndFiniteDifference(self):
        """`angle_deriv`'s value and first-derivative tensor match a direct/finite-difference computation."""
        np.random.seed(0)
        coords = np.random.rand(16, 3)
        ang, derivs, *_ = angle_deriv(coords, 5, 4, 6, order=1)
        self.assertAlmostEqual(float(ang), float(vec_angles(coords[4] - coords[5], coords[6] - coords[5])[0]), places=8)

        deriv_sub = np.concatenate([derivs[5 * 3:5 * 3 + 3], derivs[4 * 3:4 * 3 + 3], derivs[6 * 3:6 * 3 + 3]])
        fd = FiniteDifferenceDerivative(
            lambda pt: vec_angles(pt[..., 1, :] - pt[..., 0, :], pt[..., 2, :] - pt[..., 0, :])[0],
            function_shape=((None, 3), 0),
            mesh_spacing=1.0e-5
        )
        fd1, = fd(coords[(5, 4, 6),]).derivative_tensor([1])
        self.assertTrue(np.allclose(deriv_sub, fd1.flatten(), atol=1e-4), msg="{} and {} aren't close".format(
            deriv_sub, fd1.flatten()
        ))

    def test_DihedDerivValueMatchesDirectDihedral(self):
        """`dihed_deriv`'s returned value matches a direct `pts_dihedrals` computation of the same dihedral."""
        np.random.seed(0)
        coords = np.random.rand(16, 3)
        ang, *_ = dihed_deriv(coords, 4, 5, 6, 7, order=1)
        ang2 = pts_dihedrals(coords[4], coords[5], coords[6], coords[7])
        self.assertAlmostEqual(abs(float(ang2)), abs(float(ang)), places=6)

    def test_DistDerivBatchedAtomIndicesRegression(self):
        """
        `dist_deriv`'s own docstring types `i`/`j` as `int | Iterable[int]`, and the
        real `ci/tests/NumputilsTests.py::test_PtsDistDeriv` calls it exactly this
        way (`dist_deriv(coords, [5, 4], [4, 5], order=2)`) to get derivatives for
        several atom pairs at once. Against this installed version that call -- and
        even the simplest one-pair-as-a-list-of-1 case -- raises inside
        `fill_disp_jacob_atom`'s `np.broadcast_to`, regardless of `order`. Only bare
        (non-list) integer indices work. This documents that regression explicitly.
        """
        np.random.seed(14)
        coords = np.random.rand(16, 3)
        with self.assertRaises(ValueError):
            dist_deriv(coords, [5, 4], [4, 5], order=1)
        with self.assertRaises(ValueError):
            dist_deriv(coords, [5], [4], order=1)  # even a singleton list fails

    def test_AngleDerivBatchedAtomIndicesRegression(self):
        """Same batched-index regression as `test_DistDerivBatchedAtomIndicesRegression`, for `angle_deriv`."""
        np.random.seed(0)
        coords = np.random.rand(16, 3)
        with self.assertRaises(ValueError):
            angle_deriv(coords, [5, 5], [4, 6], [6, 4], order=1)

    def test_DihedDerivBatchedAtomIndicesRegression(self):
        """Same batched-index regression as `test_DistDerivBatchedAtomIndicesRegression`, for `dihed_deriv`."""
        np.random.seed(0)
        coords = np.random.rand(16, 3)
        with self.assertRaises(ValueError):
            dihed_deriv(coords, [4], [5], [6], [7], order=1)

    # endregion


if __name__ == '__main__':
    unittest.main(verbosity=2)
