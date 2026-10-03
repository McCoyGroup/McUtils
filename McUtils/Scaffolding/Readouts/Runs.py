"""
Readouts for run metadata: `Job` run directories (``job_data.json`` start/runtime/parameters,
the job log and checkpoint) and `RunEnvironment`, a snapshot of where and with what a calculation
ran (host, platform, Python and package versions, selected environment variables). Nothing that
looks like a credential is recorded.
"""

import datetime
import importlib.metadata
import json
import os
import platform
import socket
import sys

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutSection, ReadoutFields, ReadoutTable,
    FieldSet, Field, Column, TabularData, record_nodes,
)

__all__ = [
    "RunEnvironment",
    "JobRunReadout",
]

_SAFE_ENV = ("CONDA_DEFAULT_ENV", "VIRTUAL_ENV", "SLURM_JOB_ID", "SLURM_JOB_NAME", "SLURM_NTASKS", "SLURM_CPUS_PER_TASK",
             "SLURM_JOB_PARTITION", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS")


class RunEnvironment(dict):
    """A dict snapshot of the run environment; ``to_readout()`` shows it."""

    @classmethod
    def capture(cls, packages=("numpy", "scipy", "matplotlib", "rdkit"), env=_SAFE_ENV):
        info = {
            "captured": datetime.datetime.now().isoformat(timespec="seconds"),
            "host": socket.gethostname(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "python": sys.version.split()[0],
            "executable": sys.executable,
            "cpus": os.cpu_count(),
            "cwd": os.getcwd(),
        }
        versions = {}
        for p in packages:
            try:
                versions[p] = importlib.metadata.version(p)
            except importlib.metadata.PackageNotFoundError:
                mod = sys.modules.get(p)
                if mod is not None and getattr(mod, "__version__", None):
                    versions[p] = mod.__version__
        info["packages"] = versions
        info["environment"] = {k: os.environ[k] for k in env if k in os.environ}
        return cls(info)

    def to_readout(self, **opts):
        return RunEnvironmentReadout(self).to_readout(**opts)


class RunEnvironmentReadout(ReadoutAdapter):
    readout_id = "environment"

    def get_readout_title(self):
        return f"Run environment ({self.obj.get('host', '')})"

    @readout_section("system", title="System")
    def readout_system(self, ctx):
        """Host, platform, Python and working directory."""
        e = self.obj
        f = [Field(k, str(e[k]), label=k.capitalize()) for k in ("captured", "host", "platform", "machine", "python",
                                                                  "executable", "cpus", "cwd") if k in e]
        return ReadoutFields(FieldSet(f, name="system"))

    @readout_section("packages", title="Packages")
    def readout_packages(self, ctx):
        """Versions of the requested packages, and selected environment variables."""
        e = self.obj
        nodes = []
        if e.get("packages"):
            nodes.append(ReadoutFields(FieldSet([Field(k, v, label=k) for k, v in e["packages"].items()],
                                                name="packages")))
        if e.get("environment"):
            nodes.append(ReadoutFields(FieldSet([Field(k.lower(), v, label=k) for k, v in e["environment"].items()],
                                                name="environment"), title="Environment"))
        if not nodes:
            raise ReadoutSectionUnavailable("nothing recorded")
        return nodes


class JobRunReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for a `Job` run directory (a `Job` or its directory path): timing and parameters from
    ``job_data.json``, the job log (``log.txt``) and the checkpoint contents.
    """
    readout_id = "job_run"

    def __init__(self, job):
        super().__init__(job)

    @property
    def dir(self):
        j = self.obj
        return str(j) if isinstance(j, (str, os.PathLike)) else getattr(j, "dir", None)

    def data(self):
        p = os.path.join(self.dir, "job_data.json")
        if not os.path.isfile(p):
            return {}
        with open(p) as f:
            return json.load(f)

    def get_readout_title(self):
        return f"Job run: {os.path.basename(os.path.normpath(self.dir))}"

    @readout_section("summary", title="Run")
    def readout_summary(self, ctx):
        """Directory, start time and runtime."""
        d = self.data()
        f = [Field("dir", os.path.abspath(self.dir), label="Directory", quantity="path")]
        start = d.get("start") or {}
        if start.get("datetime"):
            f.append(Field("start", str(start["datetime"]), label="Started"))
        if d.get("runtime") is not None:
            f.append(Field("runtime", float(d["runtime"]), label="Runtime (s)", fmt="{:.3f}"))
        files = sorted(os.listdir(self.dir)) if os.path.isdir(self.dir) else []
        f.append(Field("files", ", ".join(files[:20]) + (" …" if len(files) > 20 else ""), label="Files"))
        return ReadoutFields(FieldSet(f, name="summary"))

    def _has_params(self):
        return bool(self.data().get("parameters")), "no parameters recorded"

    @readout_section("parameters", title="Parameters", available="_has_params")
    def readout_parameters(self, ctx):
        """Job parameters as recorded."""
        return record_nodes(self.data()["parameters"], "parameters")

    def _has_log(self):
        p = os.path.join(self.dir, "log.txt")
        return os.path.isfile(p) and os.path.getsize(p) > 0, "no log"

    @readout_section("log", title="Log", available="_has_log")
    def readout_log(self, ctx, max_blocks=6):
        """The job log (`LogReadout`)."""
        from .Logs import LogReadout
        sub = LogReadout(os.path.join(self.dir, "log.txt"))
        return ReadoutSection(*sub.get_readout_sections(ctx=ctx, exclude=["contents"]))

    def _checkpoint(self):
        for name in ("checkpoint.json", "checkpoint.npz", "checkpoint.hdf5"):
            p = os.path.join(self.dir, name)
            if os.path.isfile(p):
                return p
        return None

    def _has_checkpoint(self):
        return self._checkpoint() is not None, "no checkpoint file"

    @readout_section("checkpoint", title="Checkpoint", available="_has_checkpoint")
    def readout_checkpoint(self, ctx):
        """Checkpoint contents (`ArchiveReadout`)."""
        from .Archives import ArchiveReadout
        sub = ArchiveReadout(self._checkpoint())
        return ReadoutSection(*sub.get_readout_sections(ctx=ctx))
