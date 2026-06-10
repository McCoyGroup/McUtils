"""
A simple handler interprocess communication on HPC systems
"""
import abc
import os
import shutil
import threading, time
import socket, socketserver, json, traceback, subprocess
import sys
import multiprocessing as mp

__all__ = [
    "NodeCommTCPServer",
    "NodeCommUnixServer",
    "NodeCommHandler",
    "NodeCommClient",
    "ShellCommHandler",
    "setup_parent_terminated_listener",
    "setup_server",
    "handle_command_line"
]


# PUT HERE TO CHECK IF THE PROCESS SHOULD DIE OR NOT
def check_kill_process(w_pid, cur_pid):
    import psutil, signal
    if not psutil.pid_exists(w_pid):
        os.kill(cur_pid, signal.SIGKILL)  # maybe make this less dramatic
        exit(1)
    return True


def listen_for_proc(w_pid, cur_pid, polling_time=5):
    while check_kill_process(w_pid, cur_pid):
        time.sleep(polling_time)


def setup_parent_terminated_listener(PARENT_PID, CURRENT_PID):
    thread = threading.Thread(
        target=listen_for_proc,
        args=(PARENT_PID, CURRENT_PID)
    )
    thread.start()
    return thread


def infer_mode(connection):
    if (
            isinstance(connection, tuple)
            and isinstance(connection[0], str) and isinstance(connection[1], int)
    ):
        mode = "TCP"
    elif isinstance(connection, str):
        mode = "Unix"
    else:
        raise ValueError(f"invalid connection spec {connection}")
    return mode


class NodeCommTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

try:
    exists = socketserver.UnixStreamServer
except AttributeError:
    class NodeCommUnixServer:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("`socketserver.UnixStreamServer` not available")
else:
    class NodeCommUnixServer(socketserver.UnixStreamServer):
        allow_reuse_address = True

        def server_bind(self):
            """Called by constructor to bind the socket.

            May be overridden.

            """

            if self.allow_reuse_address:
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(self.server_address)
            self.server_address = self.socket.getsockname()


class NodeCommClient:
    def __init__(self, connection, timeout=10):
        self.conn = connection
        mode = infer_mode(connection)
        if mode == "TCP":
            self.mode = socket.AF_INET
        elif mode == "Unix":
            self.mode = socket.AF_UNIX
        else:
            raise NotImplementedError(mode)
        self.timeout = timeout

    SEND_CWD = True
    def prep_command_env(self):
        env = {}
        if self.SEND_CWD:
            env['pwd'] = os.getcwd()
        return env

    def communicate(self, command, args, kwargs):
        request = json.dumps({
            "command": command,
            "args": args,
            "kwargs": kwargs,
            "env": self.prep_command_env()
        }) + "\n"
        request = request.encode()

        # Create a socket (SOCK_STREAM means a TCP socket)
        mode = infer_mode(self.conn)
        # print(f"Sending request over {mode}")
        if mode == "Unix" and not os.path.exists(self.conn):
            raise ValueError(f"socket file {self.conn} doesn't exist")
        with socket.socket(self.mode, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect(self.conn)
            sock.settimeout(self.timeout)
            sock.sendall(request)
            # Receive data from the server and shut down
            body = b''
            while b'\n' not in body:
                body = body + sock.recv(1024)


        return json.loads(body.strip().decode())

    @classmethod
    def print_response(cls, response):
        msg = response.get("stdout", "")
        if len(msg) > 0: print(msg, file=sys.stdout)
        msg = response.get("stderr", "")
        if len(msg) > 0: print(msg, file=sys.stderr)

    def call(self, command, *args, **kwargs):
        return self.communicate(command, args, kwargs)

class NodeCommHandler(socketserver.StreamRequestHandler):

    def handle(self):
        try:
            # self.rfile is a file-like object created by the handler;
            # we can now use e.g. readline() instead of raw recv() calls
            self.data = self.rfile.readline().strip()
            response = self.handle_json_request(self.data)
            # Likewise, self.wfile is a file-like object used to write back
            # to the client
        except:
            response = {
                "stdout": "",
                "stderr": traceback.format_exc(limit=1)
            }
        try:
            self.wfile.write(json.dumps(response).encode() + b'\n')
        except:
            traceback.print_exc(limit=1)  # big ol' fallback

    def handle_json_request(self, message: bytes):
        try:
            request = json.loads(message.decode())
        except:
            response = {
                "stdout": "",
                "stderr": traceback.format_exc(limit=1)
            }
        else:
            # comm = request.get("command", '<unknown>')
            # args = request.get("args", [])
            env = request.get("env", {})
            # print(f"Got: {comm} {args}")
            response = self.dispatch_request(request, env)
            # print(f"Sending: {response}")

        return response

    def setup_env(self, env):
        ...

    @property
    def method_dispatch(self):
        return self.get_methods()

    def dispatch_request(self, request: dict, env: dict):
        method = request.get("command", None)
        if method is None:
            response = {
                "stdout": "",
                "stderr": f"no command specified"
            }
        else:
            caller = self.method_dispatch.get(method.lower(), None)
            if caller is None:
                response = {
                    "stdout": "",
                    "stderr": f"unknown command {method}"
                }
            else:
                args = request.get("args", [])
                kwargs = request.get("kwargs", {})
                # if args is None:
                #     response = {
                #         "stdout": "",
                #         "stderr": f"malformatted request {request}"
                #     }
                # else:
                try:
                    self.setup_env(env)
                    response = caller(args, kwargs)
                except:
                    response = {
                        "stdout": "",
                        "stderr": traceback.format_exc(limit=1)
                    }

        return response


    @abc.abstractmethod
    def get_methods(self) -> 'dict[str,method]':
        ...

    @staticmethod
    def get_valid_port(git_port, min_port=4000, max_port=65535):
        git_port = int(git_port)
        if git_port > max_port:
            git_port = git_port % max_port
        if git_port < min_port:
            git_port = max_port - (git_port % (max_port - min_port))
        return git_port

    @classmethod
    def get_default_connection(cls, port=None, hostname='localhost', session_var='SESSION_ID'):
        if port is None:
            port = os.environ.get(cls.DEFAULT_PORT_ENV_VAR, os.environ.get(session_var))
            if port is None:
                raise ValueError(f"`{cls.DEFAULT_PORT_ENV_VAR}` must be set at the environment level")
        port = cls.get_valid_port(port)

        return (hostname, port)

    TCP_SERVER = NodeCommTCPServer
    UNIX_SERVER = NodeCommUnixServer
    DEFAULT_CONNECTION = ("localhost", 9999)
    DEFAULT_PORT_ENV_VAR = None
    DEFAULT_SOCKET_ENV_VAR = None

    DEFAULT_CONNECTION_FILE_ENV_VAR = None

    @classmethod
    def serialize_connection(cls, connection, mode):
        """Build a JSON-serializable dict describing the connection."""
        details = {"mode": mode}
        if mode == "TCP":
            details["hostname"] = connection[0]
            details["port"] = connection[1]
        elif mode == "Unix":
            details["path"] = connection
        return details

    @classmethod
    def write_connection_file(cls, connection_file, connection, mode):
        """Write the connection details out as JSON for clients to consume."""
        details = cls.serialize_connection(connection, mode)
        tmp = connection_file + ".tmp"
        with open(tmp, "w") as f:
            json.dump(details, f, indent=2)
        os.replace(tmp, connection_file)  # atomic write
        return details

    @classmethod
    def read_connection_file(cls, connection_file):
        """Read connection details written by `start_server` and return a
        connection spec usable by a client (tuple for TCP, str path for Unix)."""
        with open(connection_file) as f:
            details = json.load(f)
        mode = details.get("mode")
        if mode == "TCP":
            return (details["hostname"], details["port"])
        elif mode == "Unix":
            return details["path"]
        else:
            raise ValueError(f"invalid connection file contents {details}")

    @classmethod
    def start_server(cls, connection=None, port=None, connection_file=None):
        # Create the server, binding to localhost on port 9999
        if connection is None and cls.DEFAULT_SOCKET_ENV_VAR is not None:
            connection = os.environ.get(cls.DEFAULT_SOCKET_ENV_VAR)
        if connection is None:
            if port is None and cls.DEFAULT_PORT_ENV_VAR:
                port = os.environ.get(cls.DEFAULT_PORT_ENV_VAR)
            if port is not None:
                connection = ('localhost', cls.get_valid_port(port))
        if connection is None:
            connection = cls.DEFAULT_CONNECTION
        if connection_file is None and cls.DEFAULT_CONNECTION_FILE_ENV_VAR is not None:
            connection_file = os.environ.get(cls.DEFAULT_CONNECTION_FILE_ENV_VAR)
        mode = infer_mode(connection)
        # print(f"Starting server at {connection} over {mode}")
        if mode == "TCP":
            server_type = cls.TCP_SERVER
        elif mode == "Unix":
            server_type = cls.UNIX_SERVER
        else:
            raise NotImplementedError(mode)
        with server_type(connection, cls) as server:
            # the bound address may differ from the requested one
            # (e.g. port 0 -> OS-assigned port), so report what we actually got
            bound_connection = server.server_address
            if mode == "TCP":
                bound_connection = tuple(bound_connection)
            if connection_file is not None:
                cls.write_connection_file(connection_file, bound_connection, mode)
            try:
                # Activate the server; this will keep running until you
                # interrupt the program with Ctrl-C
                server.serve_forever()
            finally:
                if connection_file is not None:
                    try:
                        os.remove(connection_file)
                    except OSError:
                        ...
                if mode == "Unix":
                    try:
                        os.remove(connection)
                    except OSError:
                        ...

    @staticmethod
    def _convert_value(val):
        # Try JSON first so ints, floats, bools, null, lists, and objects all
        # come through with their natural types; fall back to the raw string.
        try:
            return json.loads(val)
        except (ValueError, TypeError):
            return val

    @classmethod
    def parse_kwargs(cls, extra):
        """Convert leftover ``--`` tokens into a kwargs dict.

        Supports ``--key value``, ``--key=value``, and bare ``--flag`` (-> True).
        Values are run through JSON parsing for automatic type conversion, so
        ``--count 3`` yields ``{'count': 3}`` and ``--name foo`` yields
        ``{'name': 'foo'}``.
        """
        kwargs = {}
        i = 0
        n = len(extra)
        while i < n:
            tok = extra[i]
            if not tok.startswith("--"):
                raise ValueError(f"expected a --key token in kwargs, got {tok!r}")
            key = tok[2:]
            if "=" in key:  # --key=value
                k, v = key.split("=", 1)
                kwargs[k] = cls._convert_value(v)
                i += 1
            elif i + 1 < n and not extra[i + 1].startswith("--"):  # --key value
                kwargs[key] = cls._convert_value(extra[i + 1])
                i += 2
            else:  # bare --flag
                kwargs[key] = True
                i += 1
        return kwargs

    @classmethod
    def build_arg_parser(cls):
        import argparse
        parser = argparse.ArgumentParser(
            prog=cls.__name__,
            description="Launch a comm server, or call a running one as a client.",
        )
        parser.add_argument(
            "--start-server", action="store_true",
            help="launch the server instead of acting as a client",
        )
        parser.add_argument(
            "--socket", default=None,
            help="Unix-domain socket path (takes priority over --host/--port)",
        )
        parser.add_argument(
            "--port", type=int, default=None,
            help="TCP port to bind/connect to",
        )
        parser.add_argument(
            "--host", default="localhost",
            help="TCP hostname (default: localhost; used with --port)",
        )
        parser.add_argument(
            "--connection-file", default=None,
            help="path to read/write JSON connection details",
        )
        parser.add_argument(
            "--timeout", type=float, default=10,
            help="client socket timeout in seconds (default: 10)",
        )
        parser.add_argument(
            "command", nargs="?", default=None,
            help="command to invoke in client mode",
        )
        # positional args for the command, plus any trailing --kwargs
        parser.add_argument(
            "args", nargs=argparse.REMAINDER, default=[],
            help="positional args, then --key value pairs become kwargs",
        )
        return parser

    @classmethod
    def resolve_connection(cls, socket=None, host="localhost", port=None):
        """Pick a connection spec from CLI options.

        Priority: --socket (Unix) > --host/--port (TCP) > class defaults.
        """
        if socket is not None:
            return socket
        if port is not None:
            return (host, cls.get_valid_port(port))
        return None  # let start_server / client_request fall back to defaults

    @classmethod
    def main(cls, argv=None):
        parser = cls.build_arg_parser()
        ns = parser.parse_args(argv)

        connection = cls.resolve_connection(
            socket=ns.socket, host=ns.host, port=ns.port
        )

        if ns.start_server:
            # `command`/`args` are meaningless when starting a server
            setup_server(
                cls,
                connection=connection,
                port=ns.port,
                connection_file=ns.connection_file,
            )
            return 0

        # ---- client mode ----
        if ns.command is None:
            parser.error("a command is required in client mode (or pass --start-server)")

        # argparse.REMAINDER collects everything after `command`; split it into
        # leading positionals and the trailing --kwargs section.
        rest = list(ns.args)
        pos_args = []
        idx = 0
        while idx < len(rest) and not rest[idx].startswith("--"):
            pos_args.append(rest[idx])
            idx += 1
        kwargs = cls.parse_kwargs(rest[idx:])

        if connection is None:
            if ns.connection_file is not None:
                connection = cls.read_connection_file(ns.connection_file)
            else:
                connection = cls.DEFAULT_CONNECTION

        client = cls.client_class(connection, timeout=ns.timeout)
        response = client.communicate(ns.command, pos_args, kwargs)
        cls.client_class.print_response(response)
        # surface a failure exit code when the server reported on stderr
        return 1 if response.get("stderr") else 0

    @classmethod
    def resolve_roots(cls, base, roots=None, allowed_domains=None):
        if roots is None:
            roots = set()
        if allowed_domains is None:
            allowed_domains = base.__module__.split('.', 1)[:1]
        roots.add(base)
        for b in base.__bases__:
            if b not in roots and any(b.__module__.startswith(d) for d in allowed_domains):
                cls.resolve_roots(b, roots=roots, allowed_domains=allowed_domains)
        return roots

    @classmethod
    def create_server_package(cls,
                              hostpath,
                              package_name=None,
                              overwrite=False,
                              dependency_paths=None):
        # creates a host path that packages in just these core files
        # along with a cli template
        if package_name is None:
            package_name = cls.__name__

        target = os.path.join(hostpath, package_name)
        if os.path.exists(target):
            if not overwrite:
                raise FileExistsError(f"can't overwrite {target}")

        if dependency_paths is None:
            dependencies = cls.resolve_roots(cls)
            dependency_paths = {sys.modules[c.__module__].__file__ for c in dependencies}

        os.makedirs(target, exist_ok=True)
        for f in dependency_paths:
            new_f = os.path.join(target, os.path.basename(f))
            shutil.copy(f, new_f)

        with open(os.path.join(target, '__init__.py'), 'w+') as f:
            targ = os.path.basename(sys.modules[cls.__module__].__file__)
            name = cls.__name__
            f.write(f"from .{targ} import {name}")

        with open(os.path.join(target, '__main__.py'), 'w+') as f:
            targ = os.path.basename(sys.modules[cls.__module__].__file__)
            name = cls.__name__
            f.writelines([
                f"from .{targ} import {name}",
                f'if __name__ == "__main__": {name}.main()',
            ])

        return target

    class MultiprocessingServerContext:
        def __init__(self, proc:mp.Process, timeout=3):
            self.proc = proc
            self.timeout = timeout

        def __enter__(self):
            self.proc.start()
            time.sleep(self.timeout)
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            # self.proc.join(timeout=self.timeout)
            self.proc.kill()
    @classmethod
    def start_multiprocessing_server(cls, connection=None, port=None, timeout=3, connection_file=None):
        proc = mp.Process(
            target=cls.start_server,
            kwargs={'connection': connection, 'port': port, 'connection_file': connection_file}
        )
        return cls.MultiprocessingServerContext(proc, timeout=timeout)

    client_class = NodeCommClient
    @classmethod
    def client_request(cls, *args, client_class=None, connection=None, connection_file=None):
        if client_class is None:
            client_class = cls.client_class
        if connection is None and connection_file is not None:
            connection = cls.read_connection_file(connection_file)
        if connection is None:
            connection = cls.DEFAULT_CONNECTION
        return client_class(connection).communicate(*args)

class ShellCommHandler(NodeCommHandler):

    @classmethod
    def subprocess_response(cls, command, args):
        pipes = subprocess.Popen([command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        std_out, std_err = pipes.communicate()
        return {
            "stdout": std_out.strip().decode(),
            "stderr": std_err.strip().decode()
        }

    @staticmethod
    def kwargs_to_cli(kwargs):
        """Convert a kwargs dict into GNU/sbatch-style CLI flags.

        - single-char key  -> ``-k value``  (or bare ``-k`` for True)
        - multi-char key   -> ``--key=value`` (or bare ``--key`` for True)
        - underscores in keys become dashes (``job_name`` -> ``--job-name``)
        - ``True``          -> bare flag with no value
        - ``False``/``None`` -> flag omitted entirely
        - list/tuple value  -> flag repeated once per element
        """
        flags = []

        def emit(key, value):
            dashed = str(key).replace("_", "-")
            short = len(dashed) == 1
            prefix = f"-{dashed}" if short else f"--{dashed}"
            if value is True:
                flags.append(prefix)
            elif value is False or value is None:
                return
            elif short:
                flags.extend([prefix, str(value)])
            else:
                flags.append(f"{prefix}={value}")

        for key, value in (kwargs or {}).items():
            if isinstance(value, (list, tuple)):
                for v in value:
                    emit(key, v)
            else:
                emit(key, value)
        return flags

    @property
    def method_dispatch(self):
        return dict(
            {
                "cd": self.change_pwd,
                "pwd": self.get_pwd
            },
            **self.get_methods()
        )

    def change_pwd(self, args, kwargs):
        os.chdir(args[0])
        return {
            'stdout': "",
            'stderr': ""
        }

    def get_pwd(self, args, kwargs):
        cwd = os.getcwd()
        return {
            'stdout': cwd,
            'stderr': ""
        }

    def setup_env(self, env):
        if 'pwd' in env:
            os.chdir(env['pwd'])

    @abc.abstractmethod
    def get_subprocess_call_list(self):
        ...

    def get_methods(self) -> 'dict[str,method]':
        return {
            k: self._wrap_subprocess_call(v)
            for k, v in self.get_subprocess_call_list()
        }

    def _wrap_subprocess_call(self, command):
        # dispatch_request calls handlers as `caller(args, kwargs)`, where
        # `args` is the list of CLI args and `kwargs` the keyword dict.
        # kwargs are converted to CLI flags and placed before the positional
        # args (matching sbatch/GNU convention: options precede operands).
        if isinstance(command, str):
            # a bare command name, e.g. "sbatch"
            def wrapped(args, kwargs, _cmd=command):
                return self.subprocess_response(_cmd, [*self.kwargs_to_cli(kwargs), *args])
            return wrapped
        elif not callable(command):
            # a command given as a list/tuple of leading tokens,
            # e.g. ("git", "status") -> prepend them before the request args
            def wrapped(args, kwargs, _cmd=list(command)):
                return self.subprocess_response(
                    _cmd[0], [*_cmd[1:], *self.kwargs_to_cli(kwargs), *args]
                )
            return wrapped
        return command


def setup_server(handler_class, connection=None, port=None, ppid=None, hostname=None, connection_file=None):
    if connection is None:
        connection = handler_class.get_default_connection(port, hostname)
    if ppid is None:
        ppid = os.environ.get("PARENT_PROCESS_ID")
    if ppid is not None:
        curpid = os.environ.get("WORKER_PROCESS_ID", os.getpid())
        setup_parent_terminated_listener(ppid, curpid)

    try:
        handler_class.start_server(connection=connection, connection_file=connection_file)
    except OSError:  # server exists
        print(f"Already serving on {connection}")
        pass

def handle_command_line(handler_class, client_class, connection=None, port=None, ppid=None, hostname=None,
                        connection_file=None):
    import sys, os

    if connection is None:
        connection = handler_class.get_default_connection(port, hostname)

    if len(sys.argv) == 1:
        setup_server(handler_class, connection=connection, ppid=ppid, connection_file=connection_file)
    else:
        client_class.print_response(
            client_class.client_request(sys.argv[1], sys.argv[2:], connection=ppid)
        )