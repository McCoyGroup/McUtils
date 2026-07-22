"""Extracted from CombinatoricsTests.test_FullBasis via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_FullBasis"""

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
    def test_FullBasis(self):
        full_basis = CompleteSymmetricGroupSpace(12)
        self.assertEquals(tuple(full_basis[0]), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEquals(tuple(full_basis[555]), (0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0))
        self.assertEquals(full_basis.find([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0]), 555)
        self.assertEquals(full_basis.find([[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0]]).tolist(), [556, 555])
        full_basis.load_to_sum(11)
        why = np.random.choice(full_basis._basis.shape[0], size=100000)
        ms = np.max(why)
        with BlockProfiler(inactive=True, mode='deterministic'):
            for i in range(100):
                full_basis.take(why, max_size=ms)
        self.assertEquals(full_basis._basis.shape[0], 5200300)
        self.assertEquals(full_basis.find([10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 293930)
