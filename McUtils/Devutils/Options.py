"""
Provides functionality for managing large sets of options
"""

import os, inspect
from typing import Callable
from . import core

__all__ = [
    "OptionsSet",
    "OptionsMethodDispatch"
]

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
        if len(d) > 0:
            if isinstance(d[0], dict):
                self.ops = d[0]
                self.ops.update(ops)
            else:
                self.ops = dict(d, **ops)
        else:
            self.ops = ops
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get an option by key.

        :param item: the option name
        :return: the option value
        """
        return self.ops[item]
    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Set an option by key.

        :param key: the option name
        :param value: the option value
        """
        self.ops[key] = value
    def __delitem__(self, item):
        """
        **LLM Docstring**

        Delete an option by key.

        :param item: the option name
        """
        del self.ops[item]
    def __getattr__(self, item):
        """
        **LLM Docstring**

        Get an option via attribute access.

        :param item: the option name
        :return: the option value
        """
        return self.ops[item]
    def __setattr__(self, key, value):
        """
        **LLM Docstring**

        Set an option via attribute access (the `ops` dict itself is set normally).

        :param key: the option name (or `'ops'`)
        :param value: the value
        """
        if key == "ops":
            super().__setattr__(key, value)
        else:
            self.ops[key] = value
    def __delattr__(self, item):
        """
        **LLM Docstring**

        Delete an option via attribute access.

        :param item: the option name
        """
        del self.ops[item]
    def __hasattr__(self, key):
        """
        **LLM Docstring**

        Test whether an option exists.

        :param key: the option name
        :return: whether the option is present
        :rtype: bool
        """
        return key in self.ops
    def update(self, **ops):
        """
        **LLM Docstring**

        Update the options from keyword arguments.

        :param ops: the options to merge in
        """
        self.ops.update(**ops)

    def keys(self):
        """
        **LLM Docstring**

        The option names.

        :return: the option keys
        """
        return self.ops.keys()
    def items(self):
        """
        **LLM Docstring**

        The option `(name, value)` pairs.

        :return: the option items
        """
        return self.ops.items()

    def save(self, file, mode=None, attribute=None):
        """
        **LLM Docstring**

        Serialize the options to a file.

        :param file: the destination file
        :param mode: the serialization mode
        :param attribute: an attribute to serialize under
        """
        self.serialize(file)
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
        cls(cls.deserialize(file, mode=mode, attribute=attribute))

    def extract_kwarg_keys(self, obj):
        """
        **LLM Docstring**

        Determine the keyword-argument names of a callable from its signature (the
        trailing arguments that have defaults).

        :param obj: the callable
        :return: the keyword-argument names, or `None`
        :rtype: tuple | None
        """
        args, _, _, defaults, _, _, _  = inspect.getfullargspec(obj)
        if args is None:
            return None
        ndef = len(defaults) if defaults is not None else 0
        return tuple(args[-ndef:])
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
        if isinstance(obj, (list, tuple)):
            return sum(
                (self.get_props(o) for o in obj),
                ()
            )

        try:
            props = obj.__props__
        except AttributeError:
            try:
                annotations = obj.__annotations__
            except AttributeError:
                annotations = {}
            if len(annotations) == 0:
                props = self.extract_kwarg_keys(obj)
            else:
                props = tuple(annotations.keys())

        if props is None:
            raise AttributeError("{}: object {} needs props to filter against".format(
                type(self).__name__,
                self
            ))
        return props

    def bind(self, obj, props=None):
        """
        **LLM Docstring**

        Set each option that `obj` accepts as an attribute on `obj`.

        :param obj: the object to bind onto
        :param props: the option names to consider (inferred if omitted)
        :type props: Sequence[str] | None
        """
        for k,v in self.filter(obj, props=props).items():
            setattr(obj, k, self.ops[k])
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
        if props is None:
            props = self.get_props(obj)
        ops = self.ops
        return {k:ops[k] for k in ops.keys() & set(props)}
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
        if props is None:
            props = self.get_props(obj)
        ops = self.ops
        return {k:ops[k] for k in ops.keys() - set(props)}
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
        if props is None:
            props = self.get_props(obj)
        return self.filter(obj, props=props), self.exclude(obj, props=props)


class OptionsMethodDispatch:
    def __init__(self,
                 methods_table:'dict|Callable[[], dict]',
                 attributes_map=None,
                 default_method=None,
                 methods_enum=None,
                 case_insensitive=True,
                 allow_custom_methods=True,
                 ignore_bad_enum_keys=False,
                 method_key='method'):
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
        if not hasattr(methods_table, 'items'):
            self.methods_table_generator = methods_table
            self.methods_table = {}
        else:
            self.methods_table = methods_table
            self.methods_table_generator = None
        self.attributes_map = attributes_map
        self.case_insensitive = case_insensitive
        self.method_key = method_key
        self.methods_enum = methods_enum
        self.default_method = default_method
        self.allow_custom_methods = allow_custom_methods
        self.ignore_bad_enum_keys = ignore_bad_enum_keys

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
        self.methods_table[method_name] = method
        if base_attributes is not None:
            if self.attributes_map is None:
                self.attributes_map = {}
            if isinstance(base_attributes, str):
                base_attributes = (base_attributes,)
            self.attributes_map[tuple(base_attributes)] = method_name

    def load_methods_table(self):
        """
        **LLM Docstring**

        Return the methods table, merging any generator-produced entries with the
        explicitly registered ones.

        :return: the methods table
        :rtype: dict
        """
        if self.methods_table_generator is not None:
            return dict(self.methods_table_generator(), **self.methods_table)
        else:
            return self.methods_table

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
        if method is None and self.attributes_map is not None:
            for params, method_name in sorted(
                    self.attributes_map.items(),
                    key=lambda kt: -len(kt[0]) if not isinstance(kt[0], str) else 1
            ):
                if isinstance(params, str):
                    params = [params]
                if params is not None and all(p in opts for p in params):
                    return method_name

        return method

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
        if isinstance(method_spec, str) or core.is_default(method_spec):
            opts = {}
            method = method_spec
        elif hasattr(method_spec, 'name') and hasattr(method_spec, 'value'): # enum
            method = method_spec.value
            opts = {}
        elif core.is_dict_like(method_spec):
            opts = method_spec.copy()
            method = self._lookup_method(opts.pop(self.method_key, None), opts)
        elif callable(method_spec):
            method = method_spec
            opts = {}
        else:
            method, opts = method_spec
            method = self._lookup_method(method, opts)

        return method, opts

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
        method, opts = self.prep_method_spec(method_spec)
        methods_table = self.load_methods_table()
        if callable(method) and (
                self.allow_custom_methods
                or method in methods_table.values()
        ):
            return method, opts

        if (
                self.methods_enum is not None
                and not core.is_default(method, allow_None=True)
                and method not in methods_table
        ):
            if self.case_insensitive and isinstance(method, str):
                try:
                    method = self.methods_enum(method)
                except ValueError:
                    if self.ignore_bad_enum_keys:
                        try:
                            method = self.methods_enum(method)
                        except ValueError:
                            ...
                    else:
                        method = self.methods_enum(method.lower())
            else:
                if self.ignore_bad_enum_keys:
                    try:
                        method = self.methods_enum(method)
                    except ValueError:
                        ...
                else:
                    method = self.methods_enum(method)

            if hasattr(method, 'value'):
                return methods_table.get(
                    method,
                    methods_table.get(method.value, methods_table.get(self.default_method))
                ), opts
            else:
                return methods_table.get(
                method,
                methods_table.get(self.default_method)
            ), opts
        else:
            if self.case_insensitive and isinstance(method, str) and not method in methods_table:
                method = method.lower()

            return methods_table.get(
                method,
                methods_table.get(self.default_method)
            ), opts