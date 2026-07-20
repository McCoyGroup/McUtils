### `Permutations.py` — Utilities for working with permutations and permutation indexing
- `lehmer_encode(perms, dtype=None)` — Encode permutations as their Lehmer-code integers (a factorial-base ranking),
- `lehmer_decode(ndim, codes, dtype=None)` — Decode Lehmer-code integers back into their permutations (the inverse of
  - **class `IntegerPartitioner`**
    - `__init__()`
    - `count_partitions(n, M=None, l=None, manage_counts=True, check=True)` — Uses the recurrence relation written out here
    - `fill_counts(n, M=None, l=None)` — Fills all counts up to (n, M, l)
    - `count_exact_length_partitions(n, M, l, check=True)` — Unexpectedly common thing to want and a non-obvious formula
    - `count_exact_length_partitions_in_range(n, m, M, l, check=True)` — Returns the partitions with  k > M but length exactly L
    - `partitions(n, pad=False, return_lens=False, max_len=None, dtype=None)` — Returns partitions in descending lexicographic order
    - `partition_indices(parts, sums=None, counts=None, check=True)` — Provides a somewhat quick way to get the index of a set of
  - **class `UniqueSubsets`**
    > Provides unique subsets for an integer partition
    - `num_unique_subsets(k, partition)` — Count the number of ways to split `k` symbols into ordered blocks of the given
    - `unique_subsets(partition)` — Enumerate every way to partition `sum(partition)` symbols into ordered blocks of
  - **class `UniquePermutations`**
    > Provides permutations for a _single_ integer partition (very important)
    > Also provides a classmethod interface to support the case
    > where we don't want to instantiate a permutations object for every partition
    - `__init__(partition)`
    - `get_permutation_class_counts(partition, sort_by_counts=False)` — Return the distinct values of a partition and their multiplicities, sorted by
    - `num_permutations()` — Counts the number of unique permutations of the partition
    - `get_binoms(n)` — Return the cached `Binomial` table, (re)building it if it isn't large enough for
    - `count_permutations(counts)` — Counts the number of unique permutations of the given "counts"
    - `permutations(initial_permutation=None, return_indices=False, num_perms=None, position_blocks=None)` — Returns the permutations of the input array
    - `get_subsequent_permutations(initial_permutation, return_indices=False, classes=None, counts=None, num_perms=None)` — Returns the permutations of the input array
    - `index_permutations(perms, assume_sorted=False, preserve_ordering=True)` — Gets permutations indices assuming all the data matches the held stuff
    - `get_next_permutation_from_prev(classes, counts, class_map, ndim, cur, prev, prev_index, prev_dim, subtree_counts)` — Pulls the next index by reusing as much info as possible from
    - `get_permutation_indices(perms, classes=None, counts=None, assume_sorted=False, preserve_ordering=True, dim=None, num_permutations=None, dtype=None, block_size=100)` — Classmethod interface to get indices for permutations
    - `get_permutations_from_indices(classes, counts, indices, assume_sorted=False, preserve_ordering=True, dim=None, num_permutations=None, check_indices=True, no_backtracking=False, block_size=100)` — Classmethod interface to get permutations given a set of indices
    - `permutations_from_indices(indices, assume_sorted=False, preserve_ordering=True)` — Gets permutations indices assuming all the data matches the held stuff
    - `get_standard_permutation(counts, classes)` — Build the canonical (sorted, descending) representative permutation for a set of
    - `walk_permutation_tree(counts, on_visit, indices=None, dim=None, num_permutations=None, include_positions=False)` — Just a general purpose method that allows us to walk the permutation
    - `descend_permutation_tree_indices(perms, on_visit, classes=None, counts=None, dim=None, assume_sorted=False, num_permutations=None)` — Not sure what to call this exactly, but given that `walk_permutation_tree` maps onto `permutations_…
  - **class `IntegerPartitioner2D`**
    > Provides a tree-based approach to obtain the different integer partitions possible
    > when n balls are divided into different numbers of boxes
    - `get_partitions(boxes, balls)` — Enumerate all ways to distribute `balls` into `boxes` (a 2-D integer partition /
  - **class `UniquePartitions`**
    > Takes partitions of a set of ints with ordering
    - `__init__(partition)`
    - `partitions(sizes, take_unique=True, split=True, return_partitions=True, return_indices=False, split_indices=None, return_inverse=False, split_inverse=None)` — Enumerate the ways to split this multiset into blocks of the given sizes (a
  - **class `IntegerPartitionPermutations`**
    > Provides tools for working with permutations of a given integer partition
    - `__init__(num, dim=None)`
    - `num_elements()` — The total number of partition permutations in the space.
    - `get_partition_permutations(return_indices=False, dtype=None, flatten=False)` — :return:
    - `get_full_equivalence_class_data(perms, split_method='direct', assume_sorted=False, assume_standard=False, return_permutations=False, check_partition_counts=True)` — Returns the equivalence class data of the given permutations
    - `get_equivalence_classes(perms, split_method='direct', assume_sorted=False, return_permutations=True, check_partition_counts=True)` — Returns the equivalence classes and permutations of the given permutations
    - `get_partition_permutation_indices(perms, assume_sorted=False, preserve_ordering=True, assume_standard=False, check_partition_counts=True, dtype=None, split_method='direct')` — Assumes the perms all add up to the stored int
    - `get_partition_permutations_from_indices(indices, assume_sorted=False, preserve_ordering=True)` — Assumes the perms all add up to the stored int
  - **class `EmptyIntegerPartitionPermutations`** (IntegerPartitionPermutations)
    - `__init__(num, dim=None)`
    - `get_partition_permutations(return_indices=False, dtype=None)` — :return:
    - `get_partition_permutation_indices(perms, assume_sorted=None, preserve_ordering=None, assume_standard=None, check_partition_counts=None, dtype=None, split_method=None)` — :param perms:
    - `get_partition_permutations_from_indices(indices, assume_sorted=None, preserve_ordering=None)` — :param indices:
  - **class `SymmetricGroupGenerator`**
    > I don't know what to call this.
    > Manages elements of the symmetric group up to arbitrary size.
    > Basically just exists to merge all of the prior integer partition/permutation stuff over many integers
    > which makes it easier to calculate direct products of terms
    - `__init__(dim)`
    - `load_to_size(size)` — Generate partition permutations until the cumulative element count covers `size`.
    - `get_terms(n, flatten=True)` — Returns permutations of partitions
    - `num_terms(n)` — Return the number of partition permutations at each requested integer sum.
    - `to_indices(perms, sums=None, assume_sorted=False, assume_standard=False, check_partition_counts=True, preserve_ordering=True, dtype=None)` — Gets the indices for the given permutations.
    - `from_indices(indices, assume_sorted=False, preserve_ordering=True)` — Gets the permutations for the given indices.
    - **class `direct_sum_filter`**
      - `__init__(perms, inds)`
      - `from_perms(parent, filter_perms)` — Build a filter from a set of permutations, resolving them to indices via the
      - `from_inds(inds)` — Build a filter directly from a set of indices (no permutations).
      - `from_data(parent, filter_perms)` — Build a filter from flexible input (an existing filter, permutations, indices, or
    - `changed_index_number(idx, radix)` — Encode a set of changed positions as a single mixed-radix integer (a canonical id
    - `get_equivalence_classes(perms, sums=None, assume_sorted=False)` — Gets permutation equivalence classes
    - `take_permutation_rule_direct_sum(perms, rules, sums=None, assume_sorted=False, return_indices=False, return_excitations=True, return_change_positions=False, full_basis=None, split_results=False, excluded_permutations=None, filter_perms=None, filter_negatives=True, return_filter=False, preserve_ordering=True, indexing_method='direct', logger=None)` — Naively this is just taking every possible permutation of the rules padded to
  - **class `CompleteSymmetricGroupSpace`**
    > An object representing a full integer partition-permutation basis
    > which will work nominally at any level of excitation
    - `__init__(dim, memory_constrained=False)`
    - `dim()` — **LLM Docstring**
    - `load_to_size(size)` — Materialize the basis until it holds at least `size` permutations (a no-op when
    - `load_to_sum(max_sum)` — Materialize the basis to cover every permutation with sum up to `max_sum`.
    - `take(item, uncoerce=False, max_size=None)` — Return the permutation(s) at the given index/indices, loading the basis as needed
    - `find(perms, check_sums=True, max_sum=None, search_space_sorting=None)` — Return the indices of the given permutations in the space, pre-screening by
  - **class `LatticePathGenerator`**
    > An object to take direct products of lattice paths and
    > filter them
    - `__init__(*steps, max_len=None)`
    - `subtrees()` — The per-depth lattice-path subtrees (position-tracking), generated lazily.
    - `tree()` — The final (full-depth) lattice-path tree with positions, generated lazily.
    - `subrules()` — The per-depth lattice-path rule trees (without position tracking), generated
    - `rules()` — The final (full-depth) lattice-path rule tree, generated lazily.
    - `generate_tree(rules, max_len=None, track_positions=True)` — We take the combo of the specified rules, where we take successive products of 1D rules with the
    - `find_paths(end_spots)` — Return the starting steps of every lattice path that reaches one of the given end
    - `get_path(path)` — Pulls the places one can end up after applying the path
    - `find_intersections(other)` — Finds the paths that will make self intersect with other
  - **class `PermutationRelationGraph`**
    > Takes permutations and a set of relations and builds a graph from
    > them
    - `__init__(relations)`
    - `merge_groups(groups)` — This really needs to be cleaned up...
    - `make_relation_graph(relations)` — :param relations:
    - `apply_rels(states, max_sum=None)` — For each state checks if it is divisible by one of the group rules and if so applies the
    - `build_state_graph(states, max_sum=None, extra_groups=None, max_iterations=10, raise_iteration_error=True)` — :param states:

### `Sequences.py` — Sequences lifted from finite difference weight calculation in
- `StirlingS1(n)` — Computes the Stirling numbers
- `Binomial(n, dtype=None)` — binomial coefficients up to binom(n, n)
- `GammaBinomial(s, n)` — Generalized binomial gamma function
- `Factorial(n)` — I was hoping to do this in some built in way with numpy...but I guess it's not possible?
- `prime_sieve(ints, k, max_its=None)` — Remove repeated factors of `k` from one or more integers.
- `prime_iter(primes=None)` — Yield progressively longer lists of prime numbers.
- `prime_list(n, base_primes=[], piter=prime_iter())` — Return the first `n` primes using a shared incremental cache.
- `prime_factorize(ints, primes=None)` — Compute prime-exponent arrays for one or more positive integers.
- `stable_factorial_ratio(num_terms, denom_terms, counts=None)` — Evaluate a ratio of products using prime exponents.
- `halton_sequence(N, d, start=1)` — First N points of the d-dimensional Halton sequence, one prime base
- `sobol_sequence(N, d, n_bits=30)` — First N points of the d-dimensional Sobol sequence (Bratley-Fox

### `YoungTableaux.py`
  - **class `YoungTableauxGenerator`**
    - `__init__(base_int, tableaxu_cache=None, subset_cache=None)`
    - `number_of_tableaux(partitions=None, **partition_opts)` — Count standard Young tableaux over one or more partitions of the instance base.
    - `get_standard_tableaux(partitions=None, *, symbols=None, brute_force=False, return_partitions=False, **partition_opts)` — Generate standard Young tableaux for selected partitions.
    - `standard_partition_tableaux_bf(partition, unique_perms=False, concatenate=False)` — Enumerate tableaux for a partition by brute-force permutation filtering.
    - `populate_sst_frames(partition, frame, segment_lists)` — Fill tableau frame shapes from segmented symbol selections.
    - `standard_partitions(partition)` — Generate valid two-dimensional partition frames and cumulative offsets.
    - `hook_numbers(partition)` — Compute hook lengths for every cell of a Young diagram.
    - `count_standard_tableaux(partition)` — Count standard tableaux using the hook-length formula.
    - `split_frame(partition, offsets)` — Split a partition frame into one-row components with aligned offsets.
    - `standard_partition_tableaux(partition, cache=None, subset_cache=None, symbols=None, brute_force=False)` — Generate all standard tableaux for a single partition.
    - `print_tableaux(tableaux)` — Format and print one or more tableau collections.