from __future__ import annotations
import abc
import enum
import os.path
import time
import subprocess
from .. import Devutils as dev
from . import ManagedJobQueues as queues
__all__ = ['ExecutionStatus', 'ExecutionQueue', 'ExecutionEngine', 'ManagedJobQueueExecutionEngine', 'SLURMExecutionEngine']

class ExecutionStatus(enum.Enum):
    UNKNOWN = 'unknown'
    RUNNING = 'running'
    PENDING = 'pending'
    COMPLETED = 'completed'
    ERROR = 'error'

class ExecutionFuture(metaclass=abc.ABCMeta):
    poll_time = 1

    def __init__(self, poll_time=None):
        """
        **LLM Docstring**

        Initialize an unresolved execution handle with unknown status, no result, and a polling interval.

        :param poll_time: seconds between status polls
        :type poll_time: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def join(self, timeout=None):
        """
        **LLM Docstring**

        Poll `get_status` until the job leaves the unknown, pending, or running states, raising `TimeoutError` when the elapsed time exceeds the requested limit.

        :param timeout: maximum seconds to wait, or `None` for no deadline
        :type timeout: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    @abc.abstractmethod
    def get_result(self) -> dict:
        """
        **LLM Docstring**

        Abstract interface for retrieving a completed job result.

        :return: abstract interface for retrieving a completed job result.
        :rtype: dict
        """
        ...

    @abc.abstractmethod
    def get_status(self) -> ExecutionStatus:
        """
        **LLM Docstring**

        Abstract interface for querying the current execution state.

        :return: abstract interface for querying the current execution state.
        :rtype: ExecutionStatus
        """
        ...

class JoinableExecutionFuture(ExecutionFuture):

    @abc.abstractmethod
    def await_result(self, timeout=None):
        """
        **LLM Docstring**

        Abstract blocking hook for backends that expose a native result-wait operation.

        :param timeout: maximum seconds to wait, or `None` for no deadline
        :type timeout: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def join(self, timeout=None):
        """
        **LLM Docstring**

        Wait for completion through the backend-specific `await_result` operation instead of status polling.

        :param timeout: maximum seconds to wait, or `None` for no deadline
        :type timeout: object

        :return: No value is returned.
        :rtype: None
        """
        ...

class ExecutionQueue:

    def __init__(self, futures: list[ExecutionFuture]):
        """
        **LLM Docstring**

        Store the execution futures that form a logical submission batch.

        :param futures: the futures included in the queue
        :type futures: list[ExecutionFuture]

        :return: No value is returned.
        :rtype: None
        """
        ...

    def join(self, timeout=None):
        """
        **LLM Docstring**

        Join each future sequentially while deducting elapsed time from a shared timeout budget.

        :param timeout: maximum seconds to wait, or `None` for no deadline
        :type timeout: object

        :return: No value is returned.
        :rtype: None
        """
        ...

class ExecutionEngine(metaclass=abc.ABCMeta):
    name: str
    future_type: type[ExecutionFuture]
    engine_types = {}

    @classmethod
    def register(cls, name, engine=None):
        """
        **LLM Docstring**

        Register an execution-engine class by name, or return a decorator that performs the registration. Passing an engine instance uses its `name` attribute.

        :param name: the registry, resource, or job name
        :type name: object

        :param engine: the execution-engine class or instance to register
        :type engine: object

        :return: register an execution-engine class by name, or return a decorator that performs the registration. Passing an engine instance uses its `name` attribute.
        :rtype: type[ExecutionEngine] | callable
        """
        ...

    @classmethod
    def resolve(cls, name, **opts):
        """
        **LLM Docstring**

        Construct the engine class registered under `name` with the supplied options.

        :param name: the registry, resource, or job name
        :type name: object

        :param opts: backend-specific construction or command options
        :type opts: object

        :return: construct the engine class registered under `name` with the supplied options.
        :rtype: ExecutionEngine
        """
        ...

    def __init__(self, **opts):
        """
        **LLM Docstring**

        Initialize context nesting depth and retain backend-specific construction options.

        :param opts: backend-specific construction or command options
        :type opts: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    @abc.abstractmethod
    def submit_job(self, **kwargs) -> ExecutionFuture:
        """
        **LLM Docstring**

        Abstract interface for submitting one job and returning its future.

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: abstract interface for submitting one job and returning its future.
        :rtype: ExecutionFuture
        """
        ...

    def submit_jobs(self, jobs: list[dict], **kwargs) -> ExecutionQueue:
        """
        **LLM Docstring**

        Submit a sequence of job-option dictionaries, overlay shared options on each entry, and return an `ExecutionQueue`.

        :param jobs: per-job option dictionaries
        :type jobs: list[dict]

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: submit a sequence of job-option dictionaries, overlay shared options on each entry, and return an `ExecutionQueue`.
        :rtype: ExecutionQueue
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Increase the context nesting depth and call `startup` only on the outermost entry.

        :return: No value is returned.
        :rtype: None
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Decrease the context nesting depth and call `shutdown` after leaving the outermost context.

        :param exc_type: the exception class leaving the context
        :type exc_type: object

        :param exc_val: the exception instance leaving the context
        :type exc_val: object

        :param exc_tb: the exception traceback leaving the context
        :type exc_tb: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def startup(self):
        """
        **LLM Docstring**

        No-op lifecycle hook intended for engines that must acquire backend resources.

        :return: No value is returned.
        :rtype: None
        """
        ...

    def shutdown(self):
        """
        **LLM Docstring**

        No-op lifecycle hook intended for engines that must release backend resources.

        :return: No value is returned.
        :rtype: None
        """
        ...

class FileBackedExecutionFuture(ExecutionFuture):
    results_file = 'results.json'
    status_file = 'status.json'

    def __init__(self, watch_dir=None, poll_time=None, results_file=None, status_file=None):
        """
        **LLM Docstring**

        Configure a future whose result and status are read from JSON files, optionally relative to a watched directory.

        :param watch_dir: directory containing result and status files
        :type watch_dir: object

        :param poll_time: seconds between status polls
        :type poll_time: object

        :param results_file: result JSON filename
        :type results_file: object

        :param status_file: status JSON filename
        :type status_file: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def get_result(self) -> dict:
        """
        **LLM Docstring**

        Read and decode the configured result JSON file from the watch directory or current path.

        :return: read and decode the configured result JSON file from the watch directory or current path.
        :rtype: dict
        """
        ...

    def get_status(self) -> ExecutionStatus:
        """
        **LLM Docstring**

        Read the configured status JSON file and convert its `status` field to `ExecutionStatus`; return `UNKNOWN` while the file is absent.

        :return: read the configured status JSON file and convert its `status` field to `ExecutionStatus`; return `UNKNOWN` while the file is absent.
        :rtype: ExecutionStatus
        """
        ...

class ManagedJobQueueExecutionFuture(FileBackedExecutionFuture):

    def __init__(self, job_id, queue_manager: queues.ManagedJobQueueHandler, watch_dir=None, results_file=None, status_file=None, poll_time=None):
        """
        **LLM Docstring**

        Attach a scheduler job identifier and queue manager to a file-backed execution future.

        :param job_id: the scheduler-assigned job identifier
        :type job_id: object

        :param queue_manager: the managed queue used for submission and status lookup
        :type queue_manager: queues.ManagedJobQueueHandler

        :param watch_dir: directory containing result and status files
        :type watch_dir: object

        :param results_file: result JSON filename
        :type results_file: object

        :param status_file: status JSON filename
        :type status_file: object

        :param poll_time: seconds between status polls
        :type poll_time: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def get_status(self) -> ExecutionStatus:
        """
        **LLM Docstring**

        Query the queue manager for the scheduler state and translate it through `queue_status_map`.

        :return: query the queue manager for the scheduler state and translate it through `queue_status_map`.
        :rtype: ExecutionStatus
        """
        ...

class ManagedJobQueueExecutionEngine(ExecutionEngine):
    future_type = ManagedJobQueueExecutionFuture

    def __init__(self, queue_manager: queues.ManagedJobQueueHandler, **opts):
        """
        **LLM Docstring**

        Initialize an execution engine backed by a managed job-queue handler.

        :param queue_manager: the managed queue used for submission and status lookup
        :type queue_manager: queues.ManagedJobQueueHandler

        :param opts: backend-specific construction or command options
        :type opts: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def prep_future_opts(self, watch_dir=None, results_file=None, status_file=None, poll_time=None, **kwargs):
        """
        **LLM Docstring**

        Separate file-watching and polling options for the future from the remaining scheduler submission options.

        :param watch_dir: directory containing result and status files
        :type watch_dir: object

        :param results_file: result JSON filename
        :type results_file: object

        :param status_file: status JSON filename
        :type status_file: object

        :param poll_time: seconds between status polls
        :type poll_time: object

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: separate file-watching and polling options for the future from the remaining scheduler submission options.
        :rtype: tuple[dict, dict]
        """
        ...

    def submit_job(self, *, watch_dir=None, poll_time=None, results_file=None, status_file=None, **kwargs) -> ManagedJobQueueExecutionFuture:
        """
        **LLM Docstring**

        Submit the scheduler options through the queue manager and construct a future for the returned job identifier.

        :param watch_dir: directory containing result and status files
        :type watch_dir: object

        :param poll_time: seconds between status polls
        :type poll_time: object

        :param results_file: result JSON filename
        :type results_file: object

        :param status_file: status JSON filename
        :type status_file: object

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: submit the scheduler options through the queue manager and construct a future for the returned job identifier.
        :rtype: ManagedJobQueueExecutionFuture
        """
        ...

class SLURMExecutionFuture(ManagedJobQueueExecutionFuture):

    def get_status(self) -> ExecutionStatus:
        """
        **LLM Docstring**

        Query SLURM state, but interpret a previously visible running/completed/error job that has disappeared from the queue as completed.

        :return: query SLURM state, but interpret a previously visible running/completed/error job that has disappeared from the queue as completed.
        :rtype: ExecutionStatus
        """
        ...

class SLURMExecutionEngine(ManagedJobQueueExecutionEngine):
    future_type = SLURMExecutionFuture

    def __init__(self, **opts):
        """
        **LLM Docstring**

        Construct a managed-queue execution engine using the built-in `SLURMHandler`.

        :param opts: backend-specific construction or command options
        :type opts: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def prep_future_opts(self, *, sbatch_file, watch_dir=None, chdir=None, **kwargs):
        """
        **LLM Docstring**

        Derive the watch directory from `chdir` or the sbatch-file directory, then split future options from submission options.

        :param sbatch_file: path to the sbatch script
        :type sbatch_file: object

        :param watch_dir: directory containing result and status files
        :type watch_dir: object

        :param chdir: scheduler working-directory option
        :type chdir: object

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: derive the watch directory from `chdir` or the sbatch-file directory, then split future options from submission options.
        :rtype: tuple[dict, dict]
        """
        ...

    def submit_job(self, sbatch_file, *, watch_dir=None, poll_time=None, results_file=None, status_file=None, **kwargs) -> ManagedJobQueueExecutionFuture:
        """
        **LLM Docstring**

        Submit an sbatch file, unpack the returned SLURM job id, and create an SLURM-aware execution future.

        :param sbatch_file: path to the sbatch script
        :type sbatch_file: object

        :param watch_dir: directory containing result and status files
        :type watch_dir: object

        :param poll_time: seconds between status polls
        :type poll_time: object

        :param results_file: result JSON filename
        :type results_file: object

        :param status_file: status JSON filename
        :type status_file: object

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: submit an sbatch file, unpack the returned SLURM job id, and create an SLURM-aware execution future.
        :rtype: ManagedJobQueueExecutionFuture
        """
        ...

class ProcessExecutionFuture(JoinableExecutionFuture):

    def __init__(self, base_obj, **ignored):
        """
        **LLM Docstring**

        Wrap an asynchronous process result and mark its cached result as not yet retrieved.

        :param base_obj: the wrapped asynchronous result object
        :type base_obj: object

        :param ignored: extra options accepted for interface compatibility
        :type ignored: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def await_result(self, timeout=None):
        """
        **LLM Docstring**

        Call the wrapped result object’s blocking `get` once and cache the returned value.

        :param timeout: maximum seconds to wait, or `None` for no deadline
        :type timeout: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def get_result(self):
        """
        **LLM Docstring**

        Return the cached asynchronous result, or `None` before it has been awaited.

        :return: return the cached asynchronous result, or `None` before it has been awaited.
        :rtype: object | None
        """
        ...

    def get_status(self) -> ExecutionStatus:
        """
        **LLM Docstring**

        Use the wrapped result’s `successful` method to distinguish running, completed, and failed states.

        :return: use the wrapped result’s `successful` method to distinguish running, completed, and failed states.
        :rtype: ExecutionStatus
        """
        ...

class ProcessGeneratorExecutionEngine(ExecutionEngine):
    future_type = ProcessExecutionFuture

    def __init__(self, proc_gen, **opts):
        """
        **LLM Docstring**

        Store a pool-like process generator used for asynchronous method execution.

        :param proc_gen: a pool-like object supporting `apply_async` and context management
        :type proc_gen: object

        :param opts: backend-specific construction or command options
        :type opts: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def submit_job(self, method, **kwargs):
        """
        **LLM Docstring**

        Submit `method` with keyword arguments through `apply_async` and wrap the asynchronous result.

        :param method: the callable submitted asynchronously
        :type method: object

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: submit `method` with keyword arguments through `apply_async` and wrap the asynchronous result.
        :rtype: ProcessExecutionFuture
        """
        ...

    def startup(self):
        """
        **LLM Docstring**

        Enter the process-generator context when the engine becomes active.

        :return: No value is returned.
        :rtype: None
        """
        ...

    def shutdown(self):
        """
        **LLM Docstring**

        Exit the process-generator context when the engine is deactivated.

        :return: No value is returned.
        :rtype: None
        """
        ...