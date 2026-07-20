import numpy as np
from .CommonData import DataHandler, DataRecord
__all__ = ['ColorData']
__reload_hook__ = ['.CommonData']

class ColorDataHandler(DataHandler):

    def __init__(self):
        ...

    def __getitem__(self, item):
        ...
ColorData = ColorDataHandler()
ColorData.__doc__ = 'An instance of `ColorDataHandler` that can be used for looking up data on color palettes'
ColorData.__name__ = 'ColorData'