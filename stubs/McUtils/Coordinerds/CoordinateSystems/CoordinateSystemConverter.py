"""
Provides the conversion framework between coordinate systems
"""
from collections import OrderedDict as odict, deque
import os, abc, numpy as np, weakref
from ...Extensions import ModuleLoader
from ...Numputils import apply_by_coordinates
__all__ = ['CoordinateSystemConverters', 'CoordinateSystemConverter', 'SimpleCoordinateSystemConverter']
__reload_hook__ = ['...Extensions', '.CartesianToZMatrix', '.ZMatrixToCartesian']

class CoordinateSystemConverter(metaclass=abc.ABCMeta):
    """
    A base class for type converters
    """
    converters = None

    @property
    @abc.abstractmethod
    def types(self):
        """The types property of a converter returns the types the converter converts

        """
        ...

    def convert_many(self, coords_list, **kwargs):
        """Converts many coordinates. Used in cases where a CoordinateSet has higher dimension
        than its basis dimension. Should be overridden by a converted to provide efficient conversions
        where necessary.

        :param coords_list: many sets of coords
        :type coords_list: np.ndarray
        :param kwargs:
        :type kwargs:
        """
        ...

    @abc.abstractmethod
    def convert(self, coords, **kwargs):
        """The main necessary implementation method for a converter class.
        Provides the actual function that converts the coords set

        :param coords:
        :type coords: np.ndarray
        :param kwargs:
        :type kwargs:
        """
        ...

    def register(self, where=None, check=True):
        """
        Registers the CoordinateSystemConverter

        :return:
        :rtype:
        """
        ...

    def deregister(self, where=None, check=True):
        """
        Registers the CoordinateSystemConverter

        :return:
        :rtype:
        """
        ...

    def __call__(self, coords, **kwargs):
        ...

class CoordinateSystemConverters:
    """
    A coordinate converter class. It's a singleton so can't be instantiated.
    """
    converters = odict([])
    converter_graph = None
    converters_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Resources', 'Converters')
    converters_package = '.'.join(__name__.split('.')[:-1])
    converter_type = CoordinateSystemConverter

    def __init__(self):
        ...

    @classmethod
    def get_coordinates(self, coordinate_set):
        """Extracts coordinates from a coordinate_set
        """
        ...

    @classmethod
    def _get_converter_file(self, file):
        ...

    @classmethod
    def load_converter(self, converter):
        ...
    _converters_loaded = False

    @classmethod
    def _preload_converters(self):
        """
        Preloads Cartesian/ZMatrix converters.
        Maybe will load others in the future.
        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_converter(cls, system1, system2):
        """
        Gets the appropriate converter for two CoordinateSystem objects

        :param system1:
        :type system1: CoordinateSystem
        :param system2:
        :type system2: CoordinateSystem
        :return:
        :rtype:
        """
        ...

    @classmethod
    def register_converter(cls, system1, system2, converter, check=True):
        """
        Registers a converter between two coordinate systems

        :param system1:
        :type system1: CoordinateSystem
        :param system2:
        :type system2: CoordinateSystem
        :return:
        :rtype:
        """
        ...

    @classmethod
    def deregister_converter(cls, system1, system2, converter, check=True):
        """
        Registers a converter between two coordinate systems

        :param system1:
        :type system1: CoordinateSystem
        :param system2:
        :type system2: CoordinateSystem
        :return:
        :rtype:
        """
        ...

    @classmethod
    def _register(cls, system1, system2, converter, move_to_end=False):
        ...

class ConversionGraph:
    """
    Pulled from the UnitGraph stuff
    """

    def __init__(self, stuff_to_update=(), proxy_function=None):
        ...

    def __contains__(self, item):
        ...

    def add(self, node, connection):
        ...

    def keys(self):
        ...

    def update(self, iterable):
        ...

    def find_path_bfs(self, start, end):
        ...

class SimpleCoordinateSystemConverter(CoordinateSystemConverter):

    def __init__(self, types, conversion, **opts):
        ...

    @property
    def types(self):
        ...

    def convert(self, coords, **kw):
        ...

    def convert_many(self, coords, **kw):
        ...

class ChainedCoordinateSystemConverter(CoordinateSystemConverter):

    def __init__(self, types, conversions, **opts):
        ...

    @classmethod
    def prep_conversions(cls, conv_list):
        ...

    @property
    def types(self):
        ...

    def convert(self, crds, **kwargs):
        ...

    def convert_many(self, coords, **kw):
        ...
CoordinateSystemConverter.converters = weakref.ref(CoordinateSystemConverters)