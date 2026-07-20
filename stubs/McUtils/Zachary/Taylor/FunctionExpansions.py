from ..LazyTensors import Tensor
from .Derivatives import FiniteDifferenceDerivative
from ...Coordinerds import CoordinateSet, CoordinateSystem
from ... import Numputils as nput
import numpy as np, itertools, copy, math
__all__ = ['FunctionExpansion']

class TaylorPoly:
    """
    A handler for dealing with multidimensional polynomials

    Can be used to handle multiple polynomials simultaneously, but requires
    that all expansions are provided up to the same order.
    """

    def __init__(self, derivatives, transforms=None, transformed_derivatives=False, center=None, ref=None, weight_coefficients=False):
        """
        :param derivatives: Derivatives of the function being expanded
        :type derivatives: Iterable[np.ndarray | Tensor]
        :param transforms: Jacobian and higher order derivatives in the coordinates
        :type transforms: Iterable[np.ndarray | Tensor] | None
        :param center: the reference point for expanding aobut
        :type center: np.ndarray | None
        :param ref: the reference point value for shifting the expansion
        :type ref: float | np.ndarray
        :param weight_coefficients: whether the derivative terms need to be weighted or not
        :type weight_coefficients: bool
        """
        ...

    @property
    def center(self):
        """
        **LLM Docstring**

        The expansion center.

        :return: the center
        :rtype: np.ndarray
        """
        ...

    @property
    def is_multi(self):
        """
        **LLM Docstring**

        Whether this is a stacked (multi-function) expansion.

        :return: whether the expansion is stacked
        :rtype: bool
        """
        ...

    @classmethod
    def multipolynomial(cls, *expansions):
        """
        **LLM Docstring**

        Build a single stacked expansion from several separate expansions, stacking their
        per-order tensors, centers, and reference values.

        :param expansions: the component expansions
        :type expansions: TaylorPoly
        :return: the stacked expansion
        :rtype: TaylorPoly
        """
        ...

    @classmethod
    def canonicalize_tfs(cls, tfs):
        """
        **LLM Docstring**

        Normalize a coordinate-transform specification into `(forward_tensors,
        inverse_tensors)`, detecting whether an inverse set was supplied.

        :param tfs: the transform tensors (forward, or forward+inverse)
        :return: `(forward_tensors, inverse_tensors_or_None)`
        :rtype: tuple
        """
        ...

    @property
    def transforms(self):
        """
        **LLM Docstring**

        The coordinate-transform tensors (forward, and inverse if present), or `None`
        when the expansion has no transform.

        :return: the transform tensors
        :rtype: list | None
        """
        ...

    @property
    def expansion_tensors(self):
        """
        Provides the tensors that will contracted

        :return:
        :rtype: Iterable[np.ndarray]
        """
        ...

    @expansion_tensors.setter
    def expansion_tensors(self, tensors):
        """
        Are we going to assume in setting the tensors that
        people have done any requisite coordinate transformations?

        -> I think that's leaving room open for nasty surprises since we have
        the `_transf_ member
        -> but the `expansion_tensors` are in general expected to ... be transformed?

        Which means that we need _two_ properties 1) these tensors and 2) the derivs
        neither of which is transformed when being set
        """
        ...

    @property
    def derivative_tensors(self):
        """
        Provides the base derivative tensors
        independent of any coordinate transformations

        :return:
        :rtype: Iterable[np.ndarray]
        """
        ...

    @derivative_tensors.setter
    def derivative_tensors(self, derivs):
        """
        **LLM Docstring**

        Set the expansion's derivative tensors.

        :param derivs: the per-order derivative tensors
        :type derivs: list
        """
        ...

    def get_expansions(self, coords, transform_displacements=True, subexpansions=None, outer=True, order=None, squeeze=None):
        """

        :param coords: Coordinates to evaluate the expansion at
        :type coords: np.ndarray | CoordinateSet
        :param subexpansions: A set of tensor expansion indices to use if we have a multiexpansion
        but only want some subset of the relevant points
        :type subexpansions: int | Iterable[int]
        :return:
        :rtype:
        """
        ...

    def expand(self, coords, order=None, outer=True, transform_displacements=True, squeeze=True):
        """Returns a numerical value for the expanded coordinates

        :param coords:
        :type coords: np.ndarray
        :return:
        :rtype: float | np.ndarray
        """
        ...

    def __call__(self, coords, **kw):
        """
        **LLM Docstring**

        Evaluate the expansion at the given coordinates (delegates to `expand`).

        :param coords: the query coordinates
        :type coords: np.ndarray
        :param kw: extra options for `expand`
        :return: the expansion values
        :rtype: np.ndarray
        """
        ...

    class CoordinateTransforms:

        def __init__(self, transforms):
            """
            **LLM Docstring**

            Hold the per-order coordinate-transform tensors.

            :param transforms: the transform tensors
            :type transforms: list
            """
            ...

        def __getitem__(self, i):
            """
            **LLM Docstring**

            Return the transform tensor for the requested order.

            :param i: the order
            :type i: int
            :return: the transform tensor
            :rtype: np.ndarray
            :raises FunctionExpansionException: if the order exceeds what was provided
            """
            ...

        def __len__(self):
            """
            **LLM Docstring**

            The number of transform orders provided.

            :return: the number of orders
            :rtype: int
            """
            ...

    class FunctionDerivatives:

        def __init__(self, derivs, weight_coefficients=True):
            """
            **LLM Docstring**

            Hold the per-order function-derivative tensors, optionally weighting them by the
            Taylor coefficients (`1/n!` and permutation factors).

            :param derivs: the per-order derivative tensors
            :type derivs: list
            :param weight_coefficients: apply the Taylor coefficient weighting
            :type weight_coefficients: bool
            """
            ...

        def weight_derivs(self, t, order=None):
            """

            :param order:
            :type order: int
            :param t:
            :type t: Tensor
            :return:
            :rtype:
            """
            ...

        def __getitem__(self, i):
            """
            **LLM Docstring**

            Return the derivative tensor for the requested order.

            :param i: the order
            :type i: int
            :return: the derivative tensor
            :rtype: np.ndarray
            :raises FunctionExpansionException: if the order exceeds what was provided
            """
            ...

        def __len__(self):
            """
            **LLM Docstring**

            The number of derivative orders provided.

            :return: the number of orders
            :rtype: int
            """
            ...

    def deriv(self, which=None):
        """
        Computes the derivative(s) of the expansion(s) with respect to the
        supplied coordinates (`which=None` means compute the gradient)

        :param which:
        :type which:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def from_indices(cls, inds, ref=0, expansion_order=None, ndim=None, symmetrize=True, **opts):
        """
        **LLM Docstring**

        Build an expansion from a sparse set of `(index_tuple, value)` derivative
        entries, inferring the dimension and order and (by default) symmetrizing each
        tensor over its index permutations.

        :param inds: the derivative entries (a mapping or iterable of `(index, value)`)
        :type inds: dict | Iterable
        :param ref: the reference (zeroth-order) value
        :param expansion_order: the highest derivative order (inferred if omitted)
        :type expansion_order: int | None
        :param ndim: the coordinate dimension (inferred if omitted)
        :type ndim: int | None
        :param symmetrize: fill all index permutations of each entry
        :type symmetrize: bool
        :param opts: extra options forwarded to the constructor
        :return: the expansion
        :rtype: TaylorPoly
        """
        ...

    def _build_binomial_inds(self, g_partitions, w_partitions):
        """
        An unnecessarily efficient algorithm to get the set
        pairs of indices into the integer partitions of `g` and `w`
        plus an optional permutation of `g` which will lead to non-zero
        terms when the product of the pairwise binomial terms is computed


        :param g_partitions:
        :type g_partitions:
        :param w_partitions:
        :type w_partitions:
        :return:
        :rtype:
        """
        ...

    def shift(self, new_origin):
        """
        Uses binomial expansion to new polynomial centered at the `new_origin`

        :param new_origin:
        :type new_origin:
        :return:
        :rtype:
        """
        ...

class FunctionExpansionException(Exception):
    ...

class FunctionExpansion(TaylorPoly):
    """
    Specifically for expanding functions
    """

    @classmethod
    def expand_function(cls, f, point, order=4, basis=None, function_shape=None, transforms=None, weight_coefficients=True, **fd_options):
        """
        Expands a function about a point up to the given order

        :param f:
        :type f: function
        :param point:
        :type point: np.ndarray | CoordinateSet
        :param order:
        :type order: int
        :param basis:
        :type basis: None | CoordinateSystem
        :param fd_options:
        :type fd_options:
        :return:
        :rtype:
        """
        ...