import abc
import numpy as np
from .. import Numputils as nput

__all__ = [
    "IdentityElement",
    "SymmetryElement",
    "InversionElement",
    "RotationElement",
    "ReflectionElement",
    "ImproperRotationElement"
]

class SymmetryElement(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        raise NotImplementedError("abstract")
    @abc.abstractmethod
    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
        """
        raise NotImplementedError("abstract")
    def __eq__(self, other):
        """
        **LLM Docstring**

        Compare two elements by numerical equality of their transformation matrices.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: Whether the transformations are numerically equal.
        :rtype: bool
        """
        return np.allclose(self.get_transformation(), other.get_transformation())
    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        return ComposedSymmetryElement(self, other)

    def __matmul__(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        return self.compose(other)

    def __repr__(self):
        """
        **LLM Docstring**

        Return a diagnostic string describing the symmetry element.

        :return: The representation string.
        :rtype: str
        """
        cls = type(self)
        return f"{cls.__name__}()"

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
        _, type, axis, root, order = nput.identify_cartesian_transformation_type(x, max_rotation_order=max_rotation_order)
        type = nput.TransformationTypes(type)
        if type == nput.TransformationTypes.Identity:
            return IdentityElement()
        elif type == nput.TransformationTypes.Inversion:
            return InversionElement()
        elif type == nput.TransformationTypes.Rotation:
            return RotationElement(order, axis, root)
        elif type == nput.TransformationTypes.ImproperRotation:
            return ImproperRotationElement(order, axis, root)
        elif type == nput.TransformationTypes.Reflection:
            return ReflectionElement(axis)
        else:
            raise ValueError(f"can't understand transformation type {type}")

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
    def __init__(self, *bits:SymmetryElement):
        """
        **LLM Docstring**

        Initialize the symmetry element, normalizing any supplied axis and reducing equivalent rotation roots when possible.

        :param bits: Additional positional values forwarded or combined by the implementation.
        :type bits: tuple
        :return: No value is returned.
        :rtype: None
        """
        self.bits = bits
    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        mat = self.bits[0].get_transformation()
        for b in self.bits[1:]:
            mat = mat @ b.get_transformation()
        return mat
    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
        """
        return ComposedSymmetryElement(*(b.inverse() for b in reversed(self.bits)))
    def transform(self, tf):
        """
        **LLM Docstring**

        Express the symmetry element in a transformed Cartesian basis.

        :param tf: A `3 x 3` change-of-basis transformation.
        :type tf: object
        :return: A symmetry element with its defining axis transformed by `tf`.
        :rtype: SymmetryElement
        """
        return type(self)(*(b.transform(tf) for b in reversed(self.bits)))
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
        symm = SymmetryElement.from_transformation_matrix(self.get_transformation(), max_rotation_order=None)
        return symm.plot(figure=figure, **graphics_options)

class IdentityElement(SymmetryElement):
    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        return np.eye(3)
    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        return other
    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
        """
        return self
    def transform(self, tf):
        """
        **LLM Docstring**

        Express the symmetry element in a transformed Cartesian basis.

        :param tf: A `3 x 3` change-of-basis transformation.
        :type tf: object
        :return: A symmetry element with its defining axis transformed by `tf`.
        :rtype: SymmetryElement
        """
        return self

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
        return np.diag(-np.ones(3))
    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
        """
        return self
    def transform(self, tf):
        """
        **LLM Docstring**

        Express the symmetry element in a transformed Cartesian basis.

        :param tf: A `3 x 3` change-of-basis transformation.
        :type tf: object
        :return: A symmetry element with its defining axis transformed by `tf`.
        :rtype: SymmetryElement
        """
        return self

    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        if isinstance(other, InversionElement):
            return IdentityElement()
        elif isinstance(other, RotationElement):
            if other.order == 2:
                return ReflectionElement(other.axis)
            else:
                return (
                    RotationElement(2, other.axis) @
                        ImproperRotationElement(other.order, other.axis, root=other.root)
                )
        elif isinstance(other, ImproperRotationElement):
            new_root = (other.order - 2*other.root) % (2*other.order)
            return RotationElement(2*other.order, -other.axis, root=new_root)
        # elif isinstance(other, (RotationElement, ImproperRotationElement)):
        #     return RotationElement(other.order, other.axis, root=other.order-other.root)
        # elif isinstance(other, ReflectionElement):
        #     return ReflectionElement(-other.axis)
        return super().compose(other)

    def plot(self, figure, *, origin=None, point_type=None, radius=.1, color='red', **graphics_options):
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
        from McUtils.Plots import Sphere
        if point_type is None:
            point_type = Sphere
        if origin is None:
            origin = (0, 0, 0)
        return point_type(
            origin,
            radius=radius,
            color=color,
            **graphics_options
        ).plot(figure)

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
        ax, norm = nput.vec_normalize(axis, return_norms=True)
        if norm < 1e-6: raise ValueError("can't have rotation element with no axis")
        if root > 1 and order % root == 0:
            order = order // root
            root = 1
        self.root = root
        self.order = order
        self.axis = ax
    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
        """
        return type(self)(self.order, self.axis, self.order-self.root)
    def transform(self, tf):
        """
        **LLM Docstring**

        Express the symmetry element in a transformed Cartesian basis.

        :param tf: A `3 x 3` change-of-basis transformation.
        :type tf: object
        :return: A symmetry element with its defining axis transformed by `tf`.
        :rtype: SymmetryElement
        """
        return type(self)(self.order, tf @ self.axis, root=self.root)

    def __repr__(self):
        """
        **LLM Docstring**

        Return a diagnostic string describing the symmetry element.

        :return: The representation string.
        :rtype: str
        """
        cls = type(self)
        return f"{cls.__name__}({self.root}/{self.order}, {self.axis})"

    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        if isinstance(other, (RotationElement, ImproperRotationElement)):
            if (
                    isinstance(other, ImproperRotationElement)
                    and other.order == 2
            ):
                return self.compose(InversionElement())
            rot_type = type(other)
            check = np.dot(other.axis, self.axis)
            if abs(check) > 1-1e-6:
                gcd = np.gcd(self.order, other.order)
                order = self.order*other.order//gcd
                root = np.sign(check)*other.root*order//other.order + self.root*order//self.order
                return rot_type(order, self.axis, root=int(np.round(root)))
            elif self.order == 2 and check < 1e-6:
                x = self.get_transformation() @ other.get_transformation() # symmetric by construction
                vals, axes = np.linalg.eigh(x)
                if isinstance(other, ImproperRotationElement):
                    pos = np.where(vals < -.9)[0][0]
                    return InversionElement() @ RotationElement(self.order, axes[:, pos], self.root)
                else:
                    pos = np.where(vals > .9)[0][0]
                    return RotationElement(self.order, axes[:, pos], self.root)
            elif other.order == 2 and check < 1e-6:
                x = self.get_transformation() @ other.get_transformation() # symmetric by construction
                vals, axes = np.linalg.eigh(x)
                pos = np.where(vals > .9)[0][0]
                return rot_type(other.order, axes[:, pos], other.root)
            else:
                return super().compose(other)

        return other @ self

    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        return nput.rotation_matrix(self.axis, 2*np.pi*self.root/self.order)

    def plot(self, figure, *,
             origin=None,
             line_type=None,
             disk_type=None,
             color='black',
             radius=2,
             spoke_radius=.3,
             disk_color='black',
             disk_transparency=.8,
             **graphics_options
             ):
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
        from McUtils.Plots import Line, Disk
        if line_type is None:
            line_type = Line
        if origin is None:
            origin = (0, 0, 0)
        origin = np.asarray(origin)
        points1 = origin - radius * self.axis
        points2 = origin + radius * self.axis
        objects = []
        axis_line = line_type(
                [points1, points2],
                color=color,
                **graphics_options
            )
        objects.append(axis_line)
        if spoke_radius is not None:
            if disk_color is not None:
                if disk_type is None:
                    disk_type = Disk
                disk = disk_type(
                    origin,
                    radius=spoke_radius,
                    normal=self.axis,
                    color=None,
                    line_color=disk_color
                    # transparency=disk_transparency
                )
                objects.append(disk)

            tf = self.get_transformation()
            baseline = nput.view_matrix(self.axis)[:, 0] * spoke_radius
            for r in range(self.order):
                new_line = line_type(
                    [origin, origin+baseline],
                    color=color,
                    **graphics_options
                )
                objects.append(new_line)
                baseline = tf @ baseline

        return [
            o.plot(figure)
            for o in objects
        ]

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
        ax, norm = nput.vec_normalize(axis, return_norms=True)
        if norm < 1e-6: raise ValueError("can't have reflection element with no axis")
        self.axis = ax
    def __repr__(self):
        """
        **LLM Docstring**

        Return a diagnostic string describing the symmetry element.

        :return: The representation string.
        :rtype: str
        """
        cls = type(self)
        return f"{cls.__name__}({self.axis})"

    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        tf = nput.view_matrix(self.axis)
        return tf @ np.diag([1, -1, 1]) @ tf.T
    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
        """
        return self
    def transform(self, tf):
        """
        **LLM Docstring**

        Express the symmetry element in a transformed Cartesian basis.

        :param tf: A `3 x 3` change-of-basis transformation.
        :type tf: object
        :return: A symmetry element with its defining axis transformed by `tf`.
        :rtype: SymmetryElement
        """
        return type(self)(tf@self.axis)

    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        if isinstance(other, ReflectionElement):
            check = np.dot(other.axis, self.axis)
            if abs(check) > 1-1e-6:
                return IdentityElement()
            elif check < 1e-6:
                return RotationElement(2, np.cross(self.axis, other.axis))
        elif isinstance(other, RotationElement):
            check = np.dot(other.axis, self.axis)
            if abs(check) > 1-1e-6:
                return ImproperRotationElement(other.order, other.axis)
        elif isinstance(other, ImproperRotationElement):
            if other.order == 2:
                return self.compose(InversionElement())
            check = np.dot(other.axis, self.axis)
            if abs(check) > 1 - 1e-6:
                return RotationElement(other.order, other.axis)
        elif isinstance(other, InversionElement):
            return RotationElement(2, self.axis)

        return super().compose(other)

    def plot(self, figure, *,
             origin=None,
             disk_type=None,
             color='black',
             radius=2,
             disk_transparency=.8,
             **graphics_options
             ):
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
        from McUtils.Plots import Disk
        if origin is None:
            origin = (0, 0, 0)
        origin = np.asarray(origin)
        if disk_type is None:
            disk_type = Disk
        objs = [
            disk_type(
                origin,
                radius=radius,
                normal=self.axis,
                color=color,
                transparency=disk_transparency
            ),
            disk_type(
                origin,
                radius=radius,
                normal=self.axis,
                color=None,
                line_color='black'
                # transparency=disk_transparency
            )
        ]
        for o in objs:
            o.plot(figure)
        return objs

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
        ax, norm = nput.vec_normalize(axis, return_norms=True)
        if norm < 1e-6: raise ValueError("can't have improper rotation element with no axis")
        if root > 1 and order % root == 0:
            order = order // root
            root = 1
        self.root = root
        self.order = order
        self.axis = ax
    def inverse(self):
        """
        **LLM Docstring**

        Return the symmetry element whose transformation reverses this operation.

        :return: The inverse symmetry element.
        :rtype: SymmetryElement
        """
        return type(self)(self.order, self.axis, self.order-self.root)
    def transform(self, tf):
        """
        **LLM Docstring**

        Express the symmetry element in a transformed Cartesian basis.

        :param tf: A `3 x 3` change-of-basis transformation.
        :type tf: object
        :return: A symmetry element with its defining axis transformed by `tf`.
        :rtype: SymmetryElement
        """
        return type(self)(self.order, tf @ self.axis, root=self.root)

    def compose(self, other):
        """
        **LLM Docstring**

        Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.

        :param other: The symmetry element to compare or compose with this element.
        :type other: object
        :return: The simplified or generic composed symmetry element.
        :rtype: SymmetryElement
        """
        if self.order == 2:
            return InversionElement().compose(other)

        if isinstance(other, RotationElement):
            return other.compose(self).inverse()
            # need to get inverse
        elif isinstance(other, ImproperRotationElement):
            if other.order == 2:
                return self.compose(InversionElement())
            check = np.dot(other.axis, self.axis)
            if abs(check) > 1 - 1e-6:
                gcd = np.gcd(self.order, other.order)
                order = self.order * other.order // gcd
                root = np.sign(check) * other.root * order // other.order + self.root * order // self.order
                return ImproperRotationElement(order, self.axis, root=int(np.round(root)))
            else:
                return super().compose(other)
        else:
            return other.compose(self) # commute

    def __repr__(self):
        """
        **LLM Docstring**

        Return a diagnostic string describing the symmetry element.

        :return: The representation string.
        :rtype: str
        """
        cls = type(self)
        return f"{cls.__name__}({self.root}/{self.order}, {self.axis})"
    def get_transformation(self):
        """
        **LLM Docstring**

        Return the `3 x 3` Cartesian matrix implementing this symmetry operation.

        :return: The Cartesian transformation matrix.
        :rtype: np.ndarray
        """
        rot = nput.rotation_matrix(self.axis, 2*np.pi*self.root/self.order)
        tf = nput.view_matrix(self.axis)
        reflect = tf @ np.diag([1, -1, 1]) @ tf.T
        return reflect @ rot

    def plot(self, figure, *,
             origin=None,
             line_type=None,
             disk_type=None,
             color='black',
             line_style='dashed',
             size=2,
             spoke_radius=.3,
             disk_color='black',
             disk_transparency=.8,
             **graphics_options
             ):
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
        from McUtils.Plots import Line, Disk
        if line_type is None:
            line_type = Line
        if origin is None:
            origin = (0, 0, 0)
        origin = np.asarray(origin)
        points1 = origin - size * self.axis
        points2 = origin + size * self.axis
        objects = []
        axis_line = line_type(
            [points1, points2],
            color=color,
            line_style=line_style,
            **graphics_options
            )
        objects.append(axis_line)
        if spoke_radius is not None:
            if disk_color is not None:
                if disk_type is None:
                    disk_type = Disk
                disk = disk_type(
                    origin,
                    radius=spoke_radius,
                    normal=self.axis,
                    color=disk_color,
                    transparency=disk_transparency
                )
                objects.append(disk)

            tf = self.get_transformation()
            baseline = nput.view_matrix(self.axis)[:, 0] * spoke_radius
            for r in range(self.order):
                new_line = line_type(
                    [origin, origin+baseline],
                    color=color,
                    line_style=line_style,
                    **graphics_options
                )
                objects.append(new_line)
                baseline = tf @ baseline

        return [
            o.plot(figure)
            for o in objects
        ]

# def enumerate_symmetry_operations(generators:'list[SymmetryElement]', max_order=None):
#     if max_order is None:
#         max_order = 60 # support up to C60 rotations...
#
#     real_ops = [g for g in generators if not isinstance(g, IdentityElement)]
#     tf_cache = {}
#     def get_tf(g):
#         tf = tf_cache.get(g)
#         if tf is None:
#             tf = g.get_transformation()
#             tf_cache[g] = tf
#         return tf
#
#     generator_orbits = []
#     for g in real_ops:
#         x = get_tf(g)
#         g2 = g
#         orbit = [g]
#         for i in range(max_order):
#             g3 = g @ g2
#             x2 = g3.get_transformation()
#             if np.allclose(x2, x):
#                 break
#             else:
#                 orbit.append(g3)
#
#     return generator_orbits

