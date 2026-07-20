# <a id="McUtils.Iterators.core.take_lists">take_lists</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Iterators/core.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L175?message=Update%20Docs)]
</div>

```python
take_lists(a, splits): 
```
**LLM Docstring**

Partition an iterable according to a sequence of requested lengths.

Fixed-size inputs are sliced without copying where the input type supports that operation. After the requested lengths, a trailing slice is yielded only when `sep < len(a) - 1`, which omits a remainder containing exactly one item. Streaming inputs yield one materialized list per requested size and do not emit any unspecified remainder.
  - `a`: `collections.abc.Iterable`
    > Sequence or iterator to partition.
  - `splits`: `collections.abc.Iterable[int]`
    > Requested chunk lengths.
  - `:returns`: `collections.abc.Iterator`
    > Iterator over slices or consumed lists.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Iterators/core/take_lists.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Iterators/core/take_lists.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Iterators/core/take_lists.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Iterators/core/take_lists.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L175?message=Update%20Docs)   
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