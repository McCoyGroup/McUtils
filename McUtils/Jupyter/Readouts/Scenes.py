"""
3D scene support for readouts: a uniform wrapper over mesh sources, a camera (`SceneView`)
shared by every backend, and pluggable poster rasterizers.

PowerPoint needs a PNG behind every embedded `.glb`, so the PowerPoint renderer always asks a
`ReadoutRasterizer` for one. The default (``'software'``) only needs numpy + matplotlib;
the browser-based ``'x3d'`` rasterizer (Playwright + Chromium) is opt-in and imports
Playwright only when it actually renders.
"""

from __future__ import annotations

import abc
import dataclasses
import importlib.util
import io
import math
import os
import struct
import warnings
import zlib

import numpy as np

__all__ = [
    "MeshSceneSource",
    "SceneView",
    "PosterRequest",
    "ReadoutRasterizer",
    "RasterizerChain",
    "PlaceholderRasterizer",
    "SoftwareRasterizer",
    "X3DRasterizer",
    "CallableRasterizer",
    "PrecomputedRasterizer",
]


def _unshare(mesh):
    from ...Plots.Mesh3DAnimation import Mesh3DAnimation
    return Mesh3DAnimation._unshare_for_x3d(mesh)


class MeshSceneSource:
    """Uniform access to a `Mesh3DAnimation` or a static mesh3D figure/graphics object."""

    def __init__(self, obj):
        self.obj = obj
        if hasattr(obj, "frames") and hasattr(obj, "to_gltf"):
            self.animation = obj
            self.figure = None
        else:
            fig = obj.figure if hasattr(obj, "figure") and hasattr(obj.figure, "iter_meshes") else obj
            if not hasattr(fig, "iter_meshes"):
                raise TypeError(f"{type(obj).__name__} is not a mesh3D figure or animation "
                                f"(plot with backend='mesh3D')")
            self.animation = None
            self.figure = fig

    @property
    def animated(self):
        return self.animation is not None

    @property
    def duration(self):
        return self.animation.duration if self.animated else None

    @property
    def frames(self):
        if self.animated:
            return self.animation.frames
        return [list(self.figure.iter_meshes())]

    @property
    def background(self):
        if self.animated:
            return getattr(self.animation, "background", None) or "white"
        return getattr(self.figure, "background", None) or "white"

    def vertices(self):
        verts = [m.vertices for frame in self.frames for m in frame if len(m.vertices)]
        return np.concatenate(verts) if verts else np.zeros((0, 3))

    def to_glb(self, skinned=True):
        buf = io.BytesIO()
        if self.animated:
            self.animation.savefig(buf, skinned=skinned)
        else:
            self.figure.savefig(buf, format="glb")
        return buf.getvalue()

    def to_x3d(self, view=None, width=None, height=None, background=None, animate=True, **x3d_opts):
        """An `X3D` scene using the same camera as the `.glb` and the poster."""
        from ...Plots.Backends import Mesh3DFigure
        background = background or self.background
        if self.animated and animate:
            anim = self.animation
            figs = []
            for frame in anim.frames:
                tmp = Mesh3DFigure(background=background)
                tmp.create_axes()
                tmp.axes[0].meshes = [_unshare(m) for m in frame]
                figs.append(tmp.to_x3d())
            base = figs[0].figure
            if view is not None:
                base.axes[0].opts["viewpoint"] = view.x3d_viewpoint()
            children = [f.figure.axes[0].children for f in figs]
            scene = base.animate_frames(children, mode="list" if anim.list_mode else None,
                                        animation_duration=anim.duration)
            if width is not None:
                scene.opts["width"] = width
            if height is not None:
                scene.opts["height"] = height
            return scene
        fig = Mesh3DFigure(background=background)
        fig.create_axes()
        fig.axes[0].meshes = [_unshare(m) for m in self.frames[0]]
        xfig = fig.to_x3d().figure
        if view is not None:
            xfig.axes[0].opts["viewpoint"] = view.x3d_viewpoint()
        if width is not None:
            x3d_opts["width"] = width
        if height is not None:
            x3d_opts["height"] = height
        return xfig.to_x3d(**x3d_opts)


def _axis_angle(R):
    angle = math.acos(max(-1.0, min(1.0, (np.trace(R) - 1) / 2)))
    if abs(angle) < 1e-9:
        return (0.0, 1.0, 0.0, 0.0)
    if abs(angle - math.pi) < 1e-6:
        # axis from the symmetric part
        M = (R + np.eye(3)) / 2
        axis = np.sqrt(np.clip(np.diag(M), 0, None))
        i = int(np.argmax(axis))
        for j in range(3):
            if j != i and M[i, j] < 0:
                axis[j] = -axis[j]
        axis = axis / np.linalg.norm(axis)
        return (*axis.tolist(), angle)
    axis = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]) / (2 * math.sin(angle))
    axis = axis / np.linalg.norm(axis)
    return (*axis.tolist(), angle)


class SceneView:
    """
    A perspective camera: looks along ``forward`` at ``center`` from ``distance`` away, with a
    *vertical* field of view ``fov`` (degrees). The same view drives the PowerPoint camera,
    the poster rasterizers and the HTML X3D viewpoint, so all three agree.
    """

    def __init__(self, center, forward, up, distance, fov=45.0):
        f = np.asarray(forward, dtype=float)
        f = f / np.linalg.norm(f)
        u = np.asarray(up, dtype=float)
        u = u - np.dot(u, f) * f
        u = u / np.linalg.norm(u)
        self.center = np.asarray(center, dtype=float)
        self.forward = f
        self.up = u
        self.right = np.cross(f, u)
        self.distance = float(distance)
        self.fov = float(fov)

    @classmethod
    def fit(cls, vertices, aspect=4 / 3, fov=45.0, padding=1.15, forward=None, up=None):
        """
        Fit a camera to ``vertices`` for a viewport of the given aspect (width/height).

        By default the camera looks along the axis in which the scene is thinnest (so planar
        molecules are seen face-on), with the longest remaining axis horizontal.
        """
        vertices = np.asarray(vertices, dtype=float).reshape(-1, 3)
        lo, hi = vertices.min(axis=0), vertices.max(axis=0)
        center = (lo + hi) / 2
        ext = hi - lo
        eye = np.eye(3)
        if forward is None:
            d = int(np.argmin(ext))
            forward = -eye[d]
        forward = np.asarray(forward, dtype=float)
        forward = forward / np.linalg.norm(forward)
        if up is None:
            # among axes orthogonal-ish to forward, put the longest one horizontal
            cands = [i for i in range(3) if abs(forward[i]) < .9]
            if len(cands) == 2:
                up = eye[min(cands, key=lambda i: ext[i])]
            else:
                up = eye[2] if abs(forward[2]) < .9 else eye[1]
        view = cls(center, forward, up, 1.0, fov)
        rel = vertices - center
        e_h = np.ptp(rel @ view.right) if len(rel) else 1
        e_v = np.ptp(rel @ view.up) if len(rel) else 1
        e_d = np.ptp(rel @ view.forward) if len(rel) else 0
        t = math.tan(math.radians(fov) / 2)
        view.distance = padding * max(e_h / (2 * t * aspect), e_v / (2 * t), 1e-6) + e_d / 2
        return view

    @property
    def camera_offset(self):
        """Camera position relative to ``center``."""
        return -self.forward * self.distance

    @property
    def camera_position(self):
        return self.center + self.camera_offset

    def x3d_viewpoint(self):
        R = np.column_stack([self.right, self.up, -self.forward])
        return {
            "orientation": _axis_angle(R),
            "view_position": {"untransformed": self.camera_position},
            "centerOfRotation": self.center.tolist(),
            "fieldOfView": math.radians(self.fov),
        }

    def project(self, points):
        """Normalized screen coordinates (x in [-aspect, aspect], y in [-1, 1]) and depths."""
        v = np.asarray(points, dtype=float) - self.camera_position
        depth = v @ self.forward
        t = math.tan(math.radians(self.fov) / 2)
        safe = np.where(depth > 1e-9, depth, 1e-9)
        return (v @ self.right) / (safe * t), (v @ self.up) / (safe * t), depth

    def get_meta(self):
        return {"center": self.center.tolist(), "forward": self.forward.tolist(), "up": self.up.tolist(),
                "distance": self.distance, "fov": self.fov}

    def __repr__(self):
        return f"{type(self).__name__}(center={self.center.round(3).tolist()}, " \
               f"forward={self.forward.round(3).tolist()}, distance={self.distance:.3f})"


@dataclasses.dataclass
class PosterRequest:
    source: MeshSceneSource
    view: SceneView
    width: int
    height: int
    background: str = "white"
    frame: int = 0
    scene_id: str | None = None
    path: str | None = None

    @property
    def meshes(self):
        return self.source.frames[self.frame]


def _png_bytes(rgb, width, height):
    """A solid-colour PNG, written without any imaging library."""
    raw = b"".join(b"\x00" + bytes(rgb) * width for _ in range(height))
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def _rgb(color):
    if isinstance(color, str):
        named = {"white": (255, 255, 255), "black": (0, 0, 0)}
        if color in named:
            return named[color]
        c = color.lstrip("#")
        if len(c) == 3:
            c = "".join(ch * 2 for ch in c)
        return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    color = np.asarray(color, dtype=float)
    if color.max() <= 1:
        color = color * 255
    return tuple(int(round(v)) for v in color[:3])


class ReadoutRasterizer(metaclass=abc.ABCMeta):
    """
    Turns a `PosterRequest` into PNG bytes.

    Resolve one with `ReadoutRasterizer.resolve(spec, options)` where ``spec`` is a name
    (``'software'``, ``'x3d'``, ``'placeholder'``, ``'auto'``), an instance, a callable
    ``request -> png bytes``, a dict of precomputed posters, or a tuple (a fallback chain).
    The default comes from `ReadoutRasterizer.default` or ``MCUTILS_READOUT_RASTERIZER``.
    """
    name = None
    registry = {}
    default = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.name is not None:
            ReadoutRasterizer.registry[cls.name] = cls

    def __init__(self, validate=False, min_coverage=0.005):
        self.validate = validate
        self.min_coverage = min_coverage

    @abc.abstractmethod
    def render(self, request: PosterRequest) -> bytes:
        ...

    def available(self):
        return True

    def check_poster(self, data, request):
        try:
            from PIL import Image
        except ImportError:
            return True
        with Image.open(io.BytesIO(data)) as im:
            pix = np.asarray(im.convert("RGB"), dtype=float)
        bg = np.array(_rgb(request.background), dtype=float)
        coverage = np.mean(np.any(np.abs(pix - bg) > 35, axis=-1))
        return coverage >= self.min_coverage

    def rasterize(self, request):
        data = self.render(request)
        if self.validate and not self.check_poster(data, request):
            raise ValueError(f"{type(self).__name__} produced a blank poster for {request.scene_id!r}")
        return data

    @classmethod
    def resolve(cls, spec=None, options=None):
        options = dict(options or {})
        if spec is None:
            spec = cls.default if cls.default is not None else os.environ.get("MCUTILS_READOUT_RASTERIZER", "software")
        if isinstance(spec, ReadoutRasterizer):
            return spec
        if isinstance(spec, (tuple, list)):
            return RasterizerChain([cls.resolve(s, options.get(s, options) if isinstance(s, str) else None)
                                    for s in spec])
        if isinstance(spec, dict):
            return PrecomputedRasterizer(spec, **options)
        if isinstance(spec, str):
            if spec == "auto":
                spec = "x3d" if importlib.util.find_spec("playwright") is not None else "software"
            if spec not in cls.registry:
                raise ValueError(f"unknown rasterizer {spec!r}; known: {sorted(cls.registry) + ['auto']}")
            opts = options.get(spec, options) if isinstance(options.get(spec), dict) else options
            opts = {k: v for k, v in opts.items() if k not in cls.registry}
            return cls.registry[spec](**opts)
        if callable(spec):
            return CallableRasterizer(spec, **options)
        raise TypeError(f"can't interpret {spec!r} as a rasterizer")


class RasterizerChain(ReadoutRasterizer):
    """Try each rasterizer in turn, warning and falling back when one fails."""

    def __init__(self, rasterizers):
        super().__init__()
        self.rasterizers = list(rasterizers)

    def render(self, request):
        errors = []
        for r in self.rasterizers:
            try:
                return r.rasterize(request)
            except Exception as e:
                errors.append(f"{type(r).__name__}: {e}")
                if r is not self.rasterizers[-1]:
                    warnings.warn(f"poster rasterizer {type(r).__name__} failed ({e}); falling back")
        raise RuntimeError("all poster rasterizers failed:\n  " + "\n  ".join(errors))


class PlaceholderRasterizer(ReadoutRasterizer):
    """A solid background-coloured PNG. No dependencies."""
    name = "placeholder"

    def __init__(self, color=None, **opts):
        super().__init__(**opts)
        self.color = color

    def render(self, request):
        return _png_bytes(_rgb(self.color or request.background), request.width, request.height)


class SoftwareRasterizer(ReadoutRasterizer):
    """
    Painter's-algorithm, flat-shaded render of the first frame's triangles with matplotlib's
    Agg backend (no display, browser or GPU needed). Lights are placed relative to the camera.
    """
    name = "software"

    def __init__(self, ambient=.38, diffuse=.62, specular=.18, shininess=24, dpi=100,
                 edge_width=.35, **opts):
        super().__init__(**opts)
        self.ambient, self.diffuse, self.specular, self.shininess = ambient, diffuse, specular, shininess
        self.dpi = dpi
        self.edge_width = edge_width

    def available(self):
        return importlib.util.find_spec("matplotlib") is not None

    def render(self, request):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from matplotlib.collections import PolyCollection

        view = request.view
        W, H = int(request.width), int(request.height)
        aspect = W / H
        fig = Figure(figsize=(W / self.dpi, H / self.dpi), dpi=self.dpi)
        FigureCanvasAgg(fig)
        bg = np.array(_rgb(request.background)) / 255
        fig.patch.set_facecolor(bg)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_axis_off()
        ax.set_xlim(-aspect, aspect)
        ax.set_ylim(-1, 1)
        ax.set_facecolor(bg)

        to_light = [(-view.forward + .55 * view.up - .45 * view.right, 1.0),
                    (-view.forward - .35 * view.up + .6 * view.right, .35)]
        to_light = [(l / np.linalg.norm(l), w) for l, w in to_light]
        polys, colors, depths = [], [], []
        for mesh in request.meshes:
            if mesh.mode != "triangles" or mesh.faces is None or not len(mesh.faces):
                continue
            tris = mesh.vertices[mesh.faces]                                   # (n, 3, 3)
            sx, sy, depth = view.project(tris.reshape(-1, 3))
            if np.any(depth <= 0):
                keep = np.all(depth.reshape(-1, 3) > 0, axis=1)
            else:
                keep = slice(None)
            n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
            n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
            to_cam = view.camera_position - tris.mean(axis=1)
            to_cam /= np.maximum(np.linalg.norm(to_cam, axis=1, keepdims=True), 1e-12)
            n = np.where((np.sum(n * to_cam, axis=1) < 0)[:, None], -n, n)     # two-sided
            shade = np.full(len(n), self.ambient)
            spec = np.zeros(len(n))
            for l, w in to_light:
                ndl = np.clip(n @ l, 0, None)
                shade += w * self.diffuse * ndl
                h = l + to_cam
                h /= np.maximum(np.linalg.norm(h, axis=1, keepdims=True), 1e-12)
                spec += w * self.specular * np.clip(np.sum(n * h, axis=1), 0, None) ** self.shininess
            if mesh.vertex_colors is not None:
                vc = np.asarray(mesh.vertex_colors, dtype=float)
                if vc.max() > 1:
                    vc = vc / 255
                base = vc[mesh.faces].mean(axis=1)
            else:
                mat = mesh.material or {}
                base = np.tile(np.asarray(mat.get("base_color", [.6, .6, .6, 1.]), dtype=float), (len(n), 1))
            if base.shape[1] == 3:
                base = np.concatenate([base, np.ones((len(base), 1))], axis=1)
            rgb = np.clip(base[:, :3] * shade[:, None] + spec[:, None], 0, 1)
            rgba = np.concatenate([rgb, base[:, 3:4]], axis=1)
            pts = np.stack([sx, sy], axis=-1).reshape(-1, 3, 2)
            polys.append(pts[keep])
            colors.append(rgba[keep])
            depths.append(depth.reshape(-1, 3).mean(axis=1)[keep])
        if polys:
            polys = np.concatenate(polys)
            colors = np.concatenate(colors)
            order = np.argsort(-np.concatenate(depths), kind="stable")
            pc = PolyCollection(polys[order], facecolors=colors[order], edgecolors=colors[order],
                                linewidths=self.edge_width, antialiased=True)
            ax.add_collection(pc)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=self.dpi, facecolor=bg)
        return buf.getvalue()


class X3DRasterizer(ReadoutRasterizer):
    """
    Screenshot the X3D/X3DOM view of the scene in headless Chromium (via `X3D.rasterize`).
    Requires Playwright and a Chromium build; Playwright is imported only inside `render`.
    All browser options are forwarded to `X3D.rasterize`.
    """
    name = "x3d"

    def __init__(self, executable_path=None, channel=None, browser_args=None, timeout=20_000,
                 ready_timeout_action="raise", device_scale_factor=1, x3dom_path="local", validate=True, **opts):
        super().__init__(validate=validate, **opts)
        self.executable_path = executable_path
        self.channel = channel
        self.browser_args = browser_args
        self.timeout = timeout
        self.ready_timeout_action = ready_timeout_action
        self.device_scale_factor = device_scale_factor
        self.x3dom_path = x3dom_path

    def available(self):
        return importlib.util.find_spec("playwright") is not None

    def render(self, request):
        scene = request.source.to_x3d(
            view=request.view, width=request.width, height=request.height,
            background=request.background, animate=False,
            x3dom_path=self.x3dom_path, x3dom_css_path="data:text/css,",
            include_export_button=False, include_record_button=False, include_view_settings_button=False,
        )
        buf = scene.rasterize(
            None, width=request.width, height=request.height, background=request.background,
            device_scale_factor=self.device_scale_factor, executable_path=self.executable_path,
            channel=self.channel, browser_args=self.browser_args, timeout=self.timeout,
            ready_timeout_action=self.ready_timeout_action,
        )
        return buf.getvalue()


class CallableRasterizer(ReadoutRasterizer):
    """Wrap a user function ``request -> PNG bytes`` (or a path to a PNG)."""

    def __init__(self, func, **opts):
        super().__init__(**opts)
        self.func = func

    def render(self, request):
        res = self.func(request)
        if isinstance(res, (str, os.PathLike)):
            with open(res, "rb") as f:
                return f.read()
        if hasattr(res, "getvalue"):
            return res.getvalue()
        return res


class PrecomputedRasterizer(ReadoutRasterizer):
    """Posters keyed by scene id or readout path; missing ones fall back to ``fallback``."""

    def __init__(self, posters, fallback="software", **opts):
        super().__init__(**opts)
        self.posters = dict(posters)
        self.fallback = None if fallback is None else ReadoutRasterizer.resolve(fallback)

    def render(self, request):
        for key in (request.path, request.scene_id):
            if key is not None and key in self.posters:
                p = self.posters[key]
                if isinstance(p, (str, os.PathLike)):
                    with open(p, "rb") as f:
                        return f.read()
                return p
        if self.fallback is None:
            raise KeyError(f"no precomputed poster for {request.path or request.scene_id!r}")
        return self.fallback.rasterize(request)
