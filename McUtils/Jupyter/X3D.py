from .JHTML import HTML
from .. import Devutils as dev

__all__ = [
    "X3DHTML",
    "X3DControls"
]

__reload_hooks__ = [".JHTML"]
class X3DHTML:
    _x3d_map = None
    @classmethod
    def get_x3d_map(cls):
        if cls._x3d_map is None:
            cls._x3d_map = {}
            for v in cls.__dict__.values():
                if isinstance(v, type) and hasattr(v, 'tag'):
                    cls._x3d_map[v.tag] = v
        return cls._x3d_map

    class X3DElement(HTML.TagElement):
        ignored_styles = {"height", "width", "position", "color", "direction", "top", "bottom", "left", "right"}
        can_be_dynamic = False
        style_props = None

        @classmethod
        def get_class_map_updates(cls):
            return X3DHTML.get_x3d_map()

        @classmethod
        def convert_attr_value(cls, v):
            if isinstance(v, str):
                pass
            elif v is True or v is False:
                v = str(v).lower()
            elif dev.is_number(v):
                if abs(v - int(v)) > 1e-4:
                    v = f"{v:.3f}"
                else:
                    v = f"{v:.0f}"
            elif hasattr(v, "tolist"):
                v = cls.convert_attr_value(v.tolist())
            elif hasattr(v, "__getitem__") or hasattr(v, "__iter__"):
                v = " ".join(cls.convert_attr_value(x) for x in v)
            else:
                v = str(v)
            return v
        @classmethod
        def convert_attrs(cls, attrs:dict):
            copied = False
            for k,v in attrs.items():
                if isinstance(v, str):
                    continue
                if not copied:
                    copied = True
                    attrs = attrs.copy()
                if v is None:
                    del attrs[k]
                else:
                    attrs[k] = cls.convert_attr_value(v)
            return attrs

        attr_converter = convert_attrs
        # class_map = {"cls":"class_", "id":"id_", "style":"style_"}
        # def to_x3d(self):
        #     tag = x3d.method(self.tag)
        #     opts = {
        #         self.class_map.get(k, k): v.to_x3d() if isinstance(v, X3D.X3DElement) else v
        #         for k, v in self.attrs.items()
        #     }
        #     children = []
        #     for e in self.elems:
        #         e = e.to_x3d() if isinstance(e, X3D.X3DElement) else e
        #         if e.tag in {"head", "Scene"}:
        #             opts[e.tag] = e
        #         else:
        #             children.append(e)
        #
        #     return tag(children=children, **opts)

    class X3DCanvas(HTML.TagElement): tag = "x3d-canvas"
    class X3D(X3DElement): tag = "X3D"
    class Anchor(X3DElement): tag = "Anchor"
    class Appearance(X3DElement): tag = "Appearance"
    class Arc2D(X3DElement): tag = "Arc2D"
    class ArcClose2D(X3DElement): tag = "ArcClose2D"
    class AudioClip(X3DElement): tag = "AudioClip"
    class Background(X3DElement): tag = "Background"
    class BallJoint(X3DElement): tag = "BallJoint"
    class Billboard(X3DElement): tag = "Billboard"
    class BinaryGeometry(X3DElement): tag = "BinaryGeometry"
    class BlendMode(X3DElement): tag = "BlendMode"
    class BlendedVolumeStyle(X3DElement): tag = "BlendedVolumeStyle"
    class Block(X3DElement): tag = "Block"
    class BoundaryEnhancementVolumeStyle(X3DElement): tag = "BoundaryEnhancementVolumeStyle"
    class Box(X3DElement): tag = "Box"
    class BufferAccessor(X3DElement): tag = "BufferAccessor"
    class BufferGeometry(X3DElement): tag = "BufferGeometry"
    class BufferView(X3DElement): tag = "BufferView"
    class CADAssembly(X3DElement): tag = "CADAssembly"
    class CADFace(X3DElement): tag = "CADFace"
    class CADLayer(X3DElement): tag = "CADLayer"
    class CADPart(X3DElement): tag = "CADPart"
    class CartoonVolumeStyle(X3DElement): tag = "CartoonVolumeStyle"
    class Circle2D(X3DElement): tag = "Circle2D"
    class ClipPlane(X3DElement): tag = "ClipPlane"
    class CollidableShape(X3DElement): tag = "CollidableShape"
    class Collision(X3DElement): tag = "Collision"
    class CollisionCollection(X3DElement): tag = "CollisionCollection"
    class CollisionSensor(X3DElement): tag = "CollisionSensor"
    class Color(X3DElement): tag = "Color"
    class ColorChaser(X3DElement): tag = "ColorChaser"
    class ColorDamper(X3DElement): tag = "ColorDamper"
    class ColorInterpolator(X3DElement): tag = "ColorInterpolator"
    class ColorMaskMode(X3DElement): tag = "ColorMaskMode"
    class ColorRGBA(X3DElement): tag = "ColorRGBA"
    class CommonSurfaceShader(X3DElement): tag = "CommonSurfaceShader"
    class ComposedCubeMapTexture(X3DElement): tag = "ComposedCubeMapTexture"
    class ComposedShader(X3DElement): tag = "ComposedShader"
    class ComposedTexture3D(X3DElement): tag = "ComposedTexture3D"
    class ComposedVolumeStyle(X3DElement): tag = "ComposedVolumeStyle"
    class Cone(X3DElement): tag = "Cone"
    class Coordinate(X3DElement): tag = "Coordinate"
    class CoordinateDamper(X3DElement): tag = "CoordinateDamper"
    class CoordinateDouble(X3DElement): tag = "CoordinateDouble"
    class CoordinateInterpolator(X3DElement): tag = "CoordinateInterpolator"
    class Cylinder(X3DElement): tag = "Cylinder"
    class CylinderSensor(X3DElement): tag = "CylinderSensor"
    class DepthMode(X3DElement): tag = "DepthMode"
    class DirectionalLight(X3DElement): tag = "DirectionalLight"
    class Dish(X3DElement): tag = "Dish"
    class Disk2D(X3DElement): tag = "Disk2D"
    class DoubleAxisHingeJoint(X3DElement): tag = "DoubleAxisHingeJoint"
    class DynamicLOD(X3DElement): tag = "DynamicLOD"
    class EdgeEnhancementVolumeStyle(X3DElement): tag = "EdgeEnhancementVolumeStyle"
    class ElevationGrid(X3DElement): tag = "ElevationGrid"
    class Environment(X3DElement): tag = "Environment"
    class Extrusion(X3DElement): tag = "Extrusion"
    class Script(X3DElement): tag = "Script"
    class Field(X3DElement): tag = "Field"
    class FloatVertexAttribute(X3DElement): tag = "FloatVertexAttribute"
    class Fog(X3DElement): tag = "Fog"
    class FontStyle(X3DElement):
        class FSManager(HTML.TagElement.context):
            class FakeCSS:
                __slots__ = ["props"]
                def __init__(self, props):
                    self.props = props
            @classmethod
            def manage_styles(cls, styles):
                return cls.FakeCSS(styles)
        context = FSManager
        tag = "FontStyle"
    class GeneratedCubeMapTexture(X3DElement): tag = "GeneratedCubeMapTexture"
    class GeoCoordinate(X3DElement): tag = "GeoCoordinate"
    class GeoElevationGrid(X3DElement): tag = "GeoElevationGrid"
    class GeoLOD(X3DElement): tag = "GeoLOD"
    class GeoLocation(X3DElement): tag = "GeoLocation"
    class GeoMetadata(X3DElement): tag = "GeoMetadata"
    class GeoOrigin(X3DElement): tag = "GeoOrigin"
    class GeoPositionInterpolator(X3DElement): tag = "GeoPositionInterpolator"
    class GeoTransform(X3DElement): tag = "GeoTransform"
    class GeoViewpoint(X3DElement): tag = "GeoViewpoint"
    class Group(X3DElement): tag = "Group"
    class HAnimDisplacer(X3DElement): tag = "HAnimDisplacer"
    class HAnimHumanoid(X3DElement): tag = "HAnimHumanoid"
    class HAnimJoint(X3DElement): tag = "HAnimJoint"
    class HAnimSegment(X3DElement): tag = "HAnimSegment"
    class HAnimSite(X3DElement): tag = "HAnimSite"
    class ImageTexture(X3DElement): tag = "ImageTexture"
    class ImageTexture3D(X3DElement): tag = "ImageTexture3D"
    class ImageTextureAtlas(X3DElement): tag = "ImageTextureAtlas"
    class IndexedFaceSet(X3DElement): tag = "IndexedFaceSet"
    class IndexedLineSet(X3DElement): tag = "IndexedLineSet"
    class IndexedQuadSet(X3DElement): tag = "IndexedQuadSet"
    class IndexedTriangleSet(X3DElement): tag = "IndexedTriangleSet"
    class IndexedTriangleStripSet(X3DElement): tag = "IndexedTriangleStripSet"
    class Inline(X3DElement): tag = "Inline"
    class IsoSurfaceVolumeData(X3DElement): tag = "IsoSurfaceVolumeData"
    class LOD(X3DElement): tag = "LOD"
    class LineProperties(X3DElement): tag = "LineProperties"
    class LineSet(X3DElement): tag = "LineSet"
    class MPRPlane(X3DElement): tag = "MPRPlane"
    class MPRVolumeStyle(X3DElement): tag = "MPRVolumeStyle"
    class Material(X3DElement): tag = "Material"
    class MatrixTextureTransform(X3DElement): tag = "MatrixTextureTransform"
    class MatrixTransform(X3DElement): tag = "MatrixTransform"
    class Mesh(X3DElement): tag = "Mesh"
    class MetadataBoolean(X3DElement): tag = "MetadataBoolean"
    class MetadataDouble(X3DElement): tag = "MetadataDouble"
    class MetadataFloat(X3DElement): tag = "MetadataFloat"
    class MetadataInteger(X3DElement): tag = "MetadataInteger"
    class MetadataSet(X3DElement): tag = "MetadataSet"
    class MetadataString(X3DElement): tag = "MetadataString"
    class MotorJoint(X3DElement): tag = "MotorJoint"
    class MovieTexture(X3DElement): tag = "MovieTexture"
    class MultiTexture(X3DElement): tag = "MultiTexture"
    class MultiTextureCoordinate(X3DElement): tag = "MultiTextureCoordinate"
    class NavigationInfo(X3DElement): tag = "NavigationInfo"
    class NodeNameSpace(X3DElement): tag = "NodeNameSpace"
    class Normal(X3DElement): tag = "Normal"
    class NormalInterpolator(X3DElement): tag = "NormalInterpolator"
    class Nozzle(X3DElement): tag = "Nozzle"
    class OpacityMapVolumeStyle(X3DElement): tag = "OpacityMapVolumeStyle"
    class OrientationChaser(X3DElement): tag = "OrientationChaser"
    class OrientationDamper(X3DElement): tag = "OrientationDamper"
    class OrientationInterpolator(X3DElement): tag = "OrientationInterpolator"
    class OrthoViewpoint(X3DElement): tag = "OrthoViewpoint"
    class Param(X3DElement): tag = "Param"
    class ParticleSet(X3DElement): tag = "ParticleSet"
    class PhysicalEnvironmentLight(X3DElement): tag = "PhysicalEnvironmentLight"
    class PhysicalMaterial(X3DElement): tag = "PhysicalMaterial"
    class PixelTexture(X3DElement): tag = "PixelTexture"
    class PixelTexture3D(X3DElement): tag = "PixelTexture3D"
    class Plane(X3DElement): tag = "Plane"
    class PlaneSensor(X3DElement): tag = "PlaneSensor"
    class PointLight(X3DElement): tag = "PointLight"
    class PointProperties(X3DElement): tag = "PointProperties"
    class PointSet(X3DElement): tag = "PointSet"
    class Polyline2D(X3DElement): tag = "Polyline2D"
    class Polypoint2D(X3DElement): tag = "Polypoint2D"
    class PopGeometry(X3DElement): tag = "PopGeometry"
    class PopGeometryLevel(X3DElement): tag = "PopGeometryLevel"
    class PositionChaser(X3DElement): tag = "PositionChaser"
    class PositionChaser2D(X3DElement): tag = "PositionChaser2D"
    class PositionDamper(X3DElement): tag = "PositionDamper"
    class PositionDamper2D(X3DElement): tag = "PositionDamper2D"
    class PositionInterpolator(X3DElement): tag = "PositionInterpolator"
    class PositionInterpolator2D(X3DElement): tag = "PositionInterpolator2D"
    class ProjectionVolumeStyle(X3DElement): tag = "ProjectionVolumeStyle"
    class ProximitySensor(X3DElement): tag = "ProximitySensor"
    class Pyramid(X3DElement): tag = "Pyramid"
    class QuadSet(X3DElement): tag = "QuadSet"
    class RadarVolumeStyle(X3DElement): tag = "RadarVolumeStyle"
    class Rectangle2D(X3DElement): tag = "Rectangle2D"
    class RectangularTorus(X3DElement): tag = "RectangularTorus"
    class RefinementTexture(X3DElement): tag = "RefinementTexture"
    class RemoteSelectionGroup(X3DElement): tag = "RemoteSelectionGroup"
    class RenderedTexture(X3DElement): tag = "RenderedTexture"
    class RigidBody(X3DElement): tag = "RigidBody"
    class RigidBodyCollection(X3DElement): tag = "RigidBodyCollection"
    class Route(X3DElement): tag = "Route"
    class ScalarChaser(X3DElement): tag = "ScalarChaser"
    class ScalarDamper(X3DElement): tag = "ScalarDamper"
    class ScalarInterpolator(X3DElement): tag = "ScalarInterpolator"
    class Scene(X3DElement): tag = "Scene"
    class SegmentedVolumeData(X3DElement): tag = "SegmentedVolumeData"
    class ShadedVolumeStyle(X3DElement): tag = "ShadedVolumeStyle"
    class ShaderPart(X3DElement): tag = "ShaderPart"
    class Shape(X3DElement): tag = "Shape"
    class SilhouetteEnhancementVolumeStyle(X3DElement): tag = "SilhouetteEnhancementVolumeStyle"
    class SingleAxisHingeJoint(X3DElement): tag = "SingleAxisHingeJoint"
    class SliderJoint(X3DElement): tag = "SliderJoint"
    class SlopedCylinder(X3DElement): tag = "SlopedCylinder"
    class Snout(X3DElement): tag = "Snout"
    class SolidOfRevolution(X3DElement): tag = "SolidOfRevolution"
    class Sound(X3DElement): tag = "Sound"
    class Sphere(X3DElement): tag = "Sphere"
    class SphereSegment(X3DElement): tag = "SphereSegment"
    class SphereSensor(X3DElement): tag = "SphereSensor"
    class SplinePositionInterpolator(X3DElement): tag = "SplinePositionInterpolator"
    class SpotLight(X3DElement): tag = "SpotLight"
    class StaticGroup(X3DElement): tag = "StaticGroup"
    class StippleVolumeStyle(X3DElement): tag = "StippleVolumeStyle"
    class SurfaceShaderTexture(X3DElement): tag = "SurfaceShaderTexture"
    class Switch(X3DElement): tag = "Switch"
    class TexCoordDamper2D(X3DElement): tag = "TexCoordDamper2D"
    class Text(X3DElement): tag = "Text"
    class Texture(X3DElement): tag = "Texture"
    class TextureCoordinate(X3DElement): tag = "TextureCoordinate"
    class TextureCoordinate3D(X3DElement): tag = "TextureCoordinate3D"
    class TextureCoordinateGenerator(X3DElement): tag = "TextureCoordinateGenerator"
    class TextureProperties(X3DElement): tag = "TextureProperties"
    class TextureTransform(X3DElement): tag = "TextureTransform"
    class TextureTransform3D(X3DElement): tag = "TextureTransform3D"
    class TextureTransformMatrix3D(X3DElement): tag = "TextureTransformMatrix3D"
    class TimeSensor(X3DElement): tag = "TimeSensor"
    class IntegerSequencer(X3DElement): tag = "IntegerSequencer"
    class ToneMappedVolumeStyle(X3DElement): tag = "ToneMappedVolumeStyle"
    class Torus(X3DElement): tag = "Torus"
    class TouchSensor(X3DElement): tag = "TouchSensor"
    class Transform(X3DElement): tag = "Transform"
    class TriangleSet(X3DElement): tag = "TriangleSet"
    class TriangleSet2D(X3DElement): tag = "TriangleSet2D"
    class TwoSidedMaterial(X3DElement): tag = "TwoSidedMaterial"
    class Uniform(X3DElement): tag = "Uniform"
    class UniversalJoint(X3DElement): tag = "UniversalJoint"
    class Viewfrustum(X3DElement): tag = "Viewfrustum"
    class Viewpoint(X3DElement): tag = "Viewpoint"
    class VolumeData(X3DElement): tag = "VolumeData"
    class WorldInfo(X3DElement): tag = "WorldInfo"
    class X3DAppearanceChildNode(X3DElement): tag = "X3DAppearanceChildNode"
    class X3DAppearanceNode(X3DElement): tag = "X3DAppearanceNode"
    class X3DBackgroundNode(X3DElement): tag = "X3DBackgroundNode"
    class X3DBinaryContainerGeometryNode(X3DElement): tag = "X3DBinaryContainerGeometryNode"
    class X3DBindableNode(X3DElement): tag = "X3DBindableNode"
    class X3DBoundedObject(X3DElement): tag = "X3DBoundedObject"
    class X3DChaserNode(X3DElement): tag = "X3DChaserNode"
    class X3DChildNode(X3DElement): tag = "X3DChildNode"
    class X3DColorNode(X3DElement): tag = "X3DColorNode"
    class X3DComposableVolumeRenderStyleNode(X3DElement): tag = "X3DComposableVolumeRenderStyleNode"
    class X3DComposedGeometryNode(X3DElement): tag = "X3DComposedGeometryNode"
    class X3DCoordinateNode(X3DElement): tag = "X3DCoordinateNode"
    class X3DDamperNode(X3DElement): tag = "X3DDamperNode"
    class X3DDragSensorNode(X3DElement): tag = "X3DDragSensorNode"
    class X3DEnvironmentNode(X3DElement): tag = "X3DEnvironmentNode"
    class X3DEnvironmentTextureNode(X3DElement): tag = "X3DEnvironmentTextureNode"
    class X3DFogNode(X3DElement): tag = "X3DFogNode"
    class X3DFollowerNode(X3DElement): tag = "X3DFollowerNode"
    class X3DFontStyleNode(X3DElement): tag = "X3DFontStyleNode"
    class X3DGeometricPropertyNode(X3DElement): tag = "X3DGeometricPropertyNode"
    class X3DGeometryNode(X3DElement): tag = "X3DGeometryNode"
    class X3DGroupingNode(X3DElement): tag = "X3DGroupingNode"
    class X3DInfoNode(X3DElement): tag = "X3DInfoNode"
    class X3DInterpolatorNode(X3DElement): tag = "X3DInterpolatorNode"
    class X3DLODNode(X3DElement): tag = "X3DLODNode"
    class X3DLightNode(X3DElement): tag = "X3DLightNode"
    class X3DMaterialNode(X3DElement): tag = "X3DMaterialNode"
    class X3DMetadataObject(X3DElement): tag = "X3DMetadataObject"
    class X3DNBodyCollidableNode(X3DElement): tag = "X3DNBodyCollidableNode"
    class X3DNavigationInfoNode(X3DElement): tag = "X3DNavigationInfoNode"
    class X3DNode(X3DElement): tag = "X3DNode"
    class X3DPlanarGeometryNode(X3DElement): tag = "X3DPlanarGeometryNode"
    class X3DPointingDeviceSensorNode(X3DElement): tag = "X3DPointingDeviceSensorNode"
    class X3DRigidJointNode(X3DElement): tag = "X3DRigidJointNode"
    class X3DSensorNode(X3DElement): tag = "X3DSensorNode"
    class X3DShaderNode(X3DElement): tag = "X3DShaderNode"
    class X3DShapeNode(X3DElement): tag = "X3DShapeNode"
    class X3DSoundNode(X3DElement): tag = "X3DSoundNode"
    class X3DSoundSourceNode(X3DElement): tag = "X3DSoundSourceNode"
    class X3DSpatialGeometryNode(X3DElement): tag = "X3DSpatialGeometryNode"
    class X3DTexture3DNode(X3DElement): tag = "X3DTexture3DNode"
    class X3DTextureCoordinateNode(X3DElement): tag = "X3DTextureCoordinateNode"
    class X3DTextureNode(X3DElement): tag = "X3DTextureNode"
    class X3DTextureTransformNode(X3DElement): tag = "X3DTextureTransformNode"
    class X3DTimeDependentNode(X3DElement): tag = "X3DTimeDependentNode"
    class X3DTouchSensorNode(X3DElement): tag = "X3DTouchSensorNode"
    class X3DTransformNode(X3DElement): tag = "X3DTransformNode"
    class X3DVertexAttributeNode(X3DElement): tag = "X3DVertexAttributeNode"
    class X3DViewpointNode(X3DElement): tag = "X3DViewpointNode"
    class X3DVolumeDataNode(X3DElement): tag = "X3DVolumeDataNode"
    class X3DVolumeRenderStyleNode(X3DElement): tag = "X3DVolumeRenderStyleNode"


class X3DControls:
    """Reusable browser controls for native X3DOM scenes and primitives.

    Build scenes and geometry with McUtils.Plots.X3DInterface, then place this
    toolbar in a ReadoutHTML. Applications need no DOM scripting or HTML authoring.
    Targets may be native objects or explicit DOM ids. Native primitive targets
    resolve property aliases and their actual nodes through the native API.

    The initial control values must match the initial scene attributes. For a
    bare X3D object in a static ReadoutScene, set scene.opts['id'] = scene.id;
    X3D.id otherwise identifies the outer wrapper created by to_widget(). Both
    direct X3D nodes and to_widget() wrappers are supported by reset_view().
    """

    def __init__(self, *controls, id=None):
        if len(controls) == 1 and isinstance(controls[0], (list, tuple)):
            controls = tuple(controls[0])
        self.controls = tuple(controls)
        self.id = self._new_id() if id is None else self._check_id(id)

    @staticmethod
    def _new_id():
        import uuid
        return "x3d-controls-" + uuid.uuid4().hex

    @staticmethod
    def _check_id(value):
        if not isinstance(value, str) or not value or any(c.isspace() for c in value):
            raise ValueError("X3D target ids must be nonempty strings without whitespace")
        return value

    @classmethod
    def _target_ids(cls, targets, property=None):
        if isinstance(targets, str) or hasattr(targets, "id") or hasattr(targets, "figure") or hasattr(targets, "attrs"):
            targets = [targets]
        try:
            targets = list(targets)
        except TypeError:
            raise TypeError("X3D controls need a target object/id or an iterable of targets") from None
        result = []
        for target in targets:
            if isinstance(target, str):
                target_id = target
            elif property is not None and hasattr(target, "get_prop_node_id"):
                target_id = target.get_prop_node_id(property)
            elif hasattr(target, "id"):
                target_id = target.id
            elif hasattr(target, "figure") and hasattr(target.figure, "id"):
                target_id = target.figure.id
            elif hasattr(target, "attrs"):
                target_id = target.attrs.get("id")
            else:
                raise TypeError("X3D target has no native id or property-node resolver")
            target_id = cls._check_id(target_id)
            if target_id not in result:
                result.append(target_id)
        if not result:
            raise ValueError("X3D controls need at least one target")
        return result

    @staticmethod
    def _json(value):
        import json
        return json.dumps(value, ensure_ascii=True)

    @staticmethod
    def _number(value, name):
        import math
        import numbers
        if isinstance(value, bool) or not isinstance(value, numbers.Real) or not math.isfinite(value):
            raise ValueError(name + " must be a finite real number")
        return float(value)

    @classmethod
    def _property_targets(cls, targets, property):
        if not isinstance(property, str) or not property or any(c.isspace() for c in property):
            raise ValueError("An X3D property name is required")
        if isinstance(targets, str) or hasattr(targets, "id") or hasattr(targets, "figure") or hasattr(targets, "attrs"):
            targets = [targets]
        bindings = []
        for target in targets:
            target_id = cls._target_ids(target, property=property)[0]
            attribute = target.resolve_prop_attr(property) if hasattr(target, "resolve_prop_attr") else property
            if not isinstance(attribute, str) or not attribute or any(c.isspace() for c in attribute):
                raise ValueError("An X3D attribute name is required")
            binding = {"id": target_id, "attribute": attribute}
            if binding not in bindings:
                bindings.append(binding)
        if not bindings:
            raise ValueError("X3D controls need at least one target")
        return bindings

    @classmethod
    def switch(cls, targets, labels, *, value=0, label="Conformer", id=None):
        """A select box that updates only the supplied Switch.whichChoice nodes."""
        targets = cls._target_ids(targets)
        if isinstance(labels, str):
            raise TypeError("labels must be an iterable of choice labels")
        labels = tuple(str(s) for s in labels)
        if not labels:
            raise ValueError("a Switch control needs at least one choice")
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value < len(labels):
            raise ValueError("initial Switch choice must be a valid integer index")
        control_id = cls._new_id() if id is None else cls._check_id(id)
        handler = """
const value = Number(this.value);
if (!Number.isInteger(value) || value < 0 || value >= %d) return;
for (const id of %s) {
  const node = document.getElementById(id);
  if (node) node.setAttribute('whichChoice', String(value));
}
""" % (len(labels), cls._json(targets))
        options = [HTML.Option(text, value=str(i), **({"selected": True} if i == value else {}))
                   for i, text in enumerate(labels)]
        return HTML.Label(
            str(label),
            HTML.Select(*options, id=control_id, onchange=handler, **{"aria-label": str(label)}),
            cls="mcutils-x3d-control",
            style="display:inline-flex;align-items:center;gap:.45em;"
        )

    @classmethod
    def slider(cls, targets, property, *, value=0, min=0, max=1, step=.01, label=None, id=None):
        """Control a scalar numeric X3D property over a configurable range.

        Native objects resolve both the property alias and its owning node.
        Explicit DOM ids use property as the attribute name. Values are assigned
        directly, without property-specific transformations or formatting.
        """
        targets = cls._property_targets(targets, property)
        value, minimum, maximum, step = (cls._number(v, name) for v, name in
                                         ((value, "value"), (min, "min"), (max, "max"), (step, "step")))
        if minimum >= maximum:
            raise ValueError("slider min must be less than max")
        if step <= 0:
            raise ValueError("slider step must be positive")
        if not minimum <= value <= maximum:
            raise ValueError("slider value must be within min and max")
        if label is None:
            label = property
        control_id = cls._new_id() if id is None else cls._check_id(id)
        output_id = control_id + "-value"
        handler = """
const raw = Number(this.value);
if (!Number.isFinite(raw)) return;
const value = Math.min(%s, Math.max(%s, raw));
for (const target of %s) {
  const node = document.getElementById(target.id);
  if (node) node.setAttribute(target.attribute, String(value));
}
const output = document.getElementById(%s);
if (output) output.textContent = String(value);
""" % (cls._json(maximum), cls._json(minimum), cls._json(targets), cls._json(output_id))
        return HTML.Label(
            str(label),
            HTML.Input(type="range", min=str(minimum), max=str(maximum), step=str(step), value=str(value),
                       id=control_id, oninput=handler, **{"aria-label": str(label)}),
            HTML.Output(str(value), id=output_id),
            cls="mcutils-x3d-control",
            style="display:inline-flex;align-items:center;gap:.45em;"
        )

    @classmethod
    def reset_view(cls, targets, *, label="Reset views", id=None):
        """Reset each target X3DOM runtime once, for direct nodes or wrappers."""
        targets = cls._target_ids(targets)
        control_id = cls._new_id() if id is None else cls._check_id(id)
        handler = """
const seen = new Set();
for (const id of %s) {
  const target = document.getElementById(id);
  if (!target) continue;
  const node = target.runtime ? target :
    (target.querySelector('x3d, x3d-canvas') || target.closest('x3d, x3d-canvas'));
  if (!node || seen.has(node)) continue;
  seen.add(node);
  if (node.runtime && typeof node.runtime.resetView === 'function') node.runtime.resetView();
}
""" % cls._json(targets)
        return HTML.Button(str(label), type="button", id=control_id, onclick=handler,
                           cls="mcutils-x3d-control")

    def to_widget(self):
        """The existing McUtils HTML element consumed by ReadoutHTML."""
        return HTML.Div(*self.controls, id=self.id, cls="mcutils-x3d-controls",
                        style="display:flex;flex-wrap:wrap;align-items:center;gap:1em;padding:.45em 0;")

    def to_jhtml(self):
        return self.to_widget()

    def tostring(self, **opts):
        return self.to_widget().tostring(**opts)

    def _repr_html_(self):
        return self.tostring()
