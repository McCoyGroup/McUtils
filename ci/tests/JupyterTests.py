
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Jupyter import *
import McUtils.Jupyter as interactive
import numpy as np

class JupyterTests(TestCase):

    @validationTest
    def test_HTML(self):
        Div = HTML.Div
        Bootstrap.Panel(
            Bootstrap.Grid(np.random.rand(5, 5).round(3).tolist()),
            header='Test Panel',
            variant='primary'
        ).tostring()

    @validationTest
    def test_Styles(self):
        CSS.parse("""
a {
  text-variant:none;
}
        """)[0].tostring()

    @validationTest
    def test_WidgetConstruction(self):
        from Psience.Molecools import Molecule
        water = Molecule.from_string('O', 'smi')
        widg = interactive.JHTML.Div(water.plot(backend='x3d').figure.to_x3d(), dynamic=True)
        print(widg.elem.children[0].children)

    @debugTest
    def test_WidgetInteractivity(self):
        import McUtils.Jupyter as interactive
        from Psience.Molecools import Molecule

        reactant = Molecule.from_string("CCO", "smi")

        p = reactant.plot(backend='x3d')

        print(type(
            interactive.Grid([[
                p, p
            ]], dynamic=False).to_jhtml()
        ))

        print(type(
            interactive.Carousel([
                p, p
            ], dynamic=False).to_jhtml()
        ))