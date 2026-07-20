import numpy as np
from .TransformationFunction import TransformationFunction
from ...Numputils import affine_matrix, merge_transformation_matrix, one_pad_vecs
__all__ = ['AffineTransform']
__reload_hook__ = ['.TransformationFunction', '...Numputils']

class AffineTransform(TransformationFunction):
    """
    A simple AffineTranform implementation of the TransformationFunction abstract base class
    """

    def __init__(self, tmat, shift=None):
        """tmat must be a transformation matrix to work properly

        :param shift: the shift for the transformation
        :type shift: np.ndarray | None
        :param tmat: the matrix for the linear transformation
        :type tmat: np.ndarray
        """
        ...

    @property
    def transform(self):
        ...

    @property
    def inverse(self):
        """
        Returns the inverse of the transformation
        :return:
        :rtype:
        """
        ...

    @property
    def shift(self):
        ...

    def merge(self, other):
        """

        :param other:
        :type other: np.ndarray or AffineTransform
        """
        ...

    def reverse(self):
        """Inverts the matrix

        :return:
        :rtype:
        """
        ...

    def operate(self, coords, shift=True):
        """

        :param coords: the array of coordinates passed in
        :type coords: np.ndarry
        """
        ...

    def __repr__(self):
        ...