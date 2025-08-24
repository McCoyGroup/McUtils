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
    def test_lemherCodes(self):
        # print(
        #     lehmer_encode([0, 1, 2])
        # )
        base_perms = list(list(p) for p in itertools.permutations(range(5), 5))
        lehmers = lehmer_encode(base_perms)
        self.assertEquals(list(range(len(base_perms))), lehmers.tolist())
        decodes = lehmer_decode(5, lehmers)
        self.assertEquals(base_perms, decodes.tolist())

    @validationTest
    def test_YT(self):
        # print(
        #     lehmer_encode([0, 1, 2])
        # )

        # gen = YoungTableauxGenerator(6)
        # parts = list(itertools.chain(*IntegerPartitioner.partitions(6)))[4]
        # tabs = gen.get_standard_tableaux(parts, brute_force=False)
        # tabs_bf = gen.get_standard_tableaux(parts, brute_force=True)
        # n = gen.number_of_tableaux(parts)
        # l2 = len(tabs_bf[0])
        # self.assertEquals(n, l2)
        # l1 = len(tabs[0])
        # self.assertEquals(l1, l2)

        # gen = YoungTableauxGenerator(1)
        for i in range(1, 11):
            gen = YoungTableauxGenerator(i)
            n = gen.number_of_tableaux()
            print(">>>", n)
            tabs = gen.get_standard_tableaux(brute_force=False)
            # tabs_bf = gen.get_standard_tableaux(brute_force=True)

            # l2 = [len(t[0]) for t in tabs_bf]
            # self.assertEquals(n, sum(l2))
            # gen.print_tableaux(tabs)
            l1 = [len(t[0]) for t in tabs]
            self.assertEquals(n, sum(l1))
            # self.assertEquals(n, sum(l1))

        for i in range(1, 9):
            gen = YoungTableauxGenerator(i)
            n = gen.number_of_tableaux()
            print(">>>", n)
            tabs = gen.get_standard_tableaux(brute_force=False)
            tabs_bf = gen.get_standard_tableaux(brute_force=True)

            l2 = [len(t[0]) for t in tabs_bf]
            self.assertEquals(n, sum(l2))
            # gen.print_tableaux(tabs)
            l1 = [len(t[0]) for t in tabs]
            self.assertEquals(l1, l2)
            # self.assertEquals(n, sum(l1))

    @validationTest
    def test_PrimeFactorization(self):

        plist = prime_list(20)
        np.random.seed(1232232)
        mod_pos = np.sort(np.random.choice(np.arange(20), (4, 3)), axis=1)
        res = np.random.randint(1, 4, size=(4, 3))
        ints = np.prod(np.array(plist)[mod_pos] ** res, axis=1, dtype=int)
        _, facs = prime_factorize(ints)
        print(ints)
        print(len(_))
        print(res)
        facs = np.array(facs).T
        sel = np.where(facs > 0)
        print(facs[sel].reshape(4, 3))
        print(mod_pos)
        print(np.array(sel).T.reshape(4, 3, 2)[:, :, 1])


        plist = prime_list(20)
        np.random.seed(1232232)
        mod_pos = np.sort(np.random.choice(np.arange(20), (100, 3)), axis=1)
        res = np.random.randint(1, 4, size=(100, 3))
        ints = np.prod(np.array(plist)[mod_pos] ** res, axis=1, dtype=int)
        print(ints)
        _, facs = prime_factorize(ints)
        # facs = np.array(facs).T
        # sel = np.where(facs > 0)

        return

    @validationTest
    def test_Multinomials(self):
        print(
            stable_factorial_ratio([math.factorial(7)], [3, 4, 7])
        )

    @debugTest
    def test_Characters(self):
        print()

        elements, classes = dh_group_classes(5)
        self.assertEquals(
            np.sort(np.concatenate(classes)).tolist(),
            np.arange(sum(len(l) for l in classes)).tolist()
        )
        self.assertEquals(len(elements), sum(len(l) for l in classes))

        # ct = CharacterTable.point_group("Cv", 7)
        # # ct = CharacterTable.fixed_size_point_group("T")
        # with np.printoptions(linewidth=1e8, threshold=1e8):
        #     print(ct.format())
        #     print(np.round(np.real(ct.table.T @ np.conj(ct.table)), 8))

        return

        print(mfmt.TableFormatter("").format(symmetric_group_character_table(3)))
        print("="*50)
        print(mfmt.TableFormatter("").format(symmetric_group_character_table(4)))
        # print("="*50)
        # print(mfmt.TableFormatter("").format(symmetric_group_character_table(5)))
        # print("="*50)
        # print(mfmt.TableFormatter("").format(symmetric_group_character_table(6)))
        # print("="*50)
        # print(mfmt.TableFormatter("").format(symmetric_group_character_table(7)))
        # checked against Mathematica, good up through order 7

        weights, ct = symmetric_group_character_table(4, return_weights=True)
        weights = weights #/ np.sum(weights)
        w_vec = np.sqrt(weights[np.newaxis, :] / np.sum(weights))
        wct = w_vec * ct
        # print(weights)
        # print(ct)
        print(mfmt.TableFormatter("").format(wct))
        print(np.round(wct @ wct.T, 6))

        sel = (0, 2, 3, 4)
        b2 = wct[:, sel]
        w2 = np.sqrt(weights[np.newaxis, sel] / np.sum(weights[sel,]))
        q, r = np.linalg.qr(b2.T)
        print(q.T / w2)

        # s7 = symmetric_group_character_table(7)
        # print(np.linalg.svd(s7))

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

        # num_parts = IntegerPartitioner.count_partitions(6, 2, 3)
        # self.assertEquals(num_parts, 1)

        # num_parts = IntegerPartitioner.count_partitions(5, 3, 3)
        # self.assertEquals(num_parts, 3)

        n = np.array([3, 5, 2, 6])
        M = np.array([1, 3, 1, 2])
        l = np.array([3, 3, 3, 3])
        # raise Exception([
        #     IntegerPartitioner.count_partitions(3, 1, 3),
        #     IntegerPartitioner.count_partitions(5, 3, 3),
        #     IntegerPartitioner.count_partitions(2, 1, 3),
        #     IntegerPartitioner.count_partitions(6, 2, 3)
        # ])
        num_parts = IntegerPartitioner.count_partitions(n, M, l)
        self.assertEquals(num_parts.tolist(), [1, 3, 1, 1])

        n = np.array([3, 5, 2, 6, 10, 10])
        M = np.array([1, 3, 1, 2, 10,  5])
        l = np.array([3, 3, 3, 3,  3,  3])
        # raise Exception([
        #     IntegerPartitioner.count_partitions(3, 1, 3),
        #     IntegerPartitioner.count_partitions(5, 3, 3),
        #     IntegerPartitioner.count_partitions(2, 1, 3),
        #     IntegerPartitioner.count_partitions(6, 2, 3)
        # ])
        num_parts = IntegerPartitioner.count_partitions(n, M, l)
        self.assertEquals(num_parts.tolist(), [1, 3, 1, 1, 14, 5])

        num_greater = IntegerPartitioner.count_exact_length_partitions_in_range(4, 4, 2, 2)
        len2_4s = IntegerPartitioner.partitions(4, max_len=2)[1]
        raw_counts = len([x for x in len2_4s if len(x) == 2 and x[0] > 2])
        self.assertEquals(num_greater, raw_counts)


        parts = IntegerPartitioner.partitions(3)
        self.assertEquals([p.tolist() for p in parts], [ [[3]], [[2, 1]], [[1, 1, 1]]])

        parts = IntegerPartitioner.partitions(3, pad=True)
        self.assertEquals(parts.tolist(), [[3, 0, 0], [2, 1, 0], [1, 1, 1]])

        parts = IntegerPartitioner.partitions(3, pad=True, max_len=2)
        self.assertEquals(parts.tolist(), [[3, 0], [2, 1]])

        num_parts = IntegerPartitioner.count_partitions(10)
        self.assertEquals(num_parts, 42)

        parts = IntegerPartitioner.partitions(5)
        self.assertEquals([p.tolist() for p in parts], [
            [[5]],
            [[4, 1], [3, 2]],
            [[3, 1, 1], [2, 2, 1]],
            [[2, 1, 1, 1]],
            [[1, 1, 1, 1, 1]]
        ])

        parts = IntegerPartitioner.partitions(10, pad=True, max_len=2)
        self.assertEquals(parts.tolist(), [[10, 0], [9, 1], [8, 2], [7, 3], [6, 4], [5, 5]])

        self.assertEquals(
            IntegerPartitioner.partition_indices([[10, 0], [9, 1], [8, 2], [7, 3], [6, 4], [5, 5]]).tolist(),
            list(range(6))
        )

        np.random.seed(0)
        full_stuff = IntegerPartitioner.partitions(10, pad=True, max_len=3)
        inds = np.random.choice(len(full_stuff), 5, replace=False)

        test_parts = full_stuff[inds]
        test_inds = IntegerPartitioner.partition_indices(test_parts)
        self.assertEquals(
            test_inds.tolist(),
            inds.tolist(),
            msg="{} should have indices {} but got {}".format(test_parts, inds, test_inds)
        )

        np.random.seed(1)
        full_stuff = IntegerPartitioner.partitions(10, pad=True, max_len=7)

        inds = np.random.choice(len(full_stuff), 35, replace=False)

        test_parts = full_stuff[inds]
        # raise Exception(inds, test_parts, full_stuff)
        test_inds = IntegerPartitioner.partition_indices(test_parts)
        self.assertEquals(
            test_inds.tolist(),
            inds.tolist(),
            msg="{} should have indices {} but got {}".format(test_parts, inds, test_inds)
        )

        # just a faster code path if we _know_ we've already computed the relevant bits
        test_inds = IntegerPartitioner.partition_indices(test_parts, check=False)
        self.assertEquals(
            test_inds.tolist(),
            inds.tolist(),
            msg="{} should have indices {} but got {}".format(test_parts, inds, test_inds)
        )

    @validationTest
    def test_Partitions2D(self):
        # for p in IntegerPartitioner2D.get_partitions(
        #         [3, 2, 1],
        #         [2, 2, 1, 1]
        #     ):
        #     print(p)
        print(
            IntegerPartitioner2D.get_partitions(
                [3, 2, 1],
                [2, 2, 2]
            )
        )
        raise Exception(...)

    @inactiveTest
    def test_GenericPartitions(self):
        raise Exception(
            UniquePartitions([3, 2, 1, 0, 0, 0]).partitions([3, 2, 1])
        )

        # raise Exception(
        #     UniquePartitions([0, 1, 0, 0, 2, 0, 3]).partitions(
        #         [2, 3, 2],
        #         split=False,
        #         take_unique=True
        #     )
        # )

    @validationTest
    def test_UniquePartitionPermutations(self):
        """
        Tests the generation of unique permutations of partitions
        :return:
        :rtype:
        """

        lens, parts = IntegerPartitioner.partitions(10, pad=True, return_lens=True)

        perms = UniquePermutations(parts[0]).permutations()
        self.assertEquals(perms.tolist(),
                          [
                              [10,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                              [ 0, 10,  0,  0,  0,  0,  0,  0,  0,  0],
                              [ 0,  0, 10,  0,  0,  0,  0,  0,  0,  0],
                              [ 0,  0,  0, 10,  0,  0,  0,  0,  0,  0],
                              [ 0,  0,  0,  0, 10,  0,  0,  0,  0,  0],
                              [ 0,  0,  0,  0,  0, 10,  0,  0,  0,  0],
                              [ 0,  0,  0,  0,  0,  0, 10,  0,  0,  0],
                              [ 0,  0,  0,  0,  0,  0,  0, 10,  0,  0],
                              [ 0,  0,  0,  0,  0,  0,  0,  0, 10,  0],
                              [ 0,  0,  0,  0,  0,  0,  0,  0,  0, 10]
                          ]
                          )

        test_set = [
                              [6, 2, 1, 1, 0, 0, 0, 0, 0, 0],
                              [6, 2, 1, 0, 1, 0, 0, 0, 0, 0],
                              [6, 2, 1, 0, 0, 1, 0, 0, 0, 0],
                              [6, 2, 1, 0, 0, 0, 1, 0, 0, 0],
                              [6, 2, 1, 0, 0, 0, 0, 1, 0, 0],
                              [6, 2, 1, 0, 0, 0, 0, 0, 1, 0],
                              [6, 2, 1, 0, 0, 0, 0, 0, 0, 1],
                              [6, 2, 0, 1, 1, 0, 0, 0, 0, 0],
                              [6, 2, 0, 1, 0, 1, 0, 0, 0, 0],
                              [6, 2, 0, 1, 0, 0, 1, 0, 0, 0]
                          ]
        perm_builder = UniquePermutations(parts[15])
        perms = perm_builder.permutations(num_perms = 10)
        self.assertEquals(perms.tolist(), test_set)

        wat = UniquePermutations(parts[15]).permutations_from_indices(list(range(len(test_set))))
        # raise Exception(wat)
        self.assertEquals(wat.tolist(), test_set)

        inds = perm_builder.index_permutations(perms)
        self.assertEquals(inds.tolist(), list(range(len(inds))))

        many_perms = perm_builder.permutations(initial_permutation=perms[8])
        self.assertEquals(len(many_perms), perm_builder.num_permutations - 8)

        perms = perm_builder.permutations(initial_permutation=perms[8], num_perms=10)
        self.assertEquals(many_perms[:10].tolist(), perms.tolist())

        perm_builder = UniquePermutations([3, 1, 1, 0, 0])

        test_set = [
            [3, 0, 0, 1, 1],
            [1, 1, 3, 0, 0],
            [0, 3, 1, 1, 0]
        ]
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

        # print("="*50)
        # print(test_set)
        inds = perm_builder.index_permutations(test_set)
        self.assertEquals(inds.tolist(), test_inds.tolist())

        # print('=' * 50)
        perms = perm_builder.permutations_from_indices(inds)
        self.assertEquals(perms.tolist(), test_set.tolist())

        swaps, perms = perm_builder.permutations(return_indices=True)
        test_inds = np.random.choice(len(swaps), 10, replace=False)

        self.assertEquals([perm_builder.part[s].tolist() for s in swaps[test_inds,]], perms[test_inds,].tolist())
        # raise Exception(perms, inds)

        perm_builder = UniquePermutations([2, 1, 1, 1, 0, 0, 0, 0])
        all_perms = perm_builder.permutations()
        test_inds = [73, 237]#, 331, 561, 623, 715]
        perms = perm_builder.permutations_from_indices(test_inds)
        self.assertEquals(perms.tolist(), all_perms[test_inds].tolist())

    @inactiveTest
    def test_UniquePartitionBlocks(self):
        """
        Tests the generation of unique permutations of partitions
        :return:
        :rtype:
        """
        ...




    @validationTest
    def test_IntegerPartitionPermutations(self):
        """
        Tests generating and indexing integer partition permutations
        :return:
        :rtype:
        """

        np.random.seed(0)
        part_perms = IntegerPartitionPermutations(5)

        full_stuff = np.concatenate(part_perms.get_partition_permutations(), axis=0) # build everything so we can take subsamples to index

        inds = np.random.choice(len(full_stuff), 28, replace=False)
        subperms = full_stuff[inds,]

        # with BlockProfiler(name='perm method'):
        perm_inds = part_perms.get_partition_permutation_indices(subperms)
        self.assertEquals(inds.tolist(), perm_inds.tolist())

        # sorting = np.argsort(perm_inds)[5:7]
        # perm_inds = perm_inds[sorting]
        # subperms = subperms[sorting]

        og_perms = part_perms.get_partition_permutations_from_indices(perm_inds)
        self.assertEquals(subperms.tolist(), og_perms.tolist())

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

        self.assertEquals(inds[subinds,].tolist(), (1+subinds).tolist())

        np.random.seed(0)
        subinds = np.random.choice(len(inds), 250, replace=False)

        test_perms = gen.from_indices(1+subinds)
        self.assertEquals(part_perms[subinds,].tolist(), test_perms.tolist())

        # wat = gen.to_indices(
        #     [
        #         [1, 0, 0, 0, 0, 0, 0, 0],
        #         [1, 1, 0, 0, 0, 0, 0, 0]
        #     ]
        # )

        # test_states = np.array([
        #     [0, 0, 0, 0, 0, 0, 0, 0]
        # ])
        # test_rules = [[2], [1, 1]]
        # test_perms = gen.take_permutation_rule_direct_sum(
        #     test_states,
        #     test_rules
        # )
        #
        # sums = np.sum(test_perms, axis=1)
        # self.assertEquals(np.unique(sums).tolist(), [2])

        test_states = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [2, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 2, 0],
            [0, 1, 1, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 2, 0, 2, 0],
            [0, 0, 0, 0, 2, 0, 0, 2],
            [1, 0, 0, 0, 0, 0, 0, 2]
        ])
        test_rules = [[2], [1, 1]]
        test_perms, test_inds = gen.take_permutation_rule_direct_sum(
            test_states,
            test_rules,
            return_indices=True
        )

        sums = np.sum(test_perms, axis=1)
        test_sums = np.unique(
                            np.unique(np.sum(test_states, axis=1))[np.newaxis]
                            + np.unique([sum(x) for x in test_rules])[:, np.newaxis]
        )
        self.assertEquals(np.unique(sums).tolist(), test_sums.tolist())

        bleh = np.concatenate(
            [ UniquePermutations(x + [0] * (8-len(x))).permutations() for x in test_rules ],
            axis=0
        )

        full_perms = test_states[:, np.newaxis, :] + bleh[np.newaxis, :, :]
        full_perms = full_perms.reshape((-1, full_perms.shape[-1]))

        self.assertEquals(len(test_perms), len(full_perms))
        self.assertEquals(sorted(test_perms.tolist()), sorted(full_perms.tolist()))

        full_inds = gen.to_indices(full_perms)
        self.assertEquals(np.sort(test_inds).tolist(), np.sort(full_inds).tolist())

        test_rules = [
            [2], [-2], [-3], [1, 1], [-1, -1], [-1, 1], [-1, -1, 1]
        ]
        test_perms, test_inds = gen.take_permutation_rule_direct_sum(
            test_states,
            test_rules,
            return_indices=True
        )
        bleh = np.concatenate(
            [ UniquePermutations(x + [0] * (8-len(x))).permutations() for x in test_rules ],
            axis=0
        )

        full_full_perms = test_states[:, np.newaxis, :] + bleh[np.newaxis, :, :]
        full_perms = full_full_perms.reshape((-1, full_perms.shape[-1]))
        negs = np.where(full_perms < 0)[0]
        comp = np.setdiff1d(np.arange(len(full_perms)), negs)
        full_perms = full_perms[comp,]

        self.assertEquals(len(test_perms), len(full_perms))
        self.assertEquals(sorted(test_perms.tolist()), sorted(full_perms.tolist()))

        full_inds = gen.to_indices(full_perms)
        self.assertEquals(np.sort(test_inds).tolist(), np.sort(full_inds).tolist())
        # with BlockProfiler("secondary inds"):
        test_perms2, test_inds2 = gen.take_permutation_rule_direct_sum(
            test_states,
            test_rules,
            return_indices=True
        )

        self.assertEquals(test_inds.tolist(), test_inds2.tolist())

        # print("==" * 50)
        test_perms2, test_inds2 = gen.take_permutation_rule_direct_sum(
            test_states,
            test_rules,
            return_indices=True,
            split_results=True
        )

        bleeep = []
        for full_perms in full_full_perms.reshape((len(test_states), -1, full_perms.shape[-1])):
            negs = np.where(full_perms < 0)[0]
            comp = np.setdiff1d(np.arange(len(full_perms)), negs)
            full_perms = full_perms[comp,]
            bleeep.append(full_perms)

        self.assertEquals(len(test_states), len(test_perms2))
        self.assertEquals(len(test_states), len(test_inds2))
        self.assertEquals(
            [len(x) for x in test_perms2],
            [len(x) for x in bleeep]
        )

        for i in range(len(test_states)):
            self.assertEquals(len(test_perms2[i]), len(test_inds2[i]), msg='failed for state {}'.format(test_states[i]))
            self.assertEquals(len(test_perms2[i]), len(bleeep[i]), msg='failed for state {}'.format(test_states[i]))
            self.assertEquals(sorted(test_perms2[i].tolist()), sorted(bleeep[i].tolist()), msg='failed for state {}'.format(test_states[i]))
            self.assertEquals(sorted(test_inds2[i].tolist()), sorted(gen.to_indices(bleeep[i]).tolist()), msg='failed for state {}'.format(test_states[i]))

    @validationTest
    def test_DirectSumIndices(self):
        """
        Tests the features of the symmetric group generator
        :return:
        :rtype:
        """

        gen = SymmetricGroupGenerator(1)
        test_states = [
            [0],
            [1],
            [2],
            [3],
            [4]
        ]
        test_rules = [
            (-3,), (-1,), (1,), (3,), (-2, -1), (-2, 1), (-1, 2), (1, 2),
            (-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (1, 1, 1)
        ]
        new_exc, new_inds = gen.take_permutation_rule_direct_sum(test_states, test_rules,
                                                                              return_indices=True,
                                                                              split_results=True)

        self.assertEquals(new_exc[0].shape, (2, 1))

        test_states = gen.get_terms(range(3), flatten=True)
        test_rules = [
            [2], [-2], [-3], [1, 1], [-1, -1], [-1, 1], [-1, -1, 1]
        ]

        with BlockProfiler("direct inds", print_res=False):
            test_perms, test_inds = gen.take_permutation_rule_direct_sum(
                test_states,
                test_rules,
                return_indices=True,
                indexing_method='direct',
                split_results=True,
                preserve_ordering=False
            )


        blub = np.array([x for x in test_rules if len(x) == 1])
        for i in range(len(test_states)):
            why = test_states[i][np.newaxis, :] + blub
            why = why[why>=0].reshape(-1, 1)
            self.assertEquals(test_perms[i].tolist(), why.tolist())


        gen = SymmetricGroupGenerator(10)

        test_states = gen.get_terms(range(3), flatten=True)
        test_rules = [
            [2], [-2], [-3], [1, 1], [-1, -1], [-1, 1], [-1, -1, 1]
        ]
        with BlockProfiler("direct inds", print_res=False):
            test_perms, test_inds = gen.take_permutation_rule_direct_sum(
                test_states,
                test_rules,
                return_indices=True,
                indexing_method='direct',
                split_results=True,
                preserve_ordering=False,
                # logger=Logger()
            )

        with BlockProfiler("secondary inds", print_res=False):
            test_perms2, test_inds2 = gen.take_permutation_rule_direct_sum(
                test_states,
                test_rules,
                return_indices=True,
                indexing_method='secondary',
                split_results=True,
                preserve_ordering=False
            )

        self.assertEquals(test_inds[0].tolist(), test_inds2[0].tolist())

        u_tests = np.unique(test_perms[1], axis=0)

        test_states = gen.get_terms(range(1), flatten=True)
        bleeeh, _, filter = gen.take_permutation_rule_direct_sum(
                test_states,
                test_rules,
                return_indices=True,
                split_results=False,
                filter_perms=[
                    u_tests
                ],
                return_filter=True
            )

        bleeeh, _ = nput.unique(bleeeh)
        contained, _, _ = nput.contained(bleeeh, u_tests, invert=True)

        self.assertFalse(contained.any(),
                        msg='{} not in {}; {} in'.format(bleeeh[contained], u_tests, bleeeh[np.logical_not(contained)])
                        )
        self.assertTrue(isinstance(filter.sums, np.ndarray))

        # self.assertEquals(np.unique(bleeeh, axis=0).tolist(), u_tests.tolist())

    @validationTest
    def test_DirectSumExtra(self):
        """
        Tests the features of the symmetric group generator
        :return:
        :rtype:
        """

        # there was a crash from an improperly handled duplicate state
        gen = SymmetricGroupGenerator(6)

        # raise Exception(
        # #     gen.from_indices([778, 779, 779, 779])
        # # )
        #
        # just making sure no crashes
        test_inds = [200, 758, 203, 204, 780, 769, 781, 770, 779, 779, 782,]
        p = gen.from_indices(test_inds)
        self.assertEquals(gen.to_indices(p).tolist(), test_inds)

        test_inds = [ 200, 758, 203, 204, 780, 769, 781, 770, 779, 779, 782,
                     904, 904, 911, 901, 901, 915, 914, 2808, 789, 796, 794,
                     797, 795, 798, 895, 896, 2844, 2824, 2825, 897, 2828, 2838,
                     2906, 2835, 2839, 2913, 2907, 2833, 2836, 2918, 2914, 2840, 2908,
                     2877, 2834, 2837, 2919, 2915, 2909, 2990, 199, 757, 202, 766,
                     768, 768, 777, 777, 903, 903, 912, 2807, 788, 791, 793,
                     894, 2843, 2823, 2827, 2830, 2875, 2832, 2991, 197, 755, 745,
                     761, 764, 906, 906, 909, 198, 756, 201, 771, 746, 765,
                     774, 774, 767, 767, 776, 776, 902, 902, 913, 898, 898,
                     917, 787, 790, 792, 893, 2826, 2829, 2831, 196, 754, 744,
                     760, 763, 905, 905, 910, 195, 753, 743, 759, 762, 907,
                     908
                     ]
        # just making sure no crashes
        p = gen.from_indices(test_inds)
        self.assertEquals(gen.to_indices(p).tolist(), test_inds)

        basic_exc, _ = gen.take_permutation_rule_direct_sum(
                [
                    [1, 0, 0, 0, 0, 2],
                    [2, 0, 0, 4, 0, 0]
                ],
                [(-1,), (1,)],
                return_indices=True,
                split_results=True
            )

        test_states = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [2, 2, 1, 0, 1, 0],
            [3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0],
            [0, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 3],
            [1, 2, 0, 0, 0, 0],
            [1, 0, 2, 0, 0, 0],
            [1, 0, 0, 2, 0, 0],
            [1, 0, 0, 0, 2, 0],
            [1, 0, 0, 0, 0, 2],
            [2, 1, 0, 0, 0, 0],
            [2, 2, 1, 1, 0, 0],
            [2, 2, 1, 0, 1, 0],
            [2, 2, 1, 0, 0, 1],
            [0, 0, 1, 1, 1, 1]
        ]
        test_rules = [(-1,), (1,)]

        filter_perms = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 2, 0],
            [0, 0, 0, 2, 0, 0]
        ]
        filter_inds = gen.to_indices(filter_perms)#[0, 6, 5, 4, 3, 2, 1, 12, 11, 10]
        wat = gen.from_indices(filter_inds)
        self.assertEquals(
            wat.tolist(),
            filter_perms
        )

        # test that basic application works
        subtest = np.array(test_states)
        test_perms, test_inds = gen.take_permutation_rule_direct_sum(
            subtest,
            test_rules,
            return_indices=True,
            split_results=True
        )
        bleh = np.concatenate(
            [UniquePermutations(x + (0,) * (6 - len(x))).permutations() for x in test_rules],
            axis=0
        )
        full_perms = subtest[:, np.newaxis, :] + bleh[np.newaxis, :, :]
        nonneg_perms = []
        for f in full_perms:
            # full_perms = full_perms.reshape((-1, full_perms.shape[-1]))
            neg_pos = np.where(f < 0)[0]
            comp = np.setdiff1d(np.arange(len(f)), neg_pos)
            f = f[comp,]
            nonneg_perms.append(f)
        for i in range(len(test_states)):
            self.assertEquals(list(sorted(test_perms[i].tolist())),
                              list(sorted(nonneg_perms[i].tolist())),
                              msg='bad for {}'.format(test_states[i])
                              )

        # test that filtering is working
        bleeeh, _, filter = gen.take_permutation_rule_direct_sum(
                test_states,
                test_rules,
                return_indices=True,
                split_results=True,
                filter_perms=[filter_perms, filter_inds],
                return_filter=True,
                # logger=Logger()
            )

        self.assertEquals(len(bleeeh), len(test_states))
        for i in range(len(test_states)):
            woof = list(test_states[i])
            woof[0] += 1
            if woof in filter_perms:
                self.assertIn(
                    woof,
                    bleeeh[i].tolist()
                )
            else:
                self.assertNotIn(
                    woof,
                    bleeeh[i].tolist()
                )
        # self.assertEquals(len(bleeeh), len(test_states))

        nonneg_perms = []
        for f in full_perms:
            # full_perms = full_perms.reshape((-1, full_perms.shape[-1]))
            neg_pos = np.where(f < 0)[0]
            comp = np.setdiff1d(np.arange(len(f)), neg_pos)
            f = f[comp,]
            cont_terms, _, _ = nput.contained(f, filter_perms)
            nonneg_perms.append(f[cont_terms,])
        for i in range(len(test_states)):
            # print(">>>", test_states[i])
            # print(bleeeh[i])
            # print(".")
            # print(nonneg_perms[i])
            # print("-"*50)
            self.assertEquals(list(sorted(bleeeh[i].tolist())),
                              list(sorted(nonneg_perms[i].tolist())),
                              msg='bad for {}'.format(test_states[i])
                              )

        bleeeh2, _, filter = gen.take_permutation_rule_direct_sum(
            test_states,
            test_rules,
            return_indices=True,
            split_results=True,
            filter_perms=filter_perms,
            return_filter=True
        )

        self.assertEquals(filter.inds.tolist(), np.sort(filter_inds).tolist())
        self.assertEquals(filter.perms.tolist(), filter_perms)
        self.assertEquals([b.tolist() for b in bleeeh2], [b.tolist() for b in bleeeh])

        bleeeh, _, filter = gen.take_permutation_rule_direct_sum(
            test_states,
            test_rules,
            return_indices=True,
            split_results=True,
            filter_perms=filter_inds,
            return_filter=True
        )
        self.assertEquals(filter.inds.tolist(), np.sort(filter_inds).tolist())

        for i in range(len(test_states)):
            self.assertEquals(bleeeh2[i].tolist(), bleeeh[i].tolist(), msg='failed for state {}'.format(test_states[i]))

        test_states = [[1, 1, 0, 0, 1, 1],
                       [1, 3, 0, 0, 1, 1],
                       [1, 0, 1, 0, 1, 1],
                       [1, 0, 0, 1, 1, 1],
                       [1, 0, 0, 3, 1, 1],
                       [1, 1, 0, 0, 3, 1],
                       [1, 0, 0, 1, 3, 1],
                       [1, 1, 0, 0, 1, 3],
                       [1, 0, 1, 0, 1, 3],
                       [1, 0, 1, 0, 1, 0],
                       [1, 0, 0, 1, 1, 3],
                       [1, 1, 2, 0, 1, 1],
                       [1, 1, 2, 0, 1, 1],
                       [1, 1, 0, 2, 1, 1],
                       [1, 2, 0, 1, 1, 1],
                       [1, 2, 0, 1, 1, 1],
                       [1, 0, 1, 2, 1, 1],
                       [1, 0, 2, 1, 1, 1],
                       [3, 1, 2, 0, 1, 1],
                       [0, 1, 3, 0, 1, 1]]
        filter_inds = [0, 6, 5, 4, 3, 2, 1, 12, 11, 10, 9, 8, 7, 27, 26, 24, 21, 17, 25, 23]

        bleeeh, bleeh_inds, filter = gen.take_permutation_rule_direct_sum(
            test_states,
            test_rules,
            return_indices=True,
            split_results=True,
            filter_perms=filter_inds,
            return_filter=True
        )
        self.assertEquals(filter.inds.tolist(), np.sort(filter_inds).tolist())

        for i in range(len(test_states)):
            self.assertEquals(
                gen.to_indices(bleeeh[i]).tolist(), bleeh_inds[i].tolist(),
                msg='failed for state {}'.format(test_states[i])
            )
            conts = nput.contained(bleeh_inds[i], filter.inds, invert=True)[0]
            self.assertFalse(
                conts.any(),
                msg='failed for state {}: (failed with {}/{})'.format(
                    test_states[i],
                    bleeeh[i][conts],
                    bleeh_inds[i][conts]
                )
            )

    @inactiveTest
    def test_DirectSumExclusion(self):
        """
        Tests the features of the symmetric group generator
        :return:
        :rtype:
        """

        # there was a crash from an improperly handled duplicate state
        gen = SymmetricGroupGenerator(6)

        # raise Exception(
        # #     gen.from_indices([778, 779, 779, 779])
        # # )
        #
        # just making sure no crashes
        test_inds = [200, 758, 203, 204, 780, 769, 781, 770, 779, 779, 782, ]
        p = gen.from_indices(test_inds)
        self.assertEquals(gen.to_indices(p).tolist(), test_inds)

        test_inds = [200, 758, 203, 204, 780, 769, 781, 770, 779, 779, 782,
                     904, 904, 911, 901, 901, 915, 914, 2808, 789, 796, 794,
                     797, 795, 798, 895, 896, 2844, 2824, 2825, 897, 2828, 2838,
                     2906, 2835, 2839, 2913, 2907, 2833, 2836, 2918, 2914, 2840, 2908,
                     2877, 2834, 2837, 2919, 2915, 2909, 2990, 199, 757, 202, 766,
                     768, 768, 777, 777, 903, 903, 912, 2807, 788, 791, 793,
                     894, 2843, 2823, 2827, 2830, 2875, 2832, 2991, 197, 755, 745,
                     761, 764, 906, 906, 909, 198, 756, 201, 771, 746, 765,
                     774, 774, 767, 767, 776, 776, 902, 902, 913, 898, 898,
                     917, 787, 790, 792, 893, 2826, 2829, 2831, 196, 754, 744,
                     760, 763, 905, 905, 910, 195, 753, 743, 759, 762, 907,
                     908
                     ]
        # just making sure no crashes
        p = gen.from_indices(test_inds)
        self.assertEquals(gen.to_indices(p).tolist(), test_inds)

        basic_exc, _ = gen.take_permutation_rule_direct_sum(
            [
                [1, 0, 0, 0, 0, 2],
                [2, 0, 0, 4, 0, 0]
            ],
            [(-1,), (1,)],
            return_indices=True,
            split_results=True,
            excluded_permutations=[
                [0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0]
            ]
        )
        raise Exception(basic_exc)

        test_states = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [2, 2, 1, 0, 1, 0],
            [3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0],
            [0, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 3],
            [1, 2, 0, 0, 0, 0],
            [1, 0, 2, 0, 0, 0],
            [1, 0, 0, 2, 0, 0],
            [1, 0, 0, 0, 2, 0],
            [1, 0, 0, 0, 0, 2],
            [2, 1, 0, 0, 0, 0],
            [2, 2, 1, 1, 0, 0],
            [2, 2, 1, 0, 1, 0],
            [2, 2, 1, 0, 0, 1],
            [0, 0, 1, 1, 1, 1]
        ]
        test_rules = [(-1,), (1,)]

        filter_perms = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 2, 0],
            [0, 0, 0, 2, 0, 0]
        ]
        filter_inds = gen.to_indices(filter_perms)  # [0, 6, 5, 4, 3, 2, 1, 12, 11, 10]
        wat = gen.from_indices(filter_inds)
        self.assertEquals(
            wat.tolist(),
            filter_perms
        )

        # test that basic application works
        subtest = np.array(test_states)
        test_perms, test_inds = gen.take_permutation_rule_direct_sum(
            subtest,
            test_rules,
            return_indices=True,
            split_results=True
        )
        bleh = np.concatenate(
            [UniquePermutations(x + (0,) * (6 - len(x))).permutations() for x in test_rules],
            axis=0
        )
        full_perms = subtest[:, np.newaxis, :] + bleh[np.newaxis, :, :]
        nonneg_perms = []
        for f in full_perms:
            # full_perms = full_perms.reshape((-1, full_perms.shape[-1]))
            neg_pos = np.where(f < 0)[0]
            comp = np.setdiff1d(np.arange(len(f)), neg_pos)
            f = f[comp,]
            nonneg_perms.append(f)
        for i in range(len(test_states)):
            self.assertEquals(list(sorted(test_perms[i].tolist())),
                              list(sorted(nonneg_perms[i].tolist())),
                              msg='bad for {}'.format(test_states[i])
                              )

        # test that filtering is working
        bleeeh, _, filter = gen.take_permutation_rule_direct_sum(
            test_states,
            test_rules,
            return_indices=True,
            split_results=True,
            filter_perms=[filter_perms, filter_inds],
            return_filter=True,
            # logger=Logger()
        )

        self.assertEquals(len(bleeeh), len(test_states))
        for i in range(len(test_states)):
            woof = list(test_states[i])
            woof[0] += 1
            if woof in filter_perms:
                self.assertIn(
                    woof,
                    bleeeh[i].tolist()
                )
            else:
                self.assertNotIn(
                    woof,
                    bleeeh[i].tolist()
                )
        # self.assertEquals(len(bleeeh), len(test_states))

        nonneg_perms = []
        for f in full_perms:
            # full_perms = full_perms.reshape((-1, full_perms.shape[-1]))
            neg_pos = np.where(f < 0)[0]
            comp = np.setdiff1d(np.arange(len(f)), neg_pos)
            f = f[comp,]
            cont_terms, _, _ = nput.contained(f, filter_perms)
            nonneg_perms.append(f[cont_terms,])
        for i in range(len(test_states)):
            # print(">>>", test_states[i])
            # print(bleeeh[i])
            # print(".")
            # print(nonneg_perms[i])
            # print("-"*50)
            self.assertEquals(list(sorted(bleeeh[i].tolist())),
                              list(sorted(nonneg_perms[i].tolist())),
                              msg='bad for {}'.format(test_states[i])
                              )

        bleeeh2, _, filter = gen.take_permutation_rule_direct_sum(
            test_states,
            test_rules,
            return_indices=True,
            split_results=True,
            filter_perms=filter_perms,
            return_filter=True
        )

        self.assertEquals(filter.inds.tolist(), np.sort(filter_inds).tolist())
        self.assertEquals(filter.perms.tolist(), filter_perms)
        self.assertEquals([b.tolist() for b in bleeeh2], [b.tolist() for b in bleeeh])

        bleeeh, _, filter = gen.take_permutation_rule_direct_sum(
            test_states,
            test_rules,
            return_indices=True,
            split_results=True,
            filter_perms=filter_inds,
            return_filter=True
        )
        self.assertEquals(filter.inds.tolist(), np.sort(filter_inds).tolist())

        for i in range(len(test_states)):
            self.assertEquals(bleeeh2[i].tolist(), bleeeh[i].tolist(), msg='failed for state {}'.format(test_states[i]))

        test_states = [[1, 1, 0, 0, 1, 1],
                       [1, 3, 0, 0, 1, 1],
                       [1, 0, 1, 0, 1, 1],
                       [1, 0, 0, 1, 1, 1],
                       [1, 0, 0, 3, 1, 1],
                       [1, 1, 0, 0, 3, 1],
                       [1, 0, 0, 1, 3, 1],
                       [1, 1, 0, 0, 1, 3],
                       [1, 0, 1, 0, 1, 3],
                       [1, 0, 1, 0, 1, 0],
                       [1, 0, 0, 1, 1, 3],
                       [1, 1, 2, 0, 1, 1],
                       [1, 1, 2, 0, 1, 1],
                       [1, 1, 0, 2, 1, 1],
                       [1, 2, 0, 1, 1, 1],
                       [1, 2, 0, 1, 1, 1],
                       [1, 0, 1, 2, 1, 1],
                       [1, 0, 2, 1, 1, 1],
                       [3, 1, 2, 0, 1, 1],
                       [0, 1, 3, 0, 1, 1]]
        filter_inds = [0, 6, 5, 4, 3, 2, 1, 12, 11, 10, 9, 8, 7, 27, 26, 24, 21, 17, 25, 23]

        bleeeh, bleeh_inds, filter = gen.take_permutation_rule_direct_sum(
            test_states,
            test_rules,
            return_indices=True,
            split_results=True,
            filter_perms=filter_inds,
            return_filter=True
        )
        self.assertEquals(filter.inds.tolist(), np.sort(filter_inds).tolist())

        for i in range(len(test_states)):
            self.assertEquals(
                gen.to_indices(bleeeh[i]).tolist(), bleeh_inds[i].tolist(),
                msg='failed for state {}'.format(test_states[i])
            )
            conts = nput.contained(bleeh_inds[i], filter.inds, invert=True)[0]
            self.assertFalse(
                conts.any(),
                msg='failed for state {}: (failed with {}/{})'.format(
                    test_states[i],
                    bleeeh[i][conts],
                    bleeh_inds[i][conts]
                )
            )

    @validationTest
    def test_DirectSumIndicesLarge(self):
        """
        Tests the features of the symmetric group generator
        at scale
        :return:
        :rtype:
        """

        gen = SymmetricGroupGenerator(45)

        test_states = [
            [0]*3 + [1]*2 + [0]*40,
            [0]*4 + [1]*2 + [0]*39,
            [0]*5 + [1]*2 + [0]*38,
            [0]*5 + [2]*2 + [0]*38,
            [0]*5 + [3]*2 + [0]*38,
            [0]*4 + [2]*2 + [0]*39,
        ]
        test_rules = [
            [1, 1], [1, -1], [-1, -1]
        ]
        with BlockProfiler("direct inds", print_res=True):
            test_perms, test_inds = gen.take_permutation_rule_direct_sum(
                test_states,
                test_rules,
                return_indices=True,
                indexing_method='direct',
                split_results=True,
                preserve_ordering=False
            )

        # raise Exception(test_perms)

    @validationTest
    def test_FullBasis(self):

        full_basis = CompleteSymmetricGroupSpace(12)

        self.assertEquals(tuple(full_basis[0]), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEquals(tuple(full_basis[555]), (0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0))
        self.assertEquals(full_basis.find([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0]), 555)
        self.assertEquals(full_basis.find([
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0]
        ]).tolist(), [556, 555])

        full_basis.load_to_sum(11)

        why = np.random.choice(full_basis._basis.shape[0], size=100000)
        ms = np.max(why)
        with BlockProfiler(inactive=True, mode='deterministic'):
            for i in range(100):
                full_basis.take(why, max_size=ms)

        self.assertEquals(full_basis._basis.shape[0], 5200300)
        self.assertEquals(full_basis.find([10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 293930)

    @validationTest
    def test_SelRules(self):

        base_paths = LatticePathGenerator.generate_tree([
                [-1, 1],
                [-1, 1]
            ],
                track_positions=False
            )[-1]

        self.assertEquals(base_paths, [(), (-2,), (2,), (-1, -1), (1, -1), (1, 1)])

        # Simple lattice paths
        gen = LatticePathGenerator([-1, 1], [-1, 1])

        self.assertEquals(gen.tree[0][0], (0, 0))
        self.assertEquals(gen.tree[0][1], [(-2,), (-1, -1)])

        self.assertEquals(gen.tree[1][0], (0, 1))
        self.assertEquals(gen.tree[1][1], [(), (1, -1)])

        gen = LatticePathGenerator([-1, 1], [])
        self.assertEquals(gen.tree[0][0], (0,))
        self.assertEquals(gen.tree[0][1], [(-1,)])

        gen = LatticePathGenerator([-1, 1], [-1, 1, 2])
        self.assertEquals(gen.tree[0][0], (0, 0))
        self.assertEquals(gen.tree[0][1], [(-2,), (-1, -1)])

        self.assertEquals(gen.tree[1][0], (0, 1))
        self.assertEquals(gen.tree[1][1], [(), (1, -1)])

        self.assertEquals(gen.tree[2][0], (0, 2))
        self.assertEquals(gen.tree[2][1], [(1,), (2, -1)])

        self.assertEquals(gen.find_paths(()), [(0, 1), (1, 0)])

        self.assertEquals(gen.find_paths(()), [(0, 1), (1, 0)])

        self.assertEquals(gen.get_path((0, 1)), [(), (1, -1)])
        del gen

        subgen = LatticePathGenerator([-1, 1], [-1, 1])
        # Selection rule products
        gen2 = LatticePathGenerator(subgen.subrules[2], subgen.subrules[1])
        self.assertEquals(gen2.tree[0][0], (0, 0))
        self.assertEquals(gen2.tree[0][1], [(-1,)])

        self.assertEquals(gen2.tree[4][0], (2, 0))
        self.assertEquals(gen2.tree[4][1], [(1,), (2, -1)])

        self.assertEquals(gen2.tree [6][0], (3, 0))
        self.assertEquals(gen2.tree [6][1], [(-2, -1), (-1, -1, -1)])
        self.assertEquals(gen2.steps[0][3], (-1, -1))
        self.assertEquals(gen2.steps[1][0], (-1,))

    @validationTest
    def test_StateGraph(self):

        ndim = 6

        full_basis = CompleteSymmetricGroupSpace(ndim)

        np.random.seed(0)
        inds = np.random.random_integers(0, 1000, 10)
        sample_space = full_basis.take(inds)

        state = self.StateMaker(ndim)

        g = PermutationRelationGraph([
            [state([1, 1]), state([2, 2])],
            [state([3, 1]), state([4, 1])]
        ])

        graph = g.build_state_graph([state([1, 1])])
        self.assertEquals(graph[0].tolist(), [state([1, 1]), state([2, 2])])

        graph = g.build_state_graph([state([1, 2])])
        self.assertEquals(graph[0].tolist(), [state([1, 2]), state([2, 2], [1, 1]), state([2, 4])])

        graph = g.build_state_graph([state([1, 1]), state([1, 2])])
        self.assertEquals([g.tolist() for g in graph],
                          [
                              [state([1, 1]), state([2, 2])],
                              [state([1, 2]), state([2, 2], [1, 1]), state([2, 4])],
                          ])

        graph = g.build_state_graph([state([1, 2]), state([5, 2])])
        self.assertEquals([g.tolist() for g in graph],
                          [
                              [state([1, 2]), state([2, 2], [1, 1]), state([2, 4])],
                              [state([5, 2])]
                          ])

        graph = g.build_state_graph(sample_space, max_iterations=10)

        # raise Exception(graph)

    @validationTest # not sure what I was testing here any more
    def test_BigStateGraph(self):

        ndim = 39
        gen = SymmetricGroupGenerator(ndim)

        state = self.StateMaker(ndim)
        rules = [
            [state(*x) for x in s] for s in [
                [[[39, 1]], [[38, 1]]],
                [[[38, 1]], [[37, 1]]],
                [[[38, 1]], [[36, 1]]],
                [[[37, 1]], [[36, 1]]],
                [[[37, 1]], [[35, 1]]],
                [[[37, 1]], [[34, 1]]],
                [[[36, 1]], [[35, 1]]],
                [[[36, 1]], [[34, 1]]],
                [[[36, 1]], [[33, 1]]],
                # [[[36, 2]], [[34, 2]]],
                [[[35, 1]], [[34, 1]]],
                [[[34, 1]], [[33, 1]]],
                [[[33, 1]], [[32, 1]]],
                [[[33, 1]], [[31, 1]]],
                # [[[32, 1]], [[37, 1], [38, 1]]],
                [[[32, 1]], [[31, 1]]],
                [[[32, 1]], [[30, 1]]],
                [[[31, 1]], [[30, 1]]],
                [[[31, 1]], [[29, 1]]],
                [[[30, 1]], [[29, 1]]],
                # [[[29, 1]], [[34, 1], [36, 1]]],
                # [[[29, 1]], [[31, 1], [39, 1]]],
                [[[29, 1]], [[28, 1]]],
                # [[[28, 1]], [[30, 1], [38, 1]]],
                # [[[28, 1]], [[29, 1], [39, 1]]],
                [[[27, 1]], [[26, 1]]],
                [[[26, 1]], [[25, 1]]],
                [[[26, 1]], [[24, 1]]],
                [[[25, 1]], [[24, 1]]],
                [[[25, 1]], [[23, 1]]],
                [[[25, 1]], [[22, 1]]],
                # [[[24, 1]], [[28, 1], [33, 1]]],
                [[[24, 1]], [[23, 1]]],
                [[[24, 1]], [[22, 1]]],
                # [[[23, 1]], [[26, 1], [39, 1]]],
                [[[23, 1]], [[22, 1]]],
                [[[23, 1]], [[21, 1]]],
                # [[[22, 1]], [[26, 1], [38, 1]]],
                [[[22, 1]], [[21, 1]]],
                [[[20, 1]], [[23, 1], [37, 1]]],
                [[[19, 1]], [[27, 1], [29, 1]]],
                [[[19, 1]], [[20, 1], [39, 1]]],
                [[[19, 1]], [[18, 1]]],
                # [[[16, 2]], [[15, 2]]],
                [[[15, 1]], [[25, 1], [29, 1]]],
                [[[15, 1]], [[14, 1]]],
                [[[14, 1]], [[13, 1]]],
                [[[14, 1]], [[11, 1]]],
                [[[14, 1]], [[10, 1]]],
                [[[13, 1]], [[22, 1], [29, 1]]],
                [[[13, 1]], [[21, 1], [30, 1]]],
                [[[13, 1]], [[19, 1], [37, 1]]],
                # [[[13, 2]], [[12, 2]]],
                # [[[13, 2]], [[11, 2]]],
                # [[[13, 2]], [[10, 2]]],
                [[[12, 1]], [[18, 1], [37, 1]]],
                # [[[12, 2]], [[11, 2]]],
                # [[[12, 2]], [[10, 2]]],
                # [[[11, 2]], [[10, 2]]],
                [[[10, 1]], [[20, 1], [32, 1]]],
                [[[10, 1]], [[19, 1], [36, 1]]],
                # [[[10, 1]], [[15, 1], [39, 1]]],
                [[[9, 1]], [[11, 1], [13, 1]]],
                [[[9, 1]], [[10, 1], [12, 1]]],
                [[[9, 1]], [[7, 1]]],
                [[[9, 1]], [[6, 1]]],
                [[[9, 1]], [[5, 1]]],
                [[[9, 1]], [[4, 1]]],
                # [[[9, 2]], [[8, 2]]],
                [[[8, 1]], [[11, 2]]],
                [[[8, 1]], [[10, 2]]],
                [[[8, 1]], [[7, 1]]],
                [[[8, 1]], [[5, 1]]],
                [[[8, 1]], [[4, 1]]],
                [[[7, 1]], [[5, 1]]],
                # [[[7, 2]], [[6, 2]]],
                # [[[7, 2]], [[5, 2]]],
                # [[[7, 2]], [[4, 2]]],
                [[[6, 1]], [[5, 1]]],
                [[[6, 1]], [[3, 1]]],
                # [[[6, 2]], [[5, 2]]],
                [[[4, 1]], [[3, 1]]]
            ]
        ]

        part_perms = gen.get_terms([1, 2])
        graph = PermutationRelationGraph(rules)

        with np.printoptions(linewidth=10000000):  # infinite line width basically...

            # for g in graph.rels:
            #     print(g[1])
            # raise RuntimeError("nope")

            # new = graph.build_state_graph(part_perms[:1], max_iterations=1, raise_iteration_error=False)
            # print(new)
            # print(part_perms[:1])
            # print(graph.rels[0][1])
            # raise RuntimeError("nope")

            new = graph.build_state_graph(part_perms[:100], max_iterations=1, raise_iteration_error=False)
            raise Exception([len(n) for n in new], sum([len(n) for n in new]))

