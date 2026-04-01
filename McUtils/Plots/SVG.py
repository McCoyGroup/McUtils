
from __future__ import annotations

from .. import Numputils as nput
from ..Jupyter import JHTML
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np

__all__ = [
    "SVGFigure",
    "SVGFigure3D"
]

@dataclass
class SVGBoundingBox:
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

    def union(self, other: SVGBoundingBox) -> SVGBoundingBox:
        x  = min(self.x,  other.x)
        y  = min(self.y,  other.y)
        x2 = max(self.x2, other.x2)
        y2 = max(self.y2, other.y2)
        return SVGBoundingBox(x, y, x2 - x, y2 - y)

    def to_array(self):
        return (self.x, self.x2, self.y, self.y2)

    def __repr__(self) -> str:
        return (f"BoundingBox(x={self.x:.3g}, y={self.y:.3g}, w={self.width:.3g}, h={self.height:.3g})")

class SVGTransform:
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
        points = points @ m[:2, :2].T + m[:2, 2][np.newaxis]
        if smol:
            points = points[0]
        return points

    def apply_bbox(self, bb: SVGBoundingBox) -> SVGBoundingBox:
        """Transform all four corners then take the axis-aligned envelope."""
        (l, r, b, t) = bb.to_array()
        corners = self.apply([
            [l, b],
            [l, r],
            [r, b],
            [r, t]
        ])
        xs = corners[:, 0]
        ys = corners[:, 1]
        x = np.min(xs); y = np.min(ys)
        return SVGBoundingBox(x, y, np.max(xs) - x, np.max(ys) - y)

    @classmethod
    def from_str(cls, s: str) -> SVGTransform:
        """Parse an SVG transform attribute string into a Transform."""
        _fn = re.compile(
            r"(matrix|translate|scale|rotate|skewX|skewY)"
            r"\s*\(([^)]*)\)", re.I)
        commands = [
            (
                name,
                [float(v) for v in re.split(r"[\s,]+", args_str.strip()) if v]
            )
            for name, args_str in _fn.findall(s)
        ]
        return cls.from_commands(commands)
    @classmethod
    def matrix_to_commands(cls, mat):
        pure_scale, pure_rot = nput.polar_decomposition(mat[:2, :2])
        commands = []
        x_scale = pure_scale[0, 0]
        y_scale = pure_scale[1, 1]
        if abs(x_scale - 1) > 1e-2 or abs(y_scale - 1) > 1e-2:
            commands.append(["scale", (x_scale, y_scale)])
        x_skew = pure_scale[0, 1]
        if abs(x_skew) > 1e-2:
            commands.append(["skewx", [x_skew]])
        y_skew = pure_scale[1, 0]
        if abs(y_skew) > 1e-2:
            commands.append(["skewy", [y_skew]])
        rot_angle = np.rad2deg(np.arctan2(pure_rot[1, 0], pure_rot[0, 0]))
        if abs(rot_angle) > .5 and abs(rot_angle) < 359.5:
            commands.append(["rotate", [rot_angle]])
        translation = mat[2, :2]
        if np.linalg.norm(translation) > 1e-2:
            commands.append(["translate", translation])
        if len(commands) > 2:
            return [["matrix", mat.flatten()]]
        else:
            return commands
    def to_str(self):
        bits = []
        for cmd, args in self.matrix_to_commands(self._m):
            arg_str=",".join(f"{a:.3g}" for a in args)
            bits.append(f"{cmd}({arg_str})")
        return "\n".join(bits)

    @classmethod
    def from_commands(cls, commands):
        result = cls.identity()
        for name, args in commands:
            name = name.lower()
            if name == "matrix":
                a, b, c, d, e, f = args
                t = np.array([[a, c, e], [b, d, f], [0, 0, 1]])
            elif name == "translate":
                t = cls.translate(args[0], args[1] if len(args) > 1 else 0.0)
            elif name == "scale":
                t = cls.scale(args[0], args[1] if len(args) > 1 else None)
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

SVG = JHTML.SVGContext
class SVGPrimitive(ABC):
    wrapper: SVG.TagElement
    def __init__(self, *body, **attrs):
        self.styles, self.attrs = self.split_attrs(attrs)
        self.body = body

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

    def _transform(self) -> SVGTransform | None:
        transform = self.styles.get("transform")
        if transform is not None:
            if isinstance(transform, str):
                transform = SVGTransform.from_str(transform)
            elif not isinstance(transform, SVGTransform):
                transform = SVGTransform.from_commands(transform)
        return transform

    def _apply_transform(self, bb: SVGBoundingBox) -> SVGBoundingBox:
        t = self._transform()
        return t.apply_bbox(bb) if t else bb

    def _prep_attrs(self, attrs:dict):
        tf = attrs.pop("transform", None)
        if tf is not None and not isinstance(tf, str):
            if not isinstance(tf, SVGTransform):
                tf = SVGTransform.from_commands(tf)
            tf = tf.to_str()
            attrs["transform"] = tf
        return attrs
    def to_svg(self) -> str:
        return self.wrapper(*self.body, **self._prep_attrs(self.styles | self.attrs))

    @abstractmethod
    def _raw_bbox(self) -> list[float]:
        """
        Return the axis-aligned bounding box in the parent coordinate system
        (i.e. after any transform has been applied).
        """

    def get_bbox(self) -> SVGBoundingBox:
        return self._apply_transform(SVGBoundingBox(*self._raw_bbox()))

    def __repr__(self) -> str:
        return f"{type(self).__name__}(bbox={self.get_bbox()})"


class SVGRect(SVGPrimitive):
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
        return [self.x, self.y, self.x + self.width, self.y + self.height]
class SVGCircle(SVGPrimitive):
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
class SVGEllipse(SVGPrimitive):
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
class SVGLine(SVGPrimitive):
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
class SVGPolyline(SVGPrimitive):
    wrapper = SVG.Polyline
    def __init__(self, points, **kwargs):
        points = np.asanyarray(points)
        super().__init__(points=points, **kwargs)

    @property
    def points(self): return self.get_attr("points")
    @points.setter
    def points(self, value): self.set_attr("points", value)

    def _raw_bbox(self):
        x = np.min(self.points[:, 0])
        y = np.min(self.points[:, 1])
        bb = SVGBoundingBox(x, y, np.max(self.points[:, 0]) - x, np.min(self.points[:, 1]) - y)
        return self._apply_transform(bb)
class SVGPolygon(SVGPrimitive):
    wrapper = SVG.Polygon
    def __init__(self, points, **kwargs):
        super().__init__(points=points, **kwargs)

    @property
    def points(self): return self.get_attr("points")
    @points.setter
    def points(self, value): self.set_attr("points", value)

    def _raw_bbox(self):
        x = np.min(self.points[:, 0])
        y = np.min(self.points[:, 1])
        return [x, y, np.max(self.points[:, 0]) - x, np.max(self.points[:, 1]) - y]

    def _prep_points(self, points):
        return " ".join(f"{a:.2f}" + " " + f"{b:.2f}" for a, b in points)
    def _prep_attrs(self, attrs:dict):
        attrs = super()._prep_attrs(attrs)
        attrs["points"] = self._prep_points(attrs["points"])
        return attrs

class SVGPath(SVGPrimitive):
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
            part = part.strip()
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

    def _prep_attrs(self, attrs:dict):
        attrs = super()._prep_attrs(attrs)
        attrs["d"] = self._prep_path(attrs["d"])
        return attrs

    def _prep_path(self, d):
        if not isinstance(d, str):
            bits = []
            for cmd, args in d:
                args = " ".join(
                    f"{a:.3g}" if a not in {True, False} else str(int(a))
                    for a in args
                )
                bits.append(f"{cmd} {args}")
            d = "\n".join(bits)
        return d

    def _raw_bbox(self):
        extrema = self._all_extrema()
        x = np.min(extrema[:, 0])
        y = np.min(extrema[:, 1])
        X = np.max(extrema[:, 0])
        Y = np.max(extrema[:, 1])
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

    @classmethod
    def from_mpl(cls,
                 path,
                 target_bbox: tuple[tuple[float, float], tuple[float, float]],
                 base_height=None,
                 y_flip: bool = True):
        from matplotlib.path import Path
        # Matplotlib path code → SVG command mapping
        _CMD_MAP = {
            Path.MOVETO: "M",
            Path.LINETO: "L",
            Path.CURVE3: "Q",  # quadratic Bézier
            Path.CURVE4: "C",  # cubic Bézier
            Path.CLOSEPOLY: "Z",
        }
        # Number of vertices consumed by each code (including the "current" vertex)
        _VERT_COUNT = {
            Path.MOVETO: 1,
            Path.LINETO: 1,
            Path.CURVE3: 2,  # 1 control + 1 end
            Path.CURVE4: 3,  # 2 controls + 1 end
            Path.CLOSEPOLY: 0,  # vertex is ignored
        }

        verts = np.asarray(path.vertices, dtype=float)
        bbox_init = (
            (np.min(verts[:, 0]), np.max(verts[:, 0])),
            (np.min(verts[:, 1]), np.max(verts[:, 1]))
        )
        dims_init = (
            bbox_init[0][1] - bbox_init[0][0],
            bbox_init[1][1] - bbox_init[1][0],
        )
        codes = path.codes if path.codes is not None else (
                [Path.MOVETO] + [Path.LINETO] * (len(verts) - 1)
        )

        if y_flip:
            h = dims_init[1] if base_height is None else base_height
            verts = verts.copy()
            verts[:, 1] = h - verts[:, 1]

        dims_target = (
            target_bbox[0][1] - target_bbox[0][0],
            target_bbox[1][1] - target_bbox[1][0],
        )
        scaling = max(np.array(dims_target) / np.array(dims_init))

        verts = (
                (verts - np.array([[bbox_init[0][0], bbox_init[1][0]]])) * scaling
                + np.array([[target_bbox[0][0], target_bbox[1][0]]])
        )

        parts = []
        i = 0
        while i < len(codes):
            code = codes[i]

            if code == Path.STOP:
                i += 1
                continue

            cmd = _CMD_MAP.get(code)
            if cmd is None:
                i += 1
                continue

            if code == Path.CLOSEPOLY:
                parts.append("Z")
                i += 1
                continue

            n = _VERT_COUNT[code]
            seg_verts = verts[i: i + n]
            parts.append(np.asarray(seg_verts))
            # coord_str = " ".join(f"{x:.6g},{y:.6g}" for x, y in seg_verts)
            parts.append([cmd, seg_verts])
            i += n

        return parts

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

class SVGText(SVGPrimitive):
    wrapper = SVG.Text
    def __init__(self, text, x, y, **kwargs):
        super().__init__(text, x=x, y=y,  **kwargs)

    @property
    def x(self): return self.get_attr("x")
    @x.setter
    def x(self, value): self.set_attr("x", value)
    @property
    def y(self): return self.get_attr("y")
    @y.setter
    def y(self, value): self.set_attr("y", value)
    @property
    def text(self): return self.body[0]
    @text.setter
    def text(self, value): self.body = (value,)

    def _raw_bbox(self):
        return [self.x, self.y, self.x, self.y]

class SVGFigure:
    Circle = SVGCircle
    Line = SVGLine
    Ellipse = SVGEllipse
    Rect = SVGRect
    Polygon = SVGPolygon
    Polyline = SVGPolyline
    Path = SVGPath
    # 'ellipse': SVGEllipse,
    # 'rect': SVGRect,
    # 'line': SVGLine,
    # 'polyline': SVGPolyline,
    # 'polygon': SVGPolygon,
    # 'path': SVGPath


    def __init__(self, elements=None, defs=None, view_box=None, preserve_aspect_ratio=None, **svg_kwargs):
        if elements is None: elements = []
        self.elements = elements
        if defs is None: defs = {}
        self.defs = defs
        self.view_box = view_box
        if preserve_aspect_ratio is not None:
            svg_kwargs['preserveAspectRatio'] = preserve_aspect_ratio
        self.kwargs = svg_kwargs

    element_mapping = {
        'circle': SVGCircle,
        'ellipse': SVGEllipse,
        'rect': SVGRect,
        'line': SVGLine,
        'polyline': SVGPolyline,
        'polygon': SVGPolygon,
        'path': SVGPath,
        'text': SVGText,
    }
    def create_element(self, element_type, **kwargs):
        return self.element_mapping[element_type](**kwargs)
    def add_element(self, element_type, **kwargs):
        elem = self.create_element(element_type, **kwargs)
        self.elements.append(elem)
        return elem
    def add_rect(self, **kwargs):
        return self.add_element('rect', **kwargs)
    def add_circle(self, **kwargs):
        return self.add_element('circle', **kwargs)
    def add_ellipse(self, **kwargs):
        return self.add_element('ellipse', **kwargs)
    def add_line(self, **kwargs):
        return self.add_element('line', **kwargs)
    def add_polyline(self, **kwargs):
        return self.add_element('polyline', **kwargs)
    def add_polygon(self, **kwargs):
        return self.add_element('polygon', **kwargs)
    def add_path(self, **kwargs):
        return self.add_element('path', **kwargs)
    def add_text(self, **kwargs):
        return self.add_element('text', **kwargs)

    def compute_viewbox(self):
        #TODO: add caching, invalidate when elements are added
        bbox = None
        for e in self.elements:
            if bbox is None:
                (l, r, b, t) = e.get_bbox().to_array()
                bbox = ((l, r), (b, t))
            else:
                bb = e.get_bbox()
                (left, right, bottom, top) = bb.to_array()
                ((l, r), (b, t)) = bbox
                bbox = (
                    (min([l, left]), max([r, right])),
                    (min([b, bottom]), max([t, top]))
                )
        return bbox

    def add_def(self, id, *, tag, **opts):
        self.defs[id] = dict(tag=tag) | opts
    def create_def(self, *, id, tag="marker", body=None, **opts):
        map = SVG.get_class_map()
        try:
            tag_class = map[tag]
        except KeyError:
            tag_class = lambda *es, **ats: SVG.base_element(tag, *es, **ats)
        if body is None:
            return tag_class(id=id, **opts)
        else:
            return tag_class(body, id=id, **opts)
    def prep_element(self, e):
        return e.to_svg(), e.get_bbox()
    def prep_draw_els(self, bbox, compute_bbox=None):
        els = []
        if compute_bbox is None:
            compute_bbox = bbox is None
        for e in self.elements:
            drel, bb = self.prep_element(e)
            els.append(drel)
            if bbox is None:
                (l, r, b, t) = bb.to_array()
                bbox = ((l, r), (b, t))
            elif compute_bbox:
                (left, right, bottom, top) = bb.to_array()
                ((l, r), (b, t)) = bbox
                bbox = (
                    (min([l, left]), max([r, right])),
                    (min([b, bottom]), max([t, top]))
                )
        return bbox, els
    def to_svg(self, compute_bbox=None, **opts):
        els = []
        if len(self.defs) > 0:
            def_el = []
            for k,v in self.defs.items():
                def_el.append(self.create_def(id=k, **v))
            els.append(SVG.Defs(def_el))

        bbox, draw_els = self.prep_draw_els(self.view_box, compute_bbox=compute_bbox)
        els.extend(draw_els)
        opts = self.kwargs | opts
        if bbox is not None:
            ((l, r), (b, t)) = bbox
            opts = dict(viewBox=(l, b, r - l, t - b)) | opts

        if 'aspect_ratio' in opts:
            if opts.get('height') is None:
                opts['width'] = opts.get('width', '100%')
                opts['height'] = 'auto'
                opts['preserveAspectRatio'] = "y"
            elif opts.get('width') is None:
                opts['height'] = opts.get('height', '100%')
                opts['width'] = 'auto'
                opts['preserveAspectRatio'] = "x"

        return SVG.Svg(
            *els,
            **opts
        )

class SVGPrimitive3D:
    wrapper: type[SVGPrimitive]
    @abstractmethod
    def prep_kwargs(self, projection_matrix) -> tuple[dict, tuple[float, float]]:
        ...
    def to_2d(self, projection_matrix):
        kwargs, depth = self.prep_kwargs(projection_matrix)
        return self.wrapper(**kwargs), depth
    def to_svg(self, projection_matrix):
        return self.to_2d(projection_matrix).to_svg()

class SVGPointsToShape3D(SVGPrimitive3D):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    @abstractmethod
    def to_points(self):
        ...
    @staticmethod
    def get_depth(points):
        return (np.min(points[:, 2]), np.max(points[:, 2]))
    def prep_kwargs(self, projection_matrix):
        points = self.to_points()
        pr = np.asanyarray(projection_matrix)
        if pr.shape[-1] == 3:
            points = points @ pr
        elif pr.shape[-1] == 2:
            zvals = points[:, (2,)]
            points = np.concatenate([points[:, :2] @ np.asanyarray(projection_matrix), zvals], axis=-1)
        else:
            points = np.pad(points, ([0, 0], [0, 1]), constant_values=1)
            points = (points @ np.asanyarray(projection_matrix))[:, :3]
        depth = self.get_depth(points)
        return self.kwargs | dict(
            points=points[:, :2]
        ), depth

class SVGPolygon3D(SVGPointsToShape3D):
    wrapper: SVGPolygon
    def __init__(self, points, **kwargs):
        self.points = points
        super().__init__(**kwargs)
    def to_points(self):
        return self.points

class SVGPolyline3D(SVGPointsToShape3D):
    wrapper: SVGPolyline
    def __init__(self, points, **kwargs):
        self.points = points
        super().__init__(**kwargs)
    def to_points(self):
        return self.points

class SVGFlatPointsToShape3D(SVGPointsToShape3D):
    def __init__(self, normal=None, rotation=None, **kwargs):
        self.normal = normal
        self.rotation = rotation
        super().__init__(**kwargs)
    @abstractmethod
    def to_2d_points(self) -> tuple[np.ndarray, np.ndarray]:
        ...
    def get_rotation_matrix(self):
        rotation, normal = self.rotation, self.normal
        if normal is None:
            normal = np.array([0, 0, 1])
        if rotation is not None:
            up_vector = nput.rotation_matrix(normal, rotation)[:, 0]
        else:
            up_vector = nput.vec_crosses([1, 0, 0], normal)
        return nput.view_matrix(
            up_vector,
            view_vector=normal,
            output_order=['x', 'y', 'z']
        )
    def to_points(self):
        two_d, center = self.to_2d_points()
        pad = np.concatenate([two_d, np.zeros((len(two_d), 1))], axis=-1)
        return pad @ self.get_rotation_matrix().T + center

class SVGPolylike3D(SVGFlatPointsToShape3D):
    def __init__(self, wrapper=None, **kwargs):
        self._wrapper = wrapper
        super().__init__(**kwargs)
    def _infer_wrapper(self) -> type[SVGPrimitive]:
        if 'fill' in self.kwargs:
            return SVGPolygon
        else:
            return SVGPolyline
    @property
    def wrapper(self):
        if self._wrapper is None:
            self._wrapper = self._infer_wrapper()
        return self._wrapper
    @wrapper.setter
    def wrapper(self, value):
        self._wrapper = value

class SVGRect3D(SVGPolylike3D):
    def __init__(self, x, y, z, width, height, **kwargs):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        super().__init__(**kwargs)
    def to_2d_points(self):
        return np.array([
            [0, 0],
            [self.width,0 ],
            [self.width, self.height],
            [0, self.height]
        ]), np.array([self.x, self.y, self.z])

class SVGCircle3D(SVGPolylike3D):
    def __init__(self, x, y, z, r, minor_radius=None, npoints=48, offset_angle=0, span_angle=2*np.pi, **kwargs):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.minor_radius = minor_radius
        self.offset_angle = offset_angle
        self.span_angle = span_angle
        self.npoints = npoints
        super().__init__(**kwargs)
    def to_2d_points(self):
        nput.arc_points([0, 0], self.r, minor_radius=self.minor_radius,
                        npoints=self.num_points,
                        offset_angle=self.offset_angle, span_angle=self.span_angle)
        return np.array([
            [self.x, self.y],
            [self.x + self.width, self.y],
            [self.x + self.width, self.y + self.height],
            [self.x, self.y + self.height]
        ]), np.array([self.x, self.y, self.z])


class SVGFigure3D(SVGFigure):

    def __init__(self, elements=None, defs=None,
                 view_matrix=None,
                 projection_matrix=None,
                 world_matrix=None,
                 view_position=None,
                 view_center=None,
                 up_vector=None,
                 view_vector=None,
                 right_vector=None,
                 view_angle=None,
                 aspect_ratio=None,
                 view_distance=None,
                 clip_distance=None,
                 **kwargs):
        self._projection_kwargs = dict(
            view_matrix=view_matrix,
            projection_matrix=projection_matrix,
            world_matrix=world_matrix,
            view_position=view_position,
            view_center=view_center,
            up_vector=up_vector,
            view_vector=view_vector,
            right_vector=right_vector,
            view_angle=view_angle,
            aspect_ratio=aspect_ratio,
            view_distance=view_distance,
            clip_distance=clip_distance
        )
        self._render_matrix = None
        super().__init__(elements=elements, defs=defs, **kwargs)
    def get_projection_matrix(self):
        if self._render_matrix is None:
            self._render_matrix = nput.render_matrix(**self._projection_kwargs)
        return self._render_matrix
    def get_projection_kwargs(self):
        return self._projection_kwargs
    def set_projection_kwargs(self, render_matrix=None, **kwargs):
        if render_matrix is not None or len(kwargs) > 0:
            self._render_matrix = render_matrix
            self._projection_kwargs.update(kwargs)

    element_mapping = {
        'circle': SVGCircle3D,
        # 'ellipse': SVGEllipse3D,
        'rect': SVGRect3D,
        # 'line': SVGLine3D,
        'polyline': SVGPolyline3D,
        'polygon': SVGPolygon3D,
        # 'path': SVGPath3D,
        # 'text': SVGText3D
    }
    def create_element(self, element_type, **kwargs):
        return self.element_mapping[element_type](**kwargs)

    def prep_element(self, e):
        if isinstance(e, SVGPrimitive3D):
            e, z = e.to_2d(projection_matrix=self.get_projection_matrix())
            e._depth = z[0]
        return super().prep_element(e)

    def sort_draw_els(self, els):
        return sorted(els,
                      key=lambda e: (e._depth if hasattr(e, '_depth') else -1000),
                      reverse=True)
    def prep_draw_els(self, bbox, compute_bbox=None):
        bbox, els = super().prep_draw_els(bbox, compute_bbox=compute_bbox)
        if bbox is not None:
            bbox = bbox[:2]
        return bbox, self.sort_draw_els(els)

    def compute_viewbox(self):
        bbox = None
        for e in self.elements:
            if isinstance(e, SVGPrimitive3D):
                e, z = e.to_2d(projection_matrix=self.get_projection_matrix())
            else:
                z = (0, 0)
            if bbox is None:
                (l, r, b, t) = e.get_bbox().to_array()
                bbox = ((l, r), (b, t), z)
            else:
                bb = e.get_bbox()
                (left, right, bottom, top) = bb.to_array()
                ((l, r), (b, t), (n, f)) = bbox
                bbox = (
                    (min([l, left]), max([r, right])),
                    (min([b, bottom]), max([t, top])),
                    (min([z[0], n]), max([z[1], f]))
                )
        return bbox