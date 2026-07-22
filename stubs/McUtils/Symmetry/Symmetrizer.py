import collections
import numpy as np
import scipy
from .. import Numputils as nput
from .. import Coordinerds as coordops
from .. import Iterators as itut
from .Elements import *
from .PointGroups import PointGroup
from .SymmetryIdentifier import PointGroupIdentifier
__all__ = ['symmetrize_structure', 'symmetrized_coordinate_coefficients', 'get_internal_permutation_symmetry_matrices', 'symmetrize_internals']

def _symmetry_reduce(coords, op: np.ndarray, labels=None):
    """
    **LLM Docstring**

    Collapse coordinates into one representative per permutation cycle induced by a symmetry operation.

    :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
    :type coords: object
    :param op: Cartesian symmetry-operation matrix.
    :type op: np.ndarray
    :param labels: Optional labels associated with coordinates. Defaults to `None`.
    :type labels: object
    :return: Reduced coordinates, optionally paired with reduced labels.
    :rtype: np.ndarray | tuple[np.ndarray, list]
    """
    ...

def prep_symmetry_operations(symmetry_elements: 'PointGroup|list[SymmetryElement|np.ndarray]'):
    """
    **LLM Docstring**

    Normalize point groups, symmetry elements, and raw matrices into a list of Cartesian transformation arrays.

    :param symmetry_elements: Point group, symmetry elements, or raw transformation matrices.
    :type symmetry_elements: 'PointGroup|list[SymmetryElement|np.ndarray]'
    :return: The operation matrices.
    :rtype: list[np.ndarray]
    """
    ...

def symmetrize_structure(coords, symmetry_elements: 'PointGroup|list[SymmetryElement|np.ndarray]', labels=None, masses=None, groups=None, tol=0.1, mass_tol=1, expand=True):
    """
    **LLM Docstring**

    Reduce each chemically equivalent coordinate group under supplied operations and optionally expand complete symmetry orbits.

    :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
    :type coords: object
    :param symmetry_elements: Point group, symmetry elements, or raw transformation matrices.
    :type symmetry_elements: 'PointGroup|list[SymmetryElement|np.ndarray]'
    :param labels: Optional labels associated with coordinates. Defaults to `None`.
    :type labels: object
    :param masses: Optional atomic masses aligned with `coords`. Defaults to `None`.
    :type masses: object
    :param groups: Optional atom-index groups that constrain equivalence matching. Defaults to `None`.
    :type groups: object
    :param tol: Numerical tolerance used for geometric or equality tests. Defaults to `0.1`.
    :type tol: object
    :param mass_tol: Mass binning tolerance used when grouping atoms. Defaults to `1`.
    :type mass_tol: object
    :param expand: Whether to regenerate full symmetry orbits after reduction. Defaults to `True`.
    :type expand: object
    :return: Symmetrized coordinates, optionally paired with labels.
    :rtype: np.ndarray | tuple[np.ndarray, list]
    """
    ...

def symmetrized_coordinate_coefficients(point_group, coords, masses=None, permutation_basis=None, as_characters=True, normalize=False, perms=None, ops=None, return_basis=None, merge_equivalents=None, drop_empty_modes=None, realign=True, permutation_tol=0.01, **pg_tols):
    """
    **LLM Docstring**

    Build Cartesian or custom permutation representations, optionally project them into character blocks, normalize modes, and merge symmetry-equivalent coordinates.

    :param point_group: Point-group object, name, character table, or operation collection used for symmetrization.
    :type point_group: object
    :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
    :type coords: object
    :param masses: Optional atomic masses aligned with `coords`. Defaults to `None`.
    :type masses: object
    :param permutation_basis: Callable that builds a representation basis from atom permutations. Defaults to `None`.
    :type permutation_basis: object
    :param as_characters: Whether to project the operation basis into irreducible-character blocks. Defaults to `True`.
    :type as_characters: object
    :param normalize: Whether to normalize generated mode vectors. Defaults to `False`.
    :type normalize: object
    :param perms: Precomputed atom permutations for symmetry operations. Defaults to `None`.
    :type perms: object
    :param ops: Precomputed Cartesian symmetry matrices. Defaults to `None`.
    :type ops: object
    :param return_basis: Whether to return the underlying basis metadata. Defaults to `None`.
    :type return_basis: object
    :param merge_equivalents: Whether to merge coordinates connected by the symmetry action. Defaults to `None`.
    :type merge_equivalents: object
    :param drop_empty_modes: Whether to remove zero-norm modes. Defaults to `None`.
    :type drop_empty_modes: object
    :param realign: Whether to orient the returned point group in the molecular principal-axis frame. Defaults to `True`.
    :type realign: object
    :param permutation_tol: Tolerance used to infer atom permutations from transformed coordinates. Defaults to `0.01`.
    :type permutation_tol: object
    :param pg_tols: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
    :type pg_tols: dict
    :return: Symmetry-adapted mode coefficients, optionally with the generated basis.
    :rtype: object
    """
    ...

def get_internal_permutation_symmetry_matrices(internals, permutations):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param internals: Internal-coordinate definitions.
    :type internals: object
    :param permutations: Atom permutations for each symmetry operation.
    :type permutations: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def symmetrize_internals(point_group, internals, cartesians=None, *, masses=None, as_characters=True, normalize=None, perms=None, return_expansions=False, return_base_expansion=False, ops=None, atom_selection=None, reduce_redundant_coordinates=None, **etc):
    """
    **LLM Docstring**

    Generate symmetry-adapted internal-coordinate coefficients and optionally Cartesian expansion tensors and redundant-coordinate reductions.

    :param point_group: Point-group object, name, character table, or operation collection used for symmetrization.
    :type point_group: object
    :param internals: Internal-coordinate definitions.
    :type internals: object
    :param cartesians: Cartesian coordinates or, in supported integer-shaped cases, explicit atom permutations. Defaults to `None`.
    :type cartesians: object
    :param masses: Optional atomic masses aligned with `coords`. Defaults to `None`.
    :type masses: object
    :param as_characters: Whether to project the operation basis into irreducible-character blocks. Defaults to `True`.
    :type as_characters: object
    :param normalize: Whether to normalize generated mode vectors. Defaults to `None`.
    :type normalize: object
    :param perms: Precomputed atom permutations for symmetry operations. Defaults to `None`.
    :type perms: object
    :param return_expansions: Whether, and to what tensor order, internal-coordinate expansions are returned. Defaults to `False`.
    :type return_expansions: object
    :param return_base_expansion: Whether to include the unsymmetrized base expansion. Defaults to `False`.
    :type return_base_expansion: object
    :param ops: Precomputed Cartesian symmetry matrices. Defaults to `None`.
    :type ops: object
    :param atom_selection: Optional atom subset used for the symmetry analysis. Defaults to `None`.
    :type atom_selection: object
    :param reduce_redundant_coordinates: Whether to construct a reduced redundant-coordinate transformation. Defaults to `None`.
    :type reduce_redundant_coordinates: object
    :param etc: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
    :type etc: dict
    :return: A tuple containing coefficients, basis coordinates, and any requested expansions.
    :rtype: tuple
    """
    ...

def symmetrized_internal_coordinate_expansions(coeffs, cartesians, full_basis, order=1, masses=None, return_inverse=False, normalized_coefficients=True, return_base_expansion=False):
    """
    **LLM Docstring**

    Transform internal-coordinate derivative tensors into each symmetry-adapted coefficient block, optionally including inverse and base expansions.

    :param coeffs: Symmetry-adapted coordinate coefficient blocks.
    :type coeffs: object
    :param cartesians: Cartesian coordinates or, in supported integer-shaped cases, explicit atom permutations.
    :type cartesians: object
    :param full_basis: Internal-coordinate basis returned by the permutation representation.
    :type full_basis: object
    :param order: Order of the rotation or improper rotation. Defaults to `1`.
    :type order: object
    :param masses: Optional atomic masses aligned with `coords`. Defaults to `None`.
    :type masses: object
    :param return_inverse: Whether inverse expansion tensors are also returned. Defaults to `False`.
    :type return_inverse: object
    :param normalized_coefficients: Whether coefficient transposes can be used as inverses. Defaults to `True`.
    :type normalized_coefficients: object
    :param return_base_expansion: Whether to include the unsymmetrized base expansion. Defaults to `False`.
    :type return_base_expansion: object
    :return: Symmetry-adapted expansion tensors, optionally paired with base expansions.
    :rtype: object
    """
    ...