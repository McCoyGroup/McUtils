"""Extracted from DataTests.test_BondData via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest DataTests.test_BondData"""

import numpy as np
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Data import *

class DataTests(TestCase):

    @validationTest
    def test_BondData(self):
        self.assertIsInstance(BondData['H'], dict)
        self.assertLess(BondData['H', 'H', 1], 1)
        self.assertLess(BondData['H', 'O', 1], 1)
        self.assertGreater(BondData['H', 'C', 1], 1)
