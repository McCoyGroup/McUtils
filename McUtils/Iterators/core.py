import collections
import itertools
import numbers

__all__ = [
    "is_fixed_size",
    "consume",
    "chunked",
    "take_lists",
    "split",
    "split_by",
    "counts",
    "dict_diff",
    "transpose",
    "riffle",
    "flatten",
    "first",
    "delete_duplicates",
    "unique_product",
    "zigzag_product"
]

def is_fixed_size(iterable):
    """
    **LLM Docstring**

    Check whether an iterable exposes a `__len__` attribute.

    This is a structural check only; it does not call `len` or verify that indexing or slicing is supported.

    :param iterable: Object to inspect.
    :type iterable: object
    :return: `True` when the object has a `__len__` attribute.
    :rtype: bool
    """
    return hasattr(iterable, '__len__')

def consume(iterable, n, return_values=True):
    """
    **LLM Docstring**

    Advance an iterable by at most `n` items.

    When `return_values` is true, the consumed items are materialized in a list. Otherwise the function advances through the first `n` items using `islice` and returns `None`.

    :param iterable: Iterable or iterator to consume.
    :type iterable: collections.abc.Iterable
    :param n: Maximum number of items to consume.
    :type n: int
    :param return_values: Whether to return the consumed items.
    :type return_values: bool
    :return: A list of consumed values, or `None` when values are discarded.
    :rtype: list | None
    """
    if return_values:
        return list(itertools.islice(iterable, n))
    else:
        return next(itertools.islice(iterable, n, n), None)

def chunked(a, upto):
    """
    **LLM Docstring**

    Yield consecutive chunks from a fixed-size, sliceable object.

    For objects with `__len__`, the function slices blocks of at most `upto` items.
    The non-fixed-size branch defines a consumer and yields chunks of a given size

    :param a: Sequence or iterable to divide into chunks.
    :type a: collections.abc.Iterable
    :param upto: Maximum chunk size.
    :type upto: int
    :return: Iterator over sequence slices for fixed-size inputs.
    :rtype: collections.abc.Iterator
    """
    if is_fixed_size(a):
        l = len(a)
        blocks = (l // upto) +  (0 if (l % upto) == 0 else 1)
        for i in range(blocks):
            yield a[i*upto:(i+1)*upto]
    else:
        def consumer(a=a):
            """
            **LLM Docstring**

            Read the next chunk from the enclosing iterator.

            The closure consumes up to `upto` values from `a` and materializes them as a list. It is intended for use with the two-argument form of `iter`.

            :return: The next list of up to `upto` items, or an empty list at exhaustion.
            :rtype: list
            """
            return list(itertools.islice(a, upto))
        yield from iter(consumer, [])

def split(a, test=None):
    """
    **LLM Docstring**

    Split an iterable whenever adjacent values satisfy a boundary test.

    For non-fixed iterables, the function tees the input, compares successive values, and yields materialized groups; when `test` is omitted it splits when adjacent values differ. The fixed-size branch directly uses slicing, but its loop is written as `for i, b in a[1]` rather than enumerating `a[1:]`, and it calls `test` without installing the default, so that branch only works for unusually shaped inputs matching that unpacking behavior.

    :param a: Iterable to partition.
    :type a: collections.abc.Iterable
    :param test: Predicate receiving `(next_value, previous_group_value)` and returning true at a split boundary.
    :type test: callable | None
    :return: Iterator over contiguous groups.
    :rtype: collections.abc.Iterator
    """
    if is_fixed_size(a):
        prev = a[0]
        sep = 0
        for i, b in a[1]:
            if test(b, prev):
                yield a[sep:i+1]
                sep = i
                prev = b
    else:
        a, t = itertools.tee(a, 2)
        prev = next(t)
        sep = -1
        i = -1
        if test is None:
            test = lambda x,y: x != y
        for i, b in enumerate(t):
            if test(b, prev):
                yield consume(a, i + 1 - sep)
                sep = i
                prev = b
        yield consume(a, i + 1 - sep)

def split_by(a, canonicalizer):
    """
    **LLM Docstring**

    Split values when the result of a canonicalization function changes.

    The returned generator is produced by `split` with a stateful comparison closure. The closure stores its cache in a default list, so that cache object is shared across calls to this function, although its first-call flag is reset only when the closure is initially created.

    :param a: Iterable to partition.
    :type a: collections.abc.Iterable
    :param canonicalizer: Function mapping each value to its grouping key.
    :type canonicalizer: callable
    :return: Iterator over contiguous groups with equal canonical keys.
    :rtype: collections.abc.Iterator
    """
    def test(next, prev, canonicalizer=canonicalizer, cache=[True, None]):
        """
        **LLM Docstring**

        Compare canonical keys for two adjacent values.

        On its first invocation the closure canonicalizes `prev`, then canonicalizes `next`, reports whether the keys differ, and updates its cached key to the new value.

        :param next: Candidate value for the next group.
        :type next: object
        :param prev: Previous value, used to initialize the cache on the first call.
        :type prev: object
        :param canonicalizer: Function converting values to comparison keys.
        :type canonicalizer: callable
        :param cache: Mutable two-element state containing an initialization flag and the previous key.
        :type cache: list
        :return: Whether the canonicalized value changed.
        :rtype: bool
        """
        if cache[0]:
            cache[1] = canonicalizer(prev)
        new = canonicalizer(next)
        ret = new != cache[1]
        cache[1] = new
        return ret
    return split(a, test)

def take_lists(a, splits):
    """
    **LLM Docstring**

    Partition an iterable according to a sequence of requested lengths.

    Fixed-size inputs are sliced without copying where the input type supports that operation. After the requested lengths, a trailing slice is yielded only when `sep < len(a) - 1`, which omits a remainder containing exactly one item. Streaming inputs yield one materialized list per requested size and do not emit any unspecified remainder.

    :param a: Sequence or iterator to partition.
    :type a: collections.abc.Iterable
    :param splits: Requested chunk lengths.
    :type splits: collections.abc.Iterable[int]
    :return: Iterator over slices or consumed lists.
    :rtype: collections.abc.Iterator
    """
    if is_fixed_size(a):
        sep = 0
        for s in splits:
            new = sep + s
            yield a[sep:new]
            sep = new
        if sep < len(a) - 1:
            yield a[sep:]
    else:
        for s in splits:
            yield consume(a, s)
def counts(iterable, test=None, hashable=True):
    """
    **LLM Docstring**

    Count values after optionally mapping them through a key function.

    With `hashable=True`, results are returned as a dictionary keyed by transformed values. With `hashable=False`, linear equality lookup is used and parallel lists of keys and counts are returned, allowing unhashable keys.

    :param iterable: Values to count.
    :type iterable: collections.abc.Iterable
    :param test: Optional key-producing function; identity is used when omitted.
    :type test: callable | None
    :param hashable: Whether transformed keys can be stored in a dictionary.
    :type hashable: bool
    :return: A frequency dictionary, or `(keys, counts)` lists for unhashable keys.
    :rtype: dict | tuple[list, list]
    """
    if test is None: test = lambda x:x
    if hashable:
        counts_dict = {}
        for v in iterable:
            k = test(v)
            counts_dict[k] = counts_dict.get(k, 0) + 1
        return counts_dict
    else:
        keys = []
        counts = []
        for v in iterable:
            k = test(v)
            try:
                i = keys.index(k)
            except ValueError:
                keys.append(k)
                counts.append(1)
            else:
                counts[i] += 1

        return keys, counts

def dict_diff(iterable1:dict, iterable2):
    """
    **LLM Docstring**

    Build the asymmetric value difference between two mappings.

    The result contains entries from `iterable1` whose key is absent from `iterable2` or whose value differs, plus entries whose keys occur only in `iterable2`. For differing shared keys, the value from `iterable1` is retained.

    :param iterable1: Primary mapping whose changed values take precedence.
    :type iterable1: dict
    :param iterable2: Mapping to compare against.
    :type iterable2: collections.abc.Mapping
    :return: Dictionary containing changed and one-sided entries.
    :rtype: dict
    """
    return {
        k:v
        for k,v in iterable1.items()
        if k not in iterable2 or v != iterable2[k]
    } | {k:iterable2[k] for k in iterable2.keys() - iterable1.keys()}

def transpose_iter(data, default=None):
    """
    **LLM Docstring**

    Transpose a collection of iterators while padding exhausted inputs.

    Each iteration requests one item from every iterator and substitutes `default` for exhausted iterators. The implementation yields the constructed row before rechecking `any_full`, so it emits one final row consisting entirely of `default` values after all inputs are exhausted.

    :param data: Collection of iterator objects; each element must support `next(iterator, sentinel)`.
    :type data: collections.abc.Iterable[collections.abc.Iterator]
    :param default: Padding value for exhausted iterators.
    :type default: object
    :return: Iterator over transposed rows, including a final all-padding row.
    :rtype: collections.abc.Iterator[list]
    """
    sentinel = object()
    any_full = True
    while any_full:
        any_full = False
        sublist = []
        for d in data:
            new = next(d, sentinel)
            if new is sentinel:
                sublist.append(default)
            else:
                any_full = True
                sublist.append(new)
        yield sublist
def transpose(data, default=None, pad=False):
    """
    **LLM Docstring**

    Transpose nested data, optionally padding shorter fixed-size rows.

    Fixed-size rows are indexed up to the maximum row length. With `pad=False`, missing elements are omitted from each transposed row; with `pad=True`, they are replaced by `default`.
    If the outer container is fixed-size but its first row has no `__len__`, the function returns `transpose_iter` without first converting the rows to iterators.
    Non-fixed outer inputs are fully materialized and processed recursively.

    :param data: Nested sequence or iterable to transpose.
    :type data: collections.abc.Iterable
    :param default: Padding value used by padded or iterator-based transposition.
    :type default: object
    :param pad: Whether fixed-size rows should be padded instead of skipped.
    :type pad: bool
    :return: A list of transposed rows or an iterator from `transpose_iter`.
    :rtype: list | collections.abc.Iterator
    """
    if is_fixed_size(data):
        fixed_data = is_fixed_size(data[0])
        if fixed_data:
            max_len = max(len(x) for x in data)
            if pad:
                return [
                    [d[i] if len(d) > i else default for d in data]
                    for i in range(max_len)
                ]
            else:
                return [
                    [d[i] for d in data if len(d) > i]
                    for i in range(max_len)
                ]
        else:
           return transpose_iter(data, default=default)
    else:
        return transpose(list(data), default=default) # need to cache results...

def riffle(a, b, *extras):
    """
    **LLM Docstring**

    Interleave corresponding values from multiple iterables.

    The first iterable determines the target length and is materialized when it lacks `__len__`.
    For each zipped tuple except the last first-iterable position, every tuple element is yielded; at the last position only the value from `a` is yielded.
    Any remaining tail of `a` is then emitted. Consequently values from the other iterables aligned with the final item of `a` are omitted.

    :param a: Primary iterable controlling output length and tail handling.
    :type a: collections.abc.Iterable
    :param b: First iterable to interleave with `a`.
    :type b: collections.abc.Iterable
    :param extras: Additional iterables to interleave.
    :type extras: collections.abc.Iterable
    :return: Iterator over the interleaved values.
    :rtype: collections.abc.Iterator
    """
    if not is_fixed_size(a):
        a = list(a)
    l = len(a)
    n = -1
    for n,p in enumerate(zip(a, b, *extras)):
        if n == l - 1:
            yield p[0]
        else:
            for x in p:
                yield x
    for x in a[n+1:]: yield x # exhaust a

def _is_atomic(atomic_obj, atomic_types):
    """
    **LLM Docstring**

    Determine whether an object should be treated as a leaf during flattening.

    Instances of `atomic_types` are always atomic. Other objects are considered atomic when `iter(obj)` raises `TypeError`; otherwise the function consumes at most one value from a newly created iterator and reports the object as non-atomic.

    :param atomic_obj: Object to inspect.
    :type atomic_obj: object
    :param atomic_types: Types that must be treated as leaves even if iterable.
    :type atomic_types: tuple[type, ...]
    :return: Whether the object is treated as atomic.
    :rtype: bool
    """
    if isinstance(atomic_obj, atomic_types): return True
    try:
        for _ in iter(atomic_obj): break
    except TypeError:
        return True
    return False

def flatten(iterable, atomic_types=None):
    """
    **LLM Docstring**

    Recursively yield leaf values from nested iterables.

    By default, integers, strings, floats, and all `numbers.Number` instances are leaves. Other iterable values are recursively traversed. Because `_is_atomic` probes iterability by creating and advancing an iterator, passing a single-use iterator as a nested value can consume its first item before recursion begins.

    :param iterable: Nested iterable to flatten.
    :type iterable: collections.abc.Iterable
    :param atomic_types: Optional tuple of types that should not be recursively expanded.
    :type atomic_types: tuple[type, ...] | None
    :return: Depth-first iterator over leaf values.
    :rtype: collections.abc.Iterator
    """
    if atomic_types is None:
        atomic_types = (int,str,float,numbers.Number)
    for o in iterable:
        if _is_atomic(o, atomic_types):
            yield o
        else:
            for f in flatten(o, atomic_types=atomic_types):
                yield f

def delete_duplicates(iterable, key=None, hashable=None, cache=None):
    """
    **LLM Docstring**

    Yield the first item associated with each distinct key.

    The function uses a set by default and automatically falls back to a list when adding an unhashable key raises `TypeError`. A supplied cache is updated in place and can preserve uniqueness state across calls.

    :param iterable: Values to filter.
    :type iterable: collections.abc.Iterable
    :param key: Optional function producing the value used for duplicate detection.
    :type key: callable | None
    :param hashable: Force set-based or list-based storage; `None` enables automatic fallback.
    :type hashable: bool | None
    :param cache: Existing membership cache to update.
    :type cache: set | list | None
    :return: Iterator yielding only the first value for each key.
    :rtype: collections.abc.Iterator
    """
    hashable = hashable
    if cache is None:
        cache = set() if (hashable or hashable is None) else []
    elif hashable is None:
        hashable = hasattr(cache, 'add')
    if key is None:
        key = lambda x:x
    for o in iterable:
        test = key(o)
        if test in cache: continue
        if hashable is None:
            try:
                cache.add(test)
            except TypeError:
                cache = list(cache)
                hashable = False
        elif hashable:
            cache.add(test)
        else:
            cache.append(test)

        yield o

def unique_product(*iterables, key=None, filter=None):
    """
    **LLM Docstring**

    Generate Cartesian-product tuples subject to a uniqueness filter.

    A depth-first deque traversal builds one value from each input. By default, a candidate is accepted only when it is not already present in the partial tuple; when `key` is supplied, uniqueness is checked on accumulated keys instead. Mapping-like inputs are explicitly converted with `iter`, which still iterates their keys. Indexable inputs are accessed by index. Non-indexable iterators are cached as values are discovered; the cached-value branch contains the condition `n + 1 < m` while `m` is negative, so previously cached later positions are not requeued through that branch.

    :param iterables: Input collections contributing one value each.
    :type iterables: collections.abc.Iterable
    :param key: Optional function mapping candidates to uniqueness keys.
    :type key: callable | None
    :param filter: Predicate receiving the partial tuple or key tuple and a candidate; defaults to rejecting repeats.
    :type filter: callable | None
    :return: Iterator over accepted product tuples.
    :rtype: collections.abc.Iterator[tuple]
    """
    queue = collections.deque()
    its = [
        iter(i) if hasattr(i, 'keys') else i # handle dict iteration by default
        for i in iterables
    ]
    caches = [
        []
        for _ in iterables
    ]
    it_lens = [
        len(it) if hasattr(it, '__getitem__') else -1
        for it in its
    ]
    queue.append((0, 0, (), ()))
    if filter is None:
        filter = lambda p,v: v not in p
    while queue:
        i, n, p, k = queue.pop()
        if i < len(its):
            it = its[i]
            m = it_lens[i]
            if m > 0:
                if n < m:
                    v = it[n]
                    if n + 1 < m:
                        queue.append((i, n+1, p, k))
                    if key is None:
                        if filter(p, v):
                            queue.append((i+1, 0, p + (v,), k))
                    else:
                        k2 = key(v)
                        if filter(k, k2):
                            queue.append((i+1, 0, p + (v,), k + (k2,)))
            else:
                cache = caches[i]
                if n < len(cache):
                    v = cache[n]
                    if n + 1 < m:
                        queue.append((i, n+1, p, k))
                    if key is None:
                        if filter(p, v):
                            queue.append((i+1, 0, p + (v,), k))
                    else:
                        k2 = key(v)
                        if filter(k, k2):
                            queue.append((i+1, 0, p + (v,), k + (k2,)))
                else:
                    try:
                        v = next(it)
                    except StopIteration:
                        it_lens[i] = 0 # faster termination next time around
                    else:
                        cache.append(v)
                        queue.append((i, n+1, p, k))
                        if key is None:
                            if filter(p, v):
                                queue.append((i+1, 0, p + (v,), k))
                        else:
                            k2 = key(v)
                            if filter(k, k2):
                                queue.append((i+1, 0, p + (v,), k + (k2,)))
        else:
            yield p

def zigzag_product(*iterables, iterator_lengths=None, return_index=False):
    """
    **LLM Docstring**

    Enumerate a Cartesian product while reversing selected axes to create a serpentine order.

    Inputs are materialized, optionally taking only the supplied `iterator_lengths`. As the ordinary multi-index advances, axis-direction flags are toggled when trailing indices reset to zero.

    :param iterables: Input iterables forming the Cartesian product.
    :type iterables: collections.abc.Iterable
    :param iterator_lengths: Optional lengths used both to limit materialization and reflect indices.
    :type iterator_lengths: collections.abc.Iterable[int | None] | None
    :param return_index: Whether to yield each value tuple together with its selected index tuple.
    :type return_index: bool
    :return: Iterator over value tuples or `(values, indices)` pairs.
    :rtype: collections.abc.Iterator
    """
    if iterator_lengths is None:
        iterator_lengths = [
            len(x) if is_fixed_size(x) else None
            for x in iterables
        ]

    iterator_caches = [
        list(itertools.islice(i, l))
            if l is not None else
        list(i)
        for i,l in zip(iterables, iterator_lengths)
    ]
    iterator_lengths = [len(x) for x in iterator_caches]

    flips = [False] * len(iterables)
    for multi_index in itertools.product(*(range(len(x)) for x in iterator_caches)):
        # if the previous term in the multi_index is positive we don't modify it
        # otherwise we invert
        if multi_index[-1] == 0:
            # we check to see if we need to change the flip pattern
            for i,prev in enumerate(multi_index[-2::-1]):
                if prev != 0:
                    for k in range(i+1):
                        flips[-(k+1)] = not flips[-(k+1)]

        new_index = tuple(
            iterator_lengths[i] - (x+1) if flips[i] else x
            for i,x in enumerate(multi_index)
        )
        res = tuple(iterator_caches[i][x] for i,x in enumerate(new_index))
        if return_index:
            yield res, new_index
        else:
            yield res

def first(iterable, key=None, default=None):
    """
    **LLM Docstring**

    Return the first value satisfying an optional predicate.

    When `key` is omitted, the first item is returned without testing its truth value. If no item qualifies, `default` is returned.

    :param iterable: Values to search.
    :type iterable: collections.abc.Iterable
    :param key: Optional predicate applied to each value.
    :type key: callable | None
    :param default: Value returned when no match is found.
    :type default: object
    :return: The first matching item or `default`.
    :rtype: object
    """
    for i in iterable:
        if key is None or key(i):
            return i
    return default