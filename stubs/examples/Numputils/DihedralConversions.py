"""Extracted from NumputilsTests.test_DihedralConversions via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_DihedralConversions"""

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
    def test_DihedralConversions(self):
        np.random.seed(123123)
        for _ in range(1):
            dihed_points = np.random.rand(4, 3)[(2, 1, 0, 3),]
            ssssss = distance_matrix(dihed_points, return_triu=True)[(0, 3, 5, 1, 4, 2),]
            t = dihedral_from_distance(ssssss, 'ssssst')
            self.assertAlmostEqual(t, abs(pts_dihedrals(*dihed_points)))
            s = dihedral_distance(list(ssssss[:5]) + [t], 'ssssst')
            self.assertAlmostEqual(s, ssssss[-1])
            a1 = pts_angles(*dihed_points[:3], return_crosses=False)
            a2 = pts_angles(*dihed_points[1:], return_crosses=False)
            sssaas = list(ssssss[:3]) + [a1, a2, t]
            s2 = dihedral_distance(sssaas, 'sssaat')
            self.assertAlmostEqual(s, s2)
            sssaat = list(ssssss[:3]) + [a1, a2, s]
            t2 = dihedral_from_distance(sssaat, 'sssaat')
            self.assertAlmostEqual(t, t2)
            ssssas = list(ssssss[:4]) + [a2, t]
            s3 = dihedral_distance(ssssas, 'ssssat')
            self.assertAlmostEqual(s, s3)
            ssssat = list(ssssss[:4]) + [a2, s]
            t2 = dihedral_from_distance(ssssat, 'ssssat')
            self.assertAlmostEqual(t, t2)
