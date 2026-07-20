import collections
import itertools
import numpy as np
import scipy.spatial
import scipy.spatial as spat
import scipy.sparse
import scipy.ndimage
from ... import Devutils as dev
from ... import Numputils as nput
from ... import Combinatorics as comb
from ...Data import AtomData, UnitsData
from ...ExternalPrograms import Open3DInterface as o3d
__all__ = ['sphere_points', 'SphereUnionSurface', 'SphereUnionSurfaceMesh']

def halton_sphere(npts, **etc):
    """
    **LLM Docstring**

    Generate quasi-random points on the unit sphere from a 2-D Halton sequence.

    :param npts: the number of points
    :type npts: int
    :param etc: extra options for the sequence generator
    :return: the sphere points
    :rtype: np.ndarray
    """
    ...

def sobol_sphere(npts, **etc):
    """
    **LLM Docstring**

    Generate quasi-random points on the unit sphere from a 2-D Sobol sequence.

    :param npts: the number of points
    :type npts: int
    :param etc: extra options for the sequence generator
    :return: the sphere points
    :rtype: np.ndarray
    """
    ...

def sphere_points(npts, center=None, radius=None, method='fibonacci', **etc):
    """
    **LLM Docstring**

    Generate points on a sphere by the named method, optionally scaled to a radius
    and translated to a center.

    :param npts: the number of points
    :type npts: int
    :param center: the sphere center
    :type center: np.ndarray | None
    :param radius: the sphere radius
    :type radius: float | None
    :param method: the generator (`'fibonacci'`, `'lebedev'`, `'halton'`, `'sobol'`, or a callable)
    :type method: str | Callable
    :param etc: extra options for the generator
    :return: the sphere points
    :rtype: np.ndarray
    :raises ValueError: for an unknown method name
    """
    ...

class SphereUnionSurface:
    default_samples = 50
    default_scaling = 1
    default_expansion = 0
    default_tolerance = 0.001

    def __init__(self, centers, radii, scaling=None, expansion=None, samples=None, density=None, tolerance=None, add_intersection_circles=False, **generator_options):
        """
        **LLM Docstring**

        Set up a surface defined by the union of spheres (e.g. atomic van-der-Waals
        spheres), deferring sample-point generation.

        :param centers: the sphere centers, shape `(n, 3)`
        :type centers: np.ndarray
        :param radii: the sphere radii, shape `(n,)`
        :type radii: np.ndarray
        :param scaling: a multiplicative radius scaling
        :type scaling: float | None
        :param expansion: an additive radius expansion
        :type expansion: float | None
        :param samples: the number of sample points per sphere
        :type samples: int | None
        :param density: sample points per unit area (overrides `samples`)
        :type density: float | None
        :param tolerance: the occlusion tolerance for exterior-point tests
        :type tolerance: float | None
        :param add_intersection_circles: seed extra points along sphere-sphere intersection circles
        :type add_intersection_circles: bool
        :param generator_options: extra options for the point generator
        """
        ...

    @classmethod
    def from_xyz(cls, atoms, positions, scaling=None, expansion=None, samples=None, tolerance=None, radius_property='IconRadius', distance_units='BohrRadius'):
        """
        **LLM Docstring**

        Build a `SphereUnionSurface` from atoms and positions, taking each sphere radius
        from an atomic radius property.

        :param atoms: the atom labels
        :type atoms: Sequence[str]
        :param positions: the atomic positions
        :type positions: np.ndarray
        :param scaling: a multiplicative radius scaling
        :type scaling: float | None
        :param expansion: an additive radius expansion
        :type expansion: float | None
        :param samples: the number of sample points per sphere
        :type samples: int | None
        :param tolerance: the occlusion tolerance
        :type tolerance: float | None
        :param radius_property: the `AtomData` property to use for the radii
        :type radius_property: str
        :param distance_units: the units to convert the radii into
        :type distance_units: str
        :return: the surface
        :rtype: SphereUnionSurface
        """
        ...

    @property
    def sampling_points(self):
        """
        **LLM Docstring**

        The (flattened) exterior sample points on the sphere union, generated lazily.
        Setting this overrides them.

        :return: the sample points
        :rtype: np.ndarray
        """
        ...

    @sampling_points.setter
    def sampling_points(self, pts):
        """
        **LLM Docstring**

        The (flattened) exterior sample points on the sphere union, generated lazily.
        Setting this overrides them.

        :return: the sample points
        :rtype: np.ndarray
        """
        ...

    @property
    def atom_sampling_points(self):
        """
        **LLM Docstring**

        The per-sphere lists of exterior sample points, generated lazily.

        :return: the per-sphere sample points
        :rtype: list
        """
        ...

    @classmethod
    def nearest_centers(cls, pts, centers, return_normals=False):
        """
        **LLM Docstring**

        For each point, find the index of the nearest sphere center, optionally also
        returning the distance and outward unit vector.

        :param pts: the query points
        :type pts: np.ndarray
        :param centers: the sphere centers
        :type centers: np.ndarray
        :param return_normals: also return the `(distances, unit_vectors)`
        :type return_normals: bool
        :return: the nearest-center indices (and normals if requested)
        :rtype: np.ndarray | tuple
        """
        ...

    @classmethod
    def sphere_project(cls, pts, centers, radii):
        """
        **LLM Docstring**

        Project each point radially onto the surface of its nearest sphere.

        :param pts: the points to project
        :type pts: np.ndarray
        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :return: the projected points
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def sphere_boundary_pruning(cls, pts, centers, min_component=None):
        """
        **LLM Docstring**

        Prune points that sit too close to a neighbouring sphere's point group,
        inferring the spacing cutoff from the per-group nearest-neighbour distribution
        when one isn't supplied.

        :param pts: the points
        :type pts: np.ndarray
        :param centers: the sphere centers
        :type centers: np.ndarray
        :param min_component: the minimum-allowed inter-group spacing (inferred if omitted)
        :type min_component: float | None
        :return: the pruned points
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def point_cloud_repulsion(cls, pts, centers, radii, min_displacement_cutoff=0.001, stochastic_factor=0.0001, force_constant=0.001, power=-3, max_iterations=15):
        """
        **LLM Docstring**

        Relax a point cloud on the sphere union by iterated inverse-power repulsion
        projected onto the local tangent plane, reprojecting onto the spheres each step
        (a simple electrostatic-style even-spreading).

        :param pts: the points
        :type pts: np.ndarray
        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param min_displacement_cutoff: stop once all repulsive forces fall below this
        :type min_displacement_cutoff: float
        :param stochastic_factor: magnitude of a random jitter added each step
        :type stochastic_factor: float
        :param force_constant: the repulsion strength
        :type force_constant: float
        :param power: the repulsion distance power
        :type power: float
        :param max_iterations: the maximum number of relaxation steps
        :type max_iterations: int
        :return: the relaxed points
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def adjust_point_cloud_density(self, pts, centers=None, radii=None, min_component=None, min_component_bins=30, min_component_scaling=0.7, same_point_cutoff=1e-06, max_iterations=15):
        """
        **LLM Docstring**

        Even out a point cloud's density by iteratively merging pairs of points that are
        closer than a spacing cutoff (re-projecting the merged point onto its nearest
        sphere when centers/radii are given), inferring the cutoff from the
        nearest-neighbour distribution.

        :param pts: the points
        :type pts: np.ndarray
        :param centers: the sphere centers (optional; needed with `radii` to reproject)
        :type centers: np.ndarray | None
        :param radii: the sphere radii
        :type radii: np.ndarray | None
        :param min_component: the merge distance cutoff (inferred if omitted)
        :type min_component: float | None
        :param min_component_bins: histogram bins used to infer the cutoff
        :type min_component_bins: int
        :param min_component_scaling: scaling applied to the inferred cutoff
        :type min_component_scaling: float
        :param same_point_cutoff: distance below which points are treated as duplicates
        :type same_point_cutoff: float
        :param max_iterations: the maximum number of merge iterations
        :type max_iterations: int
        :return: the adjusted points
        :rtype: np.ndarray
        :raises ValueError: if only one of centers/radii is given
        """
        ...

    @classmethod
    def get_exterior_points(cls, points, centers, radii, tolerance: float=0, vertex_map=None, intersection_point_mask=None, intersection_point_tolerance=None, return_components=False):
        """
        **LLM Docstring**

        Return a mask (or per-sphere components) of the points that lie outside (or on)
        every sphere, i.e. on the exterior surface of the union, within a tolerance.

        :param points: the query points
        :type points: np.ndarray
        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param tolerance: the fractional distance tolerance
        :type tolerance: float
        :param vertex_map: sphere index(es) each point belongs to, forced exterior
        :type vertex_map: np.ndarray | None
        :param intersection_point_mask: points to test with a looser tolerance
        :type intersection_point_mask: np.ndarray | None
        :param intersection_point_tolerance: the looser tolerance for those points
        :type intersection_point_tolerance: float | None
        :param return_components: return the per-sphere boolean matrix
        :type return_components: bool
        :return: the exterior mask (or per-sphere components)
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def get_interior_points(cls, points, centers, radii, tolerance: float=0, return_components=False):
        """
        **LLM Docstring**

        Return a mask (or per-sphere components) of the points that lie inside (or on)
        at least one sphere, within a tolerance.

        :param points: the query points
        :type points: np.ndarray
        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param tolerance: the fractional distance tolerance
        :type tolerance: float
        :param return_components: return the per-sphere boolean matrix
        :type return_components: bool
        :return: the interior mask (or per-sphere components)
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def get_surface_points(cls, centers, radii, samples=50, density=None, scaling=1, point_generator=None, expansion=0, preserve_origins=False, circle_samples=None, min_circle_samples=0.1, add_intersection_circles=False, intersection_radius_scaling=1, intersection_boundary_clipping_threshold=None, return_intersection_point_mask=False, extend_intersection_points=True, intersection_point_tolerance=None, clear_circle_neighbors=None, neighborhood_tolerance='auto', tolerance=0, prune=True):
        """
        **LLM Docstring**

        Generate the exterior surface point cloud for a union of spheres: sample each
        sphere, optionally add and clip points along the sphere-sphere intersection
        circles, and prune occluded (interior) points.

        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param samples: the number of points per sphere
        :type samples: int
        :param density: points per unit area (overrides `samples`)
        :type density: float | None
        :param scaling: a multiplicative radius scaling
        :type scaling: float
        :param point_generator: the per-sphere point generator
        :type point_generator: str | Callable | None
        :param expansion: an additive radius expansion
        :type expansion: float
        :param preserve_origins: return per-sphere point lists rather than one array
        :type preserve_origins: bool
        :param circle_samples: number of points per intersection circle
        :type circle_samples: int | None
        :param min_circle_samples: minimum intersection-circle sampling (fraction or count)
        :type min_circle_samples: float
        :param add_intersection_circles: add points along the intersection circles
        :type add_intersection_circles: bool
        :param intersection_radius_scaling: scaling applied to the intersection-circle radius
        :type intersection_radius_scaling: float
        :param intersection_boundary_clipping_threshold: distance for snapping points onto circles
        :param return_intersection_point_mask: also return which points are intersection points
        :type return_intersection_point_mask: bool
        :param extend_intersection_points: add fresh points around the intersection circles
        :type extend_intersection_points: bool
        :param intersection_point_tolerance: exterior-test tolerance for intersection points
        :type intersection_point_tolerance: float | None
        :param clear_circle_neighbors: drop base points near added circle points
        :type clear_circle_neighbors: bool | None
        :param neighborhood_tolerance: the neighbour-clearing tolerance (or `'auto'`)
        :param tolerance: the occlusion tolerance
        :type tolerance: float
        :param prune: drop occluded (interior) points
        :type prune: bool
        :return: the surface points (array or per-sphere lists), optionally with the mask
        :rtype: np.ndarray | list | tuple
        """
        ...

    def generate_points(self, scaling=None, expansion=None, samples=None, density=None, preserve_origins=False, tolerance=None, prune=True, add_intersection_circles=None, **etc):
        """
        **LLM Docstring**

        Generate the exterior surface points for this surface, filling unset options
        from the instance defaults.

        :param scaling: a multiplicative radius scaling
        :type scaling: float | None
        :param expansion: an additive radius expansion
        :type expansion: float | None
        :param samples: the number of points per sphere
        :type samples: int | None
        :param density: points per unit area
        :type density: float | None
        :param preserve_origins: return per-sphere point lists
        :type preserve_origins: bool
        :param tolerance: the occlusion tolerance
        :type tolerance: float | None
        :param prune: drop occluded points
        :type prune: bool
        :param add_intersection_circles: add intersection-circle points
        :type add_intersection_circles: bool | None
        :param etc: extra options forwarded to `get_surface_points`
        :return: the surface points
        :rtype: np.ndarray | list
        """
        ...

    def generate_mesh(self, points=None, normals=None, scaling=None, expansion=None, samples=None, method='poisson', depth=5, **reconstruction_settings):
        """
        **LLM Docstring**

        Reconstruct a triangle mesh from the surface point cloud (currently via Open3D
        Poisson reconstruction), estimating per-point normals from the sphere centers
        when none are given.

        :param points: the surface points (generated if omitted)
        :type points: np.ndarray | list | None
        :param normals: per-point normals (estimated if omitted)
        :type normals: np.ndarray | None
        :param scaling: a multiplicative radius scaling for point generation
        :type scaling: float | None
        :param expansion: an additive radius expansion for point generation
        :type expansion: float | None
        :param samples: the number of points per sphere
        :type samples: int | None
        :param method: the reconstruction method (`'poisson'`)
        :type method: str
        :param depth: the Poisson reconstruction octree depth
        :type depth: int
        :param reconstruction_settings: extra options for the reconstruction
        :return: the reconstructed mesh
        :rtype: SphereUnionSurfaceMesh
        :raises NotImplementedError: for an unsupported method
        """
        ...
    default_point_generator = 'fibonacci'

    @classmethod
    def sphere_points(cls, centers, radii, samples, generator=None, shells=None):
        """
        **LLM Docstring**

        Generate points on each of a (possibly batched) set of spheres, supporting a
        scalar, per-sphere, or per-sphere-per-batch sample count, and optional radial
        shells.

        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param samples: the sample count (scalar, per-sphere, or per-batch)
        :param generator: the point generator (name, dict spec, or callable)
        :type generator: str | dict | Callable | None
        :param shells: number of radial shells (or explicit shell fractions)
        :type shells: int | np.ndarray | None
        :return: the sphere points (array or nested lists)
        :rtype: np.ndarray | list
        """
        ...

    @classmethod
    def fibonacci_sphere(cls, samples):
        """
        **LLM Docstring**

        Generate `samples` roughly-even points on the unit sphere via the Fibonacci
        (golden-angle) spiral.

        :param samples: the number of points
        :type samples: int
        :return: the unit-sphere points, shape `(samples, 3)`
        :rtype: np.ndarray
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axis-aligned bounding box enclosing all of the spheres.

        :return: the `[min_corner, max_corner]` bounding box
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def signed_distance(cls, inside_mask, spacing=1.0):
        """
        Exact signed distance field from a binary mask.
        Positive outside, negative inside, zero at the boundary.

        inside_mask : bool ndarray, True where the object is
        spacing     : float or tuple of floats, physical size of one voxel per axis
        """
        ...

    @classmethod
    def morphological_close_sdf(cls, inside_mask, probe_radius, spacing=1.0):
        """
        Fill concave crevices smaller than probe_radius via
        SDF dilate -> redistance -> erode.

        Returns
        -------
        F_final : float ndarray
            Signed distance field whose zero level set is the closed surface.
        """
        ...

    @classmethod
    def solvent_surface_distance(cls, points, centers, radii, probe_radius=0, probe_type='sas', grid_spacing=None):
        """
        **LLM Docstring**

        Compute the signed distance from each point to the sphere-union surface, either
        as the plain solvent-accessible (SAS) van-der-Waals distance or, for the
        solvent-excluded surface (SES), via a morphological close on a voxel grid.

        :param points: the query points
        :type points: np.ndarray
        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param probe_radius: the solvent probe radius
        :type probe_radius: float
        :param probe_type: `'sas'` or `'ses'`
        :type probe_type: str
        :param grid_spacing: the voxel spacing (required for SES)
        :type grid_spacing: Sequence[float] | None
        :return: the signed distances (shaped like the input grid)
        :rtype: np.ndarray
        :raises ValueError: for SES without a 3-D voxel grid / grid spacing
        """
        ...

    def get_surface_function(self, probe_radius=None, distance_function=None, probe_type='sas'):
        """
        **LLM Docstring**

        Return a callable mapping points to a scalar field whose zero level set is the
        (SAS/SES) molecular surface, passed through a radial decay function.

        :param probe_radius: the solvent probe radius
        :type probe_radius: float | None
        :param distance_function: the radial decay applied to the signed distance
        :type distance_function: Callable | None
        :param probe_type: `'sas'` or `'ses'`
        :type probe_type: str
        :return: the scalar-field function
        :rtype: Callable
        """
        ...
    default_triangulation_method = 'hull-union'

    def get_triangulation(self, occlusion_type='auto', deduplicate_points=None, point_gen_options=None, add_intersection_circles=True, extend_intersection_points=False, method=None, bbox_scaling=1.2, grid_samples=20, probe_radius=None, probe_type='sas', **surface_opts):
        """
        **LLM Docstring**

        Build a triangulated `SphereUnionSurfaceMesh` of the surface, either by hulling
        and unioning the per-sphere point clouds or by marching cubes on the surface
        scalar field.

        :param occlusion_type: how to prune occluded triangles (`'auto'`/`'complete'`/`'partial'`/`'centroid'`)
        :type occlusion_type: str
        :param deduplicate_points: merge coincident points before meshing
        :type deduplicate_points: bool | None
        :param point_gen_options: options for the point generation
        :type point_gen_options: dict | None
        :param add_intersection_circles: add intersection-circle points
        :type add_intersection_circles: bool
        :param extend_intersection_points: add fresh intersection-circle points
        :type extend_intersection_points: bool
        :param method: `'hull-union'` or `'isosurface'`
        :type method: str | None
        :param bbox_scaling: bounding-box padding for the isosurface grid
        :type bbox_scaling: float
        :param grid_samples: grid resolution for the isosurface
        :type grid_samples: int | Sequence[int]
        :param probe_radius: the solvent probe radius (isosurface)
        :type probe_radius: float | None
        :param probe_type: `'sas'` or `'ses'` (isosurface)
        :type probe_type: str
        :param surface_opts: extra options forwarded to the mesh builder
        :return: the triangulated mesh
        :rtype: SphereUnionSurfaceMesh
        :raises ValueError: for an unknown method
        """
        ...

    @classmethod
    def sampling_point_surface_area(cls, centers, radii, points=None, exterior_test=None, point_generator=None, generator_args=None, center_surface_areas=None, **test_args):
        """
        **LLM Docstring**

        Estimate the exposed surface area of the sphere union by Monte-Carlo sampling:
        the fraction of each sphere's sample points that are exterior times its area.

        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param points: precomputed per-sphere sample points (generated if omitted)
        :type points: list | None
        :param exterior_test: the exterior-point test (defaults to `get_exterior_points`)
        :type exterior_test: Callable | None
        :param point_generator: the per-sphere point generator
        :type point_generator: Callable | None
        :param generator_args: options for the point generator
        :type generator_args: dict | None
        :param center_surface_areas: per-sphere areas (computed if omitted)
        :type center_surface_areas: np.ndarray | None
        :param test_args: extra arguments for the exterior test
        :return: the estimated surface area
        :rtype: float
        """
        ...

    @classmethod
    def _monte_carlo_volume(cls, points, centers, radii, interior_test=None, center_volumes=None, **test_args):
        """
        **LLM Docstring**

        Estimate the union volume from per-sphere interior samples, weighting each
        sphere's volume by the average inverse number of spheres that contain its points
        (so overlaps aren't multiply counted).

        :param points: per-sphere sample points
        :type points: list
        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param interior_test: the interior-point test (defaults to `get_interior_points`)
        :type interior_test: Callable | None
        :param center_volumes: per-sphere volumes (computed if omitted)
        :type center_volumes: np.ndarray | None
        :param test_args: extra arguments for the interior test
        :return: the estimated volume
        :rtype: float
        """
        ...

    @classmethod
    def sampling_point_volume(cls, centers, radii, points=None, interior_test=None, point_generator=None, generator_args=None, center_volumes=None, shells=50, **test_args):
        """
        **LLM Docstring**

        Estimate the union volume by Monte-Carlo sampling of interior shell points.

        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param points: precomputed per-sphere sample points (generated if omitted)
        :type points: list | None
        :param interior_test: the interior-point test
        :type interior_test: Callable | None
        :param point_generator: the per-sphere point generator
        :type point_generator: Callable | None
        :param generator_args: options for the point generator
        :type generator_args: dict | None
        :param center_volumes: per-sphere volumes (computed if omitted)
        :type center_volumes: np.ndarray | None
        :param shells: number of radial shells to sample
        :type shells: int
        :param test_args: extra arguments for the interior test
        :return: the estimated volume
        :rtype: float
        """
        ...

    @classmethod
    def random_sphere_sampling(cls, center, radius, samples=500, seed=None, rng=None):
        """
        **LLM Docstring**

        Draw uniformly-distributed random points inside a sphere.

        :param center: the sphere center
        :type center: np.ndarray
        :param radius: the sphere radius
        :type radius: float
        :param samples: the number of points
        :type samples: int
        :param seed: a random seed
        :type seed: int | None
        :param rng: an explicit random generator
        :return: the sampled points
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def volume_union_mc(cls, centers, radii, n_samples=100000, seed=None):
        """
        **LLM Docstring**

        Estimate the union volume by Monte-Carlo sampling uniformly inside each sphere.

        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param n_samples: the number of samples per sphere
        :type n_samples: int
        :param seed: a random seed
        :type seed: int | None
        :return: the estimated volume
        :rtype: float
        """
        ...

    @classmethod
    def volume_voxel(cls, centers, radii, resolution=200):
        """
        **LLM Docstring**

        Estimate the union volume by voxelizing the bounding box and counting the voxels
        inside any sphere.

        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param resolution: the number of voxels along each axis
        :type resolution: int
        :return: the estimated volume
        :rtype: float
        """
        ...

    @classmethod
    def _trip_q(self, a, b, c, alpha, beta, gamma, e):
        """
        **LLM Docstring**

        Helper for the analytic triple-sphere intersection area (the `q` term from
        Gibson & Scheraga's formulation).

        :param a: the first inter-center distance
        :param b: the second inter-center distance
        :param c: the third inter-center distance
        :param alpha: the first radius
        :param beta: the second radius
        :param gamma: the third radius
        :param e: the corresponding eccentricity term
        :return: the `q` term
        :rtype: float
        """
        ...

    @classmethod
    def _trip_e(self, a, r2, r3):
        """
        **LLM Docstring**

        Helper for the analytic triple-sphere intersection area (the eccentricity `e`
        term).

        :param a: the inter-center distance
        :param r2: the second radius
        :param r3: the third radius
        :return: the `e` term
        :rtype: float
        """
        ...

    @classmethod
    def _trip_w(self, a, b, c, alpha, beta, gamma):
        """
        **LLM Docstring**

        Helper for the analytic triple-sphere intersection area: the Cayley-Menger-style
        determinant term whose sign indicates whether the three spheres share a common
        intersection.

        :param a: the first inter-center distance
        :param b: the second inter-center distance
        :param c: the third inter-center distance
        :param alpha: the first radius
        :param beta: the second radius
        :param gamma: the third radius
        :return: the `w` term (its square root, or the raw determinant if negative)
        :rtype: float
        """
        ...

    @classmethod
    def _trip_s(self, beta, a, c, q1, q3, e1, e3, w):
        """
        **LLM Docstring**

        Helper for the analytic triple-sphere intersection area: one of the arctangent
        `s` terms, branch-corrected to `[0, pi]`.

        :param beta: the relevant radius
        :param a: the first inter-center distance
        :param c: the second inter-center distance
        :param q1: the first `q` term
        :param q3: the third `q` term
        :param e1: the first eccentricity term
        :param e3: the third eccentricity term
        :param w: the `w` determinant term
        :return: the `s` term
        :rtype: float
        """
        ...

    @classmethod
    def _trip_t(cls, a, b, c):
        """
        **LLM Docstring**

        Helper for the analytic sphere-intersection area: the Heron-style product
        `(a+b+c)(-a+b+c)(a-b+c)(a+b-c)`.

        :param a: the first length
        :param b: the second length
        :param c: the third length
        :return: the product
        :rtype: float
        """
        ...

    @classmethod
    def _trip_p(cls, a, b, c, r1, r2, r3, t):
        """
        **LLM Docstring**

        Helper for the analytic triple-sphere intersection area: the two candidate `p`
        tests used to classify how the third sphere sits relative to the others'
        intersection.

        :param a: the opposite inter-center distance
        :param b: the second inter-center distance
        :param c: the third inter-center distance
        :param r1: the first radius
        :param r2: the second radius
        :param r3: the third radius
        :param t: the Heron term from `_trip_t`
        :return: the `(p_plus, p_minus)` tests
        :rtype: tuple
        """
        ...

    @classmethod
    def sphere_triple_intersection_area(cls, a, b, c, r1, r2, r3):
        """
        **LLM Docstring**

        Analytic surface area of the triple overlap of three spheres, following Gibson &
        Scheraga. Returns either a pair-index fallback (when the triple doesn't fully
        intersect) or the analytic area.

        :param a: the distance between centers 2 and 3
        :param b: the distance between centers 1 and 3
        :param c: the distance between centers 1 and 2
        :param r1: the first radius
        :param r2: the second radius
        :param r3: the third radius
        :return: `(overlap_indices_or_None, area_or_None)`
        :rtype: tuple
        """
        ...
    IntersectionCircle = collections.namedtuple('IntersectionCircle', ['center', 'normal', 'radius'])

    @classmethod
    def sphere_double_intersection_circle(cls, centers, radii, dist=None):
        """
        **LLM Docstring**

        Compute the circle where two spheres intersect (its center, unit normal, and
        radius).

        :param centers: the two sphere centers
        :type centers: np.ndarray
        :param radii: the two sphere radii
        :type radii: np.ndarray
        :param dist: the inter-center distance (computed if omitted)
        :type dist: float | None
        :return: the intersection circle
        :rtype: SphereUnionSurface.IntersectionCircle
        """
        ...

    @classmethod
    def sphere_triple_intersection_point(cls, centers, radii, dists=None):
        """
        **LLM Docstring**

        Compute the two points where three (assumed mutually intersecting) spheres meet,
        by building a local axis system and solving for the coordinates.

        :param centers: the three sphere centers
        :type centers: np.ndarray
        :param radii: the three sphere radii
        :type radii: np.ndarray
        :param dists: the `(d_12, d_13)` inter-center distances
        :type dists: tuple | None
        :return: the two intersection points
        :rtype: list
        """
        ...

    @classmethod
    def get_intersections(cls, centers, radii):
        """
        **LLM Docstring**

        Find all pairwise intersection circles and all triple intersection points among
        a set of spheres.

        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :return: `(intersection_points, intersection_disks)`
        :rtype: tuple
        """
        ...

    @classmethod
    def sphere_double_intersection_area(cls, a, r1, r2):
        """
        **LLM Docstring**

        Analytic exposed surface-area contribution of the overlap of two spheres, or a
        containment fallback when one sphere swallows the other.

        :param a: the inter-center distance
        :type a: float
        :param r1: the first radius
        :type r1: float
        :param r2: the second radius
        :type r2: float
        :return: `(overlap_indices_or_None, area)`
        :rtype: tuple
        """
        ...

    @classmethod
    def _quad_w(cls, a, b, c, f, g, h):
        """
        **LLM Docstring**

        Helper for the analytic quadruple-sphere intersection area: the Cayley-Menger
        determinant term.

        :param a: an inter-center distance
        :param b: an inter-center distance
        :param c: an inter-center distance
        :param f: an inter-center distance
        :param g: an inter-center distance
        :param h: an inter-center distance
        :return: the `w` term (its root, or the raw determinant if negative)
        :rtype: float
        """
        ...

    @classmethod
    def _quad_s(cls, a, b, c, f, g, h):
        """
        **LLM Docstring**

        Helper for the analytic quadruple-sphere intersection area: one of the `s` terms.

        :param a: an inter-center distance
        :param b: an inter-center distance
        :param c: an inter-center distance
        :param f: a radius/length term
        :param g: a radius/length term
        :param h: a radius/length term
        :return: the `s` term
        :rtype: float
        """
        ...

    @classmethod
    def _quad_term(cls, a, beta, gamma, W2, s1):
        """
        **LLM Docstring**

        Helper for the analytic quadruple-sphere intersection area: one branch-corrected
        arctangent area term.

        :param a: an inter-center distance
        :param beta: a radius
        :param gamma: a radius
        :param W2: twice the `w` determinant term
        :param s1: the corresponding `s` term
        :return: the area term
        :rtype: float
        """
        ...

    @classmethod
    def triangle_area(cls, a, b, c):
        """
        **LLM Docstring**

        Heron's-formula area of a triangle with the given side lengths.

        :param a: the first side
        :param b: the second side
        :param c: the third side
        :return: the area
        :rtype: float
        """
        ...

    @classmethod
    def sphere_quadruple_intersection_area(cls, a, b, c, f, g, h, r1, r2, r3, r4, A123, A124, A134, A234, I4, I3, I2, I1):
        """
        **LLM Docstring**

        Analytic surface-area contribution of the quadruple overlap of four spheres,
        dispatching on a set of intersection-test bit patterns to the correct lower-order
        fallback or the full analytic expression.

        :param a: the distance between centers 2 and 3
        :param b: the distance between centers 1 and 3
        :param c: the distance between centers 1 and 2
        :param f: the distance between centers 1 and 4
        :param g: the distance between centers 2 and 4
        :param h: the distance between centers 3 and 4
        :param r1: the first radius
        :param r2: the second radius
        :param r3: the third radius
        :param r4: the fourth radius
        :param A123: the 1-2-3 triple area
        :param A124: the 1-2-4 triple area
        :param A134: the 1-3-4 triple area
        :param A234: the 2-3-4 triple area
        :param I4: the pair of tests for center 4 vs the 1-2-3 intersection points
        :param I3: the pair of tests for center 3
        :param I2: the pair of tests for center 2
        :param I1: the pair of tests for center 1
        :return: `(overlap_indices_or_None, area_or_None)`
        :rtype: tuple
        :raises ValueError: for an unhandled intersection-test pattern
        """
        ...

    @classmethod
    def sphere_area(cls, radii, axis=None):
        """
        **LLM Docstring**

        The total surface area of one or more spheres, `4 pi sum(r^2)`.

        :param radii: the sphere radii
        :type radii: np.ndarray
        :param axis: the axis to sum over
        :type axis: int | None
        :return: the surface area
        :rtype: float | np.ndarray
        """
        ...

    @classmethod
    def sphere_union_surface_area(cls, centers, radii, include_doubles=True, include_triples=None, include_quadruples=None, return_terms=False, overlap_tolerance=0):
        """
        **LLM Docstring**

        Compute the exact exposed surface area of a union of spheres via
        inclusion-exclusion over the analytic single/double/triple/quadruple
        intersection-area terms, dropping fully-occluded spheres as they are detected.

        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param include_doubles: include the pairwise intersection terms
        :type include_doubles: bool
        :param include_triples: include the triple terms
        :type include_triples: bool | None
        :param include_quadruples: include the quadruple terms
        :type include_quadruples: bool | None
        :param return_terms: return the per-combination term dict rather than the sum
        :type return_terms: bool
        :param overlap_tolerance: fractional tolerance for treating spheres as overlapping
        :type overlap_tolerance: float
        :return: the surface area (or the terms dict)
        :rtype: float | dict
        """
        ...

    def surface_area(self, method='union', **opts):
        """
        **LLM Docstring**

        Compute the surface area of the sphere union by the chosen method.

        :param method: `'union'` (analytic), `'sampling'`, `'mesh'`, or `'pcmesh'`
        :type method: str
        :param opts: method-specific options
        :return: the surface area
        :rtype: float
        :raises ValueError: for an unknown method
        """
        ...

    def volume(self, method='monte-carlo', **opts):
        """
        **LLM Docstring**

        Compute the volume of the sphere union by the chosen method.

        :param method: `'monte-carlo'`, `'sampling'`, `'voxel'`, `'mesh'`, or `'pcmesh'` (`'union'` not implemented)
        :type method: str
        :param opts: method-specific options
        :return: the volume
        :rtype: float
        :raises ValueError: for an unknown method
        :raises NotImplementedError: for the analytic `'union'` method
        """
        ...

    def plot(self, figure=None, *, points=None, function=None, sphere_color='white', sphere_style=None, point_style=None, point_values=None, distance_units='Angstroms', plot_intersections=False, **etc):
        """
        **LLM Docstring**

        Plot the surface: the sample points (colored by an optional scalar function),
        the spheres, and optionally the intersection circles/points.

        :param figure: an existing figure to draw into
        :param points: the points to plot (defaults to the sampling points)
        :type points: np.ndarray | None
        :param function: a scalar function to color the points by
        :type function: Callable | None
        :param sphere_color: the sphere color
        :param sphere_style: extra sphere styling
        :type sphere_style: dict | None
        :param point_style: extra point styling
        :type point_style: dict | None
        :param point_values: explicit per-point color values
        :type point_values: np.ndarray | None
        :param distance_units: the display distance units
        :type distance_units: str
        :param plot_intersections: also draw the intersection circles/points
        :type plot_intersections: bool
        :param etc: extra plotting options
        :return: the figure
        :rtype: object
        """
        ...

    @classmethod
    def plot_sphere_points(cls, points, centers, radii, figure=None, *, color='black', backend='x3d', return_objects=False, sphere_color='white', sphere_style=None, point_colors=None, point_values=None, vertex_colormap='WarioColors', rescale_color_values=True, plot_intersections=False, intersection_point_style=None, intersection_circle_style=None, **etc):
        """
        **LLM Docstring**

        Plot a set of points, spheres, and optional intersection geometry into a 3-D
        figure.

        :param points: the points to plot
        :type points: np.ndarray
        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param figure: an existing figure to draw into
        :param color: the point color
        :param backend: the plotting backend
        :type backend: str
        :param return_objects: also return the created plot objects
        :type return_objects: bool
        :param sphere_color: the sphere color
        :param sphere_style: extra sphere styling
        :type sphere_style: dict | None
        :param point_colors: explicit per-point colors
        :param point_values: per-point scalar values to color by
        :type point_values: np.ndarray | None
        :param vertex_colormap: the colormap for point values
        :type vertex_colormap: str
        :param rescale_color_values: rescale the color values into the colormap range
        :type rescale_color_values: bool
        :param plot_intersections: draw the intersection circles/points
        :type plot_intersections: bool
        :param intersection_point_style: styling for intersection points
        :type intersection_point_style: dict | None
        :param intersection_circle_style: styling for intersection circles
        :type intersection_circle_style: dict | None
        :param etc: extra plotting options
        :return: the figure (and objects if requested)
        :rtype: object | tuple
        """
        ...

class MeshCleaner:

    def __init__(self, verts, inds, vert_map, centers=None, radii=None, max_pair_dist=None):
        """
        **LLM Docstring**

        Set up a cleaner for repairing a triangle mesh's topology (seams and holes).

        :param verts: the mesh vertices
        :type verts: np.ndarray
        :param inds: the triangle vertex indices
        :type inds: np.ndarray
        :param vert_map: the per-vertex owning-sphere map
        :type vert_map: np.ndarray
        :param centers: the sphere centers (for orienting new triangles)
        :type centers: np.ndarray | None
        :param radii: the sphere radii
        :type radii: np.ndarray | None
        :param max_pair_dist: the maximum centroid distance for pairing seam loops
        :type max_pair_dist: float | None
        """
        ...

    @property
    def report(self):
        """
        **LLM Docstring**

        The (cached) mesh topology report (boundary loops, non-manifold features, Euler
        characteristic).

        :return: the topology report
        :rtype: dict
        """
        ...

    def clean(self):
        """
        **LLM Docstring**

        Return the cleaned mesh, stitching seams and capping holes (computed lazily).

        :return: the `(verts, faces, vert_map)` of the cleaned mesh
        :rtype: tuple
        """
        ...

    @classmethod
    def mesh_topology_report(cls, verts, faces):
        """
        Diagnose a triangle mesh (as produced by `union_of_spheres_mesh`) for
        topological defects: open boundary edges (holes), non-manifold edges,
        and non-manifold ("bowtie") vertices.

        The core idea: in a closed, manifold triangle mesh every undirected
        edge is shared by *exactly* two triangles. Count how many triangles
        use each edge and:
          - count == 1  -> a boundary edge; these are exactly the edges that
                            border a hole (or, on a genuinely open surface,
                            the outer rim)
          - count == 2  -> a normal interior edge, fine
          - count >= 3  -> non-manifold: three or more triangles meet at one
                            edge. This usually means duplicate/overlapping
                            triangles rather than a "hole" and should be
                            cleaned up separately (it will also break the
                            loop-walk below, since a manifold boundary loop
                            assumes each boundary vertex touches exactly two
                            boundary edges).

        Parameters
        ----------
        verts : (V, 3) array
        faces : (F, 3) int array of vertex indices

        Returns
        -------
        report : dict with keys
            'boundary_edges'       : (E, 2) int array, undirected edges used
                                      by only one triangle
            'boundary_loops'       : list of int arrays, each an ordered
                                      vertex loop walked around one hole. If a
                                      loop can't be closed cleanly (e.g. it
                                      runs into a non-manifold vertex) it's
                                      returned as an open path instead of a
                                      closed ring -- check
                                      `loop[0] == loop[-1]` to tell them apart.
            'nonmanifold_edges'    : (K, 2) int array of edges shared by 3+
                                      triangles
            'nonmanifold_vertices' : int array of vertices where the boundary
                                      touches itself more than once (bowties)
            'euler_characteristic' : V - E + F. A closed, genus-0 mesh (i.e.
                                      topologically a sphere, no holes, no
                                      handles) has euler == 2; each hole you
                                      leave unfilled lowers it by 1.
            'n_holes'               : number of boundary loops found (only
                                      meaningful if there are no non-manifold
                                      edges/vertices confusing the count)
            'is_watertight'         : True iff there are no boundary edges and
                                      no non-manifold edges
        """
        ...

    @classmethod
    def _align_and_orient(cls, verts, A, B):
        """
        Find the best starting offset and traversal direction for loop `B` so
        that walking it lines up with walking loop `A`, using a short
        lookahead to score both candidate directions. Two loops bounding the
        same seam are typically traced in opposite directions (each patch's
        boundary is oriented outward via its own triangles), so this often
        picks the reversed direction -- that's expected, not a bug.
        """
        ...

    @classmethod
    def _zipper_ring(cls, verts, A, B):
        """
        Bridge two aligned, closed vertex loops with a ring of nA + nB
        triangles, at each step advancing whichever loop yields the shorter
        connecting edge. Standard "loft between two curves" construction, used
        here as a closed ring instead of an open strip.
        """
        ...

    @classmethod
    def _stitch_pair(cls, verts, loopA, loopB):
        """
        **LLM Docstring**

        Stitch two boundary loops together with a ring of triangles, after aligning and
        orienting them.

        :param verts: the mesh vertices
        :type verts: np.ndarray
        :param loopA: the first boundary loop (vertex indices)
        :type loopA: np.ndarray
        :param loopB: the second boundary loop
        :type loopB: np.ndarray
        :return: the new bridging triangles
        :rtype: list
        """
        ...

    @classmethod
    def _cap_loop(cls, verts, owner, loop, new_vertex_id):
        """
        Close a single, unpaired boundary loop with a triangle fan from its
        centroid. Robust for the small, roughly-circular leftover holes this
        is meant for; not guaranteed valid for highly non-convex loops (a full
        ear-clipping triangulation would be needed there, but isolated holes
        of that shape shouldn't arise from this grid construction).
        """
        ...

    @classmethod
    def _fix_orientation(cls, verts, faces, centers, radii):
        """
        Flip any new triangle whose winding points inward relative to its
        nearest sphere center. Cheap and reliable here because the surface is
        always close to spherical locally, even right at a seam.
        """
        ...

    @classmethod
    def _stitch_seams(cls, verts, faces, owner, report, centers=None, radii=None, max_pair_dist=None):
        """
        Use the boundary loops from `mesh_topology_report` to close a mesh's
        remaining holes, distinguishing two different situations:

          * Seam loops -- a "hole" that is really the same physical
            intersection curve traced twice, once by each of two neighboring
            spheres' patches, that fell just outside `weld_tol` and so wasn't
            merged by `_weld_vertices`. These are matched up by proximity and
            zipped together with a ring of new triangles connecting
            corresponding points on the two loops. Capping either loop alone
            would leave a double-layered sliver instead of one continuous
            surface, so paired loops are always zipped, never capped.
          * Isolated loops -- no nearby partner found (a true pinhole, or a
            seam whose other side failed to form at all, e.g. from an
            unusually coarse grid). These get a simple triangle-fan cap from
            their centroid instead.

        Parameters
        ----------
        verts, faces, w, owner : mesh arrays, as returned by
            `union_of_spheres_mesh`.
        report : dict, the output of `mesh_topology_report(verts, faces)` run
            on those same arrays. Only cleanly-closed loops
            (`loop[0] == loop[-1]`) are touched; a loop that didn't close
            (it ran into a non-manifold vertex) is left alone -- resolve
            `report["nonmanifold_vertices"]` first, then re-run the topology
            report and this function.
        centers, radii : optional sphere arrays. If given, every new triangle
            is checked against the outward direction from its nearest sphere
            center and flipped if it points inward.
        max_pair_dist : float or None. Two loops are only considered a
            candidate seam pair if their centroids are within this distance.
            Defaults to 4x the longest existing boundary edge -- generous
            enough to catch true seam partners without pairing unrelated holes
            on opposite sides of the mesh.

        Returns
        -------
        verts, faces, owner : updated arrays with stitching/cap triangles
            (and, for isolated-loop caps, one new centroid vertex per capped
            loop) appended. Run `mesh_topology_report` again on the result to
            confirm `is_watertight` and check for any loops left unresolved.
        """
        ...

class SphereUnionSurfaceMesh:

    def __init__(self, verts, inds, surf=None, densities=None, tri_map=None, vert_map=None, normals=None, vertex_normals=None, centers=None, radii=None):
        """
        **LLM Docstring**

        Hold a triangle mesh (vertices and triangle indices) plus optional metadata for
        a sphere-union surface.

        :param verts: the mesh vertices
        :type verts: np.ndarray
        :param inds: the triangle vertex indices
        :type inds: np.ndarray
        :param surf: the source surface, if any
        :type surf: SphereUnionSurface | None
        :param densities: per-vertex reconstruction densities
        :type densities: np.ndarray | None
        :param tri_map: per-triangle owning-sphere map
        :type tri_map: np.ndarray | None
        :param vert_map: per-vertex owning-sphere map
        :type vert_map: np.ndarray | None
        :param normals: per-triangle normals
        :type normals: np.ndarray | None
        :param vertex_normals: per-vertex normals
        :type vertex_normals: np.ndarray | None
        :param centers: the sphere centers
        :type centers: np.ndarray | None
        :param radii: the sphere radii
        :type radii: np.ndarray | None
        """
        ...

    def surface_area(self, return_components=False):
        """
        **LLM Docstring**

        Compute the mesh surface area as the sum of its triangle areas (Heron's
        formula).

        :param return_components: return the per-triangle areas rather than the sum
        :type return_components: bool
        :return: the surface area (or per-triangle areas)
        :rtype: float | np.ndarray
        """
        ...

    def volume(self, return_components=False):
        """
        Exact volume of a closed mesh via the divergence theorem.
        Assumes outward-pointing face normals and watertight mesh.
        """
        ...

    def normal_derivatives(self, order=1):
        """
        **LLM Docstring**

        Compute the derivatives (up to `order`) of each triangle's normal with respect to
        its vertex coordinates.

        :param order: the derivative order
        :type order: int
        :return: the per-order normal-derivative tensors
        :rtype: list
        """
        ...

    def _dist_deriv(self, i_list, j_list, order):
        """
        **LLM Docstring**

        Compute the derivatives (up to `order`) of the edge lengths between paired
        vertices.

        :param i_list: the first vertex indices
        :param j_list: the second vertex indices
        :param order: the derivative order
        :type order: int
        :return: the per-order distance-derivative tensors
        :rtype: list
        """
        ...

    def area_derivatives(self, order=1, return_components=False):
        """
        **LLM Docstring**

        Compute the derivatives (up to `order`) of each triangle's area with respect to
        its vertex coordinates, via the Heron expansion of its edge lengths.

        :param order: the derivative order
        :type order: int
        :param return_components: return the per-triangle derivatives rather than their sum
        :type return_components: bool
        :return: the per-order area-derivative tensors
        :rtype: list
        """
        ...

    def centroid_derivatives(self, order=1, return_components=False):
        """
        **LLM Docstring**

        Compute the derivatives (up to `order`) of each triangle's centroid with respect
        to its vertex coordinates.

        :param order: the derivative order
        :type order: int
        :param return_components: accepted for interface parity
        :type return_components: bool
        :return: the per-order centroid-derivative tensors
        :rtype: list
        """
        ...

    def volume_derivatives(self, order=1, return_components=False, normal_order=None, area_order=None, centroid_order=None):
        """
        **LLM Docstring**

        Compute the derivatives (up to `order`) of the enclosed volume with respect to
        the vertex coordinates, combining the area, centroid, and normal derivatives via
        the divergence theorem.

        :param order: the derivative order
        :type order: int
        :param return_components: return the per-triangle derivatives rather than their sum
        :type return_components: bool
        :param normal_order: override the order for the normal derivatives
        :type normal_order: int | None
        :param area_order: override the order for the area derivatives
        :type area_order: int | None
        :param centroid_order: override the order for the centroid derivatives
        :type centroid_order: int | None
        :return: the per-order volume-derivative tensors
        :rtype: list
        """
        ...

    @property
    def normals(self):
        """
        **LLM Docstring**

        The per-triangle unit normals (computed lazily).

        :return: the triangle normals
        :rtype: np.ndarray
        """
        ...

    @property
    def signed_volumes(self):
        """
        **LLM Docstring**

        The per-triangle signed tetrahedron volumes (the cross-product norms used in the
        divergence-theorem volume), computed lazily.

        :return: the signed volumes
        :rtype: np.ndarray
        """
        ...

    def get_normals(self, normalize=True):
        """
        **LLM Docstring**

        Compute the per-triangle normals (and their norms) from the triangle edge cross
        products.

        :param normalize: return unit normals
        :type normalize: bool
        :return: the `(normals, norms)`
        :rtype: tuple
        """
        ...

    @classmethod
    def from_submeshes(cls, pts, submeshes, *, centers, radii, occlusion_type='complete', occlusion_tolerance=0.01, check_normals=True, deduplicate_points=False, duplicate_point_threshold=1e-14, vert_map=None, intersection_point_mask=None, occlusion_intersection_tolerance=0.05, stitch=True, **etc):
        """
        **LLM Docstring**

        Build a mesh from a shared point set and per-sphere triangle sub-meshes,
        optionally deduplicating coincident points and pruning triangles occluded inside
        the sphere union (by vertex or centroid tests), fixing triangle orientations.

        :param pts: the shared vertex set
        :type pts: np.ndarray
        :param submeshes: the per-sphere triangle index arrays
        :type submeshes: list
        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param occlusion_type: how to prune occluded triangles (`None`/`'complete'`/`'partial'`/`'centroid'`)
        :type occlusion_type: str | None
        :param occlusion_tolerance: the exterior-test tolerance
        :type occlusion_tolerance: float
        :param check_normals: reorient triangle normals to point outward
        :type check_normals: bool
        :param deduplicate_points: merge coincident points
        :type deduplicate_points: bool
        :param duplicate_point_threshold: the coincidence distance threshold
        :type duplicate_point_threshold: float
        :param vert_map: per-vertex owning-sphere map
        :type vert_map: np.ndarray | None
        :param intersection_point_mask: which points are intersection points
        :type intersection_point_mask: np.ndarray | None
        :param occlusion_intersection_tolerance: the looser tolerance for intersection points
        :type occlusion_intersection_tolerance: float
        :param stitch: accepted for interface parity
        :type stitch: bool
        :param etc: extra options forwarded to the constructor
        :return: the mesh
        :rtype: SphereUnionSurfaceMesh
        :raises ValueError: if all triangles get pruned
        :raises NotImplementedError: for an unsupported occlusion type
        """
        ...

    def stitch(self):
        """
        **LLM Docstring**

        Return a topologically repaired copy of the mesh (seams stitched, holes capped)
        via `MeshCleaner`.

        :return: the cleaned mesh
        :rtype: SphereUnionSurfaceMesh
        """
        ...

    @classmethod
    def from_subclouds(cls, point_clouds, *, centers, radii, mesh_type='convex', occlusion_type='partial', vert_map=None, deduplicate_points=False, mesh_kwargs=None, intersection_point_mask=None, **surface_options):
        """
        **LLM Docstring**

        Build a mesh by convex-hulling each per-sphere point cloud and unioning the
        resulting sub-meshes (pruning occluded triangles).

        :param point_clouds: the per-sphere point clouds
        :type point_clouds: list
        :param centers: the sphere centers
        :type centers: np.ndarray
        :param radii: the sphere radii
        :type radii: np.ndarray
        :param mesh_type: the per-cloud hull type (`'convex'` or a hull class)
        :type mesh_type: str | type
        :param occlusion_type: how to prune occluded triangles
        :type occlusion_type: str
        :param vert_map: per-vertex owning-sphere map (built if omitted)
        :type vert_map: np.ndarray | None
        :param deduplicate_points: merge coincident points
        :type deduplicate_points: bool
        :param mesh_kwargs: extra options for the hull construction
        :type mesh_kwargs: dict | None
        :param intersection_point_mask: which points are intersection points
        :type intersection_point_mask: np.ndarray | None
        :param surface_options: extra options forwarded to `from_submeshes`
        :return: the mesh
        :rtype: SphereUnionSurfaceMesh
        """
        ...

    @classmethod
    def from_o3d(cls, mesh, densities=None, surf=None):
        """
        **LLM Docstring**

        Build a mesh from an Open3D triangle mesh.

        :param mesh: the Open3D mesh
        :param densities: per-vertex reconstruction densities
        :type densities: np.ndarray | None
        :param surf: the source surface
        :type surf: SphereUnionSurface | None
        :return: the mesh
        :rtype: SphereUnionSurfaceMesh
        """
        ...

    def plot(self, figure=None, *, function=None, vertex_values=None, normals=None, invert_mesh=False, distance_units='Angstroms', **etc):
        """
        **LLM Docstring**

        Plot the triangle mesh, optionally coloring vertices by a scalar function and
        drawing normals.

        :param figure: an existing figure to draw into
        :param function: a scalar function to color vertices by
        :type function: Callable | None
        :param vertex_values: explicit per-vertex color values
        :type vertex_values: np.ndarray | None
        :param normals: per-triangle normals to draw (or `True` to use the mesh normals)
        :param invert_mesh: flip the triangle winding
        :type invert_mesh: bool
        :param distance_units: the display distance units
        :type distance_units: str
        :param etc: extra plotting options
        :return: the figure
        :rtype: object
        """
        ...

    @classmethod
    def plot_triangle_mesh(cls, verts, indices, figure=None, *, color='blue', transparency=0.8, backend='x3d', return_objects=False, line_color='black', line_transparency=0.9, line_style=None, vertex_colors=None, vertex_values=None, vertex_colormap='WarioColors', rescale_color_values=True, normals=None, centroids=None, normal_color='black', normal_radius=0.01, normal_scaling=0.5, **etc):
        """
        **LLM Docstring**

        Plot a triangle mesh (faces, edges, and optional per-triangle normals) into a 3-D
        figure.

        :param verts: the mesh vertices
        :type verts: np.ndarray
        :param indices: the triangle vertex indices
        :type indices: np.ndarray
        :param figure: an existing figure to draw into
        :param color: the face color
        :param transparency: the face transparency
        :type transparency: float
        :param backend: the plotting backend
        :type backend: str
        :param return_objects: also return the created plot objects
        :type return_objects: bool
        :param line_color: the edge color
        :param line_transparency: the edge transparency
        :type line_transparency: float
        :param line_style: extra edge styling
        :type line_style: dict | None
        :param vertex_colors: explicit per-vertex colors
        :param vertex_values: per-vertex scalar values to color by
        :type vertex_values: np.ndarray | None
        :param vertex_colormap: the colormap for vertex values
        :type vertex_colormap: str
        :param rescale_color_values: rescale the color values into the colormap range
        :type rescale_color_values: bool
        :param normals: per-triangle normals to draw
        :type normals: np.ndarray | None
        :param centroids: triangle centroids for the normals (computed if omitted)
        :type centroids: np.ndarray | None
        :param normal_color: the normal-arrow color
        :param normal_radius: the normal-arrow radius
        :type normal_radius: float
        :param normal_scaling: the normal-arrow length scaling
        :type normal_scaling: float
        :param etc: extra plotting options
        :return: the figure (and objects if requested)
        :rtype: object | tuple
        """
        ...