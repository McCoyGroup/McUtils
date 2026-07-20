"""
Utilities for working with permutations and permutation indexing
"""
import sys
import numpy as np, time, typing, gc, itertools, math
import collections, functools as ft
from ..Misc import jit, objmode, prange
from ..Numputils import flatten_dtype, unflatten_dtype, difference as set_difference, unique, contained, group_by, split_by_regions, find, infer_int_dtype, vector_take
from ..Scaffolding import NullLogger
__all__ = ['IntegerPartitioner', 'IntegerPartitioner2D', 'UniquePermutations', 'UniqueSubsets', 'UniquePartitions', 'IntegerPartitionPermutations', 'SymmetricGroupGenerator', 'CompleteSymmetricGroupSpace', 'LatticePathGenerator', 'PermutationRelationGraph', 'lehmer_encode', 'lehmer_decode']
_infer_dtype = infer_int_dtype

def _infer_nearest_pos_neg_dtype(og_dtype):
    """
    **LLM Docstring**

    Return the smallest signed integer dtype that can hold the (positive) values of an
    unsigned dtype, so negatives can be represented.

    :param og_dtype: the original dtype
    :return: the nearest signed dtype
    """
    ...

def _as_pos_neg_dtype(ar):
    """
    **LLM Docstring**

    Cast an array to a signed dtype capable of holding negatives (via
    `_infer_nearest_pos_neg_dtype`), returning it unchanged if already signed.

    :param ar: the array
    :type ar: np.ndarray
    :return: the (possibly recast) array
    :rtype: np.ndarray
    """
    ...

def _smaller_counts(perms, i):
    """
    **LLM Docstring**

    For each row, count how many entries after position `i` are smaller than the entry
    at `i` (the Lehmer-code digit for that position).

    :param perms: the permutations, shape `(nperms, ndim)`
    :type perms: np.ndarray
    :param i: the position
    :type i: int
    :return: the per-row counts
    :rtype: np.ndarray
    """
    ...

def lehmer_encode(perms, dtype=None):
    """
    **LLM Docstring**

    Encode permutations as their Lehmer-code integers (a factorial-base ranking),
    choosing an integer or object dtype large enough for the factorials.

    :param perms: the permutations, shape `(..., ndim)`
    :type perms: np.ndarray
    :param dtype: the output dtype (inferred if omitted)
    :return: the Lehmer codes, shape `(...,)`
    :rtype: np.ndarray
    """
    ...

def lehmer_decode(ndim, codes, dtype=None):
    """
    **LLM Docstring**

    Decode Lehmer-code integers back into their permutations (the inverse of
    `lehmer_encode`).

    :param ndim: the permutation length
    :type ndim: int
    :param codes: the Lehmer codes
    :type codes: np.ndarray
    :param dtype: the output dtype
    :return: the permutations, shape `(..., ndim)`
    :rtype: np.ndarray
    """
    ...

class IntegerPartitioner:

    def __init__(self):
        """
        **LLM Docstring**

        Singleton class: instantiation is disallowed (use the classmethods).

        :raises NotImplementedError: always
        """
        ...
    _partition_counts = None

    @classmethod
    def _manage_counts_array(cls, n, M, l):
        """
        **LLM Docstring**

        Ensure the cached 3-D partition-count table is at least `(n, M, l)` in size,
        growing it (over-allocating by 2x to amortize) along whichever axes are too small.

        :param n: the required integer size
        :type n: int
        :param M: the required max-part size
        :type M: int
        :param l: the required max-length size
        :type l: int
        :return: whether the table was grown
        :rtype: bool
        """
        ...

    @classmethod
    def count_partitions(cls, n, M=None, l=None, manage_counts=True, check=True):
        """
        Uses the recurrence relation written out here
        https://en.wikipedia.org/wiki/Partition_(number_theory)#Partitions_in_a_rectangle_and_Gaussian_binomial_coefficients
        We cache the terms as a 2D list-of-lists because we don't need this
        part of the code to be blazingly fast but would like repeats to not
        do unnecessary work (and because the memory cost is small...)

        :param n:
        :type n:
        :param M:
        :type M:
        :param l:
        :type l:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def fill_counts(cls, n, M=None, l=None):
        """
        Fills all counts up to (n, M, l)
        :param n:
        :type n: int
        :param M:
        :type M:
        :param l:
        :type l:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def count_exact_length_partitions(cls, n, M, l, check=True):
        """
        Unexpectedly common thing to want and a non-obvious formula

        :param n:
        :type n:
        :param M:
        :type M:
        :param l:
        :type l:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def count_exact_length_partitions_in_range(cls, n, m, M, l, check=True):
        """
        Returns the partitions with  k > M but length exactly L

        :param n:
        :type n:
        :param M:
        :type M:
        :param l:
        :type l:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def partitions(cls, n, pad=False, return_lens=False, max_len=None, dtype=None):
        """
        Returns partitions in descending lexicographic order
        Adapted from Kelleher to return terms ordered by length and then second in descending
        lex order which while a computationally suboptimal is very natural for a mapping onto
        physical phenomena (and also it's easier for storage)

        :param n: integer to partition
        :type n: int
        :param return_len: whether to return the length or not
        :type return_len:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def partition_indices(cls, parts, sums=None, counts=None, check=True):
        """
        Provides a somewhat quick way to get the index of a set of
        integer partitions.
        Parts must be padded so that all parts are the same length.
        If the sums of the partitions are known ahead of time they may be passed
        Similarly if the numbers of non-zero elements in the partitions are known
        ahead of time they may _also_ be passed

        :param parts:
        :type parts: np.ndarray
        :param sums:
        :type sums: np.ndarray
        :return:
        :rtype:
        """
        ...

class UniqueSubsets:
    """
    Provides unique subsets for an integer partition
    """

    @classmethod
    def num_unique_subsets(cls, k, partition):
        """
        **LLM Docstring**

        Count the number of ways to split `k` symbols into ordered blocks of the given
        sizes (a product of binomial coefficients).

        :param k: the total number of symbols
        :type k: int
        :param partition: the block sizes
        :return: the number of unique subset-splittings
        :rtype: int
        """
        ...

    @classmethod
    def unique_subsets(cls, partition):
        """
        **LLM Docstring**

        Enumerate every way to partition `sum(partition)` symbols into ordered blocks of
        the given sizes, returning them as rows of a storage array (built breadth-first
        via a work queue).

        :param partition: the block sizes
        :return: the enumerated subset-splittings
        :rtype: np.ndarray
        """
        ...

class UniquePermutations:
    """
    Provides permutations for a _single_ integer partition (very important)
    Also provides a classmethod interface to support the case
    where we don't want to instantiate a permutations object for every partition
    """

    def __init__(self, partition):
        """
        **LLM Docstring**

        Set up the unique-permutation generator for a multiset partition, sorting the
        partition into descending order (recording the sorting/inverse) and computing the
        distinct values and their multiplicities.

        :param partition: the multiset (the values to permute)
        :type partition: np.ndarray
        """
        ...

    @classmethod
    def get_permutation_class_counts(cls, partition, sort_by_counts=False):
        """
        **LLM Docstring**

        Return the distinct values of a partition and their multiplicities, sorted by
        value (descending) or by count.

        :param partition: the multiset partition
        :param sort_by_counts: sort by multiplicity rather than by value
        :type sort_by_counts: bool
        :return: `(values, counts)`
        :rtype: tuple
        """
        ...

    @property
    def num_permutations(self):
        """
        Counts the number of unique permutations of the partition
        :param counts:
        :type counts:
        :return:
        :rtype:
        """
        ...
    _binoms = None

    @classmethod
    def get_binoms(cls, n):
        """
        **LLM Docstring**

        Return the cached `Binomial` table, (re)building it if it isn't large enough for
        `n`.

        :param n: the required size
        :type n: int
        :return: the binomial table
        """
        ...

    @classmethod
    def count_permutations(cls, counts):
        """
        Counts the number of unique permutations of the given "counts"
        which correspond to the number of nodes in the unique permutation tree
        :param counts:
        :type counts:
        :return:
        :rtype:
        """
        ...

    def permutations(self, initial_permutation=None, return_indices=False, num_perms=None, position_blocks=None):
        """
        Returns the permutations of the input array
        :param initial_permutation:
        :type initial_permutation:
        :param return_indices:
        :type return_indices:
        :param classes:
        :type classes:
        :param counts:
        :type counts:
        :param num_perms:
        :type num_perms:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_subsequent_permutations(cls, initial_permutation, return_indices=False, classes=None, counts=None, num_perms=None):
        """
        Returns the permutations of the input array
        :return:
        :rtype:
        """
        ...

    @staticmethod
    @jit(nopython=True, cache=True)
    def _fill_permutations_direct_jit(storage, inds, partition, dim):
        """
        Builds off of this algorithm for generating permutations
        in lexicographic order: https://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
        Then we adapt it so that it works in _reverse_ lex order since that's how our partitions come in
        This adaption is done just by pretending the the numbers are all negated so all ordering relations
        flip

        We also make it so a given partition element can only go out to `max_pos`

        :param storage:
        :type storage:
        :param inds:
        :type inds:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def _fill_permutations_direct(cls, storage, inds, partition, dim):
        """
        Builds off of this algorithm for generating permutations
        in lexicographic order: https://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
        Then we adapt it so that it works in _reverse_ lex order since that's how our partitions come in
        This adaption is done just by pretending the the numbers are all negated so all ordering relations
        flip

        :param storage:
        :type storage:
        :param inds:
        :type inds:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def _subtree_counts(total, ndim, counts, where):
        """
        Computes the number of states in the tree built from decrementing counts[where] by 1
        Is it trivially simple? Yes
        But there's power to having it be named.
        :param total:
        :type total:
        :param ndim:
        :type ndim:
        :param counts:
        :type counts:
        :param where:
        :type where:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def _reverse_subtree_counts(subtotal, ndim, counts, j):
        """
        Given subtotal = (total * counts[j]) // ndim
              total    = (subtotal * ndim) // counts[j]
        :return:
        :rtype:
        """
        ...

    def index_permutations(self, perms, assume_sorted=False, preserve_ordering=True):
        """
        Gets permutations indices assuming all the data matches the held stuff
        :param perms:
        :type perms:
        :param assume_sorted:
        :type assume_sorted:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_next_permutation_from_prev(cls, classes, counts, class_map, ndim, cur, prev, prev_index, prev_dim, subtree_counts):
        """
        Pulls the next index by reusing as much info as possible from
        previous index
        Less able to be efficient than computing many indices at once so prefer that if
        possible

        :return:
        :rtype:
        """
        ...

    @staticmethod
    @jit(nopython=True, parallel=True, cache=True)
    def _fill_permutation_indices(inds: np.ndarray, perms: np.ndarray, classes: np.ndarray, counts: np.ndarray, dim: int, num_permutations: int, block_size: int):
        """
        JIT compiled
        :param inds:
        :type inds:
        :param perms:
        :type perms:
        :param diffs:
        :type diffs:
        :param counts:
        :type counts:
        :param counts_mask:
        :type counts_mask:
        :param init_counts:
        :type init_counts:
        :param tree_data:
        :type tree_data:
        :param num_permutations:
        :type num_permutations:
        :param ndim:
        :type ndim:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_permutation_indices(cls, perms, classes=None, counts=None, assume_sorted=False, preserve_ordering=True, dim=None, num_permutations=None, dtype=None, block_size=100):
        """
        Classmethod interface to get indices for permutations
        :param perms:
        :type perms:
        :param assume_sorted:
        :type assume_sorted:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    @jit(nopython=True, cache=True)
    def _fill_permutations_from_indices(perms, indices, counts, classes, dim, num_permutations, block_size):
        """
        **LLM Docstring**

        Fill a block of permutations directly from their (sorted) unique-permutation
        indices, walking a factorial-base tree per block and reusing shared prefixes
        (numba-parallel over blocks).

        :param perms: the output permutation array (filled in place)
        :type perms: np.ndarray
        :param indices: the permutation indices to fill
        :type indices: np.ndarray
        :param counts: the per-class multiplicities
        :type counts: np.ndarray
        :param classes: the distinct values
        :type classes: np.ndarray
        :param dim: the permutation length
        :type dim: int
        :param num_permutations: the total number of unique permutations
        :type num_permutations: int
        :param block_size: the per-block chunk size
        :type block_size: int
        """
        ...

    @classmethod
    def get_permutations_from_indices(cls, classes, counts, indices, assume_sorted=False, preserve_ordering=True, dim=None, num_permutations=None, check_indices=True, no_backtracking=False, block_size=100):
        """
        Classmethod interface to get permutations given a set of indices
        :param perms:
        :type perms:
        :param assume_sorted:
        :type assume_sorted:
        :return:
        :rtype:
        """
        ...

    def permutations_from_indices(self, indices, assume_sorted=False, preserve_ordering=True):
        """
        Gets permutations indices assuming all the data matches the held stuff
        :param perms:
        :type perms:
        :param assume_sorted:
        :type assume_sorted:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_standard_permutation(cls, counts, classes):
        """
        **LLM Docstring**

        Build the canonical (sorted, descending) representative permutation for a set of
        class counts.

        :param counts: the per-class multiplicities
        :type counts: np.ndarray
        :param classes: the distinct values
        :type classes: np.ndarray
        :return: the standard permutation
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    @jit(nopython=True, cache=True)
    def _walk_perm_generator(counts, dim, num_permutations, indices, include_positions):
        """
        **LLM Docstring**

        Generate the unique permutations at a set of indices by walking the factorial-base
        permutation tree, backtracking to the shared prefix between successive indices.

        :param counts: the per-class multiplicities
        :type counts: np.ndarray
        :param dim: the permutation length
        :type dim: int
        :param num_permutations: the total number of unique permutations
        :type num_permutations: int
        :param indices: the indices to generate
        :type indices: np.ndarray
        :param include_positions: also yield the per-class position map
        :type include_positions: bool
        :return: a generator over the permutations
        :rtype: Iterator
        """
        ...

    @classmethod
    def walk_permutation_tree(cls, counts, on_visit, indices=None, dim=None, num_permutations=None, include_positions=False):
        """
        Just a general purpose method that allows us to walk the permutation
        tree built from counts and apply a function every time a node is visited.
        This can be very powerful for building algorithms that need to consider every permutation of
        an object.

        :param counts:
        :type counts:
        :param on_visit:
        :type on_visit:
        :param indices:
        :type indices:
        :param dim:
        :type dim:
        :param num_permutations:
        :type num_permutations:
        :param include_positions:
        :type include_positions:
        """
        ...

    @classmethod
    def descend_permutation_tree_indices(cls, perms, on_visit, classes=None, counts=None, dim=None, assume_sorted=False, num_permutations=None):
        """
        Not sure what to call this exactly, but given that `walk_permutation_tree` maps onto `permutations_from_indices`
        this is the counterpart that basically walks _down_ the way `permutation_indices` would.
        I guess this is basically a BFS type approach of something?

        :param perms:
        :type perms:
        :param assume_sorted:
        :type assume_sorted:
        :return:
        :rtype:
        """
        ...

class IntegerPartitioner2D:
    """
    Provides a tree-based approach to obtain the different integer partitions possible
    when n balls are divided into different numbers of boxes
    """
    partition_data = {}

    @classmethod
    def _enumerate_subtrees(self, new_boxes, new_balls, step):
        """
        **LLM Docstring**

        Enumerate the subtrees for distributing `new_balls` into `new_boxes` after taking
        one step, sorting the balls (and undoing the sort on the results) and dropping
        exhausted (zero-count) balls.

        :param new_boxes: the remaining box capacities
        :param new_balls: the remaining ball counts
        :param step: the step taken to reach this node
        :return: the enumerated subtrees
        :rtype: list
        """
        ...

    @classmethod
    def _get_tree(self, boxes, balls):
        """
        Assumes `boxes` and `balls` are reverse sorted
        """
        ...

    @classmethod
    def get_partitions(cls, boxes, balls):
        """
        **LLM Docstring**

        Enumerate all ways to distribute `balls` into `boxes` (a 2-D integer partition /
        contingency-table enumeration), sorting both descending and undoing the sort on
        the result.

        :param boxes: the box capacities
        :type boxes: np.ndarray
        :param balls: the ball counts
        :type balls: np.ndarray
        :return: the enumerated distributions
        :rtype: np.ndarray
        :raises ValueError: if the ball and box totals differ
        """
        ...

class UniquePartitions:
    """
    Takes partitions of a set of ints with ordering
    """

    def __init__(self, partition):
        """
        **LLM Docstring**

        Set up the unique-partition generator for a multiset, precomputing its unique
        permutations and the per-value "follower" table used to enumerate ordered
        splittings.

        :param partition: the multiset to partition
        :type partition: np.ndarray
        """
        ...

    @classmethod
    def _take_partitions(self, partition, sizes, take_unique=True, split=True, return_partitions=True, return_indices=None, split_indices=None, return_inverse=False, split_inverse=None):
        """
        **LLM Docstring**

        Enumerate the ways to split a partition into blocks of the given sizes, optionally
        returning the partitions, the selection indices, and/or the inverse mapping, and
        optionally deduplicating and splitting the result per block.

        :param partition: the multiset to split
        :type partition: np.ndarray
        :param sizes: the block sizes
        :type sizes: np.ndarray
        :param take_unique: deduplicate the splittings
        :type take_unique: bool
        :param split: split the result per block
        :type split: bool
        :param return_partitions: return the partition values
        :type return_partitions: bool
        :param return_indices: return the selection indices
        :type return_indices: bool | None
        :param split_indices: split the indices per block
        :param return_inverse: return the inverse mapping
        :type return_inverse: bool
        :param split_inverse: split the inverse per block
        :return: the requested partitions/indices/inverse
        :raises ValueError: if nothing is requested or the options are inconsistent
        """
        ...

    @staticmethod
    def _populate_partitions(partition, sizes, tree_sizes, blocks, N, subs, inds):
        """
        :param partition:
        :param tree_sizes:
        :param blocks: blocks of indices to sample from the partition
        :param subs:
        :return:
        """
        ...

    def partitions(self, sizes, take_unique=True, split=True, return_partitions=True, return_indices=False, split_indices=None, return_inverse=False, split_inverse=None):
        """
        **LLM Docstring**

        Enumerate the ways to split this multiset into blocks of the given sizes (a
        front-end to `_take_partitions`).

        :param sizes: the block sizes (must sum to the partition length)
        :param take_unique: deduplicate the splittings
        :type take_unique: bool
        :param split: split the result per block
        :type split: bool
        :param return_partitions: return the partition values
        :type return_partitions: bool
        :param return_indices: return the selection indices
        :type return_indices: bool
        :param split_indices: split the indices per block
        :param return_inverse: return the inverse mapping
        :type return_inverse: bool
        :param split_inverse: split the inverse per block
        :return: the requested partitions/indices/inverse
        :raises ValueError: if the sizes don't sum to the partition length
        """
        ...

class IntegerPartitionPermutations:
    """
    Provides tools for working with permutations of a given integer partition
    """

    def __init__(self, num, dim=None):
        """
        **LLM Docstring**

        Set up the space of all permutations of every integer partition of `num`
        (optionally padded to a fixed dimension), precomputing each partition's class
        counts.

        :param num: the integer being partitioned
        :type num: int
        :param dim: the (padded) permutation length (defaults to `num`)
        :type dim: int | None
        """
        ...

    @property
    def num_elements(self):
        """
        **LLM Docstring**

        The total number of partition permutations in the space.

        :return: the number of elements
        :rtype: int
        """
        ...

    def get_partition_permutations(self, return_indices=False, dtype=None, flatten=False):
        """


        :return:
        :rtype:
        """
        ...

    def _get_partition_splits(self, perms, assume_sorted=False, assume_standard=False, split_method='direct', check_partition_counts=True):
        """

        :param perms:
        :type perms:
        :param split_method:
        :type split_method:
        :return:
        :rtype:
        """
        ...

    def get_full_equivalence_class_data(self, perms, split_method='direct', assume_sorted=False, assume_standard=False, return_permutations=False, check_partition_counts=True):
        """
        Returns the equivalence class data of the given permutations
        :param perms:
        :type perms:
        :param split_method:
        :type split_method:
        :return:
        :rtype:
        """
        ...

    def get_equivalence_classes(self, perms, split_method='direct', assume_sorted=False, return_permutations=True, check_partition_counts=True):
        """
        Returns the equivalence classes and permutations of the given permutations
        :param perms:
        :type perms:
        :param split_method:
        :type split_method:
        :return:
        :rtype:
        """
        ...

    def get_partition_permutation_indices(self, perms, assume_sorted=False, preserve_ordering=True, assume_standard=False, check_partition_counts=True, dtype=None, split_method='direct'):
        """
        Assumes the perms all add up to the stored int
        They're then grouped by partition index and finally
        Those are indexed

        :param perms:
        :type perms:
        :return:
        :rtype:
        """
        ...

    def get_partition_permutations_from_indices(self, indices, assume_sorted=False, preserve_ordering=True):
        """
        Assumes the perms all add up to the stored int
        They're then grouped by partition index and finally
        Those are indexed

        :param perms:
        :type perms:
        :return:
        :rtype:
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the integer, dimension, and element count.

        :return: the representation
        :rtype: str
        """
        ...

class EmptyIntegerPartitionPermutations(IntegerPartitionPermutations):

    def __init__(self, num, dim=None):
        """
        **LLM Docstring**

        Set up the degenerate partition-permutation space for `num == 0` (a single
        all-zero permutation).

        :param num: the integer (zero)
        :type num: int
        :param dim: the permutation length
        :type dim: int | None
        """
        ...

    def get_partition_permutations(self, return_indices=False, dtype=None):
        """


        :return:
        :rtype:
        """
        ...

    def get_partition_permutation_indices(self, perms, assume_sorted=None, preserve_ordering=None, assume_standard=None, check_partition_counts=None, dtype=None, split_method=None):
        """

        :param perms:
        :type perms:
        :param split_method:
        :type split_method:
        :return:
        :rtype:
        """
        ...

    def get_partition_permutations_from_indices(self, indices, assume_sorted=None, preserve_ordering=None):
        """

        :param indices:
        :type indices:
        :param assume_sorted:
        :type assume_sorted:
        :return:
        :rtype:
        """
        ...

    def _get_partition_splits(self, perms, assume_sorted=None, assume_standard=None, check_partition_counts=None, split_method=None):
        """

        :param perms:
        :type perms:
        :param split_method:
        :type split_method:
        :return:
        :rtype:
        """
        ...

class SymmetricGroupGenerator:
    """
    I don't know what to call this.
    Manages elements of the symmetric group up to arbitrary size.
    Basically just exists to merge all of the prior integer partition/permutation stuff over many integers
    which makes it easier to calculate direct products of terms
    """

    def __init__(self, dim):
        """
        :param dim: the padding length of every term (needed for consistency reasons)
        :type dim: int
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the dimension.

        :return: the representation
        :rtype: str
        """
        ...

    def _get_partition_perms(self, iterable, ignore_negatives=False):
        """
        returns IntegerPartitionPermutation objects and cum totals for the provided quanta

        :param iterable:
        :type iterable:
        :return:
        :rtype: Tuple[List[IntegerPartitionPermutations], List]
        """
        ...

    def load_to_size(self, size):
        """
        **LLM Docstring**

        Generate partition permutations until the cumulative element count covers `size`.

        :param size: the target cumulative size
        :type size: int
        """
        ...

    def get_terms(self, n, flatten=True):
        """
        Returns permutations of partitions
        :param n:
        :type n:
        :return:
        :rtype:
        """
        ...

    def num_terms(self, n):
        """
        **LLM Docstring**

        Return the number of partition permutations at each requested integer sum.

        :param n: the integer sum(s)
        :return: the per-sum element counts
        :rtype: list
        """
        ...

    def to_indices(self, perms, sums=None, assume_sorted=False, assume_standard=False, check_partition_counts=True, preserve_ordering=True, dtype=None):
        """
        Gets the indices for the given permutations.
        First splits by sum then allows the held integer partitioners to do the rest
        :param perms:
        :type perms:
        :return:
        :rtype:
        """
        ...

    def from_indices(self, indices, assume_sorted=False, preserve_ordering=True):
        """
        Gets the permutations for the given indices.
        First splits into by which integer partitioner is the generator and lets
        the partitioner do the rest

        :param perms:
        :type perms:
        :return:
        :rtype:
        """
        ...

    class direct_sum_filter:

        def __init__(self, perms, inds):
            """
            **LLM Docstring**

            Hold a filter over permutations for the direct-sum construction, indexing the
            allowed indices by their permutation sum for fast pre-screening.

            :param perms: the filter permutations (or `None`)
            :param inds: the allowed indices
            """
            ...

        @classmethod
        def from_perms(cls, parent, filter_perms):
            """
            **LLM Docstring**

            Build a filter from a set of permutations, resolving them to indices via the
            parent generator.

            :param parent: the owning generator
            :param filter_perms: the filter permutations
            :return: the filter
            """
            ...

        @classmethod
        def from_inds(cls, inds):
            """
            **LLM Docstring**

            Build a filter directly from a set of indices (no permutations).

            :param inds: the allowed indices
            :return: the filter
            """
            ...

        @classmethod
        def from_data(cls, parent, filter_perms):
            """
            **LLM Docstring**

            Build a filter from flexible input (an existing filter, permutations, indices, or
            a `(perms, inds)` pair), inferring the structure.

            :param parent: the owning generator
            :param filter_perms: the filter data
            :return: the filter (or `None`)
            """
            ...

    @staticmethod
    @jit(nopython=True, cache=True)
    def _get_filter_mask(new_rep_perm, cls_inds, can_be_negative, class_negs):
        """
        **LLM Docstring**

        Build a boolean mask over a class's indices that drops entries which would produce
        a negative in one of the positions that can go negative.

        :param new_rep_perm: the candidate representative permutations
        :param cls_inds: the class indices
        :param can_be_negative: the positions that may go negative
        :param class_negs: the per-position negative-index sets
        :return: the keep mask
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    @jit(nopython=True, cache=True)
    def _filter_negs_by_comp(comp, not_negs, idx, idx_starts, mask, perm_counts, start, end):
        """
        **LLM Docstring**

        Apply a negative-filtering mask to the storage mask and decrement the affected
        per-permutation counts.

        :param comp: the surviving indices
        :param not_negs: the keep mask
        :param idx: the class index
        :param idx_starts: the per-block storage offsets
        :param mask: the storage mask (modified in place)
        :param perm_counts: the per-permutation counts (modified in place)
        :param start: the block start
        :param end: the block end
        """
        ...

    @classmethod
    def _filter_negatives_perms(cls, i, idx, idx_starts, perms, new_rep_perm, storage, ndim, cls_inds, class_negs, perm_counts, cum_counts, mask, can_be_negative, full_rep_changes, changed_positions):
        """
        **LLM Docstring**

        Filter out the permutations in a class that would introduce negatives, updating
        the storage mask and counts accordingly.

        :param i: the class position
        :param idx: the class index
        :param idx_starts: the per-block storage offsets
        :param perms: the source permutations
        :param new_rep_perm: the candidate representative permutations
        :param storage: the permutation storage
        :param ndim: the permutation length
        :param cls_inds: the per-class index sets
        :param class_negs: the per-position negative-index sets
        :param perm_counts: the per-permutation counts (modified in place)
        :param cum_counts: the cumulative counts
        :param mask: the storage mask (modified in place)
        :param can_be_negative: the positions that may go negative
        :param full_rep_changes: the representative-change bookkeeping
        :param changed_positions: the changed positions
        """
        ...

    @staticmethod
    def _get_standard_perms(perms):
        """
        **LLM Docstring**

        Compute each permutation's class counts and its canonical (standard) representative
        permutation.

        :param perms: the permutations
        :type perms: np.ndarray
        :return: `(class_count_data, standard_representative_perms)`
        :rtype: tuple
        """
        ...

    @classmethod
    def _process_cached_index_blocks(cls, storage, cache, paritioners, indices, filter, mask, perm_counts, merged_sums, inds_dtype=None, full_basis=None):
        """
        **LLM Docstring**

        Process the cached blocks of representative permutations produced during the
        direct-sum walk, resolving each block's permutations to indices (with the
        appropriate partition offsets) and writing them into storage.

        :param storage: the permutation storage
        :param cache: the per-class cached block data
        :type cache: dict
        :param paritioners: the partition permutation generators
        :param indices: the output index array
        :param filter: the direct-sum filter
        :param mask: the storage mask
        :param perm_counts: the per-permutation counts
        :param merged_sums: the merged permutation sums
        :param inds_dtype: the index dtype
        :param full_basis: an optional full basis to resolve against
        """
        ...

    @classmethod
    def changed_index_number(cls, idx, radix):
        """
        **LLM Docstring**

        Encode a set of changed positions as a single mixed-radix integer (a canonical id
        for which positions changed).

        :param idx: the changed positions
        :param radix: the radix (dimension)
        :type radix: int
        :return: the encoded number
        :rtype: int
        """
        ...

    @classmethod
    def _compute_changed_index_numbers(cls, mask):
        """
        **LLM Docstring**

        Encode each row's set of changed positions (from a boolean mask) as a mixed-radix
        integer id.

        :param mask: the per-row changed-position mask
        :type mask: np.ndarray
        :return: the per-row encoded numbers
        :rtype: np.ndarray
        """
        ...

    def _build_direct_sums(self, input_perm_classes, counts, classes, return_indices=False, return_change_positions=False, return_excitations=True, filter_negatives=True, allow_widen_dtypes=True, filter=None, inds_dtype=None, excluded_permutations=None, full_basis=None):
        """
        Creates direct sums of `input_perm_classes` with the unique permutations of `classes` where
        each of the classes has the same counts (just so we don't have to walk the tree as much)
        The `input_perm_classes` are tuples like `(classes, counts, perms)` where the perms are sorted
        which ensures that every subsequent addition is _also_ sorted

        :param input_perm_classes:
        :type perms:
        :param counts:
        :type counts:
        :param classes:
        :type classes:
        :return:
        :rtype:
        """
        ...

    def _get_direct_sum_rule_groups(self, rules, dim, dtype):
        """
        **LLM Docstring**

        Pad and group the direct-sum rules by their class-count structure (first by
        length, then by counts) so matching rules can be applied together.

        :param rules: the direct-sum rules
        :param dim: the permutation length
        :type dim: int
        :param dtype: the rule dtype
        :return: the grouped rule data
        """
        ...

    def get_equivalence_classes(self, perms, sums=None, assume_sorted=False):
        """
        Gets permutation equivalence classes
        :param perms:
        :type perms:
        :param sums:
        :type sums:
        :param assume_sorted:
        :type assume_sorted:
        :return:
        :rtype:
        """
        ...

    def take_permutation_rule_direct_sum(self, perms, rules, sums=None, assume_sorted=False, return_indices=False, return_excitations=True, return_change_positions=False, full_basis=None, split_results=False, excluded_permutations=None, filter_perms=None, filter_negatives=True, return_filter=False, preserve_ordering=True, indexing_method='direct', logger=None):
        """
        Applies `rules` to perms.
        Naively this is just taking every possible permutation of the rules padded to
        get to the appropriate length and then adding that to every element in perms
        and then taking the unique ones.
        We can be more intelligent about how we do this, though, first reducing perms to
        equivalence classes as integer partitions and then making use of that to
        minimize the number of operations we need to do while also ensuring sorting

        :param perms:
        :type perms:
        :param rules:
        :type rules:
        :return:
        :rtype:
        """
        ...

class CompleteSymmetricGroupSpace:
    """
    An object representing a full integer partition-permutation basis
    which will work nominally at any level of excitation
    """
    permutation_dtype = 'int8'

    def __init__(self, dim, memory_constrained=False):
        """
        **LLM Docstring**

        Set up the complete symmetric-group space of a given dimension, backed by a
        `SymmetricGroupGenerator` and a contracted (byte-packed) permutation dtype for
        fast lookups.

        :param dim: the permutation length
        :type dim: int
        :param memory_constrained: avoid materializing the full basis (compute on demand)
        :type memory_constrained: bool
        """
        ...

    @property
    def dim(self):
        """
        **LLM Docstring**

        The permutation length.

        :return: the dimension
        :rtype: int
        """
        ...

    def __getstate__(self):
        """
        **LLM Docstring**

        Return the picklable state (just the dimension; the basis is regenerated).

        :return: the state dict
        :rtype: dict
        """
        ...

    def __setstate__(self, state):
        """
        **LLM Docstring**

        Rebuild the space from its pickled state (reinitializing from the dimension).

        :param state: the state dict
        :type state: dict
        """
        ...

    def _contract_dtype(self, perms):
        """
        **LLM Docstring**

        Byte-pack permutations into the space's contracted lookup dtype (inferring it on
        first use).

        :param perms: the permutations
        :type perms: np.ndarray
        :return: the contracted permutations
        :rtype: np.ndarray
        """
        ...

    def load_to_size(self, size):
        """
        **LLM Docstring**

        Materialize the basis until it holds at least `size` permutations (a no-op when
        memory-constrained).

        :param size: the target basis size
        :type size: int
        :return: `True` if memory-constrained (nothing loaded)
        :rtype: bool | None
        """
        ...

    def load_to_sum(self, max_sum):
        """
        **LLM Docstring**

        Materialize the basis to cover every permutation with sum up to `max_sum`.

        :param max_sum: the maximum permutation sum
        :type max_sum: int
        """
        ...

    def take(self, item, uncoerce=False, max_size=None):
        """
        **LLM Docstring**

        Return the permutation(s) at the given index/indices, loading the basis as needed
        (or generating them directly when memory-constrained), optionally un-packing the
        contracted dtype.

        :param item: the index or indices
        :param uncoerce: un-pack the contracted dtype back to the original
        :type uncoerce: bool
        :param max_size: an explicit max index to load to
        :type max_size: int | None
        :return: the permutation(s)
        :rtype: np.ndarray
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Return the permutation(s) at the given index/indices (delegates to `take`).

        :param item: the index or indices
        :return: the permutation(s)
        :rtype: np.ndarray
        """
        ...

    def find(self, perms, check_sums=True, max_sum=None, search_space_sorting=None):
        """
        **LLM Docstring**

        Return the indices of the given permutations in the space, pre-screening by
        permutation sum and using the contracted-dtype sorted basis for fast lookup (or
        the generator directly when memory-constrained).

        :param perms: the permutations to locate
        :type perms: np.ndarray
        :param check_sums: pre-screen (and load) by permutation sum
        :type check_sums: bool
        :param max_sum: an explicit max sum to load to
        :type max_sum: int | None
        :param search_space_sorting: a precomputed basis sorting to reuse
        :return: the indices
        :rtype: np.ndarray
        """
        ...

class LatticePathGenerator:
    """
    An object to take direct products of lattice paths and
    filter them
    """

    def __init__(self, *steps, max_len=None):
        """
        :param steps: the steps to take a direct product of
        :type steps: Iterable[Iterable[int]]
        """
        ...

    @property
    def subtrees(self):
        """
        **LLM Docstring**

        The per-depth lattice-path subtrees (position-tracking), generated lazily.

        :return: the subtrees
        """
        ...

    @property
    def tree(self):
        """
        **LLM Docstring**

        The final (full-depth) lattice-path tree with positions, generated lazily.

        :return: the tree
        """
        ...

    @property
    def subrules(self):
        """
        **LLM Docstring**

        The per-depth lattice-path rule trees (without position tracking), generated
        lazily.

        :return: the rule subtrees
        """
        ...

    @property
    def rules(self):
        """
        **LLM Docstring**

        The final (full-depth) lattice-path rule tree, generated lazily.

        :return: the rule tree
        """
        ...

    @classmethod
    def generate_tree(self, rules, max_len=None, track_positions=True):
        """
        We take the combo of the specified rules, where we take successive products of 1D rules with the
        current set of rules following the pattern that
            1. a 1D change can apply to any index in an existing rule
            2. a 1D change can be appended to an existing rule

        We ensure at each step that the rules remain sorted & duplicates are removed so as to keep the rule sets compact.
        This is done in simple python loops, because doing it with arrayops seemed harder & not worth it for a relatively cheap operation.

        :param rules:
        :type rules:
        :return:
        :rtype:
        """
        ...

    def find_paths(self, end_spots):
        """
        **LLM Docstring**

        Return the starting steps of every lattice path that reaches one of the given end
        positions.

        :param end_spots: the target end position(s)
        :return: the qualifying starting steps
        :rtype: list
        """
        ...

    def get_path(self, path):
        """
        Pulls the places one can end up after applying the path

        :param other:
        :type other:
        :return:
        :rtype:
        """
        ...

    def find_intersections(self, other):
        """
        Finds the paths that will make self intersect with other

        :param other:
        :type other: LatticePathGenerator
        :return:
        :rtype:
        """
        ...

class PermutationRelationGraph:
    """
    Takes permutations and a set of relations and builds a graph from
    them
    """

    def __init__(self, relations):
        """
        :param relations: sets of rules connecting permutations
        :type relations:
        """
        ...

    @classmethod
    def merge_groups(cls, groups):
        """
        This really needs to be cleaned up...

        :param groups:
        :type groups:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def make_relation_graph(cls, relations):
        """

        :param relations:
        :type relations: Iterable[Iterable[Iterable[int]]]
        :return:
        :rtype:
        """
        ...

    def apply_rels(self, states, max_sum=None):
        """
        For each state checks if it is divisible by one of the group rules and if so applies the
        relevant transformations to it

        :param states:
        :type states:
        :return:
        :rtype:
        """
        ...

    def build_state_graph(self, states, max_sum=None, extra_groups=None, max_iterations=10, raise_iteration_error=True):
        """

        :param states:
        :type states:
        :param max_iterations:
        :type max_iterations:
        :param raise_iteration_error:
        :type raise_iteration_error:
        :return:
        :rtype: Iterable[np.ndarray]
        """
        ...