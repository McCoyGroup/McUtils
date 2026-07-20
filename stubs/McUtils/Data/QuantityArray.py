"""
Provides a QuantityArray class to manage data & units simultaneously
"""
import numpy as np, io
__all__ = ['QuantityArray']

class QuantityArrayException(Exception):
    ...

class QuantityArray:
    """
    A little helper for working with NumPy arrays with units.
It's mostly just a safety mechanism for imported data, but also helps keep you from messing up when you
  do addition and multiplication and stuff.
    """

    def __init__(self, array, units):
        """
        :param array: array data
        :type array: np.ndarray
        :param unit: list of units for the array
        :type unit: str | Iterable[str]
        """
        ...

    @property
    def shape(self):
        ...

    @property
    def dtype(self):
        ...

    @classmethod
    def raise_unit_mismatch(cls, u1, u2):
        ...

    def __neg__(self):
        """Implements -a"""
        ...

    def __pos__(self):
        """Implements +a"""
        ...

    def __add__(self, other):
        """Implements a+b"""
        ...

    def __sub__(self, other):
        """Implements a-b"""
        ...

    def __mul__(self, other):
        """Implements a*b"""
        ...

    def __truediv__(self, other):
        """Implements a/b"""
        ...

    def __divmod__(self, other):
        """Implements a//b"""
        ...

    def convert(self, units):
        """
        Converts the array from units A to units B
        :param units:
        :type units:
        :return:
        :rtype:
        """
        ...

    def save(self, file):
        """
        Saves the QuantityArray to a file

        :param file:
        :type file:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def load(cls, file):
        """
        Loads a QuantityArray from file

        :param file:
        :type file:
        :return:
        :rtype:
        """
        ...

    def format_header(self):
        ...

    @classmethod
    def parse_header(cls, line):
        ...

    def savetxt(self, file):
        """
        Saves the QuantityArray to a text file
        :param file:
        :type file: file
        :return:
        :rtype:
        """
        ...

    @classmethod
    def loadtxt(cls, file):
        """
        Loads a QuantityArray from a text file

        :param file:
        :type file:
        :return:
        :rtype:
        """
        ...

    def __repr__(self):
        ...