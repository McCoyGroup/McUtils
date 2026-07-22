"""Extracted from PlotsTests.test_ListTriContourPlot via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_ListTriContourPlot"""

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
    def test_ListTriContourPlot(self):
        pts = np.pi * np.random.rand(150, 2)
        sins = np.sin(pts[:, 0])
        coses = np.cos(pts[:, 1])
        ptss = np.concatenate((pts, np.reshape(sins * coses, sins.shape + (1,))), axis=1)
        plot = ListTriContourPlot(ptss)
        plot.add_colorbar()
        plot.savefig(self.result_file('test_ListTriContourPlot.png'))
        plot.close()
