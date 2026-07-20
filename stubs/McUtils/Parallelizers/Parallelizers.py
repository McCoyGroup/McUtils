"""
Provides a simple framework for unifying different parallelism approaches.
Currently primarily targets multiprocessing and mpi4py, but also should work
with Ray. Dask will require more work unfortunately...
"""
import abc, functools, multiprocessing as mp, multiprocessing.pool as mp_pool, typing, uuid, os
import contextlib
import enum
import numpy as np, pickle, time
from .. import Devutils as dev
from ..Scaffolding import Logger, NullLogger, ObjectRegistry
from .SharedMemory import SharedObjectManager, SharedMemoryList, SharedMemoryDict
__all__ = ['Parallelizer', 'MultiprocessingParallelizer', 'MPIParallelizer', 'SerialNonParallelizer', 'SendRecieveParallelizer']

class CallerContract:
    """
    Provides a structure so that a main process and child process can
    be synchronized in their MPI-like calls
    """

    def __init__(self, calls):
        """
        **LLM Docstring**

        Initialize an ordered cyclic contract for collective or point-to-point calls.

        :param calls: Value supplied for `calls`.
        :type calls: Any
        :return: None.
        :rtype: None
        """
        ...

    def handle_call(self, caller, next_call):
        """
        **LLM Docstring**

        Validate the next operation against the contract and advance the expected-call index cyclically.

        :param caller: Value supplied for `caller`.
        :type caller: Any
        :param next_call: Value supplied for `next_call`.
        :type next_call: Any
        :return: None.
        :rtype: None
        """
        ...

class ChildProcessRuntimeError(RuntimeError):
    ...

class Parallelizer(metaclass=abc.ABCMeta):
    """
    Abstract base class to help manage parallelism.
    Provides the basic API that all parallelizers can be expected
    to conform to.
    Provides effectively the union of operations supported by
    `mp.Pool` and `MPI`.
    There is also the ability to lookup and register 'named'
    parallelizers, since we expect a single program to not
    really use more than one.
    This falls back gracefully to the serial case.
    """
    _par_registry = None
    default_printer = print
    base_log_level = Logger.LogLevel.MoreDebug

    def __init__(self, logger=None, contract=None, uid=None, initialization_function=None, initialization_args=None, initialization_kwargs=None):
        """
        **LLM Docstring**

        Initialize registry, logging, call-contract, worker-initialization, and context state for a parallelizer.

        :param logger: Value supplied for `logger`.
        :type logger: Any
        :param contract: Value supplied for `contract`.
        :type contract: Any
        :param uid: Value supplied for `uid`.
        :type uid: Any
        :param initialization_function: Value supplied for `initialization_function`.
        :type initialization_function: Any
        :param initialization_args: Value supplied for `initialization_args`.
        :type initialization_args: Any
        :param initialization_kwargs: Value supplied for `initialization_kwargs`.
        :type initialization_kwargs: Any
        :return: None.
        :rtype: None
        """
        ...

    @classmethod
    def load_registry(cls):
        """
        **LLM Docstring**

        Lazily create the shared parallelizer registry with a serial fallback as its default.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    @property
    def parallelizer_registry(self):
        """
        **LLM Docstring**

        Return the lazily initialized class-level parallelizer registry.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    @classmethod
    def get_default(cls):
        """
        For compat.

        :return:
        :rtype:
        """
        ...

    class Backends(enum.Enum):
        Serial = 'serial'
        MPI = 'mpi'
        Multiprocessing = 'multiprocessing'

    @classmethod
    def get_paralellizer_types(cls):
        """
        **LLM Docstring**

        Return the built-in backend enum-to-class mapping. The method name retains the source spelling.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...
    parallelizer_dispatch = None

    @classmethod
    def lookup(cls, key, construct=True) -> 'Parallelizer':
        """
        Checks in the registry to see if a given parallelizer is there
        otherwise returns a `SerialNonParallelizer`.
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def register(self, key):
        """
        Checks in the registry to see if a given parallelizer is there
        otherwise returns a `SerialNonParallelizer`.
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    @property
    def active(self):
        """
        **LLM Docstring**

        Return whether at least one nested parallelizer context is active.
        :return: Whether the context nesting count is positive.
        :rtype: bool
        """
        ...

    def set_initializer(self, func, *args, **kwargs):
        """
        **LLM Docstring**

        Store a partially bound initializer and immediately run it through the parallelizer.

        :param func: Value supplied for `func`.
        :type func: Any
        :param args: Value supplied for `args`.
        :type args: Any
        :param kwargs: Value supplied for `kwargs`.
        :type kwargs: Any
        :return: None.
        :rtype: None
        """
        ...

    @abc.abstractmethod
    def initialize(self):
        """
        Initializes a parallelizer
        if necessary
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def finalize(self, exc_type, exc_val, exc_tb):
        """
        Finalizes a parallelizer (if necessary)
        if necessary
        :return:
        :rtype:
        """
        ...

    def __enter__(self):
        """
        Allows the parallelizer context to be set
        using `with`
        :return:
        :rtype:
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Allows the parallelizer context to be unset
        using `with`
        :param exc_type:
        :type exc_type:
        :param exc_val:
        :type exc_val:
        :param exc_tb:
        :type exc_tb:
        :return:
        :rtype:
        """
        ...

    class InMainProcess:
        """
        Singleton representing being on the
        main process
        """

    class InWorkerProcess:
        """
        Singleton representing being on a
        worker process
        """

    @property
    @abc.abstractmethod
    def on_main(self):
        """
        Returns whether or not the executing process is the main
        process or not
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def main_restricted(func):
        """
        A decorator to indicate that a function should only be
        run when on the main process
        :param func:
        :type func:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def worker_restricted(func):
        """
        A decorator to indicate that a function should only be
        run when on a worker process
        :param func:
        :type func:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def send(self, data, loc, **kwargs):
        """
        Sends data to the process specified by loc

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def receive(self, data, loc, **kwargs):
        """
        Receives data from the process specified by loc

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def broadcast(self, data, **kwargs):
        """
        Sends the same data to all processes

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def scatter(self, data, locs=None, return_locs=False, **kwargs):
        """
        Performs a scatter of data to the different
        available parallelizer processes.
        *NOTE:* unlike in the MPI case, `data` does not
        need to be evenly divisible by the number of available
        processes

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def gather(self, data, **kwargs):
        """
        Performs a gather of data from the different
        available parallelizer processes

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def map(self, function, data, extra_args=None, extra_kwargs=None, **kwargs):
        """
        Performs a parallel map of function over
        the held data on different processes

        :param function:
        :type function:
        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def starmap(self, function, data, extra_args=None, extra_kwargs=None, **kwargs):
        """
        Performs a parallel map with unpacking of function over
        the held data on different processes

        :param function:
        :type function:
        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def apply(self, func, *args, main_kwargs=None, cleanup=True, **kwargs):
        """
        Runs the callable `func` in parallel
        :param func:
        :type func:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def run(self, func, *args, comm=None, main_kwargs=None, **kwargs):
        """
        Calls `apply`, but makes sure state is handled cleanly

        :param func:
        :type func:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...
    mode_map = {}

    @classmethod
    def from_config(cls, mode=None, **kwargs):
        """
        **LLM Docstring**

        Construct the backend registered for a mode by delegating the remaining options to its `from_config` method.

        :param mode: Value supplied for `mode`.
        :type mode: Any
        :param kwargs: Value supplied for `kwargs`.
        :type kwargs: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    @property
    def nprocs(self):
        """
        Returns the number of processes the parallelizer has
        to work with
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def get_nprocs(self):
        """
        Returns the number of processes
        :return:
        :rtype:
        """
        ...

    @property
    def id(self):
        """
        Returns some form of identifier for the current process
        :return:
        :rtype:
        """
        ...

    @property
    def pid(self):
        """
        **LLM Docstring**

        Lazily cache and return the current operating-system process ID.
        :return: The cached process ID.
        :rtype: int
        """
        ...

    @abc.abstractmethod
    def get_id(self):
        """
        Returns the id for the current process
        :return:
        :rtype:
        """
        ...

    @property
    def printer(self):
        """
        **LLM Docstring**

        Return the default printer when no logger is set, otherwise return `logger.log_print`.
        :return: The callable used for output.
        :rtype: Callable
        """
        ...

    @printer.setter
    def printer(self, p):
        """
        **LLM Docstring**

        Return the default printer when no logger is set, otherwise return `logger.log_print`.
        :return: The callable used for output.
        :rtype: Callable
        """
        ...

    def main_print(self, *args, **kwargs):
        """
        Prints from the main process
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def worker_print(self, *args, **kwargs):
        """
        Prints from a main worker process
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def print(self, *args, where='both', **kwargs):
        """
        An implementation of print that operates differently on workers than on main
        processes

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def wait(self):
        """
        Causes all processes to wait until they've met up at this point.
        :return:
        :rtype:
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a diagnostic representation with backend type, process id, process count, and UUID.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def share(self, obj):
        """
        Converts `obj` into a form that can be cleanly used with shared memory via a `SharedObjectManager`

        :param obj:
        :type obj:
        :return:
        :rtype:
        """
        ...

class SendRecieveParallelizer(Parallelizer):
    """
    Parallelizer that implements `scatter`, `gather`, `broadcast`, and `map`
    based on just having a communicator that supports `send` and `receive methods
    """

    class ReceivedError:

        def __init__(self, error):
            """
            **LLM Docstring**

            Wrap an exception so it can be transferred through the communicator and re-raised by the receiver.

            :param error: Value supplied for `error`.
            :type error: Any
            :return: None.
            :rtype: None
            """
            ...

    class SendReceieveCommunicator(metaclass=abc.ABCMeta):
        """
        A base class that provides an interface for
        sending/receiving data from a specific subprocesses
        """

        @property
        @abc.abstractmethod
        def locations(self):
            """
            Returns the list of locations known by the
            `SendReceieverCommunicator`
            :return:
            :rtype:
            """
            ...

        @property
        @abc.abstractmethod
        def location(self):
            """
            Returns the _current_ location
            :return:
            :rtype:
            """
            ...

        @abc.abstractmethod
        def send(self, data, loc, **kwargs):
            """
            Sends the specified data to loc
            :param data:
            :type data:
            :param loc:
            :type loc:
            :param kwargs:
            :type kwargs:
            :return:
            :rtype:
            """
            ...

        @abc.abstractmethod
        def receive(self, data, loc, **kwargs):
            """
            Receives the specified data from loc
            :param data:
            :type data:
            :param loc:
            :type loc:
            :param kwargs:
            :type kwargs:
            :return:
            :rtype:
            """
            ...

    @property
    @abc.abstractmethod
    def comm(self):
        """
        Returns the communicator used by the paralellizer
        :return:
        :rtype: SendRecieveParallelizer.SendReceieveCommunicator
        """
        ...

    def send(self, data, loc, **kwargs):
        """
        Sends data to the process specified by loc

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def receive(self, data, loc, **kwargs):
        """
        Receives data from the process specified by loc

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def broadcast(self, data, locs=None, **kwargs):
        """
        Sends the same data to all processes

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def scatter(self, data, locs=None, return_locs=False, **kwargs):
        """
        Performs a scatter of data to the different
        available parallelizer processes.
        *NOTE:* unlike in the MPI case, `data` does not
        need to be evenly divisible by the number of available
        processes

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def gather(self, data, locs=None, **kwargs):
        """
        Performs a gather of data from the different
        available parallelizer processes

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def map(self, func, data, extra_args=None, extra_kwargs=None, vectorized=False, aggregate=True, **kwargs):
        """
        Performs a parallel map of function over
        the held data on different processes

        :param function:
        :type function:
        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def starmap(self, func, data, extra_args=None, extra_kwargs=None, **kwargs):
        """
        Performs a parallel map with unpacking of function over
        the held data on different processes

        :param function:
        :type function:
        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def wait(self):
        """
        Causes all processes to wait until they've met up at this point.
        :return:
        :rtype:
        """
        ...

class MultiprocessingParallelizer(SendRecieveParallelizer):
    """
    Parallelizes using a  process pool and a runner
    function that represents a "main loop".
    """

    class SendRecvQueuePair:

        def __init__(self, id: int, manager: 'mp.managers.SyncManager'):
            """
            **LLM Docstring**

            Allocate managed send/receive queues and an initialization event for one pool location.

            :param id: Value supplied for `id`.
            :type id: int
            :param manager: Value supplied for `manager`.
            :type manager: 'mp.managers.SyncManager'
            :return: None.
            :rtype: None
            """
            ...

        def __repr__(self):
            """
            **LLM Docstring**

            Return the queue-pair type and numeric location identifier.
            :return: The value produced by the implementation; see the summary for its exact semantics.
            :rtype: Any
            """
            ...

    class PoolCommunicator(SendRecieveParallelizer.SendReceieveCommunicator):
        """
        Defines a serializable process communicator
        that allows communication with a managed `mp.Pool`
        to support `send` and `receive` and therefore to
        support the rest of the necessary bits of the MPI API
        """

        def __init__(self, parent: 'MultiprocessingParallelizer', id: int, queues: typing.Iterable['MultiprocessingParallelizer.SendRecvQueuePair'], initialization_timeout: float=None, group: typing.Iterable['MultiprocessingParallelizer.PoolCommunicator']=None):
            """
            **LLM Docstring**

            Bind a pool rank to shared queue pairs, an optional initialization timeout, and an optional communicator group.

            :param parent: Value supplied for `parent`.
            :type parent: 'MultiprocessingParallelizer'
            :param id: Value supplied for `id`.
            :type id: int
            :param queues: Value supplied for `queues`.
            :type queues: typing.Iterable['MultiprocessingParallelizer.SendRecvQueuePair']
            :param initialization_timeout: Value supplied for `initialization_timeout`.
            :type initialization_timeout: float
            :param group: Value supplied for `group`.
            :type group: typing.Iterable['MultiprocessingParallelizer.PoolCommunicator']
            :return: None.
            :rtype: None
            """
            ...

        def __repr__(self):
            """
            **LLM Docstring**

            Return the communicator type and current rank.
            :return: The value produced by the implementation; see the summary for its exact semantics.
            :rtype: Any
            """
            ...

        class PoolError(Exception):
            """
            For errors arising from Pool operations
            """

        def initialize(self):
            """
            Performs initialization of the communicator
            (basically just waits until all threads say all is well)
            :return:
            :rtype:
            """
            ...

        def reset(self):
            """
            Performs initialization of the communicator
            (basically just waits until all threads say all is well)
            :return:
            :rtype:
            """
            ...

        @property
        def locations(self):
            """
            Returns the list of queue ids
            :return:
            :rtype:
            """
            ...

        @property
        def location(self):
            """
            Returns the _current_ location
            :return:
            :rtype:
            """
            ...

        def send(self, data, loc, prepickled=False, **kwargs):
            """
            Sends the specified data to loc
            :param data:
            :type data:
            :param loc:
            :type loc:
            :param kwargs:
            :type kwargs:
            :return:
            :rtype:
            """
            ...

        def receive(self, data, loc, prepickled=False, **kwargs):
            """
            Receives the specified data from loc
            :param data:
            :type data:
            :param loc:
            :type loc:
            :param kwargs:
            :type kwargs:
            :return:
            :rtype:
            """
            ...

        def get_subcomm(self, idx):
            """
            **LLM Docstring**

            Create a communicator restricted to selected queue and group indices while preserving the current communicator id.

            :param idx: Value supplied for `idx`.
            :type idx: Any
            :return: The value produced by the implementation; see the summary for its exact semantics.
            :rtype: Any
            """
            ...
    _is_worker = False

    def __init__(self, worker=False, pool: mp.Pool=None, context=None, manager=None, logger=None, contract=None, comm=None, rank=None, allow_restart=True, initialization_timeout=0.5, initialization_function=None, initialization_args=None, initialization_kwargs=None, **kwargs):
        """
        **LLM Docstring**

        Configure multiprocessing pool ownership, communicator state, worker rank, restart behavior, and initialization options.

        :param worker: Value supplied for `worker`.
        :type worker: Any
        :param pool: Value supplied for `pool`.
        :type pool: mp.Pool
        :param context: Value supplied for `context`.
        :type context: Any
        :param manager: Value supplied for `manager`.
        :type manager: Any
        :param logger: Value supplied for `logger`.
        :type logger: Any
        :param contract: Value supplied for `contract`.
        :type contract: Any
        :param comm: Value supplied for `comm`.
        :type comm: Any
        :param rank: Value supplied for `rank`.
        :type rank: Any
        :param allow_restart: Value supplied for `allow_restart`.
        :type allow_restart: Any
        :param initialization_timeout: Value supplied for `initialization_timeout`.
        :type initialization_timeout: Any
        :param initialization_function: Value supplied for `initialization_function`.
        :type initialization_function: Any
        :param initialization_args: Value supplied for `initialization_args`.
        :type initialization_args: Any
        :param initialization_kwargs: Value supplied for `initialization_kwargs`.
        :type initialization_kwargs: Any
        :param kwargs: Value supplied for `kwargs`.
        :type kwargs: Any
        :return: None.
        :rtype: None
        """
        ...

    def get_nprocs(self):
        """
        **LLM Docstring**

        Return the cached multiprocessing process count.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def get_id(self):
        """
        **LLM Docstring**

        Return the explicit rank when set, otherwise obtain the id from the current communicator.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    @property
    def comm(self):
        """
        Returns the communicator used by the paralellizer
        :return:
        :rtype: MultiprocessingParallelizer.PoolCommunicator
        """
        ...

    @comm.setter
    def comm(self, c):
        """
        **LLM Docstring**

        Return the current communicator, lazily constructing the full communicator group when necessary.

        :param c: Value supplied for `c`.
        :type c: Any
        :return: None.
        :rtype: None
        """
        ...

    def __getstate__(self):
        """
        **LLM Docstring**

        Prepare the parallelizer for pickling by removing live pool, manager, queue, stack, communicator, and PID state.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def __setstate__(self, state):
        """
        **LLM Docstring**

        Restore pickled state and, when available, replace it with the registered parent parallelizer state.

        :param state: Value supplied for `state`.
        :type state: Any
        :return: None.
        :rtype: None
        """
        ...

    @staticmethod
    def _run(runner, comm: PoolCommunicator, args, kwargs, main_kwargs=None):
        """
        Static runner function that just dispatches methods out to
        cores
        :param runner:
        :type runner:
        :param comm:
        :type comm:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def apply(self, func, *args, comm=None, main_kwargs=None, cleanup=True, **kwargs):
        """
        Applies func to args in parallel on all of the processes

        :param func:
        :type func:
        :param args:
        :type args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def _get_pool(self, manager: mp.Manager, **kwargs) -> mp.pool.Pool:
        """
        **LLM Docstring**

        Create a process pool from the supplied multiprocessing context, adding default size and worker initializer options.

        :param manager: Value supplied for `manager`.
        :type manager: mp.Manager
        :param kwargs: Value supplied for `kwargs`.
        :type kwargs: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: mp.pool.Pool
        """
        ...

    @staticmethod
    def get_pool_context(pool):
        """
        **LLM Docstring**

        Return the private multiprocessing context stored by a pool.

        :param pool: Value supplied for `pool`.
        :type pool: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    @staticmethod
    def get_pool_nprocs(pool):
        """
        **LLM Docstring**

        Return the private process-count field stored by a pool.

        :param pool: Value supplied for `pool`.
        :type pool: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def _reset_mp_caches(self):
        """
        **LLM Docstring**

        Clear cached pool, queues, and communicator state before attempting a restart.
        :return: None.
        :rtype: None
        """
        ...

    @classmethod
    def _initialize_worker(cls, initializer=None, *etc):
        """
        Sets a flag so that worker processes
        can know immediately that they are workers
        """
        ...

    def set_initializer(self, func, *args, **kwargs):
        """
        **LLM Docstring**

        Install and run an initializer locally, map worker initialization across the pool, and update the pool initializer.

        :param func: Value supplied for `func`.
        :type func: Any
        :param args: Value supplied for `args`.
        :type args: Any
        :param kwargs: Value supplied for `kwargs`.
        :type kwargs: Any
        :return: None.
        :rtype: None
        """
        ...

    def initialize(self, allow_restart=None):
        """
        **LLM Docstring**

        Create or re-enter the pool, create manager-backed communication queues, initialize workers, and establish process-count state.

        :param allow_restart: Value supplied for `allow_restart`.
        :type allow_restart: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def finalize(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Exit the owned pool on the main process and clear communication queues and the cached communicator.

        :param exc_type: Value supplied for `exc_type`.
        :type exc_type: Any
        :param exc_val: Value supplied for `exc_val`.
        :type exc_val: Any
        :param exc_tb: Value supplied for `exc_tb`.
        :type exc_tb: Any
        :return: None.
        :rtype: None
        """
        ...

    @property
    def on_main(self):
        """
        **LLM Docstring**

        Return `True` when this instance is not marked as a worker.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    @classmethod
    def from_config(cls, **kw):
        """
        **LLM Docstring**

        Construct a multiprocessing parallelizer directly from keyword options.

        :param kw: Value supplied for `kw`.
        :type kw: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...
Parallelizer.mode_map['multiprocessing'] = MultiprocessingParallelizer

class MPIParallelizer(SendRecieveParallelizer):
    """
    Parallelizes using `mpi4py`
    """

    class MPICommunicator(SendRecieveParallelizer.SendReceieveCommunicator):
        """
        A base class that provides an interface for
        sending/receiving data from a specific subprocesses
        """

        def __init__(self, parent, mpi_comm, api):
            """
            **LLM Docstring**

            Bind the parent parallelizer, mpi4py communicator, and MPI API module.

            :param parent: Value supplied for `parent`.
            :type parent: Any
            :param mpi_comm: Value supplied for `mpi_comm`.
            :type mpi_comm: Any
            :param api: Value supplied for `api`.
            :type api: Any
            :return: None.
            :rtype: None
            """
            ...

        @property
        def type_map(self):
            """
            Kinda hacky type map...hopefully
            sufficient to just have a few core numeric types?
            """
            ...

        def get_mpi_type(self, dtype):
            """
            Gets the MPI datatype for the numpy
            dtype
            """
            ...

        @property
        def nprocs(self):
            """
            Returns the number of available processes
            :return:
            :rtype:
            """
            ...

        @property
        def locations(self):
            """
            Returns the list of locations known by the
            `SendReceieverCommunicator`
            :return:
            :rtype:
            """
            ...

        @property
        def location(self):
            """
            Returns the _current_ location
            :return:
            :rtype:
            """
            ...

        def send(self, data, loc, **kwargs):
            """
            Sends the specified data to loc
            :param data:
            :type data:
            :param loc:
            :type loc:
            :param kwargs:
            :type kwargs:
            :return:
            :rtype:
            """
            ...

        def receive(self, data, loc, root=0, **kwargs):
            """
            Receives the specified data from loc
            :param data:
            :type data:
            :param loc:
            :type loc:
            :param kwargs:
            :type kwargs:
            :return:
            :rtype:
            """
            ...

        def broadcast(self, data, root=0, **kwargs):
            """
            Sends the same data to all processes

            :param data:
            :type data:
            :param kwargs:
            :type kwargs:
            :return:
            :rtype:
            """
            ...

        def scatter_obj(self, data, root=0, **kwargs):
            """
            Scatters data to the different MPI ranks using a series
            of send calls.
            This is the default for anything except numpy arrays.

            :param data:
            :type data:
            :param root:
            :type root:
            :param kwargs:
            :type kwargs:
            :return:
            :rtype:
            """
            ...

        def scatter(self, data, root=0, shape=None, dtype=None, **kwargs):
            """
            Performs a scatter of data to the different
            available parallelizer processes.
            *NOTE:* unlike in the MPI case, `data` does not
            need to be evenly divisible by the number of available
            processes

            :param data:
            :type data:
            :param kwargs:
            :type kwargs:
            :return:
            :rtype:
            """
            ...

        def gather_obj(self, data, root=0, **kwargs):
            """
            **LLM Docstring**

            Gather arbitrary Python objects to the root using the communicator's request/response receive protocol.

            :param data: Value supplied for `data`.
            :type data: Any
            :param root: Value supplied for `root`.
            :type root: Any
            :param kwargs: Value supplied for `kwargs`.
            :type kwargs: Any
            :return: The value produced by the implementation; see the summary for its exact semantics.
            :rtype: Any
            """
            ...

        def gather(self, data, root=0, shape=None, dtype=None, **kwargs):
            """
            Performs a gather from the different
            available parallelizer processes.

            :param data:
            :type data:
            :param kwargs:
            :type kwargs:
            :return:
            :rtype:
            """
            ...

    def __init__(self, root=0, comm=None, contract=None, logger=None):
        """
        **LLM Docstring**

        Load mpi4py, select the world or supplied communicator, and initialize the root-aware communicator wrapper.

        :param root: Value supplied for `root`.
        :type root: Any
        :param comm: Value supplied for `comm`.
        :type comm: Any
        :param contract: Value supplied for `contract`.
        :type contract: Any
        :param logger: Value supplied for `logger`.
        :type logger: Any
        :return: None.
        :rtype: None
        """
        ...

    def get_nprocs(self):
        """
        **LLM Docstring**

        Return the MPI communicator size.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def get_id(self):
        """
        **LLM Docstring**

        Return the current MPI rank.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def initialize(self):
        """
        **LLM Docstring**

        Perform no initialization because mpi4py owns MPI startup.
        :return: None.
        :rtype: None
        """
        ...

    def finalize(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Perform no finalization because mpi4py owns MPI shutdown.

        :param exc_type: Value supplied for `exc_type`.
        :type exc_type: Any
        :param exc_val: Value supplied for `exc_val`.
        :type exc_val: Any
        :param exc_tb: Value supplied for `exc_tb`.
        :type exc_tb: Any
        :return: None.
        :rtype: None
        """
        ...

    @property
    def comm(self):
        """
        Returns the communicator used by the paralellizer
        :return:
        :rtype: MPIParallelizer.MPICommunicator
        """
        ...

    @property
    def on_main(self):
        """
        **LLM Docstring**

        Return whether the current communicator rank is zero. This ignores the configurable `root` field.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def broadcast(self, data, **kwargs):
        """
        Sends the same data to all processes

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def scatter(self, data, shape=None, **kwargs):
        """
        Performs a scatter of data to the different
        available parallelizer processes.
        *NOTE:* unlike in the MPI case, `data` does not
        need to be evenly divisible by the number of available
        processes

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def gather(self, data, shape=None, **kwargs):
        """
        Performs a gather of data from the different
        available parallelizer processes

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def map(self, func, data, input_shape=None, output_shape=None, **kwargs):
        """
        Performs a parallel map of function over
        the held data on different processes

        :param function:
        :type function:
        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def apply(self, func, *args, cleanup=True, **kwargs):
        """
        Applies func to args in parallel on all of the processes.
        For MPI, since jobs are always started with mpirun, this
        is just a regular apply

        :param func:
        :type func:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def from_config(cls, **kw):
        """
        **LLM Docstring**

        Construct an MPI parallelizer directly from keyword options.

        :param kw: Value supplied for `kw`.
        :type kw: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...
Parallelizer.mode_map['mpi'] = MPIParallelizer

class SerialNonParallelizer(Parallelizer):
    """
    Totally serial evaluation for cases where no parallelism
    is provide
    """

    def get_nprocs(self):
        """
        **LLM Docstring**

        Return the fixed serial process count of one.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def get_id(self):
        """
        **LLM Docstring**

        Return the fixed serial process identifier zero.
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def initialize(self):
        """
        Initializes a parallelizer
        if necessary
        :return:
        :rtype:
        """
        ...

    def finalize(self, exc_type, exc_val, exc_tb):
        """
        Finalizes a parallelizer (if necessary)
        if necessary
        :return:
        :rtype:
        """
        ...

    @property
    def on_main(self):
        """
        Returns whether or not the executing process is the main
        process or not
        :return:
        :rtype:
        """
        ...

    def send(self, data, loc, **kwargs):
        """
        A no-op

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def receive(self, data, loc, **kwargs):
        """
        A no-op

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def broadcast(self, data, **kwargs):
        """
        A no-op

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def scatter(self, data, **kwargs):
        """
        A no-op

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def gather(self, data, **kwargs):
        """
        A no-op

        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def map(self, function, data, extra_args=None, extra_kwargs=None, vectorized=True, aggregate=False, **kwargs):
        """
        Performs a serial map of the function over
        the passed data

        :param function:
        :type function:
        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def starmap(self, function, data, extra_args=None, extra_kwargs=None, **kwargs):
        """
        Performs a serial map with unpacking of the function over
        the passed data

        :param function:
        :type function:
        :param data:
        :type data:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    def apply(self, func, *args, comm=None, main_kwargs=None, cleanup=True, **kwargs):
        """
        **LLM Docstring**

        Call the function once, injecting this serial parallelizer and merging `main_kwargs` before ordinary keyword arguments.

        :param func: Value supplied for `func`.
        :type func: Any
        :param comm: Value supplied for `comm`.
        :type comm: Any
        :param main_kwargs: Value supplied for `main_kwargs`.
        :type main_kwargs: Any
        :param cleanup: Value supplied for `cleanup`.
        :type cleanup: Any
        :param args: Value supplied for `args`.
        :type args: Any
        :param kwargs: Value supplied for `kwargs`.
        :type kwargs: Any
        :return: The value produced by the implementation; see the summary for its exact semantics.
        :rtype: Any
        """
        ...

    def wait(self):
        """
        No need to wait when you're in a serial environment
        :return:
        :rtype:
        """
        ...