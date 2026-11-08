import unittest
import numpy as np
from McUtils.ExternalPrograms.Parsers.GaussianFChkComponents import parse_pol_num_derivs


class GaussianRamanTests(unittest.TestCase):
    def test_numerical_polarizabilities_are_ordered_by_derivative_order(self):
        # Two modes: both first-derivative tensors precede both second derivatives.
        firsts, seconds = parse_pol_num_derivs(np.arange(1., 25.))
        np.testing.assert_array_equal(firsts[0], [[1, 2, 4], [2, 3, 5], [4, 5, 6]])
        np.testing.assert_array_equal(firsts[1], [[7, 8, 10], [8, 9, 11], [10, 11, 12]])
        np.testing.assert_array_equal(seconds[0, 0], [[13, 14, 16], [14, 15, 17], [16, 17, 18]])
        np.testing.assert_array_equal(seconds[1, 1], [[19, 20, 22], [20, 21, 23], [22, 23, 24]])
        np.testing.assert_array_equal(seconds[0, 1], np.zeros((3, 3)))
        np.testing.assert_array_equal(seconds[1, 0], np.zeros((3, 3)))

    def test_incomplete_polarizability_blocks_are_rejected(self):
        for size in (0, 6, 13):
            with self.subTest(size=size), self.assertRaises(ValueError):
                parse_pol_num_derivs(np.zeros(size))
