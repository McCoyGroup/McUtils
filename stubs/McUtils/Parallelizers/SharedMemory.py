"""
Provides classes for working with `multiprocessing.SharedMemory`
in a slightly more convenient way
"""
import abc, os, numpy as np, typing, weakref, mmap
from dataclasses import dataclass
from multiprocessing import Manager
from ..Scaffolding import BaseObjectManager, NDarrayMarshaller
__all__ = ['SharedObjectManager', 'SharedMemoryDict', 'SharedMemoryList']

class SharedMemoryInterface(typing.Protocol):

    @abc.abstractmethod
    def __init__(self, name=None, create=False, size=None):
        """
        **LLM Docstring**

        Define the constructor contract for a shared-memory buffer implementation.

        :param name: Value supplied for `name`.
        :type name: Any
        :param create: Value supplied for `create`.
        :type create: Any
        :param size: Value supplied for `size`.
        :type size: Any
        :return: None
        :rtype: None
        """
        ...
    buf: bytearray

    @abc.abstractmethod
    def close(self):
        """
        **LLM Docstring**

        Define the operation that closes this process's handle to the shared buffer.
        :return: None
        :rtype: None
        """
        ...

    @abc.abstractmethod
    def unlink(self):
        """
        **LLM Docstring**

        Define the operation that removes the shared-memory resource.
        :return: None
        :rtype: None
        """
        ...

class SharedMemoryNDarray:
    """
    Provides a very simple tracker for shared NumPy arrays
    """
    _buf_refs = [weakref.WeakKeyDictionary(), {}]

    def __init__(self, shape, dtype, buf, autoclose=True, parallelizer=None):
        """
        :param shape:
        :type shape: tuple[int]
        :param dtype:
        :type dtype: np.dtype
        :param buf:
        :type buf: SharedMemoryInterface
        :param parallelizer:
        :type parallelizer: Parallelizer
        """
        ...

    def _bufid_ref(self):
        """
        **LLM Docstring**

        Select a stable buffer identifier and the reference-count table used for it.
        :return: A buffer identifier and the reference-count mapping selected for that identifier.
        :rtype: tuple[object, dict]
        """
        ...

    def _ref(self):
        """
        **LLM Docstring**

        Return the tracked local reference count for this shared buffer, creating a zero entry when absent.
        :return: The current tracked reference count.
        :rtype: int
        """
        ...

    def _incref(self):
        """
        **LLM Docstring**

        Increment the tracked local reference count for this shared buffer.
        :return: None.
        :rtype: None
        """
        ...

    def _decref(self):
        """
        **LLM Docstring**

        Decrement the tracked local reference count for this shared buffer.
        :return: None.
        :rtype: None
        """
        ...

    def _rmref(self):
        """
        **LLM Docstring**

        Remove this buffer's entry from the selected reference-count table.
        :return: None.
        :rtype: None
        """
        ...

    def __getstate__(self):
        """
        **LLM Docstring**

        Serialize the array metadata, buffer handle, cleanup policy, and parallelizer without serializing the NumPy view.
        :return: The serializable state mapping.
        :rtype: dict
        """
        ...

    def __setstate__(self, state):
        """
        **LLM Docstring**

        Restore serialized metadata and rebuild the NumPy view over the shared buffer.

        :param state: Value supplied for `state`.
        :type state: Any
        :return: None.
        :rtype: None
        """
        ...

    @classmethod
    def from_array(cls, arr, buf, autoclose=None, parallelizer=None):
        """
        Initializes by pulling metainfo from an array

        :param arr:
        :type arr: np.ndarray
        :param buf:
        :type buf: SharedMemoryInterface
        :return:
        :rtype:
        """
        ...

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Assign values through the NumPy view backed by shared memory.

        :param key: Value supplied for `key`.
        :type key: Any
        :param value: Value supplied for `value`.
        :type value: Any
        :return: None.
        :rtype: None
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Read values through the NumPy view backed by shared memory.

        :param item: Value supplied for `item`.
        :type item: Any
        :return: The selected scalar or array view.
        :rtype: Any
        """
        ...

    def close(self):
        """
        **LLM Docstring**

        Release one local reference and close the underlying buffer when the count reaches zero.
        :return: None.
        :rtype: None
        """
        ...

    def unlink(self):
        """
        **LLM Docstring**

        Unlink the underlying buffer only when no tracked local references remain.
        :return: None.
        :rtype: None
        """
        ...

    def __del__(self):
        """
        **LLM Docstring**

        Automatically close and unlink the buffer on the main process when `autoclose` is enabled.
        :return: None.
        :rtype: None
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a compact representation containing the shared array shape and dtype.
        :return: A compact description of the shared array.
        :rtype: str
        """
        ...

    def unshare(self):
        """
        **LLM Docstring**

        Copy the shared NumPy view into an ordinary process-local array.
        :return: A process-local copy.
        :rtype: np.ndarray
        """
        ...

class SharedArrayAllocator:
    """
    Provides the base API to allocate/deallocate
    NumPy arrays
    """

    def __init__(self, parallelizer=None, mem_manager=None, autoclose=True):
        """
        **LLM Docstring**

        Configure shared-array allocation with an optional memory manager and cleanup policy.

        :param parallelizer: Value supplied for `parallelizer`.
        :type parallelizer: Any
        :param mem_manager: Value supplied for `mem_manager`.
        :type mem_manager: Any
        :param autoclose: Value supplied for `autoclose`.
        :type autoclose: Any
        :return: None.
        :rtype: None
        """
        ...

    @property
    def api(self):
        """
        **LLM Docstring**

        Lazily import and cache `multiprocessing.shared_memory`, raising a descriptive error if unavailable.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __getstate__(self):
        """
        **LLM Docstring**

        Return picklable allocator state with the imported shared-memory module cache cleared.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def create_shared_array(self, data, name=None):
        """
        Makes a SharedNDarray object for an existing data chunk

        :param data:
        :type data: np.ndarray
        :return:
        :rtype: SharedMemoryNDarray
        """
        ...

    def delete_shared_array(self, shared_array):
        """
        Closes a buffer for a numpy array

        :param shared_array:
        :type shared_array: SharedMemoryNDarray
        :return:
        :rtype:
        """
        ...

    def update_shared_array(self, shared_array, data):
        """
        Updates a buffer for a numpy array

        :param shared_array:
        :type shared_array: SharedMemoryNDarray
        :return:
        :rtype:
        """
        ...

class SharedMemoryPrimitive:
    """
    Provides basic support for storing shared memory arrays
    """

    def __init__(self, sync_buffer, allocator=None, marshaller=None, parallelizer=None):
        """
        **LLM Docstring**

        Bind a synchronized metadata container to an array allocator and an ndarray marshaller.

        :param sync_buffer: Value supplied for `sync_buffer`.
        :type sync_buffer: Any
        :param allocator: Value supplied for `allocator`.
        :type allocator: Any
        :param marshaller: Value supplied for `marshaller`.
        :type marshaller: Any
        :param parallelizer: Value supplied for `parallelizer`.
        :type parallelizer: Any
        :return: None.
        :rtype: None
        """
        ...

    def _save_to_buffer(self, tree, name, data):
        """
        Saves `data` to a series of `SharedNDarrays` by
        recursing into structures to save them as buffers
        in a dict-like structure

        :param tree:
        :type tree:
        :param name:
        :type name:
        :param data:
        :type data:
        :return:
        :rtype:
        """
        ...

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Marshal and recursively store a value under the requested key using shared arrays for ndarray leaves.

        :param key: Value supplied for `key`.
        :type key: Any
        :param value: Value supplied for `value`.
        :type value: Any
        :return: None.
        :rtype: None
        """
        ...

    def _handle_delete(self, arr):
        """
        Loads recursively, maintaining
        structure where possible

        :param arr:
        :type arr:
        :return:
        :rtype:
        """
        ...

    def _del_buffer(self, tree, name):
        """
        Reloads shared data from the buffers, trying
        to maintain fidelity where possible

        :param tree:
        :type tree:
        :param name:
        :type name:
        :return:
        :rtype:
        """
        ...

    def __delitem__(self, key):
        """
        **LLM Docstring**

        Recursively release shared-array leaves and remove the requested entry.

        :param key: Value supplied for `key`.
        :type key: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def _handle_load(self, arr):
        """
        Loads recursively, maintaining
        structure where possible

        :param arr:
        :type arr:
        :return:
        :rtype:
        """
        ...

    def _load_from_buffer(self, tree, name):
        """
        Reloads shared data from the buffers, trying
        to maintain fidelity where possible

        :param tree:
        :type tree:
        :param name:
        :type name:
        :return:
        :rtype:
        """
        ...

    def load_item(self, item):
        """
        **LLM Docstring**

        Reconstruct and return a process-local copy of an item from its shared-buffer tree.

        :param item: Value supplied for `item`.
        :type item: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Return the stored shared-memory representation directly without unsharing it.

        :param item: Value supplied for `item`.
        :type item: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation containing the synchronized backing container.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

class SharedMemoryList(SharedMemoryPrimitive):
    """
        Implements a shared dict that uses
        a managed dict to synchronize array metainfo
        across processes
        """

    def __init__(self, *seq, sync_list=None, manager=None, marshaller=None, allocator=None, parallelizer=None):
        """
        :param marshaller:
        :type marshaller:
        :param sync_dict:
        :type sync_dict:
        :param allocator:
        :type allocator:
        :param parallelizer:
        :type parallelizer:
        """
        ...

    def __getstate__(self):
        """
        **LLM Docstring**

        Return picklable list state while dropping the local manager object.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __contains__(self, item):
        """
        **LLM Docstring**

        Test membership against the synchronized backing list.

        :param item: Value supplied for `item`.
        :type item: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over the synchronized backing list's stored representations.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __len__(self):
        """
        **LLM Docstring**

        Return the number of entries in the synchronized backing list.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __del__(self):
        """
        **LLM Docstring**

        Attempt to delete every stored entry and release its shared arrays during finalization.
        :return: None.
        :rtype: None
        """
        ...

    def unshare(self):
        """
        **LLM Docstring**

        Reconstruct every list entry as process-local data.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def pop(self, k=0):
        """
        **LLM Docstring**

        Remove a stored representation and reconstruct it as process-local data.

        :param k: Value supplied for `k`.
        :type k: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def insert(self, k, v):
        """
        **LLM Docstring**

        Insert an empty slot and then marshal the supplied value into that position.

        :param k: Value supplied for `k`.
        :type k: Any
        :param v: Value supplied for `v`.
        :type v: Any
        :return: None.
        :rtype: None
        """
        ...

    def append(self, v):
        """
        **LLM Docstring**

        Append a placeholder and store the supplied value through the synchronized list. The implementation indexes the new slot using the post-append length.

        :param v: Value supplied for `v`.
        :type v: Any
        :return: None.
        :rtype: None
        """
        ...

    def extend(self, v):
        """
        **LLM Docstring**

        Reserve slots for all values and populate them. The current implementation stores the full input sequence in every new slot rather than each element.

        :param v: Value supplied for `v`.
        :type v: Any
        :return: None.
        :rtype: None
        """
        ...

class SharedMemoryDict(SharedMemoryPrimitive):
    """
    Implements a shared dict that uses
    a managed dict to synchronize array metainfo
    across processes
    """

    def __init__(self, *seq, sync_dict=None, manager=None, marshaller=None, allocator=None, parallelizer=None):
        """
        :param marshaller:
        :type marshaller:
        :param sync_dict:
        :type sync_dict:
        :param allocator:
        :type allocator:
        :param parallelizer:
        :type parallelizer:
        """
        ...

    def __getstate__(self):
        """
        **LLM Docstring**

        Return picklable dictionary state while dropping the local manager object.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __contains__(self, item):
        """
        **LLM Docstring**

        Test key membership in the synchronized backing dictionary.

        :param item: Value supplied for `item`.
        :type item: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over keys in the synchronized backing dictionary.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __len__(self):
        """
        **LLM Docstring**

        Return the number of entries in the synchronized backing dictionary.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __del__(self):
        """
        **LLM Docstring**

        On the main process, attempt to delete every stored key and release its shared arrays.
        :return: None.
        :rtype: None
        """
        ...

    def keys(self):
        """
        **LLM Docstring**

        Return the backing dictionary's dynamic key view.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def values(self):
        """
        **LLM Docstring**

        Return the backing dictionary's dynamic value view of shared representations.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def items(self):
        """
        **LLM Docstring**

        Return the backing dictionary's dynamic item view.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def unshare(self):
        """
        **LLM Docstring**

        Reconstruct all entries into a process-local dictionary.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def update(self, v):
        """
        **LLM Docstring**

        Reserve the incoming keys and marshal each incoming value into shared storage.

        :param v: Value supplied for `v`.
        :type v: Any
        :return: None.
        :rtype: None
        """
        ...

class SharedAttribute:

    def __init__(self, name, manager):
        """
        **LLM Docstring**

        Create an attribute marker recording a name and its associated manager.

        :param name: Value supplied for `name`.
        :type name: Any
        :param manager: Value supplied for `manager`.
        :type manager: Any
        :return: None.
        :rtype: None
        """
        ...

@dataclass
class PrimitiveTypeHolder:
    val: object

class SharedObjectManager(BaseObjectManager):
    """
    Provides a high-level interface to create a manager
    that supports shared memory objects through the multiprocessing
    interface
    Only supports data that can be marshalled into a NumPy array.
    """

    def __init__(self, obj, base_dict=None, parallelizer=None):
        """
        :param mem_manager: a memory manager like `multiprocessing.SharedMemoryManager`
        :type mem_manager:
        :param obj: the object whose attributes should be given by shared memory objects
        :type obj:
        :param base_dict: the dict that stores the shared arrays (can also be shared)
        :type base_dict: SharedMemoryDict
        """
        ...
    primitive_types = (set, list, tuple, dict, np.ndarray)

    @classmethod
    def is_primitive(cls, val):
        """
        **LLM Docstring**

        Return whether a value belongs to the container and ndarray types wrapped in `PrimitiveTypeHolder`.

        :param val: Value supplied for `val`.
        :type val: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def save_attr(self, attr):
        """
        **LLM Docstring**

        Move an object attribute into the shared dictionary and replace it with a `SharedAttribute` marker.

        :param attr: Value supplied for `attr`.
        :type attr: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def del_attr(self, attr):
        """
        **LLM Docstring**

        Delete a shared attribute's backing entry when marked, then remove the object attribute.

        :param attr: Value supplied for `attr`.
        :type attr: Any
        :return: None.
        :rtype: None
        """
        ...

    def load_attr(self, attr):
        """
        **LLM Docstring**

        Resolve a marked shared attribute and replace the marker on the object with the stored representation.

        :param attr: Value supplied for `attr`.
        :type attr: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def get_saved_keys(self, obj):
        """
        **LLM Docstring**

        Return the keys currently present in the managed object's `__dict__`.

        :param obj: Value supplied for `obj`.
        :type obj: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def save_keys(self, keys=None):
        """
        **LLM Docstring**

        Share each requested object attribute, defaulting to all keys in the object dictionary.

        :param keys: Value supplied for `keys`.
        :type keys: Any
        :return: None.
        :rtype: None
        """
        ...

    def share(self, keys=None):
        """
        **LLM Docstring**

        Delegate to an object-specific `share` method when present, otherwise share selected attributes.

        :param keys: Value supplied for `keys`.
        :type keys: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def load_keys(self, keys=None):
        """
        **LLM Docstring**

        Load each requested shared attribute, defaulting to all object dictionary keys.

        :param keys: Value supplied for `keys`.
        :type keys: Any
        :return: None.
        :rtype: None
        """
        ...

    def unshare(self, keys=None):
        """
        **LLM Docstring**

        Delegate to an object-specific `unshare` method or restore attributes and unwrap primitive holders.

        :param keys: Value supplied for `keys`.
        :type keys: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def _cleanup(self):
        """
        **LLM Docstring**

        Delete every key currently recorded in the shared backing dictionary, ignoring lookup failures.
        :return: None.
        :rtype: None
        """
        ...

    def __del__(self):
        """
        **LLM Docstring**

        Run best-effort cleanup when the manager is finalized.
        :return: None.
        :rtype: None
        """
        ...

    def list(self, *l):
        """
        **LLM Docstring**

        Create a `SharedMemoryList` reusing this manager's synchronization manager, marshaller, allocator, and parallelizer.

        :param l: Value supplied for `l`.
        :type l: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def dict(self, *d):
        """
        **LLM Docstring**

        Create a `SharedMemoryDict` reusing this manager's synchronization manager, marshaller, allocator, and parallelizer.

        :param d: Value supplied for `d`.
        :type d: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def array(self, a):
        """
        **LLM Docstring**

        Return an existing shared array unchanged or allocate a new shared-memory copy.

        :param a: Value supplied for `a`.
        :type a: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...