import numpy as np
from .. import Numputils as nput
__all__ = ['convert_cartesian_to_zmatrix', 'convert_zmatrix_to_cartesians']

def get_dists(points, centers):
    """
    **LLM Docstring**

    Compute the Euclidean distance from each `center` to the corresponding `point` using `Numputils.pts_norms`.

    The arguments are passed in reversed order to `pts_norms` (`centers` first, then `points`), matching that routine's origin/endpoint convention. Leading batch dimensions are handled by the delegated Numputils routine.

    :param points: Endpoint Cartesian coordinates.
    :type points: np.ndarray
    :param centers: Origin Cartesian coordinates broadcast-compatible with `points`.
    :type centers: np.ndarray
    :return: Distances between corresponding centers and points.
    :rtype: np.ndarray
    """
    ...

def get_angles(lefts, centers, rights):
    """
    **LLM Docstring**

    Compute angles for triples `(left, center, right)`.

    This is a thin wrapper around `Numputils.pts_angles` that suppresses the auxiliary cross-product vectors by setting `return_crosses=False`.

    :param lefts: Cartesian coordinates of the first endpoint of each angle.
    :type lefts: np.ndarray
    :param centers: Cartesian coordinates of the angle vertices.
    :type centers: np.ndarray
    :param rights: Cartesian coordinates of the second endpoint of each angle.
    :type rights: np.ndarray
    :return: Angle values for the supplied triples.
    :rtype: np.ndarray
    """
    ...

def get_diheds(points, centers, seconds, thirds):
    """
    **LLM Docstring**

    Compute signed dihedral angles for quadruples `(point, center, second, third)`.

    The coordinates are forwarded directly to `Numputils.pts_dihedrals`, which determines batching and angular units.

    :param points: Cartesian coordinates of the first atom in each dihedral.
    :type points: np.ndarray
    :param centers: Cartesian coordinates of the second atom.
    :type centers: np.ndarray
    :param seconds: Cartesian coordinates of the third atom.
    :type seconds: np.ndarray
    :param thirds: Cartesian coordinates of the fourth atom.
    :type thirds: np.ndarray
    :return: Dihedral-angle values for the supplied quadruples.
    :rtype: np.ndarray
    """
    ...

def tile_order_list(ol, ncoords):
    """
    **LLM Docstring**

    Repeat a Z-matrix ordering block until it contains one row per coordinate and offset atom-index columns in each repetition.

    The first four columns are treated as atom indices. For repetition `k`, all four are increased by `k * len(ol)`. Any columns after the fourth are copied unchanged as flags. `ncoords` must be an exact multiple of the number of rows in `ol`.

    :param ol: Two-dimensional ordering template with four index columns and optional trailing flag columns.
    :type ol: np.ndarray
    :param ncoords: Required number of rows in the expanded ordering.
    :type ncoords: int
    :return: Ordering array of shape `(ncoords, ol.shape[1])`.
    :rtype: np.ndarray
    :raises ValueError: If `ncoords` is not divisible by `len(ol)`.
    """
    ...

def convert_cartesian_to_zmatrix(coords, *, ordering, use_rad=True, return_derivs=None, order=None, strip_embedding=False, derivative_method='new'):
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

def convert_zmatrix_to_cartesians(coordlist, *, ordering, origins=None, axes=None, use_rad=True, return_derivs=None, order=None):
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