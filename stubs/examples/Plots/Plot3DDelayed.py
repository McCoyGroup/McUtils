"""Extracted from PlotsTests.test_Plot3DDelayed via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_Plot3DDelayed"""

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
    def test_Plot3DDelayed(self):
        p = Plot3D(background='black')
        for i, c in enumerate(('red', 'white', 'blue')):
            p.plot(lambda g: np.sin(g.T[0]) + np.cos(g.T[1]), [-2 + 4 / 3 * i, -2 + 4 / 3 * (i + 1)], [-2 + 4 / 3 * i, -2 + 4 / 3 * (i + 1)], color=c)
        p.savefig(self.result_file('test_Plot3DDelayed.gif'))
        p.close()
