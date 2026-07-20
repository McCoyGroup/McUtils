"""
A job management package to make it easier to instantiate
job
"""
import time, datetime, os, shutil
from .Persistence import PersistenceManager
from .Checkpointing import JSONCheckpointer
from .Logging import Logger, NullLogger
from ..Parallelizers import Parallelizer
__all__ = ['Job', 'JobManager']

class Job:
    """
    A job object to support simplified run scripting.
    Provides a `job_data` checkpoint file that stores basic
    data about job runtime and stuff, as well as a `logger` that
    makes it easy to plug into a run time that supports logging
    """
    default_job_file = 'job_data.json'
    default_log_file = 'log.txt'

    def __init__(self, job_dir, job_file=None, logger=None, parallelizer=None, job_parameters=None):
        """
        **LLM Docstring**

        Initialize a job directory, checkpoint, logger, optional parallelizer, and parameter payload.

        :param job_dir: job working directory
        :type job_dir: object
        :param job_file: checkpoint filename or path
        :type job_file: object
        :param logger: logger specification or instance
        :type logger: object
        :param parallelizer: parallelizer specification or instance
        :type parallelizer: object
        :param job_parameters: job parameter mapping written to the checkpoint
        :type job_parameters: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    @classmethod
    def from_config(cls, config_location=None, job_file=None, logger=None, parallelizer=None, job_parameters=None):
        """
        **LLM Docstring**

        Construct a job from configuration-compatible keyword arguments, using `config_location` as its directory.

        :param config_location: directory supplied by configuration persistence
        :type config_location: object
        :param job_file: checkpoint filename or path
        :type job_file: object
        :param logger: logger specification or instance
        :type logger: object
        :param parallelizer: parallelizer specification or instance
        :type parallelizer: object
        :param job_parameters: job parameter mapping written to the checkpoint
        :type job_parameters: object
        :return: The newly constructed object.
        :rtype: object
        """
        ...

    def load_checkpoint(self, job_file):
        """
        Loads the checkpoint we'll use to dump params

        :param job_file:
        :type job_file:
        :return:
        :rtype:
        """
        ...

    def load_logger(self, log_spec):
        """
        Loads the appropriate logger

        :param log_spec:
        :type log_spec: str | dict
        :return:
        :rtype:
        """
        ...

    def load_parallelizer(self, par_spec):
        """
        Loads the appropriate parallelizer.
        If something other than a dict is passed,
        tries out multiple specs sequentially until it finds one that works

        :param log_spec:
        :type log_spec: dict
        :return:
        :rtype:
        """
        ...

    def path(self, *parts):
        """
        :param parts:
        :type parts: str
        :return:
        :rtype:
        """
        ...

    @property
    def working_directory(self):
        """
        **LLM Docstring**

        Resolve a configured working directory relative to the job directory without permanently changing the process directory.

        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Enter the job directory, open checkpointing and parallelism contexts, and record start metadata and parameters.

        :return: The active context object.
        :rtype: object
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Restore the original directory, store elapsed runtime, and close checkpoint and parallelizer contexts.

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

class JobManager(PersistenceManager):
    """
    A class to manage job instances.
    Thin layer on a `PersistenceManager`
    """
    default_job_type = Job

    def __init__(self, job_dir, job_type=None):
        """
        **LLM Docstring**

        Bind a persistence manager to a job directory and the selected job class.

        :param job_dir: job working directory
        :type job_dir: object
        :param job_type: concrete `Job` subclass to construct, or `None` for the default
        :type job_type: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def job(self, name, timestamp=False, **kw):
        """
        Returns a loaded or new job with the given name and settings

        :param name:
        :type name: str
        :param timestamp:
        :type timestamp:
        :param kw:
        :type kw:
        :return:
        :rtype: Job
        """
        ...

    @classmethod
    def job_from_folder(cls, folder, job_type=None, make_config=True, **opts):
        """
        A special case convenience function that goes
        directly to starting a job from a folder

        :return:
        :rtype: Job
        """
        ...

    @classmethod
    def current_job(cls, job_type=None, make_config=True, **opts):
        """
        A special case convenience function that starts a
        JobManager one directory up from the current
        working directory and intializes a job from the
        current working directory

        :return:
        :rtype: Job
        """
        ...