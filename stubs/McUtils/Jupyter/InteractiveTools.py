"""
Miscellaneous tools for interactive messing around in Jupyter environments
"""
from .. import Devutils as dev
import sys, os, types, importlib, inspect, io, tempfile as tf
import subprocess, threading, platform
__all__ = ['ModuleReloader', 'ExamplesManager', 'NotebookExporter', 'FormattedTable', 'NoLineWrapFormatter', 'OutputCapture', 'patch_pinfo', 'JupyterSessionManager']
__reload_hook__ = ['.NBExporter']

class JupyterSessionManager:

    @classmethod
    def _get_exec_prefix(cls):
        ...
    _jupyter_dir = None

    @classmethod
    def jupyter_env(cls):
        ...
    _jupyter_dirs = None

    @classmethod
    def _get_jupyter_dirs(cls):
        ...

    @classmethod
    def jupyter_dirs(cls):
        ...

    @classmethod
    def install_extension(cls, extension_package, exec_prefix=None, extension_types=('nbextension', 'labextension'), overwrite=False):
        """
        Attempts to do a basic installation for JupterLab
        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_kernel_specs(cls, root_dirs=None):
        ...

    @classmethod
    def prep_kernel_args(cls, name, base_opts, new_opts):
        ...

    @classmethod
    def modify_kernel_spec(cls, name, root_dirs=None, **opts):
        ...

    @classmethod
    def install_ipykernel(cls, prefix):
        ...

class ModuleReloader:
    """
    Reloads a module & recursively descends its 'all' tree
    to make sure that all submodules are also reloaded
    """

    def __init__(self, modspec):
        """
        :param modspec:
        :type modspec: str | types.ModuleType
        """
        ...

    def get_parents(self):
        """
        Returns module parents
        :return:
        :rtype:
        """
        ...

    def get_members(self):
        """
        Returns module members
        :return:
        :rtype:
        """
        ...

    def reload_member(self, member, stack=None, reloaded=None, blacklist=None, reload_parents=True, verbose=False, print_indent=''):
        ...
    blacklist_keys = ['site-packages', os.path.abspath(os.path.dirname(inspect.getfile(os)))]

    def reload(self, stack=None, reloaded=None, blacklist=None, reload_parents=True, verbose=False, print_indent=''):
        """
        Recursively searches for modules to reload and then reloads them.
        Uses a cache to break cyclic dependencies of any sort.
        This turns out to also be a challenging problem, since we need to basically
        load depth-first, while never jumping too far back...


        :return:
        :rtype:
        """
        ...

    @classmethod
    def load_module(cls, module):
        ...

    @classmethod
    def import_from(cls, module, names, globs=None):
        ...

class NotebookExporter:
    tag_filters = {'cell': ('ignore',), 'output': ('ignore',), 'input': ('ignore',)}

    def __init__(self, name, src_dir=None, img_prefix=None, img_dir=None, output_dir=None, tag_filters=None):
        ...

    def load_preprocessor(self):
        ...

    def load_filters(self):
        ...

    def load_nb(self):
        ...

    def save_output_file(self, filename, body):
        ...

    def export(self):
        ...

class ExamplesManager:
    data_path = ('ci', 'tests', 'TestData')
    examples_path = ('ci', 'examples')

    def __init__(self, root, data_path=None, examples_path=None, globs=None):
        ...

    def test_data(cls, *path):
        ...

    def examples_data(cls, *path):
        ...

    def load_module(self, module, modify_relative_imports=True):
        ...

    def import_from(self, module, names, modify_relative_imports=True, globs=None):
        ...

    @classmethod
    def parse_x3d_view_matrix(cls, vs, view_all=True):
        ...

class NoLineWrapFormatter:

    def __init__(self, *objs, white_space='pre', **opts):
        ...

    def _canonicalize(self, o):
        ...

    def create_obj(self):
        ...

    def to_widget(self):
        ...

    def _ipython_display_(self):
        ...

class FormattedTable(NoLineWrapFormatter):

    def __init__(self, table_data, column_formats='8.3f', **format_opts):
        ...

class OutputCapture:

    def __init__(self, handles=None, bind_global=True, file_handles=True, autoclose=None, save_output=True):
        ...

    @classmethod
    def get_handles(cls, handles=None, file_handles=False):
        ...

    @classmethod
    def get_temp_stream(cls):
        ...

    def __enter__(self):
        ...

    def __exit__(self, *args):
        ...

class SlurmInterface:

    @classmethod
    def format_kwargs(cls, kwargs):
        ...

    @classmethod
    def run(cls, cmd, *args, **kwargs):
        ...

    @classmethod
    def parse_slurm_table(cls, tab: str, headers=True, sep=None):
        ...

    @classmethod
    def sinfo(cls, all=None, format=None, **kw):
        ...

    @classmethod
    def squeue(cls, user=None, all=None, format=None, **kw):
        ...

def patch_pinfo():
    ...