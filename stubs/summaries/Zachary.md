### `DifferentiableFunctions.py`
  - **class `DifferentiableFunction`**
    - `__init__(inds=None)`
    - `reindex(idx_perm)` — Return a copy of the function with its coordinate indices remapped under a
    - `get_consistent_inds(funcs)` — Compute the union of the coordinate indices used by a set of functions and
    - `evaluate(coords, order=0)` — Abstract: evaluate the function's expansion (value and derivatives) at the given
    - `get_children()` — Abstract: return the sub-functions this function is built from.
    - `flip()` — Return the reciprocal (`1 / self`) as a `ReciprocalFunction`.
  - **class `ConstantScaledFunction`** (DifferentiableFunction)
    - `__init__(func, scaling, inds=None)`
    - `evaluate(coords, order=0)` — Evaluate the wrapped function and scale every expansion term by the constant.
    - `get_children()` — Return the sub-functions of this scaled function.
  - **class `ConstantShiftedFunction`** (DifferentiableFunction)
    - `__init__(func, shift, inds=None)`
    - `evaluate(coords, order=0)` — Evaluate the wrapped function and add the constant to the zeroth-order (value)
    - `get_children()` — Return the sub-functions of this shifted function.
  - **class `NegatedFunction`** (DifferentiableFunction)
    - `__init__(func, inds=None)`
    - `evaluate(coords, order=0)` — Evaluate the wrapped function and negate every expansion term.
    - `get_children()` — Return the sub-functions of this negated function.
  - **class `FunctionSum`** (DifferentiableFunction)
    - `__init__(funcs, inds=None)`
    - `evaluate(coords, order=0)` — Evaluate each summand and add their expansions term by term.
    - `get_children()` — Return the sub-functions of this sum.
  - **class `FunctionProduct`** (DifferentiableFunction)
    - `__init__(funcs, inds=None)`
    - `evaluate(coords, order=0)` — Evaluate each factor and combine their expansions via the generalized product
    - `get_children()` — Return the sub-functions of this product.
  - **class `FunctionComposition`** (DifferentiableFunction)
    - `__init__(outer_func, inner_funcs, inds=None)`
    - `evaluate(coords, order=0)` — Evaluate the composition, combining the inner and outer expansions via the
    - `get_children()` — Return the sub-functions of this composition.
  - **class `ReciprocalFunction`** (DifferentiableFunction)
    - `__init__(func, inds=None)`
    - `evaluate(coords, order=0)` — Evaluate the wrapped function and form the expansion of its reciprocal.
    - `get_children()` — Return the sub-functions of this reciprocal.
  - **class `PolynomialFunction`** (DifferentiableFunction)
    - `__init__(taylor_poly, inds=None)`
    - `from_coefficients(coeffs, center=None, ref=0, inds=None)` — Build a polynomial function from a coefficient tensor, an expansion center, and a
    - `evaluate(coords, order=0)` — Evaluate the backing polynomial's expansion at the given coordinates.
    - `get_children()` — Return the sub-functions of this polynomial (a leaf).
  - **class `UnivariateFunction`** (DifferentiableFunction)
    - `__init__(term_generator, *, inds=None)`
    - `evaluate(coords, order=0)` — Evaluate the univariate function on the (single) coordinate, calling the term
  - **class `Poly1D`** (UnivariateFunction)
    - `__init__(coeffs, ref, center, inds=None)`
    - `fac_pow(k, n)` — Compute the falling-factorial coefficient `(k+1)(k+2)...(k+n)` arising when
    - `evaluate_term(r, order=0, previous_terms=None)` — Evaluate the `order`-th derivative of the polynomial at displacement `r - center`.
    - `get_children()` — Return the sub-functions of this polynomial (a leaf).
  - **class `MorseFunction`** (UnivariateFunction)
    - `__init__(*, de, a, re, inds=None)`
    - `from_anharmonicity(w, wx, g, re, inds=None)` — Build a Morse function from spectroscopic constants (harmonic frequency,
    - `evaluate_term(r, order=0, previous_terms=None)` — Evaluate the `order`-th derivative of the Morse potential at `r`.
    - `get_children()` — Return the sub-functions of this Morse function (a leaf).
  - **class `Sin`** (UnivariateFunction)
    - `__init__(*, n=1, l=1, inds=None)`
    - `evaluate_term(r, order=0, previous_terms=None)` — Evaluate the `order`-th derivative of the sine (using the phase-shift identity).
    - `get_children()` — Return the sub-functions of this sine (a leaf).
  - **class `Cos`** (UnivariateFunction)
    - `__init__(*, n=1, l=1, inds=None)`
    - `evaluate_term(r, order=0, previous_terms=None)` — Evaluate the `order`-th derivative of the cosine (using the phase-shift
    - `get_children()` — Return the sub-functions of this cosine (a leaf).
  - **class `Exp`** (UnivariateFunction)
    - `__init__(*, s=1, inds=None)`
    - `evaluate_term(r, order=0, previous_terms=None)` — Evaluate the `order`-th derivative of the exponential (`s^order exp(s r)`).
    - `get_children()` — Return the sub-functions of this exponential (a leaf).
  - **class `CoordinateFunction`**
    - `__init__(conversion, expr)`
    - `canonicalize_conversion(conv)` — Normalize a conversion specification into `(canonical_spec, conversion_function)`,
    - `merge_conversion_functions(conv_1, conv_2)` — Merge two coordinate-conversion specs into one, returning the reindexing that
    - `polynomial(coord_spec, *, coeffs, center, ref)` — Build a coordinate function from a polynomial expression in the given
    - `morse(coord, *, re, a=None, de=None, w=None, wx=None, g=None)` — Build a coordinate function from a Morse potential in the given coordinate,
    - `sin(coord, *, n=1, l=1)` — Build a coordinate function from a sine in the given coordinate.
    - `cos(coord, *, n=1, l=1)` — Build a coordinate function from a cosine in the given coordinate.
    - `exp(coord, *, s=1)` — Build a coordinate function from an exponential in the given coordinate.

### `FittableModels.py` — Defines classes for providing different approaches to fitting.
  - **class `FittedModel`**
    - `__init__(fit_basis, expansion_coeffs=None, basis_parameters=None, **kwargs)`
    - `canonicalize_basis(fit_basis, basis_parameters)`
    - `evaluate_kernel(fit_basis, basis_parameters, pts, coeffs=None, order=None, **opts)`
    - `get_kernel_and_opts(k)`
    - `parse_kernel_specs(kernels)`
    - `nonlinear_fit(kernel_specs, pts, observations, include_expansion_coefficients=True, **fit_params)`
    - `get_fit_methods()`
    - `get_fit_dispatch()`
    - `fit(kernels, pts, observations, method=None, **opts)`

### `Interpolator.py` — Sets up a general Interpolator class that looks like Mathematica's InterpolatingFunction class
  - **class `InterpolatorException`** (Exception)
  - **class `BasicInterpolator`**
    > Defines the abstract interface we'll need interpolator instances to satisfy so that we can use
    > `Interpolator` as a calling layer
    - `__init__(grid, values, **opts)`
    - `derivative(order)` — Constructs the derivatives of the interpolator at the given order
  - **class `ProductGridInterpolator`** (BasicInterpolator)
    > A set of interpolators that support interpolation
    > on a regular (tensor product) grid
    - `__init__(grids, vals, caller=None, order=None, extrapolate=True, periodic=False, boundary_conditions=None)`
    - `get_base_spline(grid, vals, order, periodic=False, boundary_conditions=None, extrapolate=False)` — Build a piecewise-polynomial (`PPoly`) spline of the given order along one grid
    - `construct_ndspline(grids, vals, order, extrapolate=True, periodic=False, boundary_conditions=None)` — Builds a tensor product ndspline by constructing a product of 1D splines
    - `handle_periodicity(coords)` — Wrap query coordinates into the base period of each periodic axis so they land
    - `derivative(order)` — :param order:
  - **class `UnstructuredGridInterpolator`** (BasicInterpolator)
    > Defines an interpolator appropriate for totally unstructured grids by
    > delegating to the scipy `RBF` interpolators
    - `__init__(grid, values, order=None, neighbors=None, extrapolate=True, **opts)`
    - `derivative(order)` — Constructs the derivatives of the interpolator at the given order
  - **class `ExtrapolatorType`** (enum.Enum)
  - **class `Interpolator`**
    > A general purpose that takes your data and just interpolates it without whining or making you do a pile of extra work
    - `__init__(grid, vals, interpolation_function=None, interpolation_order=None, extrapolator=None, extrapolation_order=None, **interpolation_opts)`
    - `get_interpolator(grid, vals, interpolation_order=None, allow_extrapolation=True, **opts)` — Returns a function that can be called on grid points to interpolate them
    - `get_extrapolator(grid, vals, extrapolation_order=1, **opts)` — Returns an Extrapolator that can be called on grid points to extrapolate them
    - `apply(grid_points, **opts)` — Interpolates then extrapolates the function at the grid_points
    - `derivative(order)` — Returns a new function representing the requested derivative
  - **class `Extrapolator`**
    > A general purpose that takes your data and just extrapolates it.
    > This currently only exists in template format.
    - `__init__(extrapolation_function, warning=False, **opts)`
    - `derivative(n)` — Return an extrapolator for the `n`-th derivative of the wrapped extrapolation
    - `find_extrapolated_points(gps, vals, extrap_value=np.nan)` — Currently super rough heuristics to determine at which points we need to extrapolate
    - `apply(gps, vals, extrap_value=np.nan)` — Replace the values at the extrapolated (out-of-range) grid points with values
  - **class `IncrementalCartesianCoordinateInterpolation`**
    - `__init__(abcissae, coords, *, coordinate_system, max_displacement_step=1.0, max_refinements=1, reembed=False, embedding_options=None)`
    - `wrap_convert(system)` — Build a converter callable that converts a coordinate set into the given
    - `prep_coordinate_system_converter(coordinate_system)` — Resolve a coordinate-system specification into a converter callable (defaulting
    - `refined_step_conv(pct, converter, init_abc, final_abc, init_coords, final_coords, init_internals, final_internals, max_refinements=None, max_disp=0.5, reembed=False, embedding_options=None)` — Interpolate a fraction `pct` of the way between two frames in the internal
    - `prep_cartesians(coords)` — Coerce a coordinate array into a list of `CoordinateSet` frames in the Cartesian
    - `incremental_interp(start, point)` — Interpolate a single point lying in the interval starting at frame `start`,
    - `interpolate(point)` — Interpolate the Cartesian geometry at each requested abcissa (sorting the
  - **class `CoordinateInterpolator`**
    - `__init__(coordinates, arc_lengths=None, distance_function=None, base_interpolator=None, coordinate_system=None, **interpolator_options)`
    - `euclidean_coordinate_distance(p1, p2)` — The Euclidean distance between two coordinate frames.
    - `lookup_distance_function(distance_function)` — Resolve a distance-function name to its implementation.
    - `uniform_distance_function(coords)` — Assign uniformly-spaced abcissae over `[0, 1]` regardless of the actual
    - `get_arc_lengths(coordinates, arc_lengths=None, distance_function=None)` — Compute the normalized (`[0, 1]`) arc-length abcissae for a path, either from an

### `LazyTensors.py` — LazyTensors provides a small framework for symbolically working with Tensors
  - **class `Tensor`**
    > A semi-symbolic representation of a tensor. Allows for lazy processing of tensor operations.
    - `__init__(a, shape=None)`
    - `from_array(a, shape=None)`
    - `array()`
    - `get_shape(a)`
    - `shape()`
    - `get_dim()`
    - `dim()`
    - `add(other, **kw)`
    - `mul(other, **kw)`
    - `dot(other, **kw)`
    - `transpose(axes, **kw)`
    - `pow(other, **kw)`
    - `handle_missing_indices(missing, extant)`
    - `pull_index(*idx)` — Defines custom logic for handling how we pull indices
  - **class `SparseTensor`** (Tensor)
    > Tensor class that uses SparseArray
    - `__init__(a, shape=None)`
    - `array()`
  - **class `TensorOp`** (Tensor)
    > A lazy representation of tensor operations to save memory
    - `__init__(a, b, axis=None)`
    - `op(a, b)`
    - `get_shape(a, b)`
    - `shape()`
    - `array()` — Ought to always compile down to a proper ndarray
  - **class `TensorPlus`** (TensorOp)
    > Represents an addition of two tensors
    - `op(a, b)`
    - `get_shape(a, b)`
  - **class `TensorPow`** (TensorOp)
    > Represents a power of a tensors
    - `op(a, b)`
    - `get_shape(a, b)`
  - **class `TensorMul`** (TensorOp)
    > Represents a multiplication of a tensor and a scalar
    - `op(a, b)`
    - `get_shape(a, b)`
  - **class `TensorTranspose`** (TensorOp)
    > Represents a tensor transposition
    - `get_shape(a, b)`
    - `op(a, b)`
  - **class `TensorDot`** (TensorOp)
    > Represents a tensor contraction
    - `get_shape(a, b)`
    - `op(a, b)`
  - **class `LazyOperatorTensor`** (Tensor)
    > A super-lazy tensor that represents the elements of an operator
    - `__init__(operator, shape, memoization=True, dtype=object, fill=None)`
    - `array()`

### `Mesh.py` — Represents an n-dimensional grid, used by Interpolator and (eventually) FiniteDifferenceFunction to…
  - **class `MeshType`** (enum.Enum)
  - **class `MeshError`** (Exception)
  - **class `Mesh`** (np.ndarray)
    > A general Mesh class representing data points in n-dimensions
    > in either a structured, unstructured, or semi-structured manner.
    > Exists mostly to provides a unified interface to difference FD and Surface methods.
    - `__init__(*args, **kwargs)`
    - `mesh_spacings()` — The per-axis grid spacings (computed and cached lazily).
    - `subgrids()` — The per-axis subgrids for a regular or structured mesh (or `None` for
    - `bounding_box()` — The `(min, max)` extent of the mesh along each coordinate.
    - `dimension()` — Returns the dimension of the grid (not necessarily ndim)
    - `npoints()` — Returns the number of gridpoints in the mesh
    - `gridpoints()` — Returns the flattened set of gridpoints for a structured tensor grid and otherwise just returns the…
    - `get_npoints(g)` — Returns the number of gridpoints in the grid
    - `get_gridpoints(g)` — Returns the gridpoints in the grid
    - `get_mesh_subgrids(grid, tol=None)` — Returns the subgrids for a mesh
    - `get_mesh_spacings(grid, tol=None)` — Compute the per-axis spacings of a grid as the unique rounded successive
    - `get_mesh_type(grid, check_product_grid=True, check_regular_grid=True, tol=None)` — Determines what kind of grid we're working with
    - `RegularMesh(*mesh_specs)` — Builds a grid from multiple linspace arguments,

### `NeighborBasedInterpolators.py` — Sets up a general Interpolator class that looks like Mathematica's InterpolatingFunction class
  - **class `NeighborBasedInterpolator`**
    > Useful base class for neighbor-based interpolation
    - `__init__(pts, values, *derivatives, clustering_radius=None, neighborhood_size=15, neighborhood_merge_threshold=None, neighborhood_max_merge_size=100, neighborhood_clustering_radius=None, coordinate_transform=None, bad_interpolation_retries=2, logger=None)`
    - `decluster_data(pts, vals, derivs, radius, return_mask=False)` — Decluster the sample points (and their values/derivatives) by dropping points
    - **class `RescalingData`**
      - `initialize_subgrid_data(pts, values, derivatives)` — Renormalize a neighborhood's points, values, and derivatives to `[0, 1]`-ish
      - `renormalize_grid(pts)` — Rescale each grid coordinate to `[0, 1]`, returning the rescaled grid and the
      - `renormalize_values(values)` — Rescale values to `[0, 1]`, returning the rescaled values and the shift and
      - `renormalize_derivs(derivs, vals_scaling, grid_scaling)` — Rescale derivative tensors consistently with the value and grid rescalings, and
      - `apply_renormalization(pts)` — Apply the stored grid renormalization (shift and scale) to a set of points.
      - `reverse_renormalization(pts)` — Undo the grid renormalization, mapping renormalized points back to the original
      - `reverse_value_renormalization(vs)` — Undo the value renormalization, mapping renormalized values back to the original
      - `reverse_derivative_renormalization(derivs, reshape=True)` — Undo the derivative renormalization, optionally re-expanding the reduced
    - `triu_inds(ndim, rank)` — Return the upper-triangular (unique) index tuples for a symmetric rank-`rank`
    - `triu_num(ndim, rank)` — Return the number of unique components of a symmetric rank-`rank` tensor in
    - `get_neighborhood(pts, *, neighbors, return_distances=False)` — Query the KD-tree for the nearest `neighbors` sample points to each query point.
    - `create_neighbor_groups(inds, merge_limit=None, max_merge_size=None)` — Group query points that share (nearly) the same neighborhood so one interpolation
    - `prep_interpolation_data(inds)` — Gather and renormalize the grid points, values, and derivatives for a
    - `construct_interpolation(inds, solver_data=False, return_error=False)` — Abstract: build the interpolation data (e.g.
    - `apply_interpolation(pts, data, inds, deriv_order=0, reshape_derivatives=True, return_data=False)` — :param pts:
    - `prep_neighborhoods(pts, hoods, distances, neighbors, merge_neighbors=None, neighborhood_clustering_radius=None, min_distance=None, max_distance=None, use_natural_neighbors=None)` — Post-process raw neighborhoods before interpolation: optionally decluster within
    - `eval(pts, deriv_order=0, neighbors=None, merge_neighbors=None, reshape_derivatives=True, return_interpolation_data=False, check_in_sample=True, zero_tol=1e-08, return_error=False, use_cache=True, retries=None, max_distance=None, min_distance=None, neighborhood_clustering_radius=None, use_natural_neighbors=False, chunk_size=None)` — Evaluate the interpolant (and derivatives up to `deriv_order`) at a set of query
    - `resiliance_test(expansion, interpolation_data, mesh_spacing=0.01, tolerance=0.05)` — Stub: intended to check an interpolation's error against a Taylor expansion over a
    - `construct_function_expansion(inds)` — Build a `FunctionExpansion` centered on a neighborhood's points from the stored
    - `create_function_interpolation(pts, fn, *derivatives, derivative_order=None, function_shape=None, **opts)` — Build an interpolator by sampling a function (and, if needed, finite-differencing
    - `nearest_interpolation(pts, neighbors=None, solver_data=False, interpolator=True)` — :param pts:
    - **class `Interpolator`**
      - `__init__(data, inds, parent)`
    - `global_interpolator()` — An `Interpolator` built over the entire sample set (all points as one
  - **class `RBFDError`** (ValueError)
  - **class `RBFDInterpolator`** (NeighborBasedInterpolator)
    > Provides a flexible RBF interpolator that also allows
    > for matching function derivatives
    - `__init__(pts, values, *derivatives, kernel='thin_plate_spline', kernel_options=None, auxiliary_basis=None, auxiliary_basis_options=None, extra_degree=0, clustering_radius=None, monomial_basis=True, multicenter_monomials=True, neighborhood_size=15, neighborhood_merge_threshold=None, neighborhood_max_merge_size=100, neighborhood_clustering_radius=None, solve_method='svd', max_condition_number=np.inf, error_threshold=0.01, bad_interpolation_retries=3, coordinate_transform=None, logger=None)`
    - `gaussian(r, e=1, inds=None)` — The Gaussian radial basis kernel `exp(-(e r)^2)` at radius `r`.
    - `gaussian_derivative(n, inds=None)` — Return a function computing the `n`-th radial derivative of the Gaussian kernel.
    - `gaussian_singularity_handler(n, ndim, inds=None)` — Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
    - `thin_plate_spline(r, o=3, inds=None)` — The thin-plate-spline radial basis kernel (`r^o log r` family) at radius `r`.
    - `thin_plate_spline_derivative(n, inds=None)` — Return a function computing the `n`-th radial derivative of the thin-plate-spline kernel.
    - `thin_plate_spline_singularity_handler(n, ndim, inds=None)` — Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
    - `wendland_coefficient(l, j, k)` — Compute a coefficient of the Wendland polynomial (from its closed-form
    - `wendland_polynomial(r, d=None, k=3, inds=None)` — The compactly-supported Wendland radial basis polynomial of smoothness `k` at
    - `wendland_polynomial_derivative(n, inds=None)` — Return a function computing the `n`-th radial derivative of the Wendland kernel.
    - `wendland_polynomial_singularity_handler(n, ndim, inds=None)` — Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
    - `zeros(r, inds=None)` — The zero kernel (returns all zeros); used to disable the RBF contribution.
    - `zeros_derivative(n, inds=None)` — Return a function computing the `n`-th radial derivative of the zero kernel.
    - `zeros_singularity_handler(n, ndim, inds=None)` — Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
    - `default_kernels()` — The registry mapping kernel names to their `{function, derivatives, zero_handler}`
    - `morse(r, a=1, inds=None)` — A Morse-type radial basis kernel at radius `r`.
    - `morse_derivative(n, inds=None)` — Return a function computing the `n`-th radial derivative of the Morse kernel.
    - `even_powers(r, o=1, inds=None)` — An even-power radial basis kernel (`r^(2o)` family) at radius `r`.
    - `even_powers_deriv(n, inds=None)` — Return a function computing the `n`-th radial derivative of the even-power kernel.
    - `laguerre(r, k=3, shift=2.29428, inds=None)` — A Laguerre-Gaussian radial basis kernel at radius `r`.
    - `laguerre_deriv(n, inds=None)` — (-1)^n LaguerreL[k - n, n, x]
    - `compact_laguerre(r, e=1, k=3, shift=2.29428, inds=None)` — A compactly-supported Laguerre radial basis kernel at radius `r`.
    - `compact_laguerre_deriv(n, inds=None)` — Return a function computing the `n`-th radial derivative of the compact-Laguerre kernel.
    - `default_auxiliary_bases()` — The registry mapping auxiliary-basis names to their `{function, derivatives}`
    - `evaluate_poly_matrix(pts, degree, deriv_order=0, poly_origin=0.5, include_constant_term=True, monomials=True)` — Evaluate the auxiliary polynomial basis (and its derivatives) at a set of points
    - `evaluate_rbf_matrix(pts, centers, inds, deriv_order=0, zero_tol=1e-08)` — Evaluate the RBF kernel (and its derivatives) between a set of points and the
    - `construct_matrix(pts, centers, inds, degree=0, deriv_order=0, zero_tol=1e-08, poly_origin=None, include_constant_term=True, force_square=False, monomials=True, multicentered_polys=False)` — Assemble the full interpolation matrix by concatenating the RBF block and the
    - `svd_solve(a, b, svd_cutoff=1e-12)` — Solve a (possibly rank-deficient) linear system via a truncated SVD
    - `solve_system(centers, vals, derivs, inds, solver=None, return_data=False, error_threshold=None)` — Solve for the RBF-plus-polynomial interpolation weights that reproduce the values
    - **class `InterpolationData`**
      - `__init__(w, grid, degree, scaling_data, extra_shift=0, interpolation_error=0, solver_data=None)`
    - `construct_evaluation_matrix(pts, data, deriv_order=0)` — :param pts:
    - `apply_interpolation(pts, data, inds, reshape_derivatives=True, return_data=False, deriv_order=0)` — :param pts:
    - `construct_interpolation(inds, solver_data=False, return_error=False)` — Build the RBF interpolation data for a neighborhood: renormalize it, solve for
    - **class `Interpolator`** (NeighborBasedInterpolator.Interpolator)
      - `matrix(pts, deriv_order=0)` — Build the RBF evaluation matrix for this neighborhood at a set of points.
  - **class `DistanceWeightedInterpolator`** (NeighborBasedInterpolator)
    > Provides a quick implementation of inverse distance weighted interpolation
    - **class `InterpolationData`**
      - `__init__(grid)`
    - `construct_interpolation(inds, solver_data=False, return_error=False)` — Build the distance-weighted interpolation data for a neighborhood (just its
    - `apply_weights(weights, inds, deriv_order=0, reshape_derivatives=False)` — :param weights: npts x hood_size matrix of weights
    - `get_weights(pts, data, inds)` — Computes weights for pts from the inds
    - `apply_interpolation(pts, data, inds, deriv_order=0, reshape_derivatives=True, return_data=False)` — :param pts:
  - **class `InverseDistanceWeightedInterpolator`** (DistanceWeightedInterpolator)
    - `weight_deriv(disp, dists, norm, power, n, gammas_1=None)` — Compute the `n`-th-order contribution to the derivative of the inverse-distance
    - `idw_derivs(deriv_order, disp, dists, norm, power, weights)` — Compute the derivatives (up to `deriv_order`, currently ≤ 2) of the
    - `get_idw_weights(pts, dists, disps=None, deriv_order=None, zero_tol=1e-06, power=2)` — Compute the normalized inverse-distance weights (and optionally their
    - `get_weights(pts, dists, inds, zero_tol=1e-06, power=2)` — Compute the inverse-distance weights for a set of query points.
    - `eval(pts, deriv_order=0, neighbors=None, merge_neighbors=None, reshape_derivatives=True, return_interpolation_data=False, check_in_sample=True, zero_tol=1e-08, return_error=False, use_cache=True, retries=None, max_distance=None, min_distance=None, neighborhood_clustering_radius=None, use_natural_neighbors=False, chunk_size=None, power=2, mode='fast')` — Evaluate the inverse-distance-weighted interpolant (and derivatives) at a set of

### `Polynomials.py`
  - **class `AbstractPolynomial`**
    > Provides the general interface an abstract polynomial needs ot support, including
    > multiplication, addition, shifting, access of coefficients, and evaluation
    - `scaling()` — Abstract: the overall scalar prefactor multiplying the polynomial.
    - `shift(shift)` — Abstract: return the polynomial shifted in its variables (i.e.
  - **class `DensePolynomial`** (AbstractPolynomial)
    > A straightforward dense n-dimensional polynomial data structure with
    > multiplications and shifts
    - `__init__(coeffs, prefactor=None, shift=None, stack_dim=0)`
    - `from_tensors(tensors, prefactor=None, shift=None, rescale=True)` — Build a `DensePolynomial` from a list of derivative/coefficient tensors (one per
    - `shape()` — The shape of the coefficient tensor (including the stack axes).
    - `scaling()` — The overall scalar prefactor (1 when unset).
    - `scaling(s)` — The overall scalar prefactor (1 when unset).
    - `coeffs()` — The materialized coefficient tensor, applying (and then clearing) any deferred
    - `coeffs(cs)` — The materialized coefficient tensor, applying (and then clearing) any deferred
    - `coordinate_dim()` — The number of polynomial variables (the coefficient rank minus the stack axes).
    - `shift(shift)` — Return the polynomial with an added deferred variable shift (`p(x + shift)`).
    - `compute_shifted_coeffs(poly_coeffs, shift, stack_dim=0)` — Compute the coefficient tensor of a polynomial after a variable shift
    - `fill_tensors(tensors, idx, value, stack_dim, pcache, permute, rescale)` — Scatter a single coefficient value into the per-order derivative tensors,
    - `extract_tensors(coeffs, stack_dim=None, permute=True, rescale=True, cutoff=1e-15)` — Decompose a coefficient tensor into a list of per-order (symmetric) derivative
    - `condense_tensors(tensors, rescale=True, allow_sparse=True)` — Collapse a list of per-order derivative tensors back into a single (dense or
    - `coefficient_tensors()` — The per-order (permutation-rescaled) derivative tensors of the polynomial,
    - `unscaled_coefficient_tensors()` — The per-order derivative tensors without permutation rescaling, computed lazily.
    - `transform(lin_transf)` — Applies (for now) a linear transformation to the polynomial
    - `outer(other)` — Form the outer-product polynomial of this one with another coefficient tensor
    - `deriv(coord)` — Differentiate the polynomial with respect to one coordinate.
    - `grad()` — Return the gradient polynomial, whose leading stack axis indexes the derivative
    - `clip(threshold=1e-15)` — Drop coefficients below a magnitude threshold, returning a trimmed polynomial
    - `make_sparse_backed(threshold=1e-15)` — Return an equivalent polynomial whose coefficients are stored as a `SparseArray`
  - **class `SparsePolynomial`** (AbstractPolynomial)
    > A semi-symbolic representation of a polynomial of tensor
    > coefficients
    - `__init__(terms, prefactor=1, ndim=None, canonicalize=True)`
    - `scaling()` — The overall scalar prefactor (1 when unset).
    - `scaling(s)` — The overall scalar prefactor (1 when unset).
    - `expand()` — Fold the prefactor into the term coefficients, returning an equivalent polynomial
    - `monomial(idx, value=1)` — Build a single-term polynomial for the monomial at the given index.
    - `shape()` — The dense coefficient shape implied by the terms (per-variable max power + 1),
    - `as_dense()` — Convert to an equivalent `DensePolynomial`, filling a dense coefficient tensor
    - `shift(shift)` — Return the polynomial shifted in its variables (`p(x + shift)`), expanding each
  - **class `PureMonicPolynomial`** (SparsePolynomial)
    - `__init__(terms, prefactor=1, canonicalize=True)`
    - `shape()` — Not supported: monic-monomial polynomials have no dense counterpart.
    - `as_dense()` — Not supported: monic-monomial polynomials have no dense counterpart.
    - `shift(shift)` — Not supported: monic-monomial polynomials have no dense counterpart.
    - `monomial(idx, value=1)` — Build a single-term polynomial for one monomial key.
    - `key_hash(monomial_tuple)` — Cheap order-independent hash of a monomial key (sum of the per-index hashes),
    - `canonical_key(monomial_tuple)` — Abstract: put a monomial key into canonical (sorted) form so equivalent keys
    - `direct_multiproduct(other, key_value_generator)` — Multiply with another monic polynomial using a generator that yields the
    - `direct_product(other, key_func=None, mul=None)` — Multiply with another monic polynomial (or scalar) using optional key-combining
    - `rebuild(new_terms, prefactor=None, canonicalize=None)` — Build a new polynomial of the same type from a term mapping, inheriting the
    - `filter(keys, mode='match')` — Filter the polynomial's terms by their monomial keys under one of three modes.
  - **class `TensorCoefficientPoly`** (PureMonicPolynomial)
    > Represents a polynomial constructed using tensor elements as monomials
    > by tracking sets of indices
    - `canonical_key(monomial_tuple)` — Canonicalize a monomial key of tensor-coefficient index tuples by grouping the

### `Surfaces/BaseSurface.py` — Provides an abstract base class off of which concrete surface implementations can be built
  - **class `BaseSurface`**
    > Surface base class which can be subclassed for relevant cases
    - `__init__(data, dimension)`
    - `evaluate(points, **kwargs)` — Evaluates the function at the points based off of "data"
    - `check_dimension(gridpoints, target=None, raise_exception=True)` — Check that a set of grid points matches the surface's expected dimension,
  - **class `TaylorSeriesSurface`** (BaseSurface)
    > A surface with an evaluator built off of a Taylor series expansion
    - `__init__(*derivs, dimension=None, **opts)`
    - `center()` — The expansion center of the underlying Taylor series.
    - `ref()` — The reference (constant) value of the underlying Taylor series.
    - `expansion_tensors()` — The derivative tensors of the underlying Taylor series.
    - `check_dimension(gridpoints, target=None, raise_exception=True)` — Check the grid-point dimension, additionally accepting either side of the
    - `evaluate(points, **kwargs)` — Since the Taylor expansion stuff is already built out this is super easy
  - **class `LinearExpansionSurface`** (BaseSurface)
    > A surface with an evaluator built off of an expansion in some user specified basis
    - `__init__(coefficients, basis=None, dimension=None)`
    - `evaluate(points, **kwargs)` — First we just apply the basis to the gridpoints, then we dot this into the coeffs
  - **class `LinearFitSurface`** (LinearExpansionSurface)
    > A surface built off of a LinearExpansionSurface, but done by fitting.
    > The basis selection
    - `__init__(points, basis=None, order=4, dimension=None)`
    - `evaluate(points, **kwargs)` — :param points:
    - `minimize(initial_guess=None, function_options=None, **opts)` — Minimize the fitted surface, defaulting the starting point to the lowest-valued
  - **class `InterpolatedSurface`** (BaseSurface)
    > A surface that operates by doing an interpolation of passed mesh data
    - `__init__(xdata, ydata=None, dimension=None, **opts)`
    - `evaluate(points, **kwargs)` — We delegate all the dirty work to the Interpolator so hopefully that's working...
    - `minimize(initial_guess=None, function_options=None, **opts)` — Minimize the interpolated surface, defaulting the starting point to the

### `Surfaces/MarchingCubesSurface.py`
- `marching_cubes(grid, isovalue, spacing=(1.0, 1.0, 1.0), origin=(0.0, 0.0, 0.0), transformation=None, return_surface=True, return_normals=True)` — Extract an isosurface from a scalar voxel grid.
- `compute_normals(vertices, triangles, grid, spacing=(1, 1, 1), origin=(0, 0, 0))` — Estimate smooth per-vertex normals by interpolating the grid gradient.

### `Surfaces/SphereUnionSurface.py`
- `halton_sphere(npts, **etc)` — Generate quasi-random points on the unit sphere from a 2-D Halton sequence.
- `sobol_sphere(npts, **etc)` — Generate quasi-random points on the unit sphere from a 2-D Sobol sequence.
- `sphere_points(npts, center=None, radius=None, method='fibonacci', **etc)` — Generate points on a sphere by the named method, optionally scaled to a radius
  - **class `SphereUnionSurface`**
    - `__init__(centers, radii, scaling=None, expansion=None, samples=None, density=None, tolerance=None, add_intersection_circles=False, **generator_options)`
    - `from_xyz(atoms, positions, scaling=None, expansion=None, samples=None, tolerance=None, radius_property='IconRadius', distance_units='BohrRadius')` — Build a `SphereUnionSurface` from atoms and positions, taking each sphere radius
    - `sampling_points()` — The (flattened) exterior sample points on the sphere union, generated lazily.
    - `sampling_points(pts)` — The (flattened) exterior sample points on the sphere union, generated lazily.
    - `atom_sampling_points()` — The per-sphere lists of exterior sample points, generated lazily.
    - `nearest_centers(pts, centers, return_normals=False)` — For each point, find the index of the nearest sphere center, optionally also
    - `sphere_project(pts, centers, radii)` — Project each point radially onto the surface of its nearest sphere.
    - `sphere_boundary_pruning(pts, centers, min_component=None)` — Prune points that sit too close to a neighbouring sphere's point group,
    - `point_cloud_repulsion(pts, centers, radii, min_displacement_cutoff=0.001, stochastic_factor=0.0001, force_constant=0.001, power=-3, max_iterations=15)` — Relax a point cloud on the sphere union by iterated inverse-power repulsion
    - `adjust_point_cloud_density(pts, centers=None, radii=None, min_component=None, min_component_bins=30, min_component_scaling=0.7, same_point_cutoff=1e-06, max_iterations=15)` — Even out a point cloud's density by iteratively merging pairs of points that are
    - `get_exterior_points(points, centers, radii, tolerance=0, vertex_map=None, intersection_point_mask=None, intersection_point_tolerance=None, return_components=False)` — Return a mask (or per-sphere components) of the points that lie outside (or on)
    - `get_interior_points(points, centers, radii, tolerance=0, return_components=False)` — Return a mask (or per-sphere components) of the points that lie inside (or on)
    - `get_surface_points(centers, radii, samples=50, density=None, scaling=1, point_generator=None, expansion=0, preserve_origins=False, circle_samples=None, min_circle_samples=0.1, add_intersection_circles=False, intersection_radius_scaling=1, intersection_boundary_clipping_threshold=None, return_intersection_point_mask=False, extend_intersection_points=True, intersection_point_tolerance=None, clear_circle_neighbors=None, neighborhood_tolerance='auto', tolerance=0, prune=True)` — Generate the exterior surface point cloud for a union of spheres: sample each
    - `generate_points(scaling=None, expansion=None, samples=None, density=None, preserve_origins=False, tolerance=None, prune=True, add_intersection_circles=None, **etc)` — Generate the exterior surface points for this surface, filling unset options
    - `generate_mesh(points=None, normals=None, scaling=None, expansion=None, samples=None, method='poisson', depth=5, **reconstruction_settings)` — Reconstruct a triangle mesh from the surface point cloud (currently via Open3D
    - `sphere_points(centers, radii, samples, generator=None, shells=None)` — Generate points on each of a (possibly batched) set of spheres, supporting a
    - `fibonacci_sphere(samples)` — Generate `samples` roughly-even points on the unit sphere via the Fibonacci
    - `get_bbox()` — Return the axis-aligned bounding box enclosing all of the spheres.
    - `signed_distance(inside_mask, spacing=1.0)` — Exact signed distance field from a binary mask.
    - `morphological_close_sdf(inside_mask, probe_radius, spacing=1.0)` — Fill concave crevices smaller than probe_radius via
    - `solvent_surface_distance(points, centers, radii, probe_radius=0, probe_type='sas', grid_spacing=None)` — Compute the signed distance from each point to the sphere-union surface, either
    - `get_surface_function(probe_radius=None, distance_function=None, probe_type='sas')` — Return a callable mapping points to a scalar field whose zero level set is the
    - `get_triangulation(occlusion_type='auto', deduplicate_points=None, point_gen_options=None, add_intersection_circles=True, extend_intersection_points=False, method=None, bbox_scaling=1.2, grid_samples=20, probe_radius=None, probe_type='sas', **surface_opts)` — Build a triangulated `SphereUnionSurfaceMesh` of the surface, either by hulling
    - `sampling_point_surface_area(centers, radii, points=None, exterior_test=None, point_generator=None, generator_args=None, center_surface_areas=None, **test_args)` — Estimate the exposed surface area of the sphere union by Monte-Carlo sampling:
    - `sampling_point_volume(centers, radii, points=None, interior_test=None, point_generator=None, generator_args=None, center_volumes=None, shells=50, **test_args)` — Estimate the union volume by Monte-Carlo sampling of interior shell points.
    - `random_sphere_sampling(center, radius, samples=500, seed=None, rng=None)` — Draw uniformly-distributed random points inside a sphere.
    - `volume_union_mc(centers, radii, n_samples=100000, seed=None)` — Estimate the union volume by Monte-Carlo sampling uniformly inside each sphere.
    - `volume_voxel(centers, radii, resolution=200)` — Estimate the union volume by voxelizing the bounding box and counting the voxels
    - `sphere_triple_intersection_area(a, b, c, r1, r2, r3)` — Analytic surface area of the triple overlap of three spheres, following Gibson &
    - `sphere_double_intersection_circle(centers, radii, dist=None)` — Compute the circle where two spheres intersect (its center, unit normal, and
    - `sphere_triple_intersection_point(centers, radii, dists=None)` — Compute the two points where three (assumed mutually intersecting) spheres meet,
    - `get_intersections(centers, radii)` — Find all pairwise intersection circles and all triple intersection points among
    - `sphere_double_intersection_area(a, r1, r2)` — Analytic exposed surface-area contribution of the overlap of two spheres, or a
    - `triangle_area(a, b, c)` — Heron's-formula area of a triangle with the given side lengths.
    - `sphere_quadruple_intersection_area(a, b, c, f, g, h, r1, r2, r3, r4, A123, A124, A134, A234, I4, I3, I2, I1)` — Analytic surface-area contribution of the quadruple overlap of four spheres,
    - `sphere_area(radii, axis=None)` — The total surface area of one or more spheres, `4 pi sum(r^2)`.
    - `sphere_union_surface_area(centers, radii, include_doubles=True, include_triples=None, include_quadruples=None, return_terms=False, overlap_tolerance=0)` — Compute the exact exposed surface area of a union of spheres via
    - `surface_area(method='union', **opts)` — Compute the surface area of the sphere union by the chosen method.
    - `volume(method='monte-carlo', **opts)` — Compute the volume of the sphere union by the chosen method.
    - `plot(figure=None, *, points=None, function=None, sphere_color='white', sphere_style=None, point_style=None, point_values=None, distance_units='Angstroms', plot_intersections=False, **etc)` — Plot the surface: the sample points (colored by an optional scalar function),
    - `plot_sphere_points(points, centers, radii, figure=None, *, color='black', backend='x3d', return_objects=False, sphere_color='white', sphere_style=None, point_colors=None, point_values=None, vertex_colormap='WarioColors', rescale_color_values=True, plot_intersections=False, intersection_point_style=None, intersection_circle_style=None, **etc)` — Plot a set of points, spheres, and optional intersection geometry into a 3-D
  - **class `MeshCleaner`**
    - `__init__(verts, inds, vert_map, centers=None, radii=None, max_pair_dist=None)`
    - `report()` — The (cached) mesh topology report (boundary loops, non-manifold features, Euler
    - `clean()` — Return the cleaned mesh, stitching seams and capping holes (computed lazily).
    - `mesh_topology_report(verts, faces)` — Diagnose a triangle mesh (as produced by `union_of_spheres_mesh`) for
  - **class `SphereUnionSurfaceMesh`**
    - `__init__(verts, inds, surf=None, densities=None, tri_map=None, vert_map=None, normals=None, vertex_normals=None, centers=None, radii=None)`
    - `surface_area(return_components=False)` — Compute the mesh surface area as the sum of its triangle areas (Heron's
    - `volume(return_components=False)` — Exact volume of a closed mesh via the divergence theorem.
    - `normal_derivatives(order=1)` — Compute the derivatives (up to `order`) of each triangle's normal with respect to
    - `area_derivatives(order=1, return_components=False)` — Compute the derivatives (up to `order`) of each triangle's area with respect to
    - `centroid_derivatives(order=1, return_components=False)` — Compute the derivatives (up to `order`) of each triangle's centroid with respect
    - `volume_derivatives(order=1, return_components=False, normal_order=None, area_order=None, centroid_order=None)` — Compute the derivatives (up to `order`) of the enclosed volume with respect to
    - `normals()` — The per-triangle unit normals (computed lazily).
    - `signed_volumes()` — The per-triangle signed tetrahedron volumes (the cross-product norms used in the
    - `get_normals(normalize=True)` — Compute the per-triangle normals (and their norms) from the triangle edge cross
    - `from_submeshes(pts, submeshes, *, centers, radii, occlusion_type='complete', occlusion_tolerance=0.01, check_normals=True, deduplicate_points=False, duplicate_point_threshold=1e-14, vert_map=None, intersection_point_mask=None, occlusion_intersection_tolerance=0.05, stitch=True, **etc)` — Build a mesh from a shared point set and per-sphere triangle sub-meshes,
    - `stitch()` — Return a topologically repaired copy of the mesh (seams stitched, holes capped)
    - `from_subclouds(point_clouds, *, centers, radii, mesh_type='convex', occlusion_type='partial', vert_map=None, deduplicate_points=False, mesh_kwargs=None, intersection_point_mask=None, **surface_options)` — Build a mesh by convex-hulling each per-sphere point cloud and unioning the
    - `from_o3d(mesh, densities=None, surf=None)` — Build a mesh from an Open3D triangle mesh.
    - `plot(figure=None, *, function=None, vertex_values=None, normals=None, invert_mesh=False, distance_units='Angstroms', **etc)` — Plot the triangle mesh, optionally coloring vertices by a scalar function and
    - `plot_triangle_mesh(verts, indices, figure=None, *, color='blue', transparency=0.8, backend='x3d', return_objects=False, line_color='black', line_transparency=0.9, line_style=None, vertex_colors=None, vertex_values=None, vertex_colormap='WarioColors', rescale_color_values=True, normals=None, centroids=None, normal_color='black', normal_radius=0.01, normal_scaling=0.5, **etc)` — Plot a triangle mesh (faces, edges, and optional per-triangle normals) into a 3-D

### `Surfaces/Surface.py`
  - **class `Surface`**
    > This actually isn't a concrete implementation of BaseSurface.
    > Instead it's a class that _dispatches_ to an implementation of BaseSurface to do its core evaluations (plus it does shape checking)
    - `__init__(data, dimension=None, base=None, **metadata)`
    - `data()` — The backing data of the dispatched base surface.
    - `minimize(initial_guess=None, function_options=None, **opts)` — Provides a uniform interface for minimization, basically just dispatching to the BaseSurface implem…
    - `detect_base(data, opts)` — Infers what type of base surface works for the data that's passed in.
    - `center()` — The expansion center of the base surface (if it has one).
    - `ref()` — The reference value of the base surface (if it has one).
    - `expansion_tensors()` — The expansion tensors of the base surface (if it has them).
  - **class `MultiSurface`**
    > A _reallly_ simple extension to the Surface infrastructure to handle vector valued functions,
    > assuming each vector value corresponds to a different Surfaces
    - `__init__(*surfs)`

### `Symbolic/ElementaryFunctions.py`
  - **class `Functionlike`**
    > A function suitable for symbolic manipulation
    > with derivatives and evlauation
    - `eval(r)`
    - `cur_var()`
    - `inc_var()`
    - `reset_var()`
    - `get_compile_var()`
    - `get_compile_spec()`
    - `compile(mode='numba')`
    - `deriv(*which, simplify=True)`
    - `invert()`
    - `copy()`
    - `compose(other)`
    - `is_zero(f)`
    - `is_one(f)`
    - `is_identity(f)`
    - `sort_val()`
    - `get_sortval()`
    - `simplify(iterations=10)`
    - `apply_simplifications()`
    - `merge_funcs(funcs, reducer, iterations=10)`
    - `get_children()`
    - `children()`
    - `traverse(root, traversal_order='depth', visit_order='post', node_test=None, max_depth=None, track_index=False)`
    - `get_child(pos)`
    - `replace_child(pos, new)`
    - `tree_repr(sep='', indent='')`
  - **class `ElementaryFunction`** (Functionlike)
    > A _univariate_ function (though it can be threadable)
    > that has known values and derivatives
    - `__init__(*, idx=None)`
    - `get_deriv()`
    - `deriv(order=1, simplify=True)`
    - `idx_compatible(other)`
  - **class `Variable`** (ElementaryFunction)
    - `__init__(name, idx)`
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv()`
    - `simplify(iterations=10)`
    - `tree_repr(sep='', indent='')`
  - **class `ElementaryVaradic`** (ElementaryFunction)
    - `__init__(*functions, idx=None)`
    - `get_sortval()`
    - `tree_equivalent(other)`
    - `get_children()`
    - `get_repr(fns)`
    - `tree_repr(sep='\n', indent='')`
    - `get_child(pos)`
    - `replace_child(pos, new)`
  - **class `ElementarySummation`** (ElementaryVaradic)
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv()`
    - `get_repr(fns)`
    - `merge_product(f1, f2)`
    - `reduce_pair(f1, f2)`
    - `apply_simplifications()`
  - **class `ElementaryProduct`** (ElementaryVaradic)
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv()`
    - `reduce_pair(f1, f2)`
    - `apply_simplifications()`
    - `get_repr(fns)`
  - **class `ElementaryComposition`** (ElementaryVaradic)
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv()`
    - `subs_identities(f1, f2)`
    - `apply_simplifications()`
    - `get_repr(fns)`
  - **class `MultivariateFunction`** (Functionlike)
    > A multivariate function composed from elementary functions.
    > This is a
    - `__init__(*functions, indices=None)`
    - `construct_varivariate(univariate, multivariate, terms, indices=None)`
    - `indices()`
    - `ndim()`
    - `get_deriv(*counts)`
    - `deriv(*which, order=1, ndim=None, simplify=True)`
    - `get_sortval()`
    - `apply_simplifications()`
    - `tree_equivalent(other)`
    - `get_children()`
    - `tree_repr(sep='\n', indent='')`
    - `get_child(pos)`
    - `replace_child(pos, new)`
  - **class `TensorFunction`** (MultivariateFunction)
    > A tensor of functions
    - `__init__(functions, symmetric=True, indices=None)`
    - `apply_function(fn, res_builder=None)`
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv(*counts)`
    - `get_sortval()`
    - `apply_simplifications()`
    - `format_repr_array(arr, ilevel=0, brackets='[]', sep=',\n', indent=' ')`
    - `tree_equivalent(other)`
    - `tree_repr(sep='\n', indent='')`
    - `copy()`
    - `get_children()`
    - `get_child(pos)`
    - `replace_child(pos, new)`
  - **class `Summation`** (MultivariateFunction)
    > A summation of 1D functions to support testing derivs
    - `eval(r)`
    - `get_compile_spec()`
    - `construct(*terms, indices=None)`
    - `get_deriv(*counts)`
    - `merge_product(f1, f2)`
    - `reduce_pair(f1, f2)`
    - `apply_simplifications()`
  - **class `Product`** (MultivariateFunction)
    > A summation of 1D functions to support testing derivs
    - `eval(r)`
    - `get_compile_spec()`
    - `construct(*terms, indices=None)`
    - `get_1d_deriv(idx, amt)`
    - `get_deriv(*counts)`
    - `apply_simplifications()`
  - **class `Composition`** (MultivariateFunction)
    > A composition of multivariate functions that
    > uses the chain rule for derivatives
    - `eval(r)`
    - `get_compile_spec()`
    - `construct(*terms, indices=None)`
    - `apply_simplifications()`
    - `get_deriv(*counts)`
  - **class `Scalar`** (ElementaryFunction)
    > Broadcasts a constant value
    - `__init__(scalar, *, idx=0)`
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv()`
    - `deriv(order=1, *, simplify=True)`
    - `get_sortval()`
    - `tree_repr(sep='\n', indent='')`
  - **class `Identity`** (ElementaryFunction)
    > Identity function for compositions
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv()`
    - `deriv(order=1, simplify=True)`
    - `simplify(iterations=10)`
    - `get_sortval()`
  - **class `Power`** (ElementaryFunction)
    - `__init__(power, *, idx=None)`
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv()`
    - `get_sortval()`
    - `apply_simplifications()`
    - `tree_repr(sep='\n', indent='')`
  - **class `Exponent`** (ElementaryFunction)
    - `__init__(base, *, idx=None)`
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv()`
    - `get_sortval()`
    - `tree_repr(sep='\n', indent='')`
  - **class `Exp`** (Exponent)
    - `__init__(*, idx=None)`
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv()`
    - `tree_repr(sep='\n', indent='')`
  - **class `Logarithm`** (ElementaryFunction)
    - `__init__(base, *, idx=None)`
    - `eval(r)`
    - `get_deriv()`
    - `get_compile_spec()`
    - `get_sortval()`
    - `tree_repr(sep='\n', indent='')`
  - **class `Ln`** (Logarithm)
    - `__init__(*, idx=None)`
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv()`
    - `tree_repr(sep='\n', indent='')`
  - **class `Sin`** (ElementaryFunction)
    - `eval(r)`
    - `get_deriv()`
    - `get_compile_spec()`
  - **class `Cos`** (ElementaryFunction)
    - `eval(r)`
    - `get_compile_spec()`
    - `get_deriv()`
  - **class `CompoundFunction`** (ElementaryFunction)
    - `__init__(*, idx=None)`
    - `get_expression()`
    - `expression()`
    - `get_deriv()`
    - `get_compile_spec()`
    - `get_sortval()`
  - **class `Morse`** (CompoundFunction)
    - `__init__(*, de=1, a=1, re=0, idx=None)`
    - `get_expression()`
    - `eval(r)`
    - `get_deriv()`
    - `tree_repr(sep='\n', indent='')`
  - **class `MorseDeriv`** (CompoundFunction)
    - `__init__(order, *, de=1, a=1, re=0, idx=None)`
    - `eval(r)`
    - `get_expression()`
    - `get_deriv()`
    - `tree_repr(sep='\n', indent='')`
  - **class `Symbols`**
    - `__init__(*vars)`
    - `scalar(v)`
    - `log(v, base=None)`
    - `exp(v, base=None)`
    - `cos(x)`
    - `sin(x)`
    - `morse(r, de=1, a=1, re=0)`
  - **class `SymPyFunction`**
    > A function suitable for symbolic manipulation
    > with derivatives and evlauation
    - `get_sympy()`
    - `sympy()`
    - `__init__(expr, vars=None)`
    - `sort_vars(vars)`
    - `merge_vars(v1, v2)`
    - `compile()`
    - `eval(r)`
    - `deriv(*which, order=1)`
    - `invert()`
    - `copy()`
    - `compose(other)`
    - `symbols(*syms)`
    - `exp(fn)`
    - `morse(var, de=10, a=1, re=0)`
  - **class `SymPyArrayFunction`**
    - `__init__(expr_array, symmetric=False)`
    - `apply_function(fn, res_builder=None)`
    - `eval(r)`
    - `invert()`
    - `copy()`
    - `compose(other)`

### `Symbolic/TensorExpressions.py`
  - **class `TensorExpression`**
    - `__init__(expr, **vars)`
    - `eval(subs=None, print_terms=False)`
    - `primitives()`
    - `walk(callback)`
    - `get_prims()`
    - **class `ArrayStack`**
      - `__init__(shape, array)`
      - `flip()`
      - `stack_dim()`
      - `shape()`
      - `ndim()`
      - `expand_dims(where)`
      - `moveaxis(i, j)`
      - `tensordot(other, axes=None)`
      - `outer(other, axes=None)`
      - `rev_outer(other, axes=None)`
    - **class `Term`**
      - `__init__(array=None, name=None)`
      - `get_children()`
      - `children()`
      - `deriv()`
      - `dQ()`
      - `array_generator(**kwargs)`
      - `ndim()`
      - `get_hash()`
      - `asarray(print_terms=False, cache=True, **kw)`
      - `array()`
      - `array(arr)`
      - `rank()`
      - `ndim()`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
      - `simplify(check_arrays=False)`
      - `flip()`
      - `divided()`
      - `dot(other, i, j)`
      - `shift(i, j)`
      - `det()`
      - `tr(axis1=1, axis2=2)`
      - `inverse()`
      - `outer(other)`
    - **class `SumTerm`** (Term)
      - `__init__(*terms, array=None, name=None)`
      - `get_children()`
      - `deriv()`
      - `array_generator(print_terms=False)`
      - `rank()`
      - `reduce_terms(check_arrays=False)`
      - `get_hash()`
      - `to_string()`
      - `substitute(other)` — substitutes other in to the sum by matching up all necessary terms
    - **class `ScalingTerm`** (Term)
      - `__init__(term, scaling, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
      - `deriv()`
    - **class `ScalarScalingTerm`** (Term)
      > Scaling elementwise with correct broadcasting
      - `__init__(term, scaling, axes=None, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
      - `deriv()`
    - **class `ScalarPowerTerm`** (Term)
      > Represents x^n.
      > Only can get valid derivatives for scalar terms.
      > Beware of that.
      - `__init__(term, pow, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
      - `deriv()`
    - **class `FlippedTerm`** (ScalarPowerTerm)
      > Represents 1/x. Only can get valid derivatives for scalar terms. Beware of that.
      - `__init__(term, pow=-1, array=None)`
      - `get_children()`
      - `to_string()`
      - `array_generator(print_terms=False)`
      - `reduce_terms(check_arrays=False)`
    - **class `AxisShiftTerm`** (Term)
      - `__init__(term, start, end, array=None, name=None)`
      - `get_children()`
      - `deriv()`
      - `array_generator(print_terms=False)`
      - `rank()`
      - `to_string()`
      - `reduce_terms(check_arrays=False)` — We simplify over the possible swap classes
    - **class `OuterTerm`** (Term)
      > Provides an outer product
      - `__init__(a, b, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
      - `deriv()`
    - **class `ContractionTerm`** (Term)
      - `__init__(left, i, j, right, array=None, name=None)`
      - `get_children()`
      - `array_generator(print_terms=False)`
      - `rank()`
      - `deriv()`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
    - **class `InverseTerm`** (Term)
      - `__init__(term, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
      - `deriv()`
    - **class `TraceTerm`** (Term)
      - `__init__(term, axis1=1, axis2=2, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
      - `deriv()`
    - **class `DeterminantTerm`** (Term)
      - `__init__(term, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
      - `deriv()`
    - **class `VectorNormTerm`** (Term)
      - `__init__(term, array=None, name=None, axis=-1)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
      - `deriv()`
    - **class `ScalarFunctionTerm`** (Term)
      - `__init__(term, name='f', f=None, array=None, derivative_order=0)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
      - `deriv()`
    - **class `ConstantArray`** (Term)
      > Square tensor of constants (squareness assumed, not checked)
      - `__init__(array, parent=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `get_hash()`
      - `to_string()`
      - `deriv()`
      - `reduce_terms(check_arrays=False)`
    - **class `IdentityMatrix`** (ConstantArray)
      - `__init__(ndim, parent=None, name='I')`
    - **class `OuterPowerTerm`** (Term)
      > Represents a matrix-power type term
      - `__init__(base, pow, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `get_hash()`
      - `to_string()`
      - `deriv()`
      - `reduce_terms(check_arrays=False)`
    - **class `TermVector`** (Term)
      - `__init__(*terms, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `deriv()`
      - `reduce_terms(check_arrays=False)`
    - **class `CoordinateVector`** (Term)
      - `__init__(vals_array, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `deriv()`
      - `reduce_terms(check_arrays=False)`
    - **class `CoordinateTerm`** (Term)
      - `__init__(idx, vec, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `deriv()`
      - `reduce_terms(check_arrays=False)`
    - **class `PolynomialTerm`** (Term)
      - `__init__(expansion, coords=None, array=None, name=None)`
      - `get_children()`
      - `rank()`
      - `array_generator(print_terms=False)`
      - `to_string()`
      - `deriv()`
      - `reduce_terms(check_arrays=False)`
  - **class `TensorExpansionError`** (Exception)
  - **class `TensorExpansionTerms`**
    > A friend of DumbTensor which exists
    > to not only make the tensor algebra suck less but also
    > to make it automated by making use of some simple rules
    > for expressing derivatives specifically in the context of
    > doing the coordinate transformations we need to do.
    > Everything here is 1 indexed since that's how I did the OG math
    - `__init__(qx_terms, xv_terms, qxv_terms=None, base_qx=None, base_xv=None, q_name='Q', v_name='V')`
    - `QX(n)`
    - `XV(m)`
    - `QXV(n, m)`
    - **class `QXTerm`** (TensorExpression.Term)
      - `__init__(terms, n, array=None)`
      - `get_children()`
      - `deriv()`
      - `array_generator(print_terms=False)`
      - `rank()`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
    - **class `XVTerm`** (TensorExpression.Term)
      - `__init__(terms, m, array=None)`
      - `get_children()`
      - `deriv()`
      - `array_generator(print_terms=False)`
      - `rank()`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
    - **class `QXVTerm`** (TensorExpression.Term)
      - `__init__(terms, n, m, array=None)`
      - `get_children()`
      - `deriv()`
      - `array_generator(print_terms=False)`
      - `rank()`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
    - **class `BasicContractionTerm`** (TensorExpression.Term)
      > Special case tensor contraction term between two elements of the
      > tensor expansion terms.
      - `__init__(terms, n, i, j, m, array=None)`
      - `deriv()`
      - `array_generator(print_terms=False)`
      - `rank()`
      - `to_string()`
      - `reduce_terms(check_arrays=False)`
  - **class `TensorDerivativeConverter`**
    > A class that makes it possible to convert expressions
    > involving derivatives in one coordinate system in another
    - `__init__(jacobians, derivatives=None, mixed_terms=None, jacobians_name='Q', values_name='V')`
    - `convert(order=None, print_transformations=False, check_arrays=False)`
    - `compute_partition_terms(partition)`
    - `convert_partition(partition, derivs, vals, val_axis=0)`
    - `convert_fast(derivs, vals, val_axis=-1, order=None)`

### `Taylor/Derivatives.py` — Module that provides a FiniteDifferenceDerivative class that does finite-difference derivatives
  - **class `FiniteDifferenceDerivative`**
    > Provides derivatives for a function (scalar or vector valued).
    > Can be indexed into or the entire tensor of derivatives may be requested.
    > The potential for optimization undoubtedly exists, but the idea is to provide as _simple_ an interface as possible.
    > Robustification needs to be done, but is currently used in `CoordinateSystem.jacobian` to good effect.
    - `__init__(f, function_shape=(0, 0), parallelizer=None, logger=None, **fd_opts)`
    - `derivatives(center, displacement_function=None, prep=None, lazy=None, mesh_spacing=None, **fd_opts)` — Generates a differencer object that can be used to get derivs however your little heart desires
  - **class `FunctionSpec`**
    > Defines a general spec that specifies a function, what it takes as coordinate inputs, and what the dimensions of what it outputs
    - `__init__(f, input_shape, output_shape)`
  - **class `DerivativeGenerator`**
    > A that generates specified derivatives, currently by FD but can be generalized out to do it other ways
    > *(truncated — see stub for full docstring)*
    - `__init__(f_spec, center, displacement_function=None, prep=None, lazy=False, mesh_spacing=0.001, cache_evaluations=True, parallelizer=None, logger=None, **fd_opts)`
    - `get_displacement(coord, mesh_spacing=None)` — Computes the displacement for the passed mesh spacing
    - `compute_derivatives(order, pos=(), coordinates=None, lazy=None, pos_filter=None, parallelizer=None)` — Computes the derivatives up to `order` filtered by `pos` over the `coordinates`
    - `derivative_tensor(order, pos=(), coordinates=None, pos_filter=None, parallelizer=None, logger=None)` — Computes a given derivative tensor

### `Taylor/FiniteDifferenceFunction.py` — Provides a general, convenient FiniteDifferenceFunction class to handle all of our difference FD im…
  - **class `FiniteDifferenceError`** (Exception)
  - **class `FiniteDifferenceFunction`**
    > The FiniteDifferenceFunction encapsulates a bunch of functionality extracted from [Fornberger's
    > Calculation of Wieghts in Finite Difference Formulas](https://epubs.siam.org/doi/pdf/10.1137/S0036144596322507)
    > *(truncated — see stub for full docstring)*
    - `__init__(*diffs, axes=0, contract=False)`
    - `apply(vals, axes=None, mesh_spacing=None, contract=None)` — Iteratively applies the stored finite difference objects to the vals
    - `order()` — :return: the order of the derivative requested
    - `weights()` — :return: the weights for the specified stencil
    - `widths()` — :return: the number of points in each dimension, left and right, for the specified stencil
    - `regular_difference(order, mesh_spacing=None, accuracy=2, stencil=None, end_point_accuracy=2, axes=0, contract=True, **kwargs)` — Constructs a `FiniteDifferenceFunction` appropriate for a _regular grid_ with the given stencil
    - `from_grid(grid, order, accuracy=2, stencil=None, end_point_accuracy=2, axes=0, contract=True, allow_irregular=False, **kwargs)` — Constructs a `FiniteDifferenceFunction` from a grid and order.
  - **class `FiniteDifference1D`**
    > A one-dimensional finite difference derivative object.
    > Higher-dimensional derivatives are built by chaining these.
    - `__init__(finite_difference_data, matrix)`
    - `order()` — **LLM Docstring**
    - `weights()` — The finite-difference weights (left, center, right).
    - `widths()` — The stencil widths (left, center, right).
    - `get_stencil(order, stencil, accuracy, only_odd_orders=None)` — Compute the stencil size (number of points minus one) for a derivative order and
    - `apply(vals, val_dim=None, axis=0, mesh_spacing=None, check_shape=True)` — Applies the held `FiniteDifferenceMatrix` to the array of values
    - `sparse_tensordot(sparse, mat, axis)` — Not sure how fast this will be, but does a very simple contraction of `mat` along `axis` by the fin…
  - **class `RegularGridFiniteDifference`** (FiniteDifference1D)
    > Defines a 1D finite difference over a regular grid
    - `__init__(order, stencil=None, accuracy=4, end_point_accuracy=2, only_odd_orders=None, **kw)`
    - `finite_difference_data(order, stencil, end_point_precision)` — Builds a FiniteDifferenceData object from an order, stencil, and end_point_precision
    - `get_weights(m, s, n)` — Extracts the weights for an evenly spaced grid
  - **class `IrregularGridFiniteDifference`** (FiniteDifference1D)
    > Defines a finite difference over an irregular grid
    - `__init__(grid, order, stencil=None, accuracy=2, end_point_accuracy=2, **kw)`
    - `get_grid_slices(grid, stencil)` — :param grid:
    - `get_weights(m, z, x)` — Extracts the grid weights for an unevenly spaced grid based off of the algorithm outlined by
    - `finite_difference_data(grid, order, stencil, end_point_precision)` — Constructs a finite-difference function that computes the nth derivative with a given width
  - **class `FiniteDifferenceData`**
    > Holds the data used by to construct a finite difference matrix
    - `__init__(weights, widths, order)`
    - `weights()` — **LLM Docstring**
    - `widths()` — **LLM Docstring**
    - `order()` — **LLM Docstring**
  - **class `FiniteDifferenceMatrix`**
    > Defines a matrix that can be applied to a regular grid of values to take a finite difference
    - `__init__(finite_difference_data, npts=None, mesh_spacing=None, only_core=False, only_center=False, mode='sparse', dtype='float64')`
    - `weights()` — The finite-difference weights backing the matrix.
    - `order()` — **LLM Docstring**
    - `npts()` — The number of grid points the matrix spans.
    - `npts(val)` — The number of grid points the matrix spans.
    - `mesh_spacing()` — The grid spacing.
    - `mesh_spacing(val)` — The grid spacing.
    - `only_core()` — Whether to build only the core (non-boundary) rows.
    - `only_core(val)` — Whether to build only the core (non-boundary) rows.
    - `only_center()` — Whether to build only the single centered row.
    - `only_center(val)` — Whether to build only the single centered row.
    - `mode()` — The storage mode (`'dense'` or `'sparse'`).
    - `mode(val)` — The storage mode (`'dense'` or `'sparse'`).
    - `dtype()` — The matrix dtype.
    - `dtype(val)` — The matrix dtype.
    - `matrix()` — The finite-difference matrix (built and cached lazily).
    - `fd_matrix()` — Builds a 1D finite difference matrix for a set of boundary weights, central weights, and num of poi…
- `finite_difference(grid, values, order, accuracy=2, stencil=None, end_point_accuracy=1, axes=None, only_core=False, only_center=False, dtype='float64', **kw)` — Computes a finite difference derivative for the values on the grid

### `Taylor/FunctionExpansions.py`
  - **class `TaylorPoly`**
    > A handler for dealing with multidimensional polynomials
    > *(truncated — see stub for full docstring)*
    - `__init__(derivatives, transforms=None, transformed_derivatives=False, center=None, ref=None, weight_coefficients=False)`
    - `center()` — **LLM Docstring**
    - `is_multi()` — Whether this is a stacked (multi-function) expansion.
    - `multipolynomial(*expansions)` — Build a single stacked expansion from several separate expansions, stacking their
    - `canonicalize_tfs(tfs)` — Normalize a coordinate-transform specification into `(forward_tensors,
    - `transforms()` — The coordinate-transform tensors (forward, and inverse if present), or `None`
    - `expansion_tensors()` — Provides the tensors that will contracted
    - `expansion_tensors(tensors)` — Are we going to assume in setting the tensors that
    - `derivative_tensors()` — Provides the base derivative tensors
    - `derivative_tensors(derivs)` — :param derivs: the per-order derivative tensors
    - `get_expansions(coords, transform_displacements=True, subexpansions=None, outer=True, order=None, squeeze=None)` — :param coords: Coordinates to evaluate the expansion at
    - `expand(coords, order=None, outer=True, transform_displacements=True, squeeze=True)` — Returns a numerical value for the expanded coordinates
    - **class `CoordinateTransforms`**
      - `__init__(transforms)`
    - **class `FunctionDerivatives`**
      - `__init__(derivs, weight_coefficients=True)`
      - `weight_derivs(t, order=None)` — :param order:
    - `deriv(which=None)` — Computes the derivative(s) of the expansion(s) with respect to the
    - `from_indices(inds, ref=0, expansion_order=None, ndim=None, symmetrize=True, **opts)` — Build an expansion from a sparse set of `(index_tuple, value)` derivative
    - `shift(new_origin)` — Uses binomial expansion to new polynomial centered at the `new_origin`
  - **class `FunctionExpansionException`** (Exception)
  - **class `FunctionExpansion`** (TaylorPoly)
    > Specifically for expanding functions
    - `expand_function(f, point, order=4, basis=None, function_shape=None, transforms=None, weight_coefficients=True, **fd_options)` — Expands a function about a point up to the given order

### `Taylor/ZachLib/coeffuncs.py` — coeffuncs defines the functions we use when computing coefficients for FD
- `StirlingS1(n)` — Computes the Stirling numbers
- `Binomial(n)` — :param n:
- `GammaBinomial(s, n)` — Generalized binomial gamma function
- `Factorial(n)` — I was hoping to do this in some built in way with numpy...but I guess it's not possible?
- `EvenFiniteDifferenceWeights(m, s, n)` — Finds the series coefficients for x^s*ln(x)^m centered at x=1.
- `UnevenFiniteDifferenceWeights(m, z, x)`

### `Taylor/ZachLib/src/setup.py`
- `get_macros()`
- `get_extension()`
- `setup_compile()`
- `compile()`
- `find_source()`
- `load()`