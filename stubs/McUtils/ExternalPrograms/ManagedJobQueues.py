import abc
import argparse
import json
import os.path
import re
import subprocess
import enum
import itertools
import uuid
import numpy as np
import getpass
import pickle
import base64
from ..Scaffolding import BaseSerializer
from .. import Devutils as dev
from .Jobs import SBatchJob
__all__ = ['ManagedJobQueueJobStatus', 'ManagedJobQueueSubmissionHandler', 'ManagedJobQueueInformationHandler', 'ManagedJobQueueHandler', 'SLURMInformationHandler', 'SLURMSubmissionHandler', 'SLURMHandler', 'serialize_python_job', 'sbatch_python_job']

class ManagedJobQueueJobStatus(enum.Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    ERROR = 'error'

class ManagedJobQueueSubmissionHandler(metaclass=abc.ABCMeta):
    START_JOB_COMMAND: str

    @classmethod
    def map_option_name(cls, key):
        """
        **LLM Docstring**

        Convert a Python-style option name to a GNU-style `--kebab-case` command-line flag.

        :param key: an option or record field name
        :type key: object

        :return: convert a Python-style option name to a GNU-style `--kebab-case` command-line flag.
        :rtype: str
        """
        ...

    @classmethod
    def format_job_args(cls, **kwargs) -> 'list[str]':
        """
        **LLM Docstring**

        Flatten keyword options into command-line arguments: true emits a flag, false omits it, and other non-`None` values emit a flag/value pair.

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: flatten keyword options into command-line arguments: true emits a flag, false omits it, and other non-`None` values emit a flag/value pair.
        :rtype: list[str]
        """
        ...

    @classmethod
    def get_job_command(cls, *args, **opts) -> 'list[str]':
        """
        **LLM Docstring**

        Assemble the queue submission command from the configured executable, formatted options, and positional arguments.

        :param args: positional command or function arguments
        :type args: object

        :param opts: backend-specific construction or command options
        :type opts: object

        :return: assemble the queue submission command from the configured executable, formatted options, and positional arguments.
        :rtype: list[str]
        """
        ...

    @classmethod
    @abc.abstractmethod
    def parse_job_id(cls, res: str):
        """
        **LLM Docstring**

        Abstract parser for extracting a scheduler job identifier from submission stdout.

        :param res: captured scheduler response text
        :type res: str

        :return: abstract parser for extracting a scheduler job identifier from submission stdout.
        :rtype: str
        """
        ...

    @classmethod
    def prep_job_kwargs(cls, **kwargs):
        """
        **LLM Docstring**

        Default submission hook that contributes no positional arguments and passes keyword arguments through unchanged.

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: default submission hook that contributes no positional arguments and passes keyword arguments through unchanged.
        :rtype: tuple[tuple, dict]
        """
        ...

    @classmethod
    def create_job_process(cls, **opts) -> 'tuple[str, _]':
        """
        **LLM Docstring**

        Prepare and run the scheduler submission command, reject nonzero or stderr-producing executions, and parse the resulting job id.

        :param opts: backend-specific construction or command options
        :type opts: object

        :return: prepare and run the scheduler submission command, reject nonzero or stderr-producing executions, and parse the resulting job id.
        :rtype: tuple[str, subprocess.CompletedProcess]
        """
        ...

class ManagedJobQueueInformationHandler(metaclass=abc.ABCMeta):
    JOB_INFO_COMMAND: str

    @classmethod
    def get_job_info_command(cls):
        """
        **LLM Docstring**

        Return the command specification used to query scheduler job information.

        :return: return the command specification used to query scheduler job information.
        :rtype: str | list[str]
        """
        ...

    @classmethod
    def run_job_info_cmd(self):
        """
        **LLM Docstring**

        Run the scheduler information command with captured text output and raise `IOError` on stderr or a nonzero return code.

        :return: run the scheduler information command with captured text output and raise `IOError` on stderr or a nonzero return code.
        :rtype: subprocess.CompletedProcess
        """
        ...

    @classmethod
    @abc.abstractmethod
    def parse_raw_job_info(cls, stdout) -> 'list[dict]':
        """
        **LLM Docstring**

        Abstract parser that converts scheduler stdout into raw per-job dictionaries.

        :param stdout: captured scheduler standard output
        :type stdout: object

        :return: abstract parser that converts scheduler stdout into raw per-job dictionaries.
        :rtype: list[dict]
        """
        ...
    STATES_MAP: tuple[list[list[str]], ManagedJobQueueJobStatus]
    _states_map = None

    @classmethod
    def _clean_job_info(cls, k, s):
        """
        **LLM Docstring**

        Strip one parsed field and lazily translate scheduler state names to `ManagedJobQueueJobStatus` values when the field key is `state`.

        :param k: the parsed field name
        :type k: object

        :param s: the parsed field value
        :type s: object

        :return: strip one parsed field and lazily translate scheduler state names to `ManagedJobQueueJobStatus` values when the field key is `state`.
        :rtype: object
        """
        ...

    @classmethod
    def parse_job_info(cls, stdout) -> 'list[dict]':
        """
        **LLM Docstring**

        Clean every field of every raw scheduler record, including state normalization.

        :param stdout: captured scheduler standard output
        :type stdout: object

        :return: clean every field of every raw scheduler record, including state normalization.
        :rtype: list[dict]
        """
        ...

    @classmethod
    def get_all_job_info(cls):
        """
        **LLM Docstring**

        Run the scheduler query and index the parsed job records by their `id` field.

        :return: run the scheduler query and index the parsed job records by their `id` field.
        :rtype: dict
        """
        ...

class ManagedJobQueueHandler:
    name: str

    def __init__(self, information_handler: ManagedJobQueueInformationHandler, submission_handler: ManagedJobQueueSubmissionHandler):
        """
        **LLM Docstring**

        Combine independent scheduler information and submission handlers behind one queue interface.

        :param information_handler: the component that queries scheduler state
        :type information_handler: ManagedJobQueueInformationHandler

        :param submission_handler: the component that submits jobs
        :type submission_handler: ManagedJobQueueSubmissionHandler

        :return: No value is returned.
        :rtype: None
        """
        ...

    def get_job_info(self):
        """
        **LLM Docstring**

        Return all current job records from the information handler.

        :return: return all current job records from the information handler.
        :rtype: dict
        """
        ...

    def get_job_status(self, job_id):
        """
        **LLM Docstring**

        Look up a job record and return its `status` field.

        :param job_id: the scheduler-assigned job identifier
        :type job_id: object

        :return: look up a job record and return its `status` field.
        :rtype: ManagedJobQueueJobStatus
        """
        ...

    def submit_job(self, **kwargs):
        """
        **LLM Docstring**

        Forward scheduler options to the submission handler and return its submission result.

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: forward scheduler options to the submission handler and return its submission result.
        :rtype: tuple
        """
        ...

class SLURMSubmissionHandler(ManagedJobQueueSubmissionHandler):
    START_JOB_COMMAND = ['sbatch']

    @classmethod
    def prep_job_kwargs(cls, *, sbatch_file, **etc):
        """
        **LLM Docstring**

        Move `sbatch_file` into the positional argument list expected by `sbatch`.

        :param sbatch_file: path to the sbatch script
        :type sbatch_file: object

        :param etc: additional scheduler options
        :type etc: object

        :return: move `sbatch_file` into the positional argument list expected by `sbatch`.
        :rtype: tuple[tuple, dict]
        """
        ...

    @classmethod
    def parse_job_id(self, res: str):
        """
        **LLM Docstring**

        Extract the numeric job id from SLURM’s `Submitted batch job N` response.

        :param res: captured scheduler response text
        :type res: str

        :return: extract the numeric job id from SLURM’s `Submitted batch job N` response.
        :rtype: str
        """
        ...

class SLURMInformationHandler(ManagedJobQueueInformationHandler):
    FMT_SQUEUE_KEYS = []
    SQUEUE_CMD = ['squeue', '--noheader', '--format="{}"'.format(''.join((f'%.{l}{k}' for l, k, n, y in FMT_SPECS)))]
    SACCT_CMD = ['sacct', '--noheader', '--format="{}"'.format(','.join((f'{k}%{l}' for l, k, n, y in FMT_SPECS)))]

    @classmethod
    def prep_job_kwargs(cls, *, sbatch_script, **kwargs):
        """
        **LLM Docstring**

        Return an sbatch script as the sole positional argument and preserve the remaining keyword options.

        :param sbatch_script: the SLURM batch script path
        :type sbatch_script: object

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: return an sbatch script as the sole positional argument and preserve the remaining keyword options.
        :rtype: tuple[tuple, dict]
        """
        ...

    @classmethod
    def get_job_info_command(cls, sacct_error=False):
        """
        **LLM Docstring**

        Build a user-scoped `sacct` query, or an `squeue` fallback command when `sacct_error` is true.

        :param sacct_error: whether to use the `squeue` fallback instead of `sacct`
        :type sacct_error: object

        :return: build a user-scoped `sacct` query, or an `squeue` fallback command when `sacct_error` is true.
        :rtype: list[str]
        """
        ...

    @classmethod
    def parse_raw_job_info(cls, stdout) -> 'list[dict]':
        """
        **LLM Docstring**

        Slice fixed-width SLURM output lines according to `FMT_SPECS` and return one dictionary per line.

        :param stdout: captured scheduler standard output
        :type stdout: object

        :return: slice fixed-width SLURM output lines according to `FMT_SPECS` and return one dictionary per line.
        :rtype: list[dict]
        """
        ...

    @classmethod
    def run_job_info_cmd(self):
        """
        **LLM Docstring**

        Run the normal SLURM accounting query and fall back to `squeue` when the first command fails.

        :return: run the normal SLURM accounting query and fall back to `squeue` when the first command fails.
        :rtype: subprocess.CompletedProcess
        """
        ...

class SLURMHandler(ManagedJobQueueHandler):
    name = 'slurm'

    def __init__(self):
        """
        **LLM Docstring**

        Construct the combined SLURM queue handler from its information and submission components.

        :return: No value is returned.
        :rtype: None
        """
        ...

    def get_job_status(self, job_id):
        """
        **LLM Docstring**

        Return the normalized `state` field for a SLURM job record.

        :param job_id: the scheduler-assigned job identifier
        :type job_id: object

        :return: return the normalized `state` field for a SLURM job record.
        :rtype: ManagedJobQueueJobStatus
        """
        ...

def sbatch_python_script(script, chdir=None, **sbatch_kwargs):
    """
    **LLM Docstring**

    Submit an existing script with `sbatch`; the `chdir` parameter is currently unused.

    :param script: the shell script or script path to submit
    :type script: object

    :param chdir: scheduler working-directory option
    :type chdir: object

    :param sbatch_kwargs: SLURM options, using underscore or native key spellings as accepted by the caller
    :type sbatch_kwargs: object

    :return: No value is returned.
    :rtype: None
    """
    ...

def serialize_python_job(func, *args, serializer='json', deserializer=None, serialization_mode=None, template='run_sbatch_python.py', path_modifications=None, script_file='run_{job_name}_{id}.py', job_name=None, id=None, state_string=None, post_processor='print', cleanup=False, function_args=None, function_kwargs=None, **kwargs):
    """
    **LLM Docstring**

    Serialize function arguments, pickle and base64-encode the callable and optional post-processor, substitute them into a Python runner template, and return a `FileBackedIO` for the generated script.

    :param func: the Python callable executed by the generated runner
    :type func: object

    :param serializer: serializer instance, registered serializer name, or callable
    :type serializer: object

    :param deserializer: deserializer name or callable embedded in the generated script
    :type deserializer: object

    :param serialization_mode: whether generated code uses McUtils serializer dispatch or an explicit function
    :type serialization_mode: object

    :param template: runner-template text or template filename
    :type template: object

    :param path_modifications: paths inserted into the generated runner’s import search path
    :type path_modifications: object

    :param script_file: format string for the generated Python filename
    :type script_file: object

    :param job_name: scheduler-visible job name
    :type job_name: object

    :param id: explicit generated-script identifier
    :type id: object

    :param state_string: pre-serialized argument state
    :type state_string: object

    :param post_processor: callable or named post-processing expression for the result
    :type post_processor: object

    :param cleanup: whether the generated runner removes its files after execution
    :type cleanup: object

    :param function_args: explicit positional arguments to serialize
    :type function_args: object

    :param function_kwargs: explicit keyword arguments to serialize
    :type function_kwargs: object

    :param args: positional command or function arguments
    :type args: object

    :param kwargs: scheduler, backend, or function keyword arguments
    :type kwargs: object

    :return: serialize function arguments, pickle and base64-encode the callable and optional post-processor, substitute them into a Python runner template, and return a `FileBackedIO` for the generated script.
    :rtype: dev.FileBackedIO
    """
    ...
'python_sbatch_template data omitted from this build (a single str value)'

def get_active_environment():
    """
    **LLM Docstring**

    Collect active Conda, virtual-environment, Singularity, container-argument, and environment-script settings from process environment variables.

    :return: collect active Conda, virtual-environment, Singularity, container-argument, and environment-script settings from process environment variables.
    :rtype: dict[str, str]
    """
    ...
python_sbatch_defaults = {'ntasks': 1, 'ntasks_per_node': 1, 'mem': '5G', 'time': '8:00:00'}

def sbatch_python_job(func, *args, sbatch_kwargs=None, job_name=None, id=None, script=None, environment=None, cleanup=False, post_processor='print', **kwargs):
    """
    **LLM Docstring**

    Build a generated Python runner and an `SBatchJob`, merging SLURM defaults, propagating the active environment, and installing a pre-call hook that writes the generated script.

    :param func: the Python callable executed by the generated runner
    :type func: object

    :param sbatch_kwargs: SLURM options, using underscore or native key spellings as accepted by the caller
    :type sbatch_kwargs: object

    :param job_name: scheduler-visible job name
    :type job_name: object

    :param id: explicit generated-script identifier
    :type id: object

    :param script: the shell script or script path to submit
    :type script: object

    :param environment: environment values exported by the generated batch job
    :type environment: object

    :param cleanup: whether the generated runner removes its files after execution
    :type cleanup: object

    :param post_processor: callable or named post-processing expression for the result
    :type post_processor: object

    :param args: positional command or function arguments
    :type args: object

    :param kwargs: scheduler, backend, or function keyword arguments
    :type kwargs: object

    :return: build a generated Python runner and an `SBatchJob`, merging SLURM defaults, propagating the active environment, and installing a pre-call hook that writes the generated script.
    :rtype: tuple[SBatchJob, dev.FileBackedIO]
    """
    ...