"""Extracted from NumputilsTests.test_SinCosDerivs via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_SinCosDerivs"""

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
    def test_SinCosDerivs(self):
        np.random.seed(0)
        coords = np.random.rand(16, 3)
        a = coords[6] - coords[5]
        b = coords[4] - coords[5]
        sin_derivs, cos_derivs = vec_sin_cos_derivs(np.array([a, b]), np.array([b, a]), order=2)
        cos_fd = FiniteDifferenceDerivative(lambda vecs: vec_cos(vecs[..., 0, :], vecs[..., 1, :]), function_shape=((None, 2, 3), 0), mesh_spacing=1e-07)
        cosDeriv_fd = FiniteDifferenceDerivative(lambda vecs: vec_sin_cos_derivs(vecs[..., 0, :], vecs[..., 1, :], order=1)[1][1].squeeze(), function_shape=((None, 2, 3), (None, 2, 3)), mesh_spacing=1e-07)
        cos_fd22_1, = cosDeriv_fd(np.array([a, b])).derivative_tensor([1])
        cos_fd22_2, = cosDeriv_fd(np.array([b, a])).derivative_tensor([1])
        cos_fd22 = np.array([cos_fd22_1, cos_fd22_2])
        cos_fd1_1, cos_fd2_1 = cos_fd(np.array([a, b])).derivative_tensor([1, 2])
        cos_fd1_2, cos_fd2_2 = cos_fd(np.array([b, a])).derivative_tensor([1, 2])
        cos_fd1 = np.array([cos_fd1_1, cos_fd1_2])
        cos_fd2 = np.array([cos_fd2_1, cos_fd2_2])
        sin_fd = FiniteDifferenceDerivative(lambda vecs: vec_sins(vecs[..., 0, :], vecs[..., 1, :]), function_shape=((None, 2, 3), 0), mesh_spacing=1e-07)
        sinDeriv_fd = FiniteDifferenceDerivative(lambda vecs: vec_sin_cos_derivs(vecs[..., 0, :], vecs[..., 1, :], order=1)[0][1].squeeze(), function_shape=((None, 2, 3), (None, 2, 3)), mesh_spacing=1e-07)
        sin_fd22_1, = sinDeriv_fd(np.array([a, b])).derivative_tensor([1])
        sin_fd22_2, = sinDeriv_fd(np.array([b, a])).derivative_tensor([1])
        sin_fd22 = np.array([sin_fd22_1, sin_fd22_2])
        sin_fd1_1, sin_fd2_1 = sin_fd(np.array([a, b])).derivative_tensor([1, 2])
        sin_fd1_2, sin_fd2_2 = sin_fd(np.array([b, a])).derivative_tensor([1, 2])
        sin_fd1 = np.array([sin_fd1_1, sin_fd1_2])
        sin_fd2 = np.array([sin_fd2_1, sin_fd2_2])
        s, s1, s2 = sin_derivs
        c, c1, c2 = cos_derivs
        self.assertTrue(np.allclose(s1.flatten(), sin_fd1.flatten()), msg='sin d1: {} and {} differ'.format(s1.flatten(), sin_fd1.flatten()))
        self.assertTrue(np.allclose(c1.flatten(), cos_fd1.flatten()), msg='cos d1: {} and {} differ'.format(c1.flatten(), cos_fd1.flatten()))
        c2_flat = np.concatenate([np.concatenate([c2[:, 0, 0], c2[:, 0, 1]], axis=2), np.concatenate([c2[:, 1, 0], c2[:, 1, 1]], axis=2)], axis=1)
        s2_flat = np.concatenate([np.concatenate([s2[:, 0, 0], s2[:, 0, 1]], axis=2), np.concatenate([s2[:, 1, 0], s2[:, 1, 1]], axis=2)], axis=1)
        self.assertTrue(np.allclose(s2_flat.flatten(), sin_fd22.flatten()), msg='sin d2: {} and {} differ'.format(s2_flat.flatten(), sin_fd22.flatten()))
        self.assertTrue(np.allclose(c2_flat.flatten(), cos_fd22.flatten()), msg='cos d2: {} and {} differ'.format(c2_flat.flatten(), cos_fd22.flatten()))
