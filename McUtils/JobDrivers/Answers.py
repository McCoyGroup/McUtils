"""
A small JSON-schema subset for validating model answers and tool arguments (no ``jsonschema`` dependency).

Supported keywords: ``type``, ``enum``, ``const``, ``properties``, ``required``, ``additionalProperties`` (a bool),
``items``, ``minItems``, ``maxItems``, ``uniqueItems``, ``minLength``, ``maxLength``, ``minimum``, ``maximum``
(plus the annotation keywords ``description``, ``title``, ``default`` and ``examples``, which are ignored). Any other keyword is a
``ValueError`` when the schema is checked, so an unsupported schema fails loudly instead of validating nothing.
"""

import json

__all__ = ["validate_answer", "check_schema", "parse_json_answer", "describe_schema"]

_TYPES = ("object", "array", "string", "integer", "number", "boolean", "null")
_ANNOTATIONS = ("description", "title", "default", "examples")
_KEYWORDS = ("type", "enum", "const", "properties", "required", "additionalProperties", "items", "minItems",
             "maxItems", "uniqueItems", "minLength", "maxLength", "minimum", "maximum")


def check_schema(schema, path="$"):
    """Raise ``ValueError`` if ``schema`` uses a keyword this validator doesn't support."""
    if not isinstance(schema, dict):
        raise ValueError(f"schema at {path} must be a dict, got {type(schema).__name__}")
    for k, v in schema.items():
        if k in _ANNOTATIONS:
            continue
        if k not in _KEYWORDS:
            raise ValueError(f"unsupported schema keyword {k!r} at {path}; supported: {', '.join(_KEYWORDS)}")
        if k == "type":
            for t in ([v] if isinstance(v, str) else v):
                if t not in _TYPES:
                    raise ValueError(f"unknown type {t!r} at {path}")
        elif k == "properties":
            if not isinstance(v, dict):
                raise ValueError(f"'properties' at {path} must be a dict")
            for name, sub in v.items():
                check_schema(sub, f"{path}.{name}")
        elif k == "items":
            check_schema(v, f"{path}[]")
        elif k == "additionalProperties" and not isinstance(v, bool):
            raise ValueError(f"'additionalProperties' at {path} must be a bool (schemas are not supported)")
        elif k == "required" and not isinstance(v, (list, tuple)):
            raise ValueError(f"'required' at {path} must be a list")
        elif k == "enum" and not isinstance(v, (list, tuple)):
            raise ValueError(f"'enum' at {path} must be a list")


def _type_ok(value, t):
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, (list, tuple))
    if t == "string":
        return isinstance(value, str)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "null":
        return value is None
    if t == "integer":
        return (isinstance(value, int) and not isinstance(value, bool)) or (isinstance(value, float) and value.is_integer())
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return False


def _same(a, b):
    # JSON equality: True is not 1
    return isinstance(a, bool) == isinstance(b, bool) and a == b


def _fmt(v, n=60):
    s = json.dumps(v, default=str) if not isinstance(v, str) else repr(v)
    return s if len(s) <= n else s[:n - 3] + "..."


def _validate(schema, value, path, errors):
    if "type" in schema:
        types = [schema["type"]] if isinstance(schema["type"], str) else list(schema["type"])
        if not any(_type_ok(value, t) for t in types):
            errors.append(f"{path}: expected {' or '.join(types)}, got {type(value).__name__} {_fmt(value)}")
            return
    if "enum" in schema and not any(_same(value, e) for e in schema["enum"]):
        choices = ", ".join(_fmt(e, 40) for e in schema["enum"])
        errors.append(f"{path}: {_fmt(value)} is not one of [{choices}]")
    if "const" in schema and not _same(value, schema["const"]):
        errors.append(f"{path}: must be {_fmt(schema['const'])}, got {_fmt(value)}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: {len(value)} characters is shorter than the minimum {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: {len(value)} characters is longer than the limit {schema['maxLength']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: {value} is below the minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: {value} is above the maximum {schema['maximum']}")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for name in schema.get("required", ()):
            if name not in value:
                errors.append(f"{path}: missing required property {name!r}")
        for name, v in value.items():
            if name in props:
                _validate(props[name], v, f"{path}.{name}", errors)
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property {name!r}; allowed: {sorted(props)}")
    if isinstance(value, (list, tuple)):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: {len(value)} items is fewer than the minimum {schema['minItems']}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: {len(value)} items is more than the limit {schema['maxItems']}")
        if schema.get("uniqueItems"):
            seen = []
            for i, v in enumerate(value):
                if any(_same(v, s) for s in seen):
                    errors.append(f"{path}[{i}]: duplicate item {_fmt(v)}")
                seen.append(v)
        if "items" in schema:
            for i, v in enumerate(value):
                _validate(schema["items"], v, f"{path}[{i}]", errors)


def validate_answer(schema, value):
    """
    Validate ``value`` against ``schema``.

    :return: ``[]`` if valid, else human-readable error strings that start with a JSON path (``$.caption: ...``)
    :raises ValueError: if the schema uses an unsupported keyword
    """
    check_schema(schema)
    errors = []
    _validate(schema, value, "$", errors)
    return errors


def describe_schema(schema, max_chars=1500):
    """A compact one-line JSON rendering of a schema, for prompts."""
    s = json.dumps(schema, separators=(",", ":"), default=str)
    return s if len(s) <= max_chars else s[:max_chars - 3] + "..."


def parse_json_answer(text):
    """
    Pull the first top-level JSON object out of a model reply, ignoring code fences and leading prose.

    :return: ``(value, error)``; exactly one of them is ``None``
    """
    if not isinstance(text, str):
        return None, f"the answer is not text ({type(text).__name__})"
    decoder = json.JSONDecoder()
    start = text.find("{")
    while start >= 0:
        try:
            value, _ = decoder.raw_decode(text, start)
        except ValueError:
            start = text.find("{", start + 1)
            continue
        return value, None
    return None, "no JSON object found in the answer; reply with one JSON object only"
