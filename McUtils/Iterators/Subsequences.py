from __future__ import annotations

from functools import cache
from typing import Callable, Sequence, Any, NamedTuple
from .. import Devutils as dev

__all__ = [
    "find_overlaps",
    "find_tree_overlaps"
]


Match = tuple[int, int, Any]
Overlap = list[Match]

def _split_contiguous_matches(
    matches: Sequence[Match],
) -> list[Overlap]:
    """
    Divide ordered matches wherever either sequence contains a gap.
    """
    overlaps: list[Overlap] = []

    for match in matches:
        i, j, _ = match

        if (
            not overlaps
            or i != overlaps[-1][-1][0] + 1
            or j != overlaps[-1][-1][1] + 1
        ):
            overlaps.append([])

        overlaps[-1].append(match)

    return overlaps

def find_overlaps(
        s1: Sequence[Any],
        s2: Sequence[Any],
        *,
        equals: Callable[..., bool] | None = None,
        contextual: bool = False,
        require_contiguous=True
) -> list[Overlap]:
    """
    Find a longest common subsequence and divide it into contiguous runs.

    In ordinary mode, ``equals`` has the signature::

        equals(s1_value, s2_value) -> bool

    In contextual mode, it has the signature::

        equals(
            s1_value,
            s2_value,
            previous_s1_value,
            previous_s2_value,
        ) -> bool

    The previous values are ``None`` when testing whether a pair can
    begin a subsequence.

    Contextual mode assumes equality depends only on the immediately
    preceding matched pair, not the entire preceding subsequence.

    Parameters
    ----------
    s1, s2
        Input sequences.
    equals
        Equality or compatibility function.
    contextual
        If true, use the more expensive contextual LCS algorithm.

    Returns
    -------
    list[list[tuple[int, int, Any]]]
        Contiguous runs forming one deterministic longest common
        subsequence.
    """
    if equals is None:
        equals = dev.is_equal

    if contextual:
        matches = _find_contextual_lcs(s1, s2, equals)
    else:
        matches = _find_standard_lcs(s1, s2, equals)

    if require_contiguous:
        matches = _split_contiguous_matches(matches)

    return matches

def _find_standard_lcs(
    s1: Sequence[Any],
    s2: Sequence[Any],
    equals: Callable[[Any, Any], bool],
) -> list[Match]:
    """
    Find one deterministic ordinary longest common subsequence.
    """
    n1 = len(s1)
    n2 = len(s2)

    # dp[i][j] is the LCS length for s1[i:] and s2[j:].
    dp = [
        [0] * (n2 + 1)
        for _ in range(n1 + 1)
    ]

    for i in range(n1 - 1, -1, -1):
        for j in range(n2 - 1, -1, -1):
            if equals(s1[i], s2[j]):
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(
                    dp[i + 1][j],
                    dp[i][j + 1],
                )

    matches: list[Match] = []
    i = j = 0

    while i < n1 and j < n2:
        if (
            equals(s1[i], s2[j])
            and dp[i][j] == 1 + dp[i + 1][j + 1]
        ):
            matches.append((i, j, s1[i]))
            i += 1
            j += 1

        elif dp[i + 1][j] >= dp[i][j + 1]:
            i += 1

        else:
            j += 1

    return matches

def _find_contextual_lcs(
    s1: Sequence[Any],
    s2: Sequence[Any],
    equals: Callable[
        [Any, Any, Any | None, Any | None],
        bool,
    ],
) -> list[Match]:
    """
    Find an LCS whose compatibility depends on the previous matched pair.

    This is a longest-path calculation over the ordered index-pair DAG.
    """
    n1 = len(s1)
    n2 = len(s2)

    if n1 == 0 or n2 == 0:
        return []

    # lengths[i][j] is the longest valid subsequence ending with
    # the pair (s1[i], s2[j]). Zero means that pair cannot be used.
    lengths = [
        [0] * n2
        for _ in range(n1)
    ]

    predecessors: list[list[tuple[int, int] | None]] = [
        [None] * n2
        for _ in range(n1)
    ]

    best_length = 0
    best_end: tuple[int, int] | None = None

    for i in range(n1):
        for j in range(n2):
            # Determine whether this pair can begin a subsequence.
            if equals(s1[i], s2[j], None, None):
                lengths[i][j] = 1

            # Try every ordered earlier matched pair as a predecessor.
            for previous_i in range(i):
                for previous_j in range(j):
                    previous_length = lengths[previous_i][previous_j]

                    if previous_length == 0:
                        continue

                    if not equals(
                        s1[i],
                        s2[j],
                        s1[previous_i],
                        s2[previous_j],
                    ):
                        continue

                    candidate_length = previous_length + 1

                    if candidate_length > lengths[i][j]:
                        lengths[i][j] = candidate_length
                        predecessors[i][j] = (
                            previous_i,
                            previous_j,
                        )

            # Strict comparison preserves the earliest endpoint when
            # multiple solutions have the same length.
            if lengths[i][j] > best_length:
                best_length = lengths[i][j]
                best_end = (i, j)

    if best_end is None:
        return []

    # Follow predecessor links backward.
    index_pairs: list[tuple[int, int]] = []
    current: tuple[int, int] | None = best_end

    while current is not None:
        i, j = current
        index_pairs.append(current)
        current = predecessors[i][j]

    index_pairs.reverse()

    return [
        (i, j, s1[i])
        for i, j in index_pairs
    ]

class RootedAlternative(NamedTuple):
    root1: int
    root2: int
    score: int
    matches: tuple[Match, ...]

def find_tree_overlaps(
        s1: Sequence[Any],
        s2: Sequence[Any],
        antecedents1: Sequence[int | None],
        antecedents2: Sequence[int | None],
        *,
        equals: Callable[
            [Any, Any, Any | None, Any | None],
            bool,
        ],
        nparents=1,
        require_contiguous=True,
        mode="best_forest",
        maximal_only=True,
):
    """
    Parameters
    ----------
    mode
        ``"best_tree"``:
            Return one highest-scoring rooted match.

        ``"best_forest"``:
            Return one highest-scoring collection of compatible,
            nonnested rooted matches.

        ``"root_alternatives"``:
            Return the best rooted match for every possible root pair.

    maximal_only
        In ``"root_alternatives"`` mode, remove alternatives whose
        complete match set is strictly contained in another alternative.
    """
    n1 = len(s1)
    n2 = len(s2)

    if len(antecedents1) != n1:
        raise ValueError("antecedents1 must have the same length as s1")
    if len(antecedents2) != n2:
        raise ValueError("antecedents2 must have the same length as s2")

    children1 = _make_child_lists(antecedents1)
    children2 = _make_child_lists(antecedents2)

    subtree_ends1 = _find_subtree_ends(children1)
    subtree_ends2 = _find_subtree_ends(children2)

    @cache
    def internal_score(i: int, j: int) -> int:
        """
        Score `(i, j)` when reached through its actual parent pair.
        """
        i0 = i
        parents1 = []
        for _ in range(nparents):
            parent1 = antecedents1[i0]
            if parent1 is None: break
            parents1.append(parent1)
            i0 = parent1
        parents1 = parents1[::-1]

        j0 = j
        parents2 = []
        for _ in range(nparents):
            parent2 = antecedents2[j0]
            if parent2 is None: break
            parents2.append(parent2)
            j0 = parent2
        parents2 = parents2[::-1]

        if not equals(
            s1[i],
            s2[j],
            [s1[p] for p in parents1],
            [s2[p] for p in parents2]
        ):
            return 0

        return subtree_score(i, j)

    @cache
    def subtree_score(i: int, j: int) -> int:
        """
        Score below an already accepted root pair `(i, j)`.
        """
        return 1 + child_alignment_score(i, j)

    @cache
    def child_alignment_score(i: int, j: int) -> int:
        """
        Weighted LCS score between the ordered child lists of `(i, j)`.
        """

        #TODO: track entire parent trunk rather than rebuilding at each step
        left_children = children1[i]
        right_children = children2[j]

        n_left = len(left_children)
        n_right = len(right_children)

        dp = [
            [0] * (n_right + 1)
            for _ in range(n_left + 1)
        ]

        for a in range(n_left - 1, -1, -1):
            child1 = left_children[a]

            for b in range(n_right - 1, -1, -1):
                child2 = right_children[b]
                matched_score = internal_score(child1, child2)

                if matched_score:
                    use_match = (
                        matched_score
                        + dp[a + 1][b + 1]
                    )
                else:
                    use_match = 0

                dp[a][b] = max(
                    use_match,
                    dp[a + 1][b],
                    dp[a][b + 1],
                )

        return dp[0][0]

    def reconstruct_subtree(
        i: int,
        j: int,
        matches: list[Match],
    ) -> None:
        matches.append((i, j, s1[i]))

        left_children = children1[i]
        right_children = children2[j]

        n_left = len(left_children)
        n_right = len(right_children)

        dp = [
            [0] * (n_right + 1)
            for _ in range(n_left + 1)
        ]

        for a in range(n_left - 1, -1, -1):
            child1 = left_children[a]

            for b in range(n_right - 1, -1, -1):
                child2 = right_children[b]
                matched_score = internal_score(child1, child2)

                use_match = (
                    matched_score + dp[a + 1][b + 1]
                    if matched_score
                    else 0
                )

                dp[a][b] = max(
                    use_match,
                    dp[a + 1][b],
                    dp[a][b + 1],
                )

        # Reconstruct the weighted child LCS.
        a = b = 0

        while a < n_left and b < n_right:
            child1 = left_children[a]
            child2 = right_children[b]
            matched_score = internal_score(child1, child2)

            use_match = (
                matched_score + dp[a + 1][b + 1]
                if matched_score
                else 0
            )

            # Prefer a match when multiple choices have equal scores.
            if matched_score and use_match == dp[a][b]:
                reconstruct_subtree(
                    child1,
                    child2,
                    matches,
                )
                a += 1
                b += 1

            elif dp[a + 1][b] >= dp[a][b + 1]:
                a += 1

            else:
                b += 1

    # Test every pair as an independently chosen starting root.
    best_root: tuple[int, int] | None = None
    best_score = 0

    for i in range(n1):
        for j in range(n2):
            if not equals(s1[i], s2[j], [], []):
                continue

            score = subtree_score(i, j)

            if score > best_score:
                best_score = score
                best_root = (i, j)

    if best_root is None:
        return []

    matches: list[Match] = []
    reconstruct_subtree(*best_root, matches)

    # Calculate the score of treating every pair as an independent root.
    root_scores = [
        [0] * n2
        for _ in range(n1)
    ]

    for i in range(n1):
        for j in range(n2):
            if equals(s1[i], s2[j], [], []):
                root_scores[i][j] = subtree_score(i, j)

    if mode == 'best_tree':
        best_score = 0
        best_root: tuple[int, int] | None = None

        for i in range(n1):
            for j in range(n2):
                if root_scores[i][j] > best_score:
                    best_score = root_scores[i][j]
                    best_root = (i, j)

        if best_root is None:
            return []

        matches: list[Match] = []
        reconstruct_subtree(*best_root, matches)
        if require_contiguous:
            matches = _split_contiguous_matches(matches)
        return matches
    elif mode == "root_alternatives":
        alternatives: list[RootedAlternative] = []

        for i in range(n1):
            for j in range(n2):
                score = root_scores[i][j]

                if not score:
                    continue

                matches: list[Match] = []
                reconstruct_subtree(i, j, matches)

                alternatives.append(
                    RootedAlternative(
                        root1=i,
                        root2=j,
                        score=score,
                        matches=tuple(matches),
                    )
                )

        if maximal_only:
            alternatives = _remove_contained_alternatives(
                alternatives
            )

        # Highest-scoring alternatives first, then deterministic root
        # ordering.
        alternatives.sort(
            key=lambda alternative: (
                -alternative.score,
                alternative.root1,
                alternative.root2,
            )
        )

        if require_contiguous:
            alternatives = [
                a._replace(matches=_split_contiguous_matches(a.matches))
                for a in alternatives
            ]

        return alternatives
    elif mode == 'best_forest':
        # dp[i][j] is the best forest score beginning at or after positions
        # i and j in the two preorder streams.
        dp = [
            [0] * (n2 + 1)
            for _ in range(n1 + 1)
        ]

        for i in range(n1 - 1, -1, -1):
            for j in range(n2 - 1, -1, -1):
                root_score = root_scores[i][j]

                if root_score:
                    use_root = (
                            root_score
                            + dp[subtree_ends1[i]][subtree_ends2[j]]
                    )
                else:
                    use_root = 0

                dp[i][j] = max(
                    use_root,
                    dp[i + 1][j],
                    dp[i][j + 1],
                )

        # Reconstruct the selected disjoint rooted subtree matches.
        rooted_matches: list[list[Match]] = []
        i = j = 0

        while i < n1 and j < n2:
            root_score = root_scores[i][j]

            if root_score:
                use_root = (
                        root_score
                        + dp[subtree_ends1[i]][subtree_ends2[j]]
                )
            else:
                use_root = 0

            # Prefer selecting a root when multiple choices have equal scores.
            if root_score and use_root == dp[i][j]:
                matches: list[Match] = []
                reconstruct_subtree(i, j, matches)
                rooted_matches.append(matches)

                # Skip the complete source subtrees. This prevents a later
                # selected root from being contained in either selected tree.
                i = subtree_ends1[i]
                j = subtree_ends2[j]

            elif dp[i + 1][j] >= dp[i][j + 1]:
                i += 1

            else:
                j += 1

        # Preserve rooted-subtree boundaries while also dividing each root
        # match at gaps in either preorder sequence.
        return [
            overlap
            for matches in rooted_matches
            for overlap in (
                _split_contiguous_matches(matches)
                    if require_contiguous else
                matches
            )
        ]
    else:
        raise ValueError(
            "mode must be 'best_tree', 'best_forest', "
            "or 'root_alternatives'"
        )

def _make_child_lists(
    antecedents: Sequence[int | None],
) -> tuple[tuple[int, ...], ...]:
    """
    Convert direct-parent indices into ordered child lists.
    """
    children = [
        []
        for _ in antecedents
    ]

    for child, parent in enumerate(antecedents):
        if parent is None:
            continue

        if not 0 <= parent < len(antecedents):
            raise ValueError(
                f"invalid antecedent {parent} for node {child}"
            )

        if parent >= child:
            raise ValueError(
                "nodes must follow their antecedents in preorder: "
                f"node {child} has antecedent {parent}"
            )

        children[parent].append(child)

    return tuple(
        tuple(child_list)
        for child_list in children
    )

def _find_subtree_ends(
    children: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    """
    Return the exclusive preorder end index of every rooted subtree.

    For a node `i`, its full rooted subtree occupies:

        [i, subtree_ends[i])

    The input must represent a preorder traversal.
    """
    ends = [i + 1 for i in range(len(children))]

    def find_end(node: int) -> int:
        end = node + 1

        for child in children[node]:
            child_end = find_end(child)

            # In a valid preorder traversal, the next child begins after
            # the preceding child's complete subtree.
            if child < end:
                raise ValueError(
                    "antecedents do not describe a valid preorder traversal"
                )

            end = child_end

        ends[node] = end
        return end

    child_nodes = {
        child
        for child_list in children
        for child in child_list
    }

    roots = [
        node
        for node in range(len(children))
        if node not in child_nodes
    ]

    for root in roots:
        find_end(root)

    return tuple(ends)

def _remove_contained_alternatives(
    alternatives: list[RootedAlternative],
) -> list[RootedAlternative]:
    """
    Remove a rooted alternative if all of its index-pair matches are
    strictly contained in another alternative.
    """
    match_sets = [
        frozenset(
            (i, j)
            for i, j, _ in alternative.matches
        )
        for alternative in alternatives
    ]

    keep = []

    for index, current in enumerate(match_sets):
        contained = any(
            current < other
            for other_index, other in enumerate(match_sets)
            if other_index != index
        )

        if not contained:
            keep.append(alternatives[index])

    return keep