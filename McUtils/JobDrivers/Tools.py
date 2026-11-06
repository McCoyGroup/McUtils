"""
`ToolSet`: Python callables with argument schemas, one dispatch for the harness, MCP servers and tests.
"""

from .Answers import validate_answer, check_schema

__all__ = ["Tool", "ToolResult", "ToolSet"]


class Tool:
    def __init__(self, name, func, schema, description=""):
        check_schema(schema)
        self.name, self.func, self.schema, self.description = name, func, schema, description

    def to_dict(self):
        """MCP-style ``{name, description, inputSchema}``."""
        return {"name": self.name, "description": self.description, "inputSchema": self.schema}


class ToolResult:
    """``ok`` with ``value``, or not ok with ``error = {"code": ..., "detail": ...}``."""

    def __init__(self, ok, value=None, error=None):
        self.ok, self.value, self.error = ok, value, error

    def to_dict(self):
        return {"ok": True, "value": self.value} if self.ok else {"ok": False, "error": self.error}

    def __repr__(self):
        return f"ToolResult(ok={self.ok}, {'value' if self.ok else 'error'}={self.value if self.ok else self.error!r})"


class ToolSet:
    """
    :param hints: ``{error code: sentence}``; an error result with that code gets the sentence as ``hint`` (what to do
        next: retry, stop, call another tool). Useful for models, which follow a hint more reliably than a bare code.
    """

    def __init__(self, hints=None):
        self._tools = {}
        self.hints = dict(hints or {})

    def add(self, name, func, schema, description=""):
        if name in self._tools:
            raise ValueError(f"tool {name!r} is already defined")
        self._tools[name] = Tool(name, func, schema, description)
        return self._tools[name]

    def names(self):
        return list(self._tools)

    def tools(self):
        return [t.to_dict() for t in self._tools.values()]

    def _error(self, err):
        hint = self.hints.get(err.get("code"))
        if hint and "hint" not in err:
            err = dict(err, hint=hint)
        return ToolResult(False, error=err)

    def call(self, name, args=None):
        """
        Validate ``args`` against the tool's schema, then call it. Exceptions that carry ``code`` and ``detail``
        (like ``ReportOperationError``) become that error; anything else is ``{"code": "internal", ...}``.
        """
        args = {} if args is None else args
        tool = self._tools.get(name)
        if tool is None:
            return self._error({"code": "unknown_tool", "detail": f"no tool {name!r}; the tools are {self.names()}"})
        errors = validate_answer(tool.schema, args)
        if errors:
            return self._error({"code": "invalid_arguments", "detail": "; ".join(errors)})
        try:
            return ToolResult(True, tool.func(**args))
        except Exception as e:
            if hasattr(e, "code") and hasattr(e, "detail"):
                err = e.to_dict() if hasattr(e, "to_dict") else {"code": e.code, "detail": e.detail}
                return self._error(err)
            return self._error({"code": "internal", "detail": repr(e)})
