## <a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer">MPIParallelizer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers.py#L1266)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers.py#L1266?message=Update%20Docs)]
</div>

Parallelizes using `mpi4py`







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
MPICommunicator: MPICommunicator
```
<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, root=0, comm=None, contract=None, logger=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1557)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1557?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.get_nprocs" class="docs-object-method">&nbsp;</a> 
```python
get_nprocs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1570)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1570?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.get_id" class="docs-object-method">&nbsp;</a> 
```python
get_id(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1572)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1572?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.initialize" class="docs-object-method">&nbsp;</a> 
```python
initialize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1575)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1575?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.finalize" class="docs-object-method">&nbsp;</a> 
```python
finalize(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1578)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1578?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.comm" class="docs-object-method">&nbsp;</a> 
```python
@property
comm(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1582)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1582?message=Update%20Docs)]
</div>
Returns the communicator used by the paralellizer
  - `:returns`: `MPIParallelizer.MPICommunicator`
    >


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.on_main" class="docs-object-method">&nbsp;</a> 
```python
@property
on_main(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1591)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1591?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.broadcast" class="docs-object-method">&nbsp;</a> 
```python
broadcast(self, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1595)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1595?message=Update%20Docs)]
</div>
Sends the same data to all processes
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.scatter" class="docs-object-method">&nbsp;</a> 
```python
scatter(self, data, shape=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1610)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1610?message=Update%20Docs)]
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


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.gather" class="docs-object-method">&nbsp;</a> 
```python
gather(self, data, shape=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1629)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1629?message=Update%20Docs)]
</div>
Performs a gather of data from the different
available parallelizer processes
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.map" class="docs-object-method">&nbsp;</a> 
```python
map(self, func, data, input_shape=None, output_shape=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1645)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1645?message=Update%20Docs)]
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


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, func, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1663)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/MPIParallelizer.py#L1663?message=Update%20Docs)]
</div>
Applies func to args in parallel on all of the processes.
For MPI, since jobs are always started with mpirun, this
is just a regular apply
  - `func`: `Any`
    > 
  - `args`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.MPIParallelizer.from_config" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_config(cls, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L1680)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L1680?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers/Parallelizers/MPIParallelizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers/Parallelizers/MPIParallelizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers/Parallelizers/MPIParallelizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers/Parallelizers/MPIParallelizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers.py#L1266?message=Update%20Docs)   
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