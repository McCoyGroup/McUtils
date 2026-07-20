import enum, numpy as np, collections
__all__ = ['FFIModule', 'FFIMethod', 'FFIArgument', 'FFIType']

class FFIType(enum.Enum):
    """
    The set of supported enum types.
    Maps onto the native python convertable types and NumPy dtypes.
    In the future, this should be done more elegantly, but for now it suffices
    that these types align on the C++ side and this side.
    Only NumPy arrays are handled using the buffer interface & so if you want to pass a pointer
    you gotta do it using a NumPy array.
    """
    _type_map = {}
    GENERIC = -1
    Void = 1
    _type_map[Void] = ('void', None)
    PY_TYPES = 1000
    UnsignedChar = PY_TYPES + 10
    _type_map[UnsignedChar] = ('b', int)
    Short = PY_TYPES + 20
    _type_map[Short] = ('h', int)
    UnsignedShort = PY_TYPES + 21
    _type_map[UnsignedShort] = ('H', int)
    Int = PY_TYPES + 30
    _type_map[Int] = ('i', int)
    UnsignedInt = PY_TYPES + 31
    _type_map['I'] = UnsignedInt
    _type_map[UnsignedInt] = ('I', int)
    Long = PY_TYPES + 40
    _type_map[Long] = ('l', int)
    UnsignedLong = PY_TYPES + 41
    _type_map[UnsignedLong] = ('L', int)
    LongLong = PY_TYPES + 50
    _type_map['k'] = LongLong
    _type_map[LongLong] = ('k', int)
    UnsignedLongLong = PY_TYPES + 51
    _type_map['K'] = UnsignedLongLong
    _type_map[UnsignedLongLong] = ('K', int)
    PySizeT = PY_TYPES + 60
    _type_map[PySizeT] = ('n', int)
    Float = PY_TYPES + 70
    _type_map['f'] = Float
    _type_map[Float] = ('f', float)
    Double = PY_TYPES + 71
    _type_map['d'] = Double
    _type_map[Double] = ('d', float)
    Bool = PY_TYPES + 80
    _type_map[Bool] = ('p', bool)
    String = PY_TYPES + 90
    _type_map[String] = ('s', str)
    PyObject = PY_TYPES + 100
    _type_map['O'] = PyObject
    _type_map[PyObject] = ('O', object)
    Compound = PY_TYPES + 500
    _type_map[Compound] = ('compound', dict)
    NUMPY_TYPES = 2000
    NUMPY_Int8 = NUMPY_TYPES + 10
    _type_map[NUMPY_Int8] = ('int8', np.int8)
    NUMPY_UnsignedInt8 = NUMPY_TYPES + 11
    _type_map[NUMPY_UnsignedInt8] = ('uint8', np.uint8)
    NUMPY_Int16 = NUMPY_TYPES + 12
    _type_map[NUMPY_Int16] = ('int16', np.int16)
    NUMPY_UnsignedInt16 = NUMPY_TYPES + 13
    _type_map[NUMPY_UnsignedInt16] = ('uint16', np.uint16)
    NUMPY_Int32 = NUMPY_TYPES + 14
    _type_map[NUMPY_Int32] = ('int32', np.int32)
    NUMPY_UnsignedInt32 = NUMPY_TYPES + 15
    _type_map[NUMPY_UnsignedInt32] = ('uint32', np.uint32)
    NUMPY_Int64 = NUMPY_TYPES + 16
    _type_map[NUMPY_Int64] = ('int64', np.int64)
    NUMPY_UnsignedInt64 = NUMPY_TYPES + 17
    _type_map[NUMPY_UnsignedInt64] = ('uint64', np.uint64)
    NUMPY_Float16 = NUMPY_TYPES + 20
    _type_map[NUMPY_Float16] = ('float16', np.float16)
    NUMPY_Float32 = NUMPY_TYPES + 21
    _type_map[NUMPY_Float32] = ('float32', np.float32)
    NUMPY_Float64 = NUMPY_TYPES + 22
    _type_map[NUMPY_Float64] = ('float64', np.float64)
    NUMPY_Float128 = NUMPY_TYPES + 23
    _type_map[NUMPY_Float128] = ('float128', np_float128)
    NUMPY_Bool = NUMPY_TYPES + 30
    _type_map[NUMPY_Bool] = ('bool', bool)

    @classmethod
    def type_data(cls, val):
        """
        **LLM Docstring**

        Return the registered format string and Python/NumPy type for an FFI enum value.

        :param val: FFI type member or raw enum value to resolve
        :type val: Any

        :return: the `(format_code, Python_type)` pair stored in the enum type map
        :rtype: tuple[str, type | None]
        """
        ...
    _rev_map = {}

    @classmethod
    def resolve_ffi_type(cls, val):
        """
        **LLM Docstring**

        Resolve a format code, dtype name, or Python/NumPy type to an `FFIType` member.

        :param val: reverse-map key such as a format character, dtype name, or Python type
        :type val: Any

        :return: the matching FFI type; raises `KeyError` when no reverse mapping exists
        :rtype: FFIType
        """
        ...

class FFIContainerType(enum.Enum):
    Untyped = 0
    Raw = 1
    Vector = 2
    Array = 3

class DebugLevels(enum.Enum):
    Quiet = 0
    Normal = 5
    More = 10
    All = 50
    Excessive = 100

class ThreadingMode(enum.Enum):
    Serial = 'serial'
    OpenMP = 'omp'
    TBB = 'tbb'

class FFISpec:
    """
    Provides a uniform layout for handling specs of different parts of an FFI library
    """
    __fields__ = []

    def __init__(self, **kwargs):
        """
        **LLM Docstring**

        Validate keyword fields against the concrete specification class's required `__fields__` list.

        :param kwargs: field values supplied for the specification
        :type kwargs: dict[str, Any]

        :return: nothing; raises `ValueError` for missing, `None`, or unexpected fields
        :rtype: None
        """
        ...

class FFIArgument(FFISpec):
    """
    An argument spec for data to be passed to an FFIMethod
    """
    __fields__ = ['name', 'dtype', 'shape', 'container_type']

    def __init__(self, name=None, dtype=None, shape=None, container_type=None, value=None):
        """
        **LLM Docstring**

        Create an FFI argument specification and normalize its data and container types.

        :param name: argument name
        :type name: Any

        :param dtype: FFI type descriptor accepted by `infer_dtype`
        :type dtype: Any

        :param shape: declared argument shape; defaults to `()`
        :type shape: Any

        :param container_type: container representation accepted by `infer_ctype`
        :type container_type: Any

        :param value: unused compatibility parameter
        :type value: Any

        :return: nothing; initializes the argument metadata
        :rtype: None
        """
        ...
    _base_dtype_map = {'int8': FFIType}

    @classmethod
    def infer_dtype(cls, dtype):
        """
        **LLM Docstring**

        Normalize an enum, integer code, string, NumPy dtype, or mapped Python type to `FFIType`.

        :param dtype: type descriptor to normalize
        :type dtype: Any

        :return: the resolved FFI type
        :rtype: FFIType
        """
        ...

    @classmethod
    def infer_ctype(cls, container_type):
        """
        **LLM Docstring**

        Normalize a container-type enum, name, or numeric value to `FFIContainerType`.

        :param container_type: container representation descriptor
        :type container_type: Any

        :return: the resolved container type
        :rtype: FFIContainerType
        """
        ...

    @classmethod
    def from_arg_sig(cls, arg):
        """
        **LLM Docstring**

        Build an FFI argument from an `ArgumentSignature.Argument`-like object.

        :param arg: argument exposing `name`, `typechar`, `is_pointer()`, and `is_array()`
        :type arg: Any

        :return: an argument marked `Raw` for pointer/array signatures and `Untyped` otherwise
        :rtype: FFIArgument
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a constructor-style representation of the argument metadata.

        :return: the formatted argument representation
        :rtype: str
        """
        ...

    def cast(self, val):
        """

        :param val:
        :type val:
        :return:
        :rtype:
        """
        ...

class FFIParameter:
    """
    Just an FFIArgument + associated value
    """

    def __init__(self, arg, val):
        """
        **LLM Docstring**

        Associate a concrete value with an `FFIArgument` specification.

        :param arg: argument specification
        :type arg: Any

        :param val: value supplied for the argument
        :type val: Any

        :return: nothing; stores the argument and value
        :rtype: None
        """
        ...

    @property
    def arg_name(self):
        """
        **LLM Docstring**

        Expose the underlying argument name.

        :return: the argument name
        :rtype: str
        """
        ...

    @property
    def arg_type(self):
        """
        **LLM Docstring**

        Expose the normalized FFI data type.

        :return: the argument type
        :rtype: FFIType
        """
        ...

    @property
    def arg_shape(self):
        """
        **LLM Docstring**

        Return the declared shape, substituting the value's array shape when the declaration is empty or contains zero.

        :return: the effective argument shape
        :rtype: tuple
        """
        ...

    @property
    def container_type(self):
        """
        **LLM Docstring**

        Expose the argument container representation.

        :return: the container type
        :rtype: FFIContainerType
        """
        ...

    @property
    def arg_value(self):
        """
        **LLM Docstring**

        Return the argument value, converting sequence-like pointer/vector inputs to contiguous NumPy arrays in place.

        :return: the prepared argument value
        :rtype: Any
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation containing the parameter name, type, shape, and prepared value.

        :return: the formatted parameter representation
        :rtype: str
        """
        ...

class FFIParameters:
    """

    """

    def __init__(self, dats):
        """
        **LLM Docstring**

        Wrap a parameter collection and defer materializing its iterable and name map.

        :param dats: mapping or iterable of `FFIParameter` objects
        :type dats: Any

        :return: nothing; stores the collection
        :rtype: None
        """
        ...

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over the materialized FFI parameters.

        :return: an iterator over `ffi_parameters`
        :rtype: iterator
        """
        ...

    @property
    def ffi_parameters(self):
        """
        **LLM Docstring**

        Materialize and cache the parameter sequence, using mapping values when initialized from a mapping.

        :return: the cached parameter collection
        :rtype: Iterable[FFIParameter]
        """
        ...

    @property
    def ffi_map(self):
        """
        **LLM Docstring**

        Build and cache a mapping from argument names to parameter objects.

        :return: the parameter lookup map
        :rtype: dict[str, FFIParameter]
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Return the prepared value for a named parameter.

        :param item: argument name
        :type item: Any

        :return: the named parameter's `arg_value`
        :rtype: Any
        """
        ...

class FFIMethod(FFISpec):
    """
    Represents a C++ method callable through the plzffi interface
    """
    __fields__ = ['name', 'arguments', 'rtype', 'vectorized']

    def __init__(self, name=None, arguments=None, rtype=None, vectorized=None, module=None):
        """
        **LLM Docstring**

        Construct a callable method specification and bind each argument dictionary to `FFIArgument`.

        :param name: method name
        :type name: Any

        :param arguments: argument specifications
        :type arguments: Any

        :param rtype: numeric FFI return-type code
        :type rtype: Any

        :param vectorized: whether the method returns vectorized output
        :type vectorized: Any

        :param module: module used to dispatch calls
        :type module: Any

        :return: nothing; initializes the method metadata
        :rtype: None
        """
        ...

    def bind_module(self, mod):
        """
        **LLM Docstring**

        Attach the module that will execute this method.

        :param mod: FFI module wrapper
        :type mod: Any

        :return: nothing; updates `self.mod`
        :rtype: None
        """
        ...

    @property
    def arg_names(self):
        """
        **LLM Docstring**

        Return argument names in declaration order.

        :return: the method argument names
        :rtype: tuple[str, ...]
        """
        ...

    @classmethod
    def collect_args_from_list(cls, arg_list, *args, excluded_args=None, **kwargs):
        """
        **LLM Docstring**

        Match positional and keyword values to argument specifications, cast them, and reject missing required arguments.

        :param arg_list: ordered argument specifications
        :type arg_list: Any

        :param excluded_args: argument names to omit from required-value checks
        :type excluded_args: Any

        :param args: positional argument values
        :type args: tuple[Any, ...]

        :param kwargs: keyword argument values
        :type kwargs: dict[str, Any]

        :return: cast parameters in supplied order
        :rtype: collections.OrderedDict[str, FFIParameter]
        """
        ...

    def collect_args(self, *args, excluded_args=None, **kwargs):
        """
        **LLM Docstring**

        Collect and cast values using this method's declared arguments.

        :param excluded_args: argument names to omit
        :type excluded_args: Any

        :param args: positional argument values
        :type args: tuple[Any, ...]

        :param kwargs: keyword argument values
        :type kwargs: dict[str, Any]

        :return: the prepared parameter mapping
        :rtype: collections.OrderedDict[str, FFIParameter]
        """
        ...

    @classmethod
    def from_signature(cls, sig, module=None):
        """
        **LLM Docstring**

        Create a method specification from the four-part native signature tuple.

        :param sig: `(name, arguments, return_type, vectorized)` signature tuple
        :type sig: Any

        :param module: optional module to bind
        :type module: Any

        :return: the reconstructed method specification
        :rtype: FFIMethod
        """
        ...

    def call(self, *args, debug=False, **kwargs):
        """
        **LLM Docstring**

        Collect arguments and dispatch a non-threaded call through the bound module.

        :param debug: debug level selector passed to the module
        :type debug: Any

        :param args: positional argument values
        :type args: tuple[Any, ...]

        :param kwargs: keyword argument values
        :type kwargs: dict[str, Any]

        :return: the native method result
        :rtype: Any
        """
        ...

    def call_threaded(self, *args, threading_var=None, threading_mode='serial', debug=False, **kwargs):
        """
        **LLM Docstring**

        Collect arguments and dispatch through the module's threaded call path.

        :param threading_var: argument name used to partition work
        :type threading_var: Any

        :param threading_mode: threading backend name or mode
        :type threading_mode: Any

        :param debug: debug level selector
        :type debug: Any

        :param args: positional argument values
        :type args: tuple[Any, ...]

        :param kwargs: keyword argument values
        :type kwargs: dict[str, Any]

        :return: the threaded native method result
        :rtype: Any
        """
        ...

    def __call__(self, *args, threading_var=None, threading_mode='serial', debug=False, **kwargs):
        """
        **LLM Docstring**

        Dispatch serially unless a threading variable or non-serial threading mode is requested.

        :param threading_var: optional partitioning argument name
        :type threading_var: Any

        :param threading_mode: threading backend or `serial`
        :type threading_mode: Any

        :param debug: debug level selector
        :type debug: Any

        :param args: positional argument values
        :type args: tuple[Any, ...]

        :param kwargs: keyword argument values
        :type kwargs: dict[str, Any]

        :return: the native method result
        :rtype: Any
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation of the method name, argument specs, and scalar or vectorized return type.

        :return: the formatted method representation
        :rtype: str
        """
        ...

class FFIModule(FFISpec):
    """
    Provides a layer to ingest a Python module containing an '_FFIModule' capsule.
    The capsule is expected to point to a `plzffi::FFIModule` object and can be called using a `PotentialCaller`
    """
    __fields__ = ['name', 'methods']

    def __init__(self, name=None, methods=None, module=None):
        """
        **LLM Docstring**

        Construct an FFI module wrapper, normalize method dictionaries, and bind every method back to this module.

        :param name: module name
        :type name: Any

        :param methods: method specifications
        :type methods: Any

        :param module: underlying Python extension module
        :type module: Any

        :return: nothing; initializes the module wrapper
        :rtype: None
        """
        ...

    @property
    def captup(self):
        """
        **LLM Docstring**

        Return the extension module's `_FFIModule` capsule.

        :return: the native module capsule
        :rtype: object
        """
        ...

    @classmethod
    def from_lib(cls, name, src=None, threaded=None, extra_compile_args=None, extra_link_args=None, linked_libs=None, debug_level=False, **compile_kwargs):
        """
        **LLM Docstring**

        Compile or load an FFI extension through `FFILoader` and return its wrapped call object.

        :param name: library/module name
        :type name: Any

        :param src: source directory
        :type src: Any

        :param threaded: optional threaded-build override
        :type threaded: Any

        :param extra_compile_args: additional compiler arguments
        :type extra_compile_args: Any

        :param extra_link_args: additional linker arguments
        :type extra_link_args: Any

        :param linked_libs: additional libraries
        :type linked_libs: Any

        :param debug_level: debug setting for the wrapper
        :type debug_level: Any

        :param compile_kwargs: other `FFILoader` options
        :type compile_kwargs: dict[str, Any]

        :return: the loaded module wrapper
        :rtype: FFIModule
        """
        ...

    @classmethod
    def from_signature(cls, sig, module=None):
        """
        **LLM Docstring**

        Create a module wrapper from a native `(name, methods)` signature.

        :param sig: module signature tuple
        :type sig: Any

        :param module: underlying extension module
        :type module: Any

        :return: the reconstructed wrapper
        :rtype: FFIModule
        """
        ...

    @classmethod
    def get_debug_level(cls, debug):
        """
        **LLM Docstring**

        Convert booleans, enum names, enum values, and numeric values to the integer native debug level.

        :param debug: debug selector
        :type debug: Any

        :return: the numeric debug level
        :rtype: int | float
        """
        ...

    @classmethod
    def from_module(cls, module, debug=False):
        """
        **LLM Docstring**

        Query an extension module for its FFI signature and wrap it.

        :param module: extension exposing `get_signature` and `_FFIModule`
        :type module: Any

        :param debug: debug selector used while requesting the signature
        :type debug: Any

        :return: the module wrapper
        :rtype: FFIModule
        """
        ...

    @property
    def method_names(self):
        """
        **LLM Docstring**

        Return method names in declaration order.

        :return: the available method names
        :rtype: tuple[str, ...]
        """
        ...

    def get_method(self, name):
        """
        **LLM Docstring**

        Look up a method by name.

        :param name: method name
        :type name: Any

        :return: the matching method; raises `AttributeError` when absent
        :rtype: FFIMethod
        """
        ...

    def call_method(self, name, params, debug=False):
        """
        Calls a method

        :param name:
        :type name:
        :param params:
        :type params:
        :return:
        :rtype:
        """
        ...

    def call_method_threaded(self, name, params, thread_var, mode='serial', debug=False):
        """
        Calls a method with threading enabled

        :param name:
        :type name:
        :param params:
        :type params:
        :param thread_var:
        :type thread_var: str
        :param mode:
        :type mode:
        :return:
        :rtype:
        """
        ...

    def __getattr__(self, item):
        """
        **LLM Docstring**

        Resolve unknown attributes as FFI methods.

        :param item: requested method name
        :type item: Any

        :return: the matching method
        :rtype: FFIMethod
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation containing the module name and available method names.

        :return: the formatted module representation
        :rtype: str
        """
        ...