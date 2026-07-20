import numpy as np, scipy.sparse as sp, itertools as ip, functools as fp, os, abc, gc
import scipy.special
from ..Scaffolding import MaxSizeCache, Logger
from .SetOps import contained, unique as nput_unique, find
from .Misc import infer_inds_dtype, downcast_index_array
__all__ = ['SparseArray', 'ScipySparseArray', 'TensorFlowSparseArray', 'sparse_tensordot']

class SparseArray(metaclass=abc.ABCMeta):
    """
    Represents a generic sparse array format
    which can be subclassed to provide a concrete implementation
    """
    backends = None

    @classmethod
    def get_backends(cls):
        """
        Provides the set of backends to try by default
        :return:
        :rtype:
        """
        ...

    @classmethod
    def from_data(cls, data, shape=None, dtype=None, target_backend=None, constructor=None, **kwargs):
        """
        A wrapper so that we can dispatch to the best
        sparse backend we've got defined.
        Can be monkey patched.

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype: SparseArray
        """
        ...

    @classmethod
    def from_diag(cls, data, shape=None, dtype=None, **kwargs):
        """
        A wrapper so that we can dispatch to the best
        sparse backend we've got defined.
        Can be monkey patched.
        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @classmethod
    @abc.abstractmethod
    def from_diagonal_data(cls, diags, **kw):
        """
        Constructs a sparse tensor from diagonal elements

        :param diags:
        :type diags:
        :param kw:
        :type kw:
        :return:
        :rtype:
        """
        ...

    @property
    @abc.abstractmethod
    def shape(self):
        """
        Provides the shape of the sparse array
        :return:
        :rtype: tuple[int]
        """
        ...

    @property
    def ndim(self):
        """
        Provides the number of dimensions in the array
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def to_state(self, serializer=None):
        """
        Provides just the state that is needed to
        serialize the object
        :param serializer:
        :type serializer:
        :return:
        :rtype:
        """
        ...

    @classmethod
    @abc.abstractmethod
    def from_state(cls, state, serializer=None):
        """
        Loads from the stored state
        :param serializer:
        :type serializer:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def empty(cls, shape, dtype=None, **kw):
        ...

    @classmethod
    @abc.abstractmethod
    def initialize_empty(cls, shp, shape=None, **kw):
        """
        Returns an empty SparseArray with the appropriate shape and dtype
        :param shape:
        :type shape:
        :param dtype:
        :type dtype:
        :param kw:
        :type kw:
        :return:
        :rtype:
        """
        ...

    @property
    @abc.abstractmethod
    def block_data(self):
        """
        Returns the vector of values and corresponding indices
        :return:
        :rtype:
        """
        ...

    @property
    @abc.abstractmethod
    def block_inds(self):
        """
        Returns indices for the stored values
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def transpose(self, axes):
        """
        Returns a transposed version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def ascoo(self):
        """
        Converts the tensor into a scipy COO matrix...
        :return:
        :rtype: sp.coo_matrix
        """
        ...

    @abc.abstractmethod
    def ascsr(self):
        """
        Converts the tensor into a scipy CSR matrix...
        :return:
        :rtype: sp.csr_matrix
        """
        ...

    @abc.abstractmethod
    def asarray(self):
        """
        Converts the tensor into a dense np.ndarray
        :return:
        :rtype: np.ndarray
        """
        ...

    @abc.abstractmethod
    def reshape(self, newshape):
        """
        Returns a reshaped version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def resize(self, newsize):
        """
        Returns a resized version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def pad_right(self, newshape):
        """
        Returns a right-padded version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def broadcast_to(self, shape) -> 'SparseArray':
        """
        Returns a broadcasted version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def expand_and_broadcast_to(self, expansion, new_shape) -> 'SparseArray':
        """
        Expands, then broadcasts (memory efficient)
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def expand_and_pad(self, expansion, padding) -> 'SparseArray':
        """
        Expands, then pads (memory efficient)
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_expanded_shape(cls, shape, axis):
        """
        adapted from np.expand_dims

        :param axis:
        :type axis:
        :return:
        :rtype:
        """
        ...

    def expand_dims(self, axis):
        """
        adapted from np.expand_dims

        :param axis:
        :type axis:
        :return:
        :rtype:
        """
        ...

    def moveaxis(self, start, end):
        """
        Adapted from np.moveaxis

        :param start:
        :type start:
        :param end:
        :type end:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def concatenate(self, *others, axis=0):
        """
        Concatenates multiple SparseArrays along the specified axis
        :return:
        :rtype: SparseArray
        """
        ...

    def __truediv__(self, other):
        ...

    def __rtruediv__(self, other):
        ...

    def __rmul__(self, other):
        ...

    def __mul__(self, other):
        ...

    def _bcast_shapes(self, other):
        ...

    @abc.abstractmethod
    def true_multiply(self, other):
        """
        Multiplies self and other
        :param other:
        :type other:
        :return:
        :rtype: SparseArray
        """
        ...

    def multiply(self, other):
        """
        Multiplies self and other but allows for broadcasting
        :param other:
        :type other: SparseArray | np.ndarray | int | float
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def dot(self, other):
        """
        Takes a regular dot product of self and other
        :param other:
        :type other:
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def outer(self, other):
        """
        Takes a tensor outer product of self and other

        :param other:
        :type other:
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

    def tensordot(self, other, axes=2):
        """
        Takes the dot product of self and other along the specified axes
        :param other:
        :type other:
        :param axes: the axes to contract along
        :type axes: Iterable[int] | Iterable[Iterable[int]]
        :return:
        :rtype:
        """
        ...

    class cacheing_manager:

        def __init__(self, parent, enabled=True, clear=False):
            ...

        def __enter__(self):
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...

    @classmethod
    def cache_options(self, enabled=True, clear=False):
        ...

    @classmethod
    def get_caching_status(cls):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to specify if caching is on or not
        :return:
        :rtype:
        """
        ...

    @classmethod
    def enable_caches(self):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to turn this on
        :return:
        :rtype:
        """
        ...

    @classmethod
    def disable_caches(self):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to turn this off
        :return:
        :rtype:
        """
        ...

    @classmethod
    def clear_cache(self):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to clear this out.
        :return:
        :rtype:
        """
        ...

    class initializer_list(list):
        """
        A simple wrapping head that allows us
        to transfer ownership of initialization data to
        a `SparseArray` during initialization
        """

        def __init__(self, *args):
            ...

class lowmem_csr(sp.csr_matrix):

    def __init__(self, arg1, shape=None, dtype=None, copy=False):
        ...

    def _init_vals(self, indices, indptr, data, idx_dtype, dtype, copy=False):
        ...

    def eval_idx_type(self, indices, indptr, maxval):
        ...

class ScipySparseArray(SparseArray):
    """
    Array class that generalize the regular `scipy.sparse.spmatrix`.
    Basically acts like a high-dimensional wrapper that manages the _shape_ of a standard `scipy.sparse_matrix`, since that is rigidly 2D.
    We always use a combo of an underlying CSR or CSC matrix & COO-like shape operations.
    """

    def __init__(self, a, shape=None, layout=None, dtype=None, initialize=True, cache_block_data=None, logger=None, init_kwargs=None):
        """

        :param a:
        :type a:
        :param shape:
        :type shape:
        :param layout:
        :type layout:
        :param dtype:
        :type dtype:
        :param initialize:
        :type initialize:
        :param cache_block_data: whether or not
        :type cache_block_data:
        :param logger: the logger to use for debug purposes
        :type logger: Logger
        """
        ...

    @classmethod
    def coo_to_cs(cls, shape, vals, ij_inds, memmap=False, assume_sorted=False):
        """
        Reimplementation of scipy's internal "coo_tocsr" for memory-limited situations
        Assumes `ij_inds` are sorted by row then column, which allows vals to be used
        directly once indptr is computed

        :return:
        :rtype:
        """
        ...

    @classmethod
    def _init_cs(cls, vals, indices, indptr, shape):
        ...

    def to_state(self, serializer=None):
        """
        Provides just the state that is needed to
        serialize the object
        :param serializer:
        :type serializer:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def from_state(cls, state, serializer=None):
        ...

    @classmethod
    def initialize_empty(cls, shape, dtype=None, layout=None, **kw):
        ...

    @staticmethod
    def _get_balanced_shape(shp):
        """
        We get a strong memory benefit from having a well-balanced
        matrix, so we do a scan to find the best balancing point
        This works by finding the first spot where the product of the remaining
        inds is less than the first inds and then checking the balance against
        cutting at the previous spot
        :param shp:
        :type shp:
        :return:
        :rtype:
        """
        ...

    def _init_matrix(self, cache_block_data=True, init_kwargs=None):
        ...

    @classmethod
    def construct_sparse_from_val_inds(cls, a, shape, fmt, cache_block_data=True, logger=None, assume_sorted=False):
        ...

    def _validate(self):
        ...

    def _get_shape(self):
        """
        Walks through the array data we're holding onto and determines
        where the sparse blocks start
        """
        ...

    def _get_data(self, non_sparse, sparse):
        """
        We'll take our blocks and arrange them as a vector of sparse arrays
        """
        ...

    def _build_data(self, block_data, inds, total_shape):
        ...

    @property
    def dtype(self):
        ...

    @property
    def diag(self):
        ...

    @classmethod
    def from_diagonal_data(cls, diags, shape=None, **kw):
        ...

    def asarray(self):
        ...

    def todense(self):
        ...

    def ascoo(self):
        ...

    def ascsr(self):
        ...

    def ascsc(self):
        ...

    @property
    def data(self):
        ...

    @data.setter
    def data(self, new):
        ...
    formats_map = {'csr': sp.csr_matrix, 'csc': sp.csc_matrix, 'coo': sp.coo_matrix}

    @classmethod
    def format_from_string(cls, fmt):
        ...

    @property
    def fmt(self):
        ...

    @property
    def shape(self):
        ...

    @property
    def ndim(self):
        ...

    @property
    def non_zero_count(self):
        ...
    default_cache_size = 2
    caching_enabled = True

    @classmethod
    def get_caching_status(cls):
        ...

    @classmethod
    def enable_caches(self):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to turn this on
        :return:
        :rtype:
        """
        ...

    @classmethod
    def disable_caches(self):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to turn this off
        :return:
        :rtype:
        """
        ...

    @classmethod
    def clear_cache(cls):
        ...

    @classmethod
    def clear_ravel_caches(cls):
        ...
    _unravel_cache = MaxSizeCache(default_cache_size)

    @classmethod
    def _unravel_indices(cls, n, dims):
        ...

    @classmethod
    def set_ravel_cache_size(cls, size):
        ...
    _ravel_cache = MaxSizeCache(default_cache_size)

    @classmethod
    def _ravel_indices(cls, mult, dims):
        ...

    def _getinds(self):
        ...

    def find(self):
        ...

    def _load_block_data(self):
        ...

    def _load_full_block_inds(self):
        ...

    def _sort_block_data(self):
        ...

    @property
    def block_vals(self):
        ...

    @block_vals.setter
    def block_vals(self, bv):
        ...

    @property
    def block_inds(self):
        ...

    @block_inds.setter
    def block_inds(self, bi):
        ...

    @property
    def block_data(self):
        ...

    @block_data.setter
    def block_data(self, bd):
        ...

    def transpose(self, transp):
        """
        Transposes the array and returns a new one.
        Not necessarily a cheap operation.

        :param transp: the transposition to do
        :type transp: Iterable[int]
        :return:
        :rtype:
        """
        ...

    def reshape_internal(self, shp):
        ...

    def reshape(self, shp):
        """
        Had to make this op not in-place because otherwise got scary errors...
        :param shp:
        :type shp:
        :return:
        :rtype:
        """
        ...

    def pad_right(self, amounts):
        ...

    def squeeze(self):
        ...

    def resize(self, newsize):
        """
        Returns a resized version of the tensor
        :param newsize:
        :type newsize: tuple[int]
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def _concat_coo(all_inds, all_vals, all_shapes, axis):
        ...

    def concatenate_coo(self, *others, axis=0):
        ...

    def _stack_data(self, dats, axis):
        ...

    def concatenate_2d(self, *others, axis=0):
        ...

    def concatenate(self, *others, axis=0):
        """
        Concatenates multiple arrays along the specified axis
        This is relatively inefficient in terms of not tracking indices
        throughout

        :param other:
        :type other:
        :param axis:
        :type axis:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def broadcast_values(cls, new_shape, old_shape, vals, inds):
        """
        Implements broadcast_to using COO-style operations
        to be a little bit more efficient

        :param shape:
        :type shape:
        :return:
        :rtype:
        """
        ...

    def broadcast_to(self, shape):
        """
        Broadcasts to shape
        :param shape:
        :return:
        """
        ...

    def expand_and_broadcast_to(self, expansion, new_shape):
        ...

    def expand_and_pad(self, expansion, padding):
        ...

    @property
    def T(self):
        ...

    def __matmul__(self, other):
        ...

    def _tocs(self):
        ...

    def ascs(self, inplace=False):
        ...

    def dot(self, b, reverse=False):
        ...

    def outer(self, other):
        ...

    def __neg__(self):
        ...

    def __pos__(self):
        ...

    def __add__(self, other):
        ...

    def __iadd__(self, other):
        ...

    def __radd__(self, other):
        ...

    def plus(self, other, inplace=False):
        ...

    def floopy_flop(self):
        ...

    def __truediv__(self, other):
        ...

    def __rtruediv__(self, other):
        ...

    def __rmul__(self, other):
        ...

    def __mul__(self, other):
        ...

    def true_multiply(self, other):
        ...

    def copy(self):
        ...

    @classmethod
    def _find_block_alignment(cls, inds, block):
        """
        finds the positions where the block & index align
        """
        ...

    def _get_filtered_elements(self, blocks, data, inds):
        ...

    def _get_element(self, idx, pull_elements=None):
        """
        Convert idx into a 1D index or slice or whatever and then convert it back to the appropriate 2D shape

        :param i:
        :type i:
        :return:
        :rtype:
        """
        ...

    def _set_data(self, unflat, val):
        """
        Tries to explicitly assign but if that fails drops back to CSR and then reconverts

        :param unflat:
        :type unflat:
        :param val:
        :type val:
        :return:
        :rtype:
        """
        ...

    def _set_element(self, idx, val):
        """
        Convert idx into a 1D index or slice or whatever and then convert it back to the appropriate 2D shape.
        Then hope that the val can be set on the sp.spmatrix backend...

        :param i:
        :type i:
        :return:
        :rtype:
        """
        ...

    def _del_element(self, idx):
        """
        Convert idx into a 1D index or slice or whatever and then convert it back to the appropriate 2D shape.
        Then hope that the val can be deleted on the sp.spmatrix backend...

        :param i:
        :type i:
        :return:
        :rtype:
        """
        ...

    def savez(self, file, compressed=True):
        """
        Saves a SparseArray to a file (must have the npz extension)
        :param file:
        :type file:
        :param compressed:
        :type compressed:
        :return: the saved file
        :rtype: str
        """
        ...

    @classmethod
    def loadz(cls, file):
        """
        Loads a SparseArray from an npz file
        :param file:
        :type file:
        :return:
        :rtype: SparseArray
        """
        ...

    def __getitem__(self, item):
        ...

    def __setitem__(self, item, val):
        ...

    def __delitem__(self, item):
        ...

    def __repr__(self):
        ...

class TensorFlowSparseArray(SparseArray):
    """
    Provides a SparseArray implementation that uses TensorFlow as the backend
    """

    def __init__(self, data, dtype=None):
        ...

    def _init_tensor(self, data, dtype=None):
        """
        :param data:
        :type data:
        :return:
        :rtype: tensorflow.sparse.SparseTensor
        """
        ...

    @property
    def shape(self):
        """
        Provides the shape of the sparse array
        :return:
        :rtype: tuple[int]
        """
        ...

    def to_state(self, serializer=None):
        """
        Provides just the state that is needed to
        serialize the object
        :param serializer:
        :type serializer:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def from_state(cls, state, serializer=None):
        """
        Loads from the stored state
        :param serializer:
        :type serializer:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def empty(cls, shape, dtype=None, **kw):
        """
        Returns an empty SparseArray with the appropriate shape and dtype
        :param shape:
        :type shape:
        :param dtype:
        :type dtype:
        :param kw:
        :type kw:
        :return:
        :rtype:
        """
        ...

    @property
    def block_data(self):
        """
        Returns the row and column indices and vector of
        values that the sparse array is storing
        :return:
        :rtype: Tuple[np.ndarray, Iterable[np.ndarray]]
        """
        ...

    def transpose(self, axes):
        """
        Returns a transposed version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

    def ascoo(self):
        """
        Converts the tensor into a scipy COO matrix...
        :return:
        :rtype: sp.coo_matrix
        """
        ...

    def ascsr(self):
        """
        Converts the tensor into a scipy COO matrix...
        :return:
        :rtype: sp.coo_matrix
        """
        ...

    def reshape(self, newshape):
        """
        Returns a reshaped version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

    def __truediv__(self, other):
        ...

    def __rtruediv__(self, other):
        ...

    def __rmul__(self, other):
        ...

    def __mul__(self, other):
        ...

    def true_multiply(self, other):
        """
        Multiplies self and other
        :param other:
        :type other:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def _tf_sparse_dot(a, b):
        ...

    def dot(self, other):
        """
        Takes a regular dot product of self and other
        :param other:
        :type other:
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        ...

def _dot(a, b):
    ...

def sparse_tensordot(a, b, axes=2):
    """Defines a version of tensordot that uses sparse arrays, adapted from the sparse package on PyPI

    :param a: the array to contract from
    :type a: SparseArray | sp.spmatrix | np.ndarray
    :param b: the array to contract with
    :type b: SparseArray | sp.spmatrix | np.ndarray
    :param axes: the axes to contract along
    :type axes: int | Iterable[int]
    :return:
    :rtype:
    """
    ...