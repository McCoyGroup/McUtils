import uuid

from .CommonCoordinateSystems import InternalCoordinateSystem, CartesianCoordinates3D
from .CoordinateSystemConverter import CoordinateSystemConverter
from ... import Numputils as nput
# import weakref

__all__ = [
    "GenericInternalCoordinateSystem",
    "GenericInternalCoordinates",
    "CartesianToGICSystemConverter",
    "GICSystemToCartesianConverter"
]

#TODO: these should all be metaclasses but :shrag:
class GenericInternalCoordinateSystem(InternalCoordinateSystem):
    """
    Represents ZMatrix coordinates generally
    """
    name = "GenericInternals"
    def __init__(self,
                 converter_options=None,
                 dimension=(None,),
                 coordinate_shape=(None,),
                 **opts):
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
        if converter_options is None:
            converter_options = opts
        super().__init__(dimension=dimension, coordinate_shape=coordinate_shape, converter_options=converter_options)

GenericInternalCoordinates = GenericInternalCoordinateSystem()
GenericInternalCoordinates.__name__ = "ZMatrixCoordinates"
GenericInternalCoordinates.__doc__ = """Generic internals"""

class CartesianToGICSystemConverter(CoordinateSystemConverter):
    """
    A converter class for going from Cartesian coordinates to internals coordinates
    """

    @property
    def types(self):
        return (CartesianCoordinates3D, GenericInternalCoordinates)

    def convert_many(self, coords, *, specs, order=0, masses=None, remove_translation_rotation=True,
                     reference_coordinates=None,
                     **kw):
        """
        We'll implement this by having the ordering arg wrap around in coords?
        """

        internals = nput.internal_coordinate_tensors(coords, specs, order=order, **kw)
        internals, derivs = internals[0], internals[1:]
        return internals, {
            'specs':specs,
            'derivs':derivs,
            'reference_coordinates':coords,
            'masses': masses,
            'remove_translation_rotation': remove_translation_rotation
        }

    def convert(self, coords, *, specs, order=0, **kw):
        return self.convert_many(coords, specs=specs, order=order, **kw)


class GICSystemToCartesianConverter(CoordinateSystemConverter):
    """
    A converter class for going from Cartesian coordinates to internals coordinates
    """

    @property
    def types(self):
        return (GenericInternalCoordinates, CartesianCoordinates3D)

    def convert_many(self, coords, *, reference_coordinates, specs, order=0,
                     masses=None,
                     remove_translation_rotation=True,
                     derivs=None,
                     **kw):
        """
        We'll implement this by having the ordering arg wrap around in coords?
        """

        if order == 0: order = 1
        (carts, errors), expansions = nput.inverse_coordinate_solve(specs, coords, reference_coordinates,
                                                                    order=order,
                                                                    return_expansions=True,
                                                                    masses=masses,
                                                                    remove_translation_rotation=remove_translation_rotation,
                                                                    **kw
                                                                    )
        derivs = expansions[1:]
        return carts, {
            'specs':specs,
            'derivs': derivs,
            'masses': masses,
            'remove_translation_rotation': remove_translation_rotation
        }

    def convert(self, coords, *, reference_coordinates, specs, order=0, **kw):
        return self.convert_many(coords, reference_coordinates=reference_coordinates, specs=specs, order=order, **kw)

__converters__ = [CartesianToGICSystemConverter(), GICSystemToCartesianConverter()]

