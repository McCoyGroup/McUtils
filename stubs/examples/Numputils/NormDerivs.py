"""Extracted from NumputilsTests.test_NormDerivs via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_NormDerivs"""

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
    def test_NormDerivs(self):
        np.random.seed(0)
        coords = np.random.rand(16, 3)
        a = coords[(4, 5),] - coords[(5, 4),]
        na, na_da, na_daa = vec_norm_derivs(a, order=2)
        na_2 = vec_norms(a)
        self.assertEquals(tuple(na_2), tuple(na))
        norm_fd = FiniteDifferenceDerivative(lambda vecs: vec_norms(vecs), function_shape=((None, 2, 3), (None,)), mesh_spacing=0.0001)
        fd_nada, fd_nadaa = norm_fd(a).derivative_tensor([1, 2])
        fd_nada = np.array([fd_nada[:3, 0], fd_nada[3:, 1]])
        fd_nadaa = np.array([fd_nadaa[:3, :3, 0], fd_nadaa[3:, 3:, 1]])
        self.assertTrue(np.allclose(na_da.flatten(), fd_nada.flatten()), msg='norm d1: {} and {} differ'.format(na_da.flatten(), fd_nada.flatten()))
        self.assertTrue(np.allclose(na_daa.flatten(), fd_nadaa.flatten(), atol=0.0001), msg='norm d1: {} and {} differ'.format(na_daa.flatten(), fd_nadaa.flatten()))
