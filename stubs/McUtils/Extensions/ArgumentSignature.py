"""
Provides classes that are necessary for managing argument signatures
"""
__all__ = ['ArgumentType', 'ArrayType', 'PointerType', 'PrimitiveType', 'RealType', 'IntType', 'BoolType', 'Argument', 'FunctionSignature']
import abc, ctypes, numpy as np, numpy.ctypeslib as npctypes, re

class ArgumentType(metaclass=abc.ABCMeta):
    """
    Defines a general purpose `ArgumentType` so that we can easily manage complicated type specs
    The basic idea is to define a hierarchy of types that can then convert themselves down to
    a `ctypes`-style spec as well as a C++ argument spec so that we can enable `SharedLibraryFunction`
    to use either the basic `ctypes` FFI or a more efficient, but fragile system based off of extension modules.
    This will be explicitly overridden by the `PrimitiveType`, `ArrayType` and `PointerType` subclasses that provide
    the actual useable classes.
    I'd really live to be integrate with what's in the `typing` module to be able to reuse that type-inference machinery
    """

    @property
    @abc.abstractmethod
    def ctypes_type(self):
        """
        **LLM Docstring**

        Return the `ctypes` representation used for foreign-function calls.

        Subclasses must implement this abstract property.

        :return: the `ctypes` representation used for foreign-function calls
        :rtype: type | None
        """
        ...

    @property
    @abc.abstractmethod
    def cpp_type(self):
        """
        **LLM Docstring**

        Return the C/C++ spelling for this argument type.

        Subclasses must implement this abstract property.

        :return: the C/C++ spelling for this argument type
        :rtype: str
        """
        ...

    @property
    @abc.abstractmethod
    def types(self):
        """
        **LLM Docstring**

        Return the accepted Python runtime types.

        Subclasses must implement this abstract property.

        :return: the accepted Python runtime types
        :rtype: tuple[type, ...]
        """
        ...

    @property
    @abc.abstractmethod
    def dtypes(self):
        """
        **LLM Docstring**

        Return the accepted NumPy data types.

        Subclasses must implement this abstract property.

        :return: the accepted NumPy data types
        :rtype: tuple[np.dtype, ...]
        """
        ...

    @property
    @abc.abstractmethod
    def typechar(self):
        """
        **LLM Docstring**

        Return the Python C-API format character for this type.

        Subclasses must implement this abstract property.

        :return: the Python C-API format character for this type
        :rtype: str
        """
        ...

    @abc.abstractmethod
    def isinstance(self, arg):
        """
        **LLM Docstring**

        Test whether a value is already compatible with this argument type.

        Subclasses must implement this abstract operation.

        :param arg: value to inspect or convert
        :type arg: Any

        :return: whether a value is already compatible with this argument type
        :rtype: bool
        """
        ...

    @abc.abstractmethod
    def cast(self, arg):
        """
        **LLM Docstring**

        Convert a Python value to the corresponding Python-side representation.

        Subclasses must implement this abstract operation.

        :param arg: value to inspect or convert
        :type arg: Any

        :return: converted a Python value to the corresponding Python-side representation
        :rtype: Any
        """
        ...

    @abc.abstractmethod
    def c_cast(self, arg):
        """
        **LLM Docstring**

        Convert a Python value to the object passed through `ctypes`.

        Subclasses must implement this abstract operation.

        :param arg: value to inspect or convert
        :type arg: Any

        :return: converted a Python value to the object passed through `ctypes`
        :rtype: Any
        """
        ...

class PrimitiveType(ArgumentType):
    """
    Defines a general purpose ArgumentType so that we can easily manage complicated type specs
    The basic idea is to define a hierarchy of types that can then convert themselves down to
    a `ctypes`-style spec as well as a C++ argument spec so that we can enable `SharedLibraryFunction`
    to use either the basic `ctypes` FFI or a more efficient, but fragile system based off of extension modules
    """
    typeset = {}

    def __init__(self, name, ctypes_spec, cpp_spec, capi_spec, python_types, numpy_dtypes, serializer, deserializer):
        """
        :param name: argument name (e.g. 'double')
        :type name: str
        :param ctypes_spec: the ctypes data-type that arguments of this type would be converted to
        :type ctypes_spec:
        :param cpp_spec: the C++ spec for this type (as a string)
        :type cpp_spec: str
        :param capi_spec: the python C-API string for use in `Py_BuildValue`
        :type capi_spec: str
        :param python_types: the python types that this argument maps onto
        :type python_types: Iterable[type]
        :param numpy_dtypes: the numpy dtypes that this argument maps onto
        :type numpy_dtypes: Iterable[np.dtype]
        :param serializer: a serializer for converting this object into a byte-stream
        :type serializer: Callable
        :param deserializer: a deserializer for converting the byte-stream into a C-level object
        :type deserializer: Callable
        """
        ...

    @property
    def name(self):
        """
        **LLM Docstring**

        Return the descriptive type name.

        :return: the descriptive type name
        :rtype: str
        """
        ...

    @property
    def ctypes_type(self):
        """
        **LLM Docstring**

        Return the stored `ctypes` type specification.

        :return: the stored `ctypes` type specification
        :rtype: type | None
        """
        ...

    @property
    def cpp_type(self):
        """
        **LLM Docstring**

        Return the stored C/C++ type spelling.

        :return: the stored C/C++ type spelling
        :rtype: str
        """
        ...

    @property
    def types(self):
        """
        **LLM Docstring**

        Return the accepted Python types.

        :return: the accepted Python types
        :rtype: tuple[type, ...]
        """
        ...

    @property
    def dtypes(self):
        """
        **LLM Docstring**

        Return the accepted NumPy dtypes.

        :return: the accepted NumPy dtypes
        :rtype: tuple[np.dtype, ...]
        """
        ...

    @property
    def typechar(self):
        """
        **LLM Docstring**

        Return the stored Python C-API format character.

        :return: the stored Python C-API format character
        :rtype: str
        """
        ...

    def isinstance(self, arg):
        """
        **LLM Docstring**

        Test whether a value belongs to one of the configured Python types.

        :param arg: value to test
        :type arg: Any

        :return: `True` when `arg` is an instance of an accepted type
        :rtype: bool
        """
        ...

    def cast(self, arg):
        """
        **LLM Docstring**

        Cast a value with the first configured Python type.

        :param arg: value to convert
        :type arg: Any

        :return: Python-side converted value
        :rtype: Any
        """
        ...

    def c_cast(self, arg):
        """
        **LLM Docstring**

        Cast a value to the configured `ctypes` scalar.

        The value is first converted with `cast`.

        :param arg: value to convert
        :type arg: Any

        :return: `ctypes` scalar instance
        :rtype: Any
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a concise representation containing the wrapper class and primitive name.

        :return: representation string
        :rtype: str
        """
        ...

class ArrayType(ArgumentType):
    """
    Extends the basic `ArgumentType` spec to handle array types of possibly fixed size.
    To start, we're only adding in proper support for numpy arrays.
    Other flavors might come, but given the use case, it's unlikely.
    """

    def __init__(self, base_type, shape=None, ctypes_spec=None):
        """
        **LLM Docstring**

        Create an array argument type around a primitive base type.

        :param base_type: element type used for dtype checks and conversion
        :type base_type: ArgumentType

        :param shape: stored optional shape metadata; it is not enforced by current methods
        :type shape: tuple[int, ...] | None

        :param ctypes_spec: optional precomputed `ctypes` array specification
        :type ctypes_spec: Any | None

        :return: no value is returned
        :rtype: None
        """
        ...

    @property
    def ctypes_type(self):
        """
        **LLM Docstring**

        Return or lazily create a C-contiguous NumPy `ndpointer` specification.

        :return: or lazily create a C-contiguous NumPy `ndpointer` specification
        :rtype: Any
        """
        ...

    @property
    def cpp_type(self):
        """
        **LLM Docstring**

        Return the pointer-like C/C++ type string formed from the cached `ctypes` specification.

        :return: the pointer-like C/C++ type string formed from the cached `ctypes` specification
        :rtype: str
        """
        ...

    @property
    def types(self):
        """
        **LLM Docstring**

        Return the accepted Python container type, `numpy.ndarray`.

        :return: the accepted Python container type, `numpy.ndarray`
        :rtype: tuple[type, ...]
        """
        ...

    @property
    def dtypes(self):
        """
        **LLM Docstring**

        Return the element dtypes accepted by the base type.

        :return: the element dtypes accepted by the base type
        :rtype: tuple[np.dtype, ...]
        """
        ...

    @property
    def typechar(self):
        """
        **LLM Docstring**

        Return the Python C-API format character of the base type.

        :return: the Python C-API format character of the base type
        :rtype: str
        """
        ...

    def isinstance(self, arg):
        """
        **LLM Docstring**

        Test whether a value is a NumPy array with an accepted base dtype.

        :param arg: value to test
        :type arg: Any

        :return: compatibility flag
        :rtype: bool
        """
        ...

    def cast(self, arg):
        """
        **LLM Docstring**

        Convert a value to an array using the first accepted base dtype.

        :param arg: array-like value
        :type arg: Any

        :return: converted NumPy array
        :rtype: np.ndarray
        """
        ...

    def c_cast(self, arg):
        """
        **LLM Docstring**

        Convert a value to a C-contiguous NumPy array of the required dtype.

        :param arg: array-like value
        :type arg: Any

        :return: contiguous converted array
        :rtype: np.ndarray
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a concise representation containing the array wrapper and base type.

        :return: representation string
        :rtype: str
        """
        ...

class PointerType(ArgumentType):
    """
    Extends the basic `ArgumentType` spec to handle pointer types
    """

    def __init__(self, base_type):
        """
        :param base_type: The base type we're building off of
        :type base_type: ArgumentType
        """
        ...

    @property
    def ctypes_type(self):
        """
        **LLM Docstring**

        Return or lazily create a `ctypes.POINTER` to the base type.

        :return: or lazily create a `ctypes.POINTER` to the base type
        :rtype: Any
        """
        ...

    @property
    def cpp_type(self):
        """
        **LLM Docstring**

        Return the pointer-like C/C++ type string formed from the cached `ctypes` specification.

        :return: the pointer-like C/C++ type string formed from the cached `ctypes` specification
        :rtype: str
        """
        ...

    @property
    def types(self):
        """
        **LLM Docstring**

        Return the Python types accepted by the base type.

        :return: the Python types accepted by the base type
        :rtype: tuple[type, ...]
        """
        ...

    @property
    def dtypes(self):
        """
        **LLM Docstring**

        Return the NumPy dtypes accepted by the base type.

        :return: the NumPy dtypes accepted by the base type
        :rtype: tuple[np.dtype, ...]
        """
        ...

    @property
    def typechar(self):
        """
        **LLM Docstring**

        Return the Python C-API format character of the base type.

        :return: the Python C-API format character of the base type
        :rtype: str
        """
        ...

    def isinstance(self, arg):
        """
        **LLM Docstring**

        Delegate compatibility testing to the base type.

        :param arg: value to test
        :type arg: Any

        :return: compatibility flag
        :rtype: bool
        """
        ...

    def cast(self, arg):
        """
        **LLM Docstring**

        Delegate Python-side conversion to the base type.

        :param arg: value to convert
        :type arg: Any

        :return: converted base value
        :rtype: Any
        """
        ...

    def c_cast(self, arg):
        """
        **LLM Docstring**

        Convert a value with the base type and return a `ctypes.byref` pointer to it.

        :param arg: value to convert
        :type arg: Any

        :return: by-reference `ctypes` object
        :rtype: Any
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a concise representation containing the pointer wrapper and base type.

        :return: representation string
        :rtype: str
        """
        ...
VoidType = PrimitiveType('void', None, 'void', 'void', (), (), None, None)
RealType = PrimitiveType('Real', ctypes.c_double, 'double', 'd', (float,), (np.dtype('float64'),), None, None)
IntegerType = PrimitiveType('int', ctypes.c_int64, 'int', 'i', (int,), (np.dtype('int64'),), None, None)
BoolType = PrimitiveType('bool', ctypes.c_bool, 'bool', 'p', (bool,), (np.dtype('bool'),), None, None)
FloatType = PrimitiveType('float', ctypes.c_float, 'float', 'f', (float,), (np.dtype('float32'),), None, None)
DoubleType = PrimitiveType('double', ctypes.c_double, 'double', 'd', (float,), (np.dtype('float64'),), None, None)
IntType = PrimitiveType('int', ctypes.c_int32, 'int', 'i', (int,), (np.dtype('int32'),), None, None)
LongType = PrimitiveType('long', ctypes.c_int64, 'long', 'i', (int,), (np.dtype('int64'),), None, None)

class Argument:
    """
    Defines a single Argument for a C-level caller to support default values, etc.
    We use a two-pronged approach where we have a set of ArgumentType serializers/deserializers
    """
    arg_types = [VoidType, RealType, IntType, BoolType]

    def __init__(self, name, dtype, default=None):
        """
        :param name: the name of the argument
        :type name: str
        :param dtype: the type of the argument; at some point we'll support type inference...
        :type dtype: ArgumentType
        :param default: the default value for the argument
        :type default:
        """
        ...

    @classmethod
    def infer_type(cls, arg):
        """
        Infers the type of an argument

        :param arg:
        :type arg: ArgumentType | str | type | ctypes type
        :return:
        :rtype:
        """
        ...
    _typesets = None
    _typestrs = None

    @classmethod
    def _prep_typesets(cls):
        """
        **LLM Docstring**

        Populate class-level lookup tables for Python types and C/C++ type strings.

        Existing mappings are preserved by only initializing when either cache is missing.

        :return: no value is returned
        :rtype: None
        """
        ...

    @classmethod
    def infer_type_type(cls, type_key):
        """
        **LLM Docstring**

        Look up an argument type from a Python type object.

        :param type_key: Python type to resolve
        :type type_key: type

        :return: matching registered argument type, or `None`
        :rtype: ArgumentType | None
        """
        ...

    @classmethod
    def infer_type_str(cls, argstr):
        """
        **LLM Docstring**

        Resolve an argument type from a string specification.

        Checks registered mappings first, then attempts the module's pointer-pattern branch. That branch constructs an `ArrayType`; malformed or unmatched strings return `None`.

        :param argstr: type spelling to resolve
        :type argstr: str

        :return: resolved argument type or `None`
        :rtype: ArgumentType | None
        """
        ...

    @classmethod
    def inferred_type_string(cls, arg):
        """
        returns a type string for the inferred type
        """
        ...

    def prep_value(self, val):
        """
        **LLM Docstring**

        Convert a value to the C-call representation required by this argument.

        :param val: Python value to prepare
        :type val: Any

        :return: converted value
        :rtype: Any
        """
        ...

    def is_pointer(self):
        """
        **LLM Docstring**

        Test whether this argument uses a `PointerType`.

        :return: pointer-type flag
        :rtype: bool
        """
        ...

    def is_array(self):
        """
        **LLM Docstring**

        Test whether this argument uses an `ArrayType`.

        :return: array-type flag
        :rtype: bool
        """
        ...

    @property
    def dtypes(self):
        """
        **LLM Docstring**

        Return the NumPy dtypes accepted by this argument type.

        :return: accepted dtypes
        :rtype: tuple[np.dtype, ...]
        """
        ...

    @property
    def typechar(self):
        """
        **LLM Docstring**

        Return the Python C-API format character for this argument type.

        :return: format character
        :rtype: str
        """
        ...

    @property
    def cpp_signature(self):
        """
        **LLM Docstring**

        Format this argument as a C/C++ declaration fragment.

        :return: string of the form `<type> <name>`
        :rtype: str
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation containing the argument name and resolved type.

        :return: representation string
        :rtype: str
        """
        ...

class FunctionSignature:
    """
    Defines a function signature for a C-level caller.
    To be used inside `SharedLibraryFunction` and things to manage the core interface.
    """

    def __init__(self, name, *args, defaults=None, return_type=None):
        """
        :param name: the name of the function
        :type name: str
        :param args: the arguments passed to the function
        :type args: Iterable[ArgumentType]
        :param return_type: the return type of the function
        :type return_type: ArgumentType | None
        """
        ...

    @classmethod
    def construct(cls, name, defaults=None, return_type=None, **args):
        """
        **LLM Docstring**

        Construct a signature from keyword argument type specifications.

        Keyword insertion order determines positional argument order.

        :param name: function name
        :type name: str

        :param defaults: default values keyed by argument name
        :type defaults: dict | None

        :param return_type: return type specification accepted by `Argument.infer_type`
        :type return_type: Any | None

        :param args: argument names mapped to type specifications
        :type args: dict[str, Any]

        :return: new function signature
        :rtype: FunctionSignature
        """
        ...

    def build_argument(self, argtup, which=None):
        """
        Converts an argument tuple into an Argument object
        :param argtup:
        :type argtup:
        :return:
        :rtype:
        """
        ...

    @property
    def args(self):
        """
        **LLM Docstring**

        Return the immutable argument sequence.

        :return: the immutable argument sequence
        :rtype: tuple[Argument, ...]
        """
        ...

    @property
    def return_argtype(self):
        """
        **LLM Docstring**

        Return the resolved return `ArgumentType`.

        :return: the resolved return `ArgumentType`
        :rtype: ArgumentType | None
        """
        ...

    @property
    def return_type(self):
        """
        **LLM Docstring**

        Return the `ctypes` return type used to configure a foreign function.

        :return: the `ctypes` return type used to configure a foreign function
        :rtype: type | None
        """
        ...

    @property
    def arg_types(self):
        """
        **LLM Docstring**

        Return the ordered `ctypes` types for all arguments.

        :return: the ordered `ctypes` types for all arguments
        :rtype: list[type]
        """
        ...

    @property
    def cpp_signature(self):
        """
        **LLM Docstring**

        Format the complete C/C++-style function signature.

        :return: Format the complete C/C++-style function signature
        :rtype: str
        """
        ...

    def populate_kwargs(self, args, kwargs, defaults=None):
        """
        **LLM Docstring**

        Merge positional and keyword arguments and fill missing entries from defaults.

        Explicit `defaults` override signature-level defaults, which override each `Argument.default`. Duplicate positional/keyword assignments raise `ValueError`; unresolved arguments remain mapped to `None`.

        :param args: positional values paired with signature arguments
        :type args: Iterable[Any]

        :param kwargs: explicit keyword values
        :type kwargs: Mapping[str, Any]

        :param defaults: per-call fallback defaults
        :type defaults: Mapping[str, Any] | None

        :return: complete argument-name mapping
        :rtype: dict[str, Any]
        """
        ...

    def prep_args(self, args, kwargs, defaults=None):
        """
        **LLM Docstring**

        Prepare arguments in signature order for a foreign-function call.

        When `args` is not `None`, positional and keyword values are first normalized with `populate_kwargs`; each value is then converted by its `Argument.prep_value` method.

        :param args: positional values, or `None` when `kwargs` is already populated
        :type args: Iterable[Any] | None

        :param kwargs: argument values keyed by name
        :type kwargs: Mapping[str, Any]

        :param defaults: per-call fallback defaults
        :type defaults: Mapping[str, Any] | None

        :return: ordered converted arguments
        :rtype: list[Any]
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the function name, arguments, and return type.

        :return: representation string
        :rtype: str
        """
        ...