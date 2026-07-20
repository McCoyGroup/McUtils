import os, collections
from ..SharedLibraryManager import SharedLibrary, SharedLibraryFunction
from .Module import FFIModule, FFIMethod, FFIArgument, FFIParameters, ThreadingMode
__all__ = ['DynamicFFIFunctionLoader', 'DynamicFFIFunction', 'DynamicFFILibrary']

class DynamicFFIFunctionLoader:
    """
    This is a singleton class that can be set to define the global
    linkage to the DynamicLibrary extension module
    """
    _loader = None
    _compile_args = {}
    _lib_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'libs', 'DynamicFFILibrary')

    @classmethod
    def configure(cls, **compile_args):
        """
        **LLM Docstring**

        Merge compiler options into the process-wide dynamic FFI loader configuration.

        :param compile_args: compiler and loader options
        :type compile_args: dict[str, Any]

        :return: nothing; updates the shared configuration
        :rtype: None
        """
        ...

    @classmethod
    def load(cls):
        """
        **LLM Docstring**

        Compile or load and cache the bundled dynamic FFI support module.

        :return: the singleton caller module
        :rtype: FFIModule
        """
        ...

class DynamicFFIFunction(SharedLibraryFunction):
    """
    Specialization of base `SharedLibraryFunction` to call
    through the `DynamicLibrary` module instead of `ctypes`
    """
    _caller = None

    @classmethod
    def _load_lib(cls):
        """
        **LLM Docstring**

        Load and cache the shared dynamic FFI caller on the function class.

        :return: the caller module
        :rtype: FFIModule
        """
        ...

    def __init__(self, shared_library, signature, defaults=None, docstring=None, call_directory=None, return_handler=None, prep_args=None):
        """
        **LLM Docstring**

        Initialize a shared-library function that dispatches through the dynamic FFI module.

        :param shared_library: library path or loader
        :type shared_library: Any

        :param signature: function signature
        :type signature: Any

        :param defaults: argument defaults
        :type defaults: Any

        :param docstring: optional function documentation
        :type docstring: Any

        :param call_directory: optional working directory
        :type call_directory: Any

        :param return_handler: result postprocessor
        :type return_handler: Any

        :param prep_args: keyword preprocessing callback
        :type prep_args: Any

        :return: nothing; initializes lazy FFI metadata and call-state storage
        :rtype: None
        """
        ...

    def initialize(self):
        """
        **LLM Docstring**

        Ensure the caller module is loaded and translate signature arguments to `FFIArgument` objects.

        :return: nothing; initializes `_ffi_args` lazily
        :rtype: None
        """
        ...

    class LibFFIMethodData:

        def __init__(self, lib, name, return_type, args, vectorized=False):
            """
            **LLM Docstring**

            Store the native library handle, symbol name, return type, argument specs, and vectorization flag expected by the caller.

            :param lib: loaded native library handle
            :type lib: Any

            :param name: symbol name
            :type name: Any

            :param return_type: FFI return type
            :type return_type: Any

            :param args: FFI argument specifications
            :type args: Any

            :param vectorized: whether the result is vectorized
            :type vectorized: Any

            :return: nothing; stores method metadata
            :rtype: None
            """
            ...

    @property
    def function_data(self):
        """
        **LLM Docstring**

        Build and cache the lightweight method metadata consumed by the dynamic caller.

        :return: the cached call descriptor
        :rtype: DynamicFFIFunction.LibFFIMethodData
        """
        ...

    def _call(self, args, kwargs):
        """
        **LLM Docstring**

        Prepare FFI parameters, validate their interface, consume queued call options, and invoke serial or threaded libffi dispatch.

        :param args: positional values or `None`
        :type args: Any

        :param kwargs: keyword argument mapping
        :type kwargs: Any

        :return: the raw result and prepared parameter collection
        :rtype: tuple[Any, FFIParameters]
        """
        ...

    def __call__(self, *args, debug=False, threading_vars=None, threading_mode=None, **kwargs):
        """
        **LLM Docstring**

        Queue debug and threading options for one call, then delegate argument preprocessing and return handling to the base class.

        :param debug: debug selector
        :type debug: Any

        :param threading_vars: argument name or names used for threaded partitioning
        :type threading_vars: Any

        :param threading_mode: threading backend
        :type threading_mode: Any

        :param args: positional argument values
        :type args: tuple[Any, ...]

        :param kwargs: keyword argument values
        :type kwargs: dict[str, Any]

        :return: the postprocessed dynamic FFI result
        :rtype: Any
        """
        ...

class DynamicFFILibrary(SharedLibrary):
    """
    Directly analogous to a regular shared library but it uses
    `DynamicFFIFunction` to dispatch calls
    """
    method_type = DynamicFFIFunction

    def __init__(self, library, compiler_options=None, **functions):
        """
        **LLM Docstring**

        Create a dynamic FFI library and retain optional compiler configuration for lazy application.

        :param library: library path or loader
        :type library: Any

        :param compiler_options: options applied before the first function lookup
        :type compiler_options: Any

        :param functions: registered function definitions
        :type functions: dict[str, Any]

        :return: nothing; initializes the library
        :rtype: None
        """
        ...

    def get_function(self, item):
        """
        **LLM Docstring**

        Apply compiler options once on first access, then retrieve a registered function.

        :param item: registered function tag
        :type item: Any

        :return: the requested function
        :rtype: DynamicFFIFunction
        """
        ...

    @classmethod
    def configure_loader(cls, **compile_opts):
        """
        **LLM Docstring**

        Forward compile options to the singleton dynamic FFI loader.

        :param compile_opts: compiler and loader options
        :type compile_opts: dict[str, Any]

        :return: nothing; updates global loader configuration
        :rtype: None
        """
        ...