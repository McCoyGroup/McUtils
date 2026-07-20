"""
Provides a set of decorators that allow code to be agnostic to whether Numba exists or not
"""
import warnings, typing
__all__ = ['njit', 'jit', 'type_spec', 'without_numba', 'numba_decorator', 'import_from_numba', 'objmode', 'prange']

class NumbaState:
    numba_disabled = False

class without_numba:

    def __init__(self):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

def load_numba(warn=False):
    ...

def njit(*args, warn=False, **kwargs):
    ...

def jit(*args, warn=False, nopython=False, **kwargs):
    ...

def numba_decorator(*args, method=None, warn=False, **kwargs):
    ...

def type_spec(t, warn=False):
    ...

def import_from_numba(name, default):
    ...

class _noop_context:

    def __init__(self, *args, **kwargs):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
objmode = import_from_numba('objmode', _noop_context)
prange = import_from_numba('prange', range)