## <a id="McUtils.Parsers.StorageBackends.GrowthPolicy">GrowthPolicy</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends.py#L121)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L121?message=Update%20Docs)]
</div>

Controls amortized growth for dynamically-sized backends.

Pulled out of the resize code so "growth is amortized" is something a
test can assert directly (`next_capacity` called N times should touch
O(log N) distinct capacities) rather than something you have to trust
from reading several cooperating methods.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
initial_capacity: int
growth_factor: float
min_growth: int
```
<a id="McUtils.Parsers.StorageBackends.GrowthPolicy.next_capacity" class="docs-object-method">&nbsp;</a> 
```python
next_capacity(self, current_capacity: 'int', required: 'int') -> 'int': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/GrowthPolicy.py#L135)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/GrowthPolicy.py#L135?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.__create_fn__.<locals>.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, initial_capacity: 'int' = 64, growth_factor: 'float' = 1.7, min_growth: 'int' = 8) -> None: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/__create_fn__.py#L)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/__create_fn__.py#L?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.__create_fn__.<locals>.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/__create_fn__/<locals>.py#L363)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/__create_fn__/<locals>.py#L363?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.__create_fn__.<locals>.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/__create_fn__/<locals>.py#L)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/__create_fn__/<locals>.py#L?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/StorageBackends/GrowthPolicy.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/StorageBackends/GrowthPolicy.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/StorageBackends/GrowthPolicy.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/StorageBackends/GrowthPolicy.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L121?message=Update%20Docs)   
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