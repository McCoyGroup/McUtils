"""Extracted from PlotsTests.test_PlotGridStyling via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_PlotGridStyling"""

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
    def test_PlotGridStyling(self):
        main = GraphicsGrid(ncols=3, nrows=1, theme='Solarize_Light2', figure_label='my beuatufil triptych', padding=((50, 10), (50, 65)), spacings=[50, 0])
        grid = np.linspace(0, 2 * np.pi, 100)
        grid_2D = np.meshgrid(grid, grid)
        x = grid_2D[1]
        y = grid_2D[0]
        main[0, 0] = ContourPlot(x, y, np.sin(y), plot_label='$sin(x)$', axes_labels=[None, 'cats (cc)'], figure=main[0, 0])
        main[0, 1] = ContourPlot(x, y, np.sin(x) * np.cos(y), plot_label='$sin(x)cos(y)$', axes_labels=[Styled('dogs (arb.)', {'color': 'red'}), None], figure=main[0, 1])
        main[0, 2] = ContourPlot(x, y, np.cos(y), plot_label='$cos(y)$', figure=main[0, 2])
        main.colorbar = {'graphics': main[0, 1].graphics}
        main.show()
        main.close()
