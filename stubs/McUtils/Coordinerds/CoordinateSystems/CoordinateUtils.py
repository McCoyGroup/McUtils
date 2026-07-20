"""
Little utils that both CoordinateSet and CoordinateSystem needed
"""
import numpy as np
__all__ = ['is_multiconfig', 'mc_safe_apply']

def is_multiconfig(coords, coord_shape=None):
    ...

def mc_safe_apply(fun, coords):
    """Applies fun to the coords in such a way that it will apply to an array of valid
    coordinates (as determined by dimension of the basis). This will either be a single configuration
    or multiple configurations

    :param fun:
    :type fun:
    :return:
    :rtype:
    """
    ...