"""Extracted from CombinatoricsTests.test_UniquePartitionPermutations via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_UniquePartitionPermutations"""

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
    def test_UniquePartitionPermutations(self):
        """
        Tests the generation of unique permutations of partitions
        :return:
        :rtype:
        """
        lens, parts = IntegerPartitioner.partitions(10, pad=True, return_lens=True)
        perms = UniquePermutations(parts[0]).permutations()
        self.assertEquals(perms.tolist(), [[10, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 10, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 10, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 10, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 10, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 10, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 10, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 10, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 10, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 10]])
        test_set = [[6, 2, 1, 1, 0, 0, 0, 0, 0, 0], [6, 2, 1, 0, 1, 0, 0, 0, 0, 0], [6, 2, 1, 0, 0, 1, 0, 0, 0, 0], [6, 2, 1, 0, 0, 0, 1, 0, 0, 0], [6, 2, 1, 0, 0, 0, 0, 1, 0, 0], [6, 2, 1, 0, 0, 0, 0, 0, 1, 0], [6, 2, 1, 0, 0, 0, 0, 0, 0, 1], [6, 2, 0, 1, 1, 0, 0, 0, 0, 0], [6, 2, 0, 1, 0, 1, 0, 0, 0, 0], [6, 2, 0, 1, 0, 0, 1, 0, 0, 0]]
        perm_builder = UniquePermutations(parts[15])
        perms = perm_builder.permutations(num_perms=10)
        self.assertEquals(perms.tolist(), test_set)
        wat = UniquePermutations(parts[15]).permutations_from_indices(list(range(len(test_set))))
        self.assertEquals(wat.tolist(), test_set)
        inds = perm_builder.index_permutations(perms)
        self.assertEquals(inds.tolist(), list(range(len(inds))))
        many_perms = perm_builder.permutations(initial_permutation=perms[8])
        self.assertEquals(len(many_perms), perm_builder.num_permutations - 8)
        perms = perm_builder.permutations(initial_permutation=perms[8], num_perms=10)
        self.assertEquals(many_perms[:10].tolist(), perms.tolist())
        perm_builder = UniquePermutations([3, 1, 1, 0, 0])
        test_set = [[3, 0, 0, 1, 1], [1, 1, 3, 0, 0], [0, 3, 1, 1, 0]]
        inds = perm_builder.index_permutations(test_set)
        all_perms = perm_builder.permutations()
        all_list_perms = all_perms.tolist()
        test_inds = [all_list_perms.index(x) for x in test_set]
        self.assertEquals(inds.tolist(), test_inds)
        np.random.seed(0)
        test_inds = np.random.choice(len(all_perms), 20, replace=False)
        test_set = all_perms[test_inds,]
        sorting = np.lexsort(-np.flip(test_set, axis=1).T)[:5]
        test_set = test_set[sorting,]
        test_inds = test_inds[sorting,]
        inds = perm_builder.index_permutations(test_set)
        self.assertEquals(inds.tolist(), test_inds.tolist())
        perms = perm_builder.permutations_from_indices(inds)
        self.assertEquals(perms.tolist(), test_set.tolist())
        swaps, perms = perm_builder.permutations(return_indices=True)
        test_inds = np.random.choice(len(swaps), 10, replace=False)
        self.assertEquals([perm_builder.part[s].tolist() for s in swaps[test_inds,]], perms[test_inds,].tolist())
        perm_builder = UniquePermutations([2, 1, 1, 1, 0, 0, 0, 0])
        all_perms = perm_builder.permutations()
        test_inds = [73, 237]
        perms = perm_builder.permutations_from_indices(test_inds)
        self.assertEquals(perms.tolist(), all_perms[test_inds].tolist())
