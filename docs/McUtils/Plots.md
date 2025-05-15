# <a id="McUtils.Plots">McUtils.Plots</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/__init__.py#L1?message=Update%20Docs)]
</div>
    
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

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[GraphicsBase](McUtils/McUtils/Plots/Graphics/GraphicsBase.md)   
</div>
   <div class="col" markdown="1">
[Graphics](McUtils/McUtils/Plots/Graphics/Graphics.md)   
</div>
   <div class="col" markdown="1">
[Graphics3D](McUtils/McUtils/Plots/Graphics/Graphics3D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[GraphicsGrid](McUtils/McUtils/Plots/Graphics/GraphicsGrid.md)   
</div>
   <div class="col" markdown="1">
[Plot](McUtils/McUtils/Plots/Plots/Plot.md)   
</div>
   <div class="col" markdown="1">
[DataPlot](McUtils/McUtils/Plots/Plots/DataPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ArrayPlot](McUtils/McUtils/Plots/Plots/ArrayPlot.md)   
</div>
   <div class="col" markdown="1">
[TensorPlot](McUtils/McUtils/Plots/Plots/TensorPlot.md)   
</div>
   <div class="col" markdown="1">
[Plot2D](McUtils/McUtils/Plots/Plots/Plot2D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ListPlot2D](McUtils/McUtils/Plots/Plots/ListPlot2D.md)   
</div>
   <div class="col" markdown="1">
[Plot3D](McUtils/McUtils/Plots/Plots/Plot3D.md)   
</div>
   <div class="col" markdown="1">
[ListPlot3D](McUtils/McUtils/Plots/Plots/ListPlot3D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CompositePlot](McUtils/McUtils/Plots/Plots/CompositePlot.md)   
</div>
   <div class="col" markdown="1">
[FilledPlot](McUtils/McUtils/Plots/Plots/FilledPlot.md)   
</div>
   <div class="col" markdown="1">
[ScatterPlot](McUtils/McUtils/Plots/Plots/ScatterPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ErrorBarPlot](McUtils/McUtils/Plots/Plots/ErrorBarPlot.md)   
</div>
   <div class="col" markdown="1">
[StickPlot](McUtils/McUtils/Plots/Plots/StickPlot.md)   
</div>
   <div class="col" markdown="1">
[DatePlot](McUtils/McUtils/Plots/Plots/DatePlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[StepPlot](McUtils/McUtils/Plots/Plots/StepPlot.md)   
</div>
   <div class="col" markdown="1">
[LogLogPlot](McUtils/McUtils/Plots/Plots/LogLogPlot.md)   
</div>
   <div class="col" markdown="1">
[SemiLogXPlot](McUtils/McUtils/Plots/Plots/SemiLogXPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[SemilogYPlot](McUtils/McUtils/Plots/Plots/SemilogYPlot.md)   
</div>
   <div class="col" markdown="1">
[HorizontalFilledPlot](McUtils/McUtils/Plots/Plots/HorizontalFilledPlot.md)   
</div>
   <div class="col" markdown="1">
[BarPlot](McUtils/McUtils/Plots/Plots/BarPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[HorizontalBarPlot](McUtils/McUtils/Plots/Plots/HorizontalBarPlot.md)   
</div>
   <div class="col" markdown="1">
[EventPlot](McUtils/McUtils/Plots/Plots/EventPlot.md)   
</div>
   <div class="col" markdown="1">
[PiePlot](McUtils/McUtils/Plots/Plots/PiePlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[StackPlot](McUtils/McUtils/Plots/Plots/StackPlot.md)   
</div>
   <div class="col" markdown="1">
[BrokenHorizontalBarPlot](McUtils/McUtils/Plots/Plots/BrokenHorizontalBarPlot.md)   
</div>
   <div class="col" markdown="1">
[VerticalLinePlot](McUtils/McUtils/Plots/Plots/VerticalLinePlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[HorizontalLinePlot](McUtils/McUtils/Plots/Plots/HorizontalLinePlot.md)   
</div>
   <div class="col" markdown="1">
[PolygonPlot](McUtils/McUtils/Plots/Plots/PolygonPlot.md)   
</div>
   <div class="col" markdown="1">
[AxisHorizontalLinePlot](McUtils/McUtils/Plots/Plots/AxisHorizontalLinePlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[AxisHorizontalSpanPlot](McUtils/McUtils/Plots/Plots/AxisHorizontalSpanPlot.md)   
</div>
   <div class="col" markdown="1">
[AxisVerticalLinePlot](McUtils/McUtils/Plots/Plots/AxisVerticalLinePlot.md)   
</div>
   <div class="col" markdown="1">
[AxisVeticalSpanPlot](McUtils/McUtils/Plots/Plots/AxisVeticalSpanPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[AxisLinePlot](McUtils/McUtils/Plots/Plots/AxisLinePlot.md)   
</div>
   <div class="col" markdown="1">
[StairsPlot](McUtils/McUtils/Plots/Plots/StairsPlot.md)   
</div>
   <div class="col" markdown="1">
[HistogramPlot](McUtils/McUtils/Plots/Plots/HistogramPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[HistogramPlot2D](McUtils/McUtils/Plots/Plots/HistogramPlot2D.md)   
</div>
   <div class="col" markdown="1">
[SpectrogramPlot](McUtils/McUtils/Plots/Plots/SpectrogramPlot.md)   
</div>
   <div class="col" markdown="1">
[AutocorrelationPlot](McUtils/McUtils/Plots/Plots/AutocorrelationPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[AngleSpectrumPlot](McUtils/McUtils/Plots/Plots/AngleSpectrumPlot.md)   
</div>
   <div class="col" markdown="1">
[CoherencePlot](McUtils/McUtils/Plots/Plots/CoherencePlot.md)   
</div>
   <div class="col" markdown="1">
[CrossSpectralDensityPlot](McUtils/McUtils/Plots/Plots/CrossSpectralDensityPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[MagnitudeSpectrumPlot](McUtils/McUtils/Plots/Plots/MagnitudeSpectrumPlot.md)   
</div>
   <div class="col" markdown="1">
[PhaseSpectrumPlot](McUtils/McUtils/Plots/Plots/PhaseSpectrumPlot.md)   
</div>
   <div class="col" markdown="1">
[PowerSpectralDensityPlot](McUtils/McUtils/Plots/Plots/PowerSpectralDensityPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CrossCorrelationPlot](McUtils/McUtils/Plots/Plots/CrossCorrelationPlot.md)   
</div>
   <div class="col" markdown="1">
[BoxPlot](McUtils/McUtils/Plots/Plots/BoxPlot.md)   
</div>
   <div class="col" markdown="1">
[ViolinPlot](McUtils/McUtils/Plots/Plots/ViolinPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[BoxAndWhiskerPlot](McUtils/McUtils/Plots/Plots/BoxAndWhiskerPlot.md)   
</div>
   <div class="col" markdown="1">
[HexagonalHistogramPlot](McUtils/McUtils/Plots/Plots/HexagonalHistogramPlot.md)   
</div>
   <div class="col" markdown="1">
[QuiverPlot](McUtils/McUtils/Plots/Plots/QuiverPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[StreamPlot](McUtils/McUtils/Plots/Plots/StreamPlot.md)   
</div>
   <div class="col" markdown="1">
[MatrixPlot](McUtils/McUtils/Plots/Plots/MatrixPlot.md)   
</div>
   <div class="col" markdown="1">
[SparsityPlot](McUtils/McUtils/Plots/Plots/SparsityPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ContourPlot](McUtils/McUtils/Plots/Plots/ContourPlot.md)   
</div>
   <div class="col" markdown="1">
[DensityPlot](McUtils/McUtils/Plots/Plots/DensityPlot.md)   
</div>
   <div class="col" markdown="1">
[HeatmapPlot](McUtils/McUtils/Plots/Plots/HeatmapPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[TriPlot](McUtils/McUtils/Plots/Plots/TriPlot.md)   
</div>
   <div class="col" markdown="1">
[TriDensityPlot](McUtils/McUtils/Plots/Plots/TriDensityPlot.md)   
</div>
   <div class="col" markdown="1">
[TriContourLinesPlot](McUtils/McUtils/Plots/Plots/TriContourLinesPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[TriContourPlot](McUtils/McUtils/Plots/Plots/TriContourPlot.md)   
</div>
   <div class="col" markdown="1">
[ListContourPlot](McUtils/McUtils/Plots/Plots/ListContourPlot.md)   
</div>
   <div class="col" markdown="1">
[ListDensityPlot](McUtils/McUtils/Plots/Plots/ListDensityPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ListTriContourPlot](McUtils/McUtils/Plots/Plots/ListTriContourPlot.md)   
</div>
   <div class="col" markdown="1">
[ListTriDensityPlot](McUtils/McUtils/Plots/Plots/ListTriDensityPlot.md)   
</div>
   <div class="col" markdown="1">
[ScatterPlot3D](McUtils/McUtils/Plots/Plots/ScatterPlot3D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[WireframePlot3D](McUtils/McUtils/Plots/Plots/WireframePlot3D.md)   
</div>
   <div class="col" markdown="1">
[ContourPlot3D](McUtils/McUtils/Plots/Plots/ContourPlot3D.md)   
</div>
   <div class="col" markdown="1">
[ListTriPlot3D](McUtils/McUtils/Plots/Plots/ListTriPlot3D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[GraphicsPrimitive](McUtils/McUtils/Plots/Primitives/GraphicsPrimitive.md)   
</div>
   <div class="col" markdown="1">
[Sphere](McUtils/McUtils/Plots/Primitives/Sphere.md)   
</div>
   <div class="col" markdown="1">
[Cylinder](McUtils/McUtils/Plots/Primitives/Cylinder.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Disk](McUtils/McUtils/Plots/Primitives/Disk.md)   
</div>
   <div class="col" markdown="1">
[Line](McUtils/McUtils/Plots/Primitives/Line.md)   
</div>
   <div class="col" markdown="1">
[Text](McUtils/McUtils/Plots/Primitives/Text.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Arrow](McUtils/McUtils/Plots/Primitives/Arrow.md)   
</div>
   <div class="col" markdown="1">
[Inset](McUtils/McUtils/Plots/Primitives/Inset.md)   
</div>
   <div class="col" markdown="1">
[EventHandler](McUtils/McUtils/Plots/Interactive/EventHandler.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Animator](McUtils/McUtils/Plots/Interactive/Animator.md)   
</div>
   <div class="col" markdown="1">
[Styled](McUtils/McUtils/Plots/Styling/Styled.md)   
</div>
   <div class="col" markdown="1">
[ThemeManager](McUtils/McUtils/Plots/Styling/ThemeManager.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[PlotLegend](McUtils/McUtils/Plots/Styling/PlotLegend.md)   
</div>
   <div class="col" markdown="1">
[Image](McUtils/McUtils/Plots/Image/Image.md)   
</div>
   <div class="col" markdown="1">
[GraphicsPropertyManager](McUtils/McUtils/Plots/Properties/GraphicsPropertyManager.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[GraphicsPropertyManager3D](McUtils/McUtils/Plots/Properties/GraphicsPropertyManager3D.md)   
</div>
   <div class="col" markdown="1">
[SceneJSON](McUtils/McUtils/Plots/SceneJSON/SceneJSON.md)   
</div>
   <div class="col" markdown="1">
[X3D](McUtils/McUtils/Plots/X3DInterface/X3D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[X3DPrimitive](McUtils/McUtils/Plots/X3DInterface/X3DPrimitive.md)   
</div>
   <div class="col" markdown="1">
[X3DGeometryObject](McUtils/McUtils/Plots/X3DInterface/X3DGeometryObject.md)   
</div>
   <div class="col" markdown="1">
[X3DGeometryGroup](McUtils/McUtils/Plots/X3DInterface/X3DGeometryGroup.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[X3DGroup](McUtils/McUtils/Plots/X3DInterface/X3DGroup.md)   
</div>
   <div class="col" markdown="1">
[X3DScene](McUtils/McUtils/Plots/X3DInterface/X3DScene.md)   
</div>
   <div class="col" markdown="1">
[X3DMaterial](McUtils/McUtils/Plots/X3DInterface/X3DMaterial.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[X3DLine](McUtils/McUtils/Plots/X3DInterface/X3DLine.md)   
</div>
   <div class="col" markdown="1">
[X3DSphere](McUtils/McUtils/Plots/X3DInterface/X3DSphere.md)   
</div>
   <div class="col" markdown="1">
[X3DCone](McUtils/McUtils/Plots/X3DInterface/X3DCone.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[X3DCylinder](McUtils/McUtils/Plots/X3DInterface/X3DCylinder.md)   
</div>
   <div class="col" markdown="1">
[X3DTorus](McUtils/McUtils/Plots/X3DInterface/X3DTorus.md)   
</div>
   <div class="col" markdown="1">
[X3DSwitch](McUtils/McUtils/Plots/X3DInterface/X3DSwitch.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[X3DListAnimator](McUtils/McUtils/Plots/X3DInterface/X3DListAnimator.md)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>













---


<div markdown="1" class="text-secondary">
<div class="container">
  <div class="row">
   <div class="col" markdown="1">
**Feedback**   
</div>
   <div class="col" markdown="1">
**Examples**   
</div>
   <div class="col" markdown="1">
**Templates**   
</div>
   <div class="col" markdown="1">
**Documentation**   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Bug](https://github.com/McCoyGroup/McUtils/issues/new?title=Documentation%20Improvement%20Needed)/[Request](https://github.com/McCoyGroup/McUtils/issues/new?title=Example%20Request)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/__init__.py#L1?message=Update%20Docs)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>
</div>