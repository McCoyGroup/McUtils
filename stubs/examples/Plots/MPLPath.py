"""Extracted from PlotsTests.test_MPLPath via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_MPLPath"""

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
    def test_MPLPath(self):
        fig = Graphics(backend='svg')
        Path([['M', [0, 0]], ['L', [100, 100]], ['Q', [100, 0, 0, 0]], ['l', [100, 0, 0, 100]]], stroke='pink', use_polyline=True).plot(fig)
        fig.show()
