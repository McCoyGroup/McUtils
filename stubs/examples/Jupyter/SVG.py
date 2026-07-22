"""Extracted from JupyterTests.test_SVG via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest JupyterTests.test_SVG"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Jupyter import *
import McUtils.Jupyter as interactive
import numpy as np

class JupyterTests(TestCase):

    @debugTest
    def test_SVG(self):
        SVG = JHTML.SVGContext
        uuh = SVG.Svg(SVG.Rect(x=0, y=0, width=10, height=10))
        uuh.display()
