"""
Provides functionality for managing large sets of options
"""
import os, inspect
from typing import Callable
from . import core
__all__ = ['OptionsSet', 'OptionsMethodDispatch']

class OptionsSet:
    """
    Provides a helpful manager for those cases where
    there are way too many options and we need to filter
    them across subclasses and things
    """

    def __init__(self, *d, **ops):
        """
        **LLM Docstring**

        Wrap a set of options (from a dict and/or keyword arguments) for filtering and
        binding.

        :param d: an optional initial options dict (positional)
        :param ops: additional options as keyword arguments
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get an option by key.

        :param item: the option name
        :return: the option value
        """
        ...

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Set an option by key.

        :param key: the option name
        :param value: the option value
        """
        ...

    def __delitem__(self, item):
        """
        **LLM Docstring**

        Delete an option by key.

        :param item: the option name
        """
        ...

    def __getattr__(self, item):
        """
        **LLM Docstring**

        Get an option via attribute access.

        :param item: the option name
        :return: the option value
        """
        ...

    def __setattr__(self, key, value):
        """
        **LLM Docstring**

        Set an option via attribute access (the `ops` dict itself is set normally).

        :param key: the option name (or `'ops'`)
        :param value: the value
        """
        ...

    def __delattr__(self, item):
        """
        **LLM Docstring**

        Delete an option via attribute access.

        :param item: the option name
        """
        ...

    def __hasattr__(self, key):
        """
        **LLM Docstring**

        Test whether an option exists.

        :param key: the option name
        :return: whether the option is present
        :rtype: bool
        """
        ...

    def update(self, **ops):
        """
        **LLM Docstring**

        Update the options from keyword arguments.

        :param ops: the options to merge in
        """
        ...

    def keys(self):
        """
        **LLM Docstring**

        The option names.

        :return: the option keys
        """
        ...

    def items(self):
        """
        **LLM Docstring**

        The option `(name, value)` pairs.

        :return: the option items
        """
        ...

    def save(self, file, mode=None, attribute=None):
        """
        **LLM Docstring**

        Serialize the options to a file.

        :param file: the destination file
        :param mode: the serialization mode
        :param attribute: an attribute to serialize under
        """
        ...

    @classmethod
    def load(cls, file, mode=None, attribute=None):
        """
        **LLM Docstring**

        Load options from a file into a new `OptionsSet`.

        :param file: the source file
        :param mode: the serialization mode
        :param attribute: the attribute to read from
        :return: the loaded options
        :rtype: OptionsSet
        """
        ...

    def extract_kwarg_keys(self, obj):
        """
        **LLM Docstring**

        Determine the keyword-argument names of a callable from its signature (the
        trailing arguments that have defaults).

        :param obj: the callable
        :return: the keyword-argument names, or `None`
        :rtype: tuple | None
        """
        ...

    def get_props(self, obj):
        """
        **LLM Docstring**

        Determine the set of option names an object accepts, from its `__props__`,
        its annotations, or (failing those) its keyword-argument signature; unions the
        results across a list/tuple of objects.

        :param obj: the object (or list of objects) to inspect
        :return: the accepted option names
        :rtype: tuple
        :raises AttributeError: if no props can be determined
        """
        ...

    def bind(self, obj, props=None):
        """
        **LLM Docstring**

        Set each option that `obj` accepts as an attribute on `obj`.

        :param obj: the object to bind onto
        :param props: the option names to consider (inferred if omitted)
        :type props: Sequence[str] | None
        """
        ...

    def filter(self, obj, props=None):
        """
        **LLM Docstring**

        Return the subset of options whose names are accepted by `obj`.

        :param obj: the object whose props to filter against
        :param props: the option names (inferred if omitted)
        :type props: Sequence[str] | None
        :return: the matching options
        :rtype: dict
        """
        ...

    def exclude(self, obj, props=None):
        """
        **LLM Docstring**

        Return the subset of options whose names are *not* accepted by `obj`.

        :param obj: the object whose props to filter against
        :param props: the option names (inferred if omitted)
        :type props: Sequence[str] | None
        :return: the non-matching options
        :rtype: dict
        """
        ...

    def split(self, obj, props=None):
        """
        **LLM Docstring**

        Split the options into the `(accepted, excluded)` subsets for `obj`.

        :param obj: the object whose props to split against
        :param props: the option names (inferred if omitted)
        :type props: Sequence[str] | None
        :return: `(filtered, excluded)`
        :rtype: tuple
        """
        ...

class OptionsMethodDispatch:

    def __init__(self, methods_table: 'dict|Callable[[], dict]', attributes_map=None, default_method=None, methods_enum=None, case_insensitive=True, allow_custom_methods=True, ignore_bad_enum_keys=False, method_key='method'):
        """
        **LLM Docstring**

        Set up a dispatcher that resolves a method specification into a `(method,
        options)` pair against a table of named methods.

        :param methods_table: the name-to-method mapping, or a callable producing one
        :type methods_table: dict | Callable
        :param attributes_map: maps attribute-name sets to a method (for keyword-based dispatch)
        :type attributes_map: dict | None
        :param default_method: the fallback method name
        :param methods_enum: an enum used to canonicalize method names
        :param case_insensitive: match method names case-insensitively
        :type case_insensitive: bool
        :param allow_custom_methods: allow passing a callable directly as the method
        :type allow_custom_methods: bool
        :param ignore_bad_enum_keys: swallow enum-lookup failures
        :type ignore_bad_enum_keys: bool
        :param method_key: the dict key holding the method name
        :type method_key: str
        """
        ...

    def register(self, method_name, method, base_attributes=None):
        """
        **LLM Docstring**

        Register a method under a name, optionally mapping a set of base attributes to
        it for keyword-based dispatch.

        :param method_name: the method name
        :param method: the method (callable)
        :param base_attributes: attribute name(s) that select this method
        :type base_attributes: str | Sequence[str] | None
        """
        ...

    def load_methods_table(self):
        """
        **LLM Docstring**

        Return the methods table, merging any generator-produced entries with the
        explicitly registered ones.

        :return: the methods table
        :rtype: dict
        """
        ...

    def _lookup_method(self, method, opts):
        """
        **LLM Docstring**

        When no method is named, infer one from the supplied options by matching the
        attributes map (preferring the most specific attribute set).

        :param method: the explicit method (or `None`)
        :param opts: the supplied options
        :type opts: dict
        :return: the resolved method name (or the original method)
        """
        ...

    def prep_method_spec(self, method_spec):
        """
        **LLM Docstring**

        Normalize a method specification into a `(method, options)` pair, accepting
        strings, enum members, dicts (with a method key), callables, and
        `(method, opts)` tuples.

        :param method_spec: the method specification
        :return: `(method, options)`
        :rtype: tuple
        """
        ...

    def resolve(self, method_spec):
        """
        **LLM Docstring**

        Resolve a method specification into the actual `(method, options)` to use,
        looking the method up in the table (canonicalizing via the enum and applying
        case-insensitive and default fallbacks as configured).

        :param method_spec: the method specification
        :return: `(resolved_method, options)`
        :rtype: tuple
        """
        ...