"""Extracted from CombinatoricsTests.test_StateGraph via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_StateGraph"""

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
    def test_StateGraph(self):
        ndim = 6
        full_basis = CompleteSymmetricGroupSpace(ndim)
        np.random.seed(0)
        inds = np.random.random_integers(0, 1000, 10)
        sample_space = full_basis.take(inds)
        state = self.StateMaker(ndim)
        g = PermutationRelationGraph([[state([1, 1]), state([2, 2])], [state([3, 1]), state([4, 1])]])
        graph = g.build_state_graph([state([1, 1])])
        self.assertEquals(graph[0].tolist(), [state([1, 1]), state([2, 2])])
        graph = g.build_state_graph([state([1, 2])])
        self.assertEquals(graph[0].tolist(), [state([1, 2]), state([2, 2], [1, 1]), state([2, 4])])
        graph = g.build_state_graph([state([1, 1]), state([1, 2])])
        self.assertEquals([g.tolist() for g in graph], [[state([1, 1]), state([2, 2])], [state([1, 2]), state([2, 2], [1, 1]), state([2, 4])]])
        graph = g.build_state_graph([state([1, 2]), state([5, 2])])
        self.assertEquals([g.tolist() for g in graph], [[state([1, 2]), state([2, 2], [1, 1]), state([2, 4])], [state([5, 2])]])
        graph = g.build_state_graph(sample_space, max_iterations=10)
