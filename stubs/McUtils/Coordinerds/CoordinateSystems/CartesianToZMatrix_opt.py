from .CoordinateSystemConverter import CoordinateSystemConverter
from .CommonCoordinateSystems import CartesianCoordinates3D, ZMatrixCoordinates
from ...Numputils import vec_norms, vec_angles, vec_dihedrals, pts_dihedrals, dist_deriv, angle_deriv, dihed_deriv, find
from ...Scaffolding import MaxSizeCache
import numpy as np

class CartesianToZMatrixConverter(CoordinateSystemConverter):
    """
    A converter class for going from Cartesian coordinates to ZMatrix coordinates
    """

    @property
    def types(self):
        ...

    @staticmethod
    def get_dists(points, centers, return_diffs=False):
        ...

    @staticmethod
    def get_angles(lefts, centers, rights, norms=None):
        ...

    @staticmethod
    def get_diheds(points, centers, seconds, thirds, crosses=None, norms=None):
        ...

    def convert_many(self, coords, ordering=None, use_rad=True, return_derivs=False, **kw):
        """
        We'll implement this by having the ordering arg wrap around in coords?
        """
        ...

    @staticmethod
    def _get_conversion_info(ncoords, ordering, canonicalize):
        ...

    @staticmethod
    def _build_ordering_list(multiconfig, ol, ncoords):
        ...

    @staticmethod
    def _get_dist_inds(mask, ol, nol):
        ...

    def _get_cached_dist_inds(self, ol_key, ncoords, ol, nol):
        ...

    def _get_cached_norms(self, distance_matrix, coords, ix, jx):
        ...

    @staticmethod
    def _get_angle_inds(mask, ol, nol):
        ...

    def _get_cached_angle_inds(self, idx_list, mask, ncoords, ol, nol):
        ...

    def _get_angles_cached(self, distance_matrix, cross_mat, cross_norms, coords, ix, jx, kx):
        ...

    def _get_cached_crosses(self, distance_matrix, cross_mat, cross_norms, coords, ix, jx, kx):
        ...

    @staticmethod
    def _get_dihed_inds(mask, ol, nol):
        ...

    def _get_cached_dihed_inds(self, idx_list, mask, ncoords, ol, nol):
        ...

    @staticmethod
    def _restructure_angles(angles, ncoords, steps, nol, use_rad):
        ...

    @staticmethod
    def _restructure_diheds(diheds, ncoords, steps, nol, use_rad):
        ...

    @staticmethod
    def _build_post_ordering_lists(ol, om, ncoords, nol, ncol, steps):
        ...

    @staticmethod
    def _build_coord_triples(dists, angles, diheds):
        ...

    @staticmethod
    def _rebuild_ordering(ncol, ol, om):
        ...

    @staticmethod
    def _compute_final_frame(multiconfig, coords, mc_ol, nol, ol):
        ...

    def _convert_multiconfig(self, coords, ol, om, orig_ol, ncoords, nol, ncol, steps, use_rad, return_derivs, derivs):
        ...
    _index_cache = MaxSizeCache()

    def convert(self, coords, ordering=None, use_rad=True, return_derivs=False, canonicalize=True, **kw):
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