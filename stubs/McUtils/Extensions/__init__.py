"""
A package for managing extension modules.
The existing `ExtensionLoader` will be moving here, and will be supplemented by classes for dealing with compiled extensions
"""
__all__ = ['CLoader', 'ModuleLoader', 'ArgumentType', 'ArrayType', 'PointerType', 'PrimitiveType', 'RealType', 'IntType', 'BoolType', 'Argument', 'FunctionSignature', 'SharedLibrary', 'SharedLibraryFunction', 'FFIModule', 'FFIMethod', 'FFIArgument', 'FFIType', 'FFILoader', 'DynamicFFIFunctionLoader', 'DynamicFFIFunction', 'DynamicFFILibrary']
from .CLoader import *
from .ModuleLoader import *
from .ArgumentSignature import *
from .SharedLibraryManager import *
from .FFI import *