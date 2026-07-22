"""Extracted from CombinatoricsTests.test_BigStateGraph via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_BigStateGraph"""

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
    def test_BigStateGraph(self):
        ndim = 39
        gen = SymmetricGroupGenerator(ndim)
        state = self.StateMaker(ndim)
        rules = [[state(*x) for x in s] for s in [[[[39, 1]], [[38, 1]]], [[[38, 1]], [[37, 1]]], [[[38, 1]], [[36, 1]]], [[[37, 1]], [[36, 1]]], [[[37, 1]], [[35, 1]]], [[[37, 1]], [[34, 1]]], [[[36, 1]], [[35, 1]]], [[[36, 1]], [[34, 1]]], [[[36, 1]], [[33, 1]]], [[[35, 1]], [[34, 1]]], [[[34, 1]], [[33, 1]]], [[[33, 1]], [[32, 1]]], [[[33, 1]], [[31, 1]]], [[[32, 1]], [[31, 1]]], [[[32, 1]], [[30, 1]]], [[[31, 1]], [[30, 1]]], [[[31, 1]], [[29, 1]]], [[[30, 1]], [[29, 1]]], [[[29, 1]], [[28, 1]]], [[[27, 1]], [[26, 1]]], [[[26, 1]], [[25, 1]]], [[[26, 1]], [[24, 1]]], [[[25, 1]], [[24, 1]]], [[[25, 1]], [[23, 1]]], [[[25, 1]], [[22, 1]]], [[[24, 1]], [[23, 1]]], [[[24, 1]], [[22, 1]]], [[[23, 1]], [[22, 1]]], [[[23, 1]], [[21, 1]]], [[[22, 1]], [[21, 1]]], [[[20, 1]], [[23, 1], [37, 1]]], [[[19, 1]], [[27, 1], [29, 1]]], [[[19, 1]], [[20, 1], [39, 1]]], [[[19, 1]], [[18, 1]]], [[[15, 1]], [[25, 1], [29, 1]]], [[[15, 1]], [[14, 1]]], [[[14, 1]], [[13, 1]]], [[[14, 1]], [[11, 1]]], [[[14, 1]], [[10, 1]]], [[[13, 1]], [[22, 1], [29, 1]]], [[[13, 1]], [[21, 1], [30, 1]]], [[[13, 1]], [[19, 1], [37, 1]]], [[[12, 1]], [[18, 1], [37, 1]]], [[[10, 1]], [[20, 1], [32, 1]]], [[[10, 1]], [[19, 1], [36, 1]]], [[[9, 1]], [[11, 1], [13, 1]]], [[[9, 1]], [[10, 1], [12, 1]]], [[[9, 1]], [[7, 1]]], [[[9, 1]], [[6, 1]]], [[[9, 1]], [[5, 1]]], [[[9, 1]], [[4, 1]]], [[[8, 1]], [[11, 2]]], [[[8, 1]], [[10, 2]]], [[[8, 1]], [[7, 1]]], [[[8, 1]], [[5, 1]]], [[[8, 1]], [[4, 1]]], [[[7, 1]], [[5, 1]]], [[[6, 1]], [[5, 1]]], [[[6, 1]], [[3, 1]]], [[[4, 1]], [[3, 1]]]]]
        part_perms = gen.get_terms([1, 2])
        graph = PermutationRelationGraph(rules)
        with np.printoptions(linewidth=10000000):
            new = graph.build_state_graph(part_perms[:100], max_iterations=1, raise_iteration_error=False)
            raise Exception([len(n) for n in new], sum([len(n) for n in new]))
