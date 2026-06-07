from __future__ import annotations

import abc
import subprocess
import itertools
import os
import importlib.util
import shutil
import tempfile

__all__ = [
    "SingularityLauncher",
    "DockerLauncher",
    "PodmanLauncher",
    "CharliecloudLauncher"
]

class ContainerLauncher(metaclass=abc.ABCMeta):
    def __init__(self,
                 cli_binary,
                 container_spec,
                 *args,
                 bind_sources=None,
                 container_process=None,
                 process_kwargs=None,
                 **kwargs):
        self.cli_binary = cli_binary
        self.container_spec = container_spec
        self.proc_args = args
        self.proc_kwargs = process_kwargs
        self.mixed_kwargs = kwargs
        self.container_process = container_process
        self.managed = container_process is None
        self.bind_sources = bind_sources
        self._bind_dir = None

    @classmethod
    def setup_bind_sources(cls, targets:str|list[str], copy_source=True, resolve_module_names=True):
        if isinstance(targets, str):
            targets = [targets]
        targets = [
            os.path.abspath(t)
                if (not resolve_module_names or os.path.exists(t)) else
            importlib.util.find_spec(t).origin #TODO: make this more robust against odd module formats
            for t in targets
        ]
        targets = [
            os.path.dirname(t)
                if os.path.isfile(t) else
            t
            for t in targets
        ]

        if copy_source:
            tempdir = tempfile.mkdtemp()
            for t in targets:
                shutil.copytree(t, os.path.join(tempdir, os.path.basename(t)))
            return [tempdir], True
        else:
            parents = {os.path.dirname(t) for t in targets}
            return parents, False

    @classmethod
    @abc.abstractmethod
    def prep_binds(cls, binds:dict[str, str]|list[tuple[str, str]|list[str]]):
        ...

    @classmethod
    @abc.abstractmethod
    def prep_envs(cls, envs:dict):
        ...

    @classmethod
    def map_option_name(cls, key):
        return "--" + key.replace('_', '-')

    LIST_JOIN_DELIMITERS: 'dict[str, str]' = {}
    VARIABLE_JOIN_DELIMITERS: 'dict[str, str]' = {}
    DEFAULT_VARIABLE_DELIMITER = '='
    @classmethod
    def _format_value(cls, key, value) -> 'list[str]':
        opt = cls.map_option_name(key)

        if value is True:
            return [opt]
        if value is False or value is None:
            return []

        # dict: expand to key=value pairs. A mapping nearly always means
        # "set several named entries for this option" (env vars, labels,
        # sysctls, ulimits, ...), which on every runtime is repeated flags.
        if isinstance(value, dict):
            delim = cls.VARIABLE_JOIN_DELIMITERS.get(key, cls.DEFAULT_VARIABLE_DELIMITER)
            pairs = [f"{k}{delim}{v}" for k, v in value.items()]
            delim = cls.LIST_JOIN_DELIMITERS.get(key)
            if delim is not None:
                joined = delim.join(p for p in pairs)
                return [f"{opt}={joined}"]
            return list(itertools.chain.from_iterable(
                [f"{opt}={p}"] for p in pairs
            ))

        # list/tuple: repeated flags unless this runtime joins them.
        if isinstance(value, (list, tuple)):
            items = [str(v) for v in value]
            delim = cls.LIST_JOIN_DELIMITERS.get(key)
            if delim is not None:
                joined = delim.join(v for v in items)
                return [f"{opt}={joined}"]
            return list(itertools.chain.from_iterable(
                [f"{opt}={v}"] for v in items
            ))

        # scalar
        return [f"{opt}={value}"]

    @classmethod
    def format_job_args(cls, kwargs) -> 'list[str]':
        return list(itertools.chain.from_iterable(
            cls._format_value(k, v) for k, v in kwargs.items()
        ))

    @abc.abstractmethod
    def prep_core_kwargs(self, kwargs):
        ...

    @abc.abstractmethod
    def get_launch_command_from_components(self, binary, spec, launch_kwargs, proc_args, proc_kwargs):
        ...

    @classmethod
    def _merge_binds(self, old, new):
        if old is None:
            return new
        if isinstance(new, str):
            new = [new]
        if isinstance(old, str):
            old = [old]
        if isinstance(new, dict):
            if not isinstance(old, dict):
                new = [k+":"+v for k, v in new.items()]
                new = new + list(old)
            else:
                new = old | new
        else:
            if isinstance(old, dict):
                old = [k+":"+v for k, v in old.items()]
            new = list(new) + list(old)
        return new

    @classmethod
    def _merge_envs(self, old, new):
        if old is None:
            return new
        if isinstance(new, str):
            new = [new]
        if isinstance(old, str):
            old = [old]
        if isinstance(new, dict):
            if not isinstance(old, dict):
                new = [k+"="+v for k, v in new.items()]
                new = new + list(old)
            else:
                new = old | new
                for k,v in old.items():
                    if k in new:
                        new[k] = new[k] + ":" + v
        else:
            if isinstance(old, dict):
                old = [k+"="+v for k, v in old.items()]
            new = list(new) + list(old)
        return new

    def get_launch_command(self) -> list[str]:
        binary = self.cli_binary
        if isinstance(binary, str):
            binary = [binary]
        spec = self.container_spec
        if isinstance(spec, str):
            spec = [spec]
        if self.proc_kwargs is None:
            launch_kwargs, proc_kwargs = self.prep_core_kwargs(self.mixed_kwargs)
        else:
            launch_kwargs, proc_kwargs = self.mixed_kwargs, self.proc_kwargs

        if self.bind_sources is not None:
            bind_paths, managed = self.setup_bind_sources(self.bind_sources)
            if managed:
                self._bind_dir = bind_paths
            bind_mods = {t:os.path.join('/tmp', 'bind', os.path.basename(t)) for t in bind_paths}
            bm = self.prep_binds(bind_mods)
            launch_kwargs = launch_kwargs.copy()
            for k,v in bm.items():
                if k in launch_kwargs:
                    v = self._merge_binds(launch_kwargs[k], v)
                launch_kwargs[k] = v
            env_mods = {'PYTHONPATH':":".join(bind_mods.values()) + ":$PYTHONPATH"}
            em = self.prep_envs(env_mods)
            for k,v in em.items():
                if k in launch_kwargs:
                    v = self._merge_envs(launch_kwargs[k], v)
                launch_kwargs[k] = v

        return self.get_launch_command_from_components(
            binary, spec,
            self.format_job_args(launch_kwargs),
            [str(s) for s in self.proc_args],
            self.format_job_args(proc_kwargs),
        )

    def launch_container(self, stdout=True, stderr=True, text=True, **subprocess_kwargs):
        if stdout is True:
            stdout = subprocess.PIPE
        if stderr is True:
            stderr = subprocess.STDOUT
        return subprocess.Popen(self.get_launch_command(),
                                stdout=stdout,
                                stderr=stderr,
                                text=text,
                                **subprocess_kwargs)

    def launch(self, **subprocess_kwargs):
        if self.container_process is None:
            self.container_process = self.launch_container(**subprocess_kwargs)
        return self.container_process
    def terminate(self):
        if self.managed:
            if self.container_process is not None:
                self.container_process.kill()
                self.container_process = None
        if self._bind_dir is not None:
            shutil.rmtree(self._bind_dir)
            self._bind_dir = None
    def run(self, text=True, **subprocess_kwargs):
        return subprocess.run(self.get_launch_command(), text=text, **subprocess_kwargs)

    def __enter__(self):
        return self.launch_container()
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()

    def __del__(self):
        try:
            self.terminate()
        except:
            ...

class DockerLauncher(ContainerLauncher):
    # docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
    # Common run-level options (extend as needed):
    LAUNCH_OPTIONS = {'detach', 'interactive', 'tty', 'rm', 'name', 'env',
                      'env_file', 'volume', 'mount', 'workdir', 'user', 'network', 'publish', 'expose',
                      'privileged', 'cap_add', 'cap_drop', 'device', 'gpus', 'memory', 'cpus', 'restart',
                      'entrypoint', 'hostname', 'add_host', 'label', 'pull', 'platform', 'read_only',
                      'init', 'tmpfs', 'volumes_from', 'publish_all', 'dns', 'security_opt', 'userns',
                      'shm_size', 'sysctl', 'ulimit'}

    # Docker uses repeated flags for every multi-value option, so no joins.
    LIST_JOIN_DELIMITERS = {}
    VARIABLE_JOIN_DELIMITERS = {'volume': ":"}

    def __init__(self, container_spec, *args, cli_binary="docker", mode='run', **kwargs):
        super().__init__(cli_binary, container_spec, *args, **kwargs)
        self.mode = mode

    @classmethod
    def prep_binds(cls, binds:dict[str, str]|list[tuple[str, str]|list[str]]):
        return {'volume':binds}

    @classmethod
    def prep_envs(cls, envs:dict):
        return {'env':envs}

    def launch_option_names(self):
        return self.LAUNCH_OPTIONS

    def prep_core_kwargs(self, kwargs):
        launch_kwargs = {k: v for k, v in kwargs.items() if k in self.LAUNCH_OPTIONS}
        proc_kwargs = {k: v for k, v in kwargs.items() if k not in self.LAUNCH_OPTIONS}
        return launch_kwargs, proc_kwargs

    def get_launch_command_from_components(self, binary, spec, launch_kwargs, proc_args, proc_kwargs):
        return binary + [self.mode] + launch_kwargs + spec + proc_args + proc_kwargs


class PodmanLauncher(DockerLauncher):
    # Podman's `run` is Docker-CLI-compatible; reuse the option set, add a few extras.
    LAUNCH_OPTIONS = DockerLauncher.LAUNCH_OPTIONS | {
        'pod', 'userns', 'uidmap', 'gidmap', 'security_opt', 'systemd',
    }

    def __init__(self, container_spec, *args, cli_binary="podman", **kwargs):
        super().__init__(container_spec, *args, cli_binary=cli_binary, **kwargs)


class SingularityLauncher(ContainerLauncher):
    # singularity {run|exec} [OPTIONS] IMAGE [COMMAND] [ARG...]
    LAUNCH_OPTIONS = {
        'bind', 'contain', 'containall', 'cleanenv', 'env', 'env_file',
        'pwd', 'home', 'workdir', 'scratch', 'no_home', 'writable',
        'writable_tmpfs', 'nv', 'rocm', 'fakeroot', 'userns', 'net',
        'network', 'dns', 'hostname', 'pid', 'ipc', 'overlay', 'app',
    }

    LIST_JOIN_DELIMITERS = {'bind': ',', 'mount': ',', 'overlay': ','}
    VARIABLE_JOIN_DELIMITERS = {'bind': ":", 'mount': ':', 'overlay': ':'}

    def __init__(self, container_spec, *args, mode='run', cli_binary="singularity", **kwargs):
        super().__init__(cli_binary, container_spec, *args, **kwargs)
        self.mode = mode

    @classmethod
    def _merge_binds(cls, new, old):
        if isinstance(new, str):
            new = new.split(',')
        if isinstance(old, str):
            old = old.split(',')
        return super()._merge_binds(new, old)

    @classmethod
    def prep_binds(cls, binds:dict[str, str]|list[tuple[str, str]|list[str]]):
        return {'bind':binds}

    @classmethod
    def prep_envs(cls, envs:dict):
        return {'env':envs}

    def prep_core_kwargs(self, kwargs):
        launch_kwargs = {k: v for k, v in kwargs.items() if k in self.LAUNCH_OPTIONS}
        proc_kwargs   = {k: v for k, v in kwargs.items() if k not in self.LAUNCH_OPTIONS}
        return launch_kwargs, proc_kwargs

    def get_launch_command_from_components(self, binary, spec, launch_kwargs, proc_args, proc_kwargs):
        return binary + [self.mode] + launch_kwargs + spec + proc_args + proc_kwargs


class CharliecloudLauncher(ContainerLauncher):
    # ch-run [OPTIONS] IMAGE -- CMD [ARG...]
    # ch-run takes no in-container option flags; everything after `--` is the command,
    LAUNCH_OPTIONS = {
        'bind', 'cd', 'env_no_passwd', 'gid', 'uid', 'no_home',
        'no_passwd', 'set_env', 'unset_env', 'write', 'writable',
        'ch_ssh', 'join', 'join_pid', 'mount',
    }

    LIST_JOIN_DELIMITERS = {}

    def __init__(self, container_spec, *args, cli_binary="ch-run", **kwargs):
        super().__init__(cli_binary, container_spec, *args, **kwargs)

    @classmethod
    def prep_binds(cls, binds:dict[str, str]|list[tuple[str, str]|list[str]]):
        return {'mount':binds}

    @classmethod
    def prep_envs(cls, envs:dict):
        return {'set_env':envs}

    def prep_core_kwargs(self, kwargs):
        launch_kwargs = {k: v for k, v in kwargs.items() if k in self.LAUNCH_OPTIONS}
        proc_kwargs   = {k: v for k, v in kwargs.items() if k not in self.LAUNCH_OPTIONS}
        return launch_kwargs, proc_kwargs

    def get_launch_command_from_components(self, binary, spec, launch_kwargs, proc_args, proc_kwargs):
        cmd = binary + launch_kwargs + spec
        if proc_args or proc_kwargs:
            cmd += ["--"] + proc_args + proc_kwargs
        return cmd