"""Extracted from CombinatoricsTests.test_YoungTableaux via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_YoungTableaux"""

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
    def test_YoungTableaux(self):
        perm_inds, perms = UniquePermutations([2, 2, 1, 1]).permutations(return_indices=True)
        print(np.concatenate([np.array([np.min(perm_inds[:, :2], axis=1), np.min(perm_inds[:, 2:], axis=1)]).T, perms], axis=1))
        return
        print(nca_partition_terms((2, 2)))
        return
        comb.UniquePermutations([0, 0, 1, 1]).permutations(position_blocks=[0])

        def populate_sst_frame_from_components(frame_shape, offsets, sub_ssts):
            frame = np.zeros(frame_shape, dtype=int)
            for i, (o, ss) in enumerate(zip(offsets, sub_ssts)):
                n = len(ss)
                frame[o:o + n] = ss
            return frame

        def validate_frame(frame):
            if np.any(np.diff([f[0] for f in frame]) < 0):
                return False
        yt = comb.YoungTableauxGenerator(6)
        p = [3, 2, 1]
        tabs = yt.get_standard_tableaux(partitions=[p])[0]
        print(len(tabs[0]))
        for t in zip(*tabs):
            print('-' * 10)
            for s in t:
                print(s)
        print('=' * 20)
        bf_tabs = yt.get_standard_tableaux(partitions=[p], brute_force=True)[0]
        print(len(bf_tabs[0]))
        for t in zip(*bf_tabs):
            print('-' * 10)
            for s in t:
                print(s)
