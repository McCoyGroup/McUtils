from .CoordinateSystemConverter import CoordinateSystemConverter
from .CommonCoordinateSystems import CartesianCoordinates3D, SphericalCoordinates
from ...Numputils import *
import numpy as np

class SphericalToCartesianConverter(CoordinateSystemConverter):
    """
    A converter class for going from ZMatrix coordinates to Cartesian coordinates
    """

    @property
    def types(self):
        ...

    def convert_many(self, coords, origin=None, axes=None, use_rad=True, **kw):
        """
        Expects to get a list of configurations
        These will look like:
            [
                [dist, angle, dihedral]
                ...
            ]

        **For efficiency it is assumed that all configurations have the same length**

        :param coords:
        :type coords:
        :param origins:
        :type origins:
        :param axes:
        :type axes:
        :param use_rad:
        :type use_rad:
        :param kw:
        :type kw:
        :param ordering:
        :type ordering:
        :param return_derivs:
        :type return_derivs:
        :return:
        :rtype:
        """
        ...

    def convert(self, coords, **kw):
        """dipatches to convert_many but only pulls the first"""
        ...
__converters__ = [SphericalToCartesianConverter()]