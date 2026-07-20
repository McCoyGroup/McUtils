import collections
import enum, types, ast
import os, sys, tempfile, uuid
import subprocess, inspect
import threading
import weakref
from ..Scaffolding import Checkpointer
__all__ = ['ScriptContext', 'ScriptRunner']

class Sentinels(enum.Enum):
    Missing = 'missing'

class ScriptContext:

    def __init__(self, objects: dict, imports=None, script_dir=None, script_id=None, context_file=None, autodelete=None, path=None):
        ...

    @classmethod
    def get_dir(cls):
        ...
    context_file_name = 'context-'
    context_file_extension = '.hdf5'

    @classmethod
    def get_context_file(cls, script_id):
        ...

    def populate_context_file(self):
        ...

    @classmethod
    def load_context(cls, context_file):
        ...

    @classmethod
    def path_loader_template(cls, path):
        ...

    @classmethod
    def context_loader_template(cls, context_file):
        ...

    @classmethod
    def chdir_template(cls, dir):
        ...

    @classmethod
    def imports_template(cls, imports):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    def create_context_loader(self):
        ...

    @classmethod
    def _handle_import_name(cls, name):
        ...

    @classmethod
    def extract_names(cls, code):
        ...

    @classmethod
    def find_globals(cls):
        ...

    @classmethod
    def from_script(cls, script, modules=None, globs=None, objects=None, imports=None, script_dir=None, script_id=None, context_file=None, autodelete=None, path=None):
        ...

class ScriptRunner:

    def __init__(self, context, script_name='script-', script_suffix='.py', python=None, autodelete=None):
        ...

    @classmethod
    def get_python(cls, python):
        ...

    class Result:
        __slots__ = ['script', 'process', 'thread']

        def __init__(self, script, process=None, thread=None):
            ...

        def join(self, timeout=None):
            ...

        @property
        def result(self):
            ...

    def _run_py_subprocess(self, result, script, dry_run=False, runner=None):
        ...

    def prep_script(self, script):
        ...

    def run_script(self, script, dry_run=False, background=True, interactive=False):
        ...

    @classmethod
    def run(cls, script, modules=None, globs=None, objects=None, imports=None, script_dir=None, script_id=None, context_file=None, autodelete=None, path=None, background=True, interactive=False, dry_run=False):
        ...