import abc
import argparse
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

__all__ = [
    "ManagedJobQueueJobStatus",
    "ManagedJobQueueSubmissionHandler",
    "ManagedJobQueueInformationHandler",
    "ManagedJobQueueHandler",
    "SLURMInformationHandler",
    "SLURMSubmissionHandler",
    "SLURMHandler",
    "prep_sbatch_python"
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
        return "--" + key.replace('_', '-')

    @classmethod
    def format_job_args(cls, **kwargs) -> 'list[str]':
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
        start_command = cls.START_JOB_COMMAND
        if isinstance(start_command, str):
            start_command = [start_command]
        opts = cls.format_job_args(**opts)
        return start_command + opts + list(args)

    @classmethod
    @abc.abstractmethod
    def parse_job_id(cls, res:str):
        ...

    @classmethod
    def prep_job_kwargs(cls, **kwargs):
        return (), kwargs
    @classmethod
    def create_job_process(cls, **opts) -> 'tuple[str, _]':
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
        return cls.JOB_INFO_COMMAND

    @classmethod
    def run_job_info_cmd(self):
        cmd = self.get_job_info_command()
        res = subprocess.run(cmd, text=True, capture_output=True)
        if len(res.stderr) > 0 or res.returncode != 0:
            raise IOError(res.returncode, res.stderr)
        return res

    @classmethod
    @abc.abstractmethod
    def parse_raw_job_info(cls, stdout) -> 'list[dict]':
        ...

    STATES_MAP: tuple[list[list[str]], ManagedJobQueueJobStatus]
    _states_map = None
    @classmethod
    def _clean_job_info(cls, k, s):
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
        self.info_handler = information_handler
        self.submission_handler = submission_handler

    def get_job_info(self):
        return self.info_handler.get_all_job_info()

    def get_job_status(self, job_id):
        base_info = self.get_job_info()[job_id]
        return base_info['status']

    def submit_job(self, **kwargs):
        return self.submission_handler.create_job_process(**kwargs)

class SLURMSubmissionHandler(ManagedJobQueueSubmissionHandler):
    START_JOB_COMMAND = ['sbatch']

    @classmethod
    def prep_job_kwargs(cls, *, sbatch_file, **etc):
        base_args, base_kwargs = super().prep_job_kwargs(**etc)
        return (sbatch_file,) + base_args, base_kwargs

    @classmethod
    def parse_job_id(self, res: str):
        return re.match('Submitted batch job (\d+)', res).group(1)

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
        return (sbatch_script,), kwargs

    @classmethod
    def get_job_info_command(cls, sacct_error=False):
        if sacct_error:
            base_cmd = cls.SQUEUE_CMD
        else:
            base_cmd = cls.SACCT_CMD
        return base_cmd + ['--user={username}'.format(username=getpass.getuser())]

    @classmethod
    def parse_raw_job_info(cls, stdout) -> 'list[dict]':
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
        super().__init__(
            SLURMInformationHandler(),
            SLURMSubmissionHandler()
        )

    def get_job_status(self, job_id):
        base_info = self.get_job_info()[job_id]
        return base_info['state']

def sbatch_python_script(script, chdir=None, **sbatch_kwargs):
    subprocess.call(["sbatch", script],
                    **sbatch_kwargs)

def prep_sbatch_python(func, *args, sbatch_kwargs=None,
                       serializer='json', deserializer=None,
                       serialization_mode=None,
                       template='run_sbatch_python.py',
                       path_modifications=None,
                       script_file='run_{job_name}_{id}.py',
                       id=None,
                       state_string=None,
                       post_processor="print",
                       function_args=None,
                       function_kwargs=None,
                       **kwargs):
    if sbatch_kwargs is None:
        sbatch_kwargs = {}
    if 'job_name' not in sbatch_kwargs:
        sbatch_kwargs['job_name'] = func.__name__

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
        'path_modifications':repr(path_modifications),
        'serialization_mode':serialization_mode,
        'state':state_string,
        'deserializer':deserializer,
        'func':func,
        "post_processor":post_processor
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
        id = str(uuid.uuid4())[:8]
    script_file = script_file.format(
        job_name=sbatch_kwargs.get('job_name'),
        id=id
    )
    dev.write_file(script_file, template)
    return script_file