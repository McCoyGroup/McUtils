from .CoordinateSystemConverter import CoordinateSystemConverter
from .CommonCoordinateSystems import CartesianCoordinates3D, ZMatrixCoordinates
from ...Numputils import *
import numpy as np

class ZMatrixToCartesianConverter(CoordinateSystemConverter):
    """
    A converter class for going from ZMatrix coordinates to Cartesian coordinates
    """

    @property
    def types(self):
        ...

    def default_ordering(self, coordlist):
        ...

    def convert_many(self, coordlist, *, ordering, origins=None, axes=None, use_rad=True, return_derivs=False, order=None, check_overlapping=False, check_ordering=False, use_direct_expansions=False, orthogonalize_derivatives=True, spec=None, **kw):
        """Expects to get a list of configurations
        These will look like:
            [
                [dist, angle, dihedral]
                ...
            ]
        and ordering will be
            [
                [pos, point, line, plane]
                ...
            ]
        **For efficiency it is assumed that all configurations have the same length**

        :param coordlist:
        :type coordlist:
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
__converters__ = [ZMatrixToCartesianConverter()]