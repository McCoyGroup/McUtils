"""
Runs documentation examples in a worker process, so a crash, hang or ``sys.exit`` in an example can't
take the documentation build down.
"""

import json, os, queue, re, signal, subprocess, sys, tempfile, threading, time

from .Examples import ExampleCache, ExampleError, ExampleResult, ExampleRunner, ExampleParser

__all__ = [
    "ExampleWorkerError",
    "ExampleWorkerCrash",
    "SubprocessExampleRunner"
]


class ExampleWorkerError(ExampleError):
    """The worker process couldn't do its job at all (e.g. it failed before running anything)."""


class ExampleWorkerCrash(ExampleError):
    """The worker process died or had to be killed while running an example."""


def _glob_escape(text):
    return re.sub(r"([*?\[])", r"[\1]", text)


class SubprocessExampleRunner:
    """
    The same interface as `ExampleRunner` (``plan``, ``run_text``, ``run_page``), but each page runs in its
    own ``python -m McUtils.Docs.ExampleWorker`` process.

    The parent plans from the store, so a page with nothing to do never starts a process. The worker
    reports one event per block; the parent enforces limits on top of the in-worker ``SIGALRM`` timeout
    (which can't interrupt native code):

    * a block that runs longer than its timeout plus ``kill_grace`` seconds gets the worker killed,
    * the worker has ``startup_timeout`` seconds to import everything and report ready,
    * ``page_timeout`` (optional) bounds the whole page.

    A block that was running when the worker died or was killed is recorded as an error (cached, like any
    other failure), the rest of its chain is reported ``blocked``, and the remaining chains are run by a
    fresh worker.

    :param store: the `ReadoutStore`
    :param timeout: default per-block limit in seconds (a marker's ``timeout`` overrides it)
    :param python: the interpreter to run (default: the current one)
    :param sys_path: extra import paths for the worker (default: the parent's ``sys.path``)
    :param cwd: working directory of the worker
    :param env: extra environment variables for the worker
    :param revisions, style, x3dom_path, css, seed, max_output, imports: as for `ExampleRunner`
    """

    def __init__(self, store, revisions=None, style=None, x3dom_path=None, css="inline", seed=True,
                 timeout=None, page_timeout=None, kill_grace=15.0, startup_timeout=120.0, python=None,
                 sys_path=None, cwd=None, env=None, max_output=20000, verbose=False, stream=None, imports=True):
        # an in-process runner is used for planning and to record failures the worker couldn't
        self.local = ExampleRunner(store, revisions=revisions, style=style, x3dom_path=x3dom_path, css=css,
                                   seed=seed, timeout=timeout, max_output=max_output, imports=imports)
        self.store = store
        self.cache = self.local.cache
        self.revisions = dict(revisions or {})
        self.style = style
        self.x3dom_path = x3dom_path
        self.css = css
        self.seed = seed
        self.imports = imports
        self.timeout = timeout
        self.page_timeout = page_timeout
        self.kill_grace = kill_grace
        self.startup_timeout = startup_timeout
        self.python = python or sys.executable
        self.sys_path = [p for p in (sys.path if sys_path is None else sys_path) if p]
        self.cwd = cwd
        self.env = dict(env or {})
        self.max_output = max_output
        self.verbose = verbose
        self.stream = stream
        self.last_log = ""

    # ---- same interface as ExampleRunner ---- #
    def plan(self, parsed, refresh=False):
        return self.cache.plan(parsed.blocks, refresh)

    def run_text(self, text, owner=None, refresh=False, first_line=1):
        return self.run_page(ExampleParser.parse(text, owner=owner, first_line=first_line), refresh=refresh)

    def run_page(self, parsed, refresh=False, sync=True):
        blocks = parsed.blocks
        by_id = {b.id: b for b in blocks}
        reasons = {b.id: r for b, r in self.cache.plan(blocks, refresh)}
        results = {}
        log = []
        passes = 0
        while True:
            remaining = [i for i in reasons if i not in results]
            if not remaining:
                break
            pass_refresh = refresh if passes == 0 else [_glob_escape(i) for i in remaining]
            _, need, doomed = self.local.analyse(parsed, pass_refresh)
            for i, culprit in doomed.items():
                results.setdefault(i, ExampleResult(by_id[i], "blocked", reason=reasons.get(i), blocked_by=culprit))
            if not need:
                break  # nothing left that has to execute, so no worker is needed
            passes += 1
            if passes > len(blocks) + 1:
                raise ExampleWorkerError("example worker kept failing; giving up on {}".format(remaining))
            events, running, finished, fatal, stderr_tail = self._run_worker(parsed, pass_refresh, by_id)
            log.append(stderr_tail)
            for ev in events:
                if ev["event"] == "result" and ev["id"] in reasons and ev["id"] not in results:
                    results[ev["id"]] = ExampleResult(
                        by_id[ev["id"]], ev["status"], ev.get("meta"), ev.get("reason"), ev.get("blocked_by")
                    )
            if finished:
                break
            if fatal is not None and running is None:
                raise ExampleWorkerError("example worker failed before running anything:\n" + fatal)
            if running is None:
                raise ExampleWorkerError(
                    "example worker exited without finishing and without running anything:\n" + stderr_tail
                )
            if running in results:
                continue  # it had reported its result just as the process went away
            message = fatal or self._crash_message
            if stderr_tail.strip():
                message += "\n--- worker stderr (tail) ---\n" + stderr_tail
            results[running] = self.local._record_error(
                by_id[running], ExampleWorkerCrash(message), reasons.get(running, "missing")
            )
        self.last_log = "\n".join(l for l in log if l.strip())
        if sync:
            self.cache.sync_manifest(blocks)
        return [results[b.id] for b in blocks if b.id in results]

    # ---- the process ---- #
    _crash_message = "the worker process died while running this example"

    def _job(self, parsed, refresh):
        return {
            "text": str(parsed), "owner": parsed.owner, "first_line": parsed.first_line, "refresh": refresh,
            "store": self.store.root, "revisions": self.revisions, "style": self.style,
            "x3dom_path": self.x3dom_path, "css": self.css, "seed": self.seed, "timeout": self.timeout,
            "max_output": self.max_output, "sys_path": self.sys_path, "imports": self.imports,
        }

    def _environment(self):
        env = dict(os.environ)
        here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        paths = [here] + [p for p in env.get("PYTHONPATH", "").split(os.pathsep) if p]
        env["PYTHONPATH"] = os.pathsep.join(paths)
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env.update(self.env)
        return env

    def _block_limit(self, block):
        limit = block.options.get("timeout", self.timeout)
        return None if limit is None else limit + self.kill_grace

    def _run_worker(self, parsed, refresh, by_id):
        """Runs one worker; returns ``(events, running_id, finished, fatal_text, stderr_tail)``."""
        job = self._job(parsed, refresh)
        errfile = tempfile.TemporaryFile(mode="w+b")
        posix = os.name == "posix"
        proc = subprocess.Popen(
            [self.python, "-m", "McUtils.Docs.ExampleWorker"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=errfile, cwd=self.cwd, env=self._environment(), start_new_session=posix,
        )
        lines = queue.Queue()

        def pump():
            for raw in proc.stdout:
                lines.put(raw)
            lines.put(None)

        reader = threading.Thread(target=pump, daemon=True)
        reader.start()
        try:
            proc.stdin.write(json.dumps(job).encode("utf-8"))
            proc.stdin.close()
        except OSError:
            pass  # the worker died early; its stderr explains
        events = []
        running = None
        finished = False
        fatal = None
        ready = False
        start = time.monotonic()
        page_deadline = None if self.page_timeout is None else start + self.page_timeout
        block_deadline = None
        startup_deadline = start + self.startup_timeout
        killed_for = None
        while True:
            deadlines = [d for d in (page_deadline, block_deadline, None if ready else startup_deadline)
                         if d is not None]
            wait = None if not deadlines else max(0.0, min(deadlines) - time.monotonic())
            try:
                raw = lines.get(timeout=wait)
            except queue.Empty:
                now = time.monotonic()
                if page_deadline is not None and now >= page_deadline:
                    killed_for = "the page time limit of {} s".format(self.page_timeout)
                elif block_deadline is not None and now >= block_deadline:
                    killed_for = "its time limit (plus {} s of grace)".format(self.kill_grace)
                else:
                    killed_for = "startup ({} s)".format(self.startup_timeout)
                self._kill(proc)
                break
            if raw is None:
                break
            try:
                ev = json.loads(raw.decode("utf-8"))
            except ValueError:
                continue
            kind = ev.get("event")
            if self.verbose and self.stream is not None and kind in ("start", "result"):
                print("  {} {}{}".format(kind, ev.get("id"), "" if kind == "start" else " -> " + ev.get("status", "")),
                      file=self.stream)
            if kind == "ready":
                ready = True
            elif kind == "start":
                running = ev["id"]
                block_deadline = None
                if running in by_id:
                    limit = self._block_limit(by_id[running])
                    block_deadline = None if limit is None else time.monotonic() + limit
            elif kind == "result":
                events.append(ev)
                if ev["id"] == running:
                    running = None
                    block_deadline = None
            elif kind == "done":
                finished = True
            elif kind == "fatal":
                fatal = ev.get("error", "")
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self._kill(proc)
            proc.wait()
        reader.join(timeout=2)
        proc.stdout.close()
        errfile.seek(0)
        stderr_tail = errfile.read()[-4000:].decode("utf-8", "replace")
        errfile.close()
        if not finished:
            if killed_for is not None:
                self._crash_message = (
                    "the worker was killed after this example exceeded {} without returning "
                    "(it may be stuck in native code)".format(killed_for)
                )
            else:
                code = proc.returncode
                what = "exit code {}".format(code)
                if code is not None and code < 0:
                    try:
                        what = "signal {}".format(signal.Signals(-code).name)
                    except ValueError:
                        pass
                self._crash_message = "the worker process died ({}) while running this example".format(what)
        return events, running, finished, fatal, stderr_tail

    @staticmethod
    def _kill(proc):
        try:
            if os.name == "posix":
                os.killpg(proc.pid, signal.SIGKILL)
            else:
                proc.kill()
        except (OSError, ProcessLookupError):
            pass
