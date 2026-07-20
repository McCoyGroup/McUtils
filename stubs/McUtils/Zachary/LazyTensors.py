"""
LazyTensors provides a small framework for symbolically working with Tensors
"""
import numpy as np
from ..Numputils import SparseArray
__all__ = ['Tensor', 'TensorOp', 'LazyOperatorTensor', 'SparseTensor']

class Tensor:
    """A semi-symbolic representation of a tensor. Allows for lazy processing of tensor operations."""

    def __init__(self, a, shape=None):
        ...

    @classmethod
    def from_array(cls, a, shape=None):
        ...

    @property
    def array(self):
        ...

    def get_shape(self, a):
        ...

    @property
    def shape(self):
        ...

    def get_dim(self):
        ...

    @property
    def dim(self):
        ...

    def add(self, other, **kw):
        ...

    def mul(self, other, **kw):
        ...

    def dot(self, other, **kw):
        ...

    def transpose(self, axes, **kw):
        ...

    def pow(self, other, **kw):
        ...

    def __mul__(self, other):
        ...

    def __rmul__(self, other):
        ...

    def __add__(self, other):
        ...

    def __pow__(self, power, modulo=None):
        ...

    def handle_missing_indices(self, missing, extant):
        ...

    def pull_index(self, *idx):
        """Defines custom logic for handling how we pull indices

        :param idx:
        :type idx:
        :return:
        :rtype:
        """
        ...

    def __getitem__(self, item):
        ...

    def __repr__(self):
        ...

class SparseTensor(Tensor):
    """
    Tensor class that uses SparseArray
    """

    def __init__(self, a, shape=None):
        ...

    @property
    def array(self):
        ...

class TensorOp(Tensor):
    """A lazy representation of tensor operations to save memory"""

    def __init__(self, a, b, axis=None):
        ...

    def op(self, a, b):
        ...

    def get_shape(self, a, b):
        ...

    @property
    def shape(self):
        ...

    @property
    def array(self):
        """Ought to always compile down to a proper ndarray

        :return:
        :rtype: np.ndarray
        """
        ...

    def __getitem__(self, i):
        ...

class TensorPlus(TensorOp):
    """Represents an addition of two tensors"""

    def op(self, a, b):
        ...

    def get_shape(self, a, b):
        ...

    def __getitem__(self, i):
        ...

class TensorPow(TensorOp):
    """Represents a power of a tensors"""

    def op(self, a, b):
        ...

    def get_shape(self, a, b):
        ...

    def __getitem__(self, i):
        ...

class TensorMul(TensorOp):
    """Represents a multiplication of a tensor and a scalar"""

    def op(self, a, b):
        ...

    def get_shape(self, a, b):
        ...

    def __getitem__(self, i):
        ...

class TensorTranspose(TensorOp):
    """Represents a tensor transposition"""

    def get_shape(self, a, b):
        ...

    def op(self, a, b):
        ...

class TensorDot(TensorOp):
    """Represents a tensor contraction"""

    def get_shape(self, a, b):
        ...

    def op(self, a, b):
        ...

    def __getitem__(self, i):
        ...

class LazyOperatorTensor(Tensor):
    """A super-lazy tensor that represents the elements of an operator """

    def __init__(self, operator, shape, memoization=True, dtype=object, fill=None):
        ...

    @property
    def array(self):
        ...

    def _get_element(self, indices):
        ...

    def __getitem__(self, item):
        ...