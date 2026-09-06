# <a id="McUtils.Parallelizers">McUtils.Parallelizers</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/__init__.py#L1?message=Update%20Docs)]
</div>
    
Provides utilities for setting up platform-independent parallelism
in a hopefully unobtrusive way.

This is used more extensively in `Psience`, but the design is to unify the MPI and `multiprocessing` APIs
so that one can simply pass in a `Parallelizer` object to a function and obtain parallelism over as
many processes as that object supports.
As a fallthrough, a `SerialNonParallelizer` is provided as a subclass that handles serial evaluation with
the same API so fewer special cases need to be checked.
Any function that supports parallelism should take the `parallelizer` keyword, which will be fed
the `Parallelizer` object itself.

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[Parallelizer](Parallelizers/Parallelizers/Parallelizer.md)   
</div>
   <div class="col" markdown="1">
[MultiprocessingParallelizer](Parallelizers/Parallelizers/MultiprocessingParallelizer.md)   
</div>
   <div class="col" markdown="1">
[MPIParallelizer](Parallelizers/Parallelizers/MPIParallelizer.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[SerialNonParallelizer](Parallelizers/Parallelizers/SerialNonParallelizer.md)   
</div>
   <div class="col" markdown="1">
[SendRecieveParallelizer](Parallelizers/Parallelizers/SendRecieveParallelizer.md)   
</div>
   <div class="col" markdown="1">
[ClientServerRunner](Parallelizers/Runner/ClientServerRunner.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[SharedObjectManager](Parallelizers/SharedMemory/SharedObjectManager.md)   
</div>
   <div class="col" markdown="1">
[SharedMemoryDict](Parallelizers/SharedMemory/SharedMemoryDict.md)   
</div>
   <div class="col" markdown="1">
[SharedMemoryList](Parallelizers/SharedMemory/SharedMemoryList.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[SharedMemoryNDarray](Parallelizers/SharedMemory/SharedMemoryNDarray.md)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>





## Examples
The simplest parallelism is just parallelizing with `multiprocessing` over a single function

<div class="card in-out-block" markdown="1">

```python
def run_job(parallelizer=None):
    if parallelizer.on_main:
        data = np.arange(1000)
    else:
        data = None
    if parallelizer.on_main:
        flag = "woop"
    else:
        flag = None
    test = parallelizer.broadcast(flag) # send a flag from the main process to all the workers
    data = parallelizer.scatter(data)
    lens = parallelizer.gather(len(data))
    return lens

MultiprocessingParallelizer().run(run_job)
```
<div class="card-body out-block" markdown="1">

```python
[67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 66, 66, 66, 66, 66]
```

</div>
</div>

This will make sure a `Pool` of workers gets set up and will create communication channels from the main process to the works, then each process will run `run_job`, spreading the data out with `scatter` and bringing it back with `gather`.

This paradigm can be handled more simply with `map`. 
Here we'll map a function over blocks of data

<div class="card in-out-block" markdown="1">

```python
def mapped_func(self, data):
    return 1 + data
def map_applier(n=10, parallelizer=None):
    if parallelizer.on_main:
        data = np.arange(n)
    else:
        data = None
    return parallelizer.map(mapped_func, data)

MultiprocessingParallelizer().run(map_applier)
```

<div class="card-body out-block" markdown="1">

```python
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

</div>
</div>

but all of these will work equivalently well if the `parallelizer` were a `MPIParallelizer` instead (with correct run setup).

This also adapts itself well to more object-oriented solutions. 
Here's a sample class that can effectively use a parallelizer

```python
class SampleProgram:
    
    def __init__(self, nvals=1000, parallelizer=None):
        if not isinstance(parallelizer, Parallelizer):
            parallelizer = Parallelizer.lookup(parallelizer) # `Parallelizer` supports a registry in case you want to give a name
        self.par = parallelizer
        self.nvals = nvals
    
    def initialize_data(self):
        data = np.random.rand(self.nvals)
        # could be more expensive too
        return data
    
    def eval_parallel(self, data, parallelizer=None):
        data = parallelizer.scatter(data)
        # this would usually be much more sophisticated
        res = data**2
        return parallelizer.gather(res)
     
    @Parallelizer.main_restricted
    def run_main(self, parallelizer=None):
        """
        A function to be run by the main processes, setting
        up data, scattering, gathering, and post-processing
        """
        data = self.initialize_data()
        vals = self.eval_parallel(data, parallelizer=parallelizer)
        post_process = np.sqrt(vals)
        return post_process
        
    @Parallelizer.worker_restricted
    def run_worker(self, parallelizer=None):
        """
        A function to be run by the worker processes, really
        just doing the parallel work
        """
        self.eval_parallel(None, parallelizer=parallelizer)
    
    def run_par(self, parallelizer=None):
        """
        Something to be called by all processes
        """
        self.run_worker(parallelizer=parallelizer)
        return self.run_main(parallelizer=parallelizer)
    
    def run(self):
        """
        Boilerplate runner
        """
        print("Running with {}".format(self.par))
        return self.par.run(self.run_par)
```

and we can easily add in a `parallelizer` at run time.

First serial evaluation

<div class="card in-out-block" markdown="1">
```python
SampleProgram(nvals=10).run()
```
<div class="card-body out-block" markdown="1">

```lang-none
Running with SerialNonParallelizer(id=0, nprocs=1)

array([0.08772434, 0.18266685, 0.11234067, 0.4918653 , 0.30925003,
       0.43065691, 0.8271145 , 0.52147149, 0.13801914, 0.92917295])
```
</div>
</div>

but adding in parallelism is straightforward


<div class="card in-out-block" markdown="1">

```python
SampleProgram(nvals=10, parallelizer=MultiprocessingParallelizer()).run()
```

<div class="card-body out-block" markdown="1">

```lang-none
Running with MultiprocessingParallelizer(id=None, nprocs=None)

array([0.5852531 , 0.63836097, 0.40315219, 0.04769397, 0.5226616 ,
       0.68647924, 0.30869102, 0.01006922, 0.07439768, 0.83100183])
```

</div>
</div>

To support MPI-style calling, a `ClientServerRunner` is also provided.

**LLM Examples**

### Write backend-independent numerical code

```python
import numpy as np
from McUtils.Parallelizers import SerialNonParallelizer

def energy(geometry, *, parallelizer=None):
    return np.sum(geometry**2)

geometries = np.arange(36.).reshape(4, 3, 3)
parallelizer = SerialNonParallelizer()
energies = parallelizer.map(energy, geometries,
                            extra_kwargs={"parallelizer": parallelizer},
                            vectorized=False, aggregate=True)
print(energies)
```

### Switch to multiprocessing

```python
import numpy as np
from McUtils.Parallelizers import MultiprocessingParallelizer

def norm(vector):
    return np.linalg.norm(vector)

vectors = np.random.default_rng(4).normal(size=(1000, 3))
with MultiprocessingParallelizer(nprocs=4) as parallelizer:
    norms = parallelizer.map(norm, vectors, vectorized=False, aggregate=True)
print("mean norm:", np.mean(norms))
```

### Share a NumPy array between processes

```python
import numpy as np
from multiprocessing.shared_memory import SharedMemory
from McUtils.Parallelizers import SharedMemoryNDarray

array = np.arange(24., dtype=float).reshape(8, 3)
buffer = SharedMemory(create=True, size=array.nbytes)
shared = SharedMemoryNDarray.from_array(array, buffer, autoclose=False)
try:
    view = shared.array
    view[:, 0] *= -1
    assert np.shares_memory(view, shared.array)
finally:
    shared.close()
    shared.unlink()
```

### Use one parallelizer contract for serial and MPI execution

```python
from McUtils.Parallelizers import Parallelizer

parallelizer = Parallelizer.lookup("serial")
with parallelizer:
    rank = parallelizer.id
    size = parallelizer.nprocs
    value = parallelizer.broadcast({"method": "CCSD(T)"})
print(rank, size, value)
```

### Scatter and gather array blocks

```python
import numpy as np
from McUtils.Parallelizers import SerialNonParallelizer

data = np.arange(24).reshape(8, 3)
parallelizer = SerialNonParallelizer()
local = parallelizer.scatter(data)
local = local**2
combined = parallelizer.gather(local)
assert np.allclose(combined, data**2)
```

### Share structured state

```python
from McUtils.Parallelizers import SharedMemoryDict

state = SharedMemoryDict({"iteration": 0, "energy": 0.0})
try:
    state["iteration"] = 12
    state["energy"] = -76.2413
    print(dict(state.items()))
finally:
    state.close()
```













<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Tests-0d8905" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-0d8905"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-0d8905" markdown="1">
 - [BasicMultiprocessing](#BasicMultiprocessing)
- [MapMultiprocessing](#MapMultiprocessing)
- [MapMultiprocessingDataSmall](#MapMultiprocessingDataSmall)
- [BroadcastParallelizer](#BroadcastParallelizer)
- [ScatterGatherMultiprocessing](#ScatterGatherMultiprocessing)
- [ScatterGatherMultiprocessingDataSmall](#ScatterGatherMultiprocessingDataSmall)
- [MiscProblems](#MiscProblems)
- [MakeSharedMem](#MakeSharedMem)
- [DistributedDict](#DistributedDict)
- [SimpleSharedDict](#SimpleSharedDict)
- [PatchBackwardsCompatibleConstruction](#PatchBackwardsCompatibleConstruction)
- [PatchNewKwargsAcceptedAndHarmless](#PatchNewKwargsAcceptedAndHarmless)
- [PatchRepeatedRoundsNoFalseFailures](#PatchRepeatedRoundsNoFalseFailures)
- [PatchDecoratorCompatibility](#PatchDecoratorCompatibility)
- [PatchDeadWorkerDetectedFast](#PatchDeadWorkerDetectedFast)
- [SuccessPathNoDelay](#SuccessPathNoDelay)
- [SuccessPathAfterShortRealDelay](#SuccessPathAfterShortRealDelay)
- [DeadWorkerRaisesImmediately](#DeadWorkerRaisesImmediately)
- [AllAliveNoStallTimeoutWaitsWithinBudget](#AllAliveNoStallTimeoutWaitsWithinBudget)
- [StallTimeoutBackstopFires](#StallTimeoutBackstopFires)
- [GetSubcommThreadsNewParams](#GetSubcommThreadsNewParams)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#Setup-b70f8d" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-b70f8d"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-b70f8d" markdown="1">
 
Before we can run our examples we should get a bit of setup out of the way.
Since these examples were harvested from the unit tests not all pieces
will be necessary for all situations.

All tests are wrapped in a test class
```python
class ParallelizersTests(TestCase):
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
    def bcast_parallelizer(self, parallelizer=None):
        root_par = parallelizer.broadcast(parallelizer)
    def scatter_gather(self, n=1000, parallelizer=None):
        if parallelizer.on_main:
            data = np.arange(n)
        else:
            data = None
        data = parallelizer.scatter(data)
        l = len(data)
        res = parallelizer.gather(l)
        return res
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
    def mutate_shared_dict(self, d, parallelizer=None):
        wat = d['d']
        parallelizer.print('{a} {b} {c} {d}', a=id(wat), b=id(d['d']), c=id(d['d']), d=d)
        if not parallelizer.on_main:
            d['a'][1, 0, 0] = 5
            wat['key'] = 5
        parallelizer.print('{v} {g}', v=wat, g=d['d'])
    def light_map_func(self, chunk):
        # a `vectorized=True`-style map function, matching `mapped_func`
        # above: operates on the whole chunk handed to one worker, not
        # element-by-element
        return [x + 1 for x in chunk]
    def light_map_job(self, data, parallelizer=None):
        if parallelizer.on_main and data is None:
            data = list(range(100))
        return parallelizer.map(self.light_map_func, data, vectorized=True)
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
```

 </div>
</div>

#### <a name="BasicMultiprocessing">BasicMultiprocessing</a>
```python
    def test_BasicMultiprocessing(self):
        par_lens = MultiprocessingParallelizer(processes=5, initialization_timeout=2).run(self.run_job)
        serial_lens = SerialNonParallelizer().run(self.run_job)
        self.assertEquals(par_lens, serial_lens)
```

#### <a name="MapMultiprocessing">MapMultiprocessing</a>
```python
    def test_MapMultiprocessing(self):
        from McUtils.Profilers import Timer
        with MultiprocessingParallelizer(initialization_timeout=1) as par:
            with Timer():
               par_lens = par.run(self.map_applier)

        with Timer():
            serial_lens = SerialNonParallelizer().run(self.map_applier)
        self.assertEquals(par_lens, serial_lens)
```

#### <a name="MapMultiprocessingDataSmall">MapMultiprocessingDataSmall</a>
```python
    def test_MapMultiprocessingDataSmall(self):
        par_lens = MultiprocessingParallelizer().run(self.map_applier, n=3, comm=[0, 1, 2])
        self.assertEquals(len(par_lens), 3)
        serial_lens = SerialNonParallelizer().run(self.map_applier, n=3)
        self.assertEquals(par_lens, serial_lens)
```

#### <a name="BroadcastParallelizer">BroadcastParallelizer</a>
```python
    def test_BroadcastParallelizer(self):
        with MultiprocessingParallelizer() as parallelizer:
            parallelizer.run(self.bcast_parallelizer)
            parallelizer.run(self.bcast_parallelizer)
```

#### <a name="ScatterGatherMultiprocessing">ScatterGatherMultiprocessing</a>
```python
    def test_ScatterGatherMultiprocessing(self):
        p = MultiprocessingParallelizer()
        par_lens = p.run(self.scatter_gather)
        self.assertEquals(len(par_lens), p.nprocs+1)
        serial_lens = SerialNonParallelizer().run(self.scatter_gather)
        self.assertEquals(sum(par_lens), serial_lens)
```

#### <a name="ScatterGatherMultiprocessingDataSmall">ScatterGatherMultiprocessingDataSmall</a>
```python
    def test_ScatterGatherMultiprocessingDataSmall(self):
        par_lens = MultiprocessingParallelizer().run(self.scatter_gather, 3, comm=[0, 1, 2])
        self.assertEquals(len(par_lens), 3)
        serial_lens = SerialNonParallelizer().run(self.scatter_gather, 3)
        self.assertEquals(sum(par_lens), serial_lens)
```

#### <a name="MiscProblems">MiscProblems</a>
```python
    def test_MiscProblems(self):

        l = MultiprocessingParallelizer().run(self.simple_scatter_1, comm=[0, 1, 2, 3, 4, 5, 6, 7, 8])
        MultiprocessingParallelizer().run(self.simple_print, comm=[0, 1, 2])
```

#### <a name="MakeSharedMem">MakeSharedMem</a>
```python
    def test_MakeSharedMem(self):

        a = np.random.rand(10, 5, 5)
        manager = SharedObjectManager(a)

        saved = manager.share()
        loaded = manager.unshare() #type: np.ndarray
        # print(type(loaded), loaded.shape, loaded.data, loaded.size)

        self.assertTrue(np.allclose(a, loaded))
```

#### <a name="DistributedDict">DistributedDict</a>
```python
    def test_DistributedDict(self):

         my_data = {'a':np.random.rand(10, 5, 5), 'b':np.random.rand(10, 3, 8), 'c':np.random.rand(10, 15, 4), 'd':{}}

         par = MultiprocessingParallelizer(processes=2, logger=Logger())
         my_data = par.share(my_data)

         par.run(self.mutate_shared_dict, my_data)

         self.assertEquals(my_data['a'][1, 0, 0], 5.0)

         my_data = my_data.unshare()
         self.assertIsInstance(my_data, dict)
         self.assertIsInstance(my_data['a'], np.ndarray)
```

#### <a name="SimpleSharedDict">SimpleSharedDict</a>
```python
    def test_SimpleSharedDict(self):
        # from McUtils.Parallelizers import SharedMemoryDict

        state = SharedMemoryDict({"iteration": 0, "energy": 0.0})
        try:
            state["iteration"] = 12
            state["energy"] = -76.2413
            print(dict(state.items()))
        finally:
            state.close()
```

#### <a name="PatchBackwardsCompatibleConstruction">PatchBackwardsCompatibleConstruction</a>
```python
    def test_PatchBackwardsCompatibleConstruction(self):
        # no new kwargs supplied: should behave exactly as it did before
        # the patch
        par_result = MultiprocessingParallelizer(processes=5).run(self.light_map_job, list(range(50)))
        serial_result = SerialNonParallelizer().run(self.light_map_job, list(range(50)))
        self.assertEqual(sorted(par_result), sorted(serial_result))
```

#### <a name="PatchNewKwargsAcceptedAndHarmless">PatchNewKwargsAcceptedAndHarmless</a>
```python
    def test_PatchNewKwargsAcceptedAndHarmless(self):
        # poll_interval/stall_timeout are new, optional, and shouldn't
        # change behavior on the happy path
        par_result = MultiprocessingParallelizer(
            processes=4, poll_interval=0.01, stall_timeout=30.0
        ).run(self.light_map_job, list(range(50)))
        serial_result = SerialNonParallelizer().run(self.light_map_job, list(range(50)))
        self.assertEqual(sorted(par_result), sorted(serial_result))
```

#### <a name="PatchRepeatedRoundsNoFalseFailures">PatchRepeatedRoundsNoFalseFailures</a>
```python
    def test_PatchRepeatedRoundsNoFalseFailures(self):
        # the polling loop shouldn't introduce spurious failures across
        # many successive dispatches -- each `.run()` re-does the init
        # handshake, so this exercises `initialize()` repeatedly
        with MultiprocessingParallelizer(processes=4) as par:
            for i in range(10):
                r = par.run(self.light_map_job, list(range(30)))
                self.assertEqual(sorted(r), list(range(1, 31)), msg="round {} produced wrong result".format(i))
```

#### <a name="PatchDecoratorCompatibility">PatchDecoratorCompatibility</a>
```python
    def test_PatchDecoratorCompatibility(self):
        with MultiprocessingParallelizer(processes=4) as par:
            r = par.run(self.decorator_check_job, 5)
        self.assertEqual(r[0], ("main-ran", 5))
```

#### <a name="PatchDeadWorkerDetectedFast">PatchDeadWorkerDetectedFast</a>
```python
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
```

#### <a name="SuccessPathNoDelay">SuccessPathNoDelay</a>
```python
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
```

#### <a name="SuccessPathAfterShortRealDelay">SuccessPathAfterShortRealDelay</a>
```python
    def test_SuccessPathAfterShortRealDelay(self):
        flags = [self._FakeFlag(set_after=0.15) for _ in range(3)]
        queues = [self._FakeQueue(f) for f in flags]
        parent = self._FakeParent([self._FakeProcess(pid=i, alive=True) for i in range(3)])
        comm = self._make_comm(parent, queues, poll_interval=0.01, stall_timeout=None)
        comm.initialize()
```

#### <a name="DeadWorkerRaisesImmediately">DeadWorkerRaisesImmediately</a>
```python
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
```

#### <a name="AllAliveNoStallTimeoutWaitsWithinBudget">AllAliveNoStallTimeoutWaitsWithinBudget</a>
```python
    def test_AllAliveNoStallTimeoutWaitsWithinBudget(self):
        flags = [self._FakeFlag(set_after=0.1) for _ in range(2)]
        queues = [self._FakeQueue(f) for f in flags]
        parent = self._FakeParent([self._FakeProcess(pid=i, alive=True) for i in range(2)])
        comm = self._make_comm(parent, queues, poll_interval=0.02, stall_timeout=None)
        comm.initialize()
```

#### <a name="StallTimeoutBackstopFires">StallTimeoutBackstopFires</a>
```python
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
```

#### <a name="GetSubcommThreadsNewParams">GetSubcommThreadsNewParams</a>
```python
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
```

 </div>
</div>






---


<div markdown="1" class="text-secondary">
<div class="container">
  <div class="row">
   <div class="col" markdown="1">
**Feedback**   
</div>
   <div class="col" markdown="1">
**Examples**   
</div>
   <div class="col" markdown="1">
**Templates**   
</div>
   <div class="col" markdown="1">
**Documentation**   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Bug](https://github.com/McCoyGroup/McUtils/issues/new?title=Documentation%20Improvement%20Needed)/[Request](https://github.com/McCoyGroup/McUtils/issues/new?title=Example%20Request)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/__init__.py#L1?message=Update%20Docs)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>
</div>