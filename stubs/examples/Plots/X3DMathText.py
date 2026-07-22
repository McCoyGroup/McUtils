"""Extracted from PlotsTests.test_X3DMathText via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_X3DMathText"""

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
    def test_X3DMathText(self):
        fig = Graphics3D(backend='x3d', view_settings={'view_distance': 5})
        Text('$\\sqrt{5}$', [1, 0, 0], color='red', billboard=False).plot(fig)
        fig.show()
