"""
Sets up a general Interpolator class that looks like Mathematica's InterpolatingFunction class
"""
import typing
import numpy as np, abc, enum, math
import scipy.interpolate as interpolate
import scipy.spatial as spat
from .Mesh import Mesh, MeshType
from .. import Numputils as nput
from .NeighborBasedInterpolators import *
__all__ = ['Interpolator', 'Extrapolator', 'RBFDInterpolator', 'InverseDistanceWeightedInterpolator', 'ProductGridInterpolator', 'UnstructuredGridInterpolator', 'CoordinateInterpolator']

class InterpolatorException(Exception):
    ...

class BasicInterpolator(metaclass=abc.ABCMeta):
    """
    Defines the abstract interface we'll need interpolator instances to satisfy so that we can use
    `Interpolator` as a calling layer
    """

    @abc.abstractmethod
    def __init__(self, grid, values, **opts):
        """
        **LLM Docstring**

        Abstract: build an interpolator from a grid and its values.

        :param grid: the sample grid
        :param values: the values at the grid points
        :param opts: implementation-specific options
        :raises NotImplementedError: always (abstract interface)
        """
        ...

    @abc.abstractmethod
    def __call__(self, points, **kwargs):
        """
        **LLM Docstring**

        Abstract: evaluate the interpolant at the given points.

        :param points: the query points
        :param kwargs: implementation-specific options
        :raises NotImplementedError: always (abstract interface)
        """
        ...

    @abc.abstractmethod
    def derivative(self, order):
        """
        Constructs the derivatives of the interpolator at the given order
        :param order:
        :type order:
        :return:
        :rtype: BasicInterpolator
        """
        ...

class ProductGridInterpolator(BasicInterpolator):
    """
    A set of interpolators that support interpolation
    on a regular (tensor product) grid
    """

    def __init__(self, grids, vals, caller=None, order=None, extrapolate=True, periodic=False, boundary_conditions=None):
        """
        :param grids:
        :type grids:
        :param points:
        :type points:
        :param caller:
        :type caller:
        :param order:
        :type order: int | Iterable[int]
        """
        ...

    @classmethod
    def get_base_spline(cls, grid, vals, order, periodic=False, boundary_conditions=None, extrapolate=False):
        """
        **LLM Docstring**

        Build a piecewise-polynomial (`PPoly`) spline of the given order along one grid
        axis, handling multi-valued data by splining each component and stacking.

        :param grid: the 1-D grid points
        :type grid: np.ndarray
        :param vals: the values at the grid points
        :type vals: np.ndarray
        :param order: the spline order
        :type order: int
        :param periodic: use periodic boundary conditions
        :type periodic: bool
        :param boundary_conditions: explicit spline boundary conditions
        :param extrapolate: allow extrapolation outside the grid
        :type extrapolate: bool
        :return: the piecewise-polynomial spline
        :rtype: interpolate.PPoly
        """
        ...

    @classmethod
    def construct_ndspline(cls, grids, vals, order, extrapolate=True, periodic=False, boundary_conditions=None):
        """
        Builds a tensor product ndspline by constructing a product of 1D splines

        :param grids: grids for each dimension independently
        :type grids: Iterable[np.ndarray]
        :param vals:
        :type vals: np.ndarray
        :param order:
        :type order: int | Iterable[int]
        :return:
        :rtype: interpolate.NdPPoly
        """
        ...

    def handle_periodicity(self, coords):
        """
        **LLM Docstring**

        Wrap query coordinates into the base period of each periodic axis so they land
        within the grid.

        :param coords: the query coordinates
        :type coords: np.ndarray
        :return: the wrapped coordinates
        :rtype: np.ndarray
        """
        ...

    def __call__(self, coords, *etc, **kwargs):
        """
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype: np.ndarray
        """
        ...

    def derivative(self, order):
        """
        :param order:
        :type order:
        :return:
        :rtype: ProductGridInterpolator
        """
        ...

class UnstructuredGridInterpolator(BasicInterpolator):
    """
    Defines an interpolator appropriate for totally unstructured grids by
    delegating to the scipy `RBF` interpolators
    """
    default_neighbors = 25

    def __init__(self, grid, values, order=None, neighbors=None, extrapolate=True, **opts):
        """
        :param grid:
        :type grid: np.ndarray
        :param values:
        :type values:  np.ndarray
        :param order:
        :type order: int
        :param neighbors:
        :type neighbors: int
        :param extrapolate:
        :type extrapolate: bool
        :param opts:
        :type opts:
        """
        ...

    def _member_q(self, points):
        """
        Checks if the points are in the interpolated convex hull
        in the case that we aren't extrpolating so we can return
        NaN for those points
        :param points:
        :type points:
        :return:
        :rtype:
        """
        ...

    def __call__(self, points):
        """
        **LLM Docstring**

        Evaluate the RBF interpolant, returning `NaN` outside the data's convex hull
        when extrapolation is disabled.

        :param points: the query points
        :type points: np.ndarray
        :return: the interpolated values
        :rtype: np.ndarray
        """
        ...

    def derivative(self, order):
        """
        Constructs the derivatives of the interpolator at the given order
        :param order:
        :type order:
        :return:
        :rtype: UnstructuredGridInterpolator
        """
        ...

class ExtrapolatorType(enum.Enum):
    Default = 'Automatic'
    Error = 'Raise'

class Interpolator:
    """
    A general purpose that takes your data and just interpolates it without whining or making you do a pile of extra work
    """
    DefaultExtrapolator = ExtrapolatorType.Default

    def __init__(self, grid, vals, interpolation_function=None, interpolation_order=None, extrapolator=None, extrapolation_order=None, **interpolation_opts):
        """
        :param grid: an unstructured grid of points **or** a structured grid of points **or** a 1D array
        :type grid: np.ndarray
        :param vals: the values at the grid points
        :type vals: np.ndarray
        :param interpolation_function: the basic function to be used to handle the raw interpolation
        :type interpolation_function: None | BasicInterpolator
        :param interpolation_order: the order of extrapolation to use (when applicable)
        :type interpolation_order: int | str | None
        :param extrapolator: the extrapolator to use for data points not on the grid
        :type extrapolator: Extrapolator | None | str | function
        :param extrapolation_order: the order of extrapolation to use by default
        :type extrapolation_order: int | str | None
        :param interpolation_opts: the options to be fed into the interpolating_function
        :type interpolation_opts:
        """
        ...

    @classmethod
    def get_interpolator(cls, grid, vals, interpolation_order=None, allow_extrapolation=True, **opts):
        """Returns a function that can be called on grid points to interpolate them

        :param grid:
        :type grid: Mesh
        :param vals:
        :type vals: np.ndarray
        :param interpolation_order:
        :type interpolation_order: int | str | None
        :param opts:
        :type opts:
        :return: interpolator
        :rtype: function
        """
        ...

    @classmethod
    def get_extrapolator(cls, grid, vals, extrapolation_order=1, **opts):
        """
        Returns an Extrapolator that can be called on grid points to extrapolate them

        :param grid:
        :type grid: Mesh
        :param extrapolation_order:
        :type extrapolation_order: int
        :return: extrapolator
        :rtype: Extrapolator
        """
        ...

    def apply(self, grid_points, **opts):
        """Interpolates then extrapolates the function at the grid_points

        :param grid_points:
        :type grid_points:
        :return:
        :rtype:
        """
        ...

    def derivative(self, order):
        """
        Returns a new function representing the requested derivative
        of the current interpolator

        :param order:
        :type order:
        :return:
        :rtype:
        """
        ...

    def __call__(self, *args, **kwargs):
        """
        **LLM Docstring**

        Evaluate the interpolant at the given points (delegates to `apply`).

        :param args: the query points
        :param kwargs: extra evaluation options
        :return: the interpolated values
        :rtype: np.ndarray
        """
        ...

class Extrapolator:
    """
    A general purpose that takes your data and just extrapolates it.
    This currently only exists in template format.
    """

    def __init__(self, extrapolation_function, warning=False, **opts):
        """
        :param extrapolation_function: the function to handle extrapolation off the interpolation grid
        :type extrapolation_function: None | function | Callable | Interpolator
        :param warning: whether to emit a message warning about extrapolation occurring
        :type warning: bool
        :param opts: the options to feed into the extrapolator call
        :type opts:
        """
        ...

    def derivative(self, n):
        """
        **LLM Docstring**

        Return an extrapolator for the `n`-th derivative of the wrapped extrapolation
        function.

        :param n: the derivative order
        :type n: int
        :return: the derivative extrapolator
        :rtype: Extrapolator
        """
        ...

    def find_extrapolated_points(self, gps, vals, extrap_value=np.nan):
        """
        Currently super rough heuristics to determine at which points we need to extrapolate
        :param gps:
        :type gps:
        :param vals:
        :type vals:
        :return:
        :rtype:
        """
        ...

    def apply(self, gps, vals, extrap_value=np.nan):
        """
        **LLM Docstring**

        Replace the values at the extrapolated (out-of-range) grid points with values
        from the extrapolation function.

        :param gps: the grid points
        :type gps: np.ndarray
        :param vals: the interpolated values (modified for the extrapolated points)
        :type vals: np.ndarray
        :param extrap_value: the sentinel marking points that need extrapolation
        :return: the values with extrapolated points filled in
        :rtype: np.ndarray
        """
        ...

    def __call__(self, *args, **kwargs):
        """
        **LLM Docstring**

        Apply the extrapolator (delegates to `apply`).

        :param args: positional arguments for `apply`
        :param kwargs: keyword arguments for `apply`
        :return: the values with extrapolated points filled in
        :rtype: np.ndarray
        """
        ...

class IncrementalCartesianCoordinateInterpolation:

    def __init__(self, abcissae, coords, *, coordinate_system, max_displacement_step=1.0, max_refinements=1, reembed=False, embedding_options=None):
        """
        **LLM Docstring**

        Set up an interpolator for a sequence of Cartesian geometries indexed by
        abcissae, working in an internal coordinate system and stepping between frames
        in bounded displacements.

        :param abcissae: the parameter values indexing the geometries
        :type abcissae: Sequence[float]
        :param coords: the Cartesian geometries
        :type coords: np.ndarray
        :param coordinate_system: the internal coordinate system to interpolate in
        :param max_displacement_step: the maximum internal displacement per refinement step
        :type max_displacement_step: float
        :param max_refinements: the maximum number of refinement steps per interval
        :type max_refinements: int
        :param reembed: Eckart-reembed each intermediate geometry
        :type reembed: bool
        :param embedding_options: options for the reembedding
        :type embedding_options: dict | None
        """
        ...

    @classmethod
    def wrap_convert(cls, system):
        """
        **LLM Docstring**

        Build a converter callable that converts a coordinate set into the given
        coordinate system.

        :param system: the target coordinate system
        :return: the converter callable
        :rtype: Callable
        """
        ...

    @classmethod
    def prep_coordinate_system_converter(cls, coordinate_system):
        """
        **LLM Docstring**

        Resolve a coordinate-system specification into a converter callable (defaulting
        to Cartesian, or wrapping a system that exposes `convert`).

        :param coordinate_system: the system, a converter, or `None`
        :return: the converter callable
        :rtype: Callable
        """
        ...

    @classmethod
    def refined_step_conv(cls, pct, converter, init_abc, final_abc, init_coords, final_coords, init_internals, final_internals, max_refinements=None, max_disp=0.5, reembed=False, embedding_options=None):
        """
        **LLM Docstring**

        Interpolate a fraction `pct` of the way between two frames in the internal
        coordinate system, subdividing the step whenever the internal displacement
        exceeds `max_disp` (and optionally reembedding), so the conversion back to
        Cartesians stays well-behaved.

        :param pct: the fractional position between the two frames
        :type pct: float
        :param converter: the Cartesian-to-internal converter
        :type converter: Callable
        :param init_abc: the starting abcissa
        :param final_abc: the ending abcissa
        :param init_coords: the starting Cartesian geometry
        :param final_coords: the ending Cartesian geometry
        :param init_internals: the starting internal coordinates
        :param final_internals: the ending internal coordinates
        :param max_refinements: the maximum number of refinement steps
        :type max_refinements: int | None
        :param max_disp: the maximum internal displacement per step
        :type max_disp: float
        :param reembed: Eckart-reembed each intermediate geometry
        :type reembed: bool
        :param embedding_options: options for the reembedding
        :type embedding_options: dict | None
        :return: `(interpolated_cartesians, (new_abcissae, new_coords, new_internals))`
        :rtype: tuple
        """
        ...

    def prep_cartesians(self, coords):
        """
        **LLM Docstring**

        Coerce a coordinate array into a list of `CoordinateSet` frames in the Cartesian
        system.

        :param coords: the coordinates
        :type coords: np.ndarray
        :return: the per-frame coordinate sets
        :rtype: list
        """
        ...

    def incremental_interp(self, start, point):
        """
        **LLM Docstring**

        Interpolate a single point lying in the interval starting at frame `start`,
        inserting the newly generated intermediate frames into the stored sequence.

        :param start: the index of the interval's starting frame
        :type start: int
        :param point: the abcissa to interpolate at
        :type point: float
        :return: the interpolated Cartesian geometry
        :rtype: np.ndarray
        """
        ...

    def interpolate(self, point):
        """
        **LLM Docstring**

        Interpolate the Cartesian geometry at each requested abcissa (sorting the
        queries so intermediate frames can be reused).

        :param point: the abcissa/abcissae to interpolate at
        :type point: np.ndarray
        :return: the interpolated geometries
        :rtype: np.ndarray
        """
        ...

    def __call__(self, point):
        """
        **LLM Docstring**

        Interpolate at the given abcissa/abcissae (delegates to `interpolate`).

        :param point: the abcissa/abcissae
        :type point: np.ndarray
        :return: the interpolated geometries
        :rtype: np.ndarray
        """
        ...

class CoordinateInterpolator:
    default_interpolator_type = IncrementalCartesianCoordinateInterpolation

    def __init__(self, coordinates, arc_lengths=None, distance_function=None, base_interpolator=None, coordinate_system=None, **interpolator_options):
        """
        **LLM Docstring**

        Interpolate a path of coordinates parametrized by (normalized) arc length,
        delegating the actual interpolation to a base interpolator.

        :param coordinates: the path coordinates
        :type coordinates: np.ndarray
        :param arc_lengths: explicit arc-length abcissae (computed if omitted)
        :type arc_lengths: np.ndarray | None
        :param distance_function: the inter-point distance function (or its name)
        :type distance_function: Callable | str | None
        :param base_interpolator: the interpolator type to use
        :param coordinate_system: the coordinate system to interpolate in
        :param interpolator_options: extra options for the base interpolator
        """
        ...

    @classmethod
    def euclidean_coordinate_distance(cls, p1, p2):
        """
        **LLM Docstring**

        The Euclidean distance between two coordinate frames.

        :param p1: the first frame
        :param p2: the second frame
        :return: the distance
        :rtype: float
        """
        ...

    @classmethod
    def lookup_distance_function(cls, distance_function):
        """
        **LLM Docstring**

        Resolve a distance-function name to its implementation.

        :param distance_function: the name (e.g. `'uniform'`)
        :type distance_function: str
        :return: the distance function
        :rtype: Callable
        """
        ...

    @classmethod
    def uniform_distance_function(cls, coords):
        """
        **LLM Docstring**

        Assign uniformly-spaced abcissae over `[0, 1]` regardless of the actual
        inter-point distances.

        :param coords: the path coordinates
        :type coords: np.ndarray
        :return: the uniform abcissae
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def get_arc_lengths(cls, coordinates: np.ndarray, arc_lengths=None, distance_function: 'typing.Callable[[np.ndarray, np.ndarray], float]'=None):
        """
        **LLM Docstring**

        Compute the normalized (`[0, 1]`) arc-length abcissae for a path, either from an
        explicit array, a named scheme, or by accumulating a distance function along the
        path.

        :param coordinates: the path coordinates
        :type coordinates: np.ndarray
        :param arc_lengths: explicit arc lengths (computed if omitted)
        :type arc_lengths: np.ndarray | None
        :param distance_function: the inter-point distance function (or its name)
        :type distance_function: Callable | str | None
        :return: `(distance_function, normalized_arc_lengths)`
        :rtype: tuple
        """
        ...

    def __call__(self, points, **etc):
        """
        **LLM Docstring**

        Evaluate the path at the given arc-length parameter(s).

        :param points: the arc-length parameter(s)
        :type points: np.ndarray
        :param etc: extra evaluation options
        :return: the interpolated coordinates
        :rtype: np.ndarray
        """
        ...