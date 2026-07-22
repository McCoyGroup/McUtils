"""Extracted from NumputilsTests.test_PtsDihedralsDeriv via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_PtsDihedralsDeriv"""

import collections
import itertools
import math
import os.path
from Peeves.TestUtils import *
from Peeves import BlockProfiler
import McUtils.Numputils as nput
from McUtils.Numputils import *
from McUtils.Zachary import FiniteDifferenceDerivative
from unittest import TestCase
import numpy as np, scipy, functools as ft

class NumputilsTests(TestCase):
    problem_coords = np.array([[-1.86403557e-17, -0.076046524, 0.0462443228], [6.70904773e-17, -0.076046524, -0.953755677], [0.929682337, 0.292315732, 0.0462443228], [2.46519033e-32, -1.38777878e-17, 0.225076602], [-1.97215226e-31, 1.4371441, -0.90030641], [-1.75999392e-16, -1.4371441, -0.90030641]])

    @classmethod
    def setUp(self):
        np.set_printoptions(linewidth=100000000.0)

    @validationTest
    def test_PtsDihedralsDeriv(self):
        np.random.seed(0)
        coords = np.random.rand(16, 3)
        angs, derivs, derivs_2 = dihed_deriv(coords, [4, 7], [5, 6], [6, 5], [7, 4], order=2)
        ang = angs[0]
        deriv = derivs[:, 0, :]
        deriv_2 = derivs_2[:, :, 0, :, :]
        ang2 = pts_dihedrals(coords[4], coords[5], coords[6], coords[7])
        self.assertEquals(ang2, ang[0])
        fd = FiniteDifferenceDerivative(lambda pt: pts_dihedrals(pt[..., 0, :], pt[..., 1, :], pt[..., 2, :], pt[..., 3, :]), function_shape=((None, 4, 3), 0), mesh_spacing=1e-05)
        dihedDeriv_fd = FiniteDifferenceDerivative(lambda pts: dihed_deriv(pts, 0, 1, 2, 3, order=1)[1].squeeze().transpose((1, 0, 2)), function_shape=((None, 4, 3), (None, 4, 3)), mesh_spacing=1e-05)
        fd1, fd2 = fd(coords[(4, 5, 6, 7),]).derivative_tensor([1, 2])
        fd2_22 = dihedDeriv_fd(coords[(4, 5, 6, 7),]).derivative_tensor(1)
        self.assertTrue(np.allclose(deriv.flatten(), fd1.flatten()), msg="{} and {} aren't close".format(deriv.flatten(), fd1.flatten()))
        d2_flat = np.concatenate([np.concatenate([deriv_2[0, 0], deriv_2[0, 1], deriv_2[0, 2], deriv_2[0, 3]], axis=1), np.concatenate([deriv_2[1, 0], deriv_2[1, 1], deriv_2[1, 2], deriv_2[1, 3]], axis=1), np.concatenate([deriv_2[2, 0], deriv_2[2, 1], deriv_2[2, 2], deriv_2[2, 3]], axis=1), np.concatenate([deriv_2[3, 0], deriv_2[3, 1], deriv_2[3, 2], deriv_2[3, 3]], axis=1)], axis=0)
        bleh = fd2_22.reshape(12, 12)
        self.assertTrue(np.allclose(d2_flat.flatten(), bleh.flatten(), atol=1e-07), msg='d2: {} and {} differ'.format(d2_flat.flatten(), bleh.flatten()))
        self.assertTrue(np.allclose(d2_flat.flatten(), fd2.flatten(), atol=0.001), msg='d2: {} and {} differ'.format(d2_flat.flatten(), fd2.flatten()))
        coords = np.array([[1, 0, 0], [1, -1, 0], [-1, 1, 0], [-1, 0, 0]])
        angs, derivs = dihed_deriv(coords, 0, 1, 2, 3, order=1)
        ang = angs[0]
        deriv = derivs
        ang2 = pts_dihedrals(coords[0], coords[1], coords[2], coords[3])
        self.assertTrue(np.allclose(np.abs(ang2), ang))
        raise Exception(deriv)
        fd = FiniteDifferenceDerivative(lambda pt: pts_dihedrals(pt[..., 0, :], pt[..., 1, :], pt[..., 2, :], pt[..., 3, :]), function_shape=((None, 4, 3), 0), mesh_spacing=1e-05)
        fd1 = fd(coords[(0, 1, 2, 3),]).derivative_tensor([1])[0]
        self.assertTrue(np.allclose(deriv.flatten(), fd1.flatten()), msg="{} and {} aren't close".format(deriv.flatten(), fd1.flatten()))
