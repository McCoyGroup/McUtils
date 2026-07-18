import importlib, importlib.abc, os, importlib.util, sys

__all__ = [
    "ModuleLoader"
]

class DynamicModuleLoader(importlib.abc.SourceLoader):
    """
    A `DynamicModuleLoader` is a Loader object that can load a python module from a file path.
    Primarily intended for workflows that don't support `importlib.import_module`
    """
    tag = "DynamicImports"
    def __init__(self, rootdir='', rootpkg=None, retag=True):
        """
        :param rootdir: root directory to look for files off of
        :type rootdir: str
        :param rootpkg: root package to look for files off of
        :type rootpkg: str or None
        """
        self._dir=rootdir
        self._pkg = rootpkg
        if retag is True:
            retag = self.tag
        self._reg=retag
        super().__init__()

    def get_data(self, file):
        """
        **LLM Docstring**

        Read source data from a file in binary mode.

        :param file: path to the source file
        :type file: str | os.PathLike

        :return: raw file contents
        :rtype: bytes
        """
        with open(file,'rb') as src:
            return src.read()

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
        if not os.path.exists(fullname):
            basename, ext = os.path.splitext(fullname.split(".")[-1])
            if ext != "":
                fullname = os.path.join(self._dir, basename+ext)
            else:
                fullname = os.path.join(self._dir, basename+".py")
                if not os.path.exists(fullname):
                    fullname = os.path.join(self._dir, basename)
        if os.path.isdir(fullname):
            fullname = os.path.join(fullname, "__init__.py")
        return fullname

    def get_spec(self, file, pkg = None):
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
        base_name = os.path.splitext(os.path.basename(file))[0]
        package_origin = file
        if pkg is None:
            pkg = self._pkg
        if pkg is None:
            raise ImportError("{}: package name required to load file".format(type(self)))
        if pkg == "":
            package_name = base_name
        else:
            package_name = pkg + "." + base_name
        spec = importlib.util.spec_from_loader(
            package_name,
            self,
            origin=package_origin
        )
        return spec

    def reregister_module(self, module, tag=None):
        """
        Sets up a secondary hook for a module so it's clear which
        ones were dynamically loaded

        :param tag:
        :type tag:
        :return:
        :rtype:
        """
        if tag is None:
            tag = self._reg
        sys.modules[tag + "." + module.__name__] = module

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
        d = self._dir
        try:
            if os.path.exists(file):
                self._dir = os.path.dirname(file)
            # print(file, self._dir)
            spec = self.get_spec(file, pkg)
            module = importlib.util.module_from_spec(spec)
            if module is None:
                module = importlib.util.module_from_spec(None)
            self.exec_module(module)
            self.reregister_module(module)
        finally:
            self._dir = d
        return module

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
        # backwards compatibility
        if not hasattr(importlib, 'import_module') and not retag:
            retag = True
        if retag:
            self.loader = DynamicModuleLoader(rootdir=rootdir, rootpkg=rootpkg, retag=retag)
        else:
            self.root_dir = rootdir
            self.loader = None

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
        if self.loader is not None:
            return self.loader.load(file, pkg=pkg)
        else:
            rootdir = os.path.dirname(file)
            if rootdir == "" or not os.path.isdir(rootdir):
                rootdir = self.root_dir
            if rootdir is not None:
                sys.path.insert(0, rootdir)
            try:
                if pkg is None:
                    file = os.path.splitext(file)[0]
                    mod = importlib.import_module(file)
                else:
                    mod = importlib.import_module(file, package=pkg)
            finally:
                if rootdir is not None:
                    sys.path.pop(0)
            return mod
