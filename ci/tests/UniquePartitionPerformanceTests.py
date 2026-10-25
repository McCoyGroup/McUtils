"""Verify the optional UniquePartitions performance candidates independently."""
import itertools
import unittest
from unittest import mock
import numpy as np
from McUtils.Combinatorics import UniquePartitions, UniquePermutations


class UniquePartitionPerformanceTests(unittest.TestCase):
    def test_constructor_and_splitting_do_not_enumerate_permutations(self):
        with mock.patch.object(UniquePermutations, 'permutations', side_effect=AssertionError('eager enumeration')):
            builder = UniquePartitions([5, 4, 3, 2, 1, 0])
            values, = builder.partitions([2, 4], split=False)
            self.assertEqual(len(values), 15)

    def test_lazy_perms_preserves_public_values(self):
        builder = UniquePartitions([2, 1, 1, 0])
        expected = np.array(sorted(set(itertools.permutations([2, 1, 1, 0])), reverse=True))
        np.testing.assert_array_equal(builder.perms, expected)
        self.assertIs(builder.perms, builder.perms)

    def test_splits_against_index_enumeration(self):
        for values in ([5, 4, 3, 2, 1, 0], [3, 3, 2, 2, 1, 0]):
            for sizes in ([2, 1, 3], [0, 2, 0, 4], [6]):
                expected_indices = []
                boundaries = np.cumsum([0] + list(sizes))
                for assignment in itertools.permutations(range(6)):
                    if all(list(assignment[a:b]) == sorted(assignment[a:b]) for a, b in zip(boundaries[:-1], boundaries[1:])):
                        expected_indices.append(assignment)
                expected_indices = np.array(expected_indices)
                expected_values = np.asarray(values)[expected_indices]
                for take_unique in (False, True):
                    builder = UniquePartitions(values)
                    actual, indices, inverse = builder.partitions(sizes, split=False, take_unique=take_unique,
                                                                  return_indices=True, return_inverse=True)
                    with self.subTest(values=values, sizes=sizes, unique=take_unique):
                        self.assertEqual(set(map(tuple, actual)), set(map(tuple, expected_values)))
                        expected_count = len(set(map(tuple, expected_values))) if take_unique else len(expected_values)
                        self.assertEqual(len(actual), expected_count)
                        np.testing.assert_array_equal(np.asarray(values)[indices], actual)
                        np.testing.assert_array_equal(np.take_along_axis(actual, inverse, axis=1), np.broadcast_to(values, actual.shape))
                        blocks, = builder.partitions(sizes, take_unique=take_unique)
                        np.testing.assert_array_equal(np.concatenate(blocks, axis=1), actual)

    def test_compiled_and_python_population_agree(self):
        function = UniquePartitions._populate_partitions
        if not hasattr(function, 'py_func'):
            self.skipTest('Numba unavailable; public checks cover the Python fallback')
        partition = np.array([4, 3, 2, 1, 0])
        sizes = np.array([2, 3])
        blocks = (np.array(list(itertools.combinations(range(5), 2))), np.array([[0, 1, 2]]))
        shapes = (10, 1)
        compiled_values, compiled_indices = np.empty((10, 5), dtype=int), np.empty((10, 5), dtype=int)
        python_values, python_indices = np.empty((10, 5), dtype=int), np.empty((10, 5), dtype=int)
        function(partition, sizes, shapes, blocks, 10, compiled_values, compiled_indices)
        function.py_func(partition, sizes, shapes, blocks, 10, python_values, python_indices)
        np.testing.assert_array_equal(compiled_values, python_values)
        np.testing.assert_array_equal(compiled_indices, python_indices)
