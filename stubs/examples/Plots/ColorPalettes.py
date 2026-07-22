"""Extracted from PlotsTests.test_ColorPalettes via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_ColorPalettes"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Plots import *
import sys, os, numpy as np

class PlotsTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        import matplotlib.pyplot as plt

    def result_file(self, fname):
        if not os.path.isdir(os.path.join(TestManager.test_dir, 'test_results')):
            os.mkdir(os.path.join(TestManager.test_dir, 'test_results'))
        return os.path.join(TestManager.test_dir, 'test_results', fname)

    @validationTest
    def test_ColorPalettes(self):
        rgb_code = np.array([255, 255, 255])
        conv = ColorPalette.color_convert(rgb_code, 'rgb', 'hsl')
        inv = ColorPalette.color_convert(conv, 'hsl', 'rgb')
        self.assertTrue(np.allclose(inv, rgb_code))
        rgb_code = [200, 10, 25]
        for space in ['rgb', 'hsv', 'hsl', 'xyz', 'lab']:
            conv = ColorPalette.color_convert(rgb_code, 'rgb', space)
            inv = ColorPalette.color_convert(conv, space, 'rgb')
            self.assertTrue(np.allclose(inv, rgb_code))
        rgb_codes = np.array([[0, 0, 0], [255, 255, 255]]).T
        for space in ['rgb', 'hsv', 'hsl', 'xyz', 'lab']:
            conv = ColorPalette.color_convert(rgb_codes, 'rgb', space)
            inv = ColorPalette.color_convert(conv, space, 'rgb')
            self.assertTrue(np.allclose(inv, rgb_codes), msg=f'bad conversion for {space}: {rgb_codes}, {inv}')
        rgb_codes = np.random.rand(3, 10, 50) * 255
        for space in ['rgb', 'hsv', 'hsl', 'xyz', 'lab']:
            conv = ColorPalette.color_convert(rgb_codes, 'rgb', space)
            inv = ColorPalette.color_convert(conv, space, 'rgb')
            self.assertTrue(np.allclose(inv, rgb_codes))
        rgb_codes = np.ones((3, 1000, 500)) * 255
        for space in ['rgb', 'hsv', 'hsl', 'xyz', 'lab']:
            conv = ColorPalette.color_convert(rgb_codes, 'rgb', space)
            inv = ColorPalette.color_convert(conv, space, 'rgb')
            self.assertTrue(np.allclose(inv, rgb_codes))
        print(ColorPalette('pastel').blend(0.2))
        grid = np.linspace(0, 2 * np.pi, 200)
        palette_base = ['#3a2652', '#dcca00', '#a15547', '#009b5d', '#14013d', '#8d0001', '#494947']
        lighter_palette = [ColorPalette.color_lighten(c, 0.2, shift=True) for c in palette_base]
        lighter_palette_hsl = [ColorPalette.color_lighten(c, 0.2, modification_space='hsl', shift=True) for c in palette_base]
        for n, p in {'starters': 'starters', 'base': palette_base, 'lighter': lighter_palette, 'lighter_hsl': lighter_palette_hsl}.items():
            base_fig = None
            print(ColorPalette(p).get_colorblindness_test_url())
            for i in range(6):
                base_fig = Plot(grid, i + np.sin((i + 1) * grid), figure=base_fig, style_list={'color': ColorPalette(p)}, plot_label=n)
