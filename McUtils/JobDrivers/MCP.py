"""
A minimal MCP server for a `ToolSet` over stdio, with no SDK: newline-delimited JSON-RPC 2.0 on stdin/stdout.

Handled: ``initialize`` (the client's ``protocolVersion`` is echoed), ``notifications/initialized`` (and any other
notification: no reply), ``ping``, ``tools/list`` and ``tools/call`` (the result is ``{content: [{type: "text", text:
<json>}], isError}``). Other methods get error ``-32601``. Logs go to stderr only; while serving, ``sys.stdout`` is
pointed at stderr so a tool that prints can't corrupt the protocol stream.
"""

import json
import sys
import time

__all__ = ["MCPServer"]

DEFAULT_PROTOCOL = "2024-11-05"


class MCPServer:
    """
    :param tools: a `ToolSet`
    :param name: ``serverInfo.name``
    :param instructions: optional text returned from ``initialize`` (clients show it to the model)
    :param call_log: a path (appended to) or ``callable(record)``; one record per ``tools/call``:
        ``{"time", "tool", "arguments", "ok", "error_code"}``. For looking at how a client uses the tools.
    """

    def __init__(self, tools, name="mcutils-tools", version="0.1.0", instructions=None, log=None, call_log=None):
        self.tools = tools
        self.name, self.version, self.instructions = name, version, instructions
        self.log = log if log is not None else sys.stderr
        self.call_log = call_log

    # ---- protocol --------------------------------------------------------------------------------- #
    @staticmethod
    def _error(id, code, message):
        return {"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}}

    def _call(self, params):
        if not isinstance(params, dict) or not isinstance(params.get("name"), str):
            return None
        args = params.get("arguments")
        if args is not None and not isinstance(args, dict):
            return None
        result = self.tools.call(params["name"], args)
        self._record(params["name"], args, result)
        body = result.value if result.ok else {"error": result.error}
        text = json.dumps(body, ensure_ascii=False, default=str)
        return {"content": [{"type": "text", "text": text}], "isError": not result.ok}

    def _record(self, name, args, result):
        if self.call_log is None:
            return
        rec = {"time": round(time.time(), 3), "tool": name, "arguments": args or {}, "ok": bool(result.ok),
               "error_code": None if result.ok else (result.error or {}).get("code")}
        try:
            if callable(self.call_log):
                self.call_log(rec)
            else:
                with open(self.call_log, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
        except Exception as e:  # noqa: BLE001 - logging must never break a call
            print(f"[{self.name}] call log failed: {e!r}", file=self.log, flush=True)

    def handle(self, message):
        """The reply (a dict) to one decoded message, or ``None`` for a notification."""
        if not isinstance(message, dict) or message.get("jsonrpc") != "2.0" or not isinstance(message.get("method"), str):
            return self._error(message.get("id") if isinstance(message, dict) else None, -32600, "invalid request")
        method, id, params = message["method"], message.get("id"), message.get("params")
        if "id" not in message:
            return None
        if method == "initialize":
            version = params.get("protocolVersion") if isinstance(params, dict) else None
            result = {"protocolVersion": version or DEFAULT_PROTOCOL, "capabilities": {"tools": {}},
                      "serverInfo": {"name": self.name, "version": self.version}}
            if self.instructions:
                result["instructions"] = self.instructions
            return {"jsonrpc": "2.0", "id": id, "result": result}
        if method == "ping":
            return {"jsonrpc": "2.0", "id": id, "result": {}}
        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": id, "result": {"tools": self.tools.tools()}}
        if method == "tools/call":
            result = self._call(params)
            if result is None:
                return self._error(id, -32602, "tools/call needs params {name: string, arguments?: object}")
            return {"jsonrpc": "2.0", "id": id, "result": result}
        return self._error(id, -32601, f"method not found: {method}")

    def handle_line(self, line):
        """The reply line (without newline) for one input line, or ``None``."""
        line = line.strip()
        if not line:
            return None
        try:
            message = json.loads(line)
        except ValueError as e:
            reply = self._error(None, -32700, f"parse error: {e}")
        else:
            try:
                reply = self.handle(message)
            except Exception as e:  # noqa: BLE001 - never let one request kill the server
                print(f"[{self.name}] internal error: {e!r}", file=self.log, flush=True)
                reply = self._error(message.get("id") if isinstance(message, dict) else None, -32603,
                                    f"internal error: {type(e).__name__}")
        return None if reply is None else json.dumps(reply, ensure_ascii=False, default=str)

    def serve(self, stdin=None, stdout=None):
        """Reads requests until end of input."""
        stdin = stdin if stdin is not None else sys.stdin
        out = stdout if stdout is not None else sys.stdout
        saved = sys.stdout
        sys.stdout = self.log
        try:
            print(f"[{self.name}] serving {len(self.tools.names())} tools on stdio", file=self.log, flush=True)
            for line in stdin:
                reply = self.handle_line(line)
                if reply is not None:
                    out.write(reply + "\n")
                    out.flush()
        finally:
            sys.stdout = saved
