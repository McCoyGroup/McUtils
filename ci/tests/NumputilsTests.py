import collections
import itertools
import math
import os.path

from Peeves.TestUtils import *
from Peeves import BlockProfiler
from McUtils.Numputils import *
from McUtils.Zachary import FiniteDifferenceDerivative
from unittest import TestCase
import numpy as np, scipy, functools as ft

class NumputilsTests(TestCase):

    problem_coords = np.array([
                                  [-1.86403557e-17, -7.60465240e-02,  4.62443228e-02],
                                  [ 6.70904773e-17, -7.60465240e-02, -9.53755677e-01],
                                  [ 9.29682337e-01,  2.92315732e-01,  4.62443228e-02],
                                  [ 2.46519033e-32, -1.38777878e-17,  2.25076602e-01],
                                  [-1.97215226e-31,  1.43714410e+00, -9.00306410e-01],
                                  [-1.75999392e-16, -1.43714410e+00, -9.00306410e-01]
    ])

    @validationTest
    def test_VecOps(self):
        v = np.random.rand(16, 3, 5)
        u = vec_normalize(v, axis=1)
        self.assertTrue(
            np.allclose(vec_norms(u, axis=1), np.ones((16, 5)))
        )

    @validationTest
    def test_OptimizeClassic(self):
        ndim = 6

        np.random.seed(1)
        rot = rotation_matrix_skew(np.random.rand(math.comb(ndim, 2)))
        # A = rot @ np.diag(np.random.uniform(.5, 2, (ndim,))) @ rot.T
        # A_inv = np.linalg.inv(A)
        # def f(guess, *_):
        #     return 1/2 * np.tensordot(guess, A, axes=[-1, 0])[:, np.newaxis, :] @ guess[:, :, np.newaxis]
        # def fjac(guess, *_):
        #     return np.tensordot(guess, A, axes=[-1, 0])
        # def fhess(guess, *_):
        #     return np.broadcast_to(A_inv[np.newaxis], (len(guess),) + A.shape)
        #
        # minimum, convd, (error, its) = iterative_step_minimize(
        #     np.random.rand(ndim),
        #     NewtonStepFinder(fjac, fhess, hess_mode='inverse'),
        #     max_iterations=3
        # )
        # self.assertEquals(error, 0)

        def f(guess, *_):
            guess = (rot[np.newaxis] @ guess[:, :, np.newaxis]).reshape(guess.shape)
            return np.sum(np.sin(guess), axis=-1) + 1/2*np.sum((guess)**2, axis=-1)
            # return 1/2*np.sum(guess**2, axis=-1)
        def fjac(guess, *_):
            guess = (rot[np.newaxis] @ guess[:, :, np.newaxis]).reshape(guess.shape)
            return (rot.T[np.newaxis] @ (np.cos(guess) + guess)[:, :, np.newaxis]).reshape(guess.shape)
            # return guess
        def fhess(guess, *_):
            guess = (rot[np.newaxis] @ guess[:, :, np.newaxis]).reshape(guess.shape)
            h = -vec_tensordiag(np.sin(guess)) + identity_tensors(guess.shape[:-1], guess.shape[-1])
            return rot.T[np.newaxis] @ h @ rot[np.newaxis]
            # return identity_tensors(guess.shape[:-1], guess.shape[-1])
        # for i in range(1000):
        np.random.seed(1)
        # [ 0.03378176  0.06135116  0.46629297  0.38138027 -1.05175418 -1.34294785]
        guess = vec_normalize(np.random.uniform(-np.pi/2, np.pi/2, ndim))
        minimum, convd, (error, its) = iterative_step_minimize(
            guess,
            NewtonStepFinder(f, fjac, fhess),
            # GradientDescentStepFinder(f, fjac),
            # ConjugateGradientStepFinder(f, fjac),
            # QuasiNewtonStepFinder(f, fjac),
            max_displacement=.1,
            max_iterations=50,
            unitary=True,
            tol=1e-15
        )
            # if error > 1e-4:
            #     print(i)
            #     break
        print()
        print(error, its)
        print(guess, np.linalg.norm(guess, axis=-1))
        print(minimum, np.linalg.norm(minimum, axis=-1))

    @validationTest
    def test_BoysLocalize(self):

        ndim = 4*3

        np.random.seed(1)
        rot = rotation_matrix_skew(np.random.uniform(
            1, 2,
            math.comb(ndim, 2)
        ))[:, 6:]

        def f(col):
            subcol = col.reshape(-1, 3)
            return np.sum(vec_dots(subcol, subcol, axis=-1)**2)
        def fprime(col):
            subcol = col.reshape(-1, 3)
            squares = vec_dots(subcol, subcol, axis=-1)
            return 4 * (subcol*squares[:, np.newaxis]).flatten()

        def op_f(col_i, col_j):
            subcol1 = col_i.reshape(-1, 3)
            subcol2 = col_j.reshape(-1, 3)
            a = np.sum(vec_dots(subcol1, subcol1, axis=-1) ** 2)
            b = np.sum(vec_dots(subcol1, subcol2, axis=-1) ** 2)
            c = np.sum(vec_dots(subcol2, subcol2, axis=-1) ** 2)
            return a, b, c



        mat, U, err = jacobi_maximize(rot,
                                      # GradientDescentRotationGenerator(f, fprime),
                                      LineSearchRotationGenerator(f),
                                      # displacement_localizing_rotation_generator,
                                      # OperatorMatrixRotationGenerator(f, op_f),
                                      max_iterations=30
                                      )
        with np.printoptions(linewidth=1e8):
            # print(
            #     np.round(100*np.sum((rot ** 2).reshape(-1, 3, rot.shape[-1]), axis=1))
            # )
            print(
                np.round(100*np.sum((mat ** 2).reshape(-1, 3, rot.shape[-1]), axis=1))
            )
            """
# Unmixed
 [[12.  1. 28.  9. 50. 51.]
  [21. 25.  5.  6. 10. 12.]
  [54. 23. 11.  9. 22. 16.]
  [13. 50. 56. 77. 17. 21.]]
 
 # Gradient Descent
 [[68.  3. 69.  1.  8.  2.]
  [ 6.  4. 13. 41.  9.  6.]
  [26. 10. 15.  1. 81.  1.]
  [ 0. 83.  3. 57.  2. 90.]]
 
 # Linesearch
 [[ 1. 71. 69.  1.  6.  2.]
  [41. 12.  7.  6. 10.  4.]
  [ 1. 16. 24.  1. 83. 10.]
  [57.  1.  0. 91.  0. 85.]]
 
 # Analytic
[[67. 63.  4.  2.  6.  8.]
 [ 6. 17.  5.  9.  8. 34.]
 [23. 15. 12.  7. 69. 10.]
 [ 5.  5. 79. 82. 17. 48.]]
 
 # Pairwise
 [[ 8.  1. 10. 15. 50. 66.]
  [13. 35.  5. 11. 10.  7.]
  [73.  7.  2.  5. 22. 25.]
  [ 6. 57. 83. 69. 17.  3.]]
"""
        raise Exception(np.linalg.det(U), err)

    @validationTest
    def test_NEB(self):
        ndim = 1

        np.random.seed(1)
        if ndim == 1:
            rot = np.array([[1]])
        else:
            rot = rotation_matrix_skew(np.random.rand(math.comb(ndim, 2)))

        # A = rot @ np.diag(np.random.uniform(.5, 2, (ndim,))) @ rot.T
        # A_inv = np.linalg.inv(A)
        # def f(guess, *_):
        #     return 1/2 * np.tensordot(guess, A, axes=[-1, 0])[:, np.newaxis, :] @ guess[:, :, np.newaxis]
        # def fjac(guess, *_):
        #     return np.tensordot(guess, A, axes=[-1, 0])
        # def fhess(guess, *_):
        #     return np.broadcast_to(A_inv[np.newaxis], (len(guess),) + A.shape)
        #
        # minimum, convd, (error, its) = iterative_step_minimize(
        #     np.random.rand(ndim),
        #     NewtonStepFinder(fjac, fhess, hess_mode='inverse'),
        #     max_iterations=3
        # )
        # self.assertEquals(error, 0)

        def f(guess, *_):
            guess = (rot[np.newaxis] @ guess[:, :, np.newaxis]).reshape(guess.shape)
            return np.sum(np.sin(guess), axis=-1) + 1 / 2 * np.sum((guess) ** 2, axis=-1)
            # return 1/2*np.sum(guess**2, axis=-1)

        def fjac(guess, *_):
            guess = (rot[np.newaxis] @ guess[:, :, np.newaxis]).reshape(guess.shape)
            return (rot.T[np.newaxis] @ (np.cos(guess) + guess)[:, :, np.newaxis]).reshape(guess.shape)
            # return guess

        def fhess(guess, *_):
            guess = (rot[np.newaxis] @ guess[:, :, np.newaxis]).reshape(guess.shape)
            h = -vec_tensordiag(np.sin(guess)) + identity_tensors(guess.shape[:-1], guess.shape[-1])
            return rot.T[np.newaxis] @ h @ rot[np.newaxis]
            # return identity_tensors(guess.shape[:-1], guess.shape[-1])

        # for i in range(1000):
        np.random.seed(1)
        # [ 0.03378176  0.06135116  0.46629297  0.38138027 -1.05175418 -1.34294785]
        guess = vec_normalize(np.random.uniform(-np.pi / 2, np.pi / 2, ndim))
        minimum, convd, (error, its) = iterative_step_minimize(
            guess,
            [
                NewtonStepFinder(f, fjac, fhess)
            ],
            # GradientDescentStepFinder(f, fjac),
            # ConjugateGradientStepFinder(f, fjac),
            # QuasiNewtonStepFinder(f, fjac),
            max_displacement=.1,
            max_iterations=50,
            unitary=True,
            tol=1e-15
        )
        # if error > 1e-4:
        #     print(i)
        #     break
        print()
        print(error, its)
        print(guess, np.linalg.norm(guess, axis=-1))
        print(minimum, np.linalg.norm(minimum, axis=-1))

    @debugTest
    def test_coordBases(self):
        coords = np.random.rand(6, 3)

        b = angle_basis(coords, 1, 0, 2)
        # print(b[0])


    @validationTest
    def test_skewRotationMatrix(self):
        for _ in range(10):
            ut = np.random.rand(3)
            U1 = rotation_matrix_skew(ut)
            U2 = scipy.linalg.expm(skew_symmetric_matrix(ut))
            self.assertTrue(np.allclose(U1, U2))

        ut = np.random.rand(3)
        reference_rotation = rotation_matrix_skew(ut)
        ref_struct = np.array([
            [0, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ])
        rot_struct = ref_struct @ reference_rotation

        def mat_fun(upper_triangle):
            test_rot = rotation_matrix_skew(upper_triangle)
            test_struct = rot_struct@test_rot
            return np.linalg.norm(ref_struct - test_struct)

        x = np.random.rand(3)
        for _ in range(10):
            opt = scipy.optimize.minimize(mat_fun, x, method='Nelder-Mead', tol=1e-8)
            x = opt.x
        print(opt)

        print('-'*20)
        print('Upper Triangle:', ut)
        print(reference_rotation.T)
        print('-'*20)
        test_rot = rotation_matrix_skew(opt.x)
        print('Upper Triangle:', opt.x)
        print(test_rot)
        print('-'*20)
        print(ref_struct)
        print(rot_struct@test_rot)

        self.assertLess(opt.fun, 1e-6)

    @validationTest
    def test_ProblemPtsAllDerivs(self):
        from McUtils.Numputils import Options as NumOpts

        NumOpts.zero_placeholder = np.inf

        coords = self.problem_coords

        # dists, dist_derivs, dist_derivs_2 = dist_deriv(coords, [0, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 0], order=2)
        # angs, ang_derivs, ang_derivs_2 = angle_deriv(coords,
        #                                              [0, 1, 2, 3, 4, 5],
        #                                              [1, 2, 3, 4, 5, 0],
        #                                              [2, 3, 4, 5, 0, 1],
        #                                              order=2
        #                                              )
        # diheds, dihed_derivs, dihed_derivs_2 = dihed_deriv(coords,
        #                                                [0, 1, 2, 3, 4, 5],
        #                                                [1, 2, 3, 4, 5, 0],
        #                                                [2, 3, 4, 5, 0, 1],
        #                                                [3, 4, 5, 0, 1, 2],
        #                                                order=2
        #                                                )

        diheds, dihed_derivs, dihed_derivs_2 = dihed_deriv(coords,
                                                           [3],
                                                           [4],
                                                           [5],
                                                           [0],
                                                           order=2
                                                           )

        # raise Exception([
        #     diheds,
        #     [np.min(dihed_derivs), np.max(dihed_derivs)],
        #     [np.min(dihed_derivs_2), np.max(dihed_derivs_2)]
        #     ])
        #
        # raise Exception(
        #     np.array([dists.flatten(), np.round(np.rad2deg(angs.flatten()), 1), np.round(np.rad2deg(diheds.flatten()), 1)]),
        #     [
        #         [np.min(dist_derivs), np.max(dist_derivs)],
        #         [np.min(dist_derivs_2), np.max(dist_derivs_2)]
        #         ],
        #     [
        #         [np.min(ang_derivs), np.max(ang_derivs)],
        #         [np.min(ang_derivs_2), np.max(ang_derivs_2)]
        #         ],
        #     [
        #         [np.min(dihed_derivs), np.max(dihed_derivs)],
        #         [np.min(dihed_derivs_2), np.max(dihed_derivs_2)]
        #     ]
        # )

    @validationTest
    def test_PtsDihedralsDeriv(self):
        # need some proper values to test this against...
        np.random.seed(0)
        coords = np.random.rand(16, 3)

        angs, derivs, derivs_2 = dihed_deriv(coords, [4, 7], [5, 6], [6, 5], [7, 4], order=2)
        ang = angs[0]; deriv = derivs[:, 0, :]; deriv_2 = derivs_2[:, :, 0, :, :]
        ang2 = pts_dihedrals(coords[4],  coords[5], coords[6], coords[7])

        self.assertEquals(ang2, ang[0])

        fd = FiniteDifferenceDerivative(
            lambda pt: pts_dihedrals(pt[..., 0, :], pt[..., 1, :], pt[..., 2, :], pt[..., 3, :]),
            function_shape=((None, 4, 3), 0),
            mesh_spacing=1.0e-5
        )
        dihedDeriv_fd = FiniteDifferenceDerivative(
            lambda pts: dihed_deriv(pts, 0, 1, 2, 3, order=1)[1].squeeze().transpose((1, 0, 2)),
            function_shape=((None, 4, 3), (None, 4, 3)),
            mesh_spacing=1.0e-5
        )

        fd1, fd2 = fd(coords[(4, 5, 6, 7),]).derivative_tensor([1, 2])
        fd2_22 = dihedDeriv_fd(coords[(4, 5, 6, 7),]).derivative_tensor(1)

        self.assertTrue(np.allclose(deriv.flatten(), fd1.flatten()), msg="{} and {} aren't close".format(
            deriv.flatten(), fd1.flatten()
        ))

        d2_flat = np.concatenate(
            [
                np.concatenate([deriv_2[0, 0], deriv_2[0, 1], deriv_2[0, 2], deriv_2[0, 3]], axis=1),
                np.concatenate([deriv_2[1, 0], deriv_2[1, 1], deriv_2[1, 2], deriv_2[1, 3]], axis=1),
                np.concatenate([deriv_2[2, 0], deriv_2[2, 1], deriv_2[2, 2], deriv_2[2, 3]], axis=1),
                np.concatenate([deriv_2[3, 0], deriv_2[3, 1], deriv_2[3, 2], deriv_2[3, 3]], axis=1)
            ],
            axis=0
        )

        bleh = fd2_22.reshape(12, 12)
        # raise Exception("\n"+"\n".join("{} {}".format(a, b) for a, b in zip(
        #     np.round(deriv_2[2, 2], 3), np.round(bleh[6:9, 6:9], 3))
        #                                ))
        # raise Exception(np.round(d2_flat-bleh, 3))
        # raise Exception("\n"+"\n".join("{}\n{}".format(a, b) for a, b in zip(np.round(d2_flat, 3), np.round(bleh, 3))))
        self.assertTrue(np.allclose(d2_flat.flatten(), bleh.flatten(), atol=1.0e-7), msg="d2: {} and {} differ".format(
            d2_flat.flatten(), bleh.flatten()
        ))
        self.assertTrue(np.allclose(d2_flat.flatten(), fd2.flatten(), atol=1.0e-3), msg="d2: {} and {} differ".format(
            d2_flat.flatten(), fd2.flatten()
        ))

        # raise Exception(fd2.flatten(), deriv_2.flatten())

        coords = np.array([
            [ 1,  0, 0],
            [ 1, -1, 0],
            [-1,  1, 0],
            [-1,  0, 0],
        ])

        angs, derivs = dihed_deriv(coords, 0, 1, 2, 3, order=1)
        ang = angs[0]
        deriv = derivs
        # deriv_2 = derivs_2[:, :, 0, :, :]
        ang2 = pts_dihedrals(coords[0], coords[1], coords[2], coords[3])

        self.assertTrue(np.allclose(np.abs(ang2), ang))

        raise Exception(deriv)

        fd = FiniteDifferenceDerivative(
            lambda pt: pts_dihedrals(pt[..., 0, :], pt[..., 1, :], pt[..., 2, :], pt[..., 3, :]),
            function_shape=((None, 4, 3), 0),
            mesh_spacing=1.0e-5
        )
        # dihedDeriv_fd = FiniteDifferenceDerivative(
        #     lambda pts: dihed_deriv(pts, 0, 1, 2, 3, order=1)[1].squeeze().transpose((1, 0, 2)),
        #     function_shape=((None, 4, 3), (None, 4, 3)),
        #     mesh_spacing=1.0e-5
        # )

        fd1 = fd(coords[(0, 1, 2, 3),]).derivative_tensor([1])[0]
        # fd2_22 = dihedDeriv_fd(coords[(4, 5, 6, 7),]).derivative_tensor(1)

        self.assertTrue(np.allclose(deriv.flatten(), fd1.flatten()), msg="{} and {} aren't close".format(
            deriv.flatten(), fd1.flatten()
        ))

    @validationTest
    def test_PtsAngleDeriv(self):
        # need some proper values to test this against...
        np.random.seed(0)
        coords = np.random.rand(16, 3)

        angs, derivs, derivs_2 = angle_deriv(coords, [5, 5], [4, 6], [6, 4], order=2)

        ang = angs[0]; deriv = derivs[:, 0, :]; deriv_2 = derivs_2[:, :, 0, :, :]
        ang2 = vec_angles(coords[4] - coords[5], coords[6] - coords[5])[0]

        self.assertEquals(ang2, ang)

        fd = FiniteDifferenceDerivative(
            lambda pt: vec_angles(pt[..., 1, :] - pt[..., 0, :], pt[..., 2, :] - pt[..., 0, :])[0],
            function_shape=((None, 3), 0),
            mesh_spacing=1.0e-5
        )

        fd1, fd2 = fd(coords[(5, 4, 6),]).derivative_tensor([1, 2])

        self.assertTrue(np.allclose(deriv.flatten(), fd1.flatten()), msg="{} and {} aren't close".format(
            deriv.flatten(), fd1.flatten()
        ))

        d2_flat = np.concatenate(
            [
                np.concatenate([deriv_2[0, 0], deriv_2[0, 1], deriv_2[0, 2]], axis=1),
                np.concatenate([deriv_2[1, 0], deriv_2[1, 1], deriv_2[1, 2]], axis=1),
                np.concatenate([deriv_2[2, 0], deriv_2[2, 1], deriv_2[2, 2]], axis=1)
            ],
            axis=0
        )

        # raise Exception("\n"+"\n".join("{} {}".format(a, b) for a, b in zip(d2_flat, fd2)))

        self.assertTrue(np.allclose(d2_flat.flatten(), fd2.flatten(), atol=1.0e-3), msg="d2: {} and {} differ".format(
            d2_flat.flatten(), fd2.flatten()
        ))

        # raise Exception(fd2.flatten(), deriv_2.flatten())

    @validationTest
    def test_PtsDistDeriv(self):
        # need some proper values to test this against...
        np.random.seed(0)
        coords = np.random.rand(16, 3)

        dists, derivs, derivs_2 = dist_deriv(coords, [5, 4], [4, 5], order=2)

        dist = dists[0]; deriv = derivs[:, 0, :]; deriv_2 = derivs_2[:, :, 0, :, :]
        dists2 = vec_norms(coords[4] - coords[5])

        self.assertEquals(dists2, dist)
        # raise Exception(dist, dists2)

        fd = FiniteDifferenceDerivative(
            lambda pt: vec_norms(pt[..., 1, :] - pt[..., 0, :]),
            function_shape=((None, 3), 0),
            mesh_spacing=1.0e-5
        )

        fd1, fd2 = fd(coords[(5, 4),]).derivative_tensor([1, 2])

        self.assertTrue(np.allclose(deriv.flatten(), fd1.flatten()), msg="{} and {} aren't close".format(
            deriv.flatten(), fd1.flatten()
        ))

        d2_flat = np.concatenate(
            [
                np.concatenate([deriv_2[0, 0], deriv_2[0, 1]], axis=1),
                np.concatenate([deriv_2[1, 0], deriv_2[1, 1]], axis=1)
            ],
            axis=0
        )

        # raise Exception("\n"+"\n".join("{} {}".format(a, b) for a, b in zip(d2_flat, fd2)))

        self.assertTrue(np.allclose(d2_flat.flatten(), fd2.flatten(), atol=1.0e-3), msg="d2: {} and {} differ".format(
            d2_flat.flatten(), fd2.flatten()
        ))

        # raise Exception(fd2.flatten(), deriv_2.flatten())

    @validationTest
    def test_NormDerivs(self):
        np.random.seed(0)
        coords = np.random.rand(16, 3)

        a = coords[(4, 5),] - coords[(5, 4),]
        na, na_da, na_daa = vec_norm_derivs(a, order=2)
        na_2 = vec_norms(a)

        self.assertEquals(tuple(na_2), tuple(na))


        norm_fd = FiniteDifferenceDerivative(
            lambda vecs: vec_norms(vecs),
            function_shape=((None, 2, 3), (None,)),
            mesh_spacing=1.0e-4
        )

        fd_nada, fd_nadaa = norm_fd(a).derivative_tensor([1, 2])

        fd_nada = np.array([fd_nada[:3, 0], fd_nada[3:, 1]])
        fd_nadaa = np.array([fd_nadaa[:3, :3, 0], fd_nadaa[3:, 3:, 1]])

        self.assertTrue(np.allclose(na_da.flatten(), fd_nada.flatten()), msg="norm d1: {} and {} differ".format(
            na_da.flatten(), fd_nada.flatten()
        ))

        self.assertTrue(np.allclose(na_daa.flatten(), fd_nadaa.flatten(), atol=1.0e-4), msg="norm d1: {} and {} differ".format(
            na_daa.flatten(), fd_nadaa.flatten()
        ))

    @validationTest
    def test_SinCosDerivs(self):
        np.random.seed(0)
        coords = np.random.rand(16, 3)

        # sin_derivs_extra, cos_derivs_extra = vec_sin_cos_derivs( # just here to make sure the shape works
        #     coords[(1, 2, 3, 4),] - coords[(0, 1, 2, 3),],
        #     coords[(2, 3, 4, 5),] - coords[(0, 1, 2, 3),],
        #     order=2)

        a = coords[6] - coords[5]
        b = coords[4] - coords[5]

        sin_derivs, cos_derivs = vec_sin_cos_derivs(np.array([a, b]), np.array([b, a]), order=2)

        cos_fd = FiniteDifferenceDerivative(
            lambda vecs: vec_cos(vecs[..., 0, :], vecs[..., 1, :]),
            function_shape=((None, 2, 3), 0),
            mesh_spacing=1.0e-7
        )
        cosDeriv_fd = FiniteDifferenceDerivative(
            lambda vecs: vec_sin_cos_derivs(vecs[..., 0, :], vecs[..., 1, :], order=1)[1][1].squeeze(),
            function_shape=((None, 2, 3), (None, 2, 3)),
            mesh_spacing=1.0e-7
        )
        cos_fd22_1, = cosDeriv_fd(np.array([a, b])).derivative_tensor([1])
        cos_fd22_2, = cosDeriv_fd(np.array([b, a])).derivative_tensor([1])
        cos_fd22 = np.array([cos_fd22_1, cos_fd22_2])

        cos_fd1_1, cos_fd2_1 = cos_fd(np.array([a, b])).derivative_tensor([1, 2])
        cos_fd1_2, cos_fd2_2 = cos_fd(np.array([b, a])).derivative_tensor([1, 2])
        cos_fd1 = np.array([cos_fd1_1, cos_fd1_2])
        cos_fd2 = np.array([cos_fd2_1, cos_fd2_2])

        sin_fd = FiniteDifferenceDerivative(
            lambda vecs: vec_sins(vecs[..., 0, :], vecs[..., 1, :]),
            function_shape=((None, 2, 3), 0),
            mesh_spacing=1.0e-7
        )
        sinDeriv_fd = FiniteDifferenceDerivative(
            lambda vecs: vec_sin_cos_derivs(vecs[..., 0, :], vecs[..., 1, :], order=1)[0][1].squeeze(),
            function_shape=((None, 2, 3), (None, 2, 3)),
            mesh_spacing=1.0e-7
        )
        sin_fd22_1, = sinDeriv_fd(np.array([a, b])).derivative_tensor([1])
        sin_fd22_2, = sinDeriv_fd(np.array([b, a])).derivative_tensor([1])
        sin_fd22 = np.array([sin_fd22_1, sin_fd22_2])
        sin_fd1_1, sin_fd2_1 = sin_fd(np.array([a, b])).derivative_tensor([1, 2])
        sin_fd1_2, sin_fd2_2 = sin_fd(np.array([b, a])).derivative_tensor([1, 2])
        sin_fd1 = np.array([sin_fd1_1, sin_fd1_2])
        sin_fd2 = np.array([sin_fd2_1, sin_fd2_2])

        s, s1, s2 = sin_derivs
        c, c1, c2 = cos_derivs

        # raise Exception(sin_fd1, s1)

        self.assertTrue(np.allclose(s1.flatten(), sin_fd1.flatten()), msg="sin d1: {} and {} differ".format(
            s1.flatten(), sin_fd1.flatten()
        ))

        self.assertTrue(np.allclose(c1.flatten(), cos_fd1.flatten()), msg="cos d1: {} and {} differ".format(
            c1.flatten(), cos_fd1.flatten()
        ))

        # raise Exception("\n", c2[0, 0], "\n", cos_fd2[:3, :3])
        # raise Exception("\n"+"\n".join("{} {}".format(a, b) for a, b in zip(c2[0, 0], cos_fd2[:3, :3])))
        c2_flat = np.concatenate(
            [
                np.concatenate([c2[:, 0, 0], c2[:, 0, 1]], axis=2),
                np.concatenate([c2[:, 1, 0], c2[:, 1, 1]], axis=2)
            ],
            axis=1
        )

        s2_flat = np.concatenate(
            [
                np.concatenate([s2[:, 0, 0], s2[:, 0, 1]], axis=2),
                np.concatenate([s2[:, 1, 0], s2[:, 1, 1]], axis=2)
            ],
            axis=1
        )

        self.assertTrue(np.allclose(s2_flat.flatten(), sin_fd22.flatten()), msg="sin d2: {} and {} differ".format(
            s2_flat.flatten(), sin_fd22.flatten()
        ))
        self.assertTrue(np.allclose(c2_flat.flatten(), cos_fd22.flatten()), msg="cos d2: {} and {} differ".format(
            c2_flat.flatten(), cos_fd22.flatten()
        ))

    @validationTest
    def test_AngleDerivs(self):
        np.random.seed(0)
        coords = np.random.rand(16, 3)

        a = coords[4] - coords[5]
        b = coords[6] - coords[5]
        ang, dang, ddang = vec_angle_derivs(np.array([a, b]),
                                            np.array([b, a]), order=2)
        ang_2 = vec_angles(a, b)[0]

        self.assertEquals(ang_2, ang.flatten()[0])

        ang_fd = FiniteDifferenceDerivative(
            lambda vecs: vec_angles(vecs[..., 0, :], vecs[..., 1, :])[0],
            function_shape=((None, 2, 3), 0),
            mesh_spacing=1.0e-4
        )

        fd_ang_1, fd_dang_1 = ang_fd([a, b]).derivative_tensor([1, 2])
        fd_ang_2, fd_dang_2 = ang_fd([b, a]).derivative_tensor([1, 2])

        fd_ang = np.array([fd_ang_1, fd_ang_2])
        fd_dang = np.array([fd_dang_1, fd_dang_2])

        self.assertTrue(np.allclose(dang.flatten(), fd_ang.flatten()), msg="ang d1: {} and {} differ".format(
            fd_ang.flatten(), fd_ang.flatten()
        ))

        d2_flat = np.concatenate(
            [
                np.concatenate([ddang[:, 0, 0], ddang[:, 0, 1]], axis=2),
                np.concatenate([ddang[:, 1, 0], ddang[:, 1, 1]], axis=2)
            ],
            axis=1
        )

        # raise Exception("\n"+"\n".join("{} {}".format(a, b) for a, b in zip(d2_flat[0], fd_dang[0])))
        self.assertTrue(np.allclose(d2_flat.flatten(), fd_dang.flatten(), atol=1.0e-2), msg="ang d2: {} and {} differ ({})".format(
            d2_flat.flatten(), fd_dang.flatten(), d2_flat.flatten() - fd_dang.flatten()
        ))

    @inactiveTest
    def test_AngleDerivScan(self):
        np.random.seed(0)
        # a = np.random.rand(3) * 2 # make it longer to avoid stability issues
        a = np.array([1, 0, 0])

        fd = FiniteDifferenceDerivative(
                lambda vecs: vec_angle_derivs(vecs[..., 0, :], vecs[..., 1, :], up_vectors=up)[1],
                function_shape=((None, 2, 3), 0),
                mesh_spacing=1.0e-4
            )

        data = {"rotations":[], 'real_angles':[], "angles":[], 'derivs':[], 'derivs2':[], 'derivs_num2':[]}
        for q in np.linspace(-np.pi, np.pi, 601):
            up = np.array([0, 0, 1])
            r = rotation_matrix(up, q)
            b = np.dot(r, a)
            ang, deriv, deriv_2 = vec_angle_derivs(a, b, up_vectors=up, order=2)
            data['rotations'].append(q)
            data['real_angles'].append(vec_angles(a, b, up_vectors=up)[0])
            data['angles'].append(ang.tolist())
            data['derivs'].append(deriv.tolist())
            data['derivs2'].append(deriv_2.tolist())

            data['derivs_num2'].append(fd(np.array([a, b])).derivative_tensor(1).tolist())

        # import json
        # with open(dump_file, 'w+') as f:
        #     json.dump(data, f)

    @validationTest
    def test_SetOps(self):

        unums, sorting = unique([1, 2, 3, 4, 5])
        self.assertEquals(unums.tolist(), [1, 2, 3, 4, 5])
        self.assertEquals(sorting.tolist(), [0, 1, 2, 3, 4])

        unums, sorting = unique([1, 1, 3, 4, 5])
        self.assertEquals(unums.tolist(), [1, 3, 4, 5])
        self.assertEquals(sorting.tolist(), [0, 1, 2, 3, 4])

        unums, sorting = unique([1, 3, 1, 1, 1])
        self.assertEquals(unums.tolist(), [1, 3])
        self.assertEquals(sorting.tolist(), [0, 2, 3, 4, 1])

        unums, sorting = unique([[1, 3], [1, 1], [1, 3]])
        self.assertEquals(unums.tolist(), [[1, 1], [1, 3]])
        self.assertEquals(sorting.tolist(), [1, 0, 2])

        inters, sortings, merge = intersection(
            [1, 1, 3, 2, 5],
            [0, 0, 0, 5, 1]
        )
        self.assertEquals(inters.tolist(), [1, 5])
        self.assertEquals(sortings[0].tolist(), [0, 1, 3, 2, 4])
        self.assertEquals(sortings[1].tolist(), [0, 1, 2, 4, 3])

        inters, sortings, merge = intersection(
            [
                [1, 3], [1, 1]
            ],
            [
                [1, 3], [0, 0]
            ]
        )
        self.assertEquals(inters.tolist(), [[1, 3]])
        self.assertEquals(sortings[0].tolist(), [1, 0])
        self.assertEquals(sortings[1].tolist(), [1, 0])

        diffs, sortings, merge = difference(
            [1, 1, 3, 2, 5],
            [0, 0, 0, 5, 1]
        )
        self.assertEquals(diffs.tolist(), [2, 3])
        self.assertEquals(sortings[0].tolist(), [0, 1, 3, 2, 4])
        self.assertEquals(sortings[1].tolist(), [0, 1, 2, 4, 3])

        diffs, sortings, merge = contained(
            [1, 1, 3, 2, 5],
            [0, 0, 0, 5, 1]
        )
        self.assertEquals(diffs.tolist(), [True, True, False, False, True])

        ugh = np.arange(1000)
        bleh = np.random.choice(1000, size=100)
        diffs, sortings, merge = contained(
            bleh,
            ugh
        )
        self.assertEquals(diffs.tolist(), np.isin(bleh, ugh).tolist())

        diffs2, sortings, merge = contained(
            bleh,
            ugh,
            method='find'
        )

        self.assertEquals(diffs.tolist(), diffs2.tolist())

    @validationTest
    def test_SparseArray(self):
        array = SparseArray([
            [
                [1, 0, 0],
                [0, 0, 1],
                [0, 1, 0]
            ],
            [
                [0, 0, 1],
                [0, 1, 0],
                [1, 0, 0]
            ],
            [
                [0, 1, 0],
                [1, 0, 1],
                [0, 0, 1]
            ],
            [
                [1, 1, 0],
                [1, 0, 1],
                [0, 1, 1]
            ]
        ])

        self.assertEquals(array.shape, (4, 3, 3))
        tp = array.transpose((1, 0, 2))
        self.assertEquals(tp.shape, (3, 4, 3))
        self.assertLess(np.linalg.norm((tp.asarray()-array.asarray().transpose((1, 0, 2))).flatten()), 1e-8)
        self.assertEquals(array[2, :, 2].shape, (3,))
        td = array.tensordot(array, axes=[1, 1])
        self.assertEquals(td.shape, (4, 3, 4, 3))
        self.assertEquals(array.tensordot(array, axes=[[1, 2], [1, 2]]).shape, (4, 4))

    @validationTest
    def test_Sparse(self):

        shape = (1000, 100, 50)

        n_els = 100
        np.random.seed(1)
        inds = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals = np.random.rand(len(inds))
        inds = inds.T

        # `from_data` for backend flexibility
        array = SparseArray.from_data(
            (
                vals,
                inds
            ),
            shape=shape
        )


        self.assertEquals(array.shape, shape)
        block_vals, block_inds = array.block_data
        self.assertEquals(len(block_vals), len(vals))
        self.assertEquals(np.sort(block_vals).tolist(), np.sort(vals).tolist())
        for i in range(len(shape)):
            self.assertEquals(np.sort(block_inds[i]).tolist(), np.sort(inds[i]).tolist())

        woof = array[:, 1, 1] #type: SparseArray
        self.assertIs(type(woof), type(array))
        self.assertEquals(woof.shape, (shape[0],))
        block_vals, block_inds = woof.block_data
        filt_pos = np.where(np.logical_and(inds[1] == 1, inds[2] == 1))
        if len(filt_pos) > 0:
            self.assertEquals(
                np.sort(block_vals).tolist(),
                np.sort(vals[filt_pos]).tolist()
            )

        # with BlockProfiler('Sparse sampling', print_res=True):
        #     new_woof = array[:, 1, 1]  # type: SparseArray

        shape = (28, 3003)

        n_els = 10000
        np.random.seed(1)
        inds = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals = np.random.rand(len(inds))
        inds = inds.T

        # `from_data` for backend flexibility
        array = SparseArray.from_data(
            (
                vals,
                inds
            ),
            shape=shape
        )

        woof = array[0, :]  # type: SparseArray
        self.assertIs(type(woof), type(array))
        self.assertEquals(woof.shape, (shape[1],))
        block_vals, block_inds = woof.block_data
        filt_pos = np.where(inds[0] == 0)
        if len(filt_pos) > 0:
            self.assertEquals(
                np.sort(block_vals).tolist(),
                np.sort(vals[filt_pos]).tolist()
            )

        woof = array[(0, 2), :]  # type: SparseArray
        self.assertEquals(woof.shape, (2, shape[1]))
        block_vals, block_inds = woof.block_data
        filt_pos = np.where(np.logical_or(inds[0] == 0, inds[0] == 2))
        if len(filt_pos) > 0:
            self.assertEquals(
                np.sort(block_vals).tolist(),
                np.sort(vals[filt_pos]).tolist()
            )

            self.assertEquals(
                block_vals[:10].tolist(),
                [0.26762682146970584, 0.3742446513095977, 0.11369722324344822, 0.4860704109280778,
                 0.09299008335958303, 0.11229999691948178, 0.0005348158154161453, 0.7711636892670307, 0.6573053253883241, 0.39084691369185387]

            )

        n_els = 1000
        inds_2 = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals_2 = np.random.rand(len(inds_2))
        inds_2 = inds_2.T

        # `from_data` for backend flexibility
        array_2 = SparseArray.from_data(
            (
                vals_2,
                inds_2
            ),
            shape=shape
        )

        meh = array.dot(array_2.transpose((1, 0)))
        self.assertTrue(
            np.allclose(
                meh.asarray(),
                np.dot(
                    array.asarray(),
                    array_2.asarray().T
                ),
                3
            )
        )

        n_els = 1000
        inds_3 = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals_3 = np.random.rand(len(inds_3))
        inds_3 = inds_3.T

        # `from_data` for backend flexibility
        array_3 = SparseArray.from_data(
            (
                vals_3,
                inds_3
            ),
            shape=shape
        )

        new2 = array_2.concatenate(array_3)
        meh = np.concatenate([array_2.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )



        new2 = array_2.concatenate(array_3, array_2)
        meh = np.concatenate([array_2.asarray(), array_3.asarray(), array_2.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat many failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        new3 = array_2.concatenate(array_2, array_3, axis=1)
        meh = np.concatenate([array_2.asarray(), array_2.asarray(), array_3.asarray()], axis=1)
        self.assertEquals(new3.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new3.asarray(),
                meh
            ),
            msg="concat along 1 failed: (ref) {} vs {}".format(
                meh,
                new3.asarray()
            )
        )

        new_shape = [1, shape[1]]

        n_els = 1000
        inds_3 = np.unique(np.array([np.random.choice(x, n_els) for x in new_shape]).T, axis=0)
        vals_3 = np.random.rand(len(inds_3))
        inds_3 = inds_3.T

        # `from_data` for backend flexibility
        array_3 = SparseArray.from_data(
            (
                vals_3,
                inds_3
            ),
            shape=new_shape
        )

        new2 = array_3.concatenate(array_2)
        meh = np.concatenate([array_3.asarray(), array_2.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        new2 = array_2.concatenate(array_3)
        meh = np.concatenate([array_2.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        new2 = array_2.concatenate(array_3, array_2)
        meh = np.concatenate([array_2.asarray(), array_3.asarray(), array_2.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat many failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        # new3 = array_2.concatenate(array_2, array_3, axis=1)
        # meh = np.concatenate([array_2.asarray(), array_2.asarray(), array_3.asarray()], axis=1)
        # self.assertEquals(new3.shape, meh.shape)
        # self.assertTrue(
        #     np.allclose(
        #         new3.asarray(),
        #         meh
        #     ),
        #     msg="concat along 1 failed: (ref) {} vs {}".format(
        #         meh,
        #         new3.asarray()
        #     )
        # )

        array_3 = array_3[:, :2500].reshape((1, 2500))

        array_3 = array_3.reshape((
                array_3.shape[1] // 2,
                2
        ))

        new2 = array_3.concatenate(array_3)
        meh = np.concatenate([array_3.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        new2 = array_3.concatenate(array_3, axis=1)
        meh = np.concatenate([array_3.asarray(), array_3.asarray()], axis=1)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        new_shape = [shape[1]]

        n_els = 1000
        inds_3 = np.unique(np.array([np.random.choice(x, n_els) for x in new_shape]).T, axis=0)
        vals_3 = np.random.rand(len(inds_3))
        inds_3 = inds_3.T

        array_3 = SparseArray.from_data(
            (
                vals_3,
                inds_3
            ),
            shape=new_shape
        )

        new2 = array_3.concatenate(array_3)
        meh = np.concatenate([array_3.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        wtf_array1 = SparseArray.from_data(
            (
                [-0.00045906, -0.00045906, -0.00045906, -0.00045906, -0.00045906,
                 -0.00045906],
                (
                    (0, 24, 51, 78, 109, 140),
                )
            ),
            shape = (155,)

        )

        wtf_array2 = SparseArray.from_data(
            (
                [-0.00045906, -0.00045906, -0.00045906, -0.00045906],
                ([ 16,  53,  88, 123],)
            ),
            shape=(155,)
        )

        new2 = wtf_array1.concatenate(wtf_array2)
        meh = np.concatenate([
            wtf_array1.asarray(),
            wtf_array2.asarray()
        ])

        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

    @validationTest
    def test_SparseConstructor(self):

        shape = (1000, 100, 50)

        n_els = 100
        np.random.seed(1)
        inds = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals = np.random.rand(len(inds))
        inds = inds.T

        # `from_data` for backend flexibility
        array = SparseArray.from_data(
            (
                vals,
                inds
            ),
            shape=shape
        )

        self.assertEquals(array.shape, shape)
        block_vals, block_inds = array.block_data
        self.assertEquals(len(block_vals), len(vals))
        self.assertEquals(np.sort(block_vals).tolist(), np.sort(vals).tolist())
        for i in range(len(shape)):
            self.assertEquals(np.sort(block_inds[i]).tolist(), np.sort(inds[i]).tolist())

        woof = array[:, 1, 1]  # type: SparseArray
        self.assertIs(type(woof), type(array))
        self.assertEquals(woof.shape, (shape[0],))
        block_vals, block_inds = woof.block_data
        filt_pos = np.where(np.logical_and(inds[1] == 1, inds[2] == 1))
        if len(filt_pos) > 0:
            self.assertEquals(
                np.sort(block_vals).tolist(),
                np.sort(vals[filt_pos]).tolist()
            )

        # with BlockProfiler('Sparse sampling', print_res=True):
        #     new_woof = array[:, 1, 1]  # type: SparseArray

        shape = (28, 3003)

        n_els = 10000
        np.random.seed(1)
        inds = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals = np.random.rand(len(inds))
        inds = inds.T

        # `from_data` for backend flexibility
        array = SparseArray.from_data(
            (
                vals,
                inds
            ),
            shape=shape
        )

        woof = array[0, :]  # type: SparseArray
        self.assertIs(type(woof), type(array))
        self.assertEquals(woof.shape, (shape[1],))
        block_vals, block_inds = woof.block_data
        filt_pos = np.where(inds[0] == 0)
        if len(filt_pos) > 0:
            self.assertEquals(
                np.sort(block_vals).tolist(),
                np.sort(vals[filt_pos]).tolist()
            )

        woof = array[(0, 2), :]  # type: SparseArray
        self.assertEquals(woof.shape, (2, shape[1]))
        block_vals, block_inds = woof.block_data
        filt_pos = np.where(np.logical_or(inds[0] == 0, inds[0] == 2))
        if len(filt_pos) > 0:
            self.assertEquals(
                np.sort(block_vals).tolist(),
                np.sort(vals[filt_pos]).tolist()
            )

            self.assertEquals(
                block_vals[:10].tolist(),
                [0.26762682146970584, 0.3742446513095977, 0.11369722324344822, 0.4860704109280778,
                 0.09299008335958303, 0.11229999691948178, 0.0005348158154161453, 0.7711636892670307,
                 0.6573053253883241, 0.39084691369185387]

            )

        n_els = 1000
        inds_2 = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals_2 = np.random.rand(len(inds_2))
        inds_2 = inds_2.T

        # `from_data` for backend flexibility
        array_2 = SparseArray.from_data(
            (
                vals_2,
                inds_2
            ),
            shape=shape
        )

        meh = array.dot(array_2.transpose((1, 0)))
        self.assertTrue(
            np.allclose(
                meh.asarray(),
                np.dot(
                    array.asarray(),
                    array_2.asarray().T
                ),
                3
            )
        )

        n_els = 1000
        inds_3 = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals_3 = np.random.rand(len(inds_3))
        inds_3 = inds_3.T

        # `from_data` for backend flexibility
        array_3 = SparseArray.from_data(
            (
                vals_3,
                inds_3
            ),
            shape=shape
        )

        new2 = array_2.concatenate(array_3)
        meh = np.concatenate([array_2.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        new2 = array_2.concatenate(array_3, array_2)
        meh = np.concatenate([array_2.asarray(), array_3.asarray(), array_2.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat many failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        new3 = array_2.concatenate(array_2, array_3, axis=1)
        meh = np.concatenate([array_2.asarray(), array_2.asarray(), array_3.asarray()], axis=1)
        self.assertEquals(new3.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new3.asarray(),
                meh
            ),
            msg="concat along 1 failed: (ref) {} vs {}".format(
                meh,
                new3.asarray()
            )
        )

        new_shape = [1, shape[1]]

        n_els = 1000
        inds_3 = np.unique(np.array([np.random.choice(x, n_els) for x in new_shape]).T, axis=0)
        vals_3 = np.random.rand(len(inds_3))
        inds_3 = inds_3.T

        # `from_data` for backend flexibility
        array_3 = SparseArray.from_data(
            (
                vals_3,
                inds_3
            ),
            shape=new_shape
        )

        new2 = array_3.concatenate(array_2)
        meh = np.concatenate([array_3.asarray(), array_2.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        new2 = array_2.concatenate(array_3)
        meh = np.concatenate([array_2.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        new2 = array_2.concatenate(array_3, array_2)
        meh = np.concatenate([array_2.asarray(), array_3.asarray(), array_2.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat many failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        # new3 = array_2.concatenate(array_2, array_3, axis=1)
        # meh = np.concatenate([array_2.asarray(), array_2.asarray(), array_3.asarray()], axis=1)
        # self.assertEquals(new3.shape, meh.shape)
        # self.assertTrue(
        #     np.allclose(
        #         new3.asarray(),
        #         meh
        #     ),
        #     msg="concat along 1 failed: (ref) {} vs {}".format(
        #         meh,
        #         new3.asarray()
        #     )
        # )

        array_3 = array_3[:, :2500].reshape((1, 2500))

        array_3 = array_3.reshape((
            array_3.shape[1] // 2,
            2
        ))

        new2 = array_3.concatenate(array_3)
        meh = np.concatenate([array_3.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        new2 = array_3.concatenate(array_3, axis=1)
        meh = np.concatenate([array_3.asarray(), array_3.asarray()], axis=1)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        new_shape = [shape[1]]

        n_els = 1000
        inds_3 = np.unique(np.array([np.random.choice(x, n_els) for x in new_shape]).T, axis=0)
        vals_3 = np.random.rand(len(inds_3))
        inds_3 = inds_3.T

        array_3 = SparseArray.from_data(
            (
                vals_3,
                inds_3
            ),
            shape=new_shape
        )

        new2 = array_3.concatenate(array_3)
        meh = np.concatenate([array_3.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

        wtf_array1 = SparseArray.from_data(
            (
                [-0.00045906, -0.00045906, -0.00045906, -0.00045906, -0.00045906,
                 -0.00045906],
                (
                    (0, 24, 51, 78, 109, 140),
                )
            ),
            shape=(155,)

        )

        wtf_array2 = SparseArray.from_data(
            (
                [-0.00045906, -0.00045906, -0.00045906, -0.00045906],
                ([16, 53, 88, 123],)
            ),
            shape=(155,)
        )

        new2 = wtf_array1.concatenate(wtf_array2)
        meh = np.concatenate([
            wtf_array1.asarray(),
            wtf_array2.asarray()
        ])

        self.assertTrue(
            np.allclose(
                new2.asarray(),
                meh
            ),
            msg="concat failed: (ref) {} vs {}".format(
                meh,
                new2.asarray()
            )
        )

    @validationTest
    def test_SparseBroadcast(self):

        shape = (10, 100, 50)

        n_els = 8
        np.random.seed(1)
        inds = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals = np.random.rand(len(inds))
        inds = inds.T

        # `from_data` for backend flexibility
        array = SparseArray.from_data(
            (
                vals,
                inds
            ),
            shape=shape
        )

        darr = array.asarray()

        exp_a = array.expand_dims([1, 2])
        self.assertTrue(
            np.allclose(
                exp_a.asarray(),
                np.expand_dims(darr, [1, 2])
            )
        )

        parr = array.pad_right((0, 3, 0))
        self.assertTrue(
            np.allclose(
                parr.block_data[0],
                array.block_data[0]
            )
        )
        self.assertTrue(
            np.allclose(parr.block_data[1], array.block_data[1]),
            msg='inds broken'
        )
        self.assertTrue(
            np.allclose(parr.asarray(), np.pad(darr, [[0, 0], [0, 3], [0, 0]])),
            msg='padding broken'
        )

        exp_a = array.expand_and_pad([1, 2], [0, 4, 4, 0, 0])
        self.assertTrue(
            np.allclose(
                exp_a.asarray(),
                np.pad(
                    np.expand_dims(darr, [1, 2]),
                    [[0, 0], [0, 4], [0, 4], [0, 0], [0, 0]]
                )
            )
        )

        for j in range(3):

                dense = np.broadcast_to(np.expand_dims(darr, j), shape[:j] + (100,) + shape[j:])
                sparse = array.reshape(shape[:j] + (1,) + shape[j:]).broadcast_to(shape[:j] + (100,) + shape[j:])

                self.assertTrue(np.allclose(dense, sparse.asarray()))

    @validationTest
    def test_VecOuter(self):

        a = np.random.rand(5, 10, 2, 3)
        b = np.random.rand(5, 10, 4, 2, 3)

        self.assertTrue(
            np.allclose(
                vec_outer(a, b, axes=[[], [2]]),
                a[:, :, np.newaxis, :, :] * b
            )
        )


        a = np.random.rand(5, 10, 9, 7)
        b = np.random.rand(5, 10, 4, 2, 3)


        # self.assertTrue(
        #     np.allclose(
        #         new_vec_outer(a, b, axes=[[2, 3], [2, 3, 4]]),
        #         vec_outer(a, b, axes=[[2, 3], [2, 3, 4]])
        #     )
        # )

    @validationTest
    def test_VecDiag(self):

        ugh = np.random.rand(3, 7, 5)
        diag_vec = vec_tensordiag(ugh, extra_dims=2, axis=-1)
        self.assertEquals(diag_vec.shape, (3, 7, 5, 5, 5))
        self.assertEquals(
            diag_vec[0, 2, 1, 1, 1],
            ugh[0, 2, 1]
        )
        diag_mats = vec_tensordiag(ugh, extra_dims=2, axis=1)
        self.assertEquals(diag_mats.shape, (3, 7, 7, 7, 5))
        self.assertTrue(np.allclose(
            diag_mats[0, 1, 1, 1],
            ugh[0, 1]
        ))

    @inactiveTest
    def test_MatrixProductDeriv(self):

        # x_grid = np.linspace(-np.pi, np.pi)
        # y_grid = np.linspace(-np.pi, np.pi)
        x = np.pi / 6
        y = np.pi / 3
        import sympy
        x, y = sympy.symbols('x y')

        sx = sympy.sin(x); cx = sympy.cos(x)
        sy = sympy.sin(y); cy = sympy.cos(y)

        A = sympy.Array([
            [sx * sy, sx * cy],
            [cx * sy, cx * cy],
        ])

        B = sympy.Array([x**3, y**3])

        AB = sympy.tensorproduct(A * B)
        raise Exception(AB)


        A_mat = np.array([
            [ np.cos(x) * np.cos(y), np.cos(y) * np.sin(np.pi / 3)],
            [-np.cos(x) * np.sin(y), np.sin(x) * np.sin(np.pi / 3)],
        ])
        sinx_cosx_expansion = ...
        a = np.random.rand(5, 10, 2, 3)
        b = np.random.rand(5, 10, 4, 2, 3)

        self.assertTrue(
            np.allclose(
                new_vec_outer(a, b, axes=[[], [2]]),
                a[:, :, np.newaxis, :, :] * b
            )
        )

        a = np.random.rand(5, 10, 9, 7)
        b = np.random.rand(5, 10, 4, 2, 3)

        self.assertTrue(
            np.allclose(
                new_vec_outer(a, b, axes=[[2, 3], [2, 3, 4]]),
                vec_outer(a, b, axes=[[2, 3], [2, 3, 4]])
            )
        )

    @validationTest
    def test_DihedralDerivativeComparison(self):
        import Psience as psi
        test_root = os.path.join(os.path.dirname(psi.__file__), "ci", "tests", "TestData")
        from Psience.Molecools import Molecule

        mol = Molecule.from_file(
            os.path.join(test_root, "HOONO_freq.fchk")
        )

        # mol = Molecule.from_file(
        #     os.path.join(test_root, "nh3.fchk")
        # )
        #
        # coords = Molecule.from_file(
        #     os.path.join(test_root, "water_freq.fchk")
        # ).coords
        #
        # coords = Molecule.from_file(
        #     os.path.join(test_root, "tbhp_180.fchk")
        # ).coords

        """
        ==> [[[ 0.77190252  0.         -0.0719183  ...  0.          0.
    0.04552509]
  [-0.16557176  0.         -0.38929849 ...  0.          0.
   -0.01881451]
  [ 0.61380168  0.         -0.01456972 ...  0.          0.
    0.08105092]
  ...
  [ 0.          0.          0.         ... -0.55669355  0.40498602
    0.00877491]
  [ 0.          0.          0.         ... -0.7321073  -0.24340891
    0.26671989]
  [ 0.          0.          0.         ... -0.39257    -0.12036494
   -0.50985179]]]"""

        coords = mol.coords

        # from McUtils.McUtils.Numputils.CoordOps import prep_disp_expansion

        # A_expansion = prep_disp_expansion(coords, 1, 0)
        # B_expansion = prep_disp_expansion(coords, 2, 0)
        # _, na_da, na_daa = vec_norm_derivs(A_expansion[0], order=2)
        # norms, units = vec_norm_unit_deriv(A_expansion, 2)
        # woof = tensor_reexpand(A_expansion[1:], [na_da, na_daa], 2)
        # raise Exception(units[1])
        # raise Exception(
        #     np.round(woof[1] - norms[2], 16)
        # )
        # new_d2 = 1/norms[0] * np.tensordot(A_expansion[1],
        #                                    np.eye(3) - units[0][np.newaxis, :] * units[0][:, np.newaxis],
        #                                    axes=[-1, -1]
        #                                    )
        # new_d3 = 1/norms[0] * np.tensordot(A_expansion[1],
        #                                    np.tensordot(A_expansion[1],
        #                                                 np.eye(3) - units[0][np.newaxis, :] * units[0][:, np.newaxis],
        #                                                 axes=[-1, -1]
        #                                                 ),
        #                                    axes=[-1, -1]
        #                                    )
        # print(norms[2] / 2 - new_d3)
        # # print(new_d3)
        # raise Exception(...)
        # raise Exception(
        #     units[2],
        #     new_d2
        # )
        # a = A_expansion[0]
        # b = B_expansion[0]
        # sin_derivs, cos_derivs = vec_sin_cos_derivs(a, b, order=2)
        # cos_expansion = sum(
        #     np.tensordot(e2, np.tensordot(e1, d, axes=[-1, -1]), axes=[-1, -1])
        #     for e1, e2, d in [
        #         [A_expansion[1], A_expansion[1], cos_derivs[2][0, 0]],
        #         [B_expansion[1], A_expansion[1], cos_derivs[2][0, 1]],
        #         [A_expansion[1], B_expansion[1], cos_derivs[2][1, 0]],
        #         [B_expansion[1], B_expansion[1], cos_derivs[2][1, 1]],
        #     ]
        #     )
        # sin_expansion = sum(
        #     np.tensordot(e2, np.tensordot(e1, d, axes=[-1, -1]), axes=[-1, -1])
        #     for e1, e2, d in [
        #         [A_expansion[1], A_expansion[1], sin_derivs[2][0, 0]],
        #         [B_expansion[1], A_expansion[1], sin_derivs[2][0, 1]],
        #         [A_expansion[1], B_expansion[1], sin_derivs[2][1, 0]],
        #         [B_expansion[1], B_expansion[1], sin_derivs[2][1, 1]],
        #     ]
        # )
        # with np.printoptions(linewidth=1e8):
        #     print()
        #     print(sin_expansion)
        #     print("-"*20)
        #     woof = angle_vec(coords, 0, 1, 2, order=2)
        # raise Exception(...)
        #
        # # raise Exception([c.shape for c in cos_derivs])
        # print(sin_derivs[2])
        # woof = angle_vec(coords, 0, 1, 2, order=2)
        # print(woof[2].reshape(4, 3, 4, 3))
        # raise Exception(...)
        # sin_expansion = tensor_reexpand(
        #     [
        #         [a, ]
        #     ],
        #     [sin_derivs[1][0], sin_derivs[2][0, 0]]
        # )
        # raise Exception(
        #     sin_derivs[2][0]
        # )

        import McUtils.McUtils.Numputils.CoordOps as coops
        import itertools
        # for c in itertools.combinations(range(coords.shape[0]), 3):
        #     for p in itertools.permutations(c):
        #         coops.fast_proj = True
        #         new = angle_vec(coords, *p, order=2)
        #         coops.fast_proj = False
        #         old = angle_vec(coords, *p, order=2)#, method='classic')
        #         if not np.allclose(new[1], old[1]):
        #             raise ValueError(
        #                 p, new[1], old[1]
        #             )
        # for c in itertools.combinations(range(coords.shape[0]), 2):
        #     for p in itertools.permutations(c):
        #         coops.fast_proj = True
        #         new = dist_vec(coords, *p, order=2)
        #         coops.fast_proj = False
        #         old = dist_vec(coords, *p, order=2)#, method='classic')
        #         if not np.allclose(new[1], old[1]):
        #             raise ValueError(
        #                 p, new[1], old[1]
        #             )

        for c in itertools.combinations(range(coords.shape[0]), 4):
            for p in itertools.permutations(c):
                coops.fast_proj = True
                new = dihed_vec(coords, *p, order=2)
                coops.fast_proj = False
                old = dihed_vec(coords, *p, order=2)#, method='classic')
                if not np.allclose(new[1], old[1]):
                    print(coords)
                    raise ValueError(
                        p, new[1], old[1]
                    )
        return
        # new = dist_vec(coords, 3, 1, order=2)
        # # coops.fast_proj = False
        # old = dist_vec(coords, 3, 1, order=2, method='classic')
        coops.fast_proj = True
        new = dihed_vec(coords, 3, 0, 2, 1, order=2)
        coops.fast_proj = False
        old = dihed_vec(coords, 3, 0, 2, 1, order=2)
        with np.printoptions(linewidth=1e8):
            print("="*10)
            print(new[0])
            print(old[0])

            print("="*10)
            print(new[1])
            print(old[1])

            # print("-"*10)
            # print(np.round(new[2] - np.moveaxis(new[2], 0, 1), 8))
            # print(old[2] - np.moveaxis(old[2], 0, 1))

            print("-"*10)
            print(new[2] - old[2])
        return
        #
        # n = 4
        # print(angle_vec(coords, 0, 1, 2, order=2)[2][:, n])
        # print(angle_vec(coords, 0, 1, 2, order=2, method='classic')[2][:, n])
        # raise Exception(...)

        inv_coords = inverse_coordinate_solve(
                [
                    (0, 1),
                    (0, 2),
                    (0, 3),
                    (0, 1, 2),
                    (0, 1, 3),
                    (0, 2, 3)
                ],
                [
                    1.9126349402213, 1.9126349325765, 1.9126349325765,
                    1.8634707086348 + .2, 1.8634707086348, 1.8634707045268
                ],
                coords,
                remove_translation_rotation=False
            )

        spec = [
                    (0, 1),
                    (0, 2),
                    (0, 3),
                    (0, 1, 2),
                    (0, 1, 3),
                    (0, 2, 3)
                ]
        fwd = internal_coordinate_tensors(
                coords,
                spec,
                order=2
            )
        (rev, _), _ = inverse_coordinate_solve(
            spec,
            fwd[0],
            coords,
            order=2
        )
        raise Exception(
            # [s.shape for s in fwd[1:]],
            # [s.shape for s in rev[1:]]
            rev[0],
            coords
        )

        coords = Molecule.from_file(
            os.path.expanduser("~/Documents/UW/Research/Development/Psience/ci/tests/TestData/HOH_freq.fchk")
        ).coords

        # np.random.seed(0)
        # coords = np.random.rand(4, 3)
        # coords = self.problem_coords
        raise Exception(
            "?",
            # coords[:3],
            wag_vec(coords, 2, 0, 1, order=1)[-1].reshape(-1, 3)[:4],
            # book_vec(coords, 0, 1, 2, 3, method='og').reshape(-1, 3)[:4]
            # dihed_vec(coords, 0, 1, 2, 3, method='og').reshape(-1, 3)[:4]
        )
        raise Exception(
            # coords[:3],
            # angle_vec(coords, 0, 1, 2, method='expansion', order=1),
            # angle_vec(coords, 0, 1, 2, method='expansion', fixed_atoms=[0], order=1)
            # angle_vec(coords, 0, 1, 2).reshape(-1, 3)[:3],
            # # angle_vec(coords, 0, 1, 2, method='og'),
            # rock_vec(coords, 0, 1, 2).reshape(-1, 3)[:3],
            int_coord_tensors(
                coords,
                [
                    (0, 1, 2),
                    {'rock': (0, 1, 2)},
                    {'rock': (0, 1, 2), 'fixed_atoms':[0]},
                ]
            )
        )
        """
        (array([ 9.29682337e-01,  3.68362256e-01,  7.97024412e-17, -9.29682337e-01,
       -3.68362256e-01, -1.00000000e+00, -1.16328812e-17,  2.93593711e-17,
        1.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00]), 
        array([ 
        9.29682337e-01,  3.68362256e-01, -1.00000000e+00, -9.29682337e-01,
       -3.68362256e-01, -7.97024412e-17, -1.16328812e-17,  2.93593711e-17,
        1.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00]))"""
        new_vecs = dihed_vec(coords, 0, 3, 2, 1, method='expansion', order=1)
        print("="*10)
        print(new_vecs[1])
        print("-"*10)
        old_vecs = dihed_vec(coords, 0, 3, 2, 1, method='og', order=1)
        print(old_vecs[1])
        raise Exception(new_vecs[0], old_vecs[0])
        raise Exception(...)


    @validationTest
    def test_ConvertInternals(self):

        from Psience.Molecools import Molecule
        import McUtils.Numputils as nput

        mol = Molecule.from_file(
            # I'm just using this to read in the atoms
            # and coordinates, you can supply your own
            TestManager.test_data('OCHD_freq.fchk'),
            internals=[
                # This can be modified to take any arbitrary function of Z-matrix
                # coordinates which allows us to use symmetrized or redundant
                # coordinate sets if needed, but I figured I'd get you started with this

                [0, -1, -1, -1], # centered on the carbon
                [1,  0, -1, -1], # OC bond length
                [2,  1,  0, -1], # HCO
                [3,  1,  0,  2], # HCO
            ]
        )

        # this stands in for your gradient and Hessian from electronic structure
        nat = 4
        nx = nat * 3
        grad = np.random.rand(nx)
        hess = np.random.rand(nx, nx)
        hess = hess @ hess.T

        # uses finite difference to get derivatives of Cartesians w.r.t internals
        # and then reexpresses the Cartesian expansion
        jacobians = mol.embedding.get_cartesians_by_internals(order=2, strip_embedding=True)
        surf = nput.tensor_reexpand(jacobians, [grad, hess])

        print(surf)
        print(surf[1])

    @validationTest
    def test_NormalFormCommutators(self):
        # phases, terms, symbols = normalize_commutators([[0, 1], 2])
        # phases, terms, symbols = normalize_commutators([0, [1, 2]])
        # phases, terms, symbols = normalize_commutators([[0, 1], [2, 3]])
        # phases, terms, symbols = normalize_commutators([[[0, 1], 2], [3, 4]])
        # phases, terms, symbols = normalize_commutators([[[0, 1], [[2, 3], [[4, 5], 6]]], [7, 8]])
        # phases, terms = normalize_commutators([[[0, 1], 2], [3, 4]])
        # print(symbols)
        # for p,t in zip(phases, terms):
        #     print(p, t)
        # phases, ct = commutator_terms([0, 1])
        # print(ct)
        # phases, ct = commutator_terms([[3, 4], [2, [0, 1]]])
        # phases, ct = commutator_terms([[0, 1], 2])
        # print(phases)
        # print(ct)
        # return
        # np.random.seed(123)
        # expansion = np.random.rand(8, 5, 5)
        # comm = [2, [[[1, [3, 4]], 5], 0]]
        # res_0 = commutator_evaluate(comm, expansion, recursive=True)
        # res_1 = commutator_evaluate(comm, expansion, direct=True)
        # res_2 = commutator_evaluate(comm, expansion, direct=False)
        # print(np.round(np.abs(res_1 - res_0), 8))
        # print(np.round(np.abs(res_1 - res_2), 8))

        def nested_commutator_expansion(k, side='left'):
            if side == 'left':
                comm = 0
                for i in range(1, k):
                    comm = [comm, i]
            else:
                comm = k - 1
                for i in range(k - 2, -1, -1):
                    comm = [i, comm]
            return comm

        c = nested_commutator_expansion(4)
        print(c)
        print(commutator_terms(c)[1])

    @validationTest
    def test_Symmetrization(self):
        # a = np.random.rand(3, 3, 3)
        # b = symmetrize_array(a,
        #                      axes=[[0, 2], [1]],
        #                      # restricted_diagonal=True,
        #                      mixed_block_symmetrize=True,
        #                      symmetrization_mode='low',
        #                      out=np.zeros_like(a)
        #                      )
        # # print(b)
        # print(b - np.transpose(b, (1, 2, 0)))

        a = [
            np.random.rand(3, 9),
            symmetrize_array(np.random.rand(3, 3, 9), axes=[[0, 1], [2]]),
            symmetrize_array(np.random.rand(3, 3, 3, 9), axes=[[0, 1, 2], [3]])
        ]

        b = [
            np.random.rand(3),
            symmetrize_array(np.random.rand(3, 3)),
            symmetrize_array(
                np.random.rand(3, 3, 9),
                axes=[[0, 1], [2]]
            ),
            symmetrize_array(
                np.random.rand(3, 3, 9, 9),
                axes=[[0, 1], [2, 3]]
            )
        ]

        c = tensor_reexpand(a, b[-2:], axes=[-1, -1])
        print([cc.shape for cc in c])
        return

    @validationTest
    def test_mixedShapeExpansions(self):
        """
        [(6, 12), (6, 6, 12), (6, 6, 6, 12)] [(3, 12), (3, 6, 12), (3, 6, 6, 12)]
        :return:
        """
        a = [
            np.random.rand(6, 12),
            symmetrize_array(np.random.rand(6, 6, 12), [0, 1]),
            symmetrize_array(np.random.rand(6, 6, 6, 12), [0, 1, 2])
        ]
        b = [
            np.random.rand(3, 12),
            symmetrize_array(np.random.rand(3, 12, 12), [1]),
            symmetrize_array(np.random.rand(3, 4, 4, 12, 12), [1, 2])
        ]
        c = tensor_reexpand(a[:2], b[:2], axes=[-1, -1])
        print([cc.shape for cc in c])


    @validationTest
    def test_YoungTableaux(self):
        import McUtils.Iterators as itut
        import McUtils.Combinatorics as comb
        from McUtils.McUtils.Numputils.TensorDerivatives import nca_partition_terms


        perm_inds, perms = comb.UniquePermutations([2, 2, 1, 1]).permutations(return_indices=True)
        print(
            np.concatenate([
                np.array([
                    np.min(perm_inds[:, :2], axis=1),
                    np.min(perm_inds[:, 2:], axis=1)
                ]).T,
                perms
            ], axis=1)
        )

        return

        print(nca_partition_terms((2, 2)))
        return

        comb.UniquePermutations([0, 0, 1, 1]).permutations(position_blocks=[0, ])



        def populate_sst_frame_from_components(
                frame_shape,
                offsets,
                sub_ssts
        ):
            frame = np.zeros(frame_shape, dtype=int)
            for i,(o,ss) in enumerate(zip(offsets, sub_ssts)):
                n = len(ss)
                frame[o:o+n] = ss
            return frame


        # print(
        #     split_frame(
        #         np.array([3, 2]),
        #         np.array([1, 0])
        #     )
        # )
        # return

        def validate_frame(frame):
            if np.any(np.diff([f[0] for f in frame]) < 0):
                return False

        # parts = comb.IntegerPartitioner2D.get_partitions([4, 3], [4, 3])
        # print(offsets)
        # print(valid)

        yt = comb.YoungTableauxGenerator(6)
        p = [3, 2, 1]
        tabs = yt.get_standard_tableaux(partitions=[p])[0]
        print(len(tabs[0]))
        for t in zip(*tabs):
            print("-" * 10)
            for s in t:
                print(s)

        print("="*20)
        bf_tabs = yt.get_standard_tableaux(partitions=[p], brute_force=True)[0]
        print(len(bf_tabs[0]))
        for t in zip(*bf_tabs):
            print("-" * 10)
            for s in t:
                print(s)


