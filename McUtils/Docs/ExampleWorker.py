"""
Worker process for `SubprocessExampleRunner`: ``python -m McUtils.Docs.ExampleWorker``.

Reads one JSON job from stdin, runs the page's examples with an in-process `ExampleRunner`, and reports
progress as one JSON object per line on the *original* stdout. Anything the examples (or the libraries
they import) write to the process's stdout/stderr, including from C code, goes to stderr instead, so it
can never corrupt that protocol. This module is deliberately not imported by the package ``__init__``,
so running it with ``-m`` doesn't import it twice.
"""

import json, os, sys, traceback

__all__ = ["main"]

# Events: {"event": "ready"}, {"event": "start", "id"}, {"event": "result", "id", "status", "reason",
# "blocked_by", "meta"}, {"event": "done"}, {"event": "fatal", "error"}.


def main(argv=None):
    import faulthandler
    faulthandler.enable()  # a segfault in native code leaves a Python traceback in the stderr log
    proto = os.fdopen(os.dup(1), "w", encoding="utf-8", buffering=1)
    os.dup2(2, 1)  # stray writes to stdout land in the stderr log
    devnull = os.open(os.devnull, os.O_RDONLY)

    def emit(**event):
        proto.write(json.dumps(event, default=str) + "\n")
        proto.flush()

    try:
        job = json.loads(sys.stdin.read())
        os.dup2(devnull, 0)  # an example calling input() gets EOF instead of hanging
        for p in reversed(job.get("sys_path") or []):
            if p and p not in sys.path:
                sys.path.insert(0, p)
        from McUtils.Docs.Examples import ExampleParser, ExampleRunner, ReadoutStore
        store = ReadoutStore(job["store"])
        runner = ExampleRunner(
            store, revisions=job.get("revisions"), style=job.get("style"), x3dom_path=job.get("x3dom_path"),
            css=job.get("css", "inline"), seed=job.get("seed", True), timeout=job.get("timeout"),
            max_output=job.get("max_output", 20000)
        )
        parsed = ExampleParser.parse(job["text"], owner=job.get("owner"), first_line=job.get("first_line", 1))
        emit(event="ready")

        def on_event(event, block, result=None):
            if event == "start":
                emit(event="start", id=block.id)
            else:
                emit(event="result", id=block.id, status=result.status, reason=result.reason,
                     blocked_by=result.blocked_by, meta=result.meta)

        runner.run_page(parsed, refresh=job.get("refresh", False), sync=False, on_event=on_event)
        emit(event="done")
        return 0
    except BaseException:
        emit(event="fatal", error=traceback.format_exc())
        return 3


if __name__ == "__main__":
    sys.exit(main())
