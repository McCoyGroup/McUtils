"""
Lebedev quadrature grids for spheres and unions of spheres.
Pure numpy/scipy implementation -- no external quadrature libraries.

References
----------
V.I. Lebedev, "Quadratures on a sphere", Zh. Vychisl. Mat. Mat. Fiz. 16 (1976).
V.I. Lebedev and D.N. Laikov, Dokl. Math. 59 (1999) 477-481.
The octahedral-orbit generator ("gen_oh") and the numeric constants below
follow the standard published Lebedev-Laikov tables (the same constants
underlie the public-domain SPHERE_LEBEDEV_RULE code and most quantum
chemistry packages' DFT integration grids).
"""
import numpy as np
import functools
__all__ = ['lebedev_rule', 'lebedev_grid']

def _gen_oh(code, a=0, b=0):
    """
    Generate one octahedral-symmetry orbit of points on the unit sphere.

    code : int
        1 -> (+-1, 0, 0) and permutations                        6 points
        2 -> (+-a, +-a, 0), a = 1/sqrt(2), and permutations     12 points
        3 -> (+-a, +-a, +-a), a = 1/sqrt(3)                      8 points
        4 -> (+-a, +-a, +-b), b = sqrt(1-2a^2), permutations    24 points
        5 -> (+-a, +-b, 0), b = sqrt(1-a^2), permutations       24 points
        6 -> (+-a, +-b, +-c), c = sqrt(1-a^2-b^2), all perms    48 points
    """
    ...
'_LEBEDEV_TABLE data omitted from this build (32 keys: [6, 14, 26, 38, 50, 74, 86, 110, 146, 170, 194, 230, 266, 302, 350, 434, 590, 770, 974, 1202, 1454, 1730, 2030, 2354, 2702, 3074, 3470, 3890, 4334, 4802, 5294, 5810])'

@functools.lru_cache(maxsize=100)
def lebedev_rule(order, exact=False, check_order=False, check_weights=False):
    """
    Return (points, weights) for a Lebedev grid of the given order
    (order = number of grid points; any of the 31 tabulated orders from
    6 up to 5294 -- see sorted(_LEBEDEV_TABLE) for the full list).

    `points` is (order, 3), on the unit sphere.
    `weights` sums to 1.0 -- multiply by 4*pi*r**2 for a surface integral.
    """
    ...

def lebedev_grid(npts, use_degree=False, return_weights=False):
    """Lebedev grid placed on one sphere; weights are surface-area weights."""
    ...