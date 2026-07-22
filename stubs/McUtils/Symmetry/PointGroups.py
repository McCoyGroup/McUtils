import abc
import enum
import numpy as np
from .. import Devutils as dev
from .. import Numputils as nput
from .Characters import *
from .Elements import *
__all__ = ['NamedPointGroups', 'ParametrizedPointGroups', 'PointGroup']

class NamedPointGroups(enum.Enum):
    """Real access pattern: NamedPointGroups.<MemberName> (this is an enum with 8 members, e.g. NamedPointGroups.Ih == 'Ih'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
    _MEMBERS = {'Ih': 'Ih', 'I': 'I', 'Oh': 'Oh', 'O': 'O', 'Th': 'Th', 'Td': 'Td', 'T': 'T', 'Cs': 'Cs'}

class ParametrizedPointGroups(enum.Enum):
    """Real access pattern: ParametrizedPointGroups.<MemberName> (this is an enum with 7 members, e.g. ParametrizedPointGroups.C == 'C'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
    _MEMBERS = {'C': 'C', 'Ch': 'Ch', 'Cv': 'Cv', 'D': 'D', 'Dh': 'Dh', 'Dd': 'Dd', 'S': 'S'}

class PointGroup(metaclass=abc.ABCMeta):
    group: 'NamedPointGroups|ParametrizedPointGroups'

    def __init__(self, character_table=None, elements=None, axes=None):
        """
        **LLM Docstring**

        Initialize lazy caches for the character table, symmetry elements, and embedding axes.

        :param character_table: Optional precomputed character table. Defaults to `None`.
        :type character_table: object
        :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
        :type elements: object
        :param axes: Requested Cartesian embedding axes. Defaults to `None`.
        :type axes: object
        :return: No value is returned.
        :rtype: None
        """
        ...

    def get_modification_kwargs(self, character_table=dev.default, elements=dev.default, axes=dev.default):
        """
        **LLM Docstring**

        Resolve modification sentinels into a complete constructor argument mapping.

        :param character_table: Optional precomputed character table. Defaults to `dev.default`.
        :type character_table: object
        :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `dev.default`.
        :type elements: object
        :param axes: Requested Cartesian embedding axes. Defaults to `dev.default`.
        :type axes: object
        :return: Constructor keyword arguments for a modified point-group copy.
        :rtype: dict
        """
        ...

    def modify(self, character_table=dev.default, elements=dev.default, axes=dev.default):
        """
        **LLM Docstring**

        Return a new point-group object with selected cached data or axes replaced.

        :param character_table: Optional precomputed character table. Defaults to `dev.default`.
        :type character_table: object
        :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `dev.default`.
        :type elements: object
        :param axes: Requested Cartesian embedding axes. Defaults to `dev.default`.
        :type axes: object
        :return: The modified point-group instance.
        :rtype: PointGroup
        """
        ...

    @abc.abstractmethod
    def get_name(self):
        """
        **LLM Docstring**

        Return the conventional point-group name.

        :return: The point-group name.
        :rtype: str
        """
        ...

    @property
    def name(self):
        """
        **LLM Docstring**

        Return the conventional point-group name.

        :return: The point-group name.
        :rtype: str
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a diagnostic string describing the symmetry element.

        :return: The representation string.
        :rtype: str
        """
        ...

    @classmethod
    def from_name(cls, key, n=None, **etc):
        """
        **LLM Docstring**

        Parse fixed and parametrized point-group names and construct the corresponding concrete group object.

        :param key: Point-group family key or fixed group name.
        :type key: object
        :param n: Group order or problem size used to construct the requested representation. Defaults to `None`.
        :type n: object
        :param etc: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
        :type etc: dict
        :return: The constructed point group.
        :rtype: PointGroup
        """
        ...

    @classmethod
    def get_symmetry_element_primary_rotation(cls, elements: 'Iterable[SymmetryElement]'):
        """
        **LLM Docstring**

        Select a highest-order proper rotation element and report how many elements share that order.

        :param elements: Selected group elements or element indices; `None` requests the full set.
        :type elements: 'Iterable[SymmetryElement]'
        :return: The selected rotation and its multiplicity, or `(None, None)` when absent.
        :rtype: tuple[RotationElement | None, int | None]
        """
        ...

    @classmethod
    def from_symmetry_elements(cls, elements: list[SymmetryElement], tol=0.01):
        """
        **LLM Docstring**

        Infer a low- or axial-symmetry point-group family from supplied symmetry elements; high-symmetry branches remain unimplemented.

        :param elements: Selected group elements or element indices; `None` requests the full set.
        :type elements: list[SymmetryElement]
        :param tol: Numerical tolerance used for geometric or equality tests. Defaults to `0.01`.
        :type tol: object
        :return: The inferred point group.
        :rtype: PointGroup
        """
        ...

    def get_symmetry_elements(self, only_class_representatives=True):
        """
        **LLM Docstring**

        Convert representative or full operation matrices into symmetry-element objects and embed them in requested axes.

        :param only_class_representatives: Whether to return one operation per conjugacy class rather than every group operation. Defaults to `True`.
        :type only_class_representatives: object
        :return: The symmetry elements.
        :rtype: tuple[SymmetryElement, ...] | list[SymmetryElement]
        """
        ...

    @property
    def character_table(self) -> CharacterTable:
        """
        **LLM Docstring**

        Lazily construct and cache the group character table.

        :return: The character table.
        :rtype: CharacterTable
        """
        ...

    @property
    def elements(self) -> 'tuple[SymmetryElement]':
        """
        **LLM Docstring**

        Lazily construct and cache representative symmetry elements.

        :return: The symmetry elements.
        :rtype: tuple[SymmetryElement, ...]
        """
        ...

    @abc.abstractmethod
    def get_character_table(self):
        """
        **LLM Docstring**

        Construct the hard-coded or analytic character table for the `get` group family.

        :return: The square character table with irreducible representations along rows.
        :rtype: np.ndarray
        """
        ...

    @abc.abstractmethod
    def get_all_character_matrices(self):
        """
        **LLM Docstring**

        Build the three-dimensional Cartesian matrix representation for selected group elements.

        :return: An array of shape `(n_elements, 3, 3)`.
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def get_axes_from_symmetry_elements(cls, elements):
        """
        **LLM Docstring**

        Choose primary and secondary molecular axes from rotations and reflection planes, then build an orthonormal view matrix.

        :param elements: Selected group elements or element indices; `None` requests the full set.
        :type elements: object
        :return: A `3 x 3` axis matrix.
        :rtype: np.ndarray
        """
        ...

    def get_axes(self, elements=None, base_axes=False):
        """
        **LLM Docstring**

        Determine embedding axes from supplied, cached, or base representative elements.

        :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
        :type elements: object
        :param base_axes: Value used as `base_axes` by the implementation. Defaults to `False`.
        :type base_axes: object
        :return: A `3 x 3` axis matrix.
        :rtype: np.ndarray
        """
        ...

    @property
    def axes(self):
        """
        **LLM Docstring**

        Lazily determine and cache the embedded or canonical point-group axes.

        :return: A `3 x 3` axis matrix.
        :rtype: np.ndarray
        """
        ...

    @property
    def base_axes(self):
        """
        **LLM Docstring**

        Lazily determine and cache the embedded or canonical point-group axes.

        :return: A `3 x 3` axis matrix.
        :rtype: np.ndarray
        """
        ...

    def align(self, axes):
        """
        **LLM Docstring**

        Return a copy aligned to explicitly supplied axes, transforming cached elements consistently.

        :param axes: Requested Cartesian embedding axes.
        :type axes: object
        :return: The aligned point group.
        :rtype: PointGroup
        """
        ...

    def transform(self, tf):
        """
        **LLM Docstring**

        Express the symmetry element in a transformed Cartesian basis.

        :param tf: A `3 x 3` change-of-basis transformation.
        :type tf: object
        :return: A symmetry element with its defining axis transformed by `tf`.
        :rtype: SymmetryElement
        """
        ...

    def get_matrices(self, only_class_representatives=True):
        """
        **LLM Docstring**

        Build the three-dimensional Cartesian matrix representation for selected group elements.

        :param only_class_representatives: Whether to return one operation per conjugacy class rather than every group operation. Defaults to `True`.
        :type only_class_representatives: object
        :return: An array of shape `(n_elements, 3, 3)`.
        :rtype: np.ndarray
        """
        ...

    def plot(self, figure=None, elements=None, origin=None, inversion_styles=None, rotation_styles=None, reflection_styles=None, improper_rotation_styles=None, **opts):
        """
        **LLM Docstring**

        Add graphical primitives representing this symmetry element to a figure.

        :param figure: Plotting figure that receives generated graphics primitives. Defaults to `None`.
        :type figure: object
        :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
        :type elements: object
        :param origin: Plot origin. Defaults to `None`.
        :type origin: object
        :param inversion_styles: Style overrides for inversion elements. Defaults to `None`.
        :type inversion_styles: object
        :param rotation_styles: Style overrides for rotation elements. Defaults to `None`.
        :type rotation_styles: object
        :param reflection_styles: Style overrides for reflection elements. Defaults to `None`.
        :type reflection_styles: object
        :param improper_rotation_styles: Style overrides for improper-rotation elements. Defaults to `None`.
        :type improper_rotation_styles: object
        :param opts: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
        :type opts: dict
        :return: The plotted primitive or list of plotted primitives.
        :rtype: object
        """
        ...

class NamedPointGroup(PointGroup):

    def __init__(self, name: 'str|NamedPointGroups', character_table=None, elements=None, axes=None):
        """
        **LLM Docstring**

        Execute the implementation of `NamedPointGroup.__init__`.

        :param name: Point-group name or enum member.
        :type name: 'str|NamedPointGroups'
        :param character_table: Optional precomputed character table. Defaults to `None`.
        :type character_table: object
        :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
        :type elements: object
        :param axes: Requested Cartesian embedding axes. Defaults to `None`.
        :type axes: object
        :return: The value produced by the implementation.
        :rtype: object
        """
        ...

    def modify(self, character_table=dev.default, elements=dev.default, axes=dev.default):
        """
        **LLM Docstring**

        Return a new point-group object with selected cached data or axes replaced.

        :param character_table: Optional precomputed character table. Defaults to `dev.default`.
        :type character_table: object
        :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `dev.default`.
        :type elements: object
        :param axes: Requested Cartesian embedding axes. Defaults to `dev.default`.
        :type axes: object
        :return: The modified point-group instance.
        :rtype: PointGroup
        """
        ...

    def get_name(self):
        """
        **LLM Docstring**

        Return the conventional point-group name.

        :return: The point-group name.
        :rtype: str
        """
        ...

    def get_character_table(self):
        """
        **LLM Docstring**

        Construct the hard-coded or analytic character table for the `get` group family.

        :return: The square character table with irreducible representations along rows.
        :rtype: np.ndarray
        """
        ...

    def get_all_character_matrices(self):
        """
        **LLM Docstring**

        Build the three-dimensional Cartesian matrix representation for selected group elements.

        :return: An array of shape `(n_elements, 3, 3)`.
        :rtype: np.ndarray
        """
        ...

class ParametrizedPointGroup(PointGroup):
    group: ParametrizedPointGroups
    n: int

    def __init__(self, name: 'str|ParametrizedPointGroups', n, character_table=None, elements=None, axes=None):
        """
        **LLM Docstring**

        Execute the implementation of `ParametrizedPointGroup.__init__`.

        :param name: Point-group name or enum member.
        :type name: 'str|ParametrizedPointGroups'
        :param n: Group order or problem size used to construct the requested representation.
        :type n: object
        :param character_table: Optional precomputed character table. Defaults to `None`.
        :type character_table: object
        :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
        :type elements: object
        :param axes: Requested Cartesian embedding axes. Defaults to `None`.
        :type axes: object
        :return: The value produced by the implementation.
        :rtype: object
        """
        ...

    def modify(self, character_table=dev.default, elements=dev.default, axes=dev.default):
        """
        **LLM Docstring**

        Return a new point-group object with selected cached data or axes replaced.

        :param character_table: Optional precomputed character table. Defaults to `dev.default`.
        :type character_table: object
        :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `dev.default`.
        :type elements: object
        :param axes: Requested Cartesian embedding axes. Defaults to `dev.default`.
        :type axes: object
        :return: The modified point-group instance.
        :rtype: PointGroup
        """
        ...

    def get_name(self):
        """
        **LLM Docstring**

        Return the conventional point-group name.

        :return: The point-group name.
        :rtype: str
        """
        ...

    def get_character_table(self):
        """
        **LLM Docstring**

        Construct the hard-coded or analytic character table for the `get` group family.

        :return: The square character table with irreducible representations along rows.
        :rtype: np.ndarray
        """
        ...

    def get_all_character_matrices(self):
        """
        **LLM Docstring**

        Build the three-dimensional Cartesian matrix representation for selected group elements.

        :return: An array of shape `(n_elements, 3, 3)`.
        :rtype: np.ndarray
        """
        ...