"""
Sets up a general Interpolator class that looks like Mathematica's InterpolatingFunction class
"""
import numpy as np, math, time, abc
import scipy.spatial as spat
import itertools, typing, dataclasses
import scipy.special as special
from ..Numputils import vec_outer, vec_tensordot, unique as nput_unique, vec_tensordiag, tensordot_deriv, tensorprod_deriv
from .Taylor import FunctionExpansion
from .Symbolic import TensorExpression
from ..Scaffolding import Logger
__all__ = ['RBFDInterpolator', 'InverseDistanceWeightedInterpolator']

class NeighborBasedInterpolator(metaclass=abc.ABCMeta):
    """
    Useful base class for neighbor-based interpolation
    """
    __props__ = ('clustering_radius', 'neighborhood_size', 'neighborhood_merge_threshold', 'neighborhood_clustering_radius', 'coordinate_transform', 'bad_interpolation_retries', 'logger')

    def __init__(self, pts, values, *derivatives, clustering_radius=None, neighborhood_size=15, neighborhood_merge_threshold=None, neighborhood_max_merge_size=100, neighborhood_clustering_radius=None, coordinate_transform=None, bad_interpolation_retries=2, logger=None):
        """
        **LLM Docstring**

        Set up a local interpolator over scattered sample points (and optional
        derivative data), building a KD-tree for neighbor lookups and optionally
        declustering near-coincident points.

        :param pts: the sample points, shape `(npts, ndim)`
        :type pts: np.ndarray
        :param values: the values at the sample points
        :type values: np.ndarray
        :param derivatives: optional per-order derivative data at the points
        :param clustering_radius: drop points closer than this (declustering)
        :type clustering_radius: float | None
        :param neighborhood_size: the number of neighbors used per interpolation
        :type neighborhood_size: int
        :param neighborhood_merge_threshold: index-overlap threshold for merging neighbor groups
        :type neighborhood_merge_threshold: int | None
        :param neighborhood_max_merge_size: the maximum merged neighbor-group size
        :type neighborhood_max_merge_size: int
        :param neighborhood_clustering_radius: declustering radius applied within a neighborhood
        :type neighborhood_clustering_radius: float | None
        :param coordinate_transform: an optional coordinate transform
        :param bad_interpolation_retries: how many times to retry a failed interpolation
        :type bad_interpolation_retries: int
        :param logger: a logger
        """
        ...

    @staticmethod
    def _decluster(pts, radius):
        """
        **LLM Docstring**

        Return a mask-pruned point set with points closer than `radius` to an earlier
        point removed (greedy declustering).

        :param pts: the points
        :type pts: np.ndarray
        :param radius: the minimum allowed spacing
        :type radius: float
        :return: the declustered points
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def decluster_data(cls, pts, vals, derivs, radius, return_mask=False):
        """
        **LLM Docstring**

        Decluster the sample points (and their values/derivatives) by dropping points
        closer than `radius`, working in the renormalized grid and in chunks for
        scalability.

        :param pts: the points
        :type pts: np.ndarray
        :param vals: the values
        :type vals: np.ndarray
        :param derivs: the per-order derivatives
        :type derivs: list
        :param radius: the minimum spacing
        :type radius: float
        :param return_mask: also return the keep mask
        :type return_mask: bool
        :return: `(pts, vals, derivs)` (and the mask if requested)
        :rtype: tuple
        """
        ...

    @dataclasses.dataclass
    class RescalingData:
        grid_shifts: 'Iterable[float]'
        grid_scaling: 'Iterable[float]'
        vals_shift: 'float'
        vals_scaling: 'float'
        __slots__ = ['grid_shifts', 'grid_scaling', 'vals_shift', 'vals_scaling']

        @classmethod
        def initialize_subgrid_data(cls, pts, values, derivatives):
            """
            **LLM Docstring**

            Renormalize a neighborhood's points, values, and derivatives to `[0, 1]`-ish
            scales and return them alongside a `RescalingData` capturing the shifts/scalings.

            :param pts: the neighborhood points
            :type pts: np.ndarray
            :param values: the values
            :type values: np.ndarray
            :param derivatives: the per-order derivatives
            :type derivatives: list
            :return: `(grid, vals, derivs, rescaling_data)`
            :rtype: tuple
            """
            ...

        @classmethod
        def renormalize_grid(cls, pts):
            """
            **LLM Docstring**

            Rescale each grid coordinate to `[0, 1]`, returning the rescaled grid and the
            per-axis shifts and scalings.

            :param pts: the grid points
            :type pts: np.ndarray
            :return: `(rescaled_grid, shifts, scalings)`
            :rtype: tuple
            """
            ...

        @classmethod
        def renormalize_values(cls, values):
            """
            **LLM Docstring**

            Rescale values to `[0, 1]`, returning the rescaled values and the shift and
            scaling.

            :param values: the values
            :type values: np.ndarray
            :return: `(rescaled_values, shift, scaling)`
            :rtype: tuple
            """
            ...

        @classmethod
        def renormalize_derivs(cls, derivs, vals_scaling, grid_scaling):
            """
            **LLM Docstring**

            Rescale derivative tensors consistently with the value and grid rescalings, and
            reduce them to their unique (upper-triangular) components.

            :param derivs: the per-order derivatives
            :type derivs: list
            :param vals_scaling: the value scaling
            :param grid_scaling: the per-axis grid scaling
            :return: the rescaled, reduced derivatives
            :rtype: list
            """
            ...

        def apply_renormalization(self, pts):
            """
            **LLM Docstring**

            Apply the stored grid renormalization (shift and scale) to a set of points.

            :param pts: the points
            :type pts: np.ndarray
            :return: the renormalized points
            :rtype: np.ndarray
            """
            ...

        def reverse_renormalization(self, pts):
            """
            **LLM Docstring**

            Undo the grid renormalization, mapping renormalized points back to the original
            coordinates.

            :param pts: the renormalized points
            :type pts: np.ndarray
            :return: the original-coordinate points
            :rtype: np.ndarray
            """
            ...

        def reverse_value_renormalization(self, vs):
            """
            **LLM Docstring**

            Undo the value renormalization, mapping renormalized values back to the original
            scale.

            :param vs: the renormalized values
            :type vs: np.ndarray
            :return: the original-scale values
            :rtype: np.ndarray
            """
            ...

        def reverse_derivative_renormalization(self, derivs, reshape=True):
            """
            **LLM Docstring**

            Undo the derivative renormalization, optionally re-expanding the reduced
            upper-triangular components back into full symmetric derivative tensors.

            :param derivs: the renormalized (reduced) derivatives
            :type derivs: list
            :param reshape: re-expand into full symmetric tensors
            :type reshape: bool
            :return: the original-scale derivatives
            :rtype: list
            """
            ...

    @staticmethod
    def triu_inds(ndim, rank):
        """
        **LLM Docstring**

        Return the upper-triangular (unique) index tuples for a symmetric rank-`rank`
        tensor in `ndim` dimensions.

        :param ndim: the number of dimensions
        :type ndim: int
        :param rank: the tensor rank
        :type rank: int
        :return: the index arrays (one per axis)
        :rtype: tuple
        """
        ...

    @staticmethod
    def triu_num(ndim, rank):
        """
        **LLM Docstring**

        Return the number of unique components of a symmetric rank-`rank` tensor in
        `ndim` dimensions.

        :param ndim: the number of dimensions
        :type ndim: int
        :param rank: the tensor rank
        :type rank: int
        :return: the number of unique components
        :rtype: int
        """
        ...

    def get_neighborhood(self, pts, *, neighbors, return_distances=False):
        """
        **LLM Docstring**

        Query the KD-tree for the nearest `neighbors` sample points to each query point.

        :param pts: the query points
        :type pts: np.ndarray
        :param neighbors: the number of neighbors (defaults to `neighborhood_size`)
        :type neighbors: int | None
        :param return_distances: also return the neighbor distances
        :type return_distances: bool
        :return: the neighbor indices (and distances if requested)
        :rtype: np.ndarray | tuple
        """
        ...

    def create_neighbor_groups(self, inds, merge_limit=None, max_merge_size=None):
        """
        **LLM Docstring**

        Group query points that share (nearly) the same neighborhood so one interpolation
        can be reused across them, optionally merging groups whose neighbor sets differ by
        fewer than a threshold.

        :param inds: the per-point neighbor-index sets
        :type inds: np.ndarray
        :param merge_limit: the index-overlap threshold for merging
        :type merge_limit: int | None
        :param max_merge_size: the maximum merged group size
        :type max_merge_size: int | None
        :return: `(neighbor_index_groups, point_index_groups)`
        :rtype: tuple
        """
        ...

    def prep_interpolation_data(self, inds):
        """
        **LLM Docstring**

        Gather and renormalize the grid points, values, and derivatives for a
        neighborhood.

        :param inds: the neighbor indices
        :type inds: np.ndarray
        :return: `(grid, vals, derivs, scaling_data)`
        :rtype: tuple
        """
        ...

    @abc.abstractmethod
    def construct_interpolation(self, inds, solver_data=False, return_error=False):
        """
        **LLM Docstring**

        Abstract: build the interpolation data (e.g. solved weights) for a neighborhood.

        :param inds: the neighbor indices
        :type inds: np.ndarray
        :param solver_data: also return solver diagnostics
        :type solver_data: bool
        :param return_error: also return the interpolation error
        :type return_error: bool
        :return: the interpolation data
        """
        ...

    @abc.abstractmethod
    def apply_interpolation(self, pts, data, inds, deriv_order=0, reshape_derivatives=True, return_data=False):
        """

        :param pts:
        :type pts:
        :param data:
        :type data:
        :param deriv_order:
        :type deriv_order:
        :return:
        :rtype:
        """
        ...

    def prep_neighborhoods(self, pts, hoods, distances, neighbors, merge_neighbors=None, neighborhood_clustering_radius=None, min_distance=None, max_distance=None, use_natural_neighbors=None):
        """
        **LLM Docstring**

        Post-process raw neighborhoods before interpolation: optionally decluster within
        each neighborhood, apply min/max distance cutoffs, switch to natural (Delaunay)
        neighbors, and group points sharing a neighborhood.

        :param pts: the query points
        :type pts: np.ndarray
        :param hoods: the per-point neighbor indices
        :type hoods: np.ndarray
        :param distances: the per-point neighbor distances
        :type distances: np.ndarray
        :param neighbors: the neighbor count
        :type neighbors: int
        :param merge_neighbors: the group-merge threshold
        :type merge_neighbors: int | None
        :param neighborhood_clustering_radius: within-neighborhood declustering radius
        :type neighborhood_clustering_radius: float | None
        :param min_distance: drop neighbors closer than this
        :type min_distance: float | None
        :param max_distance: drop neighbors farther than this
        :type max_distance: float | None
        :param use_natural_neighbors: use Delaunay natural neighbors
        :type use_natural_neighbors: bool | None
        :return: `(neighbor_index_groups, point_index_groups)`
        :rtype: tuple
        """
        ...

    def eval(self, pts, deriv_order=0, neighbors=None, merge_neighbors=None, reshape_derivatives=True, return_interpolation_data=False, check_in_sample=True, zero_tol=1e-08, return_error=False, use_cache=True, retries=None, max_distance=None, min_distance=None, neighborhood_clustering_radius=None, use_natural_neighbors=False, chunk_size=None):
        """
        **LLM Docstring**

        Evaluate the interpolant (and derivatives up to `deriv_order`) at a set of query
        points: find and prepare each point's neighborhood, build and apply the local
        interpolation (retrying on failure), and assemble the results.

        :param pts: the query points
        :type pts: np.ndarray
        :param deriv_order: the highest derivative order to return
        :type deriv_order: int
        :param neighbors: the neighbor count
        :type neighbors: int | None
        :param merge_neighbors: the group-merge threshold
        :type merge_neighbors: int | None
        :param reshape_derivatives: return full derivative tensors (vs unique components)
        :type reshape_derivatives: bool
        :param return_interpolation_data: also return the per-point interpolation data
        :type return_interpolation_data: bool
        :param check_in_sample: short-circuit points that coincide with sample points
        :type check_in_sample: bool
        :param zero_tol: the coincidence tolerance
        :type zero_tol: float
        :param return_error: also return per-point error estimates
        :type return_error: bool
        :param use_cache: reuse cached neighborhood interpolations
        :type use_cache: bool
        :param retries: number of retries on a failed interpolation
        :type retries: int | None
        :param max_distance: max neighbor distance
        :type max_distance: float | None
        :param min_distance: min neighbor distance
        :type min_distance: float | None
        :param neighborhood_clustering_radius: within-neighborhood declustering radius
        :type neighborhood_clustering_radius: float | None
        :param use_natural_neighbors: use Delaunay natural neighbors
        :type use_natural_neighbors: bool
        :param chunk_size: process the query points in chunks of this size
        :type chunk_size: int | None
        :return: the values (and derivatives / data / errors as requested)
        :rtype: np.ndarray | list | tuple
        """
        ...

    def resiliance_test(self, expansion, interpolation_data, mesh_spacing=0.01, tolerance=0.05):
        """
        **LLM Docstring**

        Stub: intended to check an interpolation's error against a Taylor expansion over a
        small mesh. Not currently implemented.

        :param expansion: the reference expansion
        :param interpolation_data: the interpolation data to test
        :param mesh_spacing: the test mesh spacing
        :type mesh_spacing: float
        :param tolerance: the allowed scaled error
        :type tolerance: float
        :raises NotImplementedError: always (not currently implemented)
        """
        ...

    def __call__(self, pts, deriv_order=0, neighbors=None, merge_neighbors=None, reshape_derivatives=True, return_interpolation_data=False, use_cache=True, return_error=False, zero_tol=1e-08, retries=None, **extra_opts):
        """
        **LLM Docstring**

        Evaluate the interpolant at the given points (delegates to `eval`).

        :param pts: the query points
        :type pts: np.ndarray
        :param deriv_order: the highest derivative order
        :type deriv_order: int
        :param neighbors: the neighbor count
        :type neighbors: int | None
        :param merge_neighbors: the group-merge threshold
        :type merge_neighbors: int | None
        :param reshape_derivatives: return full derivative tensors
        :type reshape_derivatives: bool
        :param return_interpolation_data: also return the interpolation data
        :type return_interpolation_data: bool
        :param use_cache: reuse cached interpolations
        :type use_cache: bool
        :param return_error: also return error estimates
        :type return_error: bool
        :param zero_tol: the coincidence tolerance
        :type zero_tol: float
        :param retries: number of retries on failure
        :type retries: int | None
        :param extra_opts: extra options forwarded to `eval`
        :return: the interpolated values (and extras as requested)
        :rtype: np.ndarray | list | tuple
        """
        ...

    def construct_function_expansion(self, inds):
        """
        **LLM Docstring**

        Build a `FunctionExpansion` centered on a neighborhood's points from the stored
        values and derivatives.

        :param inds: the neighbor indices
        :type inds: np.ndarray
        :return: the function expansion
        :rtype: FunctionExpansion
        """
        ...

    @classmethod
    def create_function_interpolation(cls, pts, fn, *derivatives, derivative_order=None, function_shape=None, **opts):
        """
        **LLM Docstring**

        Build an interpolator by sampling a function (and, if needed, finite-differencing
        it) at a set of points to get the values and derivatives.

        :param pts: the sample points
        :type pts: np.ndarray
        :param fn: the function to sample
        :type fn: Callable
        :param derivatives: analytic derivative functions, if available
        :param derivative_order: the highest derivative order to use
        :type derivative_order: int | None
        :param function_shape: the `(input, output)` shape for finite differencing
        :type function_shape: tuple | None
        :param opts: extra options (split between the FD machinery and the interpolator)
        :return: the interpolator
        :rtype: NeighborBasedInterpolator
        """
        ...

    def nearest_interpolation(self, pts, neighbors=None, solver_data=False, interpolator=True):
        """

        :param pts:
        :type pts:
        :param neighbors:
        :type neighbors:
        :param solver_data:
        :type solver_data:
        :param interpolator:
        :type interpolator:
        :return:
        :rtype: RBFDInterpolator.Interpolator|RBFDInterpolator.InterpolationData
        """
        ...

    class Interpolator:
        __slots__ = ['data', 'inds', 'parent']

        def __init__(self, data, inds, parent: 'NeighborBasedInterpolator'):
            """
            **LLM Docstring**

            Wrap a single neighborhood's interpolation data as a callable interpolator.

            :param data: the interpolation data
            :param inds: the neighbor indices
            :type inds: np.ndarray
            :param parent: the owning interpolator
            :type parent: NeighborBasedInterpolator
            """
            ...

        def __call__(self, pts, deriv_order=0, reshape_derivatives=True):
            """
            **LLM Docstring**

            Evaluate this neighborhood's interpolant at the given points.

            :param pts: the query points
            :type pts: np.ndarray
            :param deriv_order: the highest derivative order
            :type deriv_order: int
            :param reshape_derivatives: return full derivative tensors
            :type reshape_derivatives: bool
            :return: the value (and derivatives if `deriv_order > 0`)
            :rtype: np.ndarray | list
            """
            ...

    @property
    def global_interpolator(self):
        """
        **LLM Docstring**

        An `Interpolator` built over the entire sample set (all points as one
        neighborhood), constructed and cached lazily with error checking disabled.

        :return: the global interpolator
        :rtype: NeighborBasedInterpolator.Interpolator
        """
        ...

class RBFDError(ValueError):
    ...

class RBFDInterpolator(NeighborBasedInterpolator):
    """
    Provides a flexible RBF interpolator that also allows
    for matching function derivatives
    """

    def __init__(self, pts, values, *derivatives, kernel: typing.Union[callable, dict]='thin_plate_spline', kernel_options=None, auxiliary_basis=None, auxiliary_basis_options=None, extra_degree=0, clustering_radius=None, monomial_basis=True, multicenter_monomials=True, neighborhood_size=15, neighborhood_merge_threshold=None, neighborhood_max_merge_size=100, neighborhood_clustering_radius=None, solve_method='svd', max_condition_number=np.inf, error_threshold=0.01, bad_interpolation_retries=3, coordinate_transform=None, logger=None):
        """
        **LLM Docstring**

        Set up a radial-basis-function interpolator that fits both values and
        derivatives, with a chosen kernel and an auxiliary polynomial basis.

        :param pts: the sample points
        :type pts: np.ndarray
        :param values: the values
        :type values: np.ndarray
        :param derivatives: optional per-order derivative data
        :param kernel: the RBF kernel (name, callable, or spec dict)
        :type kernel: str | Callable | dict
        :param kernel_options: extra options bound into the kernel
        :type kernel_options: dict | None
        :param auxiliary_basis: the auxiliary polynomial basis (name/callable/spec)
        :param auxiliary_basis_options: extra options for the auxiliary basis
        :type auxiliary_basis_options: dict | None
        :param extra_degree: extra polynomial degree beyond the minimum
        :type extra_degree: int
        :param clustering_radius: declustering radius for the sample points
        :type clustering_radius: float | None
        :param monomial_basis: use a monomial (vs full outer-power) polynomial basis
        :type monomial_basis: bool
        :param multicenter_monomials: center the monomials on each RBF center
        :type multicenter_monomials: bool
        :param neighborhood_size: neighbors per interpolation
        :type neighborhood_size: int
        :param neighborhood_merge_threshold: group-merge threshold
        :type neighborhood_merge_threshold: int | None
        :param neighborhood_max_merge_size: max merged group size
        :type neighborhood_max_merge_size: int
        :param neighborhood_clustering_radius: within-neighborhood declustering radius
        :type neighborhood_clustering_radius: float | None
        :param solve_method: the linear-solve method (e.g. `'svd'`)
        :type solve_method: str
        :param max_condition_number: condition-number cap (currently unused)
        :param error_threshold: the interpolation-error rejection threshold
        :type error_threshold: float
        :param bad_interpolation_retries: retries on a failed interpolation
        :type bad_interpolation_retries: int
        :param coordinate_transform: an optional coordinate transform
        :param logger: a logger
        """
        ...

    @staticmethod
    def gaussian(r, e=1, inds=None):
        """
        **LLM Docstring**

        The Gaussian radial basis kernel `exp(-(e r)^2)` at radius `r`.

        :param r: the radius
        :type r: np.ndarray
        :param e: the shape parameter
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the kernel values
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    def gaussian_derivative(n: int, inds=None):
        """
        **LLM Docstring**

        Return a function computing the `n`-th radial derivative of the Gaussian kernel.

        :param n: the derivative order
        :type n: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the `n`-th derivative function
        :rtype: Callable
        """
        ...

    @staticmethod
    def gaussian_singularity_handler(n: int, ndim: int, inds=None):
        """
        **LLM Docstring**

        Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
        of the Gaussian kernel in `ndim` dimensions.

        :param n: the derivative order
        :type n: int
        :param ndim: the spatial dimension
        :type ndim: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the singularity-handling function
        :rtype: Callable
        """
        ...

    @staticmethod
    def thin_plate_spline(r, o=3, inds=None):
        """
        **LLM Docstring**

        The thin-plate-spline radial basis kernel (`r^o log r` family) at radius `r`.

        :param r: the radius
        :type r: np.ndarray
        :param o: the spline order
        :type o: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the kernel values
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    def thin_plate_spline_derivative(n: int, inds=None):
        """
        **LLM Docstring**

        Return a function computing the `n`-th radial derivative of the thin-plate-spline kernel.

        :param n: the derivative order
        :type n: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the `n`-th derivative function
        :rtype: Callable
        """
        ...

    @staticmethod
    def thin_plate_spline_singularity_handler(n: int, ndim: int, inds=None):
        """
        **LLM Docstring**

        Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
        of the thin-plate-spline kernel in `ndim` dimensions.

        :param n: the derivative order
        :type n: int
        :param ndim: the spatial dimension
        :type ndim: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the singularity-handling function
        :rtype: Callable
        """
        ...
    wendland_coefficient_cache = {}

    @classmethod
    def wendland_coefficient(cls, l, j, k):
        """
        **LLM Docstring**

        Compute a coefficient of the Wendland polynomial (from its closed-form
        recurrence).

        :param l: the polynomial parameter (from the dimension/smoothness)
        :type l: int
        :param j: the coefficient index
        :type j: int
        :param k: the smoothness order
        :type k: int
        :return: the coefficient
        :rtype: float
        """
        ...

    @classmethod
    def wendland_polynomial(cls, r, d=None, k=3, inds=None):
        """
        **LLM Docstring**

        The compactly-supported Wendland radial basis polynomial of smoothness `k` at
        radius `r`.

        :param r: the radius
        :type r: np.ndarray
        :param d: the spatial dimension (sets the polynomial degree)
        :type d: int | None
        :param k: the smoothness order
        :type k: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the kernel values
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def wendland_polynomial_derivative(cls, n: int, inds=None):
        """
        **LLM Docstring**

        Return a function computing the `n`-th radial derivative of the Wendland kernel.

        :param n: the derivative order
        :type n: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the `n`-th derivative function
        :rtype: Callable
        """
        ...

    @staticmethod
    def wendland_polynomial_singularity_handler(n: int, ndim: int, inds=None):
        """
        **LLM Docstring**

        Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
        of the Wendland kernel in `ndim` dimensions.

        :param n: the derivative order
        :type n: int
        :param ndim: the spatial dimension
        :type ndim: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the singularity-handling function
        :rtype: Callable
        """
        ...

    @staticmethod
    def zeros(r, inds=None):
        """
        **LLM Docstring**

        The zero kernel (returns all zeros); used to disable the RBF contribution.

        :param r: the radius
        :type r: np.ndarray
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: an array of zeros
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    def zeros_derivative(n: int, inds=None):
        """
        **LLM Docstring**

        Return a function computing the `n`-th radial derivative of the zero kernel.

        :param n: the derivative order
        :type n: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the `n`-th derivative function
        :rtype: Callable
        """
        ...

    @staticmethod
    def zeros_singularity_handler(n: int, ndim: int, inds=None):
        """
        **LLM Docstring**

        Return a function giving the `r = 0` (singularity) value of the `n`-th derivative
        of the zero kernel in `ndim` dimensions.

        :param n: the derivative order
        :type n: int
        :param ndim: the spatial dimension
        :type ndim: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the singularity-handling function
        :rtype: Callable
        """
        ...

    @property
    def default_kernels(self):
        """
        **LLM Docstring**

        The registry mapping kernel names to their `{function, derivatives, zero_handler}`
        specs.

        :return: the kernel registry
        :rtype: dict
        """
        ...

    @staticmethod
    def morse(r, a=1, inds=None):
        """
        **LLM Docstring**

        A Morse-type radial basis kernel at radius `r`.

        :param r: the radius
        :type r: np.ndarray
        :param a: the range parameter
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the kernel values
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    def morse_derivative(n: int, inds=None):
        """
        **LLM Docstring**

        Return a function computing the `n`-th radial derivative of the Morse kernel.

        :param n: the derivative order
        :type n: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the `n`-th derivative function
        :rtype: Callable
        """
        ...

    @staticmethod
    def even_powers(r, o=1, inds=None):
        """
        **LLM Docstring**

        An even-power radial basis kernel (`r^(2o)` family) at radius `r`.

        :param r: the radius
        :type r: np.ndarray
        :param o: the power order
        :type o: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the kernel values
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    def even_powers_deriv(n: int, inds=None):
        """
        **LLM Docstring**

        Return a function computing the `n`-th radial derivative of the even-power kernel.

        :param n: the derivative order
        :type n: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the `n`-th derivative function
        :rtype: Callable
        """
        ...

    @staticmethod
    def laguerre(r, k=3, shift=2.29428, inds=None):
        """
        **LLM Docstring**

        A Laguerre-Gaussian radial basis kernel at radius `r`.

        :param r: the radius
        :type r: np.ndarray
        :param k: the Laguerre order
        :type k: int
        :param shift: the argument shift
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the kernel values
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    def laguerre_deriv(n: int, inds=None):
        """(-1)^n LaguerreL[k - n, n, x]"""
        ...

    @classmethod
    def compact_laguerre(cls, r, e=1, k=3, shift=2.29428, inds=None):
        """
        **LLM Docstring**

        A compactly-supported Laguerre radial basis kernel at radius `r`.

        :param r: the radius
        :type r: np.ndarray
        :param e: the shape/support parameter
        :param k: the Laguerre order
        :type k: int
        :param shift: the argument shift
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the kernel values
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def compact_laguerre_deriv(cls, n: int, inds=None):
        """
        **LLM Docstring**

        Return a function computing the `n`-th radial derivative of the compact-Laguerre kernel.

        :param n: the derivative order
        :type n: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the `n`-th derivative function
        :rtype: Callable
        """
        ...

    @property
    def default_auxiliary_bases(self):
        """
        **LLM Docstring**

        The registry mapping auxiliary-basis names to their `{function, derivatives}`
        specs.

        :return: the auxiliary-basis registry
        :rtype: dict
        """
        ...

    def _poly_exprs(self, ndim: int, order: int, deriv_order: int, monomials=True):
        """
        **LLM Docstring**

        Build (and cache) the symbolic polynomial basis expressions (and their
        derivatives up to `deriv_order`) for the auxiliary basis.

        :param ndim: the spatial dimension
        :type ndim: int
        :param order: the polynomial degree
        :type order: int
        :param deriv_order: the highest derivative order
        :type deriv_order: int
        :param monomials: use a monomial (vs outer-power) basis
        :type monomials: bool
        :return: the polynomial expressions per derivative order
        :rtype: list
        """
        ...

    def evaluate_poly_matrix(self, pts, degree, deriv_order=0, poly_origin=0.5, include_constant_term=True, monomials=True):
        """
        **LLM Docstring**

        Evaluate the auxiliary polynomial basis (and its derivatives) at a set of points
        relative to a polynomial origin, returning the polynomial block of the
        interpolation matrix.

        :param pts: the evaluation points
        :type pts: np.ndarray
        :param degree: the polynomial degree
        :type degree: int
        :param deriv_order: the highest derivative order
        :type deriv_order: int
        :param poly_origin: the origin the polynomials are centered on
        :param include_constant_term: include the constant term
        :type include_constant_term: bool
        :param monomials: use a monomial basis
        :type monomials: bool
        :return: the polynomial matrix block
        :rtype: np.ndarray
        """
        ...

    def _rbf_exprs(self, ndim, deriv_order, inds):
        """
        **LLM Docstring**

        Build (and cache) the symbolic RBF-kernel expressions (and their derivatives up
        to `deriv_order`) as functions of the point-to-center distance.

        :param ndim: the spatial dimension
        :type ndim: int
        :param deriv_order: the highest derivative order
        :type deriv_order: int
        :param inds: the coordinate indices
        :type inds: Sequence[int] | None
        :return: the RBF expressions per derivative order
        :rtype: list
        """
        ...

    def evaluate_rbf_matrix(self, pts, centers, inds, deriv_order=0, zero_tol=1e-08):
        """
        **LLM Docstring**

        Evaluate the RBF kernel (and its derivatives) between a set of points and the
        centers, handling the `r = 0` singularities via the kernel's zero-handler,
        returning the RBF block of the interpolation matrix.

        :param pts: the evaluation points
        :type pts: np.ndarray
        :param centers: the RBF centers
        :type centers: np.ndarray
        :param inds: the coordinate indices
        :type inds: np.ndarray
        :param deriv_order: the highest derivative order
        :type deriv_order: int
        :param zero_tol: the tolerance for treating a distance as zero
        :type zero_tol: float
        :return: the RBF matrix block
        :rtype: np.ndarray
        """
        ...
    poly_origin = 0.5

    def construct_matrix(self, pts, centers, inds, degree=0, deriv_order=0, zero_tol=1e-08, poly_origin=None, include_constant_term=True, force_square=False, monomials=True, multicentered_polys=False):
        """
        **LLM Docstring**

        Assemble the full interpolation matrix by concatenating the RBF block and the
        auxiliary polynomial block, optionally padding to a square system.

        :param pts: the evaluation points
        :type pts: np.ndarray
        :param centers: the RBF centers
        :type centers: np.ndarray
        :param inds: the coordinate indices
        :type inds: np.ndarray
        :param degree: the polynomial degree
        :type degree: int
        :param deriv_order: the highest derivative order
        :type deriv_order: int
        :param zero_tol: the zero-distance tolerance
        :type zero_tol: float
        :param poly_origin: the polynomial origin (defaults to the class value)
        :param include_constant_term: include the polynomial constant term
        :type include_constant_term: bool
        :param force_square: pad with extra polynomial rows to square the matrix
        :type force_square: bool
        :param monomials: use a monomial polynomial basis
        :type monomials: bool
        :param multicentered_polys: center the polynomials on each RBF center
        :type multicentered_polys: bool
        :return: the interpolation matrix
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    def svd_solve(a, b, svd_cutoff=1e-12):
        """
        **LLM Docstring**

        Solve a (possibly rank-deficient) linear system via a truncated SVD
        pseudo-inverse.

        :param a: the system matrix
        :type a: np.ndarray
        :param b: the right-hand side
        :type b: np.ndarray
        :param svd_cutoff: the singular-value truncation cutoff
        :type svd_cutoff: float
        :return: the solution
        :rtype: np.ndarray
        """
        ...

    def solve_system(self, centers, vals, derivs: list, inds, solver=None, return_data=False, error_threshold=None):
        """
        **LLM Docstring**

        Solve for the RBF-plus-polynomial interpolation weights that reproduce the values
        and derivatives at the centers, choosing the polynomial degree needed to make the
        system solvable.

        :param centers: the RBF centers
        :type centers: np.ndarray
        :param vals: the values at the centers
        :type vals: np.ndarray
        :param derivs: the derivative data at the centers
        :type derivs: list
        :param inds: the coordinate indices
        :type inds: np.ndarray
        :param solver: an explicit solver callable
        :type solver: Callable | None
        :param return_data: also return solver diagnostics
        :type return_data: bool
        :param error_threshold: the error threshold for rejecting a fit
        :type error_threshold: float | None
        :return: `(weights, degree, extra_shift, error)` (plus solver data if requested)
        :rtype: tuple
        """
        ...

    class InterpolationData:
        __slots__ = ['weights', 'centers', 'degree', 'scaling_data', 'extra_shift', 'interpolation_error', 'solver_data']

        def __init__(self, w, grid, degree, scaling_data, extra_shift=0, interpolation_error=0, solver_data=None):
            """
            **LLM Docstring**

            Hold the solved RBF interpolation weights and the data needed to evaluate them.

            :param w: the interpolation weights
            :param grid: the (renormalized) centers
            :type grid: np.ndarray
            :param degree: the auxiliary polynomial degree
            :type degree: int
            :param scaling_data: the renormalization data
            :type scaling_data: NeighborBasedInterpolator.RescalingData
            :param extra_shift: a constant value shift
            :param interpolation_error: the estimated interpolation error
            :param solver_data: optional solver diagnostics
            """
            ...

    def construct_evaluation_matrix(self, pts, data, deriv_order=0):
        """
        :param pts:
        :type pts:
        :param data:
        :type data:
        :param deriv_order:
        :type deriv_order:
        :return:
        :rtype:
        """
        ...

    def apply_interpolation(self, pts, data, inds, reshape_derivatives=True, return_data=False, deriv_order=0):
        """

        :param pts:
        :type pts:
        :param data:
        :type data:
        :param deriv_order:
        :type deriv_order:
        :return:
        :rtype:
        """
        ...

    def construct_interpolation(self, inds, solver_data=False, return_error=False):
        """
        **LLM Docstring**

        Build the RBF interpolation data for a neighborhood: renormalize it, solve for
        the weights, and wrap the result as an `InterpolationData`.

        :param inds: the neighbor indices
        :type inds: np.ndarray
        :param solver_data: also keep solver diagnostics
        :type solver_data: bool
        :param return_error: also return the interpolation error
        :type return_error: bool
        :return: the interpolation data
        :rtype: RBFDInterpolator.InterpolationData
        """
        ...

    class Interpolator(NeighborBasedInterpolator.Interpolator):
        parent: 'RBFDInterpolator'

        def matrix(self, pts, deriv_order=0):
            """
            **LLM Docstring**

            Build the RBF evaluation matrix for this neighborhood at a set of points.

            :param pts: the query points
            :type pts: np.ndarray
            :param deriv_order: the highest derivative order
            :type deriv_order: int
            :return: the evaluation matrix
            :rtype: np.ndarray
            """
            ...

class DistanceWeightedInterpolator(NeighborBasedInterpolator):
    """
    Provides a quick implementation of inverse distance weighted interpolation
    """

    class InterpolationData:
        __slots__ = ['centers']

        def __init__(self, grid):
            """
            **LLM Docstring**

            Hold the neighborhood centers used for distance-weighted interpolation.

            :param grid: the neighborhood centers
            :type grid: np.ndarray
            """
            ...

    def construct_interpolation(self, inds, solver_data=False, return_error=False):
        """
        **LLM Docstring**

        Build the distance-weighted interpolation data for a neighborhood (just its
        centers).

        :param inds: the neighbor indices
        :type inds: np.ndarray
        :param solver_data: unused
        :type solver_data: bool
        :param return_error: unused
        :type return_error: bool
        :return: the interpolation data
        :rtype: DistanceWeightedInterpolator.InterpolationData
        """
        ...

    def apply_weights(self, weights, inds, deriv_order=0, reshape_derivatives=False):
        """
        Weights the values and derivatives

        :param weights: npts x hood_size matrix of weights
        :type weights:
        :param inds: npts x hood_size set of indices for the values
        :type inds:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def get_weights(self, pts, data, inds):
        """
        Computes weights for pts from the inds

        :param pts:
        :type pts:
        :param inds:
        :type inds:
        :return:
        :rtype:
        """
        ...

    def apply_interpolation(self, pts, data, inds, deriv_order=0, reshape_derivatives=True, return_data=False):
        """
        :param pts:
        :type pts:
        :param data:
        :type data:
        :param deriv_order:
        :type deriv_order:
        :return:
        :rtype:
        """
        ...

class InverseDistanceWeightedInterpolator(DistanceWeightedInterpolator):

    @classmethod
    def weight_deriv(cls, disp, dists, norm, power, n, gammas_1=None):
        """
        **LLM Docstring**

        Compute the `n`-th-order contribution to the derivative of the inverse-distance
        weights with respect to the query point.

        :param disp: the point-to-center displacements
        :type disp: np.ndarray
        :param dists: the point-to-center distances
        :type dists: np.ndarray
        :param norm: the per-point weight normalization
        :type norm: np.ndarray
        :param power: the inverse-distance power
        :type power: float
        :param n: the derivative order
        :type n: int
        :param gammas_1: cached lower-order gamma terms
        :type gammas_1: np.ndarray | None
        :return: `(gammas, gradient_contribution)`
        :rtype: tuple
        """
        ...

    @classmethod
    def idw_derivs(cls, deriv_order, disp, dists, norm, power, weights):
        """
        **LLM Docstring**

        Compute the derivatives (up to `deriv_order`, currently ≤ 2) of the
        inverse-distance weights with respect to the query point.

        :param deriv_order: the highest derivative order
        :type deriv_order: int
        :param disp: the point-to-center displacements
        :type disp: np.ndarray
        :param dists: the point-to-center distances
        :type dists: np.ndarray
        :param norm: the weight normalization
        :type norm: np.ndarray
        :param power: the inverse-distance power
        :type power: float
        :param weights: the base weights
        :type weights: np.ndarray
        :return: the weight-derivative tensors
        :rtype: list
        :raises NotImplementedError: for `deriv_order > 2`
        """
        ...

    @classmethod
    def get_idw_weights(cls, pts, dists, disps=None, deriv_order=None, zero_tol=1e-06, power=2):
        """
        **LLM Docstring**

        Compute the normalized inverse-distance weights (and optionally their
        derivatives) for each query point, handling exact coincidences with a sample
        point specially.

        :param pts: the query points
        :type pts: np.ndarray
        :param dists: the point-to-neighbor distances
        :type dists: np.ndarray
        :param disps: the point-to-neighbor displacements (needed for derivatives)
        :type disps: np.ndarray | None
        :param deriv_order: the highest derivative order (weights only if `None`)
        :type deriv_order: int | None
        :param zero_tol: the coincidence tolerance
        :type zero_tol: float
        :param power: the inverse-distance power
        :type power: float
        :return: the weights (and their derivatives if requested)
        :rtype: np.ndarray | list
        """
        ...

    def get_weights(self, pts, dists, inds, zero_tol=1e-06, power=2):
        """
        **LLM Docstring**

        Compute the inverse-distance weights for a set of query points.

        :param pts: the query points
        :type pts: np.ndarray
        :param dists: the point-to-neighbor distances
        :type dists: np.ndarray
        :param inds: the neighbor indices
        :type inds: np.ndarray
        :param zero_tol: the coincidence tolerance
        :type zero_tol: float
        :param power: the inverse-distance power
        :type power: float
        :return: the weights
        :rtype: np.ndarray
        """
        ...

    def eval(self, pts, deriv_order=0, neighbors=None, merge_neighbors=None, reshape_derivatives=True, return_interpolation_data=False, check_in_sample=True, zero_tol=1e-08, return_error=False, use_cache=True, retries=None, max_distance=None, min_distance=None, neighborhood_clustering_radius=None, use_natural_neighbors=False, chunk_size=None, power=2, mode='fast'):
        """
        **LLM Docstring**

        Evaluate the inverse-distance-weighted interpolant (and derivatives) at a set of
        query points, combining neighbor weights with the stored values and derivatives.

        :param pts: the query points
        :type pts: np.ndarray
        :param deriv_order: the highest derivative order
        :type deriv_order: int
        :param neighbors: the neighbor count
        :type neighbors: int | None
        :param merge_neighbors: the group-merge threshold
        :type merge_neighbors: int | None
        :param reshape_derivatives: return full derivative tensors
        :type reshape_derivatives: bool
        :param return_interpolation_data: also return the interpolation data
        :type return_interpolation_data: bool
        :param check_in_sample: short-circuit points coinciding with samples
        :type check_in_sample: bool
        :param zero_tol: the coincidence tolerance
        :type zero_tol: float
        :param return_error: also return error estimates
        :type return_error: bool
        :param use_cache: reuse cached neighborhoods
        :type use_cache: bool
        :param retries: retries on failure
        :type retries: int | None
        :return: the values (and extras as requested)
        :rtype: np.ndarray | list | tuple
        """
        ...