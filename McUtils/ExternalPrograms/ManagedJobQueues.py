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

__all__ = [
    "ManagedJobQueueJobStatus",
    "ManagedJobQueueSubmissionHandler",
    "ManagedJobQueueInformationHandler",
    "ManagedJobQueueHandler",
    "SLURMInformationHandler",
    "SLURMSubmissionHandler",
    "SLURMHandler",
    "serialize_python_job",
    "sbatch_python_job"
]

class ManagedJobQueueJobStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"

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
        return "--" + key.replace('_', '-')

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
        #TODO: use `shlex` for this instead
        return list(itertools.chain(*[
            (
                [cls.map_option_name(k)]
                    if v is True else
                []
                    if v is False else
                [cls.map_option_name(k), v]
            )
            for k, v in kwargs.items()
            if v is not None
        ]))

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
        start_command = cls.START_JOB_COMMAND
        if isinstance(start_command, str):
            start_command = [start_command]
        opts = cls.format_job_args(**opts)
        return start_command + opts + list(args)

    @classmethod
    @abc.abstractmethod
    def parse_job_id(cls, res:str):
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
        return (), kwargs
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
        args, kwargs = cls.prep_job_kwargs(**opts)
        cmd = cls.get_job_command(*args, **kwargs)
        res = subprocess.run(cmd, text=True, capture_output=True)
        if len(res.stderr) > 0 or res.returncode != 0:
            raise OSError(res.returncode, res.stderr)
        return cls.parse_job_id(res.stdout), res

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
        return cls.JOB_INFO_COMMAND

    @classmethod
    def run_job_info_cmd(self):
        """
        **LLM Docstring**

        Run the scheduler information command with captured text output and raise `IOError` on stderr or a nonzero return code.

        :return: run the scheduler information command with captured text output and raise `IOError` on stderr or a nonzero return code.
        :rtype: subprocess.CompletedProcess
        """
        cmd = self.get_job_info_command()
        res = subprocess.run(cmd, text=True, capture_output=True)
        if len(res.stderr) > 0 or res.returncode != 0:
            raise IOError(res.returncode, res.stderr)
        return res

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
        s = s.strip()
        if cls._states_map is None:
            cls._states_map = {}
            for state_names, enum_state in cls.STATES_MAP:
                for sn in state_names:
                    cls._states_map[sn] = enum_state
        if k == "state":
            s = cls._states_map.get(s, s)
        return s

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
        base_info = cls.parse_raw_job_info(stdout)
        return [
            {
                k: cls._clean_job_info(k, s)
                for k, s in info.items()
            }
            for info in base_info
        ]

    @classmethod
    def get_all_job_info(cls):
        """
        **LLM Docstring**

        Run the scheduler query and index the parsed job records by their `id` field.

        :return: run the scheduler query and index the parsed job records by their `id` field.
        :rtype: dict
        """
        res = cls.run_job_info_cmd()
        parsed_info = cls.parse_job_info(res.stdout)
        return {
            data['id']:data
            for data in parsed_info
        }

class ManagedJobQueueHandler:
    name: str
    #TODO: add caching with an update interval
    def __init__(self,
                 information_handler:ManagedJobQueueInformationHandler,
                 submission_handler:ManagedJobQueueSubmissionHandler):
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
        self.info_handler = information_handler
        self.submission_handler = submission_handler

    def get_job_info(self):
        """
        **LLM Docstring**

        Return all current job records from the information handler.

        :return: return all current job records from the information handler.
        :rtype: dict
        """
        return self.info_handler.get_all_job_info()

    def get_job_status(self, job_id):
        """
        **LLM Docstring**

        Look up a job record and return its `status` field.

        :param job_id: the scheduler-assigned job identifier
        :type job_id: object

        :return: look up a job record and return its `status` field.
        :rtype: ManagedJobQueueJobStatus
        """
        base_info = self.get_job_info()[job_id]
        return base_info['status']

    def submit_job(self, **kwargs):
        """
        **LLM Docstring**

        Forward scheduler options to the submission handler and return its submission result.

        :param kwargs: scheduler, backend, or function keyword arguments
        :type kwargs: object

        :return: forward scheduler options to the submission handler and return its submission result.
        :rtype: tuple
        """
        return self.submission_handler.create_job_process(**kwargs)

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
        base_args, base_kwargs = super().prep_job_kwargs(**etc)
        return (sbatch_file,) + base_args, base_kwargs

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
        return re.match(r'Submitted batch job (\d+)', res).group(1)

class SLURMInformationHandler(ManagedJobQueueInformationHandler):
    STATES_MAP = [
        [["CONFIGURING", "COMPLETING", "PENDING", "RUNNING", "RESIZING", "SUSPENDED"], ManagedJobQueueJobStatus.RUNNING],
        [["CANCELLED", "FAILED", "TIMEOUT", "PREEMPTED", "NODE_FAIL"], ManagedJobQueueJobStatus.ERROR],
        [["COMPLETED"], ManagedJobQueueJobStatus.COMPLETED]
    ]

    FMT_SPECS = [
        (12, "i", "jobid", "id"),
        (100, "j", "jobname", "name"),
        (25, "S", "start", "start"),
        (100, "P", "partition", "partition"),
        (20, "q", "qos", "qos"),
        (20, "T", "state", "state")
    ]
    FMT_SQUEUE_KEYS = []
    SQUEUE_CMD = ["squeue", "--noheader",
                  '--format="{}"'.format(''.join(f"%.{l}{k}" for l, k, n, y in FMT_SPECS))
                  ]
    SACCT_CMD = ['sacct', '--noheader',
                 '--format="{}"'.format(','.join(f"{k}%{l}" for l, k, n, y in FMT_SPECS))
                 ]

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
        return (sbatch_script,), kwargs

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
        if sacct_error:
            base_cmd = cls.SQUEUE_CMD
        else:
            base_cmd = cls.SACCT_CMD
        return base_cmd + ['--user={username}'.format(username=getpass.getuser())]

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
        acc = np.cumsum([1] + [l for l, _, _, _ in cls.FMT_SPECS])
        splits = {
            k: [a, b]
            for (_, _, _, k), a, b in zip(cls.FMT_SPECS, acc[:-1], acc[1:])
        }
        return [
            {
                k: line[a:b]
                for k, (a, b) in splits.items()
            }
            for line in stdout.splitlines()
        ]

    @classmethod
    def run_job_info_cmd(self):
        """
        **LLM Docstring**

        Run the normal SLURM accounting query and fall back to `squeue` when the first command fails.

        :return: run the normal SLURM accounting query and fall back to `squeue` when the first command fails.
        :rtype: subprocess.CompletedProcess
        """
        try:
            res = super().run_job_info_cmd()
        except (IOError, subprocess.CalledProcessError):
            # TODO: check that error really was what we expected
            cmd = self.get_job_info_command(sacct_error=True)
            res = subprocess.run(cmd, text=True, capture_output=True)
            if len(res.stderr) > 0 or res.returncode != 0:
                raise IOError(res.returncode, res.stderr)
        return res

class SLURMHandler(ManagedJobQueueHandler):
    name = "slurm"
    def __init__(self):
        """
        **LLM Docstring**

        Construct the combined SLURM queue handler from its information and submission components.

        :return: No value is returned.
        :rtype: None
        """
        super().__init__(
            SLURMInformationHandler(),
            SLURMSubmissionHandler()
        )

    def get_job_status(self, job_id):
        """
        **LLM Docstring**

        Return the normalized `state` field for a SLURM job record.

        :param job_id: the scheduler-assigned job identifier
        :type job_id: object

        :return: return the normalized `state` field for a SLURM job record.
        :rtype: ManagedJobQueueJobStatus
        """
        base_info = self.get_job_info()[job_id]
        return base_info['state']

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
    subprocess.call(["sbatch", script],
                    **sbatch_kwargs)

def serialize_python_job(func, *args,
                         serializer='json', deserializer=None,
                         serialization_mode=None,
                         template='run_sbatch_python.py',
                         path_modifications=None,
                         script_file='run_{job_name}_{id}.py',
                         job_name=None,
                         id=None,
                         state_string=None,
                         post_processor="print",
                         cleanup=False,
                         function_args=None,
                         function_kwargs=None,
                         **kwargs):
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
    if job_name is None:
        job_name = func.__name__

    if isinstance(serializer, str):
        serializer = BaseSerializer.construct(serializer)

    if hasattr(serializer, 'registry_name'):
        if deserializer is None:
            deserializer = serializer.registry_name
        if serialization_mode is None:
            serialization_mode = 'mcutils'
    else:
        if serialization_mode is None:
            serialization_mode = 'function'
    if serialization_mode == 'function':
        if deserializer is None:
            raise ValueError("explicit deserializer function required")

    if state_string is None:
        if function_kwargs is None:
            function_kwargs = {}
        function_kwargs = kwargs | function_kwargs
        if function_args is None:
            function_args = args

        arg_dict = {
            'args': function_args,
            'kwargs': function_kwargs
        }

        if hasattr(serializer, 'dumps'):
            state_string = serializer.dumps(arg_dict)
        else:
            state_string = serializer(arg_dict)

    if path_modifications is None:
        path_modifications = []

    func = base64.b64encode(pickle.dumps(func)).decode()
    if not isinstance(post_processor, str):
        post_processor = base64.b64encode(pickle.dumps(post_processor)).decode()
    replacements = {
        'path_modifications':",".join(path_modifications),
        'serialization_mode':serialization_mode,
        'state':state_string,
        'deserializer':deserializer,
        'func':func,
        "post_processor":post_processor,
        "cleanup":str(cleanup)
    }

    if os.path.isfile(template):
        template = dev.read_file(template)
    else:
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", template)
        if os.path.isfile(test_file):
            template = dev.read_file(test_file)

    for k, v in replacements.items():
        template = template.replace(f'`{k}`', v)

    if id is None:
        id = dev.string_hash(json.dumps(replacements), bits=None, base=None)
    script_file = script_file.format(
        job_name=job_name,
        id=id
    )
    return dev.FileBackedIO(template, file=script_file)

python_sbatch_template = """
INPUT_FILE="${{SLURM_JOB_NAME%.*}}.py"

if [ -n "$ENVIRONMENT_SCRIPT_PATH" ]; then
    source "$ENVIRONMENT_SCRIPT_PATH"
fi

if [ -z "$SBATCH_SCRIPT_PATH" ]; 
    then
        if [ -z "$CONTAINER_PATH" ]; 
            then
                curdir="$PWD"
                . ~/.bashrc
                cd "$curdir"
                if [ -n "$CONDA_ENVIRONMENT" ]; then
                  conda activate $CONDA_ENVIRONMENT
                fi
                if [ -n "$VENV_PATH" ]; then
                  source $VENV_PATH/bin/activate
                fi
                python -u $INPUT_FILE $@
            else
                env=none
                if [ -n "$CONDA_ENVIRONMENT" ]; then
                  env="$CONDA_ENVIRONMENT"
                fi
                if [ -n "$VENV_PATH" ]; then
                  env="$VENV_PATH"
                fi
                singularity run $CONTAINER_ARGS "$CONTAINER_PATH" --env="$env" python -u $INPUT_FILE $@
        fi
    else
        source "$SBATCH_SCRIPT_PATH"
fi
"""
def get_active_environment():
    """
    **LLM Docstring**

    Collect active Conda, virtual-environment, Singularity, container-argument, and environment-script settings from process environment variables.

    :return: collect active Conda, virtual-environment, Singularity, container-argument, and environment-script settings from process environment variables.
    :rtype: dict[str, str]
    """
    env = {}
    if conda := os.environ.get("CONDA_DEFAULT_ENV"):
        env["CONDA_ENVIRONMENT"] = conda
    if venv := os.environ.get("VIRTUAL_ENV"):
        env["VIRTUAL_ENV"] = venv
    if container := os.environ.get("SINGULARITY_CONTAINER"):
        env["CONTAINER_PATH"] = container
    if args := os.environ.get("CONTAINER_ARGS"):
        env["CONTAINER_ARGS"] = args
    if envscript := os.environ.get("ENVIRONMENT_SCRIPT_PATH"):
        env["ENVIRONMENT_SCRIPT_PATH"] = envscript
    return env
python_sbatch_defaults = {
    'ntasks':1,
    'ntasks_per_node':1,
    'mem':'5G',
    'time':'8:00:00'
}
def sbatch_python_job(
        func,
        *args,
        sbatch_kwargs=None,
        job_name=None,
        id=None,
        script=None,
        environment=None,
        cleanup=False,
        post_processor='print',
        **kwargs
):
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
    if sbatch_kwargs is None:
        sbatch_kwargs = {}
        for k in SBatchJob.slurm_keys:
            val = kwargs.pop(k.replace("-", "_"), None)
            if val is not None:
                sbatch_kwargs[k] = val

    sbatch_kwargs = python_sbatch_defaults | sbatch_kwargs

    script_file = serialize_python_job(
        func,
        job_name=job_name,
        id=id,
        cleanup=cleanup,
        function_args=args,
        function_kwargs=kwargs,
        post_processor=post_processor
    )

    sbatch_kwargs['job_name'] = dev.filename(script_file.name)

    env_vars = get_active_environment()
    if len(env_vars) > 0:
        if environment is None:
            environment = {}
        environment = env_vars | environment

    def precall():
        """
        **LLM Docstring**

        Write the generated Python script immediately before the associated sbatch job starts.

        :return: No value is returned.
        :rtype: None
        """
        script_file.write()

    if script is None:
        script = python_sbatch_template
    script = script.format(python_file=script_file.name)
    return SBatchJob(precall=precall, steps=script,
                     environment=environment,
                     **sbatch_kwargs), script_file