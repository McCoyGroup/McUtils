"""Extracted from PlotsTests.test_Animation via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_Animation"""

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

    @inactiveTest
    def test_Animation(self):
        """Currently broken"""

        def get_data(*args):
            pts = np.pi * np.random.normal(scale=0.25, size=(10550, 2))
            sins = np.sin(pts[:, 0])
            coses = np.cos(pts[:, 1])
            ptss = np.concatenate((pts, np.reshape(sins * coses, sins.shape + (1,))), axis=1)
            return (ptss,)
        plot = ListTriContourPlot(*get_data(), animate=get_data, plot_range=[[-np.pi, np.pi], [-np.pi, np.pi]])
        plot.show()
        plot.savefig(self.result_file('test_ListTriContourPlot.gif'))
        plot.close()
