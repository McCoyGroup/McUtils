import uuid
import numpy as np
from .CommonCoordinateSystems import InternalCoordinateSystem, CartesianCoordinates3D, ZMatrixCoordinateSystem, ZMatrixCoordinates
from .CoordinateSystemConverter import CoordinateSystemConverter
from .ZMatrixToCartesian import ZMatrixToCartesianConverter
from .CartesianToZMatrix import CartesianToZMatrixConverter
from ... import Numputils as nput
__all__ = ['IterativeZMatrixCoordinateSystem', 'IterativeZMatrixCoordinates', 'CartesianToIZSystemConverter', 'IZSystemToCartesianConverter']

class IterativeZMatrixCoordinateSystem(ZMatrixCoordinateSystem):
    """
    Represents ZMatrix coordinates generally
    """
    name = 'IterativeZMatrix'

    def __init__(self, converter_options=None, dimension=(None, None), coordinate_shape=(None, 3), **opts):
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
IterativeZMatrixCoordinates = IterativeZMatrixCoordinateSystem()
IterativeZMatrixCoordinates.__name__ = 'IterativeZMatrixCoordinates'
IterativeZMatrixCoordinates.__doc__ = 'Iterative Z-matrix internals'

class CartesianToIZSystemConverter(CartesianToZMatrixConverter):
    """
    A converter class for going from Cartesian coordinates to internals coordinates
    """

    @property
    def types(self):
        ...

    def convert_many(self, coords, *, ordering, use_rad=True, return_derivs=False, **kw):
        ...

class IZSystemToCartesianConverter(CoordinateSystemConverter):
    """
    A converter class for going from Cartesian coordinates to internals coordinates
    """

    @property
    def types(self):
        ...

    def convert_many(self, coords, *, reference_coordinates, order=0, masses=None, remove_translation_rotation=True, derivs=None, return_derivs=None, ordering=None, origins=None, axes=None, embedding_coords=None, jacobian_prep=None, axes_labels=None, fixed_atoms=None, use_rad=True, **kw):
        """
        We'll implement this by having the ordering arg wrap around in coords?
        """
        ...

    def convert(self, coords, *, reference_coordinates, specs, order=0, **kw):
        ...
__converters__ = [CartesianToIZSystemConverter(), IZSystemToCartesianConverter()]