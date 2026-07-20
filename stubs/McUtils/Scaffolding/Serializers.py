"""
Provides scaffolding for creating serializers that dump data to a reloadable format.
Light-weight and unsophisticated, but that's what makes this useful..
"""
import abc, numpy as np, json, io, pickle, os, base64, types, warnings
import tempfile
import collections
import uuid
from collections import OrderedDict
from .. import Devutils as dev
from .. import Iterators as itut
__all__ = ['PseudoPickler', 'BaseSerializer', 'JSONSerializer', 'NumPySerializer', 'NDarrayMarshaller', 'HDF5Serializer', 'YAMLSerializer', 'ModuleSerializer', 'flatten_tree', 'unflatten_tree', 'write_flat_tree', 'read_flat_tree']

class PseudoPickler:
    """
    A simple plugin to work _like_ pickle, in that it should
    hopefully support serializing arbitrary python objects, but which
    doesn't attempt to put stuff down to a single `bytearray`, instead
    supporting objects with `to_state` and `from_state` methods by converting
    them to more primitive serializble types like arrays, strings, numbers,
    etc.
    Falls back to naive pickling when necessary.
    """
    _cache = None

    def __init__(self, allow_pickle=False, protocol=1, b64encode=False):
        """
        **LLM Docstring**

        Configure pseudo-pickling fallback, protocol marker, and optional base64 encoding for embedded pickle bytes.

        :param allow_pickle: whether unsupported values may fall back to pickle
        :type allow_pickle: object
        :param protocol: pseudo-pickle protocol marker
        :type protocol: object
        :param b64encode: whether pickle bytes are base64 encoded
        :type b64encode: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...
    _primitive_types = (int, float, bool, str, np.integer, np.floating)
    _list_types = (tuple, list)
    _dict_types = (dict, OrderedDict)
    _importable_types = (type, bytes, bytearray, memoryview, np.dtype)
    _safe_modules = ['numpy', 'multiprocessing']

    def _sanitize_key(self, key):
        """
        **LLM Docstring**

        Reject nonprimitive mapping keys so the serialized structure remains compatible with JSON-like formats.

        :param key: the storage or lookup key
        :type key: object
        :return: the validated primitive key unchanged
        :rtype: str | int | float | bool
        """
        ...

    def _to_state(self, obj, cache):
        """
        Tries to extract state for `obj` by walking through the
        object dict

        :param obj:
        :type obj:
        :param cache: cache of written objects to prevent cycles
        :type cache: set
        :return:
        :rtype:
        """
        ...

    def _to_importable_state(self, obj):
        """
        **LLM Docstring**

        Pickle an importable object and wrap the bytes with protocol metadata, optionally base64-encoding them.

        :param obj: object to serialize or manage
        :type obj: object
        :return: a protocol-tagged mapping containing pickle bytes or base64 text
        :rtype: dict
        """
        ...

    def _can_import(self, obj):
        """
        **LLM Docstring**

        Allow direct pickle state for objects from the configured safe top-level modules and builtin functions.

        :param obj: object to serialize or manage
        :type obj: object
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    def to_state(self, obj, cache=None):
        """
        Tries to extract state from `obj`, first through its `to_state`
        interface, but that failing by recursively walking the object
        tree

        :param obj:
        :type obj:
        :return:
        :rtype:
        """
        ...

    def serialize(self, obj, cache=None):
        """
        Serializes an object first by checking for a `to_state`
        method, and that missing, by converting to primitive-ish types
        in a recursive strategy if the object passes `is_simple`, otherwise
        falling back to `pickle`

        :param obj: object to be serialized
        :type obj:
        :return: spec for the pseudo-pickled data
        :rtype: dict
        """
        ...

    def deserialize(self, spec):
        """
        Deserializes from an object spec, dispatching
        to regular pickle where necessary

        :param object:
        :type object:
        :return:
        :rtype:
        """
        ...

class ConvertedData:
    """
    Wrapper class for holding serialized data so we can be sure it's clean
    """

    def __init__(self, data, serializer):
        """
        **LLM Docstring**

        Pair already-converted payload data with the serializer that produced it.

        :param data: data to serialize, convert, or write
        :type data: object
        :param serializer: serializer instance or specification
        :type serializer: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

class BaseSerializer(metaclass=abc.ABCMeta):
    """
    Serializer base class to define the interface
    """
    default_extension = ''
    binary = False
    registry_name = None
    registry = {}

    @classmethod
    def register(cls, name, serializer=None):
        """
        **LLM Docstring**

        Register a serializer class under a name, either immediately or through decorator syntax.

        :param name: registry, command, resource, or object name
        :type name: object
        :param serializer: serializer instance or specification
        :type serializer: object
        :return: No explicit value unless noted by the underlying delegated operation.
        :rtype: None | object
        """
        ...

    @classmethod
    def construct(cls, serializer_type, **kwargs):
        """
        **LLM Docstring**

        Return an existing serializer or instantiate one resolved from a registry name or class.

        :param serializer_type: serializer instance, registry name, or class
        :type serializer_type: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: The resolved or newly constructed helper object.
        :rtype: object
        """
        ...

    @abc.abstractmethod
    def convert(self, data):
        """
        Converts data into a serializable format
        :param data:
        :type data:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def deconvert(self, data):
        """
        Converts data from a serialized format into a python format
        :param data:
        :type data:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def serialize(self, file, data, **kwargs):
        """
        Writes the data
        :param file:
        :type file:
        :param data:
        :type data:
        :return:
        :rtype:
        """
        ...

    def dumps(self, data, **kwargs):
        """
        Write data to a string
        :param data:
        :param kwargs:
        :return:
        """
        ...

    @abc.abstractmethod
    def deserialize(self, file, **kwargs):
        """
        Loads data from a file
        :param file:
        :type file:
        :return:
        :rtype:
        """
        ...

    def loads(self, data, **kwargs):
        """
        Write data to a string
        :param data:
        :param kwargs:
        :return:
        """
        ...

@BaseSerializer.register('pickle')
class PicklingSerializer(BaseSerializer):
    """
    A serializer that makes dumping data to JSON simpler
    """
    default_extension = '.pkl'
    binary = True

    def __init__(self, allow_pickle=True, pseudopickler=None):
        """
        **LLM Docstring**

        Configure a pseudo-pickler-backed binary serializer and whether nested pseudo-pickle payloads are restored.

        :param allow_pickle: whether unsupported values may fall back to pickle
        :type allow_pickle: object
        :param pseudopickler: pseudo-pickler used for arbitrary objects
        :type pseudopickler: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def convert(self, data):
        """
        **LLM Docstring**

        Pseudo-pickle arbitrary input and wrap the resulting payload as converted data.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    def deconvert(self, data):
        """
        **LLM Docstring**

        Restore a pseudo-pickled payload to Python objects.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def serialize(self, file, data, **kwargs):
        """
        **LLM Docstring**

        Convert input when needed and write its binary payload to the file object.

        :param file: path or file-like object
        :type file: object
        :param data: data to serialize, convert, or write
        :type data: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def dumps(self, data, **kwargs):
        """
        **LLM Docstring**

        Return the converted binary pseudo-pickle payload directly.

        :param data: data to serialize, convert, or write
        :type data: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: the binary pseudo-pickle payload
        :rtype: bytes | bytearray | memoryview
        """
        ...

    def _deserialize_dict(self, dat, key=None):
        """
        **LLM Docstring**

        Restore a payload, optionally descend through a slash-separated key path, and perform a second pseudo-pickle restoration when enabled.

        :param dat: serialized payload to restore
        :type dat: object
        :param key: the storage or lookup key
        :type key: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def loads(self, data, key=None, **kwargs):
        """
        **LLM Docstring**

        Deserialize an in-memory payload and optionally select a nested key.

        :param data: data to serialize, convert, or write
        :type data: object
        :param key: the storage or lookup key
        :type key: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def deserialize(self, file, key=None, **kwargs):
        """
        **LLM Docstring**

        Read bytes from a file or path and delegate to `loads`.

        :param file: path or file-like object
        :type file: object
        :param key: the storage or lookup key
        :type key: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

@BaseSerializer.register('json')
class JSONSerializer(BaseSerializer):
    """
    A serializer that makes dumping data to JSON simpler
    """
    default_extension = '.json'

    class BaseEncoder(json.JSONEncoder):

        def __init__(self, *args, pseudopickler=None, allow_pickle=True, **kwargs):
            """
            **LLM Docstring**

            Initialize JSON encoding with NumPy handling and optional pseudo-pickle fallback for unsupported objects.

            :param pseudopickler: pseudo-pickler used for arbitrary objects
            :type pseudopickler: object
            :param allow_pickle: whether unsupported values may fall back to pickle
            :type allow_pickle: object
            :param args: positional arguments forwarded to a callable
            :type args: object
            :param kwargs: keyword arguments forwarded to a callable
            :type kwargs: object
            :return: No explicit value; the method mutates state or performs I/O.
            :rtype: None
            """
            ...

        def default(self, obj):
            """
            **LLM Docstring**

            Convert NumPy arrays and scalars to JSON primitives, otherwise use the base encoder or pseudo-pickle fallback.

            :param obj: object to serialize or manage
            :type obj: object
            :return: a JSON-compatible primitive, list, or pseudo-pickle state
            :rtype: object
            """
            ...

    def __init__(self, encoder=None, allow_pickle=True, pseudopickler=None):
        """
        **LLM Docstring**

        Configure the JSON encoder, pseudo-pickler, and unsupported-object fallback policy.

        :param encoder: JSON encoder instance
        :type encoder: object
        :param allow_pickle: whether unsupported values may fall back to pickle
        :type allow_pickle: object
        :param pseudopickler: pseudo-pickler used for arbitrary objects
        :type pseudopickler: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def convert(self, data):
        """
        **LLM Docstring**

        Encode data to a JSON string and mark it as converted.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    def deconvert(self, data):
        """
        **LLM Docstring**

        Return decoded JSON data unchanged before optional pseudo-pickle restoration.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def serialize(self, file, data, **kwargs):
        """
        **LLM Docstring**

        JSON-encode input when needed and write the resulting text.

        :param file: path or file-like object
        :type file: object
        :param data: data to serialize, convert, or write
        :type data: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def dumps(self, data, **kwargs):
        """
        **LLM Docstring**

        Return the JSON text representation directly.

        :param data: data to serialize, convert, or write
        :type data: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: the JSON document text
        :rtype: str
        """
        ...

    def _deserialize_dict(self, dat, key=None):
        """
        **LLM Docstring**

        Optionally select a slash-delimited key path and recursively restore pseudo-pickled objects.

        :param dat: decoded JSON value to postprocess
        :type dat: object
        :param key: the storage or lookup key
        :type key: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def loads(self, file, key=None, **kwargs):
        """
        **LLM Docstring**

        Decode JSON text and postprocess optional key selection and pseudo-pickled values.

        :param file: path or file-like object
        :type file: object
        :param key: the storage or lookup key
        :type key: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def deserialize(self, file, key=None, **kwargs):
        """
        **LLM Docstring**

        Decode JSON from a file object and postprocess optional key selection and pseudo-pickled values.

        :param file: path or file-like object
        :type file: object
        :param key: the storage or lookup key
        :type key: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

@BaseSerializer.register('yaml')
class YAMLSerializer(BaseSerializer):
    """
    A serializer that makes dumping data to YAML simpler.
    Doesn't support arbitrary python objects since that hasn't seemed like
    a huge need yet...
    """
    default_extension = '.yml'

    def __init__(self):
        """
        **LLM Docstring**

        Import and retain the YAML backend, raising at construction time when YAML support is unavailable.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def convert(self, data):
        """
        **LLM Docstring**

        Wrap YAML-compatible data without structural conversion.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    def deconvert(self, data):
        """
        **LLM Docstring**

        Return YAML-loaded data unchanged.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def serialize(self, file, data, **kwargs):
        """
        **LLM Docstring**

        Dump converted or raw data through the YAML API.

        :param file: path or file-like object
        :type file: object
        :param data: data to serialize, convert, or write
        :type data: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def deserialize(self, file, key=None, **kwargs):
        """
        **LLM Docstring**

        Load YAML data, deconvert it, and optionally select a nested slash-separated key.

        :param file: path or file-like object
        :type file: object
        :param key: the storage or lookup key
        :type key: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

class NDarrayMarshaller:
    """
    Support class for `HDF5Serializer` and other
    NumPy-friendly interfaces that marshalls data
    to/from NumPy arrays
    """

    def __init__(self, base_serializer=None, allow_pickle=True, psuedopickler=None, allow_records=False, all_dicts=False, converters=None):
        """
        **LLM Docstring**

        Configure recursive conversion to NumPy-compatible trees, pseudo-pickle fallback, record handling, and custom dispatch.

        :param base_serializer: parent serializer used during deconversion
        :type base_serializer: object
        :param allow_pickle: whether unsupported values may fall back to pickle
        :type allow_pickle: object
        :param psuedopickler: pseudo-pickler used for arbitrary objects
        :type psuedopickler: object
        :param allow_records: whether homogeneous object sequences may become NumPy record arrays
        :type allow_records: object
        :param all_dicts: whether heterogeneous sequences are encoded as dictionaries
        :type all_dicts: object
        :param converters: custom ordered conversion dispatch
        :type converters: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...
    atomic_types = PseudoPickler._primitive_types

    @classmethod
    def get_default_converters(self):
        """
        **LLM Docstring**

        Build the ordered type/duck-type dispatch table used to coerce values into NumPy-compatible forms.

        :return: an ordered converter-dispatch mapping
        :rtype: collections.OrderedDict
        """
        ...

    @property
    def converter_dispatch(self):
        """
        **LLM Docstring**

        Return the custom converter mapping or create the default ordered dispatch table.

        :return: the active ordered converter-dispatch mapping
        :rtype: collections.OrderedDict
        """
        ...

    @classmethod
    def _literal_to_numpy(cls, data):
        """
        **LLM Docstring**

        Represent a scalar literal as a zero-dimensional NumPy array.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    def _dict_to_numpy(self, data):
        """
        **LLM Docstring**

        Recursively convert each dictionary value while preserving keys.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    def _none_to_none(self, data):
        """
        **LLM Docstring**

        Preserve `None` as the sentinel for an empty HDF5 dataset.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: `None`, preserved as an HDF5 empty-dataset sentinel
        :rtype: None
        """
        ...

    def _prep_iterable(self, data):
        """
        **LLM Docstring**

        Attempt homogeneous NumPy conversion, falling back to an object array for ragged or incompatible sequences.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    def _iterable_to_numpy(self, data):
        """
        **LLM Docstring**

        Convert homogeneous sequences directly and encode object sequences as records, keyed dictionaries, or recursively converted lists.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    class _pickle_cache:

        def __init__(self, parent):
            """
            **LLM Docstring**

            Initialize a stack and identity set used to detect recursive object conversion.

            :param parent: owning parser or context object
            :type parent: object
            :return: No explicit value; the method mutates state or performs I/O.
            :rtype: None
            """
            ...

        def __call__(self, key):
            """
            **LLM Docstring**

            Push an object identity into the recursion tracker and return the tracker as a context manager.

            :param key: the storage or lookup key
            :type key: object
            :return: this recursion tracker, ready for use as a context manager
            :rtype: NDarrayMarshaller._pickle_cache
            """
            ...

        def __enter__(self):
            """
            **LLM Docstring**

            Return the active recursion tracker.

            :return: The active context object.
            :rtype: object
            """
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Pop the current object and clear the parent marshaller cache when the outermost conversion finishes.

            :param exc_type: exception type passed by the context manager protocol
            :type exc_type: object
            :param exc_val: exception instance passed by the context manager protocol
            :type exc_val: object
            :param exc_tb: traceback passed by the context manager protocol
            :type exc_tb: object
            :return: No explicit value; the method mutates state or performs I/O.
            :rtype: None
            """
            ...

        def add(self, key):
            """
            **LLM Docstring**

            Record an object identity and raise `RecursionError` when conversion revisits an active object.

            :param key: the storage or lookup key
            :type key: object
            :return: No explicit value; the method mutates state or performs I/O.
            :rtype: None
            """
            ...

        def pop(self):
            """
            **LLM Docstring**

            Remove the most recently tracked object identity.

            :return: No explicit value; the method mutates state or performs I/O.
            :rtype: None
            """
            ...

    def _psuedo_pickle_to_numpy(self, data):
        """
        **LLM Docstring**

        Pseudo-pickle an unsupported object under recursion protection and recursively convert the resulting state.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: the recursively converted pseudo-pickle state
        :rtype: object
        """
        ...

    def convert(self, data, allow_pickle=None):
        """
        Recursively loop through, test data, make sure HDF5 compatible
        :param data:
        :type data:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def _default_convert(x, converter):
        """
        **LLM Docstring**

        Fallback converter that pseudo-pickles an otherwise unsupported value.

        :param x: unsupported value requiring pseudo-pickle conversion
        :type x: object
        :param converter: callable used to convert a command-line value
        :type converter: object
        :return: the pseudo-pickled NumPy-compatible representation
        :rtype: object
        """
        ...

    def deconvert(self, data):
        """
        Reverses the conversion process
        used to marshall the data

        :param data:
        :type data:
        :return:
        :rtype:
        """
        ...

    def __call__(self, data, allow_pickle=None):
        """
        **LLM Docstring**

        Invoke recursive conversion, using the marshaller default pickle policy unless overridden.

        :param data: data to serialize, convert, or write
        :type data: object
        :param allow_pickle: whether unsupported values may fall back to pickle
        :type allow_pickle: object
        :return: the NumPy-compatible converted representation
        :rtype: object
        """
        ...

@BaseSerializer.register('hdf5')
class HDF5Serializer(BaseSerializer):
    """
    Defines a serializer that can prep/dump python data to HDF5.
    To minimize complexity, we always use NumPy & Pseudopickle as an interface layer.
    This restricts what we can serialize, but generally in insignificant ways.
    """
    default_extension = '.hdf5'
    binary = True

    def __init__(self, allow_pickle=True, psuedopickler=None, converters=None):
        """
        **LLM Docstring**

        Initialize `h5py` and an ndarray marshaller configured to encode all nested sequences as dictionary-like HDF5 trees.

        :param allow_pickle: whether unsupported values may fall back to pickle
        :type allow_pickle: object
        :param psuedopickler: pseudo-pickler used for arbitrary objects
        :type psuedopickler: object
        :param converters: custom ordered conversion dispatch
        :type converters: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def convert(self, data):
        """
        Converts data into format that can be serialized easily

        :param data:
        :type data:
        :return:
        :rtype:
        """
        ...

    def _create_dataset(self, h5_obj, key, data):
        """
        Mostly exists to be overridden
        :param h5_obj:
        :type h5_obj:
        :param key:
        :type key:
        :param data:
        :type data:
        :return:
        :rtype:
        """
        ...

    def _validate_datatype(self, data):
        """
        **LLM Docstring**

        Accept only `None` or NumPy arrays as leaf HDF5 dataset values.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    def _prune_existing(self, h5_obj, key):
        """
        **LLM Docstring**

        Navigate a key path and delete the existing final HDF5 object.

        :param h5_obj: HDF5 file or group
        :type h5_obj: object
        :param key: the storage or lookup key
        :type key: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def _destroy_and_add(self, h5_obj, key, data):
        """
        **LLM Docstring**

        Delete an incompatible object, recreate intermediate groups, and create a replacement dataset.

        :param h5_obj: HDF5 file or group
        :type h5_obj: object
        :param key: the storage or lookup key
        :type key: object
        :param data: data to serialize, convert, or write
        :type data: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def _write_data(self, h5_obj, key, data):
        """
        Writes a numpy array into a group
        :param h5_group:
        :type h5_group: h5py.Group
        :param key:
        :type key: str
        :param data:
        :type data: np.ndarray
        :return:
        :rtype:
        """
        ...

    def _write_dict(self, h5_obj, data):
        """
        Writes a dict into a group
        :param h5_group:
        :type h5_group: h5py.Group
        :param data:
        :type data: dict
        :return:
        :rtype:
        """
        ...

    def serialize(self, file, data, **kwargs):
        """
        **LLM Docstring**

        Convert data, open an HDF5 file or group, and update either the `_data` dataset or a nested dictionary tree.

        :param file: path or file-like object
        :type file: object
        :param data: data to serialize, convert, or write
        :type data: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def deconvert(self, data):
        """
        Converts an HDF5 Dataset into a NumPy array or Group into a dict
        :param data:
        :type data:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def _extract_key(cls, dataset, key):
        """
        **LLM Docstring**

        Descend through a string key or iterable key path in an HDF5 group.

        :param dataset: HDF5 file, group, or dataset at which traversal begins
        :type dataset: object
        :param key: the storage or lookup key
        :type key: object
        :return: The concrete value described by the summary, with the exact type determined by the selected backend.
        :rtype: object
        """
        ...

    def deserialize(self, file, key=None, **kwargs):
        """
        **LLM Docstring**

        Open an HDF5 source, optionally select a nested object, and deconvert it to Python data.

        :param file: path or file-like object
        :type file: object
        :param key: the storage or lookup key
        :type key: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

@BaseSerializer.register('npz')
class NumPySerializer(BaseSerializer):
    """
    A serializer that implements NPZ dumps
    """
    default_extension = '.npz'
    binary = True
    atomic_types = (str, int, float)
    converter_dispatch = None

    @classmethod
    def get_default_converters(self):
        """
        **LLM Docstring**

        Build the ordered dispatch table for NumPy arrays, array-like objects, scalars, mappings, and sequences.

        :return: an ordered converter-dispatch mapping
        :rtype: collections.OrderedDict
        """
        ...

    @classmethod
    def get_converters(self):
        """
        **LLM Docstring**

        Return the custom converter dispatch or the default converter mapping.

        :return: the active converter-dispatch mapping
        :rtype: collections.OrderedDict
        """
        ...

    @classmethod
    def _literal_to_numpy(cls, data):
        """
        **LLM Docstring**

        Represent a scalar as a zero-dimensional NumPy array.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    @classmethod
    def _dict_to_numpy(cls, data):
        """
        **LLM Docstring**

        Recursively convert dictionary values to NumPy-compatible structures.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    @classmethod
    def _iterable_to_numpy(cls, data):
        """
        **LLM Docstring**

        Convert homogeneous sequences to arrays and encode heterogeneous sequences as numbered dictionary entries.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    @classmethod
    def _convert(cls, data):
        """
        Recursively loop through, test data, make sure NumPy compatible
        :param data:
        :type data:
        :return:
        :rtype:
        """
        ...
    dict_key_sep = '::>|<::'

    def _flatten_dict(self, d, sep=None):
        """
        :param d:
        :type d: dict
        :param sep:
        :type sep: str | None
        :return:
        :rtype:
        """
        ...

    def convert(self, data):
        """
        **LLM Docstring**

        Recursively convert data and flatten nested dictionaries into separator-delimited NPZ keys.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    def _deconvert_val(self, data):
        """
        **LLM Docstring**

        Reconstruct heterogeneous lists encoded with `_list_item_` keys and recursively restore mappings.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def deconvert(self, data, sep=None):
        """
        Unflattens nested dictionary structures so that the original data
        can be recovered
        :param data:
        :type data:
        :param sep:
        :type sep: str | None
        :return:
        :rtype:
        """
        ...

    def serialize(self, file, data, **kwargs):
        """
        **LLM Docstring**

        Write a single array with `np.save` or a flattened mapping with `np.savez`.

        :param file: path or file-like object
        :type file: object
        :param data: data to serialize, convert, or write
        :type data: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: No explicit value unless noted by the underlying delegated operation.
        :rtype: None | object
        """
        ...

    def deserialize(self, file, key=None, **kwargs):
        """
        **LLM Docstring**

        Load NumPy data, reconstruct nested structures, and optionally select a slash-separated key.

        :param file: path or file-like object
        :type file: object
        :param key: the storage or lookup key
        :type key: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

@BaseSerializer.register('module')
class ModuleSerializer(BaseSerializer):
    """
    A somewhat hacky serializer that supports module-based serialization.
    Writes all module parameters to a dict with a given attribute.
    Serialization doesn't support loading arbitrary python code, but deserialization does.
    Use at your own risk.
    """
    default_extension = '.py'
    binary = False
    default_loader = None
    default_attr = 'config'

    def __init__(self, attr=None, loader=None):
        """
        **LLM Docstring**

        Configure the target module attribute and optional module loader.

        :param attr: attribute name
        :type attr: object
        :param loader: module loader
        :type loader: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    @property
    def loader(self):
        """
        **LLM Docstring**

        Lazily construct or return the module loader used for deserialization.

        :return: the configured or lazily created module loader
        :rtype: object
        """
        ...

    @property
    def attr(self):
        """
        **LLM Docstring**

        Return the configured module attribute or the default `config` name.

        :return: the module attribute containing serialized data
        :rtype: str
        """
        ...

    @classmethod
    def _get_loader(cls):
        """
        **LLM Docstring**

        Create a `ModuleLoader` rooted at the `Configs` package namespace.

        :return: a module loader rooted at `Configs`
        :rtype: ModuleLoader
        """
        ...

    def convert(self, data):
        """
        **LLM Docstring**

        Wrap module configuration data without structural conversion.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The converted representation described above.
        :rtype: object
        """
        ...

    def deconvert(self, data):
        """
        **LLM Docstring**

        Return the loaded module attribute unchanged.

        :param data: data to serialize, convert, or write
        :type data: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def serialize(self, file, data, **kwargs):
        """
        **LLM Docstring**

        JSON-encode data and emit a Python assignment to the configured module attribute.

        :param file: path or file-like object
        :type file: object
        :param data: data to serialize, convert, or write
        :type data: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def deserialize(self, file, key=None, **kwargs):
        """
        **LLM Docstring**

        Execute/load the module, retrieve the configured attribute, and optionally select a nested key.

        :param file: path or file-like object
        :type file: object
        :param key: the storage or lookup key
        :type key: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

def dictify_lists(tree: dict):
    """
    **LLM Docstring**

    Recursively replace lists of dictionaries and ragged nested sequences with numbered dictionary entries and a length marker.

    :param tree: nested structure or recursion tracker
    :type tree: dict
    :return: The converted representation described above.
    :rtype: object
    """
    ...

def disambiguate_tree(tree_obj, type_map=None, aliases=None):
    """
    **LLM Docstring**

    Assign stable key types across a nested tree, creating aliases when the same key name appears with incompatible value types.

    :param tree_obj: nested dictionary to encode
    :type tree_obj: object
    :param type_map: mapping from key names to observed value types
    :type type_map: object
    :param aliases: mapping from generated aliases to original key names
    :type aliases: object
    :return: The converted representation described above.
    :rtype: object
    """
    ...

def flatten_tree(tree_obj, top_level=True, prep_tree=True, allow_pickle=False):
    """
    **LLM Docstring**

    Encode a nested dictionary as traversal metadata plus flattened value arrays and shape/sentinel streams.

    :param tree_obj: nested dictionary to encode
    :type tree_obj: object
    :param top_level: whether this is the outermost flattening call
    :type top_level: object
    :param prep_tree: whether list normalization and key disambiguation should run
    :type prep_tree: object
    :param allow_pickle: whether unsupported values may fall back to pickle
    :type allow_pickle: object
    :return: The converted representation described above.
    :rtype: object
    """
    ...

def merge_trees(subtrees, top_level=True):
    """
    **LLM Docstring**

    Merge recursively flattened subtrees into shared key tables, traversal markers, shape streams, and concatenated value arrays.

    :param subtrees: flattened child structures to merge
    :type subtrees: object
    :param top_level: whether this is the outermost flattening call
    :type top_level: object
    :return: The converted representation described above.
    :rtype: object
    """
    ...

def undictify_lists(tree: dict):
    """
    **LLM Docstring**

    Recursively reconstruct numbered dictionary encodings back into Python lists.

    :param tree: nested structure or recursion tracker
    :type tree: dict
    :return: The converted representation described above.
    :rtype: object
    """
    ...

def unflatten_tree(serial_tree, unprep_tree=True):
    """
    **LLM Docstring**

    Replay traversal markers and per-key shape/value pointers to rebuild the nested tree and restore list/`None` sentinels.

    :param serial_tree: flat-tree metadata and arrays
    :type serial_tree: object
    :param unprep_tree: whether numbered list dictionaries should be restored
    :type unprep_tree: object
    :return: The reconstructed, loaded, or selected Python value.
    :rtype: object
    """
    ...

def write_flat_tree(file, tree, flatten=None, allow_pickle=False, writer=None, **writer_options):
    """
    **LLM Docstring**

    Flatten a tree when needed and write metadata, shape streams, and value arrays to an NPZ-style writer.

    :param file: path or file-like object
    :type file: object
    :param tree: nested structure or recursion tracker
    :type tree: object
    :param flatten: whether input should be flattened before writing
    :type flatten: object
    :param allow_pickle: whether unsupported values may fall back to pickle
    :type allow_pickle: object
    :param writer: NPZ-compatible writer callable
    :type writer: object
    :param writer_options: options forwarded to the writer
    :type writer_options: object
    :return: the return value from the selected NPZ writer
    :rtype: object
    """
    ...

def read_flat_tree(file, unflatten=True, reader=None, allow_pickle=False, **reader_options):
    """
    **LLM Docstring**

    Read the NPZ-style flat-tree representation, rebuild its metadata structure, and optionally unflatten it.

    :param file: path or file-like object
    :type file: object
    :param unflatten: whether read data should be reconstructed into a nested tree
    :type unflatten: object
    :param reader: NPZ-compatible reader callable
    :type reader: object
    :param allow_pickle: whether unsupported values may fall back to pickle
    :type allow_pickle: object
    :param reader_options: options forwarded to the reader
    :type reader_options: object
    :return: The reconstructed, loaded, or selected Python value.
    :rtype: object
    """
    ...