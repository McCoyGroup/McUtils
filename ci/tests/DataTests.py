import numpy as np

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Data import *

class DataTests(TestCase):

    @validationTest
    def test_AtomData(self):
        self.assertIsInstance(AtomData["H"], DataRecord)
        self.assertIsInstance(AtomData["Hydrogen"], DataRecord)
        self.assertIsInstance(AtomData["Helium3"], DataRecord)
        self.assertIs(AtomData["Hydrogen2"], AtomData["Deuterium"])
        self.assertIs(AtomData["H2"], AtomData["Deuterium"])
        self.assertIs(AtomData["H1"], AtomData["Hydrogen"])
        self.assertIs(AtomData[8], AtomData["Oxygen"])

    @validationTest
    def test_AtomMasses(self):
        self.assertLess(AtomData["Helium3", "Mass"], AtomData["T"]["Mass"]) # fun weird divergence

    @validationTest
    def test_Conversions(self):
        # print(AtomData["T"]["Mass"]-AtomData["Helium3", "Mass"], file=sys.stderr)
        self.assertGreater(UnitsData.data[("Hartrees", "InverseMeters")]["Value"], 21947463.13)
        self.assertLess(UnitsData.data[("Hartrees", "InverseMeters")]["Value"], 21947463.14)
        self.assertAlmostEqual(
            UnitsData.convert("Hartrees", "Wavenumbers"),
            UnitsData.convert("Hartrees", "InverseMeters") / 100
        )
        self.assertAlmostEqual(
            UnitsData.convert("Hartrees", "Wavenumbers"),
            UnitsData.convert("Centihartrees", "InverseMeters")
        )

    @validationTest
    def test_AtomicUnits(self):
        # print(UnitsData["AtomicUnitOfMass"])
        self.assertAlmostEqual(UnitsData.convert("AtomicMassUnits", "AtomicUnitOfMass"), 1822.888486217313)

    @validationTest
    def test_BondData(self):
        self.assertIsInstance(BondData["H"], dict)
        self.assertLess(BondData["H", "H", 1], 1)
        self.assertLess(BondData["H", "O", 1], 1)
        self.assertGreater(BondData["H", "C", 1], 1)

    @debugTest
    def test_ColorData(self):
        rgb_code = [200, 10, 25]
        huh = ColorData.color_convert(rgb_code, 'rgb', 'xyz')
        og = ColorData.color_convert(huh, 'xyz', 'rgb')
        print(huh, og)

        huh = ColorData.color_convert(rgb_code, 'rgb', 'hsl')
        og = ColorData.color_convert(huh, 'hsl', 'rgb')
        print(huh, og, ColorData.rgb_code(og))


        huh = ColorData.color_convert(rgb_code, 'rgb', 'hsv')
        og = ColorData.color_convert(huh, 'hsv', 'rgb')
        print(huh, og, ColorData.rgb_code(og))

        huh = ColorData.color_convert(rgb_code, 'rgb', 'lab')
        og = ColorData.color_convert(huh, 'lab', 'rgb')
        print(huh, og, ColorData.rgb_code(og))

        print(ColorData["pastel"].blend(.2))
        # return

        import McUtils.Plots as plt

        grid = np.linspace(0, 2*np.pi, 200)
        base_fig = None
        for i in range(6):
            base_fig = plt.Plot(
                grid,
                i + np.sin((i+1)*grid),
                figure=base_fig,
                style_list={'color':ColorData["pastel"]}
            )

        base_fig = None
        for i in range(10):
            base_fig = plt.Plot(
                grid,
                i + np.sin((i+1)*grid),
                figure=base_fig,
                color=ColorData["WarioColors"].blend(i/9)
            )

        base_fig.show()