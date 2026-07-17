
import abc, os
from .. import Devutils as dev
from .Serializers import *

__all__ = [
    "Checkpointer",
    "CheckpointerKeyError",
    "DumpCheckpointer",
    "JSONCheckpointer",
    "NumPyCheckpointer",
    "HDF5Checkpointer",
    "DictCheckpointer",
    "NullCheckpointer"
]

class CheckpointerKeyError(KeyError):
    ...

class Checkpointer(metaclass=abc.ABCMeta):
    """
    General purpose base class that allows checkpointing to be done easily and cleanly.
    Intended to be a passable object that allows code to checkpoint easily.
    """

    default_extension=""
    def __init__(self, checkpoint_file,
                 allowed_keys=None,
                 omitted_keys=None
                 ):
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
        self.checkpoint_file = checkpoint_file
        self.allowed_keys = allowed_keys
        self.omitted_keys = omitted_keys
        self._came_open = not isinstance(checkpoint_file, str)
        self._open_depth = 0
        self._stream = None
    def __repr__(self):
        """
        **LLM Docstring**

        Render the concrete checkpointer type and checkpoint target.

        :return: A human-readable string representation.
        :rtype: str
        """
        return "{}({!r})".format(type(self).__name__, self.checkpoint_file)

    _ext_map = None
    @classmethod
    def extension_map(cls):
        """
        **LLM Docstring**

        Return the extension-to-checkpointer dispatch table, honoring a class-level override when present.

        :return: a mapping from filename extensions to concrete checkpointer classes
        :rtype: dict[str, type[Checkpointer]]
        """
        if cls._ext_map is not None:
            return cls._ext_map
        else:
            return {c.default_extension:c for c in [JSONCheckpointer, HDF5Checkpointer, NumPyCheckpointer]}

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

        if checkpoint is None:
            return NullCheckpointer(None)
        elif isinstance(checkpoint, str):
            return Checkpointer.from_file(checkpoint)
        elif isinstance(checkpoint, Checkpointer):
            return checkpoint
        elif dev.is_dict_like(checkpoint):
            if dev.Schema(["file"]).validate(checkpoint, throw=False):
                checkpoint = dev.Schema(["file"], ['keys', 'opts']).to_dict(checkpoint)
                opts = checkpoint['opts'] if 'opts' in checkpoint else {}
                if 'keys' in checkpoint:
                    allowed_opts = dev.Schema(['allowed_keys'], ['omitted_keys']).to_dict(checkpoint['keys'], throw=False)
                    if allowed_opts is not None:
                        opts = dict(opts, **allowed_opts)
                    else:
                        omitted_opts = dev.Schema(['omitted_keys']).to_dict(checkpoint['keys'], throw=False)
                        if allowed_opts is not None:
                            opts = dict(opts, **omitted_opts)
                        else:
                            opts['allowed_keys'] = checkpoint['keys']
                return cls.from_file(checkpoint['file'], **opts)
            else:
                return DictCheckpointer(checkpoint)
        else:
            return checkpoint

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

        if not isinstance(file, str):
            #TODO: make this cleaner
            file_name = file.name # might break in the future...
        else:
            file_name = file

        _, ext = os.path.splitext(file_name)

        ext_map = cls.extension_map()

        if ext not in ext_map:
            raise ValueError("don't know have default checkpointer type registered for extension {}".format(ext))

        return ext_map[ext](file, **opts)

    def __enter__(self):
        """
        **LLM Docstring**

        Increment the nested-open count and lazily open the checkpoint stream on the outermost entry.

        :return: The active context object.
        :rtype: object
        """
        self._open_depth+=1
        if self._stream is None:
            self._stream = self.open_checkpoint_file(self.checkpoint_file)
        return self
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
        self._open_depth-=1
        if self._stream is not None:
            if self._open_depth == 0:
                self.close_checkpoint_file(self._stream)
                self._stream = None

    def cached_eval(self, key, generator, *,
                    condition=None,
                    args=(),
                    kwargs=None):
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
        return dev.cached_eval(
            self,
            key,
            generator,
            condition=condition,
            args=args,
            kwargs=kwargs
        )

    @property
    def is_open(self):
        """
        **LLM Docstring**

        Report whether a checkpoint stream is currently open.

        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        return self._stream is not None

    @property
    def stream(self):
        """
        **LLM Docstring**

        Return the currently open stream, or `None` outside an active context.

        :return: the current backend stream, or `None` when closed
        :rtype: object | None
        """
        return self._stream

    @abc.abstractmethod
    def open_checkpoint_file(self, chk):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk:
        :return:
        :rtype:
        """
        raise NotImplementedError("CheckpointerBase is an abstract base class...")
    @abc.abstractmethod
    def close_checkpoint_file(self, stream):
        """
        Closes the opened checkpointing stream
        :param stream:
        :type stream:
        :return:
        :rtype:
        """
        raise NotImplementedError("CheckpointerBase is an abstract base class...")
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
        raise NotImplementedError("CheckpointerBase is an abstract base class...")
    @abc.abstractmethod
    def load_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        raise NotImplementedError("CheckpointerBase is an abstract base class...")

    def delete_parameter(self, key):
        """
        **LLM Docstring**

        Default deletion hook; concrete checkpointers must override it to support deletion.

        :param key: the storage or lookup key
        :type key: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        raise NotImplementedError("checkpointer does not need to implement deletion")
    def check_parameter(self, key):
        """
        **LLM Docstring**

        Validate the key policy and test whether loading the key succeeds.

        :param key: the storage or lookup key
        :type key: object
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        try:
            self.check_allowed_key(key)
            self.__getitem__(key)
        except KeyError:
            return False
        else:
            return True

    def update(self, vals):
        """
        **LLM Docstring**

        Write all key/value pairs from a mapping or iterable, opening the checkpoint around the operation when needed.

        :param vals: mapping or iterable of key/value pairs
        :type vals: object
        :return: No explicit value unless noted by the underlying delegated operation.
        :rtype: None | object
        """
        if dev.is_dict_like(vals):
            return self.update(vals.items())

        if not self.is_open:
            with self:
                return self.update(vals)

        for k, v in vals:
            self[k] = v
    def get_keys(self, keys):
        """
        **LLM Docstring**

        Load a sequence of keys in order, with automatic context management.

        :param keys: keys to load, save, or filter
        :type keys: object
        :return: values loaded for `keys` in the same order
        :rtype: list[object]
        """
        if not self.is_open:
            with self:
                return self.get_keys(keys)

        return [
            self[k] for k in keys
        ]

    def check_allowed_key(self, item):
        """
        **LLM Docstring**

        Enforce top-level allow and omit lists; tuple paths are checked by their first component.

        :param item: the lookup key or index
        :type item: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        if isinstance(item, tuple):
            # for subkey in item:
            self.check_allowed_key(item[0]) # only check topline items
        else:
            if self.allowed_keys is not None:
                if item not in self.allowed_keys:
                    raise CheckpointerKeyError("key {} not allowed by {}".format(
                        item,
                        self
                    ))
            if self.omitted_keys is not None:
                if item in self.omitted_keys:
                    raise CheckpointerKeyError("key {} not allowed by {}".format(
                        item,
                        self
                    ))

    def __contains__(self, key):
        """
        **LLM Docstring**

        Test whether a permitted key exists, opening the checkpoint temporarily if required.

        :param key: the storage or lookup key
        :type key: object
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        if not self.is_open:
            with self:
                return self.__contains__(key)
        return self.check_parameter(key)

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Validate and load a key, automatically managing the stream lifecycle.

        :param item: the lookup key or index
        :type item: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        if not self.is_open:
            with self:
                return self.__getitem__(item)
        self.check_allowed_key(item)
        return self.load_parameter(item)
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
        try:
            val = self[key]
        except KeyError:
            val = default
        return val
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
        if not self.is_open:
            with self:
                return self.__setitem__(key, value)
        self.check_allowed_key(key)
        self.save_parameter(key, value)

    def __delitem__(self, key):
        """
        **LLM Docstring**

        Validate and delete a key, opening the checkpoint temporarily if required.

        :param key: the storage or lookup key
        :type key: object
        :return: no explicit value; the selected key is removed
        :rtype: None
        """
        if not self.is_open:
            with self:
                return self.__delitem__(key)
        self.check_allowed_key(key)
        self.delete_parameter(key)
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
        if len(default) > 0:
            try:
                val = self[key]
            except KeyError:
                val = default[0]
            else:
                del self[key]
        else:
            val = self[key]
            del self[key]
        return val

    @abc.abstractmethod
    def keys(self):
        """
        Returns the keys of currently checkpointed
        objects

        :return:
        :rtype:
        """
        raise NotImplementedError("Checkpointer is an abstract base class...")

class DumpCheckpointer(Checkpointer):
    """
    A subclass of `CheckpointerBase` that writes an entire dump to file at once & maintains
    a backend cache to update it cleanly
    """
    def __init__(self, file, cache=None, open_kwargs=None,
                 allowed_keys=None,
                 omitted_keys=None
                 ):
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
        self.backend = cache # cache values
        super().__init__(file, allowed_keys=allowed_keys, omitted_keys=omitted_keys)
        if open_kwargs is None:
            open_kwargs = {'mode':"w+"}
        self.open_kwargs = open_kwargs
    def load_cache(self):
        """
        **LLM Docstring**

        Create an empty dictionary when no backend cache has been loaded.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        if self.backend is None:
            self.backend = {}
    def __enter__(self):
        """
        **LLM Docstring**

        Ensure the backend cache is loaded before opening the checkpoint stream.

        :return: The active context object.
        :rtype: object
        """
        self.load_cache()
        return super().__enter__()
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
        try:
            self.dump()
        finally:
            super().__exit__(exc_type, exc_val, exc_tb)
    @abc.abstractmethod
    def dump(self):
        """
        Writes the entire data structure
        :return:
        :rtype:
        """
        raise NotImplementedError("DumpCheckpointer is an ABC and doesn't know how to write to file")
    def convert(self):
        """
        Converts the cache to an exportable form if needed
        :return:
        :rtype:
        """
        return self.backend
    def open_checkpoint_file(self, chk):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk:
        :return:
        :rtype:
        """
        if isinstance(chk, str):
            chk = open(chk, **self.open_kwargs)
        return chk
    def close_checkpoint_file(self, stream):
        """
        Closes the opened checkpointing stream
        :param stream:
        :type stream:
        :return:
        :rtype:
        """
        if not self._came_open:
            stream.close()
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
        if isinstance(key, tuple):
            base = self.backend
            cur = key[0]
            for subk in key[1:]:
                if cur not in base: base[cur] = {}
                base = base[cur]
                cur = subk
            base[cur] = value
        else:
            self.backend[key] = value
    def check_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        if isinstance(key, tuple):
            base = self.backend
            cur = key[0]
            for subk in key[1:]:
                if cur not in base: return False
                base = base[cur]
                cur = subk
            return cur in base
        else:
            return key in self.backend
    def load_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        if isinstance(key, tuple):
            base = self.backend
            cur = key[0]
            for subk in key[1:]:
                if cur not in base:
                    raise KeyError(f"{key} not found")
                base = base[cur]
                cur = subk
            val = base[cur]
        else:
            val = self.backend[key]
        return val
    def delete_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        if isinstance(key, tuple):
            base = self.backend
            cur = key[0]
            for subk in key[1:]:
                if cur not in base:
                    raise KeyError(f"{key} not found")
                base = base[cur]
                cur = subk
            del base[cur]
        else:
            del self.backend[key]

    def keys(self):
        """
        **LLM Docstring**

        Return top-level backend keys, opening the checkpointer temporarily if necessary.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        if not self.is_open:
            with self:
                return self.keys()
        return self.backend.keys()

class JSONCheckpointer(DumpCheckpointer):
    """
    A checkpointer that uses JSON as a backend
    """

    default_extension=JSONSerializer.default_extension
    def __init__(self, file, cache=None, serializer=None, open_kwargs=None,
                 allowed_keys=None,
                 omitted_keys=None
                 ):
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
        if serializer is None:
            serializer = JSONSerializer()
        self.serializer = serializer
        super().__init__(file, cache=cache, open_kwargs=open_kwargs, allowed_keys=allowed_keys, omitted_keys=omitted_keys)

    def load_cache(self):
        """
        **LLM Docstring**

        Load a nonempty JSON checkpoint into a dictionary, otherwise initialize an empty cache.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        cache = self.backend
        if cache is None:
            file = self.checkpoint_file
            serializer = self.serializer
            if isinstance(file, str) and os.path.exists(file) and os.stat(file).st_size > 0:
                with open(file, 'r') as stream:
                    cache = serializer.deserialize(stream)
                if not isinstance(cache, dict):
                    cache = {}
            else:
                cache = {}
            self.backend = cache

    def dump(self):
        """
        Writes the entire data structure
        :return:
        :rtype:
        """
        self.serializer.serialize(self.stream, self.backend)

class NumPyCheckpointer(DumpCheckpointer):
    """
    A checkpointer that uses NumPy as a backend
    """

    default_extension = NumPySerializer.default_extension
    def __init__(self, file, cache=None, serializer=None, open_kwargs=None,
                 allowed_keys=None,
                 omitted_keys=None
                 ):
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
        if isinstance(file, str):
            if not os.path.exists(file):
                if os.path.exists(file + '.npz'):
                    file = file + '.npz'
                elif os.path.exists(file + '.npy'):
                    file = file + '.npy'

        if serializer is None:
            serializer = NumPySerializer()
        self.serializer = serializer
        if open_kwargs is None:
            open_kwargs = {'mode':'bw'}
        super().__init__(file, cache=cache, open_kwargs=open_kwargs,
                         allowed_keys=allowed_keys,
                         omitted_keys=omitted_keys
                         )

    def load_cache(self):
        """
        **LLM Docstring**

        Load a nonempty NumPy checkpoint into a dictionary, otherwise initialize an empty cache.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        cache = self.backend
        if cache is None:
            file = self.checkpoint_file
            serializer = self.serializer
            if isinstance(file, str) and os.path.exists(file) and os.stat(file).st_size > 0:
                with open(file, 'br') as stream:
                    cache = serializer.deserialize(stream)
                if not isinstance(cache, dict):
                    cache = {}
            else:
                cache = {}
            self.backend = cache

    def dump(self):
        """
        Writes the entire data structure
        :return:
        :rtype:
        """
        self.serializer.serialize(self.stream, self.backend)

class HDF5Checkpointer(Checkpointer):
    """
    A checkpointer that uses an HDF5 file as a backend.
    Doesn't maintain a secondary `dict`, because HDF5 is an updatable format.
    """

    default_extension = HDF5Serializer.default_extension
    def __init__(self, checkpoint_file, serializer=None,
                 allowed_keys=None,
                 omitted_keys=None
                 ):
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
        super().__init__(checkpoint_file, allowed_keys=allowed_keys, omitted_keys=omitted_keys)
        if serializer is None:
            serializer = HDF5Serializer()
        self.serializer = serializer

    def open_checkpoint_file(self, chk):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk: str | file-like
        :return:
        :rtype:
        """
        if not self._came_open:
            try:
                if os.path.exists(chk):
                    return open(chk, 'r+b')
                else:
                    return open(chk, "w+b")
            except ValueError as e:
                if e.args[0] == 'seek of closed file':
                    raise IOError("existing HDF5 file {} is corrupted and can't be opened".format(chk))
                else:
                    raise
        elif 'b' not in chk.mode:
            raise IOError("{} isn't opened in binary mode (HDF5 needs that)".format(chk))
        else:
            return chk

    def close_checkpoint_file(self, stream):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk:
        :return:
        :rtype:
        """
        if not self._came_open:
            self.stream.close()

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
        # HDF5 serialization is an updateable process
        if self.stream is None:
            raise IOError("stream for {} got closed and won't reopen".format(self.checkpoint_file))
        self.serializer.serialize(self.stream, {key:value})

    def load_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        return self.serializer.deserialize(self.stream, key=key)

    def keys(self):
        """
        **LLM Docstring**

        Open the stream as an HDF5 file or group as needed and return its top-level keys.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        if not self.is_open:
            with self:
                return self.keys()
        file = self.stream
        if not isinstance(file, (self.serializer.api.File, self.serializer.api.Group)):
            file = self.serializer.api.File(file, "a")
        return list(file.keys())

class DictCheckpointer(Checkpointer):
    """
    A checkpointer that doesn't actually do anything, but which is provided
    so that programs can turn off checkpointing without changing their layout
    """
    def __init__(self, checkpoint_file=None,
                 allowed_keys=None,
                 omitted_keys=None
                 ):
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
        if checkpoint_file is None:
            checkpoint_file = {}
        super().__init__(checkpoint_file, allowed_keys=allowed_keys, omitted_keys=omitted_keys)
        self.backend = checkpoint_file

    def open_checkpoint_file(self, chk):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk: str | file-like
        :return:
        :rtype:
        """
        return chk

    def close_checkpoint_file(self, stream):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk:
        :return:
        :rtype:
        """
        pass

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
        self.backend[key] = value

    def load_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        return self.backend[key]
    def delete_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        del self.backend[key]

    def keys(self):
        """
        **LLM Docstring**

        Return a list of in-memory checkpoint keys.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        return list(self.backend.keys())
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
        return self.backend.get(key, default)
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
        return self.backend.pop(key, *default)

class NullCheckpointer(Checkpointer):
    """
    A checkpointer that saves absolutely nothing
    """
    def __init__(self, checkpoint_file=None,
                 allowed_keys=None,
                 omitted_keys=None
                 ):
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
        super().__init__(checkpoint_file, allowed_keys=allowed_keys, omitted_keys=omitted_keys)
        self.backend = None

    def open_checkpoint_file(self, chk):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk: str | file-like
        :return:
        :rtype:
        """
        return "NotAFile"

    def close_checkpoint_file(self, stream):
        """
        Opens the passed `checkpoint_file` (if not already open)
        :param chk:
        :type chk:
        :return:
        :rtype:
        """
        pass

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
        pass

    def load_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        raise CheckpointerKeyError("NullCheckpointer doesn't support _any_ keys")

    def delete_parameter(self, key):
        """
        Loads a parameter from the checkpoint file
        :param key:
        :type key:
        :return:
        :rtype:
        """
        raise CheckpointerKeyError("NullCheckpointer doesn't support _any_ keys")

    def keys(self):
        """
        **LLM Docstring**

        Return an empty key list because the null backend never retains data.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        return []
