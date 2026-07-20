### `ArgumentSignature.py` — Provides classes that are necessary for managing argument signatures
  - **class `ArgumentType`**
    > Defines a general purpose `ArgumentType` so that we can easily manage complicated type specs
    > The basic idea is to define a hierarchy of types that can then convert themselves down to
    > a `ctypes`-style spec as well as a C++ argument spec so that we can enable `SharedLibraryFunction`
    > to use either the basic `ctypes` FFI or a more efficient, but fragile system based off of extension modules.
    > This will be explicitly overridden by the `PrimitiveType`, `ArrayType` and `PointerType` subclasses that provide
    > the actual useable classes.
    > I'd really live to be integrate with what's in the `typing` module to be able to reuse that type-inference machinery
    - `ctypes_type()` — Return the `ctypes` representation used for foreign-function calls.
    - `cpp_type()` — Return the C/C++ spelling for this argument type.
    - `types()` — Return the accepted Python runtime types.
    - `dtypes()` — Return the accepted NumPy data types.
    - `typechar()` — Return the Python C-API format character for this type.
    - `isinstance(arg)` — Test whether a value is already compatible with this argument type.
    - `cast(arg)` — Convert a Python value to the corresponding Python-side representation.
    - `c_cast(arg)` — Convert a Python value to the object passed through `ctypes`.
  - **class `PrimitiveType`** (ArgumentType)
    > Defines a general purpose ArgumentType so that we can easily manage complicated type specs
    > The basic idea is to define a hierarchy of types that can then convert themselves down to
    > a `ctypes`-style spec as well as a C++ argument spec so that we can enable `SharedLibraryFunction`
    > to use either the basic `ctypes` FFI or a more efficient, but fragile system based off of extension modules
    - `__init__(name, ctypes_spec, cpp_spec, capi_spec, python_types, numpy_dtypes, serializer, deserializer)`
    - `name()` — **LLM Docstring**
    - `ctypes_type()` — Return the stored `ctypes` type specification.
    - `cpp_type()` — Return the stored C/C++ type spelling.
    - `types()` — **LLM Docstring**
    - `dtypes()` — **LLM Docstring**
    - `typechar()` — Return the stored Python C-API format character.
    - `isinstance(arg)` — Test whether a value belongs to one of the configured Python types.
    - `cast(arg)` — Cast a value with the first configured Python type.
    - `c_cast(arg)` — Cast a value to the configured `ctypes` scalar.
  - **class `ArrayType`** (ArgumentType)
    > Extends the basic `ArgumentType` spec to handle array types of possibly fixed size.
    > To start, we're only adding in proper support for numpy arrays.
    > Other flavors might come, but given the use case, it's unlikely.
    - `__init__(base_type, shape=None, ctypes_spec=None)`
    - `ctypes_type()` — Return or lazily create a C-contiguous NumPy `ndpointer` specification.
    - `cpp_type()` — Return the pointer-like C/C++ type string formed from the cached `ctypes` specification.
    - `types()` — Return the accepted Python container type, `numpy.ndarray`.
    - `dtypes()` — Return the element dtypes accepted by the base type.
    - `typechar()` — Return the Python C-API format character of the base type.
    - `isinstance(arg)` — Test whether a value is a NumPy array with an accepted base dtype.
    - `cast(arg)` — Convert a value to an array using the first accepted base dtype.
    - `c_cast(arg)` — Convert a value to a C-contiguous NumPy array of the required dtype.
  - **class `PointerType`** (ArgumentType)
    > Extends the basic `ArgumentType` spec to handle pointer types
    - `__init__(base_type)`
    - `ctypes_type()` — Return or lazily create a `ctypes.POINTER` to the base type.
    - `cpp_type()` — Return the pointer-like C/C++ type string formed from the cached `ctypes` specification.
    - `types()` — Return the Python types accepted by the base type.
    - `dtypes()` — Return the NumPy dtypes accepted by the base type.
    - `typechar()` — Return the Python C-API format character of the base type.
    - `isinstance(arg)` — Delegate compatibility testing to the base type.
    - `cast(arg)` — Delegate Python-side conversion to the base type.
    - `c_cast(arg)` — Convert a value with the base type and return a `ctypes.byref` pointer to it.
  - **class `Argument`**
    > Defines a single Argument for a C-level caller to support default values, etc.
    > We use a two-pronged approach where we have a set of ArgumentType serializers/deserializers
    - `__init__(name, dtype, default=None)`
    - `infer_type(arg)` — Infers the type of an argument
    - `infer_type_type(type_key)` — Look up an argument type from a Python type object.
    - `infer_type_str(argstr)` — Resolve an argument type from a string specification.
    - `inferred_type_string(arg)` — returns a type string for the inferred type
    - `prep_value(val)` — Convert a value to the C-call representation required by this argument.
    - `is_pointer()` — Test whether this argument uses a `PointerType`.
    - `is_array()` — Test whether this argument uses an `ArrayType`.
    - `dtypes()` — Return the NumPy dtypes accepted by this argument type.
    - `typechar()` — Return the Python C-API format character for this argument type.
    - `cpp_signature()` — Format this argument as a C/C++ declaration fragment.
  - **class `FunctionSignature`**
    > Defines a function signature for a C-level caller.
    > To be used inside `SharedLibraryFunction` and things to manage the core interface.
    - `__init__(name, *args, defaults=None, return_type=None)`
    - `construct(name, defaults=None, return_type=None, **args)` — Construct a signature from keyword argument type specifications.
    - `build_argument(argtup, which=None)` — Converts an argument tuple into an Argument object
    - `args()` — **LLM Docstring**
    - `return_argtype()` — **LLM Docstring**
    - `return_type()` — Return the `ctypes` return type used to configure a foreign function.
    - `arg_types()` — Return the ordered `ctypes` types for all arguments.
    - `cpp_signature()` — Format the complete C/C++-style function signature.
    - `populate_kwargs(args, kwargs, defaults=None)` — Merge positional and keyword arguments and fill missing entries from defaults.
    - `prep_args(args, kwargs, defaults=None)` — Prepare arguments in signature order for a foreign-function call.

### `CLoader.py`
  - **class `CLoader`**
    > A general loader for C++ extensions to python, based off of the kind of thing that I have had to do multiple times
    - `__init__(lib_name, lib_dir=None, load_path=None, src_ext='src', libs_ext='libs', description='An extension module', version='1.0.0', include_dirs=None, runtime_dirs=None, linked_libs=None, macros=None, extra_link_args=None, extra_compile_args=None, extra_objects=None, source_files=None, build_script=None, requires_make=True, out_dir=None, cleanup_build=True, recompile=False)`
    - `load()` — Find or compile the configured extension and import it.
    - `find_extension()` — Tries to find the extension in the top-level directory
    - `compile_extension()` — Compiles and loads a C++ extension
    - `src_dir()` — **LLM Docstring**
    - `lib_lib_dir()` — **LLM Docstring**
    - `get_extension()` — Gets the Extension module to be compiled
    - `configure_make_command(make_file)` — Translate a make configuration dictionary into compiler and linker command argument lists.
    - `custom_make(make_file, make_dir)` — A way to call a custom make file either for building the helper lib or for building the proper lib
    - `make_required_libs(library_types=('.so', '.pyd', '.dll'))` — Makes any libs required by the current one
    - `build_lib()` — Build the extension in its source directory.
    - `locate_library(libname, roots, extensions, library_types=('.so', '.pyd', '.dll'))` — Tries to locate the library file (if it exists)
    - `locate_lib(name=None, roots=None, extensions=None, library_types=('.so', '.pyd', '.dll'))` — Tries to locate the build library file (if it exists)
    - `cleanup()` — Move the built extension to its output directory and optionally remove build artifacts.

### `ModuleLoader.py`
  - **class `DynamicModuleLoader`** (importlib.abc.SourceLoader)
    > A `DynamicModuleLoader` is a Loader object that can load a python module from a file path.
    > Primarily intended for workflows that don't support `importlib.import_module`
    - `__init__(rootdir='', rootpkg=None, retag=True)`
    - `get_data(file)` — Read source data from a file in binary mode.
    - `get_filename(fullname)` — Resolve a module name or path to the Python source file this loader should execute.
    - `get_spec(file, pkg=None)` — Build an import specification for a source file.
    - `reregister_module(module, tag=None)` — Sets up a secondary hook for a module so it's clear which
    - `load(file, pkg=None)` — loads a file as a module with optional package name
  - **class `ModuleLoader`**
    > Provides a way to load dynamic modules.
    > Either use a `DynamicModuleLoader` or the `importlib.import_module` function
    > depending on how much customization is needed.
    - `__init__(rootdir='', rootpkg=None, retag=False)`
    - `load(file, pkg=None)` — Load and return a Python module from a path or import name.

### `SharedLibraryManager.py` — Defines a SharedLibrary object that makes it relatively straightforward to use
  - **class `SharedLibraryLoader`**
    - `__init__(shared_library)`
    - **class `InDir`**
      > A super simple context manager that manages going into a directory and then leaving when finished
      - `__init__(dir_name)`
    - `in_dir()` — Create a context manager for entering the library directory.
    - `lib()` — Return the loaded library, loading it lazily when necessary.
    - `lib_dir()` — Return the directory containing the configured library file.
  - **class `SharedLibraryFunction`**
    > An object that provides a way to call into a shared library function
    - `__init__(shared_library, signature, defaults=None, docstring=None, call_directory=None, return_handler=None, prep_args=None)`
    - `construct(name, lib, docstring=None, defaults=None, return_type=None, return_handler=None, **args)` — Construct a shared-library function from a name and keyword type specifications.
    - `function()` — Initialize and return the underlying `ctypes` function.
    - `initialize()` — Resolve the function from the library and apply its return and argument type declarations.
    - `doc()` — Combine the generated C/C++ signature with the stored documentation string.
    - `signature()` — **LLM Docstring**
    - `uncast(res)` — Unwrap common `ctypes` by-reference and scalar containers.
    - `call(*args, **kwargs)` — This will be parallelized out to handle more complicated usages.
  - **class `SharedLibrary`**
    - `__init__(library, **functions)`
    - `register(tag, name=None, docstring=None, defaults=None, return_handler=None, prep_args=None, **params)` — Register and return a callable wrapper for one library function.
    - `get_function(item)` — Retrieve a registered function wrapper by tag.

### `FFI/DynamicFFILibrary.py`
  - **class `DynamicFFIFunctionLoader`**
    > This is a singleton class that can be set to define the global
    > linkage to the DynamicLibrary extension module
    - `configure(**compile_args)` — Merge compiler options into the process-wide dynamic FFI loader configuration.
    - `load()` — Compile or load and cache the bundled dynamic FFI support module.
  - **class `DynamicFFIFunction`** (SharedLibraryFunction)
    > Specialization of base `SharedLibraryFunction` to call
    > through the `DynamicLibrary` module instead of `ctypes`
    - `__init__(shared_library, signature, defaults=None, docstring=None, call_directory=None, return_handler=None, prep_args=None)`
    - `initialize()` — Ensure the caller module is loaded and translate signature arguments to `FFIArgument` objects.
    - **class `LibFFIMethodData`**
      - `__init__(lib, name, return_type, args, vectorized=False)`
    - `function_data()` — Build and cache the lightweight method metadata consumed by the dynamic caller.
  - **class `DynamicFFILibrary`** (SharedLibrary)
    > Directly analogous to a regular shared library but it uses
    > `DynamicFFIFunction` to dispatch calls
    - `__init__(library, compiler_options=None, **functions)`
    - `get_function(item)` — Apply compiler options once on first access, then retrieve a registered function.
    - `configure_loader(**compile_opts)` — Forward compile options to the singleton dynamic FFI loader.

### `FFI/Loader.py` — Provides a Loader object to load a potential from a C++ extension
- `brew_prefix_for_arch(pkg)` — Locate a Homebrew package prefix by probing architecture-preferred Homebrew installations.
- `find_libffi()` — Return (include_dir, lib_dir) for a user-installed libffi, or None.
  - **class `FFILoader`**
    > Provides a standardized way to load and compile a potential using a potential template
    - `__init__(name, src=None, src_ext='src', load_path=None, description='A compiled potential', version='1.0.0', include_dirs=None, linked_libs=None, runtime_dirs=None, macros=None, source_files=None, build_script=None, requires_make=True, out_dir=None, cleanup_build=True, pointer_name=None, build_kwargs=None, nodebug=False, threaded=False, manage_threading_flags=True, manage_libffi_flags=True, extra_compile_args=None, extra_link_args=None, recompile=False, debug_level=False)`
    - `lib()` — Load and cache the compiled extension module.
    - `caller_api_version()` — Detect the extension calling API from the presence of `_FFIModule`.
    - `call_obj()` — The object that defines how to call the potential.

### `FFI/Module.py`
  - **class `FFIType`** (enum.Enum)
    > The set of supported enum types.
    > Maps onto the native python convertable types and NumPy dtypes.
    > In the future, this should be done more elegantly, but for now it suffices
    > that these types align on the C++ side and this side.
    > Only NumPy arrays are handled using the buffer interface & so if you want to pass a pointer
    > you gotta do it using a NumPy array.
    - `type_data(val)` — Return the registered format string and Python/NumPy type for an FFI enum value.
    - `resolve_ffi_type(val)` — Resolve a format code, dtype name, or Python/NumPy type to an `FFIType` member.
  - **class `FFIContainerType`** (enum.Enum)
  - **class `DebugLevels`** (enum.Enum)
  - **class `ThreadingMode`** (enum.Enum)
  - **class `FFISpec`**
    > Provides a uniform layout for handling specs of different parts of an FFI library
    - `__init__(**kwargs)`
  - **class `FFIArgument`** (FFISpec)
    > An argument spec for data to be passed to an FFIMethod
    - `__init__(name=None, dtype=None, shape=None, container_type=None, value=None)`
    - `infer_dtype(dtype)` — Normalize an enum, integer code, string, NumPy dtype, or mapped Python type to `FFIType`.
    - `infer_ctype(container_type)` — Normalize a container-type enum, name, or numeric value to `FFIContainerType`.
    - `from_arg_sig(arg)` — Build an FFI argument from an `ArgumentSignature.Argument`-like object.
    - `cast(val)` — :param val:
  - **class `FFIParameter`**
    > Just an FFIArgument + associated value
    - `__init__(arg, val)`
    - `arg_name()` — **LLM Docstring**
    - `arg_type()` — Expose the normalized FFI data type.
    - `arg_shape()` — Return the declared shape, substituting the value's array shape when the declaration is empty or co…
    - `container_type()` — **LLM Docstring**
    - `arg_value()` — Return the argument value, converting sequence-like pointer/vector inputs to contiguous NumPy array…
  - **class `FFIParameters`**
    - `__init__(dats)`
    - `ffi_parameters()` — Materialize and cache the parameter sequence, using mapping values when initialized from a mapping.
    - `ffi_map()` — Build and cache a mapping from argument names to parameter objects.
  - **class `FFIMethod`** (FFISpec)
    > Represents a C++ method callable through the plzffi interface
    - `__init__(name=None, arguments=None, rtype=None, vectorized=None, module=None)`
    - `bind_module(mod)` — Attach the module that will execute this method.
    - `arg_names()` — Return argument names in declaration order.
    - `collect_args_from_list(arg_list, *args, excluded_args=None, **kwargs)` — Match positional and keyword values to argument specifications, cast them, and reject missing requi…
    - `collect_args(*args, excluded_args=None, **kwargs)` — Collect and cast values using this method's declared arguments.
    - `from_signature(sig, module=None)` — Create a method specification from the four-part native signature tuple.
    - `call(*args, debug=False, **kwargs)` — Collect arguments and dispatch a non-threaded call through the bound module.
    - `call_threaded(*args, threading_var=None, threading_mode='serial', debug=False, **kwargs)` — Collect arguments and dispatch through the module's threaded call path.
  - **class `FFIModule`** (FFISpec)
    > Provides a layer to ingest a Python module containing an '_FFIModule' capsule.
    > The capsule is expected to point to a `plzffi::FFIModule` object and can be called using a `PotentialCaller`
    - `__init__(name=None, methods=None, module=None)`
    - `captup()` — Return the extension module's `_FFIModule` capsule.
    - `from_lib(name, src=None, threaded=None, extra_compile_args=None, extra_link_args=None, linked_libs=None, debug_level=False, **compile_kwargs)` — Compile or load an FFI extension through `FFILoader` and return its wrapped call object.
    - `from_signature(sig, module=None)` — Create a module wrapper from a native `(name, methods)` signature.
    - `get_debug_level(debug)` — Convert booleans, enum names, enum values, and numeric values to the integer native debug level.
    - `from_module(module, debug=False)` — Query an extension module for its FFI signature and wrap it.
    - `method_names()` — Return method names in declaration order.
    - `get_method(name)` — Look up a method by name.
    - `call_method(name, params, debug=False)` — Calls a method
    - `call_method_threaded(name, params, thread_var, mode='serial', debug=False)` — Calls a method with threading enabled