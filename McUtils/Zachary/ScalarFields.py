"""Sampled scalar fields on affine product grids.

Temporal interpolation is pointwise linear, on the same physical grid and in
the same coordinate units. It performs no resampling, normalization, or sign
alignment. Those operations must be requested separately by the caller.
"""
import base64
import numpy as np

from .Interpolator import ProductGridInterpolator

__all__ = ["ScalarField"]


class ScalarField:
    coordinate_units = None
    default_normal_direction = 'auto'

    def __init__(self, values, origin=None, axes=None, coordinate_units=None, **interpolation_options):
        values = np.asarray(values)
        if np.iscomplexobj(values):
            raise ValueError("ScalarField requires real scalar values")
        values = np.asarray(values, dtype=float)
        if values.ndim == 0 or any(n < 2 for n in values.shape) or not np.all(np.isfinite(values)):
            raise ValueError("ScalarField requires a finite grid with at least two points per axis")
        dimension = values.ndim
        origin = np.zeros(dimension) if origin is None else np.asarray(origin, dtype=float)
        axes = np.eye(dimension) if axes is None else np.asarray(axes, dtype=float)
        if (origin.shape != (dimension,) or axes.shape != (dimension, dimension)
                or not np.all(np.isfinite(origin)) or not np.all(np.isfinite(axes))):
            raise ValueError("origin and axes must describe the scalar grid's dimension")
        if np.linalg.matrix_rank(axes) != dimension:
            raise ValueError("ScalarField grid axes must be nonsingular")
        self.values, self.origin, self.axes = values, origin, axes
        self.steps = np.asarray(values.shape, dtype=int)
        self.coordinate_units = coordinate_units
        self.interpolation_opts = interpolation_options
        self._interpolator = None

    @property
    def inverse_axes(self):
        return np.linalg.inv(self.axes)

    @property
    def element_volume(self):
        return abs(np.linalg.det(self.axes))

    @staticmethod
    def coords_from_grid(origin, axes, steps):
        indices = np.moveaxis(np.indices(tuple(steps)), 0, -1)
        return indices @ axes + origin

    @property
    def grid_coords(self):
        return self.coords_from_grid(self.origin, self.axes, self.steps)

    def embed_points(self, points):
        return (np.asarray(points) - self.origin) @ self.inverse_axes

    def unembed_points(self, points):
        return np.asarray(points) @ self.axes + self.origin

    @property
    def interpolator(self):
        if self._interpolator is None:
            self._interpolator = ProductGridInterpolator(
                [np.arange(n) for n in self.steps], self.values, **self.interpolation_opts)
        return self._interpolator

    def evaluate(self, points):
        return self.interpolator(self.embed_points(points))

    __call__ = evaluate

    def require_compatible(self, other, *, atol=0., rtol=0.):
        if not isinstance(other, ScalarField):
            raise TypeError("field interpolation requires another ScalarField")
        if self.values.shape != other.values.shape:
            raise ValueError("scalar fields must have the same grid shape; resample explicitly first")
        if self.coordinate_units != other.coordinate_units:
            raise ValueError("scalar fields must use the same coordinate units")
        if not (np.allclose(self.origin, other.origin, atol=atol, rtol=rtol)
                and np.allclose(self.axes, other.axes, atol=atol, rtol=rtol)):
            raise ValueError("scalar fields must share the same physical grid; resample explicitly first")
        return other

    def interpolate(self, other, fraction, *, method="linear"):
        self.require_compatible(other)
        if method != "linear":
            raise ValueError("supported scalar-field interpolation method: 'linear'")
        fraction = float(fraction)
        if not np.isfinite(fraction) or not 0 <= fraction <= 1:
            raise ValueError("interpolation fraction must be finite and between zero and one")
        if fraction == 0:
            return self
        if fraction == 1:
            return other
        field = ScalarField((1 - fraction) * self.values + fraction * other.values,
                            origin=self.origin, axes=self.axes, coordinate_units=self.coordinate_units,
                            **self.interpolation_opts)
        if self.default_normal_direction == other.default_normal_direction:
            field.default_normal_direction = self.default_normal_direction
        return field

    def get_isosurface(self, isovalue, **options):
        if self.values.ndim != 3:
            raise ValueError("isosurface extraction requires a three-dimensional ScalarField")
        from .Surfaces.MarchingCubesSurface import marching_cubes
        return marching_cubes(self.values, isovalue, transformation=self.unembed_points, **options)

    def isosurface(self, isovalue, **options):
        from .Surfaces.ScalarFieldIsosurface import ScalarFieldIsosurface
        options.setdefault('normal_direction', self.default_normal_direction)
        return ScalarFieldIsosurface(self, isovalue, **options)

    def to_animation_data(self):
        """Lossless portable values; grid order is NumPy's C order (z fastest)."""
        if not np.all(np.isfinite(self.values)):
            raise ValueError("animated scalar fields must contain only finite values")
        return dict(shape=list(self.values.shape), origin=self.origin.tolist(), axes=self.axes.tolist(),
                    coordinate_units=self.coordinate_units, encoding="float64-le-base64",
                    values=base64.b64encode(np.asarray(self.values, dtype='<f8').tobytes()).decode('ascii'))
