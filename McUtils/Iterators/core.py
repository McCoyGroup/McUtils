import itertools

__all__ = [
    "is_fixed_size",
    "consume",
    "chunked",
    "take_lists",
    "split",
    "split_by",
    "counts"
]

def is_fixed_size(iterable):
    return hasattr(iterable, '__len__')

def consume(iterable, n, return_values=True):
    if return_values:
        return list(itertools.islice(iterable, n))
    else:
        return next(itertools.islice(iterable, n, n), None)

def chunked(a, upto):
    if is_fixed_size(a):
        l = len(a)
        blocks = (l // upto) +  (0 if (l % upto) == 0 else 1)
        for i in range(blocks):
            yield a[i*upto:(i+1)*upto]
    else:
        def consumer(a=a):
            return list(itertools.islice(a, upto))
        return iter(consumer, [])

def split(a, test=None):
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
    def test(next, prev, canonicalizer=canonicalizer, cache=[True, None]):
        if cache[0]:
            cache[1] = canonicalizer(prev)
        new = canonicalizer(next)
        ret = new != cache[1]
        cache[1] = new
        return ret
    return split(a, test)

def take_lists(a, splits):
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
def counts(iterable, test=None):
    if test is None: test = lambda x:x
    return {k:len(g) for k,g in itertools.groupby(iterable, test)}