"""
A typed, content-addressed object store.

Each entry is a directory (see `EntryStore`) holding a metadata file (`meta.json`: class path,
``state_version``, layout, sizes, provenance, creation time, host and user) and a payload written through
the indexed NumPy checkpointer. A value is pseudo-pickled to a tree of plain data; every NumPy array in
the tree (at any depth) is taken out and stored as its own `.npy` member, so it keeps its dtype and shape
and can be memory-mapped, and the rest of the tree is stored as JSON with tuples and NumPy scalars tagged,
so the Python types come back exactly. A mapping is stored one member per key, so
``store.get(key, lazy=True)`` can load a single field. Writes are atomic and locked across processes.
"""
from __future__ import annotations

import collections.abc
import getpass
import json
import os
import socket

import numpy as np

from ..Devutils import EntryStore, chained_key, fingerprint, implementation_signature
from .Checkpointing import IndexedNumPyCheckpointer
from .Serializers import PseudoPickler

__all__ = [
    "ObjectStore",
    "LazyEntry",
    "ObjectTooLarge",
]


class _PlainJSON:
    """Writes UTF-8 JSON bytes with no pseudo-pickling (the tree was already pseudo-pickled by the store)."""

    def serialize(self, file, data, **kwargs):
        file.write(json.dumps(data).encode("utf-8"))

    def deserialize(self, file, **kwargs):
        return json.load(file)


_ARRAY, _TUPLE, _SCALAR = "__objectstore_array__", "__objectstore_tuple__", "__objectstore_scalar__"


def _extract(tree, arrays):
    """Replaces arrays, NumPy scalars and tuples in a pseudo-pickled tree so the rest is plain JSON data."""
    if isinstance(tree, np.ndarray) and tree.dtype != np.dtype(object):
        arrays.append(tree)
        return {_ARRAY: len(arrays) - 1}
    if isinstance(tree, np.generic):
        arrays.append(np.asarray(tree))
        return {_SCALAR: len(arrays) - 1}
    if isinstance(tree, tuple):
        return {_TUPLE: [_extract(x, arrays) for x in tree]}
    if isinstance(tree, list):
        return [_extract(x, arrays) for x in tree]
    if isinstance(tree, dict):
        return {k: _extract(v, arrays) for k, v in tree.items()}
    return tree


def _inject(tree, array):
    """Inverse of `_extract`; ``array(i)`` supplies the i-th array."""
    if isinstance(tree, list):
        return [_inject(x, array) for x in tree]
    if isinstance(tree, dict):
        if len(tree) == 1:
            (tag, value), = tree.items()
            if tag == _ARRAY:
                return array(value)
            if tag == _SCALAR:
                return array(value)[()]
            if tag == _TUPLE:
                return tuple(_inject(x, array) for x in value)
        return {k: _inject(v, array) for k, v in tree.items()}
    return tree


class ObjectTooLarge(ValueError):
    """Raised by `ObjectStore.put` when a payload is over the store's per-entry limit."""


class LazyEntry(collections.abc.Mapping):
    """
    A handle on a stored entry that reads data only when asked. For a stored mapping it behaves as a
    read-only mapping (each field is loaded on access); otherwise `load()` returns the object.
    """

    def __init__(self, store, key, meta, mmap=False):
        self.store = store
        self.key = key
        self.meta = meta
        self.mmap = mmap

    def _checkpoint(self):
        return self.store._payload(self.key, mmap=self.mmap)

    def load(self):
        return self.store._load(self.key, self.meta, mmap=self.mmap)

    def _fields(self):
        if self.meta.get("layout") != "mapping":
            raise TypeError("entry {} holds a single object, use `load()`".format(self.key[:12]))
        return self.meta["fields"]  # name -> "array" or "tree"

    def __getitem__(self, name):
        if name not in self._fields():
            raise KeyError(name)
        with self._checkpoint() as ckpt:
            return self.store._read_field(ckpt, name, self.meta["fields"][name])

    def __iter__(self):
        self._fields()
        return iter(self.meta.get("field_order", self.meta["fields"]))

    def __len__(self):
        return len(self._fields())

    def __repr__(self):
        return "{}({}, {})".format(type(self).__name__, self.key[:12], self.meta.get("class"))


class ObjectStore(EntryStore):
    """
    ``ObjectStore(root).put(obj)`` stores any object the serializers can handle under its fingerprint
    (or an explicit key) and ``get(key)`` rebuilds it. ``cached_eval(parts, generator)`` computes a value
    once per distinct ``parts``.
    """

    lock_name = ".lock"
    payload_name = "payload.nptar"
    store_env_var = "MCUTILS_STORE"
    _default = {}

    def __init__(self, root=None, algorithm="sha256", allow_pickle=False, max_bytes=None, max_entry_bytes=None,
                 signature_modules=(), provenance=None, serializer=None):
        """
        :param root: the store directory (default: `default_root()`)
        :param algorithm: hash used for default keys (sha256 gives the 64-hex keys the other stores use)
        :param allow_pickle: whether values the serializers can't express may be pickled (and loaded)
        :param max_bytes: when set, `gc` runs after a `put` that takes the store over this size
        :param max_entry_bytes: payloads over this size raise `ObjectTooLarge` (and aren't cached by `cached_eval`)
        :param signature_modules: packages whose `implementation_signature` is recorded with each entry
        :param provenance: default user metadata recorded with each entry
        """
        super().__init__(self.default_root() if root is None else root)
        if algorithm != "sha256":
            self.key_pattern = r"[0-9a-f]{%d}" % (len(chained_key("x", algorithm=algorithm)))
        self.algorithm = algorithm
        self.allow_pickle = allow_pickle
        self.max_bytes = max_bytes
        self.max_entry_bytes = max_entry_bytes
        self.signature_modules = tuple(signature_modules)
        self.provenance = {} if provenance is None else dict(provenance)
        self.serializer = serializer

    # ---- locations ---- #
    @classmethod
    def default_root(cls):
        """``$MCUTILS_STORE`` if set, else ``~/.local/share/McUtils/store``."""
        return os.environ.get(cls.store_env_var) or os.path.expanduser("~/.local/share/McUtils/store")

    @classmethod
    def default(cls):
        """The shared store at `default_root()` (one instance per root)."""
        root = cls.default_root()
        if root not in cls._default:
            cls._default[root] = cls(root)
        return cls._default[root]

    def key_for(self, *parts):
        """The key `cached_eval` uses for ``parts`` (or `put` for a single object)."""
        return chained_key(*parts, algorithm=self.algorithm)

    # ---- payloads ---- #
    @staticmethod
    def _field_key(name):
        return "field/" + name

    def _make_serializer(self):
        # the skeleton is plain JSON (the NumPy serializer would turn scalars and lists into arrays)
        return self.serializer if self.serializer is not None else _PlainJSON()

    def _payload(self, key, mmap=False, path=None):
        return IndexedNumPyCheckpointer(path or self.entry_path(key, self.payload_name),
                                        serializer=self._make_serializer(), mmap=mmap)

    @staticmethod
    def _class_path(obj):
        cls = type(obj)
        return "{}:{}".format(cls.__module__, cls.__qualname__)

    def _pickler(self):
        return PseudoPickler(b64encode=True, allow_pickle=self.allow_pickle)

    def _write_field(self, ckpt, name, value):
        """Writes one value; returns how it was stored (``"array"`` or ``"tree"``)."""
        field = self._field_key(name)
        if type(value) is np.ndarray and value.dtype != np.dtype(object):
            ckpt[field] = value
            return "array"
        arrays = []
        skeleton = _extract(self._pickler().serialize(value), arrays)
        ckpt[field + "/tree"] = skeleton
        for i, array in enumerate(arrays):
            ckpt["{}/array/{}".format(field, i)] = array
        return "tree"

    def _read_field(self, ckpt, name, kind):
        field = self._field_key(name)
        if kind == "array":
            return ckpt[field]
        skeleton = ckpt[field + "/tree"]
        return self._pickler().deserialize(_inject(skeleton, lambda i: ckpt["{}/array/{}".format(field, i)]))

    def _load(self, key, meta, mmap=False):
        with self._payload(key, mmap=mmap) as ckpt:
            if meta.get("layout") == "mapping":
                return {name: self._read_field(ckpt, name, meta["fields"][name])
                        for name in meta.get("field_order", meta["fields"])}
            return self._read_field(ckpt, "object", meta["fields"]["object"])

    # ---- reading ---- #
    def meta(self, key):
        """The metadata recorded for ``key``, or ``None``."""
        return self.read_meta(key)

    def get(self, key, lazy=False, mmap=False, default=KeyError):
        """
        Loads the object stored under ``key``.

        :param lazy: return a `LazyEntry` that loads fields on access instead of the object
        :param mmap: return arrays as read-only memory maps
        :param default: returned for a missing key; the default raises `KeyError`
        """
        meta = self.read_meta(key)
        if meta is None:
            if default is KeyError:
                raise KeyError(key)
            return default
        self.touch(key)
        if lazy:
            return LazyEntry(self, key, meta, mmap=mmap)
        return self._load(key, meta, mmap=mmap)

    def find(self, **filters):
        """
        Keys whose metadata matches every filter. Names may be dotted to reach into nested metadata
        (``provenance__source`` or ``provenance.source``), and a callable value is used as a predicate.
        """
        found = []
        for key in self.keys():
            meta = self.read_meta(key)
            for name, wanted in filters.items():
                value = meta
                for part in name.replace("__", ".").split("."):
                    value = value.get(part) if isinstance(value, dict) else None
                if not (wanted(value) if callable(wanted) else value == wanted):
                    break
            else:
                found.append(key)
        return found

    # ---- writing ---- #
    def put(self, obj, key=None, meta=None, replace=False):
        """
        Stores ``obj`` and returns its key (``fingerprint(obj)`` unless given).

        :param meta: extra metadata recorded as ``provenance`` (merged over the store's default)
        :param replace: overwrite an existing entry (by default an existing entry is kept)
        :raises ObjectTooLarge: if the payload is over ``max_entry_bytes``
        """
        if key is None:
            key = fingerprint(obj)
        self.check_key(key)
        if not replace and self.has(key):
            self.touch(key)
            return key
        entry_meta = {
            "class": self._class_path(obj),
            "state_version": getattr(type(obj), "state_version", None),
            "created_by": {"host": socket.gethostname(), "user": _user()},
            "provenance": dict(self.provenance, **(meta or {})),
        }
        if self.signature_modules:
            entry_meta["implementation"] = implementation_signature(*self.signature_modules)
        with self.stage(key, entry_meta, replace=replace) as staged:
            with self._payload(key, path=staged.file(self.payload_name)) as ckpt:
                if type(obj) is dict and all(isinstance(k, str) for k in obj):
                    staged.meta["layout"] = "mapping"
                    staged.meta["fields"] = {name: self._write_field(ckpt, name, value) for name, value in obj.items()}
                    staged.meta["field_order"] = list(obj)  # the metadata file is written with sorted keys
                else:
                    staged.meta["layout"] = "object"
                    staged.meta["fields"] = {"object": self._write_field(ckpt, "object", obj)}
            size = os.path.getsize(staged.file(self.payload_name))
            if self.max_entry_bytes is not None and size > self.max_entry_bytes:
                raise ObjectTooLarge("{} bytes is over the entry limit of {}".format(size, self.max_entry_bytes))
            staged.meta["payload_bytes"] = size
        if self.max_bytes is not None:
            self.gc(max_bytes=self.max_bytes, protect=[key])
        return key

    def cached_eval(self, key_parts, generator, meta=None, lazy=False, mmap=False):
        """
        Returns the stored value for ``key_parts``, computing it with ``generator()`` (and storing it) the
        first time. ``key_parts`` is a value or a tuple of values folded with `chained_key`; a value too
        large for the store is returned without being cached.
        """
        parts = key_parts if isinstance(key_parts, tuple) else (key_parts,)
        key = self.key_for(*parts)
        if self.has(key):
            return self.get(key, lazy=lazy, mmap=mmap)
        value = generator()
        try:
            self.put(value, key=key, meta=meta)
        except ObjectTooLarge:
            return value
        return self.get(key, lazy=lazy, mmap=mmap) if lazy else value


def _user():
    try:
        return getpass.getuser()
    except Exception:
        return None
