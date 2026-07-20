"""
Provides hooks for viewing images, mostly through the Matplotlib Image interface
"""
__all__ = ['Image']
import numpy as np
from .Plots import ArrayPlot

class Image(ArrayPlot):
    """
    Simple subclass of ArrayPlot that just turns off most of the unnecessary features
    """
    default_opts = {'frame': False, 'ticks_style': (False, False), 'ticks': ([], []), 'padding': ([0, 0], [0, 0]), 'aspect_ratio': 'auto'}

    def __init__(self, data, plot_range=None, image_size=None, **kwargs):
        ...

    @classmethod
    def from_file(cls, file_name, format=None, **opts):
        ...