"""Extracted from SymmetryTests.test_SymmetryElements via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest SymmetryTests.test_SymmetryElements"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Symmetry import *
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):

    @validationTest
    def test_SymmetryElements(self):
        for s in [InversionElement(), RotationElement(5, [0, 1, 1], 2), ImproperRotationElement(11, [1, 0, 0]), ReflectionElement([1, 0, 1])]:
            self.assertEquals(SymmetryElement.from_transformation_matrix(s.get_transformation()), s)
