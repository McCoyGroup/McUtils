## <a id="McUtils.Combinatorics.Permutations.UniqueSubsets">UniqueSubsets</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L593)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L593?message=Update%20Docs)]
</div>

Provides unique subsets for an integer partition







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Combinatorics.Permutations.UniqueSubsets.num_unique_subsets" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
num_unique_subsets(cls, k, partition): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L598)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L598?message=Update%20Docs)]
</div>
**LLM Docstring**

Count the number of ways to split `k` symbols into ordered blocks of the given
sizes (a product of binomial coefficients).
  - `k`: `int`
    > the total number of symbols
  - `partition`: `Any`
    > the block sizes
  - `:returns`: `int`
    > the number of unique subset-splittings


<a id="McUtils.Combinatorics.Permutations.UniqueSubsets.unique_subsets" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
unique_subsets(cls, partition): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L618)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L618?message=Update%20Docs)]
</div>
**LLM Docstring**

Enumerate every way to partition `sum(partition)` symbols into ordered blocks of
the given sizes, returning them as rows of a storage array (built breadth-first
via a work queue).
  - `partition`: `Any`
    > the block sizes
  - `:returns`: `np.ndarray`
    > the enumerated subset-splittings
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Permutations/UniqueSubsets.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Permutations/UniqueSubsets.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Permutations/UniqueSubsets.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Permutations/UniqueSubsets.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L593?message=Update%20Docs)   
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