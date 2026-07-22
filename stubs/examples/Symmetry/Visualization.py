"""Extracted from SymmetryTests.test_Visualization via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest SymmetryTests.test_Visualization"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Symmetry import *
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):

    @validationTest
    def test_Visualization(self):
        pg = PointGroup.from_name('Dd', 3)
        print(pg.axes)
        new_pg = pg.align(np.eye(3))
        print(new_pg.axes)
        new_pg.plot().show()
        for e in pg.elements:
            if hasattr(e, 'axis'):
                print(e, e.axis)
