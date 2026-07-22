"""Extracted from NumputilsTests.test_DihedralDerivativeComparison via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_DihedralDerivativeComparison"""

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
    def test_DihedralDerivativeComparison(self):
        import Psience as psi
        test_root = os.path.join(os.path.dirname(psi.__file__), 'ci', 'tests', 'TestData')
        from Psience.Molecools import Molecule
        mol = Molecule.from_file(os.path.join(test_root, 'HOONO_freq.fchk'))
        '\n        ==> [[[ 0.77190252  0.         -0.0719183  ...  0.          0.\n    0.04552509]\n  [-0.16557176  0.         -0.38929849 ...  0.          0.\n   -0.01881451]\n  [ 0.61380168  0.         -0.01456972 ...  0.          0.\n    0.08105092]\n  ...\n  [ 0.          0.          0.         ... -0.55669355  0.40498602\n    0.00877491]\n  [ 0.          0.          0.         ... -0.7321073  -0.24340891\n    0.26671989]\n  [ 0.          0.          0.         ... -0.39257    -0.12036494\n   -0.50985179]]]'
        coords = mol.coords
        import McUtils.McUtils.Numputils.CoordOps as coops
        import itertools
        for c in itertools.combinations(range(coords.shape[0]), 4):
            for p in itertools.permutations(c):
                coops.fast_proj = True
                new = dihed_vec(coords, *p, order=2)
                coops.fast_proj = False
                old = dihed_vec(coords, *p, order=2)
                if not np.allclose(new[1], old[1]):
                    print(coords)
                    raise ValueError(p, new[1], old[1])
        return
        coops.fast_proj = True
        new = dihed_vec(coords, 3, 0, 2, 1, order=2)
        coops.fast_proj = False
        old = dihed_vec(coords, 3, 0, 2, 1, order=2)
        with np.printoptions(linewidth=100000000.0):
            print('=' * 10)
            print(new[0])
            print(old[0])
            print('=' * 10)
            print(new[1])
            print(old[1])
            print('-' * 10)
            print(new[2] - old[2])
        return
        inv_coords = inverse_coordinate_solve([(0, 1), (0, 2), (0, 3), (0, 1, 2), (0, 1, 3), (0, 2, 3)], [1.9126349402213, 1.9126349325765, 1.9126349325765, 1.8634707086348 + 0.2, 1.8634707086348, 1.8634707045268], coords, remove_translation_rotation=False)
        spec = [(0, 1), (0, 2), (0, 3), (0, 1, 2), (0, 1, 3), (0, 2, 3)]
        fwd = internal_coordinate_tensors(coords, spec, order=2)
        (rev, _), _ = inverse_coordinate_solve(spec, fwd[0], coords, order=2)
        raise Exception(rev[0], coords)
        coords = Molecule.from_file(os.path.expanduser('~/Documents/UW/Research/Development/Psience/ci/tests/TestData/HOH_freq.fchk')).coords
        raise Exception('?', wag_vec(coords, 2, 0, 1, order=1)[-1].reshape(-1, 3)[:4])
        raise Exception(int_coord_tensors(coords, [(0, 1, 2), {'rock': (0, 1, 2)}, {'rock': (0, 1, 2), 'fixed_atoms': [0]}]))
        '\n        (array([ 9.29682337e-01,  3.68362256e-01,  7.97024412e-17, -9.29682337e-01,\n       -3.68362256e-01, -1.00000000e+00, -1.16328812e-17,  2.93593711e-17,\n        1.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,\n        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,\n        0.00000000e+00,  0.00000000e+00]), \n        array([ \n        9.29682337e-01,  3.68362256e-01, -1.00000000e+00, -9.29682337e-01,\n       -3.68362256e-01, -7.97024412e-17, -1.16328812e-17,  2.93593711e-17,\n        1.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,\n        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,\n        0.00000000e+00,  0.00000000e+00]))'
        new_vecs = dihed_vec(coords, 0, 3, 2, 1, method='expansion', order=1)
        print('=' * 10)
        print(new_vecs[1])
        print('-' * 10)
        old_vecs = dihed_vec(coords, 0, 3, 2, 1, method='og', order=1)
        print(old_vecs[1])
        raise Exception(new_vecs[0], old_vecs[0])
        raise Exception(...)
