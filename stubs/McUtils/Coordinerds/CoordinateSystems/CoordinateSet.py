"""
Provides a CoordinateSet class that acts as a symbolic extension of np.ndarray to provide an explicit basis
"""
import numpy as np
from .CoordinateSystem import CoordinateSystem, CoordinateSystemError
from .CommonCoordinateSystems import CartesianCoordinates3D
from .CoordinateUtils import is_multiconfig
__all__ = ['CoordinateSet']
__reload_hook__ = ['.CoordinateSystem', '.CommonCoordinateSystems', '.CoordinateUtils']

class CoordinateSet(np.ndarray):
    """
    A subclass of np.ndarray that lives in an explicit coordinate system and can convert between them
    """

    def __new__(cls, coords, system=CartesianCoordinates3D, converter_options=None):
        ...

    def __init__(self, coords, system=CartesianCoordinates3D, converter_options=None):
        ...

    def __array_finalize__(self, coords):
        ...

    def to_state(self, serializer=None):
        ...

    @classmethod
    def from_state(cls, data, serializer=None):
        ...

    def _validate(self):
        ...

    def __str__(self):
        ...

    def __eq__(self, other):
        ...

    @property
    def multiconfig(self):
        """Determines whether self.coords represents multiple configurations of the coordinates

        :return:
        :rtype:
        """
        ...

    def transform(self, tf):
        """Applies a transformation to the stored coordinates

        :param tf: the transformation function to apply to the system
        :type tf:
        :return:
        :rtype:
        """
        ...

    def convert(self, system, **kw):
        """Converts across coordinate systems

        :param system: the target coordinate system
        :type system: CoordinateSystem
        :return: new_coords
        :rtype: CoordinateSet
        """
        ...

    def derivatives(self, function, order=1, coordinates=None, result_shape=None, **fd_options):
        """
        Takes derivatives of `function` with respect to the current geometry

        :param function:
        :type function:
        :param order:
        :type order:
        :param coordinates:
        :type coordinates:
        :param fd_options:
        :type fd_options:
        :return:
        :rtype:
        """
        ...

    def jacobian(self, system, order=1, coordinates=None, converter_options=None, all_numerical=False, analytic_deriv_order=None, **fd_options):
        """
        Delegates to the jacobian function of the current coordinate system.


        :param system:
        :type system:
        :param order:
        :type order:
        :param mesh_spacing:
        :type mesh_spacing:
        :param prep:
        :type prep:
        :param coordinates:
        :type coordinates:
        :param fd_options:
        :type fd_options:
        :return:
        :rtype:
        """
        ...