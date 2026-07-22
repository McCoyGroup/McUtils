"""Extracted from PlotsTests.test_SVGBackend2D via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_SVGBackend2D"""

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
    def test_SVGBackend2D(self):
        fig = Graphics(backend='svg')
        Rectangle([[0, 0], [100, 100]], fill='red', transform=[['rotate', [30]]]).plot(fig)
        Rectangle([[100, 100], [200, 200]], fill='blue').plot(fig)
        fig.show()
