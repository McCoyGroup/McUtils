"""
Represents an n-dimensional grid, used by Interpolator and (eventually) FiniteDifferenceFunction to automatically
know what kind of data is fed in
"""
import numpy as np, enum
__all__ = ['Mesh', 'MeshType']

class MeshType(enum.Enum):
    Regular = 'regular'
    Structured = 'structured'
    Unstructured = 'unstructured'
    SemiStructured = 'semistructured'
    Indeterminate = 'indeterminate'

class MeshError(Exception):
    ...

class Mesh(np.ndarray):
    """
    A general Mesh class representing data points in n-dimensions
    in either a structured, unstructured, or semi-structured manner.
    Exists mostly to provides a unified interface to difference FD and Surface methods.
    """
    MeshError = MeshError
    MeshType = MeshType
    _allow_indeterminate = False

    def __new__(cls, data, mesh_type=None, allow_indeterminate=None):
        """
        :param griddata: the raw grid-point data the mesh uses
        :type griddata: np.ndarray
        :param mesh_type: the type of mesh we have
        :type mesh_type: None | str
        :param opts:
        :type opts:
        """
        ...

    def __init__(self, *args, **kwargs):
        """
        **LLM Docstring**

        No-op initializer; the real setup happens in `__new__` (as required for an
        `np.ndarray` subclass).

        :param args: ignored
        :param kwargs: ignored
        """
        ...

    def __array_finalize__(self, mesh):
        """
        **LLM Docstring**

        NumPy subclass hook: propagate (or infer) the mesh type and the
        `allow_indeterminate` flag onto a newly created view/copy, validating that an
        indeterminate mesh is only allowed when explicitly permitted.

        :param mesh: the source array being finalized from
        :raises MeshError: if the mesh type is indeterminate and that isn't allowed
        """
        ...

    @property
    def mesh_spacings(self):
        """
        **LLM Docstring**

        The per-axis grid spacings (computed and cached lazily).

        :return: the mesh spacings
        :rtype: np.ndarray | list
        """
        ...

    @property
    def subgrids(self):
        """
        **LLM Docstring**

        The per-axis subgrids for a regular or structured mesh (or `None` for
        unstructured meshes).

        :return: the subgrids, or `None`
        :rtype: list | None
        """
        ...

    @property
    def bounding_box(self):
        """
        **LLM Docstring**

        The `(min, max)` extent of the mesh along each coordinate.

        :return: the per-coordinate bounds
        :rtype: list[tuple]
        """
        ...

    @property
    def dimension(self):
        """Returns the dimension of the grid (not necessarily ndim)

        :return:
        :rtype: int
        """
        ...

    @property
    def npoints(self):
        """Returns the number of gridpoints in the mesh

        :return:
        :rtype: int
        """
        ...

    @property
    def gridpoints(self):
        """Returns the flattened set of gridpoints for a structured tensor grid and otherwise just returns the gridpoints

        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_npoints(cls, g):
        """Returns the number of gridpoints in the grid

        :param g:
        :type g: np.ndarray
        :return:
        :rtype: int
        """
        ...

    @classmethod
    def get_gridpoints(cls, g):
        """Returns the gridpoints in the grid

        :param g:
        :type g: np.ndarray
        :return:
        :rtype: int
        """
        ...

    @classmethod
    def get_mesh_subgrids(cls, grid, tol=None):
        """
        Returns the subgrids for a mesh
        :param grid:
        :type grid:
        :param tol:
        :type tol:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_mesh_spacings(cls, grid, tol=None):
        """
        **LLM Docstring**

        Compute the per-axis spacings of a grid as the unique rounded successive
        differences of each subgrid (or `None` if there are no subgrids).

        :param grid: the grid
        :type grid: np.ndarray
        :param tol: the rounding tolerance (decimal places)
        :type tol: int | None
        :return: the per-axis spacings
        :rtype: np.ndarray | list | None
        """
        ...

    @staticmethod
    def _is_meshgrid(grid):
        """
        Just checks if the shape of the grid
        is consistent with being a meshgrid
        :param grid:
        :type grid:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_mesh_type(cls, grid, check_product_grid=True, check_regular_grid=True, tol=None):
        """
        Determines what kind of grid we're working with

        :param grid:
        :type grid: np.ndarray
        :return: mesh_type
        :rtype: MeshType
        """
        ...

    @classmethod
    def RegularMesh(cls, *mesh_specs):
        """
        Builds a grid from multiple linspace arguments,
        basically insuring it's structured (if non-Empty)
        :param mesh_specs:
        :type mesh_specs:
        :return:
        :rtype:
        """
        ...