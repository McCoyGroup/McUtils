"""
A place to store all utilities related to combinatorics.
Currently only contains a subpackage for working with permutations.
That package is used in the `BasisReps` work in `Psience`.

It handles both integer partitions and unique permutations.
It

Might be worth extending to handle more lattice-path stuff.
"""
__all__ = ['IntegerPartitioner', 'IntegerPartitioner2D', 'UniquePermutations', 'UniqueSubsets', 'UniquePartitions', 'IntegerPartitionPermutations', 'SymmetricGroupGenerator', 'CompleteSymmetricGroupSpace', 'LatticePathGenerator', 'PermutationRelationGraph', 'lehmer_encode', 'lehmer_decode', 'StirlingS1', 'Binomial', 'GammaBinomial', 'Factorial', 'prime_sieve', 'prime_factorize', 'prime_iter', 'prime_list', 'stable_factorial_ratio', 'halton_sequence', 'sobol_sequence', 'YoungTableauxGenerator']
from .Permutations import *
from .Sequences import *
from .YoungTableaux import *