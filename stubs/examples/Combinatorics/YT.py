"""Extracted from CombinatoricsTests.test_YT via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_YT"""

import math
from Peeves.TestUtils import *
from Peeves import BlockProfiler, Timer
from unittest import TestCase
from McUtils.Combinatorics import *
import McUtils.Numputils as nput
import McUtils.Formatters as mfmt
from McUtils.Scaffolding import Logger
import sys, os, numpy as np, itertools

class CombinatoricsTests(TestCase):

    def setUp(self):
        import warnings
        np.seterr(all='raise')
        warnings.filterwarnings('error', category=np.VisibleDeprecationWarning)
        np.set_printoptions(linewidth=100000000.0)

    class StateMaker:
        """
        A tiny but useful class to make states based on their quanta
        of excitation
        """

        def __init__(self, ndim, mode='low-high'):
            self.ndim = ndim
            self.mode = mode

        def make_state(self, *specs, mode=None):
            if mode is None:
                mode = self.mode
            state = [0] * self.ndim
            for s in specs:
                if isinstance(s, (int, np.integer)):
                    i = s
                    q = 1
                else:
                    i, q = s
                if mode == 'low-high':
                    state[-i] = q
                elif mode == 'high-low':
                    state[i - 1] = q
                elif mode == 'normal':
                    state[i] = q
                else:
                    raise ValueError("don't know what to do with filling mode '{}'".format(mode))
            return state

        def __call__(self, *specs, mode=None):
            return self.make_state(*specs, mode=mode)

    @validationTest
    def test_YT(self):
        for i in range(1, 11):
            gen = YoungTableauxGenerator(i)
            n = gen.number_of_tableaux()
            print('>>>', n)
            tabs = gen.get_standard_tableaux(brute_force=False)
            l1 = [len(t[0]) for t in tabs]
            self.assertEquals(n, sum(l1))
        for i in range(1, 9):
            gen = YoungTableauxGenerator(i)
            n = gen.number_of_tableaux()
            print('>>>', n)
            tabs = gen.get_standard_tableaux(brute_force=False)
            tabs_bf = gen.get_standard_tableaux(brute_force=True)
            l2 = [len(t[0]) for t in tabs_bf]
            self.assertEquals(n, sum(l2))
            l1 = [len(t[0]) for t in tabs]
            self.assertEquals(l1, l2)
