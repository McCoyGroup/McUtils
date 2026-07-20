__all__ = ['marching_cubes']
from ... import Numputils as nput
import numpy as np
from .SphereUnionSurface import SphereUnionSurfaceMesh
'EDGE_TABLE data omitted from this build (256 items of type int, first 5: [0, 265, 515, 778, 1030] ... and 251 more)'
'TRI_TABLE data omitted from this build (256 items of type list, first 5: [[-1], [0, 8, 3, -1], [0, 1, 9, -1], [1, 8, 3, 9, 8, 1, -1], [1, 2, 10, -1]] ... and 251 more)'
EDGE_CORNERS = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
CORNER_OFFSETS = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]

def _interp(isovalue, p1, v1, p2, v2, zero_threshold=1e-10):
    """
    **LLM Docstring**

    Linearly interpolate the point on an edge where the field crosses the isovalue,
    falling back to the midpoint when the two endpoint values are nearly equal.

    :param isovalue: the isosurface value
    :type isovalue: float
    :param p1: the first edge endpoint
    :param v1: the field value at the first endpoint
    :type v1: float
    :param p2: the second edge endpoint
    :param v2: the field value at the second endpoint
    :type v2: float
    :param zero_threshold: the endpoint-value difference below which the midpoint is used
    :type zero_threshold: float
    :return: the interpolated crossing point
    :rtype: np.ndarray
    """
    ...

def _get_edge_vertex(ix, iy, iz, edge_idx, grid, verts, isovalue, position_tables, edge_cache):
    """
    **LLM Docstring**

    Return the vertex index for the isosurface crossing on a given cube edge,
    creating (and caching) the vertex the first time that edge is seen.

    :param ix: the cube's x index
    :type ix: int
    :param iy: the cube's y index
    :type iy: int
    :param iz: the cube's z index
    :type iz: int
    :param edge_idx: the local edge index (0-11)
    :type edge_idx: int
    :param grid: the scalar field
    :type grid: np.ndarray
    :param verts: the running vertex list (appended to)
    :type verts: list
    :param isovalue: the isosurface value
    :type isovalue: float
    :param position_tables: the per-axis world coordinate tables
    :param edge_cache: the `(ix,iy,iz,edge) -> vertex_index` cache
    :type edge_cache: dict
    :return: the vertex index
    :rtype: int
    """
    ...

def marching_cubes(grid, isovalue, spacing=(1.0, 1.0, 1.0), origin=(0.0, 0.0, 0.0), transformation=None, return_surface=True, return_normals=True):
    """Extract an isosurface from a scalar voxel grid.

    grid : array_like, shape (nx, ny, nz)
        Scalar field values. Axis order is (x, y, z).
    isovalue : float
        The scalar value of the isosurface to extract.
    spacing : (sx, sy, sz)
        Physical step size along each axis. Defaults to unit voxels.
    origin : (ox, oy, oz)
        World-space coordinate of grid point (0, 0, 0).
    """
    ...

def compute_normals(vertices, triangles, grid, spacing=(1, 1, 1), origin=(0, 0, 0)):
    """Estimate smooth per-vertex normals by interpolating the grid gradient.

    The gradient is computed with central differences on the scalar field and
    then sampled at each vertex position.
    """
    ...