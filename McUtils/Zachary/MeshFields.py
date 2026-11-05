"""Scalar distance representations of closed triangle meshes."""
import numpy as np
from .. import Numputils as nput
from .ScalarFields import ScalarField

__all__ = ['MeshSignedDistanceField']


class MeshSignedDistanceField(ScalarField):
    """Negative-inside triangle distance, sampled in the mesh's coordinate units.

    Conversion is performed once. Interpolating the resulting ScalarFields
    changes their zero sets; it does not prescribe material-point transport.
    """
    representation = 'signed_distance'
    default_normal_direction = 'increasing'

    @staticmethod
    def _arrays(mesh):
        return nput.mesh_arrays(mesh.verts, mesh.inds) if hasattr(mesh, 'verts') else nput.mesh_arrays(*mesh)

    @classmethod
    def common_grid(cls, meshes, *, spacing=None, resolution=80, padding=None):
        arrays = [cls._arrays(mesh)[0] for mesh in meshes]
        if not arrays or any(not len(v) for v in arrays):
            raise ValueError('a distance grid requires nonempty meshes')
        low = np.min([v.min(axis=0) for v in arrays], axis=0)
        high = np.max([v.max(axis=0) for v in arrays], axis=0)
        if spacing is None:
            if int(resolution) != resolution or resolution < 10:
                raise ValueError('resolution must be an integer of at least ten')
            spacing = (high-low).max()/(resolution-7)
        spacing = np.broadcast_to(np.asarray(spacing, float), (3,)).copy()
        if not np.all(np.isfinite(spacing)) or np.any(spacing <= 0):
            raise ValueError('grid spacing must be finite and positive')
        padding = 3*spacing if padding is None else np.broadcast_to(np.asarray(padding, float), (3,))
        if not np.all(np.isfinite(padding)) or np.any(padding <= 0):
            raise ValueError('grid padding must be finite and positive to provide an exterior band')
        origin = low-padding
        shape = np.ceil((high+padding-origin)/spacing).astype(int)+1
        return dict(origin=origin, axes=np.diag(spacing), shape=shape)

    def __init__(self, mesh, *, grid=None, spacing=None, resolution=80, padding=None,
                 coordinate_units=None, query_options=None, batch_size=65536):
        vertices, faces = self._arrays(mesh)
        options = {} if query_options is None else dict(query_options)
        query = mesh.distance_query(**options) if hasattr(mesh, 'distance_query') else nput.MeshDistanceQuery(vertices, faces, **options)
        if grid is None:
            grid = self.common_grid([mesh], spacing=spacing, resolution=resolution, padding=padding)
        elif isinstance(grid, ScalarField):
            if coordinate_units is None:
                coordinate_units = grid.coordinate_units
            grid = dict(origin=grid.origin, axes=grid.axes, shape=grid.steps)
        origin = np.asarray(grid['origin'], float); axes = np.asarray(grid['axes'], float)
        raw_shape = np.asarray(grid['shape'])
        if (raw_shape.shape != (3,) or not np.all(np.isfinite(raw_shape)) or np.any(raw_shape != raw_shape.astype(int))
                or np.any(raw_shape < 2)):
            raise ValueError('distance grid shape must contain three integers of at least two')
        shape = raw_shape.astype(int)
        if origin.shape != (3,) or axes.shape != (3,3) or not np.all(np.isfinite(origin)) or not np.all(np.isfinite(axes)) or np.linalg.matrix_rank(axes) != 3:
            raise ValueError('distance grid requires finite origin and nonsingular axes')
        if int(batch_size) != batch_size or batch_size < 1:
            raise ValueError('batch_size must be a positive integer')
        embedded = (vertices-origin) @ np.linalg.inv(axes)
        if np.any(embedded < -1.e-9) or np.any(embedded > shape-1+1.e-9):
            raise ValueError('distance grid does not enclose the input mesh')
        if np.any(embedded <= 1.e-10) or np.any(embedded >= shape-1-1.e-10):
            raise ValueError('distance grid needs an exterior band around the mesh')
        count = int(np.prod(shape)); values = np.empty(count)
        for start in range(0, count, batch_size):
            index = np.arange(start, min(count, start+batch_size))
            indices = np.column_stack(np.unravel_index(index, tuple(shape)))
            values[start:start+len(index)] = query.signed_distance(indices @ axes + origin)
        super().__init__(values.reshape(tuple(shape)), origin=origin, axes=axes,
                         coordinate_units=coordinate_units, order=1)
        self.mesh = mesh
        self.mesh_query = query

    @classmethod
    def from_meshes(cls, meshes, *, grid=None, spacing=None, resolution=80, padding=None, **options):
        meshes = list(meshes)
        if grid is None:
            grid = cls.common_grid(meshes, spacing=spacing, resolution=resolution, padding=padding)
        return [cls(mesh, grid=grid, **options) for mesh in meshes]

    def isosurface(self, isovalue=0., **options):
        options.setdefault('normal_direction', 'increasing')
        return super().isosurface(isovalue, **options)
