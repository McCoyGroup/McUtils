"""Extracted from SymmetryTests.test_Composition via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest SymmetryTests.test_Composition"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Symmetry import *
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):

    @validationTest
    def test_Composition(self):
        np.random.seed(123)
        ax = np.random.rand(3)
        ax2 = np.cross(ax, [0, 1, 0])
        ax3 = RotationElement(6, ax).get_transformation() @ ax
        for a, b in [[InversionElement(), RotationElement(7, ax2, root=5)], [RotationElement(2, ax), RotationElement(7, ax2, root=5)], [RotationElement(2, ax), ImproperRotationElement(7, ax2, root=5)], [RotationElement(3, ax), RotationElement(7, ax, root=5)], [RotationElement(6, ax), RotationElement(11, ax3)], [RotationElement(6, ax), ImproperRotationElement(12, ax3)]]:
            s1 = a @ b
            s2 = SymmetryElement.compose(a, b)
            print(a, '@', b, '=>', s1)
            if hasattr(s1, 'bits'):
                print(':', SymmetryElement.from_transformation_matrix(s1.get_transformation()))
            self.assertTrue(np.allclose(s1.get_transformation(), s2.get_transformation()))
