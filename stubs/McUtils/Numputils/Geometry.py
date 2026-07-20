from __future__ import annotations
'\nProvides analytic derivatives for some common base terms with the hope that we can reuse them elsewhere\n'
import abc
import collections
import itertools
import math
import enum
import warnings
import numpy as np
import scipy
from .. import Devutils as dev
from .VectorOps import *
from . import TensorDerivatives as td
from . import Misc as misc
from . import TransformationMatrices as tmats
from .Options import Options
from .Lebedev import lebedev_grid, lebedev_rule
__all__ = ['triangle_convert', 'triangle_converter', 'triangle_area', 'TriangleData', 'make_triangle', 'make_symbolic_triangle', 'triangle_property_specifiers', 'triangle_completions', 'triangle_completion_paths', 'enumerate_triangle_completions', 'triangle_is_complete', 'triangle_property_function', 'DihedralTetrahedronData', 'make_dihedron', 'make_symbolic_dihedron', 'dihedron_property_specifiers', 'dihedral_completions', 'dihedral_completion_paths', 'dihedron_is_complete', 'enumerate_dihedron_completions', 'sorted_dihedron_completions', 'dihedron_triangle', 'dihedron_property_function', 'dihedron_pair_dihedral_angle_function', 'arcsin_deriv', 'arccos_deriv', 'arctan_deriv', 'sin_deriv', 'cos_deriv', 'tan_deriv', 'cot_deriv', 'axis_rot_gen_deriv', 'angle_arc_parameters', 'arc_points', 'arc_angles_from_endpoints', 'arc_center_from_endpoints', 'arc_points_from_endpoints', 'bezier_coeffs', 'bezier_eval', 'bezier_solve', 'bezier_curvature', 'polygon_normal', 'triangulate_polygon', 'refine_curve', 'parametric_curve_evaluate', 'parametric_curvature', 'parametric_path_points', 'parameteric_spline_interpolate', 'parameteric_interpolation_curvature', 'check_triangle_intersection', 'check_bbox_intersections', 'check_interval_overlaps', 'check_line_intersection', 'check_segment_intersection', 'uv_mapping', 'fibonacci_sphere', 'lebedev_grid', 'lebedev_rule']

def law_of_cosines_cos(a, b, c):
    ...

def law_of_sines_sin(a, b, A):
    ...

def law_of_sines_dist(a, B, A):
    ...

def law_of_cosines_dist(a, b, C):
    ...

def tri_sss_area(a, b, c):
    ...

def tri_sas_area(a, C, b):
    ...

def tri_sss_to_sas(a, b, c):
    ...

def tri_sss_to_ssa(a, b, c):
    ...

def tri_sss_to_saa(a, b, c):
    ...

def tri_sss_to_asa(a, b, c):
    ...

def tri_sas_to_sss(a, C, b):
    ...

def tri_sas_to_ssa(a, C, b):
    ...

def tri_sas_to_saa(a, C, b):
    ...

def tri_sas_to_asa(a, C, b):
    ...

def _check_ssa(a, b, A):
    ...

class SSAWarning(UserWarning):
    ...

def tri_ssa_to_sas(a, b, A):
    ...

def tri_ssa_to_saa(a, b, A):
    ...

def tri_ssa_to_asa(a, b, A):
    ...

def tri_ssa_to_sss(a, b, A):
    ...

def tri_saa_to_ssa(a, B, A):
    ...

def tri_saa_to_sas(a, B, A):
    ...

def tri_saa_to_asa(a, B, A):
    ...

def tri_saa_to_sss(a, B, A):
    ...

def tri_asa_to_saa(C, a, B):
    ...

def tri_asa_to_sas(C, a, B):
    ...

def tri_asa_to_ssa(C, a, B):
    ...

def tri_asa_to_sss(C, a, B):
    ...

def law_of_cosines_cos_deriv(a_expansion, b_expansion, c_expansion, order, return_components=False, a2_expansion=None, b2_expansion=None, c2_expansion=None, abinv_expansion=None, ab_expansion=None):
    ...

def power_deriv(term, p, order):
    ...

def square_deriv(term, order):
    ...

def sqrt_deriv(term, order):
    ...

def cos_deriv(term, order):
    ...

def sin_deriv(term, order):
    ...

def legendre_scaling(n):
    ...

def legendre_integer_coefficients(n):
    ...

def arcsin_deriv(term, order):
    ...

def arccos_deriv(term, order):
    ...

def tan_integer_coefficients(n):
    ...

def tan_deriv(term, order):
    ...

def cot_deriv(term, order):
    ...

def arctan_deriv(term, order):
    ...

def law_of_cosines_dist_deriv(a_expansion, b_expansion, C_expansion, order, return_components=False, a2_expansion=None, b2_expansion=None, abcosC_expansion=None, ab_expansion=None, cosC_expansion=None, return_square=False):
    ...

def law_of_sines_sin_deriv(a_expansion, b_expansion, A_expansion, order, return_components=False, sinA_expansion=None, binva_expansion=None, ainv_expansion=None):
    ...

def law_of_sines_dist_deriv(a_expansion, B_expansion, A_expansion, order, return_components=False, sinBinvsinA_expansion=None, sinA_expansion=None, sinB_expansion=None, sinAinv_expansion=None):
    ...

def _angle_complement_expansion(A_expansion, B_expansion):
    ...

def tri_sss_to_sas_deriv(a_expansion, b_expansion, c_expansion, order, return_components=False, return_cos=False, a2_expansion=None, b2_expansion=None, c2_expansion=None, abinv_expansion=None, ab_expansion=None, cosC_expansion=None):
    ...

def tri_sss_to_ssa_deriv(a_expansion, b_expansion, c_expansion, order, return_components=False, return_cos=False, a2_expansion=None, b2_expansion=None, c2_expansion=None, bcinv_expansion=None, bc_expansion=None, cosA_expansion=None):
    ...

def tri_sss_to_saa_deriv(a_expansion, b_expansion, c_expansion, order, return_components=False, return_cos=False, a2_expansion=None, b2_expansion=None, c2_expansion=None, acinv_expansion=None, ac_expansion=None, bcinv_expansion=None, bc_expansion=None, cosA_expansion=None, cosB_expansion=None):
    ...

def tri_sss_to_asa_deriv(a_expansion, b_expansion, c_expansion, order, return_components=False, return_cos=False, a2_expansion=None, b2_expansion=None, c2_expansion=None, abinv_expansion=None, ab_expansion=None, acinv_expansion=None, ac_expansion=None, cosB_expansion=None, cosC_expansion=None):
    ...

def tri_sas_to_sss_deriv(a_expansion, C_expansion, b_expansion, order, return_components=False, a2_expansion=None, b2_expansion=None, abcosC_expansion=None, ab_expansion=None, cosC_expansion=None, return_square=False):
    ...

def tri_sas_to_ssa_deriv(a_expansion, b_expansion, C_expansion, order, return_components=False, return_cos=False, a2_expansion=None, b2_expansion=None, c2_expansion=None, abcosC_expansion=None, ab_expansion=None, cosC_expansion=None, bcinv_expansion=None, bc_expansion=None, cosA_expansion=None):
    ...

def tri_sas_to_saa_deriv(a_expansion, b_expansion, C_expansion, order, return_components=False, return_cos=False, a2_expansion=None, b2_expansion=None, c2_expansion=None, abcosC_expansion=None, ab_expansion=None, cosC_expansion=None, acinv_expansion=None, ac_expansion=None, bcinv_expansion=None, bc_expansion=None, cosA_expansion=None, cosB_expansion=None):
    ...

def tri_sas_to_asa_deriv(a_expansion, b_expansion, C_expansion, order, return_components=False, return_cos=False, a2_expansion=None, b2_expansion=None, c2_expansion=None, abcosC_expansion=None, ab_expansion=None, cosC_expansion=None, abinv_expansion=None, acinv_expansion=None, ac_expansion=None, cosB_expansion=None):
    ...

def tri_ssa_to_sas_deriv(a_expansion, b_expansion, A_expansion, order, return_components=False, sinA_expansion=None, binva_expansion=None, ainv_expansion=None, B_expansion=None, sinB_expansion=None):
    ...

def tri_ssa_to_saa_deriv(a_expansion, b_expansion, A_expansion, order, return_components=False, sinA_expansion=None, binva_expansion=None, ainv_expansion=None, B_expansion=None, sinB_expansion=None):
    ...

def tri_ssa_to_asa_deriv(a_expansion, b_expansion, A_expansion, order, return_components=False, sinA_expansion=None, binva_expansion=None, ainv_expansion=None, B_expansion=None, sinB_expansion=None):
    ...

def tri_ssa_to_sss_deriv(a_expansion, b_expansion, A_expansion, order, return_components=False, sinA_expansion=None, binva_expansion=None, ainv_expansion=None, B_expansion=None, sinB_expansion=None, a2_expansion=None, b2_expansion=None, abcosC_expansion=None, ab_expansion=None, cosC_expansion=None):
    ...

def tri_saa_to_ssa_deriv(a_expansion, B_expansion, A_expansion, order, return_components=False, sinBinvsinA_expansion=None, sinA_expansion=None, sinB_expansion=None, sinAinv_expansion=None):
    ...

def tri_saa_to_sas_deriv(a_expansion, B_expansion, A_expansion, order, return_components=False, sinBinvsinA_expansion=None, sinA_expansion=None, sinB_expansion=None, sinAinv_expansion=None):
    ...

def tri_saa_to_asa_deriv(a_expansion, B_expansion, A_expansion, order):
    ...

def tri_saa_to_sss_deriv(a_expansion, B_expansion, A_expansion, order, return_components=False, sinBinvsinA_expansion=None, sinA_expansion=None, sinB_expansion=None, sinAinv_expansion=None, a2_expansion=None, b2_expansion=None, abcosC_expansion=None, ab_expansion=None, cosC_expansion=None, return_square=False):
    ...

def tri_asa_to_saa_deriv(C_expansion, a_expansion, B_expansion, order):
    ...

def tri_asa_to_sas_deriv(C_expansion, a_expansion, B_expansion, order, return_components=False, A_expansion=None, sinBinvsinA_expansion=None, sinA_expansion=None, sinB_expansion=None, sinAinv_expansion=None):
    ...

def tri_asa_to_ssa_deriv(C_expansion, a_expansion, B_expansion, order, return_components=False, A_expansion=None, sinBinvsinA_expansion=None, sinA_expansion=None, sinB_expansion=None, sinAinv_expansion=None):
    ...

def tri_asa_to_sss_deriv(C_expansion, a_expansion, B_expansion, order, return_components=False, A_expansion=None, sinBinvsinA_expansion=None, sinA_expansion=None, sinB_expansion=None, sinAinv_expansion=None, a2_expansion=None, b2_expansion=None, abcosC_expansion=None, ab_expansion=None, cosC_expansion=None, return_square=False):
    ...

class TriangleType(enum.Enum):
    SSS = 'sss'
    SAS = 'sas'
    SSA = 'ssa'
    SAA = 'saa'
    ASA = 'asa'

def _echo_tri_args(x, y, z):
    ...

def _echo_tri_deriv_args(x_expansion, y_expansion, z_expansion, order, return_components=False, **kwargs):
    ...

def triangle_converter(type1: str | TriangleType, type2: str | TriangleType):
    ...

def triangle_convert(tri_spec, type1: str | TriangleType, type2: str | TriangleType, order=None, **kwargs):
    ...

def triangle_area(tri_spec, type: str | TriangleType):
    ...
TriangleData = collections.namedtuple('TriangleData', ['a', 'b', 'c', 'A', 'B', 'C'])
_tdata_name_map = {'a': 0, 'b': 1, 'c': 2, 'A': 3, 'B': 4, 'C': 5}
_triangle_point_map = {'a': (0, 1), 'b': (1, 2), 'c': (0, 2), 'A': (0, 2, 1), 'B': (1, 0, 2), 'C': (0, 1, 2)}

def triangle_property_specifiers(base_specifier=None):
    ...

def make_triangle(points=None, *, a=None, b=None, c=None, A=None, B=None, C=None):
    ...

def _symbolic_triangle_field(val, field_name, triangle, inds, use_pos):
    ...

def make_symbolic_triangle(triangle=None, indices=None, positions=False, a=None, b=None, c=None, A=None, B=None, C=None):
    ...

def _check_triangle_type(tdata, inds):
    ...

def _check_bond_valid_triangle(td_1):
    ...

def _check_angle_valid_triangle(td_1):
    ...

def _get_triangle_completions(tri: TriangleData):
    ...

def triangle_is_complete(tri: TriangleData):
    ...

def _permutation_trie(comb_lists, cache=None):
    ...

def _expand_trie(t):
    ...

def _expand_trie_iter(t, sorting=None):
    ...

def _completion_paths(dd, completions_trie, prop_func, return_trie=False):
    ...

def _trie_delete(trie: dict, key):
    ...

def _trie_add(trie: dict, key):
    ...

def _trie_replace(trie: dict, key1, key2):
    ...

def _trie_short_circuit(trie: dict, key):
    ...

def _trie_join(trie1, trie2):
    ...

def _trie_merge(trie1, trie2):
    ...

def _trie_del_add(trie1, key, key2):
    ...

def _dist_completions_trie(b, c, A, B, C):
    ...

def _angle_completions_trie(a, b, c, B, C, angle_only=True):
    ...

def _triangle_completable_trie(a, b, c, A, B, C, require_all=True):
    ...

def enumerate_triangle_completions(tdata: TriangleData):
    ...

def _triangle_data_permute(tdata: TriangleData, perm):
    ...

def _triangle_property_c(tdata: TriangleData):
    ...

def _triangle_property_a(tdata):
    ...

def _triangle_property_b(tdata):
    ...

def _triangle_property_C(tdata: TriangleData):
    ...

def _triangle_property_A(tdata):
    ...

def _triangle_property_B(tdata):
    ...

def triangle_modify(tdata: TriangleData, updates: dict):
    ...

def _tri_prop(tdata: TriangleData, field_name):
    ...

def _triangle_has_prop(tdata: TriangleData, field_name):
    ...

def triangle_property(tdata: TriangleData, field_name, allow_completion=True):
    ...

def _triangle_property_c_from_sas(a, C, b):
    ...

def _triangle_property_c_from_saa(a, B, A):
    ...

def _triangle_property_c_from_asa(C, a, B):
    ...

def _triangle_property_C_from_sss(a, b, c):
    ...

def _triangle_property_C_from_sas(a, B, c):
    ...

def _triangle_property_C_from_saa(a, B, A):
    ...

def _triangle_property_C_from_asa(A, c, B):
    ...

def triangle_completions_c(a, b, A, B, C, cache=None):
    ...

def triangle_completions_C(a, b, c, A, B, cache=None):
    ...

class TriangleCoordinateType(enum.Enum):
    Distance = 'distance'
    Angle = 'angle'

def triangle_completions_trie(tdata: TriangleData, field_name, return_args=False, cache=None):
    ...

def triangle_completions(field_name, return_trie=False, return_args=False, **triangle_values):
    ...

def triangle_completion_paths(tdata: TriangleData, field_name, return_trie=False, indices=None, positions=False, return_args=False):
    ...

def triangle_property_function(sample_tri: TriangleData, field_name, raise_on_missing=True):
    ...

def dihedral_z_from_abcXYt(a, b, c, X, Y, tau, use_cos=False):
    """
    a^2 + b^2 + c^2 - 2 (
        a b Cos[\\[Alpha]] + b c Cos[\\[Beta]]
        + a c (Cos[\\[Tau]] Sin[\\[Alpha]] Sin[\\[Beta]] - Cos[\\[Alpha]] Cos[\\[Beta]])
       )
    """
    ...

def dihedral_z_from_abcXYt_deriv(a_expansion, b_expansion, c_expansion, X_expansion, Y_expansion, tau_expansion, order, return_components=False, return_square=False, cos_X_expansion=None, cos_Y_expansion=None, sin_X_expansion=None, sin_Y_expansion=None, cos_tau_expansion=None, a2_expansion=None, b2_expansion=None, c2_expansion=None, ab_cos_X_expansion=None, ab_expansion=None, bc_cos_Y_expansion=None, bc_expansion=None, ac_expansion=None, cos_X_cos_Y_expansion=None, sin_X_sin_Y_expansion=None):
    ...

def dihedral_z_from_abcxYt(a, b, c, x, Y, tau, use_cos=False):
    ...

def _dist_cos_expansion(a2_expansion, b2_expansion, x2_expansion, ab_expansion, order):
    ...

def dihedral_z_from_abcxYt_deriv(a_expansion, b_expansion, c_expansion, x_expansion, Y_expansion, tau_expansion, order, return_components=False, return_square=False, cos_X_expansion=None, cos_Y_expansion=None, sin_X_expansion=None, sin_Y_expansion=None, cos_tau_expansion=None, a2_expansion=None, b2_expansion=None, c2_expansion=None, x2_expansion=None, ab_expansion=None, bc_cos_Y_expansion=None, bc_expansion=None, ac_expansion=None, cos_X_cos_Y_expansion=None, sin_X_sin_Y_expansion=None):
    ...

def dihedral_z_from_abcxyt(a, b, c, x, y, tau, use_cos=False):
    ...

def dihedral_z_from_abcxyt_deriv(a_expansion, b_expansion, c_expansion, x_expansion, y_expansion, tau_expansion, order, return_components=False, return_square=False, a2_expansion=None, b2_expansion=None, c2_expansion=None, x2_expansion=None, y2_expansion=None, cos_tau_expansion=None, abplus_expansion=None, abminus_expansion=None, bcplus_expansion=None, bcminus_expansion=None, det_expansion=None):
    ...

def dihedral_from_abcXYz(a, b, c, X, Y, r, use_cos=False):
    ...

def dihedral_from_abcXYz_deriv(a_expansion, b_expansion, c_expansion, X_expansion, Y_expansion, r_expansion, order, return_components=False, return_cos=False, cos_X_expansion=None, cos_Y_expansion=None, sin_X_expansion=None, sin_Y_expansion=None, a2_expansion=None, b2_expansion=None, c2_expansion=None, r2_expansion=None, ab_cos_X_expansion=None, ab_expansion=None, bc_cos_Y_expansion=None, bc_expansion=None, ac_expansion=None, cos_X_cos_Y_expansion=None, sin_X_sin_Y_expansion=None):
    ...

def dihedral_from_abcxYz(a, b, c, x, Y, r, use_cos=False):
    ...

def dihedral_from_abcxYz_deriv(a_expansion, b_expansion, c_expansion, x_expansion, Y_expansion, r_expansion, order, return_components=False, return_cos=False, cos_X_expansion=None, cos_Y_expansion=None, sin_X_expansion=None, sin_Y_expansion=None, a2_expansion=None, b2_expansion=None, c2_expansion=None, x2_expansion=None, r2_expansion=None, ab_expansion=None, bc_cos_Y_expansion=None, bc_expansion=None, ac_expansion=None, cos_X_cos_Y_expansion=None, sin_X_sin_Y_expansion=None):
    ...

def dihedral_from_abcxyz(a, b, c, x, y, r, use_cos=False):
    ...

def dihedral_from_abcxyz_deriv(a_expansion, b_expansion, c_expansion, x_expansion, y_expansion, r_expansion, order, return_components=False, return_cos=False, a2_expansion=None, b2_expansion=None, c2_expansion=None, x2_expansion=None, y2_expansion=None, r2_expansion=None, abplus_expansion=None, abminus_expansion=None, bcplus_expansion=None, bcminus_expansion=None, det_expansion=None):
    ...

def dihedral_from_XZC(X, Z, C, use_cos=False):
    """
    cos of dihedral with three angles defining a pyramid,
    X = theta_(i,j,k)
    Z = theta_(i,j,l)
    C = theta_(k,j,l)
    """
    ...

def dihedral_Z_from_XtC(X, t, C, use_cos=False):
    ...

def dihedral_Ta_from_abcXYt(a, b, c, X, Y, t):
    """ArcTan[b Sin[X]-c (Cos[Y] Sin[X]+Cos[Tb] Cos[X] Sin[Y]),-c Sin[Tb] Sin[Y]]"""
    ...

def dihedral_z_from_ayXCt(a, y, X, C, t, use_cos=False, return_square=False):
    ...

def dihedral_z_from_bAXYCt(b, A, X, Y, C, t, use_cos=False, return_square=False):
    ...

def dihedral_from_ayXCz(a, y, X, C, z, use_cos=False):
    ...

def dihedral_from_bAXYCz(b, A, X, Y, C, z, use_cos=False):
    ...

def composed_dihedral(d_ijka, d_ijkb):
    ...

class DihedralSpecifierType(enum.Enum):
    SSSAAT = 'sssaat'
    SSSSAT = 'ssssat'
    SSSSST = 'ssssst'

def dihedral_distance_converter(dihedral_type: str | DihedralSpecifierType):
    ...

def dihedral_distance(spec, dihedral_type: str | DihedralSpecifierType, order=None, use_cos=False, **deriv_kwargs) -> float | np.ndarray:
    ...

def dihedral_from_distance_converter(dihedral_type: str | DihedralSpecifierType):
    ...

def dihedral_from_distance(spec, dihedral_type: str | DihedralSpecifierType, order=None, use_cos=False, **deriv_kwargs) -> float | np.ndarray:
    ...
"_dihedron_point_map data omitted from this build (30 keys: ['a', 'b', 'c', 'x', 'y', 'z', 'X', 'Y', 'A', 'B1', 'C', 'B2', 'Z', 'Z2', 'A3', 'Y3', 'C4', 'X4', 'Tb', 'Tb_inv', 'Ta', 'Ta_inv', 'Tc', 'Tc_inv', 'Tx', 'Tx_inv', 'Ty', 'Ty_inv', 'Tz', 'Tz_inv'])"
_dp_cache = {}

def dihedron_property_specifiers(base_specifier=None, use_cache=True):
    ...

def _check_dihedron_type(ddata, inds):
    ...

def make_dihedron(points=None, *, a=None, b=None, c=None, x=None, y=None, z=None, X=None, Y=None, A=None, B1=None, B2=None, C=None, Z=None, Z2=None, A3=None, Y3=None, C4=None, X4=None, Ta=None, Tb=None, Tc=None, Tx=None, Ty=None, Tz=None):
    ...

def _symbolic_dihedron_field(val, field_name, inds, use_pos):
    ...

def make_symbolic_dihedron(indices=None, positions=False, a=None, b=None, c=None, x=None, y=None, z=None, X=None, Y=None, A=None, B1=None, B2=None, C=None, Z=None, Z2=None, A3=None, Y3=None, C4=None, X4=None, Ta=None, Tb=None, Tc=None, Tx=None, Ty=None, Tz=None):
    ...

def dihedron_triangle_1(dd: DihedralTetrahedronData):
    ...

def dihedron_triangle_2(dd: DihedralTetrahedronData):
    ...

def dihedron_triangle_3(dd: DihedralTetrahedronData):
    ...

def dihedron_triangle_4(dd: DihedralTetrahedronData):
    ...

def dihedron_triangle(dd: DihedralTetrahedronData, i):
    ...

def _dihedron_permutation_relabeling(perm):
    ...

def _dihedron_data_permute(dd, perm):
    ...

def dihedron_modify(dd, updates):
    ...

def _dihedron_property_z(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_a(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_x(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_b(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_c(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_y(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_data(Tb, X, C, td_1, names_1, field_1, td_2, names_2, field_2):
    ...

def _dihedron_complete_dihedral_angle_data_imp(dd, T, f, x, A, y, B):
    ...

def _dihedron_complete_dihedral_angle_Ta_C(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_Ta_C4(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_Tb_Z(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_Tb_Z2(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_Tc_A(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_Tc_A3(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_Tx_Y(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_Tx_Y3(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_Ty_X(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_Ty_X4(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_Tz_B1(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_angle_Tz_B2(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_Z(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_A(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_X(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_B1(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_C(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_Y(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_B2(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_Z2(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_A3(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_Y3(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_C4(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_X4(dd: DihedralTetrahedronData):
    ...

def _dihedron_complete_dihedral_from_angle_data(Z, X, C, td_1, names_1, field_1, td_2, names_2, field_2):
    ...

def _get_dihedron_triangle_completions(tri, complements, fields, comps, properties):
    ...

def _complete_dihedron_triangle_1(dd):
    ...

def _complete_dihedron_triangle_2(dd):
    ...

def _complete_dihedron_triangle_3(dd):
    ...

def _complete_dihedron_triangle_4(dd):
    ...

def _dihedron_property_Tb(dd):
    ...

def _dihedron_property_Ta(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_Tc(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_Tx(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_Ty(dd: DihedralTetrahedronData):
    ...

def _dihedron_property_Tz(dd: DihedralTetrahedronData):
    ...

def _dihed_prop(ddata: DihedralTetrahedronData, field):
    ...

def dihedron_property(ddata: DihedralTetrahedronData, field_name, allow_completion=True):
    ...

def dihedral_Tb_completions_trie(b, a, x, y, c, A, X, Y, C, z, Z, Z2, A3, Y3, Ta, Tx, C4, X4, Tc, Ty, cache=None):
    """
        elif field_name == dd.Tb:
        args = [dd.b, dd.a, dd.x, dd.y, dd.c, dd.A, dd.X, dd.Y, dd.C, dd.z, dd.Z, dd.Z2]
        completion_type = DihedronCoordinateType.Dihedral
    elif field_name == dd.Ta:
        args = [dd.a, dd.b, dd.x, dd.y, dd.z, dd.B1, dd.X, dd.Y3, dd.Z, dd.c, dd.C, dd.C4]
        completion_type = DihedronCoordinateType.Dihedral
    """
    ...

def dihedral_b_completions_trie(a, x, A, X, B1, y, c, Y, C, B2, z, Y3, C4, A3, X4, Tz, cache=None):
    ...

def dihedral_Z_completions_trie(X, C, Tb, z, a, y, A3, Y3, cache=None):
    ...

class DihedronCoordinateType(enum.Enum):
    Distance = 'distance'
    Angle = 'angle'
    Dihedral = 'dihedral'

def dihedral_completions_trie(dd, field_name, return_args=True, cache=None):
    ...

def dihedral_completions(field_name, return_trie=False, return_args=False, cache=None, **dihedron_values):
    ...

def dihedral_completion_paths(dd: DihedralTetrahedronData, field_name, return_trie=False, indices=None, positions=False, return_args=False, cache=None):
    ...

def dihedron_is_complete(dd: DihedralTetrahedronData):
    ...

def enumerate_dihedron_completions(dd, priortize_dihedrals=True):
    ...

def sorted_dihedron_completions(sample_dihed: DihedralTetrahedronData, field_name: str, *, conversion_specs=None, trie_expansions=None, cache=None):
    ...

def dihedron_property_function(sample_dihed: DihedralTetrahedronData, field_name, disallowed_conversions=None, allow_completion=True, raise_on_missing=True, return_depth=False, completion_handler=None, allow_ambiguous_completions=False, depth=0, verbose=False, cache=None):
    ...

def dihedron_pair_dihedral_angle_function(inds1, dihed1, inds2, dihed2, raise_on_missing=True, cache=None, allow_completion=False):
    ...

def _rot_gen2(axis, moments_of_inertia=None):
    ...

def _rot_gen2_deriv(axis, order):
    ...

def axis_rot_gen_deriv(angle, axis, angle_order, axis_order=0, moments_of_inertia=None, normalized=False):
    ...

def angle_arc_parameters(u, v, normal=None, up_vector=(0, 0, 1)):
    ...

def arc_points(center, radius, offset_angle, span_angle, normal=None, angular_density=None, npoints=None, minor_radius=None):
    ...

def arc_center_from_endpoints(start, end, rotation=None, normal=None, radius=None, check_radius=True, use_major_rotation=None, clockwise=None, return_angles=False):
    ...

def arc_angles_from_endpoints(centers, starts, ends, rotation=None, uv_axes=None, use_major_rotation=None, clockwise=None):
    ...

def arc_points_from_endpoints(start, end, rotation=None, normal=None, radius=None, check_radius=True, use_major_rotation=None, clockwise=None, return_arc=False, npoints=None, angular_density=None):
    ...
_binoms = [None]

def _get_binom(n):
    ...

def bezier_coeffs(n, t):
    ...

def refine_curve(point_generator, t, *, max_arc_len, vals=None, max_subdivisions=3, sort_subdivisions=True):
    ...

def parametric_curve_evaluate(evaluators_1d, t, return_points=False, max_arc_len=None, max_subdivisions=3, sort_subdivisions=True):
    ...

def parametric_curvature(first_derivs_1d, second_derivs_1d, t, zero_thresh=1e-08):
    ...

def _bezier_evaluators(control_points, order=None):
    ...

def bezier_eval(control_points, t, max_arc_len=None, max_subdivisions=3, return_points=None, sort_subdivisions=True, order=None):
    ...

def bezier_solve(control_points):
    ...

def bezier_curvature(control_points, t, **opts):
    ...

def parameteric_spline_interpolate(knots, spacings='cumulative', **spline_kwargs):
    ...

def parameteric_interpolation_curvature(interpolations, t, **opts):
    ...

def polygon_normal(vertices, normalize=True):
    ...

def winding_sign(u, v, axis1=0, axis2=1, return_component=False, zero_threshold=1e-08):
    ...

def winding_number(points, polygon, axis1=0, axis2=1, zero_threshold=None):
    ...

def point_in_triangle(p, a, b, c, diffs=None, windings=None, **winding_args):
    ...

def is_polygon_ear(plane_points, indices, i, j, k, diffs=None, windings=None):
    ...

def ear_clipping_triangulation(plane_points, indices, diffs=None, windings=None):
    ...

def triangulate_polygon(vertices):
    ...

class PathElement(metaclass=abc.ABCMeta):

    def __init__(self, relative=False):
        ...
    element_registry = {}
    element_aliases = {}

    @classmethod
    def resolve(cls, element: str | type[PathElement], *args, **opts):
        ...

    @classmethod
    def register(cls, name, element=None, *, aliases=None):
        ...

    @abc.abstractmethod
    def to_points(self, *, reference=None, start=None, samples=None, **ignored) -> tuple[np.ndarray, dict]:
        ...

@PathElement.register('LINE', aliases='L')
class LineElement(PathElement):

    def __init__(self, *points, accumulate=True, **kwargs):
        ...

    def to_points(self, *, base_points=None, reference=None, start=None, samples=None, **ignored):
        ...

@PathElement.register('OFFSET')
class OffsetLineElement(LineElement):

    def __init__(self, offsets, directions, **kwargs):
        ...

    @classmethod
    def prep_directions(cls, dirs, ref=None):
        ...

    def to_points(self, *, reference=None, start=None, samples=None):
        ...

@PathElement.register('HORIZONTAL', aliases='H')
class HorizontalLine(OffsetLineElement):

    def __init__(self, *ys, **kwargs):
        ...

@PathElement.register('VERTICAL', aliases='V')
class VerticalLine(OffsetLineElement):

    def __init__(self, *ys, **kwargs):
        ...

@PathElement.register('DEPTH')
class DepthLine(OffsetLineElement):

    def __init__(self, *ys, **kwargs):
        ...

@PathElement.register('BEZIER')
class BezierCurve(PathElement):
    allow_smoothing = False

    def __init__(self, *points, **kwargs):
        ...

    def get_knots(self, reference, *, last_control=None):
        ...
    default_samples = 32

    def to_points(self, *, reference=None, start=None, samples=None, max_arc_len=None, **opts):
        ...

@PathElement.register('QUADRATIC', aliases='Q')
class QuadraticBezierCurve(BezierCurve):
    ...

@PathElement.register('SMOOTH_QUADRATIC', aliases='T')
class SmoothQuadraticBezierCurve(QuadraticBezierCurve):
    allow_smoothing = True

@PathElement.register('CUBIC', aliases='C')
class CubicBezierCurve(BezierCurve):
    ...

@PathElement.register('SMOOTH_CUBIC', aliases='S')
class SmoothCubicBezierCurve(CubicBezierCurve):
    allow_smoothing = True

@PathElement.register('ARC', aliases='A')
class EndpointArcElement(PathElement):

    def __init__(self, endpoint, radii, rotation=None, normal=None, offset_angle=None, use_major_rotation=None, clockwise=None, check_radius=True, angular_density=None, **kwargs):
        ...

    def to_points(self, *, reference=None, start=None, samples=None, **ignored):
        ...

@PathElement.register('INTERP')
class InterpElement(PathElement):

    def __init__(self, *points, spacings='cumulative', k=3, **kwargs):
        ...

    def _make_spline(self, reference):
        ...
    default_samples = 32

    def to_points(self, *, reference=None, start=None, max_arc_len=None, samples=None, **ignored):
        ...

@PathElement.register('MOVE', aliases='M')
class MoveReferenceElement(PathElement):

    def __init__(self, *target, **kwargs):
        ...

    def to_points(self, *, reference=None, start=None, samples=None, **ignored):
        ...

@PathElement.register('CLOSE', aliases='Z')
class ClosePathElement(PathElement):

    def to_points(self, *, reference=None, start=None, samples=None, **ignored):
        ...

def parametric_path_points(path_elements, return_segments=False):
    ...

def tri_tri_intersect(t1: np.ndarray, t2: np.ndarray, eps: float=1e-09) -> bool:
    """
    Test whether two triangles in 3D intersect.
    t1, t2 : (3, 3) arrays of vertex positions.
    Returns True if they share any point (including edge/vertex touches).
    """
    ...

def _project_2d(tri, normal):
    """Drop the axis most aligned with the normal → 2D projection."""
    ...

def _segments_intersect_2d(p1, p2, p3, p4, eps=1e-09) -> bool:
    """Do line segments p1–p2 and p3–p4 intersect?"""
    ...

def _point_in_tri_2d(p, tri2d, eps=1e-09) -> bool:
    """Is point p inside triangle tri2d (2D)?"""
    ...

def _coplanar_tri_tri(t1, t2, normal, eps=1e-09) -> bool:
    ...

def triangle_plane_embedding(tris, zero_threshold=None):
    ...

def check_triangle_plane_offsets(t1, t2, embeddings=None, zero_threshold=None, return_distances=False):
    ...

def check_coplanar_triangle_intersection(t1, t2, embeddings=None, zero_threshold=None, return_crosses=False):
    ...

def get_bounding_boxes(polys, concatentate=False):
    ...

def check_interval_overlaps(bounds_1, bounds_2, include_endpoints=True, zero_threshold=None):
    ...

def check_bbox_intersections(polys1, polys2, zero_threshold=None):
    ...

def check_line_intersection(line_1, line_2, zero_threshold=None):
    ...

def check_segment_intersection(p1, p2, p3, p4, zero_threshold=None):
    ...

def check_segment_intersection_2d(p1, p2, p3, p4, axis1=0, axis2=1, zero_threshold=None):
    ...

def _tri_overlap_intervals(p, sd, zero_threshold=None):
    """Scalar intervals [lo, hi] for the triangle intersection points along the normal axis"""
    ...

def check_triangle_intersection(tris1, tris2, embeddings=None, check_indices=None, check_direct_product=False, zero_threshold=None):
    ...

def fibonacci_sphere(samples):
    ...

def uv_mapping(uv):
    """
    Map points on [0,1]^2 onto the unit sphere S^2 via the cylindrical
    equal-area (Lambert / "hat-box") projection:

        z   = 2v - 1
        phi = 2*pi*u
        x,y = sqrt(1-z^2)*cos(phi), sqrt(1-z^2)*sin(phi)

    By Archimedes' hat-box theorem, orthogonal projection of the sphere
    onto its circumscribing cylinder is area-preserving, so this map is
    the inverse of that projection: it sends the *uniform* measure on the
    square to the *uniform* (surface-area) measure on the sphere. That
    means a low-discrepancy sequence on the square pushes forward to a
    low-discrepancy-ish sample on the sphere -- no low-discrepancy
    structure is invented in 3D, but no uniformity is lost in translation
    either, since z is uniform in [-1,1] and phi uniform in [0,2*pi)
    are exactly the two conditions that characterize the uniform
    distribution on S^2.

    Parameters
    ----------
    uv : (N,2) array, both columns in [0,1)

    Returns
    -------
    (N,3) array of points on the unit sphere
    """
    ...