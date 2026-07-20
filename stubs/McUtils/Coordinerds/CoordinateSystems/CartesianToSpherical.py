from .CoordinateSystemConverter import CoordinateSystemConverter
from .CommonCoordinateSystems import CartesianCoordinates3D, SphericalCoordinates
from ...Numputils import vec_dots, vec_angles
import numpy as np

class CartesianToSphericalConverter(CoordinateSystemConverter):
    """
    A converter class for going from Cartesian coordinates to ZMatrix coordinates
    """

    @property
    def types(self):
        ...

    def convert_many(self, coords, use_rad=True, origin=None, axes=None, **kw):
        """
        We'll implement this by having the ordering arg wrap around in coords?
        """
        ...

    def convert(self, coords, ordering=None, use_rad=True, return_derivs=False, **kw):
        ...
__converters__ = [CartesianToSphericalConverter()]