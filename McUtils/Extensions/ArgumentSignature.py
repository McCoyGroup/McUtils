"""
Provides classes that are necessary for managing argument signatures
"""

__all__ = [
    "ArgumentType",
    "ArrayType",
    "PointerType",
    "PrimitiveType",
    "RealType",
    "IntType",
    "BoolType",
    "Argument",
    "FunctionSignature"
]

import abc, ctypes, numpy as np, numpy.ctypeslib as npctypes, re

# TODO: need to finish up with the actual type inference & make it
#   so that we can use a `Argument.from_value` constructor
#   Also need to have call_single do the appropriate restructing of its Arguments
#   list so that stuff can cleanly go into the C-level + add some docstring-support

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
        raise NotImplementedError()
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
        raise NotImplementedError()
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
        raise NotImplementedError()
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
        raise NotImplementedError()
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
        raise NotImplementedError()
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
        raise NotImplementedError()
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
        raise NotImplementedError()
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
        raise NotImplementedError()
class PrimitiveType(ArgumentType):
    """
    Defines a general purpose ArgumentType so that we can easily manage complicated type specs
    The basic idea is to define a hierarchy of types that can then convert themselves down to
    a `ctypes`-style spec as well as a C++ argument spec so that we can enable `SharedLibraryFunction`
    to use either the basic `ctypes` FFI or a more efficient, but fragile system based off of extension modules
    """

    typeset = {}
    def __init__(self,
                 name,
                 ctypes_spec,
                 cpp_spec,
                 capi_spec,
                 python_types,
                 numpy_dtypes,
                 serializer,
                 deserializer
                 ):
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
        self._name = name
        self._ctypes_spec = ctypes_spec
        self._cpp_spec = cpp_spec
        self._capi_spec = capi_spec
        self._types = python_types
        self._dtypes = numpy_dtypes
        self._serializer = serializer
        self._deserializer = deserializer

        self.typeset[self._cpp_spec] = self

    @property
    def name(self):
        """
        **LLM Docstring**

        Return the descriptive type name.

        :return: the descriptive type name
        :rtype: str
        """
        return self._name
    @property
    def ctypes_type(self):
        """
        **LLM Docstring**

        Return the stored `ctypes` type specification.

        :return: the stored `ctypes` type specification
        :rtype: type | None
        """
        return self._ctypes_spec
    @property
    def cpp_type(self):
        """
        **LLM Docstring**

        Return the stored C/C++ type spelling.

        :return: the stored C/C++ type spelling
        :rtype: str
        """
        return self._cpp_spec
    @property
    def types(self):
        """
        **LLM Docstring**

        Return the accepted Python types.

        :return: the accepted Python types
        :rtype: tuple[type, ...]
        """
        return self._types
    @property
    def dtypes(self):
        """
        **LLM Docstring**

        Return the accepted NumPy dtypes.

        :return: the accepted NumPy dtypes
        :rtype: tuple[np.dtype, ...]
        """
        return self._dtypes
    @property
    def typechar(self):
        """
        **LLM Docstring**

        Return the stored Python C-API format character.

        :return: the stored Python C-API format character
        :rtype: str
        """
        return self._capi_spec
    def isinstance(self, arg):
        """
        **LLM Docstring**

        Test whether a value belongs to one of the configured Python types.

        :param arg: value to test
        :type arg: Any

        :return: `True` when `arg` is an instance of an accepted type
        :rtype: bool
        """
        return isinstance(arg, self._types)
    def cast(self, arg):
        """
        **LLM Docstring**

        Cast a value with the first configured Python type.

        :param arg: value to convert
        :type arg: Any

        :return: Python-side converted value
        :rtype: Any
        """
        return self._types[0](arg)
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
        return self.ctypes_type(self.cast(arg))
        # return self._types[0](arg)
    def __repr__(self):
        """
        **LLM Docstring**

        Return a concise representation containing the wrapper class and primitive name.

        :return: representation string
        :rtype: str
        """
        return "{}({})".format(
            type(self).__name__,
            self.name
        )

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
        self.base = base_type
        self.shape = shape
        self._ctypes_spec = ctypes_spec

    @property
    def ctypes_type(self):
        """
        **LLM Docstring**

        Return or lazily create a C-contiguous NumPy `ndpointer` specification.

        :return: or lazily create a C-contiguous NumPy `ndpointer` specification
        :rtype: Any
        """
        if self._ctypes_spec is None:
            self._ctypes_spec = npctypes.ndpointer(self.base.ctypes_type, flags="C_CONTIGUOUS")
        return self._ctypes_spec
    @property
    def cpp_type(self):
        """
        **LLM Docstring**

        Return the pointer-like C/C++ type string formed from the cached `ctypes` specification.

        :return: the pointer-like C/C++ type string formed from the cached `ctypes` specification
        :rtype: str
        """
        return "*"+self._ctypes_spec
    @property
    def types(self):
        """
        **LLM Docstring**

        Return the accepted Python container type, `numpy.ndarray`.

        :return: the accepted Python container type, `numpy.ndarray`
        :rtype: tuple[type, ...]
        """
        return (np.ndarray,)
    @property
    def dtypes(self):
        """
        **LLM Docstring**

        Return the element dtypes accepted by the base type.

        :return: the element dtypes accepted by the base type
        :rtype: tuple[np.dtype, ...]
        """
        return self.base.dtypes
    @property
    def typechar(self):
        """
        **LLM Docstring**

        Return the Python C-API format character of the base type.

        :return: the Python C-API format character of the base type
        :rtype: str
        """
        return self.base.typechar
    def isinstance(self, arg):
        """
        **LLM Docstring**

        Test whether a value is a NumPy array with an accepted base dtype.

        :param arg: value to test
        :type arg: Any

        :return: compatibility flag
        :rtype: bool
        """
        return isinstance(arg, self.types) and arg.dtype in self.base.dtypes
    def cast(self, arg):
        """
        **LLM Docstring**

        Convert a value to an array using the first accepted base dtype.

        :param arg: array-like value
        :type arg: Any

        :return: converted NumPy array
        :rtype: np.ndarray
        """
        return np.asanyarray(arg).astype(self.base.dtypes[0])
    def c_cast(self, arg):
        """
        **LLM Docstring**

        Convert a value to a C-contiguous NumPy array of the required dtype.

        :param arg: array-like value
        :type arg: Any

        :return: contiguous converted array
        :rtype: np.ndarray
        """
        return np.ascontiguousarray(self.cast(arg))
    def __repr__(self):
        """
        **LLM Docstring**

        Return a concise representation containing the array wrapper and base type.

        :return: representation string
        :rtype: str
        """
        return "{}({})".format(
            type(self).__name__,
            self.base
        )

class PointerType(ArgumentType):
    """
    Extends the basic `ArgumentType` spec to handle pointer types
    """
    def __init__(self, base_type):
        """
        :param base_type: The base type we're building off of
        :type base_type: ArgumentType
        """
        self.base = base_type
        self._ctypes_spec = None

    @property
    def ctypes_type(self):
        """
        **LLM Docstring**

        Return or lazily create a `ctypes.POINTER` to the base type.

        :return: or lazily create a `ctypes.POINTER` to the base type
        :rtype: Any
        """
        if self._ctypes_spec is None:
            self._ctypes_spec = ctypes.POINTER(self.base.ctypes_type)
        return self._ctypes_spec

    @property
    def cpp_type(self):
        """
        **LLM Docstring**

        Return the pointer-like C/C++ type string formed from the cached `ctypes` specification.

        :return: the pointer-like C/C++ type string formed from the cached `ctypes` specification
        :rtype: str
        """
        return "*"+self._ctypes_spec
    @property
    def types(self):
        """
        **LLM Docstring**

        Return the Python types accepted by the base type.

        :return: the Python types accepted by the base type
        :rtype: tuple[type, ...]
        """
        return self.base.types
    @property
    def dtypes(self):
        """
        **LLM Docstring**

        Return the NumPy dtypes accepted by the base type.

        :return: the NumPy dtypes accepted by the base type
        :rtype: tuple[np.dtype, ...]
        """
        return self.base.dtypes
    @property
    def typechar(self):
        """
        **LLM Docstring**

        Return the Python C-API format character of the base type.

        :return: the Python C-API format character of the base type
        :rtype: str
        """
        return self.base.typechar
    def isinstance(self, arg):
        """
        **LLM Docstring**

        Delegate compatibility testing to the base type.

        :param arg: value to test
        :type arg: Any

        :return: compatibility flag
        :rtype: bool
        """
        return self.base.isinstance(arg)
    def cast(self, arg):
        """
        **LLM Docstring**

        Delegate Python-side conversion to the base type.

        :param arg: value to convert
        :type arg: Any

        :return: converted base value
        :rtype: Any
        """
        return self.base.cast(arg)
    def c_cast(self, arg):
        """
        **LLM Docstring**

        Convert a value with the base type and return a `ctypes.byref` pointer to it.

        :param arg: value to convert
        :type arg: Any

        :return: by-reference `ctypes` object
        :rtype: Any
        """
        # we might need to cast arg first...
        return ctypes.byref(self.base.c_cast(arg))
    def __repr__(self):
        """
        **LLM Docstring**

        Return a concise representation containing the pointer wrapper and base type.

        :return: representation string
        :rtype: str
        """
        return "{}({})".format(
            type(self).__name__,
            self.base
        )

# this is the block where we just declare a shit ton of types...
# Python types that handle the most common case
VoidType = PrimitiveType(
    "void",
    None,
    "void",
    "void",
    (),
    (),
    None,#serializer
    None#deserializer
)
RealType = PrimitiveType(
    "Real",
    ctypes.c_double,
    "double",
    "d",
    (float,),
    (np.dtype('float64'),),
    None,#serializer
    None#deserializer
)
IntegerType = PrimitiveType(
    "int",
    ctypes.c_int64,
    "int",
    "i",
    (int,),
    (np.dtype('int64'),),
    None,#serializer
    None#deserializer
)
BoolType = PrimitiveType(
    "bool",
    ctypes.c_bool,
    "bool",
    "p",
    (bool,),
    (np.dtype('bool'),),
    None,#serializer
    None#deserializer
)
# C-types with the same names
FloatType = PrimitiveType(
    "float",
    ctypes.c_float,
    "float",
    "f",
    (float,),
    (np.dtype('float32'),),
    None,#serializer
    None#deserializer
)
DoubleType = PrimitiveType(
    "double",
    ctypes.c_double,
    "double",
    "d",
    (float,),
    (np.dtype('float64'),),
    None,#serializer
    None#deserializer
)
IntType = PrimitiveType(
    "int",
    ctypes.c_int32,
    "int",
    "i",
    (int,),
    (np.dtype('int32'),),
    None,#serializer
    None#deserializer
)
LongType = PrimitiveType(
    "long",
    ctypes.c_int64,
    "long",
    "i",
    (int,),
    (np.dtype('int64'),),
    None,#serializer
    None#deserializer
)


class Argument:
    """
    Defines a single Argument for a C-level caller to support default values, etc.
    We use a two-pronged approach where we have a set of ArgumentType serializers/deserializers
    """

    arg_types = [
        VoidType,
        RealType,
        IntType,
        BoolType
    ]

    def __init__(self, name, dtype, default=None):
        """
        :param name: the name of the argument
        :type name: str
        :param dtype: the type of the argument; at some point we'll support type inference...
        :type dtype: ArgumentType
        :param default: the default value for the argument
        :type default:
        """
        self.name = name
        self.dtype = self.infer_type(dtype) #self.infer_type(dtype)
        self.default = default #self.prep_argument(default)
        self._typesets = {}

    @classmethod
    def infer_type(cls, arg):
        """
        Infers the type of an argument

        :param arg:
        :type arg: ArgumentType | str | type | ctypes type
        :return:
        :rtype:
        """

        if isinstance(arg, ArgumentType):
            return arg

        argtype = None
        if isinstance(arg, tuple): # shorthand for pointer types
            argtype = PointerType(cls.infer_type(arg[0]))
        elif isinstance(arg, (list, np.ndarray)):
            argtype = ArrayType(cls.infer_type(arg[0]))
        elif isinstance(arg, str):
            argtype = cls.infer_type_str(arg)
        elif isinstance(arg, type):
            argtype = cls.infer_type_type(arg)
        else:
            for at in cls.arg_types:
                if at.isinstance(arg):
                    argtype = at
                    break

        if argtype is None:
            raise ValueError("can't infer type from {}".format(arg))
        return argtype

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
        if cls._typesets is None or cls._typestrs is None:
            cls._typesets = {}
            cls._typestrs = {}
            for at in cls.arg_types:
                for t in at.types:
                    if t not in cls._typesets:
                        cls._typesets[t] = at
                if at.cpp_type not in cls._typestrs:
                    cls._typestrs[at.cpp_type] = at
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
        cls._prep_typesets()
        return cls._typesets.get(type_key, None)

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
        cls._prep_typesets()
        type = None
        if argstr in cls._typesets:
            type = cls._typesets[argstr]
        elif argstr in cls._typestrs:
            type = cls._typestrs[argstr]
        else:
            ptr_pat = r"\*({})".format( "|".join(cls._typestrs.keys()))
            match = re.match(ptr_pat, argstr)
            if match is not None:
                typestr = match.group(0)
                type = ArrayType(cls._typestrs[typestr])
        return type

    @classmethod
    def inferred_type_string(cls, arg):
        """
        returns a type string for the inferred type
        """
        raise NotImplementedError("...")

    def prep_value(self, val):
        """
        **LLM Docstring**

        Convert a value to the C-call representation required by this argument.

        :param val: Python value to prepare
        :type val: Any

        :return: converted value
        :rtype: Any
        """
        return self.dtype.c_cast(val)

    def is_pointer(self):
        """
        **LLM Docstring**

        Test whether this argument uses a `PointerType`.

        :return: pointer-type flag
        :rtype: bool
        """
        return isinstance(self.dtype, PointerType)
    def is_array(self):
        """
        **LLM Docstring**

        Test whether this argument uses an `ArrayType`.

        :return: array-type flag
        :rtype: bool
        """
        return isinstance(self.dtype, ArrayType)
    @property
    def dtypes(self):
        """
        **LLM Docstring**

        Return the NumPy dtypes accepted by this argument type.

        :return: accepted dtypes
        :rtype: tuple[np.dtype, ...]
        """
        return self.dtype.dtypes
    @property
    def typechar(self):
        """
        **LLM Docstring**

        Return the Python C-API format character for this argument type.

        :return: format character
        :rtype: str
        """
        return self.dtype.typechar
    @property
    def cpp_signature(self):
        """
        **LLM Docstring**

        Format this argument as a C/C++ declaration fragment.

        :return: string of the form `<type> <name>`
        :rtype: str
        """
        return "{} {}".format(
            self.dtype.cpp_type,
            self.name
        )
    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation containing the argument name and resolved type.

        :return: representation string
        :rtype: str
        """
        return "{}('{}', {})".format(
            type(self).__name__,
            self.name,
            self.dtype
        )

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
        self.name = name
        if return_type is not None:
            return_type = Argument.infer_type(return_type)
        self._ret_type = return_type
        self._arguments = tuple(self.build_argument(x, i) for i, x in enumerate(args))
        if defaults is None:
            defaults = {}
        self.defaults = defaults

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
        return FunctionSignature(
            name,
            *(Argument(k, v) for k, v in args.items()),
            defaults=defaults,
            return_type=return_type
        )

    def build_argument(self, argtup, which=None):
        """
        Converts an argument tuple into an Argument object
        :param argtup:
        :type argtup:
        :return:
        :rtype:
        """
        if isinstance(argtup, Argument):
            return argtup
        elif isinstance(argtup, str):
            argtup = ('_argument_{}'.format(which), argtup)
        elif isinstance(argtup, dict):
            if 'default' not in argtup:
                argtup['default'] = None
            argtup = (argtup['name'], argtup['dtype'], argtup['default'])
        if len(argtup) == 2:
            name, dtype = argtup
            default = None
        else:
            name, dtype, default = argtup
        return Argument(name=name, dtype=dtype, default=default)

    @property
    def args(self):
        """
        **LLM Docstring**

        Return the immutable argument sequence.

        :return: the immutable argument sequence
        :rtype: tuple[Argument, ...]
        """
        return self._arguments
    @property
    def return_argtype(self):
        """
        **LLM Docstring**

        Return the resolved return `ArgumentType`.

        :return: the resolved return `ArgumentType`
        :rtype: ArgumentType | None
        """
        return self._ret_type
    @property
    def return_type(self):
        """
        **LLM Docstring**

        Return the `ctypes` return type used to configure a foreign function.

        :return: the `ctypes` return type used to configure a foreign function
        :rtype: type | None
        """
        res = self._ret_type
        if res is not None:
            res = res.ctypes_type
        return res
    @property
    def arg_types(self):
        """
        **LLM Docstring**

        Return the ordered `ctypes` types for all arguments.

        :return: the ordered `ctypes` types for all arguments
        :rtype: list[type]
        """
        return [a.dtype.ctypes_type for a in self.args]

    @property
    def cpp_signature(self):
        """
        **LLM Docstring**

        Format the complete C/C++-style function signature.

        :return: Format the complete C/C++-style function signature
        :rtype: str
        """
        return "{} {}({})".format(
            "void" if self.return_type is None else self.return_type,
            self.name,
            ", ".join(a.cpp_signature for a in self.args)
        )

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
        kwlist = {}
        for base, val in zip(self.args, args):
            kwlist[base.name] = val
        for k, v in kwargs.items():
            if k in kwlist:
                raise ValueError("got multiple values for argument '{}'".format(k))
            kwlist[k] = v

        if defaults is None:
            defaults = {}

        for a in self.args:
            # resolve any possible default values
            kwlist[a.name] = kwlist.get(
                a.name,
                defaults.get(a.name, self.defaults.get(a.name, a.default))
            )

        return kwlist

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
        if args is not None: # easy way to say no prep needed...
            kwargs = self.populate_kwargs(args, kwargs, defaults=defaults)

        final_args = [
            # coerce to correct type
            a.prep_value(kwargs[a.name])
            for a in self.args
        ]

        return final_args

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the function name, arguments, and return type.

        :return: representation string
        :rtype: str
        """
        return "{}({}({})->{})".format(
            type(self).__name__,
            self.name,
            ", ".join(repr(a) for a in self.args),
            "Any" if self.return_type is None else self.return_type
        )


