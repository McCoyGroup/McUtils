## <a id="McUtils.Parallelizers.Parallelizers.SendRecieveParallelizer">SendRecieveParallelizer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers.py#L614)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers.py#L614?message=Update%20Docs)]
</div>

Parallelizer that implements `scatter`, `gather`, `broadcast`, and `map`
based on just having a communicator that supports `send` and `receive methods







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
ReceivedError: ReceivedError
SendReceieveCommunicator: SendReceieveCommunicator
```
<a id="McUtils.Parallelizers.Parallelizers.SendRecieveParallelizer.comm" class="docs-object-method">&nbsp;</a> 
```python
@property
comm(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L671)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L671?message=Update%20Docs)]
</div>
Returns the communicator used by the paralellizer
  - `:returns`: `SendRecieveParallelizer.SendReceieveCommunicator`
    >


<a id="McUtils.Parallelizers.Parallelizers.SendRecieveParallelizer.send" class="docs-object-method">&nbsp;</a> 
```python
send(self, data, loc, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L679)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L679?message=Update%20Docs)]
</div>
Sends data to the process specified by loc
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SendRecieveParallelizer.receive" class="docs-object-method">&nbsp;</a> 
```python
receive(self, data, loc, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L693)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L693?message=Update%20Docs)]
</div>
Receives data from the process specified by loc
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SendRecieveParallelizer.broadcast" class="docs-object-method">&nbsp;</a> 
```python
broadcast(self, data, locs=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L711)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L711?message=Update%20Docs)]
</div>
Sends the same data to all processes
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SendRecieveParallelizer.scatter" class="docs-object-method">&nbsp;</a> 
```python
scatter(self, data, locs=None, return_locs=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L732)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L732?message=Update%20Docs)]
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


<a id="McUtils.Parallelizers.Parallelizers.SendRecieveParallelizer.gather" class="docs-object-method">&nbsp;</a> 
```python
gather(self, data, locs=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L776)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L776?message=Update%20Docs)]
</div>
Performs a gather of data from the different
available parallelizer processes
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SendRecieveParallelizer.map" class="docs-object-method">&nbsp;</a> 
```python
map(self, func, data, extra_args=None, extra_kwargs=None, vectorized=False, aggregate=True, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L816)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L816?message=Update%20Docs)]
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


<a id="McUtils.Parallelizers.Parallelizers.SendRecieveParallelizer.starmap" class="docs-object-method">&nbsp;</a> 
```python
starmap(self, func, data, extra_args=None, extra_kwargs=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L871)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L871?message=Update%20Docs)]
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


<a id="McUtils.Parallelizers.Parallelizers.SendRecieveParallelizer.wait" class="docs-object-method">&nbsp;</a> 
```python
wait(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L904)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.py#L904?message=Update%20Docs)]
</div>
Causes all processes to wait until they've met up at this point.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers/Parallelizers/SendRecieveParallelizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parallelizers/Parallelizers.py#L614?message=Update%20Docs)   
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