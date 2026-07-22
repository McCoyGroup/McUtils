"""Extracted from NumputilsTests.test_BoysLocalize via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_BoysLocalize"""

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
    def test_BoysLocalize(self):
        ndim = 4 * 3
        np.random.seed(1)
        rot = rotation_matrix_skew(np.random.uniform(1, 2, math.comb(ndim, 2)))[:, 6:]

        def f(col):
            subcol = col.reshape(-1, 3)
            return np.sum(vec_dots(subcol, subcol, axis=-1) ** 2)

        def fprime(col):
            subcol = col.reshape(-1, 3)
            squares = vec_dots(subcol, subcol, axis=-1)
            return 4 * (subcol * squares[:, np.newaxis]).flatten()

        def op_f(col_i, col_j):
            subcol1 = col_i.reshape(-1, 3)
            subcol2 = col_j.reshape(-1, 3)
            a = np.sum(vec_dots(subcol1, subcol1, axis=-1) ** 2)
            b = np.sum(vec_dots(subcol1, subcol2, axis=-1) ** 2)
            c = np.sum(vec_dots(subcol2, subcol2, axis=-1) ** 2)
            return (a, b, c)
        mat, U, err = jacobi_maximize(rot, LineSearchRotationGenerator(f), max_iterations=30)
        with np.printoptions(linewidth=100000000.0):
            print(np.round(100 * np.sum((mat ** 2).reshape(-1, 3, rot.shape[-1]), axis=1)))
            '\n# Unmixed\n [[12.  1. 28.  9. 50. 51.]\n  [21. 25.  5.  6. 10. 12.]\n  [54. 23. 11.  9. 22. 16.]\n  [13. 50. 56. 77. 17. 21.]]\n \n # Gradient Descent\n [[68.  3. 69.  1.  8.  2.]\n  [ 6.  4. 13. 41.  9.  6.]\n  [26. 10. 15.  1. 81.  1.]\n  [ 0. 83.  3. 57.  2. 90.]]\n \n # Linesearch\n [[ 1. 71. 69.  1.  6.  2.]\n  [41. 12.  7.  6. 10.  4.]\n  [ 1. 16. 24.  1. 83. 10.]\n  [57.  1.  0. 91.  0. 85.]]\n \n # Analytic\n[[67. 63.  4.  2.  6.  8.]\n [ 6. 17.  5.  9.  8. 34.]\n [23. 15. 12.  7. 69. 10.]\n [ 5.  5. 79. 82. 17. 48.]]\n \n # Pairwise\n [[ 8.  1. 10. 15. 50. 66.]\n  [13. 35.  5. 11. 10.  7.]\n  [73.  7.  2.  5. 22. 25.]\n  [ 6. 57. 83. 69. 17.  3.]]\n'
        raise Exception(np.linalg.det(U), err)
