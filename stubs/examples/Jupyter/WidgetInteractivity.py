"""Extracted from JupyterTests.test_WidgetInteractivity via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest JupyterTests.test_WidgetInteractivity"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Jupyter import *
import McUtils.Jupyter as interactive
import numpy as np

class JupyterTests(TestCase):

    @validationTest
    def test_WidgetInteractivity(self):
        import McUtils.Jupyter as interactive
        from Psience.Molecools import Molecule
        reactant = Molecule.from_string('CCO', 'smi')
        p = reactant.plot(backend='x3d')
        print(type(interactive.Grid([[p, p]], dynamic=False).to_jhtml()))
        print(type(interactive.Carousel([p, p], dynamic=False).to_jhtml()))
