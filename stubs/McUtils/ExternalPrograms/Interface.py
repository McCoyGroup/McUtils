"""
Provides a uniform interface for potentially installed external programs
"""
__all__ = ['ExternalProgramInterface']
import weakref
import importlib

class ExternalProgramInterface:
    name = None
    module = None
    lib_supported = None
    library = None

    @classmethod
    def try_load_lib(cls):
        ...

    @classmethod
    def get_lib(cls):
        ...

    @classmethod
    def load_library(cls):
        ...
    method_table = weakref.WeakValueDictionary()

    @classmethod
    def method(cls, name: 'str|list[str]'):
        ...

    @classmethod
    def submodule(cls, submodule: 'str|list[str]'):
        ...

    @property
    def lib(self):
        ...

    def __getattr__(self, item):
        ...