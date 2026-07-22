"""Extracted from CombinatoricsTests.test_SelRules via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_SelRules"""

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
    def test_SelRules(self):
        base_paths = LatticePathGenerator.generate_tree([[-1, 1], [-1, 1]], track_positions=False)[-1]
        self.assertEquals(base_paths, [(), (-2,), (2,), (-1, -1), (1, -1), (1, 1)])
        gen = LatticePathGenerator([-1, 1], [-1, 1])
        self.assertEquals(gen.tree[0][0], (0, 0))
        self.assertEquals(gen.tree[0][1], [(-2,), (-1, -1)])
        self.assertEquals(gen.tree[1][0], (0, 1))
        self.assertEquals(gen.tree[1][1], [(), (1, -1)])
        gen = LatticePathGenerator([-1, 1], [])
        self.assertEquals(gen.tree[0][0], (0,))
        self.assertEquals(gen.tree[0][1], [(-1,)])
        gen = LatticePathGenerator([-1, 1], [-1, 1, 2])
        self.assertEquals(gen.tree[0][0], (0, 0))
        self.assertEquals(gen.tree[0][1], [(-2,), (-1, -1)])
        self.assertEquals(gen.tree[1][0], (0, 1))
        self.assertEquals(gen.tree[1][1], [(), (1, -1)])
        self.assertEquals(gen.tree[2][0], (0, 2))
        self.assertEquals(gen.tree[2][1], [(1,), (2, -1)])
        self.assertEquals(gen.find_paths(()), [(0, 1), (1, 0)])
        self.assertEquals(gen.find_paths(()), [(0, 1), (1, 0)])
        self.assertEquals(gen.get_path((0, 1)), [(), (1, -1)])
        del gen
        subgen = LatticePathGenerator([-1, 1], [-1, 1])
        gen2 = LatticePathGenerator(subgen.subrules[2], subgen.subrules[1])
        self.assertEquals(gen2.tree[0][0], (0, 0))
        self.assertEquals(gen2.tree[0][1], [(-1,)])
        self.assertEquals(gen2.tree[4][0], (2, 0))
        self.assertEquals(gen2.tree[4][1], [(1,), (2, -1)])
        self.assertEquals(gen2.tree[6][0], (3, 0))
        self.assertEquals(gen2.tree[6][1], [(-2, -1), (-1, -1, -1)])
        self.assertEquals(gen2.steps[0][3], (-1, -1))
        self.assertEquals(gen2.steps[1][0], (-1,))
