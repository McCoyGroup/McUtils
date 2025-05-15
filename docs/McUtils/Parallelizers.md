# <a id="McUtils.Parallelizers">McUtils.Parallelizers</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/__init__.py#L1?message=Update%20Docs)]
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
[Parallelizer](McUtils/McUtils/Parallelizers/Parallelizers/Parallelizer.md)   
</div>
   <div class="col" markdown="1">
[MultiprocessingParallelizer](McUtils/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.md)   
</div>
   <div class="col" markdown="1">
[MPIParallelizer](McUtils/McUtils/Parallelizers/Parallelizers/MPIParallelizer.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[SerialNonParallelizer](McUtils/McUtils/Parallelizers/Parallelizers/SerialNonParallelizer.md)   
</div>
   <div class="col" markdown="1">
[SendRecieveParallelizer](McUtils/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.md)   
</div>
   <div class="col" markdown="1">
[ClientServerRunner](McUtils/McUtils/Parallelizers/Runner/ClientServerRunner.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[SharedObjectManager](McUtils/McUtils/Parallelizers/SharedMemory/SharedObjectManager.md)   
</div>
   <div class="col" markdown="1">
[SharedMemoryDict](McUtils/McUtils/Parallelizers/SharedMemory/SharedMemoryDict.md)   
</div>
   <div class="col" markdown="1">
[SharedMemoryList](McUtils/McUtils/Parallelizers/SharedMemory/SharedMemoryList.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
   
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/__init__.py#L1?message=Update%20Docs)   
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