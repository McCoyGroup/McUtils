
import abc
import numpy as np
import copy

from .. import Numputils as nput
from .. import Iterators as itut
from .. import Coordinerds as coords

from .Taylor import FunctionExpansion

__all__ = [
    "DifferentiableFunction",
    "PolynomialFunction",
    "MorseFunction",
    "CoordinateFunction"
]

class DifferentiableFunction(metaclass=abc.ABCMeta):
    def __init__(self, inds=None):
        """
        **LLM Docstring**

        Set up a differentiable function, optionally restricted to act on a subset of the
        input coordinates.

        :param inds: the coordinate indices this function depends on (all if `None`)
        :type inds: Sequence[int] | None
        """
        self.inds = inds # the application inds

    def reindex(self, idx_perm):
        """
        **LLM Docstring**

        Return a copy of the function with its coordinate indices remapped under a
        permutation of the full coordinate set.

        :param idx_perm: the coordinate permutation
        :type idx_perm: np.ndarray
        :return: the reindexed function
        :rtype: DifferentiableFunction
        """
        # if self.inds is None: self.inds = [0] # this is the most reasonable default...?
        if self.inds is None: return self
        new = copy.copy(self)
        idx_perm = np.asanyarray(idx_perm)
        new.inds = [np.where(idx_perm == i)[0][0] for i in self.inds] #TODO: find a cleaner 'find'
        return new

    def get_consistent_inds(self, funcs:'list[DifferentiableFunction]'):
        """
        **LLM Docstring**

        Compute the union of the coordinate indices used by a set of functions and
        reindex each onto that shared index set.

        :param funcs: the functions to reconcile
        :type funcs: list[DifferentiableFunction]
        :return: `(shared_inds, reindexed_funcs)`
        :rtype: tuple
        """
        inds = [f.inds for f in funcs if f.inds is not None]
        if len(inds) == 0: return None, funcs
        new_inds = np.unique(np.concatenate(inds))
        new_funcs = [f.reindex(new_inds) for f in funcs]
        return new_inds, new_funcs

    def __call__(self, coords, order=0):
        """
        **LLM Docstring**

        Evaluate the function's Taylor expansion (value plus derivatives up to `order`)
        at the given coordinates, scattering the result back into the full coordinate
        space when the function acts on only a subset of coordinates.

        :param coords: the coordinates, shape `(..., ncoords)`
        :type coords: np.ndarray
        :param order: the highest derivative order to return
        :type order: int
        :return: the expansion tensors `[value, grad, hess, ...]`
        :rtype: list[np.ndarray]
        """
        coords = np.asanyarray(coords)
        if self.inds is None:
            return self.evaluate(coords, order=order)
        else:
            subc = coords[..., self.inds]
            subtensors = self.evaluate(subc, order=order)
            expansions = subtensors[:1]
            base_shape = coords.shape[:-1]
            coords_shape = expansions[0].shape[len(base_shape):]
            ncoords = coords.shape[-1]
            for n,s in enumerate(subtensors[1:]):
                t = np.zeros(base_shape + (ncoords,) * (n+1) + coords_shape, dtype=s.dtype)
                if not nput.is_numeric(s):
                    idx = (...,) + np.ix_(*[self.inds]*(n+1)) + (slice(None),) * len(coords_shape)
                    t[idx] = s
                expansions.append(t)
            return expansions

    @abc.abstractmethod
    def evaluate(self, coords, order=0) -> list[np.ndarray]:
        """
        **LLM Docstring**

        Abstract: evaluate the function's expansion (value and derivatives) at the given
        coordinates.

        :param coords: the coordinates
        :type coords: np.ndarray
        :param order: the highest derivative order
        :type order: int
        :return: the expansion tensors
        :rtype: list[np.ndarray]
        """
        ...

    @abc.abstractmethod
    def get_children(self):
        """
        **LLM Docstring**

        Abstract: return the sub-functions this function is built from.

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        ...

    def __add__(self, other):
        """
        **LLM Docstring**

        Add another differentiable function (building/merging a `FunctionSum`) or a
        constant (building a `ConstantShiftedFunction`).

        :param other: the addend
        :return: the sum function
        :rtype: DifferentiableFunction
        """
        if isinstance(other, DifferentiableFunction):
            if isinstance(self, FunctionSum):
                if isinstance(other, FunctionSum):
                    return FunctionSum(self.funcs + other.funcs)
                else:
                    return FunctionSum(self.funcs + [other])
            elif isinstance(other, FunctionSum):
                return FunctionSum([self] + other.funcs)
            else:
                return FunctionSum([self, other])
        else:
            return ConstantShiftedFunction(self, other)
    def __radd__(self, other):
        """
        **LLM Docstring**

        Right addition, delegating to `__add__`.

        :param other: the addend
        :return: the sum function
        :rtype: DifferentiableFunction
        """
        return self + other
    def __mul__(self, other):
        """
        **LLM Docstring**

        Multiply by another differentiable function (building/merging a
        `FunctionProduct`) or a constant (building a `ConstantScaledFunction`).

        :param other: the multiplier
        :return: the product function
        :rtype: DifferentiableFunction
        """
        if isinstance(other, DifferentiableFunction):
            if isinstance(self, FunctionProduct):
                if isinstance(other, FunctionProduct):
                    return FunctionProduct(self.funcs + other.funcs)
                else:
                    return FunctionProduct(self.funcs + [other])
            elif isinstance(other, FunctionProduct):
                return FunctionProduct([self] + other.funcs)
            else:
                return FunctionProduct([self, other])
        else:
            return ConstantScaledFunction(self, other)
    def __truediv__(self, other):
        """
        **LLM Docstring**

        Divide by another differentiable function (multiplying by its reciprocal) or a
        constant.

        :param other: the divisor
        :return: the quotient function
        :rtype: DifferentiableFunction
        """
        if isinstance(other, DifferentiableFunction):
            if isinstance(self, FunctionProduct):
                if isinstance(other, FunctionProduct):
                    return FunctionProduct(self.funcs + [f.flip() for f in other.funcs])
                else:
                    return FunctionProduct(self.funcs + [other.flip()])
            elif isinstance(other, FunctionProduct):
                return FunctionProduct([self] + [f.flip() for f in other.funcs])
            else:
                return FunctionProduct([self, other.flip()])
        else:
            return ConstantScaledFunction(self, 1/other)
    def __rtruediv__(self, other):
        """
        **LLM Docstring**

        Right division (`other / self`), via the reciprocal of this function.

        :param other: the numerator
        :return: the quotient function
        :rtype: DifferentiableFunction
        """
        return self.flip() * other
    def __rmul__(self, other):
        """
        **LLM Docstring**

        Right multiplication, delegating to `__mul__`.

        :param other: the multiplier
        :return: the product function
        :rtype: DifferentiableFunction
        """
        return self * other
    def __neg__(self):
        """
        **LLM Docstring**

        Negate the function (unwrapping a double negation).

        :return: the negated function
        :rtype: DifferentiableFunction
        """
        if isinstance(self, NegatedFunction):
            return self.func
        else:
            return NegatedFunction(self)

    def flip(self):
        """
        **LLM Docstring**

        Return the reciprocal (`1 / self`) as a `ReciprocalFunction`.

        :return: the reciprocal function
        :rtype: ReciprocalFunction
        """
        return ReciprocalFunction(self)

class ConstantScaledFunction(DifferentiableFunction):
    def __init__(self, func:DifferentiableFunction, scaling, inds=None):
        """
        **LLM Docstring**

        Wrap a function scaled by a constant factor.

        :param func: the wrapped function
        :type func: DifferentiableFunction
        :param scaling: the scale factor
        :param inds: the coordinate indices (inherited from `func` if omitted)
        :type inds: Sequence[int] | None
        """
        if inds is None: inds = func.inds
        super().__init__(inds=inds)
        self.func = func
        self.scaling = scaling
    def evaluate(self, coords, order=0) -> list[np.ndarray]:
        """
        **LLM Docstring**

        Evaluate the wrapped function and scale every expansion term by the constant.

        :param coords: the coordinates
        :type coords: np.ndarray
        :param order: the highest derivative order
        :type order: int
        :return: the scaled expansion tensors
        :rtype: list[np.ndarray]
        """
        expansion = self.func(coords, order=order)
        return [self.scaling*e for e in expansion]
    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this scaled function.

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return [self.func]

class ConstantShiftedFunction(DifferentiableFunction):
    def __init__(self, func:DifferentiableFunction, shift, inds=None):
        """
        **LLM Docstring**

        Wrap a function shifted by a constant added to its value.

        :param func: the wrapped function
        :type func: DifferentiableFunction
        :param shift: the constant added to the value
        :param inds: the coordinate indices (inherited from `func` if omitted)
        :type inds: Sequence[int] | None
        """
        if inds is None: inds = func.inds
        super().__init__(inds=inds)
        self.func = func
        self.shift = shift
    def evaluate(self, coords, order=0) -> list[np.ndarray]:
        """
        **LLM Docstring**

        Evaluate the wrapped function and add the constant to the zeroth-order (value)
        term.

        :param coords: the coordinates
        :type coords: np.ndarray
        :param order: the highest derivative order
        :type order: int
        :return: the shifted expansion tensors
        :rtype: list[np.ndarray]
        """
        expansion = self.func(coords, order=order)
        return [self.shift + expansion[0]] + expansion[1:]
    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this shifted function.

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return [self.func]

class NegatedFunction(DifferentiableFunction):
    def __init__(self, func:DifferentiableFunction, inds=None):
        """
        **LLM Docstring**

        Wrap the negation of a function.

        :param func: the wrapped function
        :type func: DifferentiableFunction
        :param inds: the coordinate indices (inherited from `func` if omitted)
        :type inds: Sequence[int] | None
        """
        if inds is None: inds = func.inds
        super().__init__(inds=inds)
        self.func = func
    def evaluate(self, coords, order=0) -> list[np.ndarray]:
        """
        **LLM Docstring**

        Evaluate the wrapped function and negate every expansion term.

        :param coords: the coordinates
        :type coords: np.ndarray
        :param order: the highest derivative order
        :type order: int
        :return: the negated expansion tensors
        :rtype: list[np.ndarray]
        """
        expansion = self.func(coords, order=order)
        return [-e for e in expansion]
    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this negated function.

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return [self.func]

class FunctionSum(DifferentiableFunction):
    def __init__(self, funcs: list[DifferentiableFunction], inds=None):
        """
        **LLM Docstring**

        Represent a sum of differentiable functions, reconciling their coordinate
        indices.

        :param funcs: the summed functions
        :type funcs: list[DifferentiableFunction]
        :param inds: the shared coordinate indices (computed if omitted)
        :type inds: Sequence[int] | None
        """
        if inds is None: inds, funcs = self.get_consistent_inds(funcs)
        super().__init__(inds=inds)
        self.funcs = funcs
    def evaluate(self, coords, order=0) -> list[np.ndarray]:
        """
        **LLM Docstring**

        Evaluate each summand and add their expansions term by term.

        :param coords: the coordinates
        :type coords: np.ndarray
        :param order: the highest derivative order
        :type order: int
        :return: the summed expansion tensors
        :rtype: list[np.ndarray]
        """
        expansions = [f(coords, order=order) for f in self.funcs]
        return [
            sum(e[i] for e in expansions)
            for i in range(order+1)
        ]
    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this sum.

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return self.funcs

class FunctionProduct(DifferentiableFunction):
    def __init__(self, funcs:list[DifferentiableFunction], inds=None):
        """
        **LLM Docstring**

        Represent a product of differentiable functions, reconciling their coordinate
        indices.

        :param funcs: the multiplied functions
        :type funcs: list[DifferentiableFunction]
        :param inds: the shared coordinate indices (computed if omitted)
        :type inds: Sequence[int] | None
        """
        if inds is None: inds, funcs = self.get_consistent_inds(funcs)
        super().__init__(inds=inds)
        self.funcs = funcs

    def evaluate(self, coords, order=0):
        """
        **LLM Docstring**

        Evaluate each factor and combine their expansions via the generalized product
        (Leibniz) rule to get the product's derivatives.

        :param coords: the coordinates
        :type coords: np.ndarray
        :param order: the highest derivative order
        :type order: int
        :return: the product expansion tensors
        :rtype: list[np.ndarray]
        """
        expansions = [
            f(coords, order=order)
            for f in self.funcs
        ]

        base_shape = coords.shape[:-1]
        ncs = len(base_shape)
        nvals = len(expansions[0][0].shape[ncs:])
        # we move these axes to the back of the tensor for constructing the products
        new_exps = []
        for subexp in expansions:
            sube = []
            for e in subexp:
                for _ in range(nvals):
                    e = np.moveaxis(e, -1, ncs)
                sube.append(e)
            new_exps.append(sube)

        riffs = list(itut.riffle(new_exps, ['x']*len(expansions)))
        derivs = nput.tensorops_deriv(
            *riffs,
            order=order,
            shared=ncs + nvals
        )

        finals = []
        for d in derivs:
            for _ in range(nvals):
                d = np.moveaxis(d, ncs, -1)
            finals.append(d)

        return finals
    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this product.

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return self.funcs

class FunctionComposition(DifferentiableFunction):
    def __init__(self, outer_func, inner_funcs:list[DifferentiableFunction], inds=None):
        """
        **LLM Docstring**

        Represent the composition of an outer function with a set of inner functions,
        reconciling their coordinate indices.

        :param outer_func: the outer function
        :type outer_func: DifferentiableFunction
        :param inner_funcs: the inner functions
        :type inner_funcs: list[DifferentiableFunction]
        :param inds: the shared coordinate indices (computed if omitted)
        :type inds: Sequence[int] | None
        """
        if inds is None:
            inds, funcs = self.get_consistent_inds([outer_func] + list(inner_funcs))
            outer_func, inner_funcs = funcs[0], funcs[1:]
        super().__init__(inds=inds)
        self.outer_func = outer_func
        self.inner_funcs = list(inner_funcs)
    def evaluate(self, coords, order=0):
        """
        **LLM Docstring**

        Evaluate the composition, combining the inner and outer expansions via the
        chain rule (Faà di Bruno) to get the composed derivatives.

        :param coords: the coordinates
        :type coords: np.ndarray
        :param order: the highest derivative order
        :type order: int
        :return: the composed expansion tensors
        :rtype: list[np.ndarray]
        """
        inner_expansions = [
            f(coords, order=order)
            for f in self.inner_funcs
        ]
        inner_expansion = [
            np.array([e[i] for e in inner_expansions])
            for i in range(order+1)
        ]
        outer_expansion = self.outer_func(inner_expansion[0], order=order)

        if order > 0:
            derivs = nput.tensordot_deriv(
                inner_expansion[1:],
                outer_expansion[1:],
                order=order
            )
        else:
            derivs = []

        return outer_expansion[:1] + derivs
    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this composition.

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return [self.outer_func] + self.inner_funcs

class ReciprocalFunction(DifferentiableFunction):
    def __init__(self, func: DifferentiableFunction, inds=None):
        """
        **LLM Docstring**

        Wrap the reciprocal (`1 / func`) of a function.

        :param func: the wrapped function
        :type func: DifferentiableFunction
        :param inds: the coordinate indices (inherited from `func` if omitted)
        :type inds: Sequence[int] | None
        """
        if inds is None: inds = func.inds
        super().__init__(inds=inds)
        self.func = func

    def evaluate(self, coords, order=0) -> list[np.ndarray]:
        """
        **LLM Docstring**

        Evaluate the wrapped function and form the expansion of its reciprocal.

        :param coords: the coordinates
        :type coords: np.ndarray
        :param order: the highest derivative order
        :type order: int
        :return: the reciprocal expansion tensors
        :rtype: list[np.ndarray]
        """
        expansion = self.func(coords, order=order)
        return nput.scalarinv_deriv(expansion, order)

    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this reciprocal.

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return [self.func]

class PolynomialFunction(DifferentiableFunction):
    def __init__(self, taylor_poly:FunctionExpansion, inds=None):
        """
        **LLM Docstring**

        Wrap a `FunctionExpansion` (Taylor polynomial) as a differentiable function.

        :param taylor_poly: the backing expansion
        :type taylor_poly: FunctionExpansion
        :param inds: the coordinate indices this function acts on
        :type inds: Sequence[int] | None
        """
        super().__init__(inds=inds)
        self.poly = taylor_poly

    @classmethod
    def from_coefficients(cls,
                          coeffs,
                          center=None,
                          ref=0,
                          inds=None
                          ):
        """
        **LLM Docstring**

        Build a polynomial function from a coefficient tensor, an expansion center, and a
        reference value.

        :param coeffs: the coefficient tensors
        :param center: the expansion center
        :param ref: the reference (constant) value
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the polynomial function
        :rtype: PolynomialFunction
        """
        return cls(
            FunctionExpansion(coeffs, center=center, ref=ref),
            inds=inds
        )

    def evaluate(self, coords, order=0):
        """
        **LLM Docstring**

        Evaluate the backing polynomial's expansion at the given coordinates.

        :param coords: the coordinates
        :type coords: np.ndarray
        :param order: the highest derivative order
        :type order: int
        :return: the expansion tensors
        :rtype: list[np.ndarray]
        """
        return self.poly.expand(coords, order=order)
    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this polynomial (a leaf).

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return []

class UnivariateFunction(DifferentiableFunction):

    def __init__(self, term_generator, *, inds=None):
        """
        **LLM Docstring**

        Base for one-dimensional functions defined by a term generator that returns each
        derivative order.

        :param term_generator: the callable producing the `n`-th derivative
        :type term_generator: Callable
        :param inds: the coordinate index this function acts on
        :type inds: Sequence[int] | None
        """
        super().__init__(inds=inds)
        self.term_generator = term_generator
    def evaluate(self, coords, order=0) -> list[np.ndarray]:
        """
        **LLM Docstring**

        Evaluate the univariate function on the (single) coordinate, calling the term
        generator for each derivative order and inserting the appropriate trailing axes.

        :param coords: the coordinates (only the first component is used)
        :type coords: np.ndarray
        :param order: the highest derivative order
        :type order: int
        :return: the expansion tensors
        :rtype: list[np.ndarray]
        """
        nshared = len(coords.shape[:-1])
        coords = coords[..., 0]

        expansions = []
        for n in range(order+1):
            expansions.append(
                np.expand_dims(
                    self.term_generator(coords, order=n, previous_terms=expansions),
                    list(range(nshared, nshared+n))
                )
            )

        return expansions

class Poly1D(UnivariateFunction):
    def __init__(self, coeffs, ref, center, inds=None):
        """
        **LLM Docstring**

        A 1-D polynomial (in the displacement from a center) defined by its coefficients.

        :param coeffs: the polynomial coefficients (order 1 and up)
        :param ref: the constant reference value
        :param center: the expansion center
        :param inds: the coordinate index
        :type inds: Sequence[int] | None
        """
        super().__init__(self.evaluate_term, inds=inds)
        self.coeffs = coeffs
        self.center = center
        self.ref = ref

    @classmethod
    def fac_pow(cls, k, n):
        """
        **LLM Docstring**

        Compute the falling-factorial coefficient `(k+1)(k+2)...(k+n)` arising when
        differentiating a power `n` times.

        :param k: the base exponent offset
        :type k: int
        :param n: the number of derivatives
        :type n: int
        :return: the factorial product
        :rtype: int
        """
        return np.prod(np.arange(k+1, k+n+1))

    def evaluate_term(self, r, order=0, previous_terms=None):
        """
        **LLM Docstring**

        Evaluate the `order`-th derivative of the polynomial at displacement `r - center`.

        :param r: the coordinate value
        :type r: np.ndarray
        :param order: the derivative order
        :type order: int
        :param previous_terms: earlier terms (unused)
        :return: the term values
        :rtype: np.ndarray
        """
        disp = r - self.center
        n = order

        if order == 0:
            return self.ref + sum(
                d * ( disp**(k+1) )
                for k,d in enumerate(self.coeffs)
            )
        else:
            return sum(
                (self.fac_pow(k, n)*d) * ( disp**(k) )
                for k,d in enumerate(self.coeffs[n-1:])
            )
    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this polynomial (a leaf).

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return []

class MorseFunction(UnivariateFunction):
    def __init__(self, *, de, a, re, inds=None):
        """
        **LLM Docstring**

        A Morse oscillator potential `de * (1 - exp(-a (r - re)))^2`.

        :param de: the well depth
        :param a: the range parameter
        :param re: the equilibrium position
        :param inds: the coordinate index
        :type inds: Sequence[int] | None
        """
        super().__init__(self.evaluate_term, inds=inds)
        self.de = de
        self.a = a
        self.re = re

    @classmethod
    def from_anharmonicity(cls, w, wx, g, re, inds=None):
        """
        **LLM Docstring**

        Build a Morse function from spectroscopic constants (harmonic frequency,
        anharmonicity, and reduced-mass factor).

        :param w: the harmonic frequency
        :param wx: the anharmonicity constant
        :param g: the reduced-mass / kinetic factor
        :param re: the equilibrium position
        :param inds: the coordinate index
        :type inds: Sequence[int] | None
        :return: the Morse function
        :rtype: MorseFunction
        """
        wx = np.abs(wx)
        de = (w ** 2) / (4 * wx)
        a = np.sqrt(2 * wx / g)

        return cls(de=de, a=a, re=re, inds=inds)

    def evaluate_term(self, r, order=0, previous_terms=None):
        """
        **LLM Docstring**

        Evaluate the `order`-th derivative of the Morse potential at `r`.

        :param r: the coordinate value
        :type r: np.ndarray
        :param order: the derivative order
        :type order: int
        :param previous_terms: earlier terms (unused)
        :return: the term values
        :rtype: np.ndarray
        """
        de = self.de
        a = self.a
        re = self.re
        n = order

        if order == 0:
            return de*(1 - np.exp(-a*(r-re)))**2
        else:
            return (
                    ((-1) ** (n + 1) * 2 * a ** n * de)
                    * np.exp(-2 * a * (r - re))
                    * (np.exp(a * (r - re)) - (2 ** (n - 1)))
            )

    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this Morse function (a leaf).

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return []

class Sin(UnivariateFunction):
    def __init__(self, *, n=1, l=1, inds=None):
        """
        **LLM Docstring**

        A sine function `sin((n/l) r)`.

        :param n: the wavenumber-like numerator
        :param l: the length-like denominator
        :param inds: the coordinate index
        :type inds: Sequence[int] | None
        """
        super().__init__(self.evaluate_term, inds=inds)
        self.n = n
        self.l = l

    def evaluate_term(self, r, order=0, previous_terms=None):
        """
        **LLM Docstring**

        Evaluate the `order`-th derivative of the sine (using the phase-shift identity).

        :param r: the coordinate value
        :type r: np.ndarray
        :param order: the derivative order
        :type order: int
        :param previous_terms: earlier terms (unused)
        :return: the term values
        :rtype: np.ndarray
        """
        scaling = (self.n/self.l)
        return scaling ** (order) * np.sin(order*np.pi/2 + scaling * r)

    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this sine (a leaf).

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return []

class Cos(UnivariateFunction):
    def __init__(self, *, n=1, l=1, inds=None):
        """
        **LLM Docstring**

        A cosine function `cos((n/l) r)`.

        :param n: the wavenumber-like numerator
        :param l: the length-like denominator
        :param inds: the coordinate index
        :type inds: Sequence[int] | None
        """
        super().__init__(self.evaluate_term, inds=inds)
        self.n = n
        self.l = l

    def evaluate_term(self, r, order=0, previous_terms=None):
        """
        **LLM Docstring**

        Evaluate the `order`-th derivative of the cosine (using the phase-shift
        identity).

        :param r: the coordinate value
        :type r: np.ndarray
        :param order: the derivative order
        :type order: int
        :param previous_terms: earlier terms (unused)
        :return: the term values
        :rtype: np.ndarray
        """
        scaling = (self.n/self.l)
        return scaling ** (order) * np.cos(order*np.pi/2 + scaling * r)

    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this cosine (a leaf).

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return []

class Exp(UnivariateFunction):
    def __init__(self, *, s=1, inds=None):
        """
        **LLM Docstring**

        An exponential function `exp(s r)`.

        :param s: the exponential rate
        :param inds: the coordinate index
        :type inds: Sequence[int] | None
        """
        super().__init__(self.evaluate_term, inds=inds)
        self.s = s

    def evaluate_term(self, r, order=0, previous_terms=None):
        """
        **LLM Docstring**

        Evaluate the `order`-th derivative of the exponential (`s^order exp(s r)`).

        :param r: the coordinate value
        :type r: np.ndarray
        :param order: the derivative order
        :type order: int
        :param previous_terms: earlier terms (unused)
        :return: the term values
        :rtype: np.ndarray
        """
        return self.s ** (order) * np.exp(self.s * r)

    def get_children(self):
        """
        **LLM Docstring**

        Return the sub-functions of this exponential (a leaf).

        :return: the child functions
        :rtype: list[DifferentiableFunction]
        """
        return []

class CoordinateFunction:
    def __init__(self, conversion, expr:DifferentiableFunction):
        """
        **LLM Docstring**

        Compose a coordinate-system conversion with a differentiable expression, so the
        expression (defined in internal coordinates) can be evaluated on raw (e.g.
        Cartesian) inputs.

        :param conversion: the coordinate conversion (a callable or an internal-coordinate spec)
        :param expr: the expression in the converted coordinates
        :type expr: DifferentiableFunction
        """
        self.conversion, self.coordinate_conversion = self.canonicalize_conversion(conversion)
        self._conv = None
        self.expr = expr

    @classmethod
    def canonicalize_conversion(cls, conv):
        """
        **LLM Docstring**

        Normalize a conversion specification into `(canonical_spec, conversion_function)`,
        building an internal-coordinate conversion function when a coordinate spec is
        given.

        :param conv: the conversion (callable or internal-coordinate spec)
        :return: `(canonical_spec, conversion_function)`
        :rtype: tuple
        """
        if callable(conv):
            return conv, conv
        else:
            if nput.is_numeric(conv[0]):
                conv = [conv]
            canon = [coords.canonicalize_internal(c) for c in conv]
            return canon, nput.internal_conversion_function(canon)

    def __call__(self, coords, order=0, preconverted=False, reexpress=True):
        """
        **LLM Docstring**

        Evaluate the composed function: convert the input coordinates (to the requested
        order), evaluate the expression, and re-express its derivatives back in the input
        coordinates via the chain rule.

        :param coords: the input coordinates
        :type coords: np.ndarray
        :param order: the highest derivative order
        :type order: int
        :param preconverted: treat `coords` as already in the expression's coordinates
        :type preconverted: bool
        :param reexpress: re-express the derivatives in the input coordinates
        :type reexpress: bool
        :return: `(coordinate_expansion, expression_expansion)`
        :rtype: tuple
        """
        # subexprs that only map to some coordinated need to map correctly!
        # not sure how best to handle that though...
        if not preconverted:
            coord_expansion = self.coordinate_conversion(coords, order=0 if not reexpress else order)
        else:
            coord_expansion = [coords]
            reexpress = False
        base_expr = self.expr(coord_expansion[0], order=order)
        if reexpress:
            expansion_vals = base_expr[:1] + (
                nput.tensor_reexpand(coord_expansion[1:], base_expr[1:], order)
                    if order > 0 else
                []
            )
        else:
            expansion_vals = base_expr
        return coord_expansion, expansion_vals

    @classmethod
    def merge_conversion_functions(cls, conv_1, conv_2):
        """
        **LLM Docstring**

        Merge two coordinate-conversion specs into one, returning the reindexing that
        maps the second spec's coordinates onto the merged set.

        :param conv_1: the first conversion spec
        :param conv_2: the second conversion spec
        :return: `(reindexing_for_conv_2, merged_conversion)`
        :rtype: tuple
        :raises ValueError: if either conversion is a bare callable
        """
        if conv_1 is conv_2:
            return None, conv_1

        if callable(conv_1) or callable(conv_2):
            raise ValueError("can't manage merging callable conversions")

        c1_disp = set(conv_1)
        new_conv = conv_1 + [c for c in conv_2 if c not in c1_disp]
        reindexing = np.full(len(new_conv), -1)
        for n,c in enumerate(conv_2):
            i = new_conv.index(c)
            reindexing[i] = n
        return reindexing, new_conv

    def __add__(self, other):
        """
        **LLM Docstring**

        Add another coordinate function (merging their conversions and reindexing) or a
        constant.

        :param other: the addend
        :return: the sum coordinate function
        :rtype: CoordinateFunction
        """
        if isinstance(other, CoordinateFunction):
            reindexing, conv = self.merge_conversion_functions(self.conversion, other.conversion)
            return type(self)(
                conv,
                self.expr + other.expr.reindex(reindexing)
            )
        else:
            return type(self)(self.conversion, self.expr + other)
    def __radd__(self, other):
        """
        **LLM Docstring**

        Right addition, delegating to `__add__`.

        :param other: the addend
        :return: the sum coordinate function
        :rtype: CoordinateFunction
        """
        return self + other
    def __mul__(self, other):
        """
        **LLM Docstring**

        Multiply by another coordinate function (merging their conversions) or a
        constant.

        :param other: the multiplier
        :return: the product coordinate function
        :rtype: CoordinateFunction
        """
        if isinstance(other, CoordinateFunction):
            reindexing, conv = self.merge_conversion_functions(self.conversion, other.conversion)
            return type(self)(
                conv,
                self.expr * other.expr.reindex(reindexing)
            )
        else:
            return type(self)(self.conversion, self.expr * other)
    def __rmul__(self, other):
        """
        **LLM Docstring**

        Right multiplication, delegating to `__mul__`.

        :param other: the multiplier
        :return: the product coordinate function
        :rtype: CoordinateFunction
        """
        return self * other
    def __truediv__(self, other):
        """
        **LLM Docstring**

        Divide by another coordinate function (merging their conversions) or a constant.

        :param other: the divisor
        :return: the quotient coordinate function
        :rtype: CoordinateFunction
        """
        if isinstance(other, CoordinateFunction):
            reindexing, conv = self.merge_conversion_functions(self.conversion, other.conversion)
            return type(self)(
                conv,
                self.expr / other.expr.reindex(reindexing)
            )
        else:
            return type(self)(self.conversion, self.expr / other)
    def __rtruediv__(self, other):
        """
        **LLM Docstring**

        Right division (`other / self`).

        :param other: the numerator
        :return: the quotient coordinate function
        :rtype: CoordinateFunction
        """
        return 1/self * other
    def __neg__(self):
        """
        **LLM Docstring**

        Negate the coordinate function.

        :return: the negated coordinate function
        :rtype: CoordinateFunction
        """
        return type(self)(self.conversion, -self.expr)

    @classmethod
    def polynomial(cls, coord_spec, *, coeffs, center, ref):
        """
        **LLM Docstring**

        Build a coordinate function from a polynomial expression in the given
        coordinate(s) (1-D `Poly1D` or multi-D `PolynomialFunction`).

        :param coord_spec: the coordinate spec the polynomial acts on
        :param coeffs: the polynomial coefficients
        :param center: the expansion center
        :param ref: the reference value
        :return: the coordinate function
        :rtype: CoordinateFunction
        """
        if nput.is_numeric(coord_spec[0]):
            fun = Poly1D(
                [np.array([c]).flatten()[0] for c in coeffs],
                ref=np.array([ref]).flatten()[0],
                center=np.array([center]).flatten()[0],
                inds=[0]
            )
        else:
            fun = PolynomialFunction.from_coefficients(
                coeffs=coeffs,
                center=center,
                ref=ref,
                inds=list(range(len(coord_spec)))
            )
        return cls(coord_spec, fun)

    @classmethod
    def morse(cls, coord, *, re, a=None, de=None, w=None, wx=None, g=None):
        """
        **LLM Docstring**

        Build a coordinate function from a Morse potential in the given coordinate,
        either from explicit `(de, a)` or from spectroscopic constants.

        :param coord: the coordinate spec
        :param re: the equilibrium position
        :param a: the range parameter
        :param de: the well depth
        :param w: the harmonic frequency (alternative parametrization)
        :param wx: the anharmonicity constant
        :param g: the reduced-mass factor
        :return: the coordinate function
        :rtype: CoordinateFunction
        """
        if w is not None:
            fun = MorseFunction.from_anharmonicity(w=w, wx=wx, g=g, re=re, inds=[0])
        else:
            fun = MorseFunction(a=a, de=de, re=re, inds=[0])
        return cls([coord], fun)
    @classmethod
    def sin(cls, coord, *, n=1, l=1):
        """
        **LLM Docstring**

        Build a coordinate function from a sine in the given coordinate.

        :param coord: the coordinate spec
        :param n: the numerator parameter
        :param l: the denominator parameter
        :return: the coordinate function
        :rtype: CoordinateFunction
        """
        return cls([coord], Sin(n=n, l=l, inds=[0]))
    @classmethod
    def cos(cls, coord, *, n=1, l=1):
        """
        **LLM Docstring**

        Build a coordinate function from a cosine in the given coordinate.

        :param coord: the coordinate spec
        :param n: the numerator parameter
        :param l: the denominator parameter
        :return: the coordinate function
        :rtype: CoordinateFunction
        """
        return cls([coord], Cos(n=n, l=l, inds=[0]))
    @classmethod
    def exp(cls, coord, *, s=1):
        """
        **LLM Docstring**

        Build a coordinate function from an exponential in the given coordinate.

        :param coord: the coordinate spec
        :param s: the exponential rate
        :return: the coordinate function
        :rtype: CoordinateFunction
        """
        return cls([coord], Exp(s=s, inds=[0]))


# class SympyFunction(DifferentiableFunction):
#     def __init__(self, sympy_expr):
#         self.expr = sympy_expr
#         self.coords = ...

