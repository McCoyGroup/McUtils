"""Extracted from NumputilsTests.test_Bezier via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_Bezier"""

import collections
import itertools
import math
import os.path
from Peeves.TestUtils import *
from Peeves import BlockProfiler
import McUtils.Numputils as nput
from McUtils.Numputils import *
from McUtils.Zachary import FiniteDifferenceDerivative
from unittest import TestCase
import numpy as np, scipy, functools as ft

class NumputilsTests(TestCase):
    problem_coords = np.array([[-1.86403557e-17, -0.076046524, 0.0462443228], [6.70904773e-17, -0.076046524, -0.953755677], [0.929682337, 0.292315732, 0.0462443228], [2.46519033e-32, -1.38777878e-17, 0.225076602], [-1.97215226e-31, 1.4371441, -0.90030641], [-1.75999392e-16, -1.4371441, -0.90030641]])

    @classmethod
    def setUp(self):
        np.set_printoptions(linewidth=100000000.0)

    @validationTest
    def test_Bezier(self):
        import McUtils.Plots as plt
        knots = np.array([[0, 0], [0.1, 1], [0.5, 2], [0.8, 0], [1, 0], [1.2, 0], [2, 2]])
        n = 5
        points, t = nput.bezier_eval(knots, n, max_arc_len=0.05, return_points=True)
        ders = nput.bezier_eval(knots, t, order=1)
        points0 = nput.bezier_eval(knots, n, return_points=False)
        fig = plt.Plot(*points.T, plot_range=[[0, 2], [0, 2]], padding=[[0, 0], [0, 0]], image_size=500, aspect_ratio=1)
        plt.ScatterPlot(*points.T, color=plt.prep_color(palette='WarioColors', blending=vec_rescale(bezier_curvature(knots, t))), figure=fig)
        fig.show()
