import abc, numpy as np, typing, weakref, hashlib
import collections
from ...Numputils import vec_outer, vec_tensordot
from ...Combinatorics import IntegerPartitioner, UniquePermutations
__all__ = ['TensorDerivativeConverter', 'TensorExpansionTerms', 'TensorExpression']

class TensorExpression:

    def __init__(self, expr: 'TensorExpression.Term|List', **vars):
        ...

    def eval(self, subs: dict=None, print_terms=False):
        ...

    @property
    def primitives(self):
        ...

    def walk(self, callback):
        ...

    def get_prims(self):
        ...

    def __repr__(self):
        ...

    class ArrayStack:
        __slots__ = ['stack_shape', 'array']

        def __init__(self, shape, array):
            """
            :param shape: shape of the stack of arrays to thread over
            :type shape:
            :param array:
            :type array:
            """
            ...

        def __hash__(self):
            ...

        def __eq__(self, other):
            ...

        @staticmethod
        def _make_broadcastable(a1, a2, offset):
            ...

        @classmethod
        def _pad_shape(cls, arr, other, stack_shape):
            ...

        def __add__(self, other):
            ...

        def __mul__(self, other):
            ...

        def __rmul__(self, other):
            ...

        def __pos__(self):
            ...

        def __neg__(self):
            ...

        def __truediv__(self, other):
            ...

        def __rtruediv__(self, other):
            ...

        def flip(self):
            ...

        def __pow__(self, power, modulo=None):
            ...

        @property
        def stack_dim(self):
            ...

        @property
        def shape(self):
            ...

        @property
        def ndim(self):
            ...

        def expand_dims(self, where):
            ...

        def moveaxis(self, i, j):
            ...

        def tensordot(self, other, axes=None):
            ...

        def outer(self, other, axes=None):
            ...

        def rev_outer(self, other, axes=None):
            ...

        def __repr__(self):
            ...

    class Term(metaclass=abc.ABCMeta):
        _array_cache = weakref.WeakKeyDictionary()

        def __init__(self, array=None, name=None):
            ...

        @abc.abstractmethod
        def get_children(self) -> 'Iterable[TensorExpression.Term]':
            ...

        @property
        def children(self):
            ...

        @abc.abstractmethod
        def deriv(self) -> 'TensorExpression.Term':
            ...

        def dQ(self):
            ...

        @abc.abstractmethod
        def array_generator(self, **kwargs) -> np.ndarray:
            ...

        @property
        def ndim(self):
            ...

        def get_hash(self):
            ...

        def __hash__(self):
            ...

        def __eq__(self, other):
            ...

        def asarray(self, print_terms=False, cache=True, **kw):
            ...

        @property
        def array(self):
            ...

        @array.setter
        def array(self, arr):
            ...

        @abc.abstractmethod
        def rank(self) -> int:
            ...

        @property
        def ndim(self):
            ...

        @abc.abstractmethod
        def to_string(self) -> str:
            ...

        def __repr__(self):
            ...

        @abc.abstractmethod
        def reduce_terms(self, check_arrays=False) -> 'TensorExpression.Term':
            ...

        def _check_simp(self, new):
            ...

        def simplify(self, check_arrays=False):
            ...

        def __add__(self, other):
            ...

        def __mul__(self, other):
            ...

        def __rmul__(self, other):
            ...

        def __pos__(self):
            ...

        def __neg__(self):
            ...

        def flip(self):
            ...

        def divided(self):
            ...

        def __truediv__(self, other):
            ...

        def __rtruediv__(self, other):
            ...

        def dot(self, other, i, j):
            ...

        def shift(self, i, j):
            ...

        def det(self):
            ...

        def tr(self, axis1=1, axis2=2):
            ...

        def inverse(self):
            ...

        def __invert__(self):
            ...

        def outer(self, other):
            ...

    class SumTerm(Term):

        def __init__(self, *terms: 'TensorExpression.Term', array=None, name=None):
            ...

        def get_children(self):
            ...

        def deriv(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def rank(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

        def get_hash(self):
            ...

        def to_string(self):
            ...

        def substitute(self, other):
            """substitutes other in to the sum by matching up all necessary terms"""
            ...

    class ScalingTerm(Term):

        def __init__(self, term: 'TensorExpression.Term', scaling, array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

        def deriv(self):
            ...

    class ScalarScalingTerm(Term):
        """
        Scaling elementwise with correct broadcasting
        """

        def __init__(self, term: 'TensorExpression.Term', scaling, axes=None, array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

        def deriv(self):
            ...

    class ScalarPowerTerm(Term):
        """
        Represents x^n.
        Only can get valid derivatives for scalar terms.
        Beware of that.
        """

        def __init__(self, term: 'TensorExpression.Term', pow, array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

        def deriv(self):
            ...

    class FlippedTerm(ScalarPowerTerm):
        """
        Represents 1/x. Only can get valid derivatives for scalar terms. Beware of that.
        """

        def __init__(self, term: 'TensorExpression.Term', pow=-1, array=None):
            ...

        def get_children(self):
            ...

        def to_string(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

    class AxisShiftTerm(Term):

        def __init__(self, term: 'TensorExpression.Term', start: int, end: int, array=None, name=None):
            ...

        def get_children(self):
            ...

        def deriv(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def rank(self):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            """We simplify over the possible swap classes"""
            ...

    class OuterTerm(Term):
        """
        Provides an outer product
        """

        def __init__(self, a: 'TensorExpression.Term', b: 'TensorExpression.Term', array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

        def deriv(self):
            ...

    class ContractionTerm(Term):

        def __init__(self, left: 'TensorExpression.Term', i: typing.Union[int, typing.Iterable[int]], j: typing.Union[int, typing.Iterable[int]], right: 'TensorExpression.Term', array=None, name=None):
            ...

        def get_children(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def rank(self):
            ...

        def deriv(self):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

    class InverseTerm(Term):

        def __init__(self, term: 'TensorExpression.Term', array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

        def deriv(self):
            ...

    class TraceTerm(Term):

        def __init__(self, term: 'TensorExpression.Term', axis1=1, axis2=2, array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

        def deriv(self):
            ...

    class DeterminantTerm(Term):

        def __init__(self, term: 'TensorExpression.Term', array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

        def deriv(self):
            ...

    class VectorNormTerm(Term):

        def __init__(self, term: 'TensorExpression.Term', array=None, name=None, axis=-1):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

        def deriv(self):
            ...

    class ScalarFunctionTerm(Term):

        def __init__(self, term, name='f', f=None, array=None, derivative_order=0):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

        def deriv(self):
            ...

    class ConstantArray(Term):
        """
        Square tensor of constants (squareness assumed, not checked)
        """

        def __init__(self, array, parent: 'TensorExpression.Term'=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def get_hash(self):
            ...

        def to_string(self):
            ...

        def deriv(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

    class IdentityMatrix(ConstantArray):

        def __init__(self, ndim, parent=None, name='I'):
            ...

    class OuterPowerTerm(Term):
        """
        Represents a matrix-power type term
        """

        def __init__(self, base: 'TensorExpression.Term', pow: int, array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def get_hash(self):
            ...

        def to_string(self):
            ...

        def deriv(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

    class TermVector(Term):

        def __init__(self, *terms: 'TensorExpression.Term|List[TensorExpression.Term]', array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def deriv(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

    class CoordinateVector(Term):

        def __init__(self, vals_array, array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def deriv(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

    class CoordinateTerm(Term):

        def __init__(self, idx: int, vec: 'TensorExpression.CoordinateVector', array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def deriv(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

    class PolynomialTerm(Term):

        def __init__(self, expansion: 'Taylor.FunctionExpansion', coords: 'TensorExpression.TermVector'=None, array=None, name=None):
            ...

        def get_children(self):
            ...

        def rank(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def to_string(self):
            ...

        def deriv(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

class TensorExpansionError(Exception):
    ...

class TensorExpansionTerms:
    """
    A friend of DumbTensor which exists
    to not only make the tensor algebra suck less but also
    to make it automated by making use of some simple rules
    for expressing derivatives specifically in the context of
    doing the coordinate transformations we need to do.
    Everything here is 1 indexed since that's how I did the OG math
    """

    def __init__(self, qx_terms, xv_terms, qxv_terms=None, base_qx=None, base_xv=None, q_name='Q', v_name='V'):
        """
        :param qx_terms:
        :type qx_terms: Iterable[np.ndarray]
        :param xv_terms:
        :type xv_terms: Iterable[np.ndarray]
        """
        ...

    def QX(self, n):
        ...

    def XV(self, m):
        ...

    def QXV(self, n, m):
        ...

    class QXTerm(TensorExpression.Term):

        def __init__(self, terms: 'TensorExpansionTerms', n: int, array=None):
            ...

        def get_children(self):
            ...

        def deriv(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def rank(self):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

    class XVTerm(TensorExpression.Term):

        def __init__(self, terms: 'TensorExpansionTerms', m: int, array=None):
            ...

        def get_children(self):
            ...

        def deriv(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def rank(self):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

    class QXVTerm(TensorExpression.Term):

        def __init__(self, terms: 'TensorExpansionTerms', n: int, m: int, array=None):
            ...

        def get_children(self):
            ...

        def deriv(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def rank(self):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

    class BasicContractionTerm(TensorExpression.Term):
        """
        Special case tensor contraction term between two elements of the
        tensor expansion terms.
        """

        def __init__(self, terms: 'TensorExpansionTerms', n: int, i: int, j: int, m: int, array=None):
            ...

        def deriv(self):
            ...

        def array_generator(self, print_terms=False):
            ...

        def rank(self):
            ...

        def to_string(self):
            ...

        def reduce_terms(self, check_arrays=False):
            ...

class TensorDerivativeConverter:
    """
    A class that makes it possible to convert expressions
    involving derivatives in one coordinate system in another
    """
    TensorExpansionError = TensorExpansionError

    def __init__(self, jacobians, derivatives=None, mixed_terms=None, jacobians_name='Q', values_name='V'):
        """

        :param jacobians: The Jacobian and higher-order derivatives between the coordinate systems
        :type jacobians: Iterable[np.ndarray]
        :param derivatives: Derivatives of some quantity in the original coordinate system
        :type derivatives: Iterable[np.ndarray]
        :param mixed_terms: Mixed derivatives of some quantity involving the new and old coordinates
        :type mixed_terms: Iterable[Iterable[None | np.ndarray]]
        """
        ...

    def convert(self, order=None, print_transformations=False, check_arrays=False):
        ...

    @classmethod
    def compute_partition_terms(cls, partition):
        ...

    @classmethod
    def convert_partition(cls, partition, derivs, vals, val_axis=0):
        ...

    @classmethod
    def convert_fast(cls, derivs, vals, val_axis=-1, order=None):
        ...