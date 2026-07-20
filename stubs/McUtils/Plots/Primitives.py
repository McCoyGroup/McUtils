"""
Graphics primitives module
Provides stuff like Disk, Sphere, etc. and lets them figure out how to plot themselves
"""
__all__ = ['GraphicsPrimitive', 'Cube', 'Sphere', 'Cylinder', 'Disk', 'Line', 'Text', 'Arrow', 'Inset', 'Point', 'Triangle', 'Polygon', 'Rectangle', 'Path']
import abc, numpy as np
from .VTKInterface import *

class GraphicsPrimitive(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def plot(self, axes, *args, graphics=None, **kwargs):
        """The one method that needs to be implemented, which takes the graphics and actually puts stuff on its axes

        :param axes:
        :type axes:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def get_bbox(self):
        """
        **LLM Docstring**

        Abstract: return the primitive's bounding box.

        :return: the bounding box
        """
        ...

class Disk(GraphicsPrimitive):

    def __init__(self, position=(0, 0), radius=1, **opts):
        """
        **LLM Docstring**

        Set up a `Disk` primitive.

        :param position: the disk center
        :param radius: the disk radius
        :param opts: extra styling options
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the primitive's bounding box (the square enclosing the disk).

        :return: the `[(min_x, min_y), (max_x, max_y)]` bounding box
        :rtype: list
        """
        ...

    def plot(self, axes, *args, graphics=None, zdir=None, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_disk`.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Line(GraphicsPrimitive):

    def __init__(self, points, radius=0.1, **opts):
        """
        **LLM Docstring**

        Set up a `Line` primitive.

        :param points: the line points
        :param radius: the line radius
        :param opts: extra styling options
        """
        ...

    @property
    def points(self):
        """
        **LLM Docstring**

        The line's points.

        :return: the points
        :rtype: np.ndarray
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the primitive's bounding box enclosing its points.

        :return: the `[(min_x, min_y), (max_x, max_y)]` bounding box
        :rtype: list
        """
        ...

    def plot(self, axes, *args, graphics=None, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_line`.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Text(GraphicsPrimitive):

    def __init__(self, txt, pos, bbox=((1, 1), (1, 1)), **opts):
        """
        **LLM Docstring**

        Set up a `Text` primitive.

        :param txt: the text string
        :param pos: the text position
        :param bbox: the per-side padding box around the text
        :param opts: extra styling options
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the primitive's bounding box (the padded box around the text).

        :return: the `[(min_x, min_y), (max_x, max_y)]` bounding box
        :rtype: list
        """
        ...

    def plot(self, axes, *args, graphics=None, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_text`.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Arrow(GraphicsPrimitive):

    def __init__(self, pos1, pos2, **opts):
        """
        **LLM Docstring**

        Set up a `Arrow` primitive.

        :param pos1: the arrow start point
        :param pos2: the arrow end point
        :param opts: extra styling options
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the primitive's bounding box enclosing its endpoints.

        :return: the `[(min_x, min_y), (max_x, max_y)]` bounding box
        :rtype: list
        """
        ...

    def plot(self, axes, *args, graphics=None, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_arrow`.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Path(GraphicsPrimitive):

    def __init__(self, commands, **opts):
        """
        **LLM Docstring**

        Set up a `Path` primitive.

        :param commands: the path drawing commands
        :param opts: extra styling options
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Not implemented: this primitive has no bounding-box computation.

        :raises NotImplementedError: always
        """
        ...

    def plot(self, axes, *args, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_path`.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Sphere(GraphicsPrimitive):

    def __init__(self, position=(0, 0, 0), radius=1, sphere_points=48, **opts):
        """
        **LLM Docstring**

        Set up a `Sphere` primitive.

        :param position: the sphere center
        :param radius: the sphere radius
        :param sphere_points: the tessellation resolution
        :type sphere_points: int
        :param opts: extra styling options
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Not implemented: this primitive has no bounding-box computation.

        :raises NotImplementedError: always
        """
        ...

    def plot(self, axes, *args, sphere_points=None, graphics=None, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_sphere`.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Cube(GraphicsPrimitive):

    def __init__(self, p1, p2, **opts):
        """
        **LLM Docstring**

        Set up a `Cube` primitive.

        :param p1: the min corner
        :param p2: the max corner
        :param opts: extra styling options
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the primitive's bounding box (its two corners).

        :return: the `[(min_x, min_y), (max_x, max_y)]` bounding box
        :rtype: list
        """
        ...

    def plot(self, axes, *args, circle_points=None, graphics=None, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_box`.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Cylinder(GraphicsPrimitive):

    def __init__(self, p1, p2, radius, circle_points=32, **opts):
        """
        **LLM Docstring**

        Set up a `Cylinder` primitive.

        :param p1: the start point
        :param p2: the end point
        :param radius: the cylinder radius
        :param circle_points: the number of points around the cross-section
        :type circle_points: int
        :param opts: extra styling options
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Not implemented: this primitive has no bounding-box computation.

        :raises NotImplementedError: always
        """
        ...

    def plot(self, axes, *args, circle_points=None, graphics=None, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_cylinder` (or a `VTKCylinder` when drawing into a VTK window).

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Point(GraphicsPrimitive):

    def __init__(self, pts, **opts):
        """
        **LLM Docstring**

        Set up a `Point` primitive.

        :param pts: the point position(s)
        :param opts: extra styling options
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Not implemented: this primitive has no bounding-box computation.

        :raises NotImplementedError: always
        """
        ...

    def plot(self, axes, *args, graphics=None, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_point`.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Triangle(GraphicsPrimitive):

    def __init__(self, pts, **opts):
        """
        **LLM Docstring**

        Set up a `Triangle` primitive.

        :param pts: the triangle vertices
        :param opts: extra styling options
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Not implemented: this primitive has no bounding-box computation.

        :raises NotImplementedError: always
        """
        ...

    def plot(self, axes, *args, sphere_points=None, graphics=None, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_triangle`.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Polygon(GraphicsPrimitive):

    def __init__(self, points, **opts):
        """
        **LLM Docstring**

        Set up a `Polygon` primitive.

        :param points: the polygon vertices
        :param opts: extra styling options
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Not implemented: this primitive has no bounding-box computation.

        :raises NotImplementedError: always
        """
        ...

    def plot(self, axes, *args, sphere_points=None, graphics=None, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_poly`.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Rectangle(GraphicsPrimitive):

    def __init__(self, pts, **opts):
        """
        **LLM Docstring**

        Set up a `Rectangle` primitive.

        :param pts: the rectangle corners
        :param opts: extra styling options
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Not implemented: this primitive has no bounding-box computation.

        :raises NotImplementedError: always
        """
        ...

    def plot(self, axes, *args, sphere_points=None, graphics=None, **kwargs):
        """
        **LLM Docstring**

        Draw the primitive onto the axes via `axes.draw_rect`.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the owning graphics object
        :param kwargs: extra styling options
        :return: the drawn backend object
        """
        ...

class Inset(GraphicsPrimitive):

    def __init__(self, prims, position, offset=(0.5, 0.5), dimensions=None, plot_range=None, **opts):
        """
        **LLM Docstring**

        Set up an inset primitive: a group of sub-primitives placed in their own inset
        axes at a position within the parent.

        :param prims: the sub-primitives to draw in the inset
        :param position: the inset's anchor position in the parent
        :param offset: the anchor's alignment within the inset box
        :param dimensions: the inset's `(width, height)` (inferred from the sub-primitives if omitted)
        :param plot_range: the inset's data range (inferred if omitted)
        :param opts: extra options for the inset axes
        """
        ...

    @property
    def plot_range(self):
        """
        **LLM Docstring**

        The inset's data range (computed from the sub-primitives when not set).

        :return: the `[(left, right), (bottom, top)]` range
        :rtype: list
        """
        ...

    @plot_range.setter
    def plot_range(self, pr):
        """
        **LLM Docstring**

        The inset's data range (computed from the sub-primitives when not set).

        :return: the `[(left, right), (bottom, top)]` range
        :rtype: list
        """
        ...

    def get_plot_range(self):
        """
        **LLM Docstring**

        Compute the inset's data range as the union of its sub-primitives' bounding
        boxes.

        :return: the `[(left, right), (bottom, top)]` range
        :rtype: list
        """
        ...

    @property
    def dimensions(self):
        """
        **LLM Docstring**

        The inset's `(width, height)`, derived from the data range (and filling in a
        missing dimension from the aspect ratio).

        :return: the dimensions
        :rtype: tuple
        """
        ...

    def get_bbox(self, graphics=None, preserve_aspect=None):
        """
        **LLM Docstring**

        Compute the inset's bounding box in the parent's coordinates, optionally
        correcting the height/width to preserve the sub-primitives' aspect ratio.

        :param graphics: the parent graphics (used for aspect correction)
        :param preserve_aspect: preserve the sub-primitives' aspect ratio
        :type preserve_aspect: bool | None
        :return: the `[[min_x, min_y], [max_x, max_y]]` bounding box
        :rtype: list
        """
        ...

    def get_axes(self, graphics, bbox=None, **opts):
        """
        **LLM Docstring**

        Create (and cache) the inset axes on the parent graphics for the given bounding
        box, closing any previous inset for that figure.

        :param graphics: the parent graphics
        :param bbox: the inset bounding box (computed if omitted)
        :param opts: options for the inset axes
        :return: the inset axes
        """
        ...

    def plot(self, axes, *args, graphics=None, **kwargs):
        """
        **LLM Docstring**

        Draw the inset: create its axes on the parent and render (or re-host) each
        sub-primitive into it.

        :param axes: the axes (or graphics) to draw onto
        :param args: extra positional arguments
        :param graphics: the parent graphics (defaults to `axes`)
        :param kwargs: extra options
        :return: the drawn sub-primitives
        :rtype: list
        :raises NotImplementedError: when drawing into a VTK window
        """
        ...