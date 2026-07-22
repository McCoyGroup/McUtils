"""Extracted from NumputilsTests.test_MoreGeometry via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_MoreGeometry"""

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
    def test_MoreGeometry(self):
        np.random.seed(123123)
        pts = np.random.rand(3, 3)
        tri = nput.make_triangle(pts)
        tpf_A = nput.triangle_property_function(tri, 'A')
        print(nput.triangle_property(tri, 'A'))
        print(tpf_A(tri))
        np.random.seed(123123)
        pts = np.random.rand(4, 3)
        dd = nput.make_dihedron(a=nput.pts_norms(pts[0], pts[1]), b=nput.pts_norms(pts[1], pts[2]), c=nput.pts_norms(pts[2], pts[3]), X=nput.pts_angles(pts[0], pts[1], pts[2], return_crosses=False), Y=nput.pts_angles(pts[1], pts[2], pts[3], return_crosses=False), Tb=nput.pts_dihedrals(pts[0], pts[1], pts[2], pts[3]))
        converter = nput.dihedron_property_function(dd, 'Z')
        print(nput.dihedron_property(dd, 'Z'))
        print(converter(dd))
        return
        tri = nput.make_triangle(np.random.rand(3, 3))
        A, tnew = nput.triangle_property(tri, 'A')
        tri2 = nput.make_triangle(b=tnew.b, A=tnew.A, c=tnew.c)
        C, tnew = nput.triangle_property(tri2, 'C')
        tri2 = nput.make_triangle(A=tnew.A, c=tnew.b, C=tnew.C)
        B, tnew = nput.triangle_property(tri2, 'B')
        np.random.seed(123123)
        pts = np.random.rand(4, 3)
        dd = nput.make_dihedron(a=nput.pts_norms(pts[0], pts[1]), b=nput.pts_norms(pts[1], pts[2]), c=nput.pts_norms(pts[2], pts[3]), X=nput.pts_angles(pts[0], pts[1], pts[2], return_crosses=False), Y=nput.pts_angles(pts[1], pts[2], pts[3], return_crosses=False), Tb=nput.pts_dihedrals(pts[0], pts[1], pts[2], pts[3]))
        z, dd = nput.dihedron_property(dd, 'z')
        print(z, nput.pts_norms(pts[0], pts[3]))
        x, dd = nput.dihedron_property(dd, 'x')
        print(x, nput.pts_norms(pts[0], pts[2]))
        y, dd = nput.dihedron_property(dd, 'y')
        print(y, nput.pts_norms(pts[1], pts[3]))
        dd = nput.make_dihedron(a=nput.pts_norms(pts[0], pts[1]), b=nput.pts_norms(pts[1], pts[2]), c=nput.pts_norms(pts[2], pts[3]), X=nput.pts_angles(pts[0], pts[1], pts[2], return_crosses=False), Y=nput.pts_angles(pts[1], pts[2], pts[3], return_crosses=False), Tb=nput.pts_dihedrals(pts[0], pts[1], pts[2], pts[3]))
        coords_map = {'a': (0, 1), 'b': (1, 2), 'c': (2, 3), 'x': (0, 2), 'y': (1, 3), 'z': (0, 3), 'X': (0, 1, 2), 'Y': (1, 2, 3), 'A': (0, 2, 1), 'B1': (1, 0, 2), 'C': (2, 1, 3), 'B2': (1, 3, 2), 'Z': (0, 1, 3), 'Z2': (0, 2, 3), 'A3': (0, 3, 1), 'Y3': (1, 0, 3), 'C4': (2, 0, 3), 'X4': (0, 3, 2), 'Tb': (0, 1, 2, 3), 'Ta': (2, 0, 1, 3), 'Tc': (0, 2, 3, 1), 'Tx': (1, 0, 2, 3), 'Ty': (0, 1, 3, 2), 'Tz': (1, 0, 3, 2)}
        for prop, inds in coords_map.items():
            print(f'{prop}:', end=' ')
            Z, _ = nput.dihedron_property(dd, prop)
            if len(inds) == 2:
                val = nput.pts_norms(pts[inds[0]], pts[inds[1]])
            elif len(inds) == 3:
                val = nput.pts_angles(pts[inds[0]], pts[inds[1]], pts[inds[2]], return_crosses=False)
            else:
                val = nput.pts_dihedrals(pts[inds[0]], pts[inds[1]], pts[inds[2]], pts[inds[3]])
            print(Z, val)
