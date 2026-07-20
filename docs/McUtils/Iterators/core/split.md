# <a id="McUtils.Iterators.core.split">split</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Iterators/core.py#L96)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L96?message=Update%20Docs)]
</div>

```python
split(a, test=None): 
```
**LLM Docstring**

Split an iterable whenever adjacent values satisfy a boundary test.

For non-fixed iterables, the function tees the input, compares successive values, and yields materialized groups; when `test` is omitted it splits when adjacent values differ. The fixed-size branch directly uses slicing, but its loop is written as `for i, b in a[1]` rather than enumerating `a[1:]`, and it calls `test` without installing the default, so that branch only works for unusually shaped inputs matching that unpacking behavior.
  - `a`: `collections.abc.Iterable`
    > Iterable to partition.
  - `test`: `callable | None`
    > Predicate receiving `(next_value, previous_group_value)` and returning true at a split boundary.
  - `:returns`: `collections.abc.Iterator`
    > Iterator over contiguous groups.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Iterators/core/split.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Iterators/core/split.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Iterators/core/split.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Iterators/core/split.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L96?message=Update%20Docs)   
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