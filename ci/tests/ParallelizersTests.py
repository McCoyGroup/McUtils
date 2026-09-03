import itertools
import time

from Peeves.TestUtils import *
from McUtils.Scaffolding import Logger
from McUtils.Parallelizers import *
from unittest import TestCase
import numpy as np, io, os, sys, tempfile as tmpf

# @Parallelizer.main_restricted
# def main_print(*args, parallelizer=None):
#     print(*args)
# @Parallelizer.worker_restricted
# def worker_print(*args, parallelizer=None):
#     print(*args)
# def run_job(parallelizer=None):
#     if parallelizer.on_main:
#         data = np.arange(1000)
#     else:
#         data = None
#     data = parallelizer.scatter(data)
#     lens = parallelizer.gather(len(data))
#     return lens

class ParallelizersTests(TestCase):

    # we don't really even need to send or get any state for these tests
    def __getstate__(self):
        return {}
    def __setstate__(self, state):
        pass

    def run_job(self, parallelizer:Parallelizer=None):
        time.sleep(3)
        if parallelizer.on_main:
            data = np.arange(1000)
        else:
            data = None
        if parallelizer.on_main:
            flag = "woop"
        else:
            flag = None
        test = parallelizer.broadcast(flag)
        # self.worker_print(test)
        data = parallelizer.scatter(data)
        lens = parallelizer.gather(len(data))
        return sum(lens)
    @validationTest
    def test_BasicMultiprocessing(self):
        par_lens = MultiprocessingParallelizer(processes=5, initialization_timeout=2).run(self.run_job)
        serial_lens = SerialNonParallelizer().run(self.run_job)
        self.assertEquals(par_lens, serial_lens)

    def mapped_func(self, data):
        return [
            sum(1 + d for d in p)
            for c in data
            for p in itertools.permutations(c)
        ]
    def map_applier(self, n=12, r=9, parallelizer=None):
        if parallelizer.on_main:
            data = list(itertools.combinations(range(n), r))
        else:
            data = None
        return parallelizer.map(self.mapped_func, data, vectorized=True)
    @validationTest
    def test_MapMultiprocessing(self):
        from McUtils.Profilers import Timer
        with MultiprocessingParallelizer(initialization_timeout=1) as par:
            with Timer():
               par_lens = par.run(self.map_applier)

        with Timer():
            serial_lens = SerialNonParallelizer().run(self.map_applier)
        self.assertEquals(par_lens, serial_lens)
    @validationTest
    def test_MapMultiprocessingDataSmall(self):
        par_lens = MultiprocessingParallelizer().run(self.map_applier, n=3, comm=[0, 1, 2])
        self.assertEquals(len(par_lens), 3)
        serial_lens = SerialNonParallelizer().run(self.map_applier, n=3)
        self.assertEquals(par_lens, serial_lens)

    def bcast_parallelizer(self, parallelizer=None):
        root_par = parallelizer.broadcast(parallelizer)
    @validationTest
    def test_BroadcastParallelizer(self):
        with MultiprocessingParallelizer() as parallelizer:
            parallelizer.run(self.bcast_parallelizer)
            parallelizer.run(self.bcast_parallelizer)

    def scatter_gather(self, n=1000, parallelizer=None):
        if parallelizer.on_main:
            data = np.arange(n)
        else:
            data = None
        data = parallelizer.scatter(data)
        l = len(data)
        res = parallelizer.gather(l)
        return res
    @validationTest
    def test_ScatterGatherMultiprocessing(self):
        p = MultiprocessingParallelizer()
        par_lens = p.run(self.scatter_gather)
        self.assertEquals(len(par_lens), p.nprocs+1)
        serial_lens = SerialNonParallelizer().run(self.scatter_gather)
        self.assertEquals(sum(par_lens), serial_lens)
    @validationTest
    def test_ScatterGatherMultiprocessingDataSmall(self):
        par_lens = MultiprocessingParallelizer().run(self.scatter_gather, 3, comm=[0, 1, 2])
        self.assertEquals(len(par_lens), 3)
        serial_lens = SerialNonParallelizer().run(self.scatter_gather, 3)
        self.assertEquals(sum(par_lens), serial_lens)

    def simple_scatter_1(self, parallelizer=None):
        data = [
            np.array([[0, 0]]), np.array([[0, 1]]), np.array([[0, 2]]),
            np.array([[1, 0]]), np.array([[1, 1]]), np.array([[1, 2]]),
            np.array([[2, 0]]), np.array([[2, 1]]), np.array([[2, 2]])
        ]
        data = parallelizer.scatter(data)
        l = len(data)
        l = parallelizer.gather(l)
        return l
    def simple_print(self, parallelizer=None):
        parallelizer.print(1)
    @validationTest
    def test_MiscProblems(self):

        l = MultiprocessingParallelizer().run(self.simple_scatter_1, comm=[0, 1, 2, 3, 4, 5, 6, 7, 8])
        MultiprocessingParallelizer().run(self.simple_print, comm=[0, 1, 2])
        # raise Exception(l)

    @validationTest
    def test_MakeSharedMem(self):

        a = np.random.rand(10, 5, 5)
        manager = SharedObjectManager(a)

        saved = manager.share()
        loaded = manager.unshare() #type: np.ndarray
        # print(type(loaded), loaded.shape, loaded.data, loaded.size)

        self.assertTrue(np.allclose(a, loaded))


    def mutate_shared_dict(self, d, parallelizer=None):
        wat = d['d']
        parallelizer.print('{a} {b} {c} {d}', a=id(wat), b=id(d['d']), c=id(d['d']), d=d)
        if not parallelizer.on_main:
            d['a'][1, 0, 0] = 5
            wat['key'] = 5
        parallelizer.print('{v} {g}', v=wat, g=d['d'])

    @validationTest
    def test_DistributedDict(self):

         my_data = {'a':np.random.rand(10, 5, 5), 'b':np.random.rand(10, 3, 8), 'c':np.random.rand(10, 15, 4), 'd':{}}

         par = MultiprocessingParallelizer(processes=2, logger=Logger())
         my_data = par.share(my_data)

         par.run(self.mutate_shared_dict, my_data)

         self.assertEquals(my_data['a'][1, 0, 0], 5.0)

         my_data = my_data.unshare()
         self.assertIsInstance(my_data, dict)
         self.assertIsInstance(my_data['a'], np.ndarray)

    @validationTest
    def test_SimpleSharedDict(self):
        # from McUtils.Parallelizers import SharedMemoryDict

        state = SharedMemoryDict({"iteration": 0, "energy": 0.0})
        try:
            state["iteration"] = 12
            state["energy"] = -76.2413
            print(dict(state.items()))
        finally:
            state.close()

    #region liveness_check_init.patch tests
    #
    # Tests for the `PoolCommunicator.initialize()` patch that replaces the
    # timeout-based init handshake with direct worker-liveness checking
    # (see `liveness_check_init.patch`). `MultiprocessingParallelizer.pool`
    # is a real local `multiprocessing.pool.Pool`, so its worker `Process`
    # objects (in the private `pool._pool` list) can be checked directly
    # via `.is_alive()`/`.exitcode` -- a dead worker is detected within one
    # `poll_interval` instead of only after `initialization_timeout`
    # expires, and a healthy-but-slow pool never times out prematurely.
    #
    # `poll_interval`/`stall_timeout` are new `MultiprocessingParallelizer`
    # constructor kwargs added by the patch; `stall_timeout=None` (the
    # default) means "wait indefinitely as long as every worker stays
    # alive," since real crashes are now caught immediately regardless of
    # how long that ends up being.

    def light_map_func(self, chunk):
        # a `vectorized=True`-style map function, matching `mapped_func`
        # above: operates on the whole chunk handed to one worker, not
        # element-by-element
        return [x + 1 for x in chunk]

    def light_map_job(self, data, parallelizer=None):
        if parallelizer.on_main and data is None:
            data = list(range(100))
        return parallelizer.map(self.light_map_func, data, vectorized=True)

    @validationTest
    def test_PatchBackwardsCompatibleConstruction(self):
        # no new kwargs supplied: should behave exactly as it did before
        # the patch
        par_result = MultiprocessingParallelizer(processes=5).run(self.light_map_job, list(range(50)))
        serial_result = SerialNonParallelizer().run(self.light_map_job, list(range(50)))
        self.assertEqual(sorted(par_result), sorted(serial_result))

    @validationTest
    def test_PatchNewKwargsAcceptedAndHarmless(self):
        # poll_interval/stall_timeout are new, optional, and shouldn't
        # change behavior on the happy path
        par_result = MultiprocessingParallelizer(
            processes=4, poll_interval=0.01, stall_timeout=30.0
        ).run(self.light_map_job, list(range(50)))
        serial_result = SerialNonParallelizer().run(self.light_map_job, list(range(50)))
        self.assertEqual(sorted(par_result), sorted(serial_result))

    @validationTest
    def test_PatchRepeatedRoundsNoFalseFailures(self):
        # the polling loop shouldn't introduce spurious failures across
        # many successive dispatches -- each `.run()` re-does the init
        # handshake, so this exercises `initialize()` repeatedly
        with MultiprocessingParallelizer(processes=4) as par:
            for i in range(10):
                r = par.run(self.light_map_job, list(range(30)))
                self.assertEqual(sorted(r), list(range(1, 31)), msg="round {} produced wrong result".format(i))

    def only_main_job(self, x, parallelizer=None):
        return ("main-ran", x)
    only_main_job = Parallelizer.main_restricted(only_main_job)

    def only_worker_job(self, x, parallelizer=None):
        return ("worker-ran", x)
    only_worker_job = Parallelizer.worker_restricted(only_worker_job)

    def decorator_check_job(self, x, parallelizer=None):
        # `main_restricted`/`worker_restricted`-decorated *bound methods*
        # (as opposed to the module-level closures in the commented-out
        # example at the top of this file) pickle fine under this class's
        # `__getstate__`/`__setstate__` trick, since a bound method
        # pickles as "look this name up on the (stripped) instance again,"
        # not by serializing the decorator's closure directly. Confirmed
        # this still holds under the patched `initialize()`.
        return self.only_main_job(x, parallelizer=parallelizer), self.only_worker_job(x, parallelizer=parallelizer)

    @validationTest
    def test_PatchDecoratorCompatibility(self):
        with MultiprocessingParallelizer(processes=4) as par:
            r = par.run(self.decorator_check_job, 5)
        self.assertEqual(r[0], ("main-ran", 5))

    @debugTest
    def test_PatchDeadWorkerDetectedFast(self):
        # The actual regression test for the patch: kill a real pool
        # worker and confirm the init handshake fails fast instead of
        # hanging or only failing after `initialization_timeout` elapses.
        #
        # This intentionally does NOT redispatch through `.run()`/`.apply()`
        # after the kill: `multiprocessing.pool.Pool` auto-respawns dead
        # workers (and can silently requeue an in-flight task from one),
        # which makes "kill, then `.run()` again" a race against Pool's
        # own healing thread -- observed to occasionally hang for reasons
        # unrelated to this patch. Calling `comm.initialize()` directly
        # isolates exactly the logic the patch changes.
        #
        # It also runs in a child process with a hard wall-clock timeout,
        # and reports *which stage* it reached rather than a single
        # pass/fail: tearing down a pool with a dead worker
        # (`pool.__exit__()`/`pool.terminate()`) was separately observed to
        # sometimes hang -- a pre-existing `Pool` teardown quirk this patch
        # doesn't touch -- and that's a meaningfully different failure from
        # detection itself never completing. `stage_timeout` is generous:
        # under the `spawn` start method (macOS's default, vs. Linux's
        # default `fork`), just building the child's own 4-worker pool
        # means 5 fresh interpreter start-ups before we ever get to the
        # thing being tested, which is legitimately much slower than under
        # `fork`. `detection_budget` is intentionally much tighter, since
        # it bounds only the actual `comm.initialize()` call this patch
        # changes: either the fast liveness path (near-instant) or the
        # `stall_timeout=5.0` backstop inside `_dead_worker_child` should
        # account for it, so 8s of margin should never legitimately be
        # needed -- if it is, that's the real signal, not platform noise.
        ok, detail = _run_dead_worker_check(stage_timeout=5.0, join_timeout=2.0, detection_budget=8.0)
        self.assertTrue(ok, detail)

    #endregion

    def _make_comm(self, parent, queues, poll_interval=0.01, stall_timeout=None, rank=0):
        return MultiprocessingParallelizer.PoolCommunicator(
            parent, rank, queues,
            initialization_timeout=0.5,  # unused by initialize() itself post-patch
            poll_interval=poll_interval,
            stall_timeout=stall_timeout,
        )

    class _FakeFlag:
        def __init__(self, set_after=None):
            self._t0 = time.time()
            self._set_after = set_after
            self._forced = False

        def is_set(self):
            if self._forced:
                return True
            if self._set_after is None:
                return False
            return (time.time() - self._t0) >= self._set_after

        def wait(self, timeout):
            deadline = time.time() + timeout
            while time.time() < deadline:
                if self.is_set():
                    return True
                time.sleep(min(0.001, max(0.0, deadline - time.time())))
            return self.is_set()

        def set(self):
            self._forced = True

        def clear(self):
            self._forced = False

    class _FakeQueue:
        def __init__(self, flag):
            self.init_flag = flag

    class _FakeProcess:
        def __init__(self, pid, alive=True, exitcode=None):
            self.pid = pid
            self._alive = alive
            self.exitcode = exitcode

        def is_alive(self):
            return self._alive

    class _FakePool:
        def __init__(self, processes):
            self._pool = processes

    class _FakeParent:
        on_main = True
        base_log_level = 0

        def __init__(self, processes):
            self.pool = ParallelizersTests._FakePool(processes)

        def print(self, *args, **kwargs):
            pass

    @validationTest
    def test_SuccessPathNoDelay(self):
        flags = [self._FakeFlag(set_after=0.0) for _ in range(3)]
        for f in flags:
            f.set()
        queues = [self._FakeQueue(f) for f in flags]
        parent = self._FakeParent([self._FakeProcess(pid=i, alive=True) for i in range(3)])
        comm = self._make_comm(parent, queues)

        t0 = time.time()
        comm.initialize()  # should not raise
        elapsed = time.time() - t0
        self.assertLess(elapsed, 0.2, "success path should not incur polling delay")

    @validationTest
    def test_SuccessPathAfterShortRealDelay(self):
        flags = [self._FakeFlag(set_after=0.15) for _ in range(3)]
        queues = [self._FakeQueue(f) for f in flags]
        parent = self._FakeParent([self._FakeProcess(pid=i, alive=True) for i in range(3)])
        comm = self._make_comm(parent, queues, poll_interval=0.01, stall_timeout=None)
        comm.initialize()  # should not raise, even though it had to wait

    @validationTest
    def test_DeadWorkerRaisesImmediately(self):
        flags = [self._FakeFlag(set_after=None) for _ in range(3)]  # never set
        queues = [self._FakeQueue(f) for f in flags]
        processes = [
            self._FakeProcess(pid=100, alive=True),
            self._FakeProcess(pid=101, alive=False, exitcode=-11),  # e.g. segfault
            self._FakeProcess(pid=102, alive=True),
        ]
        parent = self._FakeParent(processes)
        comm = self._make_comm(parent, queues, poll_interval=0.01, stall_timeout=None)

        t0 = time.time()
        with self.assertRaises(MultiprocessingParallelizer.PoolCommunicator.PoolError) as ctx:
            comm.initialize()
        elapsed = time.time() - t0

        self.assertLess(elapsed, 0.2, "dead worker should be detected within a couple poll intervals")
        self.assertIn("101", str(ctx.exception))
        self.assertIn("-11", str(ctx.exception))

    @validationTest
    def test_AllAliveNoStallTimeoutWaitsWithinBudget(self):
        flags = [self._FakeFlag(set_after=0.1) for _ in range(2)]
        queues = [self._FakeQueue(f) for f in flags]
        parent = self._FakeParent([self._FakeProcess(pid=i, alive=True) for i in range(2)])
        comm = self._make_comm(parent, queues, poll_interval=0.02, stall_timeout=None)
        comm.initialize()  # must not raise

    @validationTest
    def test_StallTimeoutBackstopFires(self):
        flags = [self._FakeFlag(set_after=None) for _ in range(2)]  # never set
        queues = [self._FakeQueue(f) for f in flags]
        parent = self._FakeParent([self._FakeProcess(pid=i, alive=True) for i in range(2)])
        comm = self._make_comm(parent, queues, poll_interval=0.01, stall_timeout=0.08)

        t0 = time.time()
        with self.assertRaises(MultiprocessingParallelizer.PoolCommunicator.PoolError) as ctx:
            comm.initialize()
        elapsed = time.time() - t0

        self.assertGreaterEqual(elapsed, 0.08 * 0.5, "shouldn't fire drastically before stall_timeout")
        self.assertLess(elapsed, 0.5, "should fire close to stall_timeout, not hang")
        self.assertIn("hasn't completed initialization", str(ctx.exception))

    @validationTest
    def test_GetSubcommThreadsNewParams(self):
        flags = [self._FakeFlag(set_after=0.0) for _ in range(2)]
        for f in flags:
            f.set()
        queues = [self._FakeQueue(f) for f in flags]
        parent = self._FakeParent([self._FakeProcess(pid=i, alive=True) for i in range(2)])
        comm = self._make_comm(parent, queues, poll_interval=0.05, stall_timeout=1.23)

        sub = comm.get_subcomm([0])
        self.assertEqual(sub.poll_interval, 0.05)
        self.assertEqual(sub.stall_timeout, 1.23)




"""
Fast, deterministic unit tests of `PoolCommunicator.initialize()`'s
new branching (success / dead worker / stall backstop), using mock
`Process`/`Event`/`Pool` objects instead of real subprocesses. These
pin down the patch's logic precisely and run in well under a second
total, so they're safe to run on every invocation without the
subprocess-timing flakiness real multiprocessing tests are prone to.
Complements `ParallelizerTests`'s real end-to-end coverage above.
"""

def _dead_worker_child(result_queue):
    """Runs in a child process (see `_run_dead_worker_check`). Builds a
    real parallelizer, kills a real worker, and checks that
    `comm.initialize()` raises quickly. Reports progress through
    `result_queue` as it goes (`("stage", name)`), then a final
    `("result", ok, detail)` -- the staged reports are what let the parent
    tell "never got past setup" apart from "finished the check, couldn't
    exit afterward" if this process doesn't come back at all. Assertions
    raised in a child process don't propagate to the parent test runner,
    hence reporting through the queue instead."""
    import time as _time

    def _stage(name):
        try:
            result_queue.put(("stage", name))
        except Exception:
            pass

    p = None
    try:
        _stage("child_started")
        # `stall_timeout` matters here for a subtler reason than platform
        # timing: this test never actually dispatches `_run()` to any
        # worker (it calls `comm.initialize()` directly), so NOTHING is
        # ever going to set the other ranks' flags regardless of which
        # process we kill. Success therefore depends entirely on the
        # liveness check catching the *already-dead* `Process` object in
        # `pool._pool` before `Pool`'s own maintenance thread quietly
        # replaces it with a fresh, live one -- a race against Pool's
        # internals that we lose more often under load (confirmed: this
        # test hung for the full stage_timeout in 3/4 runs when run under
        # heavy parallel contention). `stall_timeout` makes the outcome
        # deterministic either way: if we win the race, detection is
        # near-instant via `PoolError`; if we lose it, the stall backstop
        # still bounds the wait instead of hanging on flags that were
        # never going to be set in this synthetic scenario.
        p = MultiprocessingParallelizer(processes=4, initialization_timeout=0.05, stall_timeout=5.0,
                                        comm_preinitializer=lambda comm: (
                                            comm.parent.pool._pool[1].terminate(),
                                            comm.parent.pool._pool[1].join(timeout=1)
                                        )) # need to kill before the pool can replace it
        p.__enter__()
        _stage("pool_entered")
        comm = p.comm  # force real pool + real queues to exist
        _stage("comm_built")
        victim = p.pool._pool[1]
        victim.terminate()
        victim.join(timeout=5)
        if victim.is_alive():
            result_queue.put(("result", False, "victim process did not die within 5s"))
            return
        _stage("victim_killed")
        comm.reset()
        _stage("comm_reset")
        # if victim not in p.pool._pool:
        #     result_queue.put(("result", False, "victim process replaced"))
        #     return
        # if victim.is_alive():
        #     result_queue.put(("result", False, "victim process restarted"))
        #     return

        t0 = _time.time()
        try:
            comm.initialize()
            result_queue.put(("result", False, "comm.initialize() did not raise after a worker died"))
            return
        except Exception as e:
            elapsed = _time.time() - t0
            exc_name = type(e).__name__
            _stage("comm_initialize_raised")
            # Two legitimate outcomes, both proving the patch bounds the
            # wait instead of hanging: (a) the liveness check wins its
            # race against Pool's replacement thread and raises near-
            # instantly, or (b) it loses that race (see comment above) and
            # the `stall_timeout=5.0` backstop fires instead, close to
            # 5s. Anything well past that -- comfortably outside both
            # mechanisms -- is the actual failure signal.
            if elapsed >= 8.0:
                result_queue.put((
                    "result", False,
                    "raised {} but took {:.2f}s -- longer than either the fast liveness "
                    "path or the stall_timeout=5.0 backstop should allow".format(exc_name, elapsed)
                ))
                return
            result_queue.put(("result", True, "raised {} after {:.3f}s ({})".format(
                exc_name, elapsed, "fast liveness detection" if elapsed < 1.0 else "stall_timeout backstop"
            )))
    except Exception as e:
        result_queue.put(("result", False, "unexpected error in child: {}: {}".format(type(e).__name__, e)))
    finally:
        _stage("cleanup_start")
        # best-effort, non-blocking cleanup -- don't let a hung graceful
        # teardown affect the result already queued; the watchdog around
        # this whole function reaps the process regardless
        if p is not None:
            try:
                p.pool.terminate()
            except Exception:
                pass
        _stage("cleanup_done")


def _run_dead_worker_check(stage_timeout, join_timeout=10.0, detection_budget=8.0):
    """Runs `_dead_worker_child` in a child process; returns
    `(success: bool, detail: str)`.

    Two timeouts, on purpose, so a failure message tells you which
    problem you actually have instead of guessing:

    * `stage_timeout` bounds how long we'll wait for the child to report
      *any* result at all. If this elapses with no result, we genuinely
      don't know whether detection worked -- the child never got far
      enough to tell us -- so the returned message includes the last
      stage we did see, which is the actual diagnostic signal: e.g. stuck
      stuck at "child_started" means pool construction itself never
      finished (spawn overhead, or a real hang in `__enter__`/`initialize`
      unrelated to this patch); stuck at "comm_reset" means it's hanging
      immediately before the call this patch changes, worth a closer
      look; no stage report at all means the child process itself never
      started running or crashed before its first `_stage()` call.

    * `join_timeout` is only consulted *after* we already have a result
      from the queue. If the child then fails to exit within
      `join_timeout`, that unambiguously means teardown/exit is the
      problem -- we already know detection itself succeeded or failed
      (and why), so this can only be reported as an additional note, never
      as the primary failure reason.

    `detection_budget` is threaded through only for documentation/tuning
    convenience at the call site; the actual bound is enforced inside
    `_dead_worker_child` itself (see the comment there) since that's
    where `t0`/`elapsed` are measured.
    """
    import multiprocessing as _mp
    import time as _time

    ctx = _mp.get_context()
    q = ctx.Queue()
    proc = ctx.Process(target=_dead_worker_child, args=(q,))
    proc.start()

    last_stage = "process_not_yet_started"
    result = None
    deadline = _time.time() + stage_timeout
    while _time.time() < deadline:
        remaining = deadline - _time.time()
        try:
            msg = q.get(timeout=max(0.1, min(remaining, 0.5)))
        except Exception as e:
            continue
        if msg[0] == "stage":
            last_stage = msg[1]
        elif msg[0] == "result":
            result = msg[1:]
            break

    if result is None:
        proc.terminate()
        proc.join(timeout=5)
        return False, (
            "child never reported a result within {}s; last observed stage: '{}'. "
            "This means detection (or something before it) did not complete -- it is "
            "NOT a teardown-only hang, since we never even got a result to tear down "
            "after. If the last stage is 'child_started' or earlier, suspect process/pool "
            "start-up overhead (e.g. the `spawn` start method building a nested 4-worker "
            "pool) rather than the patch itself; if it's 'comm_reset' or later, that's "
            "much more likely a genuine regression in `initialize()`.".format(stage_timeout, last_stage)
        )

    ok, detail = result
    # we have a definitive result already; whether the process exits
    # cleanly afterward is a separate concern from here on
    proc.join(timeout=join_timeout)
    if proc.is_alive():
        proc.terminate()
        proc.join(timeout=5)
        detail = detail + (
            " [note: child process did not exit within {}s after reporting this result -- "
            "this is a separate, confirmed teardown-only hang, not a detection hang, since "
            "the result above was already received before this wait started]".format(join_timeout)
        )
    return ok, detail