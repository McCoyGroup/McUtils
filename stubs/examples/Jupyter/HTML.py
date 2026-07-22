"""Extracted from JupyterTests.test_HTML via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest JupyterTests.test_HTML"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Jupyter import *
import McUtils.Jupyter as interactive
import numpy as np

class JupyterTests(TestCase):

    @validationTest
    def test_HTML(self):
        Div = JHTML.HTML.Div
        JHTML.Bootstrap.Panel(JHTML.Bootstrap.Grid(np.random.rand(5, 5).round(3).tolist()), header='Test Panel', variant='primary').tostring()
