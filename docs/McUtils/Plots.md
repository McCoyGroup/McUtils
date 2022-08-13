# <a id="McUtils.Plots">McUtils.Plots</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/tree/master/Plots)]
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

<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[GraphicsBase](Plots/Graphics/GraphicsBase.md)   
</div>
   <div class="col" markdown="1">
[Graphics](Plots/Graphics/Graphics.md)   
</div>
   <div class="col" markdown="1">
[Graphics3D](Plots/Graphics/Graphics3D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[GraphicsGrid](Plots/Graphics/GraphicsGrid.md)   
</div>
   <div class="col" markdown="1">
[Plot](Plots/Plots/Plot.md)   
</div>
   <div class="col" markdown="1">
[DataPlot](Plots/Plots/DataPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ArrayPlot](Plots/Plots/ArrayPlot.md)   
</div>
   <div class="col" markdown="1">
[TensorPlot](Plots/Plots/TensorPlot.md)   
</div>
   <div class="col" markdown="1">
[Plot2D](Plots/Plots/Plot2D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ListPlot2D](Plots/Plots/ListPlot2D.md)   
</div>
   <div class="col" markdown="1">
[Plot3D](Plots/Plots/Plot3D.md)   
</div>
   <div class="col" markdown="1">
[ListPlot3D](Plots/Plots/ListPlot3D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[FilledPlot](Plots/Plots/FilledPlot.md)   
</div>
   <div class="col" markdown="1">
[ScatterPlot](Plots/Plots/ScatterPlot.md)   
</div>
   <div class="col" markdown="1">
[ErrorBarPlot](Plots/Plots/ErrorBarPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[StickPlot](Plots/Plots/StickPlot.md)   
</div>
   <div class="col" markdown="1">
[DatePlot](Plots/Plots/DatePlot.md)   
</div>
   <div class="col" markdown="1">
[StepPlot](Plots/Plots/StepPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[LogLogPlot](Plots/Plots/LogLogPlot.md)   
</div>
   <div class="col" markdown="1">
[SemiLogXPlot](Plots/Plots/SemiLogXPlot.md)   
</div>
   <div class="col" markdown="1">
[SemilogYPlot](Plots/Plots/SemilogYPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[HorizontalFilledPlot](Plots/Plots/HorizontalFilledPlot.md)   
</div>
   <div class="col" markdown="1">
[BarPlot](Plots/Plots/BarPlot.md)   
</div>
   <div class="col" markdown="1">
[HorizontalBarPlot](Plots/Plots/HorizontalBarPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[EventPlot](Plots/Plots/EventPlot.md)   
</div>
   <div class="col" markdown="1">
[PiePlot](Plots/Plots/PiePlot.md)   
</div>
   <div class="col" markdown="1">
[StackPlot](Plots/Plots/StackPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[BrokenHorizontalBarPlot](Plots/Plots/BrokenHorizontalBarPlot.md)   
</div>
   <div class="col" markdown="1">
[HorizontalLinePlot](Plots/Plots/HorizontalLinePlot.md)   
</div>
   <div class="col" markdown="1">
[PolygonPlot](Plots/Plots/PolygonPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[AxisHorizontalLinePlot](Plots/Plots/AxisHorizontalLinePlot.md)   
</div>
   <div class="col" markdown="1">
[AxisHorizontalSpanPlot](Plots/Plots/AxisHorizontalSpanPlot.md)   
</div>
   <div class="col" markdown="1">
[AxisVerticalLinePlot](Plots/Plots/AxisVerticalLinePlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[AxisVeticalSpanPlot](Plots/Plots/AxisVeticalSpanPlot.md)   
</div>
   <div class="col" markdown="1">
[AxisLinePlot](Plots/Plots/AxisLinePlot.md)   
</div>
   <div class="col" markdown="1">
[StairsPlot](Plots/Plots/StairsPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[HistogramPlot](Plots/Plots/HistogramPlot.md)   
</div>
   <div class="col" markdown="1">
[HistogramPlot2D](Plots/Plots/HistogramPlot2D.md)   
</div>
   <div class="col" markdown="1">
[SpectrogramPlot](Plots/Plots/SpectrogramPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[AutocorrelationPlot](Plots/Plots/AutocorrelationPlot.md)   
</div>
   <div class="col" markdown="1">
[AngleSpectrumPlot](Plots/Plots/AngleSpectrumPlot.md)   
</div>
   <div class="col" markdown="1">
[CoherencePlot](Plots/Plots/CoherencePlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CrossSpectralDensityPlot](Plots/Plots/CrossSpectralDensityPlot.md)   
</div>
   <div class="col" markdown="1">
[MagnitudeSpectrumPlot](Plots/Plots/MagnitudeSpectrumPlot.md)   
</div>
   <div class="col" markdown="1">
[PhaseSpectrumPlot](Plots/Plots/PhaseSpectrumPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[PowerSpectralDensityPlot](Plots/Plots/PowerSpectralDensityPlot.md)   
</div>
   <div class="col" markdown="1">
[CrossCorrelationPlot](Plots/Plots/CrossCorrelationPlot.md)   
</div>
   <div class="col" markdown="1">
[BoxPlot](Plots/Plots/BoxPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ViolinPlot](Plots/Plots/ViolinPlot.md)   
</div>
   <div class="col" markdown="1">
[BoxAndWhiskerPlot](Plots/Plots/BoxAndWhiskerPlot.md)   
</div>
   <div class="col" markdown="1">
[HexagonalHistogramPlot](Plots/Plots/HexagonalHistogramPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[QuiverPlot](Plots/Plots/QuiverPlot.md)   
</div>
   <div class="col" markdown="1">
[StreamPlot](Plots/Plots/StreamPlot.md)   
</div>
   <div class="col" markdown="1">
[MatrixPlot](Plots/Plots/MatrixPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[SparsityPlot](Plots/Plots/SparsityPlot.md)   
</div>
   <div class="col" markdown="1">
[ContourPlot](Plots/Plots/ContourPlot.md)   
</div>
   <div class="col" markdown="1">
[DensityPlot](Plots/Plots/DensityPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[HeatmapPlot](Plots/Plots/HeatmapPlot.md)   
</div>
   <div class="col" markdown="1">
[TriPlot](Plots/Plots/TriPlot.md)   
</div>
   <div class="col" markdown="1">
[TriDensityPlot](Plots/Plots/TriDensityPlot.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[TriContourLinesPlot](Plots/Plots/TriContourLinesPlot.md)   
</div>
   <div class="col" markdown="1">
[TriContourPlot](Plots/Plots/TriContourPlot.md)   
</div>
   <div class="col" markdown="1">
[ScatterPlot3D](Plots/Plots/ScatterPlot3D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[WireframePlot3D](Plots/Plots/WireframePlot3D.md)   
</div>
   <div class="col" markdown="1">
[ContourPlot3D](Plots/Plots/ContourPlot3D.md)   
</div>
   <div class="col" markdown="1">
[GraphicsPrimitive](Plots/Primitives/GraphicsPrimitive.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Sphere](Plots/Primitives/Sphere.md)   
</div>
   <div class="col" markdown="1">
[Cylinder](Plots/Primitives/Cylinder.md)   
</div>
   <div class="col" markdown="1">
[Disk](Plots/Primitives/Disk.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Line](Plots/Primitives/Line.md)   
</div>
   <div class="col" markdown="1">
[Text](Plots/Primitives/Text.md)   
</div>
   <div class="col" markdown="1">
[Arrow](Plots/Primitives/Arrow.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Inset](Plots/Primitives/Inset.md)   
</div>
   <div class="col" markdown="1">
[EventHandler](Plots/Interactive/EventHandler.md)   
</div>
   <div class="col" markdown="1">
[Animator](Plots/Interactive/Animator.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Styled](Plots/Styling/Styled.md)   
</div>
   <div class="col" markdown="1">
[ThemeManager](Plots/Styling/ThemeManager.md)   
</div>
   <div class="col" markdown="1">
[PlotLegend](Plots/Styling/PlotLegend.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Image](Plots/Image/Image.md)   
</div>
   <div class="col" markdown="1">
[GraphicsPropertyManager](Plots/Properties/GraphicsPropertyManager.md)   
</div>
   <div class="col" markdown="1">
[GraphicsPropertyManager3D](Plots/Properties/GraphicsPropertyManager3D.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>






<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#tests">Tests</a> <a class="float-right" data-toggle="collapse" href="#tests"><i class="fa fa-chevron-down"></i></a>
 </div>
<div class="collapsible-section collapsible-section-body collapse show" id="tests" markdown="1">

- [Plot](#Plot)
- [Plot3D](#Plot3D)
- [GraphicsGrid](#GraphicsGrid)
- [PlotStyling](#PlotStyling)
- [PlotGridStyling](#PlotGridStyling)
- [Scatter](#Scatter)
- [ListContourPlot](#ListContourPlot)
- [ListTriPlot3D](#ListTriPlot3D)
- [ListTriDensityPlot](#ListTriDensityPlot)
- [ListTriContourPlot](#ListTriContourPlot)
- [Animation](#Animation)
- [VTK](#VTK)
- [PlotDelayed](#PlotDelayed)
- [Plot3DDelayed](#Plot3DDelayed)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
#### <a class="collapse-link" data-toggle="collapse" href="#test-setup">Setup</a> <a class="float-right" data-toggle="collapse" href="#test-setup"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse" id="test-setup" markdown="1">

Before we can run our examples we should get a bit of setup out of the way.
Since these examples were harvested from the unit tests not all pieces
will be necessary for all situations.
```python
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Plots import *
import sys, os, numpy as np
```

All tests are wrapped in a test class
```python
class PlotsTests(TestCase):
    def tearDownClass(cls):
        import matplotlib.pyplot as plt
    def result_file(self, fname):
        if not os.path.isdir(os.path.join(TestManager.test_dir, "test_results")):
            os.mkdir(os.path.join(TestManager.test_dir, "test_results"))
        return os.path.join(TestManager.test_dir, "test_results", fname)
```

 </div>
</div>

#### <a name="Plot">Plot</a>
```python
    def test_Plot(self):
        grid = np.linspace(0, 2*np.pi, 100)
        plot = Plot(grid, np.sin(grid))

        plot.savefig(self.result_file("test_Plot.png"))
        plot.close()
```
#### <a name="Plot3D">Plot3D</a>
```python
    def test_Plot3D(self):
        import matplotlib.cm as colormaps

        f = lambda pt: np.sin(pt[0]) + np.cos(pt[1])
        plot = Plot3D(f, np.arange(0, 2 * np.pi, .1), np.arange(0, 2 * np.pi, .1),
                      plot_style={
                          "cmap": colormaps.get_cmap('viridis')
                      },
                      axes_labels=['dogs', 'cats',
                                   Styled('rats', color='red')
                                   ],
                      plot_label='my super cool 3D plot',
                      plot_range=[(-5, 5)] * 3,
                      plot_legend='i lik turtle',
                      colorbar=True
                      )
        plot.savefig(self.result_file("test_Plot3D.png"))
        plot.close()
```
#### <a name="GraphicsGrid">GraphicsGrid</a>
```python
    def test_GraphicsGrid(self):

        main = GraphicsGrid(ncols=3, nrows=1)
        grid = np.linspace(0, 2 * np.pi, 100)
        grid_2D = np.meshgrid(grid, grid)
        main[0, 0] = ContourPlot(grid_2D[1], grid_2D[0], np.sin(grid_2D[0]), figure=main[0, 0])
        main[0, 1] = ContourPlot(grid_2D[1], grid_2D[0], np.sin(grid_2D[0]) * np.cos(grid_2D[1]), figure=main[0, 1])
        main[0, 2] = ContourPlot(grid_2D[1], grid_2D[0], np.cos(grid_2D[1]), figure=main[0, 2])
        # main.show()

        main.savefig(self.result_file("test_GraphicsGrid.png"))
        main.close()
```
#### <a name="PlotStyling">PlotStyling</a>
```python
    def test_PlotStyling(self):
        grid = np.linspace(0, 2 * np.pi, 100)
        # file = '~/Desktop/y.png'
        plot = Plot(grid, np.sin(grid),
                    aspect_ratio=1.3,
                    theme='dark_background',
                    ticks_style={'color':'red', 'labelcolor':'red'},
                    plot_label='bleh',
                    padding=((30, 0), (20, 20))
                    )
        # plot.savefig(file)
        # plot = Image.from_file(file)
        # plot.show()
        plot.savefig(self.result_file("test_PlotStyling.png"))
        plot.close()
```
#### <a name="PlotGridStyling">PlotGridStyling</a>
```python
    def test_PlotGridStyling(self):
        main = GraphicsGrid(ncols=3, nrows=1, theme='Solarize_Light2', figure_label='my beuatufil triptych',
                            padding=((35, 60), (35, 40)))
        grid = np.linspace(0, 2 * np.pi, 100)
        grid_2D = np.meshgrid(grid, grid)
        x = grid_2D[1]; y = grid_2D[0]
        main[0, 0] = ContourPlot(x, y, np.sin(y), plot_label='$sin(x)$',
                                 axes_labels=[None, "cats (cc)"],
                                 figure=main[0, 0]
                                 )
        main[0, 1] = ContourPlot(x, y, np.sin(x) * np.cos(y),
                                 plot_label='$sin(x)cos(y)$',
                                 axes_labels=[Styled("dogs (arb.)", {'color': 'red'}), None],
                                 figure=main[0, 1])
        main[0, 2] = ContourPlot(x, y, np.cos(y), plot_label='$cos(y)$', figure=main[0, 2])
        main.colorbar = {"graphics": main[0, 1].graphics}

        # main.show()

        main.savefig(self.result_file("test_PlotGridStyling.png"))
        main.close()
```
#### <a name="Scatter">Scatter</a>
```python
    def test_Scatter(self):
        pts = np.random.rand(50, 2)
        plot = ScatterPlot(*pts.T,
                           aspect_ratio=2,
                           image_size=250
                           )
        # plot.show()
        plot.savefig(self.result_file("test_Scatter.pdf"), format='pdf')
        plot.close()
```
#### <a name="ListContourPlot">ListContourPlot</a>
```python
    def test_ListContourPlot(self):
        pts = np.pi*np.random.rand(150, 2)
        sins = np.sin(pts[:, 0])
        coses = np.cos(pts[:, 1])
        ptss = np.concatenate((pts, np.reshape(sins*coses, sins.shape + (1,))), axis=1)
        plot = ListContourPlot(ptss)

        plot.savefig(self.result_file("test_ListContourPlot.png"))
        plot.close()
```
#### <a name="ListTriPlot3D">ListTriPlot3D</a>
```python
    def test_ListTriPlot3D(self):
        pts = np.pi*np.random.rand(150, 2)
        sins = np.sin(pts[:, 0])
        coses = np.cos(pts[:, 1])
        ptss = np.concatenate((pts, np.reshape(sins*coses, sins.shape + (1,))), axis=1)
        plot = ListTriPlot3D(ptss)

        plot.savefig(self.result_file("test_ListTriPlot3D.png"))
        plot.close()
```
#### <a name="ListTriDensityPlot">ListTriDensityPlot</a>
```python
    def test_ListTriDensityPlot(self):
        pts = np.pi*np.random.rand(150, 2)
        sins = np.sin(pts[:, 0])
        coses = np.cos(pts[:, 1])
        ptss = np.concatenate((pts, np.reshape(sins*coses, sins.shape + (1,))), axis=1)
        plot = ListTriDensityPlot(ptss)

        plot.savefig(self.result_file("test_ListTriDensityPlot.png"))
        plot.close()
```
#### <a name="ListTriContourPlot">ListTriContourPlot</a>
```python
    def test_ListTriContourPlot(self):
        pts = np.pi*np.random.rand(150, 2)
        sins = np.sin(pts[:, 0])
        coses = np.cos(pts[:, 1])
        ptss = np.concatenate((pts, np.reshape(sins*coses, sins.shape + (1,))), axis=1)
        plot = ListTriContourPlot(ptss)
        plot.add_colorbar()

        plot.savefig(self.result_file("test_ListTriContourPlot.png"))
        plot.close()
```
#### <a name="Animation">Animation</a>
```python
    def test_Animation(self):
        "Currently broken"
        def get_data(*args):
            pts = np.pi*np.random.normal(scale = .25, size=(10550, 2))
            sins = np.sin(pts[:, 0])
            coses = np.cos(pts[:, 1])
            ptss = np.concatenate((pts, np.reshape(sins*coses, sins.shape + (1,))), axis=1)
            return (ptss, )
        plot = ListTriContourPlot(*get_data(),
                                  animate = get_data,
                                  plot_range = [
                                      [-np.pi, np.pi],
                                      [-np.pi, np.pi]
                                  ]
                                  )

        plot.show()

        plot.savefig(self.result_file("test_ListTriContourPlot.gif"))
        plot.close()
```
#### <a name="VTK">VTK</a>
```python
    def test_VTK(self):
        plot = Graphics3D(backend="VTK", image_size=[1500, 500])
        Sphere().plot(plot)
```
#### <a name="PlotDelayed">PlotDelayed</a>
```python
    def test_PlotDelayed(self):
        p = Plot(background = 'black')
        for i, c in enumerate(('red', 'white', 'blue')):
            p.plot(np.sin, [-2 + 4/3*i, -2 + 4/3*(i+1)], color = c)
        # p.show()

        p.savefig(self.result_file("test_PlotDelayed.gif"))
        p.close()
```
#### <a name="Plot3DDelayed">Plot3DDelayed</a>
```python
    def test_Plot3DDelayed(self):
        p = Plot3D(background = 'black')
        for i, c in enumerate(('red', 'white', 'blue')):
            p.plot(
                lambda g: (
                    np.sin(g.T[0]) + np.cos(g.T[1])
                ),
                [-2 + 4/3*i, -2 + 4/3*(i+1)],
                [-2 + 4/3*i, -2 + 4/3*(i+1)],
                color = c)
        # p.show()

        p.savefig(self.result_file("test_Plot3DDelayed.gif"))
        p.close()
```

 </div>
</div>

___

[Edit Examples](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Plots.md) or 
[Create New Examples](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Plots.md) <br/>
[Edit Template](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Plots.md) or 
[Create New Template](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Plots.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/master/Plots/__init__.py?message=Update%20Docs)