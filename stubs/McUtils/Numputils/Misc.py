import numpy as np
__all__ = ['infer_inds_dtype', 'infer_int_dtype', 'flatten_dtype', 'unflatten_dtype', 'recast_permutation', 'recast_indices', 'downcast_index_array', 'numeric_types', 'is_atomic', 'is_numeric', 'is_int', 'is_zero', 'is_array_like', 'is_numeric_array_like', 'flatten_inds']
int_types = (int, np.integer)
float_types = (float, np.floating)
numeric_types = int_types + float_types
atomic_types = numeric_types + (str,)

def is_atomic(obj, types=None):
    """
    **LLM Docstring**

    Test whether an object is a scalar/atomic value (a number or string, or a
    zero-dimensional array wrapping one).

    :param obj: the object to test
    :type obj: Any
    :param types: the atomic types to accept (defaults to numbers and `str`)
    :type types: tuple | None
    :return: whether the object is atomic
    :rtype: bool
    """
    ...

def is_numeric(obj, types=None):
    """
    **LLM Docstring**

    Test whether an object is a scalar numeric value (int or float, or a
    zero-dimensional numeric array).

    :param obj: the object to test
    :type obj: Any
    :param types: the numeric types to accept (defaults to int/float types)
    :type types: tuple | None
    :return: whether the object is a numeric scalar
    :rtype: bool
    """
    ...

def is_int(obj, types=None):
    """
    **LLM Docstring**

    Test whether an object is a scalar integer (Python or NumPy int, or a
    zero-dimensional integer array).

    :param obj: the object to test
    :type obj: Any
    :param types: the integer types to accept
    :type types: tuple | None
    :return: whether the object is an integer scalar
    :rtype: bool
    """
    ...

def is_zero(obj, numeric_types=None):
    """
    **LLM Docstring**

    Test whether an object is a numeric scalar equal to zero.

    :param obj: the object to test
    :type obj: Any
    :param numeric_types: the numeric types to accept
    :type numeric_types: tuple | None
    :return: whether the object is a numeric zero
    :rtype: bool
    """
    ...

def is_array_like(obj, valid_dtypes=None, ndim=None):
    """
    **LLM Docstring**

    Test whether an object is (or can be coerced into) a numeric-friendly array,
    optionally constraining the dtype and/or number of dimensions.

    Object-dtype arrays and atomic scalars are rejected; anything else is coerced
    with `np.asanyarray` and validated against `valid_dtypes` and `ndim`.

    :param obj: the object to test
    :type obj: Any
    :param valid_dtypes: acceptable dtype super-types (any-match)
    :type valid_dtypes: Iterable | None
    :param ndim: required number of dimensions (any if omitted)
    :type ndim: int | None
    :return: whether the object is array-like under the constraints
    :rtype: bool
    """
    ...

def is_numeric_array_like(obj, ndim=None):
    """
    **LLM Docstring**

    Test whether an object is (or coerces to) a numeric array of the given
    dimensionality.

    Convenience wrapper around `is_array_like` restricted to numeric dtypes.

    :param obj: the object to test
    :type obj: Any
    :param ndim: required number of dimensions (any if omitted)
    :type ndim: int | None
    :return: whether the object is a numeric array
    :rtype: bool
    """
    ...

def downcast_index_array(a, max_val):
    """
    **LLM Docstring**

    Cast an index array down to the smallest dtype that can hold `max_val`.

    :param a: the index array
    :type a: np.ndarray
    :param max_val: the largest value the array needs to represent
    :type max_val: int
    :return: the down-cast array
    :rtype: np.ndarray
    """
    ...

def recast_permutation(permutation_array):
    """
    **LLM Docstring**

    Down-cast a permutation array to the smallest dtype able to index its own
    length.

    Since a permutation of length `n` only holds values `0..n-1`, the dtype is
    chosen from the trailing dimension size.

    :param permutation_array: the permutation(s) to recast
    :type permutation_array: np.ndarray
    :return: the down-cast permutation array
    :rtype: np.ndarray
    """
    ...

def recast_indices(indexing_array):
    """
    **LLM Docstring**

    Down-cast an indexing array to the smallest dtype able to hold its maximum
    value.

    :param indexing_array: the indices to recast
    :type indexing_array: np.ndarray
    :return: the down-cast index array
    :rtype: np.ndarray
    """
    ...

def infer_inds_dtype(max_size):
    """
    **LLM Docstring**

    Choose the smallest unsigned integer dtype that can represent a value up to
    `max_size`.

    :param max_size: the largest (non-negative) value to represent
    :type max_size: int
    :return: the minimal scalar dtype
    :rtype: np.dtype
    """
    ...

def infer_int_dtype(max_dim):
    """
    **LLM Docstring**

    Choose the smallest *signed* integer dtype that can represent dimensions up to
    `max_dim`.

    Uses `np.min_scalar_type` on `-(max_dim + 1)` to force a signed result.

    :param max_dim: the largest dimension to represent
    :type max_dim: int
    :return: the minimal signed scalar dtype
    :rtype: np.dtype
    """
    ...

def flatten_dtype(ar, dtype=None):
    """
    Extracted from the way NumPy treats unique
    Coerces ar into a compound dtype so that it can be treated
    like a 1D array for set operations
    """
    ...

def unflatten_dtype(consolidated, orig_shape, orig_dtype, axis=None):
    """
    Converts a coerced array back to a full array
    :param consolidated:
    :type consolidated:
    :param orig_shape:
    :type orig_shape:
    :param orig_dtype:
    :type orig_dtype:
    :param axis: where to shift the main axis
    :type axis:
    :return:
    :rtype:
    """
    ...

def flatten_inds(A, *idx_blocks):
    """
    **LLM Docstring**

    Reshape an array by collapsing one or more contiguous axis blocks into single
    axes.

    Each `(i, j)` block (negative indices allowed) is fused into one axis of size
    `prod(shape[i:j+1])`, leaving the other axes untouched. This mirrors the index
    bookkeeping used when flattening atom/component blocks.

    :param A: the array to reshape
    :type A: np.ndarray
    :param idx_blocks: `(start, end)` inclusive axis ranges to collapse
    :type idx_blocks: tuple[int, int]
    :return: the reshaped array
    :rtype: np.ndarray
    """
    ...