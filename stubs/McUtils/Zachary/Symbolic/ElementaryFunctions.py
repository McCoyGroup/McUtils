import abc, numpy as np, itertools, collections, copy
from functools import reduce
from ...Misc import Abstract
__all__ = ['Symbols', 'SymPyFunction']

class Functionlike(metaclass=abc.ABCMeta):
    """
    A function suitable for symbolic manipulation
    with derivatives and evlauation
    """

    @abc.abstractmethod
    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...
    compile_vars = 0

    @staticmethod
    def cur_var():
        ...

    @staticmethod
    def inc_var():
        ...

    @staticmethod
    def reset_var():
        ...

    @staticmethod
    def get_compile_var():
        ...

    def get_compile_spec(self) -> 'Abstract.Expr':
        ...

    def compile(self, mode='numba'):
        ...

    @abc.abstractmethod
    def deriv(self, *which, simplify=True) -> 'Functionlike':
        ...

    def __call__(self, r):
        ...

    def __neg__(self):
        ...

    def __mul__(self, other):
        ...

    def __rmul__(self, other):
        ...

    def __truediv__(self, other):
        ...

    def __rtruediv__(self, other):
        ...

    def __add__(self, other):
        ...

    def __radd__(self, other):
        ...

    def __sub__(self, other):
        ...

    def __rsub__(self, other):
        ...

    def __pow__(self, power, modulo=None):
        ...

    def invert(self):
        ...

    def __invert__(self):
        ...

    def copy(self):
        ...

    def compose(self, other):
        ...

    @staticmethod
    def is_zero(f: 'Functionlike'):
        ...

    @staticmethod
    def is_one(f: 'Functionlike'):
        ...

    @staticmethod
    def is_identity(f: 'Functionlike'):
        ...

    @property
    def sort_val(self):
        ...

    def get_sortval(self):
        ...

    def simplify(self, iterations=10) -> 'Functionlike':
        ...

    def apply_simplifications(self) -> 'Functionlike':
        ...

    @classmethod
    def merge_funcs(cls, funcs, reducer, iterations=10):
        ...

    def __hash__(self):
        ...

    def get_children(self):
        ...

    @property
    def children(self):
        ...

    @classmethod
    def traverse(cls, root, traversal_order='depth', visit_order='post', node_test=None, max_depth=None, track_index=False):
        ...

    def get_child(self, pos) -> 'Functionlike':
        ...

    def replace_child(self, pos, new) -> 'Functionlike':
        ...

    def tree_repr(self, sep='', indent=''):
        ...

class ElementaryFunction(Functionlike):
    """
    A _univariate_ function (though it can be threadable)
    that has known values and derivatives
    """
    __slots__ = ['idx']

    def __init__(self, *, idx=None):
        ...

    @abc.abstractmethod
    def get_deriv(self) -> 'ElementaryFunction':
        ...

    def deriv(self, order=1, simplify=True):
        ...

    def __repr__(self):
        ...

    def idx_compatible(self, other):
        ...

class Variable(ElementaryFunction):

    def __init__(self, name, idx):
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self) -> 'Functionlike':
        ...

    def simplify(self, iterations=10) -> 'Functionlike':
        ...

    def __hash__(self):
        ...

    def __eq__(self, other):
        ...

    def __repr__(self):
        ...

    def tree_repr(self, sep='', indent=''):
        ...

class ElementaryVaradic(ElementaryFunction):
    __slots__ = ['functions', 'idx']

    def __init__(self, *functions: ElementaryFunction, idx=None):
        ...
    sort_key = None

    def get_sortval(self):
        ...

    def __hash__(self):
        ...

    def tree_equivalent(self, other):
        ...

    def __eq__(self, other):
        ...

    def get_children(self):
        ...

    @classmethod
    @abc.abstractmethod
    def get_repr(cls, fns) -> str:
        ...

    def __repr__(self):
        ...

    def tree_repr(self, sep='\n', indent=''):
        ...

    def get_child(self, pos):
        ...

    def replace_child(self, pos, new) -> 'ElementaryVaradic':
        ...

class ElementarySummation(ElementaryVaradic):
    sort_key = 1000

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    @classmethod
    def get_repr(cls, fns):
        ...

    @classmethod
    def merge_product(cls, f1, f2):
        ...

    @classmethod
    def reduce_pair(cls, f1, f2) -> 'Iterable[Functionlike]|bool':
        ...

    def apply_simplifications(self):
        ...

class ElementaryProduct(ElementaryVaradic):
    sort_key = 100

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    @classmethod
    def reduce_pair(cls, f1, f2) -> 'Iterable[Functionlike]|bool':
        ...

    def apply_simplifications(self):
        ...

    @classmethod
    def get_repr(cls, fns):
        ...

class ElementaryComposition(ElementaryVaradic):
    sort_key = 0

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    @classmethod
    def subs_identities(cls, f1, f2):
        ...

    def apply_simplifications(self):
        ...

    @classmethod
    def get_repr(cls, fns):
        ...

class MultivariateFunction(Functionlike):
    """
    A multivariate function composed from elementary functions.
    This is a
    """

    def __init__(self, *functions: 'ElementaryFunction|MultivariateFunction', indices=None):
        ...

    @classmethod
    def _reduce_indices(cls, terms):
        ...

    @classmethod
    def construct_varivariate(cls, univariate, multivariate, terms, indices=None):
        ...

    @property
    def indices(self):
        ...

    @property
    def ndim(self):
        ...

    @abc.abstractmethod
    def get_deriv(self, *counts) -> 'Functionlike':
        ...

    def deriv(self, *which, order=1, ndim=None, simplify=True) -> 'Functionlike':
        ...
    sort_key = None

    def get_sortval(self):
        ...

    def apply_simplifications(self) -> 'Functionlike':
        ...

    def __hash__(self):
        ...

    def tree_equivalent(self, other):
        ...

    def __eq__(self, other):
        ...

    def get_children(self):
        ...

    def tree_repr(self, sep='\n', indent=''):
        ...

    def get_child(self, pos):
        ...

    def replace_child(self, pos, new) -> 'ElementaryVaradic':
        ...

class TensorFunction(MultivariateFunction):
    """
    A tensor of functions
    """

    def __init__(self, functions: np.ndarray, symmetric=True, indices=None):
        ...

    def _get_res_array(self, v) -> np.ndarray:
        ...

    def apply_function(self, fn, res_builder=None) -> np.ndarray:
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self, *counts) -> 'TensorFunction':
        ...

    def get_sortval(self):
        ...

    def apply_simplifications(self) -> 'Functionlike':
        ...

    def __repr__(self):
        ...

    @classmethod
    def format_repr_array(cls, arr, ilevel=0, brackets='[]', sep=',\n', indent=' '):
        ...

    def tree_equivalent(self, other):
        ...

    def tree_repr(self, sep='\n', indent=''):
        ...

    def copy(self) -> 'TensorFunction':
        ...

    def get_children(self) -> 'Iterable[Functionlike]':
        ...

    def get_child(self, pos) -> 'Functionlike':
        ...

    def replace_child(self, pos, new) -> 'TensorFunction':
        ...

class Summation(MultivariateFunction):
    """
    A summation of 1D functions to support testing derivs
    """

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    @classmethod
    def construct(cls, *terms, indices=None):
        ...

    def get_deriv(self, *counts) -> 'MultivariateFunction':
        ...
    sort_key = 1000

    @classmethod
    def merge_product(cls, f1, f2):
        ...

    @classmethod
    def reduce_pair(cls, f1, f2) -> 'Iterable[Functionlike]|bool':
        ...

    def apply_simplifications(self):
        ...

    def __repr__(self):
        ...

class Product(MultivariateFunction):
    """
    A summation of 1D functions to support testing derivs
    """

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    @classmethod
    def construct(cls, *terms, indices=None):
        ...

    def get_1d_deriv(self, idx, amt):
        ...

    def get_deriv(self, *counts):
        ...
    sort_key = 100

    def apply_simplifications(self):
        ...

    def __repr__(self):
        ...

class Composition(MultivariateFunction):
    """
    A composition of multivariate functions that
    uses the chain rule for derivatives
    """

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    @classmethod
    def construct(cls, *terms, indices=None):
        ...

    def apply_simplifications(self):
        ...

    def get_deriv(self, *counts):
        ...

    def __repr__(self):
        ...

class Scalar(ElementaryFunction):
    """
    Broadcasts a constant value
    """
    __slots__ = ['scalar', 'idx']

    def __init__(self, scalar, *, idx=0):
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    def deriv(self, order=1, *, simplify=True):
        ...

    def get_sortval(self):
        ...

    def __hash__(self):
        ...

    def __eq__(self, other):
        ...

    def __repr__(self):
        ...

    def tree_repr(self, sep='\n', indent=''):
        ...

class Identity(ElementaryFunction):
    """
    Identity function for compositions
    """

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    def deriv(self, order=1, simplify=True):
        ...

    def simplify(self, iterations=10) -> 'Functionlike':
        ...

    def __hash__(self):
        ...

    def __eq__(self, other):
        ...

    def get_sortval(self):
        ...

    def __repr__(self):
        ...

class Power(ElementaryFunction):
    __slots__ = ['power', 'idx']

    def __init__(self, power, *, idx=None):
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    def __hash__(self):
        ...

    def __eq__(self, other):
        ...
    sort_key = 20

    def get_sortval(self):
        ...

    def apply_simplifications(self) -> 'Functionlike':
        ...

    def __repr__(self):
        ...

    def tree_repr(self, sep='\n', indent=''):
        ...

class Exponent(ElementaryFunction):
    __slots__ = ['base', 'idx']

    def __init__(self, base, *, idx=None):
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    def __hash__(self):
        ...

    def __eq__(self, other):
        ...
    sort_key = 50

    def get_sortval(self):
        ...

    def __repr__(self):
        ...

    def tree_repr(self, sep='\n', indent=''):
        ...

class Exp(Exponent):
    __slots__ = ['idx']

    def __init__(self, *, idx=None):
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    def __repr__(self):
        ...

    def tree_repr(self, sep='\n', indent=''):
        ...

class Logarithm(ElementaryFunction):
    __slots__ = ['base', 'idx']

    def __init__(self, base, *, idx=None):
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    def get_compile_spec(self):
        ...

    def __hash__(self):
        ...

    def __eq__(self, other):
        ...
    sort_key = 60

    def get_sortval(self):
        ...

    def __repr__(self):
        ...

    def tree_repr(self, sep='\n', indent=''):
        ...

class Ln(Logarithm):
    __slots__ = ['idx']

    def __init__(self, *, idx=None):
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    def __repr__(self):
        ...

    def tree_repr(self, sep='\n', indent=''):
        ...

class Sin(ElementaryFunction):

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    def get_compile_spec(self):
        ...

    def __hash__(self):
        ...

    def __eq__(self, other):
        ...

    def __repr__(self):
        ...

class Cos(ElementaryFunction):

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_compile_spec(self):
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    def __hash__(self):
        ...

    def __eq__(self, other):
        ...

    def __repr__(self):
        ...

class CompoundFunction(ElementaryFunction):

    def __init__(self, *, idx=None):
        ...

    @abc.abstractmethod
    def get_expression(self) -> 'ElementaryFunction':
        ...

    @property
    def expression(self):
        ...

    def __eq__(self, other):
        ...

    def get_deriv(self) -> 'ElementaryFunction':
        ...

    def get_compile_spec(self):
        ...

    def get_sortval(self):
        ...

class Morse(CompoundFunction):

    def __init__(self, *, de=1, a=1, re=0, idx=None):
        ...

    def get_expression(self):
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_deriv(self):
        ...

    def __repr__(self):
        ...

    def tree_repr(self, sep='\n', indent=''):
        ...

class MorseDeriv(CompoundFunction):

    def __init__(self, order, *, de=1, a=1, re=0, idx=None):
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def get_expression(self) -> 'ElementaryFunction':
        ...

    def get_deriv(self) -> 'MorseDeriv':
        ...

    def __repr__(self):
        ...

    def tree_repr(self, sep='\n', indent=''):
        ...

class Symbols:

    def __init__(self, *vars):
        ...

    @classmethod
    def scalar(cls, v):
        ...

    @classmethod
    def log(cls, v, base=None):
        ...

    @classmethod
    def exp(cls, v, base=None):
        ...

    @classmethod
    def cos(cls, x):
        ...

    @classmethod
    def sin(cls, x):
        ...

    @classmethod
    def morse(cls, r, de=1, a=1, re=0):
        ...

class SymPyFunction:
    """
    A function suitable for symbolic manipulation
    with derivatives and evlauation
    """

    @classmethod
    def get_sympy(cls):
        ...

    @property
    def sympy(self):
        ...

    def __init__(self, expr, vars=None):
        ...

    def _varkey(self, v):
        ...

    def sort_vars(self, vars):
        ...

    def merge_vars(self, v1, v2):
        ...

    def compile(self):
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def deriv(self, *which, order=1):
        ...

    def __call__(self, r):
        ...

    def __neg__(self):
        ...

    def __mul__(self, other):
        ...

    def __rmul__(self, other):
        ...

    def __truediv__(self, other):
        ...

    def __rtruediv__(self, other):
        ...

    def __add__(self, other):
        ...

    def __radd__(self, other):
        ...

    def __sub__(self, other):
        ...

    def __rsub__(self, other):
        ...

    def __pow__(self, power, modulo=None):
        ...

    def invert(self):
        ...

    def __invert__(self):
        ...

    def copy(self):
        ...

    def compose(self, other):
        ...

    @classmethod
    def symbols(cls, *syms):
        ...

    @classmethod
    def exp(cls, fn):
        ...

    @classmethod
    def morse(cls, var, de=10, a=1, re=0):
        ...

    def __repr__(self):
        ...

class SymPyArrayFunction:

    def __init__(self, expr_array, symmetric=False):
        ...

    def _get_res_array(self, v) -> np.ndarray:
        ...

    def apply_function(self, fn, res_builder=None) -> np.ndarray:
        ...

    def eval(self, r: np.ndarray) -> 'np.ndarray':
        ...

    def __call__(self, r):
        ...

    def __neg__(self):
        ...

    def __mul__(self, other):
        ...

    def __rmul__(self, other):
        ...

    def __truediv__(self, other):
        ...

    def __rtruediv__(self, other):
        ...

    def __add__(self, other):
        ...

    def __radd__(self, other):
        ...

    def __sub__(self, other):
        ...

    def __rsub__(self, other):
        ...

    def __pow__(self, power, modulo=None):
        ...

    def invert(self):
        ...

    def __invert__(self):
        ...

    def copy(self):
        ...

    def compose(self, other):
        ...

    def __repr__(self):
        ...