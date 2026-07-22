"""Extracted from PlotsTests.test_PlotStyling via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_PlotStyling"""

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
    def test_PlotStyling(self):
        grid = np.linspace(0, 2 * np.pi, 100)
        plot = Plot(grid, np.sin(grid), aspect_ratio=1.3, theme='dark_background', ticks_style={'color': 'red', 'labelcolor': 'red'}, plot_label='bleh', padding=((30, 0), (20, 20)))
        plot.show()
        plot.close()
