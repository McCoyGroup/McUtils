import abc, os
from .. import Devutils as dev
from .Serializers import *
__all__ = ['Checkpointer', 'CheckpointerKeyError', 'DumpCheckpointer', 'JSONCheckpointer', 'NumPyCheckpointer', 'HDF5Checkpointer', 'DictCheckpointer', 'NullCheckpointer']

class CheckpointerKeyError(KeyError):
    ...

class Checkpointer(metaclass=abc.ABCMeta):
    """
    General purpose base class that allows checkpointing to be done easily and cleanly.
    Intended to be a passable object that allows code to checkpoint easily.
    """
    default_extension = ''

    def __init__(self, checkpoint_file, allowed_keys=None, omitted_keys=None):
        """
        **LLM Docstring**

        Initialize checkpoint location, key filters, nested-open depth, and stream state.

        :param checkpoint_file: path or file-like checkpoint target
        :type checkpoint_file: object
        :param allowed_keys: optional whitelist of permitted top-level keys
        :type allowed_keys: object
        :param omitted_keys: optional blacklist of top-level keys
        :type omitted_keys: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Render the concrete checkpointer type and checkpoint target.

        :return: A human-readable string representation.
        :rtype: str
        """
        ...
    _ext_map = None

    @classmethod
    def extension_map(cls):
        """
        **LLM Docstring**

        Return the extension-to-checkpointer dispatch table, honoring a class-level override when present.

        :return: a mapping from filename extensions to concrete checkpointer classes
        :rtype: dict[str, type[Checkpointer]]
        """
        ...

    @classmethod
    def build_canonical(cls, checkpoint):
        """
        Dispatches over types of objects to make a canonical checkpointer
        from the supplied data

        :param checkpoint: provides
        :type checkpoint: None | str | Checkpoint | file | dict
        :return:
        :rtype: Checkpointer
        """
        ...

    @classmethod
    def from_file(cls, file, **opts):
        """
        Dispatch function to load from the appropriate file
        :param file:
        :type file: str | File
        :param opts:
        :type opts:
        :return:
        :rtype:
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Increment the nested-open count and lazily open the checkpoint stream on the outermost entry.

        :return: The active context object.
        :rtype: object
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Decrement the nested-open count and close the stream after the outermost context exits.

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

    def cached_eval(self, key, generator, *, condition=None, args=(), kwargs=None):
        """
        **LLM Docstring**

        Evaluate or load a keyed value through `dev.cached_eval`, using this checkpointer as the mapping backend.

        :param key: the storage or lookup key
        :type key: object
        :param generator: callable used to produce a missing cached value
        :type generator: object
        :param condition: optional predicate controlling cache reuse
        :type condition: object
        :param args: positional arguments forwarded to a callable
        :type args: object
        :param kwargs: keyword arguments forwarded to a callable
        :type kwargs: object
        :return: the cached value when valid, otherwise the newly generated and stored value
        :rtype: object
        """
        ...

    @property
    def is_open(self):
        """
        **LLM Docstring**

        Report whether a checkpoint stream is currently open.

        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    @property
    def stream(self):
        """
        **LLM Docstring**

        Return the currently open stream, or `None` outside an active context.

        :return: the current backend stream, or `None` when closed
        :rtype: object | None
        """
        ...

    @abc.abstractmethod
    def open_checkpoint_file(self, chk):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def close_checkpoint_file(self, stream):
        """
        Closes the opened checkpointing stream
        :param stream:
        :type stream:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def save_parameter(self, key, value):
        """
        Saves a parameter to the checkpoint file
        :param key:
        :type key:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def load_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def delete_parameter(self, key):
        """
        **LLM Docstring**

        Default deletion hook; concrete checkpointers must override it to support deletion.

        :param key: the storage or lookup key
        :type key: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def check_parameter(self, key):
        """
        **LLM Docstring**

        Validate the key policy and test whether loading the key succeeds.

        :param key: the storage or lookup key
        :type key: object
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    def update(self, vals):
        """
        **LLM Docstring**

        Write all key/value pairs from a mapping or iterable, opening the checkpoint around the operation when needed.

        :param vals: mapping or iterable of key/value pairs
        :type vals: object
        :return: No explicit value unless noted by the underlying delegated operation.
        :rtype: None | object
        """
        ...

    def get_keys(self, keys):
        """
        **LLM Docstring**

        Load a sequence of keys in order, with automatic context management.

        :param keys: keys to load, save, or filter
        :type keys: object
        :return: values loaded for `keys` in the same order
        :rtype: list[object]
        """
        ...

    def check_allowed_key(self, item):
        """
        **LLM Docstring**

        Enforce top-level allow and omit lists; tuple paths are checked by their first component.

        :param item: the lookup key or index
        :type item: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def __contains__(self, key):
        """
        **LLM Docstring**

        Test whether a permitted key exists, opening the checkpoint temporarily if required.

        :param key: the storage or lookup key
        :type key: object
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Validate and load a key, automatically managing the stream lifecycle.

        :param item: the lookup key or index
        :type item: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def get(self, key, default=None):
        """
        **LLM Docstring**

        Load a key and return `default` when the backend raises `KeyError`.

        :param key: the storage or lookup key
        :type key: object
        :param default: the fallback returned when a key is absent
        :type default: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Validate and save a key/value pair, opening the checkpoint temporarily if required.

        :param key: the storage or lookup key
        :type key: object
        :param value: the value to store
        :type value: object
        :return: No explicit value unless noted by the underlying delegated operation.
        :rtype: None | object
        """
        ...

    def __delitem__(self, key):
        """
        **LLM Docstring**

        Validate and delete a key, opening the checkpoint temporarily if required.

        :param key: the storage or lookup key
        :type key: object
        :return: no explicit value; the selected key is removed
        :rtype: None
        """
        ...

    def pop(self, key, *default):
        """
        **LLM Docstring**

        Load and delete a key, optionally returning a supplied default when the key is absent.

        :param key: the storage or lookup key
        :type key: object
        :param default: the fallback returned when a key is absent
        :type default: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    @abc.abstractmethod
    def keys(self):
        """
        Returns the keys of currently checkpointed
        objects

        :return:
        :rtype:
        """
        ...

class DumpCheckpointer(Checkpointer):
    """
    A subclass of `CheckpointerBase` that writes an entire dump to file at once & maintains
    a backend cache to update it cleanly
    """

    def __init__(self, file, cache=None, open_kwargs=None, allowed_keys=None, omitted_keys=None):
        """
        **LLM Docstring**

        Initialize a whole-file checkpointer with an in-memory backend cache and file-open options.

        :param file: path or file-like object
        :type file: object
        :param cache: initial in-memory backend cache
        :type cache: object
        :param open_kwargs: arguments used when opening a file target
        :type open_kwargs: object
        :param allowed_keys: optional whitelist of permitted top-level keys
        :type allowed_keys: object
        :param omitted_keys: optional blacklist of top-level keys
        :type omitted_keys: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def load_cache(self):
        """
        **LLM Docstring**

        Create an empty dictionary when no backend cache has been loaded.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Ensure the backend cache is loaded before opening the checkpoint stream.

        :return: The active context object.
        :rtype: object
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Dump the entire cache before closing the stream, even when cleanup must run after a dump failure.

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

    @abc.abstractmethod
    def dump(self):
        """
        Writes the entire data structure
        :return:
        :rtype:
        """
        ...

    def convert(self):
        """
        Converts the cache to an exportable form if needed
        :return:
        :rtype:
        """
        ...

    def open_checkpoint_file(self, chk):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk:
        :return:
        :rtype:
        """
        ...

    def close_checkpoint_file(self, stream):
        """
        Closes the opened checkpointing stream
        :param stream:
        :type stream:
        :return:
        :rtype:
        """
        ...

    def save_parameter(self, key, value):
        """
        Saves a parameter to the checkpoint file
        :param key:
        :type key:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        ...

    def check_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def load_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def delete_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def keys(self):
        """
        **LLM Docstring**

        Return top-level backend keys, opening the checkpointer temporarily if necessary.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        ...

class JSONCheckpointer(DumpCheckpointer):
    """
    A checkpointer that uses JSON as a backend
    """
    default_extension = JSONSerializer.default_extension

    def __init__(self, file, cache=None, serializer=None, open_kwargs=None, allowed_keys=None, omitted_keys=None):
        """
        **LLM Docstring**

        Configure a dump checkpointer to encode its dictionary backend with `JSONSerializer`.

        :param file: path or file-like object
        :type file: object
        :param cache: initial in-memory backend cache
        :type cache: object
        :param serializer: serializer instance or specification
        :type serializer: object
        :param open_kwargs: arguments used when opening a file target
        :type open_kwargs: object
        :param allowed_keys: optional whitelist of permitted top-level keys
        :type allowed_keys: object
        :param omitted_keys: optional blacklist of top-level keys
        :type omitted_keys: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def load_cache(self):
        """
        **LLM Docstring**

        Load a nonempty JSON checkpoint into a dictionary, otherwise initialize an empty cache.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def dump(self):
        """
        Writes the entire data structure
        :return:
        :rtype:
        """
        ...

class NumPyCheckpointer(DumpCheckpointer):
    """
    A checkpointer that uses NumPy as a backend
    """
    default_extension = NumPySerializer.default_extension

    def __init__(self, file, cache=None, serializer=None, open_kwargs=None, allowed_keys=None, omitted_keys=None):
        """
        **LLM Docstring**

        Resolve existing `.npz` or `.npy` variants and configure a binary NumPy dump backend.

        :param file: path or file-like object
        :type file: object
        :param cache: initial in-memory backend cache
        :type cache: object
        :param serializer: serializer instance or specification
        :type serializer: object
        :param open_kwargs: arguments used when opening a file target
        :type open_kwargs: object
        :param allowed_keys: optional whitelist of permitted top-level keys
        :type allowed_keys: object
        :param omitted_keys: optional blacklist of top-level keys
        :type omitted_keys: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def load_cache(self):
        """
        **LLM Docstring**

        Load a nonempty NumPy checkpoint into a dictionary, otherwise initialize an empty cache.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def dump(self):
        """
        Writes the entire data structure
        :return:
        :rtype:
        """
        ...

class HDF5Checkpointer(Checkpointer):
    """
    A checkpointer that uses an HDF5 file as a backend.
    Doesn't maintain a secondary `dict`, because HDF5 is an updatable format.
    """
    default_extension = HDF5Serializer.default_extension

    def __init__(self, checkpoint_file, serializer=None, allowed_keys=None, omitted_keys=None):
        """
        **LLM Docstring**

        Initialize direct, updateable HDF5 checkpoint access without a secondary dictionary cache.

        :param checkpoint_file: path or file-like checkpoint target
        :type checkpoint_file: object
        :param serializer: serializer instance or specification
        :type serializer: object
        :param allowed_keys: optional whitelist of permitted top-level keys
        :type allowed_keys: object
        :param omitted_keys: optional blacklist of top-level keys
        :type omitted_keys: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def open_checkpoint_file(self, chk):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk: str | file-like
        :return:
        :rtype:
        """
        ...

    def close_checkpoint_file(self, stream):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk:
        :return:
        :rtype:
        """
        ...

    def save_parameter(self, key, value):
        """
        Saves a parameter to the checkpoint file
        :param key:
        :type key:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        ...

    def load_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def keys(self):
        """
        **LLM Docstring**

        Open the stream as an HDF5 file or group as needed and return its top-level keys.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        ...

class DictCheckpointer(Checkpointer):
    """
    A checkpointer that doesn't actually do anything, but which is provided
    so that programs can turn off checkpointing without changing their layout
    """

    def __init__(self, checkpoint_file=None, allowed_keys=None, omitted_keys=None):
        """
        **LLM Docstring**

        Wrap an in-memory dictionary in the standard checkpointer interface.

        :param checkpoint_file: path or file-like checkpoint target
        :type checkpoint_file: object
        :param allowed_keys: optional whitelist of permitted top-level keys
        :type allowed_keys: object
        :param omitted_keys: optional blacklist of top-level keys
        :type omitted_keys: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def open_checkpoint_file(self, chk):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk: str | file-like
        :return:
        :rtype:
        """
        ...

    def close_checkpoint_file(self, stream):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk:
        :return:
        :rtype:
        """
        ...

    def save_parameter(self, key, value):
        """
        Saves a parameter to the checkpoint file
        :param key:
        :type key:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        ...

    def load_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def delete_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def keys(self):
        """
        **LLM Docstring**

        Return a list of in-memory checkpoint keys.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        ...

    def get(self, key, default=None):
        """
        **LLM Docstring**

        Return a dictionary value or default without opening a stream.

        :param key: the storage or lookup key
        :type key: object
        :param default: the fallback returned when a key is absent
        :type default: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def pop(self, key, *default):
        """
        **LLM Docstring**

        Remove and return a dictionary value using normal `dict.pop` semantics.

        :param key: the storage or lookup key
        :type key: object
        :param default: the fallback returned when a key is absent
        :type default: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

class NullCheckpointer(Checkpointer):
    """
    A checkpointer that saves absolutely nothing
    """

    def __init__(self, checkpoint_file=None, allowed_keys=None, omitted_keys=None):
        """
        **LLM Docstring**

        Initialize a checkpointer that deliberately stores no values.

        :param checkpoint_file: path or file-like checkpoint target
        :type checkpoint_file: object
        :param allowed_keys: optional whitelist of permitted top-level keys
        :type allowed_keys: object
        :param omitted_keys: optional blacklist of top-level keys
        :type omitted_keys: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def open_checkpoint_file(self, chk):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk: str | file-like
        :return:
        :rtype:
        """
        ...

    def close_checkpoint_file(self, stream):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk:
        :return:
        :rtype:
        """
        ...

    def save_parameter(self, key, value):
        """
        Saves a parameter to the checkpoint file
        :param key:
        :type key:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        ...

    def load_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def delete_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def keys(self):
        """
        **LLM Docstring**

        Return an empty key list because the null backend never retains data.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        ...