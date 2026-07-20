"""
Module that provides a FiniteDifferenceDerivative class that does finite-difference derivatives
"""
from .FiniteDifferenceFunction import FiniteDifferenceFunction
from ...Parallelizers import Parallelizer, SerialNonParallelizer
from ...Scaffolding import Logger, NullLogger
from ... import Numputils as nput
import numpy as np, itertools as it, scipy.sparse as sparse
__all__ = ['FiniteDifferenceDerivative']

class FiniteDifferenceDerivative:
    """
    Provides derivatives for a function (scalar or vector valued).
    Can be indexed into or the entire tensor of derivatives may be requested.
    The potential for optimization undoubtedly exists, but the idea is to provide as _simple_ an interface as possible.
    Robustification needs to be done, but is currently used in `CoordinateSystem.jacobian` to good effect.
    """
    __props__ = ('function_shape', 'displacement_function', 'prep', 'lazy', 'mesh_spacing', 'stencil', 'accuracy', 'cache_evaluations', 'parallelizer', 'logger')

    def __init__(self, f, function_shape=(0, 0), parallelizer=None, logger=None, **fd_opts):
        """
        :param f: the function we would like to take derivatives of
        :type f: FunctionSpec | callable
        :param function_shape: the shape of the function we'd like to take the derivatives of
        :type function_shape: Iterable[Iterable[int] | int] | None
        :param fd_opts: the options to pass to the finite difference function
        :type fd_opts:
        """
        ...

    def __call__(self, *args, **opts):
        """
        **LLM Docstring**

        Compute the requested finite-difference derivatives (delegates to
        `derivatives`).

        :param args: positional arguments for `derivatives`
        :param opts: keyword arguments for `derivatives`
        :return: the derivative tensors
        :rtype: object
        """
        ...

    def derivatives(self, center, displacement_function=None, prep=None, lazy=None, mesh_spacing=None, **fd_opts):
        """
        Generates a differencer object that can be used to get derivs however your little heart desires

        :param center: the center point around which to generate differences
        :type center: np.ndarray
        :param displacement_function:
        :type displacement_function:
        :param mesh_spacing:
        :type mesh_spacing:
        :param prep:
        :type prep:
        :param fd_opts:
        :type fd_opts:
        :return:
        :rtype:
        """
        ...

class FunctionSpec:
    """
    Defines a general spec that specifies a function, what it takes as coordinate inputs, and what the dimensions of what it outputs
    """

    def __init__(self, f, input_shape, output_shape):
        """

        :param f:
        :type f:
        :param input_shape: the shape of the array that should be passed in
        :type input_shape:
        :param output_shape:
        :type output_shape:
        """
        ...

    def __call__(self, *args, **kwargs):
        """
        **LLM Docstring**

        Evaluate the wrapped function.

        :param args: positional arguments for the function
        :param kwargs: keyword arguments for the function
        :return: the function value
        """
        ...

class DerivativeGenerator:
    """A that generates specified derivatives, currently by FD but can be generalized out to do it other ways

    The lower-level class that takes the entire high-level spec and converts it into derivatives.
    Allows indexing for memory efficiency
    """
    __props__ = ('displacement_function', 'prep', 'lazy', 'mesh_spacing', 'stencil', 'accuracy', 'cache_evaluations', 'parallelizer', 'logger')

    def __init__(self, f_spec, center, displacement_function=None, prep=None, lazy=False, mesh_spacing=0.001, cache_evaluations=True, parallelizer=None, logger=None, **fd_opts):
        """

        :param f_spec: The function to use when evaluating at the various displacements
        :type f_spec: FunctionSpec | function
        :param center: The position to evaluate the derivatives at
        :type center: np.ndarray
        :param displacement_function: The function to generate displacements
        :type displacement_function: FunctionSpec | function | None
        :param prep:
        :type prep: function | None
        :param mesh_spacing:
        :type mesh_spacing: float
        :param symmetric:
        :type symmetric:
        :param cache_evaluations: whether or not to cache function evaluations for reuse in other derivatives
        :type cache_evaluations: bool
        :param fd_opts:
        :type fd_opts:
        """
        ...

    def __getstate__(self):
        """
        **LLM Docstring**

        Return the picklable state, dropping the (unpicklable / regenerable) evaluation
        cache.

        :return: the state dict
        :rtype: dict
        """
        ...

    def __setstate__(self, state):
        """
        **LLM Docstring**

        Restore state from a pickled dict, reinitializing an empty evaluation cache.

        :param state: the state dict
        :type state: dict
        """
        ...

    @staticmethod
    def _default_displace(c, a):
        """
        **LLM Docstring**

        Default displacement callback: return the displacement for coordinate `c`,
        indexing into a per-coordinate array when one is given.

        :param c: the coordinate index
        :type c: int
        :param a: the displacement (scalar or per-coordinate)
        :return: the displacement for this coordinate
        :rtype: float
        """
        ...

    @staticmethod
    def _default_prep(c, a, b):
        """
        **LLM Docstring**

        Default preparation callback: pass the displacements and function values through
        unchanged.

        :param c: the derivative spec (unused)
        :param a: the displacements
        :param b: the function values
        :return: `(displacements, function_values)`
        :rtype: tuple
        """
        ...

    def _get_fdf(self, ci, mesh_spacing):
        """
        **LLM Docstring**

        Build (and cache) the `FiniteDifferenceFunction` for the derivative order implied
        by a coordinate spec and a mesh spacing, returning its stencil widths/shapes
        alongside it.

        :param ci: the coordinate spec
        :param mesh_spacing: the mesh spacing
        :return: `(stencil_widths, stencil_shapes, finite_difference, derivative_order)`
        :rtype: tuple
        :raises ValueError: if the weight/shape bookkeeping is inconsistent
        """
        ...

    def _coord_index(self, coord):
        """
        Converts the coordinate spec into a linear index

        :param coord:
        :type coord:
        :return:
        :rtype:
        """
        ...

    def _dorder(self, raveled):
        """Computes the derivative order requested from the coordinate indices requested

        :param raveled:
        :type raveled:
        :return:
        :rtype:
        """
        ...

    def get_displacement(self, coord, mesh_spacing=None):
        """
        Computes the displacement for the passed mesh spacing

        :param coord:
        :type coord:
        :param mesh_spacing:
        :type mesh_spacing:
        :return:
        :rtype:
        """
        ...

    def _build_displacement_array(self, coord, stencil_shapes, stencil_widths, displacement, use_sparse=False):
        """
        **LLM Docstring**

        Build the full tensor of coordinate displacements for a finite-difference
        stencil, scaling the base displacement of each coordinate by its stencil steps
        and broadcasting across the stencil grid.

        :param coord: the coordinate index tuples for this derivative
        :param stencil_shapes: the per-coordinate stencil shapes
        :param stencil_widths: the per-coordinate stencil widths
        :param displacement: the per-coordinate base displacements
        :param use_sparse: build a sparse displacement array
        :type use_sparse: bool
        :return: `(displacements, displacement_shape, mesh_spacings)`
        :rtype: tuple
        """
        ...

    def _get_displaced_coords(self, coord, stencil_widths, stencil_shapes, use_sparse=False):
        """
        Provides enough displacements of along `coord` to satisfy `stencil_widths` and `stencil_shapes`
        Does this by generating a big tensor of zeros, assigning parts of this for each displacement, then adding that

        :param coord:
        :type coord:
        :param stencil_widths:
        :type stencil_widths:
        :param stencil_shapes:
        :type stencil_shapes:
        :return:
        :rtype:
        """
        ...

    def _get_fd_data(self, specs):
        """
        Takes the specs and returns a generator that will create the appropriate derivatives along each coordinate
        I should add an optimization that allows displacements along single coordinates to happen fast...

        :param specs:
        :type specs:
        :param stencil_widths:
        :type stencil_widths:
        :param stencil_shapes:
        :type stencil_shapes:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def _get_diff(c, disp):
        """
        Gets the mesh spacing along coordinate c from the displaced coordinates...except there's basically no
        reason for this when I could instead _just save the number_

        :param c:
        :type c:
        :param disp:
        :type disp:
        :return:
        :rtype:
        """
        ...

    def _get_single_deriv(self, spec, disp_data, fd_data, return_coords):
        """
        **LLM Docstring**

        Compute a single derivative tensor: evaluate the function on the displaced
        coordinates (using the cache when enabled), reshape the values to the stencil
        grid, and contract them with the finite-difference weights.

        :param spec: the derivative spec (which coordinates, to what order)
        :param disp_data: `(disp_spec, displacements, displaced_coords, mesh_spacings)`
        :param fd_data: `(stencil_widths, stencil_shapes, finite_difference, order)`
        :param return_coords: also return the displaced coordinates
        :type return_coords: bool
        :return: the derivative tensor (and the displaced coords if requested)
        :rtype: np.ndarray | tuple
        """
        ...

    def _spec_derivs(self, specs, return_coords=False):
        """
        Computes a specific derivative
        The derivative is specified by repeating a coordinate the number of times we'd like its derivative:
            e.g. `[[0], [0]]` for $dx_1^2$ or `[[0], [N]]` for $dx_1dx_N$ if we have a function $f:R_N \rightarrow R$
                or `[[0, 1], [1, 0]]` for $dA_1_2dA_2_1$ if we have a function $f:(R_M, R_N) \rightarrow R$

        :param spec: the derivative to take as specified by the given indices
        :type spec: Iterable[Iterable[int]]
        :return:
        :rtype:
        """
        ...

    def _get_specs(self, order, pos=(), pos_filter=None, coordinates=None):
        """
        We compute the positions defined by the total order of the derivative as they would show up in the total tensor
        If a given block of derivatives is specified **[NOTE: I didn't finish this docstring and have no idea what it was supposed to say...]**

        :param order:
        :type order: int
        :param pos:
        :type pos: Iterable[int]
        :param coordinates:
        :type coordinates:
        :return:
        :rtype:
        """
        ...

    def _parallel_derivs(self, specs=None, parallelizer=None):
        """
        **LLM Docstring**

        Compute the derivative tensors in parallel by scattering the specs across
        workers and gathering/concatenating the results on the main process.

        :param specs: the derivative specs to compute
        :param parallelizer: the parallelization backend
        :return: the stacked derivative tensors (on the main process)
        :rtype: np.ndarray
        """
        ...

    def compute_derivatives(self, order, pos=(), coordinates=None, lazy=None, pos_filter=None, parallelizer=None):
        """
        Computes the derivatives up to `order` filtered by `pos` over the `coordinates`

        :param order: the maximum total order of the derivatives to calculate
        :type order: int | Iterable[int]
        :param pos: the positions to filter on
        :type pos:
        :param coordinates: the coordinates to compute the tensor of derivatives over
        :type coordinates: Iterable[int] | None
        :param lazy: whether or not to return a generator
        :type lazy: bool | None
        :return:
        :rtype:
        """
        ...

    def derivative_tensor(self, order, pos=(), coordinates=None, pos_filter=None, parallelizer=None, logger=None):
        """
        Computes a given derivative tensor

        :param order:
        :type order: int | Iterable[int]
        :param pos:
        :type pos:
        :param coordinates:
        :type coordinates:
        :return:
        :rtype:
        """
        ...

    def _idx(self, c, coord_shape=None):
        """
        **LLM Docstring**

        Convert flat coordinate indices into their multi-dimensional (unraveled) form.

        :param c: the flat indices
        :param coord_shape: the coordinate shape (defaults to the generator's)
        :return: the unraveled indices
        :rtype: np.ndarray
        """
        ...

    def _fidx(self, c, coord_shape=None):
        """
        **LLM Docstring**

        Convert multi-dimensional coordinate indices into flat (raveled) indices.

        :param c: the multi-dimensional indices
        :param coord_shape: the coordinate shape (defaults to the generator's)
        :return: the flat indices
        :rtype: np.ndarray
        """
        ...

    def __getitem__(self, item):
        """
        Returns a single derivative or block of derivatives, depending on how `item` is defined

        :param item: position spec
        :type item: int | tuple[int] | slice | tuple[int | slice]
        :return: derivs
        :rtype: float | np.ndarray
        """
        ...