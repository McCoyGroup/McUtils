"""
Support for turning an `ExternalProgramJob` into something an `ExecutionEngine` can run:
a `JobSubmission` (input file + run script + how to call the program) and an
`ExternalProgramFuture` (a handle that knows how to find and parse the job's results).
"""

import os
import shlex
import stat

from ..ExecutionEngine import ExecutionFuture, ExecutionStatus

__all__ = [
    "JobSubmission",
    "ExternalProgramFuture"
]


class JobSubmission:
    """
    Everything needed to run one job: the files that get written, the command, and the resources it asked for.
    Engines only ever see this object (through `ExecutionEngine.submit_command`), never the job itself.
    """
    def __init__(self, job, work_dir, name, command, *,
                 input_file=None,
                 output_file=None,
                 stdout_file=None,
                 nproc=None,
                 memory=None,
                 parallel_model='threads',
                 modules=(),
                 setup_commands=(),
                 environment=None):
        self.job = job
        self.job_class = type(job)
        self.work_dir = os.path.abspath(work_dir)
        self.name = name
        self.command = [str(c) for c in command]
        self.input_file = input_file
        self.output_file = output_file
        self.stdout_file = stdout_file  # captured stdout of the program, if it does not write its own output file
        self.nproc = nproc
        self.memory = memory
        self.parallel_model = parallel_model
        self.modules = list(modules)
        self.setup_commands = list(setup_commands)
        self.environment = dict(environment or {})

    @property
    def run_script(self):
        return os.path.join(self.work_dir, f"run_{self.name}.sh")

    @property
    def input_path(self):
        return os.path.join(self.work_dir, self.input_file)

    @property
    def output_path(self):
        return None if self.output_file is None else os.path.join(self.work_dir, self.output_file)

    @staticmethod
    def _quote_env(v):
        v = str(v)
        return '"' + v.replace('"', '\\"') + '"' if '$' in v else shlex.quote(v)

    def format_run_script(self):
        """
        :return: the text of the shell script that runs the program from inside the work directory
        :rtype: str
        """
        lines = ["#!/bin/bash", "set -e", 'cd "$(dirname "${BASH_SOURCE[0]}")"']
        lines += [f"module load {m}" for m in self.modules]
        lines += [f"export {k}={self._quote_env(v)}" for k, v in sorted(self.environment.items())]
        lines += self.setup_commands
        cmd = " ".join(shlex.quote(c) for c in self.command)
        if self.stdout_file is not None:
            cmd += f" > {shlex.quote(self.stdout_file)}"
        lines.append(cmd)
        return "\n".join(lines) + "\n"

    def write(self):
        """
        Write the job input and the run script into the work directory.

        :return: self
        """
        os.makedirs(self.work_dir, exist_ok=True)
        self.job.write(self.input_path)
        with open(self.run_script, 'w') as out:
            out.write(self.format_run_script())
        os.chmod(self.run_script, os.stat(self.run_script).st_mode | stat.S_IXUSR)
        return self

    def __repr__(self):
        return f"{type(self).__name__}({self.job_class.__name__}, {self.name!r}, command={self.command})"


class ExternalProgramFuture(ExecutionFuture):
    """
    Wraps the future an engine returned for a `JobSubmission`, adding access to the job's files and parsed results.
    Status and joining are delegated; `get_result` collects the output (so it is only meaningful once finished).
    """
    def __init__(self, future, submission, **opts):
        super().__init__(**opts)
        self.future = future
        self.submission = submission
        self.poll_time = getattr(future, 'poll_time', self.poll_time)

    def __getattr__(self, item):  # job_id, process, ... of the wrapped future
        if item in ('future', 'submission'):
            raise AttributeError(item)
        return getattr(self.future, item)

    @property
    def work_dir(self):
        return self.submission.work_dir

    @property
    def output_file(self):
        return self.submission.output_path

    def get_status(self):
        self.status = self.future.get_status()
        return self.status

    def join(self, timeout=None):
        self.future.join(timeout=timeout)
        self.status = self.get_status()
        return self

    def read_output(self):
        """
        :return: the text of the program's output file, or `None` if it does not exist (yet)
        """
        path = self.submission.output_path
        if path is None or not os.path.isfile(path):
            return None
        with open(path, errors='replace') as inp:
            return inp.read()

    def get_result(self):
        """
        :return: a dict with ``status``, ``returncode`` (when the engine knows it), the file locations, the
            ``output`` text and whatever the job class parses out of it (``results``)
        :rtype: dict
        """
        status = self.get_status()
        base = getattr(self.future, 'get_result', lambda: None)()
        base = base if isinstance(base, dict) else {}
        sub = self.submission
        res = {
            'status': status,
            'returncode': base.get('returncode'),
            'work_dir': sub.work_dir,
            'input_file': sub.input_path,
            'output_file': sub.output_path,
        }
        if status in (ExecutionStatus.COMPLETED, ExecutionStatus.ERROR):
            res['output'] = self.read_output()
            res['results'] = sub.job_class.collect_results(sub)
        if status == ExecutionStatus.ERROR:
            # whatever the run script itself printed (launcher errors never reach the program's output file)
            log = os.path.join(sub.work_dir, f"run_{sub.name}.log")
            if os.path.isfile(log):
                with open(log, errors='replace') as stream:
                    res['log'] = stream.read()[-4000:]
        return res
