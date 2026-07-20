import numpy as np
from ... import Devutils as dev
from ... import Numputils as nput
from .CoordinateSystemConverter import CoordinateSystemConverters as converters, CoordinateSystemConverter
from .CoordinateUtils import is_multiconfig, mc_safe_apply
__all__ = ['CoordinateSystem', 'BaseCoordinateSystem', 'CoordinateSystemError']
__reload_hook__ = ['.CoordinateSystemConverter', '.CoordinateUtils']

class CoordinateSystem:
    """A representation of a coordinate system. It doesn't do much on its own but it *does* provide a way
    to unify internal, cartesian, derived type coordinates

    """

    def __init__(self, name=None, basis=None, matrix=None, inverse=None, dimension=None, origin=None, coordinate_shape=None, jacobian_prep=None, converter_options=None, registered_converters=None, **extra):
        """
        Sets up the CoordinateSystem object

        :param name: a name to give to the coordinate system
        :type name: str
        :param basis: a basis for the coordinate system
        :type basis:
        :param matrix: an expansion coefficient matrix for the set of coordinates in its basis
        :type matrix: np.ndarray | None
        :param dimension: the dimension of a single configuration in the coordinate system (for validation)
        :type dimension: Iterable[None | int]
        :param jacobian_prep: a function for preparing coordinates to be used in computing the Jacobian
        :type jacobian_prep: function | None
        :param coordinate_shape: the actual shape of a single coordinate in the coordinate system
        :type coordinate_shape: iterable[int]
        """
        ...

    def to_state(self, serializer=None):
        ...

    @classmethod
    def from_state(cls, data, serializer=None):
        ...

    def __call__(self, coords, **opts):
        ...

    def pre_convert(self, system):
        """
        [DEPRECATED, see `pre_convert_to` and `pre_convert_from`]
        A hook to allow for handlign details before converting
        :param system:
        :type system:
        :return:
        :rtype:
        """
        ...

    def pre_convert_to(self, system, opts=None):
        ...

    def pre_convert_from(self, system, opts=None):
        ...

    def _validate(self):
        ...

    @property
    def basis(self):
        """
        :return: The basis for the representation of `matrix`
        :rtype: CoordinateSystem
        """
        ...

    @property
    def origin(self):
        """
        :return: The origin for the expansion defined by `matrix`
        :rtype: np.ndarray
        """
        ...

    @origin.setter
    def origin(self, orig):
        ...

    @property
    def matrix(self):
        """
        The matrix representation in the `CoordinateSystem.basis`
        `None` is shorthand for the identity matrix

        :return: mat
        :rtype:  np.ndarray
        """
        ...

    @matrix.setter
    def matrix(self, mat):
        ...

    @property
    def inverse(self):
        """
        The inverse of the representation in the `basis`.
        `None` is shorthand for the inverse or pseudoinverse of `matrix`.

        :return: inv
        :rtype:  np.ndarray
        """
        ...

    @inverse.setter
    def inverse(self, mat):
        ...

    @property
    def dimension(self):
        """
        The dimension of the coordinate system.
        `None` means unspecified dimension

        :return: dim
        :rtype: int or None
        """
        ...

    def register_converter(self, system, conversion):
        ...

    def get_direct_converter(self, target):
        ...

    def get_inverse_converter(self, target):
        ...

    def preregister_converters(self):
        ...

    def deregister_converters(self):
        ...

    def converter(self, system):
        """
        Gets the converter from the current system to a new system

        :param system: the target CoordinateSystem
        :type system: CoordinateSystem
        :return: converter object
        :rtype: CoordinateSystemConverter
        """
        ...

    @staticmethod
    def _apply_system_matrix(basis, coords, matrix, input_coordinate_shape, target_coordinate_shape):
        ...

    class _convert_caller:

        def __init__(self, converter, kw, do_many):
            ...

        def __call__(self, coords, *args, **kwargs):
            ...

    def convert_coords(self, coords, system, converter=None, apply_pre_converter=False, **kw):
        """
        Converts coordiantes from the current coordinate system to _system_

        :param coords:
        :type coords: CoordinateSet
        :param system:
        :type system: CoordinateSystem
        :param kw: options to be passed through to the converter object
        :type kw:
        :return: the converted coordiantes
        :rtype: tuple(np.ndarray, dict)
        """
        ...

    def rescale(self, scaling, in_place=False):
        ...

    def rotate(self, rot, in_place=False):
        ...

    def displacement(self, amts):
        """
        Generates a displacement or matrix of displacements based on the vector or matrix amts
        The relevance of this method has become somewhat unclear...

        :param amts:
        :type amts: np.ndarray
        :return:
        :rtype: np.ndarray
        """
        ...

    def derivatives(self, coords, function, order=1, coordinates=None, result_shape=None, **finite_difference_options):
        """
        Computes derivatives for an arbitrary function with respect to this coordinate system.
        Basically a more flexible version of `jacobian`.

        :param function:
        :type function:
        :param order:
        :type order:
        :param coordinates:
        :type coordinates:
        :param finite_difference_options:
        :type finite_difference_options:
        :return: derivative tensor
        :rtype: np.ndarray
        """
        ...

    class _converter:

        def __init__(self, system, deriv_key, parent, num_derivs, convert_kwargs):
            ...

        def __call__(self, c, *args, **kwargs):
            ...
    return_derivs_key = 'return_derivs'
    deriv_key = 'derivs'

    def jacobian(self, coords, system, order=1, coordinates=None, converter_options=None, all_numerical=False, analytic_deriv_order=None, allow_fd=True, **finite_difference_options):
        """
        Computes the Jacobian between the current coordinate system and a target coordinate system

        :param system: the target CoordinateSystem
        :type system: CoordinateSystem
        :param order: the order of the Jacobian to compute, 1 for a standard, 2 for the Hessian, etc.
        :type order: int | Iterable[int]
        :param coordinates: a spec of which coordinates to generate derivatives for (None means all)
        :type coordinates: None | iterable[iterable[int] | None
        :param mesh_spacing: the spacing to use when displacing
        :type mesh_spacing: float | np.ndarray
        :param prep: a function for pre-validating the generated coordinate values and grids
        :type prep: None | function
        :param fd_options: options to be passed straight through to FiniteDifferenceFunction
        :type fd_options:
        :return: derivative tensor
        :rtype: np.ndarray
        """
        ...

    def __repr__(self):
        """
        Provides a clean representation of a `CoordinateSystem` for printing
        :return:
        :rtype: str
        """
        ...

    @classmethod
    def is_compatible(cls, self, system):
        ...

    def has_conversion(self, system):
        ...

class CoordinateSystemError(Exception):
    """
    An exception that happens inside a `CoordinateSystem` method
    """

class BaseCoordinateSystem(CoordinateSystem):
    """
    A CoordinateSystem object that can't be reduced further.
    A common choice might be Cartesian coordinates or internal coordinates.
    This allows us to define flexible `CoordinateSystem` subclasses that we _don't_ expect to be used as a base
    """

    def __init__(self, name, dimension=None, coordinate_shape=None, converter_options=None):
        ...

    def to_state(self, serializer=None):
        ...

    @classmethod
    def from_state(cls, data, serializer=None):
        ...