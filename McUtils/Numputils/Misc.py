import numpy as np

__all__ = [
    'infer_inds_dtype',
    'infer_int_dtype',
    'flatten_dtype',
    'unflatten_dtype',
    'recast_permutation',
    'recast_indices',
    'downcast_index_array',
    'numeric_types',
    'is_atomic',
    'is_numeric',
    'is_int',
    'is_zero',
    'is_array_like',
    'is_numeric_array_like',
    'flatten_inds'
]

int_types = (int, np.integer)
float_types = (float, np.floating)
numeric_types = int_types + float_types
atomic_types = numeric_types + (str, )
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
    if types is None: types = atomic_types
    return isinstance(obj, types) or (
            isinstance(obj, np.ndarray) and obj.shape == () and is_atomic(obj[()], types)
    )
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
    if types is None: types = numeric_types
    return is_atomic(obj, types=types)
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
    if types is None: types = int_types
    return is_atomic(obj, types=types)
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
    return is_numeric(obj, types=numeric_types) and obj == 0

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
    if isinstance(obj, np.ndarray):
        if ndim is None:
            return True
        else:
            return obj.ndim == ndim
    elif is_atomic(obj):
        return False
    else:
        try:
            arr = np.asanyarray(obj)
        except ValueError:
            return False
        else:
            if (
                    valid_dtypes is not None
                    and not any(np.issubdtype(arr.dtype, dt) for dt in valid_dtypes)
            ):
                return False
            elif arr.dtype == np.dtype(object):
                return False
            elif ndim is None:
                return True
            else:
                return arr.ndim == ndim
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
    return is_array_like(obj, [np.number], ndim=ndim)

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
    return a.astype(infer_inds_dtype(max_val))

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
    a = np.asanyarray(permutation_array)
    max_val = a.shape[-1]
    return downcast_index_array(a, max_val)

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
    a = np.asanyarray(indexing_array)
    max_val = np.max(a)
    return downcast_index_array(a, max_val)

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
    return np.min_scalar_type(max_size) # reset
    # needed the memory help back...
    # if max_size < 256:
    #     minimal_dtype = 'uint8'
    # elif max_size < 65535:
    #     minimal_dtype = 'uint16'
    # elif max_size < 4294967295:
    #     minimal_dtype = 'uint32'
    # else:
    #     minimal_dtype = 'uint64'
    # return minimal_dtype

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
    return np.min_scalar_type(-(max_dim+1))
    # max_dim = abs(max_dim)
    # if max_dim < 128:
    #     minimal_dtype = 'int8'
    # elif max_dim < 32768:
    #     minimal_dtype = 'int16'
    # elif max_dim < 2147483648:
    #     minimal_dtype = 'int32'
    # else:
    #     minimal_dtype = 'int64'
    # return minimal_dtype

def flatten_dtype(ar, dtype=None):
    """
    Extracted from the way NumPy treats unique
    Coerces ar into a compound dtype so that it can be treated
    like a 1D array for set operations
    """

    # Must reshape to a contiguous 2D array for this to work...
    orig_shape, orig_dtype = ar.shape, ar.dtype
    ar = ar.reshape(orig_shape[0], np.prod(orig_shape[1:], dtype=np.intp))
    ar = np.ascontiguousarray(ar)
    if dtype is None:
        dtype = [('f{i}'.format(i=i), ar.dtype) for i in range(ar.shape[1])]
    # At this point, `ar` has shape `(n, m)`, and `dtype` is a structured
    # data type with `m` fields where each field has the data type of `ar`.
    # In the following, we create the array `consolidated`, which has
    # shape `(n,)` with data type `dtype`.
    try:
        if ar.shape[1] > 0:
            consolidated = ar.view(dtype)
            if len(consolidated.shape) > 1:
                consolidated = consolidated.squeeze()
                if consolidated.shape == ():
                    consolidated = np.expand_dims(consolidated, 0)
        else:
            # If ar.shape[1] == 0, then dtype will be `np.dtype([])`, which is
            # a data type with itemsize 0, and the call `ar.view(dtype)` will
            # fail.  Instead, we'll use `np.empty` to explicitly create the
            # array with shape `(len(ar),)`.  Because `dtype` in this case has
            # itemsize 0, the total size of the result is still 0 bytes.
            consolidated = np.empty(len(ar), dtype=dtype)
    except TypeError:
        # There's no good way to do this for object arrays, etc...
        msg = 'The axis argument to `coerce_dtype` is not supported for dtype {dt}'
        raise TypeError(msg.format(dt=ar.dtype))

    return consolidated, dtype, orig_shape, orig_dtype

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
    n = len(consolidated)
    uniq = consolidated.view(orig_dtype)
    uniq = uniq.reshape(n, *orig_shape[1:])
    if axis is not None:
        uniq = np.moveaxis(uniq, 0, axis)
    return uniq


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
    idx_blocks = [
        (
            (i + A.ndim) if i < 0 else i,
            (j + A.ndim) if j < 0 else j
        )
        for i, j in idx_blocks
    ]
    block_map = {
        i: np.prod(A.shape[i:j+1], dtype=int)
        for i, j in idx_blocks
    }
    new_shape = [
        A.shape[k]
        if not any(i <= k and k <= j for i, j in idx_blocks) else
        block_map.get(k)
        for k in range(A.ndim)
    ]
    new_shape = [s for s in new_shape if s is not None]

    return A.reshape(new_shape)