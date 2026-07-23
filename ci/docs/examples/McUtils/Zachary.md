
1D finite difference derivative via [finite_difference](Zachary/FiniteDifferenceFunction/finite_difference.md):

<div class="card in-out-block" markdown="1">

```python
from McUtils.Zachary import finite_difference
import numpy as np

sin_grid = np.linspace(0, 2*np.pi, 200)
sin_vals = np.sin(sin_grid)

deriv = finite_difference(sin_grid, sin_vals, 3) # 3rd deriv
base = Plot(sin_grid, deriv, aspect_ratio = .6, image_size=500)
Plot(sin_grid, np.sin(sin_grid), figure=base)
```
<div class="card-body out-block" markdown="1">

![plot](../img/McUtils_Zachary_1.png)
</div>
</div>

2D finite difference derivative via [finite_difference](Zachary/FiniteDifferenceFunction/finite_difference.md):

<div class="card in-out-block" markdown="1">

```python
from McUtils.Zachary import finite_difference
import numpy as np

x_grid = np.linspace(0, 2*np.pi, 200)
y_grid = np.linspace(0, 2*np.pi, 100)
sin_x_vals = np.sin(x_grid); sin_y_vals =  np.sin(y_grid)
vals_2D = np.outer(sin_x_vals, sin_y_vals)
grid_2D = np.array(np.meshgrid(x_grid, y_grid)).T

deriv = finite_difference(grid_2D, vals_2D, (1, 3))
TensorPlot(np.array([vals_2D, deriv]), image_size=500)
```

<div class="card-body out-block" markdown="1">

![plot](../img/McUtils_Zachary_2.png)
</div>
</div>

Create a convenient, low-order expansion of a (potentially expensive) function 

<div class="card in-out-block" markdown="1">

```python
def sin_xy(pt):
    ax = -1 if pt.ndim>1 else 0
    return np.prod(np.sin(pt), axis=ax)

point = np.array([.5, .5])
# create the function expansions
exp1 = FunctionExpansion.expand_function(sin_xy, point, function_shape=((2,), 0), order=1, stencil=5)
exp2 = FunctionExpansion.expand_function(sin_xy, point, function_shape=((2,), 0), order=2, stencil=6)
exp4 = FunctionExpansion.expand_function(sin_xy, point, function_shape=((2,), 0), order=4, stencil=6)

# create a test grid and plot the approximations
test_grid = np.vstack([np.linspace(-.5, .5, 100), np.zeros((100,))]).T + point[np.newaxis]
g = test_grid[:, 0]
gg = GraphicsGrid(nrows=1, ncols=3, subimage_size=350)
for i, e in zip(range(3), (exp1, exp2, exp4)):
    # plot the real answer
    gg[0, i] = Plot(g, sin_xy(test_grid), figure=gg[0, i])
    # plot the expansion
    gg[0, i] = Plot(g, e(test_grid), figure=gg[0, i])
```

<div class="card-body out-block" markdown="1">

![plot](../img/McUtils_Zachary_3.png)
</div>
</div>

expansions work in multiple dimensions, too

<div class="card in-out-block" markdown="1">

```python
mesh = np.meshgrid(np.linspace(.4, .6, 100, dtype='float128'), np.linspace(.4, .6, 100, dtype='float128'))
grid = np.array(mesh).T
gg2 = GraphicsGrid(nrows=2, ncols=3, subimage_size=350)
# plot error in linear expansion
styles = dict(ticks_style=(False, False), plot_style={'vmin': np.min(sin_xy(grid)), 'vmax': np.max(sin_xy(grid))})
gg2[0, 0] = ContourPlot(*mesh, sin_xy(grid), figure=gg2[0, 0], **styles)
gg2[0, 1] = ContourPlot(*mesh, exp1(grid), figure=gg2[0, 1], **styles)
# when we plot the error, we shift it so that it's centered around the average function value to show the scale
# of the error
gg2[0, 2] = ContourPlot(*mesh,
                        np.marginalize_out([np.min(sin_xy(grid)), np.max(sin_xy(grid))]) + sin_xy(grid) - exp1(grid),
                        figure=gg2[0, 2], **styles)
# plot error in quadratic expansion
gg2[1, 0] = ContourPlot(*mesh, sin_xy(grid), figure=gg2[1, 0], **styles)
gg2[1, 1] = ContourPlot(*mesh, exp2(grid), figure=gg2[1, 1], **styles)
gg2[1, 2] = ContourPlot(*mesh,
                        np.marginalize_out([np.min(sin_xy(grid)), np.max(sin_xy(grid))]) + sin_xy(grid) - exp2(grid),
                        figure=gg2[1, 2], **styles)
```
<div class="card-body out-block" markdown="1">

![plot](../img/McUtils_Zachary_4.png)
</div>
</div>

**LLM Examples**

These examples cover finite differences, interpolation, symbolic tensor derivatives, and molecular surfaces.

### Differentiate a two-dimensional potential

```python
import numpy as np
from McUtils.Zachary import FiniteDifferenceDerivative

def potential(q):
    x, y = q[..., 0], q[..., 1]
    return x**2 + x * y + 2 * y**2

derivs = FiniteDifferenceDerivative(potential, function_shape=((2,), ()), stencil=7)(
    np.array([1., -1.]), 
    mesh_spacing=.002
)
gradient, hessian = derivs.derivative_tensor([1, 2])
assert np.allclose(gradient, [1., -3.], atol=1e-7)
assert np.allclose(hessian, [[2., 1.], [1., 4.]], atol=1e-6)
```

### Interpolate a periodic torsional potential

```python
import numpy as np
from McUtils.Zachary import Interpolator

angles = np.linspace(-np.pi, np.pi, 25)
energies = 1.5 * (1 - np.cos(3 * angles))
potential = Interpolator(angles, energies, interpolation_order=3, periodic=True)
query = np.linspace(-np.pi, np.pi, 200)
interpolated = potential(query)
derivative = potential.derivative(1)(query)
assert interpolated.shape == query.shape
print("barrier:", interpolated.max(), "maximum slope:", np.abs(derivative).max())
```

### Construct a solvent-excluded surface

```python
import numpy as np
from McUtils.Data import UnitsData
from McUtils.Zachary import SphereUnionSurface

atoms = ["O", "H", "H"]
a2b = UnitsData.convert("Angstroms", "BohrRadius")
coords = np.array([[0, 0, 0], [.958, 0, 0], [-.240, .927, 0]]) * a2b
surface = SphereUnionSurface.from_xyz(atoms, coords, samples=250)
mesh = surface.get_triangulation(method="isosurface", probe_type="ses",
                                 probe_radius=1.4 * a2b, grid_samples=48)
print("SES area / Å²:", mesh.surface_area() / a2b**2)
mesh.plot(vertex_values=mesh.verts[:, 2], distance_units="Angstroms").show()
```

### Compose a two-mode analytic potential

`DifferentiableFunction` objects support arithmetic composition while retaining analytic
derivatives. Here two Morse oscillators act on different coordinates and are coupled by
a product term.

```python
import numpy as np
from McUtils.Zachary import MorseFunction

stretch_x = MorseFunction(de=12.0, a=1.4, re=1.0, inds=[0])
stretch_y = MorseFunction(de=8.0, a=1.1, re=1.5, inds=[1])
potential = stretch_x + stretch_y + 0.05 * stretch_x * stretch_y

points = np.array([[1.0, 1.5], [1.1, 1.7], [0.9, 1.3]])
energy, gradient, hessian = potential(points, order=2)
print("energies:", energy)
print("stationary-point gradient:", gradient[0])
print("Hessian shape:", hessian.shape)
```

### Differentiate a molecular stretch–bend potential

`CoordinateFunction` combines the differentiable-expression framework with internal
coordinate conversions. Its chain-rule machinery maps the resulting gradient and
Hessian back onto the Cartesian atom coordinates.

```python
import numpy as np
from McUtils.Zachary import CoordinateFunction

water = np.array([[0., 0., 0.], [1.81, 0., 0.], [-.45, 1.75, 0.]])
oh1 = CoordinateFunction.morse((0, 1), re=1.81, a=1.2, de=.20)
oh2 = CoordinateFunction.morse((0, 2), re=1.81, a=1.2, de=.20)
bend = CoordinateFunction.polynomial(
    (1, 0, 2), coeffs=[0., .04], center=1.824, ref=0.
)
internal, (energy, gradient, hessian) = (oh1 + oh2 + bend)(water, order=2)
print("internal coordinates:", internal[0])
print("energy:", energy, "|gradient|:", np.linalg.norm(gradient))
print("Cartesian Hessian:", hessian.shape)
```

### Interpolate a Cartesian reaction path

```python
import numpy as np
from McUtils.Zachary import CoordinateInterpolator

start = np.array([[0, 0, 0], [1.0, 0, 0], [0, 1.0, 0]])
finish = np.array([[0, 0, 0], [1.2, 0, 0], [0, .8, .4]])
path = CoordinateInterpolator(np.stack([start, finish]))
images = path(np.linspace(0, 1, 9))
print("reaction-path images:", images.shape)
```


### Evaluate a symbolic tensor norm and Hessian

```python
import numpy as np
from McUtils.Zachary import TensorExpression

q = TensorExpression.CoordinateVector(3, name="q")
norm = TensorExpression.VectorNormTerm(q)
point = np.array([1., 2., 2.])
value = TensorExpression(norm, q=point).eval()
hessian = TensorExpression(norm.dQ().dQ(), q=point).eval()
print("norm:", value, "Hessian eigenvalues:", np.linalg.eigvalsh(hessian))
```

### Differentiable Function Workflow

```python
import numpy as np
from McUtils.Zachary import CoordinateFunction, finite_difference
from McUtils.Plots import GraphicsGrid, Plot

potential = (
    CoordinateFunction.morse((0, 1), re=1.8, a=1.1, de=10.0)
    + CoordinateFunction.morse((0, 2), re=1.8, a=1.1, de=10.0)
    + 0.2 * CoordinateFunction.cos((1, 0, 2), n=2)
)

r = np.linspace(1.45, 2.25, 121)
geoms = np.zeros((len(r), 3, 3))
geoms[:, 1, 0] = r
geoms[:, 2] = [1.8 * np.cos(1.9), 1.8 * np.sin(1.9), 0.0]
internal_coords, expansion = potential(geoms, reexpress=False, order=2)
energy = expansion[0]
fd_curvature = finite_difference(r, energy, 2, stencil=7)

grid = GraphicsGrid(nrows=1, ncols=2, spacings=[5, 0], padding=50)
grid[0, 0] = Plot(r, energy, figure=grid[0, 0], plot_label="V(r)")
grid[0, 1] = Plot(r, fd_curvature, figure=grid[0, 1], plot_label="d²V/dr²")
grid.show()
```

### Solvent Accessible Surface Areas and Volumes

```python
import numpy as np
from McUtils.ExternalPrograms import RDMolecule
from McUtils.Zachary import SphereUnionSurface

mol = RDMolecule.from_smiles('O=C(O)C(c1ccccc1)')
atoms = mol.atoms
coords = mol.coords
surface = SphereUnionSurface.from_xyz(
    atoms, coords, radius_property="VanDerWaalsRadius",
    distance_units="Angstroms", samples=300
)

mesh = surface.get_triangulation(
    method='isosurface',
    probe_radius=1.4, probe_type="sas", 
    grid_samples=20
)
print("sampled SAS area:", surface.surface_area(method="sampling"))
print("triangulated area:", mesh.surface_area())
print("enclosed volume:", mesh.volume())

fig = surface.plot(points=surface.sampling_points, plot_intersections=True)
mesh.plot(figure=fig, transparency=0.35)
fig.show()
```