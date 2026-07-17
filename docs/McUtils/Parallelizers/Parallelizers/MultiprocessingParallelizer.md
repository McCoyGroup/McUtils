## <a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer">MultiprocessingParallelizer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers.py#L1077)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers.py#L1077?message=Update%20Docs)]
</div>

Parallelizes using a  process pool and a runner
function that represents a "main loop".







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
SendRecvQueuePair: SendRecvQueuePair
PoolCommunicator: PoolCommunicator
```
<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, worker=False, pool: <bound method BaseContext.Pool of <multiprocessing.context.DefaultContext instance>> = None, context=None, manager=None, logger=None, contract=None, comm=None, rank=None, allow_restart=True, initialization_timeout=0.5, initialization_function=None, initialization_args=None, initialization_kwargs=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers.py#L1296)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers.py#L1296?message=Update%20Docs)]
</div>
**LLM Docstring**

Configure multiprocessing pool ownership, communicator state, worker rank, restart behavior, and initialization options.
  - `worker`: `Any`
    > Value supplied for `worker`.
  - `pool`: `mp.Pool`
    > Value supplied for `pool`.
  - `context`: `Any`
    > Value supplied for `context`.
  - `manager`: `Any`
    > Value supplied for `manager`.
  - `logger`: `Any`
    > Value supplied for `logger`.
  - `contract`: `Any`
    > Value supplied for `contract`.
  - `comm`: `Any`
    > Value supplied for `comm`.
  - `rank`: `Any`
    > Value supplied for `rank`.
  - `allow_restart`: `Any`
    > Value supplied for `allow_restart`.
  - `initialization_timeout`: `Any`
    > Value supplied for `initialization_timeout`.
  - `initialization_function`: `Any`
    > Value supplied for `initialization_function`.
  - `initialization_args`: `Any`
    > Value supplied for `initialization_args`.
  - `initialization_kwargs`: `Any`
    > Value supplied for `initialization_kwargs`.
  - `kwargs`: `Any`
    > Value supplied for `kwargs`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.get_nprocs" class="docs-object-method">&nbsp;</a> 
```python
get_nprocs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1364)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1364?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the cached multiprocessing process count.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.get_id" class="docs-object-method">&nbsp;</a> 
```python
get_id(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1373)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1373?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the explicit rank when set, otherwise obtain the id from the current communicator.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.comm" class="docs-object-method">&nbsp;</a> 
```python
@property
comm(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1386)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1386?message=Update%20Docs)]
</div>
Returns the communicator used by the paralellizer
  - `:returns`: `MultiprocessingParallelizer.PoolCommunicator`
    >


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.__getstate__" class="docs-object-method">&nbsp;</a> 
```python
__getstate__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1424)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1424?message=Update%20Docs)]
</div>
**LLM Docstring**

Prepare the parallelizer for pickling by removing live pool, manager, queue, stack, communicator, and PID state.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.__setstate__" class="docs-object-method">&nbsp;</a> 
```python
__setstate__(self, state): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1446)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1446?message=Update%20Docs)]
</div>
**LLM Docstring**

Restore pickled state and, when available, replace it with the registered parent parallelizer state.
  - `state`: `Any`
    > Value supplied for `state`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, func, *args, comm=None, main_kwargs=None, cleanup=True, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1545)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1545?message=Update%20Docs)]
</div>
Applies func to args in parallel on all of the processes
  - `func`: `Any`
    > 
  - `args`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.get_pool_context" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
get_pool_context(pool): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1646)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1646?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the private multiprocessing context stored by a pool.
  - `pool`: `Any`
    > Value supplied for `pool`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.get_pool_nprocs" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
get_pool_nprocs(pool): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L1659)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L1659?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the private process-count field stored by a pool.
  - `pool`: `Any`
    > Value supplied for `pool`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.set_initializer" class="docs-object-method">&nbsp;</a> 
```python
set_initializer(self, func, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1693)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1693?message=Update%20Docs)]
</div>
**LLM Docstring**

Install and run an initializer locally, map worker initialization across the pool, and update the pool initializer.
  - `func`: `Any`
    > Value supplied for `func`.
  - `args`: `Any`
    > Value supplied for `args`.
  - `kwargs`: `Any`
    > Value supplied for `kwargs`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.initialize" class="docs-object-method">&nbsp;</a> 
```python
initialize(self, allow_restart=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1719)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1719?message=Update%20Docs)]
</div>
**LLM Docstring**

Create or re-enter the pool, create manager-backed communication queues, initialize workers, and establish process-count state.
  - `allow_restart`: `Any`
    > Value supplied for `allow_restart`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.finalize" class="docs-object-method">&nbsp;</a> 
```python
finalize(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1765)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1765?message=Update%20Docs)]
</div>
**LLM Docstring**

Exit the owned pool on the main process and clear communication queues and the cached communicator.
  - `exc_type`: `Any`
    > Value supplied for `exc_type`.
  - `exc_val`: `Any`
    > Value supplied for `exc_val`.
  - `exc_tb`: `Any`
    > Value supplied for `exc_tb`.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.on_main" class="docs-object-method">&nbsp;</a> 
```python
@property
on_main(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1785)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.py#L1785?message=Update%20Docs)]
</div>
**LLM Docstring**

Return `True` when this instance is not marked as a worker.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.


<a id="McUtils.Parallelizers.Parallelizers.MultiprocessingParallelizer.from_config" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_config(cls, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1796)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1796?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a multiprocessing parallelizer directly from keyword options.
  - `kw`: `Any`
    > Value supplied for `kw`.
  - `:returns`: `Any`
    > The value produced by the implementation; see the summary for its exact semantics.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers/Parallelizers/MultiprocessingParallelizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers.py#L1077?message=Update%20Docs)   
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