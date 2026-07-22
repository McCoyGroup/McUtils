"""Extracted from PlotsTests.test_Plot3D via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_Plot3D"""

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
    def test_Plot3D(self):
        import matplotlib.cm as colormaps
        f = lambda pt: np.sin(pt[0]) + np.cos(pt[1])
        plot = Plot3D(f, np.arange(0, 2 * np.pi, 0.1), np.arange(0, 2 * np.pi, 0.1), plot_style={'cmap': colormaps.get_cmap('viridis')}, axes_labels=['dogs', 'cats', Styled('rats', color='red')], plot_label='my super cool 3D plot', plot_range=[(-5, 5)] * 3, plot_legend='i lik turtle', colorbar=True)
        plot.savefig(self.result_file('test_Plot3D.png'))
        plot.close()
