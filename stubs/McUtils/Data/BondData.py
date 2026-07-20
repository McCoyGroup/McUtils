from .. import Devutils as dev
import os
from .CommonData import DataHandler, DataError
__all__ = ['BondData', 'BondDataHandler']
__reload_hook__ = ['.CommonData']

class BondDataHandler(DataHandler):
    """
    A DataHandler that's built for use with the bond data we've collected.
    Usually used through the `BondData` object.
    """

    def __init__(self):
        ...

    def load(self):
        ...

    def get_distance(self, key, default=None):
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
BondData = BondDataHandler()
BondData.__doc__ = 'An instance of BondDataHandler that can be used for looking up bond distances'
BondData.__name__ = 'BondData'