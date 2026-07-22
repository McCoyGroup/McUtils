"""Extracted from JupyterTests.test_Styles via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest JupyterTests.test_Styles"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Jupyter import *
import McUtils.Jupyter as interactive
import numpy as np

class JupyterTests(TestCase):

    @validationTest
    def test_Styles(self):
        JHTML.CSS.parse('\na {\n  text-variant:none;\n}\n        ')[0].tostring()
