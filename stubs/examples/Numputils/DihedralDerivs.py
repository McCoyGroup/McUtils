"""Extracted from NumputilsTests.test_DihedralDerivs via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_DihedralDerivs"""

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
    def test_DihedralDerivs(self):
        np.random.seed(153234)
        dihed_points = np.random.rand(4, 3)[(2, 1, 0, 3),]
        ssssss = distance_matrix(dihed_points, return_triu=True)[(0, 3, 5, 1, 4, 2),]
        t = dihedral_from_distance(ssssss, 'ssssst', use_cos=True)
        ssssss_expansion = [[z, o] for z, o in zip(ssssss, np.eye(6))]
        t_expansion = dihedral_from_distance(ssssss_expansion, 'ssssst', order=1, return_cos=True)
        print(t)
        print(t_expansion)
