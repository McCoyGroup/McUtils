"""
The Coordinerds package implements stuff for dealing with coordinates and generalized coordinate systems

It provides a semi-symbolic way to represent a CoordinateSystem and a CoordinateSet that provides coordinates within a
coordinate system. An extensible system for converting between coordinate systems and is provided.

The basic design of the package is set up so that one creates a `CoordinateSet` object, which in turn tracks its `CoordinateSystem`.
A `CoordinateSet` is a subclass of `np.ndarray`, and so any operation that works for a `np.ndarray` will work in turn for `CoordinateSet`.
This provides a large amount flexibility.

The `CoordinateSystem` object handles much of the heavy lifting for a `CoordinateSet`.
Conversions between different systems are implemented by a `CoordinateSystemConverter`.
Chained conversions are not _currently_ supported, but might well become supported in the future.
"""
__all__ = ['CoordinateSystemConverters', 'CoordinateSystemConverter', 'SimpleCoordinateSystemConverter', 'CartesianCoordinateSystem', 'InternalCoordinateSystem', 'CartesianCoordinateSystem3D', 'CartesianCoordinates3D', 'CartesianCoordinates1D', 'CartesianCoordinates2D', 'SphericalCoordinateSystem', 'SphericalCoordinates', 'ZMatrixCoordinateSystem', 'ZMatrixCoordinates', 'CoordinateSystem', 'BaseCoordinateSystem', 'CoordinateSystemError', 'CompositeCoordinateSystem', 'CompositeCoordinateSystemConverter', 'GenericInternalCoordinateSystem', 'GenericInternalCoordinates', 'CartesianToGICSystemConverter', 'GICSystemToCartesianConverter', 'IterativeZMatrixCoordinateSystem', 'IterativeZMatrixCoordinates', 'CartesianToIZSystemConverter', 'IZSystemToCartesianConverter', 'CoordinateSet', 'cartesian_to_zmatrix', 'zmatrix_to_cartesian', 'canonicalize_internal', 'get_canonical_internal_list', 'is_coordinate_list_like', 'is_valid_coordinate', 'permute_internals', 'find_internal', 'coordinate_sign', 'coordinate_indices', 'get_internal_distance_conversion', 'internal_distance_convert', 'get_internal_triangles_and_dihedrons', 'find_internal_conversion', 'get_internal_cartesian_conversion', 'validate_internals', 'InternalCoordinateType', 'InternalSpec', 'InternalCoordinateGraph', 'zmatrix_unit_convert', 'zmatrix_indices', 'num_zmatrix_coords', 'zmatrix_embedding_coords', 'set_zmatrix_embedding', 'enumerate_zmatrices', 'extract_zmatrix_internals', 'extract_zmatrix_values', 'zmatrix_from_values', 'parse_zmatrix_string', 'format_zmatrix_string', 'validate_zmatrix', 'chain_zmatrix', 'center_bound_zmatrix', 'spoke_zmatrix', 'attached_zmatrix_fragment', 'functionalized_zmatrix', 'add_missing_zmatrix_bonds', 'bond_graph_zmatrix', 'canonical_fragment_zmatrix', 'reindex_zmatrix', 'sort_complex_attachment_points', 'complex_zmatrix', 'graph_backbone_zmatrix', 'segmented_complex_backbone_zmatrix', 'enforce_required_zmatrix_coordinates', 'coordinate_label', 'get_coordinate_label', 'mode_label', 'get_mode_labels', 'coordinate_sorting_key', 'sort_internal_coordinates', 'get_stretch_angles', 'get_angle_dihedrals', 'get_angle_stretches', 'get_dihedral_stretches', 'get_stretch_angle_dihedrals', 'get_stretch_coordinate_system', 'get_fragment_coordinate_system', 'PrimitiveCoordinatePicker', 'enumerate_coordinate_sets', 'prune_internal_coordinates', 'RedundantCoordinateGenerator', 'convert_cartesian_to_zmatrix', 'convert_zmatrix_to_cartesians']
from .CoordinateSystems import *
from .Conveniences import *
from .Internals import *
from .ZMatrices import *
from .Labels import *
from .Generators import *
from .Pruning import *
from .Redundant import *
from .Conversions import *