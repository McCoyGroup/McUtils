import abc
import enum
import numpy as np
from .. import Devutils as dev
from .. import Numputils as nput

from .Characters import *
from .Elements import *

__all__ = [
    "NamedPointGroups",
    "ParametrizedPointGroups",
    "PointGroup"
]

class NamedPointGroups(enum.Enum):
    Ih = "Ih"
    I = "I"
    Oh = "Oh"
    O = "O"
    Th = "Th"
    Td = "Td"
    T = "T"
    Cs = "Cs"
class ParametrizedPointGroups(enum.Enum):
    C = "C"
    Ch = "Ch"
    Cv = "Cv"
    D = "D"
    Dh = "Dh"
    Dd = "Dd"
    S = "S"


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
        self._elements = elements
        self._character_table = character_table
        self._axes = axes
        self._base_axes = None

    def get_modification_kwargs(
            self,
            character_table=dev.default,
            elements=dev.default,
            axes=dev.default
    ):
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
        return dict(
            character_table=self.character_table if dev.is_default(character_table) else character_table,
            elements=elements if dev.is_default(elements) else elements,
            axes=axes if dev.is_default(axes) else axes,
        )
    def modify(self,
               character_table=dev.default,
               elements=dev.default,
               axes=dev.default
               ):
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
        return type(self)(**self.get_modification_kwargs(
            character_table=character_table,
            elements=elements,
            axes=axes
        ))

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
        return self.get_name()
    def __repr__(self):
        """
        **LLM Docstring**

        Return a diagnostic string describing the symmetry element.

        :return: The representation string.
        :rtype: str
        """
        return "PointGroup<{}>".format(self.name)

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
        if isinstance(key, NamedPointGroups):
            return NamedPointGroup(key, **etc)
        elif isinstance(key, ParametrizedPointGroups):
            return ParametrizedPointGroup(key, n, **etc)
        else:
            if any(x.isdigit() for x in key):
                n = int("".join(x for x in key if x.isdigit()))
                key = "".join("".join(x for x in key if not x.isdigit()))
                return cls.from_name(key, n=n, **etc)
            try:
                key = NamedPointGroups(key)
            except ValueError:
                key = ParametrizedPointGroups(key)
            return cls.from_name(key, n=n, **etc)

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
        rotors = [e for e in elements if isinstance(e, RotationElement)]
        if len(rotors) == 0:
            return None, None
        else:
            orders, loc, counts = np.unique([e.order for e in rotors], return_counts=True, return_index=True)
            return rotors[loc[-1]], counts[-1]

    @classmethod
    def from_symmetry_elements(cls, elements: list[SymmetryElement], tol=1e-2):
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
        primary_axis, counts = cls.get_symmetry_element_primary_rotation(elements)
        if primary_axis is None:
            if any(isinstance(e, InversionElement) for e in elements):
                return cls.from_name("Ci")
            elif any(isinstance(e, ReflectionElement) for e in elements):
                reflections = [e for e in elements if isinstance(e, ReflectionElement)]
                axes = nput.view_matrix(reflections[0].axis)[:, (0, 2, 1)]
                return cls.from_name("Cs", axes=axes)
            else:
                return cls.from_name("C", 1)
        elif counts > 1:  # high symmetry
            raise NotImplementedError(...)
        else:
            group_order = primary_axis.order
            primary_axis = primary_axis.axis
            c2_axis = None
            for e in elements:
                if (
                        isinstance(e, RotationElement)
                        and e.order == 2
                        and np.abs(np.dot(e.axis, primary_axis)) < tol  # perp
                ):
                    c2_axis = e
                    break

            sh_plane = None
            for e in elements:
                if (
                        isinstance(e, ReflectionElement)
                        and np.abs(np.dot(e.axis, primary_axis)) > 1 - tol  # parallel
                ):
                    sh_plane = e
                    break

            if c2_axis is not None:
                if sh_plane is not None:
                    return cls.from_name("Dh", group_order)
                else:
                    sd_plane = None
                    axes = nput.view_matrix(
                        primary_axis.axis,
                        view_vector=c2_axis.axis
                    )[:, (0, 2, 1)]
                    for e in elements:
                        if (
                                isinstance(e, ReflectionElement)
                                and np.abs(np.dot(e.axis, primary_axis)) < tol  # perp
                        ):
                            sd_plane = e
                    if sd_plane is not None:
                        return cls.from_name("Dd", group_order, axes=axes)
                    else:
                        return cls.from_name("D", group_order, axes=axes)
            else:
                if sh_plane is not None:
                    return cls.from_name("Ch", group_order)
                else:
                    sv_plane = None
                    for e in elements:
                        if (
                                isinstance(e, ReflectionElement)
                                and np.abs(np.dot(e.axis, primary_axis)) < tol  # perp
                        ):
                            sv_plane = e
                    if sv_plane is not None:
                        return cls.from_name("Cv", group_order)
                    else:
                        if any(isinstance(e, ImproperRotationElement) for e in elements):
                            return cls.from_name("S", group_order)
                        else:
                            return cls.from_name("C", group_order)

    def get_symmetry_elements(self, only_class_representatives=True):
        """
        **LLM Docstring**

        Convert representative or full operation matrices into symmetry-element objects and embed them in requested axes.

        :param only_class_representatives: Whether to return one operation per conjugacy class rather than every group operation. Defaults to `True`.
        :type only_class_representatives: object
        :return: The symmetry elements.
        :rtype: tuple[SymmetryElement, ...] | list[SymmetryElement]
        """
        ct = self.character_table
        if only_class_representatives:
            mats = ct.matrices
            if mats is None:
                raise NotImplementedError(f"no implementation for operator matrices for point group {self}")
            elems = tuple(SymmetryElement.from_transformation_matrix(x) for x in mats)
            self._base_axes = self.get_axes(elems)
            if self._axes is not None:
                tf = self._axes @ self._base_axes.T
                if abs(np.linalg.det(tf)) < 1e-6:
                    raise ValueError("bad transformation")
                elems = [e.transform(tf) for e in elems]
        else:
            all_mats = self.get_all_character_matrices()
            elems = tuple(SymmetryElement.from_transformation_matrix(x) for x in all_mats)
            if self._axes is not None:
                mats = ct.matrices
                if mats is None:
                    raise NotImplementedError(f"no implementation for operator matrices for point group {self}")
                base_elems = tuple(SymmetryElement.from_transformation_matrix(x) for x in mats)
                base_axes = self._base_axes
                if base_axes is None:
                    base_axes = self.get_axes(base_elems)
                tf = self._axes @ base_axes.T
                elems = [e.transform(tf) for e in elems]

        return elems

    @property
    def character_table(self) -> CharacterTable:
        """
        **LLM Docstring**

        Lazily construct and cache the group character table.

        :return: The character table.
        :rtype: CharacterTable
        """
        if self._character_table is None:
            self._character_table = self.get_character_table()
        return self._character_table

    @property
    def elements(self) -> 'tuple[SymmetryElement]':
        """
        **LLM Docstring**

        Lazily construct and cache representative symmetry elements.

        :return: The symmetry elements.
        :rtype: tuple[SymmetryElement, ...]
        """
        if self._elements is None:
            self._elements = self.get_symmetry_elements()
        return self._elements

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
        primary_axis = None
        secondary_axis = None

        primary, count = cls.get_symmetry_element_primary_rotation(elements)
        if primary is None:
            # search for reflection plane
            planes = [e for e in elements if isinstance(e, ReflectionElement)]
            if len(planes) == 0:
                return np.eye(3)
            primary_axis = planes[0].axis
            if len(planes) > 1: # I don't think this is possible
                secondary_axis = planes[1].axis
        else:
            primary_axis = primary.axis
            c2_axes = [e for e in elements if isinstance(e, RotationElement) and e.order == 2]
            perp_axes = [
                e for e in c2_axes
                if abs(np.dot(primary_axis, e.axis)) < 1e-2
            ]
            if len(perp_axes) == 0:
                # search for vertical reflection planes
                planes = [e for e in elements if isinstance(e, ReflectionElement)]
                v_planes = [
                    e for e in planes
                    if abs(np.dot(primary_axis, e.axis)) < 1e-2
                ]
                if len(v_planes) > 0:
                    secondary_axis = v_planes[0].axis
                else:
                    non_par = [
                        e for e in c2_axes
                        if abs(np.dot(primary_axis, e.axis)) < .9
                    ]
                    if len(non_par) > 0:
                        secondary_axis = non_par[0].axis
            else:
                secondary_axis = perp_axes[0].axis

        if primary_axis is None:
            raise ValueError("no primary axis found") # how??

        if secondary_axis is None:
            secondary_axis = [1, 0, 0]
            if abs(np.dot(secondary_axis, primary_axis)) > 1 - 1e-2:
                secondary_axis = [0, 0, 1]

        return nput.view_matrix(primary_axis, secondary_axis, output_order=['x', 'y', 'z'])

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
        # could use point group identity for short circuiting, but don't want to
        if base_axes:
            elements = tuple(
                SymmetryElement.from_transformation_matrix(x)
                for x in self.character_table.matrices
            )
        if elements is None:
            elements = self.elements
        return self.get_axes_from_symmetry_elements(elements)
        # tertiary_axis = nput.vec_crosses(primary_axis, secondary_axis, normalize=True)
        # secondary_axis = nput.vec_crosses(tertiary_axis, primary_axis, normalize=True)
        #
        # return np.array([secondary_axis, tertiary_axis, primary_axis]).T

    @property
    def axes(self):
        """
        **LLM Docstring**

        Lazily determine and cache the embedded or canonical point-group axes.

        :return: A `3 x 3` axis matrix.
        :rtype: np.ndarray
        """
        if self._axes is None:
            self._axes = self.get_axes()
        return self._axes

    @property
    def base_axes(self):
        """
        **LLM Docstring**

        Lazily determine and cache the embedded or canonical point-group axes.

        :return: A `3 x 3` axis matrix.
        :rtype: np.ndarray
        """
        if self._base_axes is None:
            self._base_axes = self.get_axes(base_axes=True)
        return self._base_axes

    def align(self, axes):
        """
        **LLM Docstring**

        Return a copy aligned to explicitly supplied axes, transforming cached elements consistently.

        :param axes: Requested Cartesian embedding axes.
        :type axes: object
        :return: The aligned point group.
        :rtype: PointGroup
        """
        tf = axes @ self.axes.T
        return self.modify(
            axes=axes,
            elements=[e.transform(tf) for e in self.elements]
        )
    def transform(self, tf):
        """
        **LLM Docstring**

        Express the symmetry element in a transformed Cartesian basis.

        :param tf: A `3 x 3` change-of-basis transformation.
        :type tf: object
        :return: A symmetry element with its defining axis transformed by `tf`.
        :rtype: SymmetryElement
        """
        return self.modify(
            axes=tf @ self.axes,
            elements=[e.transform(tf) for e in self.elements]
        )

    def get_matrices(self, only_class_representatives=True):
        """
        **LLM Docstring**

        Build the three-dimensional Cartesian matrix representation for selected group elements.

        :param only_class_representatives: Whether to return one operation per conjugacy class rather than every group operation. Defaults to `True`.
        :type only_class_representatives: object
        :return: An array of shape `(n_elements, 3, 3)`.
        :rtype: np.ndarray
        """
        if only_class_representatives:
            mats = self.character_table.matrices
        else:
            mats = self.get_all_character_matrices()
        if self._axes is not None:
            tf = self._axes @ self.base_axes.T
            mats = tf[np.newaxis] @ mats @ tf.T[np.newaxis]
        return mats

    def axis_representation(self):
        return self.character_table.axis_representation(matrices=self.get_matrices())
    def coordinate_representation(self, coords):
        return self.character_table.coordinate_representation(coords, matrices=self.get_matrices())
    def coordinate_mode_reduction(self, coords):
        return self.character_table.coordinate_mode_reduction(coords, matrices=self.get_matrices())

    def plot(self,
             figure=None,
             elements=None,
             origin=None,
             inversion_styles=None,
             rotation_styles=None,
             reflection_styles=None,
             improper_rotation_styles=None,
             **opts):
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
        from McUtils.Plots import Graphics3D

        if figure is None:
            figure = Graphics3D(backend='x3d')

        if elements is None:
            elements = self.elements
        elif dev.str_is(elements, 'all'):
            elements = self.get_symmetry_elements(only_class_representatives=False)
        if inversion_styles is None:
            inversion_styles = {}
        if rotation_styles is None:
            rotation_styles = {}
        if reflection_styles is None:
            reflection_styles = {}
        if improper_rotation_styles is None:
            improper_rotation_styles = rotation_styles
        for e in elements:
            base_styles = (
                inversion_styles
                    if isinstance(e, InversionElement) else
                reflection_styles
                    if isinstance(e, ReflectionElement) else
                rotation_styles
                    if isinstance(e, RotationElement) else
                improper_rotation_styles
                    if isinstance(e, ImproperRotationElement) else
                {}
            )
            if base_styles is False: continue
            styles = dict(
                opts,
                **base_styles
            )
            e.plot(figure, origin=origin, **styles)

        return figure
class NamedPointGroup(PointGroup):
    def __init__(self, name:'str|NamedPointGroups', character_table=None, elements=None, axes=None):
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
        super().__init__(character_table=character_table, elements=elements, axes=axes)
        self.group = NamedPointGroups(name)
    def modify(self,
               character_table=dev.default,
               elements=dev.default,
               axes=dev.default
               ):
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
        return type(self)(
            self.group,
            **self.get_modification_kwargs(
            character_table=character_table,
            elements=elements,
            axes=axes
        ))
    def get_name(self):
        """
        **LLM Docstring**

        Return the conventional point-group name.

        :return: The point-group name.
        :rtype: str
        """
        return self.group.value

    def get_character_table(self):
        """
        **LLM Docstring**

        Construct the hard-coded or analytic character table for the `get` group family.

        :return: The square character table with irreducible representations along rows.
        :rtype: np.ndarray
        """
        return CharacterTable.fixed_size_point_group(self.group.value)
    def get_all_character_matrices(self):
        """
        **LLM Docstring**

        Build the three-dimensional Cartesian matrix representation for selected group elements.

        :return: An array of shape `(n_elements, 3, 3)`.
        :rtype: np.ndarray
        """
        return point_group_data(self.group.value, prop="matrices")

class ParametrizedPointGroup(PointGroup):
    group: ParametrizedPointGroups
    n: int
    def __init__(self, name:'str|ParametrizedPointGroups', n, character_table=None, elements=None, axes=None):
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
        super().__init__(character_table=character_table, elements=elements, axes=axes)
        self.group = ParametrizedPointGroups(name)
        self.n = n
    def modify(self,
               character_table=dev.default,
               elements=dev.default,
               axes=dev.default
               ):
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
        return type(self)(
            self.group,
            self.n,
            **self.get_modification_kwargs(
                character_table=character_table,
                elements=elements,
                axes=axes
            ))
    def get_name(self):
        """
        **LLM Docstring**

        Return the conventional point-group name.

        :return: The point-group name.
        :rtype: str
        """
        return self.group.value[:1] + str(self.n) + self.group.value[1:]

    def get_character_table(self):
        """
        **LLM Docstring**

        Construct the hard-coded or analytic character table for the `get` group family.

        :return: The square character table with irreducible representations along rows.
        :rtype: np.ndarray
        """
        return CharacterTable.point_group(self.group.value, self.n)
    def get_all_character_matrices(self):
        """
        **LLM Docstring**

        Build the three-dimensional Cartesian matrix representation for selected group elements.

        :return: An array of shape `(n_elements, 3, 3)`.
        :rtype: np.ndarray
        """
        return point_group_data(self.group.value, self.n, prop="matrices")


