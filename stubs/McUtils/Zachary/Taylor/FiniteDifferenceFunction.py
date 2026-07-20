"""
Provides a general, convenient FiniteDifferenceFunction class to handle all of our difference FD imps
"""
import numpy as np, scipy.sparse as sparse, math
from ..Mesh import Mesh, MeshType
__reload_hook__ = ['..Mesh']
__all__ = ['FiniteDifferenceFunction', 'FiniteDifferenceError', 'finite_difference', 'FiniteDifference1D', 'RegularGridFiniteDifference', 'IrregularGridFiniteDifference', 'FiniteDifferenceData', 'FiniteDifferenceMatrix']

class FiniteDifferenceError(Exception):
    ...

class FiniteDifferenceFunction:
    """
    The FiniteDifferenceFunction encapsulates a bunch of functionality extracted from [Fornberger's
    Calculation of Wieghts in Finite Difference Formulas](https://epubs.siam.org/doi/pdf/10.1137/S0036144596322507)

    Only applies to direct product grids, but each subgrid can be regular or irregular.
    Used in a large number of other places, but relatively rarely on its own.
    A convenient application is the `FiniteDifferenceDerivative` class in the `Derivatives` module.
    """
    __props__ = ('mesh_spacing', 'accuracy', 'stencil', 'end_point_accuracy', 'axes', 'contract')

    def __init__(self, *diffs, axes=0, contract=False):
        """Constructs an object to take finite differences derivatives of grids of data

        :param diffs: A set of differences to take along successive axes in the data
        :type diffs: FiniteDifference1D
        :param axes: The axes to take the specified differences along
        :type axes: int | Iterable[int]
        :param contract: Whether to reduce the shape of the returned tensor if applicable after application
        :type contract: bool
        """
        ...

    def apply(self, vals, axes=None, mesh_spacing=None, contract=None):
        """
        Iteratively applies the stored finite difference objects to the vals

        :param vals: The tensor of values to take the difference on
        :type vals: np.ndarray
        :param axes: The axis or axes to take the differences along (defaults to `self.axes`)
        :type axes: int | Iterable[int]
        :return: The tensor of derivatives
        :rtype: np.ndarray
        """
        ...

    def __call__(self, vals, axes=None, mesh_spacing=None):
        """
        **LLM Docstring**

        Apply the finite-difference weights to a set of values (delegates to `apply`).

        :param vals: the values on the grid
        :type vals: np.ndarray
        :param axes: the axes to difference along
        :param mesh_spacing: the grid spacing(s)
        :return: the finite-difference derivative
        :rtype: np.ndarray
        """
        ...

    @property
    def order(self):
        """
        :return: the order of the derivative requested
        :rtype: tuple[int]
        """
        ...

    @property
    def weights(self):
        """
        :return: the weights for the specified stencil
        :rtype: tuple[np.array[float]]
        """
        ...

    @property
    def widths(self):
        """
        :return: the number of points in each dimension, left and right, for the specified stencil
        :rtype: tuple[(int, int)]
        """
        ...

    @classmethod
    def regular_difference(cls, order, mesh_spacing=None, accuracy=2, stencil=None, end_point_accuracy=2, axes=0, contract=True, **kwargs):
        """
        Constructs a `FiniteDifferenceFunction` appropriate for a _regular grid_ with the given stencil

        :param order: the order of the derivative
        :type order: tuple[int]
        :param mesh_spacing: the spacing between grid points in the regular grid `h`
        :type mesh_spacing: None | float | tuple[float]
        :param accuracy: the accuracy of the derivative that we'll try to achieve as a power on `h`
        :type accuracy: None | int | tuple[int]
        :param stencil: the stencil to use for the derivative (overrides `accuracy`)
        :type stencil: None | int | tuple[int]
        :param end_point_accuracy: the amount of extra accuracy to use at the edges of the grid
        :type end_point_accuracy: None | int | tuple[int]
        :param axes: the axes of the passed array for the derivative to be applied along
        :type axes: None | int | tuple[int]
        :param contract: whether to eliminate any axes of size `1` from the results
        :type contract: bool
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def from_grid(cls, grid, order, accuracy=2, stencil=None, end_point_accuracy=2, axes=0, contract=True, allow_irregular=False, **kwargs):
        """
        Constructs a `FiniteDifferenceFunction` from a grid and order.
         Deconstructs the grid into its subgrids and builds a different differencer for each dimension

        :param grid: The grid to use as input data when defining the derivative
        :type grid: np.ndarray
        :param order: order of the derivative to compute
        :type order: int or list of ints
        :param stencil: number of points to use in the stencil
        :type stencil: int or list of ints
        :return: deriv func
        :rtype: FiniteDifferenceFunction
        """
        ...

class FiniteDifference1D:
    """
    A one-dimensional finite difference derivative object.
    Higher-dimensional derivatives are built by chaining these.
    """

    def __init__(self, finite_difference_data, matrix):
        """
        **LLM Docstring**

        Hold a 1-D finite-difference specification and its associated matrix.

        :param finite_difference_data: the weights/widths/order data
        :type finite_difference_data: FiniteDifferenceData
        :param matrix: the associated finite-difference matrix
        :type matrix: FiniteDifferenceMatrix
        """
        ...

    @property
    def order(self):
        """
        **LLM Docstring**

        The derivative order.

        :return: the order
        :rtype: int
        """
        ...

    @property
    def weights(self):
        """
        **LLM Docstring**

        The finite-difference weights (left, center, right).

        :return: the weights
        :rtype: tuple
        """
        ...

    @property
    def widths(self):
        """
        **LLM Docstring**

        The stencil widths (left, center, right).

        :return: the widths
        :rtype: tuple
        """
        ...
    only_odd_orders = False

    @classmethod
    def get_stencil(cls, order, stencil, accuracy, only_odd_orders=None):
        """
        **LLM Docstring**

        Compute the stencil size (number of points minus one) for a derivative order and
        accuracy, optionally forcing an odd number of points.

        :param order: the derivative order
        :type order: int
        :param stencil: an explicit stencil size (derived from order+accuracy if omitted)
        :type stencil: int | None
        :param accuracy: the requested accuracy order
        :type accuracy: int
        :param only_odd_orders: force an odd stencil
        :type only_odd_orders: bool | None
        :return: the stencil size
        :rtype: int
        """
        ...

    def apply(self, vals, val_dim=None, axis=0, mesh_spacing=None, check_shape=True):
        """
        Applies the held `FiniteDifferenceMatrix` to the array of values

        :param vals: values to do the difference over
        :type vals: np.ndarray | sparse.csr_matrix
        :param val_dim: dimensions of the vals
        :type val_dim: int
        :param axis: the axis to apply along
        :type axis: int | tuple[int]
        :param mesh_spacing: the mesh spacing for the weights
        :type mesh_spacing: float
        :return:
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    def sparse_tensordot(sparse, mat, axis):
        """Not sure how fast this will be, but does a very simple contraction of `mat` along `axis` by the final axis of `sparse`

        Heavily de-generalized from here: https://github.com/pydata/sparse/blob/9dc40e15a04eda8d8efff35dfc08950b4c07a810/sparse/_coo/common.py
        :param sparse:
        :type sparse: sparse.sparsemat
        :param mat:
        :type mat: np.ndarray
        :param axis:
        :type axis:
        :return:
        :rtype:
        """
        ...

class RegularGridFiniteDifference(FiniteDifference1D):
    """
    Defines a 1D finite difference over a regular grid
    """
    only_odd_orders = True

    def __init__(self, order, stencil=None, accuracy=4, end_point_accuracy=2, only_odd_orders=None, **kw):
        """

        :param order: the order of the derivative to take
        :type order: int
        :param stencil: the number of stencil points to add
        :type stencil: int | None
        :param accuracy: the approximate accuracy to target with the method
        :type accuracy: int | None
        :param end_point_accuracy: the extra number of stencil points to add to the end points
        :type end_point_accuracy: int | None
        :param kw: options passed through to the `FiniteDifferenceMatrix`
        :type kw:
        """
        ...

    @classmethod
    def finite_difference_data(cls, order, stencil, end_point_precision):
        """Builds a FiniteDifferenceData object from an order, stencil, and end_point_precision

        :param order:
        :type order:
        :param stencil:
        :type stencil:
        :param end_point_precision:
        :type end_point_precision:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def get_weights(m, s, n):
        """Extracts the weights for an evenly spaced grid

        :param m:
        :type m:
        :param s:
        :type s:
        :param n:
        :type n:
        :return:
        :rtype:
        """
        ...

class IrregularGridFiniteDifference(FiniteDifference1D):
    """
    Defines a finite difference over an irregular grid
    """

    def __init__(self, grid, order, stencil=None, accuracy=2, end_point_accuracy=2, **kw):
        """

        :param grid: the grid to get the weights from
        :type grid: np.ndarray
        :param order: the order of the derivative to take
        :type order: int
        :param stencil: the number of stencil points to add
        :type stencil: int | None
        :param accuracy: the approximate accuracy to target with the method
        :type accuracy: int | None
        :param end_point_accuracy: the extra number of stencil points to add to the end points
        :type end_point_accuracy: int | None
        :param kw: options passed through to the `FiniteDifferenceMatrix`
        :type kw:
        """
        ...

    @staticmethod
    def get_grid_slices(grid, stencil):
        """

        :param grid:
        :type grid:
        :param stencil:
        :type stencil:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def get_weights(m, z, x):
        """Extracts the grid weights for an unevenly spaced grid based off of the algorithm outlined by
        Fronberger in https://pdfs.semanticscholar.org/8bf5/912bde884f6bd4cfb4991ba3d077cace94c0.pdf

        :param m: highest derivative order
        :type m:
        :param z: center of the derivatives
        :type z:
        :param X: grid of points
        :type X:
        """
        ...

    @classmethod
    def finite_difference_data(cls, grid, order, stencil, end_point_precision):
        """Constructs a finite-difference function that computes the nth derivative with a given width

                :param deriv:
                :type deriv:
                :param accuracy:
                :type accuracy:
                :return:
                :rtype:
                """
        ...

class FiniteDifferenceData:
    """
    Holds the data used by to construct a finite difference matrix
    """

    def __init__(self, weights, widths, order):
        """
        **LLM Docstring**

        Hold the (cleaned) finite-difference weights, widths, and derivative order.

        :param weights: the left/center/right weight lists
        :param widths: the stencil widths
        :param order: the derivative order
        :type order: int
        """
        ...

    @property
    def weights(self):
        """
        **LLM Docstring**

        The finite-difference weights.

        :return: the weights
        :rtype: tuple
        """
        ...

    @property
    def widths(self):
        """
        **LLM Docstring**

        The stencil widths.

        :return: the widths
        :rtype: tuple
        """
        ...

    @property
    def order(self):
        """
        **LLM Docstring**

        The derivative order.

        :return: the order
        :rtype: int
        """
        ...

    @classmethod
    def _clean_coeffs(cls, cfs):
        """
        **LLM Docstring**

        Validate that the weights are supplied as a `(left, center, right)` triple.

        :param cfs: the weights
        :return: the validated weights
        :raises TypeError: if not a left/center/right triple
        """
        ...

    @classmethod
    def _clean_order(cls, order):
        """
        **LLM Docstring**

        Validate that the derivative order is an integer.

        :param order: the order
        :return: the validated order
        :rtype: int
        :raises TypeError: if not an int
        """
        ...

    @classmethod
    def _clean_widths(cls, ws):
        """
        **LLM Docstring**

        Normalize the stencil widths into `(left, right)` integer pairs (recursively for
        nested specifications).

        :param ws: the widths
        :return: the normalized widths
        :rtype: tuple
        """
        ...

class FiniteDifferenceMatrix:
    """
    Defines a matrix that can be applied to a regular grid of values to take a finite difference
    """

    def __init__(self, finite_difference_data, npts=None, mesh_spacing=None, only_core=False, only_center=False, mode='sparse', dtype='float64'):
        """
        :param finite_difference_data:
        :type finite_difference_data: FiniteDifferenceData
        :param npts:
        :type npts:
        :param mesh_spacing:
        :type mesh_spacing:
        :param only_core:
        :type only_core:
        :param only_center:
        :type only_center:
        :param mode:
        :type mode:
        """
        ...

    @property
    def weights(self):
        """
        **LLM Docstring**

        The finite-difference weights backing the matrix.

        :return: the weights
        :rtype: tuple
        """
        ...

    @property
    def order(self):
        """
        **LLM Docstring**

        The derivative order.

        :return: the order
        :rtype: int
        """
        ...

    @property
    def npts(self):
        """
        **LLM Docstring**

        The number of grid points the matrix spans. Setting it invalidates the cached
        matrix.

        :return: the number of points
        :rtype: int
        """
        ...

    @npts.setter
    def npts(self, val):
        """
        **LLM Docstring**

        The number of grid points the matrix spans. Setting it invalidates the cached
        matrix.

        :return: the number of points
        :rtype: int
        """
        ...

    @property
    def mesh_spacing(self):
        """
        **LLM Docstring**

        The grid spacing. Setting it invalidates the cached matrix.

        :return: the mesh spacing
        :rtype: float
        """
        ...

    @mesh_spacing.setter
    def mesh_spacing(self, val):
        """
        **LLM Docstring**

        The grid spacing. Setting it invalidates the cached matrix.

        :return: the mesh spacing
        :rtype: float
        """
        ...

    @property
    def only_core(self):
        """
        **LLM Docstring**

        Whether to build only the core (non-boundary) rows. Setting it invalidates the
        cached matrix.

        :return: the flag
        :rtype: bool
        """
        ...

    @only_core.setter
    def only_core(self, val):
        """
        **LLM Docstring**

        Whether to build only the core (non-boundary) rows. Setting it invalidates the
        cached matrix.

        :return: the flag
        :rtype: bool
        """
        ...

    @property
    def only_center(self):
        """
        **LLM Docstring**

        Whether to build only the single centered row. Setting it invalidates the cached
        matrix.

        :return: the flag
        :rtype: bool
        """
        ...

    @only_center.setter
    def only_center(self, val):
        """
        **LLM Docstring**

        Whether to build only the single centered row. Setting it invalidates the cached
        matrix.

        :return: the flag
        :rtype: bool
        """
        ...

    @property
    def mode(self):
        """
        **LLM Docstring**

        The storage mode (`'dense'` or `'sparse'`). Setting it invalidates the cached
        matrix.

        :return: the mode
        :rtype: str
        """
        ...

    @mode.setter
    def mode(self, val):
        """
        **LLM Docstring**

        The storage mode (`'dense'` or `'sparse'`). Setting it invalidates the cached
        matrix.

        :return: the mode
        :rtype: str
        """
        ...

    @property
    def dtype(self):
        """
        **LLM Docstring**

        The matrix dtype. Setting it invalidates the cached matrix.

        :return: the dtype
        """
        ...

    @dtype.setter
    def dtype(self, val):
        """
        **LLM Docstring**

        The matrix dtype. Setting it invalidates the cached matrix.

        :return: the dtype
        """
        ...

    @property
    def matrix(self):
        """
        **LLM Docstring**

        The finite-difference matrix (built and cached lazily).

        :return: the matrix
        :rtype: np.ndarray | sparse matrix
        """
        ...

    def fd_matrix(self):
        """Builds a 1D finite difference matrix for a set of boundary weights, central weights, and num of points
        Will look like:
            b1 b2 b3 ...
            w1 w2 w3 ...
            0  w1 w2 w3 ...
            0  0  w1 w2 w3 ...
                 ...
                 ...
                 ...
                    .... b3 b2 b1
        :return: fd_mat
        :rtype: np.ndarray | sp.csr_matrix
        """
        ...

    @classmethod
    def _fdm_irregular(cls, c_left, c_center, c_right, npts, only_core, only_center, mode, dtype):
        """
        **LLM Docstring**

        Build the finite-difference matrix for an irregular grid, where the boundary,
        core, and (optionally) center-only rows carry per-position weight lists.

        :param c_left: the left-boundary weights
        :param c_center: the core (per-row) weights
        :param c_right: the right-boundary weights
        :param npts: the number of grid points
        :type npts: int
        :param only_core: build only the core rows
        :type only_core: bool
        :param only_center: build only the centered row
        :type only_center: bool
        :param mode: `'dense'` or `'sparse'`
        :type mode: str
        :param dtype: the matrix dtype
        :return: the finite-difference matrix
        :rtype: np.ndarray | sparse matrix
        """
        ...

    @classmethod
    def _fdm_regular(cls, c_left, c_center, c_right, npts, only_core, only_center, mode, dtype):
        """
        **LLM Docstring**

        Build the finite-difference matrix for a regular grid, stacking the
        left-boundary, core (banded), and right-boundary blocks.

        :param c_left: the left-boundary weights
        :param c_center: the core weights
        :param c_right: the right-boundary weights
        :param npts: the number of grid points
        :type npts: int
        :param only_core: build only the core rows
        :type only_core: bool
        :param only_center: build only the centered row
        :type only_center: bool
        :param mode: `'dense'` or `'sparse'`
        :type mode: str
        :param dtype: the matrix dtype
        :return: the finite-difference matrix
        :rtype: np.ndarray | sparse matrix
        """
        ...

    @classmethod
    def _fdm_core(cls, a, n1, n2, side='l', mode='dense'):
        """
        **LLM Docstring**

        Build a banded (Toeplitz-style) core block of the finite-difference matrix by
        placing a weight vector along each row, either from the left or right side.

        :param a: the weight vector
        :param n1: the number of rows
        :type n1: int
        :param n2: the number of columns
        :type n2: int
        :param side: `'l'` or `'r'` (which side to anchor the band)
        :type side: str
        :param mode: `'dense'` or `'sparse'`
        :type mode: str
        :return: the banded block
        :rtype: np.ndarray | sparse matrix
        """
        ...

def finite_difference(grid, values, order, accuracy=2, stencil=None, end_point_accuracy=1, axes=None, only_core=False, only_center=False, dtype='float64', **kw):
    """Computes a finite difference derivative for the values on the grid

    :param grid: the grid of points for which the vlaues lie on
    :type grid: np.ndarray
    :param values: the values on the grid
    :type values: np.ndarray
    :param order: order of the derivative to compute
    :type order: int | Iterable[int]
    :param stencil: number of points to use in the stencil
    :type stencil: int | Iterable[int]
    :param accuracy: approximate accuracy of the derivative to request (overridden by `stencil`)
    :type accuracy: int | Iterable[int]
    :param end_point_accuracy: extra stencil points to use on the edges
    :type end_point_accuracy: int | Iterable[int]
    :param end_point_accuracy: extra stencil points to use on the edges
    :param axes: which axes to perform the successive derivatives over (defaults to the first _n_ axes)
    :type axes: int | Iterable[int]
    :param only_center: whether or not to only take the central value
    :type only_center: bool
    :param only_core: whether or not to avoid edge values where a different stencil would be used
    :type only_core: bool
    :return:
    :rtype:
    """
    ...