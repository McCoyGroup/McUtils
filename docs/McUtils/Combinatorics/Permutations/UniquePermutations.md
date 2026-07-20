## <a id="McUtils.Combinatorics.Permutations.UniquePermutations">UniquePermutations</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L694)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L694?message=Update%20Docs)]
</div>

Provides permutations for a _single_ integer partition (very important)
Also provides a classmethod interface to support the case
where we don't want to instantiate a permutations object for every partition







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Combinatorics.Permutations.UniquePermutations.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, partition): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L700)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L700?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up the unique-permutation generator for a multiset partition, sorting the
partition into descending order (recording the sorting/inverse) and computing the
distinct values and their multiplicities.
  - `partition`: `np.ndarray`
    > the multiset (the values to permute)


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.get_permutation_class_counts" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_permutation_class_counts(cls, partition, sort_by_counts=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L725)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L725?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the distinct values of a partition and their multiplicities, sorted by
value (descending) or by count.
  - `partition`: `Any`
    > the multiset partition
  - `sort_by_counts`: `bool`
    > sort by multiplicity rather than by value
  - `:returns`: `tuple`
    > `(values, counts)`


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.num_permutations" class="docs-object-method">&nbsp;</a> 
```python
@property
num_permutations(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/UniquePermutations.py#L748)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/UniquePermutations.py#L748?message=Update%20Docs)]
</div>
Counts the number of unique permutations of the partition
  - `counts`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.get_binoms" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_binoms(cls, n): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L762)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L762?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the cached `Binomial` table, (re)building it if it isn't large enough for
`n`.
  - `n`: `int`
    > the required size
  - `:returns`: `_`
    > the binomial table


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.count_permutations" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
count_permutations(cls, counts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L778)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L778?message=Update%20Docs)]
</div>
Counts the number of unique permutations of the given "counts"
which correspond to the number of nodes in the unique permutation tree
  - `counts`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.permutations" class="docs-object-method">&nbsp;</a> 
```python
permutations(self, initial_permutation=None, return_indices=False, num_perms=None, position_blocks=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/UniquePermutations.py#L808)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/UniquePermutations.py#L808?message=Update%20Docs)]
</div>
Returns the permutations of the input array
  - `initial_permutation`: `Any`
    > 
  - `return_indices`: `Any`
    > 
  - `classes`: `Any`
    > 
  - `counts`: `Any`
    > 
  - `num_perms`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.get_subsequent_permutations" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_subsequent_permutations(cls, initial_permutation, return_indices=False, classes=None, counts=None, num_perms=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L915)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L915?message=Update%20Docs)]
</div>
Returns the permutations of the input array
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.index_permutations" class="docs-object-method">&nbsp;</a> 
```python
index_permutations(self, perms, assume_sorted=False, preserve_ordering=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/UniquePermutations.py#L1097)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/UniquePermutations.py#L1097?message=Update%20Docs)]
</div>
Gets permutations indices assuming all the data matches the held stuff
  - `perms`: `Any`
    > 
  - `assume_sorted`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.get_next_permutation_from_prev" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_next_permutation_from_prev(cls, classes, counts, class_map, ndim, cur, prev, prev_index, prev_dim, subtree_counts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1113)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1113?message=Update%20Docs)]
</div>
Pulls the next index by reusing as much info as possible from
previous index
Less able to be efficient than computing many indices at once so prefer that if
possible
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.get_permutation_indices" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_permutation_indices(cls, perms, classes=None, counts=None, assume_sorted=False, preserve_ordering=True, dim=None, num_permutations=None, dtype=None, block_size=100): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1317)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1317?message=Update%20Docs)]
</div>
Classmethod interface to get indices for permutations
  - `perms`: `Any`
    > 
  - `assume_sorted`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.get_permutations_from_indices" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_permutations_from_indices(cls, classes, counts, indices, assume_sorted=False, preserve_ordering=True, dim=None, num_permutations=None, check_indices=True, no_backtracking=False, block_size=100): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1504)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1504?message=Update%20Docs)]
</div>
Classmethod interface to get permutations given a set of indices
  - `perms`: `Any`
    > 
  - `assume_sorted`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.permutations_from_indices" class="docs-object-method">&nbsp;</a> 
```python
permutations_from_indices(self, indices, assume_sorted=False, preserve_ordering=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/UniquePermutations.py#L1560)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/UniquePermutations.py#L1560?message=Update%20Docs)]
</div>
Gets permutations indices assuming all the data matches the held stuff
  - `perms`: `Any`
    > 
  - `assume_sorted`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.get_standard_permutation" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_standard_permutation(cls, counts, classes): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1575)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1575?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the canonical (sorted, descending) representative permutation for a set of
class counts.
  - `counts`: `np.ndarray`
    > the per-class multiplicities
  - `classes`: `np.ndarray`
    > the distinct values
  - `:returns`: `np.ndarray`
    > the standard permutation


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.walk_permutation_tree" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
walk_permutation_tree(cls, counts, on_visit, indices=None, dim=None, num_permutations=None, include_positions=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1708)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1708?message=Update%20Docs)]
</div>
Just a general purpose method that allows us to walk the permutation
tree built from counts and apply a function every time a node is visited.
This can be very powerful for building algorithms that need to consider every permutation of
an object.
  - `counts`: `Any`
    > 
  - `on_visit`: `Any`
    > 
  - `indices`: `Any`
    > 
  - `dim`: `Any`
    > 
  - `num_permutations`: `Any`
    > 
  - `include_positions`: `Any`
    >


<a id="McUtils.Combinatorics.Permutations.UniquePermutations.descend_permutation_tree_indices" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
descend_permutation_tree_indices(cls, perms, on_visit, classes=None, counts=None, dim=None, assume_sorted=False, num_permutations=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1834)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1834?message=Update%20Docs)]
</div>
Not sure what to call this exactly, but given that `walk_permutation_tree` maps onto `permutations_from_indices`
this is the counterpart that basically walks _down_ the way `permutation_indices` would.
I guess this is basically a BFS type approach of something?
  - `perms`: `Any`
    > 
  - `assume_sorted`: `Any`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Permutations/UniquePermutations.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Permutations/UniquePermutations.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Permutations/UniquePermutations.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Permutations/UniquePermutations.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L694?message=Update%20Docs)   
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