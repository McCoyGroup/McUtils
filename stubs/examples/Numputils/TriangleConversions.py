"""Extracted from NumputilsTests.test_TriangleConversions via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_TriangleConversions"""

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
    def test_TriangleConversions(self):
        np.random.seed(15432)
        for _ in range(25):
            tri_points = np.random.rand(3, 3)
            sss = distance_matrix(tri_points, return_triu=True)[(0, 2, 1),]
            sas = np.array(triangle_convert(sss, 'sss', 'sas'))
            a = pts_angles(*tri_points, return_crosses=False)
            self.assertTrue(np.allclose(sas, [sss[0], a, sss[1]]))
            sss2 = triangle_convert(sas, 'sas', 'sss')
            self.assertTrue(np.allclose(sss, sss2))
            conv_tris = {}
            for conversion in ['sas', 'saa', 'asa']:
                new = np.array(triangle_convert(sss, 'sss', conversion))
                conv_tris[conversion] = new
                sss2 = np.array(triangle_convert(new, conversion, 'sss'))
                self.assertTrue(np.allclose(sss, sss2), msg=f'{conversion}: {sss} {sss2}')
            for conversion in ['sas', 'saa', 'asa']:
                for conversion2 in ['sas', 'saa', 'asa']:
                    new = np.array(triangle_convert(conv_tris[conversion], conversion, conversion2))
                    self.assertTrue(np.allclose(new, conv_tris[conversion2]), msg=conversion + '+' + conversion2)
