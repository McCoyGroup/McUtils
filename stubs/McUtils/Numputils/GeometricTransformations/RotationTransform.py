from .AffineTransform import AffineTransform
import numpy as np
__all__ = ['RotationTransform']
__reload_hook__ = ['.AffineTransform']

class RotationTransform(AffineTransform):
    """A simple AffineTransform implementation of the TransformationFunction abstract base class

    """

    def __init__(self, theta, axis='z', center=None):
        """

        :param theta: angle through which to rotate
        :type theta: float
        :param axis: axis about which to rotate
        :type axis: axis about which to rotate
        :param center: center point for the rotation
        :type center: None or np.array
        """
        ...

    def reverse(self):
        ...