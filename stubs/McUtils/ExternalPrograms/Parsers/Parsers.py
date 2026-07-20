import importlib
from ...Parsers import FileStreamReader, FileStreamCheckPoint, FileStreamReaderException
__all__ = ['ElectronicStructureLogReader']

class ElectronicStructureLogReader(FileStreamReader):
    """
    Implements a stream based reader for a generic electronic structure .log file.
    This is inherits from the `FileStreamReader` base, and takes a two pronged approach to getting data.
    First, a block is found in a log file based on a pair of tags.
    Next, a function (usually based on a `StringParser`) is applied to this data to convert it into a usable data format.
    The goal is to move toward wrapping all returned data in a `QuantityArray` so as to include data type information, too.
    """
    components_name = None
    components_package = '.LogComponents'
    _comps = None

    @classmethod
    def load_components(cls):
        """
        **LLM Docstring**

        Import (and cache) the module registering this reader's parse components (the
        block tag/parser table), resolving a relative `components_package`.

        :return: the loaded components module
        :rtype: module
        """
        ...

    @property
    def registered_components(self):
        """
        **LLM Docstring**

        The mapping of component name to its block specification (tags, parser, mode),
        taken from the loaded components module.

        :return: the registered components
        :rtype: dict
        """
        ...

    @property
    def default_keys(self):
        """
        **LLM Docstring**

        The default set of component keys to parse, taken from the loaded components
        module.

        :return: the default keys
        :rtype: tuple
        """
        ...

    @property
    def default_ordering(self):
        """
        **LLM Docstring**

        The default parse ordering for the components, taken from the loaded components
        module.

        :return: the ordering mapping
        :rtype: dict
        """
        ...

    def parse(self, keys, num=None, reset=False):
        """The main function we'll actually use. Parses bits out of a .log file.

        :param keys: the keys we'd like to read from the log file
        :type keys: str or list(str)
        :param num: for keys with multiple entries, the number of entries to pull
        :type num: int or None
        :return: the data pulled from the log file, strung together as a `dict` and keyed by the _keys_
        :rtype: dict
        """
        ...

    @classmethod
    def read_props(cls, file, keys):
        """
        **LLM Docstring**

        Convenience classmethod: open `file`, parse the requested keys, and return the
        result (unwrapped to the single value when one key is given).

        :param file: the log file
        :type file: str
        :param keys: the component key(s) to read
        :type keys: str | list[str]
        :return: the parsed data
        :rtype: dict | Any
        """
        ...