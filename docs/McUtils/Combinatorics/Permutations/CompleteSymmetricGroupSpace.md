## <a id="McUtils.Combinatorics.Permutations.CompleteSymmetricGroupSpace">CompleteSymmetricGroupSpace</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L4230)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L4230?message=Update%20Docs)]
</div>

An object representing a full integer partition-permutation basis
which will work nominally at any level of excitation







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
permutation_dtype: str
```
<a id="McUtils.Combinatorics.Permutations.CompleteSymmetricGroupSpace.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, dim, memory_constrained=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L4237)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L4237?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up the complete symmetric-group space of a given dimension, backed by a
`SymmetricGroupGenerator` and a contracted (byte-packed) permutation dtype for
fast lookups.
  - `dim`: `int`
    > the permutation length
  - `memory_constrained`: `bool`
    > avoid materializing the full basis (compute on demand)


<a id="McUtils.Combinatorics.Permutations.CompleteSymmetricGroupSpace.dim" class="docs-object-method">&nbsp;</a> 
```python
@property
dim(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4256)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4256?message=Update%20Docs)]
</div>
**LLM Docstring**

The permutation length.
  - `:returns`: `int`
    > the dimension


<a id="McUtils.Combinatorics.Permutations.CompleteSymmetricGroupSpace.__getstate__" class="docs-object-method">&nbsp;</a> 
```python
__getstate__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4268)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4268?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the picklable state (just the dimension; the basis is regenerated).
  - `:returns`: `dict`
    > the state dict


<a id="McUtils.Combinatorics.Permutations.CompleteSymmetricGroupSpace.__setstate__" class="docs-object-method">&nbsp;</a> 
```python
__setstate__(self, state): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4278)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4278?message=Update%20Docs)]
</div>
**LLM Docstring**

Rebuild the space from its pickled state (reinitializing from the dimension).
  - `state`: `dict`
    > the state dict


<a id="McUtils.Combinatorics.Permutations.CompleteSymmetricGroupSpace.load_to_size" class="docs-object-method">&nbsp;</a> 
```python
load_to_size(self, size): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4309)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4309?message=Update%20Docs)]
</div>
**LLM Docstring**

Materialize the basis until it holds at least `size` permutations (a no-op when
memory-constrained).
  - `size`: `int`
    > the target basis size
  - `:returns`: `bool | None`
    > `True` if memory-constrained (nothing loaded)


<a id="McUtils.Combinatorics.Permutations.CompleteSymmetricGroupSpace.load_to_sum" class="docs-object-method">&nbsp;</a> 
```python
load_to_sum(self, max_sum): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4343)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4343?message=Update%20Docs)]
</div>
**LLM Docstring**

Materialize the basis to cover every permutation with sum up to `max_sum`.
  - `max_sum`: `int`
    > the maximum permutation sum


<a id="McUtils.Combinatorics.Permutations.CompleteSymmetricGroupSpace.take" class="docs-object-method">&nbsp;</a> 
```python
take(self, item, uncoerce=False, max_size=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4355)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4355?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the permutation(s) at the given index/indices, loading the basis as needed
(or generating them directly when memory-constrained), optionally un-packing the
contracted dtype.
  - `item`: `Any`
    > the index or indices
  - `uncoerce`: `bool`
    > un-pack the contracted dtype back to the original
  - `max_size`: `int | None`
    > an explicit max index to load to
  - `:returns`: `np.ndarray`
    > the permutation(s)


<a id="McUtils.Combinatorics.Permutations.CompleteSymmetricGroupSpace.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4396)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4396?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the permutation(s) at the given index/indices (delegates to `take`).
  - `item`: `Any`
    > the index or indices
  - `:returns`: `np.ndarray`
    > the permutation(s)


<a id="McUtils.Combinatorics.Permutations.CompleteSymmetricGroupSpace.find" class="docs-object-method">&nbsp;</a> 
```python
find(self, perms, check_sums=True, max_sum=None, search_space_sorting=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4408)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.py#L4408?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the indices of the given permutations in the space, pre-screening by
permutation sum and using the contracted-dtype sorted basis for fast lookup (or
the generator directly when memory-constrained).
  - `perms`: `np.ndarray`
    > the permutations to locate
  - `check_sums`: `bool`
    > pre-screen (and load) by permutation sum
  - `max_sum`: `int | None`
    > an explicit max sum to load to
  - `search_space_sorting`: `Any`
    > a precomputed basis sorting to reuse
  - `:returns`: `np.ndarray`
    > the indices
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Permutations/CompleteSymmetricGroupSpace.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L4230?message=Update%20Docs)   
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