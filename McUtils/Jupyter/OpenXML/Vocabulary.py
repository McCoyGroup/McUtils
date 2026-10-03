"""Explicit OpenXML elements used by the presentation adapter and reference.

This is a focused vocabulary, not a bundled copy of the Office specification.
Unknown extensions remain available through OpenXML.Element/register_element.
Element names follow the MIT-licensed Open XML SDK nomenclature.
"""
from .Elements import OpenXML

class Drawing:
    class Accent1Color(OpenXML.TagElement): tag = "a:accent1"
    class Accent2Color(OpenXML.TagElement): tag = "a:accent2"
    class Accent3Color(OpenXML.TagElement): tag = "a:accent3"
    class Accent4Color(OpenXML.TagElement): tag = "a:accent4"
    class Accent5Color(OpenXML.TagElement): tag = "a:accent5"
    class Accent6Color(OpenXML.TagElement): tag = "a:accent6"
    class AdjustHandleList(OpenXML.TagElement): tag = "a:ahLst"
    class Alpha(OpenXML.TagElement): tag = "a:alpha"
    class AdjustValueList(OpenXML.TagElement): tag = "a:avLst"
    class Bevel(OpenXML.TagElement): tag = "a:bevel"
    class BackgroundFillStyleList(OpenXML.TagElement): tag = "a:bgFillStyleLst"
    class Blip(OpenXML.TagElement): tag = "a:blip"
    class BodyProperties(OpenXML.TagElement): tag = "a:bodyPr"
    class Break(OpenXML.TagElement): tag = "a:br"
    class CharacterBullet(OpenXML.TagElement): tag = "a:buChar"
    class BulletFont(OpenXML.TagElement): tag = "a:buFont"
    class NoBullet(OpenXML.TagElement): tag = "a:buNone"
    class ChildExtents(OpenXML.TagElement): tag = "a:chExt"
    class ChildOffset(OpenXML.TagElement): tag = "a:chOff"
    class CloseShapePath(OpenXML.TagElement): tag = "a:close"
    class ColorScheme(OpenXML.TagElement): tag = "a:clrScheme"
    class ComplexScriptFont(OpenXML.TagElement): tag = "a:cs"
    class CustomGeometry(OpenXML.TagElement): tag = "a:custGeom"
    class ConnectionSite(OpenXML.TagElement): tag = "a:cxn"
    class ConnectionSiteList(OpenXML.TagElement): tag = "a:cxnLst"
    class DefaultParagraphProperties(OpenXML.TagElement): tag = "a:defPPr"
    class DefaultRunProperties(OpenXML.TagElement): tag = "a:defRPr"
    class Dark1Color(OpenXML.TagElement): tag = "a:dk1"
    class Dark2Color(OpenXML.TagElement): tag = "a:dk2"
    class EastAsianFont(OpenXML.TagElement): tag = "a:ea"
    class EffectList(OpenXML.TagElement): tag = "a:effectLst"
    class EffectReference(OpenXML.TagElement): tag = "a:effectRef"
    class EffectStyle(OpenXML.TagElement): tag = "a:effectStyle"
    class EffectStyleList(OpenXML.TagElement): tag = "a:effectStyleLst"
    class EndParagraphRunProperties(OpenXML.TagElement): tag = "a:endParaRPr"
    class Extension(OpenXML.TagElement): tag = "a:ext"
    class Extents(OpenXML.TagElement): tag = "a:ext"
    class ExtensionList(OpenXML.TagElement): tag = "a:extLst"
    class ExtraColorSchemeList(OpenXML.TagElement): tag = "a:extraClrSchemeLst"
    class FillRectangle(OpenXML.TagElement): tag = "a:fillRect"
    class FillReference(OpenXML.TagElement): tag = "a:fillRef"
    class FillStyleList(OpenXML.TagElement): tag = "a:fillStyleLst"
    class Field(OpenXML.TagElement): tag = "a:fld"
    class FormatScheme(OpenXML.TagElement): tag = "a:fmtScheme"
    class FollowedHyperlinkColor(OpenXML.TagElement): tag = "a:folHlink"
    class Fonts(OpenXML.TagElement): tag = "a:font"
    class FontReference(OpenXML.TagElement): tag = "a:fontRef"
    class FontScheme(OpenXML.TagElement): tag = "a:fontScheme"
    class ShapeGuide(OpenXML.TagElement): tag = "a:gd"
    class ShapeGuideList(OpenXML.TagElement): tag = "a:gdLst"
    class GradientFill(OpenXML.TagElement): tag = "a:gradFill"
    class Graphic(OpenXML.TagElement): tag = "a:graphic"
    class GraphicData(OpenXML.TagElement): tag = "a:graphicData"
    class GraphicFrameLocks(OpenXML.TagElement): tag = "a:graphicFrameLocks"
    class GradientStop(OpenXML.TagElement): tag = "a:gs"
    class GradientStopList(OpenXML.TagElement): tag = "a:gsLst"
    class HeadEnd(OpenXML.TagElement): tag = "a:headEnd"
    class Hyperlink(OpenXML.TagElement): tag = "a:hlink"
    class LatinFont(OpenXML.TagElement): tag = "a:latin"
    class LinearGradientFill(OpenXML.TagElement): tag = "a:lin"
    class Outline(OpenXML.TagElement): tag = "a:ln"
    class LineDefault(OpenXML.TagElement): tag = "a:lnDef"
    class LineReference(OpenXML.TagElement): tag = "a:lnRef"
    class LineSpacing(OpenXML.TagElement): tag = "a:lnSpc"
    class LineStyleList(OpenXML.TagElement): tag = "a:lnStyleLst"
    class LineTo(OpenXML.TagElement): tag = "a:lnTo"
    class ListStyle(OpenXML.TagElement): tag = "a:lstStyle"
    class Light1Color(OpenXML.TagElement): tag = "a:lt1"
    class Light2Color(OpenXML.TagElement): tag = "a:lt2"
    class LuminanceModulation(OpenXML.TagElement): tag = "a:lumMod"
    class Level1ParagraphProperties(OpenXML.TagElement): tag = "a:lvl1pPr"
    class Level2ParagraphProperties(OpenXML.TagElement): tag = "a:lvl2pPr"
    class Level3ParagraphProperties(OpenXML.TagElement): tag = "a:lvl3pPr"
    class Level4ParagraphProperties(OpenXML.TagElement): tag = "a:lvl4pPr"
    class Level5ParagraphProperties(OpenXML.TagElement): tag = "a:lvl5pPr"
    class Level6ParagraphProperties(OpenXML.TagElement): tag = "a:lvl6pPr"
    class Level7ParagraphProperties(OpenXML.TagElement): tag = "a:lvl7pPr"
    class Level8ParagraphProperties(OpenXML.TagElement): tag = "a:lvl8pPr"
    class Level9ParagraphProperties(OpenXML.TagElement): tag = "a:lvl9pPr"
    class MajorFont(OpenXML.TagElement): tag = "a:majorFont"
    class MasterColorMapping(OpenXML.TagElement): tag = "a:masterClrMapping"
    class MinorFont(OpenXML.TagElement): tag = "a:minorFont"
    class Miter(OpenXML.TagElement): tag = "a:miter"
    class MoveTo(OpenXML.TagElement): tag = "a:moveTo"
    class NoAutoFit(OpenXML.TagElement): tag = "a:noAutofit"
    class NoFill(OpenXML.TagElement): tag = "a:noFill"
    class NormalAutoFit(OpenXML.TagElement): tag = "a:normAutofit"
    class ObjectDefaults(OpenXML.TagElement): tag = "a:objectDefaults"
    class Offset(OpenXML.TagElement): tag = "a:off"
    class OuterShadow(OpenXML.TagElement): tag = "a:outerShdw"
    class Paragraph(OpenXML.TagElement): tag = "a:p"
    class ParagraphProperties(OpenXML.TagElement): tag = "a:pPr"
    class PathGradientFill(OpenXML.TagElement): tag = "a:path"
    class PathList(OpenXML.TagElement): tag = "a:pathLst"
    class PictureLocks(OpenXML.TagElement): tag = "a:picLocks"
    class Position(OpenXML.TagElement): tag = "a:pos"
    class PresetDash(OpenXML.TagElement): tag = "a:prstDash"
    class PresetGeometry(OpenXML.TagElement): tag = "a:prstGeom"
    class Point(OpenXML.TagElement): tag = "a:pt"
    class Run(OpenXML.TagElement): tag = "a:r"
    class RunProperties(OpenXML.TagElement): tag = "a:rPr"
    class Rectangle(OpenXML.TagElement): tag = "a:rect"
    class Round(OpenXML.TagElement): tag = "a:round"
    class SaturationModulation(OpenXML.TagElement): tag = "a:satMod"
    class SchemeColor(OpenXML.TagElement): tag = "a:schemeClr"
    class RgbColorModelPercentage(OpenXML.TagElement): tag = "a:scrgbClr"
    class Shade(OpenXML.TagElement): tag = "a:shade"
    class SolidFill(OpenXML.TagElement): tag = "a:solidFill"
    class ShapeAutoFit(OpenXML.TagElement): tag = "a:spAutoFit"
    class ShapeLocks(OpenXML.TagElement): tag = "a:spLocks"
    class ShapeProperties(OpenXML.TagElement): tag = "a:spPr"
    class SpaceBefore(OpenXML.TagElement): tag = "a:spcBef"
    class SpacingPercent(OpenXML.TagElement): tag = "a:spcPct"
    class SpacingPoints(OpenXML.TagElement): tag = "a:spcPts"
    class SourceRectangle(OpenXML.TagElement): tag = "a:srcRect"
    class RgbColorModelHex(OpenXML.TagElement): tag = "a:srgbClr"
    class Stretch(OpenXML.TagElement): tag = "a:stretch"
    class ShapeStyle(OpenXML.TagElement): tag = "a:style"
    class ScaleX(OpenXML.TagElement): tag = "a:sx"
    class ScaleY(OpenXML.TagElement): tag = "a:sy"
    class SystemColor(OpenXML.TagElement): tag = "a:sysClr"
    class Text(OpenXML.TagElement): tag = "a:t"
    class TailEnd(OpenXML.TagElement): tag = "a:tailEnd"
    class TableStyleList(OpenXML.TagElement): tag = "a:tblStyleLst"
    class Theme(OpenXML.TagElement): tag = "a:theme"
    class ThemeElements(OpenXML.TagElement): tag = "a:themeElements"
    class Tint(OpenXML.TagElement): tag = "a:tint"
    class Transform2D(OpenXML.TagElement): tag = "a:xfrm"


class Drawing2014:
    class CreationId(OpenXML.TagElement): tag = "a16:creationId"


class Model3DAnimation:
    class AnimationProperties(OpenXML.TagElement): tag = "a3danim:animPr"
    class EmbeddedAnimation(OpenXML.TagElement): tag = "a3danim:embedAnim"
    class PosterFrame(OpenXML.TagElement): tag = "a3danim:posterFrame"


class Model3D:
    class AmbientLight(OpenXML.TagElement): tag = "am3d:ambientLight"
    class Blip(OpenXML.TagElement): tag = "am3d:blip"
    class Camera(OpenXML.TagElement): tag = "am3d:camera"
    class Color(OpenXML.TagElement): tag = "am3d:clr"
    class ExtensionList(OpenXML.TagElement): tag = "am3d:extLst"
    class IlluminancePositiveRatio(OpenXML.TagElement): tag = "am3d:illuminance"
    class IntensityPositiveRatio(OpenXML.TagElement): tag = "am3d:intensity"
    class LookAt(OpenXML.TagElement): tag = "am3d:lookAt"
    class MeterPerModelUnit(OpenXML.TagElement): tag = "am3d:meterPerModelUnit"
    class Model3D(OpenXML.TagElement): tag = "am3d:model3d"
    class ObjectViewport(OpenXML.TagElement): tag = "am3d:objViewport"
    class Orthographic(OpenXML.TagElement): tag = "am3d:orthographic"
    class Perspective(OpenXML.TagElement): tag = "am3d:perspective"
    class Position(OpenXML.TagElement): tag = "am3d:pos"
    class PostTranslate(OpenXML.TagElement): tag = "am3d:postTrans"
    class PreTranslate(OpenXML.TagElement): tag = "am3d:preTrans"
    class PointLight(OpenXML.TagElement): tag = "am3d:ptLight"
    class Model3DRaster(OpenXML.TagElement): tag = "am3d:raster"
    class Rotate3D(OpenXML.TagElement): tag = "am3d:rot"
    class Scale(OpenXML.TagElement): tag = "am3d:scale"
    class ShapeProperties(OpenXML.TagElement): tag = "am3d:spPr"
    class ScaleX(OpenXML.TagElement): tag = "am3d:sx"
    class ScaleY(OpenXML.TagElement): tag = "am3d:sy"
    class ScaleZ(OpenXML.TagElement): tag = "am3d:sz"
    class Size(OpenXML.TagElement): tag = "am3d:sz"
    class Transform(OpenXML.TagElement): tag = "am3d:trans"
    class Up(OpenXML.TagElement): tag = "am3d:up"
    class WindowViewport(OpenXML.TagElement): tag = "am3d:winViewport"


class ExtendedProperties:
    class ApplicationVersion(OpenXML.TagElement): tag = "ap:AppVersion"
    class Application(OpenXML.TagElement): tag = "ap:Application"
    class Company(OpenXML.TagElement): tag = "ap:Company"
    class HeadingPairs(OpenXML.TagElement): tag = "ap:HeadingPairs"
    class HiddenSlides(OpenXML.TagElement): tag = "ap:HiddenSlides"
    class HyperlinksChanged(OpenXML.TagElement): tag = "ap:HyperlinksChanged"
    class LinksUpToDate(OpenXML.TagElement): tag = "ap:LinksUpToDate"
    class MultimediaClips(OpenXML.TagElement): tag = "ap:MMClips"
    class Notes(OpenXML.TagElement): tag = "ap:Notes"
    class Paragraphs(OpenXML.TagElement): tag = "ap:Paragraphs"
    class PresentationFormat(OpenXML.TagElement): tag = "ap:PresentationFormat"
    class Properties(OpenXML.TagElement): tag = "ap:Properties"
    class ScaleCrop(OpenXML.TagElement): tag = "ap:ScaleCrop"
    class SharedDocument(OpenXML.TagElement): tag = "ap:SharedDoc"
    class Slides(OpenXML.TagElement): tag = "ap:Slides"
    class TitlesOfParts(OpenXML.TagElement): tag = "ap:TitlesOfParts"
    class TotalTime(OpenXML.TagElement): tag = "ap:TotalTime"
    class Words(OpenXML.TagElement): tag = "ap:Words"


class SVG:
    class SVGBlip(OpenXML.TagElement): tag = "asvg:svgBlip"


class CoreProperties:
    class CoreProperties(OpenXML.TagElement): tag = "cp:coreProperties"
    class LastModifiedBy(OpenXML.TagElement): tag = "cp:lastModifiedBy"
    class Revision(OpenXML.TagElement): tag = "cp:revision"


class DublinCore:
    class Creator(OpenXML.TagElement): tag = "dc:creator"
    class Title(OpenXML.TagElement): tag = "dc:title"


class DublinCoreTerms:
    class Created(OpenXML.TagElement): tag = "dcterms:created"
    class Modified(OpenXML.TagElement): tag = "dcterms:modified"


class Compatibility:
    class AlternateContent(OpenXML.TagElement): tag = "mc:AlternateContent"
    class Choice(OpenXML.TagElement): tag = "mc:Choice"
    class Fallback(OpenXML.TagElement): tag = "mc:Fallback"


class ContentTypes:
    class Default(OpenXML.TagElement): tag = "opc:Default"
    class Override(OpenXML.TagElement): tag = "opc:Override"
    class Types(OpenXML.TagElement): tag = "opc:Types"


class Presentation:
    class Animate(OpenXML.TagElement): tag = "p:anim"
    class AttributeName(OpenXML.TagElement): tag = "p:attrName"
    class AttributeNameList(OpenXML.TagElement): tag = "p:attrNameLst"
    class Background(OpenXML.TagElement): tag = "p:bg"
    class BackgroundStyleReference(OpenXML.TagElement): tag = "p:bgRef"
    class BlipFill(OpenXML.TagElement): tag = "p:blipFill"
    class BodyStyle(OpenXML.TagElement): tag = "p:bodyStyle"
    class CommonBehavior(OpenXML.TagElement): tag = "p:cBhvr"
    class NonVisualGraphicFrameDrawingProperties(OpenXML.TagElement): tag = "p:cNvGraphicFramePr"
    class NonVisualGroupShapeDrawingProperties(OpenXML.TagElement): tag = "p:cNvGrpSpPr"
    class NonVisualPictureDrawingProperties(OpenXML.TagElement): tag = "p:cNvPicPr"
    class NonVisualDrawingProperties(OpenXML.TagElement): tag = "p:cNvPr"
    class NonVisualShapeDrawingProperties(OpenXML.TagElement): tag = "p:cNvSpPr"
    class CommonSlideData(OpenXML.TagElement): tag = "p:cSld"
    class CommonSlideViewProperties(OpenXML.TagElement): tag = "p:cSldViewPr"
    class CommonTimeNode(OpenXML.TagElement): tag = "p:cTn"
    class CommonViewProperties(OpenXML.TagElement): tag = "p:cViewPr"
    class ChildTimeNodeList(OpenXML.TagElement): tag = "p:childTnLst"
    class ColorMap(OpenXML.TagElement): tag = "p:clrMap"
    class ColorMapOverride(OpenXML.TagElement): tag = "p:clrMapOvr"
    class Condition(OpenXML.TagElement): tag = "p:cond"
    class DefaultTextStyle(OpenXML.TagElement): tag = "p:defaultTextStyle"
    class Extension(OpenXML.TagElement): tag = "p:ext"
    class ExtensionListWithModification(OpenXML.TagElement): tag = "p:extLst"
    class FloatVariantValue(OpenXML.TagElement): tag = "p:fltVal"
    class GraphicFrame(OpenXML.TagElement): tag = "p:graphicFrame"
    class GridSpacing(OpenXML.TagElement): tag = "p:gridSpacing"
    class GroupShapeProperties(OpenXML.TagElement): tag = "p:grpSpPr"
    class GuideList(OpenXML.TagElement): tag = "p:guideLst"
    class NextConditionList(OpenXML.TagElement): tag = "p:nextCondLst"
    class NormalViewProperties(OpenXML.TagElement): tag = "p:normalViewPr"
    class NotesSize(OpenXML.TagElement): tag = "p:notesSz"
    class NotesTextViewProperties(OpenXML.TagElement): tag = "p:notesTextViewPr"
    class NonVisualGraphicFrameProperties(OpenXML.TagElement): tag = "p:nvGraphicFramePr"
    class NonVisualGroupShapeProperties(OpenXML.TagElement): tag = "p:nvGrpSpPr"
    class NonVisualPictureProperties(OpenXML.TagElement): tag = "p:nvPicPr"
    class ApplicationNonVisualDrawingProperties(OpenXML.TagElement): tag = "p:nvPr"
    class NonVisualShapeProperties(OpenXML.TagElement): tag = "p:nvSpPr"
    class Origin(OpenXML.TagElement): tag = "p:origin"
    class OtherStyle(OpenXML.TagElement): tag = "p:otherStyle"
    class ParallelTimeNode(OpenXML.TagElement): tag = "p:par"
    class PlaceholderShape(OpenXML.TagElement): tag = "p:ph"
    class Picture(OpenXML.TagElement): tag = "p:pic"
    class Presentation(OpenXML.TagElement): tag = "p:presentation"
    class PresentationProperties(OpenXML.TagElement): tag = "p:presentationPr"
    class PreviousConditionList(OpenXML.TagElement): tag = "p:prevCondLst"
    class RestoredLeft(OpenXML.TagElement): tag = "p:restoredLeft"
    class RestoredTop(OpenXML.TagElement): tag = "p:restoredTop"
    class ScaleFactor(OpenXML.TagElement): tag = "p:scale"
    class SequenceTimeNode(OpenXML.TagElement): tag = "p:seq"
    class Slide(OpenXML.TagElement): tag = "p:sld"
    class SlideId(OpenXML.TagElement): tag = "p:sldId"
    class SlideIdList(OpenXML.TagElement): tag = "p:sldIdLst"
    class SlideLayout(OpenXML.TagElement): tag = "p:sldLayout"
    class SlideLayoutId(OpenXML.TagElement): tag = "p:sldLayoutId"
    class SlideLayoutIdList(OpenXML.TagElement): tag = "p:sldLayoutIdLst"
    class SlideMaster(OpenXML.TagElement): tag = "p:sldMaster"
    class SlideMasterId(OpenXML.TagElement): tag = "p:sldMasterId"
    class SlideMasterIdList(OpenXML.TagElement): tag = "p:sldMasterIdLst"
    class SlideSize(OpenXML.TagElement): tag = "p:sldSz"
    class SlideTarget(OpenXML.TagElement): tag = "p:sldTgt"
    class SlideViewProperties(OpenXML.TagElement): tag = "p:slideViewPr"
    class Shape(OpenXML.TagElement): tag = "p:sp"
    class ShapeProperties(OpenXML.TagElement): tag = "p:spPr"
    class ShapeTarget(OpenXML.TagElement): tag = "p:spTgt"
    class ShapeTree(OpenXML.TagElement): tag = "p:spTree"
    class StartConditionList(OpenXML.TagElement): tag = "p:stCondLst"
    class ShapeStyle(OpenXML.TagElement): tag = "p:style"
    class TimeAnimateValue(OpenXML.TagElement): tag = "p:tav"
    class TimeAnimateValueList(OpenXML.TagElement): tag = "p:tavLst"
    class TargetElement(OpenXML.TagElement): tag = "p:tgtEl"
    class Timing(OpenXML.TagElement): tag = "p:timing"
    class TitleStyle(OpenXML.TagElement): tag = "p:titleStyle"
    class TimeNode(OpenXML.TagElement): tag = "p:tn"
    class TimeNodeList(OpenXML.TagElement): tag = "p:tnLst"
    class TextBody(OpenXML.TagElement): tag = "p:txBody"
    class TextStyles(OpenXML.TagElement): tag = "p:txStyles"
    class VariantValue(OpenXML.TagElement): tag = "p:val"
    class ViewProperties(OpenXML.TagElement): tag = "p:viewPr"
    class Transform(OpenXML.TagElement): tag = "p:xfrm"


class Presentation2010:
    class CreationId(OpenXML.TagElement): tag = "p14:creationId"
    class DefaultImageDpi(OpenXML.TagElement): tag = "p14:defaultImageDpi"
    class DiscardImageEditData(OpenXML.TagElement): tag = "p14:discardImageEditData"
    class ModificationId(OpenXML.TagElement): tag = "p14:modId"


class Presentation2013:
    class ChartTrackingReferenceBased(OpenXML.TagElement): tag = "p15:chartTrackingRefBased"


class Relationships:
    class Relationship(OpenXML.TagElement): tag = "rel:Relationship"
    class Relationships(OpenXML.TagElement): tag = "rel:Relationships"


class THM15:
    class ThemeFamily(OpenXML.TagElement): tag = "thm15:themeFamily"


class VT:
    class VTInt32(OpenXML.TagElement): tag = "vt:i4"
    class VTLPSTR(OpenXML.TagElement): tag = "vt:lpstr"
    class Variant(OpenXML.TagElement): tag = "vt:variant"
    class VTVector(OpenXML.TagElement): tag = "vt:vector"


class Wordprocessing:
    class Body(OpenXML.TagElement): tag = "w:body"
    class Document(OpenXML.TagElement): tag = "w:document"
    class Paragraph(OpenXML.TagElement): tag = "w:p"
    class Run(OpenXML.TagElement): tag = "w:r"
    class Text(OpenXML.TagElement): tag = "w:t"


class Spreadsheet:
    class Cell(OpenXML.TagElement): tag = "x:c"
    class CellFormula(OpenXML.TagElement): tag = "x:f"
    class InlineString(OpenXML.TagElement): tag = "x:is"
    class Row(OpenXML.TagElement): tag = "x:row"
    class Sheet(OpenXML.TagElement): tag = "x:sheet"
    class SheetData(OpenXML.TagElement): tag = "x:sheetData"
    class Sheets(OpenXML.TagElement): tag = "x:sheets"
    class Text(OpenXML.TagElement): tag = "x:t"
    class CellValue(OpenXML.TagElement): tag = "x:v"
    class Workbook(OpenXML.TagElement): tag = "x:workbook"
    class Worksheet(OpenXML.TagElement): tag = "x:worksheet"


def register_vocabularies(parent):
    namespace = parent.register_namespace("a", "http://schemas.openxmlformats.org/drawingml/2006/main", Drawing)
    namespace.public_name = "Drawing"
    parent.Drawing = namespace
    namespace = parent.register_namespace("a16", "http://schemas.microsoft.com/office/drawing/2014/main", Drawing2014)
    namespace.public_name = "Drawing2014"
    parent.Drawing2014 = namespace
    namespace = parent.register_namespace("a3danim", "http://schemas.microsoft.com/office/drawing/2018/animation/model3d", Model3DAnimation)
    namespace.public_name = "Model3DAnimation"
    parent.Model3DAnimation = namespace
    namespace = parent.register_namespace("am3d", "http://schemas.microsoft.com/office/drawing/2017/model3d", Model3D)
    namespace.public_name = "Model3D"
    parent.Model3D = namespace
    namespace = parent.register_namespace("ap", "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties", ExtendedProperties)
    namespace.public_name = "ExtendedProperties"
    parent.ExtendedProperties = namespace
    namespace = parent.register_namespace("asvg", "http://schemas.microsoft.com/office/drawing/2016/SVG/main", SVG)
    namespace.public_name = "SVG"
    parent.SVG = namespace
    namespace = parent.register_namespace("cp", "http://schemas.openxmlformats.org/package/2006/metadata/core-properties", CoreProperties)
    namespace.public_name = "CoreProperties"
    parent.CoreProperties = namespace
    namespace = parent.register_namespace("dc", "http://purl.org/dc/elements/1.1/", DublinCore)
    namespace.public_name = "DublinCore"
    parent.DublinCore = namespace
    namespace = parent.register_namespace("dcterms", "http://purl.org/dc/terms/", DublinCoreTerms)
    namespace.public_name = "DublinCoreTerms"
    parent.DublinCoreTerms = namespace
    namespace = parent.register_namespace("mc", "http://schemas.openxmlformats.org/markup-compatibility/2006", Compatibility)
    namespace.public_name = "Compatibility"
    parent.Compatibility = namespace
    namespace = parent.register_namespace("opc", "http://schemas.openxmlformats.org/package/2006/content-types", ContentTypes)
    namespace.public_name = "ContentTypes"
    parent.ContentTypes = namespace
    namespace = parent.register_namespace("p", "http://schemas.openxmlformats.org/presentationml/2006/main", Presentation)
    namespace.public_name = "Presentation"
    parent.Presentation = namespace
    namespace = parent.register_namespace("p14", "http://schemas.microsoft.com/office/powerpoint/2010/main", Presentation2010)
    namespace.public_name = "Presentation2010"
    parent.Presentation2010 = namespace
    namespace = parent.register_namespace("p15", "http://schemas.microsoft.com/office/powerpoint/2012/main", Presentation2013)
    namespace.public_name = "Presentation2013"
    parent.Presentation2013 = namespace
    namespace = parent.register_namespace("rel", "http://schemas.openxmlformats.org/package/2006/relationships", Relationships)
    namespace.public_name = "Relationships"
    parent.Relationships = namespace
    namespace = parent.register_namespace("thm15", "http://schemas.microsoft.com/office/thememl/2012/main", THM15)
    namespace.public_name = "THM15"
    parent.THM15 = namespace
    namespace = parent.register_namespace("vt", "http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes", VT)
    namespace.public_name = "VT"
    parent.VT = namespace
    namespace = parent.register_namespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main", Wordprocessing)
    namespace.public_name = "Wordprocessing"
    parent.Wordprocessing = namespace
    namespace = parent.register_namespace("x", "http://schemas.openxmlformats.org/spreadsheetml/2006/main", Spreadsheet)
    namespace.public_name = "Spreadsheet"
    parent.Spreadsheet = namespace
