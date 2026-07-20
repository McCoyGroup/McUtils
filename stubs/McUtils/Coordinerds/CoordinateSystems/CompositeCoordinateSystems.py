import uuid
import numpy as np
from .CoordinateSystem import CoordinateSystem
from .CoordinateSystemConverter import CoordinateSystemConverter
from ... import Numputils as nput
import weakref
__all__ = ['CompositeCoordinateSystem', 'CompositeCoordinateSystemConverter']

class CompositeCoordinateSystem(CoordinateSystem):
    """
    Defines a coordinate system that comes from applying a transformation
    to another coordinate system
    """
    _register_cache = weakref.WeakValueDictionary()

    def __init__(self, base_system, conversion, inverse_conversion=None, jacobian=None, inverse_jacobian=None, name=None, batched=None, pointwise=True, **opts):
        ...

    @classmethod
    def canonical_name(cls, name, conversion):
        ...

    @classmethod
    def register(cls, base_system, conversion, inverse_conversion=None, name=None, batched=None, pointwise=True, **opts):
        ...

    def unregister(self):
        ...

    def __repr__(self):
        ...

class CompositeCoordinateSystemConverter(CoordinateSystemConverter):

    def __init__(self, system: CompositeCoordinateSystem, direction='forward'):
        ...

    @property
    def types(self):
        ...

    def get_conversion(self):
        ...

    def convert(self, coords, **kw):
        ...

    def convert_many(self, coords, order=0, derivs=None, return_derivs=None, **kw):
        ...