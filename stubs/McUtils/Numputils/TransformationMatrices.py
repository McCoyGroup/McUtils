import enum
import itertools
import scipy.linalg
from .VectorOps import vec_normalize
from . import VectorOps as vec_ops
from . import Misc as misc
from . import PermutationOps as perm_ops
import math, numpy as np, scipy as sp
__all__ = ['rotation_matrix', 'skew_symmetric_matrix', 'rotation_matrix_skew', 'youla_skew_decomp', 'youla_skew_matrix', 'youla_angles', 'youla_matrix', 'skew_from_rotation_matrix', 'translation_matrix', 'affine_matrix', 'reflection_matrix', 'permutation_matrix', 'extract_rotation_angle_axis', 'extract_reflection_axis', 'view_matrix', 'rotation_normal_view_matrix', 'perspective_matrix', 'world_matrix', 'render_matrix', 'render_points', 'find_coordinate_matching_permutation', 'symmetry_permutation', 'apply_symmetries', 'symmetry_reduce', 'identify_cartesian_transformation_type', 'TransformationTypes', 'cartesian_transformation_from_data']

def rotation_matrix_2d(theta):
    """
    **LLM Docstring**

    Build a 2x2 rotation matrix (or a stack of them) for the given angle(s).

    The rotation axis is moved to the trailing matrix axes so batched angles produce
    a stack of `(..., 2, 2)` matrices.

    :param theta: rotation angle(s)
    :type theta: float | np.ndarray
    :return: the 2x2 rotation matrix (or stack)
    :rtype: np.ndarray
    """
    ...

def rotation_matrix_basic(xyz, theta):
    """rotation matrix about x, y, or z axis

    :param xyz: x, y, or z axis
    :type xyz: str
    :param theta: counter clockwise angle in radians
    :type theta: float
    """
    ...

def rotation_matrix_ER(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    ...

def rotation_matrix_ER_vec(axes, thetas):
    """
    Vectorized version of basic ER
    """
    ...

def rotation_matrix_align_vectors(vec1, vec2):
    """
    **LLM Docstring**

    Build the rotation matrix that rotates one (unit) vector onto another.

    Uses the closed-form reflection-free construction from the normalized vectors;
    the near-antiparallel case (where the formula is singular) is detected and
    replaced with `-I`.

    :param vec1: the source vector
    :type vec1: np.ndarray
    :param vec2: the target vector
    :type vec2: np.ndarray
    :return: the aligning rotation matrix (or stack)
    :rtype: np.ndarray
    """
    ...

def rotation_matrix(axis, theta=None):
    """
    :param axis:
    :type axis:
    :param theta: angle to rotate by (or Euler angles)
    :type theta:
    :return:
    :rtype:
    """
    ...

def skew_symmetric_matrix(upper_tri):
    """
    **LLM Docstring**

    Build a skew-symmetric matrix from the flattened entries of its strict upper
    triangle.

    The vector length must correspond to a valid upper triangle; the entries are
    scattered above the diagonal and negated below it.

    :param upper_tri: the strict-upper-triangle entries
    :type upper_tri: np.ndarray
    :return: the skew-symmetric matrix (or stack)
    :rtype: np.ndarray
    """
    ...

def extract_rotation_angle_axis(rot_mat, normalize=True):
    """
    **LLM Docstring**

    Extract the rotation angle and axis from a rotation matrix.

    For 2D matrices only the angle is returned; for 3D the axis comes from the skew
    part with careful handling of the near-`pi` and identity degeneracies, and the
    angle from an orthogonal reference vector. Higher-dimensional rotations are
    decomposed via a Schur/Youla factorization into a set of plane angles and axes.

    :param rot_mat: the rotation matrix (or stack)
    :type rot_mat: np.ndarray
    :param normalize: normalize the extracted axis
    :type normalize: bool
    :return: `(angle, axis)` (axis is `None` in 2D)
    :rtype: tuple
    """
    ...

def extract_reflection_axis(reflection_mat):
    """
    **LLM Docstring**

    Extract the reflection axis (plane normal) from a reflection matrix.

    Reflects a random probe vector and takes the (normalized) difference; if the
    probe happened to lie in the reflection plane a second in-plane probe is used
    instead.

    :param reflection_mat: the reflection matrix (or stack)
    :type reflection_mat: np.ndarray
    :return: the reflection axis (or stack of axes)
    :rtype: np.ndarray
    """
    ...

def youla_skew_decomp(A):
    """
    **LLM Docstring**

    Compute the Youla decomposition of a skew-symmetric matrix.

    Uses a Schur factorization to bring the matrix to block form and reads off the
    block magnitudes, handling the odd-dimension padding, returning the canonical
    Youla skew matrix together with the orthogonal transform.

    :param A: the skew-symmetric matrix
    :type A: np.ndarray
    :return: `(youla_skew_matrix, orthogonal_transform)`
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    ...

def youla_skew_matrix(l, n, axis_pos=0):
    """
    **LLM Docstring**

    Build the canonical Youla skew-symmetric block matrix from a list of block
    magnitudes.

    Places each magnitude on the appropriate super-/sub-diagonal pair, skipping the
    fixed axis position for odd dimensions.

    :param l: the block magnitudes
    :type l: np.ndarray
    :param n: the matrix dimension
    :type n: int
    :param axis_pos: index of the fixed (unpaired) axis for odd dimensions
    :type axis_pos: int
    :return: the canonical Youla skew matrix
    :rtype: np.ndarray
    """
    ...

def youla_matrix(angles, n, axis_pos=0):
    """
    **LLM Docstring**

    Build the canonical block-diagonal rotation (Youla) matrix from a list of plane
    angles.

    Assembles the `2x2` cosine/sine rotation blocks along the diagonal, leaving the
    fixed axis (for odd dimensions) as an identity entry.

    :param angles: the per-plane rotation angles
    :type angles: np.ndarray
    :param n: the matrix dimension
    :type n: int
    :param axis_pos: index of the fixed axis for odd dimensions
    :type axis_pos: int
    :return: the block-diagonal rotation matrix
    :rtype: np.ndarray
    """
    ...

def youla_angles(U, axis_pos=None):
    """
    **LLM Docstring**

    Read the plane rotation angles off the diagonal of a canonical Youla rotation
    matrix.

    Detects the fixed-axis position (for odd dimensions) automatically when not
    supplied.

    :param U: the canonical Youla rotation matrix
    :type U: np.ndarray
    :param axis_pos: index of the fixed axis (auto-detected if omitted)
    :type axis_pos: int | None
    :return: the plane rotation angles
    :rtype: np.ndarray
    """
    ...

def rotation_matrix_skew(upper_tri, create_skew=True):
    """
    **LLM Docstring**

    Exponentiate a skew-symmetric generator into a rotation matrix via its Youla
    decomposition.

    When `create_skew` is set the input may be given as the flattened upper triangle
    (or a non-skew matrix) and is converted to skew form first, then decomposed and
    reassembled as `T U Tᵀ`.

    :param upper_tri: the skew generator (matrix or flattened upper triangle)
    :type upper_tri: np.ndarray
    :param create_skew: coerce the input into a skew matrix first
    :type create_skew: bool
    :return: the corresponding rotation matrix
    :rtype: np.ndarray
    """
    ...

def skew_from_rotation_matrix(rot_mat):
    """
    **LLM Docstring**

    Recover the skew-symmetric generator of a rotation matrix (its matrix
    logarithm), returned as the flattened upper triangle.

    Uses a Schur factorization and the Youla angles to rebuild the skew generator.

    :param rot_mat: the rotation matrix
    :type rot_mat: np.ndarray
    :return: the strict-upper-triangle entries of the skew generator
    :rtype: np.ndarray
    """
    ...

def rotation_matrix_from_angles_vectors(l, T):
    """
    **LLM Docstring**

    Rebuild a rotation matrix from Youla plane angles and the orthogonal frame that
    diagonalizes it.

    For odd dimensions the fixed-axis position is recovered from the angle encoding
    before assembling `T U Tᵀ`.

    :param l: the Youla plane angles (possibly encoding the fixed axis)
    :type l: np.ndarray
    :param T: the orthogonal frame
    :type T: np.ndarray
    :return: the reconstructed rotation matrix
    :rtype: np.ndarray
    """
    ...

def translation_matrix(shift):
    """
    **LLM Docstring**

    Build a 4x4 homogeneous translation matrix (or a stack) for the given shift(s).

    :param shift: the translation vector(s)
    :type shift: np.ndarray
    :return: the homogeneous translation matrix (or stack)
    :rtype: np.ndarray
    """
    ...

def affine_matrix(tmat, shift):
    """Creates an affine transformation matrix from a 3x3 transformation matrix or set of matrices and a shift or set of vecs

    :param tmat: base transformation matrices
    :type tmat: np.ndarray
    :param shift:
    :type shift:
    :return:
    :rtype:
    """
    ...

def view_matrix(up_vector, view_vector=(0, 0, 1), output_order=(2, 0, 1)):
    """
    **LLM Docstring**

    Build a viewing (camera) frame from an up vector and a view direction.

    Orthonormalizes a right/up/view axis triple (handling the degenerate case where
    the up and view vectors are nearly parallel), then reorders and sign-corrects
    the columns according to `output_order` so the returned frame is a proper
    rotation.

    :param up_vector: the up direction(s)
    :type up_vector: np.ndarray
    :param view_vector: the view/forward direction
    :type view_vector: np.ndarray
    :param output_order: axis output ordering (indices or `'x'`/`'y'`/`'z'`)
    :type output_order: tuple
    :return: the viewing frame matrix (or stack)
    :rtype: np.ndarray
    """
    ...
default_near_scaling = 0.001
default_view_angle = np.pi / 4

def perspective_matrix(view_angle=None, aspect=None, near=None, far=None, view_distance=None):
    """
    **LLM Docstring**

    Build a 4x4 perspective-projection matrix from view-frustum parameters.

    The near/far planes are inferred from whichever of `near`, `far`, and
    `view_distance` are supplied; the focal terms are then assembled into the
    standard perspective matrix.

    :param view_angle: the field-of-view angle
    :type view_angle: float | np.ndarray | None
    :param aspect: the aspect ratio
    :type aspect: float | np.ndarray | None
    :param near: near clipping distance
    :type near: float | None
    :param far: far clipping distance
    :type far: float | None
    :param view_distance: distance from camera to the view center
    :type view_distance: float | None
    :return: the perspective-projection matrix (or stack)
    :rtype: np.ndarray
    """
    ...

def world_matrix(bbox=None, view_position=None, rescale=True):
    """
    **LLM Docstring**

    Build the world/model 4x4 matrix that maps object coordinates into the view
    volume.

    With no bounding box a simple translation by `-view_position` is produced;
    given a `bbox` the coordinates are optionally rescaled into a normalized cube
    (`rescale`) and recentered.

    :param bbox: the world bounding box as `(x_range, y_range, z_range)`
    :type bbox: tuple | None
    :param view_position: camera position to translate by
    :type view_position: np.ndarray | None
    :param rescale: rescale the bounding box into a normalized cube
    :type rescale: bool
    :return: the world matrix (or stack)
    :rtype: np.ndarray
    """
    ...
_view_transform = view_matrix
_projection_transform = perspective_matrix
_world_transform = world_matrix

def render_matrix(view_matrix=None, perspective_matrix=None, world_matrix=None, view_position=None, view_center=None, up_vector=None, view_vector=None, right_vector=None, view_angle=None, aspect_ratio=None, view_distance=None, clip_distances=None, bbox=None, rescale_world_coordinates=False, include_perspective=True):
    """
    **LLM Docstring**

    Assemble the full model-view-projection render matrix from a flexible set of
    camera parameters.

    Fills in whichever of the view, world, and perspective matrices are missing
    from the supplied vectors/positions/angles (deriving view center, distance, and
    direction as needed), then multiplies them together, optionally including the
    perspective stage.

    :param view_matrix: an explicit view matrix (derived if omitted)
    :type view_matrix: np.ndarray | None
    :param perspective_matrix: an explicit perspective matrix (derived if omitted)
    :type perspective_matrix: np.ndarray | None
    :param world_matrix: an explicit world matrix (derived if omitted)
    :type world_matrix: np.ndarray | None
    :param view_position: camera position
    :type view_position: np.ndarray | None
    :param view_center: point the camera looks at
    :type view_center: np.ndarray | None
    :param up_vector: camera up direction
    :type up_vector: np.ndarray | None
    :param view_vector: camera view/forward direction
    :type view_vector: np.ndarray | None
    :param right_vector: camera right direction
    :type right_vector: np.ndarray | None
    :param view_angle: field-of-view angle
    :type view_angle: float | np.ndarray | None
    :param aspect_ratio: viewport aspect ratio
    :type aspect_ratio: float | np.ndarray | None
    :param view_distance: camera-to-center distance
    :type view_distance: float | None
    :param clip_distances: `(near, far)` clipping distances
    :type clip_distances: np.ndarray | None
    :param bbox: world bounding box
    :type bbox: tuple | None
    :param rescale_world_coordinates: rescale world coordinates into a unit cube
    :type rescale_world_coordinates: bool
    :param include_perspective: include the perspective projection stage
    :type include_perspective: bool
    :return: the combined render matrix
    :rtype: np.ndarray
    """
    ...

def render_points(points, render_matrix, camera_cull_threshold=1e-08, return_w=False):
    """
    **LLM Docstring**

    Project a set of points through a render matrix into (culled) screen
    coordinates.

    Points are homogenized, transformed, perspective-divided by their `w` component,
    and flagged as in-view when `w` exceeds `camera_cull_threshold`.

    :param points: the points to project
    :type points: np.ndarray
    :param render_matrix: the model-view-projection matrix
    :type render_matrix: np.ndarray
    :param camera_cull_threshold: minimum `w` for a point to be considered in view
    :type camera_cull_threshold: float
    :param return_w: also return the homogeneous `w` component
    :type return_w: bool
    :return: `(projected_points, in_view_mask)` (plus `w` if requested)
    :rtype: tuple
    """
    ...
default_right_vector = [1, 0, 0]
default_up_vector = [0, 1, 0]
default_view_vector = [0, 0, 1]

def rotation_normal_view_matrix(rotation, normal, output_order=('x', 'y', 'z')):
    """
    **LLM Docstring**

    Build a viewing frame from a plane normal and an in-plane rotation angle.

    The up vector is taken either from rotating within the plane by `rotation` or,
    when no rotation is given, from the cross product of the normal with the default
    right vector; the frame is then built with `view_matrix`.

    :param rotation: in-plane rotation angle (or `None`)
    :type rotation: float | None
    :param normal: the plane normal / view direction
    :type normal: np.ndarray | None
    :param output_order: axis output ordering
    :type output_order: tuple
    :return: the viewing frame matrix
    :rtype: np.ndarray
    """
    ...

def reflection_matrix(axes):
    """
    **LLM Docstring**

    Build the reflection matrix that flips the subspace spanned by the given axes.

    The axes are completed to a full basis via QR, the sign of the spanned
    directions is flipped, and the reflection is expressed back in the original
    coordinates. Batched inputs are supported.

    :param axes: the axis (or axes) defining the reflected subspace
    :type axes: np.ndarray
    :return: the reflection matrix (or stack)
    :rtype: np.ndarray
    """
    ...

def permutation_matrix(perm):
    """
    **LLM Docstring**

    Build the permutation matrix (or stack) corresponding to a permutation array.

    Places a `1` at `(i, perm[i])` for each row; batched permutations produce a
    stack of matrices.

    :param perm: the permutation(s)
    :type perm: np.ndarray
    :return: the permutation matrix (or stack)
    :rtype: np.ndarray
    """
    ...

def find_coordinate_matching_permutation(coords, new_coords, return_row_ordering=False, tol=None):
    """
    **LLM Docstring**

    Find the permutation that best matches one set of coordinates to another by
    iterative nearest-neighbour assignment.

    Builds the coordinate distance matrix and greedily pairs up the closest
    remaining atoms, optionally enforcing a maximum-deviation `tol`. Either the
    combined column permutation or the separate row/column orderings can be returned.

    :param coords: the source coordinates
    :type coords: np.ndarray
    :param new_coords: the target coordinates
    :type new_coords: np.ndarray
    :param return_row_ordering: return separate row/column orderings
    :type return_row_ordering: bool
    :param tol: maximum allowed matching deviation (raises if exceeded)
    :type tol: float | None
    :return: the matching permutation (or the row/column orderings)
    :rtype: np.ndarray | tuple
    """
    ...

def symmetry_permutation(coords, op: np.ndarray, return_row_ordering=False, tol=None):
    """
    **LLM Docstring**

    Convert a symmetry operation into the atom permutation it induces on a set of
    coordinates.

    Applies the operation to the coordinates and matches the result back to the
    original atoms with `find_coordinate_matching_permutation`.

    :param coords: the coordinates
    :type coords: np.ndarray
    :param op: the symmetry operation matrix
    :type op: np.ndarray
    :param return_row_ordering: return separate row/column orderings
    :type return_row_ordering: bool
    :param tol: maximum allowed matching deviation
    :type tol: float | None
    :return: the induced permutation (or the row/column orderings)
    :rtype: np.ndarray | tuple
    """
    ...

def apply_symmetries(coords, symmetry_elements: 'list[np.ndarray]', labels=None, tol=0.1):
    """
    **LLM Docstring**

    Grow a set of coordinates by repeatedly applying symmetry operations, keeping
    only the newly generated (non-duplicate) points.

    For each operation the transformed points are compared against the current set
    (within tolerance `tol`) and only distinct new points are appended; optional
    `labels` are propagated alongside.

    :param coords: the seed coordinates
    :type coords: np.ndarray
    :param symmetry_elements: the symmetry operation matrices to apply
    :type symmetry_elements: list[np.ndarray]
    :param labels: optional per-point labels to carry along
    :type labels: Iterable | bool | None
    :param tol: duplicate-detection tolerance
    :type tol: float
    :return: the expanded coordinates (and labels if provided)
    :rtype: np.ndarray | tuple
    """
    ...

def symmetry_reduce(coords, op: np.ndarray, labels=None):
    """
    **LLM Docstring**

    Reduce a set of coordinates to one representative per symmetry orbit under a
    given operation.

    The operation is turned into a permutation, its cycles are found, and the first
    atom of each cycle is kept; optional labels are reduced the same way.

    :param coords: the coordinates to reduce
    :type coords: np.ndarray
    :param op: the symmetry operation matrix
    :type op: np.ndarray
    :param labels: optional per-point labels
    :type labels: Iterable | None
    :return: the orbit representatives (and reduced labels if provided)
    :rtype: np.ndarray | tuple
    """
    ...

class TransformationTypes(enum.Enum):
    """Real access pattern: TransformationTypes.<MemberName> (this is an enum with 6 members, e.g. TransformationTypes.Identity == 0). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
    _MEMBERS = {'Identity': 0, 'Inversion': 1, 'Rotation': 2, 'Reflection': 3, 'ImproperRotation': 4, 'Scaling': 5}

def identify_cartesian_transformation_type(x, max_rotation_order=None):
    """
        **LLM Docstring**

        Classify each Cartesian transformation as identity, inversion, rotation,
        reflection, or improper rotation, extracting its defining data.

        The matrix is polar-decomposed to separate scaling from the orthogonal part,
        then classified by trace/determinant tests; rotations and improper rotations
        additionally yield an axis and (when `max_rotation_order` is given) a rational
        angle expressed as a root/order pair.

        :param x: the transformation matrix (or stack)
        :type x: np.ndarray
        :param max_rotation_order: largest rotation order to rationalize angles against
        :type max_rotation_order: int | None
        :return: `(scalings, types, axes, roots, orders)`
        :rtype: tuple
        """
    ...

def cartesian_transformation_from_data(scalings, types, axes, roots, orders):
    """
    **LLM Docstring**

    Rebuild Cartesian transformation matrices from the classification data
    produced by `identify_cartesian_transformation_type`.

    Each type (identity, inversion, rotation, reflection, improper rotation) is
    reconstructed from its axis/root/order, and any scaling is reapplied on top.

    :param scalings: per-transformation scaling matrices (or `None`)
    :type scalings: np.ndarray | None
    :param types: the transformation type codes
    :type types: np.ndarray
    :param axes: the transformation axes
    :type axes: np.ndarray
    :param roots: the rational angle numerators
    :type roots: np.ndarray
    :param orders: the rational angle denominators (rotation orders)
    :type orders: np.ndarray
    :return: the reconstructed transformation matrices
    :rtype: np.ndarray
    """
    ...