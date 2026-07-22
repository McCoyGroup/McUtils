import abc
import numpy as np
from .. import Numputils as nput
__all__ = ['IdentityElement', 'SymmetryElement', 'InversionElement', 'RotationElement', 'ReflectionElement', 'ImproperRotationElement']

class SymmetryElement(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        ...

    @abc.abstractmethod
    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
        """
        ...

    def __eq__(self, other):
        """
        **LLM Docstring**

        Compare two elements by numerical equality of their transformation matrices.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: Whether the transformations are numerically equal.
        :rtype: bool
        """
        ...

    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        ...

    def __matmul__(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
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
    def from_transformation_matrix(cls, x, max_rotation_order=60):
        """
        **LLM Docstring**

        Classify a Cartesian matrix and instantiate the corresponding identity, inversion, rotation, reflection, or improper-rotation element.

        :param x: Value used as `x` by the implementation.
        :type x: object
        :param max_rotation_order: Maximum rotation order considered while classifying a matrix. Defaults to `60`.
        :type max_rotation_order: object
        :return: The classified symmetry element.
        :rtype: SymmetryElement
        """
        ...

    @abc.abstractmethod
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

    @abc.abstractmethod
    def plot(self, figure, **graphics_options):
        """
        **LLM Docstring**

        Add graphical primitives representing this symmetry element to a figure.

        :param figure: Plotting figure that receives generated graphics primitives.
        :type figure: object
        :param graphics_options: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
        :type graphics_options: dict
        :return: The plotted primitive or list of plotted primitives.
        :rtype: object
        """
        ...

class ComposedSymmetryElement(SymmetryElement):

    def __init__(self, *bits: SymmetryElement):
        """
        **LLM Docstring**

        Initialize the symmetry element, normalizing any supplied axis and reducing equivalent rotation roots when possible.

        :param bits: Additional positional values forwarded or combined by the implementation.
        :type bits: tuple
        :return: No value is returned.
        :rtype: None
        """
        ...

    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        ...

    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
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

    def plot(self, figure, **graphics_options):
        """
        **LLM Docstring**

        Add graphical primitives representing this symmetry element to a figure.

        :param figure: Plotting figure that receives generated graphics primitives.
        :type figure: object
        :param graphics_options: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
        :type graphics_options: dict
        :return: The plotted primitive or list of plotted primitives.
        :rtype: object
        """
        ...

class IdentityElement(SymmetryElement):

    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        ...

    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        ...

    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
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

    def plot(self, figure, **graphics_options):
        """
        **LLM Docstring**

        Identity elements have no graphical primitive; this stub intentionally performs no action.

        :param figure: Plotting figure that receives generated graphics primitives.
        :type figure: object
        :param graphics_options: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
        :type graphics_options: dict
        :return: No value is returned.
        :rtype: None
        """
        ...

class InversionElement(SymmetryElement):

    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        ...

    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
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

    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        ...

    def plot(self, figure, *, origin=None, point_type=None, radius=0.1, color='red', **graphics_options):
        """
        **LLM Docstring**

        Add graphical primitives representing this symmetry element to a figure.

        :param figure: Plotting figure that receives generated graphics primitives.
        :type figure: object
        :param origin: Plot origin. Defaults to `None`.
        :type origin: object
        :param point_type: Value used as `point_type` by the implementation. Defaults to `None`.
        :type point_type: object
        :param radius: Value used as `radius` by the implementation. Defaults to `0.1`.
        :type radius: object
        :param color: Value used as `color` by the implementation. Defaults to `'red'`.
        :type color: object
        :param graphics_options: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
        :type graphics_options: dict
        :return: The plotted primitive or list of plotted primitives.
        :rtype: object
        """
        ...

class RotationElement(SymmetryElement):

    def __init__(self, order, axis, root=1):
        """
        **LLM Docstring**

        Initialize the symmetry element, normalizing any supplied axis and reducing equivalent rotation roots when possible.

        :param order: Order of the rotation or improper rotation.
        :type order: object
        :param axis: Axis vector defining the symmetry operation.
        :type axis: object
        :param root: Integer power of the primitive rotation. Defaults to `1`.
        :type root: object
        :return: No value is returned.
        :rtype: None
        """
        ...

    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
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

    def __repr__(self):
        """
        **LLM Docstring**

        Return a diagnostic string describing the symmetry element.

        :return: The representation string.
        :rtype: str
        """
        ...

    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        ...

    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        ...

    def plot(self, figure, *, origin=None, line_type=None, disk_type=None, color='black', radius=2, spoke_radius=0.3, disk_color='black', disk_transparency=0.8, **graphics_options):
        """
        **LLM Docstring**

        Add graphical primitives representing this symmetry element to a figure.

        :param figure: Plotting figure that receives generated graphics primitives.
        :type figure: object
        :param origin: Plot origin. Defaults to `None`.
        :type origin: object
        :param line_type: Value used as `line_type` by the implementation. Defaults to `None`.
        :type line_type: object
        :param disk_type: Value used as `disk_type` by the implementation. Defaults to `None`.
        :type disk_type: object
        :param color: Value used as `color` by the implementation. Defaults to `'black'`.
        :type color: object
        :param radius: Value used as `radius` by the implementation. Defaults to `2`.
        :type radius: object
        :param spoke_radius: Value used as `spoke_radius` by the implementation. Defaults to `0.3`.
        :type spoke_radius: object
        :param disk_color: Value used as `disk_color` by the implementation. Defaults to `'black'`.
        :type disk_color: object
        :param disk_transparency: Value used as `disk_transparency` by the implementation. Defaults to `0.8`.
        :type disk_transparency: object
        :param graphics_options: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
        :type graphics_options: dict
        :return: The plotted primitive or list of plotted primitives.
        :rtype: object
        """
        ...

class ReflectionElement(SymmetryElement):

    def __init__(self, axis):
        """
        **LLM Docstring**

        Initialize the symmetry element, normalizing any supplied axis and reducing equivalent rotation roots when possible.

        :param axis: Axis vector defining the symmetry operation.
        :type axis: object
        :return: No value is returned.
        :rtype: None
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

    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        ...

    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
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

    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        ...

    def plot(self, figure, *, origin=None, disk_type=None, color='black', radius=2, disk_transparency=0.8, **graphics_options):
        """
        **LLM Docstring**

        Add graphical primitives representing this symmetry element to a figure.

        :param figure: Plotting figure that receives generated graphics primitives.
        :type figure: object
        :param origin: Plot origin. Defaults to `None`.
        :type origin: object
        :param disk_type: Value used as `disk_type` by the implementation. Defaults to `None`.
        :type disk_type: object
        :param color: Value used as `color` by the implementation. Defaults to `'black'`.
        :type color: object
        :param radius: Value used as `radius` by the implementation. Defaults to `2`.
        :type radius: object
        :param disk_transparency: Value used as `disk_transparency` by the implementation. Defaults to `0.8`.
        :type disk_transparency: object
        :param graphics_options: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
        :type graphics_options: dict
        :return: The plotted primitive or list of plotted primitives.
        :rtype: object
        """
        ...

class ImproperRotationElement(SymmetryElement):

    def __init__(self, order, axis, root=1):
        """
        **LLM Docstring**

        Initialize the symmetry element, normalizing any supplied axis and reducing equivalent rotation roots when possible.

        :param order: Order of the rotation or improper rotation.
        :type order: object
        :param axis: Axis vector defining the symmetry operation.
        :type axis: object
        :param root: Integer power of the primitive rotation. Defaults to `1`.
        :type root: object
        :return: No value is returned.
        :rtype: None
        """
        ...

    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
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

    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
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

    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        ...

    def plot(self, figure, *, origin=None, line_type=None, disk_type=None, color='black', line_style='dashed', size=2, spoke_radius=0.3, disk_color='black', disk_transparency=0.8, **graphics_options):
        """
        **LLM Docstring**

        Add graphical primitives representing this symmetry element to a figure.

        :param figure: Plotting figure that receives generated graphics primitives.
        :type figure: object
        :param origin: Plot origin. Defaults to `None`.
        :type origin: object
        :param line_type: Value used as `line_type` by the implementation. Defaults to `None`.
        :type line_type: object
        :param disk_type: Value used as `disk_type` by the implementation. Defaults to `None`.
        :type disk_type: object
        :param color: Value used as `color` by the implementation. Defaults to `'black'`.
        :type color: object
        :param line_style: Value used as `line_style` by the implementation. Defaults to `'dashed'`.
        :type line_style: object
        :param size: Value used as `size` by the implementation. Defaults to `2`.
        :type size: object
        :param spoke_radius: Value used as `spoke_radius` by the implementation. Defaults to `0.3`.
        :type spoke_radius: object
        :param disk_color: Value used as `disk_color` by the implementation. Defaults to `'black'`.
        :type disk_color: object
        :param disk_transparency: Value used as `disk_transparency` by the implementation. Defaults to `0.8`.
        :type disk_transparency: object
        :param graphics_options: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
        :type graphics_options: dict
        :return: The plotted primitive or list of plotted primitives.
        :rtype: object
        """
        ...