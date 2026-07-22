### `Parallelizers.py` — Provides a simple framework for unifying different parallelism approaches.
  - **class `CallerContract`**
    > Provides a structure so that a main process and child process can
    > be synchronized in their MPI-like calls
    - `__init__(calls)`
    - `handle_call(caller, next_call)` — Validate the next operation against the contract and advance the expected-call index cyclically.
  - **class `ChildProcessRuntimeError`** (RuntimeError)
  - **class `Parallelizer`**
    > Abstract base class to help manage parallelism.
    > Provides the basic API that all parallelizers can be expected
    > to conform to.
    > Provides effectively the union of operations supported by
    > `mp.Pool` and `MPI`.
    > There is also the ability to lookup and register 'named'
    > parallelizers, since we expect a single program to not
    > really use more than one.
    > This falls back gracefully to the serial case.
    - `__init__(logger=None, contract=None, uid=None, initialization_function=None, initialization_args=None, initialization_kwargs=None)`
    - `load_registry()` — Lazily create the shared parallelizer registry with a serial fallback as its default.
    - `parallelizer_registry()` — Return the lazily initialized class-level parallelizer registry.
    - `get_default()` — For compat.
    - **class `Backends`** (enum.Enum)
    - `get_paralellizer_types()` — Return the built-in backend enum-to-class mapping.
    - `lookup(key, construct=True)` — Checks in the registry to see if a given parallelizer is there
    - `register(key)` — Checks in the registry to see if a given parallelizer is there
    - `active()` — Return whether at least one nested parallelizer context is active.
    - `set_initializer(func, *args, **kwargs)` — Store a partially bound initializer and immediately run it through the parallelizer.
    - `initialize()` — Initializes a parallelizer
    - `finalize(exc_type, exc_val, exc_tb)` — Finalizes a parallelizer (if necessary)
    - **class `InMainProcess`**
      > Singleton representing being on the
      > main process
    - **class `InWorkerProcess`**
      > Singleton representing being on a
      > worker process
    - `on_main()` — Returns whether or not the executing process is the main
    - `main_restricted(func)` — A decorator to indicate that a function should only be
    - `worker_restricted(func)` — A decorator to indicate that a function should only be
    - `send(data, loc, **kwargs)` — Sends data to the process specified by loc
    - `receive(data, loc, **kwargs)` — Receives data from the process specified by loc
    - `broadcast(data, **kwargs)` — Sends the same data to all processes
    - `scatter(data, locs=None, return_locs=False, **kwargs)` — Performs a scatter of data to the different
    - `gather(data, **kwargs)` — Performs a gather of data from the different
    - `map(function, data, extra_args=None, extra_kwargs=None, **kwargs)` — Performs a parallel map of function over
    - `starmap(function, data, extra_args=None, extra_kwargs=None, **kwargs)` — Performs a parallel map with unpacking of function over
    - `apply(func, *args, main_kwargs=None, cleanup=True, **kwargs)` — Runs the callable `func` in parallel
    - `run(func, *args, comm=None, main_kwargs=None, **kwargs)` — Calls `apply`, but makes sure state is handled cleanly
    - `from_config(mode=None, **kwargs)` — Construct the backend registered for a mode by delegating the remaining options to its `from_config…
    - `nprocs()` — Returns the number of processes the parallelizer has
    - `get_nprocs()` — Returns the number of processes
    - `id()` — Returns some form of identifier for the current process
    - `pid()` — Lazily cache and return the current operating-system process ID.
    - `get_id()` — Returns the id for the current process
    - `printer()` — Return the default printer when no logger is set, otherwise return `logger.log_print`.
    - `printer(p)` — Return the default printer when no logger is set, otherwise return `logger.log_print`.
    - `main_print(*args, **kwargs)` — Prints from the main process
    - `worker_print(*args, **kwargs)` — Prints from a main worker process
    - `print(*args, where='both', **kwargs)` — An implementation of print that operates differently on workers than on main
    - `wait()` — Causes all processes to wait until they've met up at this point.
    - `share(obj)` — Converts `obj` into a form that can be cleanly used with shared memory via a `SharedObjectManager`
  - **class `SendRecieveParallelizer`** (Parallelizer)
    > Parallelizer that implements `scatter`, `gather`, `broadcast`, and `map`
    > based on just having a communicator that supports `send` and `receive methods
    - **class `ReceivedError`**
      - `__init__(error)`
    - **class `SendReceieveCommunicator`**
      > A base class that provides an interface for
      > sending/receiving data from a specific subprocesses
      - `locations()` — Returns the list of locations known by the
      - `location()` — Returns the _current_ location
      - `send(data, loc, **kwargs)` — Sends the specified data to loc
      - `receive(data, loc, **kwargs)` — Receives the specified data from loc
    - `comm()` — Returns the communicator used by the paralellizer
    - `send(data, loc, **kwargs)` — Sends data to the process specified by loc
    - `receive(data, loc, **kwargs)` — Receives data from the process specified by loc
    - `broadcast(data, locs=None, **kwargs)` — Sends the same data to all processes
    - `scatter(data, locs=None, return_locs=False, **kwargs)` — Performs a scatter of data to the different
    - `gather(data, locs=None, **kwargs)` — Performs a gather of data from the different
    - `map(func, data, extra_args=None, extra_kwargs=None, vectorized=False, aggregate=True, **kwargs)` — Performs a parallel map of function over
    - `starmap(func, data, extra_args=None, extra_kwargs=None, **kwargs)` — Performs a parallel map with unpacking of function over
    - `wait()` — Causes all processes to wait until they've met up at this point.
  - **class `MultiprocessingParallelizer`** (SendRecieveParallelizer)
    > Parallelizes using a  process pool and a runner
    > function that represents a "main loop".
    - **class `SendRecvQueuePair`**
      - `__init__(id, manager)`
    - **class `PoolCommunicator`** (SendRecieveParallelizer.SendReceieveCommunicator)
      > Defines a serializable process communicator
      > that allows communication with a managed `mp.Pool`
      > to support `send` and `receive` and therefore to
      > support the rest of the necessary bits of the MPI API
      - `__init__(parent, id, queues, initialization_timeout=None, group=None)`
      - **class `PoolError`** (Exception)
        > For errors arising from Pool operations
      - `initialize()` — (basically just waits until all threads say all is well)
      - `reset()` — (basically just waits until all threads say all is well)
      - `locations()` — Returns the list of queue ids
      - `location()` — Returns the _current_ location
      - `send(data, loc, prepickled=False, **kwargs)` — Sends the specified data to loc
      - `receive(data, loc, prepickled=False, **kwargs)` — Receives the specified data from loc
      - `get_subcomm(idx)` — Create a communicator restricted to selected queue and group indices while preserving the current c…
    - `__init__(worker=False, pool=None, context=None, manager=None, logger=None, contract=None, comm=None, rank=None, allow_restart=True, initialization_timeout=0.5, initialization_function=None, initialization_args=None, initialization_kwargs=None, **kwargs)`
    - `get_nprocs()` — Return the cached multiprocessing process count.
    - `get_id()` — Return the explicit rank when set, otherwise obtain the id from the current communicator.
    - `comm()` — Returns the communicator used by the paralellizer
    - `comm(c)` — Return the current communicator, lazily constructing the full communicator group when necessary.
    - `apply(func, *args, comm=None, main_kwargs=None, cleanup=True, **kwargs)` — Applies func to args in parallel on all of the processes
    - `get_pool_context(pool)` — Return the private multiprocessing context stored by a pool.
    - `get_pool_nprocs(pool)` — Return the private process-count field stored by a pool.
    - `set_initializer(func, *args, **kwargs)` — Install and run an initializer locally, map worker initialization across the pool, and update the p…
    - `initialize(allow_restart=None)` — Create or re-enter the pool, create manager-backed communication queues, initialize workers, and es…
    - `finalize(exc_type, exc_val, exc_tb)` — Exit the owned pool on the main process and clear communication queues and the cached communicator.
    - `on_main()` — Return `True` when this instance is not marked as a worker.
    - `from_config(**kw)` — Construct a multiprocessing parallelizer directly from keyword options.
  - **class `MPIParallelizer`** (SendRecieveParallelizer)
    > Parallelizes using `mpi4py`
    - **class `MPICommunicator`** (SendRecieveParallelizer.SendReceieveCommunicator)
      > A base class that provides an interface for
      > sending/receiving data from a specific subprocesses
      - `__init__(parent, mpi_comm, api)`
      - `type_map()` — sufficient to just have a few core numeric types?
      - `get_mpi_type(dtype)` — Gets the MPI datatype for the numpy
      - `nprocs()` — Returns the number of available processes
      - `locations()` — Returns the list of locations known by the
      - `location()` — Returns the _current_ location
      - `send(data, loc, **kwargs)` — Sends the specified data to loc
      - `receive(data, loc, root=0, **kwargs)` — Receives the specified data from loc
      - `broadcast(data, root=0, **kwargs)` — Sends the same data to all processes
      - `scatter_obj(data, root=0, **kwargs)` — Scatters data to the different MPI ranks using a series
      - `scatter(data, root=0, shape=None, dtype=None, **kwargs)` — Performs a scatter of data to the different
      - `gather_obj(data, root=0, **kwargs)` — Gather arbitrary Python objects to the root using the communicator's request/response receive proto…
      - `gather(data, root=0, shape=None, dtype=None, **kwargs)` — Performs a gather from the different
    - `__init__(root=0, comm=None, contract=None, logger=None)`
    - `get_nprocs()` — :return: The value produced by the implementation; see the summary for its exact semantics.
    - `get_id()` — :return: The value produced by the implementation; see the summary for its exact semantics.
    - `initialize()` — Perform no initialization because mpi4py owns MPI startup.
    - `finalize(exc_type, exc_val, exc_tb)` — Perform no finalization because mpi4py owns MPI shutdown.
    - `comm()` — Returns the communicator used by the paralellizer
    - `on_main()` — Return whether the current communicator rank is zero.
    - `broadcast(data, **kwargs)` — Sends the same data to all processes
    - `scatter(data, shape=None, **kwargs)` — Performs a scatter of data to the different
    - `gather(data, shape=None, **kwargs)` — Performs a gather of data from the different
    - `map(func, data, input_shape=None, output_shape=None, **kwargs)` — Performs a parallel map of function over
    - `apply(func, *args, cleanup=True, **kwargs)` — Applies func to args in parallel on all of the processes.
    - `from_config(**kw)` — Construct an MPI parallelizer directly from keyword options.
  - **class `SerialNonParallelizer`** (Parallelizer)
    > Totally serial evaluation for cases where no parallelism
    > is provide
    - `get_nprocs()` — Return the fixed serial process count of one.
    - `get_id()` — Return the fixed serial process identifier zero.
    - `initialize()` — Initializes a parallelizer
    - `finalize(exc_type, exc_val, exc_tb)` — Finalizes a parallelizer (if necessary)
    - `on_main()` — Returns whether or not the executing process is the main
    - `send(data, loc, **kwargs)` — A no-op
    - `receive(data, loc, **kwargs)` — A no-op
    - `broadcast(data, **kwargs)` — A no-op
    - `scatter(data, **kwargs)` — A no-op
    - `gather(data, **kwargs)` — A no-op
    - `map(function, data, extra_args=None, extra_kwargs=None, vectorized=True, aggregate=False, **kwargs)` — Performs a serial map of the function over
    - `starmap(function, data, extra_args=None, extra_kwargs=None, **kwargs)` — Performs a serial map with unpacking of the function over
    - `apply(func, *args, comm=None, main_kwargs=None, cleanup=True, **kwargs)` — Call the function once, injecting this serial parallelizer and merging `main_kwargs` before ordinar…
    - `wait()` — No need to wait when you're in a serial environment

### `Runner.py`
  - **class `ClientServerRunner`**
    > Provides a framework for running MPI-like scripts in a client/server
    > model
    - `__init__(client_runner, server_runner, parallelizer)`
    - `run()` — Runs the client/server processes depending on if the parallelizer

### `SharedMemory.py` — Provides classes for working with `multiprocessing.SharedMemory`
  - **class `SharedMemoryInterface`** (typing.Protocol)
    - `__init__(name=None, create=False, size=None)`
    - `close()` — Define the operation that closes this process's handle to the shared buffer.
    - `unlink()` — Define the operation that removes the shared-memory resource.
  - **class `SharedMemoryNDarray`**
    > Provides a very simple tracker for shared NumPy arrays
    - `__init__(shape, dtype, buf, autoclose=True, parallelizer=None)`
    - `from_array(arr, buf, autoclose=None, parallelizer=None)` — Initializes by pulling metainfo from an array
    - `close()` — Release one local reference and close the underlying buffer when the count reaches zero.
    - `unlink()` — Unlink the underlying buffer only when no tracked local references remain.
    - `unshare()` — Copy the shared NumPy view into an ordinary process-local array.
  - **class `SharedArrayAllocator`**
    > Provides the base API to allocate/deallocate
    > NumPy arrays
    - `__init__(parallelizer=None, mem_manager=None, autoclose=True)`
    - `api()` — Lazily import and cache `multiprocessing.shared_memory`, raising a descriptive error if unavailable.
    - `create_shared_array(data, name=None)` — Makes a SharedNDarray object for an existing data chunk
    - `delete_shared_array(shared_array)` — Closes a buffer for a numpy array
    - `update_shared_array(shared_array, data)` — Updates a buffer for a numpy array
  - **class `SharedMemoryPrimitive`**
    > Provides basic support for storing shared memory arrays
    - `__init__(sync_buffer, allocator=None, marshaller=None, parallelizer=None)`
    - `load_item(item)` — Reconstruct and return a process-local copy of an item from its shared-buffer tree.
    - `close()`
  - **class `SharedMemoryList`** (SharedMemoryPrimitive)
    > Implements a shared dict that uses
    > a managed dict to synchronize array metainfo
    > across processes
    - `__init__(*seq, sync_list=None, manager=None, marshaller=None, allocator=None, parallelizer=None)`
    - `unshare()` — Reconstruct every list entry as process-local data.
    - `pop(k=0)` — Remove a stored representation and reconstruct it as process-local data.
    - `insert(k, v)` — Insert an empty slot and then marshal the supplied value into that position.
    - `append(v)` — Append a placeholder and store the supplied value through the synchronized list.
    - `extend(v)` — Reserve slots for all values and populate them.
    - `close()`
  - **class `SharedMemoryDict`** (SharedMemoryPrimitive)
    > Implements a shared dict that uses
    > a managed dict to synchronize array metainfo
    > across processes
    - `__init__(*seq, sync_dict=None, manager=None, marshaller=None, allocator=None, parallelizer=None)`
    - `keys()` — Return the backing dictionary's dynamic key view.
    - `values()` — Return the backing dictionary's dynamic value view of shared representations.
    - `items()` — Return the backing dictionary's dynamic item view.
    - `unshare()` — Reconstruct all entries into a process-local dictionary.
    - `update(v)` — Reserve the incoming keys and marshal each incoming value into shared storage.
    - `close()`
  - **class `SharedAttribute`**
    - `__init__(name, manager)`
  - **class `PrimitiveTypeHolder`**
  - **class `SharedObjectManager`** (BaseObjectManager)
    > Provides a high-level interface to create a manager
    > that supports shared memory objects through the multiprocessing
    > interface
    > Only supports data that can be marshalled into a NumPy array.
    - `__init__(obj, base_dict=None, parallelizer=None)`
    - `is_primitive(val)` — Return whether a value belongs to the container and ndarray types wrapped in `PrimitiveTypeHolder`.
    - `save_attr(attr)` — Move an object attribute into the shared dictionary and replace it with a `SharedAttribute` marker.
    - `del_attr(attr)` — Delete a shared attribute's backing entry when marked, then remove the object attribute.
    - `load_attr(attr)` — Resolve a marked shared attribute and replace the marker on the object with the stored representati…
    - `get_saved_keys(obj)` — Return the keys currently present in the managed object's `__dict__`.
    - `save_keys(keys=None)` — Share each requested object attribute, defaulting to all keys in the object dictionary.
    - `share(keys=None)` — Delegate to an object-specific `share` method when present, otherwise share selected attributes.
    - `load_keys(keys=None)` — Load each requested shared attribute, defaulting to all object dictionary keys.
    - `unshare(keys=None)` — Delegate to an object-specific `unshare` method or restore attributes and unwrap primitive holders.
    - `list(*l)` — Create a `SharedMemoryList` reusing this manager's synchronization manager, marshaller, allocator,…
    - `dict(*d)` — Create a `SharedMemoryDict` reusing this manager's synchronization manager, marshaller, allocator,…
    - `array(a)` — Return an existing shared array unchanged or allocate a new shared-memory copy.