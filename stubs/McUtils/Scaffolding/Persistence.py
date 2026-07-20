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
__all__ = ['PersistenceLocation', 'PersistenceManager', 'ResourceManager']

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
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Render the location name, path, and cleanup policy.

        :return: A human-readable string representation.
        :rtype: str
        """
        ...

    def __del__(self):
        """
        **LLM Docstring**

        Recursively delete the location when its cleanup flag is enabled, ignoring filesystem errors.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

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
        ...

    def obj_loc(self, key):
        """
        **LLM Docstring**

        Construct the directory path for a persistent object key.

        :param key: the storage or lookup key
        :type key: object
        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        ...

    def load_config(self, key, make_new=False, init=None):
        """
        Loads the config for the persistent structure named `key`
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

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
        ...

    def contains(self, key):
        """
        Checks if `key` is a supported persistent structure

        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def load(self, key, make_new=False, strict=True, init=None):
        """
        Loads the persistent structure named `key`

        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    def save(self, obj):
        """
        Saves requisite config data for a structure

        :param obj:
        :type obj:
        :return:
        :rtype:
        """
        ...

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
        ...
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
        ...

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
        ...

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
        ...

    def get_resource_path(self, *path):
        """
        **LLM Docstring**

        Join the base location, resource namespace, and optional subpath components.

        :param path: additional resource path components
        :type path: object
        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        ...
    blacklist_files = ['.DS_Store']

    def list_resources(self):
        """
        **LLM Docstring**

        Ensure the resource directory exists and map non-blacklisted entry names to their paths.

        :return: a mapping from resource names to filesystem paths
        :rtype: dict[str, str]
        """
        ...
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
        ...

    def load_resource(self, loc):
        """
        **LLM Docstring**

        Read and decode a resource in binary, text, or JSON mode according to class flags.

        :param loc: filesystem location
        :type loc: object
        :return: decoded JSON data, text, or bytes according to class flags
        :rtype: object | str | bytes
        """
        ...

    def get_metadata_filename(self, name):
        """
        **LLM Docstring**

        Derive the sidecar metadata filename by appending `.meta.json`.

        :param name: registry, command, resource, or object name
        :type name: object
        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        ...

    def get_resource_metadata(self, loc):
        """
        **LLM Docstring**

        Default metadata hook, currently returning an empty dictionary.

        :param loc: filesystem location
        :type loc: object
        :return: an empty metadata mapping in the base implementation
        :rtype: dict
        """
        ...

    def get_resource_filename(self, name):
        """
        **LLM Docstring**

        Default filename hook, currently returning the resource name unchanged.

        :param name: registry, command, resource, or object name
        :type name: object
        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        ...
    resource_function = None

    def get_resource(self, name, resource_function=None, load_resource=True):
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
        ...