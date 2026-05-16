"""
Provides minimal utilities for making slurm stuff nicer
"""

import inspect
import os
import subprocess

__all__ = ["SBatchJob"]

class SBatchJob:
    """
    Provides a simple interface to formatting SLURM
    files so that they can be submitted to `sbatch`.
    The hope is that this can be subclassed codify
    options for different HPC paritions and whatnot.
    """
    slurm_keys = [
        "account", "acctg-freq", "array", "batch", "bb", "bbf", "begin", "chdir",
        "cluster-constraint", "clusters", "comment", "constraint", "contiguous",
        "core-spec", "cores-per-socket", "cpu-freq", "cpus-per-gpu", "cpus-per-task",
        "deadline", "delay-boot", "dependency", "distribution", "error", "exclude",
        "exclusive", "export", "export-file", "extra-node-info",
        "get-user-env", "gid", "gpu-bind", "gpu-freq", "gpus", "gpus-per-node",
        "gpus-per-socket", "gpus-per-task", "gres", "gres-flags", "help", "hint",
        "ignore-pbs", "input", "job-name", "kill-on-invalid-dep", "licenses",
        "mail-type", "mail-user", "mcs-label", "mem", "mem-bind", "mem-per-cpu",
        "mem-per-gpu", "mincpus", "network", "nice", "nodefile", "nodelist", "nodes",
        "no-kill", "no-requeue", "ntasks", "ntasks-per-core", "ntasks-per-gpu",
        "ntasks-per-node", "ntasks-per-socket", "open-mode", "output", "overcommit",
        "oversubscribe", "parsable", "partition", "power", "priority", "profile",
        "propagate", "qos", "quiet", "reboot", "requeue", "reservation", "signal",
        "sockets-per-node", "spread-job", "switches", "test-only", "thread-spec",
        "threads-per-core", "time", "time-min", "tmp", "uid", "usage", "use-min-nodes",
        "verbose", "version", "wait", "wait-all-nodes", "wckey", "wrap"
    ]
    default_opts = {
        'output': '%x-%j.out'
    }
    def __init__(self,
                 description=None,
                 job_name=None, account=None, partition=None,
                 mem=None,  nodes=None, ntasks_per_node=None,
                 chdir='#script-dir',
                 output=None,
                 steps=(),
                 precall=None,
                 environment=None,
                 **opts
                 ):
        self.description = description
        self.steps = steps
        self.precall = precall
        self.environment = environment

        base_opts = dict(
            job_name=job_name, account=account, partition=partition,
            mem=mem, nodes=nodes, ntasks_per_node=ntasks_per_node,
            output=output, chdir=chdir
        )
        base_opts = self.clean_opts(base_opts)
        base_opts = dict(self.default_opts, **base_opts)

        opts = opts | base_opts
        self.opts = self.clean_opts(opts)

    def clean_opts(self, opts):
        """
        Makes sure opt names are clean.
        Does no validation of the values sent in.

        :param opts:
        :type opts:
        :return:
        :rtype:
        """
        clean_opts = {}
        for opt_name, opt_val in opts.items():
            opt_name = opt_name.replace("_", "-")
            if opt_val is not None:
                if opt_name not in self.slurm_keys:
                    raise ValueError("SBATCH option {} invalid; accepted ones are {}".format(opt_name, self.slurm_keys))
                clean_opts[opt_name] = opt_val
        return clean_opts

    sbatch_opt_template="#SBATCH --{name}={value}"
    def format_opt_block(self):
        """
        Formats block of options
        :return:
        :rtype:
        """
        return "\n".join(
            self.sbatch_opt_template.format(name=k, value=v) for k,v in self.opts.items() if v is not None
        )

    sbatch_template = "\n".join([
        "#!/bin/bash",
        "{opts}",
        "{env}",
        "{enter}",
        "{call}",
        "{exit}"
    ])
    sbatch_enter_command = "\n".join([
        'echo "Starting Job $SLURM_JOB_NAME"',
        'START=$(date +%s.%N)',
        'echo "  START: $(date)"',
        'echo "    PWD: $PWD"',
        'echo "  NODES: $SLURM_JOB_NUM_NODES"',
        'echo "  PART.: $SLURM_JOB_PARTITION"',
        'echo "{sep}"'.format(sep="=" * 50)
    ])
    sbatch_exit_command = "\n".join([
        'echo "{sep}"'.format(sep="=" * 50),
        'END=$(date +%s.%N)',
        'DIFF=$(echo "$END - $START" | bc)',
        'echo "   END: $(date)"',
        'echo "  TIME: $DIFF"'
    ])
    def format(self):
        """
        Formats an SBATCH file from the held options
        :param call_steps:
        :type call_steps:
        :return:
        :rtype:
        """
        opts = self.format_opt_block()
        enter = self.sbatch_enter_command
        if self.description is not None:
            enter += (
                    '\necho "'
                    + inspect.cleandoc(self.description).replace("\n", '"\necho "')
                    + '"\necho\n\n'
            )
        exit = self.sbatch_exit_command

        steps = self.steps
        if isinstance(steps, str):
            steps = (steps,)
        chdir = self.opts.pop("chdir", None)
        if isinstance(chdir, str):
            if chdir == '#script-dir':
               steps = (
                   '$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)',
                   'cd "$SCRIPT_DIR"'
               ) + steps
            else:
                self.opts['chdir'] = chdir

        call = "\n".join(steps)

        if self.environment is not None:
            env = "\n".join(
                "export {}={}".format(k, v)
                for k, v in sorted(self.environment.items())
                if v is not None
            )
        else:
            env = ""

        return self.sbatch_template.format(
            opts=opts,
            env=env,
            call=call,
            enter=enter,
            exit=exit
        )

    def write(self, file, output_dir=None, mode='w+', **kwargs):
        if isinstance(file, str):
            if output_dir is None:
                output_dir, file = os.path.split(file)
        if len(output_dir) == 0:
            output_dir = None
        curdir = os.getcwd()
        try:
            if output_dir is not None:
                os.chdir(output_dir)
            if self.precall is not None:
                self.precall()
            if hasattr(file, 'write'):
                file.write(self.format())
            else:
                with open(file, mode, **kwargs) as stream:
                    stream.write(self.format())
        finally:
            os.chdir(curdir)
        if output_dir is not None:
            return os.path.join(output_dir, file)
        else:
            return file

    def run(self, file='_sbatch.sh', output_dir=None, sbatch_function='sbatch',
            delete=True,
            text=True,
            capture_output=True,
            *args, **kwargs):
        file = self.write(file, output_dir, *args, **kwargs)
        kwargs = [
            (
                f"--{k}"
                    if v is True else
                f"--{k}={v}"
            ) if len(k) > 0 else (
                f"-{k}"
                    if v is True else
                None
            )
            for k,v in kwargs.items()
        ]
        kwargs = [k for k in kwargs if k is not None]
        res = subprocess.run([sbatch_function, file, *args, *kwargs],
                             text=text, capture_output=capture_output)
        if delete:
            try:
                os.remove(file)
            except FileNotFoundError:
                ...
        return res
