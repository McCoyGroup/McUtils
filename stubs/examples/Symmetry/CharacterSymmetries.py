"""Extracted from SymmetryTests.test_CharacterSymmetries via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest SymmetryTests.test_CharacterSymmetries"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Symmetry import *
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):

    @validationTest
    def test_CharacterSymmetries(self):
        p = CharacterTable.point_group('Cv', 3)
        coords = np.concatenate([[[0, 0, 1]], nput.apply_symmetries([1, 0, 0], p.matrices)], axis=0)
        character_coeffs2 = p.symmetrized_coordinate_coefficients(coords, as_characters=False)
        print(np.round(np.sum(character_coeffs2[:6, 3], axis=0).reshape(4, 3), 8))
        print(np.round(np.sum(character_coeffs2[:6, 6], axis=0).reshape(4, 3), 8))
        print(np.round(np.sum(character_coeffs2[:6, 9], axis=0).reshape(4, 3), 8))
