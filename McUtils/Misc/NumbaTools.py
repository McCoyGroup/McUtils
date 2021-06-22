"""
Provides a set of decorators that allow code to be agnostic to whether Numba exists or not
"""
import warnings, typing

__all__ = [
    'njit',
    'jit',
    'type_spec',
    'numba_decorator'
]

def load_numba(warn=False):
    try:
        import numba
    except ImportError:
        if isinstance(warn, str) and warn == 'raise':
            raise
        if warn:
            warnings.warn("Numba not installed/code will be slower")
        numba = None

    return numba

def njit(*args, warn=False, **kwargs):
    return numba_decorator(*args, method='njit', warn=warn, **kwargs)

def jit(*args, warn=False, nopython=False, **kwargs):
    return numba_decorator(*args, method='jit', warn=warn, nopython=nopython, **kwargs)

def numba_decorator(*args, method=None, warn=False, **kwargs):
    numba = load_numba(warn=warn)
    if numba is not None:
        return getattr(numba, method)(*args, **kwargs)
    else:
        if len(args) > 0:
            return args[0]
        else:
            return lambda f:f

def type_spec(t, warn=False):
    numba = load_numba(warn=warn)
    if numba is not None:
        return getattr(numba, t)
    else:
        return typing.Any