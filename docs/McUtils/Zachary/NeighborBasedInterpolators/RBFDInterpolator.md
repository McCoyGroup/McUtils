## <a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator">RBFDInterpolator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators.py#L1297)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators.py#L1297?message=Update%20Docs)]
</div>

Provides a flexible RBF interpolator that also allows
for matching function derivatives







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
wendland_coefficient_cache: dict
poly_origin: float
InterpolationData: InterpolationData
Interpolator: Interpolator
```
<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, pts, values, *derivatives, kernel: Union[<built-in function callable>, dict] = 'thin_plate_spline', kernel_options=None, auxiliary_basis=None, auxiliary_basis_options=None, extra_degree=0, clustering_radius=None, monomial_basis=True, multicenter_monomials=True, neighborhood_size=15, neighborhood_merge_threshold=None, neighborhood_max_merge_size=100, neighborhood_clustering_radius=None, solve_method='svd', max_condition_number=inf, error_threshold=0.01, bad_interpolation_retries=3, coordinate_transform=None, logger=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators.py#L1303)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators.py#L1303?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a radial-basis-function interpolator that fits both values and
derivatives, with a chosen kernel and an auxiliary polynomial basis.
  - `pts`: `np.ndarray`
    > the sample points
  - `values`: `np.ndarray`
    > the values
  - `derivatives`: `Any`
    > optional per-order derivative data
  - `kernel`: `str | Callable | dict`
    > the RBF kernel (name, callable, or spec dict)
  - `kernel_options`: `dict | None`
    > extra options bound into the kernel
  - `auxiliary_basis`: `Any`
    > the auxiliary polynomial basis (name/callable/spec)
  - `auxiliary_basis_options`: `dict | None`
    > extra options for the auxiliary basis
  - `extra_degree`: `int`
    > extra polynomial degree beyond the minimum
  - `clustering_radius`: `float | None`
    > declustering radius for the sample points
  - `monomial_basis`: `bool`
    > use a monomial (vs full outer-power) polynomial basis
  - `multicenter_monomials`: `bool`
    > center the monomials on each RBF center
  - `neighborhood_size`: `int`
    > neighbors per interpolation
  - `neighborhood_merge_threshold`: `int | None`
    > group-merge threshold
  - `neighborhood_max_merge_size`: `int`
    > max merged group size
  - `neighborhood_clustering_radius`: `float | None`
    > within-neighborhood declustering radius
  - `solve_method`: `str`
    > the linear-solve method (e.g. `'svd'`)
  - `max_condition_number`: `Any`
    > condition-number cap (currently unused)
  - `error_threshold`: `float`
    > the interpolation-error rejection threshold
  - `bad_interpolation_retries`: `int`
    > retries on a failed interpolation
  - `coordinate_transform`: `Any`
    > an optional coordinate transform
  - `logger`: `Any`
    > a logger


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.gaussian" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
gaussian(r, e=1, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1466)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1466?message=Update%20Docs)]
</div>
**LLM Docstring**

The Gaussian radial basis kernel `exp(-(e r)^2)` at radius `r`.
  - `r`: `np.ndarray`
    > the radius
  - `e`: `Any`
    > the shape parameter
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `np.ndarray`
    > the kernel values


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.gaussian_derivative" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
gaussian_derivative(n: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1484)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1484?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a function computing the `n`-th radial derivative of the Gaussian kernel.
  - `n`: `int`
    > the derivative order
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `Callable`
    > the `n`-th derivative function


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.gaussian_singularity_handler" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
gaussian_singularity_handler(n: int, ndim: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1517)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1517?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
of the Gaussian kernel in `ndim` dimensions.
  - `n`: `int`
    > the derivative order
  - `ndim`: `int`
    > the spatial dimension
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `Callable`
    > the singularity-handling function


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.thin_plate_spline" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
thin_plate_spline(r, o=3, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1569)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1569?message=Update%20Docs)]
</div>
**LLM Docstring**

The thin-plate-spline radial basis kernel (`r^o log r` family) at radius `r`.
  - `r`: `np.ndarray`
    > the radius
  - `o`: `int`
    > the spline order
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `np.ndarray`
    > the kernel values


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.thin_plate_spline_derivative" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
thin_plate_spline_derivative(n: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1586)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1586?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a function computing the `n`-th radial derivative of the thin-plate-spline kernel.
  - `n`: `int`
    > the derivative order
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `Callable`
    > the `n`-th derivative function


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.thin_plate_spline_singularity_handler" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
thin_plate_spline_singularity_handler(n: int, ndim: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1623)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1623?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
of the thin-plate-spline kernel in `ndim` dimensions.
  - `n`: `int`
    > the derivative order
  - `ndim`: `int`
    > the spatial dimension
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `Callable`
    > the singularity-handling function


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.wendland_coefficient" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
wendland_coefficient(cls, l, j, k): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1658)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1658?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute a coefficient of the Wendland polynomial (from its closed-form
recurrence).
  - `l`: `int`
    > the polynomial parameter (from the dimension/smoothness)
  - `j`: `int`
    > the coefficient index
  - `k`: `int`
    > the smoothness order
  - `:returns`: `float`
    > the coefficient


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.wendland_polynomial" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
wendland_polynomial(cls, r, d=None, k=3, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1695)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1695?message=Update%20Docs)]
</div>
**LLM Docstring**

The compactly-supported Wendland radial basis polynomial of smoothness `k` at
radius `r`.
  - `r`: `np.ndarray`
    > the radius
  - `d`: `int | None`
    > the spatial dimension (sets the polynomial degree)
  - `k`: `int`
    > the smoothness order
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `np.ndarray`
    > the kernel values


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.wendland_polynomial_derivative" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
wendland_polynomial_derivative(cls, n: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1724)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1724?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a function computing the `n`-th radial derivative of the Wendland kernel.
  - `n`: `int`
    > the derivative order
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `Callable`
    > the `n`-th derivative function


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.wendland_polynomial_singularity_handler" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
wendland_polynomial_singularity_handler(n: int, ndim: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1759)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1759?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
of the Wendland kernel in `ndim` dimensions.
  - `n`: `int`
    > the derivative order
  - `ndim`: `int`
    > the spatial dimension
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `Callable`
    > the singularity-handling function


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.zeros" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
zeros(r, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1793)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1793?message=Update%20Docs)]
</div>
**LLM Docstring**

The zero kernel (returns all zeros); used to disable the RBF contribution.
  - `r`: `np.ndarray`
    > the radius
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `np.ndarray`
    > an array of zeros


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.zeros_derivative" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
zeros_derivative(n: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1808)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1808?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a function computing the `n`-th radial derivative of the zero kernel.
  - `n`: `int`
    > the derivative order
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `Callable`
    > the `n`-th derivative function


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.zeros_singularity_handler" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
zeros_singularity_handler(n: int, ndim: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1835)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1835?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
of the zero kernel in `ndim` dimensions.
  - `n`: `int`
    > the derivative order
  - `ndim`: `int`
    > the spatial dimension
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `Callable`
    > the singularity-handling function


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.default_kernels" class="docs-object-method">&nbsp;</a> 
```python
@property
default_kernels(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L1867)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L1867?message=Update%20Docs)]
</div>
**LLM Docstring**

The registry mapping kernel names to their `{function, derivatives, zero_handler}`
specs.
  - `:returns`: `dict`
    > the kernel registry


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.morse" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
morse(r, a=1, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1904)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1904?message=Update%20Docs)]
</div>
**LLM Docstring**

A Morse-type radial basis kernel at radius `r`.
  - `r`: `np.ndarray`
    > the radius
  - `a`: `Any`
    > the range parameter
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `np.ndarray`
    > the kernel values


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.morse_derivative" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
morse_derivative(n: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1923)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1923?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a function computing the `n`-th radial derivative of the Morse kernel.
  - `n`: `int`
    > the derivative order
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `Callable`
    > the `n`-th derivative function


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.even_powers" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
even_powers(r, o=1, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1956)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1956?message=Update%20Docs)]
</div>
**LLM Docstring**

An even-power radial basis kernel (`r^(2o)` family) at radius `r`.
  - `r`: `np.ndarray`
    > the radius
  - `o`: `int`
    > the power order
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `np.ndarray`
    > the kernel values


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.even_powers_deriv" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
even_powers_deriv(n: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1973)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1973?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a function computing the `n`-th radial derivative of the even-power kernel.
  - `n`: `int`
    > the derivative order
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `Callable`
    > the `n`-th derivative function


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.laguerre" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
laguerre(r, k=3, shift=2.29428, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L2005)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L2005?message=Update%20Docs)]
</div>
**LLM Docstring**

A Laguerre-Gaussian radial basis kernel at radius `r`.
  - `r`: `np.ndarray`
    > the radius
  - `k`: `int`
    > the Laguerre order
  - `shift`: `Any`
    > the argument shift
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `np.ndarray`
    > the kernel values


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.laguerre_deriv" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
laguerre_deriv(n: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L2023)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L2023?message=Update%20Docs)]
</div>
(-1)^n LaguerreL[k - n, n, x]


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.compact_laguerre" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
compact_laguerre(cls, r, e=1, k=3, shift=2.29428, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2041)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2041?message=Update%20Docs)]
</div>
**LLM Docstring**

A compactly-supported Laguerre radial basis kernel at radius `r`.
  - `r`: `np.ndarray`
    > the radius
  - `e`: `Any`
    > the shape/support parameter
  - `k`: `int`
    > the Laguerre order
  - `shift`: `Any`
    > the argument shift
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `np.ndarray`
    > the kernel values


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.compact_laguerre_deriv" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
compact_laguerre_deriv(cls, n: int, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2060)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2060?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a function computing the `n`-th radial derivative of the compact-Laguerre kernel.
  - `n`: `int`
    > the derivative order
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `Callable`
    > the `n`-th derivative function


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.default_auxiliary_bases" class="docs-object-method">&nbsp;</a> 
```python
@property
default_auxiliary_bases(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2101?message=Update%20Docs)]
</div>
**LLM Docstring**

The registry mapping auxiliary-basis names to their `{function, derivatives}`
specs.
  - `:returns`: `dict`
    > the auxiliary-basis registry


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.evaluate_poly_matrix" class="docs-object-method">&nbsp;</a> 
```python
evaluate_poly_matrix(self, pts, degree, deriv_order=0, poly_origin=0.5, include_constant_term=True, monomials=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2172)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2172?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the auxiliary polynomial basis (and its derivatives) at a set of points
relative to a polynomial origin, returning the polynomial block of the
interpolation matrix.
  - `pts`: `np.ndarray`
    > the evaluation points
  - `degree`: `int`
    > the polynomial degree
  - `deriv_order`: `int`
    > the highest derivative order
  - `poly_origin`: `Any`
    > the origin the polynomials are centered on
  - `include_constant_term`: `bool`
    > include the constant term
  - `monomials`: `bool`
    > use a monomial basis
  - `:returns`: `np.ndarray`
    > the polynomial matrix block


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.evaluate_rbf_matrix" class="docs-object-method">&nbsp;</a> 
```python
evaluate_rbf_matrix(self, pts, centers, inds, deriv_order=0, zero_tol=1e-08): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2335)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2335?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the RBF kernel (and its derivatives) between a set of points and the
centers, handling the `r = 0` singularities via the kernel's zero-handler,
returning the RBF block of the interpolation matrix.
  - `pts`: `np.ndarray`
    > the evaluation points
  - `centers`: `np.ndarray`
    > the RBF centers
  - `inds`: `np.ndarray`
    > the coordinate indices
  - `deriv_order`: `int`
    > the highest derivative order
  - `zero_tol`: `float`
    > the tolerance for treating a distance as zero
  - `:returns`: `np.ndarray`
    > the RBF matrix block


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.construct_matrix" class="docs-object-method">&nbsp;</a> 
```python
construct_matrix(self, pts, centers, inds, degree=0, deriv_order=0, zero_tol=1e-08, poly_origin=None, include_constant_term=True, force_square=False, monomials=True, multicentered_polys=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2422)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2422?message=Update%20Docs)]
</div>
**LLM Docstring**

Assemble the full interpolation matrix by concatenating the RBF block and the
auxiliary polynomial block, optionally padding to a square system.
  - `pts`: `np.ndarray`
    > the evaluation points
  - `centers`: `np.ndarray`
    > the RBF centers
  - `inds`: `np.ndarray`
    > the coordinate indices
  - `degree`: `int`
    > the polynomial degree
  - `deriv_order`: `int`
    > the highest derivative order
  - `zero_tol`: `float`
    > the zero-distance tolerance
  - `poly_origin`: `Any`
    > the polynomial origin (defaults to the class value)
  - `include_constant_term`: `bool`
    > include the polynomial constant term
  - `force_square`: `bool`
    > pad with extra polynomial rows to square the matrix
  - `monomials`: `bool`
    > use a monomial polynomial basis
  - `multicentered_polys`: `bool`
    > center the polynomials on each RBF center
  - `:returns`: `np.ndarray`
    > the interpolation matrix


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.svd_solve" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
svd_solve(a, b, svd_cutoff=1e-12): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L2487)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L2487?message=Update%20Docs)]
</div>
**LLM Docstring**

Solve a (possibly rank-deficient) linear system via a truncated SVD
pseudo-inverse.
  - `a`: `np.ndarray`
    > the system matrix
  - `b`: `np.ndarray`
    > the right-hand side
  - `svd_cutoff`: `float`
    > the singular-value truncation cutoff
  - `:returns`: `np.ndarray`
    > the solution


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.solve_system" class="docs-object-method">&nbsp;</a> 
```python
solve_system(self, centers, vals, derivs: list, inds, solver=None, return_data=False, error_threshold=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2508)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2508?message=Update%20Docs)]
</div>
**LLM Docstring**

Solve for the RBF-plus-polynomial interpolation weights that reproduce the values
and derivatives at the centers, choosing the polynomial degree needed to make the
system solvable.
  - `centers`: `np.ndarray`
    > the RBF centers
  - `vals`: `np.ndarray`
    > the values at the centers
  - `derivs`: `list`
    > the derivative data at the centers
  - `inds`: `np.ndarray`
    > the coordinate indices
  - `solver`: `Callable | None`
    > an explicit solver callable
  - `return_data`: `bool`
    > also return solver diagnostics
  - `error_threshold`: `float | None`
    > the error threshold for rejecting a fit
  - `:returns`: `tuple`
    > `(weights, degree, extra_shift, error)` (plus solver data if requested)


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.construct_evaluation_matrix" class="docs-object-method">&nbsp;</a> 
```python
construct_evaluation_matrix(self, pts, data, deriv_order=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2680)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2680?message=Update%20Docs)]
</div>

  - `pts`: `Any`
    > 
  - `data`: `Any`
    > 
  - `deriv_order`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.apply_interpolation" class="docs-object-method">&nbsp;</a> 
```python
apply_interpolation(self, pts, data, inds, reshape_derivatives=True, return_data=False, deriv_order=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2701)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2701?message=Update%20Docs)]
</div>

  - `pts`: `Any`
    > 
  - `data`: `Any`
    > 
  - `deriv_order`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.NeighborBasedInterpolators.RBFDInterpolator.construct_interpolation" class="docs-object-method">&nbsp;</a> 
```python
construct_interpolation(self, inds, solver_data=False, return_error=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2747)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.py#L2747?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the RBF interpolation data for a neighborhood: renormalize it, solve for
the weights, and wrap the result as an `InterpolationData`.
  - `inds`: `np.ndarray`
    > the neighbor indices
  - `solver_data`: `bool`
    > also keep solver diagnostics
  - `return_error`: `bool`
    > also return the interpolation error
  - `:returns`: `RBFDInterpolator.InterpolationData`
    > the interpolation data
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/NeighborBasedInterpolators/RBFDInterpolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators.py#L1297?message=Update%20Docs)   
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