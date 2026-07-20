import collections
import numpy as np
import scipy.sparse as spg
import itertools
from .. import Numputils as nput
from .. import Iterators as itut
from ..Graphs import EdgeGraph
from .Internals import canonicalize_internal
__all__ = ['zmatrix_unit_convert', 'zmatrix_indices', 'num_zmatrix_coords', 'zmatrix_embedding_coords', 'set_zmatrix_embedding', 'enumerate_zmatrices', 'extract_zmatrix_internals', 'extract_zmatrix_values', 'zmatrix_from_values', 'parse_zmatrix_string', 'format_zmatrix_string', 'validate_zmatrix', 'chain_zmatrix', 'center_bound_zmatrix', 'spoke_zmatrix', 'attached_zmatrix_fragment', 'functionalized_zmatrix', 'add_missing_zmatrix_bonds', 'bond_graph_zmatrix', 'canonical_fragment_zmatrix', 'reindex_zmatrix', 'sort_complex_attachment_points', 'complex_zmatrix', 'graph_backbone_zmatrix', 'segmented_complex_backbone_zmatrix', 'enforce_required_zmatrix_coordinates']

def zmatrix_unit_convert(zmat, distance_conversion, angle_conversion=None, rad2deg=False, deg2rad=False):
    """
    **LLM Docstring**

    Scale the distance and angular columns of a Z-matrix value array.

    A copy is made when `np.asanyarray` returns the original object. Column 0 is multiplied by `distance_conversion`. Columns 1 and 2 are multiplied by `angle_conversion` when supplied; otherwise they are optionally converted between degrees and radians.

    :param zmat: Z-matrix values whose final two axes are atoms by `(distance, angle, dihedral)`.
    :type zmat: array-like
    :param distance_conversion: Multiplicative factor applied to all distances.
    :type distance_conversion: float
    :param angle_conversion: Multiplicative factor applied to bends and dihedrals. When omitted, `rad2deg` or `deg2rad` controls angular conversion.
    :type angle_conversion: float | None
    :param rad2deg: Convert angular columns from radians to degrees when `angle_conversion` is omitted.
    :type rad2deg: bool
    :param deg2rad: Convert angular columns from degrees to radians when `angle_conversion` is omitted.
    :type deg2rad: bool
    :return: Converted Z-matrix values, without modifying the input array in place.
    :rtype: np.ndarray
    """
    ...

def zmatrix_indices(zmat, coords, strip_embedding=True):
    """
    **LLM Docstring**

    Locate internal coordinates within the ordered coordinate list represented by a Z-matrix.

    The Z-matrix is expanded into its bond, angle, and dihedral tuples, optionally excluding embedding coordinates. Both the extracted coordinates and requested coordinates are canonicalized before list lookup. A single coordinate returns one integer; a sequence returns a list.

    :param zmat: Four-column or reference-only Z-matrix ordering.
    :type zmat: Sequence[Sequence[int]]
    :param coords: One internal-coordinate tuple or a sequence of tuples.
    :type coords: Sequence[int] | Sequence[Sequence[int]]
    :param strip_embedding: Exclude the translational and rotational embedding entries from the searchable coordinate list.
    :type strip_embedding: bool
    :return: Position or positions of the requested coordinates.
    :rtype: int | list[int]
    """
    ...
emb_pos_map = [(0, 1), (0, 2), (0, 3), None, (1, 2), (1, 3), None, None, (2, 3)]
emb_partial_pos_map = [None, (0, 2), (0, 3), None, None, (1, 3)]

def zmatrix_embedding_coords(zmat_or_num_atoms, partial_embedding=False, array_inds=False):
    """
    **LLM Docstring**

    Return the flattened entries occupied by Z-matrix embedding coordinates.

    For a molecule with zero, one, two, or at least three atoms, this selects the distance/angle/dihedral entries used to fix overall translation and rotation. With `partial_embedding`, only the three coordinates required by the partially embedded representation are selected. With `array_inds`, flattened positions are converted to `(row, column)` pairs and adjusted for three-column orderings.

    :param zmat_or_num_atoms: Atom count or a Z-matrix-like ordering from which the atom count and column convention are inferred.
    :type zmat_or_num_atoms: int | Sequence[Sequence[int]]
    :param partial_embedding: Select the reduced embedding used by `zmatrix_from_values(..., partial_embedding=True)`.
    :type partial_embedding: bool
    :param array_inds: Return two-dimensional array indices instead of flattened indices.
    :type array_inds: bool
    :return: Embedding positions in flattened or `(row, column)` form.
    :rtype: list[int] | list[tuple[int, int]]
    """
    ...

def num_zmatrix_coords(zmat_or_num_atoms, strip_embedding=True):
    """
    **LLM Docstring**

    Count scalar Z-matrix coordinates for a molecule or ordering.

    The full representation contains three values per atom. When `strip_embedding` is true, the entries identified by `zmatrix_embedding_coords` are subtracted, giving the number of internal degrees represented after removing global translation and rotation.

    :param zmat_or_num_atoms: Atom count or Z-matrix ordering.
    :type zmat_or_num_atoms: int | Sequence[Sequence[int]]
    :param strip_embedding: Remove embedding coordinates from the count.
    :type strip_embedding: bool
    :return: Number of scalar Z-matrix values.
    :rtype: int
    """
    ...

def _zmatrix_iterate(coords, natoms=None, include_origins=False, canonicalize=True, deduplicate=True, allow_completions=False):
    """
    **LLM Docstring**

    Yield complete Z-matrix orderings consistent with a set of internal coordinates.

    Coordinates are optionally canonicalized into the orientation expected by a Z-matrix and deduplicated. Optional origin rows for atoms 0–2 are inserted. Candidate dihedrals are grouped by the atom they introduce; only dihedrals whose bond and angle prefixes are available are retained unless completions are allowed. The function then takes the Cartesian product of the admissible embedding angle and one introducing dihedral for every atom from index 3 onward, yielding four-column rows with standard negative embedding references.

    :param coords: Bond, angle, and dihedral tuples available for constructing rows.
    :type coords: Sequence[Sequence[int]]
    :param natoms: Number of atoms. Inferred from unique coordinate indices when omitted.
    :type natoms: int | None
    :param include_origins: Insert the bond and angle coordinates needed for the first three atoms.
    :type include_origins: bool
    :param canonicalize: Canonicalize coordinate orientation before matching prefixes.
    :type canonicalize: bool
    :param deduplicate: Remove repeated coordinate tuples while preserving order.
    :type deduplicate: bool
    :param allow_completions: Permit dihedrals whose bond or angle prefix is not explicitly present.
    :type allow_completions: bool
    :return: An iterator of complete four-column Z-matrix orderings.
    :rtype: Iterator[tuple[tuple[int, int, int, int], ...]]
    """
    ...

def enumerate_zmatrices(coords, natoms=None, allow_permutation=True, include_origins=False, canonicalize=True, deduplicate=True, preorder_atoms=True, allow_completions=False):
    """
    **LLM Docstring**

    Enumerate Z-matrix orderings compatible with supplied internal coordinates.

    The coordinate set is canonicalized and deduplicated. When `preorder_atoms` is enabled, atoms are ranked by how often they occur in the coordinate set so highly connected atoms are tried first. The function then considers every allowed atom permutation, rewrites each coordinate into that permutation's index space, asks `_zmatrix_iterate` for every complete choice of introducing dihedrals, and maps each yielded row back to the original atom labels.

    :param coords: Available bond, angle, and dihedral coordinate tuples.
    :type coords: Sequence[Sequence[int]]
    :param natoms: Number of atoms; inferred from coordinate indices when omitted.
    :type natoms: int | None
    :param allow_permutation: Try all atom order permutations rather than only the preordered sequence.
    :type allow_permutation: bool
    :param include_origins: Add the coordinates needed to define the first three atoms.
    :type include_origins: bool
    :param canonicalize: Canonicalize coordinate directions before enumeration.
    :type canonicalize: bool
    :param deduplicate: Remove duplicate coordinate tuples.
    :type deduplicate: bool
    :param preorder_atoms: Start permutations from atoms sorted by coordinate participation count.
    :type preorder_atoms: bool
    :param allow_completions: Allow rows whose bond or angle prefixes were not explicitly supplied.
    :type allow_completions: bool
    :return: Z-matrix orderings in original atom-index space.
    :rtype: Iterator[list[list[int]]]
    """
    ...

def extract_zmatrix_internals(zmat, strip_embedding=True, canonicalize=True):
    """
    **LLM Docstring**

    Expand a Z-matrix ordering into its bond, angle, and dihedral coordinate tuples.

    Three-column orderings are first promoted to four columns by adding the implicit atom index and embedding row. For each row the function emits the bond prefix, then the angle prefix, then the dihedral prefix, skipping the undefined embedding entries for the first three atoms when requested. Returned tuples may be canonicalized to make reversed coordinates equivalent.

    :param zmat: Three- or four-column Z-matrix ordering.
    :type zmat: Sequence[Sequence[int]]
    :param strip_embedding: Omit coordinates that only establish the external frame.
    :type strip_embedding: bool
    :param canonicalize: Canonicalize each emitted coordinate tuple.
    :type canonicalize: bool
    :return: Ordered list of internal-coordinate tuples represented by the Z-matrix.
    :rtype: list[tuple[int, ...]]
    """
    ...

def extract_zmatrix_values(zmat, inds=None, partial_embedding=False, strip_embedding=True):
    """
    **LLM Docstring**

    Flatten Z-matrix values and select internal-coordinate entries.

    A four-column array is interpreted as containing atom indices in column 0, which are removed before flattening. When no explicit indices are supplied, all values are selected and embedding entries are deleted if requested. Explicit indices are interpreted in the stripped coordinate space when `strip_embedding` is true.

    :param zmat: Z-matrix value array with shape `(..., n_atoms, 3)` or a four-column combined array.
    :type zmat: array-like
    :param inds: Coordinate positions to extract, or all positions when omitted.
    :type inds: Sequence[int] | None
    :param partial_embedding: Use the reduced embedding mask when automatically selecting coordinates.
    :type partial_embedding: bool
    :param strip_embedding: Exclude embedding entries and interpret `inds` relative to the remaining coordinates.
    :type strip_embedding: bool
    :return: Selected values with the atom/value axes flattened into one final axis.
    :rtype: np.ndarray
    """
    ...

def zmatrix_from_values(flat_z, strip_embedding=True, partial_embedding=False):
    """
    **LLM Docstring**

    Reconstruct an atom-by-three Z-matrix value array from flattened values.

    Unstripped data is reshaped directly. For partial embedding, the first atom's distance and the second atom's distance/angle are restored before remaining triples are filled. For full embedding, the first three atoms receive the conventional zero-valued undefined entries, and the supplied values begin with atom 1's distance, atom 2's distance/angle, then complete triples.

    :param flat_z: Flattened Z-matrix values with optional leading batch dimensions.
    :type flat_z: array-like
    :param strip_embedding: Whether embedding entries are absent from `flat_z`.
    :type strip_embedding: bool
    :param partial_embedding: Interpret `flat_z` using the reduced three-coordinate embedding convention.
    :type partial_embedding: bool
    :return: Z-matrix values with shape `(..., n_atoms, 3)`.
    :rtype: np.ndarray
    """
    ...
scan_spec = collections.namedtuple('scan_spec', ['value', 'steps', 'amount'])

def _prep_var_spec(v):
    """
    **LLM Docstring**

    Parse one tokenized Z-matrix variable specification.

    A single token becomes a floating-point constant. A value followed by `F` becomes a frozen `scan_spec` with `steps=-1`. Three tokens become `scan_spec(value, steps, amount)`. Other lengths are rejected.

    :param v: Tokens following a variable name.
    :type v: Sequence[str]
    :return: Numeric value or parsed scan specification.
    :rtype: float | scan_spec
    """
    ...

def parse_zmatrix_string(zmat, units='Angstroms', in_radians=False, has_values=True, atoms_are_order=False, keep_variables=False, variables=None, dialect='gaussian'):
    """
    **LLM Docstring**

    Parse a Gaussian-style textual Z-matrix into atoms, ordering, and coordinate values.

    The atom/reference/value token stream is split into rows of increasing width for the first three atoms and seven fields thereafter. Positive one-based references are converted to zero-based indices. A `Variables:` block is parsed into constants or scan specifications. Unless variables are retained, symbols are replaced by numeric values, distances are converted from `units` to Bohr, and angles and dihedrals are converted to radians unless already supplied in radians.

    :param zmat: Gaussian-style Z-matrix text, optionally followed by a `Variables:` block.
    :type zmat: str
    :param units: Distance unit used by numeric values.
    :type units: str
    :param in_radians: Treat angular values as radians instead of degrees.
    :type in_radians: bool
    :param has_values: Whether coordinate values alternate with reference indices in each row.
    :type has_values: bool
    :param atoms_are_order: Interpret the atom column as an explicit one-based atom permutation rather than element symbols.
    :type atoms_are_order: bool
    :param keep_variables: Return unresolved coordinate tokens and the variable table instead of numeric arrays.
    :type keep_variables: bool
    :param variables: Additional or overriding variable definitions.
    :type variables: dict | None
    :param dialect: Input dialect; only `gaussian` is implemented.
    :type dialect: str
    :return: Numeric `(atoms, ordering, coords)`, or `((atoms, ordering, token_coords), variables)` when variables are retained.
    :rtype: tuple
    """
    ...

def format_zmatrix_string(atoms, zmat, ordering=None, units='Angstroms', in_radians=False, float_fmt='{:11.8f}', index_padding=1, variables=None, variable_modifications=None, distance_variable_format='r{i}', angle_variable_format='a{i}', dihedral_variable_format='d{i}'):
    """
    **LLM Docstring**

    Format atoms, references, and values as a Gaussian-style Z-matrix string.

    Combined alternating reference/value rows are separated when `ordering` is omitted. Distances are converted from Bohr to `units`; angles are converted from radians to degrees unless requested otherwise. Optional generated variable names replace numeric values, coordinate-specific modifications can append scan/freeze suffixes, indices receive `index_padding`, and all columns are width-aligned. A `Variables:` block is appended when variables are present.

    :param atoms: Atom labels in output order.
    :type atoms: Sequence[str]
    :param zmat: Z-matrix values or alternating reference/value rows.
    :type zmat: array-like | Sequence
    :param ordering: Reference-index rows, optionally including explicit atom indices.
    :type ordering: Sequence[Sequence[int]] | None
    :param units: Distance unit for formatted output.
    :type units: str
    :param in_radians: Keep angular values in radians instead of converting to degrees.
    :type in_radians: bool
    :param float_fmt: Format string used for numeric values.
    :type float_fmt: str
    :param index_padding: Offset added to nonnegative atom references, normally 1 for Gaussian indexing.
    :type index_padding: int
    :param variables: Existing variable mapping, `True` to generate one variable per defined coordinate, or `None` for inline values.
    :type variables: dict | bool | None
    :param variable_modifications: Mapping from coordinate tuples to suffix text appended to variable definitions.
    :type variable_modifications: dict | None
    :param distance_variable_format: Template for generated distance symbols.
    :type distance_variable_format: str
    :param angle_variable_format: Template for generated angle symbols.
    :type angle_variable_format: str
    :param dihedral_variable_format: Template for generated dihedral symbols.
    :type dihedral_variable_format: str
    :return: Aligned Z-matrix text with an optional variable block.
    :rtype: str
    """
    ...

def validate_zmatrix(ordering, allow_reordering=True, ensure_nonnegative=True, raise_exception=False, return_reason=False):
    """
    **LLM Docstring**

    Check that a Z-matrix ordering defines atoms before they are referenced and contains valid row references.

    Embedding entries are normalized first. With reordering allowed, explicit atom labels are mapped to row positions and validation is repeated. The check rejects undefined atom labels, negative atom labels when prohibited, forward references, references larger than the row atom, duplicate indices within a row, and missing nonnegative references beyond the embedding rows.

    :param ordering: Z-matrix ordering rows.
    :type ordering: Sequence[Sequence[int]]
    :param allow_reordering: Permit arbitrary explicit atom labels by remapping them to row order.
    :type allow_reordering: bool
    :param ensure_nonnegative: Require all real atom labels and required references to be nonnegative.
    :type ensure_nonnegative: bool
    :param raise_exception: Raise `ValueError` at the first failed check.
    :type raise_exception: bool
    :param return_reason: Return `(valid, reason)` rather than only a Boolean.
    :type return_reason: bool
    :return: Validation status, optionally paired with the failure explanation.
    :rtype: bool | tuple[bool, str | None]
    """
    ...

def chain_zmatrix(n):
    """
    **LLM Docstring**

    Construct a linear-chain Z-matrix ordering.

    Each atom references the immediately preceding atom for distance, the atom two positions back for angle, and the atom three positions back for dihedral. Negative references naturally provide embedding placeholders for the first rows. An explicit atom sequence is preserved in column 0 while references use earlier entries from that sequence.

    :param n: Number of atoms or explicit atom ordering.
    :type n: int | Sequence[int]
    :return: Four-column chain Z-matrix rows.
    :rtype: list[list[int]]
    """
    ...

def center_bound_zmatrix(n, center=-1):
    """
    **LLM Docstring**

    Construct rows whose bond reference is a common center.

    Each generated atom uses `center` as its distance reference. Angle and dihedral references are chosen from earlier generated atoms, with negative embedding placeholders in the first rows.

    :param n: Number of rows to generate.
    :type n: int
    :param center: Common bond-reference index, often a negative attachment placeholder.
    :type center: int
    :return: Four-column center-bound fragment ordering.
    :rtype: list[list[int]]
    """
    ...

def _get_clean_attachment_refs(attachment_points, zm, order, a):
    """
    **LLM Docstring**

    Find usable external references for attaching a fragment at atom `a`.

    The row for `a` is located in `zm`. Negative references are resolved against nearby entries of `order`; references that are themselves attachment points or already selected are skipped. The resulting list preserves the row's reference priority.

    :param attachment_points: Atom labels reserved as attachment placeholders.
    :type attachment_points: Sequence[int]
    :param zm: Existing Z-matrix rows.
    :type zm: Sequence[Sequence[int]]
    :param order: Atom labels in Z-matrix row order.
    :type order: Sequence[int]
    :param a: Attachment atom whose row supplies candidate references.
    :type a: int
    :return: Distinct non-attachment reference atoms.
    :rtype: list[int]
    """
    ...

def attached_zmatrix_fragment(n, zm, fragment, attachment_points):
    """
    **LLM Docstring**

    Translate a fragment Z-matrix from local indices and negative placeholders into a larger Z-matrix.

    Negative entries index backward through `attachment_points`; nonnegative fragment-local indices are shifted by `n`. Before substitution, negative attachment points are resolved to clean references from the existing Z-matrix when possible.

    :param n: Number of atoms already present; used as the local-index offset.
    :type n: int
    :param zm: Existing Z-matrix used to resolve attachment references.
    :type zm: Sequence[Sequence[int]]
    :param fragment: Fragment rows in local index space.
    :type fragment: Sequence[Sequence[int]]
    :param attachment_points: External atoms replacing `-1`, `-2`, and `-3` placeholders.
    :type attachment_points: Sequence[int]
    :return: Fragment rows expressed in the combined Z-matrix index space.
    :rtype: list[list[int]]
    """
    ...

def set_zmatrix_embedding(zmat, embedding=None, partial_embedding=False):
    """
    **LLM Docstring**

    Write standard embedding reference values into a Z-matrix ordering.

    The positions are obtained from `zmatrix_embedding_coords(..., array_inds=True)`. Full embedding writes six conventional negative references; partial embedding writes three.

    :param zmat: Z-matrix ordering to copy and modify.
    :type zmat: array-like
    :param embedding: Replacement values in embedding-position order, or standard defaults.
    :type embedding: Sequence[int] | None
    :param partial_embedding: Use the reduced three-entry embedding convention.
    :type partial_embedding: bool
    :return: Integer array with embedding references assigned.
    :rtype: np.ndarray
    """
    ...

def functionalized_zmatrix(base_zm, attachments: 'dict|list[list[int], list[int]]'=None, single_atoms: list[int]=None, methyl_positions: list[int]=None, ethyl_positions: list[int]=None, validate=False):
    """
    **LLM Docstring**

    Build a larger Z-matrix by attaching fragments and optional standard substituent patterns.

    `base_zm` and numeric fragment sizes are converted to chain Z-matrices. Each attachment replaces a fragment's negative placeholders with the supplied external references and shifts its local indices. Additional single atoms are attached using available neighboring references; methyl and ethyl positions append fixed three-atom and two-atom patterns. Optional validation is performed after every fragment addition.

    :param base_zm: Existing Z-matrix or atom count for a chain base.
    :type base_zm: int | Sequence[Sequence[int]]
    :param attachments: Mapping or iterable of `(attachment_points, fragment)` pairs.
    :type attachments: dict | Iterable | None
    :param single_atoms: Existing atom labels at which to append individual atoms.
    :type single_atoms: Sequence[int] | None
    :param methyl_positions: Existing atom labels at which to append the implemented three-row methyl pattern.
    :type methyl_positions: Sequence[int] | None
    :param ethyl_positions: Existing atom labels at which to append the implemented two-row ethyl pattern.
    :type ethyl_positions: Sequence[int] | None
    :param validate: Validate the ordering after each explicit fragment attachment.
    :type validate: bool
    :return: Combined four-column Z-matrix ordering.
    :rtype: list[list[int]]
    """
    ...

def spoke_zmatrix(m, spoke=1, root=1):
    """
    **LLM Docstring**

    Construct a root fragment with `m` copies of a spoke fragment attached to its terminal atom.

    Integer `root` and `spoke` arguments are expanded as chain Z-matrices. If the root has fewer than three atoms, enough spoke atoms are first incorporated to establish three usable references. Remaining spokes are attached through the root terminal and two selected neighboring references.

    :param m: Number of spoke copies to attach, reduced by any copies consumed to complete a short root.
    :type m: int
    :param spoke: Spoke fragment ordering or atom count for a chain spoke.
    :type spoke: int | Sequence[Sequence[int]]
    :param root: Root fragment ordering or atom count for a chain root.
    :type root: int | Sequence[Sequence[int]]
    :return: Combined spoke-style Z-matrix.
    :rtype: list[list[int]]
    """
    ...

def reindex_zmatrix(zm, perm):
    """
    **LLM Docstring**

    Replace every nonnegative atom index in a Z-matrix using `perm`.

    Negative embedding and attachment placeholders are preserved unchanged.

    :param zm: Z-matrix rows to remap.
    :type zm: Sequence[Sequence[int]]
    :param perm: Indexable mapping from old labels to new labels.
    :type perm: Mapping | Sequence[int]
    :return: Reindexed rows.
    :rtype: list[list[int]]
    """
    ...

def canonicalize_zmatrix(zm):
    """
    **LLM Docstring**

    Convert a Z-matrix to row-index space while preserving its explicit atom ordering.

    A three-column ordering is promoted to four columns with an implicit atom column. The original atom labels are returned as `z_vec`; all nonnegative entries are then replaced by their row positions.

    :param zm: Three- or four-column Z-matrix ordering.
    :type zm: Sequence[Sequence[int]]
    :return: Original atom-label vector and equivalent row-indexed Z-matrix.
    :rtype: tuple[np.ndarray, list[list[int]]]
    """
    ...

def _attachment_point(i_pos, graph=None, ind_mapping=None):
    """
    **LLM Docstring**

    Complete a three-reference attachment specification `(bond, angle, dihedral)`.

    Supplied positions are retained. Missing positions are chosen from graph neighbors while avoiding already selected references; when no suitable graph neighbor exists, nearby numeric indices are used as deterministic fallbacks. References selected through the graph are translated through `ind_mapping` when provided.

    :param i_pos: One to three known attachment references, or a single bond reference.
    :type i_pos: int | Sequence[int | None]
    :param graph: Optional graph whose adjacency map is used to choose chemically connected references.
    :type graph: EdgeGraph | None
    :param ind_mapping: Mapping applied only to references selected from `graph`.
    :type ind_mapping: Mapping | None
    :return: Complete `(bond_reference, angle_reference, dihedral_reference)` tuple.
    :rtype: tuple[int, int, int]
    """
    ...

def add_missing_zmatrix_bonds(base_zmat, bonds, max_iterations=None, validate_additions=True):
    """
    **LLM Docstring**

    Recursively add atoms connected by `bonds` but absent from a partial Z-matrix.

    The input is canonicalized to row-index space. For each bond crossing from an included atom to an excluded atom, all newly reachable atoms are appended as a center-bound fragment attached to the included atom. The combined ordering is mapped back to original atom labels and the procedure repeats until no crossing bonds remain or `max_iterations` is exhausted.

    :param base_zmat: Partial Z-matrix ordering.
    :type base_zmat: Sequence[Sequence[int]]
    :param bonds: Full bond list in original atom-label space.
    :type bonds: Sequence[tuple[int, int]]
    :param max_iterations: Maximum recursive expansion depth, or no limit.
    :type max_iterations: int | None
    :param validate_additions: Validate before canonicalization, after attachment, and after reindexing.
    :type validate_additions: bool
    :return: Expanded Z-matrix and a mapping from included attachment atoms to atoms discovered from them.
    :rtype: tuple[list[list[int]], dict[int, list[int]]]
    """
    ...

def make_zmatrix_tree(zm):
    """
    **LLM Docstring**

    Represent Z-matrix parent references as a bidirectional tree-like mapping.

    For row `n`, only the first `n` nonnegative reference columns are considered defined. Each atom records its ordered parent tuple, and every parent records the atom in an unordered `children` set.

    :param zm: Four-column Z-matrix ordering.
    :type zm: Sequence[Sequence[int]]
    :return: Mapping from atom label to `{'parents': tuple, 'children': set}`.
    :rtype: dict[int, dict]
    """
    ...

def zmatrix_adjacency_matrix(zm, child_type='multi', penalty_atoms=None):
    """
    **LLM Docstring**

    Build a directed parent-to-child adjacency matrix from a Z-matrix tree.

    Atoms are ordered by parent count, except `penalty_atoms`, which are sorted as though they had six parents. In `single` mode only the first, bond-defining parent creates an edge; in `multi` mode every parent-child relationship does.

    :param zm: Z-matrix rows or a mapping produced by `make_zmatrix_tree`.
    :type zm: Sequence | dict
    :param child_type: `single` for bond-parent edges only, otherwise all parent edges.
    :type child_type: str
    :param penalty_atoms: Atoms forced toward the end of the matrix ordering.
    :type penalty_atoms: Collection[int] | None
    :return: Atom labels in matrix order and their Boolean adjacency matrix.
    :rtype: tuple[list[int], np.ndarray]
    """
    ...

def zmatrix_from_tree(zm, check_cycles=True, chain_order=None, check_unique_root=True, base_order=None):
    """
    **LLM Docstring**

    Convert a parent/children mapping back into ordered four-column Z-matrix rows.

    The optional checks require one root, then rows with one and two parents, and reject strongly connected components that indicate parent cycles. Without an explicit order, depth-first traversals of the bond-parent graph score atoms so the root and first two embedding atoms appear first. With `base_order`, atoms are appended only after all their parents have appeared. Missing parent columns are filled with standard negative placeholders.

    :param zm: Mapping from atom labels to ordered parents and children.
    :type zm: dict
    :param check_cycles: Reject cycles in the full parent graph.
    :type check_cycles: bool
    :param chain_order: Explicit output atom order.
    :type chain_order: Sequence[int] | None
    :param check_unique_root: Validate the zero-, one-, and two-parent embedding rows.
    :type check_unique_root: bool
    :param base_order: Preferred atom order constrained so parents precede children.
    :type base_order: Sequence[int] | None
    :return: Four-column Z-matrix rows.
    :rtype: list[list[int]]
    """
    ...

def check_zmatrix_coordinate_constraint(zm, coord):
    """
    **LLM Docstring**

    Test whether an internal coordinate appears as a contiguous parent prefix in a Z-matrix tree.

    The coordinate is accepted when it starts at its first atom and follows that atom's first `len(coord)-1` parents, or when the reversed coordinate follows the final atom's parent prefix.

    :param zm: Tree mapping produced by `make_zmatrix_tree`.
    :type zm: dict
    :param coord: Bond, angle, or dihedral tuple to require.
    :type coord: Sequence[int]
    :return: `(row_atom, full_parent_tuple)` for the matching orientation, otherwise `False`.
    :rtype: tuple | bool
    """
    ...

def _adjust_zm_parents(zm, i, new, constraint_map, validate=False):
    """
    **LLM Docstring**

    Attempt to replace one atom's parent tuple while preserving all registered coordinate constraints.

    The candidate parents are installed, child sets are updated, and a new bond-parent depth-first order is computed. Parents that would occur after their child are removed and replenished from earlier ancestors or earlier chain atoms until each row has the required number. The change is committed only if every constraint still matches; otherwise the original tree is restored.

    :param zm: Mutable Z-matrix tree mapping.
    :type zm: dict
    :param i: Atom whose parents are being replaced.
    :type i: int
    :param new: Candidate ordered parent tuple.
    :type new: tuple[int, ...]
    :param constraint_map: Existing coordinate constraints that must remain representable.
    :type constraint_map: dict
    :param validate: Check generated parent tuples for duplicate atoms.
    :type validate: bool
    :return: Success flag and the committed or restored tree.
    :rtype: tuple[bool, dict]
    """
    ...

def enforce_required_zmatrix_coordinates(zm, required_coordinates=None, root_coordinates=None, isolated_coordinates=None, reparent_isolated_coordinates=True, reparent_root_coordinates=True, validate=False):
    """
    **LLM Docstring**

    Reparent a Z-matrix tree so requested bonds, angles, and dihedrals occur as row parent prefixes.

    Already satisfied constraints are retained. Isolated coordinates can first be prevented from serving as references for unrelated rows, and root coordinates can be promoted into the initial embedding chain. Missing required coordinates are then tried in both orientations by replacing candidate parent prefixes through `_adjust_zm_parents`; all previously accepted constraints must remain valid. The result is returned in the same row representation as the input.

    :param zm: Z-matrix rows or tree mapping.
    :type zm: Sequence[Sequence[int]] | dict
    :param required_coordinates: Coordinates that must appear in either orientation.
    :type required_coordinates: Sequence[Sequence[int]] | None
    :param root_coordinates: Coordinates preferentially incorporated into the initial chain.
    :type root_coordinates: Sequence[Sequence[int]] | None
    :param isolated_coordinates: Coordinates whose endpoint atoms should not become unrelated parents.
    :type isolated_coordinates: Sequence[Sequence[int]] | None
    :param reparent_isolated_coordinates: Remove isolated-coordinate endpoints as references where alternatives exist.
    :type reparent_isolated_coordinates: bool
    :param reparent_root_coordinates: Attempt to move root coordinates into the root chain.
    :type reparent_root_coordinates: bool
    :param validate: Enable duplicate-parent and intermediate-tree checks.
    :type validate: bool
    :return: Reparented Z-matrix in the original input representation.
    :rtype: list[list[int]] | dict
    """
    ...

def bond_graph_zmatrix(bonds, fragments, edge_map=None, reindex=True, validate_additions=True, required_coordinates=None, isolated_coordinates=None, root_coordinates=None, enforce_requirements=True):
    """
    **LLM Docstring**

    Construct a Z-matrix spanning a bonded graph, including disconnected or fused fragments.

    Fragments and an edge map are obtained from the supplied `EdgeGraph` or bond list. Provided backbone fragments are fused first; missing graph fragments receive submatrices and are attached through graph edges. The combined local ordering is reindexed to original atom labels. Optional required, root, and isolated coordinates are enforced after assembly.

    :param bonds: Bond pairs or an `EdgeGraph` describing molecular connectivity.
    :type bonds: Sequence[tuple[int, int]] | EdgeGraph
    :param fragments: Optional atom-index fragments; inferred from the graph when omitted.
    :type fragments: Sequence[Sequence[int]] | None
    :param submats: Optional Z-matrix ordering for each fragment.
    :type submats: Sequence[Sequence[Sequence[int]]] | None
    :param backbone: Optional initial atom ordering or fragment backbone.
    :type backbone: Sequence | None
    :param edge_map: Precomputed adjacency mapping.
    :type edge_map: dict | None
    :param reindex: Map the assembled local ordering back to original atom labels.
    :type reindex: bool
    :param validate_additions: Validate intermediate fragment attachments.
    :type validate_additions: bool
    :param required_coordinates: Coordinates that must be represented after assembly.
    :type required_coordinates: Sequence | None
    :param isolated_coordinates: Coordinates to keep isolated from unrelated parent references.
    :type isolated_coordinates: Sequence | None
    :param root_coordinates: Coordinates to place near the root chain.
    :type root_coordinates: Sequence | None
    :param enforce_requirements: Apply coordinate reparenting after graph assembly.
    :type enforce_requirements: bool
    :return: Z-matrix ordering spanning the graph.
    :rtype: list[list[int]]
    """
    ...

def canonical_fragment_zmatrix(canonical_framents, validate_additions=False):
    """
    **LLM Docstring**

    Join preordered atom fragments into one canonical Z-matrix.

    Each fragment is represented by a chain Z-matrix. The first fragment becomes the backbone; every later fragment is attached to the previous combined ordering using up to the last three existing atom positions as external references. The final local rows are reindexed to the concatenated original fragment labels.

    :param canonical_framents: Atom-index fragments in the desired fragment and intra-fragment order.
    :type canonical_framents: Sequence[Sequence[int]]
    :param validate_additions: Validate the local and reindexed combined ordering.
    :type validate_additions: bool
    :return: Combined Z-matrix in original atom-label space.
    :rtype: list[list[int]]
    """
    ...

def sort_complex_attachment_points(fragment_inds, attachment_points: 'dict|tuple[tuple[int], list[list[int]]]'):
    """
    **LLM Docstring**

    Orient and order complex-fragment attachment records into a connected fragment traversal.

    Attachment endpoints are associated with the fragments containing them. Starting from `start_frag` when supplied, the routine repeatedly selects attachments that connect the current fragment to an unvisited fragment, reversing endpoint order when necessary. It returns fragments in traversal order together with attachment references keyed by the newly reached fragment.

    :param fragment_inds: Atom indices for each disconnected fragment.
    :type fragment_inds: Sequence[Sequence[int]]
    :param attachment_points: Mapping or iterable describing atom-level links between fragments.
    :type attachment_points: dict | Iterable
    :param start_frag: Optional fragment index from which to begin traversal.
    :type start_frag: int | None
    :return: Reordered fragments and attachment specifications for joining them.
    :rtype: tuple[list[tuple[int, ...]], dict]
    """
    ...

def complex_zmatrix(bonds, fragment_inds=None, fragment_zmats=None, distance_matrix=None, attachment_points=None, check_attachment_points=True, graph=None, reindex=True, required_coordinates=None, isolated_coordinates=None, root_coordinates=None, validate_additions=True):
    """
    **LLM Docstring**

    Assemble a Z-matrix for multiple disconnected fragments using explicit or distance-derived attachment points.

    Fragments are inferred from the bond graph when needed and each receives a supplied or generated Z-matrix. Attachments are sorted into a connected traversal. When an attachment is absent, the closest interfragment atom pair is selected from `distance_matrix`; `_attachment_point` supplies the remaining angle and dihedral references from the graph. Fragments are appended with `functionalized_zmatrix`, optionally reindexed to original atoms, validated, and reparented to satisfy requested coordinates.

    :param bonds: Bond list used to construct the graph when `graph` is omitted.
    :type bonds: Sequence[tuple[int, int]] | None
    :param fragment_inds: Atom indices for each fragment.
    :type fragment_inds: Sequence[Sequence[int]] | None
    :param fragment_zmats: Z-matrix ordering for each fragment.
    :type fragment_zmats: Sequence | None
    :param distance_matrix: Pairwise distances used to choose closest attachment atoms.
    :type distance_matrix: np.ndarray | None
    :param attachment_points: Explicit interfragment attachment specifications.
    :type attachment_points: dict | Sequence | None
    :param check_attachment_points: Validate that attachment references belong to the appropriate fragments.
    :type check_attachment_points: bool
    :param graph: Connectivity graph used for fragments and neighboring references.
    :type graph: EdgeGraph | None
    :param reindex: Return rows in original atom-label space.
    :type reindex: bool
    :param required_coordinates: Coordinates required in the final ordering.
    :type required_coordinates: Sequence | None
    :param isolated_coordinates: Coordinates protected from unrelated parent usage.
    :type isolated_coordinates: Sequence | None
    :param root_coordinates: Coordinates preferentially placed at the root.
    :type root_coordinates: Sequence | None
    :param validate_additions: Validate fragment assembly and final ordering.
    :type validate_additions: bool
    :return: Combined complex Z-matrix.
    :rtype: list[list[int]]
    """
    ...

def graph_backbone_zmatrix(bond_graph: EdgeGraph, root=None, segments=None, return_remainder=False, return_segments=False, validate=True):
    """
    **LLM Docstring**

    Create a Z-matrix backbone from chain segments of a connectivity graph.

    The graph is segmented into chains, optionally relative to a chosen root. Each segment is converted to a chain Z-matrix and the segments are joined through `canonical_fragment_zmatrix` or `complex_zmatrix` according to the available connectivity. Depending on requested flags, the function also returns segment or graph metadata alongside the ordering.

    :param bond_graph: Connectivity graph to segment.
    :type bond_graph: EdgeGraph
    :param root: Preferred root atom for chain segmentation.
    :type root: int | None
    :param validate: Validate fragment joins.
    :type validate: bool
    :param return_segments: Include the chain segments in the result.
    :type return_segments: bool
    :param return_graph: Include the graph in the result.
    :type return_graph: bool
    :return: Z-matrix, optionally followed by segments and graph metadata.
    :rtype: tuple | list[list[int]]
    """
    ...

def segmented_complex_backbone_zmatrix(bond_graph: EdgeGraph, fragments=None, segments=None, root=None, attachment_points=None, check_attachment_points=True, validate=True, for_fragment=None, fragment_ordering=None, distance_matrix=None):
    """
    **LLM Docstring**

    Construct a complex Z-matrix by building graph-based backbones for each disconnected fragment.

    Disconnected graph fragments are identified first. A single fragment is delegated to `graph_backbone_zmatrix`; multiple fragments are processed recursively to obtain local backbones, then joined with `complex_zmatrix` using graph connectivity, optional distances, and attachment specifications. Optional metadata is propagated with the final ordering.

    :param bond_graph: Connectivity graph, possibly containing multiple fragments.
    :type bond_graph: EdgeGraph
    :param root: Preferred root atom or fragment root.
    :type root: int | None
    :param distance_matrix: Pairwise distances used to connect disconnected fragments.
    :type distance_matrix: np.ndarray | None
    :param attachment_points: Explicit links between fragments.
    :type attachment_points: dict | Sequence | None
    :param validate: Validate each local and combined ordering.
    :type validate: bool
    :param return_segments: Include segment information in the result.
    :type return_segments: bool
    :param return_graph: Include graph metadata in the result.
    :type return_graph: bool
    :return: Combined Z-matrix, optionally with segment and graph metadata.
    :rtype: tuple | list[list[int]]
    """
    ...