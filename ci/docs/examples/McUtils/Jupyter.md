# LLM Examples

Run these examples in JupyterLab or another IPython notebook.

## Compose a calculation summary card

```python
from McUtils.Jupyter import JHTML

rows = [["Method", "Energy / Eh"], ["HF", -75.983], ["CCSD(T)", -76.241]]
card = JHTML.Bootstrap.Card(
    JHTML.Bootstrap.Table(rows, cls=["table-striped", "table-hover"]),
    header="Water calculation"
)
layout = JHTML.Div(JHTML.HTML.Header("Electronic-structure summary"), card,
                   cls="container p-3")
layout.display()
```

## Generate SVG graphics programmatically

```python
from McUtils.Jupyter import JHTML

SVG = JHTML.SVGContext
drawing = SVG.Svg(
    SVG.Circle(cx=50, cy=50, r=35, fill="steelblue"),
    SVG.Line(x1=20, y1=50, x2=80, y2=50, stroke="white", stroke_width=4),
    width=100, height=100, viewBox="0 0 100 100"
)
drawing.display()
```

## Build a small interactive control panel

```python
from McUtils.Jupyter import JHTML, Button

# you may need to run JHTML.load() first
def run(event=None, widget=None):
    status.text = "Calculation submitted"

with JHTML.OutputArea() as output:
    status = JHTML.Div("Ready", dynamic=True)
    button = Button("Run calculation", run, debug_pane=output, dynamic=True)
    
    div = JHTML.Div(button, status, output, cls="d-flex gap-3")
div
```

## Style generated HTML with CSS

```python
from McUtils.Jupyter import JHTML

rules = JHTML.CSS.parse("""
.energy { font-family: monospace; color: #164e63; }
.converged { border-left: 4px solid #16a34a; padding-left: 1rem; }
""")
panel = JHTML.Div(JHTML.Span("-76.241312 Eh", cls="energy"),
                  cls="converged")
JHTML.Div(
    JHTML.Style(
        "\n".join(css.tostring() for css in rules)
    ),
    panel
).display()
```

## Lay out several calculation panels

```python
from McUtils.Jupyter import JHTML

cards = [JHTML.Bootstrap.Card(f"Energy: {energy:.4f} Eh", header=name)
         for name, energy in [("HF", -75.98), ("MP2", -76.23), ("CCSD(T)", -76.24)]]
columns = [JHTML.Bootstrap.Col(card, width=4) for card in cards]
JHTML.Bootstrap.Row(*columns).display()
```

## Embed an X3D scene

```python
from McUtils.Jupyter import JHTML
from McUtils.Plots import Graphics3D, Sphere

figure = Graphics3D(backend="x3d")
Sphere([0, 0, 0], .5, color="red").plot(figure)
Sphere([1, 0, 0], .3, color="white").plot(figure)
scene = figure.to_widget()
JHTML.Div(scene, dynamic=False).display()
```
