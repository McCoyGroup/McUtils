"""Extracted from CombinatoricsTests.test_DirectSumIndicesLarge via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_DirectSumIndicesLarge"""

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
    def test_DirectSumIndicesLarge(self):
        """
        Tests the features of the symmetric group generator
        at scale
        :return:
        :rtype:
        """
        gen = SymmetricGroupGenerator(45)
        test_states = [[0] * 3 + [1] * 2 + [0] * 40, [0] * 4 + [1] * 2 + [0] * 39, [0] * 5 + [1] * 2 + [0] * 38, [0] * 5 + [2] * 2 + [0] * 38, [0] * 5 + [3] * 2 + [0] * 38, [0] * 4 + [2] * 2 + [0] * 39]
        test_rules = [[1, 1], [1, -1], [-1, -1]]
        with BlockProfiler('direct inds', print_res=True):
            test_perms, test_inds = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True, indexing_method='direct', split_results=True, preserve_ordering=False)
