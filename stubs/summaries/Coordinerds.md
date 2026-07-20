### `Conveniences.py` — Convenience functions that are inefficient, but are maybe a bit easier to work with?
- `cartesian_to_zmatrix(coords, ordering=None, use_rad=True)` — Converts Cartesians to Z-Matrix coords and returns the underlying arrays
- `zmatrix_to_cartesian(coords, ordering=None, origins=None, axes=None, use_rad=True)` — Converts Z-maztrix coords to Cartesians

### `Conversions.py`
- `get_dists(points, centers)` — Compute the Euclidean distance from each `center` to the corresponding `point` using `Numputils.pts…
- `get_angles(lefts, centers, rights)` — Compute angles for triples `(left, center, right)`.
- `get_diheds(points, centers, seconds, thirds)` — Compute signed dihedral angles for quadruples `(point, center, second, third)`.
- `tile_order_list(ol, ncoords)` — Repeat a Z-matrix ordering block until it contains one row per coordinate and offset atom-index col…
- `convert_cartesian_to_zmatrix(coords, *, ordering, use_rad=True, return_derivs=None, order=None, strip_embedding=False, derivative_method='new')` — The ordering should be specified like:
- `convert_zmatrix_to_cartesians(coordlist, *, ordering, origins=None, axes=None, use_rad=True, return_derivs=None, order=None)` — Expects to get a list of configurations

### `Generators.py`
- `get_stretch_angles(stretches)` — Generate every bond angle implied by pairs of stretches that share one atom.
- `get_stretch_angle_dihedrals(stretches, angles)` — Extend an angle by a bonded atom to form candidate dihedral coordinates.
- `get_angle_stretches(angles)` — Expand each angle into its two adjacent bond coordinates.
- `get_dihedral_stretches(dihedrals)` — Expand each dihedral into its three adjacent bond coordinates.
- `get_angle_dihedrals(angles)` — Join compatible pairs of angles across a shared bond to form dihedrals.
- `get_stretch_coordinate_system(stretches, include_bends=True, include_dihedrals=True)` — Construct bends and dihedrals implied by a set of stretches.
- `get_fragment_coordinate_system(bond_graph, fragments=None, masses=None, distance_matrix=None)` — Choose fragment pairs and describe intermolecular orientation coordinates between them.
  - **class `PrimitiveCoordinatePicker`**
    - `__init__(atoms, bonds, base_coords=None, rings=None, fragments=None, light_atoms=None, backbone=None, neighbor_count=3)`
    - `coords()` — Return the cached primitive coordinate set, generating it on first access.
    - `generate_coords()` — Assemble primitive coordinates for rings, fused rings, fragment connections, and non-ring atoms.
    - `canonicalize_coord(coord)` — Normalize an internal coordinate so reversal-equivalent tuples have one orientation.
    - `prep_unique_coords(coords)` — Canonicalize coordinates and identify first occurrences, but currently return the original input.
    - `prune_excess_coords(coord_set, canonicalized=False)` — Canonicalize a coordinate set and remove duplicates plus selected redundant angle/dihedral ordering…
    - `ring_coordinates(ring_atoms)` — Generate cyclic bonds, angles, and dihedrals around an ordered ring.
    - `unfused_ring_coordinates(ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2)` — Return no additional coordinates for two rings that share no atoms.
    - `pivot_fused_ring_coordinates(ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2)` — Generate four cross-ring angles for rings fused at a single pivot atom.
    - `simple_fused_ring_coordinates(ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2)` — Generate two cross-ring dihedrals for rings sharing one bond.
    - `fused_ring_coordinates(ring_atoms1, ring_atoms2)` — Dispatch fused-ring coordinate generation according to the number of shared atoms.
    - `fragment_connection_coords(frag_1, frag_2)` — Construct up to six primitive coordinates connecting two disconnected fragments.
    - `get_neighborhood_symmetries(atoms, ignored=None, neighborhood=3)` — Compare local neighbor graphs for every unordered pair of atoms.
    - `chain_coords(R, y)` — Attach an atom to the tail of a precedent chain with one stretch, one angle, and one dihedral when…
    - `RYX2_coords(R, y, X)` — Generate coordinates for a center atom with a three-member neighbor group and an optional precedent…
    - `RYX3_coords(R, y, X)` — Generate coordinates for a center atom with three neighbors and an optional precedent chain.
    - `get_precedent_chains(atom, num_precs=2, ring_atoms=None, light_atoms=None, ignored=None, backbone=None)` — Enumerate graph paths leading away from an atom up to a requested predecessor depth.
    - `get_symmetry_groups(neighbors, matches)` — Convert pairwise equality flags into groups of equivalent neighbors.
    - `symmetry_coords(atom, neighborhood=3, backbone=None)` — Generate chain-based coordinates for a non-ring atom.
- `enumerate_coordinate_completions_line(indices, coords, canonicalize=False)` — Enumerate the missing internal coordinates needed to complete a one- through four-atom geometric te…
- `enumerate_coordinate_sets(groups, coords, canonicalize=True)` — Recursively enumerate coordinate sets that complete each supplied atom group.

### `Internals.py`
  - **class `InternalCoordinateType`**
    - `register(type, typename=None)` — Register an `InternalCoordinateType` subclass under a dispatch name.
    - `get_dispatch()` — Return the lazily constructed options dispatcher used to turn dictionaries containing a `type` key…
    - `resolve(input)` — Convert either a typed option dictionary or a bare index sequence into an instantiated coordinate o…
    - `could_be(input)` — Report whether an input can represent this coordinate type.
    - `equivalent_to(other)` — Test whether two coordinates have the same concrete type and the same indices after each is put in…
    - `canonicalize()` — Return an equivalent coordinate in the canonical index orientation defined by the concrete coordina…
    - `get_indices()` — Return the atom indices that define this internal coordinate, in the type-specific ordering.
    - `reindex(reindexing)` — Return the same coordinate expressed under a supplied old-index to new-index mapping.
    - `get_carried_atoms(context)` — Determine the atom groups displaced on the two sides of this coordinate when it is varied in an `In…
    - `get_constraint_rads()` — Return the primitive distance, angle, or dihedral coordinates that must remain available to constra…
    - `get_expansion(coords, order=None, **opts)` — Evaluate Cartesian derivatives of this internal coordinate through the requested order.
    - `get_inverse_expansion(coords, order=None, moved_indices=None, **opts)` — Evaluate derivatives of the Cartesian displacement generated by changing this internal coordinate,…
  - **class `BasicInternalType`** (InternalCoordinateType)
    - `__init__(indices)`
    - `reindex(reindexing)` — Apply an index lookup to every defining atom and construct a coordinate of the same type with the m…
    - `canonicalize()` — Orient a reversible coordinate so that its final atom index is not smaller than its first; reverse…
    - `get_indices()` — Return the stored tuple of defining atom indices.
    - `get_dropped_internals()` — Return the set of coordinates removed from the bond graph when determining which atoms move with th…
    - `get_carried_atoms(context, max_branching=5)` — Split the internal-coordinate bond graph into fragments associated with the first and last atoms.
    - `get_expansion(coords, *, order=None, masses=None, **opts)` — Call the coordinate type’s forward derivative routine with the stored atom indices to obtain deriva…
    - `get_inverse_expansion(coords, *, order=None, moved_indices=None, context=None, left_atoms=None, right_atoms=None, masses=None, **opts)` — Resolve the atoms moved on each side of the coordinate and call the type’s inverse derivative routi…
  - **class `Distance`** (BasicInternalType)
    - `could_be(input)` — Recognize a distance specification as a two-element integer index sequence.
    - `get_constraint_rads()` — Return the distance itself as the sole primitive coordinate required to constrain it.
  - **class `Angle`** (BasicInternalType)
    - `could_be(input)` — Recognize an angle specification as a three-element integer index sequence.
    - `get_constraint_rads()` — Return the angle itself as the primitive coordinate required to constrain it.
    - `get_dropped_internals()` — Remove the angle and its two adjacent bond distances when finding the atom groups carried by an ang…
  - **class `Dihedral`** (BasicInternalType)
    - `could_be(input)` — Recognize a dihedral specification as a four-element integer index sequence.
    - `get_constraint_rads()` — Return the dihedral itself as the primitive coordinate required to constrain it.
    - `get_dropped_internals()` — Remove the dihedral, its central angle pair, and the three chain bond distances when separating the…
  - **class `Wag`** (BasicInternalType)
    - `get_constraint_rads()` — Represent a wagging coordinate by the three dihedrals formed by the central atom and each choice of…
  - **class `OutOfPlane`** (BasicInternalType)
  - **class `TranslatonRotation`** (BasicInternalType)
    - `__init__(indices, masses=None)`
    - `canonicalize()` — Return the rigid-body coordinate unchanged because its atom set has no reversible endpoint orientat…
    - `get_carried_atoms(context)` — Treat all atoms in the rigid-body coordinate as the moved group and return no opposing group.
    - `get_inverse_expansion(coords, *, order=None, context=None, moved_indices=None, extra_atoms=None, masses=None, **opts)` — Build the translation/rotation inverse expansion for the selected atoms using the stored or supplie…
  - **class `Orientation`** (BasicInternalType)
    - `__init__(indices, masses=None)`
    - `canonicalize()` — Return the orientation unchanged because reversing its atom order changes the directed orientation.
    - `get_indices()` — Return the stored atom indices defining the orientation.
    - `reindex(reindexing)` — Map the orientation’s atoms through a supplied reindexing and preserve its mass data.
    - `get_carried_atoms(context)` — Return the orientation atoms as the moved group and no atoms on the opposite side.
    - `get_inverse_expansion(coords, *, order=None, moved_indices=None, context=None, left_extra_atoms=None, right_extra_atoms=None, masses=None, **opts)` — Construct the Cartesian inverse expansion for changing the orientation of the selected atoms, using…
  - **class `InternalSpec`**
    - `__init__(coords, canonicalize=True, bond_graph=None, triangulation=None, masses=None, ungraphed_internals=None, distance_conversions=None)`
    - `from_zmatrix(*zmats, additions=None, **opts)` — Create an `InternalSpec` from one or more Z-matrix index arrays by collecting each row’s distance,…
    - `atom_sets()` — Return the defining atom tuple for every coordinate in the specification.
    - `atoms()` — Return the sorted unique atom indices appearing in any coordinate.
    - `get_triangulation()` — Lazily derive and cache the triangle and dihedron sets that express the specification as connected…
    - `get_pruned_rads()` — Return the subset of primitive coordinates retained after removing redundancies implied by the tria…
    - `get_pruned_triangulation()` — Return a triangulation rebuilt from the nonredundant primitive coordinates.
    - `get_bond_graph()` — Lazily construct an `EdgeGraph` whose edges are the bond distances represented by the coordinate se…
    - `graph()` — Expose the cached or newly constructed bond graph for the specification.
    - `get_distance_conversions()` — Build and cache the conversion specification and callable that reconstruct all triangulation distan…
    - `get_zmat_conv(raise_on_incomplete=True)` — Find and cache a conversion from this coordinate set to a Z-matrix ordering.
    - `get_dmat_conv()` — Build and cache a converter from internal-coordinate values to the condensed or square distance-mat…
    - `get_dropped_internal_bond_graph(internals, method=None)` — Return a copy of the bond graph with the bonds implied by selected coordinates removed, using eithe…
    - `get_direct_derivatives(coords, order=1, cache=True, reproject=False, base_transformation=None, reference_internals=None, combine_expansions=True, terms=None, **opts)` — Evaluate direct Cartesian derivatives for every coordinate, pad them to the full atom set, and stac…
    - `orthogonalize_transformations(expansion, inverse, coords=None, masses=None, order=None, remove_translation_rotations=False)` — Mass-weight and orthogonalize forward and inverse transformation matrices with an SVD-based pseudoi…
    - `get_expansion(coords, order=1, return_inverse=False, remove_translation_rotations=True, orthogonalize=True, **opts)` — Assemble derivatives of the complete internal-coordinate vector with respect to Cartesian coordinat…
    - `get_direct_inverses(coords, order=1, terms=None, combine_expansions=True, **opts)` — Evaluate each coordinate’s inverse Cartesian expansion and combine the per-coordinate tensors into…
    - `cartesians_to_internals(coords, order=None, **opts)` — Evaluate every stored coordinate on Cartesian geometries and optionally return its Cartesian deriva…
    - `internals_to_cartesians(coords, order=None, reference_cartesians=None, return_fragments=False, return_inverse=True, transformations=None, reference_internals=None, use_distance_matrix_fallback=False, **deriv_opts)` — Recover Cartesian geometries from internal values using either the cached Z-matrix route or distanc…
    - `get_triangulation_novel_internals(rads=None, triangulation=None)` — Return coordinates that contribute distances not already represented by a triangulation, together w…
    - `get_triangulation_distances(rads=None, triangulation=None)` — Collect and deduplicate all pair distances required by the triangulation and optionally by an expli…
    - `check_redundancy()` — Check whether the coordinate set contains more independent constraints than its atom count permits,…
- `canonicalize_internal(coord, return_sign=False, check_invalid=True)` — Put a distance, angle, or dihedral index sequence into its canonical orientation.
- `is_valid_coordinate(coord)` — Return whether a value is an integer index sequence of length two, three, or four.
- `is_coordinate_list_like(clist)` — Return whether every element of a sequence is a valid distance, angle, or dihedral specification.
  - **class `RADInternalCoordinateSet`**
    - `__init__(coord_specs, prepped_data=None, triangulation=None)`
    - `specs()` — Return the normalized coordinate specifications in their original coordinate-type grouping.
    - `prep_coords(coord_specs)` — Canonicalize input coordinates, group them by arity, deduplicate equivalent entries, and build maps…
    - `find(coord, missing_val='raise')` — Locate a coordinate in the canonical coordinate map, respecting the requested value for missing coo…
    - `get_coord_from_maps(item, indicator, ind_map, coord_map)` — Resolve an indexed selection through the indicator, flattened-index, and coordinate maps to recover…
    - `permute(perm, canonicalize=True)` — Apply an atom permutation to every coordinate and return a new coordinate set, optionally canonical…
    - `get_triangulation()` — Compute triangle and dihedron sets from the stored coordinates and cache the result.
    - `triangulation()` — Return the cached triangulation, computing it on first access.
- `get_canonical_internal_list(coords)` — Canonicalize every coordinate in a sequence and remove duplicates while preserving first-occurrence…
- `find_internal(coords, coord, missing_val='raise', canonicalize=True, allow_negation=False, indices=None)` — Find a coordinate in a coordinate list after optional canonicalization.
- `permute_internals(coords, perm, canonicalize=True)` — Apply an atom-index permutation to each coordinate and optionally canonicalize the resulting coordi…
- `coordinate_sign(old, new, canonicalize=True)` — Determine whether two equivalent coordinate specifications have the same or opposite orientation, r…
- `coordinate_indices(coords)` — Flatten a coordinate list into an integer array and return the per-coordinate arity indicators need…
- `get_internal_distance_conversion_spec(internals, canonicalize=True, cache=None)` — Analyze distances, angles, and dihedrals to produce an ordered recipe for reconstructing every requ…
- `internal_distance_convert(coords, specs, canonicalize=True, shift_dihedrals=True, abs_dihedrals=True, check_distance_spec=True)` — Convert internal-coordinate values to pair distances using a precomputed or newly generated convers…
- `get_internal_triangles_and_dihedrons(internals, canonicalize=True, base=None, base_internals=None, construct_shapes=True, prune_incomplete=True, validate=False, allow_partially_defined=True, create_compound_dihedra=True, add_dihedron_triangles=False, create_dihedra=True)` — Construct a dependency-ordered triangulation of an internal-coordinate set.
- `get_triangulation_internals(triangulation)` — Extract the primitive distance, angle, and dihedral coordinates represented by triangle and dihedro…
- `get_core_triangulation(internal_bag, targets, intersection='partial', cache=None, **kwargs)` — Reduce a triangulation to the connected subset needed to support target coordinates, retaining reco…
- `merge_dihedral_sets(sub_diheds, unmodified_diheds, in_place=False, merge_strategy='both')` — Merge modified dihedron records back into unmodified records while canonicalizing equivalent vertex…
- `merge_triangle_sets(sub_tris, unmodified_tris, in_place=False, merge_strategy='both')` — Merge modified triangle records back into unmodified records while canonicalizing equivalent vertex…
- `update_triangulation(triangulation, added_internals, removed_internals, triangulation_internals=None, return_split=False, validate=False)` — Update triangle and dihedron records after coordinates are added, removed, or replaced.
  - **class `InternalCoordinateConversion`**
    - `__init__(caller, provenance, name=None)`
- `find_internal_conversion(internals, targets, triangles_and_dihedrons=None, canonicalize=True, allow_completion=True, return_conversions=False, prep_conversions=True, include_shapes=False, indices=None, cache=None, disallowed_conversions=None, update_triangles_and_dihedrons=False, return_completions=False, allow_recursive_completions=None, allow_ambiguous_completions=False, dihedral_intersections=None, index_mapping=None, verbose=False, missing_val='raise')` — Build a conversion from an available internal-coordinate set to requested target coordinates.
- `enumarate_zmatrix_roots_from_triangles(atoms, tris, connectivity_graph)` — Enumerate three-atom Z-matrix roots from complete triangles whose atoms satisfy the connectivity gr…
- `construct_atom_connection_graph_from_triangulation(internals, tris, dihedrons)` — Build an atom adjacency graph from explicit distances and from edges implied by triangle and dihedr…
- `get_fragments_from_internals(internals, triangles_and_dihedrons=None)` — Construct the bond graph implied by internal coordinates and return its connected atom fragments, w…
- `enumerate_zmatrices_from_internals(internals, triangles_and_dihedrons=None, atoms=None, ordering=None, graph=None, build_conversion=True, max_ordering_passes=1, **conversion_options)` — Enumerate Z-matrix index arrays compatible with an internal-coordinate set.
- `get_internal_distance_conversion(internals, triangles_and_dihedrons=None, dist_set=None, canonicalize=True, allow_completion=True, missing_val='raise', include_shapes=False, return_conversions=False, prep_conversions=True, cache=None)` — Return a callable that transforms internal-coordinate values into the pair distances required by th…
- `get_internal_cartesian_conversion(internals, triangles_and_dihedrons=None, canonicalize=True, missing_val='raise')` — Construct a converter from internal-coordinate values to Cartesian geometries by composing internal…
- `validate_internals(internals, triangles_and_dihedrons=None, raise_on_failure=True)` — Validate that an internal-coordinate set can produce a complete, consistent triangulation and optio…
- `get_internal_bond_graph(internals, atoms=None, triangles_and_dihedrons=None, dist_set=None, return_conversions=False, complete_graph=False)` — Build an `EdgeGraph` from explicit and triangulation-implied bond distances, optionally including i…
  - **class `NonredundantInternalsChecker`**
    - `__init__(base_internals, natoms, dist_set=None)`
    - `dists()` — Return the current canonical distance set represented by the accepted coordinates.
    - `check_rigidty(dists)` — Test whether a proposed distance graph is minimally rigid for the checker’s atom count using the co…
    - `from_initial_internals(internals)` — Construct a checker from an existing coordinate list after deriving its atoms, distance set, and in…
    - `check_trilateratable_distance(i, j, dists)` — Determine whether a new distance can be inferred by trilateration from already known distances to s…
    - `check_distances_convertable(new_coords, dists, graph, allow_recursive_completions=False, filter_by_new=True)` — Determine whether all pair distances introduced by candidate coordinates are already known or recon…
    - `add_internal(c, keep_bonds=True, keep_angles=True)` — Attempt to add one coordinate without introducing redundant constraints.
  - **class `InternalCoordinateGraph`**
    > A graph mapping out the connections between a set of atoms based on the given set of internals
    - `__init__(internals, atoms=None, triangles_and_dihedrons=None)`
    - `get_target_triangulation(internals, target)` — Return the subset of the current triangulation needed to support a target coordinate.
    - `enumerate_matching_dihedrons(target_coord)` — Yield dihedron records and permutations that contain the target coordinate’s atoms in a usable arra…
    - `find_conversions(target_internals, unconvertable_atoms=None, allow_recursive_completions=False, allow_ambiguous_completions=False, find_unreachable=True, verbose=False, create_single=False, missing_val=None, depth=0, max_depth=5, **etc)` — Find or construct conversions from the graph’s current coordinates to one or more target coordinate…
    - `get_bond_graph(dist_set=None, return_conversions=True)` — Return the bond graph implied by the graph’s current coordinates and triangulation, optionally rebu…
    - **class `GraphCheckpoint`**
      - `__init__(g, reset=True)`
    - `checkpoint()` — Return a context manager for making temporary changes to the internal-coordinate graph.
    - `add_internals(internals)` — Add coordinates to the graph, update triangulation and bond data, and refresh conversion caches for…
    - `remove_internals(internals)` — A non-implemented stub for future development.

### `Labels.py`
- `get_coordinate_label(coord, atom_labels, atom_order=None)` — Build a structured label describing the chemical motif and optional ring/group membership of an int…
- `coordinate_sorting_key(label, type_ordering=None, atom_ordering=None)` — Construct a sortable tuple that orders coordinates first by type and then by their constituent atom…
- `sort_internal_coordinates(coords, atoms=None, sort_key=None)` — Sort internal coordinates or a coordinate-label mapping using a coordinate-aware key.
- `get_mode_labels(internals, internal_modes_by_coords, norm_cutoff=0.8)` — Identify the internal coordinates that carry each normal mode and infer their common coordinate typ…

### `Pruning.py`
  - **class `InternalCoordinatePruner`**
    - `pruning_iterator(coords, *args, **kwargs)` — Yield every candidate coordinate in its original order.
    - `prune_coordinates(coords, *args, base_internals=None, check_rigidity=True, natoms=None, **kwargs)` — Drive a pruning generator while optionally rejecting coordinates that do not increase the nonredund…
  - **class `UniqueInternalCoordinatePruner`** (InternalCoordinatePruner)
    - `pruning_iterator(coords)` — Yield the first occurrence of each canonical internal coordinate.
  - **class `GeometricInternalCoordinatePruner`** (InternalCoordinatePruner)
    - `pruning_iterator(coords, b_matrix, max_coords=None, base_internals=None, small_value_cutoff=0.0001, max_contrib_cutoff=0.05, return_positions=False)` — Yield a subset of coordinates whose B-matrix columns remain linearly independent above an SVD thres…
- `prune_internal_coordinates(coords, *args, method='basic', **kwargs)` — Resolve a pruning strategy and apply it to a coordinate collection.

### `Redundant.py`
  - **class `RedundantCoordinateGenerator`**
    - `__init__(coordinate_specs, angle_ordering='ijk', untransformed_coordinates=None, masses=None, relocalize=False, **opts)`
    - `base_redundant_transformation(expansion, untransformed_coordinates=None, masses=None, relocalize=False)` — Extract an orthonormal basis for the non-null internal-coordinate subspace from a Cartesian-to-inte…
    - `get_redundant_transformation(base_expansions, untransformed_coordinates=None, masses=None, relocalize=False)` — Construct the nonredundant transformation and re-expand derivative tensors into that basis.
    - `compute_redundant_expansions(coords, order=None, untransformed_coordinates=None, expansions=None, relocalize=None)` — Evaluate Cartesian derivatives of the configured redundant coordinates and transform them to a nonr…
    - `prune_coordinate_specs(expansion, masses=None, untransformed_coordinates=None, pruning_mode='loc', **opts)` — Mass-weight a coordinate Jacobian and dispatch one of the supported column-selection algorithms.
  - **class `MultiOriginCoordinates`**
    - `__init__(origins, zmats)`

### `ZMatrices.py`
- `zmatrix_unit_convert(zmat, distance_conversion, angle_conversion=None, rad2deg=False, deg2rad=False)` — Scale the distance and angular columns of a Z-matrix value array.
- `zmatrix_indices(zmat, coords, strip_embedding=True)` — Locate internal coordinates within the ordered coordinate list represented by a Z-matrix.
- `zmatrix_embedding_coords(zmat_or_num_atoms, partial_embedding=False, array_inds=False)` — Return the flattened entries occupied by Z-matrix embedding coordinates.
- `num_zmatrix_coords(zmat_or_num_atoms, strip_embedding=True)` — Count scalar Z-matrix coordinates for a molecule or ordering.
- `enumerate_zmatrices(coords, natoms=None, allow_permutation=True, include_origins=False, canonicalize=True, deduplicate=True, preorder_atoms=True, allow_completions=False)` — Enumerate Z-matrix orderings compatible with supplied internal coordinates.
- `extract_zmatrix_internals(zmat, strip_embedding=True, canonicalize=True)` — Expand a Z-matrix ordering into its bond, angle, and dihedral coordinate tuples.
- `extract_zmatrix_values(zmat, inds=None, partial_embedding=False, strip_embedding=True)` — Flatten Z-matrix values and select internal-coordinate entries.
- `zmatrix_from_values(flat_z, strip_embedding=True, partial_embedding=False)` — Reconstruct an atom-by-three Z-matrix value array from flattened values.
- `parse_zmatrix_string(zmat, units='Angstroms', in_radians=False, has_values=True, atoms_are_order=False, keep_variables=False, variables=None, dialect='gaussian')` — Parse a Gaussian-style textual Z-matrix into atoms, ordering, and coordinate values.
- `format_zmatrix_string(atoms, zmat, ordering=None, units='Angstroms', in_radians=False, float_fmt='{:11.8f}', index_padding=1, variables=None, variable_modifications=None, distance_variable_format='r{i}', angle_variable_format='a{i}', dihedral_variable_format='d{i}')` — Format atoms, references, and values as a Gaussian-style Z-matrix string.
- `validate_zmatrix(ordering, allow_reordering=True, ensure_nonnegative=True, raise_exception=False, return_reason=False)` — Check that a Z-matrix ordering defines atoms before they are referenced and contains valid row refe…
- `chain_zmatrix(n)` — Each atom references the immediately preceding atom for distance, the atom two positions back for a…
- `center_bound_zmatrix(n, center=-1)` — Construct rows whose bond reference is a common center.
- `attached_zmatrix_fragment(n, zm, fragment, attachment_points)` — Translate a fragment Z-matrix from local indices and negative placeholders into a larger Z-matrix.
- `set_zmatrix_embedding(zmat, embedding=None, partial_embedding=False)` — Write standard embedding reference values into a Z-matrix ordering.
- `functionalized_zmatrix(base_zm, attachments=None, single_atoms=None, methyl_positions=None, ethyl_positions=None, validate=False)` — Build a larger Z-matrix by attaching fragments and optional standard substituent patterns.
- `spoke_zmatrix(m, spoke=1, root=1)` — Construct a root fragment with `m` copies of a spoke fragment attached to its terminal atom.
- `reindex_zmatrix(zm, perm)` — Replace every nonnegative atom index in a Z-matrix using `perm`.
- `canonicalize_zmatrix(zm)` — Convert a Z-matrix to row-index space while preserving its explicit atom ordering.
- `add_missing_zmatrix_bonds(base_zmat, bonds, max_iterations=None, validate_additions=True)` — Recursively add atoms connected by `bonds` but absent from a partial Z-matrix.
- `make_zmatrix_tree(zm)` — Represent Z-matrix parent references as a bidirectional tree-like mapping.
- `zmatrix_adjacency_matrix(zm, child_type='multi', penalty_atoms=None)` — Build a directed parent-to-child adjacency matrix from a Z-matrix tree.
- `zmatrix_from_tree(zm, check_cycles=True, chain_order=None, check_unique_root=True, base_order=None)` — Convert a parent/children mapping back into ordered four-column Z-matrix rows.
- `check_zmatrix_coordinate_constraint(zm, coord)` — Test whether an internal coordinate appears as a contiguous parent prefix in a Z-matrix tree.
- `enforce_required_zmatrix_coordinates(zm, required_coordinates=None, root_coordinates=None, isolated_coordinates=None, reparent_isolated_coordinates=True, reparent_root_coordinates=True, validate=False)` — Reparent a Z-matrix tree so requested bonds, angles, and dihedrals occur as row parent prefixes.
- `bond_graph_zmatrix(bonds, fragments, edge_map=None, reindex=True, validate_additions=True, required_coordinates=None, isolated_coordinates=None, root_coordinates=None, enforce_requirements=True)` — Construct a Z-matrix spanning a bonded graph, including disconnected or fused fragments.
- `canonical_fragment_zmatrix(canonical_framents, validate_additions=False)` — Join preordered atom fragments into one canonical Z-matrix.
- `sort_complex_attachment_points(fragment_inds, attachment_points)` — Orient and order complex-fragment attachment records into a connected fragment traversal.
- `complex_zmatrix(bonds, fragment_inds=None, fragment_zmats=None, distance_matrix=None, attachment_points=None, check_attachment_points=True, graph=None, reindex=True, required_coordinates=None, isolated_coordinates=None, root_coordinates=None, validate_additions=True)` — Assemble a Z-matrix for multiple disconnected fragments using explicit or distance-derived attachme…
- `graph_backbone_zmatrix(bond_graph, root=None, segments=None, return_remainder=False, return_segments=False, validate=True)` — Create a Z-matrix backbone from chain segments of a connectivity graph.
- `segmented_complex_backbone_zmatrix(bond_graph, fragments=None, segments=None, root=None, attachment_points=None, check_attachment_points=True, validate=True, for_fragment=None, fragment_ordering=None, distance_matrix=None)` — Construct a complex Z-matrix by building graph-based backbones for each disconnected fragment.

### `CoordinateSystems/CartesianToSpherical.py`
  - **class `CartesianToSphericalConverter`** (CoordinateSystemConverter)
    > A converter class for going from Cartesian coordinates to ZMatrix coordinates
    - `types()`
    - `convert_many(coords, use_rad=True, origin=None, axes=None, **kw)` — We'll implement this by having the ordering arg wrap around in coords?
    - `convert(coords, ordering=None, use_rad=True, return_derivs=False, **kw)`

### `CoordinateSystems/CartesianToZMatrix.py`
  - **class `CartesianToZMatrixConverter`** (CoordinateSystemConverter)
    > A converter class for going from Cartesian coordinates to ZMatrix coordinates
    - `types()`
    - `get_dists(points, centers)`
    - `get_angles(lefts, centers, rights)`
    - `get_diheds(points, centers, seconds, thirds)`
    - `convert_many(coords, *, ordering, use_rad=True, return_derivs=False, **kw)` — We'll implement this by having the ordering arg wrap around in coords?
    - `convert(coords, *, ordering, use_rad=True, return_derivs=None, order=None, strip_embedding=False, derivative_method='new', validate=True, **kw)` — The ordering should be specified like:

### `CoordinateSystems/CartesianToZMatrix_opt.py`
  - **class `CartesianToZMatrixConverter`** (CoordinateSystemConverter)
    > A converter class for going from Cartesian coordinates to ZMatrix coordinates
    - `types()`
    - `get_dists(points, centers, return_diffs=False)`
    - `get_angles(lefts, centers, rights, norms=None)`
    - `get_diheds(points, centers, seconds, thirds, crosses=None, norms=None)`
    - `convert_many(coords, ordering=None, use_rad=True, return_derivs=False, **kw)` — We'll implement this by having the ordering arg wrap around in coords?
    - `convert(coords, ordering=None, use_rad=True, return_derivs=False, canonicalize=True, **kw)` — The ordering should be specified like:

### `CoordinateSystems/CommonCoordinateSystems.py`
  - **class `CartesianCoordinateSystem`** (BaseCoordinateSystem)
    > Represents Cartesian coordinates generally
    - `__init__(dimension=None, converter_options=None, coordinate_shape=None, **opts)`
    - `from_state(data, serializer=None)`
  - **class `InternalCoordinateSystem`** (BaseCoordinateSystem)
    > Represents Internal coordinates generally
    - `__init__(dimension=None, coordinate_shape=None, converter_options=None, **opts)`
    - `from_state(data, serializer=None)`
  - **class `CartesianCoordinateSystem1D`** (CartesianCoordinateSystem)
    > Represents Cartesian coordinates in 1D
    - `__init__(converter_options=None, dimension=(None, 1), **opts)`
  - **class `CartesianCoordinateSystem2D`** (CartesianCoordinateSystem)
    > Represents Cartesian coordinates in 2D
    - `__init__(converter_options=None, dimension=(None, 2), **opts)`
  - **class `CartesianCoordinateSystem3D`** (CartesianCoordinateSystem)
    > Represents Cartesian coordinates in 3D
    - `__init__(converter_options=None, dimension=(None, 3), **opts)`
  - **class `ZMatrixCoordinateSystem`** (InternalCoordinateSystem)
    > Represents ZMatrix coordinates generally
    - `__init__(converter_options=None, dimension=(None, None), coordinate_shape=(None, 3), spec=None, **opts)`
    - `jacobian_prep_coordinates(coord, displacements, values, dihedral_cutoff=6)`
    - `to_state(serializer=None)`
    - `canonicalize_order_list(ncoords, order_list)` — Normalizes the way the ZMatrix coordinates are built out
    - `tile_order_list(ol, ncoords)`
    - `ordering()`
    - `spec()`
    - `pre_convert_to(system, opts=None)`
  - **class `SphericalCoordinateSystem`** (BaseCoordinateSystem)
    > Represents Spherical coordinates generally
    - `__init__(converter_options=None, **opts)`

### `CoordinateSystems/CompositeCoordinateSystems.py`
  - **class `CompositeCoordinateSystem`** (CoordinateSystem)
    > Defines a coordinate system that comes from applying a transformation
    > to another coordinate system
    - `__init__(base_system, conversion, inverse_conversion=None, jacobian=None, inverse_jacobian=None, name=None, batched=None, pointwise=True, **opts)`
    - `canonical_name(name, conversion)`
    - `register(base_system, conversion, inverse_conversion=None, name=None, batched=None, pointwise=True, **opts)`
    - `unregister()`
  - **class `CompositeCoordinateSystemConverter`** (CoordinateSystemConverter)
    - `__init__(system, direction='forward')`
    - `types()`
    - `get_conversion()`
    - `convert(coords, **kw)`
    - `convert_many(coords, order=0, derivs=None, return_derivs=None, **kw)`

### `CoordinateSystems/CoordinateSet.py` — Provides a CoordinateSet class that acts as a symbolic extension of np.ndarray to provide an explic…
  - **class `CoordinateSet`** (np.ndarray)
    > A subclass of np.ndarray that lives in an explicit coordinate system and can convert between them
    - `__init__(coords, system=CartesianCoordinates3D, converter_options=None)`
    - `to_state(serializer=None)`
    - `from_state(data, serializer=None)`
    - `multiconfig()` — Determines whether self.coords represents multiple configurations of the coordinates
    - `transform(tf)` — Applies a transformation to the stored coordinates
    - `convert(system, **kw)` — :param system: the target coordinate system
    - `derivatives(function, order=1, coordinates=None, result_shape=None, **fd_options)` — Takes derivatives of `function` with respect to the current geometry
    - `jacobian(system, order=1, coordinates=None, converter_options=None, all_numerical=False, analytic_deriv_order=None, **fd_options)` — Delegates to the jacobian function of the current coordinate system.

### `CoordinateSystems/CoordinateSystem.py`
  - **class `CoordinateSystem`**
    > A representation of a coordinate system. It doesn't do much on its own but it *does* provide a way
    > to unify internal, cartesian, derived type coordinates
    - `__init__(name=None, basis=None, matrix=None, inverse=None, dimension=None, origin=None, coordinate_shape=None, jacobian_prep=None, converter_options=None, registered_converters=None, **extra)`
    - `to_state(serializer=None)`
    - `from_state(data, serializer=None)`
    - `pre_convert(system)` — A hook to allow for handlign details before converting
    - `pre_convert_to(system, opts=None)`
    - `pre_convert_from(system, opts=None)`
    - `basis()` — :return: The basis for the representation of `matrix`
    - `origin()` — :return: The origin for the expansion defined by `matrix`
    - `origin(orig)`
    - `matrix()` — The matrix representation in the `CoordinateSystem.basis`
    - `matrix(mat)`
    - `inverse()` — The inverse of the representation in the `basis`.
    - `inverse(mat)`
    - `dimension()` — The dimension of the coordinate system.
    - `register_converter(system, conversion)`
    - `get_direct_converter(target)`
    - `get_inverse_converter(target)`
    - `preregister_converters()`
    - `deregister_converters()`
    - `converter(system)` — Gets the converter from the current system to a new system
    - **class `_convert_caller`**
      - `__init__(converter, kw, do_many)`
    - `convert_coords(coords, system, converter=None, apply_pre_converter=False, **kw)` — Converts coordiantes from the current coordinate system to _system_
    - `rescale(scaling, in_place=False)`
    - `rotate(rot, in_place=False)`
    - `displacement(amts)` — Generates a displacement or matrix of displacements based on the vector or matrix amts
    - `derivatives(coords, function, order=1, coordinates=None, result_shape=None, **finite_difference_options)` — Computes derivatives for an arbitrary function with respect to this coordinate system.
    - **class `_converter`**
      - `__init__(system, deriv_key, parent, num_derivs, convert_kwargs)`
    - `jacobian(coords, system, order=1, coordinates=None, converter_options=None, all_numerical=False, analytic_deriv_order=None, allow_fd=True, **finite_difference_options)` — Computes the Jacobian between the current coordinate system and a target coordinate system
    - `is_compatible(self, system)`
    - `has_conversion(system)`
  - **class `CoordinateSystemError`** (Exception)
    > An exception that happens inside a `CoordinateSystem` method
  - **class `BaseCoordinateSystem`** (CoordinateSystem)
    > A CoordinateSystem object that can't be reduced further.
    > A common choice might be Cartesian coordinates or internal coordinates.
    > This allows us to define flexible `CoordinateSystem` subclasses that we _don't_ expect to be used as a base
    - `__init__(name, dimension=None, coordinate_shape=None, converter_options=None)`
    - `to_state(serializer=None)`
    - `from_state(data, serializer=None)`

### `CoordinateSystems/CoordinateSystemConverter.py` — Provides the conversion framework between coordinate systems
  - **class `CoordinateSystemConverter`**
    > A base class for type converters
    - `types()` — The types property of a converter returns the types the converter converts
    - `convert_many(coords_list, **kwargs)` — Converts many coordinates.
    - `convert(coords, **kwargs)` — The main necessary implementation method for a converter class.
    - `register(where=None, check=True)` — Registers the CoordinateSystemConverter
    - `deregister(where=None, check=True)` — Registers the CoordinateSystemConverter
  - **class `CoordinateSystemConverters`**
    > A coordinate converter class. It's a singleton so can't be instantiated.
    - `__init__()`
    - `get_coordinates(coordinate_set)` — Extracts coordinates from a coordinate_set
    - `load_converter(converter)`
    - `get_converter(system1, system2)` — Gets the appropriate converter for two CoordinateSystem objects
    - `register_converter(system1, system2, converter, check=True)` — Registers a converter between two coordinate systems
    - `deregister_converter(system1, system2, converter, check=True)` — Registers a converter between two coordinate systems
  - **class `ConversionGraph`**
    > Pulled from the UnitGraph stuff
    - `__init__(stuff_to_update=(), proxy_function=None)`
    - `add(node, connection)`
    - `keys()`
    - `update(iterable)`
    - `find_path_bfs(start, end)`
  - **class `SimpleCoordinateSystemConverter`** (CoordinateSystemConverter)
    - `__init__(types, conversion, **opts)`
    - `types()`
    - `convert(coords, **kw)`
    - `convert_many(coords, **kw)`
  - **class `ChainedCoordinateSystemConverter`** (CoordinateSystemConverter)
    - `__init__(types, conversions, **opts)`
    - `prep_conversions(conv_list)`
    - `types()`
    - `convert(crds, **kwargs)`
    - `convert_many(coords, **kw)`

### `CoordinateSystems/CoordinateUtils.py` — Little utils that both CoordinateSet and CoordinateSystem needed
- `is_multiconfig(coords, coord_shape=None)`
- `mc_safe_apply(fun, coords)` — Applies fun to the coords in such a way that it will apply to an array of valid

### `CoordinateSystems/GenericInternalCoordinateSystem.py`
  - **class `GenericInternalCoordinateSystem`** (InternalCoordinateSystem)
    > Represents ZMatrix coordinates generally
    - `__init__(converter_options=None, dimension=(None,), coordinate_shape=(None,), angle_ordering='ijk', internal_spec=None, **opts)`
    - `pre_convert_to(system, opts=None)`
    - `pre_convert_from(system, opts=None)`
  - **class `CartesianToGICSystemConverter`** (CoordinateSystemConverter)
    > A converter class for going from Cartesian coordinates to internals coordinates
    - `types()`
    - `convert_many(coords, *, specs, order=0, masses=None, remove_translation_rotation=True, reference_coordinates=None, return_derivs=None, derivs=None, gradient_function=None, gradient_scaling=None, method='direct', internal_spec=None, **kw)` — We'll implement this by having the ordering arg wrap around in coords?
    - `convert(coords, *, specs, order=0, **kw)`
  - **class `GICSystemToCartesianConverter`** (CoordinateSystemConverter)
    > A converter class for going from Cartesian coordinates to internals coordinates
    - `types()`
    - `convert_many(coords, *, reference_coordinates, specs, order=0, masses=None, remove_translation_rotation=True, derivs=None, return_derivs=None, internal_spec=None, method='direct', transformations=None, **kw)` — We'll implement this by having the ordering arg wrap around in coords?
    - `convert(coords, *, reference_coordinates, specs, order=0, **kw)`

### `CoordinateSystems/IterativeZMatrixCoordinateSystem.py`
  - **class `IterativeZMatrixCoordinateSystem`** (ZMatrixCoordinateSystem)
    > Represents ZMatrix coordinates generally
    - `__init__(converter_options=None, dimension=(None, None), coordinate_shape=(None, 3), **opts)`
  - **class `CartesianToIZSystemConverter`** (CartesianToZMatrixConverter)
    > A converter class for going from Cartesian coordinates to internals coordinates
    - `types()`
    - `convert_many(coords, *, ordering, use_rad=True, return_derivs=False, **kw)`
  - **class `IZSystemToCartesianConverter`** (CoordinateSystemConverter)
    > A converter class for going from Cartesian coordinates to internals coordinates
    - `types()`
    - `convert_many(coords, *, reference_coordinates, order=0, masses=None, remove_translation_rotation=True, derivs=None, return_derivs=None, ordering=None, origins=None, axes=None, embedding_coords=None, jacobian_prep=None, axes_labels=None, fixed_atoms=None, use_rad=True, **kw)` — We'll implement this by having the ordering arg wrap around in coords?
    - `convert(coords, *, reference_coordinates, specs, order=0, **kw)`

### `CoordinateSystems/SphericalToCartesian.py`
  - **class `SphericalToCartesianConverter`** (CoordinateSystemConverter)
    > A converter class for going from ZMatrix coordinates to Cartesian coordinates
    - `types()`
    - `convert_many(coords, origin=None, axes=None, use_rad=True, **kw)` — Expects to get a list of configurations
    - `convert(coords, **kw)` — dipatches to convert_many but only pulls the first

### `CoordinateSystems/ZMatrixToCartesian.py`
  - **class `ZMatrixToCartesianConverter`** (CoordinateSystemConverter)
    > A converter class for going from ZMatrix coordinates to Cartesian coordinates
    - `types()`
    - `default_ordering(coordlist)`
    - `convert_many(coordlist, *, ordering, origins=None, axes=None, use_rad=True, return_derivs=False, order=None, check_overlapping=False, check_ordering=False, use_direct_expansions=False, orthogonalize_derivatives=True, spec=None, **kw)` — Expects to get a list of configurations
    - `convert(coords, **kw)` — dipatches to convert_many but only pulls the first