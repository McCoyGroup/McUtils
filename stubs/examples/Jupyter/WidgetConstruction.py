"""Extracted from JupyterTests.test_WidgetConstruction via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest JupyterTests.test_WidgetConstruction"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Jupyter import *
import McUtils.Jupyter as interactive
import numpy as np

class JupyterTests(TestCase):

    @validationTest
    def test_WidgetConstruction(self):
        from Psience.Molecools import Molecule
        water = Molecule.from_string('O', 'smi')
        widg = interactive.JHTML.Div(water.plot(backend='x3d').figure.to_x3d(), dynamic=True)
        print(widg.elem.children[0].children)
