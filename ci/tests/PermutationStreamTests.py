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

    def test_class_ranges_match_actual_HNO3_orbits_and_signed_rules(self):
        group=SymmetricGroupGenerator(self.states.shape[1])
        representatives=list(dict.fromkeys(tuple(sorted(map(int,s),reverse=True)) for s in self.states if sum(s)<=3))[:7]
        rules=[(),(1,),(-1,),(2,-1),(1,1,-1),(1,1,1)]
        for representative in representatives:
            source=UniquePermutations(np.asarray(representative)).permutations()
            expected=np.unique(np.concatenate([ids for rows,ids in group.iter_permutation_rule_direct_sum(source,rules,return_indices=True)]))
            ranges=group.get_direct_sum_class_ranges(np.asarray(representative),rules)
            actual=np.concatenate([np.arange(low,high) for low,high in ranges]) if len(ranges) else np.empty(0,dtype=int)
            np.testing.assert_array_equal(actual,expected)

    def test_class_ranges_use_native_partition_order_at_higher_order(self):
        group=SymmetricGroupGenerator(self.states.shape[1])
        representatives=list(dict.fromkeys(tuple(sorted(map(int,s),reverse=True)) for s in self.states if sum(s)<=2))[:4]
        rules=[(1,1,1,1,1,1),(-1,-1,2,1),(-3,),()]
        for representative in representatives:
            source=UniquePermutations(np.asarray(representative)).permutations()
            blocks=[ids for rows,ids in group.iter_permutation_rule_direct_sum(source,rules,return_indices=True)]
            expected=np.unique(np.concatenate(blocks)) if blocks else np.empty(0,dtype=int)
            ranges=group.get_direct_sum_class_ranges(np.asarray(representative),rules)
            actual=np.concatenate([np.arange(low,high) for low,high in ranges]) if len(ranges) else np.empty(0,dtype=int)
            np.testing.assert_array_equal(actual,expected)

    def test_class_multiplicity_iterator_matches_existing_HNO3_tables(self):
        from McUtils.Combinatorics import IntegerPartitioner2D
        for state in self.states[:6]:
            values,rows=UniquePermutations.get_permutation_class_counts(state)
            for rule in [(1,),(-1,1),(1,1,1)]:
                padded=np.zeros(len(state),dtype=int);padded[:len(rule)]=rule
                increments,columns=UniquePermutations.get_permutation_class_counts(padded)
                tables=IntegerPartitioner2D.get_partitions(rows,columns)
                key=lambda table:tuple(map(int,table.flat))
                self.assertEqual(set(map(key,tables)),set(map(key,IntegerPartitioner2D.iter_partitions(rows,columns))))
                allowed=values[:,None]+increments[None,:]>=0
                expected={key(table) for table in tables if np.all((table==0)|allowed)}
                actual={key(table) for table in IntegerPartitioner2D.iter_partitions(rows,columns,allowed=allowed)}
                self.assertEqual(actual,expected)

    def test_class_multiplicity_iteration_does_not_mutate_previous_tables(self):
        from McUtils.Combinatorics import IntegerPartitioner2D
        state=self.states[-1]
        values,rows=UniquePermutations.get_permutation_class_counts(state)
        columns=np.array([1,len(state)-1])
        iterator=IntegerPartitioner2D.iter_partitions(rows,columns)
        first=next(iterator);saved=first.copy();list(iterator)
        np.testing.assert_array_equal(first,saved)


    # Native Psience frequencies from the same actual HNO3 FChk as the row
    # fixture; input SHA256 5b2ad55197b40440c868158ce8757be8997b00df39ae99713821a2b3341cd32b.
    filter_frequencies=np.array([0.0022091806829265537,0.0026866989790004497,
        0.0030336185319669155,0.0035333560019367226,0.0040757163706985075,
        0.005995761249610487,0.006121095689537073,0.008412070536502078,0.016940751588948696])

    def _compare_constraint_ranges(self,partition,constraints,size=3):
        generator=UniquePermutations(np.asarray(partition))
        values=generator.permutations()
        expected=np.flatnonzero(UniquePermutations.test_constraints(values,constraints))
        stats={};blocks=list(generator.iter_index_ranges(constraints,block_size=size,statistics=stats))
        self.assertTrue(all(len(block)<=size for block in blocks))
        actual=np.concatenate([np.arange(a,b) for block in blocks for a,b in block]) if blocks else np.empty(0,dtype=int)
        np.testing.assert_array_equal(actual,expected)
        return stats

    def test_structured_ranges_match_actual_HNO3_orbits(self):
        representatives=list(dict.fromkeys(tuple(sorted(map(int,s),reverse=True)) for s in self.states if sum(s)<=3))[:8]
        n=self.states.shape[1]
        lower=np.zeros(n,dtype=int);lower[2]=1
        upper=np.full(n,2);upper[0]=0;upper[-1]=1
        for partition in representatives:
            for filters in [{'maximum':1},{'minimum':lower,'maximum':upper},
                            {'parity':'odd'},{'partitions':[(1,),(2,1),(1,1,1)]},
                            {'weights':self.filter_frequencies,'windows':[[0,0.014],[0.020,0.024]]},
                            {'maximum':upper,'weights':self.filter_frequencies,'windows':[[0.003,0.025]]}]:
                self._compare_constraint_ranges(partition,filters)

    def test_structured_energy_endpoints_match_reference_exactly(self):
        partition=next(tuple(sorted(map(int,s),reverse=True)) for s in self.states if sum(s)==2)
        values=UniquePermutations(np.asarray(partition)).permutations()
        energies=np.zeros(len(values))
        for i,w in enumerate(self.filter_frequencies):energies+=values[:,i]*w
        e=float(energies[len(energies)//2])
        for low,high in [(e,e),(np.nextafter(e,-np.inf),e),
                         (np.nextafter(e,np.inf),np.inf),(0,np.nextafter(e,-np.inf))]:
            self._compare_constraint_ranges(partition,{'weights':self.filter_frequencies,'windows':[[low,high]]},size=1)

    def test_structured_filters_combine_without_mutating_inputs(self):
        cap=np.full(self.states.shape[1],2);saved=cap.copy()
        filters=[{'maximum':cap},{'parity':'even'},
                 {'weights':self.filter_frequencies,'windows':[[0,0.03]]},
                 {'weights':self.filter_frequencies[::-1],'windows':[[0,0.025]]}]
        for state in self.states[:5]:self._compare_constraint_ranges(state,filters,size=1)
        np.testing.assert_array_equal(cap,saved)
        no_states=UniquePermutations.prepare_constraints([{'parity':0},{'parity':1}],len(cap))
        self.assertFalse(np.any(UniquePermutations.test_constraints(self.states,no_states)))

    def test_structured_invalid_windows_and_mode_counts_are_rejected(self):
        for filters in [{'maximum':[1,2]}, {'parity':'unknown'},
                        {'weights':self.filter_frequencies,'windows':[[2,1]]},
                        {'weights':self.filter_frequencies,'windows':[[float('nan'),2]]}]:
            with self.assertRaises(ValueError):UniquePermutations.prepare_constraints(filters,self.states.shape[1])


if __name__=='__main__':unittest.main()
