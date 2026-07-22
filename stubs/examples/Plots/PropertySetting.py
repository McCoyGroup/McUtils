"""Extracted from PlotsTests.test_PropertySetting via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_PropertySetting"""

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
    def test_PropertySetting(self):
        StickPlot(np.linspace(0, 2 * np.pi, 35), np.sin(np.linspace(0, 2 * np.pi, 35)), color='red', label='spec_1', plot_legend=True).show()
