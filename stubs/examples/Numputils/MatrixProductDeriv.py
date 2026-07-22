"""Extracted from NumputilsTests.test_MatrixProductDeriv via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_MatrixProductDeriv"""

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

    @inactiveTest
    def test_MatrixProductDeriv(self):
        x = np.pi / 6
        y = np.pi / 3
        import sympy
        x, y = sympy.symbols('x y')
        sx = sympy.sin(x)
        cx = sympy.cos(x)
        sy = sympy.sin(y)
        cy = sympy.cos(y)
        A = sympy.Array([[sx * sy, sx * cy], [cx * sy, cx * cy]])
        B = sympy.Array([x ** 3, y ** 3])
        AB = sympy.tensorproduct(A * B)
        raise Exception(AB)
        A_mat = np.array([[np.cos(x) * np.cos(y), np.cos(y) * np.sin(np.pi / 3)], [-np.cos(x) * np.sin(y), np.sin(x) * np.sin(np.pi / 3)]])
        sinx_cosx_expansion = ...
        a = np.random.rand(5, 10, 2, 3)
        b = np.random.rand(5, 10, 4, 2, 3)
        self.assertTrue(np.allclose(new_vec_outer(a, b, axes=[[], [2]]), a[:, :, np.newaxis, :, :] * b))
        a = np.random.rand(5, 10, 9, 7)
        b = np.random.rand(5, 10, 4, 2, 3)
        self.assertTrue(np.allclose(new_vec_outer(a, b, axes=[[2, 3], [2, 3, 4]]), vec_outer(a, b, axes=[[2, 3], [2, 3, 4]])))
