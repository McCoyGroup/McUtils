"""Extracted from SymmetryTests.test_InternalSymmetries via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest SymmetryTests.test_InternalSymmetries"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Symmetry import *
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):

    @debugTest
    def test_InternalSymmetries(self):
        import McUtils.Coordinerds as coordops
        import McUtils.Numputils as nput
        p = CharacterTable.point_group('Cv', 3)
        coords = np.concatenate([[[0, 0, 1]], nput.apply_symmetries([1, 0, 0], p.matrices)], axis=0)
        symm_modes = symmetrized_coordinate_coefficients(p, coords, drop_empty_modes=False)
        self.assertEquals([s.shape for s in symm_modes], [(12, 4), (12, 4), (12, 7)])
        internals = coordops.extract_zmatrix_internals([[0, -1, -1, -1], [1, 0, -1, -1], [2, 0, 1, -1], [3, 0, 2, 1]], canonicalize=True)
        coeffs, full_internals, red_exps, expansions, base = symmetrize_internals(p, internals, coords, return_expansions=True, return_base_expansion=True, reduce_redundant_coordinates=True)
        self.assertEquals(len(full_internals), 9)
        self.assertEquals([s.shape for s in coeffs], [(9, 3), (9, 3), (9, 6)])
        a1_coeffs, a1_inv = expansions[0]
        int_vals, _ = base
        self.assertAlmostEquals(a1_coeffs[0][0], int_vals[0][0] * np.sqrt(3))
        print(red_exps[1].shape)
        coeffs, full_internals, expansions, base = symmetrize_internals(p, internals, coords, return_expansions=True, return_base_expansion=True, atom_selection=[1, 2, 3])
