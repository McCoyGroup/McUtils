"""
Provides constants data and conversions between units and unit systems
"""
from .CommonData import DataHandler
from collections import OrderedDict, deque
__all__ = ['UnitsData', 'UnitsDataHandler']
__reload_hook__ = ['.CommonData']

class ConversionError(Exception):
    ...

class UnitGraph:

    def __init__(self, stuff_to_update=()):
        ...

    def __contains__(self, item):
        ...

    def add(self, node, connection):
        ...

    def update(self, iterable):
        ...

    def keys(self):
        ...

    def __getitem__(self, item):
        ...

    def find_path_bfs(self, start, end):
        ...

class UnitsDataHandler(DataHandler):
    """
    A DataHandler that's built for use with the units data we've collected.
    Usually used through the `UnitsData` object.
    """
    postfix_map = OrderedDict((('Squared', 2), ('Cubed', 3), ('Fourthed', 4), ('Fifthed', 5)))

    def __init__(self):
        ...

    def load(self):
        ...

    def _load_unit_graph(self):
        """Builds a graph of units to traverse when finding conversions"""
        ...

    def _get_unit_modifiers(self, unit):
        """Pulls modifiers off strings like InverseDecimeters

        :param unit:
        :type unit: str
        :return: scaling, inverted, base_unit, power
        :rtype:
        """
        ...

    def _canonicalize_unit(self, unit):
        ...

    def _find_direct_conversion(self, src, targ):
        ...

    def _get_pathy_conversion(self, src, targ):
        ...

    def _find_path_conversion(self, src, targ):
        ...

    def expand_conversions(self, unit_stuff_1):
        ...

    def find_conversion(self, unit, target):
        """Attempts to find a conversion between two sets of units. Currently only implemented for "plain" units.

        :param unit:
        :type unit:
        :param target:
        :type target:
        :return:
        :rtype:
        """
        ...

    def add_conversion(self, unit, target, value):
        ...

    def convert(self, unit, target):
        """Converts base unit into target using the scraped NIST data

        :param unit:
        :type unit:
        :param target:
        :type target:
        :return:
        :rtype:
        """
        ...

    @property
    def constants(self):
        ...

    def constant(self, const):
        """Converts base unit into target using the scraped NIST data

        :param unit:
        :type unit:
        :param target:
        :type target:
        :return:
        :rtype:
        """
        ...
    "Real access pattern: UnitsDataHandler.<AttrName> (9 class attributes, e.g. UnitsDataHandler.Wavenumbers == 'Wavenumbers'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"
    _MEMBERS = {'Wavenumbers': 'Wavenumbers', 'Hartrees': 'Hartrees', 'Angstroms': 'Angstroms', 'BohrRadius': 'BohrRadius', 'ElectronMass': 'ElectronMass', 'AtomicMassUnits': 'AtomicMassUnits', 'ElectronVolts': 'ElectronVolts', 'KilocaloriesPerMole': 'Kilocalories/Mole', 'KilojoulesPerMole': 'Kilocalories/Mole'}

    @property
    def hartrees_to_wavenumbers(self):
        ...

    @property
    def bohr_to_angstroms(self):
        ...

    @property
    def amu_to_me(self):
        ...

    @property
    def moles(self):
        ...
UnitsData = UnitsDataHandler()
UnitsData.__doc__ = 'An instance of UnitsDataHandler that can be used for unit conversion and fundamental constant lookups'
UnitsData.__name__ = 'UnitsData'