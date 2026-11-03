import itertools
import unittest
from unittest import mock
import numpy as np
from McUtils.Combinatorics import SymmetricGroupGenerator, UniquePermutations


class CombinatoricsStreamingTests(unittest.TestCase):
    @staticmethod
    def collect(group, states, rules, block_size):
        result=[]
        for rows, values in group.iter_permutation_rule_direct_sum(states,rules,block_size):
            assert len(rows)==len(values)<=block_size
            result.append(np.column_stack((rows,values)))
        data=np.concatenate(result) if result else np.empty((0,group.dim+1),int)
        return data[np.lexsort(data.T[::-1])] if len(data) else data

    @staticmethod
    def brute(states, rules):
        rows=[];dim=states.shape[1]
        signatures={tuple(sorted(x for x in rule if x)) for rule in rules}
        for signature in signatures:
            if len(signature)>dim:continue
            for change in set(itertools.permutations(signature+(0,)*(dim-len(signature)))):
                targets=states+change
                for i in np.flatnonzero(np.all(targets>=0,axis=1)):
                    rows.append((i,*targets[i]))
        data=np.array(rows,dtype=int).reshape(-1,dim+1)
        return data[np.lexsort(data.T[::-1])] if len(data) else data

    def test_source_identities_and_small_blocks(self):
        states=np.array([[2,0,1,0],[0,1,2,0],[0,0,0,0],[2,0,1,0],[-1,1,0,0]])
        rules=[(),(1,),(-1,),(2,-1),(1,-1,-1),(0,1,0),(1,)]
        group=SymmetricGroupGenerator(4)
        expected=self.brute(states,rules)
        for size in [1,3,7,64]:
            np.testing.assert_array_equal(self.collect(group,states,rules,size),expected)

    def test_native_collecting_implementation_agrees(self):
        states=np.array([[2,0,0,0,0],[0,1,0,1,0],[0,0,0,0,0],[0,2,0,0,0]])
        rules=[(),(1,),(-1,),(2,),(-2,),(1,1),(-1,1),(-1,-1,1)]
        group=SymmetricGroupGenerator(5)
        targets=group.take_permutation_rule_direct_sum(states,rules,split_results=True)[0]
        native=np.concatenate([np.column_stack((np.full(len(v),i),v)) for i,v in enumerate(targets)])
        native=native[np.lexsort(native.T[::-1])]
        np.testing.assert_array_equal(self.collect(group,states,rules,13),native)

    def test_impossible_lowering_never_expands_rule_permutations(self):
        states=np.zeros((4,72),int);states[np.arange(4),np.arange(4)]=2
        with mock.patch.object(UniquePermutations,'iter_permutations',
                               side_effect=AssertionError('impossible rule was expanded')):
            actual=self.collect(SymmetricGroupGenerator(72),states,[(-1,-1,1)],7)
        self.assertEqual(len(actual),0)

    def test_higher_degree_rules(self):
        states=np.array([[1]*8,[0]*8])
        rules=[(-1,)*4+(2,)*4,(1,)*8,(-3,2,1)]
        group=SymmetricGroupGenerator(8)
        # The native implementation is the independent reference for a rule
        # spanning eight modes; no VPT-order specialization enters the iterator.
        native=group.take_permutation_rule_direct_sum(states,rules,split_results=True)[0]
        expected=np.concatenate([np.column_stack((np.full(len(v),i),v)) for i,v in enumerate(native)])
        expected=expected[np.lexsort(expected.T[::-1])]
        np.testing.assert_array_equal(self.collect(group,states,rules,11),expected)

    def test_large_quanta_does_not_populate_unused_partition_manifolds(self):
        group=SymmetricGroupGenerator(3)
        with mock.patch.object(group,'_get_partition_perms',side_effect=AssertionError('unneeded manifold')):
            actual=self.collect(group,np.array([[1000000,0,0]]),[(-1,1)],3)
        np.testing.assert_array_equal(actual,[[0,999999,0,1],[0,999999,1,0]])

    def test_zero_change_does_not_build_permutation_plans_or_alias_input(self):
        group=SymmetricGroupGenerator(3)
        states=np.array([[2,0,0],[0,1,0],[-1,2,0]])
        before=states.copy()
        with mock.patch.object(group,'_get_direct_sum_rule_groups',
                               side_effect=AssertionError('zero change needs no rule plan')):
            blocks=list(group.iter_permutation_rule_direct_sum(states,[(),(0,0)],2))
        self.assertEqual(sum(len(rows) for rows,_ in blocks),2)
        blocks[0][1][:]=-10
        np.testing.assert_array_equal(states,before)

    def test_empty_and_all_lowering_inputs(self):
        group=SymmetricGroupGenerator(1);states=np.array([[2],[0],[1]],dtype=np.uint8)
        np.testing.assert_array_equal(self.collect(group,states,[(-1,),(-2,)],1),
                                      self.brute(states.astype(int),[(-1,),(-2,)]))
        self.assertEqual(len(self.collect(group,states,[],3)),0)
        self.assertEqual(len(self.collect(group,np.empty((0,1),int),[(1,)],3)),0)
        with self.assertRaises(ValueError):list(group.iter_permutation_rule_direct_sum(states,[(1,)],0))


if __name__=='__main__':unittest.main()
