"""Extracted from SymmetryTests.test_PointGroupElements via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest SymmetryTests.test_PointGroupElements"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Symmetry import *
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):

    @validationTest
    def test_PointGroupElements(self):
        for name in [('T',), ('Td',), ('Th',), ('O',), ('Oh',), ('I',), ('Ih',)]:
            pg = PointGroup.from_name(*name)
            ct = pg.character_table
            elements = ct.permutations
            classes = ct.classes
            print(pg, pg.elements)
            self.assertIsNot(classes, None)
            self.assertEquals(np.sort(np.concatenate(classes)).tolist(), np.arange(sum((len(l) for l in classes))).tolist())
            self.assertEquals(len(elements), sum((len(l) for l in classes)))
