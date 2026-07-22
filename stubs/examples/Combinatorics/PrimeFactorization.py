"""Extracted from CombinatoricsTests.test_PrimeFactorization via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_PrimeFactorization"""

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
    def test_PrimeFactorization(self):
        plist = prime_list(20)
        np.random.seed(1232232)
        mod_pos = np.sort(np.random.choice(np.arange(20), (4, 3)), axis=1)
        res = np.random.randint(1, 4, size=(4, 3))
        ints = np.prod(np.array(plist)[mod_pos] ** res, axis=1, dtype=int)
        _, facs = prime_factorize(ints)
        print(ints)
        print(len(_))
        print(res)
        facs = np.array(facs).T
        sel = np.where(facs > 0)
        print(facs[sel].reshape(4, 3))
        print(mod_pos)
        print(np.array(sel).T.reshape(4, 3, 2)[:, :, 1])
        plist = prime_list(20)
        np.random.seed(1232232)
        mod_pos = np.sort(np.random.choice(np.arange(20), (100, 3)), axis=1)
        res = np.random.randint(1, 4, size=(100, 3))
        ints = np.prod(np.array(plist)[mod_pos] ** res, axis=1, dtype=int)
        print(ints)
        _, facs = prime_factorize(ints)
        return
