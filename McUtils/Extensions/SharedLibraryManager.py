"""
Defines a SharedLibrary object that makes it relatively straightforward to use
extensions direclty from .so files
"""

import os, ctypes
from .ArgumentSignature import FunctionSignature, Argument

__all__ = [
    "SharedLibrary",
    "SharedLibraryFunction"
]

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
        if not isinstance(shared_library, str):
            lib_file = shared_library._name # I'd prefer not to access private members but my options were limited
            if not os.path.isfile(lib_file):
                lib_file = None
        else:
            lib_file = shared_library
            shared_library = None
        self._lib = shared_library
        self._lib_file = lib_file

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
            self._to = dir_name
            self._from = None

        def __enter__(self):
            """
            **LLM Docstring**

            Save the current directory and change to the target directory.

            :return: the context manager does not return a value
            :rtype: None
            """
            self._from = os.getcwd()
            os.chdir(self._to)

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
            if self._from is not None:
                os.chdir(self._from)
            self._from = None

    def in_dir(self):
        """
        **LLM Docstring**

        Create a context manager for entering the library directory.

        :return: directory-changing context manager
        :rtype: SharedLibraryLoader.InDir
        """
        return self.InDir(self.lib_dir)

    @property
    def lib(self):
        """
        **LLM Docstring**

        Return the loaded library, loading it lazily when necessary.

        `ctypes.cdll.LoadLibrary` is executed while the process is in the library directory.

        :return: loaded shared-library handle
        :rtype: ctypes.CDLL
        """
        if self._lib is None:
            with self.in_dir():
                self._lib = ctypes.cdll.LoadLibrary(self._lib_file)
        return self._lib

    @property
    def lib_dir(self):
        """
        **LLM Docstring**

        Return the directory containing the configured library file.

        :return: library directory path
        :rtype: str
        """
        return os.path.dirname(self._lib_file)

class SharedLibraryFunction:
    """
    An object that provides a way to call into a shared library function
    """

    def __init__(self,
                 shared_library,
                 signature:FunctionSignature,
                 defaults=None,
                 docstring=None,
                 call_directory=None,
                 return_handler=None,
                 prep_args=None
                 ):
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
        if not isinstance(shared_library, SharedLibraryLoader):
            shared_library = SharedLibraryLoader(shared_library)
        self._loader = shared_library
        self._fun = None
        self._fname = None
        self._sig = signature
        self._doc = docstring
        # if call_directory is None:
        #     call_directory = self._loader.lib_dir
        self._dir = call_directory  # we could be kinder here and do stuff like add support for ".." and friends
        self.defaults = defaults
        if return_handler is None:
            return_handler = self._manage_return
        self.return_handler = return_handler
        self.arg_prepper = prep_args

    @classmethod
    def construct(cls,
                  name,
                  lib,
                  docstring=None,
                  defaults=None,
                  return_type=None,
                  return_handler=None,
                  **args
                  ):
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

        return cls(
            lib,
            FunctionSignature.construct(
                name
                **args,
                return_type=return_type
            ),
            docstring=docstring,
            defaults=defaults,
            return_handler=return_handler
        )

    @property
    def function(self):
        """
        **LLM Docstring**

        Initialize and return the underlying `ctypes` function.

        :return: configured foreign function
        :rtype: ctypes._CFuncPtr
        """
        self.initialize()
        return self._fun
    def initialize(self):
        """
        **LLM Docstring**

        Resolve the function from the library and apply its return and argument type declarations.

        Initialization is performed only once and cached in `_fun`.

        :return: no value is returned
        :rtype: None
        """
        if self._fun is None:
            # means we need to load it from the shared lib
            if self._fname is None:
                self._fname = self._sig.name
            self._fun = getattr(self._loader.lib, self._fname)

            # now initialize the arg signature
            self._fun.restype = self._sig.return_type
            self._fun.argtypes = self._sig.arg_types # need to figure out what type I need...
    def doc(self):
        """
        **LLM Docstring**

        Combine the generated C/C++ signature with the stored documentation string.

        :return: signature and documentation separated by a newline
        :rtype: str
        """
        return self._sig.cpp_signature+"\n"+self._doc
    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation containing the signature and loaded library.

        :return: representation string
        :rtype: str
        """
        return "{}({}, {})".format(
            type(self).__name__,
            self._sig,
            self._loader.lib
        )

    @property
    def signature(self):
        """
        **LLM Docstring**

        Return the stored function signature.

        :return: function signature
        :rtype: FunctionSignature
        """
        return self._sig

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
        return cls.uncast(res)
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
        if hasattr(res, '_obj'): #byref
            res = res._obj
        if hasattr(res, 'value'):
            res = res.value
        return res

    def _call(self, args, kwargs): # here to be overloaded
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
        args = self._sig.prep_args(args, kwargs, defaults=self.defaults)
        if self._dir is not None:
            with SharedLibraryLoader.InDir(self._dir):
                res = self.function(*args)
        else:
            res = self.function(*args)
        args = dict(zip((a.name for a in self._sig.args), args))
        return res, args

    def call(self, *args, **kwargs):
        """
        Calls the function we loaded.
        This will be parallelized out to handle more complicated usages.

        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        if self.arg_prepper is not None:
            kwargs = self._sig.populate_kwargs(args, kwargs,  defaults=self.defaults)
            args = None
            kwargs = self.arg_prepper(kwargs)
        res, args = self._call(args, kwargs)
        return self.return_handler(res, args)

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
        return self.call(*args, **kwargs)

class SharedLibrary:

    method_type = SharedLibraryFunction
    def __init__(
            self,
            library,
            **functions
    ):
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
        if not isinstance(library, SharedLibraryLoader):
            library = SharedLibraryLoader(library)
        self._loader = library
        self._functions = {}
        for k,v in functions.items():
            self.register(k, **v)
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
        if name is None:
            name = tag
        fn = self.method_type(
            self._loader,
            FunctionSignature.construct(name, **params),
            docstring=docstring,
            defaults=defaults,
            return_handler=return_handler,
            prep_args=prep_args
        )
        self._functions[tag] = fn
        return fn

    def get_function(self, item):
        """
        **LLM Docstring**

        Retrieve a registered function wrapper by tag.

        :param item: registered function tag
        :type item: str

        :return: registered wrapper
        :rtype: SharedLibraryFunction
        """
        if item in self._functions:
            return self._functions[item]
        else:
            raise ValueError("no shared library function {}".format(item))

    def __getattr__(self, item):
        """
        **LLM Docstring**

        Resolve missing attributes as registered function tags.

        :param item: attribute name
        :type item: str

        :return: registered wrapper
        :rtype: SharedLibraryFunction
        """
        return self.get_function(item)

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation of the library facade.

        The current formatting expression passes a generator to `str.format` without a placeholder and therefore does not list the registered signatures.

        :return: representation string
        :rtype: str
        """
        return "{}({})".format(
            type(self).__name__,
            ", ".format(repr(fn.sig) for fn in self._functions)
        )