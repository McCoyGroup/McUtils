"""Extracted from SymmetryTests.test_CharacterDecomposition via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest SymmetryTests.test_CharacterDecomposition"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Symmetry import *
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):

    @validationTest
    def test_CharacterDecomposition(self):
        pg = CharacterTable.point_group('Cv', 2)
        coords = np.array([[0.0, 0.0, 0.12595], [1.43714, 0.0, -0.99944], [-1.43714, 0.0, -0.99944]])
        self.assertEquals([2, 0, 1, 0], np.round(pg.coordinate_mode_reduction(coords), 8).tolist())
        pg = CharacterTable.point_group('Cv', 3)
        rep = pg.axis_representation()
        decomp = pg.decompose_representation(rep).T
        self.assertEquals([np.round(decomp[0] + decomp[1], 8).tolist(), np.round(decomp[2], 8).tolist()], [[0, 0, 1], [1, 0, 0]])
        self.assertEquals([np.round(decomp[3] + decomp[4], 8).tolist(), np.round(decomp[5], 8).tolist()], [[0, 0, 1], [0, 1, 0]])
        pg = CharacterTable.point_group('Td')
        rep = pg.axis_representation()
        decomp = pg.decompose_representation(rep).T
        self.assertEquals([np.round(np.sum(decomp[:3], axis=0), 8).tolist(), np.round(np.sum(decomp[3:], axis=0), 8).tolist()], [[0, 0, 0, 0, 1], [0, 0, 0, 1, 0]])
        print(np.round(np.sum(decomp[:3], axis=0), 8))
        print(np.round(np.sum(decomp[3:], axis=0), 8))
