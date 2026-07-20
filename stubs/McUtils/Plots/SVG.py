from __future__ import annotations
import functools
from .. import Numputils as nput
from ..Jupyter import JHTML
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
import numpy as np
__all__ = ['SVGFigure', 'SVGFigure3D']

@dataclass
class SVGBoundingBox:
    x: float
    y: float
    width: float
    height: float

    @property
    def x2(self) -> float:
        ...

    @property
    def y2(self) -> float:
        ...

    @property
    def cx(self) -> float:
        ...

    @property
    def cy(self) -> float:
        ...

    def union(self, other: SVGBoundingBox) -> SVGBoundingBox:
        ...

    def to_array(self):
        ...

    def __repr__(self) -> str:
        ...

class SVGTransform:
    __slots__ = ('_m',)

    def __init__(self, m):
        ...

    @classmethod
    def identity(cls):
        ...

    @classmethod
    def translate(cls, tx, ty):
        ...

    @classmethod
    def scale(cls, sx, sy):
        ...

    @classmethod
    def rotate(cls, deg: float, shift=None):
        ...

    @classmethod
    def skew(cls, deg_x: float, deg_y: float):
        ...

    def apply(self, points):
        ...

    def apply_bbox(self, bb: SVGBoundingBox) -> SVGBoundingBox:
        """Transform all four corners then take the axis-aligned envelope."""
        ...

    @classmethod
    def from_str(cls, s: str) -> SVGTransform:
        """Parse an SVG transform attribute string into a Transform."""
        ...

    @classmethod
    def matrix_to_commands(cls, mat):
        ...

    def to_str(self):
        ...

    @classmethod
    def from_commands(cls, commands):
        ...
SVG = JHTML.SVGContext

class SVGPrimitive(ABC):
    wrapper: SVG.TagElement

    def __init__(self, *body, **attrs):
        ...

    def get_attr(self, attr):
        ...

    def set_attr(self, attr, val):
        ...

    def split_attrs(self, attrs):
        ...

    def _build_attrs(self, shape_attrs: dict[str, Any]) -> dict[str, str]:
        """Merge shape geometry, presentation, and extra attrs → str dict."""
        ...

    def _transform(self) -> SVGTransform | None:
        ...

    def _apply_transform(self, bb: SVGBoundingBox) -> SVGBoundingBox:
        ...

    def _prep_attrs(self, attrs: dict):
        ...

    def to_svg(self) -> str:
        ...

    @abstractmethod
    def _raw_bbox(self) -> list[float]:
        """
        Return the axis-aligned bounding box in the parent coordinate system
        (i.e. after any transform has been applied).
        """
        ...

    def get_bbox(self) -> SVGBoundingBox:
        ...

    def __repr__(self) -> str:
        ...

class SVGRect(SVGPrimitive):
    wrapper = SVG.Rect

    def __init__(self, x, y, width, height, **kwargs):
        ...

    @property
    def x(self):
        ...

    @x.setter
    def x(self, value):
        ...

    @property
    def y(self):
        ...

    @y.setter
    def y(self, value):
        ...

    @property
    def width(self):
        ...

    @width.setter
    def width(self, value):
        ...

    @property
    def height(self):
        ...

    @height.setter
    def height(self, value):
        ...

    def _raw_bbox(self):
        ...

class SVGCircle(SVGPrimitive):
    wrapper = SVG.Circle

    def __init__(self, cx, cy, r, **kwargs):
        ...

    @property
    def cx(self):
        ...

    @cx.setter
    def cx(self, value):
        ...

    @property
    def cy(self):
        ...

    @cy.setter
    def cy(self, value):
        ...

    @property
    def r(self):
        ...

    @r.setter
    def r(self, value):
        ...

    def _raw_bbox(self):
        ...

class SVGEllipse(SVGPrimitive):
    wrapper = SVG.Ellipse

    def __init__(self, cx, cy, rx, ry, **kwargs):
        ...

    @property
    def cx(self):
        ...

    @cx.setter
    def cx(self, value):
        ...

    @property
    def cy(self):
        ...

    @cy.setter
    def cy(self, value):
        ...

    @property
    def rx(self):
        ...

    @rx.setter
    def rx(self, value):
        ...

    @property
    def ry(self):
        ...

    @ry.setter
    def ry(self, value):
        ...

    def _raw_bbox(self):
        ...

class SVGLine(SVGPrimitive):
    wrapper = SVG.Line

    def __init__(self, x1, y1, x2, y2, **kwargs):
        ...

    @property
    def x1(self):
        ...

    @x1.setter
    def x1(self, value):
        ...

    @property
    def y1(self):
        ...

    @y1.setter
    def y1(self, value):
        ...

    @property
    def x2(self):
        ...

    @x2.setter
    def x2(self, value):
        ...

    @property
    def y2(self):
        ...

    @y2.setter
    def y2(self, value):
        ...

    def _raw_bbox(self):
        ...

class SVGPolyline(SVGPrimitive):
    wrapper = SVG.Polyline

    def __init__(self, points, **kwargs):
        ...

    @property
    def points(self):
        ...

    @points.setter
    def points(self, value):
        ...

    def _raw_bbox(self):
        ...

    def _prep_points(self, points):
        ...

    def _prep_attrs(self, attrs: dict):
        ...

class SVGPolygon(SVGPrimitive):
    wrapper = SVG.Polygon

    def __init__(self, points, **kwargs):
        ...

    @property
    def points(self):
        ...

    @points.setter
    def points(self, value):
        ...

    def _raw_bbox(self):
        ...

    def _prep_points(self, points):
        ...

    def _prep_attrs(self, attrs: dict):
        ...

class SVGPath(SVGPrimitive):
    wrapper = SVG.Path

    def __init__(self, d, **kwargs):
        ...
    _CMD_RE = re.compile('([MmZzLlHhVvCcSsQqTtAa])')
    _NUM_RE = re.compile('[+-]?(?:\\d+\\.?\\d*|\\.\\d+)(?:[eE][+-]?\\d+)?')

    @classmethod
    def parse_path(cls, d: str) -> list[tuple[str, list[float]]]:
        """Return list of (command, [args]) tuples."""
        ...

    @property
    def d(self):
        ...

    @d.setter
    def d(self, value):
        ...

    def _prep_attrs(self, attrs: dict):
        ...

    def _prep_path(self, d):
        ...

    def _raw_bbox(self):
        ...

    def _quadratic_solve(self, cx, cy, x1, y1, x2, y2):
        ...

    def _cubic_solve(self, cx, cy, x1, y1, x2, y2, x3, y3):
        ...

    @classmethod
    def from_mpl(cls, path, target_bbox: tuple[tuple[float, float], tuple[float, float]]=None, base_height=None, y_flip: bool=True):
        ...

    def _all_extrema(self) -> np.ndarray:
        """Walk the path and collect all geometrically significant points."""
        ...

class SVGText(SVGPrimitive):
    wrapper = SVG.Text

    def __init__(self, text, x, y, **kwargs):
        ...

    @property
    def x(self):
        ...

    @x.setter
    def x(self, value):
        ...

    @property
    def y(self):
        ...

    @y.setter
    def y(self, value):
        ...

    @property
    def text(self):
        ...

    @text.setter
    def text(self, value):
        ...

    def _raw_bbox(self):
        ...

class SVGFigure:
    Circle = SVGCircle
    Line = SVGLine
    Ellipse = SVGEllipse
    Rect = SVGRect
    Polygon = SVGPolygon
    Polyline = SVGPolyline
    Path = SVGPath

    def __init__(self, elements=None, defs=None, view_box=None, preserve_aspect_ratio=None, **svg_kwargs):
        ...

    def create_element(self, element_type, **kwargs):
        ...

    def add_element(self, element_type, **kwargs):
        ...

    def add_rect(self, **kwargs):
        ...

    def add_circle(self, **kwargs):
        ...

    def add_ellipse(self, **kwargs):
        ...

    def add_line(self, **kwargs):
        ...

    def add_polyline(self, **kwargs):
        ...

    def add_polygon(self, **kwargs):
        ...

    def add_path(self, **kwargs):
        ...

    def add_text(self, **kwargs):
        ...

    def compute_viewbox(self):
        ...

    def add_def(self, id, *, tag, **opts):
        ...

    def create_def(self, *, id, tag='marker', body=None, **opts):
        ...

    def prep_element(self, e):
        ...

    def prep_draw_els(self, bbox, compute_bbox=None):
        ...

    def to_svg(self, compute_bbox=None, view_box=None, **opts):
        ...

class SVGPrimitive3D:
    wrapper: type[SVGPrimitive]

    @abstractmethod
    def prep_kwargs(self, projection_matrix) -> tuple[dict, tuple[float, float]]:
        ...

    def to_2d(self, projection_matrix):
        ...

    def compare_primitive(self, prim, depth1, depth2) -> int:
        ...

    def to_svg(self, projection_matrix):
        ...

class SVGPointsToShape3D(SVGPrimitive3D):

    def __init__(self, **kwargs):
        ...

    @abstractmethod
    def to_points(self):
        ...

    def get_depth(self, points):
        ...

    def prep_kwargs(self, projection_matrix, return_w=False, **extra):
        ...

class SVGPolygon3D(SVGPointsToShape3D):
    wrapper = SVGPolygon

    def __init__(self, points, **kwargs):
        ...

    def to_points(self):
        ...

class SVGPolyline3D(SVGPointsToShape3D):
    wrapper = SVGPolyline

    def __init__(self, points, **kwargs):
        ...

    def to_points(self):
        ...

class SVGLine3D(SVGPolyline3D):

    def __init__(self, x1, y1, z1, x2, y2, z2, **kwargs):
        ...

    @property
    def x1(self):
        ...

    @x1.setter
    def x1(self, value):
        ...

    @property
    def y1(self):
        ...

    @y1.setter
    def y1(self, value):
        ...

    @property
    def z1(self):
        ...

    @z1.setter
    def z1(self, value):
        ...

    @property
    def x2(self):
        ...

    @x2.setter
    def x2(self, value):
        ...

    @property
    def y2(self):
        ...

    @y2.setter
    def y2(self, value):
        ...

    @property
    def z2(self):
        ...

    @z2.setter
    def z2(self, value):
        ...

class SVGFlatPointsToShape3D(SVGPointsToShape3D):

    def __init__(self, normal=None, rotation=None, **kwargs):
        ...

    @abstractmethod
    def to_2d_points(self) -> tuple[np.ndarray, np.ndarray]:
        ...

    def get_rotation_matrix(self):
        ...

    def to_points(self):
        ...

class SVGPolylike3D(SVGFlatPointsToShape3D):

    def __init__(self, wrapper=None, **kwargs):
        ...

    def _infer_wrapper(self) -> type[SVGPrimitive]:
        ...

    @property
    def wrapper(self):
        ...

    @wrapper.setter
    def wrapper(self, value):
        ...

class SVGRect3D(SVGPolylike3D):

    def __init__(self, x, y, z, width, height, **kwargs):
        ...

    def to_2d_points(self):
        ...

class SVGCircle3D(SVGPolylike3D):

    def __init__(self, x, y, z, r, minor_radius=None, npoints=48, offset_angle=0, span_angle=2 * np.pi, **kwargs):
        ...

    def to_2d_points(self):
        ...

class SVGEllipse3D(SVGCircle3D):

    def __init__(self, x, y, z, rx, ry, **kwargs):
        ...

    @property
    def rx(self):
        ...

    @rx.setter
    def rx(self, value):
        ...

    @property
    def ry(self):
        ...

    @ry.setter
    def ry(self, value):
        ...

class SVGNonPlanarPolylike3D(SVGPointsToShape3D):

    def __init__(self, points, wrapper=None, **kwargs):
        ...

    def _infer_wrapper(self) -> type[SVGPrimitive]:
        ...

    @property
    def wrapper(self):
        ...

    @wrapper.setter
    def wrapper(self, value):
        ...

    def to_points(self):
        ...

class SVGPath3D(SVGNonPlanarPolylike3D):

    def __init__(self, d, rotation=None, normal=None, **kwargs):
        ...

    def prep_points(self, commands, rotation=None, normal=None):
        ...

class SVGCylinder(SVGPointsToShape3D):

    def __init__(self, start, end, radius, wrapper=None, **kwargs):
        ...

    def _infer_wrapper(self) -> type[SVGPrimitive]:
        ...

    @property
    def wrapper(self):
        ...

    @wrapper.setter
    def wrapper(self, value):
        ...

    def to_points(self):
        ...

    def compare_primitive(self, prim, depth1, depth2) -> int:
        ...

    def prep_kwargs(self, projection_matrix) -> tuple[dict, tuple[float, float]]:
        ...

class SVGSphere(SVGPointsToShape3D):
    wrapper = SVGCircle

    def __init__(self, center, radius, **kwargs):
        ...

    def to_points(self):
        ...

    def compare_primitive(self, prim, depth1, depth2) -> int:
        ...

    def prep_kwargs(self, projection_matrix) -> tuple[dict, tuple[float, float]]:
        ...

class SVGText3D(SVGPointsToShape3D):
    wrapper = SVGText

    def __init__(self, text, x, y, z, overlay=True, **kwargs):
        ...

    def to_points(self):
        ...

    def prep_kwargs(self, projection_matrix) -> tuple[dict, tuple[float, float]]:
        ...

    @property
    def x(self):
        ...

    @x.setter
    def x(self, value):
        ...

    @property
    def y(self):
        ...

    @y.setter
    def y(self, value):
        ...

    @property
    def z(self):
        ...

    @z.setter
    def z(self, value):
        ...

    def _raw_bbox(self):
        ...

class SVGFigure3D(SVGFigure):

    def __init__(self, elements=None, defs=None, view_matrix=None, perspective_matrix=None, world_matrix=None, view_position=None, view_center=None, up_vector=None, view_vector=None, right_vector=None, view_angle=None, aspect_ratio=None, view_distance=None, clip_distances=None, **kwargs):
        ...

    def get_projection_matrix(self):
        ...

    def get_projection_kwargs(self):
        ...

    def set_projection_kwargs(self, render_matrix=None, **kwargs):
        ...

    def create_element(self, element_type, **kwargs):
        ...

    def add_cylinder(self, **kwargs):
        ...

    def add_sphere(self, **kwargs):
        ...

    def prep_element(self, e):
        ...

    def compare_primitives(self, e1, e2):
        ...

    def sort_draw_els(self, els):
        ...

    def prep_draw_els(self, bbox, compute_bbox=None):
        ...

    def compute_viewbox(self):
        ...

    def to_svg(self, compute_bbox=None, view_box=None, **opts):
        ...