

__all__ = [
    "merge_sets"
]


def merge_sets(iterable):
    """
    **LLM Docstring**

    Merge an iterable of sets into transitive connected components under nonempty intersection.

    :param iterable: Sets or set-like iterables to merge by transitive overlap.
    :type iterable: object

    :return: A list of pairwise-disjoint merged sets.
    :rtype: list
    """
    groups:list[set] = []
    for s in iterable:
        s = set(s)
        for g in groups:
            if len(s.intersection(g)) > 0:
                g.update(s)
                break
        else:
            groups.append(s)

    skipped = [False]*len(groups)
    final = []
    for n,g in enumerate(groups):
        if skipped[n]: continue
        for m,g1 in enumerate(groups[n:]):
            j = n + m
            if skipped[j]: continue
            if len(g1.intersection(g)) > 0:
                g.update(g1)
                skipped[j] = True
        final.append(g)
    return final

