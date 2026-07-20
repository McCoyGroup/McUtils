## <a id="McUtils.Combinatorics.Permutations.SymmetricGroupGenerator">SymmetricGroupGenerator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L2716)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L2716?message=Update%20Docs)]
</div>

I don't know what to call this.
Manages elements of the symmetric group up to arbitrary size.
Basically just exists to merge all of the prior integer partition/permutation stuff over many integers
which makes it easier to calculate direct products of terms







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
direct_sum_filter: direct_sum_filter
```
<a id="McUtils.Combinatorics.Permutations.SymmetricGroupGenerator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, dim): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L2724)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L2724?message=Update%20Docs)]
</div>

  - `dim`: `int`
    > the padding length of every term (needed for consistency reasons)


<a id="McUtils.Combinatorics.Permutations.SymmetricGroupGenerator.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2735)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2735?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the dimension.
  - `:returns`: `str`
    > the representation


<a id="McUtils.Combinatorics.Permutations.SymmetricGroupGenerator.load_to_size" class="docs-object-method">&nbsp;</a> 
```python
load_to_size(self, size): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2780)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2780?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate partition permutations until the cumulative element count covers `size`.
  - `size`: `int`
    > the target cumulative size


<a id="McUtils.Combinatorics.Permutations.SymmetricGroupGenerator.get_terms" class="docs-object-method">&nbsp;</a> 
```python
get_terms(self, n, flatten=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2793)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2793?message=Update%20Docs)]
</div>
Returns permutations of partitions
  - `n`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.SymmetricGroupGenerator.num_terms" class="docs-object-method">&nbsp;</a> 
```python
num_terms(self, n): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2810)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2810?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the number of partition permutations at each requested integer sum.
  - `n`: `Any`
    > the integer sum(s)
  - `:returns`: `list`
    > the per-sum element counts


<a id="McUtils.Combinatorics.Permutations.SymmetricGroupGenerator.to_indices" class="docs-object-method">&nbsp;</a> 
```python
to_indices(self, perms, sums=None, assume_sorted=False, assume_standard=False, check_partition_counts=True, preserve_ordering=True, dtype=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2825)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2825?message=Update%20Docs)]
</div>
Gets the indices for the given permutations.
First splits by sum then allows the held integer partitioners to do the rest
  - `perms`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.SymmetricGroupGenerator.from_indices" class="docs-object-method">&nbsp;</a> 
```python
from_indices(self, indices, assume_sorted=False, preserve_ordering=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2886)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L2886?message=Update%20Docs)]
</div>
Gets the permutations for the given indices.
First splits into by which integer partitioner is the generator and lets
the partitioner do the rest
  - `perms`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.SymmetricGroupGenerator.changed_index_number" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
changed_index_number(cls, idx, radix): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3280)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3280?message=Update%20Docs)]
</div>
**LLM Docstring**

Encode a set of changed positions as a single mixed-radix integer (a canonical id
for which positions changed).
  - `idx`: `Any`
    > the changed positions
  - `radix`: `int`
    > the radix (dimension)
  - `:returns`: `int`
    > the encoded number


<a id="McUtils.Combinatorics.Permutations.SymmetricGroupGenerator.get_equivalence_classes" class="docs-object-method">&nbsp;</a> 
```python
get_equivalence_classes(self, perms, sums=None, assume_sorted=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L3684)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L3684?message=Update%20Docs)]
</div>
Gets permutation equivalence classes
  - `perms`: `Any`
    > 
  - `sums`: `Any`
    > 
  - `assume_sorted`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.SymmetricGroupGenerator.take_permutation_rule_direct_sum" class="docs-object-method">&nbsp;</a> 
```python
take_permutation_rule_direct_sum(self, perms, rules, sums=None, assume_sorted=False, return_indices=False, return_excitations=True, return_change_positions=False, full_basis=None, split_results=False, excluded_permutations=None, filter_perms=None, filter_negatives=True, return_filter=False, preserve_ordering=True, indexing_method='direct', logger=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L3738)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.py#L3738?message=Update%20Docs)]
</div>
Applies `rules` to perms.
Naively this is just taking every possible permutation of the rules padded to
get to the appropriate length and then adding that to every element in perms
and then taking the unique ones.
We can be more intelligent about how we do this, though, first reducing perms to
equivalence classes as integer partitions and then making use of that to
minimize the number of operations we need to do while also ensuring sorting
  - `perms`: `Any`
    > 
  - `rules`: `Any`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Permutations/SymmetricGroupGenerator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L2716?message=Update%20Docs)   
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