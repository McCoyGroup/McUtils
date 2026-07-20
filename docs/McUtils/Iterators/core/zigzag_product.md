# <a id="McUtils.Iterators.core.zigzag_product">zigzag_product</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Iterators/core.py#L527)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L527?message=Update%20Docs)]
</div>

```python
zigzag_product(*iterables, iterator_lengths=None, return_index=False): 
```
**LLM Docstring**

Enumerate a Cartesian product while reversing selected axes to create a serpentine order.

Inputs are materialized, optionally taking only the supplied `iterator_lengths`. As the ordinary multi-index advances, axis-direction flags are toggled when trailing indices reset to zero.
  - `iterables`: `collections.abc.Iterable`
    > Input iterables forming the Cartesian product.
  - `iterator_lengths`: `collections.abc.Iterable[int | None] | None`
    > Optional lengths used both to limit materialization and reflect indices.
  - `return_index`: `bool`
    > Whether to yield each value tuple together with its selected index tuple.
  - `:returns`: `collections.abc.Iterator`
    > Iterator over value tuples or `(values, indices)` pairs.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Iterators/core/zigzag_product.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Iterators/core/zigzag_product.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Iterators/core/zigzag_product.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Iterators/core/zigzag_product.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L527?message=Update%20Docs)   
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