"""
Provides customized set operations based off of the NumPy builtins
to minimize things like excess sorts
"""
import numpy as np, itertools, math
from .Misc import flatten_dtype, unflatten_dtype, recast_permutation, downcast_index_array, is_numeric
__all__ = ['unique', 'intersection', 'contained', 'difference', 'find', 'fast_first_nonzero', 'fast_first_zero', 'partial_sort', 'argsort', 'group_by', 'group_indices', 'grouping_info', 'take_where_groups', 'split_by_regions', 'combination_indices', 'permutation_indices', 'vector_ix', 'vector_take', 'vector_take_ix', 'index_mask', 'index_complement']
coerce_dtype = flatten_dtype
uncoerce_dtype = unflatten_dtype

def argsort(ar):
    """
    **LLM Docstring**

    Stable argsort that supports multi-dimensional rows by coercing them to a
    compound dtype first.

    Uses a mergesort for stability and down-casts the resulting permutation to a
    minimal dtype.

    :param ar: the array to sort
    :type ar: np.ndarray
    :return: the (down-cast) sort permutation
    :rtype: np.ndarray
    """
    ...

def unique(ar, return_index=False, return_inverse=False, return_counts=False, axis=0, sorting=None, minimal_dtype=False):
    """
    A variant on np.unique with default support for `axis=0` and sorting
    """
    ...

def unique1d(ar, return_index=False, return_inverse=False, return_counts=False, sorting=None, minimal_dtype=False):
    """
    Find the unique elements of an array, ignoring shape.
    """
    ...

def intersection(ar1, ar2, assume_unique=False, return_indices=False, sortings=None, union_sorting=None, minimal_dtype=False):
    """
    **LLM Docstring**

    Compute the intersection of two arrays, supporting multi-dimensional rows.

    For 1D inputs this defers to `intersect1d`; for higher-dimensional inputs the
    rows are coerced to a compound dtype, intersected, and un-coerced back. Indices
    into the inputs can optionally be returned.

    :param ar1: the first array
    :type ar1: np.ndarray
    :param ar2: the second array
    :type ar2: np.ndarray
    :param assume_unique: assume both inputs already contain no duplicates
    :type assume_unique: bool
    :param return_indices: also return the indices of the shared rows
    :type return_indices: bool
    :param sortings: precomputed sortings of the inputs
    :type sortings: tuple | None
    :param union_sorting: precomputed sorting of the concatenated inputs
    :type union_sorting: np.ndarray | None
    :param minimal_dtype: down-cast returned indices to a minimal dtype
    :type minimal_dtype: bool
    :return: the intersection (plus indices if requested)
    :rtype: np.ndarray | tuple
    """
    ...

def intersect1d(ar1, ar2, assume_unique=False, return_indices=False, sortings=None, union_sorting=None, minimal_dtype=False):
    """
    Find the intersection of two arrays.

    """
    ...

def contained(ar1, ar2, assume_unique=False, invert=False, sortings=None, union_sorting=None, method=None):
    """
    Test whether each element of `ar1` is also present in `ar2`.
    """
    ...

def difference(ar1, ar2, assume_unique=False, sortings=None, method=None, union_sorting=None):
    """
    Calculates set differences over any shape of array
    """
    ...

def difference1d(ar1, ar2, assume_unique=False, sortings=None, method=None, union_sorting=None):
    """
    Calculates set differences in 1D
    """
    ...

def find1d(ar, to_find, sorting=None, search_space_sorting=None, return_search_space_sorting=False, check=True, minimal_dtype=False, missing_val='raise'):
    """
    Finds elements in an array and returns sorting
    """
    ...

def find(ar, to_find, sorting=None, search_space_sorting=None, return_search_space_sorting=False, check=True, minimal_dtype=False, missing_val='raise'):
    """
    Finds elements in an array and returns sorting
    """
    ...

def group_by_spec1d(keys, sorting=None, return_sizes=False):
    """
    **LLM Docstring**

    Compute the grouping specification for a set of 1D keys.

    Returns the unique keys, the split offsets that partition the sorting into
    groups, and the sorting itself (optionally the group sizes), so callers can
    split associated data by key without repeated `unique` calls.

    :param keys: the keys to group by
    :type keys: np.ndarray
    :param sorting: precomputed sorting of the keys
    :type sorting: np.ndarray | None
    :param return_sizes: also return the per-group sizes
    :type return_sizes: bool
    :return: `(unique_keys, split_offsets, sorting[, sizes])`
    :rtype: tuple
    """
    ...

def group_by1d(ar, keys, sorting=None, return_sizes=False, return_indices=False):
    """
    Splits an array by a keys
    :param ar:
    :type ar:
    :param keys:
    :type keys:
    :param sorting:
    :type sorting:
    :return:
    :rtype:
    """
    ...

def grouping_info(keys, sorting=None, return_sizes=False):
    """
    Grouping info for keys

    :param keys:
    :type keys:
    :param sorting:
    :type sorting:
    :return: group pairs & sorting info
    :rtype:
    """
    ...

def group_by(ar, keys, sorting=None, return_sizes=False, return_indices=False):
    """
    Groups an array by keys

    :param ar:
    :type ar:
    :param keys:
    :type keys:
    :param sorting:
    :type sorting:
    :return: group pairs & sorting info
    :rtype:
    """
    ...

def group_indices(keys, sorting=None, return_sizes=None, return_indices=None):
    """
    **LLM Docstring**

    Group the positional indices `0..len(keys)-1` by their key values.

    Convenience wrapper over `group_by` that groups a plain `arange` by `keys`.

    :param keys: the keys to group by
    :type keys: np.ndarray
    :param sorting: precomputed sorting of the keys
    :type sorting: np.ndarray | None
    :param return_sizes: also return per-group sizes
    :type return_sizes: bool | None
    :param return_indices: also return grouping indices
    :type return_indices: bool | None
    :return: the grouped indices (plus extras if requested)
    :rtype: tuple
    """
    ...

def split_by_regions1d(ar, regions, sortings=None, return_indices=False):
    """
    :param regions:
    :type regions:
    :param ar1:
    :type ar1:
    :return:
    :rtype:
    """
    ...

def split_by_regions(ar, regions, sortings=None, return_indices=False):
    """
    Splits an array up by edges defined by regions.
    Operates in 1D but can take compound dtypes using lexicographic
    ordering.
    In that case it is on the user to ensure that lex ordering is what is desired.
    :param ar:
    :type ar:
    :param regions:
    :type regions:
    :param sortings:
    :type sortings:
    :return:
    :rtype:
    """
    ...

class version_info:
    numpy_version = None

    @classmethod
    def get_np_version(cls):
        """
        **LLM Docstring**

        Return the installed NumPy version as a tuple of integers, caching the result
        on the class.

        :return: the NumPy version, e.g. `(1, 26, 4)`
        :rtype: tuple[int, ...]
        """
        ...

def from_iter_nd(iter, dtype, shape, like=None, **extra):
    """
    **LLM Docstring**

    Build an n-dimensional array from an iterator of rows, using the fast
    `np.fromiter` path on newer NumPy and an explicit fallback on older versions.

    :param iter: an iterator yielding the rows
    :type iter: Iterator
    :param dtype: element dtype
    :type dtype: np.dtype
    :param shape: full target shape (first axis is the row count)
    :type shape: tuple[int, ...]
    :param like: array-creation callable used in the fallback path
    :type like: Callable | None
    :param extra: extra keyword arguments for `np.fromiter`
    :return: the assembled array
    :rtype: np.ndarray
    """
    ...

def permutation_indices(n, r, dtype=int):
    """
    **LLM Docstring**

    Enumerate all length-`r` ordered permutations of `range(n)` as an index array.

    :param n: size of the pool
    :type n: int
    :param r: length of each permutation
    :type r: int
    :param dtype: index dtype
    :type dtype: np.dtype
    :return: the `(n!/(n-r)!, r)` permutation-index array
    :rtype: np.ndarray
    """
    ...

def combination_indices(n, r, dtype=int):
    """
    **LLM Docstring**

    Enumerate all length-`r` combinations of `range(n)` as an index array.

    :param n: size of the pool
    :type n: int
    :param r: size of each combination
    :type r: int
    :param dtype: index dtype
    :type dtype: np.dtype
    :return: the `(C(n, r), r)` combination-index array
    :rtype: np.ndarray
    """
    ...

def vector_ix(shape, inds, return_shape=False):
    """
    **LLM Docstring**

    Build the fancy-index tuple that addresses positions `inds` within an array of
    shape `shape`, broadcasting over any leading batch dimensions carried by `inds`.

    :param shape: the shape of the array being indexed
    :type shape: int | tuple[int, ...]
    :param inds: the per-axis index arrays (a tuple, or a single array)
    :type inds: tuple | np.ndarray
    :param return_shape: also return the broadcast output shape
    :type return_shape: bool
    :return: the index tuple (and the output shape if requested)
    :rtype: tuple
    """
    ...

def index_mask(shape, inds, complement=False):
    """
    **LLM Docstring**

    Build a boolean mask that is `True` at the given positions (or `False` there
    when `complement` is set).

    :param shape: the shape of the mask
    :type shape: int | tuple[int, ...]
    :param inds: the positions to mark
    :type inds: tuple | np.ndarray
    :param complement: mark everything *except* the given positions
    :type complement: bool
    :return: the boolean mask
    :rtype: np.ndarray
    """
    ...

def index_complement(shape, inds):
    """
    **LLM Docstring**

    Return the index tuple for all positions *not* in `inds` within `shape`.

    Builds the complement mask and reshapes the `where` result to preserve any
    leading batch dimensions.

    :param shape: the shape of the space
    :type shape: int | tuple[int, ...]
    :param inds: the positions to exclude
    :type inds: tuple | np.ndarray
    :return: the complementary index tuple
    :rtype: tuple[np.ndarray, ...]
    """
    ...

def vector_take_ix(base_shape, inds, shared=None):
    """
    **LLM Docstring**

    Build the fancy-index tuple for a broadcasted `take` over a shared batch
    prefix.

    Broadcasts the supplied indices against the array's leading (non-shared) axes
    and hands off to `vector_ix`, so values can be gathered along the trailing axes
    while sharing the first `shared` batch axes.

    :param base_shape: the shape of the array being indexed
    :type base_shape: tuple[int, ...]
    :param inds: the per-axis index arrays
    :type inds: tuple | np.ndarray
    :param shared: number of shared leading batch axes (inferred if omitted)
    :type shared: int | None
    :return: the broadcasted index tuple
    :rtype: tuple
    """
    ...

def vector_take(arr, inds, shared=None, return_spec=False):
    """
    A generalized array indexing that broadcasts properly across everything except for the specified "take" index
    :param arr:
    :param inds:
    :return:
    """
    ...

def take_where_groups(arr, where, presorted=True, return_rows=False):
    """
    **LLM Docstring**

    Gather the values selected by a multi-axis `where` result and split them into
    groups by their leading index.

    When the groups are equal-sized (and presorted) the values are simply reshaped;
    otherwise they are split at the group boundaries. The group row labels can
    optionally be returned alongside.

    :param arr: the array to gather from
    :type arr: np.ndarray
    :param where: a multi-axis `where`-style index tuple
    :type where: tuple[np.ndarray, ...]
    :param presorted: whether the `where` entries are already grouped/sorted
    :type presorted: bool
    :param return_rows: also return the group row labels
    :type return_rows: bool
    :return: the grouped values (and rows if requested)
    :rtype: list | tuple
    """
    ...

def fast_first_nonzero(arr, axis=-1):
    """
    **LLM Docstring**

    Find, for each row, the index of the first nonzero entry along an axis (or
    `-1` if the row is all zeros).

    Uses a byte-view `argmax` trick for speed, so the input must be an integer
    array.

    :param arr: the integer array to scan
    :type arr: np.ndarray
    :param axis: the axis to scan along
    :type axis: int
    :return: the first-nonzero index per row (`-1` where none)
    :rtype: np.ndarray
    """
    ...

def fast_first_zero(arr, axis=-1):
    """
    **LLM Docstring**

    Find, for each row, the index of the first zero entry along an axis (or `-1`
    if the row has no zeros).

    The integer counterpart of `fast_first_nonzero`, using a byte-view trick.

    :param arr: the integer array to scan
    :type arr: np.ndarray
    :param axis: the axis to scan along
    :type axis: int
    :return: the first-zero index per row (`-1` where none)
    :rtype: np.ndarray
    """
    ...

def partial_sort(array, k, return_order=False):
    """
    **LLM Docstring**

    Return the `k` smallest (or, for negative `k`, the `|k|` largest) elements of
    an array in sorted order.

    Uses `np.argpartition` to isolate the partition cheaply, then sorts only that
    slice. The corresponding original indices can optionally be returned.

    :param array: the array to partially sort
    :type array: np.ndarray
    :param k: number of smallest (positive) or largest (negative) elements
    :type k: int
    :param return_order: also return the original indices of the selected elements
    :type return_order: bool
    :return: the sorted partial values (and their indices if requested)
    :rtype: np.ndarray | tuple
    """
    ...