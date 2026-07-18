import os, collections
from ..SharedLibraryManager import SharedLibrary, SharedLibraryFunction
from .Module import FFIModule, FFIMethod, FFIArgument, FFIParameters, ThreadingMode

__all__ = [
    "DynamicFFIFunctionLoader",
    "DynamicFFIFunction",
    "DynamicFFILibrary"
]

class DynamicFFIFunctionLoader:
    """
    This is a singleton class that can be set to define the global
    linkage to the DynamicLibrary extension module
    """
    _loader=None
    _compile_args={}
    _lib_dir=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'libs', 'DynamicFFILibrary')
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
        cls._compile_args.update(compile_args)
    @classmethod
    def load(cls):
        """
        **LLM Docstring**

        Compile or load and cache the bundled dynamic FFI support module.

        :return: the singleton caller module
        :rtype: FFIModule
        """
        if cls._loader is None:
            cls._loader = FFIModule.from_lib(
                cls._lib_dir,
                **cls._compile_args
                # threaded=True,
                # extra_compile_args=(['-ftime-report'] if opts.time_report else []) + (
                #     ['-O0'] if opts.cmode == 'fast' else []),
                # include_dirs=['/usr/local/opt/llvm/include'],
                # runtime_dirs=['/usr/local/opt/llvm/lib', '/usr/local/opt/llvm/lib/c++'],
                # extra_link_args=['-mmacosx-version-min=12.0'],
                # recompile=opts.recompile
            )
        return cls._loader

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
        if cls._caller is None:
            cls._caller = DynamicFFIFunctionLoader.load()
        return cls._caller

    def __init__(self,
                 shared_library,
                 signature,
                 defaults=None,
                 docstring=None,
                 call_directory=None,
                 return_handler=None,
                 prep_args=None
                 ):
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
        super().__init__(shared_library, signature,
                         defaults=defaults, docstring=docstring,
                         call_directory=call_directory, return_handler=return_handler,
                         prep_args=prep_args
                         )
        self._ffi_args = None
        self._func_data = None
        self._call_info = []

    def initialize(self):
        """
        **LLM Docstring**

        Ensure the caller module is loaded and translate signature arguments to `FFIArgument` objects.

        :return: nothing; initializes `_ffi_args` lazily
        :rtype: None
        """
        # super().initialize()
        self._load_lib()
        if self._ffi_args is None:
            self._ffi_args = [
                FFIArgument.from_arg_sig(a) for a
                in self._sig.args
            ]

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
            self.library = lib
            self.name = name
            self.return_type = return_type
            self.args = args
            self.vectorized = vectorized
    @property
    def function_data(self):
        """
        **LLM Docstring**

        Build and cache the lightweight method metadata consumed by the dynamic caller.

        :return: the cached call descriptor
        :rtype: DynamicFFIFunction.LibFFIMethodData
        """
        if self._func_data is None:
            self.initialize()
            self._func_data = self.LibFFIMethodData(
                self._loader.lib,
                self._sig.name,
                FFIArgument.infer_dtype(self.signature.return_argtype.typechar),
                self._ffi_args
            )
        return self._func_data

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
        fdat = self.function_data # needs to be calculated here...
        if args is not None: # easy way to say no prep needed...
            kwargs = self._sig.populate_kwargs(args, kwargs, defaults=self.defaults) # populate args from ...
        params = FFIMethod.collect_args_from_list(self._ffi_args, **kwargs)
        req_attrs = ("arg_type", "arg_name", "arg_shape", "arg_value")
        if isinstance(params, (dict, collections.OrderedDict)):
            params = FFIParameters(params)
        for p in params:
            if not all(hasattr(p, x) for x in req_attrs):
                raise AttributeError("parameter {} needs attributes {}".format(p, req_attrs))
        callinfo = self._call_info.pop()
        debug = callinfo['debug']
        threading_vars = callinfo['threading_vars']
        threading_mode = callinfo['threading_mode']
        if threading_vars is not None:
            if isinstance(threading_vars, str):
                threading_vars = [threading_vars]
            if threading_mode is None:
                threading_mode = 'serial'
            if not isinstance(threading_mode, ThreadingMode):
                threading_mode = ThreadingMode(threading_mode)
            threading_mode = threading_mode.name
            res = self._caller.call_libffi_threaded.call(
                function_data=fdat, parameters=params,
                threading_vars=threading_vars, threading_mode=threading_mode, debug=debug
            )
        else:
            res = self._caller.call_libffi.call(function_data=fdat, parameters=params, debug=debug)
        return res, params

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
        # kinda hacky...
        self._call_info.append({
            'debug':debug,
            'threading_vars':threading_vars,
            'threading_mode':threading_mode
        })
        return super().call(*args, **kwargs)

class DynamicFFILibrary(SharedLibrary):
    """
    Directly analogous to a regular shared library but it uses
    `DynamicFFIFunction` to dispatch calls
    """
    method_type = DynamicFFIFunction

    def __init__(
            self,
            library,
            compiler_options=None,
            **functions
    ):
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
        super().__init__(library, **functions)
        self._loaded = False
        self.compiler_opts = compiler_options

    def get_function(self, item):
        """
        **LLM Docstring**

        Apply compiler options once on first access, then retrieve a registered function.

        :param item: registered function tag
        :type item: Any

        :return: the requested function
        :rtype: DynamicFFIFunction
        """
        if not self._loaded and self.compiler_opts is not None:
            self.configure_loader(**self.compiler_opts)
        self._loaded = True
        return super().get_function(item)

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
        DynamicFFIFunctionLoader.configure(**compile_opts)