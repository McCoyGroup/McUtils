"""
Provides utilities for managing object persistence.
Two classes of persistence are provided.
 1. Config persistence: stores objects by turning them into a
    set of config variables & provides reloading
 2. File-backed objects: stores objects by making serializing core
    pieces of the data
"""
import json
import os, shutil, tempfile as tf, weakref

from .Checkpointing import Checkpointer, NumPyCheckpointer
from .Configurations import Config

__all__ = [
    "PersistenceLocation",
    "PersistenceManager",
    "ResourceManager"
]

class PersistenceLocation:
    """
    An object that tracks a location to persist data
    and whether or not that data should be cleaned up on
    exit
    """
    _cache = weakref.WeakValueDictionary()
    def __init__(self, loc, name=None, delete=None):
        """
        **LLM Docstring**

        Normalize a persistence path, infer temporary cleanup behavior, and coordinate deletion policy among cached references to the same location.

        :param loc: filesystem location
        :type loc: object
        :param name: registry, command, resource, or object name
        :type name: object
        :param delete: whether the location should be recursively deleted when the tracker is collected
        :type delete: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        if name is None:
            name = os.path.basename(loc)
        self.name = name

        if delete is None:
            delete = not os.path.isdir(loc)

        absloc = os.path.abspath(loc)
        if not os.path.isdir(absloc):
            if absloc != loc:
                loc = os.path.join(tf.TemporaryDirectory().name, loc)
        else:
            loc = absloc

        # all it takes is a single location
        # saying "don't delete" for us to not
        # delete...note that if the location
        # dies and then is reborn as a deletable
        # then it will be deleted
        for k,v in self._cache.items():
            if v.loc == loc:
                if not delete:
                    v.delete = False
                elif not v.delete:
                    delete = False

        self.loc = loc
        self.delete = delete

        self._cache[loc] = self

    def __repr__(self):
        """
        **LLM Docstring**

        Render the location name, path, and cleanup policy.

        :return: A human-readable string representation.
        :rtype: str
        """
        return "{}({}, {}, delete={})".format(
            type(self).__name__,
            self.name,
            self.loc,
            self.delete
        )

    def __del__(self):
        """
        **LLM Docstring**

        Recursively delete the location when its cleanup flag is enabled, ignoring filesystem errors.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        if self.delete:
            try:
                shutil.rmtree(self.loc)
            except OSError:
                pass

class PersistenceManager:
    """
    Defines a manager that can load configuration data from a directory
    or, maybe in the future, a SQL database or similar.
    Requires class that supports `from_config` to load and `to_config` to save.
    """
    def __init__(self, cls, persistence_loc=None):
        """
        :param cls:
        :type cls: type
        :param persistence_loc: location from which to load/save objects
        :type persistence_loc: str | None
        """
        self.cls = cls
        if persistence_loc is None:
            if not hasattr(cls, 'persistence_loc'):
                raise AttributeError("{me}: to support persistence either a '{ploc}'' must be passed or {cls} needs the attribute '{ploc}'".format(
                    me=type(self).__name__,
                    cls=cls.__name__,
                    ploc=persistence_loc
                ))
            persistence_loc = cls.persistence_loc
        self.loc = persistence_loc

    def obj_loc(self, key):
        """
        **LLM Docstring**

        Construct the directory path for a persistent object key.

        :param key: the storage or lookup key
        :type key: object
        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        return os.path.join(self.loc, key)

    def load_config(self, key, make_new=False, init=None):
        """
        Loads the config for the persistent structure named `key`
        :param key:
        :type key:
        :return:
        :rtype:
        """
        if self.contains(key):
            return Config(self.obj_loc(key), extra_params=init)
        elif make_new:
            return self.new_config(key, init=init)
        else:
            raise KeyError("{}: no persistent object {}".format(
                type(self).__name__,
                key
            ))

    def new_config(self, key, init=None):
        """
        Creates a new space and config for the persistent structure named `key`

        :param key: name for job
        :type key: str
        :param init: initial parameters
        :type init: str | dict | None
        :return:
        :rtype:
        """
        loc = self.obj_loc(key)
        if init is None:
            init = {}
        elif isinstance(init, str):
            if os.path.isdir(init):
                init_dir = init
                init = Config(init).opt_dict
                if 'initialization_directory' not in init:
                    init['initialization_directory'] = init_dir
            else:
                init = Config(init).opt_dict

        if not os.path.isdir(loc):
            if 'initialization_directory' in init:
                shutil.copytree(
                    init['initialization_directory'],
                    loc
                )
            else:
                os.makedirs(loc, exist_ok=True)

        # now we prune, because we don't want to preserve this forever...
        if 'initialization_directory' in init:
            del init['initialization_directory']

        if Config.find_config(loc) is None:
            return Config.new(loc, init=init)
        else:
            conf = Config(loc)
            if len(init) > 0:
                conf.update(**init)
            return conf

    def contains(self, key):
        """
        Checks if `key` is a supported persistent structure

        :param key:
        :type key:
        :return:
        :rtype:
        """
        return os.path.isdir(self.obj_loc(key))

    def load(self, key, make_new=False, strict=True, init=None):
        """
        Loads the persistent structure named `key`

        :param key:
        :type key:
        :return:
        :rtype:
        """
        cfg = self.load_config(key, make_new=make_new, init=init)
        try:
            loader = self.cls.from_config
        except AttributeError:
            loader = None
        if loader is None:
            raise AttributeError("{}.{}: to support persistence {} has to have a classmethod '{}'".format(
                type(self).__name__,
                'load',
                self.cls,
                'from_config'
            ))
        return cfg.apply(loader, strict=strict)
    def save(self, obj):
        """
        Saves requisite config data for a structure

        :param obj:
        :type obj:
        :return:
        :rtype:
        """
        if not isinstance(obj, self.cls):
            raise TypeError("{}.{}: object {} isn't of persistence type {}".format(
                type(self).__name__,
                'save',
                obj,
                self.cls.__name__
            ))

        try:
            loader = obj.to_config
        except AttributeError:
            loader = None
        if loader is None:
            raise AttributeError("{}.{}: to support persistence {} has to have a classmethod '{}'".format(
                type(self).__name__,
                'save',
                self.cls,
                'to_config'
            ))
        data = loader()

        key = data['name']
        cfg = self.load_config(key, make_new=True)
        cfg.update(**data)

class ResourceManager:
    """
    A very simple framework for writing resources to a given directory
    Designed to be extended and to support metadata
    """

    default_resource_name = 'resource'
    def __init__(self, name=None, location=None, write_metadata=False, temporary=None):
        """
        **LLM Docstring**

        Configure resource namespace, base location, metadata preference, and temporary-location policy.

        :param name: registry, command, resource, or object name
        :type name: object
        :param location: explicit resource base directory, or `None` to resolve the class default
        :type location: object
        :param write_metadata: whether resource metadata should be written
        :type write_metadata: object
        :param temporary: whether a temporary base directory should be used
        :type temporary: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.name = self.default_resource_name if name is None else name
        self.location = self.get_base_location(temporary=temporary) if location is None else location
        self.write_metadata = write_metadata

    base_location = None
    location_env_var = None
    use_temporary = True
    @classmethod
    def resolve_shared_directory(cls):
        """
        **LLM Docstring**

        Return the user-local shared resource directory `~/.local`.

        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        #TODO: make this less Unix specific
        return os.path.expanduser('~/.local')
    @classmethod
    def get_default_base_location(cls, temporary=None):
        """
        **LLM Docstring**

        Choose a new temporary directory or the shared user directory.

        :param temporary: whether a temporary base directory should be used
        :type temporary: object
        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        if temporary:
            return tf.TemporaryDirectory().name
        else:
            return cls.resolve_shared_directory()
    @classmethod
    def get_base_location(cls, temporary=True):
        """
        **LLM Docstring**

        Lazily resolve and cache the class base directory from an environment variable or default location.

        :param temporary: whether a temporary base directory should be used
        :type temporary: object
        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        if cls.base_location is None:
            if cls.location_env_var is not None:
                cls.base_location = os.environ.get(cls.location_env_var)
            if cls.base_location is None:
                cls.base_location = cls.get_default_base_location(temporary=temporary)
        return cls.base_location

    def get_resource_path(self, *path):
        """
        **LLM Docstring**

        Join the base location, resource namespace, and optional subpath components.

        :param path: additional resource path components
        :type path: object
        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        return os.path.join(self.location, self.name, *path)

    blacklist_files = ['.DS_Store']
    def list_resources(self):
        """
        **LLM Docstring**

        Ensure the resource directory exists and map non-blacklisted entry names to their paths.

        :return: a mapping from resource names to filesystem paths
        :rtype: dict[str, str]
        """
        base_dir = self.get_resource_path()
        os.makedirs(base_dir, exist_ok=True)
        return {
            p:os.path.join(base_dir, p)
            for p in os.listdir(base_dir)
            if p not in self.blacklist_files
        }

    binary_resource = True
    json_resource = False
    def save_resource(self, loc, val):
        """
        **LLM Docstring**

        Write a resource in binary, text, or JSON mode according to class flags.

        :param loc: filesystem location
        :type loc: object
        :param val: the value being stored, converted, or installed
        :type val: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        with open(loc, 'w+' if not self.binary_resource else 'wb') as res_file:
            if self.json_resource:
                json.dump(res_file, val)
            else:
                res_file.write(val)
    def load_resource(self, loc):
        """
        **LLM Docstring**

        Read and decode a resource in binary, text, or JSON mode according to class flags.

        :param loc: filesystem location
        :type loc: object
        :return: decoded JSON data, text, or bytes according to class flags
        :rtype: object | str | bytes
        """
        with open(loc, 'r' if not self.binary_resource else 'rb') as res_file:
            if self.json_resource:
                return json.load(res_file)
            else:
                return res_file.read()

    def get_metadata_filename(self, name):
        """
        **LLM Docstring**

        Derive the sidecar metadata filename by appending `.meta.json`.

        :param name: registry, command, resource, or object name
        :type name: object
        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        return name + '.meta.json'
    def get_resource_metadata(self, loc):
        """
        **LLM Docstring**

        Default metadata hook, currently returning an empty dictionary.

        :param loc: filesystem location
        :type loc: object
        :return: an empty metadata mapping in the base implementation
        :rtype: dict
        """
        return {}
    def get_resource_filename(self, name):
        """
        **LLM Docstring**

        Default filename hook, currently returning the resource name unchanged.

        :param name: registry, command, resource, or object name
        :type name: object
        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        return name

    resource_function = None
    def get_resource(self, name,
                     resource_function=None,
                     load_resource=True):
        """
        **LLM Docstring**

        Return an existing resource, or generate and persist it with the configured factory before loading it.

        :param name: registry, command, resource, or object name
        :type name: object
        :param resource_function: factory used to create a missing resource
        :type resource_function: object
        :param load_resource: whether to return loaded content instead of its path
        :type load_resource: object
        :return: loaded resource content, its path when `load_resource=False`, or `None` when unavailable
        :rtype: object | str | None
        """
        resource_file = self.get_resource_filename(name)
        loc = self.get_resource_path(resource_file)
        if not os.path.exists(loc):
            base_dir = self.get_resource_path()
            os.makedirs(base_dir, exist_ok=True)
            if resource_function is None:
                resource_function = self.resource_function
            if resource_function is not None:
                default_val = resource_function(name)
                self.save_resource(loc, default_val)
            else:
                return None
        if load_resource:
            return self.load_resource(loc)
        else:
            return loc