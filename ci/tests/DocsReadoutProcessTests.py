"""Running documentation examples in a worker process: results, limits, crashes, protocol hygiene."""

import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from unittest import mock

from McUtils.Docs.Examples import ExampleRunner, ExampleParser, ReadoutStore
from McUtils.Docs.ExampleProcess import ExampleWorkerCrash, ExampleWorkerError, SubprocessExampleRunner


def block(id, code, **options):
    opts = ", ".join(["id={!r}".format(id)] + ["{}={!r}".format(k, v) for k, v in options.items()])
    return "<!-- readout({}) -->\n```python\n{}\n```\n\n".format(opts, textwrap.dedent(code).strip("\n"))


class ProcessTestBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.store = ReadoutStore(os.path.join(self._tmp.name, "readouts"))

    def runner(self, **kw):
        kw.setdefault("timeout", 20)
        kw.setdefault("kill_grace", 3)
        return SubprocessExampleRunner(self.store, **kw)

    def statuses(self, results):
        return {r.block.id: r.status for r in results}

    def error_of(self, result):
        return result.meta["error"]


class SubprocessRunnerTests(ProcessTestBase):
    def test_runs_a_page_in_a_worker_and_stores_the_output(self):
        text = "Intro\n\n" + block("a", "import numpy as np\nx = {'n': 3, 'v': np.arange(3.)}\nx") + block("b", "x['n'] + 1")
        results = self.runner().run_text(text, owner="demo")
        self.assertEqual(self.statuses(results), {"a": "ok", "b": "ok"})
        a, b = [r.block for r in results]
        self.assertTrue(self.store.has_file(a.key, "fragment.html"))
        self.assertIn("v", self.store.read_file(a.key, "readout.txt"))   # namespace shared, output real
        self.assertEqual(self.store.load_manifest()["entries"]["b"]["status"], "ok")
        self.assertEqual(results[0].meta["python"], sys.version.split()[0])

    def test_nothing_to_do_means_no_process(self):
        text = block("a", "{'k': 1}")
        self.runner().run_text(text)
        with mock.patch.object(subprocess, "Popen", side_effect=AssertionError("a worker was started")):
            self.assertEqual(self.runner().run_text(text), [])

    def test_same_output_as_the_in_process_runner(self):
        text = block("a", "import random\nimport numpy as np\n{'r': random.random(), 'n': float(np.random.rand())}")
        other = ReadoutStore(os.path.join(self._tmp.name, "inproc"))
        (inproc,) = ExampleRunner(other, timeout=20).run_text(text)
        (sub,) = self.runner().run_text(text)
        self.assertEqual(inproc.block.key, sub.block.key)
        self.assertEqual(other.read_file(inproc.block.key, "readout.txt"), self.store.read_file(sub.block.key, "readout.txt"))
        self.assertEqual(other.read_file(inproc.block.key, "fragment.html"), self.store.read_file(sub.block.key, "fragment.html"))

    def test_errors_are_cached_and_the_chain_is_blocked(self):
        text = block("a", "x = 1", display="none") + block("boom", "1/0") + block("after", "x") + block("other", "{'ok': 1}", isolated=True)
        runner = self.runner()
        results = runner.run_text(text)
        self.assertEqual(self.statuses(results), {"a": "ok", "boom": "error", "after": "blocked", "other": "ok"})
        err = self.error_of(results[1])
        self.assertEqual(err["type"], "ZeroDivisionError")
        self.assertIn("1/0", err["traceback"])
        self.assertEqual(results[2].blocked_by, "boom")
        # nothing is stored for the blocked block, and the cached failure is not re-run: no worker is needed
        # to say that `after` is still blocked
        with mock.patch.object(subprocess, "Popen", side_effect=AssertionError("worker started")):
            again = self.runner().run_text(text)
        self.assertEqual(self.statuses(again), {"after": "blocked"})
        self.assertFalse(self.store.has(results[2].block.key))

    def test_blocked_blocks_do_not_replay_their_broken_chain(self):
        text = block("a", "print('replayed a')\nx = 1", display="none") + block("boom", "1/0") + block("after", "x")
        self.runner().run_text(text)
        with mock.patch.object(subprocess, "Popen", side_effect=AssertionError("worker started")):
            results = self.runner().run_text(text, refresh="after")
        self.assertEqual(self.statuses(results), {"after": "blocked"})
        self.assertEqual(results[0].blocked_by, "boom")

    def test_refreshing_the_failed_block_itself_does_run_it_again(self):
        text = block("a", "x = 1", display="none") + block("boom", "1/0") + block("after", "x")
        self.runner().run_text(text)
        results = self.runner().run_text(text, refresh="boom")
        self.assertEqual(self.statuses(results), {"boom": "error", "after": "blocked"})

    def test_soft_timeout_inside_the_worker(self):
        text = block("slow", "import time\ntime.sleep(30)", timeout=1) + block("fine", "{'ok': 1}", isolated=True)
        results = self.runner().run_text(text)
        self.assertEqual(self.statuses(results), {"slow": "error", "fine": "ok"})
        self.assertEqual(self.error_of(results[0])["type"], "ExampleTimeout")

    def test_a_hung_example_is_killed_and_the_rest_of_the_page_still_runs(self):
        hang = """
            import signal
            signal.signal(signal.SIGALRM, signal.SIG_IGN)   # the in-worker timeout can't interrupt this
            while True:
                pass
            """
        text = (block("a", "x = 1", display="none") + block("hang", hang, timeout=1) + block("after", "x")
                + block("fine", "{'ok': 1}", isolated=True))
        results = self.runner(kill_grace=2).run_text(text)
        self.assertEqual(self.statuses(results), {"a": "ok", "hang": "error", "after": "blocked", "fine": "ok"})
        err = self.error_of(results[1])
        self.assertEqual(err["type"], "ExampleWorkerCrash")
        self.assertIn("killed", err["message"])
        self.assertEqual(results[2].blocked_by, "hang")

    def test_a_crashing_example_is_reported_with_the_workers_stderr(self):
        crash = """
            import os
            os.write(2, b"last words from the example\\n")   # straight to the worker's stderr
            os._exit(7)
            """
        text = block("crash", crash) + block("fine", "{'ok': 1}", isolated=True)
        results = self.runner().run_text(text)
        self.assertEqual(self.statuses(results), {"crash": "error", "fine": "ok"})
        message = self.error_of(results[0])["message"]
        self.assertIn("exit code 7", message)
        self.assertIn("last words from the example", message)

    def test_page_timeout_bounds_examples_without_their_own_limit(self):
        text = block("nap", "import time\ntime.sleep(60)") + block("fine", "{'ok': 1}", isolated=True)
        results = self.runner(timeout=None, page_timeout=2).run_text(text)
        self.assertEqual(self.statuses(results), {"nap": "error", "fine": "ok"})
        self.assertIn("page time limit", self.error_of(results[0])["message"])

    def test_stray_output_and_stdin_cannot_break_the_worker(self):
        code = """
            import os
            os.write(1, b"raw bytes written straight to fd 1\\n")
            print("printed text")
            try:
                input()
            except EOFError:
                got = "eof"
            {"input": got}
            """
        (result,) = self.runner().run_text(block("noisy", code, display="both"))
        self.assertEqual(result.status, "ok")
        self.assertEqual(result.meta["stdout"].strip(), "printed text")
        self.assertIn("eof", self.store.read_file(result.block.key, "readout.txt"))

    def test_a_worker_that_never_becomes_ready_is_an_error_not_a_hang(self):
        runner = self.runner(startup_timeout=0.001)
        with self.assertRaises(ExampleWorkerError):
            runner.run_text(block("a", "{'k': 1}"))

    def test_stylesheet_mode_publishes_one_shared_css(self):
        text = block("a", "{'k': 1}") + block("b", "{'k': 2}")
        results = self.runner(css="stylesheet").run_text(text)
        self.assertTrue(all(r.ok for r in results))
        self.assertIsNotNone(self.store.stylesheet_md5())
        self.assertNotIn("<style", self.store.read_file(results[0].block.key, "fragment.html"))

    def test_the_worker_reads_and_writes_the_same_store_as_the_parent(self):
        text = block("a", "{'k': 1}")
        self.runner().run_text(text)
        # a changed example gets its own entry; the old one is left for --prune
        self.runner().run_text(text.replace("'k': 1", "'k': 2"))
        self.assertEqual(len(self.store.keys()), 2)


if __name__ == "__main__":
    unittest.main()
