from .BaseSurface import *
import numpy as np
from collections import namedtuple
__all__ = ['Surface', 'MultiSurface']

class Surface:
    """
    This actually isn't a concrete implementation of BaseSurface.
    Instead it's a class that _dispatches_ to an implementation of BaseSurface to do its core evaluations (plus it does shape checking)
    """

    def __init__(self, data, dimension=None, base=None, **metadata):
        """

        :param data:
        :type data:
        :param dimension:
        :type dimension:
        :param base:
        :type base: None | Type[BaseSurface]
        :param metadata:
        :type metadata:
        """
        ...

    @property
    def data(self):
        """
        **LLM Docstring**

        The backing data of the dispatched base surface.

        :return: the surface data
        """
        ...

    def minimize(self, initial_guess=None, function_options=None, **opts):
        """
        Provides a uniform interface for minimization, basically just dispatching to the BaseSurface implementation if provided

        :param initial_guess: initial starting point for the minimization
        :type initial_guess: np.ndarray | None
        :param function_options:
        :type function_options: None | dict
        :param opts:
        :type opts:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def detect_base(cls, data, opts):
        """
        Infers what type of base surface works for the data that's passed in.
        It's _super_ roughly done so...yeah generally better to pass the base class you want explicitly.
        But in the absence of that we can do this ?_?

        Basic strategy:
            1. look for options that go with specific methods
            2. look at data structures to guess
                i.   gradient as the first data arg + all data args are ndarrays -> Taylor Series
                ii.  callables as second arg -> Linear expansion or Linear fit
                iii. just like...one big array -> Interpolatin

        :param data:
        :type data: tuple
        :param opts:
        :type opts: dict
        :return:
        :rtype:
        """
        ...

    def __call__(self, gridpoints, **kwargs):
        """
        **LLM Docstring**

        Evaluate the surface at the given grid points (dispatching to the base surface).

        :param gridpoints: the points to evaluate at
        :type gridpoints: np.ndarray
        :param kwargs: extra evaluation options
        :return: the surface values
        :rtype: np.ndarray
        """
        ...

    @property
    def center(self):
        """
        **LLM Docstring**

        The expansion center of the base surface (if it has one).

        :return: the center
        """
        ...

    @property
    def ref(self):
        """
        **LLM Docstring**

        The reference value of the base surface (if it has one).

        :return: the reference value
        """
        ...

    @property
    def expansion_tensors(self):
        """
        **LLM Docstring**

        The expansion tensors of the base surface (if it has them).

        :return: the expansion tensors
        """
        ...

class MultiSurface:
    """
    A _reallly_ simple extension to the Surface infrastructure to handle vector valued functions,
    assuming each vector value corresponds to a different Surfaces
    """

    def __init__(self, *surfs):
        """

        :param surfs: a set of Surface objects to use when evaluating
        :type surfs: Iterable[Surface]
        """
        ...

    def __call__(self, gridpoints, order=None, **kwargs):
        """
        **LLM Docstring**

        Evaluate every component surface at the grid points, stacking the results (per
        derivative order when `order` is given).

        :param gridpoints: the points to evaluate at
        :type gridpoints: np.ndarray
        :param order: the derivative order to request from each surface
        :type order: int | None
        :param kwargs: extra evaluation options
        :return: the stacked per-surface values
        :rtype: np.ndarray | list
        """
        ...