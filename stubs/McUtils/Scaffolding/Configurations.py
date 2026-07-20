"""
Provides functionality for managing configurations stored in files
without having to write bespoke serialization/deserialization/application
code every time a new job type comes up
"""
import os, inspect
from .Serializers import *
from ..Devutils import OptionsSet
__all__ = ['Config', 'ParameterManager']

class Config:
    """
    A configuration object which basically just supports
    a dictionary interface, but which also can automatically
    filter itself so that it only provides the keywords supported
    by a `from_config` method.
    """

    def __init__(self, config, serializer=None, extra_params=None):
        """Loads the config from a file
        :param config:
        :type config: str
        :param serializer:
        :type serializer: None | BaseSerializer
        """
        ...
    config_file_name = 'config'
    config_file_extensions = ['.json', '.yml', '.yaml', '.py']

    @classmethod
    def find_config(self, config, name=None, extensions=None):
        """
        Finds configuration file (if config isn't a file)

        :param config:
        :type config:
        :return:
        :rtype:
        """
        ...
    _serializer_map = {'.py': ModuleSerializer, '.json': JSONSerializer, '.yaml': YAMLSerializer, '.yml': YAMLSerializer}

    @classmethod
    def get_serializer(self, file):
        """
        **LLM Docstring**

        Select a serializer instance from the configuration file extension.

        :param file: path or file-like object
        :type file: object
        :return: The resolved or newly constructed helper object.
        :rtype: object
        """
        ...

    @classmethod
    def new(cls, loc, init=None):
        """
        **LLM Docstring**

        Create the default JSON configuration file in a directory and initialize it with the supplied mapping.

        :param loc: filesystem location
        :type loc: object
        :param init: initial configuration mapping or source
        :type init: object
        :return: The newly constructed object.
        :rtype: object
        """
        ...

    def serialize(self, file, ops):
        """
        **LLM Docstring**

        Choose the configured or extension-derived serializer and write options to a text file.

        :param file: path or file-like object
        :type file: object
        :param ops: options mapping to serialize
        :type ops: object
        :return: No explicit value unless noted by the underlying delegated operation.
        :rtype: None | object
        """
        ...

    def deserialize(self, file):
        """
        **LLM Docstring**

        Choose the configured or extension-derived serializer and read options from a text file.

        :param file: path or file-like object
        :type file: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    def save(self):
        """
        **LLM Docstring**

        Serialize the current merged option dictionary back to the configuration file.

        :return: No explicit value unless noted by the underlying delegated operation.
        :rtype: None | object
        """
        ...

    def load(self):
        """
        **LLM Docstring**

        Deserialize and return the raw configuration file contents.

        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...

    @property
    def name(self):
        """
        **LLM Docstring**

        Return the configured `name`, falling back to the configuration filename when absent.

        :return: the configured name or configuration filename
        :rtype: str
        """
        ...

    @property
    def opt_dict(self):
        """
        **LLM Docstring**

        Return loaded configuration values merged with runtime-only extra parameters.

        :return: a new dictionary containing file options plus runtime extras
        :rtype: dict
        """
        ...

    def filter(self, keys, strict=True):
        """
        Returns a filtered option dictionary according to keys.
        Strict mode will raise an error if there is a key in the config that isn't
        in keys.

        :param keys:
        :type keys: Iterable[str] | function
        :param strict:
        :type strict: bool
        :return:
        :rtype:
        """
        ...

    def apply(self, func, strict=True):
        """
        Applies func to stored parameters

        :param func:
        :type func:
        :return:
        :rtype:
        """
        ...

    def update(self, **kw):
        """
        **LLM Docstring**

        Merge keyword updates into the current option dictionary and persist the result.

        :param kw: keyword values merged into the current configuration
        :type kw: object
        :return: no explicit value; the configuration file is rewritten
        :rtype: None
        """
        ...

    def load_opts(self):
        """
        **LLM Docstring**

        Load the configuration once and add its containing directory as `config_location`.

        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def get_conf_attr(self, item):
        """
        **LLM Docstring**

        Read a value from the loaded configuration object using item or attribute access according to its stored type.

        :param item: the lookup key or index
        :type item: object
        :return: the selected configuration value
        :rtype: object
        """
        ...

    def __getattr__(self, item):
        """
        **LLM Docstring**

        Forward unresolved attributes to the loaded configuration data.

        :param item: the lookup key or index
        :type item: object
        :return: the selected configuration value
        :rtype: object
        """
        ...

class ParameterManager(OptionsSet):

    def serialize(self, file, mode=None):
        """
        **LLM Docstring**

        Write the managed options as a Python module configuration through `ModuleSerializer`.

        :param file: path or file-like object
        :type file: object
        :param mode: serialization or dispatch mode
        :type mode: object
        :return: No explicit value unless noted by the underlying delegated operation.
        :rtype: None | object
        """
        ...

    @classmethod
    def deserialize(cls, file, mode=None, attribute=None):
        """
        **LLM Docstring**

        Load options from a Python module, optionally selecting an attribute.

        :param file: path or file-like object
        :type file: object
        :param mode: serialization or dispatch mode
        :type mode: object
        :param attribute: module attribute to load
        :type attribute: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        ...