# <a id="McUtils.Combinatorics.Sequences.prime_list">prime_list</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Sequences.py#L210)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L210?message=Update%20Docs)]
</div>

```python
prime_list(n, base_primes=[], piter=<generator object prime_iter at 0x7f4f8018e4a0>): 
```
**LLM Docstring**

Return the first `n` primes using a shared incremental cache.

The default `base_primes` list and `piter` generator are intentionally persistent across calls. The cache is extended until the iterator yields more than `n` entries, then the first `n` values are returned.
  - `n`: `int`
    > number of primes requested
  - `base_primes`: `list[int]`
    > mutable cache populated in place
  - `piter`: `collections.abc.Iterator[list[int]]`
    > cumulative prime-list iterator used to extend the cache
  - `:returns`: `list[int]`
    > the first `n` cached primes











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Sequences/prime_list.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Sequences/prime_list.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Sequences/prime_list.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Sequences/prime_list.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L210?message=Update%20Docs)   
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