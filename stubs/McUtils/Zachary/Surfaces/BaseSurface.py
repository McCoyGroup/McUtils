"""
Provides an abstract base class off of which concrete surface implementations can be built
"""
import abc, numpy as np
from ... import Numputils as nput
__all__ = ['BaseSurface', 'TaylorSeriesSurface', 'InterpolatedSurface']

class BaseSurface(metaclass=abc.ABCMeta):
    """
    Surface base class which can be subclassed for relevant cases
    """

    def __init__(self, data, dimension):
        """
        **LLM Docstring**

        Store the core surface data and its dimension.

        :param data: the surface's backing data (interpreted by the subclass)
        :param dimension: the dimensionality of the surface's input space
        :type dimension: int | None
        """
        ...

    @abc.abstractmethod
    def evaluate(self, points, **kwargs):
        """
        Evaluates the function at the points based off of "data"

        :param points:
        :type points:
        :return:
        :rtype:
        """
        ...

    def check_dimension(self, gridpoints, target=None, raise_exception=True):
        """
        **LLM Docstring**

        Check that a set of grid points matches the surface's expected dimension,
        optionally raising on a mismatch.

        :param gridpoints: the points to check
        :type gridpoints: np.ndarray
        :param target: the expected dimension (defaults to the surface's)
        :type target: int | None
        :param raise_exception: raise (rather than return `False`) on a mismatch
        :type raise_exception: bool
        :return: whether the dimension matches
        :rtype: bool
        :raises ValueError: on a mismatch when `raise_exception` is set
        """
        ...

    def __call__(self, gridpoints, **kwargs):
        """

        :param gridpoints:
        :type gridpoints: np.ndarray
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

class TaylorSeriesSurface(BaseSurface):
    """
    A surface with an evaluator built off of a Taylor series expansion
    """

    def __init__(self, *derivs, dimension=None, **opts):
        """
        :param data: derivs or a tuple of derivs + options
        :type data:
        :param dimension:
        :type dimension:
        """
        ...

    @property
    def center(self):
        """
        **LLM Docstring**

        The expansion center of the underlying Taylor series.

        :return: the center
        :rtype: np.ndarray
        """
        ...

    @property
    def ref(self):
        """
        **LLM Docstring**

        The reference (constant) value of the underlying Taylor series.

        :return: the reference value
        """
        ...

    @property
    def expansion_tensors(self):
        """
        **LLM Docstring**

        The derivative tensors of the underlying Taylor series.

        :return: the expansion tensors
        :rtype: list
        """
        ...

    def check_dimension(self, gridpoints, target=None, raise_exception=True):
        """
        **LLM Docstring**

        Check the grid-point dimension, additionally accepting either side of the
        expansion's coordinate transform when one is present.

        :param gridpoints: the points to check
        :type gridpoints: np.ndarray
        :param target: an explicit expected dimension
        :type target: int | None
        :param raise_exception: raise on a mismatch
        :type raise_exception: bool
        :return: whether the dimension matches
        :rtype: bool
        """
        ...

    def evaluate(self, points, **kwargs):
        """
        Since the Taylor expansion stuff is already built out this is super easy

        :param points:
        :type points:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

class LinearExpansionSurface(BaseSurface):
    """
    A surface with an evaluator built off of an expansion in some user specified basis
    """

    def __init__(self, coefficients, basis=None, dimension=None):
        """
        :param coefficients: the expansion coefficients in the basis
        :type coefficients: np.ndarray
        :param basis: a basis of functions to use (defaults to power series)
        :type basis: Iterable[function] | None
        """
        ...

    def evaluate(self, points, **kwargs):
        """
        First we just apply the basis to the gridpoints, then we dot this into the coeffs

        :param points:
        :type points:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

class LinearFitSurface(LinearExpansionSurface):
    """
    A surface built off of a LinearExpansionSurface, but done by fitting.
    The basis selection
    """

    def __init__(self, points, basis=None, order=4, dimension=None):
        """
        :param points: a set of points to fit to
        :type points: np.ndarray
        :param basis: a basis of functions to use (defaults to power series)
        :type basis: Iterable[function] | None
        """
        ...

    def evaluate(self, points, **kwargs):
        """

        :param points:
        :type points:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def minimize(self, initial_guess=None, function_options=None, **opts):
        """
        **LLM Docstring**

        Minimize the fitted surface, defaulting the starting point to the lowest-valued
        fit sample.

        :param initial_guess: the starting point (defaults to the best fit sample)
        :type initial_guess: np.ndarray | None
        :param function_options: options forwarded to the surface evaluation
        :type function_options: dict | None
        :param opts: options forwarded to the optimizer
        :return: the minimizing point
        :rtype: np.ndarray
        """
        ...

class InterpolatedSurface(BaseSurface):
    """
    A surface that operates by doing an interpolation of passed mesh data
    """

    def __init__(self, xdata, ydata=None, dimension=None, **opts):
        """
        **LLM Docstring**

        Build a surface that evaluates by interpolating supplied mesh data.

        When only `xdata` is given, its last column is taken as the values.

        :param xdata: the sample points (or points-plus-values)
        :type xdata: np.ndarray
        :param ydata: the sample values
        :type ydata: np.ndarray | None
        :param dimension: the input dimensionality (inferred from `xdata`)
        :type dimension: int | None
        :param opts: options forwarded to the interpolator
        """
        ...

    def evaluate(self, points, **kwargs):
        """
        We delegate all the dirty work to the Interpolator so hopefully that's working...
        :param points:
        :type points:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def minimize(self, initial_guess=None, function_options=None, **opts):
        """
        **LLM Docstring**

        Minimize the interpolated surface, defaulting the starting point to the
        lowest-valued sample.

        :param initial_guess: the starting point (defaults to the best sample)
        :type initial_guess: np.ndarray | None
        :param function_options: options forwarded to the surface evaluation
        :type function_options: dict | None
        :param opts: options forwarded to the optimizer
        :return: the minimizing point
        :rtype: np.ndarray
        """
        ...