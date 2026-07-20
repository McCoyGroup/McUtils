import functools
__all__ = ['mixedmethod']

class mixedmethod:

    def __init__(self, wrapped_fn):
        ...

    def __get__(self, obj, obj_type=None):
        ...