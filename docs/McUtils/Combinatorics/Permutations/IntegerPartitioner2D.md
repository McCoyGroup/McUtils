## <a id="McUtils.Combinatorics.Permutations.IntegerPartitioner2D">IntegerPartitioner2D</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L1951)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L1951?message=Update%20Docs)]
</div>

Provides a tree-based approach to obtain the different integer partitions possible
when n balls are divided into different numbers of boxes







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
partition_data: dict
```
<a id="McUtils.Combinatorics.Permutations.IntegerPartitioner2D.get_partitions" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_partitions(cls, boxes, balls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2025)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2025?message=Update%20Docs)]
</div>
**LLM Docstring**

Enumerate all ways to distribute `balls` into `boxes` (a 2-D integer partition /
contingency-table enumeration), sorting both descending and undoing the sort on
the result.
  - `boxes`: `np.ndarray`
    > the box capacities
  - `balls`: `np.ndarray`
    > the ball counts
  - `:returns`: `np.ndarray`
    > the enumerated distributions
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Permutations/IntegerPartitioner2D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Permutations/IntegerPartitioner2D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Permutations/IntegerPartitioner2D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Permutations/IntegerPartitioner2D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L1951?message=Update%20Docs)   
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