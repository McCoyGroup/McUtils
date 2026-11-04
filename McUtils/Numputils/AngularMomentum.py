"""Low-level angular-momentum coupling functions."""
import functools
import operator
import numpy as np

__all__ = ['clebsch_gordan_spin1_couplings']


@functools.lru_cache(256)
def clebsch_gordan_spin1_couplings(j, ell, q):
    """Condon--Shortley Clebsch--Gordan coefficients <j,m;1,q|ell,m+q>.

    Integer j and spin-one q=-1,0,+1 only. Return (source,target,coefficients)
    for all allowed m: source=m+j, target=m+q+ell. These are generic spin-one
    coupling data, independent of Wigner expansions or orientational averages.
    Returned arrays are read-only and cached.
    """
    j, ell, q = operator.index(j), operator.index(ell), operator.index(q)
    if j < 0 or q not in (-1, 0, 1) or ell not in range(abs(j-1), j+2):
        raise ValueError('expected nonnegative integer j and an allowed j x 1 Clebsch-Gordan coupling')
    m = np.arange(-j, j + 1)
    valid = np.abs(m + q) <= ell
    m = m[valid]
    if ell == j + 1:
        denominator = (j + 1) * (2*j + 1)
        if q == 0:
            value = np.sqrt((j-m+1)*(j+m+1) / denominator)
        else:
            value = np.sqrt((j+q*m+1)*(j+q*m+2) / (2*denominator))
    elif ell == j and j:
        if q == 0:
            value = m / np.sqrt(j*(j+1))
        else:
            value = -q * np.sqrt((j-q*m)*(j+q*m+1) / (2*j*(j+1)))
    elif ell == j - 1:
        denominator = j * (2*j+1)
        if q == 0:
            value = -np.sqrt((j-m)*(j+m) / denominator)
        else:
            value = np.sqrt((j-q*m)*(j-q*m-1) / (2*denominator))
    else:
        raise ValueError('invalid spin-one coupling')
    source, target = m+j, m+q+ell
    for array in (source, target, value):
        array.flags.writeable = False
    return source, target, value
