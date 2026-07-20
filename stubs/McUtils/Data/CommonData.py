"""
Defines a common data handler
"""
import os, sys
__all__ = ['DataHandler', 'DataError', 'DataRecord']
default_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
default_data_package = 'TheRealMcCoy'
default_data_key = 'data'
default_data_source_key = 'source'

class DataError(KeyError):
    """
    Exception subclass for data error
    """

class DataHandler:
    """
    Defines a general data loader class that we can use for `AtomData` and any other data classes we might find useful.
    """

    def __init__(self, data_name, data_key=None, source_key=None, data_dir=None, data_pkg=None, alternate_keys=None, getter=None, record_type=None):
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
        ...

    @property
    def data_file(self):
        ...

    def _load_alts(self):
        ...

    def load(self, env=None):
        """
        Actually loads the data from `data_file`.
        Currently set up to just use an `import` statement but should
        be reimplemented to use a `Deserializer` from `Scaffolding.Serializers`

        :return:
        :rtype:
        """
        ...

    @property
    def data(self):
        ...

    @property
    def source(self):
        ...

    def _get_data(self, key):
        ...

    def __getitem__(self, key):
        ...

    def __len__(self):
        ...

    def __iter__(self):
        ...

    def __getstate__(self):
        ...

    def __setstate__(self, state):
        ...

    def __repr__(self):
        ...

class DataRecord:
    """
    Represents an individual record that might be accessed from a `DataHandler`.
    Implements _most_ of the `dict` interface, but, to make things a bit easier when
    pickling, is not implemented as a proper subclass of `dict`.
    """

    def __init__(self, data_handler, key, records):
        ...

    def keys(self):
        ...

    def values(self):
        ...

    def items(self):
        ...

    def __getitem__(self, item):
        ...

    def __repr__(self):
        ...

    def __getstate__(self):
        ...

    def __setstate__(self, state):
        ...