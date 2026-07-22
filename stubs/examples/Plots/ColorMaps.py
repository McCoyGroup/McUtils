"""Extracted from PlotsTests.test_ColorMaps via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_ColorMaps"""

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
    def test_ColorMaps(self):
        print(ColorPalette('pastel').blend([0, 0.2, 0.5, 1.1]))
        print(ColorPalette('pastel')([0, 0.2, 0.5, 1.1]))
        grid_x = np.linspace(0, 2 * np.pi, 100)
        grid_y = np.linspace(0, 2 * np.pi, 100)
        mg = np.meshgrid(grid_x, grid_y)
        grid_z = np.sum(np.meshgrid(np.sin(grid_x), np.cos(grid_y)), axis=0)
        ContourPlot(*mg, grid_z, cmap=ColorPalette('starters').as_colormap(levels=np.linspace(0, 1, 20) ** 2, cmap_type='interpolated'), levels=50, colorbar=True).show()
