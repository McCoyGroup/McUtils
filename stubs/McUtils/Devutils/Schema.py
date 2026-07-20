"""
Basic layer for Schema validation that provides a superset of JSON schema validation
"""
import enum
import importlib
import re
import sys
import numbers
from . import core, Options as opts
__all__ = ['Schema']

class JSONSchemaTypes(enum.Enum):
    """Real access pattern: JSONSchemaTypes.<MemberName> (this is an enum with 6 members, e.g. JSONSchemaTypes.String == 'string'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
    _MEMBERS = {'String': 'string', 'Null': 'null', 'Boolean': 'boolean', 'Object': 'object', 'Number': 'number', 'Array': 'array'}

class TypeValidator:
    schema_types = JSONSchemaTypes

    def __init__(self, type_obj):
        """
        **LLM Docstring**

        Build a validator that checks a value against a set of types and/or validator
        callables.

        :param type_obj: the type specification (a type, name, schema-type, or list thereof)
        """
        ...
    allow_imports = True

    @classmethod
    def resolve_typestr(cls, type_spec):
        """
        **LLM Docstring**

        Resolve a type name to an actual type: a builtin alias, a JSON schema type, or a
        dotted `module.Type` import path.

        :param type_spec: the type name
        :type type_spec: str
        :return: the resolved type (or schema-type enum member)
        """
        ...

    @classmethod
    def get_schema_type(cls, t):
        """
        **LLM Docstring**

        Map a JSON-schema type enum member to the concrete type(s)/predicate(s) that
        test for it.

        :param t: the schema type
        :return: the type/predicate tuple
        :rtype: tuple
        :raises ValueError: for an unrecognized schema type
        """
        ...

    @classmethod
    def prep_type_obj(cls, t):
        """
        **LLM Docstring**

        Normalize a type object into a tuple of type(s)/predicate(s), expanding
        schema-type enum members.

        :param t: the type object
        :return: the type tuple
        :rtype: tuple
        """
        ...

    @classmethod
    def get_validators(cls, type_spec):
        """
        **LLM Docstring**

        Split a type specification into a tuple of concrete types (for `isinstance`) and
        a tuple of validator callables.

        :param type_spec: the type specification
        :return: `(types, validators)` (each `None` if empty)
        :rtype: tuple
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the types and validators.

        :return: the representation
        :rtype: str
        """
        ...

    def validate(self, obj, throw=False):
        """
        **LLM Docstring**

        Validate a value against the types and validator callables.

        :param obj: the value to validate
        :param throw: accepted for interface parity
        :type throw: bool
        :return: whether the value is valid
        :rtype: bool
        """
        ...

    def __call__(self, obj):
        """
        **LLM Docstring**

        Validate a value (delegates to `validate`).

        :param obj: the value to validate
        :return: whether the value is valid
        :rtype: bool
        """
        ...

class ValueValidator:
    __props__ = ('enum', 'const', 'multipleOf', 'maximum', 'minimum', 'exclusiveMaximum', 'exclusiveMinimum', 'maxLength', 'minLength', 'pattern', 'maxItems', 'minItems', 'uniqueItems', 'maxProperties', 'minProperties', 'required', 'validation_function')

    def __init__(self, enum=None, const=None, multipleOf=None, maximum=None, minimum=None, exclusiveMaximum=None, exclusiveMinimum=None, maxLength=None, minLength=None, pattern=None, maxItems=None, minItems=None, uniqueItems=None, maxProperties=None, minProperties=None, required=None, validation_function=None):
        """
        **LLM Docstring**

        Build a validator enforcing JSON-schema-style value constraints; only the
        supplied (non-`None`) constraints are activated as tests.

        :param enum: the value must be one of these
        :param const: the value must equal this
        :param multipleOf: the value must be a multiple of this
        :param maximum: inclusive upper bound
        :param minimum: inclusive lower bound
        :param exclusiveMaximum: exclusive upper bound
        :param exclusiveMinimum: exclusive lower bound
        :param maxLength: maximum length
        :param minLength: minimum length
        :param pattern: regex the value must match
        :param maxItems: maximum item count
        :param minItems: minimum item count
        :param uniqueItems: require unique items
        :param maxProperties: maximum number of keys
        :param minProperties: minimum number of keys
        :param required: keys that must be present
        :param validation_function: a custom predicate the value must satisfy
        """
        ...

    def _test_validation_function(self, value):
        ...

    def _test_enum(self, value):
        ...

    def _test_const(self, value):
        ...

    def _test_multipleOf(self, value):
        ...

    def _test_maximum(self, value):
        ...

    def _test_minimum(self, value):
        ...

    def _test_exclusiveMaximum(self, value):
        ...

    def _test_exclusiveMinimum(self, value):
        ...

    def _test_maxLength(self, value):
        ...

    def _test_minLength(self, value):
        ...

    def _test_maxItems(self, value):
        ...

    def _test_minItems(self, value):
        ...

    def _test_maxProperties(self, value):
        ...

    def _test_minProperties(self, value):
        ...

    def _test_required(self, value):
        ...

    def _test_uniqueItems(self, value):
        """
        **LLM Docstring**

        Failure test for the `uniqueItems` constraint: returns `True` when the value violates
        it (so `validate` rejects the value).

        :param value: the value to test
        :return: whether the constraint is violated
        :rtype: bool
        """
        ...

    def _test_pattern(self, value):
        """
        **LLM Docstring**

        Failure test for the `pattern` constraint: returns `True` when the value violates
        it (so `validate` rejects the value).

        :param value: the value to test
        :return: whether the constraint is violated
        :rtype: bool
        """
        ...

    def validate(self, value, throw=False):
        """
        **LLM Docstring**

        Validate a value against all active constraints.

        :param value: the value to validate
        :param throw: accepted for interface parity
        :type throw: bool
        :return: whether the value satisfies every constraint
        :rtype: bool
        """
        ...

    def __call__(self, obj):
        """
        **LLM Docstring**

        Validate a value (delegates to `validate`).

        :param obj: the value to validate
        :return: whether the value is valid
        :rtype: bool
        """
        ...

class Schema:
    """
    An object that represents a schema that can be used to test
    if an object matches that schema or not
    """
    type_validator = TypeValidator
    value_validator = ValueValidator

    def __init__(self, schema, optional_schema=None):
        """
        **LLM Docstring**

        Build a schema object from a schema specification (and optional additional
        optional-key schema).

        :param schema: the schema specification
        :param optional_schema: extra, non-required properties
        """
        ...

    @property
    def required_keys(self):
        """
        **LLM Docstring**

        The set of property keys the schema requires (computed lazily).

        :return: the required keys
        :rtype: set
        """
        ...

    @classmethod
    def is_json_schema(self, schema):
        """
        **LLM Docstring**

        Test whether a schema dict is already a JSON schema (has a `$schema` key).

        :param schema: the schema dict
        :return: whether it's a JSON schema
        :rtype: bool
        """
        ...

    @classmethod
    def _prep_schema_dict(cls, schema):
        """
        **LLM Docstring**

        Coerce a schema given as a list of keys (or `(key, value)` pairs) into a dict.

        :param schema: the schema (dict or list)
        :return: the schema dict
        :rtype: dict
        :raises ValueError: if it can't be canonicalized
        """
        ...

    @classmethod
    def _prep_validators(cls, schema):
        """
        **LLM Docstring**

        Replace each property's `type`/`value` specification in a JSON schema with the
        corresponding `TypeValidator`/`ValueValidator` objects (recursing into nested
        schemas).

        :param schema: the JSON schema
        :type schema: dict
        :return: the schema with validators installed
        :rtype: dict
        """
        ...
    json_schema_version = 'https://json-schema.org/draft/2020-12/schema'

    @classmethod
    def canonicalize_schema(cls, schema, optional_schema=None):
        """
        **LLM Docstring**

        Normalize any accepted schema form into a JSON schema with validator objects,
        folding in the required and optional properties.

        :param schema: the schema specification
        :param optional_schema: extra optional properties
        :return: the canonicalized schema (or `None`)
        :rtype: dict | None
        """
        ...

    @staticmethod
    def _get_prop(o, k):
        """
        **LLM Docstring**

        Read property `k` from an object, via item access when supported, else attribute
        access.

        :param o: the object
        :param k: the property key
        :return: the property value
        """
        ...

    def _validate_entry(self, obj, k, v: dict, prop_getter=None, required=True, throw=False):
        """
        **LLM Docstring**

        Validate a single property of an object against its schema entry, classifying
        missing/mistyped/mismatched cases and optionally raising.

        :param obj: the object
        :param k: the property key
        :param v: the property's schema entry
        :type v: dict
        :param prop_getter: the property accessor (defaults to `_get_prop`)
        :type prop_getter: Callable | None
        :param required: whether the property is required
        :type required: bool
        :param throw: raise on a mismatch
        :type throw: bool
        :return: `(value, matched)`
        :rtype: tuple
        :raises KeyError: on a mismatch when `throw` is set
        """
        ...

    def validate(self, obj, throw=True):
        """
        Validates that `obj` matches the provided schema
        and throws an error if not

        :param obj:
        :type obj:
        :param throw:
        :type throw:
        :return:
        :rtype:
        """
        ...

    def to_dict(self, obj, throw=True, ignore_invalid=False):
        """
        Converts `obj` into a plain `dict` representation

        :param obj:
        :type obj:
        :return:
        :rtype:
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the canonicalized schema.

        :return: the representation
        :rtype: str
        """
        ...