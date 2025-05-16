## <a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer">SerialNonParallelizer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers.py#L1685)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers.py#L1685?message=Update%20Docs)]
</div>

Totally serial evaluation for cases where no parallelism
is provide







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.get_nprocs" class="docs-object-method">&nbsp;</a> 
```python
get_nprocs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1691)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1691?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.get_id" class="docs-object-method">&nbsp;</a> 
```python
get_id(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1693)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1693?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.initialize" class="docs-object-method">&nbsp;</a> 
```python
initialize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1696)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1696?message=Update%20Docs)]
</div>
Initializes a parallelizer
if necessary
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.finalize" class="docs-object-method">&nbsp;</a> 
```python
finalize(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1704)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1704?message=Update%20Docs)]
</div>
Finalizes a parallelizer (if necessary)
if necessary
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.on_main" class="docs-object-method">&nbsp;</a> 
```python
@property
on_main(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1712)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1712?message=Update%20Docs)]
</div>
Returns whether or not the executing process is the main
process or not
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.send" class="docs-object-method">&nbsp;</a> 
```python
send(self, data, loc, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1721)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1721?message=Update%20Docs)]
</div>
A no-op
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.receive" class="docs-object-method">&nbsp;</a> 
```python
receive(self, data, loc, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1733)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1733?message=Update%20Docs)]
</div>
A no-op
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.broadcast" class="docs-object-method">&nbsp;</a> 
```python
broadcast(self, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1745)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1745?message=Update%20Docs)]
</div>
A no-op
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.scatter" class="docs-object-method">&nbsp;</a> 
```python
scatter(self, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1757)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1757?message=Update%20Docs)]
</div>
A no-op
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.gather" class="docs-object-method">&nbsp;</a> 
```python
gather(self, data, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1769)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1769?message=Update%20Docs)]
</div>
A no-op
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.map" class="docs-object-method">&nbsp;</a> 
```python
map(self, function, data, extra_args=None, extra_kwargs=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1782)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1782?message=Update%20Docs)]
</div>
Performs a serial map of the function over
the passed data
  - `function`: `Any`
    > 
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.starmap" class="docs-object-method">&nbsp;</a> 
```python
starmap(self, function, data, extra_args=None, extra_kwargs=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1806)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1806?message=Update%20Docs)]
</div>
Performs a serial map with unpacking of the function over
the passed data
  - `function`: `Any`
    > 
  - `data`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, func, *args, comm=None, main_kwargs=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1829)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1829?message=Update%20Docs)]
</div>


<a id="McUtils.Parallelizers.Parallelizers.SerialNonParallelizer.wait" class="docs-object-method">&nbsp;</a> 
```python
wait(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1835)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers/SerialNonParallelizer.py#L1835?message=Update%20Docs)]
</div>
No need to wait when you're in a serial environment
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parallelizers/Parallelizers/SerialNonParallelizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parallelizers/Parallelizers/SerialNonParallelizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parallelizers/Parallelizers/SerialNonParallelizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parallelizers/Parallelizers/SerialNonParallelizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Parallelizers/Parallelizers.py#L1685?message=Update%20Docs)   
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