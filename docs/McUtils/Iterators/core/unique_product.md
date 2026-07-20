# <a id="McUtils.Iterators.core.unique_product">unique_product</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Iterators/core.py#L446)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L446?message=Update%20Docs)]
</div>

```python
unique_product(*iterables, key=None, filter=None): 
```
**LLM Docstring**

Generate Cartesian-product tuples subject to a uniqueness filter.

A depth-first deque traversal builds one value from each input. By default, a candidate is accepted only when it is not already present in the partial tuple; when `key` is supplied, uniqueness is checked on accumulated keys instead. Mapping-like inputs are explicitly converted with `iter`, which still iterates their keys. Indexable inputs are accessed by index. Non-indexable iterators are cached as values are discovered; the cached-value branch contains the condition `n + 1 < m` while `m` is negative, so previously cached later positions are not requeued through that branch.
  - `iterables`: `collections.abc.Iterable`
    > Input collections contributing one value each.
  - `key`: `callable | None`
    > Optional function mapping candidates to uniqueness keys.
  - `filter`: `callable | None`
    > Predicate receiving the partial tuple or key tuple and a candidate; defaults to rejecting repeats.
  - `:returns`: `collections.abc.Iterator[tuple]`
    > Iterator over accepted product tuples.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Iterators/core/unique_product.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Iterators/core/unique_product.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Iterators/core/unique_product.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Iterators/core/unique_product.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L446?message=Update%20Docs)   
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