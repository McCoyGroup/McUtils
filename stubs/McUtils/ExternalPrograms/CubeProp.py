from __future__ import annotations
import numpy as np
from ..Zachary import Interpolator, marching_cubes
from .Parsers import CubeFileParser
__all__ = ['CubePropEvaluator']

class CubePropEvaluator:

    def __init__(self, origin, axes, steps, values, base_data=None, **opts):
        """
        **LLM Docstring**

        Hold a volumetric grid property (a cube file's values on a parallelepiped grid)
        and set up lazy interpolation.

        :param origin: the grid origin
        :type origin: np.ndarray
        :param axes: the three grid axis vectors (rows)
        :type axes: np.ndarray
        :param steps: the number of grid points along each axis
        :type steps: Sequence[int]
        :param values: the flat grid values (reshaped to `steps`)
        :type values: np.ndarray
        :param base_data: the full parsed cube data, if available
        :param opts: interpolation options
        """
        ...

    @classmethod
    def from_file(cls, file, **interpolation_opts):
        """
        **LLM Docstring**

        Build a `CubePropEvaluator` by parsing a cube file.

        :param file: the cube file
        :type file: str
        :param interpolation_opts: interpolation options
        :return: the evaluator
        :rtype: CubePropEvaluator
        """
        ...

    @property
    def element_volume(self):
        """
        **LLM Docstring**

        The volume of one grid cell (the absolute determinant of the axis vectors),
        computed lazily.

        :return: the grid-cell volume
        :rtype: float
        """
        ...

    @classmethod
    def coords_from_grid(cls, origin, axes, steps):
        """
        **LLM Docstring**

        Build the Cartesian coordinates of every grid point from the origin, axis
        vectors, and step counts.

        :param origin: the grid origin
        :type origin: np.ndarray
        :param axes: the three grid axis vectors
        :type axes: np.ndarray
        :param steps: the number of grid points along each axis
        :type steps: Sequence[int]
        :return: the `(nx, ny, nz, 3)` coordinate array
        :rtype: np.ndarray
        """
        ...

    @property
    def grid_coords(self):
        """
        **LLM Docstring**

        The Cartesian coordinates of every grid point (computed lazily).

        :return: the grid coordinates
        :rtype: np.ndarray
        """
        ...

    def get_value_interpolator(self, steps, values, **interpolation_options):
        """
        **LLM Docstring**

        Build an interpolator over the grid values in (integer) grid-index space.

        :param steps: the number of grid points along each axis
        :type steps: Sequence[int]
        :param values: the grid values
        :type values: np.ndarray
        :param interpolation_options: interpolation options
        :return: the interpolator
        :rtype: Interpolator
        """
        ...

    @property
    def interpolator(self):
        """
        **LLM Docstring**

        The value interpolator over the grid (built lazily).

        :return: the interpolator
        :rtype: Interpolator
        """
        ...

    @property
    def inverse_axes(self):
        """
        **LLM Docstring**

        The inverse of the grid axis matrix (computed lazily), used to map Cartesian
        points into grid-index space.

        :return: the inverse axis matrix
        :rtype: np.ndarray
        """
        ...

    def embed_points(self, points):
        """
        **LLM Docstring**

        Map Cartesian points into (fractional) grid-index coordinates.

        :param points: the Cartesian points
        :type points: np.ndarray
        :return: the grid-index coordinates
        :rtype: np.ndarray
        """
        ...

    def unembed_points(self, points):
        """
        **LLM Docstring**

        Map (fractional) grid-index coordinates back into Cartesian space.

        :param points: the grid-index coordinates
        :type points: np.ndarray
        :return: the Cartesian points
        :rtype: np.ndarray
        """
        ...

    def evaluate(self, points):
        """
        **LLM Docstring**

        Interpolate the grid property at arbitrary Cartesian points.

        :param points: the Cartesian points
        :type points: np.ndarray
        :return: the interpolated values
        :rtype: np.ndarray
        """
        ...

    def get_isosurface(self, isoval, **opts):
        """
        **LLM Docstring**

        Extract an isosurface at the given value via marching cubes, transformed back
        into Cartesian coordinates.

        :param isoval: the isosurface value
        :type isoval: float
        :param opts: extra marching-cubes options
        :return: the isosurface mesh
        :rtype: object
        """
        ...