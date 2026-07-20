"""
Defines a SharedLibrary object that makes it relatively straightforward to use
extensions direclty from .so files
"""
import os, ctypes
from .ArgumentSignature import FunctionSignature, Argument
__all__ = ['SharedLibrary', 'SharedLibraryFunction']

class SharedLibraryLoader:

    def __init__(self, shared_library):
        """
        **LLM Docstring**

        Wrap a shared-library path or an existing loaded library handle.

        For an existing handle, the private `_name` attribute is used to recover its path; nonexistent paths are stored as `None`.

        :param shared_library: library path or loaded handle
        :type shared_library: str | ctypes.CDLL

        :return: no value is returned
        :rtype: None
        """
        ...

    class InDir:
        """
        A super simple context manager that manages going into a directory and then leaving when finished
        """

        def __init__(self, dir_name):
            """
            **LLM Docstring**

            Create a context manager that temporarily changes the working directory.

            :param dir_name: directory entered by the context
            :type dir_name: str

            :return: no value is returned
            :rtype: None
            """
            ...

        def __enter__(self):
            """
            **LLM Docstring**

            Save the current directory and change to the target directory.

            :return: the context manager does not return a value
            :rtype: None
            """
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Restore the saved working directory and clear the saved path.

            :param exc_type: exception type from the context
            :type exc_type: type | None

            :param exc_val: exception value from the context
            :type exc_val: BaseException | None

            :param exc_tb: exception traceback from the context
            :type exc_tb: types.TracebackType | None

            :return: `None`, so exceptions are not suppressed
            :rtype: None
            """
            ...

    def in_dir(self):
        """
        **LLM Docstring**

        Create a context manager for entering the library directory.

        :return: directory-changing context manager
        :rtype: SharedLibraryLoader.InDir
        """
        ...

    @property
    def lib(self):
        """
        **LLM Docstring**

        Return the loaded library, loading it lazily when necessary.

        `ctypes.cdll.LoadLibrary` is executed while the process is in the library directory.

        :return: loaded shared-library handle
        :rtype: ctypes.CDLL
        """
        ...

    @property
    def lib_dir(self):
        """
        **LLM Docstring**

        Return the directory containing the configured library file.

        :return: library directory path
        :rtype: str
        """
        ...

class SharedLibraryFunction:
    """
    An object that provides a way to call into a shared library function
    """

    def __init__(self, shared_library, signature: FunctionSignature, defaults=None, docstring=None, call_directory=None, return_handler=None, prep_args=None):
        """
        :param shared_library: the path to the shared library file you want to use
        :type shared_library: str |
        :param function_signature: the signature of the function to load
        :type function_signature: FunctionSignature
        :param call_directory: the directory for calling
        :type call_directory: str
        :param docstring: the docstring for the function
        :type docstring: str
        """
        ...

    @classmethod
    def construct(cls, name, lib, docstring=None, defaults=None, return_type=None, return_handler=None, **args):
        """
        **LLM Docstring**

        Construct a shared-library function from a name and keyword type specifications.

        The current implementation evaluates `name ** args` before calling `FunctionSignature.construct`, rather than forwarding `name, **args`; ordinary string names and dictionaries will therefore raise `TypeError` before construction.

        :param name: left operand used by the current exponentiation expression
        :type name: Any

        :param lib: library source
        :type lib: str | ctypes.CDLL | SharedLibraryLoader

        :param docstring: optional function documentation
        :type docstring: str | None

        :param defaults: argument defaults
        :type defaults: dict | None

        :param return_type: return type specification
        :type return_type: Any | None

        :param return_handler: postprocessor receiving the raw result and prepared arguments
        :type return_handler: Callable | None

        :param args: argument type specifications used as the exponentiation right operand
        :type args: dict[str, Any]

        :return: constructed wrapper if the current expression succeeds
        :rtype: SharedLibraryFunction
        """
        ...

    @property
    def function(self):
        """
        **LLM Docstring**

        Initialize and return the underlying `ctypes` function.

        :return: configured foreign function
        :rtype: ctypes._CFuncPtr
        """
        ...

    def initialize(self):
        """
        **LLM Docstring**

        Resolve the function from the library and apply its return and argument type declarations.

        Initialization is performed only once and cached in `_fun`.

        :return: no value is returned
        :rtype: None
        """
        ...

    def doc(self):
        """
        **LLM Docstring**

        Combine the generated C/C++ signature with the stored documentation string.

        :return: signature and documentation separated by a newline
        :rtype: str
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation containing the signature and loaded library.

        :return: representation string
        :rtype: str
        """
        ...

    @property
    def signature(self):
        """
        **LLM Docstring**

        Return the stored function signature.

        :return: function signature
        :rtype: FunctionSignature
        """
        ...

    @classmethod
    def _manage_return(cls, res, args):
        """
        **LLM Docstring**

        Apply the default return conversion by unwrapping `ctypes` containers.

        The prepared argument mapping is accepted but ignored.

        :param res: raw foreign-function result
        :type res: Any

        :param args: prepared arguments keyed by name
        :type args: dict[str, Any]

        :return: unwrapped result
        :rtype: Any
        """
        ...

    @classmethod
    def uncast(cls, res):
        """
        **LLM Docstring**

        Unwrap common `ctypes` by-reference and scalar containers.

        Objects with `_obj` are replaced by that object; objects with `value` are then replaced by their Python value.

        :param res: result to unwrap
        :type res: Any

        :return: unwrapped value
        :rtype: Any
        """
        ...

    def _call(self, args, kwargs):
        """
        **LLM Docstring**

        Prepare arguments, invoke the foreign function, and retain prepared values by name.

        When a call directory is configured, invocation occurs while temporarily changed into that directory.

        :param args: positional values or `None`
        :type args: Iterable[Any] | None

        :param kwargs: keyword argument values
        :type kwargs: Mapping[str, Any]

        :return: pair of the raw result and a name-to-prepared-argument mapping
        :rtype: tuple[Any, dict[str, Any]]
        """
        ...

    def call(self, *args, **kwargs):
        """
        Calls the function we loaded.
        This will be parallelized out to handle more complicated usages.

        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def __call__(self, *args, **kwargs):
        """
        **LLM Docstring**

        Forward a normal Python call to `call`.

        :param args: positional function arguments
        :type args: tuple

        :param kwargs: keyword function arguments
        :type kwargs: dict

        :return: postprocessed foreign-function result
        :rtype: Any
        """
        ...

class SharedLibrary:
    method_type = SharedLibraryFunction

    def __init__(self, library, **functions):
        """
        **LLM Docstring**

        Create a shared-library facade and optionally register functions from configuration dictionaries.

        :param library: library path, handle, or loader
        :type library: str | ctypes.CDLL | SharedLibraryLoader

        :param functions: registration options keyed by exposed attribute name
        :type functions: dict[str, dict]

        :return: no value is returned
        :rtype: None
        """
        ...

    def register(self, tag, name=None, docstring=None, defaults=None, return_handler=None, prep_args=None, **params):
        """
        **LLM Docstring**

        Register and return a callable wrapper for one library function.

        The exposed `tag` may differ from the native function `name`; remaining keyword parameters define the `FunctionSignature` arguments.

        :param tag: lookup name stored in the facade
        :type tag: str

        :param name: native symbol name, defaulting to `tag`
        :type name: str | None

        :param docstring: optional function documentation
        :type docstring: str | None

        :param defaults: argument defaults
        :type defaults: dict | None

        :param return_handler: raw-result postprocessor
        :type return_handler: Callable | None

        :param prep_args: keyword-argument preprocessing callback
        :type prep_args: Callable | None

        :param params: argument names mapped to type specifications
        :type params: dict[str, Any]

        :return: registered function wrapper
        :rtype: SharedLibraryFunction
        """
        ...

    def get_function(self, item):
        """
        **LLM Docstring**

        Retrieve a registered function wrapper by tag.

        :param item: registered function tag
        :type item: str

        :return: registered wrapper
        :rtype: SharedLibraryFunction
        """
        ...

    def __getattr__(self, item):
        """
        **LLM Docstring**

        Resolve missing attributes as registered function tags.

        :param item: attribute name
        :type item: str

        :return: registered wrapper
        :rtype: SharedLibraryFunction
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation of the library facade.

        The current formatting expression passes a generator to `str.format` without a placeholder and therefore does not list the registered signatures.

        :return: representation string
        :rtype: str
        """
        ...