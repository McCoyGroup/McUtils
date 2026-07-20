from ..Data import AtomData
import abc, typing
__all__ = ['ExternalMolecule']

class ExternalMolecule(metaclass=abc.ABCMeta):
    """
    Defines a common interface so that a programs can define one interface and not need to
    adjust for every new type of chemistry package they want to support.
    Not all properties need to be well-defined on every type of molecule, but this defines the core interface
    that _must_ be implemented
    """

    def __init__(self, external_mol):
        ...

    @property
    @abc.abstractmethod
    def atoms(self):
        ...

    @property
    @abc.abstractmethod
    def coords(self):
        ...

    @property
    def masses(self):
        ...

    @property
    def bonds(self):
        ...

    @property
    def charges(self):
        ...

    @classmethod
    @abc.abstractmethod
    def from_coords(cls, atoms, coords, **etc) -> 'typing.Self':
        ...

    @classmethod
    def from_mol(cls, atoms, coords, **etc) -> 'typing.Self':
        ...

    def show(self):
        ...