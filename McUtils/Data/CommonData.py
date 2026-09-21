"""
Defines a common data handler
"""
from .. import Devutils as dev
import os, sys
import importlib.util
import importlib.machinery

__all__ = [ "DataHandler", "DataError", "DataRecord" ]

default_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
default_data_package = "TheRealMcCoy"
default_data_key = "data"
default_data_source_key = "source"

class DataError(KeyError):
    """
    Exception subclass for data error
    """

class DataHandler:
    """
    Defines a general data loader class that we can use for `AtomData` and any other data classes we might find useful.
    """
    def __init__(self,
                 data_name,
                 data_key=None,
                 source_key=None,
                 data_dir=None,
                 data_pkg=None,
                 alternate_keys=None,
                 getter=None,
                 record_type=None,
                 extension='.py'
                 ):
        """
        :param data_name: the name of the dataset
        :type data_name: str
        :param data_key: the key in the loaded dictionary to use for the actual data (`"data"` by default)
        :type data_key: str | None
        :param source_key: the key in the loaded dictionary for the original data source (`"source"` by default)
        :type source_key: str | None
        :param data_dir: the main directory data will be loaded from (`.` by default)
        :type data_dir: str | None
        :param data_pkg: the python package to load (`TheRealMcCoy` by default)
        :type data_pkg: str | None
        :param alternate_keys: alternate keys that can be used to index into the dataset which can will be populated at runtime
        :type alternate_keys: Iterable[str] | None
        :param getter: a function to use to resolve a key
        :type getter: callable | None
        :param record_type: the class to use for holding data (`DataRecord` by default)
        :type record_type: type | None
        """
        if data_dir is None:
            data_dir = default_data_dir
        if data_key is None:
            data_key = default_data_key
        if source_key is None:
            source_key = default_data_source_key
        if data_pkg is None:
            data_pkg = default_data_package
        self.extension = extension
        self._data = None # this'll be a dict where we store all our data
        self._src = None
        self._dir = data_dir
        self._name = data_name
        self._key = data_key
        self._src_key = source_key
        self._pkg = data_pkg
        self._alts = alternate_keys
        self.record_type = DataRecord if record_type is None else record_type
        self._loaded = False
        self.getter = getter
    @property
    def data_file(self): # in case other people want to load it...
        if self._pkg is None:
            return os.path.join(self._dir, self._name+self.extension)
        return os.path.join(self._dir, self._pkg, self._name+self.extension)
    def _load_alts(self):
        # assumes we have dict data, but this entire structure does that anyway
        if not self._alts is None:
            extras = {}
            if isinstance(self._alts, str):
                self._alts = (self._alts,)
            for k in self._alts:
                extras.update({a[k]:a for a in self._data.values()}) #shouldn't increase memory bc mutable
            self._data.update(extras)
    def _load_package(self, pkg_name, pkg_dir):
        """
        Registers `pkg_name` in `sys.modules` as a package rooted at `pkg_dir`,
        without ever touching `sys.path`. This is what lets a submodule inside
        `pkg_dir` (e.g. `TheRealMcCoy/AtomData.py`) use ordinary relative
        imports (`from . import whatever`) the way it could if `pkg_dir`'s
        *parent* had been added to `sys.path`, the way `load()` used to do it.

        A no-op if `pkg_name` is already imported (e.g. from a previous call).
        """
        existing = sys.modules.get(pkg_name)
        if existing is not None:
            return existing
        pkg_init = os.path.join(pkg_dir, "__init__.py")
        if os.path.isfile(pkg_init):
            spec = importlib.util.spec_from_file_location(
                pkg_name, pkg_init, submodule_search_locations=[pkg_dir]
            )
            if spec is None or spec.loader is None:
                raise ImportError(f"can't load package {pkg_name!r} from {pkg_init!r}")
            module = importlib.util.module_from_spec(spec)
            sys.modules[pkg_name] = module
            try:
                spec.loader.exec_module(module)
            except Exception:
                sys.modules.pop(pkg_name, None)
                raise
        else:
            # no __init__.py -- treat it as a PEP 420 namespace package
            spec = importlib.machinery.ModuleSpec(pkg_name, loader=None, is_package=True)
            spec.submodule_search_locations = [pkg_dir]
            module = importlib.util.module_from_spec(spec)
            sys.modules[pkg_name] = module
        return module
    def _import_data_module(self):
        """
        Imports the python file backing this handler's data using `importlib`,
        resolving straight from the known file path instead of stashing
        `self._dir` on `sys.path` and hoping the normal import machinery finds
        it (and then leaving it there for the life of the process, which is
        what this replaces).

        If the data lives inside a package (the usual case -- e.g. `TheRealMcCoy`
        or `PsiDatasets`), that package is registered under its own name first
        (see `_load_package`) so relative imports inside it keep working.
        Either way, nothing is ever added to `sys.path`.

        Modules are cached in `sys.modules` under their normal dotted name, so
        loading the same dataset twice doesn't re-parse a (potentially large,
        e.g. `AtomData.py`) data file.
        """
        full_name = self._name if self._pkg is None else f"{self._pkg}.{self._name}"
        cached = sys.modules.get(full_name)
        if cached is not None:
            return cached
        if self._pkg is not None:
            self._load_package(self._pkg, os.path.join(self._dir, self._pkg))
        mod_file = self.data_file
        spec = importlib.util.spec_from_file_location(full_name, mod_file)
        if spec is None or spec.loader is None:
            raise ImportError(f"can't load {full_name!r} from {mod_file!r}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[full_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            sys.modules.pop(full_name, None)
            raise
        return module
    def load(self, env=None):
        """
        Actually loads the data from `data_file`.

        :return:
        :rtype:
        """
        if self.extension == '.py':
            module = self._import_data_module()
            try:
                self._data = getattr(module, self._key)
            except AttributeError:
                raise DataError(
                    "{}: data source {} has no key {}".format(
                        type(self).__name__, self._name, self._key
                    )
                )
            self._src = getattr(module, self._src_key, None)
        elif self.extension == '.json':
            env = dev.read_json(self.data_file)
            self._data = env[self._key]
            try:
                self._src = env[self._src_key]
            except:
                pass
        else:
            raise ValueError(f"don't know how to load from {self.extension}")
        self._load_alts()
        self._loaded = True
    @property
    def data(self):
        if self._data is None:
            self.load()
        return self._data
    @property
    def source(self):
        if self._src is None and not self._loaded:
            self.load()
        return self._src
    def _get_data(self, key):
        def _get(a, k):
            if k not in a:
                raise DataError("{}: data source {} doesn't have subkey {} of {}".format(
                    type(self).__name__,
                    self._name,
                    k,
                    key
                ))
            return a[k]

        data = self.data
        if self.getter is None:
            if isinstance(key, tuple):
                from functools import reduce
                return reduce(_get, key, data)
            else:
                if key not in data:
                    raise DataError("{}: data source {} doesn't have key {}".format(
                        type(self).__name__,
                        self._name,
                        key
                    ))
                return data[key]
        else:
            return self.getter(data, key)
    def __getitem__(self, key):
        data = self._get_data(key)
        return self.record_type(self, key, data)
    def __len__(self):
        return len(self.data)
    def __iter__(self):
        return iter(self.data.items())

    # implementing to make pickling of data objects possible...
    def __getstate__(self):
        state = self.__dict__.copy()
        state['_data'] = None
        state['_src'] = None
        state['_loaded'] = False

        # raise Exception(state)
        return state
    def __setstate__(self, state):
        self.__dict__.update(state)
        self._loaded = False

    def __repr__(self):
        return "{}('{}', file='{}')".format(
            type(self).__name__,
            self._name,
            self._src
        )

class DataRecord:
    """
    Represents an individual record that might be accessed from a `DataHandler`.
    Implements _most_ of the `dict` interface, but, to make things a bit easier when
    pickling, is not implemented as a proper subclass of `dict`.
    """
    def __init__(self, data_handler, key, records):
        self.data = records
        self.handler = data_handler
        self.key = key

    def keys(self):
        return self.data.keys()
    def values(self):
        return self.data.keys()
    def items(self):
        return self.data.keys()

    def __getitem__(self, item):
        return self.data[item]

    def __repr__(self):
        return "{}('{}', {})".format(
            type(self).__name__,
            self.key,
            self.handler
        )

    # implementing to make pickling of data objects possible...
    def __getstate__(self):
        # it turns out we really need the dict.copy()...?
        state = self.__dict__.copy()
        del state['data']
        return state
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.data = self.handler._get_data(self.key)
