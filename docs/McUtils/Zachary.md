# <a id="McUtils.Zachary">McUtils.Zachary</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/__init__.py#L1?message=Update%20Docs)]
</div>
    
Handles much of the "numerical math" stuff inside Mcutils which has made it balloon a little bit
Deals with anything tensor, Taylor expansion, or interpolation related

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[FiniteDifferenceFunction](Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceFunction.md)   
</div>
   <div class="col" markdown="1">
[FiniteDifferenceError](Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceError.md)   
</div>
   <div class="col" markdown="1">
[finite_difference](Zachary/Taylor/FiniteDifferenceFunction/finite_difference.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[FiniteDifference1D](Zachary/Taylor/FiniteDifferenceFunction/FiniteDifference1D.md)   
</div>
   <div class="col" markdown="1">
[RegularGridFiniteDifference](Zachary/Taylor/FiniteDifferenceFunction/RegularGridFiniteDifference.md)   
</div>
   <div class="col" markdown="1">
[IrregularGridFiniteDifference](Zachary/Taylor/FiniteDifferenceFunction/IrregularGridFiniteDifference.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[FiniteDifferenceData](Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceData.md)   
</div>
   <div class="col" markdown="1">
[FiniteDifferenceMatrix](Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md)   
</div>
   <div class="col" markdown="1">
[FunctionExpansion](Zachary/Taylor/FunctionExpansions/FunctionExpansion.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[FiniteDifferenceDerivative](Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.md)   
</div>
   <div class="col" markdown="1">
[Mesh](Zachary/Mesh/Mesh.md)   
</div>
   <div class="col" markdown="1">
[MeshType](Zachary/Mesh/MeshType.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[BaseSurface](Zachary/Surfaces/BaseSurface/BaseSurface.md)   
</div>
   <div class="col" markdown="1">
[TaylorSeriesSurface](Zachary/Surfaces/BaseSurface/TaylorSeriesSurface.md)   
</div>
   <div class="col" markdown="1">
[LinearExpansionSurface](Zachary/Surfaces/BaseSurface/LinearExpansionSurface.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[LinearFitSurface](Zachary/Surfaces/BaseSurface/LinearFitSurface.md)   
</div>
   <div class="col" markdown="1">
[InterpolatedSurface](Zachary/Surfaces/BaseSurface/InterpolatedSurface.md)   
</div>
   <div class="col" markdown="1">
[Surface](Zachary/Surfaces/Surface/Surface.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[MultiSurface](Zachary/Surfaces/Surface/MultiSurface.md)   
</div>
   <div class="col" markdown="1">
[FittableModel](Zachary/FittableModels/FittableModel.md)   
</div>
   <div class="col" markdown="1">
[LinearFittableModel](Zachary/FittableModels/LinearFittableModel.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[LinearFitBasis](Zachary/FittableModels/LinearFitBasis.md)   
</div>
   <div class="col" markdown="1">
[Interpolator](Zachary/Interpolator/Interpolator.md)   
</div>
   <div class="col" markdown="1">
[Extrapolator](Zachary/Interpolator/Extrapolator.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[RBFDInterpolator](Zachary/NeighborBasedInterpolators/RBFDInterpolator.md)   
</div>
   <div class="col" markdown="1">
[InverseDistanceWeightedInterpolator](Zachary/NeighborBasedInterpolators/InverseDistanceWeightedInterpolator.md)   
</div>
   <div class="col" markdown="1">
[ProductGridInterpolator](Zachary/Interpolator/ProductGridInterpolator.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[UnstructuredGridInterpolator](Zachary/Interpolator/UnstructuredGridInterpolator.md)   
</div>
   <div class="col" markdown="1">
[Tensor](Zachary/LazyTensors/Tensor.md)   
</div>
   <div class="col" markdown="1">
[TensorOp](Zachary/LazyTensors/TensorOp.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[LazyOperatorTensor](Zachary/LazyTensors/LazyOperatorTensor.md)   
</div>
   <div class="col" markdown="1">
[SparseTensor](Zachary/LazyTensors/SparseTensor.md)   
</div>
   <div class="col" markdown="1">
[TensorDerivativeConverter](Zachary/Symbolic/TensorExpressions/TensorDerivativeConverter.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[TensorExpansionTerms](Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.md)   
</div>
   <div class="col" markdown="1">
[TensorExpression](Zachary/Symbolic/TensorExpressions/TensorExpression.md)   
</div>
   <div class="col" markdown="1">
[Symbols](Zachary/Symbolic/ElementaryFunctions/Symbols.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[SymPyFunction](Zachary/Symbolic/ElementaryFunctions/SymPyFunction.md)   
</div>
   <div class="col" markdown="1">
[AbstractPolynomial](Zachary/Polynomials/AbstractPolynomial.md)   
</div>
   <div class="col" markdown="1">
[DensePolynomial](Zachary/Polynomials/DensePolynomial.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[SparsePolynomial](Zachary/Polynomials/SparsePolynomial.md)   
</div>
   <div class="col" markdown="1">
[PureMonicPolynomial](Zachary/Polynomials/PureMonicPolynomial.md)   
</div>
   <div class="col" markdown="1">
[TensorCoefficientPoly](Zachary/Polynomials/TensorCoefficientPoly.md)   
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





## Examples

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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Zachary.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Zachary.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Zachary.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Zachary.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/__init__.py#L1?message=Update%20Docs)   
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