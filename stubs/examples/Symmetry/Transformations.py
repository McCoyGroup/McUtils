"""Extracted from SymmetryTests.test_Transformations via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest SymmetryTests.test_Transformations"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Symmetry import *
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):

    @validationTest
    def test_Transformations(self):
        np.random.seed(12223)
        tf = nput.view_matrix(np.random.rand(3))
        ax = np.random.rand(3)
        for a in [InversionElement(), RotationElement(2, ax), RotationElement(5, ax), RotationElement(7, ax, 2), RotationElement(22, ax, 11), ReflectionElement(ax), ImproperRotationElement(3, ax), ImproperRotationElement(6, ax, 5), ImproperRotationElement(7, ax, 5)]:
            s = a.transform(tf)
            x1 = s.get_transformation()
            x2 = tf @ a.get_transformation() @ tf.T
            self.assertTrue(np.allclose(x1, x2))
