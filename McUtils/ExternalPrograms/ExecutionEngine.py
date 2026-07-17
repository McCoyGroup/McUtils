from __future__ import annotations

import abc
import enum
import os.path
import time
import subprocess
from .. import Devutils as dev
from . import ManagedJobQueues as queues

__all__ = [
    "ExecutionStatus",
    "ExecutionQueue",
    "ExecutionEngine",
    # "PoolSubmissionEngine",
    "ManagedJobQueueExecutionEngine",
    "SLURMExecutionEngine"
]

class ExecutionStatus(enum.Enum):
    UNKNOWN = "unknown"
    RUNNING = "running"
    PENDING = "pending"
    COMPLETED = "completed"
    ERROR = "error"

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
        self.status = ExecutionStatus.UNKNOWN
        self._is_complete = False
        self._result = None
        self.poll_time = self.poll_time if poll_time is None else poll_time
    def join(self, timeout=None):
        """
        **LLM Docstring**

        Poll `get_status` until the job leaves the unknown, pending, or running states, raising `TimeoutError` when the elapsed time exceeds the requested limit.

        :param timeout: maximum seconds to wait, or `None` for no deadline
        :type timeout: object

        :return: No value is returned.
        :rtype: None
        """
        self.status = self.get_status()
        cur = time.time()
        while self.status in {ExecutionStatus.UNKNOWN, ExecutionStatus.RUNNING, ExecutionStatus.PENDING}:
            time.sleep(self.poll_time)
            self.status = self.get_status()
            if timeout is not None:
                now = time.time()
                if now - cur > timeout:
                    raise TimeoutError(f"job {self} timed out during join")
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
        self.await_result(timeout=timeout)

class ExecutionQueue:
    def __init__(self, futures:list[ExecutionFuture]):
        """
        **LLM Docstring**

        Store the execution futures that form a logical submission batch.

        :param futures: the futures included in the queue
        :type futures: list[ExecutionFuture]

        :return: No value is returned.
        :rtype: None
        """
        self.futures = futures
    def join(self, timeout=None):
        """
        **LLM Docstring**

        Join each future sequentially while deducting elapsed time from a shared timeout budget.

        :param timeout: maximum seconds to wait, or `None` for no deadline
        :type timeout: object

        :return: No value is returned.
        :rtype: None
        """
        for j in self.futures:
            cur = time.time()
            j.join(timeout=timeout)
            if timeout is not None:
                timeout = timeout - (time.time() - cur)
                if timeout < 0:
                    raise TimeoutError(f"pool {self} timed out during join")

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
        if engine is None:
            if isinstance(name, str):
                def register(engine):
                    """
                    **LLM Docstring**

                    Decorator closure that registers the decorated engine class under the captured name.

                    :param engine: the execution-engine class or instance to register
                    :type engine: object

                    :return: decorator closure that registers the decorated engine class under the captured name.
                    :rtype: type[ExecutionEngine]
                    """
                    return cls.register(name, engine)
                return register
            elif isinstance(name, ExecutionEngine):
                engine = name
                return cls.register(engine.name, engine)
        else:
            cls.engine_types[name] = engine
        return engine
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
        return cls.engine_types[name](**opts)

    def __init__(self, **opts):
        """
        **LLM Docstring**

        Initialize context nesting depth and retain backend-specific construction options.

        :param opts: backend-specific construction or command options
        :type opts: object

        :return: No value is returned.
        :rtype: None
        """
        self._call_depth = 0
        self.opts = opts

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
        return ExecutionQueue([
            self.submit_job(**dict(job, **kwargs))
            for job in jobs
        ])

    def __enter__(self):
        """
        **LLM Docstring**

        Increase the context nesting depth and call `startup` only on the outermost entry.

        :return: No value is returned.
        :rtype: None
        """
        # here to be extended
        self._call_depth += 1
        if self._call_depth == 1:
            self.startup()

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
        self._call_depth -= 1
        if self._call_depth < 1:
            self.shutdown()

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
    def __init__(self,
                 watch_dir=None,
                 poll_time=None,
                 results_file=None,
                 status_file=None):
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
        super().__init__(poll_time=poll_time)
        self.watch_dir = watch_dir
        if results_file is None:
            results_file = self.results_file
        self.results_file = results_file
        if status_file is None:
            status_file = self.status_file
        self.status_file = status_file
    def get_result(self) -> dict:
        """
        **LLM Docstring**

        Read and decode the configured result JSON file from the watch directory or current path.

        :return: read and decode the configured result JSON file from the watch directory or current path.
        :rtype: dict
        """
        if self.watch_dir is None:
            results_file = self.results_file
        else:
            results_file = os.path.join(self.watch_dir, self.results_file)
        return dev.read_json(results_file)
    def get_status(self) -> ExecutionStatus:
        """
        **LLM Docstring**

        Read the configured status JSON file and convert its `status` field to `ExecutionStatus`; return `UNKNOWN` while the file is absent.

        :return: read the configured status JSON file and convert its `status` field to `ExecutionStatus`; return `UNKNOWN` while the file is absent.
        :rtype: ExecutionStatus
        """
        if self.watch_dir is None:
            status_file = self.status_file
        else:
            status_file = os.path.join(self.watch_dir, self.status_file)
        if os.path.isfile(status_file):
            stat_dict = dev.read_json(status_file)
            return ExecutionStatus(stat_dict.get('status', 'UNKNOWN'))
        else:
            return ExecutionStatus.UNKNOWN

class ManagedJobQueueExecutionFuture(FileBackedExecutionFuture):
    def __init__(self,
                 job_id,
                 queue_manager:queues.ManagedJobQueueHandler,
                 watch_dir=None,
                 results_file=None,
                 status_file=None,
                 poll_time=None):
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
        super().__init__(
            watch_dir=watch_dir, poll_time=poll_time,
            results_file=results_file,
            status_file=status_file
        )
        self.queue_manager = queue_manager
        self.job_id = job_id

    queue_status_map = {
        queues.ManagedJobQueueJobStatus.PENDING:ExecutionStatus.PENDING,
        queues.ManagedJobQueueJobStatus.COMPLETED:ExecutionStatus.COMPLETED,
        queues.ManagedJobQueueJobStatus.RUNNING:ExecutionStatus.RUNNING,
        queues.ManagedJobQueueJobStatus.ERROR:ExecutionStatus.ERROR,
    }
    def get_status(self) -> ExecutionStatus:
        """
        **LLM Docstring**

        Query the queue manager for the scheduler state and translate it through `queue_status_map`.

        :return: query the queue manager for the scheduler state and translate it through `queue_status_map`.
        :rtype: ExecutionStatus
        """
        return self.queue_status_map[
            self.queue_manager.get_job_status(self.job_id)
        ]

class ManagedJobQueueExecutionEngine(ExecutionEngine):
    future_type = ManagedJobQueueExecutionFuture
    def __init__(self, queue_manager:queues.ManagedJobQueueHandler, **opts):
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
        super().__init__(**opts)
        self.queue_manager = queue_manager

    def prep_future_opts(self,
                         watch_dir=None,
                         results_file=None,
                         status_file=None,
                         poll_time=None,
                         **kwargs):
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
        return dict(
            watch_dir=watch_dir,
            results_file=results_file,
            status_file=status_file,
            poll_time=poll_time
        ), kwargs

    def submit_job(self, *,
                   watch_dir=None, poll_time=None,
                   results_file=None,
                   status_file=None,
                   **kwargs) -> ManagedJobQueueExecutionFuture:
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
        #TODO: track output files
        fut_opts, job_opts = self.prep_future_opts(**kwargs)
        id = self.queue_manager.submit_job(**job_opts)
        return self.future_type(
            id,
            self.queue_manager,
            **fut_opts
        )

class SLURMExecutionFuture(ManagedJobQueueExecutionFuture):
    def get_status(self) -> ExecutionStatus:
        """
        **LLM Docstring**

        Query SLURM state, but interpret a previously visible running/completed/error job that has disappeared from the queue as completed.

        :return: query SLURM state, but interpret a previously visible running/completed/error job that has disappeared from the queue as completed.
        :rtype: ExecutionStatus
        """
        if self.status in {ExecutionStatus.RUNNING, ExecutionStatus.COMPLETED, ExecutionStatus.ERROR}:
            try:
                return super().get_status()
            except KeyError: # job no longer exists because it's done or errored
                return ExecutionStatus.COMPLETED
        else:
            return super().get_status()

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
        super().__init__(queues.SLURMHandler(), **opts)

    def prep_future_opts(self, *,
                         sbatch_file,
                         watch_dir=None,
                         chdir=None, **kwargs):
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
        if watch_dir is None:
            if chdir is None:
                watch_dir = os.path.dirname(sbatch_file)
            else:
                watch_dir = chdir

        return super().prep_future_opts(
            watch_dir=watch_dir,
            chdir=chdir,
            sbatch_file=sbatch_file,
            **kwargs
        )

    def submit_job(self,
                   sbatch_file,
                   *,
                   watch_dir=None, poll_time=None,
                   results_file=None,
                   status_file=None,
                   **kwargs) -> ManagedJobQueueExecutionFuture:
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
        #TODO: track output files
        fut_opts, job_opts = self.prep_future_opts(sbatch_file=sbatch_file, **kwargs)
        id, _ = self.queue_manager.submit_job(**job_opts)
        return self.future_type(
            id,
            self.queue_manager,
            **fut_opts
        )

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
        super().__init__(**ignored)
        self.obj = base_obj
        self._get_result = dev.default
    def await_result(self, timeout=None):
        """
        **LLM Docstring**

        Call the wrapped result object’s blocking `get` once and cache the returned value.

        :param timeout: maximum seconds to wait, or `None` for no deadline
        :type timeout: object

        :return: No value is returned.
        :rtype: None
        """
        if dev.is_default(self._get_result, allow_None=False):
            self._get_result = self.obj.get(timeout=timeout)
    def get_result(self):
        """
        **LLM Docstring**

        Return the cached asynchronous result, or `None` before it has been awaited.

        :return: return the cached asynchronous result, or `None` before it has been awaited.
        :rtype: object | None
        """
        if dev.is_default(self._get_result):
            return None
        else:
            return self._get_result
    def get_status(self) -> ExecutionStatus:
        """
        **LLM Docstring**

        Use the wrapped result’s `successful` method to distinguish running, completed, and failed states.

        :return: use the wrapped result’s `successful` method to distinguish running, completed, and failed states.
        :rtype: ExecutionStatus
        """
        try:
            res = self.obj.successful()
        except (ValueError, AssertionError):
            return ExecutionStatus.RUNNING
        else:
            if res:
                return ExecutionStatus.COMPLETED
            else:
                return ExecutionStatus.ERROR

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
        super().__init__(**opts)
        self.proc_gen = proc_gen

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
        # TODO: track output files
        proc = self.proc_gen.apply_async(method, **kwargs)
        return self.future_type(
            proc
        )

    def startup(self):
        """
        **LLM Docstring**

        Enter the process-generator context when the engine becomes active.

        :return: No value is returned.
        :rtype: None
        """
        self.proc_gen.__enter__()

    def shutdown(self):
        """
        **LLM Docstring**

        Exit the process-generator context when the engine is deactivated.

        :return: No value is returned.
        :rtype: None
        """
        self.proc_gen.__exit__()