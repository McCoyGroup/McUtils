## <a id="McUtils.Combinatorics.Permutations.IntegerPartitionPermutations">IntegerPartitionPermutations</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L2313)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L2313?message=Update%20Docs)]
</div>

Provides tools for working with permutations of a given integer partition







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Combinatorics.Permutations.IntegerPartitionPermutations.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, num, dim=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L2317)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L2317?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up the space of all permutations of every integer partition of `num`
(optionally padded to a fixed dimension), precomputing each partition's class
counts.
  - `num`: `int`
    > the integer being partitioned
  - `dim`: `int | None`
    > the (padded) permutation length (defaults to `num`)


<a id="McUtils.Combinatorics.Permutations.IntegerPartitionPermutations.num_elements" class="docs-object-method">&nbsp;</a> 
```python
@property
num_elements(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2356)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2356?message=Update%20Docs)]
</div>
**LLM Docstring**

The total number of partition permutations in the space.
  - `:returns`: `int`
    > the number of elements


<a id="McUtils.Combinatorics.Permutations.IntegerPartitionPermutations.get_partition_permutations" class="docs-object-method">&nbsp;</a> 
```python
get_partition_permutations(self, return_indices=False, dtype=None, flatten=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2368)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2368?message=Update%20Docs)]
</div>

  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.IntegerPartitionPermutations.get_full_equivalence_class_data" class="docs-object-method">&nbsp;</a> 
```python
get_full_equivalence_class_data(self, perms, split_method='direct', assume_sorted=False, assume_standard=False, return_permutations=False, check_partition_counts=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2440)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2440?message=Update%20Docs)]
</div>
Returns the equivalence class data of the given permutations
  - `perms`: `Any`
    > 
  - `split_method`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.IntegerPartitionPermutations.get_equivalence_classes" class="docs-object-method">&nbsp;</a> 
```python
get_equivalence_classes(self, perms, split_method='direct', assume_sorted=False, return_permutations=True, check_partition_counts=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2473)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2473?message=Update%20Docs)]
</div>
Returns the equivalence classes and permutations of the given permutations
  - `perms`: `Any`
    > 
  - `split_method`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.IntegerPartitionPermutations.get_partition_permutation_indices" class="docs-object-method">&nbsp;</a> 
```python
get_partition_permutation_indices(self, perms, assume_sorted=False, preserve_ordering=True, assume_standard=False, check_partition_counts=True, dtype=None, split_method='direct'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2497)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2497?message=Update%20Docs)]
</div>
Assumes the perms all add up to the stored int
They're then grouped by partition index and finally
Those are indexed
  - `perms`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.IntegerPartitionPermutations.get_partition_permutations_from_indices" class="docs-object-method">&nbsp;</a> 
```python
get_partition_permutations_from_indices(self, indices, assume_sorted=False, preserve_ordering=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2560)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2560?message=Update%20Docs)]
</div>
Assumes the perms all add up to the stored int
They're then grouped by partition index and finally
Those are indexed
  - `perms`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.IntegerPartitionPermutations.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2605)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.py#L2605?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the integer, dimension, and element count.
  - `:returns`: `str`
    > the representation
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Permutations/IntegerPartitionPermutations.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L2313?message=Update%20Docs)   
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