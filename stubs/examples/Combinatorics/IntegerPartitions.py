"""Extracted from CombinatoricsTests.test_IntegerPartitions via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest CombinatoricsTests.test_IntegerPartitions"""

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
    def test_IntegerPartitions(self):
        """
        Tests integer partitioning algs
        """
        num_parts = IntegerPartitioner.count_partitions(3)
        self.assertEquals(num_parts, 3)
        n = np.array([3])
        M = n
        l = n
        num_parts = IntegerPartitioner.count_partitions(n, M, l)
        self.assertEquals(num_parts, [3])
        n = np.array([3, 5, 2, 6])
        M = np.array([1, 3, 1, 2])
        l = np.array([3, 3, 3, 3])
        num_parts = IntegerPartitioner.count_partitions(n, M, l)
        self.assertEquals(num_parts.tolist(), [1, 3, 1, 1])
        n = np.array([3, 5, 2, 6, 10, 10])
        M = np.array([1, 3, 1, 2, 10, 5])
        l = np.array([3, 3, 3, 3, 3, 3])
        num_parts = IntegerPartitioner.count_partitions(n, M, l)
        self.assertEquals(num_parts.tolist(), [1, 3, 1, 1, 14, 5])
        num_greater = IntegerPartitioner.count_exact_length_partitions_in_range(4, 4, 2, 2)
        len2_4s = IntegerPartitioner.partitions(4, max_len=2)[1]
        raw_counts = len([x for x in len2_4s if len(x) == 2 and x[0] > 2])
        self.assertEquals(num_greater, raw_counts)
        parts = IntegerPartitioner.partitions(3)
        self.assertEquals([p.tolist() for p in parts], [[[3]], [[2, 1]], [[1, 1, 1]]])
        parts = IntegerPartitioner.partitions(3, pad=True)
        self.assertEquals(parts.tolist(), [[3, 0, 0], [2, 1, 0], [1, 1, 1]])
        parts = IntegerPartitioner.partitions(3, pad=True, max_len=2)
        self.assertEquals(parts.tolist(), [[3, 0], [2, 1]])
        num_parts = IntegerPartitioner.count_partitions(10)
        self.assertEquals(num_parts, 42)
        parts = IntegerPartitioner.partitions(5)
        self.assertEquals([p.tolist() for p in parts], [[[5]], [[4, 1], [3, 2]], [[3, 1, 1], [2, 2, 1]], [[2, 1, 1, 1]], [[1, 1, 1, 1, 1]]])
        parts = IntegerPartitioner.partitions(10, pad=True, max_len=2)
        self.assertEquals(parts.tolist(), [[10, 0], [9, 1], [8, 2], [7, 3], [6, 4], [5, 5]])
        self.assertEquals(IntegerPartitioner.partition_indices([[10, 0], [9, 1], [8, 2], [7, 3], [6, 4], [5, 5]]).tolist(), list(range(6)))
        np.random.seed(0)
        full_stuff = IntegerPartitioner.partitions(10, pad=True, max_len=3)
        inds = np.random.choice(len(full_stuff), 5, replace=False)
        test_parts = full_stuff[inds]
        test_inds = IntegerPartitioner.partition_indices(test_parts)
        self.assertEquals(test_inds.tolist(), inds.tolist(), msg='{} should have indices {} but got {}'.format(test_parts, inds, test_inds))
        np.random.seed(1)
        full_stuff = IntegerPartitioner.partitions(10, pad=True, max_len=7)
        inds = np.random.choice(len(full_stuff), 35, replace=False)
        test_parts = full_stuff[inds]
        test_inds = IntegerPartitioner.partition_indices(test_parts)
        self.assertEquals(test_inds.tolist(), inds.tolist(), msg='{} should have indices {} but got {}'.format(test_parts, inds, test_inds))
        test_inds = IntegerPartitioner.partition_indices(test_parts, check=False)
        self.assertEquals(test_inds.tolist(), inds.tolist(), msg='{} should have indices {} but got {}'.format(test_parts, inds, test_inds))
