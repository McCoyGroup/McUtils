# LLM Examples

## Overlay a model and observations

```python
import numpy as np
from McUtils.Plots import Plot, ScatterPlot

rng = np.random.default_rng(2)
x = np.linspace(0, 2 * np.pi, 50)
observed = np.sin(x) + rng.normal(0, .08, len(x))
figure = Plot(x, np.sin(x), plot_label="model", plot_style={"color": "navy"})
ScatterPlot(x, observed, figure=figure, plot_label="data",
            plot_style={"color": "crimson", "s": 18})
figure.axes_labels = ["phase / rad", "signal"]
figure.show()
```

## Plot a three-dimensional surface

```python
import numpy as np
from McUtils.Plots import Plot3D

x = y = np.linspace(-2, 2, 80)
xx, yy = np.meshgrid(x, y)
zz = np.exp(-(xx**2 + yy**2)) * np.cos(3 * xx)
figure = Plot3D(xx, yy, zz, plot_style={"cmap": "viridis"},
                axes_labels=["x", "y", "V(x,y)"])
figure.show()
```

## Apply a reusable theme

```python
import numpy as np
from McUtils.Plots import Plot, ThemeManager, ColorPalette

ThemeManager.add_theme('paper',
                       'mccoy',
                       background=ColorPalette.prep_color('yellow', lighten=.3, saturate=-.5),
                       palette="viridis",
                       )
x = np.linspace(0, 5, 100)
fig = Plot(x, np.exp(-x) * np.cos(5 * x), axes_labels=["t", "signal"], theme="paper")
fig.show()
```

## Compare scalar fields in a graphics grid

```python
import numpy as np
from McUtils.Plots import GraphicsGrid, ContourPlot

x = y = np.linspace(-2, 2, 80)
xx, yy = np.meshgrid(x, y)
fields = [np.exp(-(xx**2 + yy**2)), xx * np.exp(-(xx**2 + yy**2))]
grid = GraphicsGrid(nrows=1, ncols=2, spacings=[10, 0], padding=50)
for column, (field, label) in enumerate(zip(fields, ["density", "x-weighted density"])):
    ContourPlot(xx, yy, field, figure=grid[0, column], plot_label=label, cmap="magma")
grid.show()
```

## Draw geometric primitives in 3-D

```python
import numpy as np
from McUtils.Plots import Graphics3D, Sphere, Line

figure = Graphics3D(axes_labels=["x", "y", "z"], backend='plotly3D') # requires plotly
Sphere([0, 0, 0], radius=1, color="lightblue").plot(figure)
axes = np.eye(3)
colors = ["red", "green", "blue"]
for axis, color in zip(axes, colors):
    Line([[0, 0, 0], axis * 1.5], color=color).plot(figure)
figure.show()
```
