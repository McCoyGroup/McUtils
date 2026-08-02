from __future__ import annotations

from typing import Callable, Sequence, TypeAlias, Any
from .. import Devutils as dev

__all__ = [
    "find_overlaps"
]


Match: TypeAlias = tuple[int, int, Any]
Overlap: TypeAlias = list[Match]
def find_overlaps(
        s1: Sequence[Any],
        s2: Sequence[Any],
        *,
        rel_tol: float = 1e-9,
        abs_tol: float = 1e-12,
        equals: Callable[[Any, Any], bool] | None = None,
) -> list[Overlap]:
    """
    Find a longest common subsequence of `s1` and `s2`, then divide it
    into contiguous overlap blocks.

    Each returned match is `(index_in_s1, index_in_s2, entry_from_s1)`.
    Consecutive matches belong to the same block only when their indices
    are consecutive in both input sequences.

    Parameters
    ----------
    s1, s2
        Sequences containing `(element, r, a, d)` quadruples.
    rel_tol, abs_tol
        Tolerances used to compare the three floating-point values.
    equals
        Optional custom equality function. When supplied, it replaces
        the default element-and-numerical-tolerance comparison.

    Returns
    -------
    list[list[tuple[int, int, Entry]]]
        The disjoint contiguous blocks forming one longest common
        subsequence.
    """
    if equals is None:
        equals = dev.is_equal

    n1, n2 = len(s1), len(s2)

    # dp[i][j] is the LCS length for s1[i:] and s2[j:].
    dp = [[0] * (n2 + 1) for _ in range(n1 + 1)]

    for i in range(n1 - 1, -1, -1):
        for j in range(n2 - 1, -1, -1):
            if equals(s1[i], s2[j]):
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])

    # Reconstruct one deterministic LCS.
    matches: list[Match] = []
    i = j = 0

    while i < n1 and j < n2:
        if equals(s1[i], s2[j]) and dp[i][j] == 1 + dp[i + 1][j + 1]:
            matches.append((i, j, s1[i]))
            i += 1
            j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            i += 1
        else:
            j += 1

    # Split the LCS wherever either sequence contains an intervening gap.
    overlaps: list[Overlap] = []

    for match in matches:
        if (
            not overlaps
            or match[0] != overlaps[-1][-1][0] + 1
            or match[1] != overlaps[-1][-1][1] + 1
        ):
            overlaps.append([])

        overlaps[-1].append(match)

    return overlaps