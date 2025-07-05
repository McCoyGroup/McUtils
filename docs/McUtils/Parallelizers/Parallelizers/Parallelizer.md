## <a id="McUtils.Parallelizers.Parallelizers.Parallelizer">Parallelizer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers.py#L47?message=Update%20Docs)]
</div>

Abstract base class to help manage parallelism.
Provides the basic API that all parallelizers can be expected
to conform to.
Provides effectively the union of operations supported by
`mp.Pool` and `MPI`.
There is also the ability to lookup and register 'named'
parallelizers, since we expect a single program to not
really use more than one.
This falls back gracefully to the serial case.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_printer: builtin_function_or_method
base_log_level: LogLevel
Backends: Backends
parallelizer_dispatch: NoneType
InMainProcess: InMainProcess
InWorkerProcess: InWorkerProcess
mode_map: dict
```
<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, logger=None, contract=None, uid=None, initialization_function=None, initialization_args=None, initialization_kwargs=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers.py#L68)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers.py#L68?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.load_registry" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_registry(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L101?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.parallelizer_registry" class="docs-object-method">&nbsp;</a> 
```python
@property
parallelizer_registry(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L106?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.get_default" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_default(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L110?message=Update%20Docs)]
</div>
For compat.
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.get_paralellizer_types" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_paralellizer_types(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L123)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L123?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.lookup" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lookup(cls, key, construct=True) -> 'Parallelizer': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L131)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L131?message=Update%20Docs)]
</div>
Checks in the registry to see if a given parallelizer is there
otherwise returns a `SerialNonParallelizer`.
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.register" class="docs-object-method">&nbsp;</a> 
```python
register(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L167)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L167?message=Update%20Docs)]
</div>
Checks in the registry to see if a given parallelizer is there
otherwise returns a `SerialNonParallelizer`.
  - `key`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.active" class="docs-object-method">&nbsp;</a> 
```python
@property
active(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L178)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L178?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.set_initializer" class="docs-object-method">&nbsp;</a> 
```python
set_initializer(self, func, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L182)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L182?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.initialize" class="docs-object-method">&nbsp;</a> 
```python
initialize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L193)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L193?message=Update%20Docs)]
</div>
Initializes a parallelizer
if necessary
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.finalize" class="docs-object-method">&nbsp;</a> 
```python
finalize(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L202)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L202?message=Update%20Docs)]
</div>
Finalizes a parallelizer (if necessary)
if necessary
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L212?message=Update%20Docs)]
</div>
Allows the parallelizer context to be set
using `with`
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L228)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L228?message=Update%20Docs)]
</div>
Allows the parallelizer context to be unset
using `with`
  - `exc_type`: `Any`
    > 
  - `exc_val`: `Any`
    > 
  - `exc_tb`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.on_main" class="docs-object-method">&nbsp;</a> 
```python
@property
on_main(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L264)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L264?message=Update%20Docs)]
</div>
Returns whether or not the executing process is the main
process or not
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.main_restricted" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
main_restricted(func): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L274)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L274?message=Update%20Docs)]
</div>
A decorator to indicate that a function should only be
run when on the main process
  - `func`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.worker_restricted" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
worker_restricted(func): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L296)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L296?message=Update%20Docs)]
</div>
A decorator to indicate that a function should only be
run when on a worker process
  - `func`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.send" class="docs-object-method">&nbsp;</a> 
```python
send(self, data, loc, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L326)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L326?message=Update%20Docs)]
</div>
Sends data to the process specified by loc
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.receive" class="docs-object-method">&nbsp;</a> 
```python
receive(self, data, loc, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L339)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L339?message=Update%20Docs)]
</div>
Receives data from the process specified by loc
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.broadcast" class="docs-object-method">&nbsp;</a> 
```python
broadcast(self, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L352)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L352?message=Update%20Docs)]
</div>
Sends the same data to all processes
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.scatter" class="docs-object-method">&nbsp;</a> 
```python
scatter(self, data, locs=None, return_locs=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L365)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L365?message=Update%20Docs)]
</div>
Performs a scatter of data to the different
available parallelizer processes.
*NOTE:* unlike in the MPI case, `data` does not
need to be evenly divisible by the number of available
processes
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.gather" class="docs-object-method">&nbsp;</a> 
```python
gather(self, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L382)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L382?message=Update%20Docs)]
</div>
Performs a gather of data from the different
available parallelizer processes
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.map" class="docs-object-method">&nbsp;</a> 
```python
map(self, function, data, extra_args=None, extra_kwargs=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L401)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L401?message=Update%20Docs)]
</div>
Performs a parallel map of function over
the held data on different processes
  - `function`: `Any`
    > 
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.starmap" class="docs-object-method">&nbsp;</a> 
```python
starmap(self, function, data, extra_args=None, extra_kwargs=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L418)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L418?message=Update%20Docs)]
</div>
Performs a parallel map with unpacking of function over
the held data on different processes
  - `function`: `Any`
    > 
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, func, *args, main_kwargs=None, cleanup=True, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L436)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L436?message=Update%20Docs)]
</div>
Runs the callable `func` in parallel
  - `func`: `Any`
    > 
  - `args`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.run" class="docs-object-method">&nbsp;</a> 
```python
run(self, func, *args, comm=None, main_kwargs=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L451)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L451?message=Update%20Docs)]
</div>
Calls `apply`, but makes sure state is handled cleanly
  - `func`: `Any`
    > 
  - `args`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.from_config" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_config(cls, mode=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L469)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L469?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.nprocs" class="docs-object-method">&nbsp;</a> 
```python
@property
nprocs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L485)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L485?message=Update%20Docs)]
</div>
Returns the number of processes the parallelizer has
to work with
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.get_nprocs" class="docs-object-method">&nbsp;</a> 
```python
get_nprocs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L494)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L494?message=Update%20Docs)]
</div>
Returns the number of processes
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.id" class="docs-object-method">&nbsp;</a> 
```python
@property
id(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L502)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L502?message=Update%20Docs)]
</div>
Returns some form of identifier for the current process
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.pid" class="docs-object-method">&nbsp;</a> 
```python
@property
pid(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L510)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L510?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.get_id" class="docs-object-method">&nbsp;</a> 
```python
get_id(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L515)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L515?message=Update%20Docs)]
</div>
Returns the id for the current process
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.printer" class="docs-object-method">&nbsp;</a> 
```python
@property
printer(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L524)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L524?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.main_print" class="docs-object-method">&nbsp;</a> 
```python
main_print(self, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L533)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L533?message=Update%20Docs)]
</div>
Prints from the main process
  - `args`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.worker_print" class="docs-object-method">&nbsp;</a> 
```python
worker_print(self, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L544)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L544?message=Update%20Docs)]
</div>
Prints from a main worker process
  - `args`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.print" class="docs-object-method">&nbsp;</a> 
```python
print(self, *args, where='both', **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L555)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L555?message=Update%20Docs)]
</div>
An implementation of print that operates differently on workers than on main
processes
  - `args`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.wait" class="docs-object-method">&nbsp;</a> 
```python
wait(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L574)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L574?message=Update%20Docs)]
</div>
Causes all processes to wait until they've met up at this point.
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L583)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L583?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.Parallelizer.share" class="docs-object-method">&nbsp;</a> 
```python
share(self, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L594)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/Parallelizer.py#L594?message=Update%20Docs)]
</div>
Converts `obj` into a form that can be cleanly used with shared memory via a `SharedObjectManager`
  - `obj`: `Any`
    > 
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers/Parallelizers/Parallelizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers/Parallelizers/Parallelizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers/Parallelizers/Parallelizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers/Parallelizers/Parallelizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers.py#L47?message=Update%20Docs)   
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