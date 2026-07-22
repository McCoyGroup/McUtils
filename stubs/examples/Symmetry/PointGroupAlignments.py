"""Extracted from SymmetryTests.test_PointGroupAlignments via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest SymmetryTests.test_PointGroupAlignments"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Symmetry import *
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):

    @validationTest
    def test_PointGroupAlignments(self):
        pg = PointGroup.from_name('Ch', 6)
        print(pg.axes @ pg.axes.T)
        new_pg = pg.align(np.eye(3))
        print(new_pg.get_axes())
