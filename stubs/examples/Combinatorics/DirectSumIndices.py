"""Extracted from CombinatoricsTests.test_DirectSumIndices via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_DirectSumIndices"""

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
    def test_DirectSumIndices(self):
        """
        Tests the features of the symmetric group generator
        :return:
        :rtype:
        """
        gen = SymmetricGroupGenerator(1)
        test_states = [[0], [1], [2], [3], [4]]
        test_rules = [(-3,), (-1,), (1,), (3,), (-2, -1), (-2, 1), (-1, 2), (1, 2), (-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (1, 1, 1)]
        new_exc, new_inds = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True, split_results=True)
        self.assertEquals(new_exc[0].shape, (2, 1))
        test_states = gen.get_terms(range(3), flatten=True)
        test_rules = [[2], [-2], [-3], [1, 1], [-1, -1], [-1, 1], [-1, -1, 1]]
        with BlockProfiler('direct inds', print_res=False):
            test_perms, test_inds = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True, indexing_method='direct', split_results=True, preserve_ordering=False)
        blub = np.array([x for x in test_rules if len(x) == 1])
        for i in range(len(test_states)):
            why = test_states[i][np.newaxis, :] + blub
            why = why[why >= 0].reshape(-1, 1)
            self.assertEquals(test_perms[i].tolist(), why.tolist())
        gen = SymmetricGroupGenerator(10)
        test_states = gen.get_terms(range(3), flatten=True)
        test_rules = [[2], [-2], [-3], [1, 1], [-1, -1], [-1, 1], [-1, -1, 1]]
        with BlockProfiler('direct inds', print_res=False):
            test_perms, test_inds = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True, indexing_method='direct', split_results=True, preserve_ordering=False)
        with BlockProfiler('secondary inds', print_res=False):
            test_perms2, test_inds2 = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True, indexing_method='secondary', split_results=True, preserve_ordering=False)
        self.assertEquals(test_inds[0].tolist(), test_inds2[0].tolist())
        u_tests = np.unique(test_perms[1], axis=0)
        test_states = gen.get_terms(range(1), flatten=True)
        bleeeh, _, filter = gen.take_permutation_rule_direct_sum(test_states, test_rules, return_indices=True, split_results=False, filter_perms=[u_tests], return_filter=True)
        bleeeh, _ = nput.unique(bleeeh)
        contained, _, _ = nput.contained(bleeeh, u_tests, invert=True)
        self.assertFalse(contained.any(), msg='{} not in {}; {} in'.format(bleeeh[contained], u_tests, bleeeh[np.logical_not(contained)]))
        self.assertTrue(isinstance(filter.sums, np.ndarray))
