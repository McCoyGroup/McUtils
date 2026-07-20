from .CoordinateSystemConverter import CoordinateSystemConverter
from .CommonCoordinateSystems import CartesianCoordinates3D, ZMatrixCoordinates
from ...Numputils import vec_norms, vec_angles, pts_dihedrals, dist_deriv, angle_deriv, dihed_deriv
from ... import Numputils as nput
import numpy as np

class CartesianToZMatrixConverter(CoordinateSystemConverter):
    """
    A converter class for going from Cartesian coordinates to ZMatrix coordinates
    """

    @property
    def types(self):
        ...

    @staticmethod
    def get_dists(points, centers):
        ...

    @staticmethod
    def get_angles(lefts, centers, rights):
        ...

    @staticmethod
    def get_diheds(points, centers, seconds, thirds):
        ...

    def convert_many(self, coords, *, ordering, use_rad=True, return_derivs=False, **kw):
        """
        We'll implement this by having the ordering arg wrap around in coords?
        """
        ...

    def convert(self, coords, *, ordering, use_rad=True, return_derivs=None, order=None, strip_embedding=False, derivative_method='new', validate=True, **kw):
        """The ordering should be specified like:

        [
            [n1],
            [n2, n1]
            [n3, n1/n2, n1/n2]
            [n4, n1/n2/n3, n1/n2/n3, n1/n2/n3]
            [n5, ...]
            ...
        ]

        :param coords:    array of cartesian coordinates
        :type coords:     np.ndarray
        :param use_rad:   whether to user radians or not
        :type use_rad:    bool
        :param ordering:  optional ordering parameter for the z-matrix
        :type ordering:   None or tuple of ints or tuple of tuple of ints
        :param kw:        ignored key-word arguments
        :type kw:
        :return: z-matrix coords
        :rtype: np.ndarray
        """
        ...
__converters__ = [CartesianToZMatrixConverter()]