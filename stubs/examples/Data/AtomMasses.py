"""Extracted from DataTests.test_AtomMasses via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest DataTests.test_AtomMasses"""

import numpy as np
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Data import *

class DataTests(TestCase):

    @validationTest
    def test_AtomMasses(self):
        self.assertLess(AtomData['Helium3', 'Mass'], AtomData['T']['Mass'])
