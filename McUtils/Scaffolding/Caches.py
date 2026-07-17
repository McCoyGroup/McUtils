import abc, weakref
import enum
from collections import OrderedDict
from .. import Devutils as dev

__all__ = [
    "Cache",
    "MaxSizeCache",
    "ObjectRegistry"
]

class Cache(metaclass=abc.ABCMeta):
    """
    Simple cache base class
    """
    @abc.abstractmethod
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Retrieve a cached value for `item`; concrete cache classes define the storage and access policy.

        This is an abstract or unfinished implementation and raises `NotImplementedError`.

        :param item: the lookup key or index
        :type item: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        raise NotImplementedError("Cache is an abstract base class")
    def get(self, item, default=None):
        """
        **LLM Docstring**

        Retrieve `item`, returning `default` only when the cache raises `KeyError`.

        :param item: the lookup key or index
        :type item: object
        :param default: the fallback returned when a key is absent
        :type default: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            return default
    @abc.abstractmethod
    def __contains__(self, item):
        """
        **LLM Docstring**

        Test whether an item is present in the concrete cache backend.

        This is an abstract or unfinished implementation and raises `NotImplementedError`.

        :param item: the lookup key or index
        :type item: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        raise NotImplementedError("Cache is an abstract base class")
    @abc.abstractmethod
    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Store a value under a cache key using the concrete backend policy.

        This is an abstract or unfinished implementation and raises `NotImplementedError`.

        :param key: the storage or lookup key
        :type key: object
        :param value: the value to store
        :type value: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        raise NotImplementedError("Cache is an abstract base class")

class MaxSizeBackend(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def keys(self):
        """
        **LLM Docstring**

        Return the keys currently stored by the bounded-cache backend.

        This is an abstract or unfinished implementation and raises `NotImplementedError`.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        cls = type(self)
        raise NotImplementedError(f"{cls.__name__} is an abstract base class")
    @abc.abstractmethod
    def __len__(self):
        """
        **LLM Docstring**

        Return the number of entries currently stored by the backend.

        This is an abstract or unfinished implementation and raises `NotImplementedError`.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        cls = type(self)
        raise NotImplementedError(f"{cls.__name__} is an abstract base class")
    @abc.abstractmethod
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Retrieve an entry from the backend, including any access-order side effects implemented by the backend.

        This is an abstract or unfinished implementation and raises `NotImplementedError`.

        :param item: the lookup key or index
        :type item: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        cls = type(self)
        raise NotImplementedError(f"{cls.__name__} is an abstract base class")
    @abc.abstractmethod
    def __contains__(self, item):
        """
        **LLM Docstring**

        Test whether the backend contains an item.

        This is an abstract or unfinished implementation and raises `NotImplementedError`.

        :param item: the lookup key or index
        :type item: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        cls = type(self)
        raise NotImplementedError(f"{cls.__name__} is an abstract base class")
    @abc.abstractmethod
    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Insert or replace an entry in the backend.

        This is an abstract or unfinished implementation and raises `NotImplementedError`.

        :param key: the storage or lookup key
        :type key: object
        :param value: the value to store
        :type value: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        cls = type(self)
        raise NotImplementedError(f"{cls.__name__} is an abstract base class")
    @abc.abstractmethod
    def pop(self):
        """
        **LLM Docstring**

        Remove and return the entry selected for eviction by the backend policy.

        This is an abstract or unfinished implementation and raises `NotImplementedError`.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        cls = type(self)
        raise NotImplementedError(f"{cls.__name__} is an abstract base class")

class LRUDict(MaxSizeBackend):
    def __init__(self):
        """
        **LLM Docstring**

        Initialize an empty `OrderedDict` used to track keys from least to most recently accessed.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.od = OrderedDict()
    def __len__(self):
        """
        **LLM Docstring**

        Return the number of entries in the ordered backend.

        :return: The number of stored entries.
        :rtype: int
        """
        return len(self.od)
    def keys(self):
        """
        **LLM Docstring**

        Return the ordered key view of the backend.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        return self.od.keys()
    def __contains__(self, item):
        """
        **LLM Docstring**

        Test membership without changing recency order.

        :param item: the lookup key or index
        :type item: object
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        return item in self.od
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Return a value and move its key to the most-recently-used end of the ordering.

        :param item: the lookup key or index
        :type item: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        val = self.od[item]
        self.od.move_to_end(item)
        return val
    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Store a value and mark its key as most recently used.

        :param key: the storage or lookup key
        :type key: object
        :param value: the value to store
        :type value: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.od[key] = value
        self.od.move_to_end(key)
    def pop(self):
        """
        **LLM Docstring**

        Evict and return the least-recently-used key/value pair.

        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        return self.od.popitem(last=False)

class FIFODict(MaxSizeBackend):
    def __init__(self):
        """
        **LLM Docstring**

        Initialize an insertion-ordered dictionary used as a first-in-first-out eviction queue.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.od = {}
    def __len__(self):
        """
        **LLM Docstring**

        Return the number of FIFO entries.

        :return: The number of stored entries.
        :rtype: int
        """
        return len(self.od)
    def keys(self):
        """
        **LLM Docstring**

        Return the insertion-ordered key view.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        return self.od.keys()
    def __contains__(self, item):
        """
        **LLM Docstring**

        Test membership without modifying insertion order.

        :param item: the lookup key or index
        :type item: object
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        return item in self.od
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Retrieve a value without changing its eviction position.

        :param item: the lookup key or index
        :type item: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        val = self.od[item]
        return val
    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Insert or replace a value; new keys remain ordered by insertion time.

        :param key: the storage or lookup key
        :type key: object
        :param value: the value to store
        :type value: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.od[key] = value
    def pop(self):
        """
        **LLM Docstring**

        Remove and return the earliest inserted key/value pair.

        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        return self.od.pop(next(iter(self.od.keys())))

class MaxSizeCache(Cache):
    """
    Simple lru-cache to support ravel/unravel ops
    """
    def __init__(self, max_items=128, cache_type=None):
        """
        **LLM Docstring**

        Construct a bounded cache using the selected backend and maximum entry count.

        :param max_items: maximum number of entries retained before eviction
        :type max_items: object
        :param cache_type: backend specification, callable, or registered backend name
        :type cache_type: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.backend = self.resolve_cache_type(cache_type)
        self.max_items = max_items
    class Backends(enum.Enum):
        LRU = "lru"
        FIFO = "fifo"
    cache_types = dev.OptionsMethodDispatch(
        {
            Backends.LRU:LRUDict,
            Backends.FIFO:FIFODict,
        },
        methods_enum=Backends,
        default_method=Backends.LRU
    )
    @classmethod
    def resolve_cache_type(cls, type_name):
        """
        **LLM Docstring**

        Resolve a callable or registered backend specification and instantiate the backend with its options.

        :param type_name: the backend class, registered name, option specification, or factory to resolve
        :type type_name: object
        :return: an initialized cache backend
        :rtype: MaxSizeBackend
        """
        if callable(type_name):
            method = type_name
            opts = {}
        else:
            method, opts = cls.cache_types.resolve(type_name)
        return method(**opts)

    def keys(self):
        """
        **LLM Docstring**

        Expose the keys from the selected backend.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        return self.backend.keys()
    def __contains__(self, item):
        """
        **LLM Docstring**

        Delegate membership testing to the backend.

        :param item: the lookup key or index
        :type item: object
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        return item in self.backend
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Retrieve an item through the backend, allowing policies such as LRU to update access order.

        :param item: the lookup key or index
        :type item: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        return self.backend.__getitem__(item)
    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Store an item and evict one backend-selected entry when the size exceeds `max_items`.

        :param key: the storage or lookup key
        :type key: object
        :param value: the value to store
        :type value: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.backend.__setitem__(key, value)
        if len(self.backend) > self.max_items:
            self.backend.pop()

class ObjectRegistryDefaults:
    Raise="raise"
    NotFound="NotFound"

class RegistryDefaultContext:
    def __init__(self, registry:'ObjectRegistry', value):
        """
        **LLM Docstring**

        Capture a registry and the temporary default value that should be installed in a context.

        :param registry: registry whose default is being changed
        :type registry: 'ObjectRegistry'
        :param value: the value to store
        :type value: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.reg = registry
        self.old = None
        self.val = value
    def __enter__(self):
        """
        **LLM Docstring**

        Save the current registry default and replace it with the temporary value.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.old = self.reg.default
        self.reg.default = self.val
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Restore the registry default that was active before entering the context.

        :param exc_type: exception type passed by the context manager protocol
        :type exc_type: object
        :param exc_val: exception instance passed by the context manager protocol
        :type exc_val: object
        :param exc_tb: traceback passed by the context manager protocol
        :type exc_tb: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.reg.default = self.old

class ObjectRegistry:
    """
    Provides a simple interface to global object registries
    so that pieces of code don't need to pass things like loggers
    or parallelizers through every step of the code
    """

    def __init__(self, default=ObjectRegistryDefaults.Raise):
        """
        **LLM Docstring**

        Create a weak-value registry with configurable behavior for missing keys.

        :param default: the fallback returned when a key is absent
        :type default: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.cache = weakref.WeakValueDictionary() # allow unused vals to get gc'd
        self.default = default

    def temp_default(self, val):
        """
        **LLM Docstring**

        Create a context manager that temporarily replaces the registry fallback value.

        :param val: the value being stored, converted, or installed
        :type val: object
        :return: The resolved or newly constructed helper object.
        :rtype: object
        """
        return RegistryDefaultContext(self, val)

    def __contains__(self, item):
        """
        **LLM Docstring**

        Test whether a live weakly referenced object is registered under a key.

        :param item: the lookup key or index
        :type item: object
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        return self.cache.__contains__(item)

    def lookup(self, key):
        """
        **LLM Docstring**

        Return the registered object, or the configured default when missing-key lookup is non-raising.

        :param key: the storage or lookup key
        :type key: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        if self.default is ObjectRegistryDefaults.Raise:
            return self.cache[key]
        else:
            try:
                return self.cache[key]
            except KeyError:
                return self.default
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Look up a registry key using the configured missing-key policy.

        :param item: the lookup key or index
        :type item: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        return self.lookup(item)

    def register(self, key, val):
        """
        **LLM Docstring**

        Store a weak reference to `val` under `key`.

        :param key: the storage or lookup key
        :type key: object
        :param val: the value being stored, converted, or installed
        :type val: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.cache[key] = val
    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Register a value using dictionary assignment syntax.

        :param key: the storage or lookup key
        :type key: object
        :param value: the value to store
        :type value: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.register(key, value)

    def keys(self):
        """
        **LLM Docstring**

        Return the live registry keys.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        return self.cache.keys()
    def items(self):
        """
        **LLM Docstring**

        Return the live registry key/value pairs.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        return self.cache.items()
    def values(self):
        """
        **LLM Docstring**

        Return the live registered objects.

        :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
        :rtype: collections.abc.KeysView | collections.abc.ItemsView | collections.abc.ValuesView | list
        """
        return self.cache.values()