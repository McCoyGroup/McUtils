"""
Misc utilities for debugging
"""
__all__ = ['ModificationTracker']
import enum, inspect
from ..Scaffolding import Logger

class ModificationType(enum.Enum):
    """Real access pattern: ModificationType.<MemberName> (this is an enum with 8 members, e.g. ModificationType.GetAttr == '__getattr__'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
    _MEMBERS = {'GetAttr': '__getattr__', 'SetAttr': '__setattr__', 'Add': '__iadd__', 'Sub': '__isub__', 'Div': '__idiv__', 'Mul': '__imul__', 'MatMul': '__imatmul__', 'Any': 'any'}

class ModificationTypeHandler(enum.Enum):
    Raise = 'raise'
    Log = 'log'

class ModificationTracker:
    """
    A simple class to wrap an object to track when it is accessed or
    modified
    """

    def __init__(self, obj, handlers=ModificationTypeHandler.Log, logger=None):
        ...

    @property
    def handler_dispatch(self):
        ...

    def log_modification(self, obj, handler_type, *args, **kwargs):
        """
        Logs on modification

        :param obj:
        :type obj:
        :param handler_type:
        :type handler_type:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def raise_modification(self, obj, handler_type, *args, **kwargs):
        """
        Raises an error on modification

        :param obj:
        :type obj:
        :param handler_type:
        :type handler_type:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def _dispatch_handler(self, handler_type, *args, **kwargs):
        ...

    def __getattr__(self, item):
        """
        Handler to intercept `getattr` requests
        :param item:
        :type item:
        :return:
        :rtype:
        """
        ...

    def __setattr__(self, item, val):
        """
        Handler to intercept `setattr` requests

        :param item:
        :type item:
        :param val:
        :type val:
        :return:
        :rtype:
        """
        ...

    def __iadd__(self, other):
        """
        Handler to intercept `add` requests

        :param item:
        :type item:
        :param val:
        :type val:
        :return:
        :rtype:
        """
        ...

    def __isub__(self, other):
        """
        Handler to intercept `sub` requests

        :param item:
        :type item:
        :param val:
        :type val:
        :return:
        :rtype:
        """
        ...

    def __imul__(self, other):
        """
        Handler to intercept `div` requests

        :param item:
        :type item:
        :param val:
        :type val:
        :return:
        :rtype:
        """
        ...

    def __idiv__(self, other):
        """
        Handler to intercept `div` requests

        :param item:
        :type item:
        :param val:
        :type val:
        :return:
        :rtype:
        """
        ...

    def __imatmul__(self, other):
        """
        Handler to intercept `matmul` requests

        :param item:
        :type item:
        :param val:
        :type val:
        :return:
        :rtype:
        """
        ...