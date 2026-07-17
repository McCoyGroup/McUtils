from __future__ import annotations

import numpy as np
from ..Zachary import Interpolator, marching_cubes
from .Parsers import CubeFileParser

__all__ = [
    "CubePropEvaluator"
]

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
        self.origin = np.asanyarray(origin)
        self.axes = np.asanyarray(axes)
        self._inverse = None
        self._element_volume = None
        self.steps = np.asanyarray(steps, dtype=int)
        self.values = np.asanyarray(values).reshape(steps)
        self.base_data = base_data
        self._interpolator = None
        self._grid_coords = None
        self.interpolation_opts = opts

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
        with CubeFileParser(file) as parser:
            data = parser.parse()
        return cls(data.grid.origin, data.grid.axes, data.grid.steps, data.values, base_data=data, **interpolation_opts)

    @property
    def element_volume(self):
        """
        **LLM Docstring**

        The volume of one grid cell (the absolute determinant of the axis vectors),
        computed lazily.

        :return: the grid-cell volume
        :rtype: float
        """
        if self._element_volume is None:
            self._element_volume = abs(np.linalg.det(self.axes))
        return self._element_volume

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
        nx, ny, nz = steps
        i = np.arange(nx)
        j = np.arange(ny)
        k = np.arange(nz)
        ii, jj, kk = np.meshgrid(i, j, k, indexing="ij")
        coords = (
                origin
                + ii[..., np.newaxis] * axes[0]
                + jj[..., np.newaxis] * axes[1]
                + kk[..., np.newaxis] * axes[2]
        )
        return coords

    @property
    def grid_coords(self):
        """
        **LLM Docstring**

        The Cartesian coordinates of every grid point (computed lazily).

        :return: the grid coordinates
        :rtype: np.ndarray
        """
        if self._grid_coords is None:
            self._grid_coords = self.coords_from_grid(self.origin, self.axes, self.steps)
        return self._grid_coords

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
        nx, ny, nz = steps
        i = np.arange(nx)
        j = np.arange(ny)
        k = np.arange(nz)
        ii, jj, kk = np.meshgrid(i, j, k, indexing="ij")
        return Interpolator(np.moveaxis(np.array([ii, jj, kk]), 0, -1), values, **interpolation_options)

    @property
    def interpolator(self):
        """
        **LLM Docstring**

        The value interpolator over the grid (built lazily).

        :return: the interpolator
        :rtype: Interpolator
        """
        if self._interpolator is None:
            self._interpolator = self.get_value_interpolator(self.steps, self.values, **self.interpolation_opts)
        return self._interpolator

    @property
    def inverse_axes(self):
        """
        **LLM Docstring**

        The inverse of the grid axis matrix (computed lazily), used to map Cartesian
        points into grid-index space.

        :return: the inverse axis matrix
        :rtype: np.ndarray
        """
        if self._inverse is None:
            self._inverse = np.linalg.inv(self.axes)
        return self._inverse
    def embed_points(self, points):
        """
        **LLM Docstring**

        Map Cartesian points into (fractional) grid-index coordinates.

        :param points: the Cartesian points
        :type points: np.ndarray
        :return: the grid-index coordinates
        :rtype: np.ndarray
        """
        points = np.asarray(points)
        points = points - self.origin[np.newaxis]
        return points @ self.inverse_axes
    def unembed_points(self, points):
        """
        **LLM Docstring**

        Map (fractional) grid-index coordinates back into Cartesian space.

        :param points: the grid-index coordinates
        :type points: np.ndarray
        :return: the Cartesian points
        :rtype: np.ndarray
        """
        return np.asarray(points) @ self.axes + self.origin[np.newaxis]

    def evaluate(self, points):
        """
        **LLM Docstring**

        Interpolate the grid property at arbitrary Cartesian points.

        :param points: the Cartesian points
        :type points: np.ndarray
        :return: the interpolated values
        :rtype: np.ndarray
        """
        return self.interpolator(self.embed_points(points))

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
        return marching_cubes(self.values, isoval,
                              transformation=self.unembed_points,
                              **opts)