import numpy as np
from .CoordinateSystem import BaseCoordinateSystem
from ... import Numputils as nput
__all__ = ['CartesianCoordinateSystem', 'InternalCoordinateSystem', 'CartesianCoordinateSystem3D', 'CartesianCoordinates3D', 'CartesianCoordinates1D', 'CartesianCoordinates2D', 'SphericalCoordinateSystem', 'SphericalCoordinates', 'ZMatrixCoordinateSystem', 'ZMatrixCoordinates']

class CartesianCoordinateSystem(BaseCoordinateSystem):
    """
    Represents Cartesian coordinates generally
    """
    name = 'Cartesian'

    def __init__(self, dimension=None, converter_options=None, coordinate_shape=None, **opts):
        """
        :param converter_options: options to be passed through to a `CoordinateSystemConverter`
        :type converter_options: None | dict
        :param dimension: the dimension of the coordinate system
        :type dimension: Iterable[None | int]
        :param opts: other options, if `converter_options` is None, these are used as the `converter_options`
        :type opts:
        """
        ...

    @classmethod
    def from_state(cls, data, serializer=None):
        ...

class InternalCoordinateSystem(BaseCoordinateSystem):
    """
    Represents Internal coordinates generally
    """
    name = 'Internal'

    def __init__(self, dimension=None, coordinate_shape=None, converter_options=None, **opts):
        """
        :param converter_options: options to be passed through to a `CoordinateSystemConverter`
        :type converter_options: None | dict
        :param coordinate_shape: shape of a single coordinate in this coordiante system
        :type coordinate_shape: Iterable[None | int]
        :param dimension: the dimension of the coordinate system
        :type dimension: Iterable[None | int]
        :param opts: other options, if `converter_options` is None, these are used as the `converter_options`
        :type opts:
        """
        ...

    @classmethod
    def from_state(cls, data, serializer=None):
        ...

class CartesianCoordinateSystem1D(CartesianCoordinateSystem):
    """
    Represents Cartesian coordinates in 1D
    """
    name = 'Cartesian1D'

    def __init__(self, converter_options=None, dimension=(None, 1), **opts):
        """
        :param converter_options: options to be passed through to a `CoordinateSystemConverter`
        :type converter_options: None | dict
        :param dimension: the dimension of the coordinate system
        :type dimension: Iterable[None | int]
        :param opts: other options, if `converter_options` is None, these are used as the `converter_options`
        :type opts:
        """
        ...
CartesianCoordinates1D = CartesianCoordinateSystem1D()
CartesianCoordinates1D.__name__ = 'CartesianCoordinates1D'
CartesianCoordinates1D.__doc__ = '\n    A concrete instance of `CartesianCoordinateSystem3D`\n    '

class CartesianCoordinateSystem2D(CartesianCoordinateSystem):
    """
    Represents Cartesian coordinates in 2D
    """
    name = 'Cartesian2D'

    def __init__(self, converter_options=None, dimension=(None, 2), **opts):
        """
        :param converter_options: options to be passed through to a `CoordinateSystemConverter`
        :type converter_options: None | dict
        :param dimension: the dimension of the coordinate system
        :type dimension: Iterable[None | int]
        :param opts: other options, if `converter_options` is None, these are used as the `converter_options`
        :type opts:
        """
        ...
CartesianCoordinates2D = CartesianCoordinateSystem2D()
CartesianCoordinates2D.__name__ = 'CartesianCoordinates2D'
CartesianCoordinates2D.__doc__ = '\n    A concrete instance of `CartesianCoordinateSystem3D`\n    '

class CartesianCoordinateSystem3D(CartesianCoordinateSystem):
    """
    Represents Cartesian coordinates in 3D
    """
    name = 'Cartesian3D'

    def __init__(self, converter_options=None, dimension=(None, 3), **opts):
        """
        :param converter_options: options to be passed through to a `CoordinateSystemConverter`
        :type converter_options: None | dict
        :param dimension: the dimension of the coordinate system
        :type dimension: Iterable[None | int]
        :param opts: other options, if `converter_options` is None, these are used as the `converter_options`
        :type opts:
        """
        ...
CartesianCoordinates3D = CartesianCoordinateSystem3D()
CartesianCoordinates3D.__name__ = 'CartesianCoordinates3D'
CartesianCoordinates3D.__doc__ = '\n    A concrete instance of `CartesianCoordinateSystem3D`\n    '

class ZMatrixCoordinateSystem(InternalCoordinateSystem):
    """
    Represents ZMatrix coordinates generally
    """
    name = 'ZMatrix'

    def __init__(self, converter_options=None, dimension=(None, None), coordinate_shape=(None, 3), spec=None, **opts):
        """
        :param converter_options: options to be passed through to a `CoordinateSystemConverter`
        :type converter_options: None | dict
        :param coordinate_shape: shape of a single coordinate in this coordiante system
        :type coordinate_shape: Iterable[None | int]
        :param dimension: the dimension of the coordinate system
        :type dimension: Iterable[None | int]
        :param opts: other options, if `converter_options` is None, these are used as the `converter_options`
        :type opts:
        """
        ...

    @staticmethod
    def jacobian_prep_coordinates(coord, displacements, values, dihedral_cutoff=6):
        ...

    def to_state(self, serializer=None):
        ...

    @classmethod
    def canonicalize_order_list(self, ncoords, order_list):
        """
        Normalizes the way the ZMatrix coordinates are built out

        :param ncoords:
        :type ncoords:
        :param order_list: the basic ordering to apply for the
        :type order_list: iterable or None
        :return:
        :rtype: iterator of int triples
        """
        ...

    @classmethod
    def tile_order_list(self, ol, ncoords):
        ...

    @property
    def ordering(self):
        ...

    def _prep_spec(self, ordering=None):
        ...

    @property
    def spec(self):
        ...

    def pre_convert_to(self, system, opts=None):
        ...
ZMatrixCoordinates = ZMatrixCoordinateSystem()
ZMatrixCoordinates.__name__ = 'ZMatrixCoordinates'
ZMatrixCoordinates.__doc__ = '\n    A concrete instance of `ZMatrixCoordinateSystem`\n    '

class SphericalCoordinateSystem(BaseCoordinateSystem):
    """
    Represents Spherical coordinates generally
    """
    name = 'SphericalCoordinates'

    def __init__(self, converter_options=None, **opts):
        """
        :param converter_options: options to be passed through to a `CoordinateSystemConverter`
        :type converter_options: None | dict
        :param opts: other options, if `converter_options` is None, these are used as the `converter_options`
        :type opts:
        """
        ...
SphericalCoordinates = SphericalCoordinateSystem()
SphericalCoordinates.__name__ = 'SphericalCoordinates'
SphericalCoordinates.__doc__ = '\n    A concrete instance of `SphericalCoordinateSystem`\n    '