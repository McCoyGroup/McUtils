"""Extracted from CombinatoricsTests.test_SymmetricGroupGenerator via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_SymmetricGroupGenerator"""

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
    def test_SymmetricGroupGenerator(self):
        """
        Tests the features of the symmetric group generator
        :return:
        :rtype:
        """
        gen = SymmetricGroupGenerator(8)
        part_perms = gen.get_terms([1, 2, 3, 4, 5])
        inds = gen.to_indices(part_perms)
        self.assertEquals(inds[:100,].tolist(), list(range(1, 101)))
        np.random.seed(0)
        subinds = np.random.choice(len(inds), 250, replace=False)
        self.assertEquals(inds[subinds,].tolist(), (1 + subinds).tolist())
        np.random.seed(0)
        subinds = np.random.choice(len(inds), 250, replace=False)
        test_perms = gen.from_indices(1 + subinds)
        self.assertEquals(part_perms[subinds,].tolist(), test_perms.tolist())
        test_states = np.array([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [2, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 2, 0], [0, 1, 1, 0, 0, 0, 2, 0], [0, 0, 0, 0, 2, 0, 2, 0], [0, 0, 0, 0, 2, 0, 0, 2], [1, 0, 0, 0, 0, 0, 0, 2]])
        test_rules = [[2], [1, 1]]
        test_perms, test_inds = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True)
        sums = np.sum(test_perms, axis=1)
        test_sums = np.unique(np.unique(np.sum(test_states, axis=1))[np.newaxis] + np.unique([sum(x) for x in test_rules])[:, np.newaxis])
        self.assertEquals(np.unique(sums).tolist(), test_sums.tolist())
        bleh = np.concatenate([UniquePermutations(x + [0] * (8 - len(x))).permutations() for x in test_rules], axis=0)
        full_perms = test_states[:, np.newaxis, :] + bleh[np.newaxis, :, :]
        full_perms = full_perms.reshape((-1, full_perms.shape[-1]))
        self.assertEquals(len(test_perms), len(full_perms))
        self.assertEquals(sorted(test_perms.tolist()), sorted(full_perms.tolist()))
        full_inds = gen.to_indices(full_perms)
        self.assertEquals(np.sort(test_inds).tolist(), np.sort(full_inds).tolist())
        test_rules = [[2], [-2], [-3], [1, 1], [-1, -1], [-1, 1], [-1, -1, 1]]
        test_perms, test_inds = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True)
        bleh = np.concatenate([UniquePermutations(x + [0] * (8 - len(x))).permutations() for x in test_rules], axis=0)
        full_full_perms = test_states[:, np.newaxis, :] + bleh[np.newaxis, :, :]
        full_perms = full_full_perms.reshape((-1, full_perms.shape[-1]))
        negs = np.where(full_perms < 0)[0]
        comp = np.setdiff1d(np.arange(len(full_perms)), negs)
        full_perms = full_perms[comp,]
        self.assertEquals(len(test_perms), len(full_perms))
        self.assertEquals(sorted(test_perms.tolist()), sorted(full_perms.tolist()))
        full_inds = gen.to_indices(full_perms)
        self.assertEquals(np.sort(test_inds).tolist(), np.sort(full_inds).tolist())
        test_perms2, test_inds2 = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True)
        self.assertEquals(test_inds.tolist(), test_inds2.tolist())
        test_perms2, test_inds2 = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True, split_results=True)
        bleeep = []
        for full_perms in full_full_perms.reshape((len(test_states), -1, full_perms.shape[-1])):
            negs = np.where(full_perms < 0)[0]
            comp = np.setdiff1d(np.arange(len(full_perms)), negs)
            full_perms = full_perms[comp,]
            bleeep.append(full_perms)
        self.assertEquals(len(test_states), len(test_perms2))
        self.assertEquals(len(test_states), len(test_inds2))
        self.assertEquals([len(x) for x in test_perms2], [len(x) for x in bleeep])
        for i in range(len(test_states)):
            self.assertEquals(len(test_perms2[i]), len(test_inds2[i]), msg='failed for state {}'.format(test_states[i]))
            self.assertEquals(len(test_perms2[i]), len(bleeep[i]), msg='failed for state {}'.format(test_states[i]))
            self.assertEquals(sorted(test_perms2[i].tolist()), sorted(bleeep[i].tolist()), msg='failed for state {}'.format(test_states[i]))
            self.assertEquals(sorted(test_inds2[i].tolist()), sorted(gen.to_indices(bleeep[i]).tolist()), msg='failed for state {}'.format(test_states[i]))
