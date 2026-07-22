"""Extracted from CombinatoricsTests.test_DirectSumExtra via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_DirectSumExtra"""

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
    def test_DirectSumExtra(self):
        """
        Tests the features of the symmetric group generator
        :return:
        :rtype:
        """
        gen = SymmetricGroupGenerator(6)
        test_inds = [200, 758, 203, 204, 780, 769, 781, 770, 779, 779, 782]
        p = gen.from_indices(test_inds)
        self.assertEquals(gen.to_indices(p).tolist(), test_inds)
        test_inds = [200, 758, 203, 204, 780, 769, 781, 770, 779, 779, 782, 904, 904, 911, 901, 901, 915, 914, 2808, 789, 796, 794, 797, 795, 798, 895, 896, 2844, 2824, 2825, 897, 2828, 2838, 2906, 2835, 2839, 2913, 2907, 2833, 2836, 2918, 2914, 2840, 2908, 2877, 2834, 2837, 2919, 2915, 2909, 2990, 199, 757, 202, 766, 768, 768, 777, 777, 903, 903, 912, 2807, 788, 791, 793, 894, 2843, 2823, 2827, 2830, 2875, 2832, 2991, 197, 755, 745, 761, 764, 906, 906, 909, 198, 756, 201, 771, 746, 765, 774, 774, 767, 767, 776, 776, 902, 902, 913, 898, 898, 917, 787, 790, 792, 893, 2826, 2829, 2831, 196, 754, 744, 760, 763, 905, 905, 910, 195, 753, 743, 759, 762, 907, 908]
        p = gen.from_indices(test_inds)
        self.assertEquals(gen.to_indices(p).tolist(), test_inds)
        basic_exc, _ = gen.take_permutation_rule_direct_sum([[1, 0, 0, 0, 0, 2], [2, 0, 0, 4, 0, 0]], [(-1,), (1,)], return_indices=True, split_results=True)
        test_states = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 1, 0, 1, 0], [3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 3], [1, 2, 0, 0, 0, 0], [1, 0, 2, 0, 0, 0], [1, 0, 0, 2, 0, 0], [1, 0, 0, 0, 2, 0], [1, 0, 0, 0, 0, 2], [2, 1, 0, 0, 0, 0], [2, 2, 1, 1, 0, 0], [2, 2, 1, 0, 1, 0], [2, 2, 1, 0, 0, 1], [0, 0, 1, 1, 1, 1]]
        test_rules = [(-1,), (1,)]
        filter_perms = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0]]
        filter_inds = gen.to_indices(filter_perms)
        wat = gen.from_indices(filter_inds)
        self.assertEquals(wat.tolist(), filter_perms)
        subtest = np.array(test_states)
        test_perms, test_inds = gen.take_permutation_rule_direct_sum(subtest, test_rules, return_indices=True, split_results=True)
        bleh = np.concatenate([UniquePermutations(x + (0,) * (6 - len(x))).permutations() for x in test_rules], axis=0)
        full_perms = subtest[:, np.newaxis, :] + bleh[np.newaxis, :, :]
        nonneg_perms = []
        for f in full_perms:
            neg_pos = np.where(f < 0)[0]
            comp = np.setdiff1d(np.arange(len(f)), neg_pos)
            f = f[comp,]
            nonneg_perms.append(f)
        for i in range(len(test_states)):
            self.assertEquals(list(sorted(test_perms[i].tolist())), list(sorted(nonneg_perms[i].tolist())), msg='bad for {}'.format(test_states[i]))
        bleeeh, _, filter = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True, split_results=True, filter_perms=[filter_perms, filter_inds], return_filter=True)
        self.assertEquals(len(bleeeh), len(test_states))
        for i in range(len(test_states)):
            woof = list(test_states[i])
            woof[0] += 1
            if woof in filter_perms:
                self.assertIn(woof, bleeeh[i].tolist())
            else:
                self.assertNotIn(woof, bleeeh[i].tolist())
        nonneg_perms = []
        for f in full_perms:
            neg_pos = np.where(f < 0)[0]
            comp = np.setdiff1d(np.arange(len(f)), neg_pos)
            f = f[comp,]
            cont_terms, _, _ = nput.contained(f, filter_perms)
            nonneg_perms.append(f[cont_terms,])
        for i in range(len(test_states)):
            self.assertEquals(list(sorted(bleeeh[i].tolist())), list(sorted(nonneg_perms[i].tolist())), msg='bad for {}'.format(test_states[i]))
        bleeeh2, _, filter = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True, split_results=True, filter_perms=filter_perms, return_filter=True)
        self.assertEquals(filter.inds.tolist(), np.sort(filter_inds).tolist())
        self.assertEquals(filter.perms.tolist(), filter_perms)
        self.assertEquals([b.tolist() for b in bleeeh2], [b.tolist() for b in bleeeh])
        bleeeh, _, filter = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True, split_results=True, filter_perms=filter_inds, return_filter=True)
        self.assertEquals(filter.inds.tolist(), np.sort(filter_inds).tolist())
        for i in range(len(test_states)):
            self.assertEquals(bleeeh2[i].tolist(), bleeeh[i].tolist(), msg='failed for state {}'.format(test_states[i]))
        test_states = [[1, 1, 0, 0, 1, 1], [1, 3, 0, 0, 1, 1], [1, 0, 1, 0, 1, 1], [1, 0, 0, 1, 1, 1], [1, 0, 0, 3, 1, 1], [1, 1, 0, 0, 3, 1], [1, 0, 0, 1, 3, 1], [1, 1, 0, 0, 1, 3], [1, 0, 1, 0, 1, 3], [1, 0, 1, 0, 1, 0], [1, 0, 0, 1, 1, 3], [1, 1, 2, 0, 1, 1], [1, 1, 2, 0, 1, 1], [1, 1, 0, 2, 1, 1], [1, 2, 0, 1, 1, 1], [1, 2, 0, 1, 1, 1], [1, 0, 1, 2, 1, 1], [1, 0, 2, 1, 1, 1], [3, 1, 2, 0, 1, 1], [0, 1, 3, 0, 1, 1]]
        filter_inds = [0, 6, 5, 4, 3, 2, 1, 12, 11, 10, 9, 8, 7, 27, 26, 24, 21, 17, 25, 23]
        bleeeh, bleeh_inds, filter = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True, split_results=True, filter_perms=filter_inds, return_filter=True)
        self.assertEquals(filter.inds.tolist(), np.sort(filter_inds).tolist())
        for i in range(len(test_states)):
            self.assertEquals(gen.to_indices(bleeeh[i]).tolist(), bleeh_inds[i].tolist(), msg='failed for state {}'.format(test_states[i]))
            conts = nput.contained(bleeh_inds[i], filter.inds, invert=True)[0]
            self.assertFalse(conts.any(), msg='failed for state {}: (failed with {}/{})'.format(test_states[i], bleeeh[i][conts], bleeh_inds[i][conts]))
