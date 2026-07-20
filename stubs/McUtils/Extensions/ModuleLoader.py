import importlib, importlib.abc, os, importlib.util, sys
__all__ = ['ModuleLoader']

class DynamicModuleLoader(importlib.abc.SourceLoader):
    """
    A `DynamicModuleLoader` is a Loader object that can load a python module from a file path.
    Primarily intended for workflows that don't support `importlib.import_module`
    """
    tag = 'DynamicImports'

    def __init__(self, rootdir='', rootpkg=None, retag=True):
        """
        :param rootdir: root directory to look for files off of
        :type rootdir: str
        :param rootpkg: root package to look for files off of
        :type rootpkg: str or None
        """
        ...

    def get_data(self, file):
        """
        **LLM Docstring**

        Read source data from a file in binary mode.

        :param file: path to the source file
        :type file: str | os.PathLike

        :return: raw file contents
        :rtype: bytes
        """
        ...

    def get_filename(self, fullname):
        """
        **LLM Docstring**

        Resolve a module name or path to the Python source file this loader should execute.

        Nonexistent dotted names are searched relative to the configured root directory; directories resolve to `__init__.py`.

        :param fullname: module identifier or candidate filesystem path
        :type fullname: str

        :return: resolved source-file path
        :rtype: str
        """
        ...

    def get_spec(self, file, pkg=None):
        """
        **LLM Docstring**

        Build an import specification for a source file.

        The package name is taken from `pkg` or the loader default and combined with the file basename.

        :param file: source-file path used as the module origin
        :type file: str

        :param pkg: parent package name; an empty string creates a top-level module
        :type pkg: str | None

        :return: loader-backed module specification
        :rtype: importlib.machinery.ModuleSpec
        """
        ...

    def reregister_module(self, module, tag=None):
        """
        Sets up a secondary hook for a module so it's clear which
        ones were dynamically loaded

        :param tag:
        :type tag:
        :return:
        :rtype:
        """
        ...

    def load(self, file, pkg=None):
        """
        loads a file as a module with optional package name

        :param file:
        :type file: str
        :param pkg:
        :type pkg: str or None
        :return:
        :rtype: module
        """
        ...

class ModuleLoader:
    """
    Provides a way to load dynamic modules.
    Either use a `DynamicModuleLoader` or the `importlib.import_module` function
    depending on how much customization is needed.
    """

    def __init__(self, rootdir='', rootpkg=None, retag=False):
        """
        :param rootdir: root directory to look for files off of
        :type rootdir: str
        :param rootpkg: root package to look for files off of
        :type rootpkg: str or None
        """
        ...

    def load(self, file, pkg=None):
        """
        **LLM Docstring**

        Load and return a Python module from a path or import name.

        Uses the custom dynamic loader when configured; otherwise temporarily prepends the containing directory to `sys.path` and delegates to `importlib.import_module`.

        :param file: module path or import name
        :type file: str

        :param pkg: optional package for relative import resolution
        :type pkg: str | None

        :return: loaded module object
        :rtype: types.ModuleType
        """
        ...