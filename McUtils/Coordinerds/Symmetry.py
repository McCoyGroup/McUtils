
from .Internals import permute_internals
from ..Numputils import permutation_cycles

def get_internal_symmetries(internals, permutations):
    cycles = permutation_cycles(permutations, return_groups=True)
    max_cycle_length = max(len(c) for c in cycles)
    internal_sets = []
    