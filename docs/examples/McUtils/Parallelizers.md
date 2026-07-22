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
