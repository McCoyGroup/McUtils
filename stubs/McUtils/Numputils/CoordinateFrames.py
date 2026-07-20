__all__ = ['center_of_mass', 'inertia_tensors', 'moments_of_inertia', 'moments_of_inertia_expansion', 'inertial_frame_derivatives', 'frame_displacement_projector', 'translation_rotation_eigenvectors', 'translation_rotation_projector', 'remove_translation_rotations', 'translation_rotation_invariant_transformation', 'eckart_embedding', 'rmsd_minimizing_transformation', 'eckart_permutation', 'eckart_rmsd', 'incremental_eckart_rmsd']
import itertools, collections
import numpy as np, scipy.optimize as opt
from . import VectorOps as vec_ops
from . import PermutationOps as perm_ops
from . import TensorDerivatives as td

def center_of_mass(coords, masses=None):
    """Gets the center of mass for the coordinates

    :param coords:
    :type coords: CoordinateSet
    :param masses:
    :type masses:
    :return:
    :rtype:
    """
    ...

def inertia_tensors(coords, masses=None, mass_weighted=False, return_com=False):
    """
    Computes the moment of intertia tensors for the walkers with coordinates coords (assumes all have the same masses)

    :param coords:
    :type coords: CoordinateSet
    :param masses:
    :type masses: np.ndarray
    :return:
    :rtype:
    """
    ...

def inertial_frame_derivatives(coords, masses=None, sel=None, mass_weighted=True):
    """
    **LLM Docstring**

    Compute the first and second derivatives of the moment-of-inertia tensor with
    respect to the (mass-weighted) Cartesian coordinates.

    Working in center-of-mass, mass-weighted coordinates, the first derivatives are
    assembled from the standard inertia-tensor identities and reshaped to `(3N, 3,
    3)`; the second derivatives are coordinate-independent and nonzero only on the
    diagonal atom blocks, so one block is built and tiled to `(3N, 3N, 3, 3)`. When
    `mass_weighted` is off the derivatives are un-weighted by `M^{1/2}`.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param sel: optional subset of atoms to include
    :type sel: Iterable[int] | None
    :param mass_weighted: whether to return mass-weighted derivatives
    :type mass_weighted: bool
    :return: `[first_derivatives, second_derivatives]` of the inertia tensor
    :rtype: list[np.ndarray]
    """
    ...

def moments_of_inertia(coords, masses=None, force_rotation=True, return_com=False):
    """
    Computes the moment of inertia tensor for the walkers with coordinates coords (assumes all have the same masses)

    :param coords:
    :type coords: CoordinateSet
    :param masses:
    :type masses: np.ndarray
    :return:
    :rtype:
    """
    ...

def moments_of_inertia_expansion(coords, masses=None, order=1, force_rotation=True, mass_weighted=True):
    """
    **LLM Docstring**

    Compute the derivative expansion of the moments of inertia (eigenvalues) and
    principal axes (eigenvectors) with respect to the Cartesian coordinates.

    The inertia tensor and its derivatives (from `inertial_frame_derivatives`) form
    an expansion that is fed, together with the base eigenvalues/eigenvectors, to
    `TensorDerivatives.mateigh_deriv`; the eigenvalue derivatives are read off the
    diagonal of the resulting tensors.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param order: maximum derivative order
    :type order: int
    :param force_rotation: force a proper-rotation (right-handed) axis convention
    :type force_rotation: bool
    :param mass_weighted: whether the expansion is mass-weighted
    :type mass_weighted: bool
    :return: `(eigenvalue_expansion, eigenvector_expansion)`
    :rtype: tuple[list, list]
    """
    ...

def translation_rotation_eigenvectors(coords, masses=None, mass_weighted=True, ref=None, ref_masses=None, axes=None, align_with_frame=True, return_values=False, return_com=False, return_rot=True, return_principle_axes=False):
    """
    Returns the eigenvectors corresponding to translations and rotations
    in the system

    :param coords:
    :type coords:
    :param masses:
    :type masses:
    :return:
    :rtype:
    """
    ...

def frame_displacement_projector(tr_modes, masses, mass_weighted=False, orthonormal=True, pre_weighted=False):
    """
    **LLM Docstring**

    Build the projector that removes a set of frame (translation/rotation) modes
    from a displacement space.

    Depending on `mass_weighted` and `pre_weighted`, the appropriate left inverse of
    the mode matrix is formed (applying or assuming the `M^{±1/2}` weighting), then
    the complementary projector `I - L Lᵀ` is assembled — orthonormally via
    `orthogonal_projection_matrix` when `orthonormal` is set, otherwise by an
    explicit contraction.

    :param tr_modes: the translation/rotation mode vectors
    :type tr_modes: np.ndarray
    :param masses: per-atom masses
    :type masses: np.ndarray
    :param mass_weighted: whether the output space should be mass-weighted
    :type mass_weighted: bool
    :param orthonormal: whether the modes are orthonormal
    :type orthonormal: bool
    :param pre_weighted: whether the modes already carry the mass weighting
    :type pre_weighted: bool
    :return: the frame-removing projector
    :rtype: np.ndarray
    """
    ...

def translation_rotation_projector(coords, masses=None, mass_weighted=False, return_modes=False, orthonormal=True):
    """
    **LLM Docstring**

    Build the projector that removes overall translation and rotation from a
    Cartesian displacement space.

    The translation/rotation eigenvectors are obtained from
    `translation_rotation_eigenvectors` and passed to
    `frame_displacement_projector`. The mode vectors themselves can optionally be
    returned alongside the projector.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param mass_weighted: whether the output space should be mass-weighted
    :type mass_weighted: bool
    :param return_modes: also return the translation/rotation modes
    :type return_modes: bool
    :param orthonormal: whether to build an orthonormal projector
    :type orthonormal: bool
    :return: the projector (and the modes if `return_modes`)
    :rtype: np.ndarray | tuple
    """
    ...

def remove_translation_rotations(expansion, coords, masses=None, mass_weighted=False):
    """
    **LLM Docstring**

    Apply the translation/rotation projector to every tensor in a derivative
    expansion, removing the overall translation/rotation content from each
    Cartesian axis.

    :param expansion: the derivative expansion `[value, d1, d2, ...]`
    :type expansion: list[np.ndarray]
    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param mass_weighted: whether the working space is mass-weighted
    :type mass_weighted: bool
    :return: the projected expansion
    :rtype: list[np.ndarray]
    """
    ...

def translation_rotation_invariant_transformation(coords, masses=None, mass_weighted=True, strip_embedding=True):
    """
    **LLM Docstring**

    Construct the transformation (and its inverse) into the space of internal,
    translation/rotation-invariant coordinates.

    The translation/rotation projector is diagonalized; the near-zero eigenvectors
    are replaced by the exact translation/rotation modes, and the remaining
    eigenvectors span the invariant subspace (optionally stripped of the embedding
    directions). The transformation and inverse are un-mass-weighted with `M^{±1/2}`
    when `mass_weighted` is off.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param mass_weighted: whether to keep the transformation mass-weighted
    :type mass_weighted: bool
    :param strip_embedding: drop the translation/rotation columns from the result
    :type strip_embedding: bool
    :return: `(transformation, inverse)`
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    ...
EmbeddingData = collections.namedtuple('PrincipleAxisData', ['coords', 'com', 'axes'])
EckartData = collections.namedtuple('EckartData', ['rotations', 'coordinates', 'reference_data', 'coord_data'])

def principle_axis_embedded_coords(coords, masses=None, sel=None):
    """
    Returns coordinate embedded in the principle axis frame

    :param coords:
    :type coords:
    :param masses:
    :type masses:
    :return:
    :rtype:
    """
    ...

def _prep_eckart_data(ref, coords, masses, in_paf=False, sel=None):
    """
    **LLM Docstring**

    Prepare a reference and a set of coordinates for an Eckart embedding.

    Unless the inputs are already in the principal-axis frame (`in_paf`), both the
    coordinates and the reference are moved into their principal-axis embeddings.
    Atoms are optionally restricted to `sel`, dummy atoms (non-positive mass) are
    dropped, and the reference is broadcast to match a stacked set of coordinates.

    :param ref: the reference geometry
    :type ref: np.ndarray
    :param coords: the coordinates to embed
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param in_paf: whether the inputs are already in the principal-axis frame
    :type in_paf: bool
    :param sel: optional subset of atoms to use
    :type sel: Iterable[int] | None
    :return: `((ref, ref_com, ref_axes), (coords, com, axes), masses,
        (original_ref, original_coords))`
    :rtype: tuple
    """
    ...

def _eckart_embedding(ref, coords, masses=None, sel=None, in_paf=False, planar_ref_tolerance=1e-06, proper_rotation=False, permutable_groups=None, reset_com=True, transform_coordinates=True):
    """
    Generates the Eckart rotation that will align ref and coords, assuming initially that `ref` and `coords` are
    in the principle axis frame

    :param masses:
    :type masses:
    :param ref:
    :type ref:
    :param coords:
    :type coords: np.ndarray
    :return:
    :rtype:
    """
    ...

def eckart_embedding(ref, coords, masses=None, sel=None, in_paf=False, planar_ref_tolerance=1e-06, proper_rotation=False, permutable_groups=None, reset_com=True, transform_coordinates=True) -> EckartData:
    """
    **LLM Docstring**

    Compute the Eckart embedding that rotates a set of coordinates into maximal
    alignment with a reference geometry.

    Thin public wrapper over the internal `_eckart_embedding`, forwarding all
    options (atom selection, principal-axis handling, planarity tolerance,
    proper-rotation constraint, permutable groups, center-of-mass reset, and whether
    to actually transform the coordinates).

    :param ref: the reference geometry
    :type ref: np.ndarray
    :param coords: the coordinates to embed
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param sel: optional subset of atoms used to define the embedding
    :type sel: Iterable[int] | None
    :param in_paf: whether the inputs are already in the principal-axis frame
    :type in_paf: bool
    :param planar_ref_tolerance: tolerance for detecting a planar reference
    :type planar_ref_tolerance: float
    :param proper_rotation: restrict the embedding to proper rotations
    :type proper_rotation: bool
    :param permutable_groups: groups of atoms allowed to permute
    :type permutable_groups: Iterable | None
    :param reset_com: re-center on the center of mass after embedding
    :type reset_com: bool
    :param transform_coordinates: apply the rotation to the coordinates
    :type transform_coordinates: bool
    :return: the Eckart embedding data
    :rtype: EckartData
    """
    ...
rmsd_minimizing_transformation = eckart_embedding

def eckart_permutation(ref, coords, masses=None, sel=None, in_paf=False, prealign=False, planar_ref_tolerance=1e-06, proper_rotation=False, permutable_groups=None):
    """
    **LLM Docstring**

    Find, for each structure, the atom permutation that best matches a reference
    under the Eckart embedding.

    Optionally pre-aligns the coordinates, then works group by group over the
    `permutable_groups`: for each group it Eckart-embeds, builds the mass-weighted
    distance matrix between embedded coordinates and reference atoms, and solves the
    assignment problem (`scipy.optimize.linear_sum_assignment`) to get the optimal
    relabeling.

    :param ref: the reference geometry
    :type ref: np.ndarray
    :param coords: the coordinates to permute
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param sel: optional subset of atoms to consider
    :type sel: Iterable[int] | None
    :param in_paf: whether the inputs are already in the principal-axis frame
    :type in_paf: bool
    :param prealign: Eckart-align the coordinates before matching
    :type prealign: bool
    :param planar_ref_tolerance: tolerance for detecting a planar reference
    :type planar_ref_tolerance: float
    :param proper_rotation: restrict embeddings to proper rotations
    :type proper_rotation: bool
    :param permutable_groups: groups of atoms allowed to permute (defaults to all)
    :type permutable_groups: Iterable | None
    :return: the optimal per-structure atom permutations
    :rtype: np.ndarray
    """
    ...

def eckart_displacement_coords(coords, ref, masses=None, **embedding_parameters):
    """
    **LLM Docstring**

    Express Eckart-embedded coordinates in the reference's translation/rotation-
    invariant (internal) coordinate frame.

    The reference's invariant transformation (from
    `translation_rotation_invariant_transformation`) is applied to the Eckart-embedded
    coordinates.

    :param coords: the coordinates to embed and project
    :type coords: np.ndarray
    :param ref: the reference geometry
    :type ref: np.ndarray
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param embedding_parameters: extra options forwarded to `eckart_embedding`
    :return: the displacement coordinates in the reference internal frame
    :rtype: np.ndarray
    """
    ...

def eckart_rmsd(coords, ref, masses=None, embed=True, comparison_sel=None, embedding_sel=None, mass_weighted=False, return_diffs=False, averaged=False, total=False, **embedding_parameters):
    """
    **LLM Docstring**

    Compute the RMSD between a set of coordinates and a reference after Eckart
    embedding.

    The coordinates are optionally Eckart-embedded onto the reference (using
    `embedding_sel`), optionally mass-weighted, and optionally restricted to
    `comparison_sel` before the (unaligned) RMSD is taken with
    `unembedded_pts_rmsd`.

    :param coords: the coordinates to compare
    :type coords: np.ndarray
    :param ref: the reference geometry
    :type ref: np.ndarray
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param embed: whether to Eckart-embed before comparing
    :type embed: bool
    :param comparison_sel: atoms included in the RMSD
    :type comparison_sel: Iterable[int] | None
    :param embedding_sel: atoms used to define the embedding
    :type embedding_sel: Iterable[int] | None
    :param mass_weighted: mass-weight the coordinates before comparison
    :type mass_weighted: bool
    :param return_diffs: also return the difference vectors
    :type return_diffs: bool
    :param averaged: per-atom rather than per-coordinate normalization
    :type averaged: bool
    :param total: apply the per-atom normalization
    :type total: bool
    :param embedding_parameters: extra options forwarded to `eckart_embedding`
    :return: the Eckart RMSD (plus diffs if requested)
    :rtype: np.ndarray | tuple
    """
    ...

def incremental_eckart_rmsd(coords, refs=None, masses=None, mass_weighted=False, **embedding_parameters):
    """
    **LLM Docstring**

    Compute the cumulative Eckart RMSD along a sequence of geometries.

    Consecutive structures are compared pairwise with `eckart_rmsd` (or against the
    supplied `refs`), and the resulting step RMSDs are cumulatively summed to give a
    running path length; a leading zero is prepended so the output aligns with the
    input sequence.

    :param coords: the sequence of geometries
    :type coords: np.ndarray
    :param refs: explicit references per step (defaults to the previous frame)
    :type refs: np.ndarray | None
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param mass_weighted: mass-weight the coordinates before comparison
    :type mass_weighted: bool
    :param embedding_parameters: extra options forwarded to `eckart_rmsd`
    :return: the cumulative Eckart RMSD along the sequence
    :rtype: np.ndarray
    """
    ...