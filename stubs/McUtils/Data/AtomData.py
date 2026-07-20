"""
Provides a class for handling a compiled set of atomic data
"""
import os
from .. import Devutils as dev
from .CommonData import DataHandler
__all__ = ['AtomData', 'AtomDataHandler']
__reload_hook__ = ['.CommonData']

class AtomDataHandler(DataHandler):
    """
    A DataHandler that's built for use with the atomic data we've collected.
    Usually used through the `AtomData` object.
    """

    def __init__(self):
        ...

    def __getitem__(self, item):
        """
        Special cases the default getitem so tuples are mapped
        :param item:
        :type item:
        :return:
        :rtype:
        """
        ...

    def load(self):
        ...
AtomData = AtomDataHandler()
AtomData.__doc__ = 'An instance of AtomDataHandler that can be used for looking up atom data'
AtomData.__name__ = 'AtomData'