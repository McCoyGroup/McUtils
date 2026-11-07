"""Index-only streaming tests using the existing actual HNO3 row fixture."""
import json, math, unittest
from pathlib import Path
import numpy as np
from McUtils.Combinatorics import SymmetricGroupGenerator, UniquePermutations

class PermutationStreamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data=json.loads((Path(__file__).parent/'TestData/hno3_vpt2_rows.json').read_text())
        cls.states=np.asarray(list(dict.fromkeys(tuple(r['state']) for r in data['rows'])),dtype=np.int64)

    def compare_stream(self, states, rules, size):
        group=SymmetricGroupGenerator(states.shape[1])
        dense=list(group.iter_permutation_rule_direct_sum(states,rules,block_size=size))
        indexed=list(group.iter_permutation_rule_direct_sum(states,rules,block_size=size,return_indices=True))
        self.assertEqual(len(dense),len(indexed))
        for (rows,values),(index_rows,indices) in zip(dense,indexed):
            self.assertLessEqual(len(indices),size)
            self.assertEqual(indices.ndim,1)
            np.testing.assert_array_equal(rows,index_rows)
            np.testing.assert_array_equal(indices,group.to_indices(values))

    def test_actual_fundamental_overtone_combination_indices(self):
        self.compare_stream(self.states,[(),(1,),(-1,),(2,),(-1,1),(2,-1),(1,1,-1)],64)

    def test_output_block_caps_and_duplicate_sources(self):
        states=self.states[[0,1,1,2,3]]
        for size in [7,31]:
            self.compare_stream(states,[(1,),(-1,1),(1,1,1)],size)

    def test_higher_order_rules_use_same_native_ids(self):
        self.compare_stream(self.states,[(1,1,1,1,1,1),(-1,-1,2,1)],31)

    def test_zero_and_impossible_lowering(self):
        ground=np.zeros((1,self.states.shape[1]),dtype=np.int64)
        self.compare_stream(ground,[()],3)
        self.compare_stream(ground,[(-4,)],3)

    def test_virtual_coordinate_maps_match_materialized_native_ranks(self):
        group=SymmetricGroupGenerator(self.states.shape[1])
        maps=np.stack([np.arange(group.dim),np.arange(group.dim)[::-1],np.roll(np.arange(group.dim),2)])
        physical=self.states[:,maps].reshape(-1,group.dim)
        expected=group.to_indices(physical).reshape(len(self.states),len(maps))
        np.testing.assert_array_equal(group.to_indices(self.states,permutation_maps=maps),expected)

    def test_empty_states_and_coordinate_maps(self):
        group=SymmetricGroupGenerator(self.states.shape[1])
        maps=np.arange(group.dim)[None]
        self.assertEqual(group.to_indices(np.empty((0,group.dim),dtype=int),permutation_maps=maps).shape,(0,1))
        self.assertEqual(group.to_indices(self.states,permutation_maps=np.empty((0,group.dim),dtype=int)).shape,(len(self.states),0))

    def test_invalid_coordinate_map_rejected(self):
        group=SymmetricGroupGenerator(self.states.shape[1])
        with self.assertRaises(ValueError):
            group.to_indices(self.states,permutation_maps=np.zeros((1,group.dim),dtype=int))

    def test_large_native_permutation_rank_is_exact(self):
        descending=np.arange(19,-1,-1,dtype=np.int64)
        ascending=descending[::-1].copy()
        before_last=ascending.copy();before_last[-2:]=before_last[-2:][::-1]
        values=np.stack([descending,ascending,before_last])
        expected=np.array([0,math.factorial(20)-1,math.factorial(20)-2],dtype=np.int64)
        np.testing.assert_array_equal(UniquePermutations.get_permutation_indices(values),expected)
        maps=np.stack([np.arange(20),np.r_[np.arange(18),19,18]])
        wanted=np.column_stack([expected,[1,math.factorial(20)-2,math.factorial(20)-1]])
        np.testing.assert_array_equal(UniquePermutations.get_permutation_indices(values,permutation_maps=maps),wanted)

if __name__=='__main__':unittest.main()
