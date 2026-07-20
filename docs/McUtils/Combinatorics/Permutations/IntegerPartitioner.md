## <a id="McUtils.Combinatorics.Permutations.IntegerPartitioner">IntegerPartitioner</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L170)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L170?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Combinatorics.Permutations.IntegerPartitioner.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L172)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L172?message=Update%20Docs)]
</div>
**LLM Docstring**

Singleton class: instantiation is disallowed (use the classmethods).


<a id="McUtils.Combinatorics.Permutations.IntegerPartitioner.count_partitions" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
count_partitions(cls, n, M=None, l=None, manage_counts=True, check=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L254)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L254?message=Update%20Docs)]
</div>
Uses the recurrence relation written out here
https://en.wikipedia.org/wiki/Partition_(number_theory)#Partitions_in_a_rectangle_and_Gaussian_binomial_coefficients
We cache the terms as a 2D list-of-lists because we don't need this
part of the code to be blazingly fast but would like repeats to not
do unnecessary work (and because the memory cost is small...)
  - `n`: `Any`
    > 
  - `M`: `Any`
    > 
  - `l`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.IntegerPartitioner.fill_counts" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fill_counts(cls, n, M=None, l=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L362)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L362?message=Update%20Docs)]
</div>
Fills all counts up to (n, M, l)
  - `n`: `int`
    > 
  - `M`: `Any`
    > 
  - `l`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.IntegerPartitioner.count_exact_length_partitions" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
count_exact_length_partitions(cls, n, M, l, check=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L389)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L389?message=Update%20Docs)]
</div>
Unexpectedly common thing to want and a non-obvious formula
  - `n`: `Any`
    > 
  - `M`: `Any`
    > 
  - `l`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.IntegerPartitioner.count_exact_length_partitions_in_range" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
count_exact_length_partitions_in_range(cls, n, m, M, l, check=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L405)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L405?message=Update%20Docs)]
</div>
Returns the partitions with  k > M but length exactly L
  - `n`: `Any`
    > 
  - `M`: `Any`
    > 
  - `l`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.IntegerPartitioner.partitions" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
partitions(cls, n, pad=False, return_lens=False, max_len=None, dtype=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L428)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L428?message=Update%20Docs)]
</div>
Returns partitions in descending lexicographic order
Adapted from Kelleher to return terms ordered by length and then second in descending
lex order which while a computationally suboptimal is very natural for a mapping onto
physical phenomena (and also it's easier for storage)
  - `n`: `int`
    > integer to partition
  - `return_len`: `Any`
    > whether to return the length or not
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.IntegerPartitioner.partition_indices" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
partition_indices(cls, parts, sums=None, counts=None, check=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L528)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L528?message=Update%20Docs)]
</div>
Provides a somewhat quick way to get the index of a set of
integer partitions.
Parts must be padded so that all parts are the same length.
If the sums of the partitions are known ahead of time they may be passed
Similarly if the numbers of non-zero elements in the partitions are known
ahead of time they may _also_ be passed
  - `parts`: `np.ndarray`
    > 
  - `sums`: `np.ndarray`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Permutations/IntegerPartitioner.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Permutations/IntegerPartitioner.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Permutations/IntegerPartitioner.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Permutations/IntegerPartitioner.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L170?message=Update%20Docs)   
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