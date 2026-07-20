"""
The coordinate mats class defines an architecture to mats coordinates
"""
import numpy as np
from collections import namedtuple
from .TransformationFunction import TransformationFunction
from .AffineTransform import AffineTransform
from .RotationTransform import RotationTransform
from .ScalingTransform import ScalingTransform
from .TranslationTransform import TranslationTransform
__all__ = ['GeometricTransformation']
__reload_hook__ = ['.TransformationFunction', '.AffineTransform', '.RotationTransform', '.ScalingTransform', '.TranslationTransform']

class GeometricTransformation:
    """
    The GeometricTransformation class provides a simple, general way to represent a
    compound coordinate transformation.
    In general, it's basically just a wrapper chaining together a number of TransformationFunctions.
    """

    def __init__(self, *transforms):
        ...

    @property
    def is_affine(self):
        ...

    @property
    def transformation_function(self):
        """

        :return:
        :rtype: TransformationFunction
        """
        ...

    @property
    def transforms(self):
        ...

    def apply(self, coords, shift=True):
        ...

    def __call__(self, coords, shift=True):
        ...

    def condense_transforms(self):
        ...

    @property
    def inverse(self):
        ...

    @staticmethod
    def parse_transform(tf):
        """
        Provides a way to "tag" a transformation
        :param tf:
        :type tf:
        :return:
        :rtype:
        """
        ...