"""
Provides classes for working with `multiprocessing.SharedMemory`
in a slightly more convenient way
"""

import abc, os, numpy as np, typing, weakref, mmap
from dataclasses import dataclass

from multiprocessing import Manager

from ..Scaffolding import BaseObjectManager, NDarrayMarshaller

__all__ = [
    "SharedObjectManager",
    "SharedMemoryDict",
    "SharedMemoryList",
    "SharedMemoryNDarray"
]

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
        raise NotImplementedError("interface class")

    buf: bytearray
    @abc.abstractmethod
    def close(self):
        """
        **LLM Docstring**

        Define the operation that closes this process's handle to the shared buffer.
        :return: None
        :rtype: None
        """
        raise NotImplementedError("interface class")

    @abc.abstractmethod
    def unlink(self):
        """
        **LLM Docstring**

        Define the operation that removes the shared-memory resource.
        :return: None
        :rtype: None
        """
        raise NotImplementedError("interface class")

class SharedMemoryNDarray:
    """
    Provides a very simple tracker for shared NumPy arrays
    """

    # track reference counts to the existing buffer to hopefully keep it from
    # being deleted...
    _buf_refs = [
        weakref.WeakKeyDictionary(),
        {}
    ]
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
        self.dtype = dtype
        self.shape = shape
        self.buf = buf
        self.autoclose = autoclose
        self.array = np.ndarray(self.shape, dtype=self.dtype, buffer=self.buf.buf)
        self._incref()
        self.parallelizer = parallelizer
        # self.parallelizer.print("initializing {} ({})".format(
        #     self._bufid_ref()[0],
        #     os.getpid()
        # ))

    def _bufid_ref(self):
        """
        **LLM Docstring**

        Select a stable buffer identifier and the reference-count table used for it.
        :return: A buffer identifier and the reference-count mapping selected for that identifier.
        :rtype: tuple[object, dict]
        """
        try:
            obj = self.buf.name
        except AttributeError:
            obj = self.buf.buf
        if isinstance(obj, memoryview):
            obj = obj.obj
        # if isinstance(obj, mmap.mmap):
        #     raise Exception(obj.fileno)
            # obj = obj.
        if isinstance(obj, (int, str)):
            br = self._buf_refs[1]
        else:
            br = self._buf_refs[0]
        return obj, br

    def _ref(self):
        """
        **LLM Docstring**

        Return the tracked local reference count for this shared buffer, creating a zero entry when absent.
        :return: The current tracked reference count.
        :rtype: int
        """
        bid, br = self._bufid_ref()
        if bid not in br:
            br[bid] = 0
        return br[bid]
    def _incref(self):
        """
        **LLM Docstring**

        Increment the tracked local reference count for this shared buffer.
        :return: None.
        :rtype: None
        """
        bid, br = self._bufid_ref()
        if bid not in br:
            br[bid] = 0
        br[bid] += 1
    def _decref(self):
        """
        **LLM Docstring**

        Decrement the tracked local reference count for this shared buffer.
        :return: None.
        :rtype: None
        """
        bid, br = self._bufid_ref()
        if bid not in br:
            br[bid] = 0
        br[bid] -= 1
    def _rmref(self):
        """
        **LLM Docstring**

        Remove this buffer's entry from the selected reference-count table.
        :return: None.
        :rtype: None
        """
        bid, br = self._bufid_ref()
        del br[bid]

    # def to_state(self, serializer=None):
    #     return self.__getstate__()
    # @classmethod
    # def from_state(cls, state, serializer=None):
    #     return cls(state['shape'], state['dtype'], state['buf'],
    #                autoclose=state['autoclose'],
    #                parallelizer=serializer.deserialize(state['parallelizer'])
    #                )

    def __getstate__(self):
        """
        **LLM Docstring**

        Serialize the array metadata, buffer handle, cleanup policy, and parallelizer without serializing the NumPy view.
        :return: The serializable state mapping.
        :rtype: dict
        """
        return {
            'dtype': self.dtype,
            'shape': self.shape,
            'buf': self.buf,
            'autoclose': self.autoclose,
            'parallelizer': self.parallelizer
        }

    def __setstate__(self, state):
        """
        **LLM Docstring**

        Restore serialized metadata and rebuild the NumPy view over the shared buffer.

        :param state: Value supplied for `state`.
        :type state: Any
        :return: None.
        :rtype: None
        """
        self.dtype = state['dtype']
        self.shape = state['shape']
        self.buf = state['buf']
        self.autoclose = state['autoclose']
        self.parallelizer = state['parallelizer']
        self.array = np.ndarray(self.shape, dtype=self.dtype, buffer=self.buf.buf)
        self._incref()
        # self.parallelizer.print("cloned {} ({})".format(
        #     self._bufid_ref()[0],
        #     os.getpid()
        # ))

    @classmethod
    def from_array(cls, arr, buf,
                   autoclose=None,
                   parallelizer=None
                   ):
        """
        Initializes by pulling metainfo from an array

        :param arr:
        :type arr: np.ndarray
        :param buf:
        :type buf: SharedMemoryInterface
        :return:
        :rtype:
        """
        opts = {}
        if autoclose is not None:
            opts['autoclose'] = autoclose
        if parallelizer is not None:
            opts['parallelizer'] = parallelizer
        new = cls(arr.shape, arr.dtype, buf, **opts)
        new[:] = arr
        return new

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
        self.array[key] = value

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Read values through the NumPy view backed by shared memory.

        :param item: Value supplied for `item`.
        :type item: Any
        :return: The selected scalar or array view.
        :rtype: Any
        """
        return self.array[item]

    def close(self):
        """
        **LLM Docstring**

        Release one local reference and close the underlying buffer when the count reaches zero.
        :return: None.
        :rtype: None
        """
        self._decref()
        if self._ref() <= 0:
            # self.parallelizer.print("???? {}".format(self._bufid_ref()[0]))
            self._rmref()
            self.buf.close()

    def unlink(self):
        """
        **LLM Docstring**

        Unlink the underlying buffer only when no tracked local references remain.
        :return: None.
        :rtype: None
        """
        if self._ref() <= 0:
            self.buf.unlink()

    def __del__(self):
        """
        **LLM Docstring**

        Automatically close and unlink the buffer on the main process when `autoclose` is enabled.
        :return: None.
        :rtype: None
        """
        try:
            ac = self.autoclose
        except AttributeError:
            pass
        else:
            if ac:
                if self.parallelizer is not None and self.parallelizer.on_main:
                    # self.parallelizer.print("closing {} ({})".format(
                    #     self._bufid_ref()[0],
                    #     os.getpid()
                    # ))
                    self.close()
                    self.unlink()

    def __repr__(self):
        """
        **LLM Docstring**

        Return a compact representation containing the shared array shape and dtype.
        :return: A compact description of the shared array.
        :rtype: str
        """
        return "{}({}, dtype={})".format(
            type(self).__name__,
            self.shape,
            self.dtype
        )

    def unshare(self):
        """
        **LLM Docstring**

        Copy the shared NumPy view into an ordinary process-local array.
        :return: A process-local copy.
        :rtype: np.ndarray
        """
        return self.array.copy()

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
        # if mem_manager is None:
        #     try:
        #         from multiprocessing import shared_memory
        #         self._api = shared_memory
        #     except ImportError:
        #         self._api = None
        #         raise NotImplementedError(
        #             "{}: either `multiprocessing` needs the `shared_memory` submodule or `mem_manager` must be provided".format(
        #                 type(self).__name__
        #             )
        #         )
        self.parallelizer = parallelizer
        self.mem_manager = mem_manager
        self.autoclose = autoclose
        self._api = None
        # self._refbuf = []

    @property
    def api(self):
        """
        **LLM Docstring**

        Lazily import and cache `multiprocessing.shared_memory`, raising a descriptive error if unavailable.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        if self._api is None:
            try:
                from multiprocessing import shared_memory
                self._api = shared_memory
            except ImportError:
                self._api = None
                raise NotImplementedError(
                    "{}: either `multiprocessing` needs the `shared_memory` submodule or `mem_manager` must be provided".format(
                        type(self).__name__
                    )
                )
        return self._api

    def __getstate__(self):
        """
        **LLM Docstring**

        Return picklable allocator state with the imported shared-memory module cache cleared.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        base = self.__dict__.copy()
        base['_api'] = None
        return base

    # def __setstate__(self, state):
    #     self.__dict__.update(state)
    #     if self.mem_manager is None:
    #         try:
    #             from multiprocessing import shared_memory
    #             self.api = shared_memory
    #         except ImportError:
    #             self.api = None
    #             raise NotImplementedError(
    #                 "{}: either `multiprocessing` needs the `shared_memory` submodule or `mem_manager` must be provided".format(
    #                     type(self).__name__
    #                 )
    #             )


    def create_shared_array(self, data, name=None):
        """
        Makes a SharedNDarray object for an existing data chunk

        :param data:
        :type data: np.ndarray
        :return:
        :rtype: SharedMemoryNDarray
        """

        if self.mem_manager is not None:
            shm = self.mem_manager.SharedMemory
        else:
            shm = self.api.SharedMemory
        buf = shm(name, create=True, size=data.nbytes)
        arr = SharedMemoryNDarray.from_array(data, buf, parallelizer=self.parallelizer, autoclose=self.autoclose)
        # self._refbuf.append(arr) # kludge to keep stuff from going out of scope
        return arr

    def delete_shared_array(self, shared_array):
        """
        Closes a buffer for a numpy array

        :param shared_array:
        :type shared_array: SharedMemoryNDarray
        :return:
        :rtype:
        """
        shared_array.close()
        # try:
        #     self._refbuf.remove(shared_array)
        # except IndexError:
        #     pass

    def update_shared_array(self, shared_array, data):
        """
        Updates a buffer for a numpy array

        :param shared_array:
        :type shared_array: SharedMemoryNDarray
        :return:
        :rtype:
        """
        try:
            shared_array.array[:] = data
        except ValueError:
            self.delete_shared_array(shared_array)
            shared_array = self.create_shared_array(data)
        return shared_array

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

        self.buffers = sync_buffer

        self.allocator = SharedArrayAllocator(parallelizer=parallelizer, autoclose=False) if allocator is None else allocator

        if marshaller is None:
            marshaller = NDarrayMarshaller()
        self.marshaller = marshaller
        # self.buffers = {} if buffers is None else buffers
        self.parallelizer = parallelizer

    def _set_tree_array_entry(self, tree, name, arr, cur):
        if arr.ndim == 0:
            tree[name] = arr.tolist()
        else:
            if isinstance(cur, SharedMemoryNDarray):
                tree[name] = self.allocator.update_shared_array(tree[name], arr)
            else:
                tree[name] = self.allocator.create_shared_array(arr)

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
        arr = self.marshaller.convert(data)
        del data # just to help minimize bugs
        if isinstance(arr, np.ndarray):
            if hasattr(tree, 'keys'):
                # add the array as an attr
                self._set_tree_array_entry(tree, name, arr, tree[name])
            elif isinstance(name, (int, np.integer)):
                # add the array as a list element
                if len(tree) < name:
                    self._set_tree_array_entry(tree, name, arr, tree[name])
                else:
                    # expand the tree to just the necessary space
                    padding = len(tree) - name - 1
                    tree = tree + [None] * padding
                    self._set_tree_array_entry(tree, name, arr, None)
            else:
                raise ValueError("cannot save {} into {}".format(arr, tree))
        else:
            # walk an expression tree, updating buffers as needed
            if hasattr(arr, 'items'):
                subtree = {} if name not in tree or not hasattr(tree[name], 'items') else tree[name]
                for k,v in arr.items():
                    self._save_to_buffer(subtree, k, v)
            else:
                try:
                    iter(tree[name])
                except (AttributeError, TypeError):
                    subtree = []
                else:
                    subtree = tree[name]
                for i,v in enumerate(arr):
                    self._save_to_buffer(subtree, i, v)

            tree[name] = subtree

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
        self._save_to_buffer(self.buffers, key, value)

    def _handle_delete(self, arr):
        """
        Loads recursively, maintaining
        structure where possible

        :param arr:
        :type arr:
        :return:
        :rtype:
        """
        if arr is None:
            pass
        elif isinstance(arr, SharedMemoryNDarray):
            self.allocator.delete_shared_array(arr)
        elif isinstance(arr, dict):
            for v in arr.values():
                self._handle_delete(v)
        else:  # build a list of loaded values
            for v in arr:
                self._handle_delete(v)

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
        self._handle_delete(tree[name])
        del tree[name]

    def __delitem__(self, key):
        """
        **LLM Docstring**

        Recursively release shared-array leaves and remove the requested entry.

        :param key: Value supplied for `key`.
        :type key: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return self._del_buffer(self.buffers, key)

    def _handle_load(self, arr):
        """
        Loads recursively, maintaining
        structure where possible

        :param arr:
        :type arr:
        :return:
        :rtype:
        """
        if arr is None:
            data = None
        elif isinstance(arr, SharedMemoryNDarray):
            data = arr.array.copy()
            self.allocator.delete_shared_array(arr)
        elif isinstance(arr, np.ndarray): # protection but not sure how we'd get here...
            data = arr
        elif isinstance(arr, dict):
            data = {
                k:self._handle_load(v) for k,v in arr.items()
            }
        else: # build a list of loaded values
            data = [self._handle_load(v) for v in arr]

        return data

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
        data = self._handle_load(tree[name])
        # self._del_buffer(tree, name)
        return data

    def load_item(self, item):
        """
        **LLM Docstring**

        Reconstruct and return a process-local copy of an item from its shared-buffer tree.

        :param item: Value supplied for `item`.
        :type item: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return self._load_from_buffer(self.buffers, item)

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Return the stored shared-memory representation directly without unsharing it.

        :param item: Value supplied for `item`.
        :type item: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return self.buffers[item]
        #
        # self.buffers[key] = self.marshaller.convert(value)

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation containing the synchronized backing container.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return "{}({})".format(type(self).__name__, self.buffers)

    @abc.abstractmethod
    def close(self):
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

        if sync_list is None:
            if manager is None:
                manager = Manager()
            sync_list = manager.list()
        self.manager = manager

        super().__init__(sync_list, marshaller=marshaller, allocator=allocator, parallelizer=parallelizer)

        if len(seq) == 1:
            self.extend(seq[0])
        elif len(seq) > 0:
            raise ValueError("only one positional argument allowed") # standardize this

    def __getstate__(self):
        """
        **LLM Docstring**

        Return picklable list state while dropping the local manager object.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        d = self.__dict__.copy()
        d['manager'] = None
        return d

    def __contains__(self, item):
        """
        **LLM Docstring**

        Test membership against the synchronized backing list.

        :param item: Value supplied for `item`.
        :type item: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return self.buffers.__contains__(item)
    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over the synchronized backing list's stored representations.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return iter(self.buffers)
    def __len__(self):
        """
        **LLM Docstring**

        Return the number of entries in the synchronized backing list.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return len(self.buffers)
    def __del__(self):
        """
        **LLM Docstring**

        Attempt to delete every stored entry and release its shared arrays during finalization.
        :return: None.
        :rtype: None
        """
        for i in range(len(self)):
            del self[i]

    def unshare(self):
        """
        **LLM Docstring**

        Reconstruct every list entry as process-local data.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return [self._load_from_buffer(self.buffers, i) for i in range(len(self))]

    def pop(self, k=0):
        """
        **LLM Docstring**

        Remove a stored representation and reconstruct it as process-local data.

        :param k: Value supplied for `k`.
        :type k: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        val = self.buffers.pop(k)
        return self._handle_load(val)
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
        self.buffers.insert(k, None)
        self[k] = v
    def append(self, v):
        """
        **LLM Docstring**

        Append a placeholder and store the supplied value through the synchronized list. The implementation indexes the new slot using the post-append length.

        :param v: Value supplied for `v`.
        :type v: Any
        :return: None.
        :rtype: None
        """
        self.buffers.append(None)
        self.buffers[len(self.buffers)] = v
    def extend(self, v):
        """
        **LLM Docstring**

        Reserve slots for all values and populate them. The current implementation stores the full input sequence in every new slot rather than each element.

        :param v: Value supplied for `v`.
        :type v: Any
        :return: None.
        :rtype: None
        """
        base_len = len(self.buffers)
        self.buffers.extend([None]*len(v))
        for i,a in enumerate(v):
            self.buffers[base_len+i] = v

    def close(self):
        for b in self.buffers:
            b.close()

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

        if sync_dict is None:
            if manager is None:
                manager = Manager()
            sync_dict = manager.dict()
        self.manager = manager

        super().__init__(sync_dict, marshaller=marshaller, allocator=allocator, parallelizer=parallelizer)

        if len(seq) == 1:
            self.update(seq[0])
        elif len(seq) > 0:
            raise ValueError("only one positional argument allowed") # standardize this

    def __getstate__(self):
        """
        **LLM Docstring**

        Return picklable dictionary state while dropping the local manager object.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        d = self.__dict__.copy()
        d['manager'] = None
        return d

    def __contains__(self, item):
        """
        **LLM Docstring**

        Test key membership in the synchronized backing dictionary.

        :param item: Value supplied for `item`.
        :type item: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return self.buffers.__contains__(item)
    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over keys in the synchronized backing dictionary.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return iter(self.buffers)
    def __len__(self):
        """
        **LLM Docstring**

        Return the number of entries in the synchronized backing dictionary.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return len(self.buffers)
    def __del__(self):
        """
        **LLM Docstring**

        On the main process, attempt to delete every stored key and release its shared arrays.
        :return: None.
        :rtype: None
        """
        if self.parallelizer is not None and self.parallelizer.on_main:
            try:
                for k in self.keys():
                    del self[k]
            except FileNotFoundError:
                pass

    def keys(self):
        """
        **LLM Docstring**

        Return the backing dictionary's dynamic key view.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return self.buffers.keys()
    def values(self):
        """
        **LLM Docstring**

        Return the backing dictionary's dynamic value view of shared representations.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return self.buffers.values()
    def items(self):
        """
        **LLM Docstring**

        Return the backing dictionary's dynamic item view.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return self.buffers.items()
    def unshare(self):
        """
        **LLM Docstring**

        Reconstruct all entries into a process-local dictionary.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return {k:self._load_from_buffer(self.buffers, k) for k in self.keys()}

    def update(self, v):
        """
        **LLM Docstring**

        Reserve the incoming keys and marshal each incoming value into shared storage.

        :param v: Value supplied for `v`.
        :type v: Any
        :return: None.
        :rtype: None
        """
        v = dict(v)
        self.buffers.update({k:None for k in v.keys()})
        for k,a in v.items():
            self[k] = a

    def close(self):
        for b in self.values():
            if hasattr(b, 'close'):
                b.close()

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
        self.name = name
        self.manager = manager

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

        if self.is_primitive(obj):
            obj = PrimitiveTypeHolder(obj)
        super().__init__(obj)

        self.base_dict = SharedMemoryDict(parallelizer=parallelizer) if base_dict is None else base_dict
        self.parallelizer = parallelizer

    primitive_types = (
        set,
        list,
        tuple,
        dict,
        np.ndarray
    )
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
        return isinstance(val, cls.primitive_types)

    def save_attr(self, attr):
        """
        **LLM Docstring**

        Move an object attribute into the shared dictionary and replace it with a `SharedAttribute` marker.

        :param attr: Value supplied for `attr`.
        :type attr: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        val = getattr(self.obj, attr)
        if not isinstance(val, SharedAttribute):
            self.base_dict[attr] = val
            setattr(self.obj, attr, SharedAttribute(self, attr))
            val = getattr(self.obj, attr)
        return val

    def del_attr(self, attr):
        """
        **LLM Docstring**

        Delete a shared attribute's backing entry when marked, then remove the object attribute.

        :param attr: Value supplied for `attr`.
        :type attr: Any
        :return: None.
        :rtype: None
        """
        val = getattr(self.obj, attr)
        if isinstance(val, SharedAttribute):
            del self.base_dict[attr]
        delattr(self.obj, attr)

    def load_attr(self, attr):
        """
        **LLM Docstring**

        Resolve a marked shared attribute and replace the marker on the object with the stored representation.

        :param attr: Value supplied for `attr`.
        :type attr: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        val = getattr(self.obj, attr)
        if isinstance(val, SharedAttribute):
            val = self.base_dict[attr]
            setattr(self.obj, attr, val)
        return val

    def get_saved_keys(self, obj):
        """
        **LLM Docstring**

        Return the keys currently present in the managed object's `__dict__`.

        :param obj: Value supplied for `obj`.
        :type obj: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return obj.__dict__.keys()

    def save_keys(self, keys=None):
        """
        **LLM Docstring**

        Share each requested object attribute, defaulting to all keys in the object dictionary.

        :param keys: Value supplied for `keys`.
        :type keys: Any
        :return: None.
        :rtype: None
        """
        if keys is None:
            keys = self.get_saved_keys(self.obj)
        for k in keys:
            self.save_attr(k)

    def share(self, keys=None):
        """
        **LLM Docstring**

        Delegate to an object-specific `share` method when present, otherwise share selected attributes.

        :param keys: Value supplied for `keys`.
        :type keys: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        try:
            res = self.obj.share(self)
        except AttributeError:
            res = None
            self.save_keys(keys=keys)

        if res is None:
            return self.obj
        else:
            return res

    def load_keys(self, keys=None):
        """
        **LLM Docstring**

        Load each requested shared attribute, defaulting to all object dictionary keys.

        :param keys: Value supplied for `keys`.
        :type keys: Any
        :return: None.
        :rtype: None
        """
        if keys is None:
            keys = self.get_saved_keys(self.obj)
        for k in keys:
            self.load_attr(k)

    def unshare(self, keys=None):
        """
        **LLM Docstring**

        Delegate to an object-specific `unshare` method or restore attributes and unwrap primitive holders.

        :param keys: Value supplied for `keys`.
        :type keys: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        try:
            res = self.obj.unshare(self)
        except AttributeError:
            res = None
            self.load_keys(keys=keys)

        if res is None:
            if isinstance(self.obj, PrimitiveTypeHolder):
                return self.obj.val
            else:
                return self.obj
        else:
            return res

    def _cleanup(self):
        """
        **LLM Docstring**

        Delete every key currently recorded in the shared backing dictionary, ignoring lookup failures.
        :return: None.
        :rtype: None
        """
        try:
            saved_keys = self.base_dict.keys()
        except:
            pass
        else:
            for k in saved_keys:
                self.del_attr(k)

    def __del__(self):
        """
        **LLM Docstring**

        Run best-effort cleanup when the manager is finalized.
        :return: None.
        :rtype: None
        """
        self._cleanup()
    # def delete(self):
    #     for k in self.get_saved_keys(self.obj):
    #         self.del_attr(k)


    def list(self, *l):
        """
        **LLM Docstring**

        Create a `SharedMemoryList` reusing this manager's synchronization manager, marshaller, allocator, and parallelizer.

        :param l: Value supplied for `l`.
        :type l: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return SharedMemoryList(*l,
                                manager=self.base_dict.manager,
                                marshaller=self.base_dict.marshaller,
                                allocator=self.base_dict.allocator,
                                parallelizer=self.parallelizer
                                )
    def dict(self, *d):
        """
        **LLM Docstring**

        Create a `SharedMemoryDict` reusing this manager's synchronization manager, marshaller, allocator, and parallelizer.

        :param d: Value supplied for `d`.
        :type d: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        return SharedMemoryDict(*d,
                                manager=self.base_dict.manager,
                                marshaller=self.base_dict.marshaller,
                                allocator=self.base_dict.allocator,
                                parallelizer=self.parallelizer
                                )
    def array(self, a):
        """
        **LLM Docstring**

        Return an existing shared array unchanged or allocate a new shared-memory copy.

        :param a: Value supplied for `a`.
        :type a: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        if not isinstance(a, SharedMemoryNDarray):
           return self.base_dict.allocator.create_shared_array(a)
        else:
           return a