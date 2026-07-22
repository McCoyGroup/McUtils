"""Extracted from PlotsTests.test_SVGBackend3D via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest PlotsTests.test_SVGBackend3D"""

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

    @debugTest
    def test_SVGBackend3D(self):
        fig = Graphics3D(backend='svg3D', image_size=[500, 500], padding=0, plot_range=[[-100, 100], [-100, 100], [-100, 100]], background='gray', view_settings={'view_vector': [0, 0, 1], 'up_vector': [0, 1, 0]})
        Path([['M', [0, 0]], ['L', [100, 100]], ['Q', [100, 0, 0, 0]], ['l', [100, 0, 0, 100]]], stroke='green', fill='none', rotation=np.pi / 6, normal=[0, 1, 1]).plot(fig)
        fig.show()
