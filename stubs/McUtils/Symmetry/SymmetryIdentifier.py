from __future__ import annotations
import abc
import numpy as np
import enum
import itertools
import McUtils.Numputils as nput
import McUtils.Combinatorics as comb
from .Elements import *
from .PointGroups import *
from .Rotors import RotorTypes, identify_rotor_type
__all__ = ['PointGroupIdentifier', 'identify_symmetry_equivalent_atoms', 'identify_point_group']

class SymmetryEquivalentAtomData:
    __slots__ = ['coords', 'moms', 'com', 'axes', 'rotor_type', 'planar']
    coords: np.ndarray

    def __init__(self, coords, moms, com, axes, rotor_type, planar):
        """
        **LLM Docstring**

        Store centered coordinates, principal moments, center of mass, principal axes, rotor classification, and planarity.

        :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
        :type coords: object
        :param moms: Value used as `moms` by the implementation.
        :type moms: object
        :param com: Value used as `com` by the implementation.
        :type com: object
        :param axes: Requested Cartesian embedding axes.
        :type axes: object
        :param rotor_type: Value used as `rotor_type` by the implementation.
        :type rotor_type: object
        :param planar: Value used as `planar` by the implementation.
        :type planar: object
        :return: No value is returned.
        :rtype: None
        """
        ...

def identify_symmetry_equivalent_atoms(coords, masses=None, base_groups=None, mass_tol=1, tol=0.01):
    """
    **LLM Docstring**

    Partition atoms into groups with matching masses and sorted intragroup distance profiles.

    :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
    :type coords: object
    :param masses: Optional atomic masses aligned with `coords`. Defaults to `None`.
    :type masses: object
    :param base_groups: Initial atom groups within which geometric equivalence is tested. Defaults to `None`.
    :type base_groups: object
    :param mass_tol: Mass binning tolerance used when grouping atoms. Defaults to `1`.
    :type mass_tol: object
    :param tol: Numerical tolerance used for geometric or equality tests. Defaults to `0.01`.
    :type tol: object
    :return: Lists of atom indices judged symmetry equivalent.
    :rtype: list[list[int]]
    """
    ...

class PointGroupIdentifier:

    def __init__(self, coords, masses=None, groups=None, tol=0.01, mass_tol=1, mom_tol=1, grouping_tol=0.01, verbose=False):
        """
        **LLM Docstring**

        Prepare atom-equivalence groups, principal-axis coordinates, group rotation orders, and per-group rotor data for point-group detection.

        :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
        :type coords: object
        :param masses: Optional atomic masses aligned with `coords`. Defaults to `None`.
        :type masses: object
        :param groups: Optional atom-index groups that constrain equivalence matching. Defaults to `None`.
        :type groups: object
        :param tol: Numerical tolerance used for geometric or equality tests. Defaults to `0.01`.
        :type tol: object
        :param mass_tol: Mass binning tolerance used when grouping atoms. Defaults to `1`.
        :type mass_tol: object
        :param mom_tol: Tolerance used to compare principal moments of inertia. Defaults to `1`.
        :type mom_tol: object
        :param grouping_tol: Distance-profile tolerance used to identify equivalent atoms. Defaults to `0.01`.
        :type grouping_tol: object
        :param verbose: Whether to print diagnostic information. Defaults to `False`.
        :type verbose: object
        :return: No value is returned.
        :rtype: None
        """
        ...

    def get_groups(self, coords, base_groups):
        """
        **LLM Docstring**

        Refine supplied atom groups by matching sorted distance profiles and merging overlapping equivalence sets.

        :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
        :type coords: object
        :param base_groups: Initial atom groups within which geometric equivalence is tested.
        :type base_groups: object
        :return: The refined atom-index groups.
        :rtype: list[list[int]]
        """
        ...

    def get_rotor_type(self, moms):
        """
        **LLM Docstring**

        Classify principal moments using the identifier moment tolerance.

        :param moms: Value used as `moms` by the implementation.
        :type moms: object
        :return: The rotor type and planarity flag.
        :rtype: tuple[RotorTypes, bool]
        """
        ...

    def get_group_orders(self):
        """
        **LLM Docstring**

        Derive candidate proper-rotation orders from common factors of equivalent-atom group sizes.

        :return: Candidate orders sorted from largest to smallest.
        :rtype: list[int]
        """
        ...

    def check_element(self, elem: SymmetryElement, verbose=False):
        """
        **LLM Docstring**

        Test whether a candidate operation maps every equivalent-atom group onto itself within coordinate tolerances.

        :param elem: Candidate symmetry element.
        :type elem: SymmetryElement
        :param verbose: Whether to print diagnostic information. Defaults to `False`.
        :type verbose: object
        :return: Whether the element is a molecular symmetry.
        :rtype: bool
        """
        ...

    def get_groups_from_masses(self, masses):
        """
        **LLM Docstring**

        Group atom indices by rounded mass values.

        :param masses: Optional atomic masses aligned with `coords`.
        :type masses: object
        :return: Mass-equivalent atom groups.
        :rtype: list[np.ndarray]
        """
        ...

    def prep_coords(self, coords, masses=None):
        """
        **LLM Docstring**

        Center coordinates, diagonalize the inertia tensor, rotate into principal axes, and classify rotor type and planarity.

        :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
        :type coords: object
        :param masses: Optional atomic masses aligned with `coords`. Defaults to `None`.
        :type masses: object
        :return: Prepared coordinate metadata.
        :rtype: SymmetryEquivalentAtomData
        """
        ...

    def rotation_axis_iterator(self):
        """
        **LLM Docstring**

        Yield candidate rotation axes from Cartesian basis axes, atom directions, and pair midpoints while suppressing collinear duplicates.

        :return: An iterator over normalized axis vectors.
        :rtype: typing.Iterator[np.ndarray]
        """
        ...

    def reflection_plane_iterator(self):
        """
        **LLM Docstring**

        Yield candidate reflection-plane normals from Cartesian axes and pairwise coordinate differences.

        :return: An iterator over plane-normal vectors.
        :rtype: typing.Iterator[np.ndarray]
        """
        ...

    def rotation_face_iterator(self):
        """
        **LLM Docstring**

        Yield normals to equilateral-like faces formed by triples of equivalent atoms.

        :return: An iterator over candidate rotation axes.
        :rtype: typing.Iterator[np.ndarray]
        """
        ...

    def embed_point_group(self, point_group: 'PointGroup|list[SymmetryElement]'):
        """
        **LLM Docstring**

        Construct the hard-coded or analytic character table for the `embed` group family.

        :param point_group: Point-group object, name, character table, or operation collection used for symmetrization.
        :type point_group: 'PointGroup|list[SymmetryElement]'
        :return: The square character table with irreducible representations along rows.
        :rtype: np.ndarray
        """
        ...

    def find_point_group_alignment_axes(self, point_group: 'PointGroup|list[SymmetryElement]'):
        """
        **LLM Docstring**

        Match defining rotations or reflection planes from a reference group to molecular symmetry elements and construct embedded axes.

        :param point_group: Point-group object, name, character table, or operation collection used for symmetrization.
        :type point_group: 'PointGroup|list[SymmetryElement]'
        :return: A `3 x 3` axis matrix in the original Cartesian frame.
        :rtype: np.ndarray
        """
        ...

    def identify_point_group(self, realign=True) -> tuple[list[SymmetryElement], PointGroup]:
        """
        **LLM Docstring**

        Construct the hard-coded or analytic character table for the `identify` group family.

        :param realign: Whether to orient the returned point group in the molecular principal-axis frame. Defaults to `True`.
        :type realign: object
        :return: The square character table with irreducible representations along rows.
        :rtype: np.ndarray
        """
        ...

def identify_point_group(coords, masses=None, groups=None, tol=1e-08, mass_tol=1, mom_tol=1, grouping_tol=0.01, realign=True, verbose=False):
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `identify` group family.

    :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
    :type coords: object
    :param masses: Optional atomic masses aligned with `coords`. Defaults to `None`.
    :type masses: object
    :param groups: Optional atom-index groups that constrain equivalence matching. Defaults to `None`.
    :type groups: object
    :param tol: Numerical tolerance used for geometric or equality tests. Defaults to `1e-08`.
    :type tol: object
    :param mass_tol: Mass binning tolerance used when grouping atoms. Defaults to `1`.
    :type mass_tol: object
    :param mom_tol: Tolerance used to compare principal moments of inertia. Defaults to `1`.
    :type mom_tol: object
    :param grouping_tol: Distance-profile tolerance used to identify equivalent atoms. Defaults to `0.01`.
    :type grouping_tol: object
    :param realign: Whether to orient the returned point group in the molecular principal-axis frame. Defaults to `True`.
    :type realign: object
    :param verbose: Whether to print diagnostic information. Defaults to `False`.
    :type verbose: object
    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...