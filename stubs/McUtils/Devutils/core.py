"""
Provides a set of singleton objects that can declare their purpose a little bit better than None can
"""
import itertools
import types
import numbers
__all__ = ['default', 'is_default', 'handle_default', 'uninitialized', 'is_uninitialized', 'handle_uninitialized', 'missing', 'is_missing', 'is_interface_like', 'is_dict_like', 'is_option_spec_like', 'destructure_option_spec', 'is_list_like', 'is_number', 'is_int', 'is_atomic', 'cached_eval', 'merge_dicts', 'str_comp', 'str_is', 'str_in', 'str_startswith', 'str_endswith', 'str_elide', 'resolve_key_collision', 'merge_dicts', 'context_wrap', 'slice_dict', 'dict_take']

class SingletonType:
    """
    A base type for singletons
    """
    __slots__ = []

    def __eq__(self, other):
        """
        **LLM Docstring**

        Two singletons compare equal if they are the same object, or share a type name
        and defining module (so equivalent singletons survive re-imports/pickling).

        :param other: the object to compare against
        :return: whether they represent the same singleton
        :rtype: bool
        """
        ...

    def __hash__(self):
        """
        **LLM Docstring**

        Hash the singleton by its module-qualified type name (consistent with `__eq__`).

        :return: the hash
        :rtype: int
        """
        ...

class DefaultType(SingletonType):
    """
    A type for declaring an argument should use its default value (for when `None` has meaning)
    """
    __is_default__ = True
default = DefaultType()

class MissingType(SingletonType):
    """
    A type for declaring a value is missing (for when `None` has meaning)
    """
    __is_missing__ = False
missing = MissingType()

class UninitializedType(SingletonType):
    """
    A type for declaring an argument should use its default value (for when `None` has meaning)
    """
    __is_uninitialized__ = True
uninitialized = UninitializedType()

def is_atomic(obj, interface_types=(str, bool, numbers.Number), exlusion_types=None, implementation_props=None):
    """
    **LLM Docstring**

    Test whether an object is an atomic value (string, bool, or number by default).

    :param obj: the object to test
    :param interface_types: the types treated as atomic
    :param exlusion_types: types to explicitly exclude
    :param implementation_props: attributes an object must have to qualify
    :return: whether the object is atomic
    :rtype: bool
    """
    ...

def is_number(obj, interface_types=(numbers.Number,), exlusion_types=None, implementation_props=None):
    """
    **LLM Docstring**

    Test whether an object is a number.

    :param obj: the object to test
    :param interface_types: the numeric types
    :param exlusion_types: types to exclude
    :param implementation_props: attributes an object must have to qualify
    :return: whether the object is a number
    :rtype: bool
    """
    ...

def is_int(obj, interface_types=(numbers.Integral,), exlusion_types=None, implementation_props=None):
    """
    **LLM Docstring**

    Test whether an object is an integer.

    :param obj: the object to test
    :param interface_types: the integral types
    :param exlusion_types: types to exclude
    :param implementation_props: attributes an object must have to qualify
    :return: whether the object is an integer
    :rtype: bool
    """
    ...

def is_interface_like(obj, interface_types, exlusion_types, implementation_attrs):
    """
    **LLM Docstring**

    General duck-typing test: an object qualifies if it isn't an excluded type and is
    either an instance of one of the interface types or has all of the required
    implementation attributes.

    :param obj: the object to test
    :param interface_types: the accepted types (or `None`)
    :param exlusion_types: types to reject (or `None`)
    :param implementation_attrs: attributes the object must expose (or `None`)
    :return: whether the object matches the interface
    :rtype: bool
    """
    ...

def is_dict_like(obj, interface_types=(dict, types.MappingProxyType), exlusion_types=None, implementation_props=('items',)):
    """
    **LLM Docstring**

    Test whether an object is dict-like (a mapping, or exposes `items`).

    :param obj: the object to test
    :param interface_types: the mapping types
    :param exlusion_types: types to exclude
    :param implementation_props: attributes an object must have to qualify
    :return: whether the object is dict-like
    :rtype: bool
    """
    ...

def is_list_like(obj, interface_types=(list, tuple), exlusion_types=(str, dict, type), implementation_props=('__getitem__',)):
    """
    **LLM Docstring**

    Test whether an object is list-like (a sequence, excluding strings/dicts/types).

    :param obj: the object to test
    :param interface_types: the sequence types
    :param exlusion_types: types to exclude
    :param implementation_props: attributes an object must have to qualify
    :return: whether the object is list-like
    :rtype: bool
    """
    ...

def is_default(obj, allow_None=True):
    """
    **LLM Docstring**

    Test whether a value is the `default` singleton (optionally treating `None` as
    default too).

    :param obj: the value to test
    :param allow_None: treat `None` as default
    :type allow_None: bool
    :return: whether the value is default
    :rtype: bool
    """
    ...

def is_option_spec_like(obj, allow_enums=True):
    """
    **LLM Docstring**

    Test whether an object can be destructured into a `(method, options)` option
    specification.

    :param obj: the object to test
    :param allow_enums: allow enum members (using their `value` as the method)
    :type allow_enums: bool
    :return: whether the object is option-spec-like
    :rtype: bool
    """
    ...

def destructure_option_spec(spec, allow_enums=True, method_key='method'):
    """
    **LLM Docstring**

    Split an option specification into a `(method, options)` pair, accepting bare
    values/callables, enum members, dicts (with a method key), and `(method, opts)`
    tuples.

    :param spec: the option specification
    :param allow_enums: treat enum members as methods
    :type allow_enums: bool
    :param method_key: the dict key holding the method
    :type method_key: str
    :return: `(method, options)` (both `None` if it can't be destructured)
    :rtype: tuple
    """
    ...

def handle_default(opt, default_value, allow_None=True):
    """
    **LLM Docstring**

    Return `default_value` when `opt` is the `default` singleton, else `opt`.

    :param opt: the supplied value
    :param default_value: the value to substitute for `default`
    :param allow_None: treat `None` as default
    :type allow_None: bool
    :return: the resolved value
    """
    ...

def is_uninitialized(obj, allow_None=True):
    """
    **LLM Docstring**

    Test whether a value is the `uninitialized` singleton (optionally treating `None`
    as uninitialized too).

    :param obj: the value to test
    :param allow_None: treat `None` as uninitialized
    :type allow_None: bool
    :return: whether the value is uninitialized
    :rtype: bool
    """
    ...

def handle_uninitialized(opt, initializer, allow_None=True, args=(), kwargs=None):
    """
    **LLM Docstring**

    Return the result of calling `initializer` when `opt` is uninitialized, else
    `opt` (lazy initialization).

    :param opt: the supplied value
    :param initializer: the callable producing the initial value
    :type initializer: Callable
    :param allow_None: treat `None` as uninitialized
    :type allow_None: bool
    :param args: positional arguments for the initializer
    :param kwargs: keyword arguments for the initializer
    :return: the resolved value
    """
    ...

def is_missing(obj, allow_None=True):
    """
    **LLM Docstring**

    Test whether a value is the `missing` singleton (optionally treating `None` as
    missing too).

    :param obj: the value to test
    :param allow_None: treat `None` as missing
    :type allow_None: bool
    :return: whether the value is missing
    :rtype: bool
    """
    ...

def cached_eval(cache, key, generator, *, condition=None, args=(), kwargs=None):
    """
    **LLM Docstring**

    Return `cache[key]`, computing and storing it via `generator` on a miss;
    optionally bypass the cache entirely when a `condition` on the key fails.

    :param cache: the cache mapping
    :type cache: dict
    :param key: the cache key
    :param generator: the callable that computes the value
    :type generator: Callable
    :param condition: a predicate on the key gating whether to cache
    :type condition: Callable | None
    :param args: positional arguments for the generator
    :param kwargs: keyword arguments for the generator
    :return: the cached (or freshly computed) value
    """
    ...

def _case_folded_iterable(test_val):
    """
    **LLM Docstring**

    Return a case-folded copy of an iterable of strings (preserving its type), or
    `None` if it isn't such an iterable.

    :param test_val: the iterable to fold
    :return: the case-folded iterable, or `None`
    """
    ...

def str_comp(str_val, test, test_val, ignore_case=False):
    """
    **LLM Docstring**

    Compare a string against a test value with a comparison callback, optionally
    case-insensitively (folding both sides, including iterables of strings).

    :param str_val: the value being tested (must be a string to match)
    :param test: the comparison callback `(a, b) -> bool`
    :type test: Callable
    :param test_val: the value to compare against
    :param ignore_case: compare case-insensitively
    :type ignore_case: bool
    :return: the comparison result
    :rtype: bool
    """
    ...

def str_is(str_val, test_val, ignore_case=False):
    """
    **LLM Docstring**

    Test whether a string equals a value (optionally case-insensitively).

    :param str_val: the value being tested
    :param test_val: the value to compare against
    :param ignore_case: compare case-insensitively
    :type ignore_case: bool
    :return: whether they are equal
    :rtype: bool
    """
    ...

def str_in(str_val, test_vals, ignore_case=False):
    """
    **LLM Docstring**

    Test whether a string is contained in a collection (optionally
    case-insensitively).

    :param str_val: the value being tested
    :param test_vals: the collection to test membership in
    :param ignore_case: compare case-insensitively
    :type ignore_case: bool
    :return: whether the string is a member
    :rtype: bool
    """
    ...

def str_startswith(str_val, test_vals, ignore_case=False):
    """
    **LLM Docstring**

    Test whether a string starts with a prefix (optionally case-insensitively).

    :param str_val: the value being tested
    :param test_vals: the prefix(es)
    :param ignore_case: compare case-insensitively
    :type ignore_case: bool
    :return: whether the string starts with the prefix
    :rtype: bool
    """
    ...

def str_endswith(str_val, test_vals, ignore_case=False):
    """
    **LLM Docstring**

    Test whether a string ends with a suffix (optionally case-insensitively).

    :param str_val: the value being tested
    :param test_vals: the suffix(es)
    :param ignore_case: compare case-insensitively
    :type ignore_case: bool
    :return: whether the string ends with the suffix
    :rtype: bool
    """
    ...

def str_elide(long_str, width=80, placeholder='...'):
    """
    **LLM Docstring**

    Truncate a long string to `width` characters by replacing its middle with a
    placeholder.

    :param long_str: the string to elide
    :type long_str: str
    :param width: the maximum width
    :type width: int
    :param placeholder: the middle placeholder
    :type placeholder: str
    :return: the elided string
    :rtype: str
    """
    ...

def resolve_key_collision(a, b, k, merge_iterables=True):
    """
    **LLM Docstring**

    Default collision handler for `merge_dicts`: recursively merge dict values, union
    sets, and chain list-like values, otherwise take the value from `b`.

    :param a: the first dict
    :param b: the second dict
    :param k: the colliding key
    :param merge_iterables: merge set/list values rather than overwriting
    :type merge_iterables: bool
    :return: the merged value for the key
    """
    ...

def merge_dicts(a, b, collision_handler=None, merge_iterables=True):
    """
    **LLM Docstring**

    Merge two dicts, resolving colliding keys with a handler (defaulting to
    `resolve_key_collision`).

    :param a: the first dict
    :param b: the second dict
    :param collision_handler: the `(a, b, k) -> value` collision handler
    :type collision_handler: Callable | None
    :param merge_iterables: merge iterable values on collisions
    :type merge_iterables: bool
    :return: the merged dict
    :rtype: dict
    """
    ...

class context_wrap:

    def __init__(self, obj):
        """
        **LLM Docstring**

        Wrap an arbitrary object so it can be used as a context manager, delegating to
        its own `__enter__`/`__exit__` when present.

        :param obj: the object to wrap
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Enter the wrapped object's context (or just return it if it isn't a context
        manager).

        :return: the entered object
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Exit the wrapped object's context, if it is a context manager.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        :return: the wrapped `__exit__`'s result, if any
        """
        ...

class slice_dict:
    __slots__ = ['dict_obj']

    def __init__(self, dict_obj: types.MappingProxyType):
        """
        **LLM Docstring**

        Wrap a mapping to support slice/index/key-based extraction via `[]`.

        :param dict_obj: the mapping to wrap
        :type dict_obj: Mapping
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Extract from the wrapped mapping by index, slice, or key spec (delegates to
        `dict_take`).

        :param item: the extraction spec
        :return: the extracted entries
        """
        ...

def dict_take(dict_obj: types.MappingProxyType, spec):
    """
    **LLM Docstring**

    Extract entries from a mapping by an integer position, a slice of positions, a
    list of keys, or a list of integer positions.

    :param dict_obj: the mapping
    :type dict_obj: Mapping
    :param spec: the extraction spec (int, slice, key list, or position list)
    :return: the extracted `(key, value)` entry or sub-dict
    :raises IndexError: if a requested position can't be found
    """
    ...