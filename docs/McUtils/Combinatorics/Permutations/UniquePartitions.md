## <a id="McUtils.Combinatorics.Permutations.UniquePartitions">UniquePartitions</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L2068)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L2068?message=Update%20Docs)]
</div>

Takes partitions of a set of ints with ordering







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Combinatorics.Permutations.UniquePartitions.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, partition): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L2072)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L2072?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up the unique-partition generator for a multiset, precomputing its unique
permutations and the per-value "follower" table used to enumerate ordered
splittings.
  - `partition`: `np.ndarray`
    > the multiset to partition


<a id="McUtils.Combinatorics.Permutations.UniquePartitions.partitions" class="docs-object-method">&nbsp;</a> 
```python
partitions(self, sizes, take_unique=True, split=True, return_partitions=True, return_indices=False, split_indices=None, return_inverse=False, split_inverse=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/UniquePartitions.py#L2244)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/UniquePartitions.py#L2244?message=Update%20Docs)]
</div>
**LLM Docstring**

Enumerate the ways to split this multiset into blocks of the given sizes (a
front-end to `_take_partitions`).
  - `sizes`: `Any`
    > the block sizes (must sum to the partition length)
  - `take_unique`: `bool`
    > deduplicate the splittings
  - `split`: `bool`
    > split the result per block
  - `return_partitions`: `bool`
    > return the partition values
  - `return_indices`: `bool`
    > return the selection indices
  - `split_indices`: `Any`
    > split the indices per block
  - `return_inverse`: `bool`
    > return the inverse mapping
  - `split_inverse`: `Any`
    > split the inverse per block
  - `:returns`: `_`
    > the requested partitions/indices/inverse
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Permutations/UniquePartitions.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Permutations/UniquePartitions.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Permutations/UniquePartitions.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Permutations/UniquePartitions.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L2068?message=Update%20Docs)   
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