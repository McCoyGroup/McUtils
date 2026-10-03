"""Declarative PresentationML and a mutable PowerPoint drawing interface.

Layout, appearance and playback wrappers accept ordinary Python values and
serialize them to OpenXML alongside the presentation primitives.
Coordinates default to points, with the origin at the top left. Export does not
render text, SVGs or models: externally generated raster fallbacks are accepted.
"""

import copy
import math
import mimetypes
import os
import posixpath
import operator
from dataclasses import dataclass

from ..Jupyter.OpenXML import OpenXML, OpenXMLPackage, OpenXMLPart

__all__ = [
    'PresentationML',
    'PresentationMLSlide',
    'PresentationMLPrimitive',
    'PresentationMLText',
    'PresentationMLImage',
    'PresentationMLModel3D',
    'PresentationMLShape',
    'PresentationMLAsset',
    'PresentationMLContext',
    'PresentationMLSlideContext',
    'PowerPointPresentation',
    'PowerPointSlide',
    'PresentationMLElementLayout',
    'PresentationMLAppearance',
    'PresentationMLMaterial',
    'PresentationMLSolidFill',
    'PresentationMLNoFill',
    'PresentationMLLine',
    'PresentationMLFont',
    'PresentationMLCamera',
    'PresentationMLModelTransform',
    'PresentationMLModel3DView',
    'PresentationMLAmbientLight',
    'PresentationMLPointLight',
    'PresentationMLAnimation',
]

P, A, M = OpenXML.Presentation, OpenXML.Drawing, OpenXML.Model3D
REL = OpenXML.namespace_uris["r"] + "/"
MODEL_REL = "http://schemas.microsoft.com/office/2017/06/relationships/model3d"
PRES_TYPE = "application/vnd.openxmlformats-officedocument.presentationml."
SLIDE_TYPE = PRES_TYPE + "slide+xml"
UNITS = {"pt": 12700, "in": 914400, "cm": 360000, "mm": 36000, "emu": 1}


def _emu(value, units="pt"):
    if units not in UNITS:
        raise ValueError("unknown dimension units: " + str(units))
    if not math.isfinite(value):
        raise ValueError("dimensions must be finite")
    return int(round(value * UNITS[units]))


class _Options:
    option_names = frozenset()

    def get_options(self):
        return _copy_options(self.opts)

    def snapshot(self):
        new = copy.copy(self)
        new.__dict__ = {key: _copy_options(value) for key, value in self.__dict__.items()}
        return new

    @classmethod
    def from_options(cls, options=None, **overrides):
        if isinstance(options, cls):
            options = options.get_options()
        elif options is None:
            options = {}
        else:
            options = dict(options)
        options.update(overrides)
        return cls(**options)


def _copy_options(value):
    if isinstance(value, OpenXML.Element):
        return value.clone()
    if isinstance(value, _Options):
        return value.snapshot()
    if isinstance(value, dict):
        return {key: _copy_options(v) for key, v in value.items()}
    if isinstance(value, tuple):
        return tuple(_copy_options(v) for v in value)
    if isinstance(value, list):
        return [_copy_options(v) for v in value]
    return copy.deepcopy(value)


class PresentationMLElementLayout(_Options):
    """Geometry and text/image layout; dimensions use points unless overridden.

    ``position`` is a top-left (x, y) pair; ``size`` is (width, height).
    ``bounds`` is accepted as shorthand for their concatenation. Padding uses
    CSS order (top, right, bottom, left), crop uses fractions of image dimensions,
    and rotations use degrees. The model view belongs here as well.
    """
    option_names = frozenset({
        "position", "width", "height", "size", "bounds", "units", "rotation",
        "flip_horizontal", "flip_vertical", "padding", "wrap", "alignment",
        "align", "vertical_alignment", "crop", "view",
    })
    alignments = {"left": "l", "center": "ctr", "right": "r", "justify": "just",
                  "l": "l", "ctr": "ctr", "r": "r", "just": "just"}
    vertical_alignments = {"top": "t", "center": "ctr", "bottom": "b"}

    def __init__(self, position=None, width=None, height=None, size=None, bounds=None,
                 units="pt", rotation=0, flip_horizontal=False, flip_vertical=False,
                 padding=0, wrap="square", alignment="left", align=None,
                 vertical_alignment="top", crop=None, view=None):
        if bounds is not None:
            if any(value is not None for value in (position, width, height, size)):
                raise ValueError("use bounds or position/size, not both")
            if len(bounds) != 4:
                raise ValueError("bounds must be (x, y, width, height)")
            position, width, height = tuple(bounds[:2]), bounds[2], bounds[3]
        if size is not None:
            if len(size) != 2 or width is not None or height is not None:
                raise ValueError("size must be (width, height), without separate width/height")
            width, height = size
        position = (0, 0) if position is None else tuple(position)
        if len(position) != 2:
            raise ValueError("position must be (x, y)")
        for value in position:
            _emu(value, units)
        for value in (width, height):
            if value is not None and _emu(value, units) <= 0:
                raise ValueError("width and height must be positive")
        if not math.isfinite(rotation):
            raise ValueError("rotation must be finite")
        if align is not None:
            alignment = align
        if alignment not in self.alignments or vertical_alignment not in self.vertical_alignments:
            raise ValueError("invalid text alignment")
        if wrap not in {"square", "none"}:
            raise ValueError("wrap must be square or none")
        self.opts = dict(position=position, width=width, height=height, units=units,
                         rotation=rotation, flip_horizontal=flip_horizontal,
                         flip_vertical=flip_vertical, padding=padding, wrap=wrap,
                         alignment=alignment, vertical_alignment=vertical_alignment,
                         crop=copy.deepcopy(crop), view=copy.deepcopy(view))

    @classmethod
    def from_options(cls, options=None, **overrides):
        options = {} if options is None else (options.get_options() if isinstance(options, cls) else dict(options))
        base = options.pop("layout", None)
        if base is not None:
            values = base.get_options() if isinstance(base, cls) else cls.from_options(base).get_options()
            values.update(options)
            options = values
        options.update(overrides)
        # A shorthand replaces dimensions inherited from another layout.
        if "bounds" in options:
            for key in ("position", "width", "height", "size"):
                options.pop(key, None)
        elif "size" in options:
            options.pop("width", None)
            options.pop("height", None)
        return cls(**options)

    @property
    def bounds(self):
        width, height = self.opts["width"], self.opts["height"]
        if width is None or height is None:
            raise ValueError("a positioned primitive requires width and height")
        return tuple(_emu(v, self.opts["units"]) for v in (*self.opts["position"], width, height))

    def to_presml(self, tag=None, local=False):
        x, y, width, height = self.bounds
        attrs = {}
        if self.opts["rotation"]:
            attrs["rot"] = round(self.opts["rotation"] * 60000)
        if self.opts["flip_horizontal"]:
            attrs["flipH"] = True
        if self.opts["flip_vertical"]:
            attrs["flipV"] = True
        if tag is P.Transform:
            attrs = {}  # PresentationML frame transforms only hold an offset/size.
        return (A.Transform2D if tag is None else tag)(
            A.Offset(x=0 if local else x, y=0 if local else y), A.Extents(cx=width, cy=height), **attrs)

    def to_paragraph_properties(self):
        return A.ParagraphProperties(algn=self.alignments[self.opts["alignment"]], lvl=0, marL=0, indent=0)

    def to_body_properties(self):
        padding = self.opts["padding"]
        if isinstance(padding, (int, float)):
            padding = (padding,) * 4
        elif len(padding) == 2:
            padding = (padding[0], padding[1], padding[0], padding[1])
        if len(padding) != 4 or any(value < 0 for value in padding):
            raise ValueError("padding must be nonnegative: scalar, pair or four sides")
        top, right, bottom, left = (_emu(v, self.opts["units"]) for v in padding)
        return A.BodyProperties(A.NoAutoFit(), wrap=self.opts["wrap"],
                                anchor=self.vertical_alignments[self.opts["vertical_alignment"]],
                                lIns=left, tIns=top, rIns=right, bIns=bottom)

    def to_crop(self):
        crop = self.opts["crop"]
        if crop is None:
            return None
        if not isinstance(crop, dict):
            if len(crop) != 4:
                raise ValueError("crop must be four sides or a dictionary")
            crop = dict(zip(("top", "right", "bottom", "left"), crop))
        names = {"left": "l", "top": "t", "right": "r", "bottom": "b"}
        if set(crop) - (set(names) | set(names.values())):
            raise ValueError("unknown crop side")
        for key, value in crop.items():
            if key in names and not 0 <= value < 1:
                raise ValueError("crop fractions must be in [0, 1)")
        return {names.get(k, k): round(v * 100000) if k in names else v for k, v in crop.items()}

    def prepare_view(self):
        return PresentationMLModel3DView.from_options(self.opts["view"])


def _color(value, opacity=1):
    if isinstance(value, str) and value.startswith("#") and len(value) == 4:
        value = "#" + "".join(character * 2 for character in value[1:])
    hexadecimal = isinstance(value, str) and len(value.lstrip("#")) == 6 \
        and all(c in "0123456789abcdefABCDEF" for c in value.lstrip("#"))
    if not hexadecimal:
        from .Colors import ColorPalette
        if isinstance(value, str):
            value = ColorPalette.parse_color_string(value)
        value = tuple(value)
        if len(value) != 3:
            raise ValueError("colors require three RGB components")
        scale = 255 if all(0 <= channel <= 1 for channel in value) else 1
        value = "".join(f"{round(channel * scale):02X}" for channel in value)
    value = value.lstrip("#")
    if len(value) != 6 or any(c not in "0123456789abcdefABCDEF" for c in value):
        raise ValueError("color must be a six-digit RGB value")
    if not 0 <= opacity <= 1:
        raise ValueError("opacity must be in [0, 1]")
    return A.RgbColorModelHex(*([] if opacity == 1 else [A.Alpha(val=round(opacity * 100000))]), val=value.upper())


class PresentationMLMaterial(_Options):
    """Base for fill subtypes; dictionaries and RGB strings select a solid fill."""
    @classmethod
    def from_options(cls, options=None, **overrides):
        if isinstance(options, PresentationMLMaterial):
            return options.snapshot()
        if isinstance(options, OpenXML.Element):
            return _XMLMaterial(options)
        if options is None:
            return PresentationMLNoFill()
        if isinstance(options, str):
            options = {"color": options}
        return PresentationMLSolidFill(**dict(options, **overrides))


class _XMLMaterial(PresentationMLMaterial):
    def __init__(self, element):
        self.element = element.clone()
    def to_presml(self):
        return self.element.clone()


class PresentationMLNoFill(PresentationMLMaterial):
    def __init__(self):
        self.opts = {}
    def to_presml(self):
        return A.NoFill()


class PresentationMLSolidFill(PresentationMLMaterial):
    def __init__(self, color="4472C4", opacity=1):
        _color(color, opacity)
        self.opts = dict(color=color, opacity=opacity)
    def to_presml(self):
        return A.SolidFill(_color(self.opts["color"], self.opts["opacity"]))


class PresentationMLLine(_Options):
    """Stroke width in points, with a material, dash and optional arrowheads."""
    def __init__(self, color="4472C4", width=1, material=None, opacity=1, dash="solid",
                 cap="flat", join=None, start_arrow=None, end_arrow=None, element=None):
        if not math.isfinite(width) or width <= 0:
            raise ValueError("line width must be positive")
        dash = {"dashed": "dash", "dotted": "sysDot"}.get(dash, dash)
        if cap not in {"flat", "rnd", "sq"} or join not in {None, "round", "bevel", "miter"}:
            raise ValueError("unsupported line cap or join")
        self.opts = dict(color=color, width=width, material=material, opacity=opacity, dash=dash,
                         cap=cap, join=join, start_arrow=start_arrow, end_arrow=end_arrow,
                         element=element)

    @classmethod
    def from_options(cls, options=None, **overrides):
        if isinstance(options, OpenXML.Element):
            return cls(element=options.clone())
        if isinstance(options, str):
            options = {"color": options}
        return super().from_options(options, **overrides)

    def to_presml(self):
        if self.opts["element"] is not None:
            return self.opts["element"].clone()
        fill = self.opts["material"]
        if fill is None:
            fill = dict(color=self.opts["color"], opacity=self.opts["opacity"])
        children = [PresentationMLMaterial.from_options(fill).to_presml(), A.PresetDash(val=self.opts["dash"])]
        if self.opts["join"] is not None:
            constructors = {"round": A.Round, "bevel": A.Bevel, "miter": A.Miter}
            children.append(constructors[self.opts["join"]]())
        for option, constructor in (("start_arrow", A.HeadEnd), ("end_arrow", A.TailEnd)):
            if self.opts[option] is not None:
                children.append(constructor(type=self.opts[option]))
        return A.Outline(*children, w=_emu(self.opts["width"]), cap=self.opts["cap"])


class PresentationMLFont(_Options):
    def __init__(self, family="Arial", size=18, color="000000", bold=False, italic=False):
        if not math.isfinite(size) or size <= 0:
            raise ValueError("font size must be positive")
        _color(color)
        self.opts = dict(family=family, size=size, color=color, bold=bold, italic=italic)

    def to_presml(self):
        return A.RunProperties(A.SolidFill(_color(self.opts["color"])), A.LatinFont(typeface=self.opts["family"]),
                               lang="en-US", sz=round(self.opts["size"] * 100),
                               b=self.opts["bold"], i=self.opts["italic"])


class PresentationMLAppearance(_Options):
    """Owns fills, strokes, typography, effects and 3D lighting."""
    option_names = frozenset({"material", "fill", "line", "font", "font_size", "font_family",
                              "bold", "italic", "color", "opacity", "effects", "lighting", "style"})
    def __init__(self, material=None, fill=None, line=None, font=None, font_size=None,
                 font_family=None, bold=None, italic=None, color=None, opacity=1,
                 effects=(), lighting=None, style=None):
        if material is not None and fill is not None:
            raise ValueError("use material or fill, not both")
        material = material if material is not None else fill
        if material is None and color is not None:
            material = dict(color=color, opacity=opacity)
        elif isinstance(material, str):
            material = dict(color=material, opacity=opacity)
        elif isinstance(material, dict):
            material = dict(material)
            material.setdefault("opacity", opacity)
        self.material = PresentationMLMaterial.from_options(material)
        self.line = None if line is None else PresentationMLLine.from_options(line)
        font_options = font.get_options() if isinstance(font, PresentationMLFont) else dict(font or {})
        for key, value in (("size", font_size), ("family", font_family), ("bold", bold), ("italic", italic), ("color", color)):
            if value is not None:
                font_options[key] = value
        self.font = PresentationMLFont.from_options(font_options)
        self.effects = tuple(e.clone() for e in effects)
        self.style = None if style is None else style.clone()
        self.lighting = None if lighting is None else tuple(self.prepare_light(light) for light in lighting)
        self.opts = dict(material=self.material, line=self.line, font=self.font,
                         effects=self.effects, lighting=self.lighting, style=self.style)

    def get_options(self):
        return _copy_options(dict(material=self.material, line=self.line, font=self.font,
                                  effects=self.effects, lighting=self.lighting, style=self.style))

    @classmethod
    def from_options(cls, options=None, **overrides):
        options = {} if options is None else (options.get_options() if isinstance(options, cls) else dict(options))
        appearance = options.pop("appearance", None)
        if appearance is not None:
            base = appearance.get_options() if isinstance(appearance, cls) else dict(appearance)
            base.update(options)
            options = base
        options.update(overrides)
        if "fill" in options and "material" in options:
            options.pop("material")
        return cls(**options)

    def to_presml(self):
        children = [self.material.to_presml()]
        if self.line is not None:
            children.append(self.line.to_presml())
        if self.effects:
            children.append(A.EffectList(*(e.clone() for e in self.effects)))
        return tuple(children)

    def to_model_properties(self):
        lights = self.lighting
        if lights is None:
            lights = (PresentationMLAmbientLight(), PresentationMLPointLight(position=(0.6, 2, 1.6)))
        return tuple(light.to_presml() if hasattr(light, "to_presml") else light.clone() for light in lights)

    @staticmethod
    def prepare_light(light):
        if isinstance(light, _Options):
            return light.snapshot()
        if isinstance(light, OpenXML.Element):
            return light.clone()
        light = dict(light)
        kind = light.pop("type", "point")
        if kind not in {"point", "ambient"}:
            raise ValueError("unsupported model light: " + kind)
        return (PresentationMLPointLight if kind == "point" else PresentationMLAmbientLight)(**light)


def _ratio(value):
    if not math.isfinite(value):
        raise ValueError("ratios must be finite")
    return dict(n=round(value * 1000000), d=1000000)


class PresentationMLCamera(_Options):
    """A camera described in centred model units, with an angle in degrees."""
    def __init__(self, position=(0, 0, 3), look_at=(0, 0, 0), up=(0, 1, 0),
                 field_of_view=45, projection="perspective", orthographic_size=1):
        if projection not in {"perspective", "orthographic"} or not 0 < field_of_view < 180:
            raise ValueError("invalid camera projection or field of view")
        if any(len(v) != 3 or not all(math.isfinite(x) for x in v) for v in (position, look_at, up)):
            raise ValueError("camera vectors must contain three finite values")
        if sum(x * x for x in up) == 0 or tuple(position) == tuple(look_at):
            raise ValueError("camera direction and up vector must be nonzero")
        if not math.isfinite(orthographic_size) or orthographic_size <= 0:
            raise ValueError("orthographic_size must be positive")
        self.opts = dict(position=tuple(position), look_at=tuple(look_at), up=tuple(up),
                         field_of_view=field_of_view, projection=projection, orthographic_size=orthographic_size)

    def to_presml(self, metres_per_unit=0.03):
        emus = 36000000 * metres_per_unit
        point = lambda v: dict(zip(("x", "y", "z"), (round(x * emus) for x in v)))
        up = dict(zip(("dx", "dy", "dz"), (round(x * 36000000) for x in self.opts["up"])))
        projection = M.Perspective(fov=round(self.opts["field_of_view"] * 60000)) \
            if self.opts["projection"] == "perspective" else M.Orthographic(M.Size(**_ratio(self.opts["orthographic_size"])))
        return M.Camera(M.Position(**point(self.opts["position"])), M.Up(**up),
                        M.LookAt(**point(self.opts["look_at"])), projection)


class PresentationMLModelTransform(_Options):
    def __init__(self, center=(0, 0, 0), metres_per_unit=0.03, scale=(1, 1, 1),
                 rotation=(0, 0, 0), translation=(0, 0, 0)):
        if not math.isfinite(metres_per_unit) or metres_per_unit <= 0:
            raise ValueError("metres_per_unit must be positive")
        for vector in (center, scale, rotation, translation):
            if len(vector) != 3 or not all(math.isfinite(v) for v in vector):
                raise ValueError("model transforms require three finite values")
        self.opts = dict(center=tuple(center), metres_per_unit=metres_per_unit, scale=tuple(scale),
                         rotation=tuple(rotation), translation=tuple(translation))

    def to_presml(self):
        emus = 36000000 * self.opts["metres_per_unit"]
        vector = lambda v: dict(zip(("dx", "dy", "dz"), (round(x * emus) for x in v)))
        return M.Transform(
            M.MeterPerModelUnit(**_ratio(self.opts["metres_per_unit"])),
            M.PreTranslate(**vector(tuple(-x for x in self.opts["center"]))),
            M.Scale(*(constructor(**_ratio(value)) for constructor, value in
                      zip((M.ScaleX, M.ScaleY, M.ScaleZ), self.opts["scale"]))),
            M.Rotate3D(**dict(zip(("ax", "ay", "az"), (round(v * 60000) for v in self.opts["rotation"])))),
            M.PostTranslate(**vector(self.opts["translation"])),
        )


class PresentationMLModel3DView(_Options):
    def __init__(self, camera=None, transform=None, viewport=None):
        self.camera = camera.clone() if isinstance(camera, OpenXML.Element) else PresentationMLCamera.from_options(camera)
        self.transform = transform.clone() if isinstance(transform, OpenXML.Element) else PresentationMLModelTransform.from_options(transform)
        self.opts = dict(camera=self.camera, transform=self.transform, viewport=viewport)

    def get_options(self):
        return _copy_options(dict(camera=self.camera, transform=self.transform, viewport=self.opts["viewport"]))

    @classmethod
    def from_presml(cls, model):
        camera, transform = model.find("camera"), model.find("trans")
        if camera is None or transform is None:
            raise ValueError("a model view requires camera and trans elements")
        viewport = model.find("objViewport")
        if viewport is None:
            viewport = model.find("winViewport")
        return cls(camera=camera, transform=transform, viewport=viewport)

    def to_presml(self, layout):
        viewport = self.opts["viewport"]
        if isinstance(viewport, OpenXML.Element):
            viewport = viewport.clone()
        else:
            viewport = layout.bounds[3] if viewport is None else _emu(viewport, layout.opts["units"])
            if viewport <= 0:
                raise ValueError("model viewport must be positive")
            viewport = M.ObjectViewport(viewportSz=viewport)
        transform = self.transform.clone() if isinstance(self.transform, OpenXML.Element) else self.transform.to_presml()
        if isinstance(self.camera, OpenXML.Element):
            camera = self.camera.clone()
        else:
            ratio = transform.find("meterPerModelUnit")
            metres = 1 if ratio is None else int(ratio.attrs["n"]) / int(ratio.attrs["d"])
            camera = self.camera.to_presml(metres)
        return camera, transform, viewport


class PresentationMLAmbientLight(_Options):
    def __init__(self, color=(0.5, 0.5, 0.5), illuminance=0.5):
        _validate_light(color, illuminance)
        self.opts = dict(color=tuple(color), illuminance=illuminance)
    def to_presml(self):
        return M.AmbientLight(M.Color(A.RgbColorModelPercentage(**dict(zip(("r", "g", "b"),
                             (round(v * 100000) for v in self.opts["color"]))))),
                             M.IlluminancePositiveRatio(**_ratio(self.opts["illuminance"])))


class PresentationMLPointLight(_Options):
    """Light position/radius in metres; RGB components in [0, 1]."""
    def __init__(self, position=(0.6, 2, 1.6), color=(1, 1, 1), intensity=10, radius=0):
        _validate_light(color, intensity)
        if len(position) != 3 or not all(math.isfinite(v) for v in position) or not math.isfinite(radius) or radius < 0:
            raise ValueError("light position must be finite and radius nonnegative")
        self.opts = dict(position=tuple(position), color=tuple(color), intensity=intensity, radius=radius)
    def to_presml(self):
        return M.PointLight(
            M.Color(A.RgbColorModelPercentage(**dict(zip(("r", "g", "b"),
                    (round(v * 100000) for v in self.opts["color"]))))),
            M.IntensityPositiveRatio(**_ratio(self.opts["intensity"])),
            M.Position(**dict(zip(("x", "y", "z"), (round(v * 36000000) for v in self.opts["position"])))),
            rad=round(self.opts["radius"] * 36000000),
        )


def _validate_light(color, strength):
    if len(color) != 3 or any(not math.isfinite(c) or not 0 <= c <= 1 for c in color):
        raise ValueError("light color requires three RGB values in [0, 1]")
    if not math.isfinite(strength) or strength < 0:
        raise ValueError("light strength must be nonnegative")


class PresentationMLAnimation(_Options):
    """Embedded GLB playback, with automatic slide timing for its allocated ID."""
    @classmethod
    def from_presml(cls, model):
        embedded = model.find("embedAnim")
        if embedded is None:
            return None
        properties = embedded.find("animPr")
        if properties is None:
            raise ValueError("embedded animation is missing playback properties")
        return cls(duration=int(properties.attrs["length"]) / 1000,
                   loop=properties.attrs.get("count") == "indefinite",
                   animation_id=int(embedded.attrs["animId"]))

    def __init__(self, duration=2, loop=True, autoplay=True, animation_id=0):
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("animation duration must be positive")
        if not isinstance(animation_id, int) or animation_id < 0:
            raise ValueError("animation_id must be a nonnegative integer")
        self.opts = dict(duration=duration, loop=loop, autoplay=autoplay, animation_id=animation_id)

    def to_presml(self):
        animation = OpenXML.Model3DAnimation
        return M.ExtensionList(
            A.Extension(animation.EmbeddedAnimation(
                animation.AnimationProperties(length=round(self.opts["duration"] * 1000),
                                              count="indefinite" if self.opts["loop"] else "1"),
                animId=self.opts["animation_id"]), uri="{9A65AA19-BECB-4387-8358-8AD5134E1D82}"),
            A.Extension(animation.PosterFrame(animId=self.opts["animation_id"]),
                        uri="{E9DE012E-A134-456F-84FE-255F9AAD75C6}"),
        )

    def to_timing(self, shape_id, first_id=3, sequence_id=2):
        # The sequence targets the model's actual export-time shape identifier.
        ids = iter(range(first_id, first_id + 4))
        outer, middle, effect, behavior = (next(ids) for _ in range(4))
        conditions = [P.Condition(delay="indefinite")]
        if self.opts["autoplay"]:
            conditions.append(P.Condition(P.TimeNode(val=sequence_id), evt="onBegin", delay=0))
        return P.ParallelTimeNode(P.CommonTimeNode(
            P.StartConditionList(*conditions), P.ChildTimeNodeList(
                P.ParallelTimeNode(P.CommonTimeNode(
                    P.StartConditionList(P.Condition(delay=0)), P.ChildTimeNodeList(
                        P.ParallelTimeNode(P.CommonTimeNode(
                            P.StartConditionList(P.Condition(delay=0)), P.ChildTimeNodeList(
                                P.Animate(P.CommonBehavior(
                                    P.CommonTimeNode(id=behavior, dur=round(self.opts["duration"] * 1000), fill="hold"),
                                    P.TargetElement(P.ShapeTarget(spid=shape_id)),
                                    P.AttributeNameList(P.AttributeName("embedded" + str(self.opts["animation_id"] + 1))),
                                ), P.TimeAnimateValueList(
                                    P.TimeAnimateValue(P.VariantValue(P.FloatVariantValue(val=0)), tm=0),
                                    P.TimeAnimateValue(P.VariantValue(P.FloatVariantValue(val=1)), tm=100000),
                                ), calcmode="lin", valueType="num"),
                            ), id=effect, presetID=100, presetClass="emph", presetSubtype=1,
                            repeatCount="indefinite" if self.opts["loop"] else "1000", fill="hold",
                            nodeType="withEffect" if self.opts["autoplay"] else "clickEffect")),
                    ), id=middle, fill="hold")),
            ), id=outer, fill="hold"))

    @staticmethod
    def slide_timing(animations):
        return P.Timing(P.TimeNodeList(P.ParallelTimeNode(P.CommonTimeNode(
            P.ChildTimeNodeList(P.SequenceTimeNode(
                P.CommonTimeNode(P.ChildTimeNodeList(*(animation.to_timing(shape_id, 3 + 4 * i)
                                                     for i, (shape_id, animation) in enumerate(animations))),
                                id=2, dur="indefinite", nodeType="mainSeq"),
                P.PreviousConditionList(P.Condition(P.TargetElement(P.SlideTarget()), evt="onPrev", delay=0)),
                P.NextConditionList(P.Condition(P.TargetElement(P.SlideTarget()), evt="onNext", delay=0)),
                concurrent=True, nextAc="seek")),
            id=1, dur="indefinite", restart="never", nodeType="tmRoot"))))


def _children(children):
    return tuple(children[0]) if len(children) == 1 and isinstance(children[0], (list, tuple)) else tuple(children)


def _group_tree():
    return P.ShapeTree(
        P.NonVisualGroupShapeProperties(P.NonVisualDrawingProperties(id=1, name=""),
                                       P.NonVisualGroupShapeDrawingProperties(), P.ApplicationNonVisualDrawingProperties()),
        P.GroupShapeProperties(A.Transform2D(A.Offset(x=0, y=0), A.Extents(cx=0, cy=0),
                                            A.ChildOffset(x=0, y=0), A.ChildExtents(cx=0, cy=0)))
    )


@dataclass(frozen=True)
class PresentationMLAsset:
    """An asset with an explicit media type and optional stable package name."""
    data: bytes
    content_type: str
    extension: str
    name: str = None

    def __post_init__(self):
        object.__setattr__(self, "data", bytes(self.data))
        object.__setattr__(self, "extension", self.extension.lower().lstrip("."))
        if not self.content_type or not self.extension or "/" in self.extension or "\\" in self.extension:
            raise ValueError("asset requires a content type and filename extension")

    @classmethod
    def from_file(cls, file, content_type=None, extension=None, name=None):
        if hasattr(file, "read"):
            data = file.read()
            filename = getattr(file, "name", "")
        else:
            filename = os.fspath(file)
            with open(filename, "rb") as stream:
                data = stream.read()
        extension = extension or posixpath.splitext(filename)[1].lstrip(".")
        content_type = content_type or {"glb": "model/gltf.binary", "svg": "image/svg+xml"}.get(extension)
        content_type = content_type or mimetypes.guess_type(filename)[0]
        if not extension or not content_type:
            raise ValueError("asset requires an extension and content type")
        return cls(bytes(data), content_type, extension.lower().lstrip("."), name)


def _asset(value, content_type=None, extension=None):
    if isinstance(value, PresentationMLAsset):
        return value
    if isinstance(value, (bytes, bytearray)):
        if not content_type or not extension:
            raise ValueError("byte assets require content_type and extension")
        return PresentationMLAsset(bytes(value), content_type, extension)
    return PresentationMLAsset.from_file(value, content_type, extension)


def _snapshot(value):
    if hasattr(value, "snapshot"):
        return value.snapshot()
    if isinstance(value, OpenXML.Element):
        return value.clone()
    if isinstance(value, OpenXMLPart):
        return value.clone()
    if isinstance(value, tuple):
        return tuple(_snapshot(v) for v in value)
    if isinstance(value, list):
        return [_snapshot(v) for v in value]
    if isinstance(value, dict):
        return {k: _snapshot(v) for k, v in value.items()}
    return value


class PresentationMLContext:
    """Per-export package context. Declarative objects never own export counters."""
    def __init__(self, presentation, package=None):
        self.presentation = presentation
        self.package = package if package is not None else presentation.scaffold.clone()

    def asset_part(self, asset):
        # Identical bytes can be shared across slides; relationship IDs cannot.
        if asset.name is not None:
            existing = self.package.parts.get(asset.name)
            if existing is not None:
                if existing.content_type != asset.content_type or existing.to_bytes() != asset.data:
                    raise ValueError("conflicting asset part: " + asset.name)
                return asset.name
        for part in self.package.parts.values():
            if part.content_type == asset.content_type and not isinstance(part.data, OpenXML.Element) \
                    and part.to_bytes() == asset.data:
                return part.name
        if asset.name is not None:
            name = asset.name
        else:
            prefix = "model3d" if asset.extension == "glb" else "image"
            i = 1
            while "ppt/media/" + prefix + str(i) + "." + asset.extension in self.package.parts:
                i += 1
            name = "ppt/media/" + prefix + str(i) + "." + asset.extension
        self.package.add_part(name, asset.content_type, asset.data)
        return name


class PresentationMLSlideContext:
    def __init__(self, context, slide, part_name=None):
        self.context, self.slide = context, slide
        self.part_name = part_name or slide.part_name
        self.used_ids = {1}
        self.reserved_ids = set()
        self.animations = []
        # Imported XML preserves shape IDs, including Choice/Fallback duplicates.
        for primitive in slide.children:
            if primitive.element is not None:
                ids = {int(e.attrs["id"]) for e in primitive.element.walk() if e.local_tag == "cNvPr"}
                if ids & self.used_ids:
                    raise ValueError("duplicate shape ID across primitives")
                self.used_ids.update(ids)
            elif primitive.id is not None:
                if primitive.id in self.reserved_ids:
                    raise ValueError("duplicate requested shape ID")
                self.reserved_ids.add(primitive.id)
        if self.used_ids & self.reserved_ids:
            raise ValueError("requested shape ID conflicts with an existing primitive")

    def shape_id(self, requested=None):
        if requested is not None:
            try:
                requested = operator.index(requested)
            except TypeError:
                raise ValueError("shape IDs must be integers") from None
            if requested in self.used_ids:
                raise ValueError("duplicate shape ID: " + str(requested))
            if not 2 <= requested <= 4294967295:
                raise ValueError("shape IDs must be in [2, 4294967295]")
            self.used_ids.add(requested)
            return requested
        i = 2
        while i in self.used_ids | self.reserved_ids:
            i += 1
        self.used_ids.add(i)
        return i

    def asset(self, asset, relationship_type=REL + "image"):
        name = self.context.asset_part(asset)
        return self.context.package.add_relationship(self.part_name, name, relationship_type)



class PresentationMLPrimitive:
    """Content with a layout and appearance, or an imported editable XML tree.

    Ordinary options are separated just as in the X3D adapter. XML construction
    belongs to ``to_presml``; geometry is owned by ``prepare_layout`` and styles
    by ``prepare_appearance``. Explicit XML is an optional extension mechanism.
    """
    Layout = PresentationMLElementLayout
    Appearance = PresentationMLAppearance

    def __init__(self, *children, element=None, tag=None, parts=(), relationships=(),
                 content_options=None, layout=None, appearance=None, position=None,
                 width=None, height=None, bounds=None, units=None, name=None, id=None, **options):
        layout_options = {k: options.pop(k) for k in tuple(options) if k in self.Layout.option_names}
        appearance_options = {k: options.pop(k) for k in tuple(options) if k in self.Appearance.option_names}
        for key, value in (("position", position), ("width", width), ("height", height),
                           ("bounds", bounds), ("units", units)):
            if value is not None:
                layout_options[key] = value
        self._appearance_requested = appearance is not None or bool(appearance_options)
        self.layout = self.Layout.from_options(dict(layout=layout, **layout_options))
        self.appearance = self.Appearance.from_options(dict(appearance=appearance, **appearance_options))
        self.name, self.id = name, id
        self.content_options = dict(content_options or {})
        if options and tag is None:
            raise TypeError("unknown primitive options: " + ", ".join(sorted(options)))
        self.content_options.update(options)
        if element is None and tag is not None:
            element = OpenXML.Element(tag, *_children(children), **self.content_options)
        elif element is None and children:
            if len(children) != 1 or not isinstance(children[0], OpenXML.Element):
                raise TypeError("provide a single OpenXML element or an explicit tag")
            element = children[0]
        self.element = None if element is None else element.clone()
        self.parts, self.relationships = tuple(parts), tuple(relationships)

    def get_layout_options(self):
        return self.layout.get_options() if isinstance(self.layout, self.Layout) else dict(self.layout)

    def prepare_layout(self):
        return self.Layout.from_options(self.get_layout_options())

    def get_appearance_options(self):
        return self.appearance.get_options() if isinstance(self.appearance, self.Appearance) else dict(self.appearance)

    def prepare_appearance(self):
        return self.Appearance.from_options(self.get_appearance_options())

    @property
    def bounds(self):
        return self.prepare_layout().bounds

    def _context(self, context):
        if context is None:
            raise ValueError("a slide export context is required for a generated primitive")
        self.prepare_layout().bounds
        return context.shape_id(self.id)

    def to_presml(self, context=None):
        if self.element is None:
            raise TypeError("the base primitive requires XML content; use a concrete primitive")
        if context is not None:
            for part in self.parts:
                existing = context.context.package.parts.get(part.name)
                if existing is not None and (existing.content_type != part.content_type
                                             or existing.to_bytes() != part.to_bytes()):
                    raise ValueError("conflicting primitive part: " + part.name)
                context.context.package.add_part(part.name, part.content_type, part.data)
            for relation in self.relationships:
                target = relation.target if relation.target_mode == "External" else \
                    context.context.package.resolve_target(context.part_name, relation.target)
                context.context.package.add_relationship(context.part_name, target, relation.type,
                                                         id=relation.id, external=relation.target_mode == "External")
        root = self.element.clone()
        properties = root.find("spPr")
        frame = root.find("graphicFrame")
        layout = self.prepare_layout()
        positioned = layout.opts["width"] is not None and layout.opts["height"] is not None
        if frame is not None and positioned:
            frame.elems = tuple(layout.to_presml(P.xfrm) if isinstance(e, OpenXML.Element)
                                and e.local_tag == "xfrm" else e for e in frame.elems)
        if properties is not None:
            if positioned:
                properties.elems = (layout.to_presml(local=frame is not None), *(e for e in properties.elems
                                                          if not isinstance(e, OpenXML.Element) or e.local_tag != "xfrm"))
            if self._appearance_requested:
                properties.elems = (*(e for e in properties.elems if not isinstance(e, OpenXML.Element)
                                      or e.local_tag not in {"solidFill", "noFill", "gradFill", "ln", "effectLst"}),
                                    *self.prepare_appearance().to_presml())
        return root

    def snapshot(self):
        new = copy.copy(self)
        new.__dict__ = {k: _snapshot(v) for k, v in self.__dict__.items()}
        return new

    @classmethod
    def from_presml(cls, element):
        if element.find("model3d") is not None:
            kind = PresentationMLModel3D
        elif element.local_tag == "pic":
            kind = PresentationMLImage
        elif element.local_tag == "sp" and element.find("txBody") is not None \
                and (element.find("t") is not None or element.find("ph") is not None
                     or element.find("cNvSpPr").attrs.get("txBox") == "1"):
            kind = PresentationMLText
        elif element.local_tag == "sp":
            kind = PresentationMLShape
        else:
            kind = cls
        return kind(element=element)


class PresentationMLText(PresentationMLPrimitive):
    def __init__(self, text="", bounds=None, paragraphs=None, body_properties=None, **options):
        # Text color is typography; a frame fill must be requested explicitly.
        appearance = options.get("appearance")
        if options.get("element") is None and appearance is None:
            options["appearance"] = dict(material=PresentationMLNoFill())
        elif options.get("element") is None and isinstance(appearance, dict) and not {"fill", "material"}.intersection(appearance):
            options["appearance"] = dict(appearance, material=PresentationMLNoFill())
        super().__init__(bounds=bounds, **options)
        self.text = text
        self.paragraphs = None if paragraphs is None else tuple(p.clone() for p in paragraphs)
        self.body_properties = None if body_properties is None else body_properties.clone()

    def to_presml(self, context=None):
        if self.element is not None:
            return super().to_presml(context)
        identifier = self._context(context)
        layout, appearance = self.prepare_layout(), self.prepare_appearance()
        paragraphs = self.paragraphs
        if paragraphs is None:
            paragraphs = tuple(OpenXML.Drawing.Paragraph(
                layout.to_paragraph_properties(),
                OpenXML.Drawing.Run(appearance.font.to_presml(), OpenXML.Drawing.Text(line)),
                OpenXML.Drawing.EndParagraphRunProperties(lang="en-US")
            ) for line in str(self.text).split("\n"))
        body = self.body_properties or layout.to_body_properties()
        return OpenXML.Presentation.Shape(
            P.nvSpPr(P.cNvPr(id=identifier, name=self.name or "TextBox " + str(identifier)),
                     P.cNvSpPr(txBox=True), P.nvPr()),
            P.spPr(layout.to_presml(), A.prstGeom(A.avLst(), prst="rect"),
                   *appearance.to_presml()),
            P.txBody(body.clone(), A.lstStyle(), *(p.clone() for p in paragraphs))
        )


def _picture(identifier, name, layout, appearance, rid, svg_rid=None):
    extensions = []
    if svg_rid is not None:
        extensions.append(A.extLst(A.ext(OpenXML.SVG.SVGBlip(r__embed=svg_rid),
                                        uri="{96DAC541-7B7A-43D3-8B79-37D633B846F1}")))
    fill = [A.blip(*extensions, r__embed=rid)]
    crop = layout.to_crop()
    if crop is not None:
        fill.append(A.srcRect(**crop))
    fill.append(A.stretch(A.fillRect()))
    return P.pic(
        P.nvPicPr(P.cNvPr(id=identifier, name=name), P.cNvPicPr(A.picLocks(noChangeAspect=True)), P.nvPr()),
        P.blipFill(*fill),
        P.spPr(layout.to_presml(), A.prstGeom(A.avLst(), prst="rect"), *appearance.to_presml())
    )


class PresentationMLImage(PresentationMLPrimitive):
    def __init__(self, image=None, bounds=None, fallback=None, content_type=None, extension=None, **options):
        super().__init__(bounds=bounds, **options)
        self.image = None if image is None else _asset(image, content_type, extension)
        self.fallback = None if fallback is None else _asset(fallback)

    def to_presml(self, context=None):
        if self.element is not None:
            return super().to_presml(context)
        identifier = self._context(context)
        if self.image is None or not self.image.content_type.startswith("image/"):
            raise ValueError("picture requires an image asset")
        rid, svg_rid = context.asset(self.image), None
        if self.image.extension == "svg":
            svg_rid, rid = rid, None
            if self.fallback is not None:
                if self.fallback.content_type != "image/png":
                    raise ValueError("SVG fallback must be PNG")
                rid = context.asset(self.fallback)
        return _picture(identifier, self.name or "Picture " + str(identifier),
                        self.prepare_layout(), self.prepare_appearance(), rid, svg_rid)


class PresentationMLShape(PresentationMLPrimitive):
    def __init__(self, geometry="rect", bounds=None, text_body=None, **options):
        if options.get("element") is None and "appearance" not in options and not self.Appearance.option_names.intersection(options):
            options["appearance"] = dict(fill="4472C4")
        super().__init__(bounds=bounds, **options)
        self.geometry = geometry.clone() if isinstance(geometry, OpenXML.Element) else geometry
        self.text_body = None if text_body is None else text_body.clone()

    def to_presml(self, context=None):
        if self.element is not None:
            return super().to_presml(context)
        identifier = self._context(context)
        geometry = self.geometry.clone() if isinstance(self.geometry, OpenXML.Element) else \
            A.prstGeom(A.avLst(), prst=self.geometry)
        appearance = self.prepare_appearance()
        return P.sp(
            P.nvSpPr(P.cNvPr(id=identifier, name=self.name or "Shape " + str(identifier)), P.cNvSpPr(), P.nvPr()),
            P.spPr(self.prepare_layout().to_presml(), geometry, *appearance.to_presml()),
            *([] if appearance.style is None else [appearance.style.clone()]),
            *([] if self.text_body is None else [self.text_body.clone()])
        )


class PresentationMLModel3D(PresentationMLPrimitive):
    """GLB content; view belongs to Layout, lighting to Appearance, playback to Animation."""
    def __init__(self, model=None, bounds=None, fallback=None, animation=None, **options):
        super().__init__(bounds=bounds, **options)
        self.model = None if model is None else _asset(model, "model/gltf.binary", "glb")
        self.fallback = None if fallback is None else _asset(fallback)
        self.animation = None if animation is None else PresentationMLAnimation.from_options(animation)

    def to_presml(self, context=None):
        if self.element is not None:
            return super().to_presml(context)
        identifier = self._context(context)
        if self.model is None or self.fallback is None:
            raise ValueError("native GLB export requires a model and PNG fallback")
        if self.model.extension != "glb" or self.fallback.content_type != "image/png":
            raise ValueError("native 3D assets must be GLB with a PNG fallback")
        if not self.model.data.startswith(b"glTF"):
            raise ValueError("model asset is not a binary glTF file")
        layout, appearance = self.prepare_layout(), self.prepare_appearance()
        camera, transform, viewport = layout.prepare_view().to_presml(layout)
        properties = [camera, transform]
        if self.animation is not None:
            properties.append(self.animation.to_presml())
        properties.extend((viewport, *appearance.to_model_properties()))
        tags = [p.local_tag for p in properties]
        if "camera" not in tags or "trans" not in tags:
            raise ValueError("native GLB export requires camera and trans properties")
        if "spPr" in tags or "raster" in tags:
            raise ValueError("model spPr and raster are supplied by the exporter")
        rid, raster = context.asset(self.model, MODEL_REL), context.asset(self.fallback)
        name = self.name or "3D Model " + str(identifier)
        properties.insert(tags.index("trans") + 1,
                          M.raster(M.blip(r__embed=raster), rName="Office3DRenderer", rVer="16.0.8326"))
        model = M.model3d(
            M.spPr(layout.to_presml(local=True), A.prstGeom(A.avLst(), prst="rect"), *appearance.to_presml()),
            *properties, r__embed=rid)
        frame = P.graphicFrame(
            P.nvGraphicFramePr(P.cNvPr(id=identifier, name=name),
                              P.cNvGraphicFramePr(A.graphicFrameLocks(noChangeAspect=True)), P.nvPr()),
            layout.to_presml(P.xfrm),
            A.graphic(A.graphicData(model, uri=OpenXML.namespace_uris["am3d"]))
        )
        if self.animation is not None:
            context.animations.append((identifier, self.animation))
        return OpenXML.Compatibility.AlternateContent(
            OpenXML.Compatibility.Choice(frame, Requires="am3d"),
            OpenXML.Compatibility.Fallback(_picture(identifier, name, layout, appearance, raster)))


class PresentationMLSlide:
    """Static slide data; the presentation binds its parent reference at construction."""
    def __init__(self, *children, presentation=None, structure=None, part_name=None,
                 layout=None, id=None, relationship_id=None, relationships=()):
        self.children = tuple(c.snapshot() if isinstance(c, PresentationMLPrimitive)
                              else PresentationMLPrimitive(c) for c in _children(children))
        self.presentation = presentation
        self.structure = None if structure is None else structure.clone()
        self.part_name, self.layout = part_name, layout
        self.id, self.relationship_id = id, relationship_id
        self.relationships = tuple(relationships)

    def __getitem__(self, item):
        return self.children[item]

    def __len__(self):
        return len(self.children)

    def to_presml(self, context=None):
        if context is None:
            if self.presentation is None:
                if any(c.element is None for c in self.children):
                    raise ValueError("generated slides require a presentation context")
            else:
                global_context = PresentationMLContext(self.presentation)
                part = self.part_name or "ppt/slides/slide1.xml"
                context = PresentationMLSlideContext(global_context, self, part)
        if context is not None:
            for relation in self.relationships:
                external = relation.target_mode == "External"
                target = relation.target if external else context.context.package.resolve_target(
                    context.part_name, relation.target)
                context.context.package.add_relationship(context.part_name, target, relation.type,
                                                         id=relation.id, external=external)
        root = self.structure.clone() if self.structure is not None else \
            P.sld(P.cSld(_group_tree()), P.clrMapOvr(A.masterClrMapping()))
        tree = root.find("spTree")
        if tree is None:
            raise ValueError("slide is missing its shape tree")
        tree.elems = [e for e in tree.elems if isinstance(e, OpenXML.Element)
                       and e.local_tag in {"nvGrpSpPr", "grpSpPr"}]
        tree.elems = (*tree.elems, *(c.to_presml(context) for c in self.children))
        if context is not None and context.animations:
            timing = root.find("timing")
            if timing is None:
                root.append(PresentationMLAnimation.slide_timing(context.animations))
            else:
                sequence = next((e for e in timing.walk() if e.local_tag == "cTn"
                                 and e.attrs.get("nodeType") == "mainSeq"), None)
                if sequence is None or sequence.find("childTnLst") is None:
                    raise ValueError("imported slide timing has no main sequence to extend")
                first_id = 1 + max(int(e.attrs["id"]) for e in timing.walk()
                                   if e.local_tag == "cTn" and "id" in e.attrs)
                for i, (shape_id, animation) in enumerate(context.animations):
                    sequence.find("childTnLst").append(animation.to_timing(shape_id, first_id + 4 * i,
                                                                          sequence.attrs["id"]))
        return root


def _default_package():
    package = OpenXMLPackage()
    colors = {"dk1": "000000", "lt1": "FFFFFF", "dk2": "44546A", "lt2": "E7E6E6",
              "accent1": "4472C4", "accent2": "ED7D31", "accent3": "A5A5A5",
              "accent4": "FFC000", "accent5": "5B9BD5", "accent6": "70AD47",
              "hlink": "0563C1", "folHlink": "954F72"}
    fill = lambda: A.solidFill(A.schemeClr(val="phClr"))
    font = lambda tag: tag(A.latin(typeface="Arial"), A.ea(typeface=""), A.cs(typeface=""))
    theme = A.theme(A.themeElements(
        A.clrScheme(*(getattr(A, k)(A.srgbClr(val=v)) for k, v in colors.items()), name="McUtils"),
        A.fontScheme(font(A.majorFont), font(A.minorFont), name="McUtils"),
        A.fmtScheme(A.fillStyleLst(*(fill() for _ in range(3))),
                    A.lnStyleLst(*(A.ln(fill(), A.prstDash(val="solid"), A.miter(lim=800000),
                                        w=w, cap="flat", cmpd="sng", algn="ctr")
                                   for w in (9525, 25400, 38100))),
                    A.effectStyleLst(*(A.effectStyle(A.effectLst()) for _ in range(3))),
                    A.bgFillStyleLst(*(fill() for _ in range(3))), name="McUtils")
    ), name="McUtils")
    layout_name = "ppt/slideLayouts/slideLayout1.xml"
    master_name = "ppt/slideMasters/slideMaster1.xml"
    package.add_part("ppt/theme/theme1.xml", "application/vnd.openxmlformats-officedocument.theme+xml", theme)
    layout = P.sldLayout(P.cSld(_group_tree(), name="Blank"),
                         P.clrMapOvr(A.masterClrMapping()), type="blank", preserve=True)
    package.add_part(layout_name, PRES_TYPE + "slideLayout+xml", layout)
    package.add_relationship(layout_name, master_name, REL + "slideMaster")
    lrid = package.add_relationship(master_name, layout_name, REL + "slideLayout")
    package.add_relationship(master_name, "ppt/theme/theme1.xml", REL + "theme")
    mapping = {k: k for k in ("accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink")}
    mapping.update(bg1="lt1", tx1="dk1", bg2="lt2", tx2="dk2")
    master = P.sldMaster(P.cSld(_group_tree()), P.clrMap(**mapping),
                         P.sldLayoutIdLst(P.sldLayoutId(id=2147483649, r__id=lrid)),
                         P.txStyles(P.titleStyle(), P.bodyStyle(), P.otherStyle()))
    package.add_part(master_name, PRES_TYPE + "slideMaster+xml", master)
    return package, layout_name, master_name


class PresentationML:
    """A complete declarative presentation. There is intentionally no add_slide."""
    Layout = PresentationMLElementLayout
    Appearance = PresentationMLAppearance
    Material = PresentationMLMaterial
    SolidFill = PresentationMLSolidFill
    NoFill = PresentationMLNoFill
    Line = PresentationMLLine
    Font = PresentationMLFont
    Camera = PresentationMLCamera
    ModelTransform = PresentationMLModelTransform
    Model3DView = PresentationMLModel3DView
    AmbientLight = PresentationMLAmbientLight
    PointLight = PresentationMLPointLight
    Animation = PresentationMLAnimation
    def __init__(self, *slides, size=None, units="pt", scaffold=None, structure=None,
                 part_name="ppt/presentation.xml", default_layout=None):
        if scaffold is None:
            scaffold, default_layout, master = _default_package()
            mrid = scaffold.add_relationship(part_name, master, REL + "slideMaster")
            structure = P.presentation(P.sldMasterIdLst(P.sldMasterId(id=2147483648, r__id=mrid)),
                                        P.sldIdLst(), P.sldSz(cx=12192000, cy=6858000),
                                        P.notesSz(cx=6858000, cy=9144000))
        self.scaffold = scaffold.clone()
        self.structure = structure.clone() if structure is not None else P.presentation(P.sldIdLst())
        if size is None:
            existing = self.structure.find("sldSz")
            size = (960, 540) if existing is None else \
                (int(existing.attrs["cx"]) / UNITS[units], int(existing.attrs["cy"]) / UNITS[units])
        self.size = tuple(_emu(v, units) for v in size)
        if len(self.size) != 2 or min(self.size) <= 0:
            raise ValueError("presentation size must be two positive dimensions")
        self.part_name, self.default_layout = part_name, default_layout
        bound = []
        for slide in _children(slides):
            if not isinstance(slide, PresentationMLSlide):
                raise TypeError("presentation children must be PresentationMLSlide objects")
            slide = copy.copy(slide)
            slide.children = tuple(c.snapshot() for c in slide.children)
            slide.structure = None if slide.structure is None else slide.structure.clone()
            slide.presentation = self
            bound.append(slide)
        self.slides = tuple(bound)

    @property
    def children(self):
        return self.slides

    def __getitem__(self, item):
        return self.slides[item]

    def __len__(self):
        return len(self.slides)

    @classmethod
    def from_package(cls, package):
        main = next(r for r in package.relationships() if r.type == REL + "officeDocument")
        part_name = package.resolve_target("", main.target)
        structure = package[part_name].data
        relations = {r.id: r for r in package.relationships(part_name)}
        slides = []
        for node in structure.find("sldIdLst").elems:
            if not isinstance(node, OpenXML.Element):
                continue
            rid = node.attrs.get("r:id")
            if rid is None:
                # Parsed documents can use a different lexical prefix.
                rid = next(v for k, v in node.attrs.items() if k.endswith(":id"))
            name = package.resolve_target(part_name, relations[rid].target)
            root = package[name].data
            rels = package.relationships(name)
            layout = next((package.resolve_target(name, r.target) for r in rels
                           if r.type == REL + "slideLayout"), None)
            primitives = [PresentationMLPrimitive.from_presml(e) for e in root.find("spTree").elems
                          if isinstance(e, OpenXML.Element) and e.local_tag not in {"nvGrpSpPr", "grpSpPr"}]
            slides.append(PresentationMLSlide(*primitives, structure=root, part_name=name,
                                               id=int(node.attrs["id"]), relationship_id=rid,
                                               layout=layout, relationships=rels))
        blank = next((p.name for p in package.parts.values()
                      if p.content_type == PRES_TYPE + "slideLayout+xml"
                      and p.data.attrs.get("type") == "blank"), None)
        return cls(*slides, scaffold=package, structure=structure,
                   part_name=part_name, default_layout=blank)

    @classmethod
    def from_file(cls, file):
        return cls.from_package(OpenXMLPackage.from_file(file))

    def to_presml(self, context=None):
        context = context or PresentationMLContext(self)
        root = self.structure.clone()
        size = root.find("sldSz")
        if size is None:
            root.append(P.sldSz(cx=self.size[0], cy=self.size[1]))
        else:
            size.attrs = dict(size.attrs, cx=str(self.size[0]), cy=str(self.size[1]))
        ids = root.find("sldIdLst")
        if ids is None:
            ids = P.sldIdLst()
            root.insert(1 if root.find("sldMasterIdLst") is not None else 0, ids)
        # Preserve unmodified sldId nodes, including extension attributes.
        old_ids = {e.attrs["id"]: e for e in ids.elems if isinstance(e, OpenXML.Element)}
        ids.elems = []
        used_parts, used_ids = set(), set()
        reserved_parts = {s.part_name for s in self.slides if s.part_name is not None}
        reserved_ids = {s.id for s in self.slides if s.id is not None}
        for slide in self.slides:
            name = slide.part_name
            if name is None:
                i = 1
                while "ppt/slides/slide" + str(i) + ".xml" in used_parts | reserved_parts:
                    i += 1
                name = "ppt/slides/slide" + str(i) + ".xml"
            if name in used_parts:
                raise ValueError("duplicate slide part: " + name)
            used_parts.add(name)
            id = slide.id
            if id is None:
                id = 256
                while id in used_ids | reserved_ids:
                    id += 1
            try:
                id = operator.index(id)
            except TypeError:
                raise ValueError("slide IDs must be integers") from None
            if id in used_ids or not 256 <= id < 2147483648:
                raise ValueError("duplicate or invalid slide ID: " + str(id))
            used_ids.add(id)
            layout = slide.layout or self.default_layout
            if layout is None:
                raise ValueError("slide requires a layout")
            context.package.add_relationship(name, layout, REL + "slideLayout")
            local_context = PresentationMLSlideContext(context, slide, name)
            context.package.add_part(name, SLIDE_TYPE, slide.to_presml(local_context))
            rid = context.package.add_relationship(self.part_name, name, REL + "slide", id=slide.relationship_id)
            old = old_ids.get(str(id))
            if old is not None and old.attrs.get("r:id") == rid:
                ids.append(old.clone())
            else:
                ids.append(P.sldId(id=id, r__id=rid))
        context.package.add_part(self.part_name, PRES_TYPE + "presentation.main+xml", root)
        context.package.add_relationship("", self.part_name, REL + "officeDocument")
        return root

    def to_package(self):
        context = PresentationMLContext(self)
        self.to_presml(context)
        return context.package

    def write(self, file, validate=True):
        return self.to_package().write(file, validate=validate)

    def to_bytes(self, validate=True):
        return self.to_package().to_bytes(validate=validate)


class PowerPointSlide:
    """Mutable child drawing surface. Each slide owns its primitive data."""
    def __init__(self, presentation, *children, **opts):
        self.presentation = presentation
        self.children = list(_children(children))
        self.opts = dict(opts)

    def __getitem__(self, item):
        return self.children[item]

    def __len__(self):
        return len(self.children)

    def draw_primitive(self, primitive):
        if isinstance(primitive, OpenXML.Element):
            primitive = PresentationMLPrimitive(primitive)
        if not isinstance(primitive, PresentationMLPrimitive):
            raise TypeError("expected a PresentationML primitive")
        self.children.append(primitive)
        return primitive

    def _drawing_options(self, opts):
        layout = opts.get("layout")
        layout_units = (layout.opts.get("units") if isinstance(layout, PresentationMLElementLayout)
                        else (layout or {}).get("units"))
        if layout_units is None:
            opts.setdefault("units", self.presentation.units)
        return opts

    def draw_text(self, text, bounds=None, **opts):
        self._drawing_options(opts)
        return self.draw_primitive(PresentationMLText(text, bounds, **opts))

    def draw_image(self, image, bounds=None, **opts):
        self._drawing_options(opts)
        return self.draw_primitive(PresentationMLImage(image, bounds, **opts))

    def draw_model3d(self, model, bounds=None, **opts):
        self._drawing_options(opts)
        return self.draw_primitive(PresentationMLModel3D(model, bounds, **opts))

    draw_glb = draw_model3d

    def draw_shape(self, geometry, bounds=None, **opts):
        self._drawing_options(opts)
        return self.draw_primitive(PresentationMLShape(geometry, bounds, **opts))

    def to_presentationml(self, presentation=None):
        return PresentationMLSlide(*self.children, presentation=presentation, **self.opts)

    def to_presml(self, context=None):
        if context is not None:
            return self.to_presentationml().to_presml(context)
        presentation = self.presentation.to_presentationml()
        index = next(i for i, slide in enumerate(self.presentation.slides) if slide is self)
        return presentation[index].to_presml()


class PowerPointPresentation:
    """Mutable builder; serialize by taking a declarative PresentationML snapshot."""
    Slide = PowerPointSlide

    def __init__(self, *slides, size=(960, 540), units="pt", template=None):
        self.size, self.units = size, units
        self.template = template
        self.slides = []
        for slide in _children(slides):
            if isinstance(slide, PresentationMLSlide):
                self.add_slide(*slide.children, structure=slide.structure,
                               part_name=slide.part_name, layout=slide.layout,
                               id=slide.id, relationship_id=slide.relationship_id,
                               relationships=slide.relationships)
            else:
                raise TypeError("initial slides must be PresentationMLSlide objects")

    def __getitem__(self, item):
        return self.slides[item]

    def __len__(self):
        return len(self.slides)

    def add_slide(self, *children, **opts):
        slide = self.Slide(self, *children, **opts)
        self.slides.append(slide)
        return slide

    @classmethod
    def from_file(cls, file):
        presentation = PresentationML.from_file(file)
        return cls(*presentation.slides, size=tuple(v / UNITS["pt"] for v in presentation.size),
                   units="pt", template=presentation)

    def to_presentationml(self):
        opts = dict(size=self.size, units=self.units)
        if self.template is not None:
            opts.update(scaffold=self.template.scaffold, structure=self.template.structure,
                        part_name=self.template.part_name, default_layout=self.template.default_layout)
        return PresentationML(*(s.to_presentationml() for s in self.slides), **opts)

    def to_presml(self, context=None):
        return self.to_presentationml().to_presml(context)

    def to_package(self):
        return self.to_presentationml().to_package()

    def write(self, file, validate=True):
        return self.to_presentationml().write(file, validate=validate)

    def to_bytes(self, validate=True):
        return self.to_presentationml().to_bytes(validate=validate)
