import multiprocessing as mp
import unittest

import numpy as np

from McUtils.Parallelizers.SharedMemory import (
    SharedArrayAllocator,
    SharedMemoryArrayTree,
    SharedMemoryDict,
    SharedMemoryList,
    SharedObjectManager
)


def inspect_shared_tree(tree):
    rank_three = tree[0][1]
    rank_four = tree[1]['tensor']
    return {
        'pid': mp.current_process().pid,
        'name': tree.descriptor.name,
        'rank_three_sum': float(rank_three.sum()),
        'rank_four_sum': float(rank_four.sum()),
        'rank_three_writeable': rank_three.flags.writeable,
        'rank_four_writeable': rank_four.flags.writeable
    }


class SharedMemoryTests(unittest.TestCase):

    def test_shared_ndarray_numpy_protocol_and_cleanup(self):
        allocator = SharedArrayAllocator(autoclose=False)
        source = np.arange(24.0).reshape(2, 3, 4)
        shared = allocator.create_shared_array(source, readonly=True)
        name = shared.buf.name
        try:
            loaded = np.asanyarray(shared)
            self.assertEqual(loaded.dtype, source.dtype)
            self.assertEqual(loaded.shape, source.shape)
            self.assertFalse(loaded.flags.writeable)
            np.testing.assert_array_equal(loaded, source)
        finally:
            allocator.delete_shared_array(shared)

        from multiprocessing import shared_memory
        with self.assertRaises(FileNotFoundError):
            shared_memory.SharedMemory(name=name, create=False)

    def test_shared_list_nested_roundtrip_append_extend_and_pop(self):
        shared = SharedMemoryList([
            np.arange(6).reshape(2, 3),
            {'nested': np.linspace(0, 1, 5)},
            7
        ])
        try:
            shared.append(np.array([8.0, 9.0]))
            shared.extend([
                {'more': np.arange(3)},
                -4
            ])
            loaded = shared.unshare()
            np.testing.assert_array_equal(loaded[0], np.arange(6).reshape(2, 3))
            np.testing.assert_array_equal(loaded[1]['nested'], np.linspace(0, 1, 5))
            self.assertEqual(loaded[2], 7)
            np.testing.assert_array_equal(loaded[3], [8.0, 9.0])
            np.testing.assert_array_equal(loaded[4]['more'], np.arange(3))
            self.assertEqual(loaded[5], -4)

            popped = shared.pop(1)
            np.testing.assert_array_equal(popped['nested'], np.linspace(0, 1, 5))
            self.assertEqual(len(shared), 5)
        finally:
            shared.close()

    def test_shared_dict_nested_roundtrip_and_replacement(self):
        shared = SharedMemoryDict({
            'array': np.arange(4.0),
            'nested': {'left': np.ones((2, 2)), 'removed': np.arange(2)},
            'scalar': 3
        })
        try:
            shared['nested'] = {'left': np.zeros((3, 1))}
            shared['array'] = [1, {'inside': np.arange(5)}]
            loaded = shared.unshare()
            self.assertEqual(set(loaded['nested']), {'left'})
            np.testing.assert_array_equal(loaded['nested']['left'], np.zeros((3, 1)))
            self.assertEqual(loaded['array'][0], 1)
            np.testing.assert_array_equal(loaded['array'][1]['inside'], np.arange(5))
            self.assertEqual(loaded['scalar'], 3)
        finally:
            shared.close()

    def test_shared_dict_nested_mapping_mutation_is_visible(self):
        shared = SharedMemoryDict({'nested': {}})
        try:
            nested = shared['nested']
            nested['key'] = 5
            self.assertEqual(shared['nested']['key'], 5)
            self.assertEqual(shared.unshare()['nested']['key'], 5)
        finally:
            shared.close()

    def test_shared_dict_reallocates_shape_and_dtype_changes(self):
        shared = SharedMemoryDict({'value': np.arange(4)})
        try:
            reshaped = np.arange(6).reshape(2, 3)
            shared['value'] = reshaped
            np.testing.assert_array_equal(shared.load_item('value'), reshaped)

            retyped = np.linspace(0, 1, 6).reshape(2, 3)
            shared['value'] = retyped
            loaded = shared.load_item('value')
            self.assertEqual(loaded.dtype, retyped.dtype)
            np.testing.assert_array_equal(loaded, retyped)

            shared['value'] = 12
            self.assertEqual(shared.load_item('value'), 12)
        finally:
            shared.close()

    def test_shared_object_manager_primitive_array_roundtrip(self):
        source = np.arange(30.0).reshape(2, 3, 5)
        manager = SharedObjectManager(source)
        manager.share()
        loaded = manager.unshare()
        self.assertIsInstance(loaded, np.ndarray)
        np.testing.assert_array_equal(loaded, source)

    def test_array_tree_preserves_structure_aliases_and_scalar_shape(self):
        repeated = np.arange(12.0).reshape(3, 4)
        scalar = np.array(2.5)
        noncontiguous = np.arange(24).reshape(4, 6)[:, ::2]
        source = [
            repeated,
            ({'same': repeated, 'scalar': scalar}, noncontiguous)
        ]
        tree = SharedMemoryArrayTree.create(source)
        name = tree.descriptor.name
        try:
            self.assertIs(tree[0], tree[1][0]['same'])
            self.assertEqual(tree[1][0]['scalar'].shape, ())
            self.assertEqual(tree[1][1].shape, noncontiguous.shape)
            self.assertFalse(tree[0].flags.writeable)
            self.assertFalse(tree[1][1].flags.writeable)
            np.testing.assert_array_equal(tree[0], repeated)
            np.testing.assert_array_equal(tree[1][1], noncontiguous)
            loaded = tree.unshare()
            np.testing.assert_array_equal(loaded[1][0]['scalar'], scalar)
        finally:
            tree.dispose()

        from multiprocessing import shared_memory
        with self.assertRaises(FileNotFoundError):
            shared_memory.SharedMemory(name=name, create=False)

    def test_array_tree_spawn_attachment(self):
        rng = np.random.default_rng(8675309)
        rank_three = rng.normal(size=(7, 7, 7))
        rank_four = rng.normal(size=(7, 7, 7, 7))
        tree = SharedMemoryArrayTree.create([
            [0, rank_three],
            {'tensor': rank_four}
        ])
        try:
            context = mp.get_context('spawn')
            with context.Pool(2) as pool:
                reports = pool.map(inspect_shared_tree, [tree, tree])
            self.assertEqual(len({report['pid'] for report in reports}), 2)
            self.assertEqual(
                {report['name'] for report in reports},
                {tree.descriptor.name}
            )
            for report in reports:
                self.assertFalse(report['rank_three_writeable'])
                self.assertFalse(report['rank_four_writeable'])
                self.assertEqual(report['rank_three_sum'], float(rank_three.sum()))
                self.assertEqual(report['rank_four_sum'], float(rank_four.sum()))
        finally:
            tree.dispose()

    def test_array_tree_rejects_object_arrays(self):
        with self.assertRaises(TypeError):
            SharedMemoryArrayTree.create([np.array([object()], dtype=object)])


if __name__ == '__main__':
    unittest.main()
