import numpy as np, scipy.sparse as sp, itertools as ip, functools as fp, os, abc, gc
import scipy.special
import contextlib, errno, mmap, tempfile, time, weakref
from pathlib import Path

from ..Scaffolding import MaxSizeCache, Logger
from .SetOps import contained, unique as nput_unique, find
from .Misc import infer_inds_dtype, downcast_index_array, infer_int_dtype

__all__ = [
    "SparseArray",
    "ScipySparseArray",
    "EvaluatedSparseMatrix",
    "TensorFlowSparseArray",
    "sparse_tensordot",
    "matrix_dot_into",
    "PackedIndexArray",
    "CompactSparseRow",
    "RowSparseArray",
    "RowSpillStore"
]

#   I should provide a general "ArrayWrapper" class that allows all these arrays to interact nicely
#   with eachother with a very general `dot` syntax and shared `reshape` interface and all of that
#   that way I would never need to check if things are numpy.ndarray or sp.spmatrix or those kinds of things
#
#   And actually by providing a constructor like np.array that dispatches to the appropriate class
#   for a given data type we'd be able to avoid the need to explicitly declare our data-type
#
#   This would also allow us to more conveniently swap out the backend for our different arrays, in
#   case we want to use a different sparse matrix format.

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
        if cls.backends is None:
            return (('scipy', ScipySparseArray),)
        else:
            return cls.backends

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

        if shape is not None:
            kwargs['shape'] = shape
        if dtype is not None:
            kwargs['dtype'] = dtype
        backend_errors = []
        backends = cls.get_backends()
        for name,backend in backends:
            if target_backend is not None and name == target_backend:
                if constructor is not None:
                    backend = getattr(backend, constructor)
                return backend(data, **kwargs)
            else:
                try:
                    if constructor is not None:
                        backend = getattr(backend, constructor)
                    return backend(data, **kwargs)
                except Exception as e:
                    backend_errors.append(e)
        else:
            if target_backend is None:
                raise backend_errors[0]
            else:
                raise ValueError("`target_backend` {} not in available sparse backends {}".format(
                    target_backend,
                    backends
                ))
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
        return cls.from_data(data,
                             constructor='from_diagonal_data',
                             shape=shape, dtype=dtype,
                             **kwargs
                             )
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
        raise NotImplementedError("{}.{} is an abstract method".format(cls.__name__, 'from_diagonal_data'))
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
        return len(self.shape)
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
        raise NotImplementedError("{}.{} is an abstract method".format(cls.__name__, 'from_state'))
        ...
    @classmethod
    def empty(cls, shape, dtype=None, **kw):
        return cls.from_data(shape,
                             constructor='initialize_empty',
                             dtype=dtype,
                             **kw
                             )
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
        raise NotImplementedError("{}.{} is an abstract method".format(cls.__name__, 'empty'))
        ...
    @property
    @abc.abstractmethod
    def block_data(self):
        """
        Returns the vector of values and corresponding indices
        :return:
        :rtype:
        """
        raise NotImplementedError("{}.{} is an abstract method".format(type(self).__name__, 'block_data'))
        ...
    @property
    def block_inds(self):
        return self.block_data[1]

    @property
    def block_vals(self):
        return self.block_data[0]
    @abc.abstractmethod
    def transpose(self, axes):
        """
        Returns a transposed version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        raise NotImplementedError("{}.{} is an abstract method".format(type(self).__name__, 'transpose'))
        ...
    @abc.abstractmethod
    def ascoo(self):
        """
        Converts the tensor into a scipy COO matrix...
        :return:
        :rtype: sp.coo_matrix
        """
        raise NotImplementedError("{}.{} is an abstract method".format(type(self).__name__, 'ascoo'))

    @abc.abstractmethod
    def ascsr(self):
        """
        Converts the tensor into a scipy CSR matrix...
        :return:
        :rtype: sp.csr_matrix
        """
        raise NotImplementedError("{}.{} is an abstract method".format(type(self).__name__, 'ascsr'))
    def iter_nonzero_blocks(self, block_size=65536, value_filter=None):
        """Yield bounded (values, coordinate-tuple) blocks of stored entries.

        value_filter is applied before constructing coordinates where the
        backend supports this. The generic fallback uses existing block data.
        """
        if not isinstance(block_size, (int, np.integer)) or block_size < 1:
            raise ValueError('block_size must be a positive integer')
        values, indices = self.block_data
        for start in range(0,len(values),block_size):
            stop = min(start+block_size,len(values))
            selected = np.arange(start,stop)
            if value_filter is not None:selected = selected[np.asarray(value_filter(values[start:stop]),dtype=bool)]
            if len(selected):yield values[selected],tuple(index[selected] for index in indices)

    @abc.abstractmethod
    def asarray(self):
        """
        Converts the tensor into a dense np.ndarray
        :return:
        :rtype: np.ndarray
        """
        raise NotImplementedError("{}.{} is an abstract method".format(type(self).__name__, 'asarray'))
    @abc.abstractmethod
    def reshape(self, newshape):
        """
        Returns a reshaped version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        raise NotImplementedError("{}.{} is an abstract method".format(type(self).__name__, 'reshape'))
    @abc.abstractmethod
    def resize(self, newsize):
        """
        Returns a resized version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        raise NotImplementedError("{}.{} is an abstract method".format(type(self).__name__, 'resize'))
    @abc.abstractmethod
    def pad_right(self, newshape):
        """
        Returns a right-padded version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        raise NotImplementedError("{}.{} is an abstract method".format(type(self).__name__, 'pad_right'))
    @abc.abstractmethod
    def broadcast_to(self, shape) -> 'SparseArray':
        """
        Returns a broadcasted version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        raise NotImplementedError("{}.{} is an abstract method".format(type(self).__name__, 'broadcast_to'))
    @abc.abstractmethod
    def expand_and_broadcast_to(self, expansion, new_shape) -> 'SparseArray':

        """
        Expands, then broadcasts (memory efficient)
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        raise NotImplementedError("{}.{} is an abstract method".format(type(self).__name__, 'expand_and_broadcast_to'))
    @abc.abstractmethod
    def expand_and_pad(self, expansion, padding) -> 'SparseArray':

        """
        Expands, then pads (memory efficient)
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        raise NotImplementedError("{}.{} is an abstract method".format(type(self).__name__, 'expand_and_pad'))

    @classmethod
    def get_expanded_shape(cls, shape, axis):
        """
        adapted from np.expand_dims

        :param axis:
        :type axis:
        :return:
        :rtype:
        """

        if isinstance(axis, (int, np.integer)):
            axis = [axis]

        out_ndim = len(axis) + len(shape)
        axis = [out_ndim + a if a < 0 else a for a in axis]

        shape_it = iter(shape)
        new_shape = tuple(1 if ax in axis else next(shape_it) for ax in range(out_ndim))

        return new_shape
    def expand_dims(self, axis):
        """
        adapted from np.expand_dims

        :param axis:
        :type axis:
        :return:
        :rtype:
        """
        shape = self.get_expanded_shape(self.shape, axis)
        return self.reshape(shape)

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

        if isinstance(start, (int, np.integer)):
            start = [start]
        if isinstance(end, (int, np.integer)):
            end = [end]

        start = [self.ndim + a if a < 0 else a for a in start]
        end = [self.ndim + a if a < 0 else a for a in end]

        order = [n for n in range(self.ndim) if n not in start]

        for dest, src in sorted(zip(end, start)):
            order.insert(dest, src)

        # raise Exception(order)

        return self.transpose(order)

    @abc.abstractmethod
    def concatenate(self, *others, axis=0):
        """
        Concatenates multiple SparseArrays along the specified axis
        :return:
        :rtype: SparseArray
        """
        ...

    # def broadcast_to(self, shape):
    #     """
    #     Broadcasts self to the given shape.
    #     Incredibly inefficient implementation but useful in smaller cases.
    #     Might need to optimize later.
    #
    #     :param shape:
    #     :type shape:
    #     :return:
    #     :rtype:
    #     """
    #
    #     # precheck b.c. concatenate is expensive
    #     compat = all(a%b == 0 for a,b in zip(shape, self.shape))
    #     if not compat:
    #         raise ValueError("{} with shape {} can't be broadcast to shape {}".format(
    #             type(self).__name__,
    #             self.shape,
    #             shape
    #         ))
    #
    #     new = self
    #     for i, (shs, sho) in enumerate(zip(self.shape, shape)):
    #         if shs != sho:
    #             reps = sho // shs
    #             for _ in range(reps):
    #                 new = new.concatenate(self, axis=i)
    #
    #     return new

    @property
    def T(self):
        if self.ndim == 2:
            return self.transpose((1, 0))
        raise ValueError("dunno what T means for high dimensional arrays")

    @staticmethod
    def _index_dtype(size):
        # Reuse the package's signed range inference while retaining the
        # int32 minimum required by native CSR kernels.
        return np.promote_types(np.int32, infer_int_dtype(size))

    def __matmul__(self, other):
        return self.dot(other)

    def __neg__(self):
        return -1 * self

    def __pos__(self):
        return self

    def __add__(self, other):
        return self.plus(other)

    def __iadd__(self, other):
        return self.plus(other, inplace=True)

    def __radd__(self, other):
        return self.plus(other)

    def __truediv__(self, other):
        return self.true_multiply(1 / other)
    def __rtruediv__(self, other):
        return self.true_multiply(1 / other)
    def __rmul__(self, other):
        return self.true_multiply(other)
    def __mul__(self, other):
        return self.true_multiply(other)

    def _bcast_shapes(self, other):
        if other.ndim != self.ndim:
            raise NotImplementedError("{} object only supports broadcasting when `ndims` align".format(
                type(self).__name__
            ))

        total_shape = []
        for shs, sho in zip(self.shape, other.shape):
            if shs == 1:
                total_shape.append(sho)
            elif sho == 1:
                total_shape.append(shs)
            elif shs == sho:
                total_shape.append(shs)
            else:
                raise ValueError("shape mismatch for multiply of objects with shapes {} and {}".format(
                    self.shape,
                    other.shape
                ))

        if total_shape != self.shape:
            self = self.broadcast_to(total_shape)

        if total_shape != other.shape:
            if isinstance(other, np.ndarray):
                other = np.broadcast_to(other, total_shape)
            else:
                other = other.broadcast_to(total_shape)

        return self,other

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
        if isinstance(other, (int, float)):
            return self.true_multiply(other)

        self, other = self._bcast_shapes(other)

        return self.true_multiply(other)

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

        caching_status = self.get_caching_status()
        try:
            self.disable_caches()
            try:
                iter(axes)
            except TypeError:
                axes_a = list(range(-axes, 0))
                axes_b = list(range(0, axes))
            else:
                axes_a, axes_b = axes
            try:
                na = len(axes_a)
                axes_a = list(axes_a)
            except TypeError:
                axes_a = [axes_a]
                na = 1
            try:
                nb = len(axes_b)
                axes_b = list(axes_b)
            except TypeError:
                axes_b = [axes_b]
                nb = 1

            a = self
            b = other

            as_ = a.shape
            nda = a.ndim
            bs = b.shape
            ndb = b.ndim
            equal = True
            if na != nb:
                equal = False
            elif max(axes_a) >= nda:
                raise ValueError("tensor with shape {} doesn't have {} axes".format(
                    as_, axes_a
                ))
            elif max(axes_b) >= ndb:
                raise ValueError("tensor with shape {} doesn't have {} axes".format(
                    bs, axes_b
                ))
            else:
                for k in range(na):
                    if as_[axes_a[k]] != bs[axes_b[k]]:
                        equal = False
                        break
                    if axes_a[k] < 0:
                        axes_a[k] += nda
                    if axes_b[k] < 0:
                        axes_b[k] += ndb
            if not equal:
                raise ValueError("shape-mismatch for sum ({}{}@{}{})".format(as_, axes_a, bs, axes_b))

            # Move the axes to sum over to the end of "a"
            # and to the front of "b"
            notin = [k for k in range(nda) if k not in axes_a]
            newaxes_a = [notin, axes_a]
            N2 = 1
            for axis in axes_a:
                N2 *= as_[axis]
            totels_a = np.prod(as_)
            newshape_a = (totels_a // N2, N2)
            olda = [as_[axis] for axis in notin]

            notin = [k for k in range(ndb) if k not in axes_b]
            newaxes_b = [axes_b, notin]
            N2 = 1
            for axis in axes_b:
                N2 *= bs[axis]
            totels_b = np.prod(bs)
            newshape_b = (N2, totels_b // N2)
            oldb = [bs[axis] for axis in notin]

            # if any(dim == 0 for dim in ip.chain(newshape_a, newshape_b)):
            #     # shortcut for when we aren't even doing a contraction...?
            #     res = sp.csr_matrix((olda + oldb), dtype=b.dtype)
            #     # dense output...I guess that's clean?
            #     if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
            #         res = res.todense()
            #     return res


            # import time
            if a.ndim > 1:
                at = a.transpose(newaxes_a[0] + newaxes_a[1])
            else:
                at = a
            a = None
            at = at.reshape(newshape_a)

            if b.ndim > 1:
                bt = b.transpose(newaxes_b[0] + newaxes_b[1])
            else:
                bt = b
            b = None
            bt = bt.reshape(newshape_b)

            # time.sleep(.3)
            res = at.dot(bt)

            return res.reshape(olda + oldb)
        finally:
            if caching_status:
                self.enable_caches()

    # TODO: Caching should be managed by keeping track of 'parent' `SparseArray`
    #       objects using a weakref so that it's possible to just ask the parents
    #       if they have the data we need in their caches and then all caches
    #       will properly be cleaned up when objects go out of scope
    class cacheing_manager:
        def __init__(self, parent, enabled=True, clear=False):
            self.to_set = enabled
            self.cache_status = None
            self.parent = parent
            self.clear = clear
        def __enter__(self):
            self.cache_status = self.parent.get_caching_status()
            if self.to_set:
                self.parent.enable_caches()
            else:
                self.parent.disable_caches()
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.cache_status:
                self.parent.enable_caches()
            else:
                self.parent.disable_caches()
            self.cache_status = None
            if self.clear:
                self.parent.clear_caches()
    @classmethod
    def cache_options(self, enabled=True, clear=False):
        return self.cacheing_manager(self, enabled=enabled, clear=clear)
    @classmethod
    def get_caching_status(cls):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to specify if caching is on or not
        :return:
        :rtype:
        """
    @classmethod
    def enable_caches(self):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to turn this on
        :return:
        :rtype:
        """
    @classmethod
    def disable_caches(self):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to turn this off
        :return:
        :rtype:
        """
    @classmethod
    def clear_cache(self):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to clear this out.
        :return:
        :rtype:
        """

    class initializer_list(list):
        """
        A simple wrapping head that allows us
        to transfer ownership of initialization data to
        a `SparseArray` during initialization
        """
        def __init__(self, *args):
            super().__init__(args)

    # TODO: need to figure out if I want to support item assignment or not

class lowmem_csr(sp.csr_matrix):
    def __init__(self, arg1, shape=None, dtype=None, copy=False):
        from scipy.sparse.compressed import _data_matrix, get_index_dtype
        _data_matrix.__init__(self)
        (data, indices, indptr) = arg1

        # Select index dtype large enough to pass array and
        # scalar parameters to sparsetools
        maxval = None
        if shape is not None:
            maxval = max(shape)

        idx_dtype = self.eval_idx_type(indices, indptr, maxval)
        self._shape = shape
        self._init_vals(indices, indptr, data, idx_dtype, dtype, copy=copy)

    # @profile
    def _init_vals(self, indices, indptr, data, idx_dtype, dtype, copy=False):
        # import time

        self.indices = np.array(indices, copy=copy, dtype=idx_dtype)
        self.indptr = np.array(indptr, copy=copy, dtype=idx_dtype)
        self.data = np.array(data, copy=copy, dtype=dtype)
        # time.sleep(.2)

    # @profile
    def eval_idx_type(self, indices, indptr, maxval):
        return infer_inds_dtype(maxval)
        # from scipy.sparse.compressed import get_index_dtype
        #
        # idx_dtype = get_index_dtype((indices, indptr),
        #                             maxval=maxval,
        #                             check_contents=True)
        #
        # return idx_dtype

class EvaluatedSparseMatrix(SparseArray):
    """Two-dimensional sparse matrix backend with on-demand element evaluation.

    This is a matrix-only specialization of the n-dimensional SparseArray
    interface. Its two axes are rows and columns; support, products and
    bilinear projections are matrix operations. It does not provide lazy
    evaluation of arbitrary-rank tensors. SparseArray and ScipySparseArray
    retain their existing n-dimensional interfaces. Reshaping to another
    rank explicitly materializes a bounded ordinary sparse tensor.

    ``evaluate(rows, columns)`` evaluates paired coordinates. Either provide
    canonical CSC ``positions=(indices, indptr)`` without values, or a
    ``pair_generator(row_slice, columns, block_size)`` yielding unique paired
    coordinates for the requested output rows and sorted input columns.
    The generator must not cache a global graph. An explicit diagonal vector
    is also supported, without CSR/CSC index arrays.

    This backend is immutable. Whole-array exports are explicit and bounded
    by ``block_bytes``; products do not export the matrix. Callbacks and their
    bound state spaces must outlive the matrix and all borrowed views.
    """
    def __init__(self, shape, evaluate=None, *, positions=None,
                 pair_generator=None, diagonal=None, dtype=float,
                 block_size=65536, block_bytes=64*1024**2):
        shape = tuple(shape)
        if len(shape) != 2 or any(not isinstance(n, (int, np.integer)) or n < 0 for n in shape):
            raise ValueError('EvaluatedSparseMatrix requires a two-dimensional nonnegative shape')
        if any(not isinstance(n, (int, np.integer)) or n < 1 for n in (block_size, block_bytes)):
            raise ValueError('block_size and block_bytes must be positive integer byte/count limits')
        if sum(x is not None for x in (positions, pair_generator, diagonal)) != 1:
            raise ValueError('Provide exactly one of positions, pair_generator or diagonal')
        self._shape = shape
        self.block_size, self.block_bytes = int(block_size), int(block_bytes)
        self.positions = positions
        self.pair_generator, self.evaluate = pair_generator, evaluate
        self.diagonal_data = None if diagonal is None else np.asarray(diagonal)
        if diagonal is not None:
            if shape[0] != shape[1] or self.diagonal_data.shape != (shape[0],):
                raise ValueError('Diagonal data must match a square matrix')
            dtype = self.diagonal_data.dtype
        elif not callable(evaluate):
            raise TypeError('An element evaluator is required')
        self._dtype = np.dtype(dtype)
        if positions is not None:
            indices, indptr = positions
            if (np.ndim(indices) != 1 or np.ndim(indptr) != 1
                    or len(indptr) != shape[1]+1 or indptr[0] != 0 or indptr[-1] != len(indices)
                    or indices.dtype.kind not in 'iu' or indptr.dtype.kind not in 'iu'):
                raise ValueError('Invalid CSC support')
            # Validate in chunks; do not create nnz-sized temporary arrays.
            for start in range(0, len(indptr)-1, self.block_size):
                part = indptr[start:start+self.block_size+1]
                if np.any(part[1:] < part[:-1]):
                    raise ValueError('CSC pointers must be monotone')
            for column in range(shape[1]):
                lo, hi = int(indptr[column]), int(indptr[column+1])
                previous = -1
                for start in range(lo, hi, self.block_size):
                    rows = indices[start:min(start+self.block_size, hi)]
                    if len(rows) and (rows[0] <= previous or rows[-1] >= shape[0]
                                     or np.any(rows[1:] <= rows[:-1])):
                        raise ValueError('CSC row positions must be sorted, unique and in range')
                    if len(rows): previous = int(rows[-1])

    @property
    def shape(self): return self._shape
    @property
    def dtype(self): return self._dtype
    @property
    def evaluation_mode(self):
        return 'diagonal' if self.diagonal_data is not None else 'positions' if self.positions is not None else 'runtime'
    @property
    def nbytes(self):
        """Owned/borrowed numerical storage, excluding callback-owned state spaces."""
        return (self.diagonal_data.nbytes if self.diagonal_data is not None else
                sum(a.nbytes for a in self.positions) if self.positions is not None else 0)
    def __len__(self): return self.shape[0]
    def __repr__(self):
        return '{}(shape={}, evaluation_mode={!r}, storage_bytes={})'.format(
            type(self).__name__, self.shape, self.evaluation_mode, self.nbytes)

    def _iter_pairs(self, rows, columns, block_size):
        if self.diagonal_data is not None:
            selected = columns[(columns >= rows.start) & (columns < rows.stop)]
            for start in range(0, len(selected), block_size):
                block = selected[start:start+block_size]
                yield block, block
        elif self.positions is not None:
            indices, indptr = self.positions
            for column in columns:
                lo, hi = int(indptr[column]), int(indptr[column+1])
                values = indices[lo:hi]
                first, last = np.searchsorted(values, [rows.start, rows.stop])
                for start in range(int(first), int(last), block_size):
                    selected = values[start:min(start+block_size, int(last))]
                    yield selected, np.full(len(selected), column, dtype=np.int64)
        else:
            yield from self.pair_generator(rows, columns, block_size)

    def iter_evaluated_blocks(self, rows=None, columns=None, block_size=None):
        """Yield values and global coordinates; retain no computed values."""
        rows = slice(0, self.shape[0]) if rows is None else rows
        size = min(self.block_size, block_size or self.block_size)
        if columns is None:
            for start in range(0, self.shape[1], size):
                yield from self.iter_evaluated_blocks(rows, np.arange(start, min(start+size, self.shape[1])), size)
            return
        columns = np.asarray(columns)
        for r, c in self._iter_pairs(rows, columns, size):
            r, c = np.asarray(r), np.asarray(c)
            if r.shape != c.shape or r.ndim != 1 or len(r) > size:
                raise ValueError('Pair provider violated its bounded coordinate contract')
            if (np.any(r < rows.start) or np.any(r >= rows.stop)
                    or np.any(~np.isin(c, columns))):
                raise ValueError('Pair provider returned coordinates outside the request')
            values = self.diagonal_data[r] if self.diagonal_data is not None else np.asarray(self.evaluate(r, c))
            if values.shape != r.shape:
                raise ValueError('Element evaluator must return one scalar per pair')
            if not np.can_cast(values.dtype, self.dtype, casting='same_kind'):
                raise TypeError('Element evaluator returned an incompatible dtype')
            yield values, (r, c)

    def iter_nonzero_blocks(self, block_size=65536, value_filter=None):
        for values, indices in self.iter_evaluated_blocks(block_size=block_size):
            keep = values != 0
            if value_filter is not None: keep &= value_filter(values)
            if np.any(keep): yield values[keep], tuple(i[keep] for i in indices)

    def dot_into(self, b, out, *, alpha=1, beta=0, working_memory=64*1024**2, block_callback=None):
        """Bounded product accumulation, sharing matrix_dot_into's callback contract.

        Each callback receives a COMPLETE unscaled product tile once, including
        zero tiles. Active input support is detected in bounded scans. A target
        is not modified until its current tile has been fully evaluated.
        """
        if not isinstance(working_memory, (int, np.integer)) or working_memory < 1:
            raise ValueError('working_memory must be a positive integer')
        b = b if isinstance(b, SparseArray) or sp.issparse(b) else np.asarray(b)
        out = np.asarray(out)
        right = b[:, None] if len(b.shape) == 1 else b
        target = out[:, None] if out.ndim == 1 else out
        if (len(b.shape) not in (1, 2) or target.ndim != 2 or right.shape[0] != self.shape[1]
                or target.shape != (self.shape[0], right.shape[1])
                or (len(b.shape) == 1) != (out.ndim == 1)):
            raise ValueError('Incompatible matrix_dot_into shapes')
        if not target.flags.writeable: raise ValueError('matrix_dot_into output is read-only')
        storage = (() if self.diagonal_data is None else (self.diagonal_data,))
        storage += () if self.positions is None else tuple(self.positions)
        native_right = b.data if isinstance(b, ScipySparseArray) else b
        right_buffers = ([native_right.data, native_right.indices, native_right.indptr]
                         if sp.issparse(native_right) else
                         [v for row in b.rows for v in (row.values, row.columns.bits if row.dense else row.columns)]
                         if isinstance(b, RowSparseArray) else [native_right])
        if any(np.shares_memory(target, a) for a in right_buffers+list(storage)):
            raise ValueError('matrix_dot_into inputs must not overlap the output')
        dtype = np.result_type(self.dtype, right.dtype)
        if not np.can_cast(np.result_type(dtype, alpha, beta), target.dtype, casting='same_kind'):
            raise TypeError('matrix_dot_into output dtype cannot hold the result')
        if alpha == 0 and block_callback is None:
            if beta == 0: target.fill(0)
            elif beta != 1: np.multiply(target, beta, out=target)
            return out
        for rows, columns, product in self.iter_dot_blocks(right, working_memory=working_memory):
            if block_callback is not None: block_callback(rows, columns, product)
            dest = target[rows, columns]
            if beta == 0: dest.fill(0)
            elif beta != 1: np.multiply(dest, beta, out=dest)
            if alpha == 1: np.add(dest, product, out=dest)
            elif alpha == -1: np.subtract(dest, product, out=dest)
            elif alpha != 0: np.add(dest, alpha*product, out=dest)
        return out

    @staticmethod
    def _vector_block(matrix, index, start, stop, *, axis):
        """Borrow/decode a bounded row or column, including compact corrections."""
        if isinstance(matrix, RowSparseArray) and (axis == 1) == matrix.transposed:
            row = matrix.rows[index]
            with RowSpillStore.pin_rows([row]):
                if row.dense:
                    values = np.asarray(row.values[start:stop])
                    return values.copy() if getattr(row, '_spill_segment', None) is not None else values
                native = row.select(np.arange(start, stop), matrix.block_size).native()
                return native.toarray().reshape(-1) if sp.issparse(native) else np.asarray(native).reshape(-1)
        if isinstance(matrix, ScipySparseArray): matrix = matrix.data
        part = matrix[index, start:stop] if axis == 0 else matrix[start:stop, index]
        if isinstance(part, SparseArray): part = part.asarray()
        elif sp.issparse(part): part = part.toarray()
        return np.asarray(part).reshape(-1)

    def iter_dot_blocks(self, right, *, working_memory=None):
        """Yield complete product tiles without retaining a full H@right result."""
        budget = self.block_bytes if working_memory is None else working_memory
        if not isinstance(budget, (int, np.integer)) or budget < 1:
            raise ValueError('working_memory must be a positive integer')
        if not isinstance(right, SparseArray) and not sp.issparse(right): right = np.asarray(right)
        if len(right.shape) == 1: right = right[:, None]
        if len(right.shape) != 2 or right.shape[0] != self.shape[1]:
            raise ValueError('Incompatible matrix product shapes')
        dtype = np.result_type(self.dtype, right.dtype)
        itemsize = np.dtype(dtype).itemsize
        size = max(1, min(self.block_size, budget//max(128, 16*itemsize)))
        row_size = max(1, min(self.shape[0], budget//max(1, 8*itemsize)))
        for first in range(0, self.shape[0], row_size):
            last = min(first+row_size, self.shape[0]); rows = slice(first, last)
            for column in range(right.shape[1]):
                product = np.zeros(last-first, dtype=dtype)
                if self.diagonal_data is not None:
                    values = self._vector_block(right, column, first, last, axis=1)
                    np.multiply(self.diagonal_data[rows], values, out=product)
                else:
                    for start in range(0, self.shape[1], size):
                        values = self._vector_block(right, column, start, min(start+size, self.shape[1]), axis=1)
                        active = np.flatnonzero(values != 0)+start
                        if not len(active): continue
                        for elements, (r, c) in self.iter_evaluated_blocks(rows, active, size):
                            np.add.at(product, r-first, elements*values[c-start])
                yield rows, slice(column, column+1), product[:, None]

    def bilinear(self, left, right, *, working_memory=None):
        """Return left@self@right without either large intermediate product.

        Compact/file-backed correction rows are consumed directly in bounded
        slices. This is a transpose algebraic contraction, not a conjugation.
        """
        if not hasattr(left, 'shape'): left = np.asarray(left)
        if not hasattr(right, 'shape'): right = np.asarray(right)
        if len(left.shape) != 2 or len(right.shape) != 2 or left.shape[1] != self.shape[0]:
            raise ValueError('Incompatible bilinear product shapes')
        result = np.zeros((left.shape[0], right.shape[1]), dtype=np.result_type(left.dtype, self.dtype, right.dtype))
        for rows, columns, product in self.iter_dot_blocks(right, working_memory=working_memory):
            for i in range(left.shape[0]):
                values = self._vector_block(left, i, rows.start, rows.stop, axis=0)
                result[i, columns] += values @ product
        return result

    def _right_dot(self, left):
        """Binary left products retain their explicitly requested row output."""
        if len(left.shape) != 2 or left.shape[1] != self.shape[0]:
            raise ValueError('Matrix dimensions do not align')
        transposed = self.T
        rows = []
        for i in range(left.shape[0]):
            right = left[i:i+1, :].T
            result = np.empty(self.shape[1], dtype=np.result_type(left.dtype, self.dtype))
            for selected, _, product in transposed.iter_dot_blocks(right):
                result[selected] = product[:, 0]
            rows.append(CompactSparseRow.from_dense(result, None, self.block_size))
        return RowSparseArray(rows, self.shape[1], block_bytes=self.block_bytes, block_size=self.block_size)

    def dot(self, other):
        if not hasattr(other, 'shape'): other = np.asarray(other)
        if len(other.shape) not in (1, 2): raise ValueError('Vector or matrix required')
        vector = len(other.shape) == 1
        shape = (self.shape[0],) if vector else (self.shape[0], other.shape[1])
        result = np.empty(shape, dtype=np.result_type(self.dtype, other.dtype))
        for rows, columns, product in self.iter_dot_blocks(other):
            if vector: result[rows] = product[:, 0]
            else: result[rows, columns] = product
        return result

    def _export_check(self, size):
        if size > self.block_bytes:
            raise MemoryError('Explicit evaluated-matrix export exceeds block_bytes; use dot_into or block iteration')
    def asarray(self):
        self._export_check(self.shape[0]*self.shape[1]*self.dtype.itemsize)
        out = np.zeros(self.shape, dtype=self.dtype)
        for values, indices in self.iter_nonzero_blocks(): out[indices] = values
        return out
    toarray = asarray
    todense = asarray
    def ascsr(self):
        # A conservative dense bound prevents an unknown-size implicit export.
        self._export_check(self.shape[0]*self.shape[1]*(self.dtype.itemsize+16)+(self.shape[0]+1)*8)
        values, rows, columns = [], [], []
        for data, (r, c) in self.iter_nonzero_blocks():
            values.append(data); rows.append(r); columns.append(c)
        if not values: return sp.csr_matrix(self.shape, dtype=self.dtype)
        return sp.csr_matrix((np.concatenate(values), (np.concatenate(rows), np.concatenate(columns))), shape=self.shape)
    def ascoo(self): return self.ascsr().tocoo()
    @property
    def block_data(self):
        coo = self.ascoo(); return coo.data, (coo.row, coo.col)

    def get_elements(self, rows, columns):
        rows, columns = np.broadcast_arrays(np.asarray(rows), np.asarray(columns))
        if rows.dtype.kind not in 'iu' or columns.dtype.kind not in 'iu': raise IndexError('Integer coordinates required')
        rows = np.where(rows < 0, rows+self.shape[0], rows)
        columns = np.where(columns < 0, columns+self.shape[1], columns)
        if (np.any(rows < 0) or np.any(rows >= self.shape[0])
                or np.any(columns < 0) or np.any(columns >= self.shape[1])):
            raise IndexError('Matrix coordinate outside shape')
        self._export_check(rows.size*self.dtype.itemsize)
        result = np.zeros(rows.size, dtype=self.dtype)
        rflat, cflat = rows.reshape(-1), columns.reshape(-1)
        for start in range(0, rows.size, self.block_size):
            r, c = rflat[start:start+self.block_size], cflat[start:start+self.block_size]
            if not len(r): continue
            if self.diagonal_data is not None:
                result[start:start+len(r)] = np.where(r == c, self.diagonal_data[r], 0)
            else:
                # Small indexed reads preserve broadcasting, order and duplicates.
                locations = {}
                for i, pair in enumerate(zip(r.tolist(), c.tolist())): locations.setdefault(pair, []).append(start+i)
                for values, (br, bc) in self.iter_evaluated_blocks(slice(int(r.min()), int(r.max())+1), np.unique(c)):
                    for rr, cc, value in zip(br, bc, values):
                        for i in locations.get((int(rr), int(cc)), ()): result[i] = value
        return result.reshape(rows.shape)[()] if rows.ndim == 0 else result.reshape(rows.shape)
    @property
    def diag(self):
        if self.diagonal_data is not None: return self.diagonal_data
        n = min(self.shape); out = np.empty(n, dtype=self.dtype)
        for start in range(0, n, self.block_size):
            inds = np.arange(start, min(start+self.block_size, n)); out[start:start+len(inds)] = self.get_elements(inds, inds)
        return out

    def __getitem__(self, item):
        if not isinstance(item, tuple): item = (item, slice(None))
        if len(item) != 2: raise IndexError('Two-dimensional matrix required')
        if not any(isinstance(i, slice) for i in item): return self.get_elements(*item)
        selectors = []
        for i, n in zip(item, self.shape):
            if isinstance(i, slice): selectors.append(range(*i.indices(n)))
            else:
                arr = np.atleast_1d(i)
                if arr.dtype.kind == 'b':
                    if arr.shape != (n,): raise IndexError('Boolean selector shape')
                    arr = np.flatnonzero(arr)
                if arr.dtype.kind not in 'iu': raise IndexError('Integer selector required')
                arr = np.where(arr < 0, arr+n, arr)
                if np.any((arr < 0) | (arr >= n)): raise IndexError('Selector outside shape')
                selectors.append(arr)
        rsel, csel = selectors
        def pairs(rows, columns, size):
            selected_rows = np.array(rsel[rows], dtype=np.int64)
            selected_cols = np.array([csel[int(i)] for i in columns], dtype=np.int64)
            if not len(selected_rows) or not len(selected_cols): return
            row_map, col_map = {}, {}
            for i, r in enumerate(selected_rows): row_map.setdefault(int(r), []).append(rows.start+i)
            for i, c in zip(columns, selected_cols): col_map.setdefault(int(c), []).append(int(i))
            rr, cc = [], []
            for br, bc in self._iter_pairs(
                    slice(int(selected_rows.min()), int(selected_rows.max())+1), np.unique(selected_cols), size):
                for r, c in zip(br, bc):
                    for ri in row_map.get(int(r), ()):
                        for ci in col_map.get(int(c), ()):
                            rr.append(ri); cc.append(ci)
                            if len(rr) == size:
                                yield np.array(rr), np.array(cc); rr, cc = [], []
            if rr: yield np.array(rr), np.array(cc)
        def evaluate(r, c):
            return self.get_elements(np.array([rsel[int(i)] for i in r]), np.array([csel[int(i)] for i in c]))
        return type(self)((len(rsel), len(csel)), evaluate, pair_generator=pairs,
                          dtype=self.dtype, block_size=self.block_size, block_bytes=self.block_bytes)

    def copy(self):
        return type(self)(self.shape, self.evaluate, positions=self.positions, pair_generator=self.pair_generator,
                          diagonal=self.diagonal_data, dtype=self.dtype, block_size=self.block_size, block_bytes=self.block_bytes)
    def transpose(self, axes=None):
        if axes is not None and tuple(axes) == (0, 1): return self.copy()
        if axes is not None and tuple(axes) != (1, 0): raise ValueError(axes)
        if self.diagonal_data is not None: return self.copy()
        def pairs(rows, columns, size):
            if not len(columns): return
            for start in range(rows.start, rows.stop, size):
                query = np.arange(start, min(start+size, rows.stop))
                for r, c in self._iter_pairs(slice(int(columns.min()), int(columns.max())+1), query, size):
                    keep = np.isin(r, columns)
                    if np.any(keep): yield c[keep], r[keep]
        return type(self)(self.shape[::-1], lambda r, c: self.get_elements(c, r), pair_generator=pairs,
                          dtype=self.dtype, block_size=self.block_size, block_bytes=self.block_bytes)
    def true_multiply(self, other):
        if not np.isscalar(other): raise NotImplementedError('Only scalar multiplication is implicit')
        if self.diagonal_data is not None:
            return type(self).from_diagonal_data(self.diagonal_data*other, block_bytes=self.block_bytes, block_size=self.block_size)
        return type(self)(self.shape, lambda r, c: self.evaluate(r, c)*other, positions=self.positions,
                          pair_generator=self.pair_generator, dtype=np.result_type(self.dtype, other),
                          block_bytes=self.block_bytes, block_size=self.block_size)
    def plus(self, other, inplace=False):
        if np.isscalar(other) and other == 0: return self.copy()
        raise NotImplementedError('Implicit matrix addition requires an operator representation')
    def reshape(self, newshape):
        if tuple(newshape) == self.shape: return self.copy()
        return SparseArray.from_data(self.asarray().reshape(newshape))
    def to_state(self, serializer=None):
        if self.diagonal_data is None:
            raise TypeError('Runtime operator bindings must be rebuilt, not serialized as sparse values')
        return dict(diagonal=self.diagonal_data, block_size=self.block_size, block_bytes=self.block_bytes)
    @classmethod
    def from_state(cls, state, serializer=None): return cls.from_diagonal_data(**state)
    @classmethod
    def from_diagonal_data(cls, diagonal, **opts):
        diagonal = np.asarray(diagonal)
        return cls((len(diagonal), len(diagonal)), diagonal=diagonal, **opts)
    @classmethod
    def initialize_empty(cls, shp, shape=None, **opts):
        shape = shp if shape is None else shape
        return cls(shape, lambda r, c: np.zeros(len(r)), pair_generator=lambda *args: iter(()), **opts)
    def resize(self, newsize): raise NotImplementedError('Rebind the operator to the new state space')
    def pad_right(self, newshape): raise NotImplementedError('Rebind the operator to the new state space')
    def broadcast_to(self, shape): raise NotImplementedError('Two-dimensional operator backend')
    def expand_and_broadcast_to(self, expansion, new_shape): raise NotImplementedError('Two-dimensional operator backend')
    def expand_and_pad(self, expansion, padding): raise NotImplementedError('Two-dimensional operator backend')
    def concatenate(self, *others, axis=0): raise NotImplementedError('Concatenate explicit state spaces before binding')
    def outer(self, other): raise NotImplementedError('Outer products need an explicit output plan')

class ScipySparseArray(SparseArray):
    """
    Array class that generalize the regular `scipy.sparse.spmatrix`.
    Basically acts like a high-dimensional wrapper that manages the _shape_ of a standard `scipy.sparse_matrix`, since that is rigidly 2D.
    We always use a combo of an underlying CSR or CSC matrix & COO-like shape operations.
    """

    def __init__(self, a,
                 shape=None,
                 layout=None,
                 dtype=None,
                 initialize=True,
                 cache_block_data=None,
                 logger=None,
                 init_kwargs=None
                 ):
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
        self._shape = tuple(shape) if shape is not None else shape
        self._a = a
        self._fmt = layout
        self._dtype = dtype
        self._validated = False
        self._block_data_sorted = False
        self._block_inds = None # cached to speed things up
        self._block_vals = None # cached to speed things up
        self.logger = logger
        if initialize:
            cache_block_data = self.get_caching_status() if cache_block_data is None else cache_block_data
            self._init_matrix(cache_block_data=cache_block_data, init_kwargs=init_kwargs)
            self._validate()

    # from memory_profiler import profile
    @classmethod
    # @profile
    def coo_to_cs(cls, shape, vals, ij_inds, memmap=False, assume_sorted=False):
        """
        Reimplementation of scipy's internal "coo_tocsr" for memory-limited situations
        Assumes `ij_inds` are sorted by row then column, which allows vals to be used
        directly once indptr is computed

        :return:
        :rtype:
        """

        # if shape[0] > shape[1]:
        #     return sp.csc_matrix((vals, ij_inds), shape=shape)
        # else:
        #     return sp.csr_matrix((vals, ij_inds), shape=shape)

        # return sp.csr_matrix((vals, ij_inds), shape=shape)

        if shape[0] > shape[1]:
            axis = 1
            other = 0
        else:
            axis = 0
            other = 1

        # hopefully this doesn't destroy my memmap...
        ij_inds = np.asanyarray(ij_inds)
        vals = np.asanyarray(vals)

        if not assume_sorted:
            sorting = None
        else:
            sorting = np.arange(ij_inds.shape[1])

        if memmap:
            raise NotImplementedError("meh")
        else:
            indptr = np.zeros(shape[axis] + 1, dtype=infer_inds_dtype(ij_inds.shape[1]+1))
            indices = ij_inds[other]#.astype(indptr.dtype)

        urows, sorting, ucounts = nput_unique(ij_inds[axis], sorting=sorting, return_counts=True)
        # urows, ucounts = np.unique(ij_inds[axis], return_counts=True)
        indptr[urows+1] = ucounts.astype(indptr.dtype)
        # gc.collect()
        indptr = np.cumsum(indptr, out=indptr)

        if not assume_sorted:
            indices = indices[sorting]
            vals = vals[sorting]

        # if shape[0] > shape[1]:
        #     real = sp.csc_matrix((vals, ij_inds), shape=shape)
        # else:
        #     real = sp.csr_matrix((vals, ij_inds), shape=shape)
        # print("??", indptr.shape, indptr)
        # print(">>", real.indptr.shape, real.indptr)
        # print("??", indices.shape, indices)
        # print(">>", real.indices.shape, real.indices)

        # meh = sp.csr_matrix((vals, indices, indptr), shape=shape)
        # a, b, c = sp.find(meh)
        # feh = sp.csr_matrix((vals, ij_inds), shape=shape)
        # d, e, f = sp.find(feh)
        #
        #
        # assert np.allclose(a, d)

        return cls._init_cs(vals, indices, indptr, shape)
        # we'll assume no duplicate entries...

        # coo_tocsr(M, N, self.nnz, row, col, self.data,
        #           indptr, indices, data)

    @classmethod
    # @profile
    def _init_cs(cls, vals, indices, indptr, shape):
        if shape[0] > shape[1]:
            res = sp.csc_matrix((vals, indices, indptr), shape=shape)
        else:
            res = sp.csr_matrix((vals, indices, indptr), shape=shape)
        # print("?>>>>>?", res.nnz, len(vals), len(indices), len(indptr), indptr[0], indptr[-1])
        return res

    def to_state(self, serializer=None):
        """
        Provides just the state that is needed to
        serialize the object
        :param serializer:
        :type serializer:
        :return:
        :rtype:
        """
        return {
            'layout': serializer.serialize(self._fmt),
            'shape': self.shape,
            'dtype': self.dtype.name,
            'block_data': self.block_data
        }
    @classmethod
    def from_state(cls, state, serializer=None):
        block_vals, block_inds = state['block_data']
        block_vals = np.asarray(block_vals)
        block_inds = tuple(np.asarray(x) for x in block_inds)
        return cls(
            (block_vals, block_inds),
            dtype=np.dtype(state['dtype']),
            layout=serializer.deserialize(state['layout']),
            shape=state['shape']
        )
    @classmethod
    def initialize_empty(cls, shape, dtype=None, layout=None, **kw):
        matshape = cls._get_balanced_shape(shape)
        if dtype is None:
            dtype=np.float64
        if layout is None:
            if matshape[0] > matshape[1]:
                layout = sp.csc_matrix
            else:
                layout = sp.csr_matrix
        new = cls(layout(matshape, dtype=dtype), shape=shape, **kw)
        return new
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

        cumprods_left = np.cumprod(shp)
        cumprods_right = np.flip(np.cumprod(np.flip(shp)))
        vl, vr = o_vl, o_vr = 1, cumprods_right[0]
        for vl, vr in zip(cumprods_left, cumprods_right[1:]):
            if vr == vl: # perfect balance
                break
            elif vr < vl:
                if (vr / vl) < (o_vl / o_vr):
                    vl, vr = o_vl, o_vr
                break
            o_vl, o_vr = vl, vr

        return (vl, vr)

    # from memory_profiler import profile
    # @profile
    def _init_matrix(self, cache_block_data=True, init_kwargs=None):
        a = self._a
        if isinstance(a, ScipySparseArray):
            if self.logger is not None:
                self.logger.log_print("initializing from existing `SparseArray`", log_level=self.logger.LogLevel.Debug)
            if self.fmt is not a.fmt:
                self._a = self.fmt(a._a, shape=a.shape)
            else:
                self._a = a._a
            shp = self._shape
            if shp is not None:
                self.reshape(a.shape)
            else:
                self._shape = a.shape
        elif isinstance(a, sp.spmatrix):
            if self.logger is not None:
                self.logger.log_print("initializing from existing `spmatrix`", log_level=self.logger.LogLevel.Debug)
            if self._shape is None:
                self._shape = a.shape
        elif isinstance(a, np.ndarray):
            self._shape = a.shape
            if len(a.shape) > 2:
                # we want this to be more balanced b.c. it helps for transposes
                total_shape = self._get_balanced_shape(a.shape)
                a = a.reshape(total_shape)
            elif len(a.shape) == 1:
                a = a.reshape(a.shape + (1,))
            if self._fmt is None:
                if a.shape[0] > a.shape[1]:
                    fmt = sp.csc_matrix
                else:
                    fmt = sp.csr_matrix
            elif isinstance(self._fmt, str):
                fmt = self.format_from_string(self._fmt)
            else:
                fmt = self._fmt
            if self.logger is not None:
                self.logger.log_print("initializing from `ndarray`", log_level=self.logger.LogLevel.Debug)
            self._a = fmt(a, shape=a.shape)

        # we're gonna support the (vals, (i_1, i_2, i_3, ...)) syntax for constructing
        # an array based on its non-zero positions
        elif len(a) == 2 and len(a[1]) > 0 and len(a[0]) == len(a[1][0]):
            if self.logger is not None:
                self.logger.log_print("initializing from vals and indices", log_level=self.logger.LogLevel.Debug)
            if init_kwargs is None:
                init_kwargs = {}
            data, block_vals, block_inds, self._shape = self.construct_sparse_from_val_inds(
                a, self._shape, self._fmt,
                cache_block_data=cache_block_data,
                **init_kwargs
            )
            self._a = data
            if cache_block_data and block_inds is not None: # corner case to avoid a sort in low-mem situation
                self._block_vals = block_vals
                self._block_inds = block_inds
                self._block_data_sorted = True
        else:
            non_sparse, sparse = self._get_shape()
            if non_sparse is None:
                self._a = np.array(self._a)
                self._init_matrix()
            else:
                self._shape = non_sparse + sparse
                data, other = self._get_data(non_sparse, sparse)
                block_data, inds, total_shape = other
                self._a = data
                if cache_block_data:
                    flat = np.ravel_multi_index(inds, data.shape)
                    self._block_inds = flat, inds
                    self._block_data_sorted = False

    @classmethod
    def construct_sparse_from_val_inds(cls, a, shape, fmt,
                                       cache_block_data=True, logger=None,
                                       assume_sorted=False
                                       ):
        block_vals, block_inds = a
        # import sys
        # print("???2", sys.getrefcount(block_vals), sys.getrefcount(block_inds))
        # print("?", shape, min(block_inds[0]), max(block_inds[1]))
        block_vals = np.asanyarray(block_vals)
        if shape is None:
            shape = tuple(np.max(x) for x in block_inds)

        # special case esp. for square matrices
        shape_rat = max(shape) / min(shape)
        if len(shape) == 2 and shape_rat < 5:
            init_inds = block_inds
            total_shape = shape
            block_inds = None
        else:
            block_inds = tuple(np.asanyarray(i) for i in block_inds)
            if isinstance(a, cls.initializer_list):
                a[1] = None
            if len(block_inds) != len(shape):
                raise ValueError("{}: can't initialize array of shape {} from non-zero indices of dimension {}".format(
                    cls.__name__,
                    shape,
                    len(block_inds)
                ))

            if logger is not None:
                logger.log_print("calculating flat indices", log_level=logger.LogLevel.Debug)

            flat = np.ravel_multi_index(block_inds, shape)  # no reason to cache this since we're going to sort it...
            if cache_block_data:
                if logger is not None:
                    logger.log_print("sorting cached data", log_level=logger.LogLevel.Debug)
                # gotta make sure our inds are sorted so we don't run into sorting issues later...
                sort = np.argsort(flat)
                flat = flat[sort]
                block_vals = block_vals[sort]
                block_inds = (flat, tuple(i[sort] for i in block_inds))
                del sort  # clean up for memory reasons

            if logger is not None:
                logger.log_print("constructing 2D indices", log_level=logger.LogLevel.Debug)
            # this can help significantly with memory usage...
            total_shape = cls._get_balanced_shape(shape)
            init_inds = np.unravel_index(flat, total_shape)  # no reason to cache this since we're not going to use it

            if not cache_block_data:
                block_inds = None
                del flat

        if fmt is None:
            if total_shape[0] > total_shape[1]:
                fmt = sp.csc_matrix
            else:
                fmt = sp.csr_matrix
        elif isinstance(fmt, str):
            fmt = cls.format_from_string(fmt)

        if logger is not None:
            logger.log_print("initializing {fmt} from indices and values", fmt=fmt, log_level=logger.LogLevel.Debug)

        if fmt in [sp.csc_matrix, sp.csr_matrix]:
            data = cls.coo_to_cs(total_shape, block_vals, init_inds, assume_sorted=assume_sorted)
            if isinstance(a, cls.initializer_list):
                a[0] = None

            if fmt is sp.csc_matrix and data.format is sp.csr_matrix:
                data = data.asformat('csc', copy=False)
            elif fmt is sp.csr_matrix and data.format is sp.csc_matrix:
                data = data.asformat('csr', copy=False)
        else:
            try:
                data = fmt((block_vals, init_inds), shape=total_shape)
            except TypeError:
                data = fmt(sp.coo_matrix((block_vals, init_inds)), shape=total_shape)
            except MemoryError:
                if total_shape[0] > total_shape[1]:
                    fmt = sp.csc_matrix
                else:
                    fmt = sp.csr_matrix
                data = fmt((block_vals, init_inds), shape=total_shape)

            if isinstance(a, cls.initializer_list):
                a[0] = None

        if not cache_block_data:
            block_vals = None

        return data, block_vals, block_inds, shape

    def _validate(self):
        shp1 = self._a.shape
        shp2 = self._shape
        if np.prod(shp1) != np.prod(shp2):
            raise ValueError("sparse data with shape {} cannot correspond to shape {}".format(
                shp1,
                shp2
            ))
        self._validated = True
    def _get_shape(self):
        """
        Walks through the array data we're holding onto and determines
        where the sparse blocks start
        """
        non_sp = []
        elm = self._a
        while not isinstance(elm, sp.spmatrix):
            try:
                elm_2 = elm[0]
            except (TypeError, IndexError):
                return None, None
            else:
                non_sp.append(len(elm))
                elm = elm_2
        else: # only catch if no break
            shape = elm.shape

        non_sparse_shape = tuple(non_sp)
        return non_sparse_shape, tuple(shape)
    def _get_data(self, non_sparse, sparse):
        """
        We'll take our blocks and arrange them as a vector of sparse arrays
        """
        inds = ip.product(*(list(range(x)) for x in non_sparse))
        a = self._a
        bits = np.cumprod(non_sparse) # so that we can build our vector of blocks
        if len(sparse) == 1:
            sparse = sparse+(1,)
        def pull(a, idx, bits=bits, shp = sparse):
            block = fp.reduce(lambda b,i:b[i], idx, a)
            if not isinstance(block, (sp.spmatrix, np.ndarray)):
                block = np.array(block)
            block_data, row_ind, col_ind = sp.find(block)
            offset = np.dot(idx, bits)*shp[1]
            return block_data, row_ind, col_ind + offset

        blocks = [pull(a, idx) for idx in inds]
        block_data = np.concatenate([b[2] for b in blocks])
        row_inds = np.concatenate([b[0] for b in blocks])
        col_inds = np.concatenate([b[1] for b in blocks])
        total_shape = (sparse[0], bits[-1]*sparse[1])
        inds = (row_inds, col_inds)
        data = self._build_data(block_data, inds, total_shape)
        return data, (block_data, inds, total_shape)
    def _build_data(self, block_data, inds, total_shape):
        if len(block_data) == 0 or np.prod(block_data.shape) == 0.: # empty array
            if total_shape[0] > total_shape[1]:
                base_sparse = sp.coo_matrix(total_shape, dtype=self.dtype)
            else:
                base_sparse = sp.coo_matrix(total_shape, dtype=self.dtype)
            try:
                return self.fmt(base_sparse)
            except MemoryError:
                self._fmt = base_sparse.format
                return base_sparse

        # shp = self.shape
        # if len(shp) == 5 and shp[:4] == (12, 12, 12, 12):
        #     raise RuntimeError(self.shape, self.fmt, total_shape, "why")

        try:
            data = self.fmt((block_data, inds), shape=total_shape, dtype=self.dtype)
        except (ValueError, TypeError):
            if total_shape[0] > total_shape[1]:
                base_sparse = sp.csc_matrix(total_shape, dtype=self.dtype)
            else:
                base_sparse = sp.csr_matrix(total_shape, dtype=self.dtype)
            try:
                data = self.fmt(base_sparse)
            except MemoryError:
                data = base_sparse
                self._fmt = base_sparse.format
        return data

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def diag(self):
        if len(self.shape) != 2:
            raise NotImplementedError("haven't decided what I want to do for tensors")
        N = np.min(self.shape)
        diag = self[np.arange(N), np.arange(N)]
        return diag.flatten()

    @classmethod
    def from_diagonal_data(cls, diags, shape=None, **kw):
        if isinstance(diags[0], (int, np.integer, float, np.floating)):
            # just a plain old diagonal matrix
            N = len(diags)
            # print(len(diags))
            if shape is None:
                shape = (N, N)
            return cls(sp.csr_matrix(sp.diags([diags], [0])), shape=shape, **kw)
        else:
            data = sp.block_diag(diags, format='csr')
            block_size = diags[0].shape
            if shape is None:
                shape = (len(diags), block_size[0], len(diags), block_size[1])
            wat = cls(data, shape=shape, **kw).transpose((0, 2, 1, 3))
            return wat
    def iter_nonzero_blocks(self, block_size=65536, value_filter=None):
        """Scan CSR/CSC/COO storage without creating or caching full coordinates.

        The predicate sees at most block_size values. Coordinates are expanded
        only for its retained entries. No matrix conversion or global sort.
        """
        if not isinstance(block_size, (int, np.integer)) or block_size < 1:
            raise ValueError('block_size must be a positive integer')
        matrix = self.data
        if matrix.format not in {'csr','csc','coo'}:
            raise NotImplementedError('stored-entry blocks require CSR, CSC or COO storage')
        for start in range(0,len(matrix.data),block_size):
            stop = min(start+block_size,len(matrix.data))
            values = matrix.data[start:stop]
            selected = np.arange(start,stop)
            if value_filter is not None:
                keep = np.asarray(value_filter(values),dtype=bool)
                if keep.shape != values.shape:raise ValueError('value_filter must return one boolean per value')
                selected = selected[keep];values = values[keep]
            if not len(selected):continue
            if matrix.format == 'coo':rows,columns = matrix.row[selected],matrix.col[selected]
            else:
                major = np.searchsorted(matrix.indptr,selected,side='right')-1
                minor = matrix.indices[selected]
                rows,columns = (major,minor) if matrix.format == 'csr' else (minor,major)
            if self.ndim == 2 and tuple(self.shape) == tuple(matrix.shape):indices = (rows,columns)
            else:
                flat = np.ravel_multi_index((rows,columns),matrix.shape)
                indices = np.unravel_index(flat,self.shape)
            yield values,indices

    def asarray(self):
        return np.reshape(self.data.toarray(), self.shape)
    def todense(self):
        return np.reshape(np.asarray(self.data.todense()), self.shape)
    def ascoo(self):
        return sp.coo_matrix(self.data)
    def ascsr(self):
        return sp.csr_matrix(self.data)
    def ascsc(self):
        return sp.csc_matrix(self.data)
    @property
    def data(self):
        if not isinstance(self._a, sp.spmatrix):
            self._init_matrix()
        if not self._validated:
            self._validate()
        return self._a
    @data.setter
    def data(self, new):
        if not isinstance(new, sp.spmatrix):
            raise ValueError("new underlying sparse buffer must be of type {}".format(
                sp.spmatrix
            ))
        elif np.prod(new.shape) != np.prod(self.shape):
            raise ValueError("can't use sparse buffer of shape {} for tensor of shape {}".format(
                new.shape,
                self.shape
            ))
        else:
            if new.format != self.data.format:
                new = self.fmt(new)
            self._a = new
    formats_map = {
        'csr': sp.csr_matrix,
        'csc': sp.csc_matrix,
        'coo': sp.coo_matrix
    }
    @classmethod
    def format_from_string(cls, fmt):
        if isinstance(fmt, str):
            return cls.formats_map[fmt]
        elif isinstance(fmt, type):
            return fmt
        else:
            raise TypeError("not sure how to get a valid sparse format class from {}".format(fmt))
    @property
    def fmt(self):
        if self._fmt is None:
            return self.format_from_string(self.data.format)
        elif isinstance(self._fmt, str):
            return self.format_from_string(self._fmt)
        else:
            return self._fmt
    @property
    def shape(self):
        if self._shape is None:
            self._init_matrix()
        if not self._validated:
            self._validate()
        return self._shape
    @property
    def ndim(self):
        return len(self.shape)
    @property
    def non_zero_count(self):
        return self.data.nnz
    # def __len__(self):
    #     return self.shape[0]
    default_cache_size = 2
    caching_enabled=True
    @classmethod
    def get_caching_status(cls):
        return cls.caching_enabled
    @classmethod
    def enable_caches(self):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to turn this on
        :return:
        :rtype:
        """
        self.caching_enabled = True
    @classmethod
    def disable_caches(self):
        """
        A method to be overloaded.
        Subclasses may want to cache things for performance, so we
        provide a way for them to turn this off
        :return:
        :rtype:
        """
        self.caching_enabled = False
    @classmethod
    def clear_cache(cls):
        cls.clear_ravel_caches()
    @classmethod
    def clear_ravel_caches(cls):
        cls._unravel_cache = MaxSizeCache(cls.default_cache_size)
        cls._ravel_cache = MaxSizeCache(cls.default_cache_size)

    # this saves time when we have to do a bunch of reshaping into similarly sized arrays,
    # but won't help as much when the shape changes
    _unravel_cache = MaxSizeCache(default_cache_size)  # hopefully faster than bunches of unravel_index calls...

    @classmethod
    def _unravel_indices(cls, n, dims):

        # we're hoping that we call with `n` often enough that we get a performance benefit
        if not cls.caching_enabled:
            minimal_dtype = infer_inds_dtype(np.max(dims))
            res = tuple(x.astype(minimal_dtype) for x in np.unravel_index(n, dims))
            return res
        if dims not in cls._unravel_cache:
            cls._unravel_cache[dims] = MaxSizeCache(cls.default_cache_size)
        cache = cls._unravel_cache[dims]

        if isinstance(n, np.ndarray):
            n_hash = hash(n.data.tobytes())
        else:
            n_hash = hash(n)

        if n_hash in cache:
            res = cache[n_hash]
        else:
            minimal_dtype = infer_inds_dtype(np.max(dims))
            res = tuple(x.astype(minimal_dtype) for x in np.unravel_index(n, dims))
            cache[n_hash] = res
        return res

    # we cache the common ops...
    @classmethod
    def set_ravel_cache_size(cls, size):
        cls.default_cache_size = size
        if cls._ravel_cache is None:
            cls._ravel_cache = MaxSizeCache(size)
        elif cls._ravel_cache.max_items != size:
            cls._ravel_cache = MaxSizeCache(size)

        if cls._unravel_cache is None:
            cls._unravel_cache = MaxSizeCache(size)
        elif cls._unravel_cache.max_items != size:
            cls._unravel_cache = MaxSizeCache(size)


    _ravel_cache = MaxSizeCache(default_cache_size)  # hopefully faster than bunches of ravel_index calls...
    @classmethod
    def _ravel_indices(cls, mult, dims):
        # we're hoping that we call with `n` often enough that we get a performance benefit
        # # need to make sure all mult objects have same dtype...
        # dtypes = {m.dtype for m in mult}
        # max_dtype = max(dtypes)
        # mult = tuple(m.astype(max_dtype) for m in mult)
        if not cls.caching_enabled:
            return np.ravel_multi_index(mult, dims)
        if isinstance(dims, list):
            dims = tuple(dims)
        if dims not in cls._ravel_cache:
            cls._ravel_cache[dims] = MaxSizeCache(cls.default_cache_size)
        cache = cls._ravel_cache[dims]
        if isinstance(mult[0], np.ndarray):
            n_hash = hash(tuple(m.data.tobytes() for m in mult))
        else:
            try:
                n_hash = hash(mult)
            except TypeError:
                # means hashing failed so we just shortcut out rather than try to be clever
                # raise Exception([mult, dims])
                return np.ravel_multi_index(mult, dims)
        if n_hash in cache:
            res = cache[n_hash]
        else:
            try:
                res = np.ravel_multi_index(mult, dims)
            except:
                raise Exception(mult, dims)
            cache[n_hash] = res
        return res

    def _getinds(self):
        # pulled from tocoo except without the final conversion to COO...
        from scipy.sparse import _sparsetools

        data = self.data
        major_dim, minor_dim = data._swap(data.shape)
        minor_indices = data.indices
        major_indices = np.empty(len(minor_indices), dtype=data.indices.dtype)
        _sparsetools.expandptr(major_dim, data.indptr, major_indices)
        row, col = data._swap((major_indices, minor_indices))

        return row, col
    def find(self):
        fmt = self.data.format
        if fmt in ['csr', 'csc']:
            d = self.data # type: sp.csr_matrix
            vals = d.data
            row_inds, col_inds = self._getinds()
        else:
            row_inds, col_inds, vals = sp.find(self.data)
        return row_inds, col_inds, vals


    # import memory_profiler
    # @memory_profiler.profile
    def _load_block_data(self):
        d = self.data

        row_inds, col_inds, data = self.find()

        flat = self._ravel_indices((row_inds, col_inds), d.shape)
        sort = np.argsort(flat)
        flat = flat[sort]
        data = data[sort]
        unflat = self._unravel_indices(flat, self.shape)
        self._block_inds = (flat, unflat)
        self._block_vals = data
        self._block_data_sorted = True

    def _load_full_block_inds(self):
        if self._block_inds.ndim == 1:
            flat = self._block_inds
            unflat = self._unravel_indices(flat, self.shape)
        else:
            unflat = self._block_inds
            flat = self._ravel_indices(unflat, self.shape)
        self._block_inds = (flat, unflat)

    def _sort_block_data(self):
        flat, unflat = self._block_inds
        sort = np.argsort(flat)
        flat = flat[sort]
        unflat = tuple(x[sort] for x in unflat)
        self._block_inds = (flat, unflat)
        self._block_vals = self._block_vals[sort]
        self._block_data_sorted = True

    @property
    def block_vals(self):
        if self._block_vals is None:
            self._load_block_data()
        if not self._block_data_sorted:
            self._sort_block_data()
        return self._block_vals
    @block_vals.setter
    def block_vals(self, bv):
        self._block_vals = bv


    @property
    def block_inds(self):
        if self._block_inds is None:
            self._load_block_data()
        elif not (
                isinstance(self._block_inds[0], np.ndarray)
                and self._block_inds[0].ndim == 1
        ):
            self._load_full_block_inds()
        if not self._block_data_sorted:
            self._sort_block_data()
        return self._block_inds
    @block_inds.setter
    def block_inds(self, bi):
        if bi is None:
            self._block_inds = None
        else:
            if isinstance(bi, tuple) and len(bi) == 2:
                flat, unflat = bi
                if isinstance(unflat[0], int):
                    row_inds, col_inds = bi
                    flat = self._ravel_indices((row_inds, col_inds), self.data.shape)
                    unflat = self._unravel_indices(flat, self.shape)
            elif isinstance(bi[0], int):
                flat = bi
                unflat = self._unravel_indices(flat, self.shape)
            else:
                unflat = bi
                flat = self._ravel_indices(bi, self.shape)
            if len(unflat) != len(self.shape):
                raise ValueError("{}: block indices must have same dimension as array ({}); was given {}".format(
                    type(self).__name__,
                    len(self.shape),
                    len(unflat)
                ))
            if self._block_vals is not None and len(flat) != len(self._block_vals):
                    raise ValueError("{}: number of block indices must match number of non-zero elements ({}); was given {}".format(
                        type(self).__name__,
                        len(self._block_vals),
                        len(flat)
                    ))
            self._block_inds = (flat, unflat)
    @property
    def block_data(self):
        res = self.block_vals, self.block_inds[1]
        return res
    @block_data.setter
    def block_data(self, bd):
        if bd is None:
            self.block_vals = None
            self.block_inds = None
        else:
            self.block_vals, self.block_inds = bd


    # import memory_profiler
    # @memory_profiler.profile
    def transpose(self, transp):
        """
        Transposes the array and returns a new one.
        Not necessarily a cheap operation.

        :param transp: the transposition to do
        :type transp: Iterable[int]
        :return:
        :rtype:
        """

        # import time

        shp = self.shape

        if len(transp) != self.ndim or np.any(np.sort(transp) != np.arange(self.ndim)):
            raise ValueError("transposition {} can't apply to shape {}".format(
                transp, self.shape
            ))

        if self.ndim == 2 and tuple(self.shape) == tuple(self.data.shape):
            data = self.data.copy() if tuple(transp) == (0,1) else self.data.transpose(copy=True)
            return type(self)(data,shape=tuple(shp[i] for i in transp),layout=type(data),initialize=False)

        track_data = self.get_caching_status()
        if self._block_vals is None:
            row_inds, col_inds, data = self.find()
            flat = self._ravel_indices((row_inds, col_inds), self.data.shape)
            del row_inds
            del col_inds
            inds = self._unravel_indices(flat, self.shape)
            del flat
            new_inds = [inds[i] for i in transp]
            del inds
        else:
            data = self.block_vals
            (flat, inds) = self.block_inds
            new_inds = [inds[i] for i in transp]

        new_shape = tuple(shp[i] for i in transp)
        if len(data) == 0:
            return type(self).empty(new_shape, layout=self.fmt, dtype=data.dtype)

        if len(new_shape) > 2:
            total_shape = self._get_balanced_shape(new_shape)
            flat = self._ravel_indices(new_inds, new_shape)
            unflat = self._unravel_indices(flat, total_shape)
        else:
            flat = None
            unflat = new_inds
            total_shape = new_shape

        # time.sleep(.5)
        data = self._build_data(data, unflat, total_shape)
        if not track_data:
            del flat
            del unflat
            del new_inds
            del total_shape
        # except MemoryError:
        #     raise Exception(data, unflat, new_shape, total_shape)
        new = type(self)(data, shape=new_shape, layout=self.fmt, initialize=False) # this is tuned for SciPySparse array...
        # time.sleep(.5)

        if track_data:

            if flat is not None:
                arr = np.argsort(flat)
            else:
                arr = np.lexsort(unflat)

            new_inds = [inds[arr] for inds in new_inds]
            if self._block_vals is not None:
                new_v = self._block_vals[arr]
                new._block_vals = new_v
            if flat is None:
                new.block_inds = new_inds
            else:
                # try:
                new.block_inds = (flat[arr], new_inds)
            new._block_data_sorted = True
                # except:
                #     raise Exception(new_shape, len(total_shape))

        return new

    # def transpose(self, transp):
    #     """
    #     Transposes the array and returns a new one.
    #     Not necessarily a cheap operation.
    #
    #     :param transp: the transposition to do
    #     :type transp: Iterable[int]
    #     :return:
    #     :rtype:
    #     """
    #
    #     if len(self.shape) > 4:
    #         return self.profiled_transpose(transp)
    #
    #     shp = self.shape
    #
    #     if len(transp) != self.ndim or np.any(np.sort(transp) != np.arange(self.ndim)):
    #         raise ValueError("transposition {} can't apply to shape {}".format(
    #             transp, self.shape
    #         ))
    #
    #     data, inds = self.block_data
    #
    #     new_inds = [inds[i] for i in transp]
    #     new_shape = tuple(shp[i] for i in transp)
    #     if len(data) == 0:
    #         return type(self).empty(new_shape, layout=self.fmt, dtype=data.dtype)
    #
    #     if len(new_shape) > 2:
    #         total_shape = self._get_balanced_shape(new_shape)
    #         flat = self._ravel_indices(new_inds, new_shape)
    #         unflat = self._unravel_indices(flat, total_shape)
    #     else:
    #         flat = None
    #         unflat = new_inds
    #         total_shape = new_shape
    #
    #     data = self._build_data(data, unflat, total_shape)
    #     new = type(self)(data, shape = new_shape, layout = self.fmt)
    #
    #     arr = np.lexsort(unflat)
    #
    #     new_inds = [inds[arr] for inds in new_inds]
    #     if self._block_vals is not None:
    #         new_v = self._block_vals[arr]
    #         new._block_vals = new_v
    #     if flat is None:
    #         new.block_inds = new_inds
    #     else:
    #         new.block_inds = (flat, new_inds)
    #
    #     return new

    def reshape_internal(self, shp):
        # TODO: find a way to do with a resize instead of making a new
        #       array

        if np.prod(shp) < np.prod(self.shape):
            raise ValueError("can't reshape {} into {}...".format(self.shape, shp))

        # cur_size = np.prod(self.shape)
        # new_size = np.prod(shp)

        self._shape = tuple(shp)
        # if new_size > cur_size:
        #     new_matshape = self.data.shape
        #     bi = self._block_inds
        #     if bi is not None:
        #         if isinstance(bi, np.ndarray) and bi.ndim == 1:
        #             flat = bi
        #         else:
        #             flat, unflat = bi
        #         # unflat = self._unravel_indices(flat, self.data.shape)
        #         # new_flat = self._ravel_indices(unflat, new_matshape)
        #         # if unflat is not None:
        #         #     flat = self._ravel_indices(unflat, shp)
        #         #     self._block_inds = (flat, unflat)
        #         # else:
        #         self._block_vals = None
        #         self._block_inds = None
        #         self._block_data_sorted = False
        #     # self.data.resize(new_matshape)
        # else:
        bi = self._block_inds
        if bi is not None:
            if isinstance(bi, np.ndarray) and bi.ndim == 1:
                self._block_inds = bi
            else:
                flat, unflat = bi
                self._block_inds = flat
        if len(shp) == 2 and np.prod(shp) == np.prod(self.shape):
            self.data = self.data.reshape(shp) # turns out this can break shit...

    def reshape(self, shp):
        """
        Had to make this op not in-place because otherwise got scary errors...
        :param shp:
        :type shp:
        :return:
        :rtype:
        """

        if np.prod(shp) != np.prod(self.shape):
            raise ValueError("Can't reshape {} into {}".format(self.shape, shp))
        new = self.copy() # I'm not sure I want a whole copy here...?
        new.reshape_internal(shp)
        return new
    def pad_right(self, amounts):
        shp = self.shape
        if len(amounts) != len(shp): raise ValueError("can't pad {} onto shape {}".format(amounts, shp))
        new_shape = [s+a for a,s in zip(amounts, shp)] #+ amounts[len(shp):]
        return type(self)(self.block_data, shape=new_shape)
    def squeeze(self):
        self.reshape([x for x in self.shape if x != 1])
        return self

    def resize(self, newsize):
        """
        Returns a resized version of the tensor
        :param newsize:
        :type newsize: tuple[int]
        :return:
        :rtype:
        """
        # we'll simply construct a totally new tensor by dropping any indices which are out of bounds
        # in any coordinate
        # otherwise the multidimensional indices are clean so we'll just use those
        if len(newsize) != self.ndim:
            raise ValueError("unclear how to resize a tensor with rank {} into a tensor of rank {}".format(
                self.ndim,
                len(newsize)
            ))

        if len(newsize) == 2:
            return type(self)(self.data.copy().resize(newsize), shape=newsize)

        vals, inds = self.block_data
        # now we've got to filter out the indices which are out of bounds in any dimension
        for i,sizes in enumerate(zip(newsize, self.shape)):
            n, o = sizes
            if n < o:
                mask = inds[:i]
                vals = vals[mask]
                inds = inds[mask]

        return type(self)((vals, inds), shape=newsize)

    @staticmethod
    def _concat_coo(all_inds, all_vals, all_shapes, axis):

        full_vals = np.concatenate(all_vals)

        tot_shape = list(all_shapes[0])
        tot_shape[axis] = sum(a[axis] for a in all_shapes)

        # pull all the shapes along the concatenation axis

        # add the offset to each block along the concatenation axis
        # to create new vector of inds
        full_inds = None
        prev = 0
        for offset, ind_block in zip(all_shapes, all_inds):
            if full_inds is None:
                full_inds = ind_block
                prev += offset[axis]
            else:
                ind_block = ind_block[:axis] + (ind_block[axis] + prev,) + ind_block[axis + 1:]
                prev += offset[axis]
                full_inds = tuple(
                    np.concatenate([a, b])
                    for a, b in zip(full_inds, ind_block)
                )

        return full_vals, full_inds, tot_shape

    def concatenate_coo(self, *others, axis=0):
        all_inds = [self.block_inds[1]] + [other.block_inds[1] for other in others]
        all_vals = [self.block_vals] + [other.block_vals for other in others]
        all_shapes = [self.shape] + [other.shape for other in others]

        full_vals, full_inds, tot_shape = self._concat_coo(all_inds, all_vals, all_shapes, axis)

        return type(self)(
            (
                full_vals,
                full_inds
            ),
            shape=tot_shape
        )

    # @profile
    # def _build_concat_inds(self, blocks, data, idx_dtype, axis, other_axis, constant_dim):
    #
    #     indices = np.empty(data.size, dtype=idx_dtype)
    #     indptr = np.empty(sum(b.shape[axis] for b in blocks) + 1, dtype=idx_dtype)
    #     last_indptr = idx_dtype(0)
    #     sum_dim = 0
    #     sum_indices = 0
    #     for b in blocks:
    #         if b.shape[other_axis] != constant_dim:
    #             raise ValueError('incompatible dimensions for axis %d' % other_axis)
    #         indices[sum_indices:sum_indices + b.indices.size] = b.indices
    #         sum_indices += b.indices.size
    #         idxs = slice(sum_dim, sum_dim + b.shape[axis])
    #         indptr[idxs] = b.indptr[:-1]
    #         indptr[idxs] += last_indptr
    #         sum_dim += b.shape[axis]
    #         last_indptr += b.indptr[-1]
    #     indptr[-1] = last_indptr
    #
    #     return indices, indptr, sum_dim
    #
    # @profile
    # def _fast_stack(self, blocks, axis):
    #     """
    #     Copy from scipy.sparse.construct...
    #     Stacking fast path for CSR/CSC matrices
    #     (i) vstack for CSR, (ii) hstack for CSC.
    #     """
    #     from scipy.sparse.compressed import get_index_dtype
    #
    #     import time
    #     time.sleep(.5)
    #
    #     other_axis = 1 if axis == 0 else 0
    #     data = np.concatenate([b.data for b in blocks])
    #     constant_dim = blocks[0].shape[other_axis]
    #     idx_dtype = get_index_dtype(arrays=[b.indptr for b in blocks],
    #                                 maxval=max(data.size, constant_dim))
    #
    #     indices, indptr, sum_dim = self._build_concat_inds(blocks, data, idx_dtype, axis, other_axis, constant_dim)
    #
    #     return self._construct_mat(data, indices, indptr, sum_dim, constant_dim, axis)
    #
    # def _construct_mat(self, data, indices, indptr, sum_dim, constant_dim, axis):
    #     if axis == 0:
    #         return sp.csr_matrix((data, indices, indptr),
    #                           shape=(sum_dim, constant_dim))
    #     else:
    #         return sp.csc_matrix((data, indices, indptr),
    #                           shape=(constant_dim, sum_dim))

    def _stack_data(self, dats, axis):
        # return self._fast_stack(dats, axis)
        return (
            sp.hstack(dats)
            if axis == 1 else sp.vstack(dats)
        )

    # @profile
    def concatenate_2d(self, *others, axis=0):
        dats = [self.data] + [o.data for o in others]

        all_shapes = [self.shape] + [other.shape for other in others]
        tot_shape = list(self.shape)
        tot_shape[axis] = sum(a[axis] for a in all_shapes)

        if self.ndim == 1:
            axis = 1
        return type(self)(
            self._stack_data(dats, axis),
            shape=tot_shape
        )

    # @profile
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

        others = [
            ScipySparseArray(o)
                if not isinstance(o, ScipySparseArray) else
            o
            for o in others
        ]

        # all_inds = [self.block_inds[1]] + [other.block_inds[1] for other in others]
        # all_vals = [self.block_vals] + [other.block_vals for other in others]
        # all_shapes = [self.shape] + [other.shape for other in others]
        #
        # full_vals, full_inds, tot_shape = self._concat_coo(all_inds, all_vals, all_shapes, axis)
        #
        # return type(self)(
        #     (
        #         full_vals,
        #         full_inds
        #     ),
        #     shape=tot_shape
        # )

        if (
                self.fmt is sp.csr_matrix and axis == 0
                or self.fmt is sp.csc_matrix and axis == 1
        ):
            # return self.concatenate_2d(*(o for o in others if o.non_zero_count > 0), axis=axis)
            # this was breaking the shape constraints
            return self.concatenate_2d(*others, axis=axis)
        else:
            return self.concatenate_coo(*others, axis=axis)

    # def broadcast_to(self, shp):
    #     """
    #     Had to make this op not in-place because otherwise got scary errors...
    #     :param shp:
    #     :type shp:
    #     :return:
    #     :rtype:
    #     """
    #
    #     curshp = self.shape
    #     if (
    #             len(shp) != len(curshp)
    #             or not all(os == ns or os == 1 for os, ns in zip(self.shape, shp))
    #     ):
    #         raise ValueError("can't broadcast {} to {}".format(self.shape, shp))
    #     block_vals, block_inds = self.block_data # why not cache it on self if I'm gonna need it...
    #     for i,(os, ns) in enumerate(zip(self.shape, shp, block_inds)):
    #         if ns != os: # we know from above os == 1
    #             ndupes = ns
    #             cursize = len(block_vals)
    #             block_vals = np.concatenate([block_vals] * ndupes)
    #             block_inds = tuple(
    #                 np.concatenate([bis] * ndupes)
    #                     if j != i else
    #                 np.broadcast_to(np.arange(ndupes)[:, np.newaxis], (ndupes, cursize)).flatten()
    #                 for j,bis in zip(block_inds)
    #             )
    #     return type(self)((block_vals, block_inds), shape=shp)

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

        # precheck b.c. concatenate is expensive
        # TODO: this has changed to be fully compatible with standard broadcast_to --> is that an issue?
        compat = all(a == b or b == 1 for a, b in zip(new_shape, old_shape))
        if not compat:
            raise ValueError("{} with shape {} can't be broadcast to shape {}".format(
                cls.__name__,
                old_shape,
                new_shape
            ))

        full_vals = vals
        full_inds = inds
        tot_shape = old_shape

        for i, (shs, sho) in enumerate(zip(old_shape, new_shape)):
            if shs != sho:
                reps = sho // shs

                all_vals = [full_vals] * reps
                all_inds = [full_inds] * reps
                all_shapes = [tot_shape] * reps

                full_vals, full_inds, tot_shape = cls._concat_coo(all_inds, all_vals, all_shapes, i)

        return cls(
            (
                full_vals,
                full_inds
            ),
            shape=tot_shape
        )
    def broadcast_to(self, shape):
        """
        Broadcasts to shape
        :param shape:
        :return:
        """

        if shape == self.shape:
            return self

        return self.broadcast_values(
            shape,
            self.shape,
            self.block_vals,
            self.block_inds[1]
        )

    def expand_and_broadcast_to(self, expansion, new_shape):
        shape = self.get_expanded_shape(self.shape, expansion)
        cur_vals = self.block_vals
        flat_inds = self.block_inds[0]
        cur_inds = self._unravel_indices(flat_inds, shape) # we know the shape still works b.c. it's just adding 1s
        return self.broadcast_values(
            new_shape,
            shape,
            cur_vals,
            cur_inds
        )

    def expand_and_pad(self, expansion, padding):
        shape = self.get_expanded_shape(self.shape, expansion)
        if len(padding) != len(shape): raise ValueError("can't pad {} onto shape {}".format(padding, shape))
        new_shape = [s + a for a, s in zip(padding, shape)]

        cur_vals = self.block_vals
        flat_inds = self.block_inds[0]
        cur_inds = self._unravel_indices(flat_inds, shape)  # we know the shape still works b.c. it's just adding 1s
            # return type(self)(self.block_data, shape=new_shape)

        return type(self)(
            (
                cur_vals,
                cur_inds
            ),
            shape=new_shape
        )
        # return self.broadcast_values(
        #     new_shape,
        #     shape,
        #     cur_vals,
        #     cur_inds
        # )

    def _tocs(self):
        if self.fmt not in [sp.csr_matrix, sp.csc_matrix]:
            a = self.data
            if a.shape[0] > a.shape[1]:
                self._a = a.asformat('csc', copy=False)
                self._fmt = None
            else:
                self._a = a.asformat('csr', copy=False)
                self._fmt = None
    def ascs(self, inplace=False):
        if not inplace:
            self = self.copy()
        self._tocs()
        return self

    @staticmethod
    def _matrix_dot(a, b):
        try:
            return a.dot(b)
        except ValueError as error:
            if error.args and error.args[0] == 'dimension mismatch':
                raise ValueError("dimensions of tensors not aligned {} and {} incompatible".format(
                    a.shape, b.shape)) from error
            raise

    def dot(self, b, reverse=False):
        self._tocs()

        bshp = b.shape
        if isinstance(b, SparseArray) and len(bshp) > 2:
            bcols = int(np.prod(bshp[1:]))
            b = b.reshape((bshp[0], bcols))
        if self.shape != self.data.shape:
            arows = int(np.prod(self.shape[:-1]))
            a = self.reshape((arows, self.shape[-1])).data
        else:
            a = self.data

        if isinstance(b, ScipySparseArray):
            if b.shape != b.data.shape:
                bcols = int(np.prod(b.shape[1:]))
                b = b.reshape((b.shape[0], bcols)).data
            b = b.data
        elif isinstance(b, SparseArray):
            # Opt-in row backends handle the right product without global CSR conversion.
            if hasattr(b, '_right_dot'):
                return b._right_dot(self)
            b = b.ascsr()

        woof = self._matrix_dot(a, b)

        if isinstance(woof, sp.spmatrix):
            return type(self)(woof)
        else:
            return woof

    def outer(self, other):
        if isinstance(other, ScipySparseArray):
            oshp = other.shape
            other = other.data
        elif isinstance(other, SparseArray):
            oshp = other.shape
            other = other.ascsr()
        else:
            oshp = other.shape

        new_data = sp.kron(self.data, other)

        return type(self)(
            new_data,
            shape=self.shape + oshp
        )

    def plus(self, other, inplace=False):
        d = self.data
        if isinstance(other, (int, float, np.integer, np.floating)):
            if other == 0.:
                return self.copy()
            else:
                if inplace:
                    d += other
                    return self
                else:
                    d = other + d
                    new = type(self)(d, shape=self.shape, layout=self.fmt)
                    if self._block_vals is not None:
                        bvs = self._block_vals
                        bi = self._block_inds
                        new._block_vals = other + bvs
                        new._block_inds = bi
                        new._block_data_sorted = self._block_data_sorted
                    return new

        if isinstance(other, ScipySparseArray):
            other = other.data
        if isinstance(other, sp.spmatrix):
            other = other.reshape(d.shape)
        elif isinstance(other, np.ndarray):
            other = np.broadcast_to(other, self.shape).reshape(d.shape)

        if inplace:
            d += other
            self.data = d # hmm...
            self.block_data = None
            return self
        else:
            new = d.__add__(other)
            if isinstance(new, sp.spmatrix):
                return type(self)(new, shape=self.shape, layout=self.fmt)
            else:
                return np.array(new).reshape(self.shape)

    def floopy_flop(self):
        return type(self)(1/self.data, shape = self.shape, layout=self.fmt)

    def __truediv__(self, other):
        return self.multiply(1 / other)
    def __rtruediv__(self, other):
        if other == 1:
            return self.floopy_flop()
        return self.multiply(1 / other)
    def __rmul__(self, other):
        return self.multiply(other)
    def __mul__(self, other):
        return self.multiply(other)
    def true_multiply(self, other):
        d = self.data
        if isinstance(other, (int, float, np.integer, np.floating)):
            if other == 0.:
                new = self.fmt(d.shape)
                return type(self)(new, shape=self.shape, layout=self.fmt)
            elif other == 1.:
                return self.copy()
            else:
                d = other * self.data
                new = type(self)(d, shape=self.shape, layout=self.fmt)
                if self._block_vals is not None:
                    bvs = self._block_vals
                    bi = self._block_inds
                    new._block_vals = other * bvs
                    new._block_inds = bi
                    new._block_data_sorted = self._block_data_sorted
                return new

        if isinstance(other, ScipySparseArray):
            other = other.data
        if isinstance(other, sp.spmatrix):
            other = other.reshape(d.shape)
        elif isinstance(other, np.ndarray):
            other = np.broadcast_to(other, self.shape).reshape(d.shape)
        new = d.multiply(other)
        if isinstance(new, sp.spmatrix):
            return type(self)(new, shape=self.shape, layout=self.fmt)
        else:
            return np.array(new).reshape(self.shape)

    def copy(self):
        import copy

        base = copy.copy(self)
        if base.data is self.data:
            base.data = base.data.copy()
        # I'm not sure I mutate anything else?

        # if base._block_inds is not None:
        #
        # if self.data is n
        # base.
        return base

    @classmethod
    def _find_block_alignment(cls, inds, block):
        """
        finds the positions where the block & index align
        """

        # duh...
        filter, _, _ = contained(inds, block,
                                 assume_unique=(False, True),
                                 sortings=(None, np.arange(len(block)))
                                 )

        # I was hoping I could make use of that filter stuff to
        # build the mapping but it honestly seems like the two are completely
        # different?

        # we find the first position where the positions occur (we assume they _do_ occur)
        # using `searchsorted`
        mapping = np.searchsorted(block, np.arange(max(block)+1))#, sorter=sorter)


        return filter, mapping

    def _get_filtered_elements(self, blocks, data, inds):

        inds = list(inds)
        for i, b, s in zip(range(len(blocks)), blocks, self.shape):
            if b is not None:
                # need to sort the block bits it turns out...
                ixs = inds[i]
                b2, sorting = nput_unique(b)
                if len(b2) < len(b):
                    raise ValueError("sparse array slicing can't duplicate indices")
                b = b2
                # print("...", ixs)
                filter, mapping = self._find_block_alignment(ixs, b)#, sorting)
                # print("  .", b)
                # args = np.argsort(sorting)
                mapping = sorting[mapping]
                # print("  .", mapping)

                # the filter specifies which indices survive
                # and the mapping tells us where each index will go
                # in the final set of indices
                inds = [ix[filter] for ix in inds]
                data = data[filter]
                inds[i] = mapping[inds[i]]

        return data, inds

    def _get_matrix_block(self, indices):
        """Two-dimensional block slicing without full tensor coordinates.

        Preserve the tensor API's singleton-axis removal and duplicate-index
        checks. Unusual indexing falls back to its existing implementation.
        """
        if self.ndim != 2 or tuple(self.shape) != tuple(self.data.shape):return NotImplemented
        if not isinstance(indices,tuple) or not 1 <= len(indices) <= 2:return NotImplemented
        indices=indices+(slice(None),)*(2-len(indices))
        selected=[];counts=[]
        for index,size in zip(indices,self.shape):
            if isinstance(index,(int,np.integer)):
                if index < 0 or index >= size:return NotImplemented
                selected.append(int(index));counts.append(1)
            elif isinstance(index,slice):
                counts.append(len(range(*index.indices(size))));selected.append(index)
            else:
                array=np.asarray(index)
                if array.ndim!=1 or array.dtype.kind not in 'iub':return NotImplemented
                if array.dtype.kind=='b':
                    if len(array)!=size:return NotImplemented
                    array=np.flatnonzero(array)
                if len(array) and np.min(array)<0:return NotImplemented
                if len(np.unique(array))!=len(array):raise ValueError("sparse array slicing can't duplicate indices")
                selected.append(array);counts.append(len(array))
        shape=tuple(count for count in counts if count>1)
        if not shape:return NotImplemented
        if 0 in counts:return NotImplemented
        # SciPy block indexing copies the selected buffers. Transposing the
        # one-row result below shares that private copy, never the source.
        # Apply the axes separately: simultaneous fancy-row/strided-column
        # indexing is inconsistent across supported SciPy versions.
        data=self.data;copied=False
        for axis,index in enumerate(selected):
            if isinstance(index,slice) and index.indices(self.shape[axis])==(0,self.shape[axis],1):continue
            data=data[index,:] if axis==0 else data[:,index]
            copied=True
        if not copied:data=data.copy()
        if len(shape)==1 and counts[0]==1:data=data.transpose(copy=False)
        return type(self)(data,shape=shape,layout=type(data),initialize=False)


    def _get_element(self, idx, pull_elements=None):
        """
        Convert idx into a 1D index or slice or whatever and then convert it back to the appropriate 2D shape

        :param i:
        :type i:
        :return:
        :rtype:
        """

        # TODO: take a look at the numpy "fancy indexing" code to speed this up...
        if pull_elements is None:
            # we check first to see if we were asked for just a single vector of elements
            # the detection heuristic is basically: is everything just a slice of ints or nah
            if isinstance(idx, (int, np.integer)):
                idx = (idx,)
            pull_elements = len(idx) == len(self.shape) and all(isinstance(x, (int, np.integer)) for x in idx)
            if not pull_elements:
                pull_elements = all(not isinstance(x, (int, np.integer, slice)) for x in idx)
                if pull_elements:
                    e1 = len(idx[0])
                    pull_elements = all(len(x) == e1 for x in idx)

        if not pull_elements:
            block = self._get_matrix_block(idx)
            if block is not NotImplemented:return block

        if pull_elements:
            # try:
            flat = self._ravel_indices(idx, self.shape)
            # except:
            #     raise Exception(idx)

            unflat = self._unravel_indices(flat, self.data.shape)
            res = self.data[unflat]
            if not isinstance(flat, int):
                res = np.array(res)
            return res
        else:
            # need to compute the shape of the resultant block
            # we treat slice(None, None, None) as a special case because
            # it's so common
            blocks = [
                (
                    np.array([i]) if isinstance(i, (int, np.integer)) else (
                        np.arange(s)[i,].flatten()
                            if not (isinstance(i, slice) and i == slice(None, None, None)) else
                        None
                    )
                )
                for i, s in zip(idx, self.shape)
            ]
            # we filter out places where new_shape[i] == 1 at a later stage
            # for now we just build out the total shape it _would_ have with axes of len 1
            new_shape = [
                            len(x) if x is not None else s for x,s in zip(blocks, self.shape[:len(blocks)])
                         ] + list(self.shape[len(blocks):])

            # now we iterate over each block and use it as a successive filter on our non-zero positions
            data, inds = self.block_data
            data, inds = self._get_filtered_elements(blocks, data, inds)
            # print(blocks, inds, old_inds)

            # now that we've filtered our data, we filter out axes of size 1
            # print(inds, new_shape)
            inds = [ix for ix, j in zip(inds, new_shape) if j > 1]
            new_shape = tuple(j for j in new_shape if j > 1)
            # we also apply this to the indices that we're filtering on

            # if idx[0] == 0 and isinstance(idx[2], slice):
            #     raise Exception(blocks)

            # finally, we track our indices so that we don't need to recompute anything later
            if len(new_shape) > 2:
                total_shape = (np.prod(new_shape[:-2]) * new_shape[-2], new_shape[-1])
                flat = self._ravel_indices(inds, new_shape)
                unflat = self._unravel_indices(flat, total_shape)
            elif len(new_shape) == 1:
                flat = None
                unflat = inds+[np.zeros((len(inds[0]),))]
                total_shape = new_shape+(1,)
            else:
                flat = None
                unflat = inds
                total_shape = new_shape

            # raise Exception(blocks, new_shape, len(inds), len(unflat))
            # od = data
            if len(unflat) == 0:
                if len(total_shape) == 0:
                    total_shape = ((1,))
                return self.empty(total_shape, dtype=self.dtype)
            else:
                try:
                    data = self._build_data(data, unflat, total_shape)
                except Exception as e:
                    # print(data, data.shape, unflat, total_shape)
                    exc = e
                else:
                    exc = None
            # raise Exception(unflat, od, data, inds, total_shape)
            if exc is not None:
                raise IndexError("{}: couldn't take element {} of array {} (Got Error: '{}')".format(
                    type(self).__name__,
                    idx,
                    self,
                    exc
                ))

            new = type(self)(data, shape=new_shape, layout=self.fmt)
            if flat is None:
                new.block_inds = inds
            else:
                new.block_inds = flat, inds
            new._block_data_sorted = True
            return new

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
        # Just here so I can be smart
        try:
            self.data[unflat] = val
        except TypeError:
            if self.data.shape[0] > self.data.shape[1]:
                sub_sparse = sp.csc_matrix(self.data)
            else:
                sub_sparse = sp.csr_matrix(self.data)
            sub_sparse[unflat] = val
            self.data = self.fmt(sub_sparse)

        # TODO: figure out how to resolve the collisions
        #       more efficiently
        self._block_vals = None
        self._block_inds = None

    def _set_element(self, idx, val):
        """
        Convert idx into a 1D index or slice or whatever and then convert it back to the appropriate 2D shape.
        Then hope that the val can be set on the sp.spmatrix backend...

        :param i:
        :type i:
        :return:
        :rtype:
        """

        # we check first to see if we were asked for just a single vector of elements
        # the detection heuristic is basically: is everything just a slice of ints or nah
        if isinstance(idx, (int, np.integer)):
            idx = (idx,)
        set_elements = len(idx) == len(self.shape) and all(isinstance(x, (int, np.integer)) for x in idx)
        if not set_elements:
            set_elements = all(not isinstance(x, (int, np.integer, slice)) for x in idx)
            if set_elements:
                e1 = len(idx[0])
                set_elements = all(len(x) == e1 for x in idx)

        if set_elements:
            flat = self._ravel_indices(idx, self.shape)
            unflat = self._unravel_indices(flat, self.data.shape)
            # try:

            self._set_data(unflat, val)
            # except TypeError:
            #     # need to construct a new data object in its entirety :weep:
            #     # or convert to an assignable format?
            #
        else:
            # need to compute the proper block indices, unfortunately
            # so that they can be down-converted to their 2D equivalents
            blocks = [
                (
                    np.array([i]) if isinstance(i, (int, np.integer)) else (
                        np.arange(s)[i,].flatten()
                    )
                )
                for i, s in zip(idx, self.shape)
            ]

            block_inds = np.array([p for p in ip.product(*blocks)]).T

            flat = self._ravel_indices(block_inds, self.shape)
            unflat = self._unravel_indices(flat, self.data.shape)

            self._set_data(unflat, val)

    def _del_element(self, idx):
        """
        Convert idx into a 1D index or slice or whatever and then convert it back to the appropriate 2D shape.
        Then hope that the val can be deleted on the sp.spmatrix backend...

        :param i:
        :type i:
        :return:
        :rtype:
        """

        # we check first to see if we were asked for just a single vector of elements
        # the detection heuristic is basically: is everything just a slice of ints or nah
        if isinstance(idx, (int, np.integer)):
            idx = (idx,)
        set_elements = len(idx) == len(self.shape) and all(isinstance(x, (int, np.integer)) for x in idx)
        if not set_elements:
            set_elements = all(not isinstance(x, (int, np.integer, slice)) for x in idx)
            if set_elements:
                e1 = len(idx[0])
                set_elements = all(len(x) == e1 for x in idx)

        if set_elements:
            flat = self._ravel_indices(idx, self.shape)
            unflat = self._unravel_indices(flat, self.data.shape)
            del self.data[unflat]
            # TODO: figure out how to resolve the collisions
            #       more efficiently
            self._block_vals = None
            self._block_inds = None
        else:
            # need to compute the proper block indices, unfortunately
            # so that they can be down-converted to their 2D equivalents
            blocks = [
                (
                    np.array([i]) if isinstance(i, (int, np.integer)) else (
                        np.arange(s)[i,].flatten()
                    )
                )
                for i, s in zip(idx, self.shape)
            ]

            block_inds = np.array([p for p in ip.product(*blocks)]).T

            flat = self._ravel_indices(block_inds, self.shape)
            unflat = self._unravel_indices(flat, self.data.shape)
            del self.data[unflat]
            # TODO: figure out how to resolve the collisions
            #       more efficiently
            self._block_vals = None
            self._block_inds = None

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

        # sp.save_npz already sticks the extension on so it doesn't hurt to explicitly add it...
        if isinstance(file, str) and os.path.splitext(file)[1] != ".npz":
            file += ".npz"
        sp.save_npz(file, self.data, compressed=compressed)
        bleh = np.load(file)
        flat, unflat = self.block_inds
        bv = self.block_vals
        if compressed:
            np.savez_compressed(
                file,
                _block_shape=np.array(self.shape),
                _block_inds_flat=np.array(flat),
                _block_inds_unflat=np.array(unflat),
                _block_vals=bv,
                compressed=compressed,
                **bleh
            )
        else:
            np.savez(
                file,
                _block_shape=np.array(self.shape),
                _block_inds_flat=np.array(flat),
                _block_inds_unflat=np.array(unflat),
                _block_vals=bv,
                compressed=compressed,
                **bleh
                )
        return file
    @classmethod
    def loadz(cls, file):
        """
        Loads a SparseArray from an npz file
        :param file:
        :type file:
        :return:
        :rtype: SparseArray
        """
        data = sp.load_npz(file) #type: sp.spmatrix
        other = np.load(file)
        new = cls(data, shape=other['_block_shape'], layout=type(data), initialize=False)
        new._block_inds = (other['_block_inds_flat'], other['_block_inds_unflat'])
        new._block_inds = other['_block_vals']
        return new

    def __getitem__(self, item):
        return self._get_element(item)
    def __setitem__(self, item, val):
        return self._set_element(item, val)
    def __delitem__(self, item):
        return self._del_element(item)

    def __repr__(self):
        return "{}(<{}> nonzero={})".format(type(self).__name__,
                                           ", ".join([str(x) for x in self.shape]),
                                          self.non_zero_count
                                           )

class PackedIndexArray:
    """Sorted positions represented by bits and small rank/select checkpoints."""
    _popcount = np.array([int(i).bit_count() for i in range(256)], dtype=np.uint8)
    ndim = 1
    is_sorted = True
    def __init__(self, bits, size, block_size=65536):
        self.bits = np.asarray(bits, dtype=np.uint8)
        self.size = int(size)
        self.block_size = max(8, (int(block_size)+7)//8*8)
        self.dtype = SparseArray._index_dtype(self.size)
        if len(self.bits) != (self.size+7)//8:
            raise ValueError("Incorrect packed support size")
        if self.size % 8 and len(self.bits):
            if self.bits[-1] & ((1 << (8-self.size%8))-1):
                raise ValueError("Nonzero padding in packed support")
        step = self.block_size//8
        self.prefix = np.zeros((len(self.bits)+step-1)//step+1, dtype=np.int64)
        for i, start in enumerate(range(0, len(self.bits), step)):
            self.prefix[i+1] = self.prefix[i]+int(self._popcount[self.bits[start:start+step]].sum())
        self.bits.flags.writeable = False
        self.prefix.flags.writeable = False

    @property
    def nbytes(self): return self.bits.nbytes+self.prefix.nbytes
    @property
    def shape(self): return (len(self),)
    def __len__(self): return int(self.prefix[-1])
    def min(self): return self[0]
    def max(self): return self[-1]
    def view(self): return self

    def __getitem__(self, selector):
        scalar = np.isscalar(selector)
        if isinstance(selector, slice):
            start, stop, step = selector.indices(len(self))
            requested = np.arange(start, stop, step, dtype=np.int64)
        else:
            requested = np.asarray(selector)
            if requested.dtype.kind == "b":
                if requested.shape != (len(self),): raise IndexError("Boolean support selector size")
                requested = np.flatnonzero(requested)
            if requested.size == 0: return np.empty(requested.shape, dtype=self.dtype)
            if requested.dtype.kind not in "iu": raise IndexError("Integer support selector required")
            requested = requested.astype(np.int64, copy=False)
            requested = np.where(requested < 0, requested+len(self), requested)
        shape = requested.shape
        requested = np.atleast_1d(requested).reshape(-1)
        if np.any((requested < 0) | (requested >= len(self))): raise IndexError(selector)
        blocks = np.searchsorted(self.prefix, requested, side="right")-1
        result = np.empty(len(requested), dtype=self.dtype)
        for block in np.unique(blocks):
            selected = np.flatnonzero(blocks == block)
            start = int(block)*self.block_size
            bits = np.unpackbits(self.bits[start//8:(start+self.block_size)//8])
            positions = np.flatnonzero(bits)
            result[selected] = start+positions[requested[selected]-self.prefix[block]]
        return result[0] if scalar else result.reshape(shape)

    def searchsorted(self, values, side="left"):
        values = np.asarray(values)
        scalar = values.ndim == 0
        work = values.astype(np.int64, copy=False).reshape(-1)
        if side == "right": work = work+1
        elif side != "left": raise ValueError(side)
        work = np.clip(work, 0, self.size)
        result = np.empty(len(work), dtype=np.int64)
        blocks = work//self.block_size
        for block in np.unique(blocks):
            selected = np.flatnonzero(blocks == block)
            start = int(block)*self.block_size
            stop = min(start+self.block_size, self.size)
            bits = np.unpackbits(self.bits[start//8:(stop+7)//8])[:stop-start]
            prefix = np.empty(len(bits)+1, dtype=np.int64)
            prefix[0] = 0
            np.cumsum(bits, out=prefix[1:])
            result[selected] = self.prefix[min(int(block), len(self.prefix)-1)]+prefix[work[selected]-start]
        return result[0] if scalar else result.reshape(values.shape)

    def contains(self, positions):
        positions = np.asarray(positions)
        safe = np.clip(positions, 0, max(0, self.size-1)).astype(np.int64)
        if self.size == 0: return np.zeros(positions.shape, dtype=bool)
        return ((positions >= 0) & (positions < self.size)
                & ((self.bits[safe//8] >> (7-safe%8)) & 1).astype(bool))

    def __array__(self, dtype=None, copy=None):
        result = self[:]
        return result.astype(dtype, copy=False) if dtype is not None else result


class CompactSparseRow:
    """One immutable dense or sparse row, including its exact retained support."""
    def __init__(self, values, columns, size):
        self.values, self.columns, self.size = values, columns, int(size)
    @property
    def dense(self): return isinstance(self.columns, PackedIndexArray)
    @property
    def nnz(self): return len(self.columns)
    @property
    def nbytes(self): return self.values.nbytes+self.columns.nbytes
    @classmethod
    def from_dense(cls, vector, cutoff=0, block_size=65536):
        vector = np.asarray(vector)
        if vector.ndim != 1: raise ValueError("Row must be one dimensional")
        size = len(vector)
        dtype = SparseArray._index_dtype(size)
        def mask(block):
            return block != 0 if cutoff is None or cutoff < 0 else np.abs(block) > cutoff
        counts = [int(np.count_nonzero(mask(vector[start:start+block_size])))
                  for start in range(0, size, block_size)]
        count = sum(counts)
        support_bytes = (size+7)//8+8*((size+block_size-1)//block_size+1)
        use_dense = size*vector.dtype.itemsize+support_bytes < count*(vector.dtype.itemsize+dtype.itemsize)
        if use_dense:
            values = vector.copy()
            bits = np.zeros((size+7)//8, dtype=np.uint8)
            # Byte aligned chunks avoid a whole-row boolean/coordinate temporary.
            step = max(8, (block_size+7)//8*8)
            for start in range(0, size, step):
                keep = mask(values[start:start+step])
                values[start:start+step][~keep] = 0
                packed = np.packbits(keep)
                bits[start//8:start//8+len(packed)] = packed
            columns = PackedIndexArray(bits, size, block_size)
        else:
            values = np.empty(count, dtype=vector.dtype)
            columns = np.empty(count, dtype=dtype)
            offset = 0
            for start, count in zip(range(0, size, block_size), counts):
                block = vector[start:start+block_size]
                keep = np.flatnonzero(mask(block))
                values[offset:offset+count] = block[keep]
                columns[offset:offset+count] = keep+start
                offset += count
        return cls(values, columns, size)

    @classmethod
    def from_native(cls, matrix, block_size=65536):
        if sp.issparse(matrix):
            row = matrix.tocsr()
            row.sum_duplicates(); row.sort_indices(); row.eliminate_zeros()
            # Only build a dense row when its actual byte cost is smaller.
            size = row.shape[1]
            dtype = SparseArray._index_dtype(size)
            support = (size+7)//8+8*((size+block_size-1)//block_size+1)
            if size*row.dtype.itemsize+support < row.nnz*(row.dtype.itemsize+np.dtype(dtype).itemsize):
                return cls.from_dense(row.toarray().reshape(-1), None, block_size)
            return cls(row.data.copy(), row.indices.astype(dtype, copy=True), size)
        return cls.from_dense(np.asarray(matrix).reshape(-1), None, block_size)

    def native(self):
        if self.dense: return self.values.reshape(1, -1)
        return sp.csr_matrix((self.values, self.columns, np.array([0, self.nnz], dtype=self.columns.dtype)),
                             shape=(1, self.size), copy=False)

    def entries(self, block_size=65536):
        if self.dense:
            for start in range(0, self.size, block_size):
                block = self.values[start:start+block_size]
                keep = np.flatnonzero(block != 0)
                if len(keep): yield block[keep], (keep+start).astype(self.columns.dtype)
        else:
            for start in range(0, self.nnz, block_size):
                yield self.values[start:start+block_size], self.columns[start:start+block_size]

    def select(self, columns, block_size=65536):
        columns = np.asarray(columns)
        if self.dense: return type(self).from_dense(self.values[columns], None, block_size)
        pos = np.searchsorted(self.columns, columns)
        valid = pos < self.nnz
        if self.nnz: valid &= self.columns[np.minimum(pos, self.nnz-1)] == columns
        values = np.zeros(len(columns), dtype=self.values.dtype)
        values[valid] = self.values[pos[valid]]
        return type(self).from_dense(values, None, block_size)


class RowSpillStore:
    """Soft resident-payload target and capped, append-only mapped segments.

    This does not cap process RSS. When the disk allowance is exhausted, rows
    remain resident and the process/scheduler resource guard remains decisive.
    ``allocation_check(bytes)`` can additionally enforce a shared scratch cap.
    The store is opt in; no files are made until a completed row is spilled.
    """
    active_stores = weakref.WeakSet()

    @staticmethod
    def _remove_segment(path):
        path = Path(path)
        try: path.unlink()
        except FileNotFoundError: pass
        try: path.parent.rmdir()
        except (FileNotFoundError, OSError): pass


    def __init__(self, directory, resident_bytes, max_bytes, *,
                 segment_bytes=512*1024**2, copy_block_bytes=64*1024**2,
                 allocation_check=None):
        for name, value in [('resident_bytes', resident_bytes), ('max_bytes', max_bytes),
                            ('segment_bytes', segment_bytes), ('copy_block_bytes', copy_block_bytes)]:
            if not isinstance(value, (int, np.integer)) or value < (0 if name == 'resident_bytes' else 1):
                raise ValueError(name + ' must be an integer byte count')
        self.directory = Path(directory)
        self.resident_limit, self.max_bytes = int(resident_bytes), int(max_bytes)
        self.segment_bytes, self.copy_block_bytes = int(segment_bytes), int(copy_block_bytes)
        self.allocation_check = allocation_check
        self._root = None
        self._segments, self._positions, self._pins = [], [], {}
        self._known = weakref.WeakSet()
        self.resident_bytes = self.file_backed_bytes = self.reserved_bytes = 0
        self.peak_resident_bytes = self.peak_file_backed_bytes = self.peak_reserved_bytes = 0
        self.spilled_rows = self.budget_refusals = self.drop_calls = self.drop_failures = 0
        self.write_seconds = self.drop_seconds = 0.
        self.active_stores.add(self)

    @staticmethod
    def _align(value, alignment=64):
        return (int(value)+alignment-1)//alignment*alignment

    def _reserve(self, size):
        size = self._align(size)
        if self._segments:
            segment = self._segments[-1]
            offset = self._align(self._positions[-1])
            if offset+size <= segment.nbytes:
                self._positions[-1] = offset+size
                return segment, offset
        available = self.max_bytes-self.reserved_bytes
        capacity = min(max(self.segment_bytes, size), available)
        if capacity < size:
            self.budget_refusals += 1
            return None
        if self.allocation_check is not None and not self.allocation_check(capacity):
            capacity = size
            if not self.allocation_check(capacity):
                self.budget_refusals += 1
                return None
        if self._root is None:
            self.directory.mkdir(parents=True, exist_ok=True)
            self._root = Path(tempfile.mkdtemp(prefix='compact_rows_', dir=self.directory))
        path = self._root / ('segment_%06d.bin' % len(self._segments))
        try:
            with path.open('xb') as stream:
                try: os.posix_fallocate(stream.fileno(), 0, capacity)
                except AttributeError: stream.truncate(capacity)
                except OSError as error:
                    if error.errno not in {errno.ENOSYS, errno.EOPNOTSUPP}: raise
                    stream.truncate(capacity)
            segment = np.memmap(path, dtype=np.uint8, mode='r+', shape=(capacity,))
        except OSError as error:
            try: path.unlink()
            except FileNotFoundError: pass
            if error.errno not in {errno.ENOSPC, errno.EDQUOT}: raise
            self.budget_refusals += 1
            return None
        weakref.finalize(segment, self._remove_segment, str(path))
        self._segments.append(segment)
        self._positions.append(size)
        self.reserved_bytes += capacity
        self.peak_reserved_bytes = max(self.peak_reserved_bytes, self.reserved_bytes)
        return segment, 0

    def _copy_arrays(self, arrays):
        offsets, size = [], 0
        for array in arrays:
            size = self._align(size)
            offsets.append(size)
            size += array.nbytes
        allocation = self._reserve(size)
        if allocation is None: return None
        segment, offset = allocation
        result = []
        for array, start in zip(arrays, offsets):
            # Slicing the memmap preserves its owning base through ndarray views.
            view = segment[offset+start:offset+start+array.nbytes].view(array.dtype).reshape(array.shape)
            flat, source = view.reshape(-1), np.asarray(array).reshape(-1)
            step = max(1, self.copy_block_bytes//array.dtype.itemsize)
            for at in range(0, len(source), step): flat[at:at+step] = source[at:at+step]
            view.flags.writeable = False
            result.append(np.asarray(view))
        segment.flush()
        return result, segment

    def retain(self, row):
        if row in self._known or getattr(row, '_storage_owner', None) is not None:
            return row
        tick = time.perf_counter()
        file_bytes = 0
        segment = None
        if row.nbytes and self.resident_bytes+row.nbytes > self.resident_limit:
            arrays = [row.values, row.columns.bits if row.dense else row.columns]
            copied = self._copy_arrays(arrays)
            if copied is not None:
                buffers, segment = copied
                columns = (PackedIndexArray(buffers[1], row.size, row.columns.block_size)
                           if row.dense else buffers[1])
                row = CompactSparseRow(buffers[0], columns, row.size)
                file_bytes = sum(a.nbytes for a in buffers)
                self.spilled_rows += 1
        resident = row.nbytes-file_bytes
        row._storage_owner = self
        row._spill_segment = segment
        row._file_backed_bytes = file_bytes
        self._known.add(row)
        self.resident_bytes += resident
        self.file_backed_bytes += file_bytes
        self.peak_resident_bytes = max(self.peak_resident_bytes, self.resident_bytes)
        self.peak_file_backed_bytes = max(self.peak_file_backed_bytes, self.file_backed_bytes)
        weakref.finalize(row, self._release_row, resident, file_bytes)
        self.write_seconds += time.perf_counter()-tick
        if segment is not None: self._drop(segment)
        return row

    def _release_row(self, resident, file_bytes):
        self.resident_bytes -= resident
        self.file_backed_bytes -= file_bytes

    def _drop(self, segment):
        if self._pins.get(id(segment), 0): return
        tick = time.perf_counter()
        try:
            from .ExternalMemory import release_mapped_pages
            if not release_mapped_pages(segment, writeback=False):
                raise OSError('Mapped-page advice is unavailable')
            self.drop_calls += 1
        except (AttributeError, OSError, ValueError):
            self.drop_failures += 1
        self.drop_seconds += time.perf_counter()-tick

    def snapshot(self):
        return dict(resident_payload_bytes=self.resident_bytes,
                    file_backed_payload_bytes=self.file_backed_bytes,
                    reserved_file_bytes=self.reserved_bytes,
                    peak_resident_payload_bytes=self.peak_resident_bytes,
                    peak_file_backed_payload_bytes=self.peak_file_backed_bytes,
                    peak_reserved_file_bytes=self.peak_reserved_bytes,
                    resident_target_bytes=self.resident_limit, disk_limit_bytes=self.max_bytes,
                    segment_bytes=self.segment_bytes, segment_count=len(self._segments),
                    spilled_rows=self.spilled_rows, disk_budget_refusals=self.budget_refusals,
                    write_seconds=self.write_seconds, drop_seconds=self.drop_seconds,
                    drop_calls=self.drop_calls, drop_failures=self.drop_failures)

    @staticmethod
    @contextlib.contextmanager
    def pin_rows(rows):
        pairs = {}
        for row in rows:
            owner, segment = getattr(row, '_storage_owner', None), getattr(row, '_spill_segment', None)
            if owner is not None and segment is not None: pairs[id(segment)] = owner, segment
        for key, (owner, segment) in pairs.items(): owner._pins[key] = owner._pins.get(key, 0)+1
        try:
            yield
        finally:
            for key, (owner, segment) in pairs.items():
                owner._pins[key] -= 1
                if not owner._pins[key]:
                    del owner._pins[key]
                    owner._drop(segment)


class RowSparseArray(SparseArray):
    """Two-dimensional row-block backend. Views borrow immutable row storage."""
    def __init__(self, rows, ncols, *, block_bytes=64*1024**2, block_size=65536, transposed=False, storage=None):
        if not isinstance(block_bytes, (int, np.integer)) or block_bytes < 1:
            raise ValueError("block_bytes must be a positive integer")
        self.storage = storage
        self.rows = tuple(rows) if storage is None else tuple(storage.retain(row) for row in rows)
        self.ncols = int(ncols)
        self.block_bytes, self.block_size = int(block_bytes), int(block_size)
        self.transposed = transposed
    def _new(self, rows, ncols, **opts):
        return type(self)(rows, ncols, storage=self.storage, **opts)

    def _retain(self, row):
        return row if self.storage is None else self.storage.retain(row)

    @property
    def shape(self):
        shape = (len(self.rows), self.ncols)
        return shape[::-1] if self.transposed else shape
    @property
    def dtype(self): return np.result_type(*[r.values.dtype for r in self.rows]) if self.rows else np.dtype(float)
    @property
    def non_zero_count(self): return sum(r.nnz for r in self.rows)
    @property
    def nbytes(self): return sum(r.nbytes for r in self.rows)
    def __len__(self): return self.shape[0]
    def __repr__(self):
        return "{}(shape={}, nonzero={}, retained_bytes={})".format(type(self).__name__, self.shape, self.non_zero_count, self.nbytes)
    def copy(self): return self._new(self.rows, self.ncols, block_bytes=self.block_bytes, block_size=self.block_size, transposed=self.transposed)
    def transpose(self, axes=None):
        if axes is None or tuple(axes) == (1, 0):
            result = self.copy(); result.transposed = not result.transposed; return result
        if tuple(axes) == (0, 1): return self.copy()
        raise ValueError(axes)

    @classmethod
    def from_native(cls, matrix, **opts):
        if isinstance(matrix, cls): return matrix
        if isinstance(matrix, SparseArray): matrix = matrix.ascsr()
        if not hasattr(matrix, "shape") or len(matrix.shape) != 2: raise ValueError("Matrix required")
        step = opts.get("block_size", 65536)
        return cls((CompactSparseRow.from_native(matrix[i:i+1], step)
                    for i in range(matrix.shape[0])), matrix.shape[1], **opts)

    def __getitem__(self, item):
        if not isinstance(item, tuple): item = (item, slice(None))
        if len(item) != 2: raise IndexError("Two-dimensional row matrix")
        if self.transposed: return self.T[item[::-1]].T
        rsel, csel = item
        if isinstance(rsel, tuple): rsel = list(rsel)
        rows = np.arange(len(self.rows))[rsel]
        scalar_row = np.ndim(rows) == 0
        rows = np.atleast_1d(rows)
        selected = [self.rows[int(i)] for i in rows]
        if isinstance(csel, slice) and csel == slice(None):
            return self._new(selected, self.ncols, block_bytes=self.block_bytes, block_size=self.block_size)
        if isinstance(csel, slice):
            columns = np.arange(*csel.indices(self.ncols), dtype=np.int64)
        else:
            columns = np.atleast_1d(np.asarray(csel))
            if columns.dtype.kind == "b":
                if columns.shape != (self.ncols,): raise IndexError("Boolean column selector size")
                columns = np.flatnonzero(columns)
            columns = columns.astype(np.int64, copy=False)
            columns = np.where(columns < 0, columns+self.ncols, columns)
            if np.any((columns < 0) | (columns >= self.ncols)): raise IndexError(csel)
        selected = [row.select(columns, self.block_size) for row in selected]
        result = self._new(selected, len(columns), block_bytes=self.block_bytes, block_size=self.block_size)
        if scalar_row and np.isscalar(csel): return result.asarray()[0, 0]
        return result

    def iter_row_blocks(self, max_rows=None):
        if self.transposed: raise ValueError("Use the base rows of a transpose view")
        start, size, rows = 0, 0, []
        for i, row in enumerate(self.rows):
            if rows and (size+row.nbytes > self.block_bytes or (max_rows is not None and len(rows) >= max_rows)):
                with RowSpillStore.pin_rows(rows):
                    yield start, self._stack(rows)
                start, size, rows = i, 0, []
            rows.append(row); size += row.nbytes
        if rows:
            with RowSpillStore.pin_rows(rows):
                yield start, self._stack(rows)
    @staticmethod
    def _stack(rows):
        if len(rows) == 1: return rows[0].native()
        if all(r.dense for r in rows): return np.vstack([r.values for r in rows])
        return sp.vstack([sp.csr_matrix(r.native()) for r in rows], format="csr")
    def iter_nonzero_blocks(self, block_size=65536, value_filter=None):
        for i, row in enumerate(self.rows):
            with RowSpillStore.pin_rows([row]):
                for values, columns in row.entries(block_size):
                    if value_filter is not None:
                        keep = value_filter(values); values, columns = values[keep], columns[keep]
                    if len(values):
                        rows = np.full(len(values), i, dtype=np.int64)
                        yield values, (columns, rows) if self.transposed else (rows, columns)

    def _export_check(self, size):
        if size > self.block_bytes:
            raise MemoryError("Whole row-matrix export needs {} bytes; block_bytes={}. Use row/block iteration or explicitly increase the export/workspace target.".format(size, self.block_bytes))
    def ascsr(self):
        self._export_check(self.non_zero_count*(self.dtype.itemsize+8)+(len(self.rows)+1)*8)
        base = sp.vstack([sp.csr_matrix(r.native()) for r in self.rows], format="csr") if self.rows else sp.csr_matrix((0,self.ncols))
        return base.T.tocsr() if self.transposed else base
    def ascoo(self): return self.ascsr().tocoo()
    def asarray(self):
        self._export_check(int(np.prod(self.shape, dtype=object))*self.dtype.itemsize)
        base = np.zeros((len(self.rows), self.ncols), dtype=self.dtype)
        for i, row in enumerate(self.rows):
            if row.dense: base[i] = row.values
            else: base[i, row.columns] = row.values
        return base.T if self.transposed else base
    toarray = asarray
    todense = asarray
    @property
    def block_data(self):
        coo = self.ascoo()
        return coo.data, (coo.row, coo.col)

    def dot(self, other):
        if isinstance(other, EvaluatedSparseMatrix): return other._right_dot(self)
        if self.shape[1] != other.shape[0]: raise ValueError("Matrix dimensions do not align")
        if self.transposed:
            right = other.T if isinstance(other, SparseArray) else other.T
            result = type(self).from_native(right, block_bytes=self.block_bytes, block_size=self.block_size, storage=self.storage).dot(self.T)
            return result.T
        if isinstance(other, RowSparseArray) and other.transposed:
            output = []
            max_rows = max(1, self.block_bytes//max(1, other.shape[1]*self.dtype.itemsize))
            for start, left in self.iter_row_blocks(max_rows):
                # The output, unlike the correction basis, is the requested state-pair block.
                result = np.zeros((left.shape[0], other.shape[1]), dtype=np.result_type(self.dtype, other.dtype))
                for stop, right in other.T.iter_row_blocks():
                    part = ScipySparseArray._matrix_dot(sp.csr_matrix(left), sp.csr_matrix(right.T))
                    if sp.issparse(part): part = part.toarray()
                    result[:,stop:stop+right.shape[0]] = part
                output.extend(self._retain(CompactSparseRow.from_dense(row, None, self.block_size)) for row in result)
            return self._new(output, other.shape[1], block_bytes=self.block_bytes, block_size=self.block_size)
        output = []
        max_rows = max(1, self.block_bytes//max(1, other.shape[1]*self.dtype.itemsize))
        for start, left in self.iter_row_blocks(max_rows):
            if isinstance(other, RowSparseArray):
                result = None
                for inner, right in other.iter_row_blocks():
                    part = ScipySparseArray._matrix_dot(sp.csr_matrix(left[:,inner:inner+right.shape[0]]), sp.csr_matrix(right))
                    result = part if result is None else result+part
                if result is None: result = sp.csr_matrix((left.shape[0], other.shape[1]))
            else:
                right = other.ascsr() if isinstance(other, SparseArray) else other
                result = ScipySparseArray._matrix_dot(sp.csr_matrix(left), sp.csr_matrix(right))
            output.extend(self._retain(CompactSparseRow.from_native(result[i:i+1], self.block_size)) for i in range(left.shape[0]))
        return self._new(output, other.shape[1], block_bytes=self.block_bytes, block_size=self.block_size)
    def _right_dot(self, left):
        return type(self).from_native(left, block_bytes=self.block_bytes, block_size=self.block_size, storage=self.storage).dot(self)

    def true_multiply(self, other):
        if np.isscalar(other):
            if self.transposed: return self.T.true_multiply(other).T
            rows = (self._retain(CompactSparseRow.from_native(row.native()*other, self.block_size)) for row in self.rows)
            return self._new(rows, self.ncols, block_bytes=self.block_bytes, block_size=self.block_size)
        raise NotImplementedError("Elementwise row-matrix multiplication requires a scalar")
    def plus(self, other, inplace=False):
        if np.isscalar(other) and other == 0: return self.copy()
        if self.transposed: return self.T.plus(other.T, inplace).T
        other = type(self).from_native(other, block_bytes=self.block_bytes, block_size=self.block_size)
        if other.shape != self.shape: raise ValueError("Row matrix addition shape mismatch")
        rows = (self._retain(CompactSparseRow.from_native(a.native()+b.native(), self.block_size))
                for a,b in zip(self.rows, other.rows))
        return self._new(rows, self.ncols, block_bytes=self.block_bytes, block_size=self.block_size)
    def reshape(self, newshape):
        if tuple(newshape) == self.shape: return self.copy()
        return SparseArray.from_data(self.asarray().reshape(newshape))
    def concatenate(self, *others, axis=0):
        if axis != 0 or self.transposed: raise NotImplementedError("Only row concatenation is supported")
        rows = list(self.rows)
        for other in others:
            other = type(self).from_native(other, block_bytes=self.block_bytes, block_size=self.block_size)
            if other.ncols != self.ncols or other.transposed: raise ValueError("Incompatible row blocks")
            rows.extend(other.rows)
        return self._new(rows, self.ncols, block_bytes=self.block_bytes, block_size=self.block_size)
    def to_state(self, serializer=None):
        return dict(rows=[dict(values=r.values,columns=r.columns.bits if r.dense else r.columns,dense=r.dense) for r in self.rows],
                    ncols=self.ncols,block_bytes=self.block_bytes,block_size=self.block_size,transposed=self.transposed)
    @classmethod
    def from_state(cls, state, serializer=None):
        state = dict(state); rows = state.pop("rows"); ncols = state["ncols"]
        return cls([CompactSparseRow(r["values"], PackedIndexArray(r["columns"],ncols,state["block_size"]) if r["dense"] else r["columns"], ncols) for r in rows], **state)
    @classmethod
    def initialize_empty(cls, shp, shape=None, **kw):
        shape = shp if shape is None else shape
        return cls([CompactSparseRow.from_dense(np.zeros(shape[1])) for _ in range(shape[0])], shape[1], **kw)
    @classmethod
    def from_diagonal_data(cls, diags, **kw):
        return cls.from_native(sp.diags(diags, format="csr"), **kw)
    def resize(self, newsize): raise NotImplementedError("Row matrix resizing is explicit")
    def pad_right(self, newshape): raise NotImplementedError("Row matrix padding is explicit")
    def broadcast_to(self, shape): raise NotImplementedError("Row matrix broadcasting is explicit")
    def expand_and_broadcast_to(self, expansion, new_shape): raise NotImplementedError("Two-dimensional backend")
    def expand_and_pad(self, expansion, padding): raise NotImplementedError("Two-dimensional backend")
    def outer(self, other): raise NotImplementedError("Outer products require an explicit output plan")


# import tensorflow
class TensorFlowSparseArray(SparseArray):
    """
    Provides a SparseArray implementation that uses TensorFlow as the backend
    """
    def __init__(self, data, dtype=None):
        import tensorflow
        self.tensor = self._init_tensor(data, dtype=dtype) #type: tensorflow.sparse.SparseTensor

    def _init_tensor(self, data, dtype=None):
        """
        :param data:
        :type data:
        :return:
        :rtype: tensorflow.sparse.SparseTensor
        """
        import tensorflow
        if isinstance(data, TensorFlowSparseArray):
            import copy
            new = copy.copy(data.tensor)
            if dtype is not None and new.dtype != dtype:
                raise NotImplementedError("not sure how to convert dtypes...")
            return new
        elif isinstance(data, tensorflow.sparse.SparseTensor):
            if dtype is not None and data.dtype != dtype:
                raise NotImplementedError("not sure how to convert dtypes...")
            return data
        elif isinstance(data, ScipySparseArray):
            vals, inds = data.block_data
            if dtype is not None and vals.dtype != dtype:
                vals = vals.astype(dtype)
            return tensorflow.sparse.SparseTensor(inds, vals, data.shape)
        elif isinstance(data, sp.spmatrix):
            row_inds, col_inds, vals = sp.find(data)
            if dtype is not None and vals.dtype != dtype:
                vals = vals.astype(dtype)
            return tensorflow.sparse.SparseTensor((row_inds, col_inds), vals, data.shape)
        elif isinstance(data, np.ndarray) and data.dtype != np.dtype(object):
            return self._init_tensor(ScipySparseArray(data))
        elif isinstance(data, (list, tuple)) and len(data) == 2:
            if all(isinstance(x, (int, np.integer)) for x in data):
                # empty tensor
                return tensorflow.sparse.SparseTensor([], [], data)
            elif len(data[1]) == 2 and all(isinstance(x, (int, np.integer)) for x in data[1]):
                # second arg is shape
                vals = np.array(data[0][0])
                inds = data[0][1]
                if dtype is not None and vals.dtype != dtype:
                    vals = vals.astype(dtype)
                return tensorflow.sparse.SparseTensor(inds, vals, data[1])
            else:
                raise TypeError("don't know how to turn {} into a tensorflow SparseTensor".format(
                    data
                ))
        else:
            raise TypeError("don't know how to turn {} into a tensorflow SparseTensor".format(
                data
            ))

    @property
    def shape(self):
        """
        Provides the shape of the sparse array
        :return:
        :rtype: tuple[int]
        """
        return tuple(self.tensor.shape)

    def to_state(self, serializer=None):
        """
        Provides just the state that is needed to
        serialize the object
        :param serializer:
        :type serializer:
        :return:
        :rtype:
        """
        raise NotImplementedError("coming")

    @classmethod
    def from_state(cls, state, serializer=None):
        """
        Loads from the stored state
        :param serializer:
        :type serializer:
        :return:
        :rtype:
        """
        raise NotImplementedError("coming")

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
        return cls(shape, dtype=dtype)

    @property
    def block_data(self):
        """
        Returns the row and column indices and vector of
        values that the sparse array is storing
        :return:
        :rtype: Tuple[np.ndarray, Iterable[np.ndarray]]
        """
        return (self.tensor.values, self.tensor.indices)

    def transpose(self, axes):
        """
        Returns a transposed version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        import tensorflow as tf
        new = tf.sparse.transpose(self.tensor, perm=axes)
        return type(self)(new)

    def ascoo(self):
        """
        Converts the tensor into a scipy COO matrix...
        :return:
        :rtype: sp.coo_matrix
        """
        return ScipySparseArray(self).ascoo()
    def ascsr(self):
        """
        Converts the tensor into a scipy COO matrix...
        :return:
        :rtype: sp.coo_matrix
        """
        return ScipySparseArray(self).ascsr()
    def reshape(self, newshape):
        """
        Returns a reshaped version of the tensor
        :param axes:
        :type axes:
        :return:
        :rtype:
        """
        import tensorflow as tf
        new = tf.sparse.reshape(self.tensor, newshape)
        return type(self)(new)

    def __truediv__(self, other):
        return self.true_multiply(1 / other)

    def __rtruediv__(self, other):
        return self.true_multiply(1 / other)

    def __rmul__(self, other):
        return self.true_multiply(other)

    def __mul__(self, other):
        return self.true_multiply(other)

    def true_multiply(self, other):
        """
        Multiplies self and other
        :param other:
        :type other:
        :return:
        :rtype:
        """
        import tensorflow as tf
        if isinstance(other, TensorFlowSparseArray):
            new = self.tensor * other.tensor
            return type(self)(new)
        elif isinstance(other, (tf.Tensor, tf.SparseTensor)):
            new = self.tensor * other
            return type(self)(new)
        elif isinstance(other, (int, np.integer, float, np.floating)):
            if other == 0:
                return type(self).empty(self.shape)
            else:
                vals, inds = self.block_data
                vals = vals * other
                return type(self)(((vals, inds), self.shape))

    @staticmethod
    def _tf_sparse_dot(a, b):
        from tensorflow.python.ops.linalg.sparse import sparse_csr_matrix_ops
        ashp = tuple(a.shape)
        if len(ashp) > 2:
            arows = int(np.prod(ashp[:-1]))
            acols = ashp[-1]
            a = a.reshape((arows, acols))
        bshp = tuple(b.shape)
        if len(bshp) > 2:
            brows = bshp[0]
            bcols = int(np.prod(bshp[1:]))
            b = b.reshape((brows, bcols))
        # woof..
        csr_1 = sparse_csr_matrix_ops.sparse_tensor_to_csr_sparse_matrix(
            a.indices,
            a.values,
            a.shape
        )
        csr_2 = sparse_csr_matrix_ops.sparse_tensor_to_csr_sparse_matrix(
            b.indices,
            b.values,
            b.shape
        )
        new = sparse_csr_matrix_ops.sparse_matrix_mat_mul(csr_1, csr_2)
        if len(ashp) > 2 or len(b) > 2:
            remainder_a = ashp[:-1]
            remainder_b = bshp[1:]
            new = new.reshape(remainder_a + remainder_b)
        return new

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
        import tensorflow as tf

        if isinstance(other, tf.SparseTensor):
            # one main case to which all others will defer

            return type(self)(self._tf_sparse_dot(self.tensor, other))
        elif isinstance(other, TensorFlowSparseArray):
            return self.dot(other.tensor)
        elif isinstance(other, (sp.spmatrix, ScipySparseArray)):
            # heavy duty...
            return self.dot(type(self)(other))
        elif isinstance(other, tf.Tensor):
            return tf.sparse.sparse_dense_matmul(self, other)
        else:
            raise TypeError("dot not defined for {} and {}".format(type(self).__name__, type(other).__name__))


def _dot(a, b):
    if isinstance(a, SparseArray):
        a = a.ascsr()
    if isinstance(b, SparseArray):
        b = b.ascsr()

    if isinstance(a, sp.spmatrix):
        dense_output = False
        if not isinstance(b, sp.spmatrix):
            dense_output = True
            # we convert it to a sparse thing to avoid memory blow-ups when we get dense unpacking...?
            b = sp.csr_matrix(b)

        wat = a.dot(b)
        # raise Exception(wat.shape, a.shape, b.shape)
    else:
        dense_output = True
        # we convert it to a sparse thing to avoid memory blow-ups when we get dense unpacking...?
        a = sp.csr_matrix(a)
        if not isinstance(b, sp.spmatrix):
            dense_output = True
            # we convert it to a sparse thing to avoid memory blow-ups when we get dense unpacking...?
            b = sp.csr_matrix(b)
        wat = a.dot(b)

    # print(">>>>>", a.shape, b.shape, wat.shape)

    if dense_output:
        wat = wat.toarray()
    return wat

# def asCOO(a):
#     if not isinstance(a, sp.coo_matrix):
#         a = sp.coo_matrix(a)
#     return a
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

    try:
        iter(axes)
    except TypeError:
        axes_a = list(range(-axes, 0))
        axes_b = list(range(0, axes))
    else:
        axes_a, axes_b = axes
    try:
        na = len(axes_a)
        axes_a = list(axes_a)
    except TypeError:
        axes_a = [axes_a]
        na = 1
    try:
        nb = len(axes_b)
        axes_b = list(axes_b)
    except TypeError:
        axes_b = [axes_b]
        nb = 1

    as_ = a.shape
    nda = a.ndim
    bs = b.shape
    ndb = b.ndim
    equal = True
    if na != nb:
        equal = False
    else:
        for k in range(na):
            if as_[axes_a[k]] != bs[axes_b[k]]:
                equal = False
                break
            if axes_a[k] < 0:
                axes_a[k] += nda
            if axes_b[k] < 0:
                axes_b[k] += ndb
    if not equal:
        raise ValueError("shape-mismatch for sum ({}{}@{}{})".format(as_, axes_a, bs, axes_b))

    # Move the axes to sum over to the end of "a"
    # and to the front of "b"
    notin = [k for k in range(nda) if k not in axes_a]
    newaxes_a = [notin, axes_a]
    N2 = 1
    for axis in axes_a:
        N2 *= as_[axis]
    totels_a = np.prod(as_)
    newshape_a = (totels_a // N2, N2)
    olda = [as_[axis] for axis in notin]

    notin = [k for k in range(ndb) if k not in axes_b]
    newaxes_b = [axes_b, notin]
    N2 = 1
    for axis in axes_b:
        N2 *= bs[axis]
    totels_b = np.prod(bs)
    newshape_b = (N2, totels_b // N2)
    oldb = [bs[axis] for axis in notin]

    if any(dim == 0 for dim in ip.chain(newshape_a, newshape_b)):
        res = sp.csr_matrix((olda + oldb), dtype=b.dtype)
        # dense output...I guess that's clean?
        if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
            res = res.todense()
        return res

    if newshape_a[0] > 2 * newshape_b[1]:
        # indicates it will be faster to transpose both arrays, dot, and transpose back
        if a.ndim > 1:
            # print(">>>>", newaxes_a)
            at = a.transpose(newaxes_a[1] + newaxes_a[0])
            # if newshape_a[1] > 5000:
            #     raise Exception("why")
        else:
            at = a

        at = at.reshape(np.flip(newshape_a))

        if b.ndim > 1:
            bt = b.transpose(newaxes_b[1] + newaxes_b[0])
        else:
            bt = b
        bt = bt.reshape(np.flip(newshape_b))

        # if isinstance(bt, np.ndarray):
        #     bt = sp.csr_matrix(bt)

        res = _dot(bt, at).transpose()

    else:
        if a.ndim > 1:
            at = a.transpose(newaxes_a[0] + newaxes_a[1])
        else:
            at = a
        at = at.reshape(newshape_a)

        if b.ndim > 1:
            bt = b.transpose(newaxes_b[0] + newaxes_b[1])
        else:
            bt = b
        bt = bt.reshape(newshape_b)

        res = _dot(at, bt)

    if isinstance(res, sp.spmatrix):
        if isinstance(a, ScipySparseArray):
            res = ScipySparseArray(res, shape=olda + oldb, layout=a.fmt)
        elif isinstance(b, sp.spmatrix):
            res = ScipySparseArray(res, shape=olda + oldb, layout=b.fmt)
        else:
            res = res.reshape(olda + oldb)
    else:
        res = res.reshape(olda + oldb)

    return res

def matrix_dot_into(a, b, out, *, alpha=1, beta=0,
                    working_memory=64*1024**2, block_callback=None):
    """Accumulate ``alpha * a @ b + beta * out`` into an existing array.

    Supports dense/CSR left and dense/sparse right matrices, including ScipySparseArray.
    Products are consumed in bounded output blocks. Sparse products use
    individual dense columns, avoiding a full C-order copy of a transposed
    multi-vector. Inputs must not overlap the output. A block_callback, if
    supplied, receives (row_slice, column_slice, unscaled_product); its product
    is borrowed and must not be retained. working_memory is a temporary-buffer
    target, excluding input storage and backend-private workspaces.
    """
    if isinstance(a, EvaluatedSparseMatrix):
        return a.dot_into(b, out, alpha=alpha, beta=beta,
                          working_memory=working_memory, block_callback=block_callback)
    if not isinstance(working_memory, (int, np.integer)) or working_memory < 1:
        raise ValueError('working_memory must be a positive integer byte count')
    if isinstance(a, ScipySparseArray):
        if len(a.shape) != 2 or a.shape != a.data.shape:
            raise ValueError('matrix_dot_into requires a two-dimensional matrix')
        a = a.data
    if isinstance(b, ScipySparseArray):
        b = b.data
    sparse_right = sp.issparse(b)
    original_b = b.data if sparse_right else b
    b = b.tocsc(copy=False) if sparse_right else np.asarray(b)
    out = np.asarray(out)
    vector = not sparse_right and b.ndim == 1
    if vector:
        b = b[:, np.newaxis]
        target = out[:, np.newaxis] if out.ndim == 1 else out
    else:
        target = out
    if (getattr(a, 'ndim', None) != 2 or b.ndim != 2 or target.ndim != 2
            or a.shape[1] != b.shape[0]
            or target.shape != (a.shape[0], b.shape[1])):
        raise ValueError('Incompatible matrix_dot_into shapes')
    sparse = sp.issparse(a)
    if sparse and sparse_right:
        # Convert once per product, rather than once per output column/tile.
        # The right CSR row pointer is sparse storage, never a dense C1 copy.
        b = b.tocsr(copy=False)
    if sparse and a.format != 'csr':
        raise ValueError('matrix_dot_into requires CSR sparse input')
    if not sparse:
        a = np.asarray(a)
    if not target.flags.writeable:
        raise ValueError('matrix_dot_into output is read-only')
    if (np.shares_memory(target, original_b)
            or np.shares_memory(target, a.data if sparse else a)):
        raise ValueError('matrix_dot_into inputs must not overlap the output')
    dtype = np.result_type(a.dtype, b.dtype)
    if not np.can_cast(np.result_type(dtype, alpha, beta), target.dtype, casting='same_kind'):
        raise TypeError('matrix_dot_into output dtype cannot hold the result')
    if beta == 0:
        target.fill(0)
    elif beta != 1:
        np.multiply(target, beta, out=target)
    if not target.size or (alpha == 0 and block_callback is None):
        return out

    def consume(rows, columns, values):
        if block_callback is not None:
            block_callback(rows, columns, values)
        dest = target[rows, columns]
        if alpha == 1:
            np.add(dest, values, out=dest)
        elif alpha == -1:
            np.subtract(dest, values, out=dest)
        elif alpha != 0:
            np.add(dest, alpha*values, out=dest)

    itemsize = max(np.dtype(dtype).itemsize, target.dtype.itemsize)
    if sparse:
        ptr = a.indptr
        width = max(1, b.shape[1]) if sparse_right else 1
        max_rows = max(1, working_memory//(4*ptr.dtype.itemsize + 4*itemsize*width))
        max_nnz = max(1, working_memory//(a.data.dtype.itemsize + a.indices.dtype.itemsize))
        start = 0
        while start < a.shape[0]:
            last = int(np.searchsorted(ptr, int(ptr[start])+max_nnz, side='right'))-1
            stop = max(start+1, min(a.shape[0], start+max_rows, last))
            lo, hi = int(ptr[start]), int(ptr[stop])
            rows = slice(start, stop)
            # Values and indices are borrowed when their native dtype permits;
            # only the row pointer needs rebasing. No full COO coordinates.
            part = sp.csr_matrix((a.data[lo:hi], a.indices[lo:hi], ptr[start:stop+1]-lo),
                                 shape=(stop-start, a.shape[1]), copy=False)
            if sparse_right:
                value = part.dot(b).toarray()
                consume(rows, slice(0, b.shape[1]), value)
                del value
            else:
                for column in range(b.shape[1]):
                    value = part.dot(b[:, column])
                    consume(rows, slice(column, column+1), value[:, np.newaxis])
                    del value
            start = stop
    else:
        rows_per_block = min(a.shape[0], max(1, working_memory//(4*itemsize)))
        columns_per_block = min(b.shape[1], max(1,
            working_memory//(4*itemsize*max(1, rows_per_block+a.shape[1]))))
        work = np.empty(rows_per_block*columns_per_block, dtype=dtype)
        for start in range(0, a.shape[0], rows_per_block):
            stop = min(a.shape[0], start+rows_per_block)
            for first in range(0, b.shape[1], columns_per_block):
                last = min(b.shape[1], first+columns_per_block)
                value = work[:(stop-start)*(last-first)].reshape(stop-start, last-first)
                if sparse_right:
                    value[:] = b[:, first:last].T.dot(a[start:stop].T).T
                else:
                    np.dot(a[start:stop], b[:, first:last], out=value)
                consume(slice(start, stop), slice(first, last), value)
    return out
