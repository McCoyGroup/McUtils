import uuid
from .CommonCoordinateSystems import InternalCoordinateSystem, CartesianCoordinates3D
from .CoordinateSystemConverter import CoordinateSystemConverter
from ..Internals import InternalSpec
from ... import Numputils as nput
__all__ = ['GenericInternalCoordinateSystem', 'GenericInternalCoordinates', 'CartesianToGICSystemConverter', 'GICSystemToCartesianConverter']

class GenericInternalCoordinateSystem(InternalCoordinateSystem):
    """
    Represents ZMatrix coordinates generally
    """
    name = 'GenericInternals'

    def __init__(self, converter_options=None, dimension=(None,), coordinate_shape=(None,), angle_ordering='ijk', internal_spec=None, **opts):
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

    def _prep_spec(self):
        ...

    def pre_convert_to(self, system, opts=None):
        ...

    def pre_convert_from(self, system, opts=None):
        ...
GenericInternalCoordinates = GenericInternalCoordinateSystem()
GenericInternalCoordinates.__name__ = 'ZMatrixCoordinates'
GenericInternalCoordinates.__doc__ = 'Generic internals'

class CartesianToGICSystemConverter(CoordinateSystemConverter):
    """
    A converter class for going from Cartesian coordinates to internals coordinates
    """

    @property
    def types(self):
        ...

    def convert_many(self, coords, *, specs, order=0, masses=None, remove_translation_rotation=True, reference_coordinates=None, return_derivs=None, derivs=None, gradient_function=None, gradient_scaling=None, method='direct', internal_spec=None, **kw):
        """
        We'll implement this by having the ordering arg wrap around in coords?
        """
        ...

    def convert(self, coords, *, specs, order=0, **kw):
        ...

class GICSystemToCartesianConverter(CoordinateSystemConverter):
    """
    A converter class for going from Cartesian coordinates to internals coordinates
    """

    @property
    def types(self):
        ...

    def convert_many(self, coords, *, reference_coordinates, specs, order=0, masses=None, remove_translation_rotation=True, derivs=None, return_derivs=None, internal_spec=None, method='direct', transformations=None, **kw):
        """
        We'll implement this by having the ordering arg wrap around in coords?
        """
        ...

    def convert(self, coords, *, reference_coordinates, specs, order=0, **kw):
        ...
__converters__ = [CartesianToGICSystemConverter(), GICSystemToCartesianConverter()]