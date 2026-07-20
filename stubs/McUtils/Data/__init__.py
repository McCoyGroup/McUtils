"""
Provides a small data framework for wrapping up datasets into classes for access and loading.

The basic structure for a new dataset is defined in `CommonData.DataHandler`.
A simple, concrete example is in `AtomData.AtomData`.
A slightly more involved example is in `ConstantsData.UnitsData`.
"""
__all__ = ['DataHandler', 'DataError', 'DataRecord', 'AtomData', 'AtomDataHandler', 'UnitsData', 'UnitsDataHandler', 'BondData', 'BondDataHandler', 'WavefunctionData', 'PotentialData', 'ColorData']
from .CommonData import *
from .AtomData import *
from .ConstantsData import *
from .BondData import *
from .WavefunctionData import *
from .PotentialData import *
from .ColorData import *