
from __future__ import annotations

from .. import Numputils as nput
from ..Jupyter import JHTML
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# Bounding box
# ---------------------------------------------------------------------------

@dataclass
class BoundingBox:
    x:      float   # left edge
    y:      float   # top edge
    width:  float
    height: float

    @property
    def x2(self) -> float: return self.x + self.width
    @property
    def y2(self) -> float: return self.y + self.height
    @property
    def cx(self) -> float: return self.x + self.width  / 2
    @property
    def cy(self) -> float: return self.y + self.height / 2

    def union(self, other: BoundingBox) -> BoundingBox:
        x  = min(self.x,  other.x)
        y  = min(self.y,  other.y)
        x2 = max(self.x2, other.x2)
        y2 = max(self.y2, other.y2)
        return BoundingBox(x, y, x2 - x, y2 - y)

    def __repr__(self) -> str:
        return (f"BoundingBox(x={self.x:.3g}, y={self.y:.3g}, w={self.width:.3g}, h={self.height:.3g})")

class Transform:
    __slots__ = ("_m",)
    def __init__(self, m):
        self._m = np.asanyarray(m)

    @classmethod
    def identity(cls):
        return np.eye(3)

    @classmethod
    def translate(cls, tx, ty):
        mat = np.eye(3)
        mat[2, 0] = tx
        mat[2, 1] = ty
        return mat

    @classmethod
    def scale(cls, sx, sy):
        mat = np.eye(3)
        mat[0, 0] = sx
        mat[1, 1] = sy
        return mat

    @classmethod
    def rotate(cls, deg: float, shift=None):
        mat = np.eye(3)
        r = nput.rotation_matrix('2d', np.deg2rad(deg))
        mat[:2, :2] = r
        if shift is not None:
            tf = cls.translate(*shift)
            tf_inv = cls.translate(-shift[0], -shift[1])
            mat = (
                tf
                @ mat
                @ tf_inv
            )
        return mat

    @classmethod
    def skew(cls, deg_x: float, deg_y:float):
        mat = np.eye(3)
        skew_x = np.tan(np.deg2rad(deg_x))
        skew_y = np.tan(np.deg2rad(deg_y))
        mat[0, 1] = skew_x
        mat[1, 0] = skew_y
        return mat

    def apply(self, points):
        m = self._m
        points = np.asanyarray(points)
        smol = points.ndim == 1
        if smol:
            points = points[np.newaxis]
        points = points @ m[:2, :2] + m[:2, 2][np.newaxis]
        if smol:
            points = points[0]
        return points

    def apply_bbox(self, bb: BoundingBox) -> BoundingBox:
        """Transform all four corners then take the axis-aligned envelope."""
        points = bb.to_array()
        corners = self.apply(points)
        xs = corners[:, 0]
        ys = corners[:, 1]
        x = np.min(xs); y = np.min(ys)
        return BoundingBox(x, y, np.max(xs)-x, np.max(ys)-y)

    # ── parsing ────────────────────────────────────────────────────────────

    @classmethod
    def from_str(cls, s: str) -> Transform:
        """Parse an SVG transform attribute string into a Transform."""
        _fn = re.compile(
            r"(matrix|translate|scale|rotate|skewX|skewY)"
            r"\s*\(([^)]*)\)", re.I)
        result = cls.identity()
        for name, args_str in _fn.findall(s):
            args = [float(v) for v in re.split(r"[\s,]+", args_str.strip()) if v]
            name = name.lower()
            if name == "matrix":
                a,b,c,d,e,f = args
                t = np.array([[a,c,e], [b,d,f], [0,0,1]])
            elif name == "translate":
                t = cls.translate(args[0], args[1] if len(args)>1 else 0.0)
            elif name == "scale":
                t = cls.scale(args[0], args[1] if len(args)>1 else None)
            elif name == "rotate":
                cx, cy = (args[1], args[2]) if len(args) == 3 else (0.0, 0.0)
                t = cls.rotate(args[0], [cx, cy])
            elif name == "skewx":
                t = cls.skew(args[0], 0)
            elif name == "skewy":
                t = cls.skew(1, args[0])
            else:
                continue
            result = result @ t
        return cls(result)


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------
SVG = JHTML.SVGContext
class SVGPrimitive(ABC):
    """
    Abstract base for SVG 2-D shape primitives.

    Parameters
    ----------
    presentation : dict
        Any SVG presentation attributes (fill, stroke, transform, …).
        Validated against COMMON_PRESENTATION + COMMON_TEXT_PRESENTATION
        when svg_validator is available.
    extra_attrs  : dict
        Additional element-level attributes not covered by presentation
        (e.g. id, class, data-*).
    """

    wrapper: SVG.TagElement
    def __init__(self, **attrs):
        self.styles, self.attrs = self.split_attrs(attrs)

    def get_attr(self, attr):
        return self.attrs.get(attr)
    def set_attr(self, attr, val):
        self.attrs[attr] = val

    def split_attrs(self, attrs):
        styles = {}
        new_attrs = {}
        for k,v in attrs.items():
            if k in SVG.COMMON_ALL:
                styles[k] = v
            else:
                new_attrs[k] = v
        return styles, new_attrs

    def _build_attrs(self, shape_attrs: dict[str, Any]) -> dict[str, str]:
        """Merge shape geometry, presentation, and extra attrs → str dict."""
        merged: dict[str, Any] = {**shape_attrs, **self.presentation, **self.extra_attrs}
        return {k: str(v) for k, v in merged.items() if v is not None}

    def _transform(self) -> Transform | None:
        t = self.styles.get("transform")
        return Transform.from_str(t) if t else None

    def _apply_transform(self, bb: BoundingBox) -> BoundingBox:
        t = self._transform()
        return t.apply_bbox(bb) if t else bb

    def _fmt(self, v: float, precision: int = 6) -> str:
        """Format a float compactly (strip trailing zeros)."""
        return f"{v:.{precision}f}".rstrip("0").rstrip(".")

    def _prep_attrs(self, attrs:dict):
        return attrs
    def to_svg(self) -> str:
        return self.wrapper(self._prep_attrs(self.styles | self.attrs))

    @abstractmethod
    def _raw_bbox(self) -> list[float]:
        """
        Return the axis-aligned bounding box in the parent coordinate system
        (i.e. after any transform has been applied).
        """

    def get_bbox(self) -> BoundingBox:
        return self._apply_transform(BoundingBox(*self._raw_bbox()))

    def __repr__(self) -> str:
        return f"{type(self).__name__}(bbox={self.get_bbox()})"


class Rect(SVGPrimitive):
    wrapper = SVG.Rect
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x=x, y=y, width=width, height=height, **kwargs)

    @property
    def x(self): return self.get_attr("x")
    @x.setter
    def x(self, value): self.set_attr("x", value)
    @property
    def y(self): return self.get_attr("y")
    @y.setter
    def y(self, value): self.set_attr("y", value)
    @property
    def width(self): return self.get_attr("width")
    @width.setter
    def width(self, value): self.set_attr("width", value)
    @property
    def height(self): return self.get_attr("height")
    @height.setter
    def height(self, value): self.set_attr("height", value)

    def _raw_bbox(self):
        ...
class Circle(SVGPrimitive):
    wrapper = SVG.Circle
    def __init__(self, cx, cy, r, **kwargs):
        super().__init__(cx=cx, cy=cy, r=r, **kwargs)

    @property
    def cx(self): return self.get_attr("cx")
    @cx.setter
    def cx(self, value): self.set_attr("cx", value)
    @property
    def cy(self): return self.get_attr("cy")
    @cy.setter
    def cy(self, value): self.set_attr("cy", value)
    @property
    def r(self): return self.get_attr("r")
    @r.setter
    def r(self, value): self.set_attr("r", value)

    def _raw_bbox(self):
        return [self.cx - self.r, self.cy - self.r, self.r * 2, self.r * 2]
class Ellipse(SVGPrimitive):
    wrapper = SVG.Ellipse
    def __init__(self, cx, cy, rx, ry, **kwargs):
        super().__init__(cx=cx, cy=cy, rx=rx, ry=ry, **kwargs)

    @property
    def cx(self): return self.get_attr("cx")
    @cx.setter
    def cx(self, value): self.set_attr("cx", value)
    @property
    def cy(self): return self.get_attr("cy")
    @cy.setter
    def cy(self, value): self.set_attr("cy", value)
    @property
    def rx(self): return self.get_attr("rx")
    @rx.setter
    def rx(self, value): self.set_attr("rx", value)
    @property
    def ry(self): return self.get_attr("ry")
    @ry.setter
    def ry(self, value): self.set_attr("ry", value)

    def _raw_bbox(self):
        return [
            self.cx - self.rx, self.cy - self.ry,
            self.rx * 2, self.ry * 2
        ]

class Line(SVGPrimitive):
    wrapper = SVG.Line
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super().__init__(x1=x1, y1=y1, x2=x2, y2=y2, **kwargs)

    @property
    def x1(self): return self.get_attr("x1")
    @x1.setter
    def x1(self, value): self.set_attr("x1", value)
    @property
    def y1(self): return self.get_attr("y1")
    @y1.setter
    def y1(self, value): self.set_attr("y1", value)
    @property
    def x2(self): return self.get_attr("x2")
    @x2.setter
    def x2(self, value): self.set_attr("x2", value)
    @property
    def y2(self): return self.get_attr("y2")
    @y2.setter
    def y2(self, value): self.set_attr("y2", value)

    def _raw_bbox(self):
        x = min(self.x1, self.x2); y = min(self.y1, self.y2)
        return [x, y, abs(self.x2 - self.x1), abs(self.y2 - self.y1)]

class Polyline(SVGPrimitive):
    wrapper = SVG.Polyline
    def __init__(self, points, **kwargs):
        points = np.asanyarray(points)
        super().__init__(points=points, **kwargs)

    @property
    def points(self): return self.get_attr("points")
    @points.setter
    def points(self, value): self.set_attr("points", value)

    def _raw_bbox(self):
        x = np.min(self.points, axis=0)
        y = np.min(self.points, axis=1)
        bb = BoundingBox(x, y, np.max(self.points, axis=0) - x, np.max(self.points, axis=1) - y)
        return self._apply_transform(bb)
class Polygon(SVGPrimitive):
    wrapper = SVG.Polygon
    def __init__(self, points, **kwargs):
        super().__init__(points=points, **kwargs)

    @property
    def points(self): return self.get_attr("points")
    @points.setter
    def points(self, value): self.set_attr("points", value)

    def _raw_bbox(self):
        x = np.min(self.points, axis=0)
        y = np.min(self.points, axis=1)
        bb = BoundingBox(x, y, np.max(self.points, axis=0) - x, np.max(self.points, axis=1) - y)
        return self._apply_transform(bb)
class Path(SVGPrimitive):
    wrapper = SVG.Path
    def __init__(self, d, **kwargs):
        if isinstance(d, str):
            d = self.parse_path(d)
        super().__init__(d=d, **kwargs)

    _CMD_RE = re.compile(r"([MmZzLlHhVvCcSsQqTtAa])")
    _NUM_RE = re.compile(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")
    @classmethod
    def parse_path(cls, d: str) -> list[tuple[str, list[float]]]:
        """Return list of (command, [args]) tuples."""
        tokens = []
        for part in cls._CMD_RE.split(d):
            part = part.strip().upper()
            if not part:
                continue
            if cls._CMD_RE.fullmatch(part):
                tokens.append((part, []))
            else:
                if tokens:
                    tokens[-1][1].extend(float(v) for v in cls._NUM_RE.findall(part))
        return tokens

    @property
    def d(self): return self.get_attr("d")
    @d.setter
    def d(self, value): self.set_attr("d", value)

    def _raw_bbox(self):
        extrema = self._all_extrema()
        x = np.min(extrema, axis=0)
        y = np.min(extrema, axis=1)
        X = np.max(x, axis=0)
        Y = np.max(x, axis=1)
        return [x, y, X-x, Y-y]

    def _quadratic_solve(self, cx, cy, x1, y1, x2, y2):
        subpoints = []
        subpoints.append(np.array([[cx, cy]]))
        tx = nput.bezier_solve([x1, cx, x2])
        tx = tx[tx >= 0]
        xx_points = nput.bezier_eval([x1, cx, x2], tx)
        xy_points = nput.bezier_eval([y1, cy, y2], tx)
        subpoints.append(np.concatenate([
            xx_points[:, np.newaxis],
            xy_points[:, np.newaxis],
        ], axis=1))

        ty = nput.bezier_solve([y1, cy, y2])
        ty = ty[ty >= 0]
        yx_points = nput.bezier_eval([x1, cx, x2], ty)
        yy_points = nput.bezier_eval([y1, cy, y2], ty)
        subpoints.append(np.concatenate([
            yx_points[:, np.newaxis],
            yy_points[:, np.newaxis],
        ], axis=1))

        return subpoints

    def _cubic_solve(self, cx, cy, x1, y1, x2, y2, x3, y3):
        subpoints = []
        subpoints.append(np.array([[cx, cy]]))
        tx = nput.bezier_solve([x1, cx, x2, x3])
        tx = tx[tx >= 0]
        xx_points = nput.bezier_eval([x1, cx, x2, x3], tx)
        xy_points = nput.bezier_eval([y1, cy, y2, y3], tx)
        subpoints.append(np.concatenate([
            xx_points[:, np.newaxis],
            xy_points[:, np.newaxis],
        ], axis=1))

        ty = nput.bezier_solve([y1, cy, y2, y3])
        ty = ty[ty >= 0]
        yx_points = nput.bezier_eval([x1, cx, x2, x3], ty)
        yy_points = nput.bezier_eval([y1, cy, y2, y3], ty)
        subpoints.append(np.concatenate([
            yx_points[:, np.newaxis],
            yy_points[:, np.newaxis],
        ], axis=1))

        return subpoints

    def _all_extrema(self) -> np.ndarray:
        """Walk the path and collect all geometrically significant points."""
        point_lists: list[np.ndarray] = []
        cx = cy = 0.0          # current point
        sx = sy = 0.0          # start of current subpath (for Z)
        last_ctrl: tuple[float,float] | None = None  # last control point for S/T

        for cmd, args in self.d:
            rel = cmd.islower()
            ox, oy = (cx, cy) if rel else (0.0, 0.0)

            if cmd in "Mm":
                args = np.asanyarray(args).reshape((-1, 2))
                new_points = args + np.array([[ox, oy]])
                # point_lists.append(new_points)
                cx, cy = new_points[-1]
                sx, sy = new_points[0]
                last_ctrl = None

            elif cmd in "Zz":
                # point_lists.append([[sx, sy]])
                cx, cy = sx, sy
                last_ctrl = None

            elif cmd in "Ll":
                args = np.asanyarray(args).reshape((-1, 2))
                new_points = args + np.array([[ox, oy]])
                point_lists.append(new_points)
                cx, cy = new_points[-1]
                last_ctrl = None

            elif cmd in "Hh":
                new_x = ox + np.asanyarray(args)
                point_lists.append(np.array([new_x, np.full(new_x.shape, cy)]).T)
                last_ctrl = None

            elif cmd in "Vv":
                new_y = oy + np.asanyarray(args)
                point_lists.append(np.array([np.full(new_y.shape, cx), new_y]).T)
                last_ctrl = None

            elif cmd in "Cc":
                args = np.asanyarray(args).reshape((-1, 3, 2)) + np.array([[[ox, oy]]])
                point_lists.append(args.reshape((-1, 2)))
                subpoints = []

                for (x1, y1), (x2, y2), (x3, y3) in args:
                    subpoints.extend(
                        self._cubic_solve(cx, cy, x1, y1, x2, y2, x3, y3)
                    )
                    last_ctrl = (x2, y2)
                    cx, cy = x3, y3

                point_lists.append(np.concatenate(subpoints, axis=0))

            elif cmd in "Ss":
                args = np.asanyarray(args).reshape((-1, 2, 2)) + np.array([[[ox, oy]]])
                subpoints = []
                for (x2, y2), (x3, y3) in args:
                    lc = last_ctrl or (cx, cy)
                    x1,y1 = 2*cx-lc[0], 2*cy-lc[1]  # reflected control
                    subpoints.extend(
                        self._cubic_solve(cx, cy, x1, y1, x2, y2, x3, y3)
                    )
                    last_ctrl = (x2, y2)
                    cx, cy = x3, y3

                point_lists.append(np.concatenate(subpoints, axis=0))

            elif cmd in "Qq":
                args = np.asanyarray(args).reshape((-1, 2, 2)) + np.array([[[ox, oy]]])
                subpoints = []
                for (x1, y1), (x2, y2) in args:
                    subpoints.extend(
                        self._quadratic_solve(cx, cy, x1, y1, x2, y2)
                    )
                    last_ctrl = (x1, y1)
                    cx, cy = x2, y2

                point_lists.append(np.concatenate(subpoints, axis=0))

            elif cmd in "Tt":
                args = np.asanyarray(args).reshape((-1, 2)) + np.array([[ox, oy]])
                subpoints = []
                for x2, y2 in args:
                    lc = last_ctrl or (cx, cy)
                    x1,y1 = 2*cx-lc[0], 2*cy-lc[1]
                    subpoints.append([(cx,cy),(x1,y1),(x2,y2)])
                    subpoints.extend(self._quadratic_solve(cx, cy, x1, y1, x2, y2))
                    last_ctrl = (x1, y1)
                    cx, cy = x2, y2

                point_lists.append(np.concatenate(subpoints, axis=0))

            elif cmd in "Aa":
                args = np.asanyarray(args).reshape((-1, 7))
                for rx, ry, phi_deg, large, sweep, x2, y2 in args:
                    if isinstance(large, str):
                        large = int(large)
                    if isinstance(sweep, str):
                        sweep = int(sweep)
                    x2, y2 = x2+ox, y2+oy
                    point_lists.append(
                        nput.arc_points_from_endpoints(
                            [cx, cy],
                            end=[x2, y2],
                            radius=[rx, ry],
                            rotation=phi_deg,
                            use_major_rotation=large,
                            clockwise=sweep
                        )
                    )
                    cx, cy = x2, y2
                last_ctrl = None

        return np.concatenate(point_lists, axis=0)

# class SVGAxes(GraphicsAxes3D):
#     """
#     3D SVG Renderer
#     ===============
#     Renders 3D objects to SVG by projecting geometry through a render matrix,
#     then dispatching to pluggable draw_* primitives.
#
#     Pipeline:
#       3D world coords → render matrix (model-view-projection) → NDC → SVG coords
#       → depth-sorted draw calls → SVG document
#     """
#
#     import xml.etree.ElementTree as ET
#     from dataclasses import dataclass, field
#     from typing import Callable, Any
#     import math
#
#     # ---------------------------------------------------------------------------
#     # Linear algebra helpers
#     # ---------------------------------------------------------------------------
#
#     Vec3 = tuple[float, float, float]
#     Vec4 = tuple[float, float, float, float]
#     Mat4 = list[list[float]]  # row-major 4×4
#
#     def mat4_identity() -> Mat4:
#         return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
#
#     def mat4_mul(a: Mat4, b: Mat4) -> Mat4:
#         return [
#             [sum(a[r][k] * b[k][c] for k in range(4)) for c in range(4)]
#             for r in range(4)
#         ]
#
#     def mat4_transform(m: Mat4, v: Vec4) -> Vec4:
#         return tuple(sum(m[r][c] * v[c] for c in range(4)) for r in range(4))
#
#     def perspective_matrix(fov_deg: float, aspect: float,
#                            near: float, far: float) -> Mat4:
#         f = 1.0 / math.tan(math.radians(fov_deg) / 2)
#         nf = 1.0 / (near - far)
#         return [
#             [f / aspect, 0, 0, 0],
#             [0, f, 0, 0],
#             [0, 0, (far + near) * nf, 2 * far * near * nf],
#             [0, 0, -1, 0],
#         ]
#
#     def look_at(eye: Vec3, center: Vec3, up: Vec3) -> Mat4:
#         ex, ey, ez = eye
#         cx, cy, cz = center
#         ux, uy, uz = up
#
#         fz = _norm((ex - cx, ey - cy, ez - cz))
#         fx = _norm(_cross((ux, uy, uz), fz))
#         fy = _cross(fz, fx)
#
#         return [
#             [fx[0], fx[1], fx[2], -_dot(fx, eye)],
#             [fy[0], fy[1], fy[2], -_dot(fy, eye)],
#             [fz[0], fz[1], fz[2], -_dot(fz, eye)],
#             [0, 0, 0, 1],
#         ]
#
#     def _dot(a: Vec3, b: Vec3) -> float:
#         return sum(x * y for x, y in zip(a, b))
#
#     def _cross(a: Vec3, b: Vec3) -> Vec3:
#         return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
#
#     def _norm(v: Vec3) -> Vec3:
#         n = math.sqrt(sum(x * x for x in v))
#         return tuple(x / n for x in v)
#
#     # ---------------------------------------------------------------------------
#     # SVG primitive builders  (draw_* functions)
#     # ---------------------------------------------------------------------------
#     # Each returns an (element, depth) pair so the renderer can depth-sort.
#     # All coordinates are already in SVG space when these are called.
#
#     Style = dict[str, str]
#
#     _DEFAULT_LINE = {"stroke": "black", "stroke-width": "1.5", "stroke-linecap": "round"}
#     _DEFAULT_DISK = {"fill": "steelblue", "stroke": "black", "stroke-width": "1"}
#     _DEFAULT_POLY = {"fill": "lightgray", "stroke": "black", "stroke-width": "1"}
#     _DEFAULT_TEXT = {"font-size": "12", "font-family": "sans-serif", "fill": "black"}
#
#     def draw_line(x1: float, y1: float, x2: float, y2: float,
#                   depth: float = 0.0, style: Style | None = None) -> tuple[ET.Element, float]:
#         """Straight line between two projected 2-D points."""
#         attrs = {**_DEFAULT_LINE, **(style or {}),
#                  "x1": f"{x1:.2f}", "y1": f"{y1:.2f}",
#                  "x2": f"{x2:.2f}", "y2": f"{y2:.2f}"}
#         return ET.Element("line", attrs), depth
#
#     def draw_disk(cx: float, cy: float, r: float,
#                   depth: float = 0.0, style: Style | None = None) -> tuple[ET.Element, float]:
#         """Filled circle (projected sphere cross-section or point marker)."""
#         attrs = {**_DEFAULT_DISK, **(style or {}),
#                  "cx": f"{cx:.2f}", "cy": f"{cy:.2f}", "r": f"{r:.2f}"}
#         return ET.Element("circle", attrs), depth
#
#     def draw_polygon(points: list[tuple[float, float]],
#                      depth: float = 0.0, style: Style | None = None) -> tuple[ET.Element, float]:
#         """Filled polygon (face of a mesh)."""
#         pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
#         attrs = {**_DEFAULT_POLY, **(style or {}), "points": pts}
#         return ET.Element("polygon", attrs), depth
#
#     def draw_text(x: float, y: float, label: str,
#                   depth: float = 0.0, style: Style | None = None) -> tuple[ET.Element, float]:
#         """Text label at a projected point."""
#         attrs = {**_DEFAULT_TEXT, **(style or {}), "x": f"{x:.2f}", "y": f"{y:.2f}"}
#         el = ET.Element("text", attrs)
#         el.text = label
#         return el, depth
#
#     # ---------------------------------------------------------------------------
#     # Projection helpers
#     # ---------------------------------------------------------------------------
#
#     @dataclass
#     class Viewport:
#         width: float = 800.0
#         height: float = 600.0
#
#     def project_point(p: Vec3, mvp: Mat4, vp: Viewport) -> tuple[float, float, float] | None:
#         """
#         Transform a world-space point through the MVP matrix and map to SVG coords.
#         Returns (svg_x, svg_y, ndc_z) or None if behind the near plane / clipped.
#         """
#         x, y, z = p
#         clip = mat4_transform(mvp, (x, y, z, 1.0))
#         cx, cy, cz, cw = clip
#
#         if cw <= 0:  # behind camera
#             return None
#         if abs(cx / cw) > 1.1 or abs(cy / cw) > 1.1:  # simple frustum cull
#             return None
#
#         ndc_x = cx / cw
#         ndc_y = cy / cw
#         ndc_z = cz / cw  # depth in [-1, 1]
#
#         svg_x = (ndc_x + 1.0) * 0.5 * vp.width
#         svg_y = (1.0 - (ndc_y + 1.0) * 0.5) * vp.height  # flip Y
#         return svg_x, svg_y, ndc_z
#
#     # ---------------------------------------------------------------------------
#     # 3-D object descriptors
#     # ---------------------------------------------------------------------------
#
#     @dataclass
#     class Object3D:
#         """Base class — subclass and override `to_draw_calls`."""
#         style: Style = field(default_factory=dict)
#
#         def to_draw_calls(self, mvp: Mat4, vp: Viewport
#                           ) -> list[tuple[ET.Element, float]]:
#             raise NotImplementedError
#
#     @dataclass
#     class Point3D(Object3D):
#         position: Vec3 = (0, 0, 0)
#         radius: float = 5.0
#
#         def to_draw_calls(self, mvp, vp):
#             proj = project_point(self.position, mvp, vp)
#             if proj is None:
#                 return []
#             sx, sy, depth = proj
#             return [draw_disk(sx, sy, self.radius, depth, self.style or None)]
#
#     @dataclass
#     class Line3D(Object3D):
#         start: Vec3 = (0, 0, 0)
#         end: Vec3 = (1, 0, 0)
#
#         def to_draw_calls(self, mvp, vp):
#             p1 = project_point(self.start, mvp, vp)
#             p2 = project_point(self.end, mvp, vp)
#             if p1 is None or p2 is None:
#                 return []
#             depth = (p1[2] + p2[2]) / 2
#             return [draw_line(p1[0], p1[1], p2[0], p2[1], depth, self.style or None)]
#
#     @dataclass
#     class Polygon3D(Object3D):
#         vertices: list[Vec3] = field(default_factory=list)
#
#         def to_draw_calls(self, mvp, vp):
#             projected = [project_point(v, mvp, vp) for v in self.vertices]
#             if any(p is None for p in projected):
#                 return []
#             pts = [(p[0], p[1]) for p in projected]
#             depth = sum(p[2] for p in projected) / len(projected)
#             return [draw_polygon(pts, depth, self.style or None)]
#
#     @dataclass
#     class Label3D(Object3D):
#         position: Vec3 = (0, 0, 0)
#         text: str = ""
#
#         def to_draw_calls(self, mvp, vp):
#             proj = project_point(self.position, mvp, vp)
#             if proj is None:
#                 return []
#             sx, sy, depth = proj
#             return [draw_text(sx, sy, self.text, depth, self.style or None)]
#
#     @dataclass
#     class Mesh3D(Object3D):
#         """Triangle/quad mesh defined by vertices + face index lists."""
#         vertices: list[Vec3] = field(default_factory=list)
#         faces: list[list[int]] = field(default_factory=list)
#         face_styles: list[Style] = field(default_factory=list)
#
#         def to_draw_calls(self, mvp, vp):
#             calls = []
#             for i, face in enumerate(self.faces):
#                 verts = [self.vertices[j] for j in face]
#                 st = self.face_styles[i] if i < len(self.face_styles) else self.style or {}
#                 poly = Polygon3D(vertices=verts, style=st)
#                 calls.extend(poly.to_draw_calls(mvp, vp))
#             return calls
#
#     # ---------------------------------------------------------------------------
#     # Main renderer
#     # ---------------------------------------------------------------------------
#
#     def render_svg(
#             objects: list[Object3D],
#             render_matrix: Mat4,
#             viewport: Viewport | None = None,
#             background: str | None = None,
#             title: str | None = None,
#             sort_order: str = "back_to_front",  # "back_to_front" | "front_to_back" | "none"
#     ) -> str:
#         """
#         Render a list of Object3D instances to an SVG string.
#
#         Parameters
#         ----------
#         objects       : Scene objects to render.
#         render_matrix : Combined MVP (model-view-projection) matrix — a 4×4
#                         row-major list-of-lists.  Build it with, e.g.:
#                           mvp = mat4_mul(perspective_matrix(...), look_at(...))
#         viewport      : SVG canvas size (default 800×600).
#         background    : Optional background fill colour.
#         title         : Optional <title> element text.
#         sort_order    : Painter's-algorithm sort direction.
#
#         Returns
#         -------
#         SVG markup as a string.
#         """
#         vp = viewport or Viewport()
#
#         svg = ET.Element("svg", {
#             "xmlns": "http://www.w3.org/2000/svg",
#             "width": str(vp.width),
#             "height": str(vp.height),
#             "viewBox": f"0 0 {vp.width} {vp.height}",
#         })
#
#         if title:
#             t = ET.SubElement(svg, "title")
#             t.text = title
#
#         if background:
#             ET.SubElement(svg, "rect", {
#                 "width": str(vp.width), "height": str(vp.height), "fill": background
#             })
#
#         # Collect all (element, depth) pairs
#         draw_calls: list[tuple[ET.Element, float]] = []
#         for obj in objects:
#             draw_calls.extend(obj.to_draw_calls(render_matrix, vp))
#
#         # Depth sort (painter's algorithm)
#         if sort_order == "back_to_front":
#             draw_calls.sort(key=lambda x: -x[1])  # largest ndc_z = furthest away
#         elif sort_order == "front_to_back":
#             draw_calls.sort(key=lambda x: x[1])
#
#         for el, _ in draw_calls:
#             svg.append(el)
#
#         ET.indent(svg, space="  ")
#         return ET.tostring(svg, encoding="unicode", xml_declaration=False)

# class SVGFigure(GraphicsFigure):
#     Axes = SVGAxes