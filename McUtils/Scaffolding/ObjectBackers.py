"""
Provides interfaces that _support_ objects
and make it easier to build more reliable,
higher-functioning classes
"""

import abc, os

from .Persistence import PersistenceLocation
from .Checkpointing import NumPyCheckpointer

__all__ = ["BaseObjectManager", "FileBackedObjectManager"]

class BaseObjectManager(metaclass=abc.ABCMeta):
    """
    Defines the basic parameters of an object interface
    that can handle marshalling the core data behind
    and object attribute to disk or vice versa
    """

    def __init__(self, obj):
        """
        **LLM Docstring**

        Associate the manager with an object and initialize lazy basename storage.

        :param obj: object to serialize or manage
        :type obj: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.obj = obj
        self._base_name = None

    def get_basename(self):
        """
        **LLM Docstring**

        Build a storage basename from the object type and its `serialization_id` or runtime identity.

        :return: the generated storage basename
        :rtype: str
        """
        if hasattr(self.obj, 'serialization_id'):
            obj_id = self.obj.serialization_id
        else:
            obj_id = id(self.obj)
        return "{}_{}".format(type(self.obj).__name__, obj_id)

    @property
    def basename(self):
        """
        **LLM Docstring**

        Lazily compute and cache the manager basename.

        :return: The resolved filesystem path or basename.
        :rtype: str
        """
        if self._base_name is None:
            self._base_name = self.get_basename()
        return self._base_name

    @abc.abstractmethod
    def save_attr(self, attr):
        """
        Saves some attribute of the object

        :param attr:
        :type attr:
        :return:
        :rtype:
        """
        raise NotImplementedError("abstract interface")

    @abc.abstractmethod
    def load_attr(self, attr):
        """
        Loads some attribute of the object

        :param attr:
        :type attr:
        :return:
        :rtype:
        """
        raise NotImplementedError("abstract interface")

    @abc.abstractmethod
    def del_attr(self, attr):
        """
        Deletes some attribute of the object

        :param attr:
        :type attr:
        :return:
        :rtype:
        """
        raise NotImplementedError("abstract interface")

class FileBackedObjectManager(BaseObjectManager):
    """
    Provides an interface to back an object with
    a serializer
    """

    default_directory = None
    def __init__(self,
                 obj,
                 chk=None,
                 loc=None,
                 checkpoint_class=NumPyCheckpointer
                 ):
        """
        :param obj: the object to back
        :type obj: object
        :param chk: a checkpointer to manage storing attributes
        :type chk: Checkpointer
        :param loc: the location where attributes should be stored
        :type loc: str
        :param checkpoint_class: a subclass of Checkpointer that implements the actual writing to disk
        :type checkpoint_class: Type[Checkpointer]
        """
        super().__init__(obj)
        if chk is None:
            if loc is None:
                loc = self.get_default_directory().loc
            obj_file = os.path.join(loc, self.basename+checkpoint_class.default_extension)
            chk = checkpoint_class(obj_file)

        self.chk = chk
        self._id = None
        self._cache = {}

    @classmethod
    def get_default_directory(cls):
        """
        **LLM Docstring**

        Create or return the shared persistence location used for file-backed objects.

        :return: The resolved or newly constructed helper object.
        :rtype: object
        """
        if cls.default_directory is None:
            cls.default_directory = PersistenceLocation("file_backed_objects")
        return cls.default_directory

    @property
    def basename(self):
        """
        **LLM Docstring**

        Get or set the explicit file tag used as the manager basename.

        :param v: new explicit backing-file tag
        :type v: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        if self._tag is None:
            self._tag = self.get_basename()
        return self.basename
    @basename.setter
    def basename(self, v):
        """
        **LLM Docstring**

        Get or set the explicit file tag used as the manager basename.

        :param v: new explicit backing-file tag
        :type v: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self._tag = v

    def get_basename(self):
        """
        **LLM Docstring**

        Build the default file tag from the managed object type and stable or runtime identity.

        :return: the generated file tag
        :rtype: str
        """
        if hasattr(self.obj, 'serialization_id'):
            obj_id = self.obj.serialization_id
        else:
            obj_id = id(self.obj)
        return "{}_{}".format(type(self.obj).__name__, obj_id)

    def save_attr(self, attr):
        """
        **LLM Docstring**

        Checkpoint an object attribute and return a marker describing the file-backed attribute.

        :param attr: attribute name
        :type attr: object
        :return: No explicit value unless noted by the underlying delegated operation.
        :rtype: None | object
        """
        with self.chk:
            self.chk[attr] = getattr(self.obj, attr)
        return FileBackedAttribute(self, attr)

    def load_attr(self, attr):
        """
        **LLM Docstring**

        Load an attribute value from the backing checkpointer.

        :param attr: attribute name
        :type attr: object
        :return: The reconstructed, loaded, or selected Python value.
        :rtype: object
        """
        with self.chk:
            return self.chk[attr]

class FileBackedAttribute:
    """
    A helper class to make it very clear that
    an attribute is backed by a file on disk
    """

    def __init__(self, manager, attr):
        """
        **LLM Docstring**

        Record the manager and attribute name represented by this file-backed marker.

        :param manager: owning object manager
        :type manager: object
        :param attr: attribute name
        :type attr: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        self.manager = manager
        self.attr = attr