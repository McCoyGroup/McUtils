"""
Stable content fingerprints for arbitrary Python values.

`freeze` turns a value into a JSON-able structure (arrays by digest, functions by bytecode, objects by
attributes), and `fingerprint` hashes that with sha256. Classes can control this with a
`__fingerprint__(self)` method that returns the state to hash in place of the object, and callers can
exclude runtime-only attributes or add handlers for types they know about.
"""
from __future__ import annotations

import functools
import hashlib
import inspect
import json
import marshal
import sys
from pathlib import Path

import numpy as np

__all__ = [
    "freeze",
    "fingerprint",
    "file_hash",
    "implementation_signature",
    "chained_key",
]

def file_hash(path, algorithm='sha256', chunk_size=1 << 20):
    """
    **LLM Docstring**

    Hex digest of a file's contents.

    :param path: the file to hash
    :type path: str | os.PathLike
    :param algorithm: a `hashlib` algorithm name
    :type algorithm: str
    :param chunk_size: bytes read at a time
    :type chunk_size: int
    :return: the hex digest
    :rtype: str
    """
    digest = hashlib.new(algorithm)
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b''):
            digest.update(chunk)
    return digest.hexdigest()

def freeze(value, *, seen=None, handlers=(), pre_handlers=(), exclude_attrs=()):
    """
    **LLM Docstring**

    Reduce `value` to a JSON-able structure that only depends on what it means, not on where it lives
    in memory. Shared references are recorded as `['reference', n]` so aliasing is part of the result.

    :param value: the value to freeze
    :type value: object
    :param seen: identity table used for shared references (internal)
    :type seen: dict | None
    :param handlers: `(predicate, function)` pairs checked for objects after the built-in containers,
        arrays and functions; `function(value, kind, rec)` returns the frozen form, where `kind` is
        `'module.QualName'` and `rec(sub_value)` freezes children with the same options
    :type handlers: Sequence[tuple[callable, callable]]
    :param pre_handlers: like `handlers` but checked first, with `function(value, rec)`
    :type pre_handlers: Sequence[tuple[callable, callable]]
    :param exclude_attrs: attribute names left out for every object (a class can also list names in
        `__fingerprint_exclude__`)
    :type exclude_attrs: Collection[str]
    :return: the frozen structure
    :rtype: object
    """
    if seen is None:
        seen = {}
    exclude_attrs = frozenset(exclude_attrs)
    def rec(v):
        return freeze(v, seen=seen, handlers=handlers, pre_handlers=pre_handlers, exclude_attrs=exclude_attrs)

    for test, fn in pre_handlers:
        if test(value):
            return fn(value, rec)
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, np.generic):
        return rec(value.item())
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.ndarray):
        array = np.ascontiguousarray(value)
        if array.dtype.hasobject:
            return ['object-array', array.shape, rec(array.tolist())]
        return ['array', array.shape, array.dtype.str,
                hashlib.sha256(memoryview(array).cast('B')).hexdigest()]
    if isinstance(value, (list, tuple)):
        return [type(value).__name__, [rec(v) for v in value]]
    if isinstance(value, (set, frozenset)):
        return ['set', sorted((rec(v) for v in value), key=repr)]
    if isinstance(value, dict):
        return ['dict', sorted([[rec(k), rec(v)] for k, v in value.items()], key=lambda p: repr(p[0]))]
    if isinstance(value, functools.partial):
        return ['partial', rec(value.func), rec(value.args), rec(value.keywords)]
    if inspect.ismethod(value):
        return ['method', rec(value.__self__), rec(value.__func__)]
    if inspect.isfunction(value):
        return ['function', value.__module__, value.__qualname__,
                hashlib.sha256(marshal.dumps(value.__code__)).hexdigest(),
                rec(value.__defaults__),
                rec(tuple(c.cell_contents for c in (value.__closure__ or ())))]
    identity = id(value)
    if identity in seen:
        return ['reference', seen[identity]]
    seen[identity] = len(seen)
    kind = type(value).__module__ + '.' + type(value).__qualname__
    hook = getattr(type(value), '__fingerprint__', None)
    if hook is not None:
        return rec(hook(value))
    for test, fn in handlers:
        if test(value):
            return fn(value, kind, rec)
    skip = exclude_attrs.union(getattr(type(value), '__fingerprint_exclude__', ()))
    attrs = getattr(value, '__dict__', None)
    if attrs is not None:
        return [kind, {name: rec(v) for name, v in sorted(attrs.items()) if name not in skip}]
    slots = {}
    for base in type(value).__mro__:
        names = getattr(base, '__slots__', ())
        if isinstance(names, str):
            names = (names,)
        for name in names:
            if name not in {'__weakref__', '__dict__'} and name not in skip and hasattr(value, name):
                slots[name] = rec(getattr(value, name))
    if slots:
        return [kind, slots]
    raise TypeError('no fingerprint for {}'.format(kind))

def fingerprint(value, **freeze_options):
    """
    **LLM Docstring**

    sha256 hex digest of `freeze(value, **freeze_options)` serialized as sorted-key JSON.

    :param value: the value to fingerprint
    :type value: object
    :param freeze_options: forwarded to `freeze`
    :return: the hex digest
    :rtype: str
    """
    return hashlib.sha256(json.dumps(freeze(value, **freeze_options), sort_keys=True).encode()).hexdigest()

@functools.lru_cache(None)
def _implementation_signature(modules):
    import importlib
    result = dict(numpy=np.__version__, python=list(sys.version_info[:2]))
    for name in modules:
        module = importlib.import_module(name)
        root = Path(module.__file__).parent
        digest = hashlib.sha256()
        for path in sorted(root.rglob('*.py')):
            digest.update(str(path.relative_to(root)).encode())
            digest.update(bytes.fromhex(file_hash(path)))
        result[module.__name__] = digest.hexdigest()
    return result

def implementation_signature(*modules):
    """
    **LLM Docstring**

    Digest of the source of the given packages plus the NumPy and Python versions, for keys that must
    change when the code that produced a result changes. Cached per process.

    :param modules: importable package names
    :type modules: str
    :return: the signature
    :rtype: dict
    """
    return dict(_implementation_signature(tuple(modules)))


def chained_key(*parts, algorithm='sha256', **freeze_options):
    """
    **LLM Docstring**

    A key built by folding the fingerprints of `parts` in order (each step hashes the previous key with
    the next part's fingerprint), so a key depends on every earlier part and on their order.

    :param parts: the values (or already-computed keys) that define the result
    :param algorithm: a `hashlib` algorithm name
    :type algorithm: str
    :param freeze_options: forwarded to `freeze`
    :return: the hex digest
    :rtype: str
    """
    if not parts:
        raise ValueError("chained_key needs at least one part")
    key = ''
    for part in parts:
        text = json.dumps(freeze(part, **freeze_options), sort_keys=True)
        key = hashlib.new(algorithm, (key + ':' + text).encode()).hexdigest()
    return key
