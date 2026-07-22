"""
A plotting framework that builds off of `matplotlib`, but potentially could use a different backend.
The design is intended to mirror the `Graphics` framework in Mathematica and where possible option
names have been chosen to be the same.
Difficulties with `matplotlib` prevent a perfect mirror but the design is consistent.
There are a few primary divisions:
1. `Graphics`/`Graphics3D`/`GraphicsGrid` provide basic access to `matplotlib.figure` and `matplotlib.axes`
    they also hold a `GraphicsPropertyManager`/`GraphicsPropertyManager3D` that manages all properties
    (`image_size`, `axes_label`, `ticks_style`, etc.).
    The full lists can be found on the relevant reference pages and are bound as `properties` on the
    `Graphics`/`Graphics3D` instances.
2. `Plot/Plot3D` and everything in the `Plots` subpackage provide concrete instances of common plots
    with nice names/consistent with Mathematica for discoverability but primarily fall back onto
    `matplotlib` built-in methods and then allow for restyling/data reuse, etc.
3. `Primitives` provide direct access to the shapes that are actually plotted on screen (i.e. `matplotlib.Patch` objects)
    in a convenient way to add on to existing plots
4. `Styling` provides access to theme management/construction

Image/animation support and other back end support for 3D graphics (`VTK`) are provided at the experimental level.
"""
__all__ = ['GraphicsBase', 'Graphics', 'Graphics3D', 'GraphicsGrid', 'Plot', 'DataPlot', 'ArrayPlot', 'TensorPlot', 'Plot2D', 'ListPlot2D', 'Plot3D', 'ListPlot3D', 'CompositePlot', 'resolve_plotter', 'plot_generic', 'plot_multi', 'FilledPlot', 'ScatterPlot', 'ListScatterPlot', 'ErrorBarPlot', 'ListErrorBarPlot', 'StickPlot', 'DatePlot', 'StepPlot', 'LogLogPlot', 'SemiLogXPlot', 'SemilogYPlot', 'HorizontalFilledPlot', 'BarPlot', 'HorizontalBarPlot', 'EventPlot', 'PiePlot', 'StackPlot', 'BrokenHorizontalBarPlot', 'VerticalLinePlot', 'HorizontalLinePlot', 'PolygonPlot', 'AxisHorizontalLinePlot', 'AxisHorizontalSpanPlot', 'AxisVerticalLinePlot', 'AxisVeticalSpanPlot', 'AxisLinePlot', 'StairsPlot', 'HistogramPlot', 'HistogramPlot2D', 'SpectrogramPlot', 'AutocorrelationPlot', 'AngleSpectrumPlot', 'CoherencePlot', 'CrossSpectralDensityPlot', 'MagnitudeSpectrumPlot', 'PhaseSpectrumPlot', 'PowerSpectralDensityPlot', 'CrossCorrelationPlot', 'BoxPlot', 'ViolinPlot', 'BoxAndWhiskerPlot', 'HexagonalHistogramPlot', 'QuiverPlot', 'StreamPlot', 'MatrixPlot', 'SparsityPlot', 'ContourPlot', 'ContourLinePlot', 'DensityPlot', 'HeatmapPlot', 'TriPlot', 'TriDensityPlot', 'TriContourLinesPlot', 'TriContourPlot', 'ListContourPlot', 'ListDensityPlot', 'ListTriContourPlot', 'ListTriDensityPlot', 'ScatterPlot3D', 'WireframePlot3D', 'ContourPlot3D', 'ListTriPlot3D', 'GraphicsPrimitive', 'Cube', 'Sphere', 'Cylinder', 'Disk', 'Line', 'Text', 'Arrow', 'Inset', 'Point', 'Triangle', 'Polygon', 'Rectangle', 'Path', 'EventHandler', 'Animator', 'Styled', 'ThemeManager', 'PlotLegend', 'Image', 'GraphicsPropertyManager', 'GraphicsPropertyManager3D', 'SceneJSON', 'X3D', 'X3DPrimitive', 'X3DGeometryObject', 'X3DGeometryGroup', 'X3DGroup', 'X3DScene', 'X3DBackground', 'X3DMaterial', 'X3DLine', 'X3DSphere', 'X3DCone', 'X3DBox', 'X3DCylinder', 'X3DCappedCylinder', 'X3DArrow', 'X3DTorus', 'X3DRectangle2D', 'X3DDisk2D', 'X3DCircle2D', 'X3DPolyline2D', 'X3DTriangleSet', 'X3DIndexedTriangleSet', 'X3DIndexedLineSet', 'X3DSwitch', 'X3DListAnimator', 'X3DInterpolatingAnimator', 'ColorPalette', 'prep_color', 'SVGFigure', 'SVGFigure3D']
from .Graphics import *
from .Plots import *
from .Primitives import *
from .Interactive import *
from .Styling import *
from .Image import *
from .Properties import *
from .SceneJSON import *
from .X3DInterface import *
from .Colors import *
from .SVG import *