from __future__ import annotations

import numpy as np
from ..Zachary import Interpolator, marching_cubes
from .Parsers import CubeFileParser

__all__ = [
    "CubePropEvaluator"
]

class CubePropEvaluator:
    def __init__(self, origin, axes, steps, values, base_data=None, **opts):
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
        with CubeFileParser(file) as parser:
            data = parser.parse()
        return cls(data.grid.origin, data.grid.axes, data.grid.steps, data.values, base_data=data, **interpolation_opts)

    @property
    def element_volume(self):
        if self._element_volume is None:
            self._element_volume = abs(np.linalg.det(self.axes))
        return self._element_volume

    @classmethod
    def coords_from_grid(cls, origin, axes, steps):
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
        if self._grid_coords is None:
            self._grid_coords = self.coords_from_grid(self.origin, self.axes, self.steps)
        return self._grid_coords

    def get_value_interpolator(self, steps, values, **interpolation_options):
        nx, ny, nz = steps
        i = np.arange(nx)
        j = np.arange(ny)
        k = np.arange(nz)
        ii, jj, kk = np.meshgrid(i, j, k, indexing="ij")
        return Interpolator(np.moveaxis(np.array([ii, jj, kk]), 0, -1), values, **interpolation_options)

    @property
    def interpolator(self):
        if self._interpolator is None:
            self._interpolator = self.get_value_interpolator(self.steps, self.values, **self.interpolation_opts)
        return self._interpolator

    @property
    def inverse_axes(self):
        if self._inverse is None:
            self._inverse = np.linalg.inv(self.axes)
        return self._inverse
    def embed_points(self, points):
        points = np.asarray(points)
        points = points - self.origin[np.newaxis]
        return points @ self.inverse_axes
    def unembed_points(self, points):
        return np.asarray(points) @ self.axes + self.origin[np.newaxis]

    def evaluate(self, points):
        return self.interpolator(self.embed_points(points))

    def get_isosurface(self, isoval, **opts):
        return marching_cubes(self.values, isoval,
                              transformation=self.unembed_points,
                              **opts)

