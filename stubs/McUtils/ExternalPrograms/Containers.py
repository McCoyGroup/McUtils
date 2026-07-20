from __future__ import annotations
import abc
import subprocess
import itertools
import os
import importlib.util
import shutil
import tempfile
__all__ = ['SingularityLauncher', 'DockerLauncher', 'PodmanLauncher', 'CharliecloudLauncher']

class ContainerLauncher(metaclass=abc.ABCMeta):

    def __init__(self, cli_binary, container_spec, *args, bind_sources=None, container_process=None, process_kwargs=None, **kwargs):
        ...

    @classmethod
    def setup_bind_sources(cls, targets: str | list[str], copy_source=True, resolve_module_names=True):
        ...

    @classmethod
    @abc.abstractmethod
    def prep_binds(cls, binds: dict[str, str] | list[tuple[str, str] | list[str]]):
        ...

    @classmethod
    @abc.abstractmethod
    def prep_envs(cls, envs: dict):
        ...

    @classmethod
    def map_option_name(cls, key):
        ...
    LIST_JOIN_DELIMITERS: 'dict[str, str]' = {}
    VARIABLE_JOIN_DELIMITERS: 'dict[str, str]' = {}
    DEFAULT_VARIABLE_DELIMITER = '='

    @classmethod
    def _format_value(cls, key, value) -> 'list[str]':
        ...

    @classmethod
    def format_job_args(cls, kwargs) -> 'list[str]':
        ...

    @abc.abstractmethod
    def prep_core_kwargs(self, kwargs):
        ...

    @abc.abstractmethod
    def get_launch_command_from_components(self, binary, spec, launch_kwargs, proc_args, proc_kwargs):
        ...

    @classmethod
    def _merge_binds(self, old, new):
        ...

    @classmethod
    def _merge_envs(self, old, new):
        ...

    def get_launch_command(self) -> list[str]:
        ...

    def launch_container(self, stdout=True, stderr=True, text=True, **subprocess_kwargs):
        ...

    def launch(self, **subprocess_kwargs):
        ...

    def terminate(self):
        ...

    def run(self, text=True, **subprocess_kwargs):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    def __del__(self):
        ...

class DockerLauncher(ContainerLauncher):
    LIST_JOIN_DELIMITERS = {}
    VARIABLE_JOIN_DELIMITERS = {'volume': ':'}

    def __init__(self, container_spec, *args, cli_binary='docker', mode='run', **kwargs):
        ...

    @classmethod
    def prep_binds(cls, binds: dict[str, str] | list[tuple[str, str] | list[str]]):
        ...

    @classmethod
    def prep_envs(cls, envs: dict):
        ...

    def launch_option_names(self):
        ...

    def prep_core_kwargs(self, kwargs):
        ...

    def get_launch_command_from_components(self, binary, spec, launch_kwargs, proc_args, proc_kwargs):
        ...

class PodmanLauncher(DockerLauncher):
    LAUNCH_OPTIONS = DockerLauncher.LAUNCH_OPTIONS | {'pod', 'userns', 'uidmap', 'gidmap', 'security_opt', 'systemd'}

    def __init__(self, container_spec, *args, cli_binary='podman', **kwargs):
        ...

class SingularityLauncher(ContainerLauncher):
    LIST_JOIN_DELIMITERS = {'bind': ',', 'mount': ',', 'overlay': ','}
    VARIABLE_JOIN_DELIMITERS = {'bind': ':', 'mount': ':', 'overlay': ':'}

    def __init__(self, container_spec, *args, mode='run', cli_binary='singularity', **kwargs):
        ...

    @classmethod
    def _merge_binds(cls, new, old):
        ...

    @classmethod
    def prep_binds(cls, binds: dict[str, str] | list[tuple[str, str] | list[str]]):
        ...

    @classmethod
    def prep_envs(cls, envs: dict):
        ...

    def prep_core_kwargs(self, kwargs):
        ...

    def get_launch_command_from_components(self, binary, spec, launch_kwargs, proc_args, proc_kwargs):
        ...

class CharliecloudLauncher(ContainerLauncher):
    LIST_JOIN_DELIMITERS = {}

    def __init__(self, container_spec, *args, cli_binary='ch-run', **kwargs):
        ...

    @classmethod
    def prep_binds(cls, binds: dict[str, str] | list[tuple[str, str] | list[str]]):
        ...

    @classmethod
    def prep_envs(cls, envs: dict):
        ...

    def prep_core_kwargs(self, kwargs):
        ...

    def get_launch_command_from_components(self, binary, spec, launch_kwargs, proc_args, proc_kwargs):
        ...