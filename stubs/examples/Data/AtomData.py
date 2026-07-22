"""Extracted from DataTests.test_AtomData via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest DataTests.test_AtomData"""

import numpy as np
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Data import *

class DataTests(TestCase):

    @validationTest
    def test_AtomData(self):
        self.assertIsInstance(AtomData['H'], DataRecord)
        self.assertIsInstance(AtomData['Hydrogen'], DataRecord)
        self.assertIsInstance(AtomData['Helium3'], DataRecord)
        self.assertIs(AtomData['Hydrogen2'], AtomData['Deuterium'])
        self.assertIs(AtomData['H2'], AtomData['Deuterium'])
        self.assertIs(AtomData['H1'], AtomData['Hydrogen'])
        self.assertIs(AtomData[8], AtomData['Oxygen'])
